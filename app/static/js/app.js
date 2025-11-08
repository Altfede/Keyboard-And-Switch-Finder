/**
 * Main app logic
 */

const API_BASE = '/api';

/**
 * Starts a new search session with the selected mode
 */
async function startMode(mode) {
    try {
        const response = await fetch(`${API_BASE}/session/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mode })
        });

        if (!response.ok) {
            throw new Error('Failed to start session');
        }

        const data = await response.json();

        // Save session ID to localStorage
        localStorage.setItem('sessionId', data.session_id);
        localStorage.setItem('searchMode', mode);

        // Redirect to wizard
        window.location.href = '/wizard';
    } catch (error) {
        console.error('Error starting session:', error);
        alert('Errore nell\'avvio della sessione. Riprova.');
    }
}

/**
 * Utility: Format price
 */
function formatPrice(price) {
    if (!price) return 'N/A';
    return `€${price.toFixed(2)}`;
}

/**
 * Utility: Get mode emoji
 */
function getModeEmoji(mode) {
    const emojis = {
        'switch': '⚙️',
        'keycap': '🔤',
        'board': '⌨️'
    };
    return emojis[mode] || '🔍';
}
