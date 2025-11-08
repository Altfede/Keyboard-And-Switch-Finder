"""Modello per la sessione utente e le preferenze"""
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class SearchMode(str, Enum):
    SWITCH = "switch"
    KEYCAP = "keycap"
    BOARD = "board"


class SessionEvent(BaseModel):
    """Evento nella sessione con timestamp e contesto"""
    timestamp: str
    event_type: str  # question_answered, filter_applied, result_viewed, etc.
    question_id: Optional[str] = None
    answer: Any = None
    context: Dict[str, Any] = {}


class Session(BaseModel):
    """Sessione utente completa"""

    # Identificazione
    session_id: str
    created_at: str
    updated_at: str

    # Modalità di ricerca
    mode: SearchMode

    # Risposte utente
    answers: Dict[str, Any] = {}

    # Eventi tracciati
    events: List[SessionEvent] = []

    # Preferenze calcolate (vettore)
    preference_vector: Dict[str, float] = {}

    # Vincoli hard
    hard_constraints: Dict[str, Any] = {}

    # Budget
    budget_hard: Optional[float] = None
    budget_soft: Optional[float] = None

    # Regione e lingua
    region: str = "EU"
    language: str = "IT"

    # Risultati
    results: List[Dict[str, Any]] = []
    selected_result: Optional[str] = None

    # Stato
    completed: bool = False
    current_question_index: int = 0

    def add_event(self, event_type: str, question_id: Optional[str] = None,
                  answer: Any = None, context: Dict[str, Any] = None):
        """Aggiunge un evento alla sessione"""
        event = SessionEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            question_id=question_id,
            answer=answer,
            context=context or {}
        )
        self.events.append(event)
        self.updated_at = datetime.now().isoformat()

    def add_answer(self, question_id: str, answer: Any):
        """Aggiunge una risposta e registra l'evento"""
        self.answers[question_id] = answer
        self.add_event("question_answered", question_id=question_id, answer=answer)

    def get_summary(self) -> Dict[str, Any]:
        """Genera un riepilogo trasparente della sessione"""
        return {
            "session_id": self.session_id,
            "mode": self.mode,
            "created_at": self.created_at,
            "total_questions_answered": len(self.answers),
            "answers": self.answers,
            "hard_constraints": self.hard_constraints,
            "budget": {
                "hard": self.budget_hard,
                "soft": self.budget_soft
            },
            "events_count": len(self.events),
            "completed": self.completed
        }

    class Config:
        use_enum_values = True
