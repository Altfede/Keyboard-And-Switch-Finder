"""Sistema di compatibilità e validazione tra componenti"""
from typing import List, Dict, Any, Optional
from ..models.switch import Switch
from ..models.keycap import KeycapSet
from ..models.board import Board


class CompatibilityIssue:
    """Rappresenta un problema di compatibilità"""

    def __init__(
        self,
        severity: str,  # "error", "warning", "info"
        category: str,
        message: str,
        solution: Optional[str] = None
    ):
        self.severity = severity
        self.category = category
        self.message = message
        self.solution = solution

    def to_dict(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "solution": self.solution
        }


class CompatibilityChecker:
    """Verifica compatibilità tra Board, Switch e Keycaps"""

    @staticmethod
    def check_board_switch_compatibility(
        board: Board,
        switch: Switch
    ) -> List[CompatibilityIssue]:
        """
        Verifica compatibilità tra board e switch

        Args:
            board: Tastiera
            switch: Switch

        Returns:
            Lista di problemi di compatibilità
        """
        issues = []

        # Check 1: Hot-swap pin compatibility
        if board.hot_swap:
            if board.hot_swap_pin_support == 3 and switch.pin_count == 5:
                issues.append(CompatibilityIssue(
                    severity="error",
                    category="pins",
                    message=f"La board {board.name} supporta solo switch 3-pin, "
                           f"ma {switch.name} è 5-pin.",
                    solution="Puoi tagliare i 2 pin plastici dello switch (operazione "
                            "irreversibile) oppure scegliere uno switch 3-pin."
                ))
            elif board.hot_swap_pin_support == 5 and switch.pin_count == 3:
                issues.append(CompatibilityIssue(
                    severity="info",
                    category="pins",
                    message=f"La board {board.name} supporta 5-pin ma {switch.name} "
                           f"è 3-pin.",
                    solution="Gli switch 3-pin funzionano su board 5-pin, ma potrebbero "
                            "essere meno stabili. Considera di usare switch 5-pin per "
                            "maggiore stabilità."
                ))
        else:
            # Board non hot-swap, switch devono essere saldati
            if switch.pin_count not in [3, 5]:
                issues.append(CompatibilityIssue(
                    severity="error",
                    category="pins",
                    message=f"{switch.name} non è compatibile con saldatura standard.",
                    solution="Usa switch MX-compatibili standard."
                ))

        # Check 2: MX compatibility
        if not switch.mx_compatible:
            issues.append(CompatibilityIssue(
                severity="error",
                category="stem",
                message=f"{switch.name} non ha stem MX-compatibile.",
                solution="La maggior parte dei keycaps non sarà compatibile."
            ))

        return issues

    @staticmethod
    def check_board_keycap_compatibility(
        board: Board,
        keycaps: KeycapSet
    ) -> List[CompatibilityIssue]:
        """
        Verifica compatibilità tra board e keycaps

        Args:
            board: Tastiera
            keycaps: Set di keycaps

        Returns:
            Lista di problemi di compatibilità
        """
        issues = []

        # Check 1: Layout compatibility
        board_layouts = set(board.layout)
        keycap_layouts = set(keycaps.layout_support)

        if not (board_layouts & keycap_layouts):
            issues.append(CompatibilityIssue(
                severity="error",
                category="layout",
                message=f"Layout incompatibile: board supporta {board.layout}, "
                       f"keycaps supportano {keycaps.layout_support}.",
                solution="Scegli keycaps che supportano il layout della tua board."
            ))

        # Check 2: ISO-IT specifico
        if "ISO_IT" in board.layout and "ISO_IT" not in keycaps.layout_support:
            issues.append(CompatibilityIssue(
                severity="warning",
                category="layout",
                message="La board richiede ISO-IT ma i keycaps non includono "
                       "leggende italiane.",
                solution="Puoi comunque usare i keycaps con layout ISO generico, "
                        "ma le leggende saranno in inglese o altre lingue."
            ))

        # Check 3: ISO enter key
        if "ISO" in board_layouts and not keycaps.iso_enter:
            issues.append(CompatibilityIssue(
                severity="error",
                category="keys",
                message="Board ISO ma keycaps non includono tasto ISO Enter.",
                solution="Scegli un set con supporto ISO completo."
            ))

        # Check 4: Numpad coverage
        if board.has_numpad and not keycaps.includes_numpad:
            issues.append(CompatibilityIssue(
                severity="warning",
                category="coverage",
                message=f"{board.name} ha numpad ma {keycaps.name} non lo include.",
                solution="Dovrai acquistare un kit numpad separato o scegliere "
                        "un set più completo."
            ))

        # Check 5: Bottom row compatibility
        # Assumiamo che la maggior parte delle board moderne usi 6.25u
        # ma potremmo estendere con più dettagli nel modello Board
        if not keycaps.bottom_row_6_25u:
            issues.append(CompatibilityIssue(
                severity="warning",
                category="bottom_row",
                message="I keycaps potrebbero non avere la barra spaziatrice 6.25u "
                       "standard.",
                solution="Verifica le dimensioni della bottom row della tua board."
            ))

        # Check 6: MX stem compatibility
        if not keycaps.mx_compatible:
            issues.append(CompatibilityIssue(
                severity="error",
                category="stem",
                message=f"{keycaps.name} non è compatibile con switch MX.",
                solution="Questi keycaps richiedono switch con stem diverso."
            ))

        return issues

    @staticmethod
    def check_keycap_switch_compatibility(
        keycaps: KeycapSet,
        switch: Switch,
        board: Optional[Board] = None
    ) -> List[CompatibilityIssue]:
        """
        Verifica compatibilità tra keycaps e switch (considerando anche PCB orientation)

        Args:
            keycaps: Set di keycaps
            switch: Switch
            board: Board opzionale per check PCB orientation

        Returns:
            Lista di problemi di compatibilità
        """
        issues = []

        # Check 1: North-facing interference
        if board and board.pcb_orientation == "north_facing":
            # Profili Cherry e OEM con north-facing possono interferire
            interference_profiles = ["cherry", "oem"]
            if keycaps.profile.lower() in interference_profiles:
                if not keycaps.north_facing_compatible:
                    issues.append(CompatibilityIssue(
                        severity="warning",
                        category="interference",
                        message=f"Profilo {keycaps.profile} su PCB north-facing "
                               f"può causare interferenza con switch lunghi.",
                        solution="Scegli keycaps con profilo più alto (XDA, SA) "
                                "o switch con stem più corto, oppure verifica "
                                "che questi keycaps siano testati per north-facing."
                    ))

        # Check 2: Stem fit
        if keycaps.stem_fit == "tight" and switch.stem_wobble_xy > 3.0:
            issues.append(CompatibilityIssue(
                severity="info",
                category="fit",
                message=f"{keycaps.name} ha fit stretto, potrebbe ridurre il wobble "
                       f"di {switch.name}.",
                solution="Questo è generalmente un vantaggio."
            ))
        elif keycaps.stem_fit == "loose" and switch.stem_wobble_xy > 4.0:
            issues.append(CompatibilityIssue(
                severity="warning",
                category="fit",
                message=f"{keycaps.name} ha fit largo e {switch.name} ha già wobble "
                       f"elevato.",
                solution="La combinazione potrebbe risultare in keycaps instabili. "
                        "Considera keycaps con fit più stretto."
            ))

        return issues

    @staticmethod
    def check_full_build_compatibility(
        board: Board,
        switch: Switch,
        keycaps: KeycapSet
    ) -> Dict[str, Any]:
        """
        Verifica compatibilità completa di un build

        Args:
            board: Tastiera
            switch: Switch
            keycaps: Set di keycaps

        Returns:
            Dizionario con tutti i check e problemi
        """
        all_issues = []

        # Check board-switch
        all_issues.extend(
            CompatibilityChecker.check_board_switch_compatibility(board, switch)
        )

        # Check board-keycaps
        all_issues.extend(
            CompatibilityChecker.check_board_keycap_compatibility(board, keycaps)
        )

        # Check keycaps-switch (con board context)
        all_issues.extend(
            CompatibilityChecker.check_keycap_switch_compatibility(
                keycaps, switch, board
            )
        )

        # Categorizza per severity
        errors = [i for i in all_issues if i.severity == "error"]
        warnings = [i for i in all_issues if i.severity == "warning"]
        infos = [i for i in all_issues if i.severity == "info"]

        # Determina compatibilità generale
        is_compatible = len(errors) == 0
        has_warnings = len(warnings) > 0

        return {
            "compatible": is_compatible,
            "has_warnings": has_warnings,
            "errors": [e.to_dict() for e in errors],
            "warnings": [w.to_dict() for w in warnings],
            "info": [i.to_dict() for i in infos],
            "summary": f"Build {'✓ compatibile' if is_compatible else '✗ incompatibile'}"
                      f"{' (con avvisi)' if has_warnings else ''}"
        }

    @staticmethod
    def suggest_alternatives(
        board: Board,
        switch: Switch,
        keycaps: KeycapSet,
        all_switches: List[Switch],
        all_keycaps: List[KeycapSet]
    ) -> Dict[str, List[Any]]:
        """
        Suggerisce alternative compatibili se ci sono problemi

        Args:
            board: Board attuale
            switch: Switch attuale
            keycaps: Keycaps attuali
            all_switches: Database di tutti gli switch
            all_keycaps: Database di tutti i keycaps

        Returns:
            Dizionario con suggerimenti di alternative
        """
        compatibility = CompatibilityChecker.check_full_build_compatibility(
            board, switch, keycaps
        )

        if compatibility["compatible"] and not compatibility["has_warnings"]:
            return {"switches": [], "keycaps": [], "message": "Build già compatibile!"}

        suggestions = {"switches": [], "keycaps": [], "reasons": []}

        # Se ci sono errori di pin
        pin_errors = [e for e in compatibility["errors"] if e["category"] == "pins"]
        if pin_errors and board.hot_swap:
            # Suggerisci switch con pin count corretto
            compatible_switches = [
                s for s in all_switches
                if s.pin_count == board.hot_swap_pin_support
            ][:3]
            suggestions["switches"].extend(compatible_switches)
            suggestions["reasons"].append("Compatibilità pin")

        # Se ci sono errori di layout
        layout_errors = [e for e in compatibility["errors"] if e["category"] == "layout"]
        if layout_errors:
            # Suggerisci keycaps con layout compatibile
            board_layouts = set(board.layout)
            compatible_keycaps = [
                k for k in all_keycaps
                if board_layouts & set(k.layout_support)
            ][:3]
            suggestions["keycaps"].extend(compatible_keycaps)
            suggestions["reasons"].append("Compatibilità layout")

        return suggestions
