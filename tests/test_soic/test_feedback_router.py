"""Tests for soic.feedback_router — Prioritized feedback generation."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.feedback_router import MAX_FEEDBACK_ITEMS, FeedbackRouter
from soic.models import GateResult, GateStatus, PhaseGateReport


def _gate(
    gate_id: str, dim: str, status: GateStatus, score: float, evidence: str = "test"
) -> GateResult:
    return GateResult(
        gate_id=gate_id,
        name=f"test-{gate_id}",
        dimension=dim,
        status=status,
        score=score,
        evidence=evidence,
        duration_ms=0,
        command="",
    )


def _make_report(gates: list[GateResult]) -> PhaseGateReport:
    report = PhaseGateReport(phase="ph5-qa")
    report.gates = gates
    report.compute_score()
    return report


class TestFeedbackMaxItems:
    def test_max_5_items_from_16_fails(self):
        """16 FAIL gates → max 5 in feedback output."""
        gates = []
        dims = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"]
        for i in range(16):
            dim = dims[i % len(dims)]
            gates.append(_gate(f"W-{i + 1:02d}", dim, GateStatus.FAIL, float(i), f"issue {i}"))

        report = _make_report(gates)
        router = FeedbackRouter()
        feedback = router.generate(report)

        # Count the number of gate entries in feedback
        gate_entries = [line for line in feedback.split("\n") if line.startswith("[D")]
        assert len(gate_entries) <= MAX_FEEDBACK_ITEMS

    def test_deferred_count_shown(self):
        """When more than 5 failures, deferred count should be mentioned."""
        gates = [
            _gate(f"W-{i + 1:02d}", f"D{(i % 9) + 1}", GateStatus.FAIL, float(i)) for i in range(10)
        ]
        report = _make_report(gates)
        router = FeedbackRouter()
        feedback = router.generate(report)
        assert "corrections" in feedback.lower() and "reportee" in feedback.lower()


class TestFeedbackPriority:
    def test_d4_d8_always_included(self):
        """D4 and D8 failures should always be in feedback even with high scores."""
        gates = [
            # D4 and D8 with high scores (but still FAIL)
            _gate("W-05", "D4", GateStatus.FAIL, 7.0, "security issue"),
            _gate("W-14", "D8", GateStatus.FAIL, 7.0, "legal issue"),
            # Other dims with lower scores
            _gate("W-01", "D1", GateStatus.FAIL, 1.0, "low score 1"),
            _gate("W-02", "D2", GateStatus.FAIL, 1.0, "low score 2"),
            _gate("W-03", "D3", GateStatus.FAIL, 1.0, "low score 3"),
            _gate("W-12", "D7", GateStatus.FAIL, 1.0, "low score 4"),
            _gate("W-15", "D9", GateStatus.FAIL, 1.0, "low score 5"),
        ]
        report = _make_report(gates)
        router = FeedbackRouter()
        feedback = router.generate(report)

        # D4 and D8 must appear in feedback
        assert "D4" in feedback
        assert "D8" in feedback

    def test_priority_order(self):
        """CRITIQUE (D4/D8) should appear before HAUTE (D5/D6) before NORMALE."""
        gates = [
            _gate("W-15", "D9", GateStatus.FAIL, 3.0, "lint error"),
            _gate("W-05", "D4", GateStatus.FAIL, 3.0, "security"),
            _gate("W-08", "D5", GateStatus.FAIL, 3.0, "perf"),
        ]
        report = _make_report(gates)
        router = FeedbackRouter()
        feedback = router.generate(report)

        # D4 should appear before D5, D5 before D9
        d4_pos = feedback.find("D4")
        d5_pos = feedback.find("D5")
        d9_pos = feedback.find("D9")
        assert d4_pos < d5_pos < d9_pos


class TestFeedbackAllPass:
    def test_no_feedback_when_all_pass(self):
        """All PASS → feedback says no action needed."""
        gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-02", "D2", GateStatus.PASS, 10.0),
        ]
        report = _make_report(gates)
        router = FeedbackRouter()
        feedback = router.generate(report)
        assert "no corrective action" in feedback.lower() or "all gates passed" in feedback.lower()


class TestFeedbackFormat:
    def test_feedback_contains_dimension_and_gate(self):
        """Feedback lines should contain [DX/W-XX] format."""
        gates = [
            _gate("W-05", "D4", GateStatus.FAIL, 3.0, "vuln found"),
        ]
        report = _make_report(gates)
        router = FeedbackRouter()
        feedback = router.generate(report)
        assert "[D4/W-05]" in feedback

    def test_generate_full_includes_all(self):
        """generate_full() should include ALL failed gates, not just top 5."""
        gates = [
            _gate(f"W-{i + 1:02d}", f"D{(i % 9) + 1}", GateStatus.FAIL, float(i)) for i in range(10)
        ]
        report = _make_report(gates)
        router = FeedbackRouter()
        full = router.generate_full(report)

        # All 10 gates should appear
        for i in range(10):
            assert f"W-{i + 1:02d}" in full
