"""Tests for soic.iterator.PhaseIterator — on_enriched_retry hook (P8.3).

The hook lets the NEXOS orchestrator branch a dimension-scoped auto_fix on
Decision.ENRICHED_RETRY without SOIC having any knowledge of NEXOS internals.
Calling protocol (verified here):

  1. Hook is invoked exactly when Decision.ENRICHED_RETRY fires.
  2. Hook receives the same PlateauDiagnosis as feedback_router.
  3. Hook is called AFTER diagnose_plateau and BEFORE rerun_phase.
  4. Hook is NOT called on ACCEPT / ITERATE / ABORT_*.
  5. Hook is optional — `on_enriched_retry=None` preserves P8.2 behavior.

The tests fake the GateEngine + RunStore via monkeypatch so we can drive
the Converger through controlled (mu, fail_count) trajectories that
trigger the plateau detection deterministically.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.converger import Decision, PlateauDiagnosis
from soic.iterator import PhaseIterator
from soic.models import GateResult, GateStatus, PhaseGateReport


def _gate(gate_id: str, dim: str, status: GateStatus, score: float) -> GateResult:
    return GateResult(
        gate_id=gate_id,
        name=f"test-{gate_id}",
        dimension=dim,
        status=status,
        score=score,
        evidence="synthetic",
        duration_ms=0,
        command="",
    )


def _plateau_report(mu_target: float, phase: str = "ph5-qa") -> PhaseGateReport:
    """Build a report whose μ lands near `mu_target` with a D8 fail.

    Coverage stays above 0.7 so the converger does not abort early on coverage.
    Two consecutive identical reports trigger the plateau path; a third makes
    the second ENRICHED_RETRY into ABORT_PLATEAU.
    """
    # Mix of pass + fail tuned so weighted mu ~ mu_target. We just need the
    # decision branch (FAIL on D8 + similar mu across runs).
    gates = [
        _gate("W-01", "D1", GateStatus.PASS, 10.0),
        _gate("W-02", "D2", GateStatus.PASS, 10.0),
        _gate("W-03", "D3", GateStatus.PASS, mu_target),
        _gate("W-05", "D4", GateStatus.PASS, mu_target),
        _gate("W-08", "D5", GateStatus.PASS, mu_target),
        _gate("W-10", "D6", GateStatus.PASS, mu_target),
        _gate("W-12", "D7", GateStatus.PASS, mu_target),
        _gate("W-14", "D8", GateStatus.FAIL, 3.0),  # blocking → prevents ACCEPT
        _gate("W-15", "D9", GateStatus.PASS, mu_target),
    ]
    report = PhaseGateReport(phase=phase)
    report.gates = gates
    report.compute_score()
    return report


class _FakeGateEngine:
    """Yields a deterministic sequence of reports — drives plateau detection."""

    def __init__(self, reports: list[PhaseGateReport]) -> None:
        self._reports = reports
        self._idx = 0

    def __call__(self, *_args, **_kwargs) -> "_FakeGateEngine":
        # PhaseIterator instantiates GateEngine inside the loop — re-return self
        # so each iteration grabs the next pre-computed report.
        return self

    def run_all_gates(self, iteration: int = 1) -> PhaseGateReport:
        report = self._reports[min(self._idx, len(self._reports) - 1)]
        self._idx += 1
        return report


class _FakeRunStore:
    """No-op RunStore so tests don't touch disk."""

    def __init__(self, *_args, **_kwargs) -> None:
        self.saved: list[PhaseGateReport] = []

    def save_run(self, report: PhaseGateReport) -> None:
        self.saved.append(report)


def _wire_fakes(monkeypatch, reports: list[PhaseGateReport]) -> _FakeRunStore:
    fake_engine = _FakeGateEngine(reports)
    monkeypatch.setattr("soic.iterator.GateEngine", fake_engine)
    fake_store = _FakeRunStore()
    monkeypatch.setattr("soic.iterator.RunStore", lambda *_a, **_kw: fake_store)
    return fake_store


def _build_plateau_iterator(
    monkeypatch,
    *,
    on_enriched_retry=None,
    tmp_path: Path,
) -> PhaseIterator:
    """3 identical reports → ITERATE, ITERATE, then plateau (ENRICHED_RETRY).

    The 3rd report yields ENRICHED_RETRY because Converger._is_plateau() checks
    the last 2 mu deltas (both ≤ 0) and fail_count non-decreasing. We pad with
    one extra report so the iterator can re-run after the hook fires.
    """
    reports = [
        _plateau_report(7.50),
        _plateau_report(7.50),
        _plateau_report(7.50),
        _plateau_report(7.50),  # post-hook re-run (may not be reached)
    ]
    _wire_fakes(monkeypatch, reports)
    return PhaseIterator(
        phase="ph5-qa",
        client_dir=str(tmp_path),
        max_iter=4,
        store=_FakeRunStore(),
        site_dir=str(tmp_path / "site"),
        on_enriched_retry=on_enriched_retry,
    )


class TestEnrichedRetryHookInvocation:
    """The plateau detector needs ≥ 3 iterations (mu_history has 3+ entries
    before _is_plateau() returns True). We therefore let rerun_phase return
    True for all but the final ABORT_PLATEAU iteration so the loop drives
    the converger through iter 1 (ITERATE) → iter 2 (ITERATE) → iter 3
    (ENRICHED_RETRY, hook fires) → iter 4 (ABORT_PLATEAU, break).
    """

    def test_hook_called_on_enriched_retry_with_plateau_diagnosis(self, tmp_path, monkeypatch):
        """Hook fires exactly when ENRICHED_RETRY fires and receives the same
        PlateauDiagnosis the FeedbackRouter consumes."""
        captured: list[PlateauDiagnosis] = []

        def hook(diag: PlateauDiagnosis) -> None:
            captured.append(diag)

        iterator = _build_plateau_iterator(monkeypatch, on_enriched_retry=hook, tmp_path=tmp_path)
        iterator.run(rerun_phase=lambda *_args: True)

        assert len(captured) == 1, f"Hook should fire exactly once, got {len(captured)}"
        diag = captured[0]
        assert isinstance(diag, PlateauDiagnosis)
        assert diag.phase == "ph5-qa"
        gate_ids = {a.gate_id for a in diag.failing_assertions}
        assert "W-14" in gate_ids, f"Expected W-14 in failing_assertions, got {gate_ids}"
        assert "D8" in diag.failing_dimensions

    def test_hook_optional_preserves_p82_behavior(self, tmp_path, monkeypatch):
        """on_enriched_retry=None: loop must behave exactly as in P8.2 — plateau
        detected, feedback enriched, rerun attempted. No crash, no skipped
        ENRICHED_RETRY decision."""
        iterator = _build_plateau_iterator(monkeypatch, on_enriched_retry=None, tmp_path=tmp_path)
        result = iterator.run(rerun_phase=lambda *_args: True)

        decisions = [it.decision for it in result.iterations]
        assert Decision.ENRICHED_RETRY in decisions, (
            f"Expected ENRICHED_RETRY in {decisions} even without hook (P8.2 behavior)"
        )

    def test_hook_not_called_on_non_plateau_decisions(self, tmp_path, monkeypatch):
        """Hook must NOT fire on ACCEPT, ITERATE, or ABORT_* decisions.

        Improving μ trajectory → ITERATE on early iters, plateau never reached
        because each delta is strictly positive.
        """
        captured: list[PlateauDiagnosis] = []

        def hook(diag: PlateauDiagnosis) -> None:
            captured.append(diag)

        improving_reports = [
            _plateau_report(7.0),
            _plateau_report(8.0),
            _plateau_report(8.6),
            _plateau_report(9.0),
        ]
        _wire_fakes(monkeypatch, improving_reports)
        iterator = PhaseIterator(
            phase="ph5-qa",
            client_dir=str(tmp_path),
            max_iter=4,
            store=_FakeRunStore(),
            site_dir=str(tmp_path / "site"),
            on_enriched_retry=hook,
        )
        iterator.run(rerun_phase=lambda *_args: True)

        assert captured == [], (
            f"Hook should never fire without ENRICHED_RETRY, got {len(captured)} call(s)"
        )

    def test_hook_called_before_rerun_phase(self, tmp_path, monkeypatch):
        """Temporal ordering: hook MUST run before the rerun_phase of the SAME
        iteration (so the host's dimension-scoped auto-fix has applied its
        filesystem changes before the LLM re-prompt sees them).

        We check this by verifying that the index of 'hook' in `call_order`
        is followed immediately by 'rerun' — not preceded by it within the
        same iteration window."""
        call_order: list[str] = []

        def hook(_diag: PlateauDiagnosis) -> None:
            call_order.append("hook")

        def rerun(_phase: str, _feedback: str, _iter: int) -> bool:
            call_order.append("rerun")
            return True  # keep loop going so plateau is reached at iter 3

        iterator = _build_plateau_iterator(monkeypatch, on_enriched_retry=hook, tmp_path=tmp_path)
        iterator.run(rerun_phase=rerun)

        assert "hook" in call_order, f"Hook never called, got {call_order}"
        hook_idx = call_order.index("hook")
        # The element immediately AFTER hook in call_order must be 'rerun',
        # proving hook fired before that same iteration's rerun_phase.
        assert hook_idx + 1 < len(call_order), (
            f"No rerun after hook — expected pattern [..., 'hook', 'rerun', ...], got {call_order}"
        )
        assert call_order[hook_idx + 1] == "rerun", (
            f"Hook must be immediately followed by rerun in same iteration, got {call_order}"
        )

    def test_hook_receives_same_diagnosis_as_feedback_router(self, tmp_path, monkeypatch):
        """The PlateauDiagnosis passed to the hook is the same snapshot that
        the FeedbackRouter uses to generate the enriched feedback. Ensures
        host's auto-fix and the LLM prompt see a coherent view of the plateau."""
        captured: list[PlateauDiagnosis] = []

        def hook(diag: PlateauDiagnosis) -> None:
            captured.append(diag)

        iterator = _build_plateau_iterator(monkeypatch, on_enriched_retry=hook, tmp_path=tmp_path)
        result = iterator.run(rerun_phase=lambda *_args: True)

        enriched = [it for it in result.iterations if it.decision == Decision.ENRICHED_RETRY]
        assert enriched, "Expected at least one ENRICHED_RETRY iteration"
        assert len(captured) == 1
        diag = captured[0]
        feedback = enriched[0].feedback
        for dim in diag.failing_dimensions:
            assert dim in feedback, (
                f"Hook diagnosis dim {dim} missing from feedback (out-of-sync state)"
            )
