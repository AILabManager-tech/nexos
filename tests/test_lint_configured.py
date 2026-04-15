"""Tests: lint correctement configuré (phase G chantier2)."""

from __future__ import annotations

import pathlib
import subprocess
import sys

REPO = pathlib.Path(__file__).resolve().parents[1]


def test_pyproject_has_ruff_config():
    if sys.version_info >= (3, 11):
        import tomllib
    else:
        import tomli as tomllib  # type: ignore[import-not-found]
    data = tomllib.loads((REPO / "pyproject.toml").read_text())
    assert "ruff" in data.get("tool", {}), "Missing [tool.ruff] in pyproject.toml"
    assert "lint" in data["tool"]["ruff"], "Missing [tool.ruff.lint]"


def test_precommit_config_exists():
    pc = REPO / ".pre-commit-config.yaml"
    assert pc.exists(), ".pre-commit-config.yaml missing"
    content = pc.read_text()
    assert "ruff" in content
    assert "trailing-whitespace" in content


def test_ruff_available_and_no_errors():
    result = subprocess.run(["ruff", "--version"], capture_output=True)
    if result.returncode != 0:
        import pytest

        pytest.skip("ruff not installed in env")

    result = subprocess.run(
        ["ruff", "check", "."],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"ruff check a trouvé des erreurs:\n{result.stdout}"

    result = subprocess.run(
        ["ruff", "format", "--check", "."],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"ruff format --check a trouvé des fichiers non formatés:\n{result.stdout}"
    )
