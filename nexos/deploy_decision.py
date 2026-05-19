"""NEXOS — Verdict deploy à N axes : SOIC + Osiris + Lighthouse + npm audit + pa11y.

Architecture séparée de la mesure et de la décision :
- SOIC garde sa souveraineté sur D1-D9 (technique interne, ce que le pipeline contrôle).
- Osiris reste un signal externe distinct (santé opérationnelle réelle).
- Lighthouse perf score = signal performance web (Core Web Vitals composite).
- npm audit HIGH+CRITICAL count = signal supply chain (zero tolerance).
- pa11y error count = signal accessibilité WCAG (zero tolerance pour erreurs).

Le verdict deploy est composite : TOUS les axes doivent être PASS (ou UNKNOWN) pour
ACCEPT. Si bloqué, `blockers: list[str]` énumère exactement les axes responsables —
pas de score composite opaque.

P9 D2 (2026-05-18) : pattern dual-axis initial (SOIC + Osiris).
Extension (2026-05-18 suite) : axes 3 (Lighthouse) + 4 (npm audit).
Extension² (2026-05-18 suite) : axe 5 (pa11y a11y) — démontre la généricité du pattern.
Le pattern reste extensible : build status, lighthouse a11y/SEO/best-practices,
custom gates peuvent être ajoutés comme axes 6+ sans toucher aux axes existants.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

JointVerdict = Literal["ACCEPT", "FAIL"]
AxisVerdict = Literal["PASS", "FAIL", "UNKNOWN"]

SOIC_GATES_FILENAME = "soic-gates.json"
OSIRIS_TOOLING_FILENAME = "osiris.json"
LIGHTHOUSE_TOOLING_FILENAME = "lighthouse.json"
NPM_AUDIT_TOOLING_FILENAME = "npm-audit.json"
PA11Y_TOOLING_FILENAME = "a11y.json"
DEPLOY_DECISION_FILENAME = "deploy-decision.json"

# Axes canoniques (ordre stable pour rapports + blockers)
AXIS_SOIC = "soic"
AXIS_OSIRIS = "osiris"
AXIS_LIGHTHOUSE = "lighthouse"
AXIS_NPM_AUDIT = "npm_audit"
AXIS_PA11Y = "pa11y"


@dataclass(frozen=True)
class DeployDecision:
    """Verdict deploy composite, traçable aux N axes sources."""

    # SOIC axis — qualité technique interne (D1-D9)
    soic_mu: float | None
    soic_verdict: AxisVerdict
    soic_threshold: float

    # Osiris axis — santé opérationnelle externe (8 sous-axes O/S/I/R/V/L/A/E)
    osiris_score: float | None
    osiris_grade: str | None
    osiris_verdict: AxisVerdict
    osiris_threshold: float

    # Lighthouse axis — performance web (Core Web Vitals composite)
    lighthouse_perf: float | None  # normalisé 0-100
    lighthouse_verdict: AxisVerdict
    lighthouse_threshold: float

    # npm audit axis — supply chain (HIGH + CRITICAL CVE count)
    npm_audit_high: int | None
    npm_audit_critical: int | None
    npm_audit_verdict: AxisVerdict
    npm_audit_threshold: int

    # pa11y axis — accessibilité WCAG (error count)
    pa11y_errors: int | None
    pa11y_warnings_count: int | None
    pa11y_verdict: AxisVerdict
    pa11y_threshold: int

    # Joint
    joint_verdict: JointVerdict
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ── Lecteurs de fichiers (defensive) ────────────────────────────────────────


def _load_latest_soic_gate(client_dir: Path, phase: str = "ph5-qa") -> dict[str, Any] | None:
    """Lit le dernier gate SOIC d'une phase depuis soic-gates.json (defensive)."""
    path = client_dir / SOIC_GATES_FILENAME
    if not path.exists():
        return None
    try:
        gates = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(gates, list):
        return None
    matching = [g for g in gates if isinstance(g, dict) and g.get("phase") == phase]
    return matching[-1] if matching else None


def _load_tooling_json(client_dir: Path, filename: str) -> dict[str, Any] | None:
    """Lit tooling/<filename> en tant qu'objet JSON (defensive)."""
    path = client_dir / "tooling" / filename
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _load_tooling_list(client_dir: Path, filename: str) -> list[dict[str, Any]] | None:
    """Lit tooling/<filename> en tant que list JSON (pa11y a11y.json schema)."""
    path = client_dir / "tooling" / filename
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, list) else None


# ── Extracteurs par axe ─────────────────────────────────────────────────────


def _extract_osiris_axis(
    report: dict[str, Any] | None,
    threshold: float,
) -> tuple[float | None, str | None, AxisVerdict, list[str]]:
    """Décode tooling/osiris.json en (score, grade, verdict, warnings).

    Politique UNKNOWN : missing / scan error / non-numeric → ne bloque pas.
    Le JSON brut Osiris scanner.py utilise `score` ; le RunStore SOIC utilise
    `osiris_score` ; on tolère les deux.
    """
    if report is None:
        return None, None, "UNKNOWN", ["Osiris report absent (tooling/osiris.json missing)"]

    if "error" in report and "osiris_score" not in report and "score" not in report:
        err = str(report.get("error", "unknown"))[:120]
        return None, None, "UNKNOWN", [f"Osiris scan failed: {err}"]

    score = report.get("osiris_score")
    if score is None:
        score = report.get("score")
    if not isinstance(score, (int, float)):
        return None, None, "UNKNOWN", ["Osiris score missing or non-numeric"]

    grade = report.get("grade")
    grade_str = str(grade) if isinstance(grade, str) else None
    score_f = float(score)
    verdict: AxisVerdict = "PASS" if score_f >= threshold else "FAIL"
    return score_f, grade_str, verdict, []


def _extract_lighthouse_axis(
    report: dict[str, Any] | None,
    threshold: float,
) -> tuple[float | None, AxisVerdict, list[str]]:
    """Décode tooling/lighthouse.json en (perf_score_0_100, verdict, warnings).

    Lighthouse écrit `categories.performance.score` sur 0-1 ; on multiplie par 100
    pour avoir un score lisible (cohérent avec la convention humaine 0-100).

    Politique UNKNOWN : missing / score non-numeric → ne bloque pas (don't punish
    missing signal — un site peut ne pas avoir tourné lighthouse sans que ce soit
    bloquant pour le verdict joint).
    """
    if report is None:
        return None, "UNKNOWN", ["Lighthouse report absent (tooling/lighthouse.json missing)"]

    perf_section = report.get("categories", {}).get("performance")
    if not isinstance(perf_section, dict):
        return None, "UNKNOWN", ["Lighthouse categories.performance missing"]
    raw_score = perf_section.get("score")
    if not isinstance(raw_score, (int, float)):
        return None, "UNKNOWN", ["Lighthouse performance.score missing or non-numeric"]

    perf_100 = float(raw_score) * 100.0
    verdict: AxisVerdict = "PASS" if perf_100 >= threshold else "FAIL"
    return perf_100, verdict, []


def _extract_pa11y_axis(
    issues: list[dict[str, Any]] | None,
    threshold: int,
) -> tuple[int | None, int | None, AxisVerdict, list[str]]:
    """Décode tooling/a11y.json en (errors, warnings, verdict, warnings_log).

    Schema pa11y JSON : list d'issues, chacune avec `type` in
    {"error", "warning", "notice"}.

    Politique FAIL : error_count > threshold → FAIL. Zero tolerance par défaut
    (threshold=0) cohérent avec npm audit et la convention pa11y prod-ready.

    Politique UNKNOWN : missing / structure invalide → ne bloque pas. Permet
    de déployer même si pa11y n'a pas tourné (preflight optionnel sur certains
    pipelines).
    """
    if issues is None:
        return None, None, "UNKNOWN", ["pa11y report absent (tooling/a11y.json missing)"]

    error_count = 0
    warning_count = 0
    for issue in issues:
        if not isinstance(issue, dict):
            continue
        t = issue.get("type")
        if t == "error":
            error_count += 1
        elif t == "warning":
            warning_count += 1

    verdict: AxisVerdict = "PASS" if error_count <= threshold else "FAIL"
    return error_count, warning_count, verdict, []


def _extract_npm_audit_axis(
    report: dict[str, Any] | None,
    threshold: int,
) -> tuple[int | None, int | None, AxisVerdict, list[str]]:
    """Décode tooling/npm-audit.json en (high, critical, verdict, warnings).

    Schema npm audit JSON : `metadata.vulnerabilities.{high,critical}` (int counts).

    Politique FAIL : (high + critical) > threshold → FAIL. Aligné CLAUDE.md règle
    absolue "npm audit = 0 vulnérabilités HIGH/CRITICAL".

    Politique UNKNOWN : missing / structure invalide → ne bloque pas.
    """
    if report is None:
        return None, None, "UNKNOWN", ["npm audit report absent (tooling/npm-audit.json missing)"]

    vulns = report.get("metadata", {}).get("vulnerabilities")
    if not isinstance(vulns, dict):
        return None, None, "UNKNOWN", ["npm audit metadata.vulnerabilities missing"]

    high = vulns.get("high")
    critical = vulns.get("critical")
    if not isinstance(high, int) or not isinstance(critical, int):
        return None, None, "UNKNOWN", ["npm audit high/critical counts missing or non-int"]

    total = high + critical
    verdict: AxisVerdict = "PASS" if total <= threshold else "FAIL"
    return high, critical, verdict, []


# ── Calcul du verdict joint ─────────────────────────────────────────────────


def _compute_joint(
    axis_verdicts: dict[str, AxisVerdict],
) -> tuple[JointVerdict, list[str]]:
    """Logique deploy joint N-axes :
    - TOUS les axes PASS ou UNKNOWN → ACCEPT, blockers=[]
    - Au moins un FAIL → FAIL, blockers = liste des axes en FAIL (ordre stable)
    - SOIC UNKNOWN traité comme FAIL en amont par evaluate_deploy_decision
      (pas de gate = pas de deploy ; autres axes UNKNOWN tolérés).
    """
    failed = [axis for axis, verdict in axis_verdicts.items() if verdict == "FAIL"]
    if failed:
        return "FAIL", failed
    return "ACCEPT", []


def evaluate_deploy_decision(
    client_dir: Path,
    osiris_threshold: float = 6.0,
    soic_threshold: float = 8.5,
    lighthouse_threshold: float = 85.0,
    npm_audit_threshold: int = 0,
    pa11y_threshold: int = 0,
) -> DeployDecision:
    """Calcule le verdict deploy à 5 axes pour un client.

    Args:
        client_dir: dossier client (contient soic-gates.json + tooling/*.json).
        osiris_threshold: seuil minimum osiris_score pour PASS (défaut 6.0).
        soic_threshold: seuil μ_SOIC pour PASS (défaut 8.5).
        lighthouse_threshold: seuil minimum perf 0-100 pour PASS (défaut 85.0).
        npm_audit_threshold: max HIGH+CRITICAL count pour PASS (défaut 0).
        pa11y_threshold: max pa11y error count pour PASS (défaut 0).

    Returns:
        DeployDecision immuable, prête à sérialiser.
    """
    warnings: list[str] = []

    # SOIC axis (special — UNKNOWN traité comme FAIL pour joint)
    gate = _load_latest_soic_gate(client_dir)
    soic_mu: float | None = None
    soic_verdict: AxisVerdict = "UNKNOWN"

    if gate is not None:
        raw_mu = gate.get("mu")
        if isinstance(raw_mu, (int, float)):
            soic_mu = float(raw_mu)
        decision = gate.get("decision", "")
        if decision == "ACCEPT" and soic_mu is not None and soic_mu >= soic_threshold:
            soic_verdict = "PASS"
        elif soic_mu is None:
            soic_verdict = "UNKNOWN"
            warnings.append("SOIC mu missing in soic-gates.json")
        else:
            soic_verdict = "FAIL"
    else:
        warnings.append("SOIC gate ph5-qa absent (soic-gates.json missing or empty)")

    # Osiris axis
    osiris_report = _load_tooling_json(client_dir, OSIRIS_TOOLING_FILENAME)
    osiris_score, osiris_grade, osiris_verdict, osiris_warns = _extract_osiris_axis(
        osiris_report, osiris_threshold
    )
    warnings.extend(osiris_warns)

    # Lighthouse axis
    lh_report = _load_tooling_json(client_dir, LIGHTHOUSE_TOOLING_FILENAME)
    lh_perf, lh_verdict, lh_warns = _extract_lighthouse_axis(lh_report, lighthouse_threshold)
    warnings.extend(lh_warns)

    # npm audit axis
    npm_report = _load_tooling_json(client_dir, NPM_AUDIT_TOOLING_FILENAME)
    npm_high, npm_crit, npm_verdict, npm_warns = _extract_npm_audit_axis(
        npm_report, npm_audit_threshold
    )
    warnings.extend(npm_warns)

    # pa11y axis (a11y.json est un schema list, pas dict)
    pa11y_issues = _load_tooling_list(client_dir, PA11Y_TOOLING_FILENAME)
    pa11y_errors, pa11y_warns_count, pa11y_verdict, pa11y_warns = _extract_pa11y_axis(
        pa11y_issues, pa11y_threshold
    )
    warnings.extend(pa11y_warns)

    # SOIC UNKNOWN → FAIL pour joint (pas de gate = pas de deploy)
    soic_for_joint: AxisVerdict = soic_verdict if soic_verdict != "UNKNOWN" else "FAIL"
    joint, blockers = _compute_joint(
        {
            AXIS_SOIC: soic_for_joint,
            AXIS_OSIRIS: osiris_verdict,
            AXIS_LIGHTHOUSE: lh_verdict,
            AXIS_NPM_AUDIT: npm_verdict,
            AXIS_PA11Y: pa11y_verdict,
        }
    )

    return DeployDecision(
        soic_mu=soic_mu,
        soic_verdict=soic_verdict,
        soic_threshold=soic_threshold,
        osiris_score=osiris_score,
        osiris_grade=osiris_grade,
        osiris_verdict=osiris_verdict,
        osiris_threshold=osiris_threshold,
        lighthouse_perf=lh_perf,
        lighthouse_verdict=lh_verdict,
        lighthouse_threshold=lighthouse_threshold,
        npm_audit_high=npm_high,
        npm_audit_critical=npm_crit,
        npm_audit_verdict=npm_verdict,
        npm_audit_threshold=npm_audit_threshold,
        pa11y_errors=pa11y_errors,
        pa11y_warnings_count=pa11y_warns_count,
        pa11y_verdict=pa11y_verdict,
        pa11y_threshold=pa11y_threshold,
        joint_verdict=joint,
        blockers=blockers,
        warnings=warnings,
    )


def persist_deploy_decision(decision: DeployDecision, client_dir: Path) -> Path:
    """Écrit deploy-decision.json à la racine du client (idempotent, overwrite)."""
    path = client_dir / DEPLOY_DECISION_FILENAME
    path.write_text(
        json.dumps(decision.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def format_axes_table(decision: DeployDecision) -> str:
    """Tableau markdown 5 axes + verdict joint pour rapport Ph5 et nexos doctor."""
    soic_mu = f"{decision.soic_mu:.2f}" if decision.soic_mu is not None else "—"
    osiris_score = f"{decision.osiris_score:.1f}" if decision.osiris_score is not None else "—"
    osiris_grade = decision.osiris_grade or "—"
    lh_perf = f"{decision.lighthouse_perf:.0f}" if decision.lighthouse_perf is not None else "—"
    npm_high_str = "—" if decision.npm_audit_high is None else str(decision.npm_audit_high)
    npm_crit_str = "—" if decision.npm_audit_critical is None else str(decision.npm_audit_critical)
    pa11y_err_str = "—" if decision.pa11y_errors is None else str(decision.pa11y_errors)
    pa11y_warn_str = (
        "—" if decision.pa11y_warnings_count is None else str(decision.pa11y_warnings_count)
    )
    blockers_str = ", ".join(decision.blockers) if decision.blockers else "—"
    lines = [
        "| Axe | Mesure | Seuil | Verdict | Source |",
        "|-----|-------:|------:|---------|--------|",
        f"| SOIC (qualité technique) | μ={soic_mu} | ≥{decision.soic_threshold:.1f} "
        f"| {decision.soic_verdict} | `soic-gates.json` |",
        f"| Osiris (santé opérationnelle) | score={osiris_score} ({osiris_grade}) "
        f"| ≥{decision.osiris_threshold:.1f} | {decision.osiris_verdict} "
        f"| `tooling/osiris.json` |",
        f"| Lighthouse (performance) | perf={lh_perf}/100 | ≥{decision.lighthouse_threshold:.0f} "
        f"| {decision.lighthouse_verdict} | `tooling/lighthouse.json` |",
        f"| npm audit (supply chain) | high={npm_high_str} critical={npm_crit_str} "
        f"| ≤{decision.npm_audit_threshold} HIGH+CRIT | {decision.npm_audit_verdict} "
        f"| `tooling/npm-audit.json` |",
        f"| pa11y (accessibilité WCAG) | errors={pa11y_err_str} warnings={pa11y_warn_str} "
        f"| ≤{decision.pa11y_threshold} errors | {decision.pa11y_verdict} "
        f"| `tooling/a11y.json` |",
        f"| **Joint** | **{decision.joint_verdict}** | — | **blockers: {blockers_str}** | — |",
    ]
    return "\n".join(lines)


# Rétrocompat : alias gardé pour ne pas casser les imports existants pendant
# la transition. À supprimer dans une future itération une fois les consommateurs
# migrés.
format_dual_axis_table = format_axes_table


__all__ = [
    "AXIS_LIGHTHOUSE",
    "AXIS_NPM_AUDIT",
    "AXIS_OSIRIS",
    "AXIS_PA11Y",
    "AXIS_SOIC",
    "DEPLOY_DECISION_FILENAME",
    "DeployDecision",
    "evaluate_deploy_decision",
    "format_axes_table",
    "format_dual_axis_table",
    "persist_deploy_decision",
]
