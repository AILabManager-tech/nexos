"""Tests pour nexos.changelog — Audit trail NEXOS."""

import json
from datetime import datetime

from nexos.changelog import (
    CHANGELOG_FILENAME,
    ChangelogEntry,
    EventType,
    get_changelog,
    get_changelog_summary,
    log_event,
)

# ── TestLogEvent ─────────────────────────────────────────────────────


class TestLogEvent:
    """Tests pour log_event() — append au fichier JSON."""

    def test_creates_file_if_absent(self, tmp_path):
        log_event(tmp_path, EventType.PIPELINE_START)
        assert (tmp_path / CHANGELOG_FILENAME).exists()

    def test_append_preserves_existing(self, tmp_path):
        log_event(tmp_path, EventType.PIPELINE_START, phase="ph0-discovery")
        log_event(tmp_path, EventType.PHASE_START, phase="ph0-discovery")
        entries = json.loads((tmp_path / CHANGELOG_FILENAME).read_text())
        assert len(entries) == 2
        assert entries[0]["event"] == "pipeline_start"
        assert entries[1]["event"] == "phase_start"

    def test_handles_corrupted_json(self, tmp_path):
        (tmp_path / CHANGELOG_FILENAME).write_text("NOT JSON {{{")
        log_event(tmp_path, EventType.PIPELINE_START)
        entries = json.loads((tmp_path / CHANGELOG_FILENAME).read_text())
        assert len(entries) == 1

    def test_stores_details(self, tmp_path):
        log_event(tmp_path, EventType.AUTOFIX_APPLIED, details={"fix": "vercel_headers"})
        entries = json.loads((tmp_path / CHANGELOG_FILENAME).read_text())
        assert entries[0]["details"]["fix"] == "vercel_headers"

    def test_timestamp_iso_format(self, tmp_path):
        entry = log_event(tmp_path, EventType.PIPELINE_START)
        # Should parse without error
        dt = datetime.fromisoformat(entry.timestamp)
        assert dt.year >= 2026

    def test_optional_fields_omitted(self, tmp_path):
        log_event(tmp_path, EventType.PIPELINE_START)
        entries = json.loads((tmp_path / CHANGELOG_FILENAME).read_text())
        assert "phase" not in entries[0]
        assert "agent" not in entries[0]

    def test_returns_entry(self, tmp_path):
        entry = log_event(tmp_path, EventType.PHASE_START, phase="ph1", agent="orchestrator")
        assert isinstance(entry, ChangelogEntry)
        assert entry.event == "phase_start"
        assert entry.phase == "ph1"


# ── TestGetChangelog ─────────────────────────────────────────────────


class TestGetChangelog:
    """Tests pour get_changelog() — lecture."""

    def test_returns_empty_if_absent(self, tmp_path):
        assert get_changelog(tmp_path) == []

    def test_reads_entries(self, tmp_path):
        log_event(tmp_path, EventType.PIPELINE_START)
        log_event(tmp_path, EventType.PIPELINE_END)
        entries = get_changelog(tmp_path)
        assert len(entries) == 2

    def test_handles_corrupted_json(self, tmp_path):
        (tmp_path / CHANGELOG_FILENAME).write_text("{invalid")
        assert get_changelog(tmp_path) == []

    def test_entries_are_dicts(self, tmp_path):
        log_event(tmp_path, EventType.BUILD_PASS, phase="ph4-build")
        entries = get_changelog(tmp_path)
        assert isinstance(entries[0], dict)
        assert entries[0]["event"] == "build_pass"


# ── TestGetChangelogSummary ──────────────────────────────────────────


class TestGetChangelogSummary:
    """Tests pour get_changelog_summary() — agrégation."""

    def test_empty_summary(self, tmp_path):
        summary = get_changelog_summary(tmp_path)
        assert summary["total"] == 0
        assert summary["fixes"] == 0
        assert summary["first"] is None

    def test_summary_with_events(self, tmp_path):
        log_event(tmp_path, EventType.PIPELINE_START)
        log_event(tmp_path, EventType.PHASE_START, phase="ph0-discovery")
        log_event(tmp_path, EventType.AUTOFIX_APPLIED, details={"fix": "headers"})
        log_event(tmp_path, EventType.AUTOFIX_APPLIED, details={"fix": "config"})
        log_event(tmp_path, EventType.PIPELINE_END)

        summary = get_changelog_summary(tmp_path)
        assert summary["total"] == 5
        assert summary["fixes"] == 2
        assert "ph0-discovery" in summary["phases"]
        assert summary["by_type"]["autofix_applied"] == 2

    def test_timestamps_first_last(self, tmp_path):
        log_event(tmp_path, EventType.PIPELINE_START)
        log_event(tmp_path, EventType.PIPELINE_END)
        summary = get_changelog_summary(tmp_path)
        assert summary["first"] is not None
        assert summary["last"] is not None
        assert summary["first"] <= summary["last"]


# ── TestChangelogEntry ───────────────────────────────────────────────


class TestChangelogEntry:
    """Tests pour ChangelogEntry dataclass."""

    def test_to_dict_minimal(self):
        entry = ChangelogEntry(event="pipeline_start")
        d = entry.to_dict()
        assert d["event"] == "pipeline_start"
        assert "timestamp" in d
        assert "phase" not in d
        assert "agent" not in d
        assert "details" not in d

    def test_to_dict_complete(self):
        entry = ChangelogEntry(
            event="autofix_applied",
            phase="ph5-qa",
            agent="auto_fixer",
            details={"fix": "vercel_headers", "target": "vercel.json"},
        )
        d = entry.to_dict()
        assert d["phase"] == "ph5-qa"
        assert d["agent"] == "auto_fixer"
        assert d["details"]["target"] == "vercel.json"


# ── TestEventType ────────────────────────────────────────────────────


class TestEventType:
    """Tests pour l'enum EventType."""

    def test_types_are_strings(self):
        assert EventType.PIPELINE_START.value == "pipeline_start"
        assert isinstance(EventType.AUTOFIX_APPLIED.value, str)

    def test_all_values_unique(self):
        values = [e.value for e in EventType]
        assert len(values) == len(set(values))
        assert len(values) == 19
