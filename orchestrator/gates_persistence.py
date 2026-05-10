"""Persistance idempotente de `soic-gates.json`.

Sans le merge implémenté ici, un mode partiel (`audit`, `modify`, `content`)
écraserait les entrées des phases qu'il n'a pas réexécutées (cf.
BUG_NEXOS_SOIC_GATES_OVERWRITE, chantier mode B A-005). Le merge garantit
que chaque appel ne touche que les phases qu'il a effectivement (re)jouées.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PHASE_ORDER: tuple[str, ...] = (
    "ph0-discovery",
    "ph1-strategy",
    "ph2-design",
    "ph3-content",
    "ph4-build",
    "ph5-qa",
)


def _load_existing(gates_path: Path) -> list[dict[str, Any]]:
    if not gates_path.exists():
        return []
    try:
        loaded = json.loads(gates_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return loaded if isinstance(loaded, list) else []


def merge_gate_history(
    existing: list[dict[str, Any]],
    new_runs: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Merge `new_runs` sur `existing` en utilisant la clé `phase`.

    Les nouvelles entrées écrasent les anciennes pour les phases ré-jouées.
    L'ordre canonique ph0..ph5 est préservé, et toute phase inconnue est
    appended à la fin (forward-compat).
    """
    merged: dict[str, dict[str, Any]] = {
        entry["phase"]: entry for entry in existing if isinstance(entry, dict) and "phase" in entry
    }
    for entry in new_runs:
        if isinstance(entry, dict) and "phase" in entry:
            merged[entry["phase"]] = entry

    ordered = [merged[p] for p in PHASE_ORDER if p in merged]
    ordered += [v for k, v in merged.items() if k not in PHASE_ORDER]
    return ordered


def save_gate_history(gates_path: Path, new_runs: list[dict[str, Any]]) -> None:
    """Écrit `soic-gates.json` en mergeant avec le contenu existant.

    Idempotent : appeler avec `new_runs=[]` ne perd aucune donnée historique.
    """
    existing = _load_existing(gates_path)
    ordered = merge_gate_history(existing, new_runs)
    gates_path.write_text(json.dumps(ordered, indent=2, ensure_ascii=False), encoding="utf-8")
