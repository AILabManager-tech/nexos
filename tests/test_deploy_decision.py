"""Tests régression — verdict deploy à 2 axes (SOIC + Osiris).

P9 D2 — chantier dette pipeline 2026-05-18.

Garanties testées :
  - 4 cas joint (SOIC PASS|FAIL x Osiris PASS|FAIL)
  - Cas Osiris UNKNOWN (missing / scan error) → joint suit SOIC, warning émis
  - Cas SOIC UNKNOWN (gate absent) → traité comme FAIL pour joint
  - Threshold custom (env override)
  - Idempotence + round-trip JSON deploy-decision.json
  - Format markdown 2-axes table
"""

from __future__ import annotations

import json
from pathlib import Path

from nexos.deploy_decision import (
    DEPLOY_DECISION_FILENAME,
    DeployDecision,
    evaluate_deploy_decision,
    format_dual_axis_table,
    persist_deploy_decision,
)


def _write_soic_gates(client_dir: Path, mu: float, decision: str = "ACCEPT") -> None:
    gates = [
        {
            "phase": "ph5-qa",
            "mu": mu,
            "decision": decision,
            "threshold": 8.5,
            "coverage": 0.9,
            "iteration": 1,
        }
    ]
    (client_dir / "soic-gates.json").write_text(json.dumps(gates), encoding="utf-8")


def _write_osiris(client_dir: Path, payload: dict) -> None:
    tooling = client_dir / "tooling"
    tooling.mkdir(parents=True, exist_ok=True)
    (tooling / "osiris.json").write_text(json.dumps(payload), encoding="utf-8")


# ── Les 4 cas joint canoniques ──────────────────────────────────────────────


def test_joint_accept_when_both_pass(tmp_path: Path) -> None:
    """SOIC ACCEPT μ=9.0 + Osiris score=7.4 ≥ 6.0 → ACCEPT, blocker=None."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": 7.4, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "ACCEPT"
    assert d.blocker is None
    assert d.soic_verdict == "PASS"
    assert d.osiris_verdict == "PASS"
    assert d.warnings == []


def test_joint_fail_when_only_soic_fails(tmp_path: Path) -> None:
    """SOIC FAIL μ=7.0 + Osiris score=8.5 ≥ 6.0 → FAIL, blocker='soic'."""
    _write_soic_gates(tmp_path, mu=7.0, decision="FAIL")
    _write_osiris(tmp_path, {"osiris_score": 8.5, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "FAIL"
    assert d.blocker == "soic"
    assert d.soic_verdict == "FAIL"
    assert d.osiris_verdict == "PASS"


def test_joint_fail_when_only_osiris_fails(tmp_path: Path) -> None:
    """SOIC ACCEPT μ=9.0 + Osiris score=4.0 < 6.0 → FAIL, blocker='osiris'."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": 4.0, "grade": "Critique"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "FAIL"
    assert d.blocker == "osiris"
    assert d.soic_verdict == "PASS"
    assert d.osiris_verdict == "FAIL"
    assert d.osiris_score == 4.0
    assert d.osiris_grade == "Critique"


def test_joint_fail_when_both_fail(tmp_path: Path) -> None:
    """SOIC FAIL μ=7.0 + Osiris score=3.0 < 6.0 → FAIL, blocker='both'."""
    _write_soic_gates(tmp_path, mu=7.0, decision="FAIL")
    _write_osiris(tmp_path, {"osiris_score": 3.0, "grade": "Critique"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "FAIL"
    assert d.blocker == "both"


# ── Politique UNKNOWN ───────────────────────────────────────────────────────


def test_osiris_missing_does_not_block_when_soic_accepts(tmp_path: Path) -> None:
    """SOIC ACCEPT + Osiris file absent → joint ACCEPT avec warning."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    # Pas de tooling/osiris.json

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "ACCEPT"
    assert d.osiris_verdict == "UNKNOWN"
    assert d.osiris_score is None
    assert any("Osiris report absent" in w for w in d.warnings)


def test_osiris_scan_error_does_not_block(tmp_path: Path) -> None:
    """Osiris scan failed (error JSON) → UNKNOWN, ne bloque pas le joint."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_osiris(tmp_path, {"error": "osiris scan failed after 3 attempts"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.osiris_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"
    assert any("Osiris scan failed" in w for w in d.warnings)


def test_soic_gate_absent_treated_as_fail(tmp_path: Path) -> None:
    """SOIC gate absent (pas de soic-gates.json) → joint FAIL, blocker='soic'."""
    _write_osiris(tmp_path, {"osiris_score": 7.4, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.soic_verdict == "UNKNOWN"
    assert d.joint_verdict == "FAIL"
    assert d.blocker == "soic"
    assert any("SOIC gate ph5-qa absent" in w for w in d.warnings)


def test_soic_decision_accept_but_mu_below_threshold_fails(tmp_path: Path) -> None:
    """Edge case : decision='ACCEPT' mais μ<8.5 (incohérence) → FAIL strict.

    Empêche un bug GateEngine de laisser passer un deploy sous le seuil.
    """
    _write_soic_gates(tmp_path, mu=8.2, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": 8.0, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.soic_verdict == "FAIL"
    assert d.joint_verdict == "FAIL"


# ── Threshold custom ────────────────────────────────────────────────────────


def test_custom_osiris_threshold(tmp_path: Path) -> None:
    """Osiris score=5.5 < default 6.0 → FAIL, mais avec threshold=5.0 → PASS."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": 5.5, "grade": "Acceptable"})

    d_default = evaluate_deploy_decision(tmp_path)
    assert d_default.osiris_verdict == "FAIL"

    d_relaxed = evaluate_deploy_decision(tmp_path, osiris_threshold=5.0)
    assert d_relaxed.osiris_verdict == "PASS"
    assert d_relaxed.joint_verdict == "ACCEPT"


# ── Robustesse JSON ─────────────────────────────────────────────────────────


def test_corrupted_soic_gates_treated_as_missing(tmp_path: Path) -> None:
    """soic-gates.json corrompu → SOIC UNKNOWN, ne crash pas."""
    (tmp_path / "soic-gates.json").write_text("not json {", encoding="utf-8")
    _write_osiris(tmp_path, {"osiris_score": 7.0, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.soic_verdict == "UNKNOWN"
    assert d.joint_verdict == "FAIL"
    assert d.blocker == "soic"


def test_corrupted_osiris_treated_as_unknown(tmp_path: Path) -> None:
    """tooling/osiris.json corrompu → Osiris UNKNOWN, ne crash pas."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    tooling = tmp_path / "tooling"
    tooling.mkdir()
    (tooling / "osiris.json").write_text("garbage", encoding="utf-8")

    d = evaluate_deploy_decision(tmp_path)
    assert d.osiris_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"


def test_osiris_score_non_numeric_treated_as_unknown(tmp_path: Path) -> None:
    """osiris_score présent mais non-numeric → UNKNOWN."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": "n/a", "grade": "Indéterminé"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.osiris_verdict == "UNKNOWN"
    assert d.osiris_score is None


def test_osiris_raw_scanner_json_uses_score_key(tmp_path: Path) -> None:
    """Le JSON brut osiris/scanner.py utilise `score` (pas `osiris_score`).

    Tolérance : si le report a `score` (raw scanner output) au lieu de
    `osiris_score` (RunStore SOIC), on lit `score`. Évite le mismatch
    silencieux observé en B1+ (preflight écrivait UNKNOWN partout).
    """
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    # Format JSON brut Osiris scanner.py (cf tools/osiris-scan.sh output)
    _write_osiris(
        tmp_path,
        {
            "osiris_version": "0.2.0",
            "url": "https://example.com",
            "domain": "example.com",
            "score": 7.9,
            "grade": "Conforme",
        },
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.osiris_score == 7.9
    assert d.osiris_grade == "Conforme"
    assert d.osiris_verdict == "PASS"
    assert d.joint_verdict == "ACCEPT"


# ── Persistance + format ────────────────────────────────────────────────────


def test_persist_and_reload_roundtrip(tmp_path: Path) -> None:
    """Le JSON persisté contient tous les champs et est relisible."""
    _write_soic_gates(tmp_path, mu=9.46, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": 7.4, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    path = persist_deploy_decision(d, tmp_path)
    assert path.name == DEPLOY_DECISION_FILENAME
    assert path.exists()

    reloaded = json.loads(path.read_text(encoding="utf-8"))
    assert reloaded["joint_verdict"] == "ACCEPT"
    assert reloaded["soic_mu"] == 9.46
    assert reloaded["osiris_score"] == 7.4
    assert reloaded["blocker"] is None


def test_persist_is_idempotent(tmp_path: Path) -> None:
    """Appeler persist 2x produit le même contenu (write deterministe)."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_osiris(tmp_path, {"osiris_score": 7.0, "grade": "Conforme"})

    d = evaluate_deploy_decision(tmp_path)
    persist_deploy_decision(d, tmp_path)
    first = (tmp_path / DEPLOY_DECISION_FILENAME).read_text(encoding="utf-8")
    persist_deploy_decision(d, tmp_path)
    second = (tmp_path / DEPLOY_DECISION_FILENAME).read_text(encoding="utf-8")
    assert first == second


def test_format_dual_axis_table_contains_both_axes() -> None:
    """Le tableau markdown contient les 2 axes et le verdict joint."""
    d = DeployDecision(
        soic_mu=9.11,
        soic_verdict="PASS",
        soic_threshold=8.5,
        osiris_score=4.0,
        osiris_grade="Critique",
        osiris_verdict="FAIL",
        osiris_threshold=6.0,
        joint_verdict="FAIL",
        blocker="osiris",
        warnings=[],
    )
    table = format_dual_axis_table(d)
    assert "μ=9.11" in table
    assert "score=4.0" in table
    assert "Critique" in table
    assert "FAIL" in table
    assert "blocker: osiris" in table
