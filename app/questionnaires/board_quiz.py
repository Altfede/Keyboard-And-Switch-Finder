"""Questionario per Tastiere complete"""
from typing import List, Dict, Any
from .switch_quiz import Question


class BoardQuestionnaire:
    """Questionario per tastiere complete"""

    @staticmethod
    def get_questions() -> List[Question]:
        """Restituisce tutte le domande per Board"""

        return [
            # Q1: Uso principale
            Question(
                id="primary_use",
                text="Qual è l'uso principale della tastiera?",
                type="single_choice",
                options=[
                    {"value": "gaming_comp", "label": "Gaming competitivo"},
                    {"value": "gaming_casual", "label": "Gaming casual"},
                    {"value": "typing", "label": "Scrittura/Programmazione"},
                    {"value": "mixed", "label": "Uso misto"}
                ]
            ),

            # Q2: Form factor
            Question(
                id="form_factor",
                text="Che form factor preferisci?",
                type="single_choice",
                description="Considera lo spazio sulla scrivania e le funzioni necessarie",
                options=[
                    {"value": "100%", "label": "100% (Full size, con numpad)"},
                    {"value": "96%", "label": "96% (compact full, numpad compatto)"},
                    {"value": "80%", "label": "80%/TKL (senza numpad)"},
                    {"value": "75%", "label": "75% (compatto, con F-row)"},
                    {"value": "65%", "label": "65% (compatto, con frecce)"},
                    {"value": "60%", "label": "60% (minimal)"}
                ],
                weight_mapping={
                    "100%": {"ff_full": 1.0, "has_numpad": 1.0},
                    "96%": {"ff_full": 0.8, "has_numpad": 1.0},
                    "80%": {"ff_tkl": 1.0},
                    "75%": {"ff_75": 1.0},
                    "65%": {"ff_65": 1.0},
                    "60%": {"ff_60": 1.0}
                },
                constraint_mapping={
                    "100%": {"form_factor": "100%"},
                    "80%": {"form_factor": "80%"},
                    "75%": {"form_factor": "75%"},
                    "65%": {"form_factor": "65%"},
                    "60%": {"form_factor": "60%"}
                }
            ),

            # Q3: Layout
            Question(
                id="layout",
                text="Che layout ti serve?",
                type="single_choice",
                options=[
                    {"value": "ANSI", "label": "ANSI (US)"},
                    {"value": "ISO", "label": "ISO"},
                    {"value": "ISO_IT", "label": "ISO-IT (obbligatorio)"}
                ],
                weight_mapping={
                    "ISO": {"layout_iso": 1.0},
                    "ISO_IT": {"layout_iso_it": 1.0},
                    "ANSI": {}
                },
                constraint_mapping={
                    "ISO_IT": {"layout": ["ISO_IT"]}
                }
            ),

            # Q4: Hot-swap
            Question(
                id="hot_swap",
                text="Vuoi hot-swap?",
                type="single_choice",
                description="Hot-swap ti permette di cambiare switch senza saldare",
                options=[
                    {"value": "yes_5pin", "label": "Sì, 5-pin"},
                    {"value": "yes_any", "label": "Sì, qualsiasi"},
                    {"value": "no", "label": "No, saldato va bene"}
                ],
                weight_mapping={
                    "yes_5pin": {"hot_swap": 1.0, "hot_swap_5pin": 1.0},
                    "yes_any": {"hot_swap": 1.0},
                    "no": {}
                },
                constraint_mapping={
                    "yes_5pin": {"hot_swap": True, "hot_swap_pin_support": 5},
                    "yes_any": {"hot_swap": True}
                }
            ),

            # Q5: Mounting type
            Question(
                id="mounting",
                text="Che tipo di mounting preferisci?",
                type="single_choice",
                description="Il mounting influenza feel e suono",
                options=[
                    {"value": "gasket", "label": "Gasket (flex, thocky)"},
                    {"value": "top", "label": "Top mount (rigido)"},
                    {"value": "tray", "label": "Tray mount (economico, rigido)"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "gasket": {"mount_gasket": 1.0},
                    "top": {"mount_top": 1.0},
                    "tray": {"mount_tray": 1.0},
                    "indifferent": {}
                }
            ),

            # Q6: Connettività
            Question(
                id="connectivity",
                text="Che connettività ti serve?",
                type="multi_choice",
                options=[
                    {"value": "wired", "label": "Wired (bassa latenza)"},
                    {"value": "wireless", "label": "Wireless 2.4GHz"},
                    {"value": "bluetooth", "label": "Bluetooth"}
                ],
                weight_mapping={
                    "wired": {"wired": 1.0},
                    "wireless": {"wireless": 1.0},
                    "bluetooth": {"wireless": 1.0}
                }
            ),

            # Q7: Programmabilità
            Question(
                id="programmable",
                text="Ti serve programmabilità (QMK/VIA)?",
                type="yes_no",
                description="QMK/VIA permettono remapping tasti e macro custom",
                weight_mapping={
                    "yes": {"qmk_via": 1.0, "programmable": 1.0},
                    "no": {}
                }
            ),

            # Q8: RGB
            Question(
                id="rgb",
                text="Ti serve RGB?",
                type="single_choice",
                options=[
                    {"value": "per_key", "label": "Sì, per-key RGB"},
                    {"value": "any", "label": "Sì, qualsiasi RGB"},
                    {"value": "no", "label": "No, non mi serve"}
                ],
                weight_mapping={
                    "per_key": {"rgb_per_key": 1.0},
                    "any": {},
                    "no": {}
                }
            ),

            # Q9: Sound signature
            Question(
                id="sound",
                text="Che sound signature preferisci?",
                type="single_choice",
                options=[
                    {"value": "thock", "label": "Thock (basso, pieno)"},
                    {"value": "clack", "label": "Clack (alto, secco)"},
                    {"value": "muted", "label": "Muted (silenzioso)"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "thock": {"sound_thock": 1.0},
                    "clack": {"sound_clack": 1.0},
                    "muted": {"sound_muted": 1.0},
                    "indifferent": {}
                }
            ),

            # Q10: Prebuilt vs Barebone
            Question(
                id="product_type",
                text="Preferisci prebuilt o barebone?",
                type="single_choice",
                description="Prebuilt è ready-to-use, barebone richiede switch e keycaps",
                options=[
                    {"value": "prebuilt", "label": "Prebuilt (pronta all'uso)"},
                    {"value": "barebone", "label": "Barebone (personalizzerò)"},
                    {"value": "any", "label": "Indifferente"}
                ],
                weight_mapping={
                    "prebuilt": {"prebuilt": 1.0},
                    "barebone": {"barebone": 1.0},
                    "any": {}
                }
            ),

            # Q11: Budget
            Question(
                id="budget",
                text="Qual è il tuo budget?",
                type="single_choice",
                options=[
                    {"value": "low", "label": "<100€"},
                    {"value": "mid", "label": "100-200€"},
                    {"value": "high", "label": "200-400€"},
                    {"value": "premium", "label": ">400€"}
                ]
            ),

            # Q12: Rumorosità per ufficio
            Question(
                id="office_quiet",
                text="Devi usarla in ufficio/ambiente silenzioso?",
                type="yes_no",
                skip_if={"sound": ["muted"]},
                weight_mapping={
                    "yes": {"sound_muted": 1.0, "has_foam": 1.0},
                    "no": {}
                }
            )
        ]

    @staticmethod
    def build_preference_vector(answers: Dict[str, Any]) -> Dict[str, float]:
        """Costruisce vettore preferenze da risposte"""
        preference_vector = {}
        questions = BoardQuestionnaire.get_questions()

        # Applica weight mapping
        for question in questions:
            if question.id not in answers:
                continue

            answer_value = answers[question.id]

            if question.weight_mapping:
                if isinstance(answer_value, list):
                    for val in answer_value:
                        if val in question.weight_mapping:
                            for k, v in question.weight_mapping[val].items():
                                preference_vector[k] = max(preference_vector.get(k, 0), v)
                else:
                    if str(answer_value) in question.weight_mapping:
                        for k, v in question.weight_mapping[str(answer_value)].items():
                            preference_vector[k] = v

        # Applica preset basato su primary_use
        if "primary_use" in answers:
            use = answers["primary_use"]
            if use == "gaming_comp":
                preference_vector.update({
                    "low_latency": 1.5,
                    "mount_tray": 1.2,
                    "nkro": 1.0
                })
            elif use == "typing":
                preference_vector.update({
                    "mount_gasket": 1.5,
                    "sound_thock": 1.2
                })

        return preference_vector

    @staticmethod
    def build_hard_constraints(answers: Dict[str, Any]) -> Dict[str, Any]:
        """Costruisce vincoli hard da risposte"""
        constraints = {}
        questions = BoardQuestionnaire.get_questions()

        for question in questions:
            if question.id not in answers:
                continue

            answer_value = answers[question.id]

            if question.constraint_mapping:
                key = str(answer_value) if not isinstance(answer_value, list) else answer_value[0]
                if key in question.constraint_mapping:
                    for k, v in question.constraint_mapping[key].items():
                        constraints[k] = v

        # Budget
        if "budget" in answers:
            budget_map = {
                "low": 100,
                "mid": 200,
                "high": 400,
                "premium": None
            }
            budget = budget_map.get(answers["budget"])
            if budget:
                constraints["_budget_hard"] = budget

        return constraints
