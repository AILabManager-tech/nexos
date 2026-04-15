"""Tests for section manifest injection in build_phase_prompt()."""

import json
import tempfile
from pathlib import Path

from orchestrator import build_phase_prompt


def _make_manifest(sections: list[dict]) -> dict:
    """Helper — build a valid section-manifest.json payload."""
    return {
        "$schema": "section-manifest-v1",
        "generated_at": "2026-03-04T10:00:00Z",
        "total_sections": len(sections),
        "sections": sections,
    }


def _section(
    sid: str,
    page: str = "home",
    name: str = "Hero",
    status: str = "planned",
    component: str = "HeroSection",
) -> dict:
    """Helper — build a single section entry."""
    return {
        "id": sid,
        "page": page,
        "name": name,
        "status": status,
        "component_name": component,
    }


class TestSectionManifestInjection:
    def test_manifest_injected_when_present(self):
        """S-001 appears in prompt when manifest exists."""
        with tempfile.TemporaryDirectory() as tmp:
            client_dir = Path(tmp)
            manifest = _make_manifest([_section("S-001")])
            (client_dir / "section-manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            prompt = build_phase_prompt("ph1-strategy", client_dir)
            assert "S-001" in prompt
            assert "Section Manifest" in prompt

    def test_no_manifest_no_injection(self):
        """No crash when section-manifest.json is absent."""
        with tempfile.TemporaryDirectory() as tmp:
            client_dir = Path(tmp)
            prompt = build_phase_prompt("ph1-strategy", client_dir)
            assert "Section Manifest" not in prompt

    def test_invalid_manifest_no_crash(self):
        """Invalid JSON falls back silently."""
        with tempfile.TemporaryDirectory() as tmp:
            client_dir = Path(tmp)
            (client_dir / "section-manifest.json").write_text(
                "NOT VALID JSON {{{", encoding="utf-8"
            )
            prompt = build_phase_prompt("ph1-strategy", client_dir)
            assert "Section Manifest" not in prompt

    def test_manifest_summary_capped(self):
        """Summary is capped at 30 sections max in prompt output."""
        with tempfile.TemporaryDirectory() as tmp:
            client_dir = Path(tmp)
            sections = [_section(f"S-{i:03d}") for i in range(1, 36)]
            manifest = _make_manifest(sections)
            (client_dir / "section-manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            prompt = build_phase_prompt("ph1-strategy", client_dir)
            assert "S-030" in prompt
            assert "S-031" not in prompt
