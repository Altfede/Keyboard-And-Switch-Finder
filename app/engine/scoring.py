"""Motore di scoring con cosine similarity e sistema di pesatura"""
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from ..models.switch import Switch
from ..models.keycap import KeycapSet
from ..models.board import Board


class ScoringEngine:
    """Motore di scoring universale per tutti i tipi di prodotto"""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Inizializza il motore con pesi personalizzati

        Args:
            weights: Dizionario di pesi per ogni feature (default: pesi uniformi)
        """
        self.weights = weights or {}

    @staticmethod
    def cosine_similarity(vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """
        Calcola la similarità coseno tra due vettori sparsi

        Args:
            vec_a: Primo vettore (preferenze utente)
            vec_b: Secondo vettore (caratteristiche prodotto)

        Returns:
            Similarità coseno tra 0 e 1
        """
        # Trova tutte le chiavi comuni
        common_keys = set(vec_a.keys()) & set(vec_b.keys())

        if not common_keys:
            return 0.0

        # Costruisci array numpy solo per chiavi comuni
        a_values = np.array([vec_a[k] for k in common_keys])
        b_values = np.array([vec_b[k] for k in common_keys])

        # Calcola cosine similarity
        dot_product = np.dot(a_values, b_values)
        norm_a = np.linalg.norm(a_values)
        norm_b = np.linalg.norm(b_values)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def apply_weights(self, preference_vector: Dict[str, float]) -> Dict[str, float]:
        """
        Applica i pesi al vettore di preferenze

        Args:
            preference_vector: Vettore preferenze utente

        Returns:
            Vettore pesato
        """
        if not self.weights:
            return preference_vector

        weighted = {}
        for key, value in preference_vector.items():
            weight = self.weights.get(key, 1.0)
            weighted[key] = value * weight

        return weighted

    def calculate_hard_constraint_bonus(
        self,
        product_features: Dict[str, Any],
        hard_constraints: Dict[str, Any]
    ) -> float:
        """
        Calcola bonus/penalità per vincoli hard

        Args:
            product_features: Features del prodotto (modello completo)
            hard_constraints: Vincoli obbligatori dell'utente

        Returns:
            Bonus o penalità (può essere negativo)
        """
        bonus = 0.0

        for constraint_key, constraint_value in hard_constraints.items():
            product_value = product_features.get(constraint_key)

            if product_value is None:
                continue

            # Match esatto
            if isinstance(constraint_value, bool):
                if product_value == constraint_value:
                    bonus += 0.15
                else:
                    bonus -= 0.20

            # Match in lista
            elif isinstance(constraint_value, (list, set)):
                if isinstance(product_value, list):
                    # Intersezione non vuota
                    if set(constraint_value) & set(product_value):
                        bonus += 0.10
                    else:
                        bonus -= 0.15
                else:
                    if product_value in constraint_value:
                        bonus += 0.10
                    else:
                        bonus -= 0.15

            # Range numerico
            elif isinstance(constraint_value, dict) and 'min' in constraint_value:
                min_val = constraint_value.get('min', float('-inf'))
                max_val = constraint_value.get('max', float('inf'))
                if min_val <= product_value <= max_val:
                    bonus += 0.10
                else:
                    # Penalità proporzionale alla distanza
                    if product_value < min_val:
                        distance = (min_val - product_value) / min_val
                    else:
                        distance = (product_value - max_val) / max_val
                    bonus -= min(0.30, distance * 0.20)

        return bonus

    def score_product(
        self,
        product,
        preference_vector: Dict[str, float],
        hard_constraints: Dict[str, Any] = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calcola il punteggio per un singolo prodotto

        Args:
            product: Oggetto prodotto (Switch, KeycapSet, o Board)
            preference_vector: Vettore preferenze utente
            hard_constraints: Vincoli hard opzionali

        Returns:
            Tuple (punteggio_totale, breakdown_dettagliato)
        """
        # Ottieni feature vector del prodotto
        product_vector = product.to_feature_vector()

        # Applica pesi alle preferenze
        weighted_preferences = self.apply_weights(preference_vector)

        # Calcola similarità coseno
        cosine_score = self.cosine_similarity(weighted_preferences, product_vector)

        # Calcola bonus/penalità per hard constraints
        hard_bonus = 0.0
        if hard_constraints:
            product_dict = product.dict()
            hard_bonus = self.calculate_hard_constraint_bonus(product_dict, hard_constraints)

        # Punteggio finale
        total_score = cosine_score + hard_bonus

        # Breakdown dettagliato per spiegabilità
        breakdown = {
            "cosine_similarity": cosine_score,
            "hard_constraints_bonus": hard_bonus,
            "total": total_score
        }

        # Aggiungi contributi individuali delle features
        for key in weighted_preferences.keys():
            if key in product_vector:
                contribution = weighted_preferences[key] * product_vector[key]
                if abs(contribution) > 0.01:  # Solo contributi significativi
                    breakdown[f"feature_{key}"] = contribution

        return total_score, breakdown

    def rank_products(
        self,
        products: List[Any],
        preference_vector: Dict[str, float],
        hard_constraints: Dict[str, Any] = None,
        top_n: int = 5,
        diversity_threshold: float = 0.15
    ) -> List[Tuple[Any, float, Dict[str, float]]]:
        """
        Classifica e filtra prodotti per diversità

        Args:
            products: Lista di prodotti da classificare
            preference_vector: Vettore preferenze utente
            hard_constraints: Vincoli hard opzionali
            top_n: Numero di risultati da restituire
            diversity_threshold: Soglia di diversità (0-1)

        Returns:
            Lista di tuple (prodotto, score, breakdown) ordinate per score
        """
        # Calcola score per tutti i prodotti
        scored_products = []
        for product in products:
            score, breakdown = self.score_product(
                product,
                preference_vector,
                hard_constraints
            )
            scored_products.append((product, score, breakdown))

        # Ordina per score decrescente
        scored_products.sort(key=lambda x: x[1], reverse=True)

        # Filtra per diversità
        diverse_results = []
        for product, score, breakdown in scored_products:
            if len(diverse_results) >= top_n:
                break

            # Se è il primo o sufficientemente diverso dagli altri
            if not diverse_results:
                diverse_results.append((product, score, breakdown))
            else:
                # Controlla diversità rispetto ai già selezionati
                product_vec = product.to_feature_vector()
                is_diverse = True

                for selected_product, _, _ in diverse_results:
                    selected_vec = selected_product.to_feature_vector()
                    similarity = self.cosine_similarity(product_vec, selected_vec)

                    if similarity > (1.0 - diversity_threshold):
                        is_diverse = False
                        break

                if is_diverse:
                    diverse_results.append((product, score, breakdown))

        return diverse_results

    def explain_score(
        self,
        breakdown: Dict[str, float],
        product_name: str,
        top_features: int = 5
    ) -> str:
        """
        Genera spiegazione human-readable del punteggio

        Args:
            breakdown: Breakdown del punteggio
            product_name: Nome del prodotto
            top_features: Numero di features da mostrare

        Returns:
            Stringa di spiegazione
        """
        explanation = [f"Punteggio per {product_name}:"]

        # Cosine similarity base
        explanation.append(f"  • Similarità base: +{breakdown['cosine_similarity']:.2f}")

        # Hard constraints bonus
        if breakdown.get('hard_constraints_bonus', 0) != 0:
            bonus = breakdown['hard_constraints_bonus']
            sign = "+" if bonus >= 0 else ""
            explanation.append(f"  • Vincoli obbligatori: {sign}{bonus:.2f}")

        # Top contributing features
        feature_contributions = {
            k: v for k, v in breakdown.items()
            if k.startswith('feature_')
        }

        if feature_contributions:
            sorted_features = sorted(
                feature_contributions.items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )[:top_features]

            explanation.append("  • Contributi principali:")
            for feature_key, contribution in sorted_features:
                feature_name = feature_key.replace('feature_', '').replace('_', ' ')
                sign = "+" if contribution >= 0 else ""
                explanation.append(f"    - {feature_name}: {sign}{contribution:.2f}")

        # Totale
        explanation.append(f"  • TOTALE: {breakdown['total']:.2f}")

        return "\n".join(explanation)


class WeightPresets:
    """Preset di pesi per diversi use case"""

    @staticmethod
    def gaming_competitive() -> Dict[str, float]:
        """Preset per gaming competitivo"""
        return {
            "feel_linear": 2.0,
            "actuation_force_norm": 1.5,
            "smoothness": 2.0,
            "low_latency": 2.5,
            "mount_tray": 1.5,  # Più rigido
            "stability": 2.0,
            "nkro": 1.5,
        }

    @staticmethod
    def typing_comfort() -> Dict[str, float]:
        """Preset per scrittura confortevole"""
        return {
            "feel_tactile": 2.0,
            "sound_thock": 1.5,
            "mount_gasket": 2.0,
            "smoothness": 2.0,
            "case_pc": 1.5,
            "plate_pc": 1.5,
            "profile_cherry": 1.5,
        }

    @staticmethod
    def silent_office() -> Dict[str, float]:
        """Preset per ufficio silenzioso"""
        return {
            "silent": 3.0,
            "sound_muted": 2.5,
            "has_foam": 2.0,
            "feel_linear": 1.5,
            "sound_level": -2.0,  # Penalità per rumore alto
        }

    @staticmethod
    def premium_build() -> Dict[str, float]:
        """Preset per build premium"""
        return {
            "mount_gasket": 2.0,
            "case_aluminum": 1.5,
            "stabs_screw_in": 2.0,
            "stabs_lubed": 1.5,
            "hot_swap_5pin": 1.5,
            "qmk_via": 1.5,
            "material_doubleshot": 2.0,
            "legend_quality_norm": 2.0,
        }

    @staticmethod
    def budget_conscious() -> Dict[str, float]:
        """Preset per budget limitato"""
        return {
            "prebuilt": 1.5,
            # Penalizza features costose
            "case_aluminum": -1.0,
            "rgb_per_key": -0.5,
        }

    @staticmethod
    def get_preset(preset_name: str) -> Dict[str, float]:
        """Ottiene un preset per nome"""
        presets = {
            "gaming": WeightPresets.gaming_competitive(),
            "typing": WeightPresets.typing_comfort(),
            "silent": WeightPresets.silent_office(),
            "premium": WeightPresets.premium_build(),
            "budget": WeightPresets.budget_conscious(),
        }
        return presets.get(preset_name, {})
