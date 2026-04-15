"""Tests unitaires des classes orchestrator (chantier2 phase O).

Valide le contrat des classes extraites de l'ancien god-object `orchestrator.py` :
- `PhaseStatus`, `GateResult`, `PhaseRun`, `PipelineContext` (dataclasses)
- `GateEngine` (évaluation SOIC + seuils)
- `ConvergeLoop` (boucle validate → auto_fix → re-validate)
- `PipelineOrchestrator` (facade mode → phases)

Les tests E2E (`test_e2e_orchestrator.py`) restent la source de vérité pour
le contrat CLI externe ; ici on couvre la logique OOP interne.
"""

from __future__ import annotations

import dataclasses
from pathlib import Path
from unittest.mock import patch

import pytest


def test_phase_status_values() -> None:
    from orchestrator import PhaseStatus

    assert PhaseStatus.PENDING.value == "pending"
    assert PhaseStatus.PASSED.value == "passed"
    assert PhaseStatus.FAILED.value == "failed"


def test_gate_result_immutable() -> None:
    from orchestrator import GateResult

    r = GateResult(phase="ph1→ph2", passed=True, mu=8.5, threshold=8.0)
    assert r.passed is True
    assert r.mu == 8.5
    with pytest.raises(dataclasses.FrozenInstanceError):
        r.passed = False  # type: ignore[misc]


def test_pipeline_context_record_and_update() -> None:
    from orchestrator import PhaseStatus, PipelineContext

    ctx = PipelineContext(mode="audit", client_dir=Path("/tmp/fake"))
    ctx.record("ph5-qa", PhaseStatus.RUNNING)
    assert len(ctx.runs) == 1
    assert ctx.runs[0].status is PhaseStatus.RUNNING

    ctx.record("ph5-qa", PhaseStatus.PASSED, retries=1)
    assert len(ctx.runs) == 1  # updated, not appended
    assert ctx.runs[0].status is PhaseStatus.PASSED
    assert ctx.runs[0].retries == 1


def test_gate_engine_thresholds() -> None:
    from orchestrator import GateEngine

    assert GateEngine.THRESHOLDS["ph0→ph1"] == 7.0
    assert GateEngine.THRESHOLDS["ph5→deploy"] == 8.5
    assert GateEngine.THRESHOLDS["ph4→tooling"] is None


def test_gate_engine_evaluate_pass(tmp_client_dir: Path) -> None:
    from orchestrator import GateEngine

    engine = GateEngine()
    with patch("soic.gate.evaluate_gate", return_value=9.1):
        result = engine.evaluate("ph1→ph2", tmp_client_dir)

    assert result.passed is True
    assert result.mu == 9.1
    assert result.threshold == 8.0


def test_gate_engine_evaluate_fail(tmp_client_dir: Path) -> None:
    from orchestrator import GateEngine

    engine = GateEngine()
    with patch("soic.gate.evaluate_gate", return_value=7.2):
        result = engine.evaluate("ph1→ph2", tmp_client_dir)

    assert result.passed is False
    assert result.mu == 7.2


def test_gate_engine_build_gate_uses_log_fallback(tmp_client_dir: Path) -> None:
    from orchestrator import GateEngine

    (tmp_client_dir / "ph4-build-log.md").write_text("BUILD PASS OK\n", encoding="utf-8")
    engine = GateEngine()
    result = engine.evaluate("ph4→tooling", tmp_client_dir)
    assert result.passed is True
    assert result.threshold == 0.0


def test_converge_loop_retries_on_failure(tmp_client_dir: Path) -> None:
    from orchestrator import ConvergeLoop, GateEngine, GateResult

    engine = GateEngine()
    loop = ConvergeLoop(engine, max_retries=1)
    phase_calls = {"n": 0}

    def fake_run(cd: Path) -> None:
        phase_calls["n"] += 1

    with (
        patch.object(
            GateEngine,
            "evaluate",
            side_effect=[
                GateResult("ph1→ph2", False, 7.0, 8.0),
                GateResult("ph1→ph2", True, 8.5, 8.0),
            ],
        ),
        patch("nexos.auto_fixer.auto_fix", return_value=None),
    ):
        result = loop.converge("ph1→ph2", tmp_client_dir, fake_run)

    assert result.passed is True
    assert phase_calls["n"] == 2  # initial run + 1 retry


def test_converge_loop_gives_up_after_max_retries(tmp_client_dir: Path) -> None:
    from orchestrator import ConvergeLoop, GateEngine, GateResult

    engine = GateEngine()
    loop = ConvergeLoop(engine, max_retries=1)

    def fake_run(cd: Path) -> None:
        pass

    with (
        patch.object(
            GateEngine,
            "evaluate",
            return_value=GateResult("ph1→ph2", False, 6.0, 8.0),
        ),
        patch("nexos.auto_fixer.auto_fix", return_value=None),
    ):
        result = loop.converge("ph1→ph2", tmp_client_dir, fake_run)

    assert result.passed is False


def test_pipeline_orchestrator_mode_unknown_raises() -> None:
    from orchestrator import PipelineOrchestrator

    orch = PipelineOrchestrator()
    with pytest.raises(ValueError, match="Mode inconnu"):
        orch.run("bogus", Path("/tmp"))


def test_pipeline_orchestrator_dry_run_skips_phases(tmp_client_dir: Path) -> None:
    from orchestrator import PhaseStatus, PipelineOrchestrator

    orch = PipelineOrchestrator(dry_run=True)
    ctx = orch.run("audit", tmp_client_dir)

    assert ctx.mode == "audit"
    assert len(ctx.runs) == 1
    assert ctx.runs[0].status is PhaseStatus.SKIPPED


def test_pipeline_orchestrator_run_delegates_to_run_pipeline(tmp_client_dir: Path) -> None:
    """PipelineOrchestrator.run() doit déléguer à run_pipeline (frontière E2E)."""
    from orchestrator import PhaseStatus, PipelineOrchestrator

    with patch("orchestrator.run_pipeline", return_value=None) as mock_rp:
        orch = PipelineOrchestrator()
        ctx = orch.run("audit", tmp_client_dir, url="https://example.com")

    assert mock_rp.called
    args, kwargs = mock_rp.call_args
    assert args[0] == "audit"
    assert Path(args[1]) == tmp_client_dir
    assert kwargs.get("url") == "https://example.com"
    assert all(r.status is PhaseStatus.PASSED for r in ctx.runs)
