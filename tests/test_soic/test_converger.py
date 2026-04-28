"""Tests for soic.converger — Decision engine with blocking dims, plateau, coverage."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.converger import Converger, Decision
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
    def test_plateau_detected(self):
        """mu stagnant over 3 iterations + same fail count → ABORT_PLATEAU.

        Plateau requires 3 data points (2 consecutive non-positive deltas).
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

        # Iteration 3: still same → 3 data points, plateau detected
        report3 = _make_report(
            [
                _gate("W-01", "D1", GateStatus.PASS, 10.0),
                _gate("W-05", "D4", GateStatus.FAIL, 0.0),
            ]
        )
        decision3 = conv.decide(report3, iteration=3)
        assert decision3 == Decision.ABORT_PLATEAU

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
