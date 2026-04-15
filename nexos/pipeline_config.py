"""NEXOS v4.0 — Dynamic pipeline configuration.

PipelineConfig resolves the phase sequence and template directory
based on the client brief (site type, stack, mode).

Replaces the static PHASES_MAP dict in orchestrator.py while keeping
it as a fallback for backward compatibility.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ── Color validation ─────────────────────────────────────────────────────────

_HEX_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}){1,2}$")

VALID_COLOR_ROLES = frozenset(
    {
        "primary",
        "secondary",
        "accent",
        "background",
        "surface",
        "text",
        "error",
        "success",
        "warning",
        "info",
        "border",
    }
)


def parse_color_args(raw: list[str]) -> dict[str, str]:
    """Parse CLI color arguments like ['primary=#1A2B3C', 'accent=#FFD700'].

    Returns a dict {role: hex_value}. Raises ValueError on invalid input.
    """
    colors: dict[str, str] = {}
    for item in raw:
        if "=" not in item:
            raise ValueError(f"Format invalide '{item}' — attendu: role=#HEXCODE")
        role, hex_val = item.split("=", 1)
        role = role.strip().lower()
        hex_val = hex_val.strip()
        if not hex_val.startswith("#"):
            hex_val = f"#{hex_val}"
        if not _HEX_RE.match(hex_val):
            raise ValueError(f"Code hex invalide '{hex_val}' pour le rôle '{role}'")
        colors[role] = hex_val.upper()
    return colors


# ── Default phase sequences (kept as fallbacks) ─────────────────────────────

PHASES_CREATE = [
    "ph0-discovery",
    "ph1-strategy",
    "ph2-design",
    "ph3-content",
    "ph4-build",
    "ph5-qa",
]

_MODE_PHASES: dict[str, list[str]] = {
    "create": PHASES_CREATE,
    "audit": ["ph5-qa"],
    "modify": ["site-update"],
    "content": ["ph3-content"],
    "analyze": ["ph0-discovery"],
}

# ── Stack options (for brief_wizard integration) ─────────────────────────────

STACK_OPTIONS: list[dict[str, Any]] = [
    {"value": "nextjs", "label": "Next.js 15+ (App Router)", "default": True},
    {"value": "nuxt", "label": "Nuxt 3 (Vue)", "default": False},
    {"value": "astro", "label": "Astro", "default": False},
    {"value": "fastapi", "label": "FastAPI (API only)", "default": False},
    {"value": "generic", "label": "Autre / Générique", "default": False},
]


@dataclass
class PipelineConfig:
    """Resolved pipeline configuration for a specific client/run."""

    mode: str
    phases: list[str]
    stack: str = "nextjs"
    site_type: str = "vitrine"
    template_dir: Path | None = None
    target_sections: list[str] | None = None
    color_overrides: dict[str, str] | None = None

    @classmethod
    def from_brief(
        cls,
        brief: dict[str, Any] | None,
        mode: str,
        nexos_root: Path | None = None,
    ) -> PipelineConfig:
        """Build a PipelineConfig from a client brief and mode.

        Args:
            brief: Client brief dict (from brief-client.json). Can be None.
            mode: Pipeline mode (create, audit, modify, content, analyze).
            nexos_root: Root of the NEXOS project (for resolving template dirs).
        """
        # Resolve stack and site_type from brief (canonical: site.stack, site.type)
        stack = "nextjs"
        site_type = "vitrine"
        if brief:
            site = brief.get("site", {})
            stack = site.get("stack", "nextjs")
            site_type = site.get("type", "vitrine")

        # Resolve phases based on mode and site_type
        phases = list(_MODE_PHASES.get(mode, PHASES_CREATE))

        # Application-type sites may skip some early phases in audit mode
        # but in create mode, all phases are needed regardless of site_type

        # Resolve template directory
        template_dir = None
        if nexos_root is not None:
            template_dir = cls._resolve_template_dir(nexos_root, stack)

        return cls(
            mode=mode,
            phases=phases,
            stack=stack,
            site_type=site_type,
            template_dir=template_dir,
        )

    @staticmethod
    def _resolve_template_dir(nexos_root: Path, stack: str) -> Path:
        """Find the most specific template directory for the given stack.

        Resolution order:
        1. templates/{stack}/ (e.g., templates/nextjs/)
        2. templates/generic/
        3. templates/ (legacy flat structure)
        """
        stack_dir = nexos_root / "templates" / stack
        if stack_dir.is_dir():
            return stack_dir

        generic_dir = nexos_root / "templates" / "generic"
        if generic_dir.is_dir():
            return generic_dir

        # Fallback to flat templates/ (pre-R3 layout)
        return nexos_root / "templates"

    @staticmethod
    def get_template_dir(nexos_root: Path, stack: str) -> Path:
        """Public API for template directory resolution."""
        return PipelineConfig._resolve_template_dir(nexos_root, stack)
