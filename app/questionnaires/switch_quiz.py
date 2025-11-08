"""Questionario per Switch meccanici"""
from typing import List, Dict, Any, Optional


class Question:
    """Rappresenta una singola domanda del questionario"""

    def __init__(
        self,
        id: str,
        text: str,
        type: str,  # single_choice, multi_choice, slider, number, yes_no
        options: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        audio_samples: Optional[List[str]] = None,
        skip_if: Optional[Dict[str, Any]] = None,  # Condizioni per skip
        weight_mapping: Optional[Dict[str, Dict[str, float]]] = None,
        constraint_mapping: Optional[Dict[str, Any]] = None
    ):
        self.id = id
        self.text = text
        self.type = type
        self.options = options or []
        self.description = description
        self.audio_samples = audio_samples or []
        self.skip_if = skip_if
        self.weight_mapping = weight_mapping or {}
        self.constraint_mapping = constraint_mapping or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "type": self.type,
            "options": self.options,
            "description": self.description,
            "audio_samples": self.audio_samples
        }


class SwitchQuestionnaire:
    """Questionario completo per Switch"""

    @staticmethod
    def get_questions() -> List[Question]:
        """Restituisce tutte le domande per Switch"""

        return [
            # Q1: Tipo di feel
            Question(
                id="switch_feel",
                text="Che tipo di feeling preferisci?",
                type="single_choice",
                description="Il 'feel' determina la sensazione tattile durante la pressione",
                options=[
                    {
                        "value": "linear",
                        "label": "Lineare",
                        "description": "Corsa liscia dall'inizio alla fine, senza bump"
                    },
                    {
                        "value": "tactile",
                        "label": "Tattile",
                        "description": "Bump tattile al punto di attuazione"
                    },
                    {
                        "value": "clicky",
                        "label": "Clicky",
                        "description": "Bump tattile + click sonoro"
                    },
                    {
                        "value": "indifferent",
                        "label": "Indifferente",
                        "description": "Non ho preferenze particolari"
                    }
                ],
                audio_samples=[
                    "/audio/switch_linear_sample.mp3",
                    "/audio/switch_tactile_sample.mp3",
                    "/audio/switch_clicky_sample.mp3"
                ],
                weight_mapping={
                    "linear": {"feel_linear": 1.0, "feel_tactile": 0.0, "feel_clicky": 0.0},
                    "tactile": {"feel_linear": 0.0, "feel_tactile": 1.0, "feel_clicky": 0.0},
                    "clicky": {"feel_linear": 0.0, "feel_tactile": 0.0, "feel_clicky": 1.0},
                    "indifferent": {}  # Nessun peso specifico
                }
            ),

            # Q2: Peso di attuazione
            Question(
                id="actuation_force",
                text="Quale peso di attuazione preferisci?",
                type="slider",
                description="Più leggero = meno forza richiesta (affaticamento minore), "
                           "più pesante = più controllo e precisione",
                options=[
                    {"min": 35, "max": 80, "step": 1, "unit": "g",
                     "marks": [
                         {"value": 45, "label": "45g (leggero)"},
                         {"value": 50, "label": "50g"},
                         {"value": 62, "label": "62g (medio)"},
                         {"value": 67, "label": "67g (pesante)"}
                     ]}
                ],
                weight_mapping={
                    # Mapping dinamico basato sul valore
                    "_dynamic": True
                }
            ),

            # Q3: Pre-lubrificazione
            Question(
                id="factory_lubed",
                text="Preferisci switch pre-lubrificati di fabbrica?",
                type="single_choice",
                description="Gli switch pre-lubed sono pronti all'uso e più smooth, "
                           "quelli dry richiedono lubrificazione manuale",
                options=[
                    {"value": "yes", "label": "Sì, voglio switch già lubrificati"},
                    {"value": "no", "label": "No, preferisco lubrificare io"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "yes": {"factory_lubed": 1.0},
                    "no": {"factory_lubed": 0.0},
                    "indifferent": {}
                }
            ),

            # Q4: RGB e housing trasparente
            Question(
                id="rgb_housing",
                text="Ti serve housing trasparente per RGB?",
                type="yes_no",
                description="Housing trasparente lascia passare meglio la luce RGB",
                weight_mapping={
                    "yes": {"transparent_housing": 1.0, "rgb_compatible": 1.0},
                    "no": {}
                }
            ),

            # Q5: Stile di suono
            Question(
                id="sound_style",
                text="Quale stile di suono preferisci?",
                type="multi_choice",
                description="Il suono finale dipende anche da case, plate e keycaps",
                options=[
                    {
                        "value": "thock",
                        "label": "Thock",
                        "description": "Suono profondo e pieno (basso)"
                    },
                    {
                        "value": "clack",
                        "label": "Clack",
                        "description": "Suono più alto e secco"
                    },
                    {
                        "value": "marbly",
                        "label": "Marbly",
                        "description": "Suono simile a biglie/marmo"
                    },
                    {
                        "value": "muted",
                        "label": "Muted/Silent",
                        "description": "Suono attenuato e discreto"
                    },
                    {
                        "value": "creamy",
                        "label": "Creamy",
                        "description": "Suono morbido e vellutato"
                    },
                    {
                        "value": "indifferent",
                        "label": "Indifferente",
                        "description": "Non ho preferenze sul suono"
                    }
                ],
                audio_samples=[
                    "/audio/sound_thock.mp3",
                    "/audio/sound_clack.mp3",
                    "/audio/sound_marbly.mp3",
                    "/audio/sound_muted.mp3",
                    "/audio/sound_creamy.mp3"
                ],
                weight_mapping={
                    "thock": {"sound_thock": 1.0},
                    "clack": {"sound_clack": 1.0},
                    "marbly": {"sound_marbly": 1.0},
                    "muted": {"sound_muted": 1.0},
                    "creamy": {"sound_creamy": 1.0},
                    "indifferent": {}
                }
            ),

            # Q6: Silenziosità richiesta
            Question(
                id="silent_required",
                text="Hai bisogno di switch silenziosi?",
                type="yes_no",
                description="Gli switch silent hanno dampeners che riducono il rumore "
                           "sia in bottom-out che in top-out",
                skip_if={
                    "sound_style": ["muted"]  # Skip se già scelto muted
                },
                weight_mapping={
                    "yes": {"silent": 1.0},
                    "no": {}
                },
                constraint_mapping={
                    "yes": {"silent_variant": True}
                }
            ),

            # Q7: Smoothness desiderato
            Question(
                id="smoothness",
                text="Quanto è importante la smoothness (scorrevolezza)?",
                type="single_choice",
                options=[
                    {"value": "5", "label": "Fondamentale - solo buttery smooth"},
                    {"value": "4", "label": "Molto importante"},
                    {"value": "3", "label": "Moderatamente importante"},
                    {"value": "2", "label": "Poco importante"},
                    {"value": "1", "label": "Non mi interessa"}
                ],
                weight_mapping={
                    "5": {"smoothness": 1.0},
                    "4": {"smoothness": 0.8},
                    "3": {"smoothness": 0.5},
                    "2": {"smoothness": 0.3},
                    "1": {}
                }
            ),

            # Q8: Tolleranza spring ping
            Question(
                id="spring_ping",
                text="Quanto tolleri il ping della molla?",
                type="single_choice",
                description="Il 'spring ping' è un suono metallico della molla interna",
                options=[
                    {"value": "low", "label": "Bassa - deve essere assente"},
                    {"value": "medium", "label": "Media - tollerabile se lieve"},
                    {"value": "high", "label": "Alta - non mi disturba"}
                ],
                weight_mapping={
                    "low": {"no_ping": 1.0},
                    "medium": {"no_ping": 0.5},
                    "high": {}
                }
            ),

            # Q9: Stabilità e wobble
            Question(
                id="stem_stability",
                text="Quanto è importante la stabilità dello stem (assenza wobble)?",
                type="single_choice",
                description="Il wobble è il movimento laterale del keycap sullo switch",
                options=[
                    {"value": "high", "label": "Molto importante - zero wobble"},
                    {"value": "medium", "label": "Moderatamente importante"},
                    {"value": "low", "label": "Non è una priorità"}
                ],
                weight_mapping={
                    "high": {"stability": 1.0},
                    "medium": {"stability": 0.6},
                    "low": {}
                }
            ),

            # Q10: Long-pole stem
            Question(
                id="long_pole",
                text="Vuoi switch con long-pole stem?",
                type="single_choice",
                description="Long-pole stem riduce il travel e cambia il suono "
                           "(più clacky)",
                options=[
                    {"value": "yes", "label": "Sì, preferisco long-pole"},
                    {"value": "no", "label": "No, preferisco standard"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "yes": {"long_pole": 1.0},
                    "no": {"long_pole": 0.0},
                    "indifferent": {}
                }
            ),

            # Q11: Total travel
            Question(
                id="travel_preference",
                text="Preferisci travel ridotto o standard?",
                type="single_choice",
                description="Travel ridotto (3.6-3.8mm) è più veloce, "
                           "standard (4.0mm) è più tradizionale",
                options=[
                    {"value": "reduced", "label": "Ridotto (3.6-3.8mm) - gaming"},
                    {"value": "standard", "label": "Standard (4.0mm)"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "reduced": {"travel_norm": 0.0},  # Valore basso
                    "standard": {"travel_norm": 0.67},  # Valore medio-alto
                    "indifferent": {}
                }
            ),

            # Q12: Pin count
            Question(
                id="pin_count",
                text="Hai vincoli sul numero di pin?",
                type="single_choice",
                description="5-pin sono più stabili, 3-pin più universali",
                options=[
                    {"value": "5", "label": "Solo 5-pin"},
                    {"value": "3", "label": "Solo 3-pin"},
                    {"value": "both", "label": "Entrambi vanno bene"}
                ],
                weight_mapping={
                    "5": {"pin_5": 1.0},
                    "3": {"pin_5": 0.0},
                    "both": {}
                },
                constraint_mapping={
                    "5": {"pin_count": 5},
                    "3": {"pin_count": 3}
                }
            ),

            # Q13: Budget
            Question(
                id="budget",
                text="Qual è il tuo budget per uno switch set?",
                type="single_choice",
                description="Indica la quantità di switch necessari e il budget",
                options=[
                    {
                        "value": "70_low",
                        "label": "70 switch - Budget <35€",
                        "quantity": 70,
                        "budget": 35
                    },
                    {
                        "value": "70_mid",
                        "label": "70 switch - Budget 35-50€",
                        "quantity": 70,
                        "budget": 50
                    },
                    {
                        "value": "90_low",
                        "label": "90 switch - Budget <45€",
                        "quantity": 90,
                        "budget": 45
                    },
                    {
                        "value": "90_mid",
                        "label": "90 switch - Budget 45-65€",
                        "quantity": 90,
                        "budget": 65
                    },
                    {
                        "value": "110_mid",
                        "label": "110 switch - Budget 50-80€",
                        "quantity": 110,
                        "budget": 80
                    },
                    {
                        "value": "unlimited",
                        "label": "Nessun limite di budget",
                        "quantity": 90,
                        "budget": None
                    }
                ]
            ),

            # Q14: Disponibilità regionale
            Question(
                id="region",
                text="Dove preferisci acquistare?",
                type="single_choice",
                options=[
                    {"value": "EU", "label": "Unione Europea (no dazi)"},
                    {"value": "EU_UK", "label": "EU + UK"},
                    {"value": "ALL", "label": "Ovunque (accetto extra-UE)"}
                ],
                constraint_mapping={
                    "EU": {"availability_region": ["EU"]},
                    "EU_UK": {"availability_region": ["EU", "UK"]},
                    "ALL": {}
                }
            )
        ]

    @staticmethod
    def should_skip_question(
        question: Question,
        answers: Dict[str, Any]
    ) -> bool:
        """
        Determina se una domanda deve essere saltata in base alle risposte precedenti

        Args:
            question: Domanda da valutare
            answers: Risposte già fornite

        Returns:
            True se la domanda va saltata
        """
        if not question.skip_if:
            return False

        for answer_key, skip_values in question.skip_if.items():
            if answer_key in answers:
                answer_value = answers[answer_key]
                # Se la risposta è in skip_values, salta la domanda
                if isinstance(answer_value, list):
                    if any(v in skip_values for v in answer_value):
                        return True
                elif answer_value in skip_values:
                    return True

        return False

    @staticmethod
    def build_preference_vector(
        answers: Dict[str, Any]
    ) -> Dict[str, float]:
        """
        Costruisce il vettore di preferenze dalle risposte

        Args:
            answers: Risposte dell'utente

        Returns:
            Vettore di preferenze normalizzato
        """
        preference_vector = {}
        questions = SwitchQuestionnaire.get_questions()

        for question in questions:
            if question.id not in answers:
                continue

            answer_value = answers[question.id]

            # Applica weight mapping
            if question.weight_mapping:
                # Dynamic mapping per slider
                if question.weight_mapping.get("_dynamic"):
                    if question.id == "actuation_force":
                        # Normalizza 35-80 -> 0-1
                        norm_value = (float(answer_value) - 35) / 45
                        preference_vector["actuation_force_norm"] = norm_value
                else:
                    # Static mapping
                    if isinstance(answer_value, list):
                        # Multi-choice
                        for val in answer_value:
                            if val in question.weight_mapping:
                                for k, v in question.weight_mapping[val].items():
                                    preference_vector[k] = max(
                                        preference_vector.get(k, 0), v
                                    )
                    else:
                        # Single choice
                        if str(answer_value) in question.weight_mapping:
                            for k, v in question.weight_mapping[str(answer_value)].items():
                                preference_vector[k] = v

        return preference_vector

    @staticmethod
    def build_hard_constraints(
        answers: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Costruisce i vincoli hard dalle risposte

        Args:
            answers: Risposte dell'utente

        Returns:
            Dizionario di vincoli hard
        """
        constraints = {}
        questions = SwitchQuestionnaire.get_questions()

        for question in questions:
            if question.id not in answers:
                continue

            answer_value = answers[question.id]

            # Applica constraint mapping
            if question.constraint_mapping and str(answer_value) in question.constraint_mapping:
                for k, v in question.constraint_mapping[str(answer_value)].items():
                    constraints[k] = v

        # Gestisci budget
        if "budget" in answers:
            budget_option = answers["budget"]
            budget_opts = [opt for q in questions if q.id == "budget"
                          for opt in q.options if opt["value"] == budget_option]
            if budget_opts:
                constraints["_quantity"] = budget_opts[0].get("quantity")
                if budget_opts[0].get("budget"):
                    constraints["_budget_hard"] = budget_opts[0]["budget"]

        return constraints
