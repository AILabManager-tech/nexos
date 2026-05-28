"""Pipeline orchestrator — façade OOP haut-niveau.

Expose :
- `PhaseStatus`: enum du statut d'une phase
- `PhaseRun`: dataclass d'état d'une phase pendant le run
- `PipelineContext`: contexte partagé (runs + options)
- `PipelineOrchestrator`: façade testable qui délègue à `run_pipeline`
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, ClassVar

from nexos.logging_config import get_logger

from .converge import ConvergeLoop
from .gates import GateEngine, GateResult


class PhaseStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PhaseRun:
    """État d'une phase pendant un run de pipeline."""

    phase_id: str
    status: PhaseStatus = PhaseStatus.PENDING
    gate_result: GateResult | None = None
    retries: int = 0
    error: str | None = None


@dataclass
class PipelineContext:
    """Contexte partagé entre les classes pendant un run."""

    mode: str
    client_dir: Path
    profile_name: str = "default"
    max_retries: int = 1
    dry_run: bool = False
    runs: list[PhaseRun] = field(default_factory=list)

    def record(self, phase_id: str, status: PhaseStatus, **kwargs: Any) -> None:
        """Ajoute ou met à jour une entrée phase."""
        existing = next((r for r in self.runs if r.phase_id == phase_id), None)
        if existing is not None:
            existing.status = status
            for k, v in kwargs.items():
                setattr(existing, k, v)
        else:
            self.runs.append(PhaseRun(phase_id=phase_id, status=status, **kwargs))


class PipelineOrchestrator:
    """Orchestration haut niveau du pipeline NEXOS.

    Façade OOP testable. Délègue l'exécution lourde à `run_pipeline()` qui
    reste la frontière mockée par les tests E2E (iso-comportement phase O).
    """

    PHASES_BY_MODE: ClassVar[dict[str, list[str]]] = {
        "create": [
            "ph0-discovery",
            "ph1-strategy",
            "ph2-design",
            "ph3-content",
            "ph4-build",
            "ph5-qa",
        ],
        "audit": ["ph5-qa"],
        "modify": ["site-update"],
        "content": ["ph3-content"],
        "analyze": ["ph0-discovery"],
    }

    def __init__(
        self,
        profile: str = "default",
        max_retries: int = 1,
        dry_run: bool = False,
    ) -> None:
        self.profile = profile
        self.max_retries = max_retries
        self.dry_run = dry_run
        self.gate_engine = GateEngine(profile=profile)
        self.converge_loop = ConvergeLoop(self.gate_engine, max_retries=max_retries)
        self._log = get_logger("nexos.pipeline")

    def run(
        self,
        mode: str,
        client_dir: Path,
        url: str | None = None,
        target_sections: list[str] | None = None,
        color_overrides: dict[str, str] | None = None,
    ) -> PipelineContext:
        """Point d'entrée principal. Retourne le contexte final (runs + statuts)."""
        phases = self.PHASES_BY_MODE.get(mode)
        if phases is None:
            raise ValueError(f"Mode inconnu: {mode}")

        ctx = PipelineContext(
            mode=mode,
            client_dir=client_dir,
            profile_name=self.profile,
            max_retries=self.max_retries,
            dry_run=self.dry_run,
        )
        self._log.info(
            "Pipeline %s start: client_dir=%s profile=%s",
            mode,
            client_dir,
            self.profile,
        )

        if self.dry_run:
            for phase_id in phases:
                ctx.record(phase_id, PhaseStatus.SKIPPED)
            self._log.info("Pipeline %s end (dry-run)", mode)
            return ctx

        # Lazy import through the package surface so monkeypatch on
        # `orchestrator.run_pipeline` (used by tests/conftest.py) is respected.
        import orchestrator as _pkg

        try:
            _pkg.run_pipeline(
                mode,
                client_dir,
                url=url,
                target_sections=target_sections,
                color_overrides=color_overrides,
            )
            for phase_id in phases:
                ctx.record(phase_id, PhaseStatus.PASSED)
        except Exception as e:
            self._log.exception("Pipeline %s: exception", mode)
            last = phases[-1] if phases else mode
            ctx.record(last, PhaseStatus.FAILED, error=str(e))

        self._log.info("Pipeline %s end", mode)
        return ctx


__all__ = [
    "PhaseRun",
    "PhaseStatus",
    "PipelineContext",
    "PipelineOrchestrator",
]
