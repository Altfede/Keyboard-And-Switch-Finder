/**
 * Results page logic
 */

const API_BASE = '/api';
let resultsData = null;
let sessionId = null;

document.addEventListener('DOMContentLoaded', () => {
    sessionId = localStorage.getItem('sessionId');
    const resultsJson = localStorage.getItem('results');

    if (!resultsJson || !sessionId) {
        alert('Nessun risultato trovato. Torna alla home.');
        window.location.href = '/';
        return;
    }

    resultsData = JSON.parse(resultsJson);
    renderResults();
    loadSessionSummary();
});

function renderResults() {
    if (!resultsData || !resultsData.results || resultsData.results.length === 0) {
        document.getElementById('mainResult').innerHTML = '<p>Nessun risultato trovato</p>';
        return;
    }

    // Main result (first one)
    const main = resultsData.results[0];
    renderMainResult(main);

    // Alternatives (rest)
    if (resultsData.results.length > 1) {
        renderAlternatives(resultsData.results.slice(1));
    }
}

function renderMainResult(result) {
    const product = result.product;
    const mode = resultsData.mode;

    let html = `
        <div class="result-card main-card">
            <div class="badge badge-success">✨ Scelta Principale</div>
            <h2>${product.name}</h2>
            <p class="brand">${product.brand}</p>

            <div class="score-section">
                <div class="score-badge">
                    <span class="score-value">${(result.score * 100).toFixed(0)}</span>
                    <span class="score-label">Match</span>
                </div>
                <div class="score-breakdown">
                    <h4>🎯 Perché l'abbiamo scelto:</h4>
                    <pre class="explanation">${result.explanation}</pre>
                </div>
            </div>

            ${renderProductDetails(product, mode)}

            <div class="result-actions">
                <button class="btn btn-primary">🛒 Vedi su shop</button>
                <button class="btn btn-secondary" onclick="checkCompatibility('${product.id}')">
                    🔍 Verifica compatibilità
                </button>
            </div>
        </div>
    `;

    document.getElementById('mainResult').innerHTML = html;
}

function renderAlternatives(alternatives) {
    let html = '';

    alternatives.forEach((result, index) => {
        const product = result.product;
        const mode = resultsData.mode;

        html += `
            <div class="result-card alternative-card">
                <div class="badge badge-info">Alternativa ${index + 1}</div>
                <h3>${product.name}</h3>
                <p class="brand">${product.brand}</p>

                <div class="score-mini">
                    Match: ${(result.score * 100).toFixed(0)}%
                </div>

                ${renderProductDetails(product, mode, true)}

                <details class="breakdown-details">
                    <summary>Vedi breakdown punteggio</summary>
                    <pre class="explanation">${result.explanation}</pre>
                </details>

                <button class="btn btn-sm btn-primary">Seleziona</button>
            </div>
        `;
    });

    document.getElementById('alternativeResults').innerHTML = html;
}

function renderProductDetails(product, mode, compact = false) {
    let html = '<div class="product-details">';

    if (mode === 'switch') {
        html += `
            <div class="detail-row">
                <span class="label">Feel:</span>
                <span class="value">${product.feel}</span>
            </div>
            <div class="detail-row">
                <span class="label">Attuazione:</span>
                <span class="value">${product.actuation_force}g</span>
            </div>
            <div class="detail-row">
                <span class="label">Suono:</span>
                <span class="value">${product.sound_profile.join(', ')}</span>
            </div>
            <div class="detail-row">
                <span class="label">Prezzo (90pz):</span>
                <span class="value">€${product.price_90 || 'N/A'}</span>
            </div>
        `;
    } else if (mode === 'keycap') {
        html += `
            <div class="detail-row">
                <span class="label">Materiale:</span>
                <span class="value">${product.material}</span>
            </div>
            <div class="detail-row">
                <span class="label">Profilo:</span>
                <span class="value">${product.profile}</span>
            </div>
            <div class="detail-row">
                <span class="label">Layout:</span>
                <span class="value">${product.layout_support.join(', ')}</span>
            </div>
            <div class="detail-row">
                <span class="label">Prezzo:</span>
                <span class="value">€${product.price_base_kit || 'N/A'}</span>
            </div>
        `;
    } else if (mode === 'board') {
        html += `
            <div class="detail-row">
                <span class="label">Form Factor:</span>
                <span class="value">${product.form_factor}</span>
            </div>
            <div class="detail-row">
                <span class="label">Layout:</span>
                <span class="value">${product.layout.join(', ')}</span>
            </div>
            <div class="detail-row">
                <span class="label">Hot-swap:</span>
                <span class="value">${product.hot_swap ? 'Sì' : 'No'}</span>
            </div>
            <div class="detail-row">
                <span class="label">Mounting:</span>
                <span class="value">${product.mounting_type}</span>
            </div>
            <div class="detail-row">
                <span class="label">Prezzo:</span>
                <span class="value">€${product.price || 'N/A'}</span>
            </div>
        `;
    }

    html += '</div>';
    return html;
}

async function loadSessionSummary() {
    try {
        const response = await fetch(`${API_BASE}/session/${sessionId}`);
        const data = await response.json();

        let html = `
            <div class="summary-content">
                <h3>📋 Le tue risposte:</h3>
                <pre>${JSON.stringify(data.answers, null, 2)}</pre>

                <h3>⚙️ Vincoli hard applicati:</h3>
                <pre>${JSON.stringify(data.hard_constraints, null, 2)}</pre>

                <h3>💰 Budget:</h3>
                <p>Hard: €${data.budget.hard || 'Nessun limite'}</p>
                <p>Soft: €${data.budget.soft || 'N/A'}</p>

                <h3>📊 Statistiche:</h3>
                <p>Domande risposte: ${data.total_questions_answered}</p>
                <p>Eventi tracciati: ${data.events_count}</p>
            </div>
        `;

        document.getElementById('sessionSummary').innerHTML = html;
    } catch (error) {
        console.error('Error loading session summary:', error);
    }
}

function checkCompatibility(productId) {
    // TODO: Implement compatibility check
    alert('Funzionalità compatibility check in sviluppo');
}

function goBackToWizard() {
    window.location.href = '/wizard';
}

function exportResults() {
    // Create build sheet
    const buildSheet = {
        mode: resultsData.mode,
        recommendations: resultsData.results.map(r => ({
            name: r.product.name,
            brand: r.product.brand,
            score: r.score,
            price: r.product.price || r.product.price_base_kit || r.product.price_90
        })),
        session_id: sessionId,
        exported_at: new Date().toISOString()
    };

    // Download as JSON
    const blob = new Blob([JSON.stringify(buildSheet, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `keyboard-finder-results-${Date.now()}.json`;
    a.click();
}

function startNew() {
    localStorage.removeItem('sessionId');
    localStorage.removeItem('results');
    localStorage.removeItem('searchMode');
    window.location.href = '/';
}
