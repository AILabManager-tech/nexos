"""Tests régression pour soic.domain_grids.phase_early.ReportScorePresentGate (PE-02).

Couvre BUG_SOIC_PE02_REGEX_SCORE_GLOBAL (A-008) : la regex initiale
n'acceptait que `score\\s*global`, rejetant toute formulation alternative
utilisée par les templates NEXOS (`Score éditorial`, `Score qualitatif`,
`Score discovery`).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from soic.domain_grids.phase_early import ReportScorePresentGate


@pytest.fixture
def gate():
    return ReportScorePresentGate()


def _write_report(tmp_path: Path, body: str) -> Path:
    """Crée la structure attendue par _get_report_content."""
    client = tmp_path / "fakeclient"
    client.mkdir()
    (client / "ph0-discovery-report.md").write_text(body, encoding="utf-8")
    return client


def test_pe02_passes_with_score_global(gate, tmp_path: Path):
    """Cas historique : `Score global: X/10` doit passer (régression OK)."""
    client = _write_report(tmp_path, "## Résumé\n\nScore global: 8.5/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"
    assert result.score == 10.0


def test_pe02_accepts_score_editorial_with_accent(gate, tmp_path: Path):
    """A-008 cas 1 : `Score éditorial: 7.8/10` (template NEXOS actuel)."""
    client = _write_report(tmp_path, "**Score éditorial** : **7.8 / 10**\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"
    assert result.score == 10.0


def test_pe02_accepts_score_editorial_without_accent(gate, tmp_path: Path):
    """A-008 cas 2 : `Score editorial: 7.8/10` (sans accent, autorisé)."""
    client = _write_report(tmp_path, "Score editorial: 7.8/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"


def test_pe02_accepts_score_qualitatif(gate, tmp_path: Path):
    """A-008 cas 3 : `Score qualitatif: 8.4/10`."""
    client = _write_report(tmp_path, "Score qualitatif: 8.4/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"


def test_pe02_accepts_score_discovery(gate, tmp_path: Path):
    """A-008 cas 4 : `Score discovery: 7.5/10`."""
    client = _write_report(tmp_path, "Score discovery: 7.5/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"


def test_pe02_accepts_score_strategique(gate, tmp_path: Path):
    """A-008 ext : `Score stratégique: 7.5/10` (ph1+)."""
    client = _write_report(tmp_path, "Score stratégique: 7.5/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"


def test_pe02_accepts_mu_symbol(gate, tmp_path: Path):
    """Régression : `μ = 8.0/10` doit toujours passer."""
    client = _write_report(tmp_path, "μ = 8.0/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "PASS"


def test_pe02_fails_on_unrecognized_label(gate, tmp_path: Path):
    """Négatif explicite : un label non reconnu doit toujours FAIL."""
    client = _write_report(tmp_path, "Note finale: 7/10\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "FAIL"
    assert result.score == 3.0


def test_pe02_fails_on_empty_report(gate, tmp_path: Path):
    """Régression : pas de rapport = FAIL avec evidence claire."""
    client = tmp_path / "fakeclient"
    client.mkdir()
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "FAIL"
    assert "No report" in result.evidence


def test_pe02_fails_on_score_without_slash_10(gate, tmp_path: Path):
    """Cas piégeux : `Score global: 8` sans `/10` doit FAIL (pas un score sur 10)."""
    client = _write_report(tmp_path, "Score global: 8\n")
    result = gate.run(str(client), site_dir=str(client / "site"))
    assert result.status.value == "FAIL"
