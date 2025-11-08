"""API Routes per il recommendation engine"""
from flask import Blueprint, request, jsonify
from typing import Dict, Any
import uuid
from datetime import datetime
import json

from ..models.session import Session, SearchMode
from ..models.switch import Switch
from ..models.keycap import KeycapSet
from ..models.board import Board
from ..engine.scoring import ScoringEngine, WeightPresets
from ..engine.compatibility import CompatibilityChecker
from ..questionnaires.switch_quiz import SwitchQuestionnaire
from ..questionnaires.keycap_quiz import KeycapQuestionnaire
from ..questionnaires.board_quiz import BoardQuestionnaire


api = Blueprint('api', __name__)

# Storage in-memory per sessioni (in produzione usare Redis o DB)
sessions_store: Dict[str, Session] = {}

# Storage in-memory per prodotti (caricati da JSON)
products_db = {
    "switches": [],
    "keycaps": [],
    "boards": []
}


def load_products():
    """Carica prodotti dai file JSON"""
    import os
    from pathlib import Path

    data_dir = Path(__file__).parent.parent / "data"

    try:
        # Carica switches
        switches_file = data_dir / "switches.json"
        if switches_file.exists():
            with open(switches_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products_db["switches"] = [Switch(**item) for item in data]

        # Carica keycaps
        keycaps_file = data_dir / "keycaps.json"
        if keycaps_file.exists():
            with open(keycaps_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products_db["keycaps"] = [KeycapSet(**item) for item in data]

        # Carica boards
        boards_file = data_dir / "boards.json"
        if boards_file.exists():
            with open(boards_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                products_db["boards"] = [Board(**item) for item in data]

    except Exception as e:
        print(f"Errore caricamento prodotti: {e}")


@api.route('/session/start', methods=['POST'])
def start_session():
    """
    Avvia una nuova sessione

    Body: {
        "mode": "switch" | "keycap" | "board",
        "region": "EU" (optional),
        "language": "IT" (optional)
    }
    """
    data = request.json
    mode = data.get('mode')

    if not mode or mode not in ['switch', 'keycap', 'board']:
        return jsonify({"error": "Mode invalido"}), 400

    # Crea nuova sessione
    session_id = str(uuid.uuid4())
    session = Session(
        session_id=session_id,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        mode=SearchMode(mode),
        region=data.get('region', 'EU'),
        language=data.get('language', 'IT')
    )

    sessions_store[session_id] = session

    return jsonify({
        "session_id": session_id,
        "mode": mode,
        "created_at": session.created_at
    })


@api.route('/session/<session_id>/questions', methods=['GET'])
def get_questions(session_id: str):
    """
    Ottiene le domande per la sessione corrente

    Query params:
        - skip_answered: bool (default True) - salta domande già risposte
    """
    session = sessions_store.get(session_id)
    if not session:
        return jsonify({"error": "Sessione non trovata"}), 404

    # Ottieni questionario appropriato
    if session.mode == SearchMode.SWITCH:
        questions = SwitchQuestionnaire.get_questions()
    elif session.mode == SearchMode.KEYCAP:
        questions = KeycapQuestionnaire.get_questions()
    else:  # BOARD
        questions = BoardQuestionnaire.get_questions()

    # Filtra domande già risposte se richiesto
    skip_answered = request.args.get('skip_answered', 'true').lower() == 'true'
    if skip_answered:
        questions = [q for q in questions if q.id not in session.answers]

    # Filtra domande da saltare in base a risposte precedenti
    if session.mode == SearchMode.SWITCH:
        questions = [
            q for q in questions
            if not SwitchQuestionnaire.should_skip_question(q, session.answers)
        ]

    # Converti in dict
    questions_data = [q.to_dict() for q in questions]

    return jsonify({
        "session_id": session_id,
        "mode": session.mode,
        "questions": questions_data,
        "total_questions": len(questions_data),
        "answered": len(session.answers),
        "progress": len(session.answers) / max(len(questions_data), 1) * 100
    })


@api.route('/session/<session_id>/answer', methods=['POST'])
def submit_answer(session_id: str):
    """
    Invia una risposta

    Body: {
        "question_id": "switch_feel",
        "answer": "linear"
    }
    """
    session = sessions_store.get(session_id)
    if not session:
        return jsonify({"error": "Sessione non trovata"}), 404

    data = request.json
    question_id = data.get('question_id')
    answer = data.get('answer')

    if not question_id or answer is None:
        return jsonify({"error": "question_id e answer richiesti"}), 400

    # Salva risposta
    session.add_answer(question_id, answer)

    return jsonify({
        "success": True,
        "session_id": session_id,
        "answered": len(session.answers)
    })


@api.route('/session/<session_id>/recommend', methods=['POST'])
def get_recommendations(session_id: str):
    """
    Ottiene raccomandazioni basate sulle risposte

    Body: {
        "top_n": 5 (optional),
        "preset_weights": "gaming" | "typing" | ... (optional)
    }
    """
    session = sessions_store.get(session_id)
    if not session:
        return jsonify({"error": "Sessione non trovata"}), 404

    data = request.json or {}
    top_n = data.get('top_n', 5)
    preset_name = data.get('preset_weights')

    # Costruisci vettore preferenze
    if session.mode == SearchMode.SWITCH:
        preference_vector = SwitchQuestionnaire.build_preference_vector(session.answers)
        hard_constraints = SwitchQuestionnaire.build_hard_constraints(session.answers)
        products = products_db["switches"]
    elif session.mode == SearchMode.KEYCAP:
        preference_vector = KeycapQuestionnaire.build_preference_vector(session.answers)
        hard_constraints = KeycapQuestionnaire.build_hard_constraints(session.answers)
        products = products_db["keycaps"]
    else:  # BOARD
        preference_vector = BoardQuestionnaire.build_preference_vector(session.answers)
        hard_constraints = BoardQuestionnaire.build_hard_constraints(session.answers)
        products = products_db["boards"]

    session.preference_vector = preference_vector
    session.hard_constraints = hard_constraints

    # Ottieni pesi da preset se specificato
    weights = WeightPresets.get_preset(preset_name) if preset_name else None

    # Inizializza scoring engine
    engine = ScoringEngine(weights=weights)

    # Filtra per budget hard se presente
    budget_hard = hard_constraints.get('_budget_hard')
    if budget_hard:
        if session.mode == SearchMode.SWITCH:
            quantity = hard_constraints.get('_quantity', 90)
            products = [
                p for p in products
                if p.get_price_for_quantity(quantity) and
                   p.get_price_for_quantity(quantity) <= budget_hard
            ]
        else:
            products = [
                p for p in products
                if (p.price and p.price <= budget_hard) or
                   (p.price_base_kit and p.price_base_kit <= budget_hard)
            ]

    # Filtra per regione se presente
    if 'availability_region' in hard_constraints:
        required_regions = hard_constraints['availability_region']
        products = [
            p for p in products
            if any(r in p.availability_region for r in required_regions)
        ]

    # Calcola ranking
    ranked_products = engine.rank_products(
        products,
        preference_vector,
        hard_constraints,
        top_n=top_n
    )

    # Formatta risultati con spiegazioni
    results = []
    for product, score, breakdown in ranked_products:
        explanation = engine.explain_score(breakdown, product.name)

        result = {
            "product": product.dict(),
            "score": score,
            "breakdown": breakdown,
            "explanation": explanation
        }
        results.append(result)

    # Salva risultati in sessione
    session.results = results
    session.completed = True

    return jsonify({
        "session_id": session_id,
        "mode": session.mode,
        "results": results,
        "total_results": len(results)
    })


@api.route('/compatibility/check', methods=['POST'])
def check_compatibility():
    """
    Verifica compatibilità tra componenti

    Body: {
        "board_id": "...",
        "switch_id": "...",
        "keycap_id": "..."
    }
    """
    data = request.json

    board_id = data.get('board_id')
    switch_id = data.get('switch_id')
    keycap_id = data.get('keycap_id')

    # Trova prodotti
    board = next((b for b in products_db["boards"] if b.id == board_id), None)
    switch = next((s for s in products_db["switches"] if s.id == switch_id), None)
    keycap = next((k for k in products_db["keycaps"] if k.id == keycap_id), None)

    if not all([board, switch, keycap]):
        return jsonify({"error": "Prodotto non trovato"}), 404

    # Verifica compatibilità
    result = CompatibilityChecker.check_full_build_compatibility(
        board, switch, keycap
    )

    # Suggerisci alternative se ci sono problemi
    if not result["compatible"]:
        suggestions = CompatibilityChecker.suggest_alternatives(
            board, switch, keycap,
            products_db["switches"],
            products_db["keycaps"]
        )
        result["suggestions"] = suggestions

    return jsonify(result)


@api.route('/session/<session_id>', methods=['GET'])
def get_session(session_id: str):
    """Ottiene lo stato della sessione"""
    session = sessions_store.get(session_id)
    if not session:
        return jsonify({"error": "Sessione non trovata"}), 404

    return jsonify(session.get_summary())


@api.route('/products/<product_type>', methods=['GET'])
def list_products(product_type: str):
    """
    Lista prodotti per tipo

    Query params:
        - limit: int (default 50)
        - region: str (filter by region)
        - in_stock: bool (filter by stock status)
    """
    if product_type not in products_db:
        return jsonify({"error": "Tipo prodotto invalido"}), 400

    products = products_db[product_type]

    # Applica filtri
    region = request.args.get('region')
    if region:
        products = [p for p in products if region in p.availability_region]

    in_stock = request.args.get('in_stock')
    if in_stock and in_stock.lower() == 'true':
        products = [p for p in products if p.stock_status == 'in_stock']

    # Limita risultati
    limit = int(request.args.get('limit', 50))
    products = products[:limit]

    return jsonify({
        "product_type": product_type,
        "count": len(products),
        "products": [p.dict() for p in products]
    })


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "products_loaded": {
            "switches": len(products_db["switches"]),
            "keycaps": len(products_db["keycaps"]),
            "boards": len(products_db["boards"])
        },
        "active_sessions": len(sessions_store)
    })
