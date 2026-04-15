"""Tests for soic.gate_engine — Gate instantiation and phase mapping."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from soic.domain_grids import get_phase_gates
from soic.gate_engine import GateEngine


class TestPhaseGateMapping:
    def test_ph5_qa_has_17_gates(self):
        """ph5-qa (WEB_FULL) should have exactly 17 gates."""
        gates = get_phase_gates("ph5-qa")
        assert len(gates) == 17

    def test_ph4_build_has_7_gates(self):
        """ph4-build (WEB_BUILD) should have a subset of gates."""
        gates = get_phase_gates("ph4-build")
        assert len(gates) == 7

    def test_ph0_discovery_has_4_gates(self):
        """ph0-discovery (PHASE_EARLY) should have 4 gates."""
        gates = get_phase_gates("ph0-discovery")
        assert len(gates) == 4

    def test_early_phases_same_gates(self):
        """ph0-ph3 should all use PHASE_EARLY gates."""
        for phase in ["ph0-discovery", "ph1-strategy", "ph2-design", "ph3-content"]:
            gates = get_phase_gates(phase)
            assert len(gates) == 4
            gate_ids = {g.gate_id for g in gates}
            assert gate_ids == {"PE-01", "PE-02", "PE-03", "PE-04"}


class TestGateEngineInit:
    def test_engine_loads_gates(self):
        """GateEngine should load gates for the given phase."""
        engine = GateEngine(phase="ph5-qa", client_dir="/tmp/test-client")
        assert len(engine.gates) == 17

    def test_engine_unknown_phase_raises(self):
        """Unknown phase should raise ValueError."""
        import pytest

        with pytest.raises(ValueError, match="Unknown phase"):
            get_phase_gates("unknown-phase")


class TestGateIds:
    def test_web_gate_ids(self):
        """Verify expected web gate IDs are present in ph5-qa."""
        gates = get_phase_gates("ph5-qa")
        gate_ids = {g.gate_id for g in gates}
        expected = {f"W-{i:02d}" for i in range(1, 18)}  # W-01 to W-17
        assert expected == gate_ids

    def test_phase_early_gate_ids(self):
        """Verify expected early phase gate IDs."""
        gates = get_phase_gates("ph0-discovery")
        gate_ids = {g.gate_id for g in gates}
        expected = {"PE-01", "PE-02", "PE-03", "PE-04"}
        assert expected == gate_ids

    def test_no_duplicate_gate_ids(self):
        """Gate IDs should be unique within a phase."""
        for phase in ["ph0-discovery", "ph4-build", "ph5-qa"]:
            gates = get_phase_gates(phase)
            ids = [g.gate_id for g in gates]
            assert len(ids) == len(set(ids)), f"Duplicate gate IDs in {phase}"
