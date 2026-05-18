"""Tests régression pour orchestrator.score_injection.

Couvre item N (P1) chantier dette pipeline — divergence agent Ph5 vs SOIC.
Source de vérité unique = SOIC GateEngine ; ce module substitue les
placeholders du rapport markdown par les valeurs SOIC officielles.

Garanties testées :
  - Substitution effective des placeholders supportés
  - Idempotence : rapport sans placeholder = pas de modification
  - Robustesse : gates/runs absents/corrompus = no-op (pas de crash)
  - Cohérence : le μ injecté correspond exactement à soic-gates.json
  - Tableau D1-D9 : pondération correcte, dimensions absentes signalées
"""

from __future__ import annotations

import json
from pathlib import Path

from orchestrator.score_injection import (
    PLACEHOLDER_DIM_TABLE,
    PLACEHOLDER_MU,
    PLACEHOLDER_THRESHOLD,
    PLACEHOLDER_VERDICT,
    inject_soic_scores,
)


def _write_gates(client_dir: Path, gates: list[dict]) -> Path:
    path = client_dir / "soic-gates.json"
    path.write_text(json.dumps(gates), encoding="utf-8")
    return path


def _write_runs(client_dir: Path, runs: list[dict]) -> Path:
    path = client_dir / "soic-runs.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in runs) + "\n", encoding="utf-8")
    return path


def _write_report(client_dir: Path, body: str) -> Path:
    path = client_dir / "ph5-qa-report.md"
    path.write_text(body, encoding="utf-8")
    return path


def test_substitute_mu_and_verdict(tmp_path: Path) -> None:
    """Les placeholders [[SOIC_MU]] et [[SOIC_VERDICT]] sont remplacés."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 9.10925, "decision": "ACCEPT", "threshold": 8.5}],
    )
    report = _write_report(
        tmp_path,
        f"μ = {PLACEHOLDER_MU} -> {PLACEHOLDER_VERDICT} (seuil {PLACEHOLDER_THRESHOLD})\n",
    )

    changed = inject_soic_scores(report, tmp_path)

    assert changed is True
    content = report.read_text(encoding="utf-8")
    assert PLACEHOLDER_MU not in content
    assert PLACEHOLDER_VERDICT not in content
    assert PLACEHOLDER_THRESHOLD not in content
    assert "9.11" in content
    assert "ACCEPT" in content
    assert "8.5" in content


def test_idempotent_when_no_placeholder(tmp_path: Path) -> None:
    """Un rapport sans placeholder n'est PAS modifié."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 9.11, "decision": "ACCEPT", "threshold": 8.5}],
    )
    original = "μ = 8.39 FAIL (rapport pré-fix, codé en dur)\n"
    report = _write_report(tmp_path, original)

    changed = inject_soic_scores(report, tmp_path)

    assert changed is False
    assert report.read_text(encoding="utf-8") == original


def test_missing_gates_returns_false(tmp_path: Path) -> None:
    """Sans soic-gates.json ni soic-runs.jsonl, no-op gracieux."""
    report = _write_report(tmp_path, f"μ = {PLACEHOLDER_MU}\n")

    changed = inject_soic_scores(report, tmp_path)

    assert changed is False
    assert PLACEHOLDER_MU in report.read_text(encoding="utf-8")


def test_missing_report_returns_false(tmp_path: Path) -> None:
    """Sans rapport, no-op gracieux (pas de crash)."""
    _write_gates(tmp_path, [{"phase": "ph5-qa", "mu": 9.11, "decision": "ACCEPT"}])

    changed = inject_soic_scores(tmp_path / "ph5-qa-report.md", tmp_path)

    assert changed is False


def test_corrupted_gates_json_returns_false(tmp_path: Path) -> None:
    """JSON corrompu = no-op (pas de crash)."""
    (tmp_path / "soic-gates.json").write_text("not json {", encoding="utf-8")
    report = _write_report(tmp_path, f"μ = {PLACEHOLDER_MU}\n")

    changed = inject_soic_scores(report, tmp_path)

    assert changed is False


def test_verdict_fail_when_not_accept(tmp_path: Path) -> None:
    """decision != 'ACCEPT' -> verdict 'FAIL'."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 7.5, "decision": "ITERATE", "threshold": 8.5}],
    )
    report = _write_report(tmp_path, f"{PLACEHOLDER_VERDICT}\n")

    inject_soic_scores(report, tmp_path)

    assert report.read_text(encoding="utf-8").strip() == "FAIL"


def test_takes_latest_ph5_gate_when_multiple(tmp_path: Path) -> None:
    """Si soic-gates.json contient plusieurs runs ph5-qa, on prend le dernier."""
    _write_gates(
        tmp_path,
        [
            {"phase": "ph5-qa", "mu": 7.52, "decision": "FAIL", "threshold": 8.5},
            {"phase": "ph5-qa", "mu": 9.11, "decision": "ACCEPT", "threshold": 8.5},
        ],
    )
    report = _write_report(tmp_path, f"{PLACEHOLDER_MU} {PLACEHOLDER_VERDICT}\n")

    inject_soic_scores(report, tmp_path)

    assert report.read_text(encoding="utf-8").strip() == "9.11 ACCEPT"


def test_dimension_scores_table_uses_runs_data(tmp_path: Path) -> None:
    """Le placeholder [[SOIC_DIM_SCORES_TABLE]] est remplacé par un tableau D1-D9."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 9.11, "decision": "ACCEPT", "threshold": 8.5}],
    )
    _write_runs(
        tmp_path,
        [
            {
                "phase": "ph5-qa",
                "dimension_scores": {
                    "D1": 10.0,
                    "D2": 8.5,
                    "D4": 9.44,
                    "D5": 9.6,
                    "D6": 10.0,
                    "D7": 6.6,
                    "D8": 8.5,
                    "D9": 9.75,
                },
                "mu": 9.07,
            },
        ],
    )
    report = _write_report(tmp_path, f"{PLACEHOLDER_DIM_TABLE}\n")

    inject_soic_scores(report, tmp_path)

    content = report.read_text(encoding="utf-8")
    assert PLACEHOLDER_DIM_TABLE not in content
    assert "| D1 | Architecture | 10.00 | ×1.0 |" in content
    assert "| D3 | Tests | — | ×0.9 | — | NOT_EVALUATED |" in content
    assert "| D4 | Securite | 9.44 | ×1.2 |" in content
    assert "**μ** | **Score Final**" in content


def test_individual_dimension_placeholder(tmp_path: Path) -> None:
    """Les placeholders [[SOIC_D4]] etc. sont substitués individuellement."""
    _write_gates(tmp_path, [{"phase": "ph5-qa", "mu": 9.11, "decision": "ACCEPT"}])
    _write_runs(
        tmp_path,
        [{"phase": "ph5-qa", "dimension_scores": {"D4": 9.44, "D8": 8.50}}],
    )
    report = _write_report(tmp_path, "D4=[[SOIC_D4]] D8=[[SOIC_D8]] D3=[[SOIC_D3]]\n")

    inject_soic_scores(report, tmp_path)

    content = report.read_text(encoding="utf-8").strip()
    assert content == "D4=9.44 D8=8.50 D3=N/A"


def test_report_mu_matches_gates_mu_exactly(tmp_path: Path) -> None:
    """Régression clé du P1 : μ injecté = μ de soic-gates.json (2 décimales).

    Cas concret depanneur-nobert 2026-05-15 : avant fix, rapport disait 8.39
    alors que soic-gates.json disait 9.10925. Après fix, le rapport DOIT
    refléter exactement la valeur SOIC.
    """
    gates_mu = 9.10925925925926
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": gates_mu, "decision": "ACCEPT", "threshold": 8.5}],
    )
    report = _write_report(tmp_path, f"Score Final {PLACEHOLDER_MU}\n")

    inject_soic_scores(report, tmp_path)

    content = report.read_text(encoding="utf-8").strip()
    # On vérifie qu'aucun ancien score divergent (ex 8.39) ne subsiste,
    # et que la valeur affichée est bien dérivée de gates_mu arrondie 2 décimales.
    assert content == "Score Final 9.11"
    assert "8.39" not in content


# ── P9 D2 : intégration dual-axis Osiris ────────────────────────────────────


def test_osiris_placeholders_substituted_and_decision_persisted(tmp_path: Path) -> None:
    """[[OSIRIS_*]] + [[JOINT_*]] sont substitués, deploy-decision.json est écrit."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 9.10, "decision": "ACCEPT", "threshold": 8.5}],
    )
    _write_runs(tmp_path, [{"phase": "ph5-qa", "mu": 9.10, "dimension_scores": {}}])
    tooling = tmp_path / "tooling"
    tooling.mkdir()
    (tooling / "osiris.json").write_text(
        json.dumps({"osiris_score": 4.0, "grade": "Critique"}), encoding="utf-8"
    )

    report = _write_report(
        tmp_path,
        "μ=[[SOIC_MU]] osiris=[[OSIRIS_SCORE]]/[[OSIRIS_GRADE]] "
        "osiris_verdict=[[OSIRIS_VERDICT]] joint=[[JOINT_VERDICT]] blocker=[[JOINT_BLOCKER]]",
    )

    assert inject_soic_scores(report, tmp_path) is True
    content = report.read_text(encoding="utf-8")
    assert "μ=9.10" in content
    assert "osiris=4.0/Critique" in content
    assert "osiris_verdict=FAIL" in content  # 4.0 < 6.0
    assert "joint=FAIL" in content  # SOIC PASS mais Osiris FAIL
    assert "blocker=osiris" in content

    # deploy-decision.json persisté à la racine du client
    deploy_path = tmp_path / "deploy-decision.json"
    assert deploy_path.exists()
    persisted = json.loads(deploy_path.read_text(encoding="utf-8"))
    assert persisted["joint_verdict"] == "FAIL"
    assert persisted["blocker"] == "osiris"


def test_dual_axis_table_renders_full_markdown(tmp_path: Path) -> None:
    """[[DUAL_AXIS_TABLE]] insère le tableau 3 lignes complet."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 9.46, "decision": "ACCEPT", "threshold": 8.5}],
    )
    _write_runs(tmp_path, [{"phase": "ph5-qa", "mu": 9.46, "dimension_scores": {}}])
    tooling = tmp_path / "tooling"
    tooling.mkdir()
    (tooling / "osiris.json").write_text(
        json.dumps({"osiris_score": 7.4, "grade": "Conforme"}), encoding="utf-8"
    )

    report = _write_report(tmp_path, "[[DUAL_AXIS_TABLE]]")
    assert inject_soic_scores(report, tmp_path) is True
    content = report.read_text(encoding="utf-8")
    assert "| Axe | Mesure | Seuil | Verdict | Source |" in content
    assert "μ=9.46" in content
    assert "score=7.4" in content
    assert "Conforme" in content
    assert "**ACCEPT**" in content
    assert "blocker: —" in content


def test_osiris_unknown_does_not_block_joint(tmp_path: Path) -> None:
    """SOIC ACCEPT + Osiris UNKNOWN (file absent) → joint ACCEPT, warning."""
    _write_gates(
        tmp_path,
        [{"phase": "ph5-qa", "mu": 9.0, "decision": "ACCEPT", "threshold": 8.5}],
    )
    _write_runs(tmp_path, [{"phase": "ph5-qa", "mu": 9.0, "dimension_scores": {}}])
    # Pas de tooling/osiris.json

    report = _write_report(tmp_path, "verdict=[[JOINT_VERDICT]] osiris=[[OSIRIS_VERDICT]]")
    assert inject_soic_scores(report, tmp_path) is True
    content = report.read_text(encoding="utf-8")
    assert "verdict=ACCEPT" in content
    assert "osiris=UNKNOWN" in content

    persisted = json.loads((tmp_path / "deploy-decision.json").read_text(encoding="utf-8"))
    assert any("Osiris report absent" in w for w in persisted["warnings"])
