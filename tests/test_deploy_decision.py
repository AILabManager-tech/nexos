"""Tests régression — verdict deploy à N axes (SOIC + Osiris + Lighthouse + npm audit).

P9 D2 (2026-05-18) : pattern dual-axis initial (SOIC + Osiris).
Extension (2026-05-18 suite) : axes 3 (Lighthouse) + 4 (npm audit).

Garanties testées :
  - Verdict joint = ACCEPT si tous les axes PASS ou UNKNOWN
  - Verdict joint = FAIL si au moins un axe FAIL, blockers énumère lesquels
  - Politique UNKNOWN : missing / corrompu / non-numeric ne bloque pas
  - SOIC UNKNOWN traité comme FAIL (pas de gate = pas de deploy)
  - Thresholds custom par axe
  - Persistance + format markdown 4 axes
"""

from __future__ import annotations

import json
from pathlib import Path

from nexos.deploy_decision import (
    AXIS_LIGHTHOUSE,
    AXIS_NPM_AUDIT,
    AXIS_OSIRIS,
    AXIS_SOIC,
    DEPLOY_DECISION_FILENAME,
    DeployDecision,
    evaluate_deploy_decision,
    format_axes_table,
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


def _write_tooling(client_dir: Path, filename: str, payload: dict) -> None:
    tooling = client_dir / "tooling"
    tooling.mkdir(parents=True, exist_ok=True)
    (tooling / filename).write_text(json.dumps(payload), encoding="utf-8")


def _write_all_pass(tmp_path: Path) -> None:
    """Helper : configure les 4 axes en PASS pour tester ACCEPT joint."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_tooling(tmp_path, "osiris.json", {"score": 7.4, "grade": "Conforme"})
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.92}}})
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 0, "critical": 0}}},
    )


# ── Verdict joint : cas canoniques ──────────────────────────────────────────


def test_joint_accept_when_all_4_pass(tmp_path: Path) -> None:
    """4 axes PASS → ACCEPT, blockers=[]."""
    _write_all_pass(tmp_path)
    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "ACCEPT"
    assert d.blockers == []
    assert d.soic_verdict == "PASS"
    assert d.osiris_verdict == "PASS"
    assert d.lighthouse_verdict == "PASS"
    assert d.npm_audit_verdict == "PASS"


def test_joint_fail_lists_only_failed_axes(tmp_path: Path) -> None:
    """SOIC PASS, Osiris FAIL, Lighthouse FAIL, npm audit PASS → blockers=[osiris, lighthouse]."""
    _write_all_pass(tmp_path)
    # Override Osiris + Lighthouse en FAIL
    _write_tooling(tmp_path, "osiris.json", {"score": 4.0, "grade": "Critique"})
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.40}}})

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "FAIL"
    assert set(d.blockers) == {AXIS_OSIRIS, AXIS_LIGHTHOUSE}


def test_joint_fail_all_4_axes(tmp_path: Path) -> None:
    """Tous FAIL → blockers contient les 4."""
    _write_soic_gates(tmp_path, mu=7.0, decision="FAIL")
    _write_tooling(tmp_path, "osiris.json", {"score": 3.0, "grade": "Critique"})
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.30}}})
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 3, "critical": 1}}},
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.joint_verdict == "FAIL"
    assert set(d.blockers) == {AXIS_SOIC, AXIS_OSIRIS, AXIS_LIGHTHOUSE, AXIS_NPM_AUDIT}


# ── Axe Lighthouse ──────────────────────────────────────────────────────────


def test_lighthouse_perf_normalized_to_0_100(tmp_path: Path) -> None:
    """Lighthouse stocke score en 0-1 ; on l'expose en 0-100."""
    _write_all_pass(tmp_path)
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.87}}})

    d = evaluate_deploy_decision(tmp_path)
    assert d.lighthouse_perf == 87.0
    assert d.lighthouse_verdict == "PASS"  # ≥ 85


def test_lighthouse_below_threshold_fails(tmp_path: Path) -> None:
    """Lighthouse perf=40/100 < 85 → FAIL, blocker=lighthouse."""
    _write_all_pass(tmp_path)
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.40}}})

    d = evaluate_deploy_decision(tmp_path)
    assert d.lighthouse_perf == 40.0
    assert d.lighthouse_verdict == "FAIL"
    assert d.joint_verdict == "FAIL"
    assert d.blockers == [AXIS_LIGHTHOUSE]


def test_lighthouse_missing_does_not_block(tmp_path: Path) -> None:
    """tooling/lighthouse.json absent → UNKNOWN, ne bloque pas."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_tooling(tmp_path, "osiris.json", {"score": 7.4, "grade": "Conforme"})
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 0, "critical": 0}}},
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.lighthouse_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"
    assert any("Lighthouse report absent" in w for w in d.warnings)


def test_lighthouse_custom_threshold(tmp_path: Path) -> None:
    """Threshold paramétrable : perf=80 PASS si threshold=75, FAIL si threshold=90."""
    _write_all_pass(tmp_path)
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.80}}})

    d_strict = evaluate_deploy_decision(tmp_path, lighthouse_threshold=90.0)
    assert d_strict.lighthouse_verdict == "FAIL"

    d_relaxed = evaluate_deploy_decision(tmp_path, lighthouse_threshold=75.0)
    assert d_relaxed.lighthouse_verdict == "PASS"
    assert d_relaxed.joint_verdict == "ACCEPT"


# ── Axe npm audit ───────────────────────────────────────────────────────────


def test_npm_audit_zero_high_critical_passes(tmp_path: Path) -> None:
    """high=0 + critical=0 → PASS (aligné CLAUDE.md règle absolue)."""
    _write_all_pass(tmp_path)
    d = evaluate_deploy_decision(tmp_path)
    assert d.npm_audit_high == 0
    assert d.npm_audit_critical == 0
    assert d.npm_audit_verdict == "PASS"


def test_npm_audit_any_high_fails(tmp_path: Path) -> None:
    """1 HIGH → FAIL avec threshold default 0 (zero tolerance)."""
    _write_all_pass(tmp_path)
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 1, "critical": 0}}},
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.npm_audit_high == 1
    assert d.npm_audit_verdict == "FAIL"
    assert d.joint_verdict == "FAIL"
    assert d.blockers == [AXIS_NPM_AUDIT]


def test_npm_audit_critical_fails(tmp_path: Path) -> None:
    """1 CRITICAL → FAIL."""
    _write_all_pass(tmp_path)
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 0, "critical": 1}}},
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.npm_audit_critical == 1
    assert d.npm_audit_verdict == "FAIL"


def test_npm_audit_missing_does_not_block(tmp_path: Path) -> None:
    """tooling/npm-audit.json absent → UNKNOWN, ne bloque pas."""
    _write_soic_gates(tmp_path, mu=9.0, decision="ACCEPT")
    _write_tooling(tmp_path, "osiris.json", {"score": 7.4, "grade": "Conforme"})
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.92}}})

    d = evaluate_deploy_decision(tmp_path)
    assert d.npm_audit_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"


def test_npm_audit_custom_threshold_allows_some_high(tmp_path: Path) -> None:
    """threshold=2 permet jusqu'à 2 HIGH+CRIT cumulés."""
    _write_all_pass(tmp_path)
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 2, "critical": 0}}},
    )

    d_zero = evaluate_deploy_decision(tmp_path)  # default threshold=0
    assert d_zero.npm_audit_verdict == "FAIL"

    d_relaxed = evaluate_deploy_decision(tmp_path, npm_audit_threshold=2)
    assert d_relaxed.npm_audit_verdict == "PASS"
    assert d_relaxed.joint_verdict == "ACCEPT"


# ── Axe Osiris (rétrocompat P9 D2) ──────────────────────────────────────────


def test_osiris_raw_scanner_json_uses_score_key(tmp_path: Path) -> None:
    """Le JSON brut osiris/scanner.py utilise `score` (pas `osiris_score`)."""
    _write_all_pass(tmp_path)
    # Override avec format raw scanner
    _write_tooling(
        tmp_path,
        "osiris.json",
        {
            "osiris_version": "0.2.0",
            "url": "https://example.com",
            "score": 7.9,
            "grade": "Conforme",
        },
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.osiris_score == 7.9
    assert d.osiris_grade == "Conforme"
    assert d.osiris_verdict == "PASS"


def test_osiris_scan_error_does_not_block(tmp_path: Path) -> None:
    """Osiris scan failed (error JSON) → UNKNOWN, ne bloque pas."""
    _write_all_pass(tmp_path)
    _write_tooling(tmp_path, "osiris.json", {"error": "osiris scan failed"})

    d = evaluate_deploy_decision(tmp_path)
    assert d.osiris_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"


# ── Axe SOIC (UNKNOWN traité comme FAIL) ────────────────────────────────────


def test_soic_gate_absent_treated_as_fail(tmp_path: Path) -> None:
    """SOIC gate absent → UNKNOWN, mais joint FAIL (no gate = no deploy)."""
    _write_tooling(tmp_path, "osiris.json", {"score": 7.4, "grade": "Conforme"})
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": 0.92}}})
    _write_tooling(
        tmp_path,
        "npm-audit.json",
        {"metadata": {"vulnerabilities": {"high": 0, "critical": 0}}},
    )

    d = evaluate_deploy_decision(tmp_path)
    assert d.soic_verdict == "UNKNOWN"
    assert d.joint_verdict == "FAIL"
    assert d.blockers == [AXIS_SOIC]


def test_soic_decision_accept_but_mu_below_threshold_fails(tmp_path: Path) -> None:
    """Edge case incohérence GateEngine : decision=ACCEPT mais μ<8.5 → FAIL strict."""
    _write_all_pass(tmp_path)
    _write_soic_gates(tmp_path, mu=8.2, decision="ACCEPT")

    d = evaluate_deploy_decision(tmp_path)
    assert d.soic_verdict == "FAIL"
    assert d.joint_verdict == "FAIL"


# ── Robustesse JSON ─────────────────────────────────────────────────────────


def test_corrupted_lighthouse_treated_as_unknown(tmp_path: Path) -> None:
    """lighthouse.json corrompu → UNKNOWN, pas de crash."""
    _write_all_pass(tmp_path)
    (tmp_path / "tooling" / "lighthouse.json").write_text("garbage{", encoding="utf-8")

    d = evaluate_deploy_decision(tmp_path)
    assert d.lighthouse_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"  # UNKNOWN ne bloque pas


def test_corrupted_npm_audit_treated_as_unknown(tmp_path: Path) -> None:
    """npm-audit.json corrompu → UNKNOWN."""
    _write_all_pass(tmp_path)
    (tmp_path / "tooling" / "npm-audit.json").write_text("not json", encoding="utf-8")

    d = evaluate_deploy_decision(tmp_path)
    assert d.npm_audit_verdict == "UNKNOWN"
    assert d.joint_verdict == "ACCEPT"


def test_lighthouse_score_non_numeric_treated_as_unknown(tmp_path: Path) -> None:
    """Lighthouse perf score non-numeric → UNKNOWN."""
    _write_all_pass(tmp_path)
    _write_tooling(tmp_path, "lighthouse.json", {"categories": {"performance": {"score": "n/a"}}})

    d = evaluate_deploy_decision(tmp_path)
    assert d.lighthouse_verdict == "UNKNOWN"
    assert d.lighthouse_perf is None


# ── Persistance + format ────────────────────────────────────────────────────


def test_persist_includes_all_4_axes(tmp_path: Path) -> None:
    """Le JSON persisté contient tous les champs des 4 axes."""
    _write_all_pass(tmp_path)
    d = evaluate_deploy_decision(tmp_path)
    persist_deploy_decision(d, tmp_path)
    reloaded = json.loads((tmp_path / DEPLOY_DECISION_FILENAME).read_text(encoding="utf-8"))
    for key in (
        "soic_mu",
        "soic_verdict",
        "osiris_score",
        "osiris_verdict",
        "lighthouse_perf",
        "lighthouse_verdict",
        "npm_audit_high",
        "npm_audit_critical",
        "npm_audit_verdict",
        "joint_verdict",
        "blockers",
    ):
        assert key in reloaded
    assert reloaded["joint_verdict"] == "ACCEPT"
    assert reloaded["blockers"] == []


def test_persist_is_idempotent(tmp_path: Path) -> None:
    """Appeler persist 2x produit le même contenu."""
    _write_all_pass(tmp_path)
    d = evaluate_deploy_decision(tmp_path)
    persist_deploy_decision(d, tmp_path)
    first = (tmp_path / DEPLOY_DECISION_FILENAME).read_text(encoding="utf-8")
    persist_deploy_decision(d, tmp_path)
    second = (tmp_path / DEPLOY_DECISION_FILENAME).read_text(encoding="utf-8")
    assert first == second


def test_format_axes_table_contains_4_axes() -> None:
    """Le tableau markdown contient les 4 axes + le verdict joint."""
    d = DeployDecision(
        soic_mu=9.11,
        soic_verdict="PASS",
        soic_threshold=8.5,
        osiris_score=4.0,
        osiris_grade="Critique",
        osiris_verdict="FAIL",
        osiris_threshold=6.0,
        lighthouse_perf=92.0,
        lighthouse_verdict="PASS",
        lighthouse_threshold=85.0,
        npm_audit_high=2,
        npm_audit_critical=0,
        npm_audit_verdict="FAIL",
        npm_audit_threshold=0,
        joint_verdict="FAIL",
        blockers=["osiris", "npm_audit"],
        warnings=[],
    )
    table = format_axes_table(d)
    assert "μ=9.11" in table
    assert "score=4.0" in table
    assert "Critique" in table
    assert "perf=92/100" in table
    assert "high=2" in table
    assert "critical=0" in table
    assert "blockers: osiris, npm_audit" in table
