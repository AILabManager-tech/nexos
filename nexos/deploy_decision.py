"""NEXOS — Verdict deploy à 2 axes : SOIC (qualité technique) + Osiris (santé opérationnelle).

Architecture séparée de la mesure et de la décision :
- SOIC garde sa souveraineté sur D1-D9 (technique interne, ce que le pipeline contrôle).
- Osiris reste un signal externe distinct (santé opérationnelle réelle).
- Le verdict deploy est composite : `μ_SOIC ≥ 8.5` ET `osiris_score ≥ threshold`.

Si bloqué, le `blocker` est traçable aux 2 mesures sources (pas de score composite opaque).

Pattern réutilisable : on peut étendre `evaluate_deploy_decision` à d'autres gates
indépendants (Lighthouse perf, npm audit HIGH count, pa11y a11y score) sans toucher
à SOIC. Le verdict final reste joint, lisible, traçable.

P9 D2 — chantier dette pipeline 2026-05-18.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

JointVerdict = Literal["ACCEPT", "FAIL"]
AxisVerdict = Literal["PASS", "FAIL", "UNKNOWN"]
Blocker = Literal["soic", "osiris", "both"] | None

SOIC_GATES_FILENAME = "soic-gates.json"
OSIRIS_TOOLING_FILENAME = "osiris.json"
DEPLOY_DECISION_FILENAME = "deploy-decision.json"


@dataclass(frozen=True)
class DeployDecision:
    """Verdict deploy composite, traçable aux 2 axes sources."""

    # SOIC axis
    soic_mu: float | None
    soic_verdict: AxisVerdict
    soic_threshold: float

    # Osiris axis
    osiris_score: float | None
    osiris_grade: str | None
    osiris_verdict: AxisVerdict
    osiris_threshold: float

    # Joint
    joint_verdict: JointVerdict
    blocker: Blocker
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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


def _load_osiris_report(client_dir: Path) -> dict[str, Any] | None:
    """Lit tooling/osiris.json (defensive)."""
    path = client_dir / "tooling" / OSIRIS_TOOLING_FILENAME
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _extract_osiris_axis(
    report: dict[str, Any] | None,
    threshold: float,
) -> tuple[float | None, str | None, AxisVerdict, list[str]]:
    """Décode le rapport Osiris en (score, grade, verdict, warnings).

    Politique UNKNOWN : Osiris missing / scan error → verdict UNKNOWN, ne bloque
    pas le deploy (don't punish missing signal). Une warning explicite est émise
    pour rendre la dette visible.

    Politique FAIL : score numérique < threshold → verdict FAIL, blocker traçable.
    """
    if report is None:
        return None, None, "UNKNOWN", ["Osiris report absent (tooling/osiris.json missing)"]

    # Le JSON Osiris brut (sortie scanner.py) utilise `score`. Le RunStore SOIC
    # (osiris_history.db) utilise `osiris_score`. On tolère les deux noms.
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

    if score_f >= threshold:
        return score_f, grade_str, "PASS", []
    return score_f, grade_str, "FAIL", []


def _compute_joint(
    soic_verdict: AxisVerdict,
    osiris_verdict: AxisVerdict,
) -> tuple[JointVerdict, Blocker]:
    """Logique deploy joint :
    - SOIC FAIL + Osiris FAIL → FAIL, blocker="both"
    - SOIC FAIL + (Osiris PASS|UNKNOWN) → FAIL, blocker="soic"
    - SOIC PASS + Osiris FAIL → FAIL, blocker="osiris"
    - SOIC PASS + (Osiris PASS|UNKNOWN) → ACCEPT
    """
    soic_ok = soic_verdict == "PASS"
    osiris_ok = osiris_verdict in ("PASS", "UNKNOWN")  # UNKNOWN ne bloque pas
    osiris_fail = osiris_verdict == "FAIL"

    if soic_ok and osiris_ok:
        return "ACCEPT", None
    if not soic_ok and osiris_fail:
        return "FAIL", "both"
    if not soic_ok:
        return "FAIL", "soic"
    return "FAIL", "osiris"


def evaluate_deploy_decision(
    client_dir: Path,
    osiris_threshold: float = 6.0,
    soic_threshold: float = 8.5,
) -> DeployDecision:
    """Calcule le verdict deploy à 2 axes pour un client.

    Args:
        client_dir: dossier client (contient soic-gates.json et tooling/osiris.json).
        osiris_threshold: seuil minimum osiris_score pour PASS (défaut 6.0).
        soic_threshold: seuil μ_SOIC pour PASS (défaut 8.5, aligné Ph5 deploy).

    Returns:
        DeployDecision immuable, prête à sérialiser et injecter en rapport.
    """
    gate = _load_latest_soic_gate(client_dir)
    soic_mu: float | None = None
    soic_verdict: AxisVerdict = "UNKNOWN"
    warnings: list[str] = []

    if gate is not None:
        raw_mu = gate.get("mu")
        if isinstance(raw_mu, (int, float)):
            soic_mu = float(raw_mu)
        decision = gate.get("decision", "")
        # SOIC GateEngine émet "ACCEPT" en décision finale ; tout autre = FAIL
        if decision == "ACCEPT" and soic_mu is not None and soic_mu >= soic_threshold:
            soic_verdict = "PASS"
        elif soic_mu is None:
            soic_verdict = "UNKNOWN"
            warnings.append("SOIC mu missing in soic-gates.json")
        else:
            soic_verdict = "FAIL"
    else:
        warnings.append("SOIC gate ph5-qa absent (soic-gates.json missing or empty)")

    report = _load_osiris_report(client_dir)
    osiris_score, osiris_grade, osiris_verdict, osiris_warnings = _extract_osiris_axis(
        report, osiris_threshold
    )
    warnings.extend(osiris_warnings)

    # SOIC UNKNOWN traité comme FAIL pour la décision (pas de gate = pas de deploy)
    soic_for_joint: AxisVerdict = soic_verdict if soic_verdict != "UNKNOWN" else "FAIL"
    joint, blocker = _compute_joint(soic_for_joint, osiris_verdict)

    return DeployDecision(
        soic_mu=soic_mu,
        soic_verdict=soic_verdict,
        soic_threshold=soic_threshold,
        osiris_score=osiris_score,
        osiris_grade=osiris_grade,
        osiris_verdict=osiris_verdict,
        osiris_threshold=osiris_threshold,
        joint_verdict=joint,
        blocker=blocker,
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


def format_dual_axis_table(decision: DeployDecision) -> str:
    """Tableau markdown 2 axes pour rapport Ph5 et nexos doctor."""
    soic_mu = f"{decision.soic_mu:.2f}" if decision.soic_mu is not None else "—"
    osiris_score = f"{decision.osiris_score:.1f}" if decision.osiris_score is not None else "—"
    osiris_grade = decision.osiris_grade or "—"
    blocker = decision.blocker or "—"
    lines = [
        "| Axe | Mesure | Seuil | Verdict | Source |",
        "|-----|-------:|------:|---------|--------|",
        f"| SOIC (qualité technique) | μ={soic_mu} | ≥{decision.soic_threshold:.1f} "
        f"| {decision.soic_verdict} | `soic-gates.json` |",
        f"| Osiris (santé opérationnelle) | score={osiris_score} ({osiris_grade}) "
        f"| ≥{decision.osiris_threshold:.1f} | {decision.osiris_verdict} "
        f"| `tooling/osiris.json` |",
        f"| **Joint** | **{decision.joint_verdict}** | — | **blocker: {blocker}** | — |",
    ]
    return "\n".join(lines)


__all__ = [
    "DEPLOY_DECISION_FILENAME",
    "DeployDecision",
    "evaluate_deploy_decision",
    "format_dual_axis_table",
    "persist_deploy_decision",
]
