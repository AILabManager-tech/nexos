"""Helpers autour du brief client.

- `slugify()`: conversion nom → slug kebab-case (Unicode-safe).
- `generate_brief()`: assemble un brief à partir des réponses CLI.
- `generate_brief_from_wizard()`: écrit un brief validé par `nexos.brief_wizard`.
- `load_runtime_brief()`: charge + normalise + valide un brief avant exécution.
"""

from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from ._shared import _HAS_CHANGELOG, CLIENTS_DIR, PHASES_MAP, say


def slugify(name: str) -> str:
    """Convertit un nom en slug kebab-case (supporte Unicode composé)."""
    slug = unicodedata.normalize("NFC", name).lower().strip()
    slug = unicodedata.normalize("NFD", slug)
    slug = "".join(c for c in slug if unicodedata.category(c) != "Mn")
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug


def generate_brief(mode: str, answers: dict, free_text: str = "") -> Path:
    """Génère le brief-client.json et retourne le chemin du dossier client."""
    timestamp = datetime.now().isoformat()
    client_name = answers.get("client_name", f"projet-{datetime.now().strftime('%Y-%m-%d')}")
    slug = slugify(client_name)

    client_dir = CLIENTS_DIR / slug
    client_dir.mkdir(parents=True, exist_ok=True)
    (client_dir / "tooling").mkdir(exist_ok=True)
    (client_dir / "site").mkdir(exist_ok=True)

    brief = {
        "_meta": {
            "generator": "nexos-v3.0",
            "created_at": timestamp,
            "mode": mode,
        },
        "client": {"name": client_name, "slug": slug},
        "mission": {
            "mode": mode,
            "phases": PHASES_MAP[mode],
        },
        "inputs": answers,
        "context_libre": free_text,
    }

    brief_path = client_dir / "brief-client.json"
    brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    say(f"[green]✓[/] Brief généré : {brief_path}")

    if _HAS_CHANGELOG:
        from nexos.changelog import EventType, log_event

        log_event(
            client_dir,
            EventType.BRIEF_CREATED,
            agent="orchestrator",
            details={"slug": slug, "mode": mode},
        )

    return client_dir


def generate_brief_from_wizard(mode: str, brief_data: dict) -> Path:
    """Crée le dossier client et écrit le brief généré par le wizard interactif."""
    from nexos.brief_contract import normalize_brief, validate_brief

    brief_data = normalize_brief(brief_data, mode=mode)
    errors = validate_brief(brief_data)
    if errors:
        raise ValueError(f"Brief wizard invalide: {', '.join(errors)}")
    slug = brief_data["client"]["slug"]
    client_dir = CLIENTS_DIR / slug
    client_dir.mkdir(parents=True, exist_ok=True)
    (client_dir / "tooling").mkdir(exist_ok=True)
    (client_dir / "site").mkdir(exist_ok=True)

    brief_data["mission"] = {
        "mode": mode,
        "phases": PHASES_MAP[mode],
    }

    brief_path = client_dir / "brief-client.json"
    brief_path.write_text(json.dumps(brief_data, ensure_ascii=False, indent=2), encoding="utf-8")

    say(f"[green]✓[/] Brief wizard généré : {brief_path}")
    return client_dir


def load_runtime_brief(brief_path: Path, mode: str | None = None) -> dict:
    """Charge, normalise et valide un brief avant exécution."""
    from nexos.brief_contract import normalize_brief, validate_brief

    brief_data = json.loads(brief_path.read_text())
    normalized = normalize_brief(brief_data, mode=mode)
    errors = validate_brief(normalized)
    if errors:
        raise ValueError(f"Brief invalide ({brief_path}): {', '.join(errors)}")
    return normalized


__all__ = [
    "generate_brief",
    "generate_brief_from_wizard",
    "load_runtime_brief",
    "slugify",
]
