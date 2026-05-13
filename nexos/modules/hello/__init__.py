"""Module bidon qui valide le mécanisme registre + contrats I/O."""

from __future__ import annotations

from typing import Any


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Retourne un message déterministe pour tester l'exécution modulaire."""
    name = str(payload.get("name") or "NEXOS")
    uppercase = bool(payload.get("uppercase", False))
    message = f"Bonjour {name}"
    if uppercase:
        message = message.upper()

    return {
        "module_id": "hello",
        "message": message,
        "echo": {
            "name": name,
            "uppercase": uppercase,
        },
    }
