"""Tests pour nexos.tooling_manager."""

import subprocess
from unittest.mock import MagicMock, patch

from nexos.tooling_manager import _parse_version, check_tool, doctor_report, ensure_tooling


class TestParseVersion:
    def test_simple_version(self):
        assert _parse_version("20.11.1") == (20, 11, 1)

    def test_v_prefix(self):
        assert _parse_version("v22.20.0") == (22, 20, 0)

    def test_with_text(self):
        assert _parse_version("0.43.0 (Codex CLI)") == (0, 43, 0)

    def test_no_version(self):
        assert _parse_version("no version here") == (0,)


class TestCheckTool:
    @patch("nexos.tooling_manager.subprocess.run")
    def test_tool_found(self, mock_run):
        mock_run.return_value = MagicMock(stdout="v22.20.0\n", stderr="", returncode=0)
        available, version = check_tool("node")
        assert available is True
        assert "22.20.0" in version

    @patch("nexos.tooling_manager.subprocess.run")
    def test_tool_not_found(self, mock_run):
        mock_run.side_effect = FileNotFoundError()
        available, version = check_tool("node")
        assert available is False
        assert version is None

    @patch("nexos.tooling_manager.subprocess.run")
    def test_tool_timeout(self, mock_run):
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="node", timeout=10)
        available, _version = check_tool("node")
        assert available is False

    @patch("nexos.tooling_manager.subprocess.run")
    def test_version_too_low(self, mock_run):
        mock_run.return_value = MagicMock(stdout="v18.0.0\n", stderr="", returncode=0)
        available, version = check_tool("node")  # min_version = 20.0.0
        assert available is False
        assert "18.0.0" in version

    def test_unknown_tool(self):
        available, version = check_tool("nonexistent_tool_xyz")
        assert available is False
        assert version is None


class TestEnsureTooling:
    @patch("nexos.tooling_manager.check_tool")
    def test_all_tools_ok(self, mock_check):
        mock_check.return_value = (True, "1.0.0")
        results = ensure_tooling(interactive=False)
        assert all(results.values())

    @patch("nexos.tooling_manager.check_tool")
    def test_critical_tool_missing_raises(self, mock_check):
        def side_effect(name):
            if name == "node":
                return (False, None)
            return (True, "1.0.0")

        mock_check.side_effect = side_effect
        try:
            ensure_tooling(interactive=False)
            raise AssertionError("Should have raised RuntimeError")
        except RuntimeError as e:
            assert "node" in str(e)

    @patch("nexos.tooling_manager.check_tool")
    def test_optional_tool_missing_no_raise(self, mock_check):
        def side_effect(name):
            if name == "pa11y":
                return (False, None)
            return (True, "1.0.0")

        mock_check.side_effect = side_effect
        results = ensure_tooling(interactive=False)
        assert results["pa11y"] is False
        assert results["node"] is True


class TestDoctorReport:
    @patch("nexos.tooling_manager.check_tool")
    def test_report_format(self, mock_check):
        mock_check.return_value = (True, "1.0.0")
        report = doctor_report()
        assert "NEXOS v4.0" in report
        assert "node" in report
        assert "OUTILS CLI" in report

    def test_report_includes_templates(self):
        report = doctor_report()
        assert "TEMPLATES" in report
        assert "cookie-consent-component.tsx" in report

    def test_report_includes_soic(self):
        report = doctor_report()
        assert "SOIC ENGINE" in report

    def test_report_includes_clients(self):
        report = doctor_report()
        assert "CLIENTS" in report
