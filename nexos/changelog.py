"""
NEXOS v4.0 — Changelog / Audit Trail

Journal structuré append-only par client (nexos-changelog.json).
Trace automatiquement les événements pipeline, phases, SOIC, auto-fix, tooling, CLI.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

# ── Event types ──────────────────────────────────────────────────────


class EventType(StrEnum):
    """17 types d'événements traçables."""

    # Pipeline
    PIPELINE_START = "pipeline_start"
    PIPELINE_END = "pipeline_end"

    # Phases
    PHASE_START = "phase_start"
    PHASE_END = "phase_end"
    PHASE_FAIL = "phase_fail"

    # SOIC
    SOIC_GATE_PASS = "soic_gate_pass"
    SOIC_GATE_FAIL = "soic_gate_fail"
    SOIC_ITERATION = "soic_iteration"

    # Build
    BUILD_PASS = "build_pass"
    BUILD_FAIL = "build_fail"

    # Auto-fix
    AUTOFIX_START = "autofix_start"
    AUTOFIX_APPLIED = "autofix_applied"
    AUTOFIX_END = "autofix_end"

    # Tooling / Preflight
    PREFLIGHT_START = "preflight_start"
    PREFLIGHT_SCAN = "preflight_scan"
    PREFLIGHT_END = "preflight_end"

    # CLI
    CLI_FIX = "cli_fix"
    CLI_REPORT = "cli_report"

    # Brief
    BRIEF_CREATED = "brief_created"


# ── Entry dataclass ──────────────────────────────────────────────────


@dataclass
class ChangelogEntry:
    """Une entrée du changelog."""

    event: str
    timestamp: str = ""
    phase: str | None = None
    agent: str | None = None
    details: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict[str, Any]:
        """Convertit en dict, omet les champs None."""
        d: dict[str, Any] = {"event": self.event, "timestamp": self.timestamp}
        if self.phase is not None:
            d["phase"] = self.phase
        if self.agent is not None:
            d["agent"] = self.agent
        if self.details:
            d["details"] = self.details
        return d


CHANGELOG_FILENAME = "nexos-changelog.json"


# ── Core functions ───────────────────────────────────────────────────


def log_event(
    client_dir: Path,
    event: EventType,
    phase: str | None = None,
    agent: str | None = None,
    details: dict[str, Any] | None = None,
) -> ChangelogEntry:
    """
    Append un événement au changelog du client.

    Crée le fichier s'il n'existe pas. Défensif contre JSON corrompu.
    """
    entry = ChangelogEntry(
        event=event.value,
        phase=phase,
        agent=agent,
        details=details or {},
    )

    changelog_path = client_dir / CHANGELOG_FILENAME
    entries: list[dict[str, Any]] = []

    if changelog_path.exists():
        try:
            raw = changelog_path.read_text(encoding="utf-8")
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                entries = parsed
        except (json.JSONDecodeError, OSError):
            # Fichier corrompu — on repart avec les données lisibles
            pass

    entries.append(entry.to_dict())
    changelog_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return entry


def get_changelog(client_dir: Path) -> list[dict[str, Any]]:
    """
    Lit le changelog complet d'un client.

    Retourne une liste vide si le fichier n'existe pas ou est corrompu.
    """
    changelog_path = client_dir / CHANGELOG_FILENAME
    if not changelog_path.exists():
        return []

    try:
        raw = changelog_path.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
    except (json.JSONDecodeError, OSError):
        pass

    return []


def get_changelog_summary(client_dir: Path) -> dict[str, Any]:
    """
    Retourne un résumé du changelog : total, par type, fixes, phases, timestamps.
    """
    entries = get_changelog(client_dir)

    if not entries:
        return {"total": 0, "by_type": {}, "fixes": 0, "phases": [], "first": None, "last": None}

    by_type: dict[str, int] = {}
    fixes = 0
    phases: list[str] = []

    for e in entries:
        evt = e.get("event", "unknown")
        by_type[evt] = by_type.get(evt, 0) + 1

        if evt == EventType.AUTOFIX_APPLIED.value:
            fixes += 1

        if evt == EventType.PHASE_START.value:
            p = e.get("phase")
            if p and p not in phases:
                phases.append(p)

    timestamps = [e.get("timestamp", "") for e in entries if e.get("timestamp")]

    return {
        "total": len(entries),
        "by_type": by_type,
        "fixes": fixes,
        "phases": phases,
        "first": min(timestamps) if timestamps else None,
        "last": max(timestamps) if timestamps else None,
    }
