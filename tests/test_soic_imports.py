"""Vérifie que le paquet soic est importable après fix du symlink (phase A chantier2).

Ce test protège contre une régression du symlink qui a bloqué tout le pipeline
en v4.0 jusqu'à la phase A du chantier mise_a_niveau (v4.2.0).
"""

from __future__ import annotations

import importlib
import pathlib

import pytest

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SOIC_SYMLINK = REPO_ROOT / "soic"


def test_symlink_exists_and_resolved():
    assert SOIC_SYMLINK.exists(), f"soic symlink missing at {SOIC_SYMLINK}"
    resolved = SOIC_SYMLINK.resolve()
    assert resolved.is_dir(), f"soic target is not a directory: {resolved}"
    assert (resolved / "__init__.py").exists() or any(resolved.glob("*.py")), (
        f"soic target {resolved} has no Python modules"
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
