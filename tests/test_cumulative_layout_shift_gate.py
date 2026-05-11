"""Tests régression pour soic.domain_grids.web.CumulativeLayoutShiftGate (W-18).

Item 1 chantier 4 dette pipeline : la gate W-18 lit lighthouse.json et
bloque Ph5 si CLS dépasse les seuils Google web-vitals.

Couvre le bug central de l'audit chantier knowledge (2026-05-08) :
- Ph4 voyait BUILD PASS
- Ph5 mesurait CLS=0.502 sans bloquer
- → site avec CLS catastrophique passait à DEPLOY

Avec W-18, μ ph5 reflète maintenant la qualité réelle CLS.
"""

from __future__ import annotations

import json
from pathlib import Path

from soic.domain_grids.web import CumulativeLayoutShiftGate
from soic.models import GateStatus


def _write_lighthouse(tooling_dir: Path, cls_value: float | None) -> None:
    tooling_dir.mkdir(parents=True, exist_ok=True)
    audits = {}
    if cls_value is not None:
        audits["cumulative-layout-shift"] = {"numericValue": cls_value, "score": 1.0}
    (tooling_dir / "lighthouse.json").write_text(
        json.dumps({"audits": audits, "categories": {}}), encoding="utf-8"
    )


def test_cls_good_passes_with_10(tmp_path: Path):
    """CLS ≤ 0.1 → PASS, score 10."""
    _write_lighthouse(tmp_path / "tooling", 0.05)
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.status == GateStatus.PASS
    assert result.score == 10.0
    assert "Good" in result.evidence
    assert "0.050" in result.evidence


def test_cls_at_threshold_good_boundary(tmp_path: Path):
    """CLS = 0.1 → PASS, score 10 (limite haute Good)."""
    _write_lighthouse(tmp_path / "tooling", 0.1)
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.status == GateStatus.PASS
    assert result.score == 10.0


def test_cls_needs_improvement(tmp_path: Path):
    """0.1 < CLS ≤ 0.25 → PASS dégradé, score entre 7 et 10."""
    _write_lighthouse(tmp_path / "tooling", 0.17)  # milieu de la zone
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.status == GateStatus.PASS
    assert 7.0 < result.score < 10.0
    assert "Needs Improvement" in result.evidence


def test_cls_poor_fails(tmp_path: Path):
    """CLS = 0.3 → FAIL, score entre 3 et 7."""
    _write_lighthouse(tmp_path / "tooling", 0.3)
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.status == GateStatus.FAIL
    assert 3.0 < result.score < 7.0
    assert "Poor" in result.evidence


def test_cls_central_audit_bug_fails(tmp_path: Path):
    """Cas central audit knowledge : CLS=0.502 doit FAIL maintenant.
    Avant W-18, le site avec CLS=0.502 passait silencieusement à DEPLOY."""
    _write_lighthouse(tmp_path / "tooling", 0.502)
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.status == GateStatus.FAIL
    assert "0.502" in result.evidence


def test_cls_catastrophic_zero_score(tmp_path: Path):
    """CLS > 0.5 → score 0, FAIL Critical."""
    _write_lighthouse(tmp_path / "tooling", 1.0)
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.status == GateStatus.FAIL
    assert result.score == 0.0
    assert "Critical" in result.evidence


def test_missing_lighthouse_skipped(tmp_path: Path):
    """Sans lighthouse.json → SKIP (not_executed), pas FAIL."""
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert "lighthouse" in result.evidence.lower()


def test_lighthouse_without_cls_audit_handles_gracefully(tmp_path: Path):
    """lighthouse.json présent mais sans audit CLS → error_result, pas crash."""
    _write_lighthouse(tmp_path / "tooling", None)  # pas d'audit CLS
    gate = CumulativeLayoutShiftGate()
    result = gate.run(str(tmp_path), site_dir=str(tmp_path))
    assert result.score == 0
    # Le gate ne crash pas


def test_w18_registered_in_full_set():
    """W-18 doit être dans WEB_FULL pour s'exécuter en ph5-qa."""
    from soic.domain_grids.web import _load_web_full_gates

    gates = _load_web_full_gates()
    gate_ids = {g.gate_id for g in gates}
    assert "W-18" in gate_ids


def test_w18_not_in_build_set():
    """W-18 dépend de lighthouse (preflight Ph5), donc pas dans WEB_BUILD."""
    from soic.domain_grids.web import _load_web_build_gates

    gates = _load_web_build_gates()
    gate_ids = {g.gate_id for g in gates}
    assert "W-18" not in gate_ids
