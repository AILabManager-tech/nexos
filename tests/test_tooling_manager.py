"""Tests pour nexos.tooling_manager."""

import subprocess
from unittest.mock import MagicMock, patch

from nexos.tooling_manager import (
    _client_status_row,
    _parse_version,
    check_tool,
    doctor_all_clients_report,
    doctor_report,
    ensure_tooling,
)


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


class TestDoctorAllClients:
    """Rapport tabulaire multi-clients (P4e)."""

    def test_returns_string(self):
        report = doctor_all_clients_report()
        assert isinstance(report, str)
        assert len(report) > 0

    def test_includes_header(self):
        report = doctor_all_clients_report()
        assert "All Clients" in report
        # Colonnes attendues
        assert "Client" in report
        assert "Brief" in report
        assert "Site" in report
        assert "Gates" in report
        assert "Ph5" in report
        assert "Deploy" in report

    def test_deployable_count_line(self):
        """Footer indique combien de clients sont déployables."""
        report = doctor_all_clients_report()
        assert "Déployables" in report
        # Format : "X/Y"
        assert "/" in report.split("Déployables")[-1]

    def test_includes_known_clients(self):
        """Au moins quelques clients connus apparaissent dans le rapport."""
        report = doctor_all_clients_report()
        # depanneur-nobert est notre client de référence — doit toujours être présent
        assert "depanneur-nobert" in report

    def test_client_status_row_missing_brief(self, tmp_path, monkeypatch):
        """Client sans brief → status 'missing'."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "clients" / "ghost").mkdir(parents=True)
        row = _client_status_row("ghost")
        assert row["slug"] == "ghost"
        assert row["brief"] == "missing"
        assert row["site"] == "missing"

    def test_client_status_row_with_brief_and_site(self, tmp_path, monkeypatch):
        """Client avec brief + site → status 'ok'."""
        import json as _json

        monkeypatch.chdir(tmp_path)
        client_dir = tmp_path / "clients" / "alpha"
        client_dir.mkdir(parents=True)
        (client_dir / "brief-client.json").write_text(_json.dumps({"company_name": "Alpha"}))
        (client_dir / "site").mkdir()
        (client_dir / "site" / "package.json").write_text("{}")
        row = _client_status_row("alpha")
        assert row["brief"] == "ok"
        assert row["site"] == "ok"

    def test_client_status_row_deploy_ready(self, tmp_path, monkeypatch):
        """Ph5 ACCEPT μ ≥ 8.5 → deploy READY."""
        import json as _json

        monkeypatch.chdir(tmp_path)
        client_dir = tmp_path / "clients" / "beta"
        client_dir.mkdir(parents=True)
        (client_dir / "soic-gates.json").write_text(
            _json.dumps([{"phase": "ph5-qa", "mu": 9.2, "threshold": 8.5, "decision": "ACCEPT"}])
        )
        row = _client_status_row("beta")
        assert row["ph5_mu"] == "9.20"
        assert row["deploy"] == "READY"

    def test_client_status_row_deploy_below_threshold(self, tmp_path, monkeypatch):
        """Ph5 ACCEPT mais μ < 8.5 → deploy BELOW."""
        import json as _json

        monkeypatch.chdir(tmp_path)
        client_dir = tmp_path / "clients" / "gamma"
        client_dir.mkdir(parents=True)
        (client_dir / "soic-gates.json").write_text(
            _json.dumps([{"phase": "ph5-qa", "mu": 8.0, "threshold": 8.5, "decision": "ACCEPT"}])
        )
        row = _client_status_row("gamma")
        assert "BELOW" in row["deploy"]

    def test_client_status_row_corrupted_gates(self, tmp_path, monkeypatch):
        """Gates JSON corrompu → status 'corrupt' (pas de crash)."""
        monkeypatch.chdir(tmp_path)
        client_dir = tmp_path / "clients" / "delta"
        client_dir.mkdir(parents=True)
        (client_dir / "soic-gates.json").write_text("{ not valid json")
        row = _client_status_row("delta")
        assert row["gates"] == "corrupt"

    def test_skips_underscore_directories(self, tmp_path, monkeypatch):
        """Dossiers commençant par _ (archive, fixtures) ignorés."""
        monkeypatch.chdir(tmp_path)
        (tmp_path / "clients" / "_ARCHIVE").mkdir(parents=True)
        (tmp_path / "clients" / "real-client").mkdir()
        report = doctor_all_clients_report()
        assert "_ARCHIVE" not in report
        assert "real-client" in report

    def test_client_status_row_picks_latest_gate_when_multi_runs(self, tmp_path, monkeypatch):
        """P9 D9 — Pour un client multi-runs, doctor doit lire la DERNIÈRE
        entrée ph5-qa de soic-gates.json, pas la première. Bug découvert
        pendant P8.5 vertex-pmo : run 1 ABORT_PLATEAU μ=7.91 puis run 4
        ACCEPT μ=9.00 → doctor doit afficher 9.00 READY, pas 7.91."""
        import json as _json

        monkeypatch.chdir(tmp_path)
        client_dir = tmp_path / "clients" / "multirun"
        client_dir.mkdir(parents=True)
        (client_dir / "soic-gates.json").write_text(
            _json.dumps(
                [
                    {
                        "phase": "ph5-qa",
                        "mu": 7.91,
                        "threshold": 8.5,
                        "decision": "ABORT_PLATEAU",
                        "iterations": 3,
                        "timestamp": "2026-05-07T00:00:00",
                    },
                    {
                        "phase": "ph5-qa",
                        "mu": 9.00,
                        "threshold": 8.5,
                        "decision": "ACCEPT",
                        "iterations": 4,
                        "timestamp": "2026-05-17T00:00:00",
                    },
                ]
            )
        )
        row = _client_status_row("multirun")
        assert row["ph5_mu"] == "9.00", (
            "doctor a lu la 1ère entrée (mu=7.91) au lieu de la dernière "
            "(mu=9.00) — bug P9 D9 régressé"
        )
        assert row["deploy"] == "READY", (
            f"deploy={row['deploy']!r}, attendu 'READY' (dernière entrée = ACCEPT μ=9.00 ≥ 8.5)"
        )
        assert row["gates"] == "2", "compte total des gates incorrect"
