"""Tests pour nexos.build_validator."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from nexos.build_validator import (
    REQUIRED_HEADERS,
    BuildResult,
    _check_audit,
    _check_critical_files,
    _check_vercel_headers,
    format_build_report,
    validate_build,
)


class TestBuildResult:
    def test_default_is_fail(self):
        r = BuildResult()
        assert r.overall_pass is False

    def test_format_report_pass(self):
        r = BuildResult(
            npm_install_ok=True,
            tsc_ok=True,
            build_ok=True,
            headers_ok=True,
            overall_pass=True,
        )
        report = format_build_report(r)
        assert "BUILD PASS" in report

    def test_format_report_fail(self):
        r = BuildResult(npm_install_ok=True, tsc_ok=False, tsc_errors=["error TS2345"])
        report = format_build_report(r)
        assert "BUILD FAIL" in report
        assert "1 erreurs" in report


class TestCheckCriticalFiles:
    def test_all_present(self, tmp_path):
        (tmp_path / "vercel.json").touch()
        (tmp_path / "next.config.mjs").touch()
        p = tmp_path / "src" / "app" / "[locale]" / "politique-confidentialite"
        p.mkdir(parents=True)
        (p / "page.tsx").touch()
        m = tmp_path / "src" / "app" / "[locale]" / "mentions-legales"
        m.mkdir(parents=True)
        (m / "page.tsx").touch()

        missing = _check_critical_files(tmp_path)
        assert missing == []

    def test_all_missing(self, tmp_path):
        missing = _check_critical_files(tmp_path)
        assert len(missing) == 4


class TestCheckVercelHeaders:
    def test_valid_headers(self, tmp_path):
        vercel = {
            "headers": [
                {
                    "source": "/(.*)",
                    "headers": [{"key": k.title(), "value": "v"} for k in REQUIRED_HEADERS],
                }
            ]
        }
        (tmp_path / "vercel.json").write_text(json.dumps(vercel))
        assert _check_vercel_headers(tmp_path) is True

    def test_missing_headers(self, tmp_path):
        vercel = {"headers": [{"source": "/(.*)", "headers": []}]}
        (tmp_path / "vercel.json").write_text(json.dumps(vercel))
        assert _check_vercel_headers(tmp_path) is False

    def test_no_vercel_json(self, tmp_path):
        assert _check_vercel_headers(tmp_path) is False

    def test_invalid_json(self, tmp_path):
        (tmp_path / "vercel.json").write_text("not json{")
        assert _check_vercel_headers(tmp_path) is False


class TestCheckAudit:
    @patch("nexos.build_validator.subprocess.run")
    def test_no_vulns(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout=json.dumps({"metadata": {"vulnerabilities": {"high": 0, "critical": 0}}}),
            returncode=0,
        )
        highs, crits = _check_audit(Path("/fake"))
        assert highs == 0
        assert crits == 0

    @patch("nexos.build_validator.subprocess.run")
    def test_with_vulns(self, mock_run):
        mock_run.return_value = MagicMock(
            stdout=json.dumps({"metadata": {"vulnerabilities": {"high": 3, "critical": 1}}}),
            returncode=1,
        )
        highs, crits = _check_audit(Path("/fake"))
        assert highs == 3
        assert crits == 1


class TestValidateBuild:
    @patch("nexos.build_validator._check_audit", return_value=(0, 0))
    @patch("nexos.build_validator._check_build", return_value=(True, ""))
    @patch("nexos.build_validator._check_tsc", return_value=(True, []))
    @patch("nexos.build_validator._check_npm_install", return_value=True)
    def test_full_pass(self, mock_npm, mock_tsc, mock_build, mock_audit, tmp_path):
        # Créer fichiers critiques + vercel.json avec headers
        (tmp_path / "vercel.json").write_text(
            json.dumps(
                {
                    "headers": [
                        {
                            "source": "/(.*)",
                            "headers": [{"key": h, "value": "v"} for h in REQUIRED_HEADERS],
                        }
                    ]
                }
            )
        )
        (tmp_path / "next.config.mjs").touch()
        for p in [
            "src/app/[locale]/politique-confidentialite",
            "src/app/[locale]/mentions-legales",
        ]:
            d = tmp_path / p
            d.mkdir(parents=True)
            (d / "page.tsx").touch()

        result = validate_build(tmp_path)
        assert result.overall_pass is True

    @patch("nexos.build_validator._check_audit", return_value=(0, 0))
    @patch("nexos.build_validator._check_build", return_value=(True, ""))
    @patch("nexos.build_validator._check_tsc", return_value=(False, ["error TS2345 in test file"]))
    @patch("nexos.build_validator._check_npm_install", return_value=True)
    def test_tsc_fail_but_build_ok_passes(
        self, mock_npm, mock_tsc, mock_build, mock_audit, tmp_path
    ):
        """TSC errors in test files should not block if build passes."""
        (tmp_path / "vercel.json").write_text(
            json.dumps(
                {
                    "headers": [
                        {
                            "source": "/(.*)",
                            "headers": [{"key": h, "value": "v"} for h in REQUIRED_HEADERS],
                        }
                    ]
                }
            )
        )
        result = validate_build(tmp_path)
        assert result.tsc_ok is False
        assert result.build_ok is True
        assert result.overall_pass is True

    @patch("nexos.build_validator._check_npm_install", return_value=False)
    def test_npm_fail_short_circuits(self, mock_npm, tmp_path):
        result = validate_build(tmp_path)
        assert result.overall_pass is False
        assert result.npm_install_ok is False
