"""Vérifie que le paquet soic est importable.

Historique :
- v4.2 : protégé contre régression du symlink soic → ../soic_v3 (phase A chantier2).
- v4.4 (2026-05-27) : symlink retiré ; soic est maintenant un vrai package pip
  (repo AILabManager-tech/soic, layout PEP, installé via pip install -e ../soic_v3
  par install_nexos.sh). Ce test vérifie l'install pip et l'absence du symlink legacy.
"""

from __future__ import annotations

import importlib
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
LEGACY_SYMLINK = REPO_ROOT / "soic"


def test_legacy_symlink_removed():
    """Le symlink soic → ../soic_v3 a été retiré en v4.4. soic vient de pip."""
    assert not LEGACY_SYMLINK.exists() or not LEGACY_SYMLINK.is_symlink(), (
        f"Legacy symlink encore présent à {LEGACY_SYMLINK} — utiliser pip install -e ../soic_v3"
    )


def test_soic_installed_as_package():
    """soic doit être un vrai package importable (pip install -e), pas un namespace."""
    import soic

    assert soic.__file__ is not None, (
        "soic.__file__ is None → namespace package détecté (symlink ou install cassé). "
        "Vérifier 'pip install -e ../soic_v3' dans le venv."
    )
    soic_path = pathlib.Path(soic.__file__)
    assert soic_path.name == "__init__.py", f"soic.__file__ inattendu: {soic_path}"
    assert soic_path.parent.name == "soic", (
        f"soic doit être un package, pas un module : {soic_path}"
    )


@pytest.mark.parametrize(
    "module_name",
    [
        "soic",
        "soic.converger",
        "soic.domain_grids",
        "soic.feedback_router",
        "soic.gate",
        "soic.gate_engine",
        "soic.iterator",
        "soic.models",
        "soic.persistence",
        "soic.report",
    ],
)
def test_import_ok(module_name: str):
    mod = importlib.import_module(module_name)
    assert mod is not None
