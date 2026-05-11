"""Tests régression pour orchestrator.reconciliation.

Couvre l'item 3 chantier 4 — détection de la divergence Ph4 ment / Ph5
mesure réelle. Filet de sécurité défensif universel : signale si μ Ph4
et μ Ph5 divergent au-delà d'un seuil (par défaut 2.0 points).
"""

from __future__ import annotations

import json
from pathlib import Path

from orchestrator.reconciliation import (
    ReconciliationResult,
    append_reconciliation_to_report,
    format_reconciliation_report_section,
    load_phase_mu,
    reconcile_ph4_ph5,
)


def _write_gates(tmp_path: Path, gates: list[dict]) -> Path:
    path = tmp_path / "soic-gates.json"
    path.write_text(json.dumps(gates), encoding="utf-8")
    return path


def test_load_phase_mu_returns_mu_when_present(tmp_path: Path):
    gates_path = _write_gates(tmp_path, [{"phase": "ph4-build", "mu": 9.84}])
    assert load_phase_mu(gates_path, "ph4-build") == 9.84


def test_load_phase_mu_returns_none_for_missing_phase(tmp_path: Path):
    gates_path = _write_gates(tmp_path, [{"phase": "ph0-discovery", "mu": 8.0}])
    assert load_phase_mu(gates_path, "ph4-build") is None


def test_load_phase_mu_returns_none_for_missing_file(tmp_path: Path):
    assert load_phase_mu(tmp_path / "nope.json", "ph4-build") is None


def test_load_phase_mu_returns_none_for_invalid_json(tmp_path: Path):
    path = tmp_path / "broken.json"
    path.write_text("not json", encoding="utf-8")
    assert load_phase_mu(path, "ph4-build") is None


def test_load_phase_mu_returns_latest_when_multiple(tmp_path: Path):
    """Si plusieurs runs : on prend la dernière entrée."""
    gates_path = _write_gates(
        tmp_path,
        [
            {"phase": "ph4-build", "mu": 6.5, "iteration": 1},
            {"phase": "ph4-build", "mu": 9.84, "iteration": 2},
        ],
    )
    assert load_phase_mu(gates_path, "ph4-build") == 9.84


def test_reconcile_returns_none_when_phases_missing(tmp_path: Path):
    """Pipeline partiel sans Ph4 ou Ph5 → pas de reconciliation (None)."""
    gates_path = _write_gates(tmp_path, [{"phase": "ph0-discovery", "mu": 8.0}])
    assert reconcile_ph4_ph5(gates_path) is None


def test_reconcile_converged_when_close(tmp_path: Path):
    """μ4≈μ5 → diverged=False."""
    gates_path = _write_gates(
        tmp_path,
        [
            {"phase": "ph4-build", "mu": 9.84},
            {"phase": "ph5-qa", "mu": 9.47},
        ],
    )
    result = reconcile_ph4_ph5(gates_path)
    assert result is not None
    assert result.diverged is False
    assert abs(result.delta - 0.37) < 0.01


def test_reconcile_diverged_ph4_overestimates(tmp_path: Path):
    """Cas central audit knowledge : Ph4=10 ment, Ph5=6.79 → WARNING."""
    gates_path = _write_gates(
        tmp_path,
        [
            {"phase": "ph4-build", "mu": 10.0},
            {"phase": "ph5-qa", "mu": 6.79},
        ],
    )
    result = reconcile_ph4_ph5(gates_path)
    assert result is not None
    assert result.diverged is True
    assert abs(result.delta - 3.21) < 0.01
    assert "Ph4 surévalue" in result.reason


def test_reconcile_diverged_ph5_overestimates(tmp_path: Path):
    """Cas inverse atypique : Ph5 > Ph4 + seuil → WARNING différent."""
    gates_path = _write_gates(
        tmp_path,
        [
            {"phase": "ph4-build", "mu": 5.0},
            {"phase": "ph5-qa", "mu": 9.0},
        ],
    )
    result = reconcile_ph4_ph5(gates_path)
    assert result is not None
    assert result.diverged is True
    assert "Ph5 surévalue" in result.reason


def test_reconcile_custom_threshold(tmp_path: Path):
    """Seuil personnalisable : 1.0 doit déclencher là où 2.0 ne le ferait pas."""
    gates_path = _write_gates(
        tmp_path,
        [
            {"phase": "ph4-build", "mu": 9.0},
            {"phase": "ph5-qa", "mu": 7.5},
        ],
    )
    result_default = reconcile_ph4_ph5(gates_path, threshold=2.0)
    assert result_default is not None
    assert result_default.diverged is False  # 1.5 ≤ 2.0

    result_strict = reconcile_ph4_ph5(gates_path, threshold=1.0)
    assert result_strict is not None
    assert result_strict.diverged is True  # 1.5 > 1.0


def test_format_section_includes_warning_icon_when_diverged():
    result = ReconciliationResult(
        ph4_mu=10.0,
        ph5_mu=6.79,
        delta=3.21,
        threshold=2.0,
        diverged=True,
        reason="Ph4 surévalue …",
    )
    section = format_reconciliation_report_section(result)
    assert "WARNING" in section
    assert "10.0" in section
    assert "6.79" in section
    assert "3.21" in section


def test_format_section_shows_ok_when_converged():
    result = ReconciliationResult(
        ph4_mu=9.84,
        ph5_mu=9.47,
        delta=0.37,
        threshold=2.0,
        diverged=False,
        reason="cohérents",
    )
    section = format_reconciliation_report_section(result)
    assert "✓" in section
    assert "WARNING" not in section


def test_append_to_report_when_section_absent(tmp_path: Path):
    report = tmp_path / "ph5-qa-report.md"
    report.write_text("# Rapport Ph5\n\n## 0. Cadrage\n\nContent\n", encoding="utf-8")
    result = ReconciliationResult(
        ph4_mu=9.84,
        ph5_mu=9.47,
        delta=0.37,
        threshold=2.0,
        diverged=False,
        reason="cohérents",
    )
    assert append_reconciliation_to_report(report, result) is True
    content = report.read_text(encoding="utf-8")
    assert "## Reconciliation Ph4 ↔ Ph5" in content
    assert "## 0. Cadrage" in content  # contenu original préservé


def test_append_to_report_replaces_existing_section(tmp_path: Path):
    """Idempotence : appeler 2x ne duplique pas la section."""
    report = tmp_path / "ph5-qa-report.md"
    report.write_text(
        "# Rapport Ph5\n\n## Reconciliation Ph4 ↔ Ph5\n\nOLD\n\n## 1. Suite\n",
        encoding="utf-8",
    )
    result = ReconciliationResult(
        ph4_mu=9.84,
        ph5_mu=9.47,
        delta=0.37,
        threshold=2.0,
        diverged=False,
        reason="nouveau",
    )
    assert append_reconciliation_to_report(report, result) is True
    content = report.read_text(encoding="utf-8")
    # OLD remplacé par nouveau
    assert "OLD" not in content
    assert "nouveau" in content
    # Section suivante préservée
    assert "## 1. Suite" in content
    # Une seule occurrence du marker
    assert content.count("## Reconciliation Ph4 ↔ Ph5") == 1


def test_append_returns_false_when_report_missing(tmp_path: Path):
    result = ReconciliationResult(
        ph4_mu=9.0,
        ph5_mu=8.5,
        delta=0.5,
        threshold=2.0,
        diverged=False,
        reason="ok",
    )
    assert append_reconciliation_to_report(tmp_path / "absent.md", result) is False
