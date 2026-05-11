"""Formatage des messages de SOIC gates pour l'affichage opérateur.

Extrait de phases.py pour respecter la cible de taille de fichier (≤600 L) et
faciliter les tests régression (fonction pure, sans dépendance sur `say`).

A-003 fix : distinguer les 3 cas (ACCEPT / ABORT_* / REJECT) pour éviter
le message trompeur `μ < seuil` quand l'ABORT vient d'une autre cause
(rate limit, callback subprocess failed, plateau de convergence) avec
μ effectif ≥ seuil.
"""

from __future__ import annotations


def format_gate_result(
    *,
    converged: bool,
    mu: float,
    threshold: float,
    decision: str,
    iterations: int,
) -> str:
    """Formate le message de fin de SOIC gate.

    - ACCEPT (converged=True)  → `✓ SOIC GATE: μ=X ≥ seuil — ACCEPT`
    - ABORT_*  (decision startswith 'ABORT')
                              → `✗ SOIC ABORT_*: μ=X (seuil=Y) — boucle interrompue`
                                car μ peut être ≥ ou < seuil (échec callback, plateau).
    - REJECT (decision='REJECT')
                              → `✗ SOIC GATE: μ=X < seuil — REJECT`
    """
    if converged:
        return f"[green]✓ SOIC GATE: μ={mu:.2f} ≥ {threshold} — ACCEPT ({iterations} iter)[/]"
    if decision.startswith("ABORT"):
        return (
            f"[red]✗ SOIC {decision}: μ={mu:.2f} "
            f"(seuil={threshold}, {iterations} iter) — boucle interrompue[/]"
        )
    return f"[red]✗ SOIC GATE: μ={mu:.2f} < {threshold} — {decision} ({iterations} iter)[/]"
