/**
 * Wizard logic for questionnaire
 */

const API_BASE = '/api';
let sessionId = null;
let questions = [];
let currentQuestionIndex = 0;
let answers = {};

// Initialize wizard on page load
document.addEventListener('DOMContentLoaded', async () => {
    sessionId = localStorage.getItem('sessionId');

    if (!sessionId) {
        alert('Sessione non trovata. Torna alla home.');
        window.location.href = '/';
        return;
    }

    await loadQuestions();
    renderCurrentQuestion();
});

/**
 * Load questions from API
 */
async function loadQuestions() {
    try {
        const response = await fetch(`${API_BASE}/session/${sessionId}/questions`);

        if (!response.ok) {
            throw new Error('Failed to load questions');
        }

        const data = await response.json();
        questions = data.questions;

        updateProgress();
    } catch (error) {
        console.error('Error loading questions:', error);
        alert('Errore nel caricamento delle domande');
    }
}

/**
 * Render current question
 */
function renderCurrentQuestion() {
    if (currentQuestionIndex >= questions.length) {
        // All questions answered
        showSubmitButton();
        return;
    }

    const question = questions[currentQuestionIndex];
    const container = document.getElementById('questionContainer');

    let html = `
        <div class="question">
            <h2 class="question-title">
                <span class="question-number">Domanda ${currentQuestionIndex + 1} di ${questions.length}</span>
                ${question.text}
            </h2>
    `;

    if (question.description) {
        html += `<p class="question-description">${question.description}</p>`;
    }

    // Render based on type
    switch (question.type) {
        case 'single_choice':
            html += renderSingleChoice(question);
            break;
        case 'multi_choice':
            html += renderMultiChoice(question);
            break;
        case 'slider':
            html += renderSlider(question);
            break;
        case 'yes_no':
            html += renderYesNo(question);
            break;
        default:
            html += '<p>Tipo domanda non supportato</p>';
    }

    // Audio samples if present
    if (question.audio_samples && question.audio_samples.length > 0) {
        html += renderAudioSamples(question.audio_samples);
    }

    html += '</div>';
    container.innerHTML = html;

    // Restore previous answer if exists
    if (answers[question.id]) {
        restoreAnswer(question);
    }

    updateNavigationButtons();
}

function renderSingleChoice(question) {
    let html = '<div class="options single-choice">';

    question.options.forEach((option, index) => {
        html += `
            <label class="option-card">
                <input type="radio"
                       name="${question.id}"
                       value="${option.value}"
                       onchange="saveCurrentAnswer()">
                <div class="option-content">
                    <strong>${option.label}</strong>
                    ${option.description ? `<p>${option.description}</p>` : ''}
                </div>
            </label>
        `;
    });

    html += '</div>';
    return html;
}

function renderMultiChoice(question) {
    let html = '<div class="options multi-choice">';

    question.options.forEach((option, index) => {
        html += `
            <label class="option-card">
                <input type="checkbox"
                       name="${question.id}"
                       value="${option.value}"
                       onchange="saveCurrentAnswer()">
                <div class="option-content">
                    <strong>${option.label}</strong>
                    ${option.description ? `<p>${option.description}</p>` : ''}
                </div>
            </label>
        `;
    });

    html += '</div>';
    return html;
}

function renderSlider(question) {
    const opts = question.options[0];
    const mid = (opts.min + opts.max) / 2;

    let html = `
        <div class="slider-container">
            <input type="range"
                   id="${question.id}"
                   name="${question.id}"
                   min="${opts.min}"
                   max="${opts.max}"
                   step="${opts.step}"
                   value="${mid}"
                   oninput="updateSliderValue(this)"
                   onchange="saveCurrentAnswer()">
            <div class="slider-value">
                <span id="${question.id}_value">${mid}</span>
                <span>${opts.unit || ''}</span>
            </div>
    `;

    // Marks
    if (opts.marks) {
        html += '<div class="slider-marks">';
        opts.marks.forEach(mark => {
            html += `<span class="mark">${mark.label}</span>`;
        });
        html += '</div>';
    }

    html += '</div>';
    return html;
}

function renderYesNo(question) {
    return `
        <div class="options yes-no">
            <label class="option-card">
                <input type="radio"
                       name="${question.id}"
                       value="yes"
                       onchange="saveCurrentAnswer()">
                <div class="option-content">
                    <strong>Sì</strong>
                </div>
            </label>
            <label class="option-card">
                <input type="radio"
                       name="${question.id}"
                       value="no"
                       onchange="saveCurrentAnswer()">
                <div class="option-content">
                    <strong>No</strong>
                </div>
            </label>
        </div>
    `;
}

function renderAudioSamples(samples) {
    let html = '<div class="audio-samples"><h4>🔊 Campioni audio</h4>';

    samples.forEach((sample, index) => {
        html += `
            <audio controls>
                <source src="${sample}" type="audio/mpeg">
                Il tuo browser non supporta l'audio.
            </audio>
        `;
    });

    html += '</div>';
    return html;
}

function updateSliderValue(slider) {
    document.getElementById(`${slider.id}_value`).textContent = slider.value;
}

function saveCurrentAnswer() {
    const question = questions[currentQuestionIndex];
    let answer = null;

    if (question.type === 'multi_choice') {
        const checkboxes = document.querySelectorAll(`input[name="${question.id}"]:checked`);
        answer = Array.from(checkboxes).map(cb => cb.value);
    } else if (question.type === 'slider') {
        const slider = document.getElementById(question.id);
        answer = parseInt(slider.value);
    } else {
        const input = document.querySelector(`input[name="${question.id}"]:checked`);
        answer = input ? input.value : null;
    }

    if (answer !== null) {
        answers[question.id] = answer;
    }
}

function restoreAnswer(question) {
    const answer = answers[question.id];

    if (question.type === 'multi_choice' && Array.isArray(answer)) {
        answer.forEach(value => {
            const checkbox = document.querySelector(`input[name="${question.id}"][value="${value}"]`);
            if (checkbox) checkbox.checked = true;
        });
    } else if (question.type === 'slider') {
        const slider = document.getElementById(question.id);
        if (slider) {
            slider.value = answer;
            updateSliderValue(slider);
        }
    } else {
        const radio = document.querySelector(`input[name="${question.id}"][value="${answer}"]`);
        if (radio) radio.checked = true;
    }
}

function goNext() {
    saveCurrentAnswer();

    const question = questions[currentQuestionIndex];
    if (!answers[question.id]) {
        alert('Per favore rispondi alla domanda prima di proseguire');
        return;
    }

    // Send answer to server
    sendAnswer(question.id, answers[question.id]);

    currentQuestionIndex++;
    renderCurrentQuestion();
    updateProgress();
}

function goBack() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        renderCurrentQuestion();
        updateProgress();
    }
}

async function sendAnswer(questionId, answer) {
    try {
        await fetch(`${API_BASE}/session/${sessionId}/answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_id: questionId,
                answer: answer
            })
        });
    } catch (error) {
        console.error('Error sending answer:', error);
    }
}

async function submitQuiz() {
    // Show loading
    document.getElementById('loadingOverlay').style.display = 'flex';

    try {
        const response = await fetch(`${API_BASE}/session/${sessionId}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ top_n: 5 })
        });

        if (!response.ok) {
            throw new Error('Failed to get recommendations');
        }

        const data = await response.json();

        // Save results and redirect
        localStorage.setItem('results', JSON.stringify(data));
        window.location.href = '/results';

    } catch (error) {
        console.error('Error getting recommendations:', error);
        alert('Errore nel calcolo delle raccomandazioni');
        document.getElementById('loadingOverlay').style.display = 'none';
    }
}

function updateProgress() {
    const progress = (currentQuestionIndex / questions.length) * 100;
    document.getElementById('progressBar').style.width = `${progress}%`;
    document.getElementById('progressText').textContent = `${Math.round(progress)}%`;
}

function updateNavigationButtons() {
    document.getElementById('backBtn').disabled = currentQuestionIndex === 0;

    if (currentQuestionIndex === questions.length) {
        document.getElementById('nextBtn').style.display = 'none';
        document.getElementById('submitBtn').style.display = 'block';
    } else {
        document.getElementById('nextBtn').style.display = 'block';
        document.getElementById('submitBtn').style.display = 'none';
    }
}

function showSubmitButton() {
    document.getElementById('questionContainer').innerHTML = `
        <div class="completion-message">
            <h2>✅ Questionario completato!</h2>
            <p>Hai risposto a tutte le domande. Clicca qui sotto per ottenere le tue raccomandazioni personalizzate.</p>
        </div>
    `;
    updateNavigationButtons();
}
