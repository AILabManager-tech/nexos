"""Synchronisation barrière entre l'agent ph4-build et le checker SOIC.

A-002 fix : le checker SOIC ph4 tournait avant que l'agent ph4-build n'ait
fini d'écrire tous ses fichiers (race condition write/check observée sur
Nobert 2026-04-28 : décalage 2-3 min entre check SOIC iter 1 et écriture
finale des composants secondaires comme `ContactForm.tsx`).

Stratégie : attendre la **quiescence filesystem** — aucun fichier modifié
dans `site_dir/` pendant `idle_seconds` consécutives. Plus robuste qu'un
sentinel file car ne dépend pas de la discipline de l'agent LLM.
"""

from __future__ import annotations

import time
from pathlib import Path


def _get_latest_mtime(site_dir: Path) -> float:
    """Retourne le mtime le plus récent parmi tous les fichiers de site_dir.

    Exclut `node_modules/` et `.next/` (volumineux, modifiés pendant le build
    mais pas par l'agent). Retourne 0.0 si le dossier n'existe pas.
    """
    if not site_dir.exists():
        return 0.0

    excluded_parts = {"node_modules", ".next", ".git", "__pycache__"}
    latest = 0.0
    for path in site_dir.rglob("*"):
        if any(part in excluded_parts for part in path.parts):
            continue
        try:
            mtime = path.stat().st_mtime
            if mtime > latest:
                latest = mtime
        except OSError:
            # fichier supprimé entre rglob et stat — ignorer
            continue
    return latest


def wait_for_ph4_sync(
    site_dir: Path,
    *,
    idle_seconds: float = 3.0,
    max_wait: float = 120.0,
    poll_interval: float = 1.0,
) -> bool:
    """Attend que le filesystem soit stable avant d'évaluer les gates SOIC.

    Retourne True si la quiescence est atteinte (aucune modif depuis
    `idle_seconds` sec), False si le timeout `max_wait` est atteint.

    Args:
        site_dir: dossier scaffold ph4 à surveiller
        idle_seconds: durée de stabilité requise pour considérer fini
        max_wait: durée max d'attente totale avant d'abandonner
        poll_interval: période de scan mtime

    Behavior:
        - Si site_dir n'existe pas → retourne False immédiatement
        - Si site_dir est vide → retourne True après idle_seconds
        - Tant que le mtime le plus récent change, repart le compteur
        - Aucune dépendance sur l'agent LLM (pas de sentinel file requis)
    """
    if not site_dir.exists():
        return False

    deadline = time.monotonic() + max_wait
    last_change_ts = _get_latest_mtime(site_dir)

    while time.monotonic() < deadline:
        time.sleep(poll_interval)
        current_mtime = _get_latest_mtime(site_dir)
        if current_mtime > last_change_ts:
            last_change_ts = current_mtime
            continue

        idle_duration = time.time() - last_change_ts
        if idle_duration >= idle_seconds:
            return True

    return False
