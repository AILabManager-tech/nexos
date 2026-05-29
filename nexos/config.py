"""NEXOS — Configuration centralisée.

Source de vérité pour tous les chemins et variables d'environnement.
Remplace les chemins absolus hardcodés (ex: paths utilisateur d'une autre
machine) disséminés dans le code par une config portable.

Usage:
    from nexos.config import settings
    >>> settings.repo_root
    >>> settings.workspace_root

Variables lues depuis l'environnement (ou .env si python-dotenv est installé) :
    NEXOS_REPO_ROOT        : racine du repo (défaut: auto-détectée)
    NEXOS_WORKSPACE_ROOT   : racine du workspace (défaut: parent du repo)
    NEXOS_CLIENTS_DIR      : dossier des clients (défaut: repo/clients)
    NEXOS_SOIC_PATH        : dossier SOIC (défaut: repo/soic, qui est un symlink)
    NEXOS_TEMPLATES_DIR    : dossier templates (défaut: repo/templates)
    NEXOS_TOOLS_DIR        : dossier tools (défaut: repo/tools)
    NEXOS_OUTPUT_DIR       : dossier output (défaut: repo/output)
    NEXOS_LOG_LEVEL        : INFO | DEBUG | WARNING | ERROR (défaut: INFO)

Audit / analyse :
    AUDIT_TOOLKIT_PATH     : chemin vers audit_toolkit/ (défaut: WORKSPACE/audit_toolkit)
    OSIRIS_PATH            : chemin vers le repo osiris-scanner (défaut: WORKSPACE/../osiris/osiris-scanner)
    NEXOS_OSIRIS_THRESHOLD : seuil minimum osiris_score pour ACCEPT deploy (défaut: 6.0)

API externes (vides par défaut, optionnelles) :
    MOZ_API_KEY
    WHOIS_API_KEY
    GSC_SERVICE_ACCOUNT_JSON
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _auto_repo_root() -> Path:
    """Détecte la racine du repo en remontant depuis ce fichier."""
    here = Path(__file__).resolve()
    # nexos/config.py → parent (nexos) → parent (repo)
    return here.parent.parent


def _env_path(key: str, default: Path) -> Path:
    val = os.environ.get(key)
    return Path(val).expanduser().resolve() if val else default


def _env_str(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def _env_float(key: str, default: float) -> float:
    val = os.environ.get(key)
    if val is None:
        return default
    try:
        return float(val)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    """Configuration NEXOS immuable, lue au démarrage."""

    # Paths core
    repo_root: Path
    workspace_root: Path
    clients_dir: Path
    soic_path: Path
    templates_dir: Path
    tools_dir: Path
    output_dir: Path

    # Paths périphériques
    audit_toolkit_path: Path | None = None
    osiris_path: Path | None = None

    # Gates seuils (déploy 2-axes : SOIC + Osiris)
    osiris_threshold: float = 6.0

    # Logging
    log_level: str = "INFO"

    # API externes (laissées vides — le code appelant décide si obligatoire)
    moz_api_key: str = ""
    whois_api_key: str = ""
    gsc_service_account_json: str = ""


def _build_settings() -> Settings:
    repo_root = _env_path("NEXOS_REPO_ROOT", _auto_repo_root())
    workspace_root = _env_path("NEXOS_WORKSPACE_ROOT", repo_root.parent)

    return Settings(
        repo_root=repo_root,
        workspace_root=workspace_root,
        clients_dir=_env_path("NEXOS_CLIENTS_DIR", repo_root / "clients"),
        soic_path=_env_path("NEXOS_SOIC_PATH", repo_root / "soic"),
        templates_dir=_env_path("NEXOS_TEMPLATES_DIR", repo_root / "templates"),
        tools_dir=_env_path("NEXOS_TOOLS_DIR", repo_root / "tools"),
        output_dir=_env_path("NEXOS_OUTPUT_DIR", repo_root / "output"),
        audit_toolkit_path=_env_path("AUDIT_TOOLKIT_PATH", workspace_root / "audit_toolkit"),
        osiris_path=_env_path("OSIRIS_PATH", workspace_root.parent / "osiris" / "osiris-scanner"),
        osiris_threshold=_env_float("NEXOS_OSIRIS_THRESHOLD", 6.0),
        log_level=_env_str("NEXOS_LOG_LEVEL", "INFO"),
        moz_api_key=_env_str("MOZ_API_KEY", ""),
        whois_api_key=_env_str("WHOIS_API_KEY", ""),
        gsc_service_account_json=_env_str("GSC_SERVICE_ACCOUNT_JSON", ""),
    )


# Instance singleton chargée au import.
# Le code appelant fait: from nexos.config import settings
settings = _build_settings()


__all__ = ["Settings", "settings"]
