"""Questionario per Keycaps"""
from typing import List, Dict, Any
from .switch_quiz import Question


class KeycapQuestionnaire:
    """Questionario per keycaps"""

    @staticmethod
    def get_questions() -> List[Question]:
        """Restituisce tutte le domande per Keycaps"""

        return [
            # Q1: Layout e compatibilità
            Question(
                id="layout",
                text="Che layout utilizza la tua tastiera?",
                type="multi_choice",
                options=[
                    {"value": "ANSI", "label": "ANSI (US standard)"},
                    {"value": "ISO", "label": "ISO (Enter verticale)"},
                    {"value": "ISO_IT", "label": "ISO-IT (con leggende italiane)"}
                ],
                constraint_mapping={
                    "ANSI": {"layout_support": ["ANSI"]},
                    "ISO": {"layout_support": ["ISO"]},
                    "ISO_IT": {"layout_support": ["ISO_IT"]}
                }
            ),

            # Q2: Materiale
            Question(
                id="material",
                text="Quale materiale preferisci?",
                type="single_choice",
                description="PBT è più durevole e resistente allo shine, "
                           "ABS ha colori più vividi",
                options=[
                    {"value": "pbt", "label": "PBT (texture matte, durevole)"},
                    {"value": "abs", "label": "ABS (colori vividi, smooth)"},
                    {"value": "pbt_doubleshot", "label": "PBT Doubleshot (leggende durature)"},
                    {"value": "abs_doubleshot", "label": "ABS Doubleshot"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "pbt": {"material_pbt": 1.0},
                    "abs": {"material_abs": 1.0},
                    "pbt_doubleshot": {"material_pbt": 1.0, "material_doubleshot": 1.0},
                    "abs_doubleshot": {"material_abs": 1.0, "material_doubleshot": 1.0},
                    "indifferent": {}
                }
            ),

            # Q3: Profilo
            Question(
                id="profile",
                text="Quale profilo di keycap preferisci?",
                type="single_choice",
                description="Il profilo determina altezza e sculpting dei keycaps",
                options=[
                    {"value": "cherry", "label": "Cherry (basso, typing confortevole)"},
                    {"value": "oem", "label": "OEM (standard, versatile)"},
                    {"value": "xda", "label": "XDA (uniforme, basso)"},
                    {"value": "sa", "label": "SA (alto, vintage)"},
                    {"value": "mt3", "label": "MT3 (ergonomico, deep dish)"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "cherry": {"profile_cherry": 1.0, "height_low": 1.0},
                    "oem": {"profile_oem": 1.0},
                    "xda": {"profile_xda": 1.0, "height_low": 1.0},
                    "sa": {"profile_sa": 1.0, "height_high": 1.0},
                    "mt3": {"profile_mt3": 1.0},
                    "indifferent": {}
                }
            ),

            # Q4: Stile estetico
            Question(
                id="aesthetic",
                text="Quale stile estetico preferisci?",
                type="multi_choice",
                options=[
                    {"value": "wob", "label": "WoB (White on Black)"},
                    {"value": "bow", "label": "BoW (Black on White)"},
                    {"value": "retro", "label": "Retro Beige"},
                    {"value": "minimal", "label": "Minimal/Mono"},
                    {"value": "pastello", "label": "Pastello"},
                    {"value": "vaporwave", "label": "Vaporwave"},
                    {"value": "any", "label": "Qualsiasi stile"}
                ]
            ),

            # Q5: Legending
            Question(
                id="legending",
                text="Che tipo di leggende preferisci?",
                type="single_choice",
                options=[
                    {"value": "doubleshot", "label": "Doubleshot (più durature)"},
                    {"value": "dyesub", "label": "Dye-sublimation (PBT, qualità alta)"},
                    {"value": "blank", "label": "Blank (senza leggende)"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "doubleshot": {"legend_doubleshot": 1.0},
                    "dyesub": {"material_dyesub": 1.0},
                    "blank": {},
                    "indifferent": {}
                }
            ),

            # Q6: Sound preference
            Question(
                id="sound",
                text="Che suono desideri dai keycaps?",
                type="single_choice",
                description="PBT spesso tende a thock, ABS sottile tende a clack",
                options=[
                    {"value": "thock", "label": "Thock (basso, pieno)"},
                    {"value": "clack", "label": "Clack (alto, secco)"},
                    {"value": "indifferent", "label": "Indifferente"}
                ],
                weight_mapping={
                    "thock": {"sound_thock": 1.0, "thickness_norm": 1.0},
                    "clack": {"sound_clack": 1.0},
                    "indifferent": {}
                }
            ),

            # Q7: Coverage necessaria
            Question(
                id="coverage",
                text="Di quale coverage hai bisogno?",
                type="multi_choice",
                options=[
                    {"value": "base", "label": "Base (60-65%)"},
                    {"value": "numpad", "label": "Numpad"},
                    {"value": "f13", "label": "F13 e tasti extra"},
                    {"value": "iso_kit", "label": "ISO Kit"},
                    {"value": "novelties", "label": "Novelties"}
                ],
                weight_mapping={
                    "numpad": {"includes_numpad": 1.0},
                    "iso_kit": {"includes_iso_kit": 1.0, "iso_enter": 1.0}
                }
            ),

            # Q8: Budget
            Question(
                id="budget",
                text="Qual è il tuo budget per i keycaps?",
                type="single_choice",
                options=[
                    {"value": "low", "label": "<50€ (base kit)"},
                    {"value": "mid", "label": "50-100€"},
                    {"value": "high", "label": "100-150€"},
                    {"value": "premium", "label": ">150€ (no limiti)"}
                ]
            ),

            # Q9: Disponibilità
            Question(
                id="availability",
                text="Preferisci set in stock o accetti group buy?",
                type="single_choice",
                options=[
                    {"value": "in_stock", "label": "Solo in stock (disponibilità immediata)"},
                    {"value": "both", "label": "Anche group buy (attesa 6-12 mesi)"}
                ],
                constraint_mapping={
                    "in_stock": {"stock_status": "in_stock"}
                }
            )
        ]

    @staticmethod
    def build_preference_vector(answers: Dict[str, Any]) -> Dict[str, float]:
        """Costruisce vettore preferenze da risposte"""
        preference_vector = {}
        questions = KeycapQuestionnaire.get_questions()

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

        return preference_vector

    @staticmethod
    def build_hard_constraints(answers: Dict[str, Any]) -> Dict[str, Any]:
        """Costruisce vincoli hard da risposte"""
        constraints = {}
        questions = KeycapQuestionnaire.get_questions()

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
                "low": 50,
                "mid": 100,
                "high": 150,
                "premium": None
            }
            budget = budget_map.get(answers["budget"])
            if budget:
                constraints["_budget_hard"] = budget

        return constraints
