"""Tests for soic.models — GateStatus, GateResult, PhaseGateReport, SOICScore."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.models import GateResult, GateStatus, PhaseGateReport


def _gate(gate_id: str, dim: str, status: GateStatus, score: float) -> GateResult:
    """Helper to create a GateResult quickly."""
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


class TestGateStatus:
    def test_not_executed_exists(self):
        assert hasattr(GateStatus, "NOT_EXECUTED")
        assert GateStatus.NOT_EXECUTED.value == "NOT_EXECUTED"

    def test_all_statuses(self):
        expected = {"PASS", "FAIL", "SKIP", "ERROR", "NOT_EXECUTED"}
        actual = {s.value for s in GateStatus}
        assert actual == expected


class TestPhaseGateReport:
    def test_compute_score_basic(self):
        """All PASS gates → mu reflects weighted average across ALL 9 dimensions.

        With only D1/D2/D3 populated (10.0 each), D4-D9 default to 0.0,
        so mu ≈ (10*1.0 + 10*1.0 + 10*0.8) / 8.0 = 3.5.
        """
        report = PhaseGateReport(phase="ph5-qa")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-02", "D2", GateStatus.PASS, 10.0),
            _gate("W-03", "D3", GateStatus.PASS, 10.0),
        ]
        score = report.compute_score()
        assert report.mu >= 3.0  # 3/9 dims = partial coverage, mu = 3.0
        assert score.passed == 3
        assert score.failed == 0
        assert score.coverage == 1.0

    def test_not_executed_scores_zero(self):
        """NOT_EXECUTED gates should score 0.0, not 5.0."""
        report = PhaseGateReport(phase="ph5-qa")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate(
                "W-08",
                "D5",
                GateStatus.NOT_EXECUTED,
                0.0,
            ),
        ]
        score = report.compute_score()
        assert score.not_executed == 1
        # D5 should be 0.0, not 5.0
        assert report.dimension_scores.get("D5", 999) == 0.0

    def test_coverage_with_not_executed(self):
        """Coverage should reflect actually executed gates."""
        report = PhaseGateReport(phase="ph5-qa")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-08", "D5", GateStatus.NOT_EXECUTED, 0.0),
            _gate("W-10", "D6", GateStatus.NOT_EXECUTED, 0.0),
        ]
        report.compute_score()
        # 1 executed out of 3 (NOT_EXECUTED ≠ SKIP)
        assert report.coverage < 0.7
        assert abs(report.coverage - 1 / 3) < 0.01

    def test_skip_excluded_from_scoring(self):
        """SKIP gates should be excluded from dimension scoring (not count as 0)."""
        report = PhaseGateReport(phase="ph5-qa")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-02", "D2", GateStatus.SKIP, 5.0),  # Should be excluded from scoring
        ]
        score = report.compute_score()
        assert score.skipped == 1
        # Coverage = actually_ran / total_gates = 1/2 = 0.5
        assert abs(report.coverage - 0.5) < 0.01

    def test_fail_count_property(self):
        """fail_count should count FAIL + ERROR."""
        report = PhaseGateReport(phase="ph5-qa")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-05", "D4", GateStatus.FAIL, 2.0),
            _gate("W-06", "D4", GateStatus.ERROR, 0.0),
            _gate("W-10", "D6", GateStatus.NOT_EXECUTED, 0.0),
        ]
        assert report.fail_count == 2

    def test_mixed_pass_fail_not_executed(self):
        """Mix of all statuses: verify aggregation."""
        report = PhaseGateReport(phase="ph5-qa")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-05", "D4", GateStatus.FAIL, 3.0),
            _gate("W-08", "D5", GateStatus.NOT_EXECUTED, 0.0),
            _gate("W-02", "D2", GateStatus.SKIP, 5.0),
        ]
        score = report.compute_score()
        assert score.passed == 1
        assert score.failed == 1
        assert score.skipped == 1
        assert score.not_executed == 1
        assert score.total_gates == 4
        # Coverage = actually_ran / total_gates = 2/4 = 0.5
        assert abs(report.coverage - 0.5) < 0.01

    def test_to_dict(self):
        """to_dict should contain all fields."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [_gate("W-01", "D1", GateStatus.PASS, 10.0)]
        report.compute_score()
        d = report.to_dict()
        assert "coverage" in d
        assert "mu" in d
        assert "gates" in d
        assert len(d["gates"]) == 1
