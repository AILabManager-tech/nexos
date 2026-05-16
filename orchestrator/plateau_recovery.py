"""Dimension-scoped plateau recovery hook (P8.3).

When SOIC's `Converger` returns `Decision.ENRICHED_RETRY`, the `PhaseIterator`
invokes its `on_enriched_retry` callback before re-prompting the LLM. NEXOS
plugs `make_plateau_auto_fix_hook(...)` into that slot so the auto-fixer can
correct exactly the dimensions that caused the plateau (e.g. D4 sécurité +
D8 Loi 25) before the rerun sees the filesystem.

This module is intentionally separate from `orchestrator/phases.py` so that:
- the hook is unit-testable in isolation (no need to drive the full pipeline);
- `phases.py` stays under its modularity budget (test_file_sizes_targets);
- the late-binding closure trap (ruff B023) disappears — captured state is
  passed via explicit factory arguments, not via lexical scope.

Failure modes handled defensively:
- `site_dir is None`              -> log + return (e.g., ph0-discovery before scaffold)
- `diagnosis.failing_dimensions`  -> log + return (defensive, should not happen)
  empty
- No registered fixer for the     -> log "coverage gap" + return (D1/D3/D5/D6/D7/D9
  reported dimensions                today are not covered by any auto-fixer)
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from soic.converger import PlateauDiagnosis


class _Say(Protocol):
    """Rich-styled output sink (same callable as orchestrator/_shared.say)."""

    def __call__(self, message: str) -> None: ...


def _is_changelog_available() -> bool:
    """Defensive import probe — keeps the hook usable in tests that mock
    `nexos.changelog` out, and avoids hard dependency on the v4 changelog."""
    try:
        import nexos.changelog  # noqa: F401
    except ImportError:
        return False
    return True


def make_plateau_auto_fix_hook(
    *,
    phase: str,
    site_dir: Path | None,
    client_dir: Path,
    mode: str,
    say: _Say,
    brief_loader: Callable[[Path], dict | None],
) -> Callable[[PlateauDiagnosis], None]:
    """Build the `on_enriched_retry` callback for one phase iteration.

    Captured state is passed via arguments — no closure over loop variables.
    The returned callable matches `soic.iterator.EnrichedRetryHook`.

    Args:
        phase           : current SOIC phase ("ph5-qa", etc.) — only used for log/event.
        site_dir        : Next.js site root. `None` triggers a defensive skip.
        client_dir      : NEXOS client directory containing `brief-client.json`.
        mode            : pipeline mode ("create"/"audit"/...) — forwarded to brief loader.
        say             : Rich-styled output sink (orchestrator/_shared.say).
        brief_loader    : callable that loads + normalizes the brief (e.g.
                          `lambda p: load_runtime_brief(p, mode=mode)`).
                          Decoupled from the loader implementation so this
                          module can be tested without importing the full
                          orchestrator stack.

    Returns:
        A `(PlateauDiagnosis) -> None` callable safe to pass as
        `PhaseIterator(..., on_enriched_retry=...)`.
    """

    def _hook(diagnosis: PlateauDiagnosis) -> None:
        if site_dir is None:
            say("[yellow]  ⚠ Plateau détecté — pas de site_dir, auto-fix skip (hook P8.3)[/]")
            return

        dims = list(diagnosis.failing_dimensions)
        if not dims:
            say("[yellow]  ⚠ Plateau détecté — diagnostic vide, auto-fix skip (hook P8.3)[/]")
            return

        # Lazy imports so this module loads even when nexos.auto_fixer is
        # being patched / mocked in tests.
        from nexos.auto_fixer import auto_fix, fixers_for_dimensions

        covered = fixers_for_dimensions(dims)
        has_changelog = _is_changelog_available()

        if not covered:
            say(
                f"[yellow]  ⚠ Plateau {phase} sur {dims} — aucun fixer "
                f"NEXOS pour ces dimensions (gap P8/P9 connu)[/]"
            )
            if has_changelog:
                from nexos.changelog import EventType, log_event

                log_event(
                    client_dir,
                    EventType.AUTOFIX_END,
                    phase=phase,
                    agent="auto_fixer",
                    details={
                        "trigger": "plateau",
                        "dimensions": dims,
                        "fixers_applied": 0,
                        "coverage_gap": True,
                    },
                )
            return

        say(
            f"[cyan]  Plateau {phase} — auto-fix ciblé dimensions={dims} "
            f"({len(covered)} fixer(s))[/]"
        )

        brief_path = client_dir / "brief-client.json"
        brief = brief_loader(brief_path) if brief_path.exists() else None
        fix_report = auto_fix(site_dir, client_dir, brief, dimensions=dims)
        say(f"[cyan]  Auto-fix dim-scoped: {fix_report.total_fixes} correction(s)[/]")

        if has_changelog:
            from nexos.changelog import EventType, log_event

            from .verify import _fix_report_to_dict

            log_event(
                client_dir,
                EventType.AUTOFIX_END,
                phase=phase,
                agent="auto_fixer",
                details={
                    "trigger": "plateau",
                    "dimensions": dims,
                    **_fix_report_to_dict(fix_report),
                },
            )

    return _hook


__all__ = ["make_plateau_auto_fix_hook"]
