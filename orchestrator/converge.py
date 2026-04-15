"""Boucle de convergence — run → validate → auto_fix → re-validate.

Expose `ConvergeLoop`, qui relance une phase si sa gate échoue et applique
`nexos.auto_fixer.auto_fix` entre les tentatives (max 1 retry par défaut).
"""

from __future__ import annotations

import contextlib
from collections.abc import Callable
from pathlib import Path
from typing import Any

from nexos.logging_config import get_logger

from .gates import GateEngine, GateResult


class ConvergeLoop:
    """Boucle de convergence : relance une phase avec retry + auto_fix.

    Pattern: run → validate → auto_fix → re-validate (max 1 retry par défaut).
    """

    def __init__(self, gate_engine: GateEngine, max_retries: int = 1) -> None:
        self.gate_engine = gate_engine
        self.max_retries = max_retries
        self._log = get_logger("nexos.converge")

    def converge(
        self,
        transition: str,
        client_dir: Path,
        run_phase_fn: Callable[[Path], Any],
    ) -> GateResult:
        """Lance la phase, évalue la gate, relance avec auto_fix si échec.

        Args:
            transition: ex "ph1→ph2"
            client_dir: dossier client
            run_phase_fn: callable qui lance la phase (peut être rappelée)

        Returns:
            Le GateResult final (succès ou échec définitif).
        """
        run_phase_fn(client_dir)
        gate = self.gate_engine.evaluate(transition, client_dir)

        attempt = 0
        while not gate.passed and attempt < self.max_retries:
            attempt += 1
            self._log.warning(
                "Gate %s échoue (μ=%.2f), attempt %d/%d → auto_fix",
                transition,
                gate.mu,
                attempt,
                self.max_retries,
            )
            try:
                from nexos.auto_fixer import auto_fix

                from .brief import load_runtime_brief

                site_dir = client_dir / "site"
                brief_path = client_dir / "brief-client.json"
                brief_data = None
                if brief_path.exists():
                    with contextlib.suppress(Exception):
                        brief_data = load_runtime_brief(brief_path)
                if site_dir.exists():
                    auto_fix(site_dir, client_dir, brief_data)
            except Exception as e:
                self._log.error("auto_fix a levé: %s", e)
                break

            run_phase_fn(client_dir)
            gate = self.gate_engine.evaluate(transition, client_dir)

        return gate


__all__ = ["ConvergeLoop"]
