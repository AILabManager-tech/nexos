"""Tests régression pour orchestrator.gates_persistence.

Couvre BUG_NEXOS_SOIC_GATES_OVERWRITE (A-005) : un mode partiel
(`audit`, `modify`, `content`) ne doit pas écraser les entrées des
phases qu'il n'a pas réexécutées.
"""

from __future__ import annotations

import json
from pathlib import Path

from orchestrator.gates_persistence import (
    PHASE_ORDER,
    merge_gate_history,
    save_gate_history,
)


def _entry(phase: str, mu: float = 9.0, decision: str = "ACCEPT") -> dict:
    return {
        "phase": phase,
        "mu": mu,
        "threshold": 8.0,
        "converged": True,
        "iterations": 1,
        "decision": decision,
        "timestamp": "2026-05-10T00:00:00",
    }


class TestMergeGateHistory:
    def test_empty_existing_returns_new_runs_in_canonical_order(self):
        new_runs = [_entry("ph2-design"), _entry("ph0-discovery")]
        merged = merge_gate_history([], new_runs)
        assert [e["phase"] for e in merged] == ["ph0-discovery", "ph2-design"]

    def test_existing_phases_preserved_when_not_in_new_runs(self):
        existing = [_entry(p) for p in ("ph0-discovery", "ph1-strategy", "ph2-design")]
        new_runs = [_entry("ph5-qa")]
        merged = merge_gate_history(existing, new_runs)
        phases = [e["phase"] for e in merged]
        assert phases == ["ph0-discovery", "ph1-strategy", "ph2-design", "ph5-qa"]

    def test_new_runs_overwrite_existing_for_same_phase(self):
        existing = [_entry("ph5-qa", mu=6.5, decision="REJECT")]
        new_runs = [_entry("ph5-qa", mu=9.2, decision="ACCEPT")]
        merged = merge_gate_history(existing, new_runs)
        assert len(merged) == 1
        assert merged[0]["mu"] == 9.2
        assert merged[0]["decision"] == "ACCEPT"

    def test_canonical_phase_order_is_preserved(self):
        # Existing dans l'ordre désordre, on attend l'ordre canonique
        existing = [
            _entry("ph5-qa"),
            _entry("ph0-discovery"),
            _entry("ph3-content"),
        ]
        merged = merge_gate_history(existing, [])
        assert [e["phase"] for e in merged] == [
            "ph0-discovery",
            "ph3-content",
            "ph5-qa",
        ]

    def test_unknown_phases_appended_after_canonical(self):
        existing = [_entry("ph0-discovery"), _entry("custom-phase")]
        merged = merge_gate_history(existing, [_entry("ph2-design")])
        phases = [e["phase"] for e in merged]
        assert phases.index("ph0-discovery") < phases.index("ph2-design")
        assert phases.index("ph2-design") < phases.index("custom-phase")

    def test_malformed_existing_entries_dropped_silently(self):
        existing = [
            _entry("ph0-discovery"),
            "not a dict",  # type: ignore[list-item]
            {"no_phase_key": True},
            None,  # type: ignore[list-item]
        ]
        merged = merge_gate_history(existing, [])
        assert len(merged) == 1
        assert merged[0]["phase"] == "ph0-discovery"


class TestSaveGateHistory:
    def test_save_creates_file_when_none_exists(self, tmp_path: Path):
        gates_path = tmp_path / "soic-gates.json"
        save_gate_history(gates_path, [_entry("ph0-discovery")])
        assert gates_path.exists()
        data = json.loads(gates_path.read_text())
        assert len(data) == 1
        assert data[0]["phase"] == "ph0-discovery"

    def test_audit_after_create_preserves_full_history(self, tmp_path: Path):
        """Régression A-005 : un `nexos audit` (qui ne joue que ph5-qa) ne
        doit pas écraser les ph0-ph4 produites par un `nexos create` antérieur."""
        gates_path = tmp_path / "soic-gates.json"

        # Step 1 : `nexos create` écrit les 6 phases
        create_runs = [_entry(p) for p in PHASE_ORDER]
        save_gate_history(gates_path, create_runs)
        assert len(json.loads(gates_path.read_text())) == 6

        # Step 2 : `nexos audit` ne touche que ph5-qa
        audit_runs = [_entry("ph5-qa", mu=9.5)]
        save_gate_history(gates_path, audit_runs)

        # Les 6 entrées doivent toujours être là
        data = json.loads(gates_path.read_text())
        assert len(data) == 6
        assert [e["phase"] for e in data] == list(PHASE_ORDER)
        # ph5-qa doit refléter le nouveau run
        assert data[-1]["mu"] == 9.5

    def test_save_with_empty_runs_is_idempotent(self, tmp_path: Path):
        gates_path = tmp_path / "soic-gates.json"
        save_gate_history(gates_path, [_entry(p) for p in ("ph0-discovery", "ph1-strategy")])
        before = gates_path.read_text()
        save_gate_history(gates_path, [])
        after = gates_path.read_text()
        assert before == after

    def test_save_recovers_from_corrupted_existing(self, tmp_path: Path):
        gates_path = tmp_path / "soic-gates.json"
        gates_path.write_text("not valid json {{{")
        # Doit pas crasher, doit écrire les nouvelles entrées
        save_gate_history(gates_path, [_entry("ph0-discovery")])
        data = json.loads(gates_path.read_text())
        assert len(data) == 1

    def test_save_recovers_from_non_list_existing(self, tmp_path: Path):
        gates_path = tmp_path / "soic-gates.json"
        # Ancien format object-based (cf. baseline pre-runtime)
        gates_path.write_text(json.dumps({"_meta": "scaffold"}))
        save_gate_history(gates_path, [_entry("ph0-discovery")])
        data = json.loads(gates_path.read_text())
        assert isinstance(data, list)
        assert len(data) == 1


def test_phase_order_constant_matches_pipeline():
    """Le tuple PHASE_ORDER doit refléter les 6 phases canoniques NEXOS."""
    assert PHASE_ORDER == (
        "ph0-discovery",
        "ph1-strategy",
        "ph2-design",
        "ph3-content",
        "ph4-build",
        "ph5-qa",
    )
