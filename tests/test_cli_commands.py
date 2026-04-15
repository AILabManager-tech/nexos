"""Tests pour nexos.cli_commands (doctor, fix, report)."""

import json
from unittest.mock import patch

from nexos.cli_commands import _dry_run_analysis, run_doctor, run_fix, run_report


class TestRunDoctor:
    @patch("nexos.cli_commands.console")
    def test_runs_without_error(self, mock_console):
        # Should not raise
        run_doctor()
        # Should have printed a Panel
        mock_console.print.assert_called()


class TestRunFix:
    @patch("nexos.cli_commands.console")
    def test_no_package_json_prints_error(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        run_fix(client_dir)
        # Should print error about missing package.json
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("package.json" in c for c in calls)

    @patch("nexos.cli_commands.console")
    def test_fix_with_clean_build(self, mock_console, tmp_path):
        """Build passes and no issues → exits early, validate called once."""
        from nexos.build_validator import BuildResult

        client_dir = tmp_path / "client"
        client_dir.mkdir()
        site_dir = client_dir / "site"
        site_dir.mkdir()
        (site_dir / "package.json").write_text("{}")

        with (
            patch("nexos.cli_commands.validate_build") as mock_validate,
            patch("nexos.cli_commands.auto_fix"),
        ):
            # No issues at all → should exit early
            mock_validate.return_value = BuildResult(
                npm_install_ok=True,
                tsc_ok=True,
                build_ok=True,
                headers_ok=True,
                overall_pass=True,
            )
            run_fix(client_dir)
            mock_validate.assert_called_once()

    @patch("nexos.cli_commands.console")
    def test_fix_with_issues_runs_twice(self, mock_console, tmp_path):
        """Build passes but has issues → applies fix, validates twice."""
        from nexos.auto_fixer import FixReport
        from nexos.build_validator import BuildResult

        client_dir = tmp_path / "client"
        client_dir.mkdir()
        site_dir = client_dir / "site"
        site_dir.mkdir()
        (site_dir / "package.json").write_text("{}")

        with (
            patch("nexos.cli_commands.validate_build") as mock_validate,
            patch("nexos.cli_commands.auto_fix") as mock_fix,
        ):
            mock_validate.return_value = BuildResult(
                npm_install_ok=True,
                tsc_ok=False,
                build_ok=True,
                headers_ok=True,
                overall_pass=True,
                audit_highs=2,
            )
            mock_fix.return_value = FixReport()
            run_fix(client_dir)
            assert mock_validate.call_count == 2
            mock_fix.assert_called_once()

    @patch("nexos.cli_commands.console")
    def test_dry_run_analysis(self, mock_console, tmp_path):
        site_dir = tmp_path / "site"
        site_dir.mkdir()
        client_dir = tmp_path / "client"
        client_dir.mkdir()

        # Créer un next.config sans poweredByHeader
        (site_dir / "next.config.mjs").write_text("const nextConfig = {};\n")

        _dry_run_analysis(site_dir, client_dir)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("poweredByHeader" in c for c in calls)


class TestRunReport:
    @patch("nexos.cli_commands.console")
    def test_empty_client(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        run_report(client_dir)
        # Should not raise, should print absent phases
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("absent" in c for c in calls)

    @patch("nexos.cli_commands.console")
    def test_with_soic_gates(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        gates = [
            {"phase": "ph0-discovery", "mu": 8.5, "decision": "ACCEPT", "iterations": 1},
            {"phase": "ph5-qa", "mu": 9.0, "decision": "ACCEPT", "iterations": 2},
        ]
        (client_dir / "soic-gates.json").write_text(json.dumps(gates))

        run_report(client_dir)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("8.5" in c or "9.0" in c for c in calls)

    @patch("nexos.cli_commands.console")
    def test_with_phase_reports(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "ph5-qa-report.md").write_text("# QA Report\nContent here")

        run_report(client_dir)
        calls = [str(c) for c in mock_console.print.call_args_list]
        # Should show ph5-qa as present
        assert any("ph5-qa" in c and "octets" in c for c in calls)

    @patch("nexos.cli_commands.console")
    def test_with_brief(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "brief-client.json").write_text(
            json.dumps(
                {
                    "company_name": "TestCorp",
                    "legal": {"rpp_name": "Jean Test"},
                }
            )
        )

        run_report(client_dir)
        calls = [str(c) for c in mock_console.print.call_args_list]
        assert any("TestCorp" in c for c in calls)
