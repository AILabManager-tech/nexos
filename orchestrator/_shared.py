"""Constantes et helpers partagés par les modules du package orchestrator.

Regroupe ce qui était au sommet de l'ancien `orchestrator.py` :
- Chemins racines (`NEXOS_ROOT`, `CLIENTS_DIR`, ...)
- Sortie console (`console`, `say()`) — `say()` passe par `console`
  pour rester patchable dans les tests.
- Flags d'import optionnels (`_NEXOS_V4`, `_HAS_CHANGELOG`, `_HAS_AUDIT_TOOLKIT`)
- Catalogue des phases (`PHASES_MAP`, `PHASES_CREATE`)
- Résolution SOIC (`_get_default_profile`, `_resolve_profile`)
- Carte des rapports (`OUTPUT_MAP`)
"""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from nexos.logging_config import get_logger

logger = get_logger("orchestrator")
console = Console()


def say(*args, **kwargs):
    """UX output: route via `console` (patchable in tests)."""
    console.print(*args, **kwargs)


# NEXOS_ROOT pointe vers la racine du projet (parent du package).
NEXOS_ROOT = Path(__file__).resolve().parent.parent
CLIENTS_DIR = NEXOS_ROOT / "clients"
AGENTS_DIR = NEXOS_ROOT / "agents"
TOOLS_DIR = NEXOS_ROOT / "tools"
LOGS_DIR = NEXOS_ROOT / "logs"
KNOWLEDGE_DIR = NEXOS_ROOT / "output" / "knowledge"


# ── Feature detection ────────────────────────────────────────────────────────
try:
    from nexos.auto_fixer import auto_fix as _auto_fix  # noqa: F401
    from nexos.brief_contract import (
        normalize_brief as _normalize_brief,  # noqa: F401
        validate_brief as _validate_brief,  # noqa: F401
    )
    from nexos.brief_wizard import interactive_brief as _interactive_brief  # noqa: F401
    from nexos.build_validator import validate_build as _validate_build  # noqa: F401
    from nexos.tooling_manager import ensure_tooling as _ensure_tooling  # noqa: F401

    _NEXOS_V4 = True
except ImportError:
    _NEXOS_V4 = False

try:
    from nexos.changelog import (
        EventType as _EventType,  # noqa: F401
        log_event as _log_event,  # noqa: F401
    )

    _HAS_CHANGELOG = True
except ImportError:
    _HAS_CHANGELOG = False

try:
    from audit_toolkit.config import AuditConfig as _ToolkitConfig  # noqa: F401
    from audit_toolkit.scanner import run_full_audit as _run_source_audit  # noqa: F401

    _HAS_AUDIT_TOOLKIT = True
except ImportError:
    _HAS_AUDIT_TOOLKIT = False


# ── Phase sequence ───────────────────────────────────────────────────────────
PHASES_CREATE = [
    "ph0-discovery",
    "ph1-strategy",
    "ph2-design",
    "ph3-content",
    "ph4-build",
    "ph5-qa",
]

PHASES_MAP = {
    "create": PHASES_CREATE,
    "audit": ["ph5-qa"],
    "modify": ["site-update"],
    "content": ["ph3-content"],
    "analyze": ["ph0-discovery"],
}

OUTPUT_MAP = {
    "ph0-discovery": "ph0-discovery-report.md",
    "ph1-strategy": "ph1-strategy-report.md",
    "ph2-design": "ph2-design-report.md",
    "ph3-content": "ph3-content-report.md",
    "ph4-build": "ph4-build-log.md",
    "ph5-qa": "ph5-qa-report.md",
    "site-update": "site-update-report.md",
}


# ── SOIC profile resolution ──────────────────────────────────────────────────
_STACK_PROFILE_MAP = {
    "nextjs": "web-nextjs",
    "nuxt": "web-generic",
    "astro": "web-generic",
    "fastapi": "api-fastapi",
    "generic": "web-generic",
}


def _get_default_profile():
    """Lazy-load the default SOICProfile to avoid import-time side effects."""
    from soic.profile import get_profile

    return get_profile("web-nextjs")


def _resolve_profile(stack=None, profile_name=None):
    """Resolve a SOICProfile from --stack or --profile CLI args."""
    from soic.profile import get_profile

    if profile_name:
        return get_profile(profile_name)
    if stack:
        return get_profile(_STACK_PROFILE_MAP.get(stack, "web-generic"))
    return None


# ── Knowledge agent constants ────────────────────────────────────────────────
VALID_TYPES = ("dev-perso", "technique", "fiction", "academique", "business", "philosophie")
VALID_OBJECTIFS = ("appliquer", "partager", "memoriser", "decider")
VALID_NIVEAUX = ("express", "complet", "approfondi")


__all__ = [
    "AGENTS_DIR",
    "CLIENTS_DIR",
    "KNOWLEDGE_DIR",
    "LOGS_DIR",
    "NEXOS_ROOT",
    "OUTPUT_MAP",
    "PHASES_CREATE",
    "PHASES_MAP",
    "TOOLS_DIR",
    "VALID_NIVEAUX",
    "VALID_OBJECTIFS",
    "VALID_TYPES",
    "_HAS_AUDIT_TOOLKIT",
    "_HAS_CHANGELOG",
    "_NEXOS_V4",
    "_get_default_profile",
    "_resolve_profile",
    "console",
    "logger",
    "say",
]
