"""Tests anti-régression: mypy passe clean sur les modules typés (chantier2-H).

Vérifie que :
1. La config [tool.mypy] est présente dans pyproject.toml.
2. Le marker PEP 561 ``nexos/py.typed`` existe.
3. ``mypy nexos/ nexos_cli.py`` ne rapporte aucune erreur.
4. La couverture type hints sur ``nexos/`` reste ≥ 60 %.
"""

from __future__ import annotations

import ast
import pathlib
import shutil
import subprocess

import pytest

REPO = pathlib.Path(__file__).resolve().parents[1]


def test_pyproject_has_mypy_config() -> None:
    import tomllib

    data = tomllib.loads((REPO / "pyproject.toml").read_text())
    assert "mypy" in data.get("tool", {}), "[tool.mypy] manquant dans pyproject.toml"


def test_py_typed_marker_exists() -> None:
    assert (REPO / "nexos" / "py.typed").exists(), "nexos/py.typed (PEP 561) manquant"


def _resolve_mypy() -> str | None:
    """Return path to mypy: prefer .venv/bin/mypy, fall back to PATH."""
    venv_mypy = REPO / ".venv" / "bin" / "mypy"
    if venv_mypy.exists():
        return str(venv_mypy)
    return shutil.which("mypy")


def test_mypy_passes_on_nexos_package() -> None:
    mypy = _resolve_mypy()
    if mypy is None:
        pytest.skip("mypy non disponible dans cet environnement de test")

    result = subprocess.run(
        [mypy, "nexos/", "nexos_cli.py"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"mypy a échoué (exit {result.returncode}):\n"
            f"--- stdout ---\n{result.stdout}\n"
            f"--- stderr ---\n{result.stderr}"
        )


def test_type_hint_coverage_60pct() -> None:
    """Couverture type hints (fonctions annotées) sur ``nexos/`` ≥ 60 %."""
    pkg = REPO / "nexos"
    total = 0
    typed = 0
    for py in pkg.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total += 1
                has_ret = node.returns is not None
                args = node.args.args + node.args.kwonlyargs
                all_annot = all(
                    a.annotation is not None for a in args if a.arg not in ("self", "cls")
                )
                if has_ret and all_annot:
                    typed += 1

    pct = (typed / total * 100) if total else 0.0
    assert pct >= 60, (
        f"Couverture type hints {pct:.1f}% < 60% (cible chantier2-H). "
        f"Détail: {typed}/{total} fonctions annotées."
    )
