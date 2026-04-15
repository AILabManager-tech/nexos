"""Tests for soic.report — Report generation with NOT_EXECUTED and coverage."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.models import GateResult, GateStatus, PhaseGateReport
from soic.report import generate_report_v2


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


class TestReportNotExecuted:
    def test_not_executed_icon(self):
        """NOT_EXECUTED gates should show ? icon in the report."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-08", "D5", GateStatus.NOT_EXECUTED, 0.0, "tooling missing"),
        ]
        report.compute_score()
        text = generate_report_v2(report)
        assert "? W-08" in text

    def test_pass_icon(self):
        """PASS gates should show + icon."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [_gate("W-01", "D1", GateStatus.PASS, 10.0)]
        report.compute_score()
        text = generate_report_v2(report)
        assert "+ W-01" in text


class TestReportCoverage:
    def test_coverage_displayed(self):
        """Coverage percentage should appear in the report."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-08", "D5", GateStatus.NOT_EXECUTED, 0.0),
        ]
        report.compute_score()
        text = generate_report_v2(report)
        assert "Coverage" in text or "coverage" in text

    def test_incomplete_verdict_low_coverage(self):
        """Coverage < 0.7 should show INCOMPLETE verdict."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-08", "D5", GateStatus.NOT_EXECUTED, 0.0),
            _gate("W-10", "D6", GateStatus.NOT_EXECUTED, 0.0),
            _gate("W-11", "D6", GateStatus.NOT_EXECUTED, 0.0),
        ]
        report.compute_score()
        assert report.coverage < 0.7
        text = generate_report_v2(report)
        assert "INCOMPLETE" in text

    def test_full_coverage_no_incomplete(self):
        """Full coverage should not show INCOMPLETE."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [
            _gate("W-01", "D1", GateStatus.PASS, 10.0),
            _gate("W-02", "D2", GateStatus.PASS, 10.0),
        ]
        report.compute_score()
        text = generate_report_v2(report)
        assert "INCOMPLETE" not in text


class TestReportStructure:
    def test_report_has_dimension_table(self):
        """Report should contain a dimension scores table."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [_gate("W-01", "D1", GateStatus.PASS, 10.0)]
        report.compute_score()
        text = generate_report_v2(report)
        assert "Dimension" in text
        assert "Score" in text

    def test_report_has_gate_detail(self):
        """Report should contain gate-level detail table."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [_gate("W-01", "D1", GateStatus.PASS, 10.0, "all good")]
        report.compute_score()
        text = generate_report_v2(report)
        assert "W-01" in text
        assert "all good" in text

    def test_report_has_verdict(self):
        """Report should have a Verdict section."""
        report = PhaseGateReport(phase="ph5-qa", client_slug="test")
        report.gates = [_gate("W-01", "D1", GateStatus.PASS, 10.0)]
        report.compute_score()
        text = generate_report_v2(report)
        assert "Verdict" in text
