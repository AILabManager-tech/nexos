"""Tests for soic.converger — Decision engine with blocking dims, plateau, coverage."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.converger import Converger, Decision, FailingAssertion, PlateauDiagnosis
from soic.feedback_router import FeedbackRouter
from soic.models import GateResult, GateStatus, PhaseGateReport


def _gate(gate_id: str, dim: str, status: GateStatus, score: float) -> GateResult:
    return GateResult(
        gate_id=gate_id,
        name=f"test-{gate_id}",
        dimension=dim,
        status=status,
        score=score,
        evidence="test",
        duration_ms=0,
        command="",
    )


def _make_report(gates: list[GateResult], phase: str = "ph5-qa") -> PhaseGateReport:
    """Build a report and compute its score."""
    report = PhaseGateReport(phase=phase)
    report.gates = gates
    report.compute_score()
    return report


class TestConvergerAccept:
    def test_all_pass_high_mu_accepts(self):
        """All PASS + mu >= threshold → ACCEPT."""
        conv = Converger(phase="ph5-qa", max_iter=4)
        report = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-02", "D2", GateStatus.PASS, 10.0),
                _gate("W-03", "D3", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.PASS, 10.0),
                _gate("W-08", "D5", GateStatus.PASS, 10.0),
                _gate("W-10", "D6", GateStatus.PASS, 10.0),
                _gate("W-12", "D7", GateStatus.PASS, 10.0),
                _gate("W-14", "D8", GateStatus.PASS, 10.0),
                _gate("W-15", "D9", GateStatus.PASS, 10.0),
            ]
        )
        assert report.mu >= 8.5
        decision = conv.decide(report, iteration=1)
        assert decision == Decision.ACCEPT


class TestConvergerBlocking:
    def test_d4_fail_blocks_accept(self):
        """D4 FAIL + high mu → NOT ACCEPT (blocking dimension)."""
        conv = Converger(phase="ph5-qa", max_iter=4)
        report = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-02", "D2", GateStatus.PASS, 10.0),
                _gate("W-03", "D3", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 3.0),
                _gate("W-08", "D5", GateStatus.PASS, 10.0),
                _gate("W-10", "D6", GateStatus.PASS, 10.0),
                _gate("W-12", "D7", GateStatus.PASS, 10.0),
                _gate("W-14", "D8", GateStatus.PASS, 10.0),
                _gate("W-15", "D9", GateStatus.PASS, 10.0),
            ]
        )
        decision = conv.decide(report, iteration=1)
        assert decision != Decision.ACCEPT

    def test_d8_fail_blocks_accept(self):
        """D8 FAIL + high mu → NOT ACCEPT (blocking dimension)."""
        conv = Converger(phase="ph5-qa", max_iter=4)
        report = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-02", "D2", GateStatus.PASS, 10.0),
                _gate("W-03", "D3", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.PASS, 10.0),
                _gate("W-08", "D5", GateStatus.PASS, 10.0),
                _gate("W-10", "D6", GateStatus.PASS, 10.0),
                _gate("W-12", "D7", GateStatus.PASS, 10.0),
                _gate("W-14", "D8", GateStatus.FAIL, 2.0),
                _gate("W-15", "D9", GateStatus.PASS, 10.0),
            ]
        )
        decision = conv.decide(report, iteration=1)
        assert decision != Decision.ACCEPT


class TestConvergerCoverage:
    def test_low_coverage_aborts_immediately(self):
        """Coverage < 0.7 → ABORT_LOW_COVERAGE on any iteration.

        Historical note: an earlier draft of this test (written 2026-03-04 in
        nexos_v.3.0 commit 49dd0f0) asserted iter-1 tolerance ("ITERATE on
        first iter to allow preflight"). That tolerance was never implemented
        in the Converger code (initial commit fc7ccdc of soic_v3 on
        2026-03-19, 15 days later, shipped the unconditional ABORT at
        converger.py:80-82). Commit c1ea513 explicitly noted this as a
        pre-existing unrelated failure.

        Design rationale validated in chantier mode B SESSION_03.5: preflight
        tooling now runs upstream of the Converger loop (phases.py:131-138),
        so a low-coverage signal at this point indicates a structural problem,
        not a missing preflight — abort is the correct decision.
        """
        conv = Converger(phase="ph5-qa", max_iter=4)
        # 1 PASS + 3 NOT_EXECUTED → coverage = 1/4 = 0.25
        report = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-08", "D5", GateStatus.NOT_EXECUTED, 0.0),
                _gate("W-10", "D6", GateStatus.NOT_EXECUTED, 0.0),
                _gate("W-11", "D6", GateStatus.NOT_EXECUTED, 0.0),
            ]
        )
        assert report.coverage < 0.7

        # Iter 1: aborts immediately on low coverage
        decision1 = Converger(phase="ph5-qa", max_iter=4).decide(report, iteration=1)
        assert decision1 == Decision.ABORT_LOW_COVERAGE

        # Iter 2: same outcome — coverage is unconditional
        decision2 = conv.decide(report, iteration=2)
        assert decision2 == Decision.ABORT_LOW_COVERAGE


class TestConvergerPlateau:
    def test_first_plateau_yields_enriched_retry(self):
        """3 data points showing plateau -> ENRICHED_RETRY (P8.2).

        Plateau requires 3 data points (2 consecutive non-positive deltas).
        Previously this returned ABORT_PLATEAU immediately; since P8.2 the
        first plateau triggers an informational retry pass before giving up.
        """
        conv = Converger(phase="ph5-qa", max_iter=5)

        # Iteration 1: stagnant mu, 1 fail
        report1 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        decision1 = conv.decide(report1, iteration=1)
        assert decision1 == Decision.ITERATE

        # Iteration 2: same mu, same fail count
        report2 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        decision2 = conv.decide(report2, iteration=2)
        assert decision2 == Decision.ITERATE  # Only 2 data points, no plateau yet

        # Iteration 3: still same → 3 data points, plateau detected → ENRICHED_RETRY
        report3 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        decision3 = conv.decide(report3, iteration=3)
        assert decision3 == Decision.ENRICHED_RETRY

    def test_second_plateau_yields_abort(self):
        """After ENRICHED_RETRY is consumed, a subsequent plateau aborts."""
        conv = Converger(phase="ph5-qa", max_iter=10)

        # Build up a 3-point plateau (i=1..3) -> ENRICHED_RETRY at i=3
        for i in range(1, 4):
            report = _make_report(
                [
                    _gate("W-01", "D1", GateStatus.PASS, 10.0),
                    _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                ]
            )
            d = conv.decide(report, iteration=i)
        assert d == Decision.ENRICHED_RETRY
        assert conv._enriched_retry_used is True

        # Iteration 4: still plateau → ABORT_PLATEAU (retry consumed)
        report4 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        decision4 = conv.decide(report4, iteration=4)
        assert decision4 == Decision.ABORT_PLATEAU

    def test_enriched_retry_offered_once_per_lifecycle(self):
        """`reset()` re-arms ENRICHED_RETRY for the next run."""
        conv = Converger(phase="ph5-qa", max_iter=10)
        for i in range(1, 4):
            conv.decide(
                _make_report(
                    [
                        _gate("W-01", "D1", GateStatus.PASS, 10.0),
                        _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                    ]
                ),
                iteration=i,
            )
        assert conv._enriched_retry_used is True

        conv.reset()
        assert conv._enriched_retry_used is False
        assert conv.diagnose_plateau() is None
        assert conv.mu_history == []
        assert conv.fail_history == []

    def test_diagnose_plateau_returns_none_before_plateau(self):
        """Before any plateau is detected, diagnose_plateau() returns None."""
        conv = Converger(phase="ph5-qa", max_iter=5)
        conv.decide(
            _make_report([_gate("W-01", "D1", GateStatus.PASS, 10.0)]),
            iteration=1,
        )
        assert conv.diagnose_plateau() is None

    def test_diagnose_plateau_captures_failing_dimensions(self):
        """The diagnosis exposes which dimensions are stuck failing."""
        conv = Converger(phase="ph5-qa", max_iter=5)
        for i in range(1, 4):
            conv.decide(
                _make_report(
                    [
                        _gate("W-01", "D1", GateStatus.PASS, 10.0),
                        _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                        _gate("W-14", "D8", GateStatus.FAIL, 3.0),
                    ]
                ),
                iteration=i,
            )

        diagnosis = conv.diagnose_plateau()
        assert isinstance(diagnosis, PlateauDiagnosis)
        # D4 + D8 (blocking dimensions) are reported
        assert set(diagnosis.failing_dimensions) == {"D4", "D8"}
        # Assertions are exposed with gate_id + dimension + score
        assertion_ids = {a.gate_id for a in diagnosis.failing_assertions}
        assert assertion_ids == {"W-05", "W-14"}
        assert all(isinstance(a, FailingAssertion) for a in diagnosis.failing_assertions)
        # Trajectory recorded
        assert len(diagnosis.mu_trajectory) == 3
        assert len(diagnosis.fail_trajectory) == 3
        assert diagnosis.phase == "ph5-qa"
        assert diagnosis.iteration == 3

    def test_diagnose_plateau_to_dict_is_json_safe(self):
        """`PlateauDiagnosis.to_dict()` produces a JSON-serialisable mapping."""
        import json

        conv = Converger(phase="ph5-qa", max_iter=5)
        for i in range(1, 4):
            conv.decide(
                _make_report(
                    [
                        _gate("W-01", "D1", GateStatus.PASS, 10.0),
                        _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                    ]
                ),
                iteration=i,
            )

        diagnosis = conv.diagnose_plateau()
        assert diagnosis is not None
        # Round-trip via json: any non-serialisable field would raise here.
        encoded = json.dumps(diagnosis.to_dict())
        decoded = json.loads(encoded)
        assert decoded["phase"] == "ph5-qa"
        assert decoded["failing_dimensions"] == ["D4"]
        assert decoded["failing_assertions"][0]["gate_id"] == "W-05"

    def test_summary_for_enriched_retry_is_informative(self):
        """`get_summary(ENRICHED_RETRY)` mentions the diagnostic step."""
        conv = Converger(phase="ph5-qa", max_iter=5)
        for i in range(1, 4):
            conv.decide(
                _make_report(
                    [
                        _gate("W-01", "D1", GateStatus.PASS, 10.0),
                        _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                    ]
                ),
                iteration=i,
            )
        summary = conv.get_summary(Decision.ENRICHED_RETRY, iteration=3)
        assert "ENRICHED_RETRY" in summary
        assert "diagnostic" in summary.lower() or "diagnosis" in summary.lower()

    def test_feedback_router_with_plateau_context(self):
        """FeedbackRouter.generate_with_plateau_context injects diagnosis prefix."""
        conv = Converger(phase="ph5-qa", max_iter=5)
        for i in range(1, 4):
            conv.decide(
                _make_report(
                    [
                        _gate("W-01", "D1", GateStatus.PASS, 10.0),
                        _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                    ]
                ),
                iteration=i,
            )
        diagnosis = conv.diagnose_plateau()
        assert diagnosis is not None

        last_report = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        out = FeedbackRouter().generate_with_plateau_context(last_report, diagnosis)
        assert "Plateau detecte" in out
        # The mu trajectory shows up so the LLM sees the stagnation pattern
        assert "Trajectoire mu" in out
        # The original feedback block follows
        assert "Corrections requises" in out or "Action" in out

    def test_stagnant_mu_fewer_fails_continues(self):
        """mu stagnant but fewer failures → NOT plateau (qualitative progress)."""
        conv = Converger(phase="ph5-qa", max_iter=4)

        # Iteration 1: 2 fails
        report1 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                _gate("W-06", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        conv.decide(report1, iteration=1)

        # Iteration 2: same mu but only 1 fail → not plateau
        report2 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
                _gate("W-06", "D4", GateStatus.PASS, 5.0),
            ]
        )
        decision2 = conv.decide(report2, iteration=2)
        assert decision2 != Decision.ABORT_PLATEAU


class TestConvergerMaxIter:
    def test_max_iter_abort(self):
        """Reaching max_iter → ABORT_MAX_ITER."""
        conv = Converger(phase="ph5-qa", max_iter=2)

        report1 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 2.0),
            ]
        )
        decision1 = conv.decide(report1, iteration=1)
        assert decision1 == Decision.ITERATE

        # Same but iteration=2 (max)
        report2 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 3.0),
            ]
        )
        decision2 = conv.decide(report2, iteration=2)
        assert decision2 in (Decision.ABORT_MAX_ITER, Decision.ABORT_PLATEAU)


class TestConvergerSummary:
    def test_summary_not_empty(self):
        """get_summary should return a non-empty string with mu info."""
        conv = Converger(phase="ph5-qa")
        report = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
            ]
        )
        decision = conv.decide(report, iteration=1)
        summary = conv.get_summary(decision, iteration=1)
        assert len(summary) > 0
        assert "mu=" in summary or "coverage" in summary.lower()
