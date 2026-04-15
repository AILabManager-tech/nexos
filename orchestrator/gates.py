"""Quality gates SOIC — évaluation des transitions entre phases.

Expose :
- `GateResult`: dataclass immuable du résultat d'une gate
- `GateEngine`: évalue une transition contre son seuil SOIC

Le nom `GateEngine` ne collide pas avec `soic.GateEngine` : ce dernier est
importé de manière function-locale dans les consommateurs (converge, iterator).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from nexos.logging_config import get_logger


@dataclass(frozen=True)
class GateResult:
    """Résultat d'évaluation d'une gate SOIC entre 2 phases."""

    phase: str
    passed: bool
    mu: float
    threshold: float
    dimensions: dict[str, float] = field(default_factory=dict)
    reason: str = ""


class GateEngine:
    """Évalue les quality gates SOIC entre phases.

    Responsabilités:
    - Exposer les seuils par transition (CLAUDE.md §QUALITY GATES)
    - Appeler soic.gate.evaluate_gate sur le répertoire client
    - Retourner un GateResult structuré
    """

    THRESHOLDS: ClassVar[dict[str, float | None]] = {
        "ph0→ph1": 7.0,
        "ph1→ph2": 8.0,
        "ph2→ph3": 8.0,
        "ph3→ph4": 8.0,
        "ph4→tooling": None,  # BUILD PASS, pas μ
        "ph5→deploy": 8.5,
    }

    def __init__(self, profile: str = "default") -> None:
        self.profile = profile
        self._log = get_logger("nexos.gate_engine")

    def evaluate(self, transition: str, client_dir: Path) -> GateResult:
        """Évalue une gate SOIC pour une transition donnée."""
        threshold = self.THRESHOLDS.get(transition)
        if threshold is None:
            return self._evaluate_build(client_dir, transition)

        try:
            from soic.gate import evaluate_gate
        except ImportError as e:
            self._log.error("soic.gate indisponible: %s", e)
            return GateResult(
                phase=transition,
                passed=False,
                mu=0.0,
                threshold=threshold,
                reason=f"soic import failed: {e}",
            )

        source_phase = transition.split("→")[0]
        try:
            mu = float(evaluate_gate(source_phase, client_dir))
        except Exception as e:
            self._log.exception("evaluate_gate a levé pour %s", transition)
            return GateResult(
                phase=transition,
                passed=False,
                mu=0.0,
                threshold=threshold,
                reason=f"evaluate_gate error: {e}",
            )

        passed = mu >= threshold
        self._log.info(
            "Gate %s : μ=%.2f (threshold=%.2f) → %s",
            transition,
            mu,
            threshold,
            "PASS" if passed else "FAIL",
        )
        return GateResult(
            phase=transition,
            passed=passed,
            mu=mu,
            threshold=threshold,
        )

    def _evaluate_build(self, client_dir: Path, transition: str) -> GateResult:
        """Gate ph4 : BUILD PASS binaire, pas de score μ."""
        site_dir = client_dir / "site"
        if not (site_dir / "package.json").exists():
            build_log = client_dir / "ph4-build-log.md"
            if build_log.exists():
                content = build_log.read_text(encoding="utf-8", errors="replace")
                ok = "BUILD PASS" in content or "build réussi" in content.lower()
            else:
                ok = True
            return GateResult(
                phase=transition,
                passed=ok,
                mu=10.0 if ok else 0.0,
                threshold=0.0,
                reason="" if ok else "BUILD FAIL (log-based fallback)",
            )

        try:
            from nexos.build_validator import validate_build
        except ImportError as e:
            self._log.error("nexos.build_validator indisponible: %s", e)
            return GateResult(
                phase=transition,
                passed=False,
                mu=0.0,
                threshold=0.0,
                reason=f"build_validator import failed: {e}",
            )

        result = validate_build(site_dir)
        ok = bool(result.overall_pass)
        return GateResult(
            phase=transition,
            passed=ok,
            mu=10.0 if ok else 0.0,
            threshold=0.0,
            reason="" if ok else "BUILD FAIL",
        )


__all__ = ["GateEngine", "GateResult"]
