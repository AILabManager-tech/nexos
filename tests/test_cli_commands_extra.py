"""Tests complémentaires pour nexos.cli_commands (chantier2 phase I).

Cible les branches non couvertes par tests/test_cli_commands.py :
- run_fix : structure plate (client_dir == site_dir), dry-run avec analyse,
  brief corrompu (json), résumé fix_report avec tous les flags allumés.
- run_report : gates au format dict, gates corrompus, dossier tooling avec
  fichiers, structure site plate, brief corrompu.
- _dry_run_analysis : vercel.json corrompu, headers manquants, page légale
  présente.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from nexos.auto_fixer import FixReport
from nexos.build_validator import BuildResult
from nexos.cli_commands import _dry_run_analysis, run_fix, run_report


class TestRunFixFlatStructure:
    @patch("nexos.cli_commands.console")
    def test_flat_structure_is_supported(self, mock_console, tmp_path):
        """`client_dir/package.json` (sans `site/`) doit être détecté comme site."""
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "package.json").write_text("{}")

        with (
            patch("nexos.cli_commands.validate_build") as mock_validate,
            patch("nexos.cli_commands.auto_fix"),
        ):
            mock_validate.return_value = BuildResult(
                npm_install_ok=True,
                tsc_ok=True,
                build_ok=True,
                headers_ok=True,
                overall_pass=True,
            )
            run_fix(client_dir)
            mock_validate.assert_called_once()
            # Le site_dir transmis doit être client_dir lui-même
            assert mock_validate.call_args.args[0] == client_dir


class TestRunFixDryRun:
    @patch("nexos.cli_commands.console")
    def test_dry_run_with_failing_build_runs_analysis(self, mock_console, tmp_path):
        """Dry-run doit appeler _dry_run_analysis sans appliquer auto_fix."""
        client_dir = tmp_path / "client"
        site_dir = client_dir / "site"
        site_dir.mkdir(parents=True)
        (site_dir / "package.json").write_text("{}")

        with (
            patch("nexos.cli_commands.validate_build") as mock_validate,
            patch("nexos.cli_commands.auto_fix") as mock_fix,
            patch("nexos.cli_commands._dry_run_analysis") as mock_analysis,
        ):
            mock_validate.return_value = BuildResult(
                npm_install_ok=True,
                tsc_ok=False,
                build_ok=False,
                headers_ok=False,
                overall_pass=False,
                audit_highs=3,
            )
            run_fix(client_dir, dry_run=True)
            mock_validate.assert_called_once()
            mock_fix.assert_not_called()
            mock_analysis.assert_called_once()


class TestRunFixReportSummary:
    @patch("nexos.cli_commands.console")
    def test_fix_report_all_flags_set(self, mock_console, tmp_path):
        """Tous les compteurs de FixReport non-nuls doivent être affichés."""
        client_dir = tmp_path / "client"
        site_dir = client_dir / "site"
        site_dir.mkdir(parents=True)
        (site_dir / "package.json").write_text("{}")

        with (
            patch("nexos.cli_commands.validate_build") as mock_validate,
            patch("nexos.cli_commands.auto_fix") as mock_fix,
        ):
            # Avant fix : build casse
            # Après fix : on retourne le même résultat (peu importe ici)
            mock_validate.return_value = BuildResult(
                npm_install_ok=True,
                tsc_ok=False,
                build_ok=False,
                headers_ok=False,
                overall_pass=False,
                audit_highs=2,
            )
            # total_fixes est une @property dérivée des autres attributs.
            mock_fix.return_value = FixReport(
                cookie_consent_added=True,
                npm_audit_fixed=2,
                vercel_headers_fixed=True,
                next_config_patched=True,
                privacy_page_added=True,
                legal_page_added=True,
            )
            run_fix(client_dir)
            calls = [str(c) for c in mock_console.print.call_args_list]
            joined = "\n".join(calls)
            for fragment in (
                "Cookie consent",
                "npm audit fix",
                "Headers",
                "next.config",
                "politique-confidentialite",
                "mentions-legales",
            ):
                assert fragment in joined, f"Manque : {fragment}"
            # Build après fix toujours en échec → branche "yellow BUILD FAIL"
            assert "BUILD FAIL" in joined or "intervention manuelle" in joined


class TestDryRunAnalysisExtra:
    @patch("nexos.cli_commands.console")
    def test_corrupted_vercel_json(self, mock_console, tmp_path):
        site_dir = tmp_path / "site"
        site_dir.mkdir()
        (site_dir / "vercel.json").write_text("{ not json")
        client_dir = tmp_path / "client"
        client_dir.mkdir()

        _dry_run_analysis(site_dir, client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "corrompu" in calls

    @patch("nexos.cli_commands.console")
    def test_vercel_json_missing_headers(self, mock_console, tmp_path):
        site_dir = tmp_path / "site"
        site_dir.mkdir()
        # vercel.json existe mais sans le bloc headers → détecte les manques
        (site_dir / "vercel.json").write_text(json.dumps({"headers": []}))
        client_dir = tmp_path / "client"
        client_dir.mkdir()

        _dry_run_analysis(site_dir, client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "Headers manquants" in calls

    @patch("nexos.cli_commands.console")
    def test_powered_by_header_true_is_flagged(self, mock_console, tmp_path):
        site_dir = tmp_path / "site"
        site_dir.mkdir()
        (site_dir / "next.config.mjs").write_text("const nextConfig = { poweredByHeader: true };\n")
        client_dir = tmp_path / "client"
        client_dir.mkdir()

        _dry_run_analysis(site_dir, client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "poweredByHeader=true" in calls

    @patch("nexos.cli_commands.console")
    def test_legal_pages_already_present_skipped(self, mock_console, tmp_path):
        site_dir = tmp_path / "site"
        # Crée les deux pages légales déjà présentes
        for page in ("politique-confidentialite", "mentions-legales"):
            d = site_dir / "src" / "app" / "[locale]" / page
            d.mkdir(parents=True)
            (d / "page.tsx").write_text("export default function P() { return null }\n")
        client_dir = tmp_path / "client"
        client_dir.mkdir()

        _dry_run_analysis(site_dir, client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        # Aucune mention "Politique" ni "Mentions" dans les findings
        assert "politique-confidentialite absente" not in calls.lower()


class TestRunReportExtra:
    @patch("nexos.cli_commands.console")
    def test_gates_dict_with_history_key(self, mock_console, tmp_path: Path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "soic-gates.json").write_text(
            json.dumps(
                {
                    "history": [
                        {"phase": "ph0-discovery", "mu": 7.5, "decision": "ACCEPT"},
                    ]
                }
            )
        )
        run_report(client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "7.5" in calls and "ACCEPT" in calls

    @patch("nexos.cli_commands.console")
    def test_corrupted_gates_json_is_handled(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "soic-gates.json").write_text("{ broken")
        run_report(client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "corrompu" in calls

    @patch("nexos.cli_commands.console")
    def test_tooling_directory_lists_files(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        tooling = client_dir / "tooling"
        tooling.mkdir(parents=True)
        (tooling / "lighthouse.json").write_text("{}")
        (tooling / "pa11y.json").write_text("[]")
        run_report(client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "lighthouse.json" in calls
        assert "pa11y.json" in calls

    @patch("nexos.cli_commands.console")
    def test_flat_site_structure_in_report(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "package.json").write_text("{}")
        run_report(client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "structure plate" in calls

    @patch("nexos.cli_commands.console")
    def test_corrupted_brief_json_in_report(self, mock_console, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        (client_dir / "brief-client.json").write_text("{ broken")
        run_report(client_dir)
        calls = "\n".join(str(c) for c in mock_console.print.call_args_list)
        assert "corrompu" in calls
