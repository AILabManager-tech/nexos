"""Tests for orchestrator.plateau_recovery (P8.3).

The `make_plateau_auto_fix_hook` factory builds the `on_enriched_retry`
callback that SOIC's PhaseIterator invokes on plateau. These tests cover
the hook's defensive branches (no site, empty diagnosis, coverage gap)
and its happy path (dimensions routed to auto_fix), without spinning
the full pipeline.

The auto_fixer module is patched at the symbol nexos.auto_fixer would
resolve to from inside the hook — `nexos.auto_fixer.auto_fix` and
`nexos.auto_fixer.fixers_for_dimensions`. We avoid touching the
filesystem entirely; the hook should never call auto_fix when the
defensive guards trip.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from nexos.auto_fixer import FixReport
from orchestrator.plateau_recovery import make_plateau_auto_fix_hook
from soic.converger import FailingAssertion, PlateauDiagnosis


def _diagnosis(
    failing_dimensions: tuple[str, ...] = ("D4", "D8"),
    iteration: int = 3,
) -> PlateauDiagnosis:
    """Build a representative PlateauDiagnosis (D4 + D8 fails)."""
    return PlateauDiagnosis(
        iteration=iteration,
        mu_trajectory=(7.5, 7.5, 7.5),
        fail_trajectory=(2, 2, 2),
        failing_dimensions=failing_dimensions,
        failing_assertions=(
            FailingAssertion("W-05", "npm-audit", "D4", 3.0, "1 HIGH"),
            FailingAssertion("W-14", "loi-25", "D8", 2.0, "missing privacy"),
        ),
        phase="ph5-qa",
    )


@pytest.fixture()
def say_log():
    """Capture every line written by the hook to its `say` sink."""
    lines: list[str] = []

    def _say(message: str) -> None:
        lines.append(message)

    return lines, _say


@pytest.fixture()
def brief_loader_log():
    """Track every brief_loader invocation (path it was called with)."""
    calls: list[Path] = []

    def _loader(path: Path) -> dict:
        calls.append(path)
        return {"company_name": "TestCo"}

    return calls, _loader


class TestPlateauHookDefensive:
    """The hook must never crash on degenerate inputs — every branch short-
    circuits with a log line and a clean return. No fixer should be invoked."""

    def test_skips_when_site_dir_is_none(self, tmp_path, say_log, brief_loader_log):
        lines, say = say_log
        _, loader = brief_loader_log

        hook = make_plateau_auto_fix_hook(
            phase="ph5-qa",
            site_dir=None,  # ← defensive branch
            client_dir=tmp_path,
            mode="create",
            say=say,
            brief_loader=loader,
        )

        with patch("nexos.auto_fixer.auto_fix") as mock_fix:
            hook(_diagnosis())
            mock_fix.assert_not_called()

        joined = " | ".join(lines)
        assert "pas de site_dir" in joined, f"Expected skip log, got: {joined}"

    def test_skips_when_diagnosis_has_no_failing_dimensions(
        self, tmp_path, say_log, brief_loader_log
    ):
        lines, say = say_log
        _, loader = brief_loader_log

        hook = make_plateau_auto_fix_hook(
            phase="ph5-qa",
            site_dir=tmp_path / "site",
            client_dir=tmp_path,
            mode="create",
            say=say,
            brief_loader=loader,
        )

        with patch("nexos.auto_fixer.auto_fix") as mock_fix:
            hook(_diagnosis(failing_dimensions=()))  # ← empty
            mock_fix.assert_not_called()

        joined = " | ".join(lines)
        assert "diagnostic vide" in joined, f"Expected empty-diag log, got: {joined}"

    def test_logs_coverage_gap_when_no_fixer_matches(self, tmp_path, say_log, brief_loader_log):
        """Plateau on D5/D6/D9 (no NEXOS fixer today) → coverage gap log,
        auto_fix NOT invoked. This is the signal that future P8/P9 work
        should extend fixer coverage to these dimensions."""
        lines, say = say_log
        _, loader = brief_loader_log

        hook = make_plateau_auto_fix_hook(
            phase="ph5-qa",
            site_dir=tmp_path / "site",
            client_dir=tmp_path,
            mode="create",
            say=say,
            brief_loader=loader,
        )

        with patch("nexos.auto_fixer.auto_fix") as mock_fix:
            hook(_diagnosis(failing_dimensions=("D5", "D6", "D9")))
            mock_fix.assert_not_called()

        joined = " | ".join(lines)
        assert "aucun fixer" in joined, f"Expected coverage-gap log, got: {joined}"


class TestPlateauHookHappyPath:
    """When site_dir + non-empty + covered dimensions all line up, the hook
    must invoke auto_fix with the failing_dimensions passed through verbatim."""

    def test_invokes_auto_fix_with_failing_dimensions(self, tmp_path, say_log, brief_loader_log):
        _lines, say = say_log
        loader_calls, loader = brief_loader_log

        # Make brief-client.json exist so the loader is invoked
        (tmp_path / "brief-client.json").write_text('{"company_name": "TestCo"}')

        hook = make_plateau_auto_fix_hook(
            phase="ph5-qa",
            site_dir=tmp_path / "site",
            client_dir=tmp_path,
            mode="create",
            say=say,
            brief_loader=loader,
        )

        with patch("nexos.auto_fixer.auto_fix") as mock_fix:
            mock_fix.return_value = FixReport(vercel_headers_fixed=True, csp_added=True)
            hook(_diagnosis(failing_dimensions=("D4", "D8")))
            mock_fix.assert_called_once()
            kwargs = mock_fix.call_args.kwargs
            args = mock_fix.call_args.args
            # auto_fix(site_dir, client_dir, brief, dimensions=...)
            assert args[0] == tmp_path / "site"
            assert args[1] == tmp_path
            assert args[2] == {"company_name": "TestCo"}
            assert kwargs["dimensions"] == ["D4", "D8"]

        # brief_loader was called with the brief-client.json path
        assert loader_calls == [tmp_path / "brief-client.json"]

    def test_skips_brief_loader_when_brief_file_absent(self, tmp_path, say_log, brief_loader_log):
        """If brief-client.json doesn't exist, brief_loader is NOT called and
        auto_fix receives None as the brief (caller will fall back to {})."""
        _lines, say = say_log
        loader_calls, loader = brief_loader_log

        # No brief-client.json created on disk

        hook = make_plateau_auto_fix_hook(
            phase="ph5-qa",
            site_dir=tmp_path / "site",
            client_dir=tmp_path,
            mode="create",
            say=say,
            brief_loader=loader,
        )

        with patch("nexos.auto_fixer.auto_fix") as mock_fix:
            mock_fix.return_value = FixReport()
            hook(_diagnosis(failing_dimensions=("D4",)))
            mock_fix.assert_called_once()
            assert mock_fix.call_args.args[2] is None

        assert loader_calls == [], "brief_loader should not be called when file is absent"

    def test_logs_count_of_covered_fixers(self, tmp_path, say_log, brief_loader_log):
        """The 'auto-fix ciblé dimensions=...' log line must include the
        number of fixers covering the requested dimensions so the operator
        sees at a glance whether routing actually had work to do."""
        lines, say = say_log
        _, loader = brief_loader_log

        hook = make_plateau_auto_fix_hook(
            phase="ph5-qa",
            site_dir=tmp_path / "site",
            client_dir=tmp_path,
            mode="create",
            say=say,
            brief_loader=loader,
        )

        with patch("nexos.auto_fixer.auto_fix") as mock_fix:
            mock_fix.return_value = FixReport(vercel_headers_fixed=True)
            # D4 → 5 fixers (npm_audit, vercel_headers, csp, csp_middleware, next_config)
            hook(_diagnosis(failing_dimensions=("D4",)))

        joined = " | ".join(lines)
        assert "5 fixer" in joined, f"Expected '5 fixer(s)' in cyan plateau log, got: {joined}"
        assert (
            "dimensions=['D4']" in joined
            or "dimensions=[\\'D4\\']" in joined
            or ("dimensions=" in joined and "D4" in joined)
        ), f"Expected dimensions list in log, got: {joined}"
