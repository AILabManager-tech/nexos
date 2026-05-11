"""Reconciliation Ph4 ↔ Ph5 — détection de la divergence Ph4 ment / Ph5 mesure réelle.

Item 3 du chantier 4 dette pipeline.

Contexte : l'audit du chantier knowledge (verdict E2E 2026-05-08) a révélé
que Ph4 peut s'auto-attribuer μ=10.00 alors que Ph5 mesure μ=6.79 sur le
même site. Sans détection, le SaaS commercialiserait des sites avec
scoring surévalué.

Stratégie : après Ph5, comparer μ Ph4 et μ Ph5. Si écart > seuil (par
défaut 2.0 points), émettre un WARNING visible dans :
- le log opérateur (`say` console)
- `nexos-changelog.json` (event)
- une section dédiée injectée dans `ph5-qa-report.md`

Pas de blocage — filet de sécurité défensif.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReconciliationResult:
    """Résultat de la comparaison μ Ph4 vs μ Ph5."""

    ph4_mu: float
    ph5_mu: float
    delta: float  # toujours ≥ 0 (valeur absolue)
    threshold: float
    diverged: bool
    reason: str  # description courte (humain-lisible) du verdict


def load_phase_mu(soic_gates_path: Path, phase: str) -> float | None:
    """Récupère le μ final d'une phase depuis soic-gates.json.

    Le fichier soic-gates.json est une liste de dicts {phase, mu, threshold,
    decision, ...}. On prend la dernière entrée matchant `phase` (cas où
    plusieurs runs ont eu lieu).

    Retourne None si la phase n'est pas trouvée ou si le fichier est invalide.
    """
    if not soic_gates_path.exists():
        return None
    try:
        gates: list[dict[str, Any]] = json.loads(soic_gates_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(gates, list):
        return None

    matching = [g for g in gates if isinstance(g, dict) and g.get("phase") == phase]
    if not matching:
        return None

    mu = matching[-1].get("mu")
    if not isinstance(mu, (int, float)):
        return None
    return float(mu)


def reconcile_ph4_ph5(
    soic_gates_path: Path,
    *,
    threshold: float = 2.0,
) -> ReconciliationResult | None:
    """Compare μ Ph4 et μ Ph5 dans soic-gates.json.

    Retourne None si Ph4 ou Ph5 sont absents (cas d'un pipeline partiel
    où la reconciliation n'a pas de sens — pas un signal de problème).

    Sinon retourne un `ReconciliationResult` avec `diverged=True` si
    `abs(μ4 - μ5) > threshold`.
    """
    ph4_mu = load_phase_mu(soic_gates_path, "ph4-build")
    ph5_mu = load_phase_mu(soic_gates_path, "ph5-qa")

    if ph4_mu is None or ph5_mu is None:
        return None

    delta = abs(ph4_mu - ph5_mu)
    diverged = delta > threshold

    if diverged:
        if ph4_mu > ph5_mu:
            reason = (
                f"Ph4 surévalue par rapport à Ph5 (Ph4 ment ?) : "
                f"μ4={ph4_mu:.2f} vs μ5={ph5_mu:.2f}, écart={delta:.2f} > seuil={threshold}"
            )
        else:
            reason = (
                f"Ph5 surévalue par rapport à Ph4 (cas atypique — investiguer) : "
                f"μ4={ph4_mu:.2f} vs μ5={ph5_mu:.2f}, écart={delta:.2f} > seuil={threshold}"
            )
    else:
        reason = (
            f"Ph4 et Ph5 cohérents : μ4={ph4_mu:.2f} vs μ5={ph5_mu:.2f}, "
            f"écart={delta:.2f} ≤ seuil={threshold}"
        )

    return ReconciliationResult(
        ph4_mu=ph4_mu,
        ph5_mu=ph5_mu,
        delta=delta,
        threshold=threshold,
        diverged=diverged,
        reason=reason,
    )


def format_reconciliation_report_section(result: ReconciliationResult) -> str:
    """Formate une section markdown injectable dans ph5-qa-report.md."""
    icon = "⚠️ WARNING" if result.diverged else "✓ OK"
    return (
        f"\n## Reconciliation Ph4 ↔ Ph5\n\n"
        f"**Statut** : {icon}\n"
        f"**μ Ph4** : {result.ph4_mu:.2f}\n"
        f"**μ Ph5** : {result.ph5_mu:.2f}\n"
        f"**Écart** : {result.delta:.2f} (seuil divergence = {result.threshold})\n\n"
        f"{result.reason}\n"
    )


def append_reconciliation_to_report(
    report_path: Path,
    result: ReconciliationResult,
) -> bool:
    """Ajoute la section reconciliation au ph5-qa-report.md.

    Idempotent : si une section `## Reconciliation Ph4 ↔ Ph5` existe déjà,
    elle est remplacée. Retourne True si l'écriture a réussi.
    """
    if not report_path.exists():
        return False

    section = format_reconciliation_report_section(result)
    existing = report_path.read_text(encoding="utf-8")

    marker = "## Reconciliation Ph4 ↔ Ph5"
    if marker in existing:
        # Remplacer la section existante (jusqu'au prochain `##` ou EOF)
        start = existing.index(marker)
        rest = existing[start:]
        next_section = rest[len(marker) :].find("\n## ")
        if next_section >= 0:
            end = start + len(marker) + next_section
            new_content = existing[:start] + section.lstrip("\n") + existing[end:]
        else:
            new_content = existing[:start] + section.lstrip("\n")
    else:
        new_content = existing.rstrip() + "\n" + section

    report_path.write_text(new_content, encoding="utf-8")
    return True


def run_reconciliation_step(
    client_dir: Path,
    *,
    say: Callable[[str], None],
    has_changelog: bool = False,
    threshold: float = 2.0,
) -> ReconciliationResult | None:
    """Exécute le step de reconciliation post-pipeline.

    Compare μ Ph4 et μ Ph5, log le verdict, append au rapport Ph5, log un
    event changelog si divergence. Centralise la logique pour garder
    phases.py mince (≤620 lignes).

    Args:
        client_dir: dossier client (contient soic-gates.json et ph5-qa-report.md)
        say: callback d'affichage console (signature `say(msg: str)`)
        has_changelog: si True, émet un event changelog en cas de divergence
        threshold: seuil de divergence (par défaut 2.0)

    Retourne le `ReconciliationResult` ou None si Ph4/Ph5 absents.
    """
    soic_gates_path = client_dir / "soic-gates.json"
    result = reconcile_ph4_ph5(soic_gates_path, threshold=threshold)
    if result is None:
        return None

    if result.diverged:
        say(f"[yellow]⚠ RECONCILIATION: {result.reason}[/]")
    else:
        say(f"[dim]✓ Reconciliation Ph4↔Ph5: {result.reason}[/]")

    append_reconciliation_to_report(client_dir / "ph5-qa-report.md", result)

    if has_changelog and result.diverged:
        from nexos.changelog import EventType, log_event

        log_event(
            client_dir,
            EventType.SOIC_GATE_FAIL,
            phase="reconciliation",
            agent="orchestrator",
            details={
                "ph4_mu": result.ph4_mu,
                "ph5_mu": result.ph5_mu,
                "delta": result.delta,
                "threshold": result.threshold,
                "reason": result.reason,
            },
        )

    return result
