"""Injection du score SOIC officiel + Osiris dans ph5-qa-report.md.

Source de vérité unique pour le score Ph5 = SOIC GateEngine (déterministe).
L'agent Ph5 rédige le rapport qualitatif avec des placeholders ; ce module
substitue les placeholders avec les valeurs mesurées par SOIC en
post-traitement.

P9 D2 (2026-05-18) : ajout du verdict dual-axis (SOIC + Osiris). SOIC mesure
la qualité technique (D1-D9), Osiris mesure la santé opérationnelle externe.
Verdict deploy joint = `μ_SOIC ≥ 8.5` ET `osiris_score ≥ 6.0`. Le blocker est
traçable au gate qui a fail (pas de score composite opaque).

Placeholders SOIC :
    [[SOIC_MU]]                 -> "9.11"  (2 décimales)
    [[SOIC_VERDICT]]            -> "ACCEPT" | "FAIL"
    [[SOIC_THRESHOLD]]          -> "8.5"
    [[SOIC_DIM_SCORES_TABLE]]   -> tableau markdown D1-D9 complet
    [[SOIC_D1]] ... [[SOIC_D9]] -> score par dimension (2 décimales)

Placeholders Osiris + Lighthouse + npm audit + joint (P9 D2 + extension) :
    [[OSIRIS_SCORE]]            -> "4.0" | "UNKNOWN"
    [[OSIRIS_GRADE]]            -> "Critique" | "Conforme" | "UNKNOWN"
    [[OSIRIS_VERDICT]]          -> "PASS" | "FAIL" | "UNKNOWN"
    [[OSIRIS_THRESHOLD]]        -> "6.0"
    [[LIGHTHOUSE_PERF]]         -> "92" (0-100) | "UNKNOWN"
    [[LIGHTHOUSE_VERDICT]]      -> "PASS" | "FAIL" | "UNKNOWN"
    [[LIGHTHOUSE_THRESHOLD]]    -> "85"
    [[NPM_AUDIT_HIGH]]          -> "0" | "UNKNOWN"
    [[NPM_AUDIT_CRITICAL]]      -> "0" | "UNKNOWN"
    [[NPM_AUDIT_VERDICT]]       -> "PASS" | "FAIL" | "UNKNOWN"
    [[JOINT_VERDICT]]           -> "ACCEPT" | "FAIL"
    [[JOINT_BLOCKERS]]          -> "osiris, npm_audit" | "—"
    [[DUAL_AXIS_TABLE]]         -> tableau markdown 4 axes + verdict joint
                                   (nom historique conservé pour compat ; le tableau
                                    contient maintenant 4 axes, pas 2)

Item N (P1) — chantier dette pipeline 2026-05-15.
Item D2 (P9) — dual-axis 2026-05-18.
Extension (2026-05-18) — axes Lighthouse + npm audit.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nexos.deploy_decision import (
    DeployDecision,
    evaluate_deploy_decision,
    format_axes_table,
    persist_deploy_decision,
)
from soic.dimensions import DIMENSIONS

PLACEHOLDER_MU = "[[SOIC_MU]]"
PLACEHOLDER_VERDICT = "[[SOIC_VERDICT]]"
PLACEHOLDER_THRESHOLD = "[[SOIC_THRESHOLD]]"
PLACEHOLDER_DIM_TABLE = "[[SOIC_DIM_SCORES_TABLE]]"
_PLACEHOLDER_DIM_MARKER = "[[SOIC_D"  # détection [[SOIC_D1]] ... [[SOIC_D9]]

PLACEHOLDER_OSIRIS_SCORE = "[[OSIRIS_SCORE]]"
PLACEHOLDER_OSIRIS_GRADE = "[[OSIRIS_GRADE]]"
PLACEHOLDER_OSIRIS_VERDICT = "[[OSIRIS_VERDICT]]"
PLACEHOLDER_OSIRIS_THRESHOLD = "[[OSIRIS_THRESHOLD]]"
PLACEHOLDER_LIGHTHOUSE_PERF = "[[LIGHTHOUSE_PERF]]"
PLACEHOLDER_LIGHTHOUSE_VERDICT = "[[LIGHTHOUSE_VERDICT]]"
PLACEHOLDER_LIGHTHOUSE_THRESHOLD = "[[LIGHTHOUSE_THRESHOLD]]"
PLACEHOLDER_NPM_AUDIT_HIGH = "[[NPM_AUDIT_HIGH]]"
PLACEHOLDER_NPM_AUDIT_CRITICAL = "[[NPM_AUDIT_CRITICAL]]"
PLACEHOLDER_NPM_AUDIT_VERDICT = "[[NPM_AUDIT_VERDICT]]"
PLACEHOLDER_JOINT_VERDICT = "[[JOINT_VERDICT]]"
PLACEHOLDER_JOINT_BLOCKERS = "[[JOINT_BLOCKERS]]"
PLACEHOLDER_DUAL_AXIS_TABLE = "[[DUAL_AXIS_TABLE]]"

# Rétrocompat : alias historique singulier conservé pour les rapports legacy
PLACEHOLDER_JOINT_BLOCKER = "[[JOINT_BLOCKER]]"


def _load_latest_gate(soic_gates_path: Path, phase: str) -> dict[str, Any] | None:
    """Récupère le dernier gate d'une phase depuis soic-gates.json."""
    if not soic_gates_path.exists():
        return None
    try:
        gates = json.loads(soic_gates_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(gates, list):
        return None
    matching = [g for g in gates if isinstance(g, dict) and g.get("phase") == phase]
    return matching[-1] if matching else None


def _load_latest_run(runs_path: Path, phase: str) -> dict[str, Any] | None:
    """Récupère le dernier run d'une phase depuis soic-runs.jsonl (NDJSON).

    Parcourt le fichier en arrière pour s'arrêter au run le plus récent.
    Tolère les lignes JSON invalides (les saute silencieusement).
    """
    if not runs_path.exists():
        return None
    try:
        lines = runs_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        if not line.strip():
            continue
        try:
            run = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(run, dict) and run.get("phase") == phase:
            return run
    return None


def _status_for_score(score: float) -> str:
    """Convention statut par score : ≥8.5 PASS, [7.0-8.5[ PASS réserve, <7.0 FAIL."""
    if score >= 8.5:
        return "PASS"
    if score >= 7.0:
        return "PASS réserve"
    return "FAIL"


def _format_dimension_scores_table(dim_scores: dict[str, float]) -> str:
    """Génère le tableau markdown D1-D9 avec score, poids, pondéré, statut.

    Dimensions absentes -> ligne `NOT_EVALUATED` (visible dans le rapport).
    μ final calculé sur les dimensions présentes (cohérent avec calculate_mu).
    """
    lines = [
        "| Dim | Nom | Score | Poids | Pondéré | Statut |",
        "|-----|-----|------:|------:|--------:|--------|",
    ]
    total_weighted = 0.0
    total_weight = 0.0
    for dim_id in sorted(DIMENSIONS.keys()):
        meta = DIMENSIONS[dim_id]
        name = meta["name"]
        weight = float(meta["weight"])
        score = dim_scores.get(dim_id)
        if score is None:
            lines.append(f"| {dim_id} | {name} | — | ×{weight:.1f} | — | NOT_EVALUATED |")
            continue
        weighted = score * weight
        total_weighted += weighted
        total_weight += weight
        status = _status_for_score(score)
        lines.append(
            f"| {dim_id} | {name} | {score:.2f} | ×{weight:.1f} | {weighted:.2f} | {status} |"
        )
    mu = total_weighted / total_weight if total_weight else 0.0
    lines.append(f"| **μ** | **Score Final** | | | **{mu:.2f}** | |")
    return "\n".join(lines)


def _has_any_placeholder(content: str) -> bool:
    """True si le rapport contient au moins un placeholder SOIC ou multi-axes."""
    fixed_placeholders = (
        PLACEHOLDER_MU,
        PLACEHOLDER_VERDICT,
        PLACEHOLDER_THRESHOLD,
        PLACEHOLDER_DIM_TABLE,
        PLACEHOLDER_OSIRIS_SCORE,
        PLACEHOLDER_OSIRIS_GRADE,
        PLACEHOLDER_OSIRIS_VERDICT,
        PLACEHOLDER_OSIRIS_THRESHOLD,
        PLACEHOLDER_LIGHTHOUSE_PERF,
        PLACEHOLDER_LIGHTHOUSE_VERDICT,
        PLACEHOLDER_LIGHTHOUSE_THRESHOLD,
        PLACEHOLDER_NPM_AUDIT_HIGH,
        PLACEHOLDER_NPM_AUDIT_CRITICAL,
        PLACEHOLDER_NPM_AUDIT_VERDICT,
        PLACEHOLDER_JOINT_VERDICT,
        PLACEHOLDER_JOINT_BLOCKERS,
        PLACEHOLDER_JOINT_BLOCKER,
        PLACEHOLDER_DUAL_AXIS_TABLE,
    )
    if any(ph in content for ph in fixed_placeholders):
        return True
    return _PLACEHOLDER_DIM_MARKER in content


def _inject_multi_axis(content: str, decision: DeployDecision) -> str:
    """Substitue les placeholders Osiris + Lighthouse + npm audit + joint."""
    osiris_score_str = (
        f"{decision.osiris_score:.1f}" if decision.osiris_score is not None else "UNKNOWN"
    )
    osiris_grade_str = decision.osiris_grade or "UNKNOWN"
    lh_perf_str = (
        f"{decision.lighthouse_perf:.0f}" if decision.lighthouse_perf is not None else "UNKNOWN"
    )
    npm_high_str = "UNKNOWN" if decision.npm_audit_high is None else str(decision.npm_audit_high)
    npm_crit_str = (
        "UNKNOWN" if decision.npm_audit_critical is None else str(decision.npm_audit_critical)
    )
    blockers_str = ", ".join(decision.blockers) if decision.blockers else "—"

    content = content.replace(PLACEHOLDER_OSIRIS_SCORE, osiris_score_str)
    content = content.replace(PLACEHOLDER_OSIRIS_GRADE, osiris_grade_str)
    content = content.replace(PLACEHOLDER_OSIRIS_VERDICT, decision.osiris_verdict)
    content = content.replace(PLACEHOLDER_OSIRIS_THRESHOLD, f"{decision.osiris_threshold:.1f}")
    content = content.replace(PLACEHOLDER_LIGHTHOUSE_PERF, lh_perf_str)
    content = content.replace(PLACEHOLDER_LIGHTHOUSE_VERDICT, decision.lighthouse_verdict)
    content = content.replace(
        PLACEHOLDER_LIGHTHOUSE_THRESHOLD, f"{decision.lighthouse_threshold:.0f}"
    )
    content = content.replace(PLACEHOLDER_NPM_AUDIT_HIGH, npm_high_str)
    content = content.replace(PLACEHOLDER_NPM_AUDIT_CRITICAL, npm_crit_str)
    content = content.replace(PLACEHOLDER_NPM_AUDIT_VERDICT, decision.npm_audit_verdict)
    content = content.replace(PLACEHOLDER_JOINT_VERDICT, decision.joint_verdict)
    content = content.replace(PLACEHOLDER_JOINT_BLOCKERS, blockers_str)
    # Rétrocompat : legacy [[JOINT_BLOCKER]] singulier → premier blocker (ou —)
    legacy_blocker = decision.blockers[0] if decision.blockers else "—"
    content = content.replace(PLACEHOLDER_JOINT_BLOCKER, legacy_blocker)
    if PLACEHOLDER_DUAL_AXIS_TABLE in content:
        content = content.replace(PLACEHOLDER_DUAL_AXIS_TABLE, format_axes_table(decision))
    return content


def inject_soic_scores(report_path: Path, client_dir: Path) -> bool:
    """Substitue les placeholders SOIC + Osiris (dual-axis) dans ph5-qa-report.md.

    Args:
        report_path: chemin vers ph5-qa-report.md.
        client_dir:  dossier client (contient soic-gates.json, soic-runs.jsonl,
                     tooling/osiris.json).

    Retourne True si une substitution a été effectuée, False sinon
    (rapport sans placeholder, gates absents, ou rapport inexistant).
    Idempotent : un fichier sans placeholder est laissé intact.

    Effet de bord : si au moins une donnée est lisible (SOIC ou Osiris),
    persiste `deploy-decision.json` à la racine du client avec le verdict
    joint à 2 axes (P9 D2). Ceci tourne avant la substitution markdown pour
    garantir que deploy-decision.json reflète bien l'état pris en compte
    pour les placeholders.
    """
    if not report_path.exists():
        return False
    content = report_path.read_text(encoding="utf-8")
    if not _has_any_placeholder(content):
        return False

    gate = _load_latest_gate(client_dir / "soic-gates.json", "ph5-qa")
    run = _load_latest_run(client_dir / "soic-runs.jsonl", "ph5-qa")
    if gate is None and run is None:
        return False

    # P9 D2 — verdict dual-axis SOIC + Osiris, persisté avant injection markdown.
    deploy_decision = evaluate_deploy_decision(client_dir)
    persist_deploy_decision(deploy_decision, client_dir)

    mu = (gate or {}).get("mu")
    if mu is None and run is not None:
        mu = run.get("mu")
    decision = (gate or {}).get("decision", "")
    verdict = "ACCEPT" if decision == "ACCEPT" else "FAIL"
    threshold = (gate or {}).get("threshold")

    raw_dim_scores = (run or {}).get("dimension_scores", {}) if isinstance(run, dict) else {}
    dim_scores: dict[str, float] = {}
    if isinstance(raw_dim_scores, dict):
        for k, v in raw_dim_scores.items():
            if isinstance(v, (int, float)):
                dim_scores[str(k)] = float(v)

    original = content
    if mu is not None and isinstance(mu, (int, float)):
        content = content.replace(PLACEHOLDER_MU, f"{float(mu):.2f}")
    content = content.replace(PLACEHOLDER_VERDICT, verdict)
    if threshold is not None and isinstance(threshold, (int, float)):
        content = content.replace(PLACEHOLDER_THRESHOLD, f"{float(threshold):.1f}")

    if PLACEHOLDER_DIM_TABLE in content:
        table = _format_dimension_scores_table(dim_scores)
        content = content.replace(PLACEHOLDER_DIM_TABLE, table)

    for dim_id in DIMENSIONS:
        ph = f"[[SOIC_{dim_id}]]"
        if ph in content:
            value = dim_scores.get(dim_id)
            content = content.replace(ph, f"{value:.2f}" if value is not None else "N/A")

    # P9 D2 + extension — substitution des placeholders Osiris + Lighthouse +
    # npm audit + verdict joint multi-axes.
    content = _inject_multi_axis(content, deploy_decision)

    if content == original:
        return False
    report_path.write_text(content, encoding="utf-8")
    return True


__all__ = [
    "PLACEHOLDER_DIM_TABLE",
    "PLACEHOLDER_DUAL_AXIS_TABLE",
    "PLACEHOLDER_JOINT_BLOCKER",
    "PLACEHOLDER_JOINT_BLOCKERS",
    "PLACEHOLDER_JOINT_VERDICT",
    "PLACEHOLDER_LIGHTHOUSE_PERF",
    "PLACEHOLDER_LIGHTHOUSE_THRESHOLD",
    "PLACEHOLDER_LIGHTHOUSE_VERDICT",
    "PLACEHOLDER_MU",
    "PLACEHOLDER_NPM_AUDIT_CRITICAL",
    "PLACEHOLDER_NPM_AUDIT_HIGH",
    "PLACEHOLDER_NPM_AUDIT_VERDICT",
    "PLACEHOLDER_OSIRIS_GRADE",
    "PLACEHOLDER_OSIRIS_SCORE",
    "PLACEHOLDER_OSIRIS_THRESHOLD",
    "PLACEHOLDER_OSIRIS_VERDICT",
    "PLACEHOLDER_THRESHOLD",
    "PLACEHOLDER_VERDICT",
    "inject_soic_scores",
]
