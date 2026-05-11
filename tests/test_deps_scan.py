"""Tests régression pour tools/deps-scan.sh.

Couvre BUG_NEXOS_DEPS_SCAN_DUPLICATE (A-010) : `npm audit --json` peut
retourner exit!=0 avec stdout JSON valide (cas où des vulns sont détectées).
L'ancien `npm audit --json || echo '{...}'` ajoutait alors un 2e objet JSON
à la suite, produisant un fichier invalide qui faisait échouer pre-commit
hook `check-json`.

Le fix capture stdout, valide en Python, et n'émet le fallback QUE si stdout
est vide ou invalide.
"""

from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
DEPS_SCAN = REPO_ROOT / "tools" / "deps-scan.sh"


def _run_deps_scan(project_dir: Path) -> tuple[str, int]:
    result = subprocess.run(
        ["bash", str(DEPS_SCAN), str(project_dir)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout, result.returncode


def test_deps_scan_missing_package_json(tmp_path: Path) -> None:
    """Sans package.json, le script doit émettre un JSON d'erreur valide."""
    stdout, code = _run_deps_scan(tmp_path)
    assert code == 0
    data = json.loads(stdout)  # ne doit PAS lever
    assert "error" in data
    assert "no package.json" in data["error"]


def test_deps_scan_with_vulnerabilities_produces_single_json(tmp_path: Path) -> None:
    """Cas A-010 : npm audit retourne exit!=0 avec stdout JSON valide.
    Le script doit émettre exactement UN objet JSON, pas deux concaténés."""
    # Setup : un package.json + package-lock.json minimal qui déclenche
    # potentiellement des vulns (next 14.0.0 a des vulns connues).
    (tmp_path / "package.json").write_text(
        json.dumps({"name": "test", "version": "1.0.0", "dependencies": {"next": "14.0.0"}}),
        encoding="utf-8",
    )
    # Installer pour avoir un lock file (skip si npm absent ou offline)
    try:
        subprocess.run(
            ["npm", "install", "--package-lock-only", "--no-audit"],
            cwd=tmp_path,
            timeout=60,
            capture_output=True,
            check=True,
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        pytest.skip("npm absent ou install --package-lock-only échoué")

    stdout, code = _run_deps_scan(tmp_path)
    assert code == 0

    # Crucial : stdout doit être UN SEUL objet JSON valide.
    # Si A-010 régresse, json.loads lève "Extra data" car 2 objets sont concaténés.
    data = json.loads(stdout)
    assert isinstance(data, dict)


def test_deps_scan_empty_npm_output_falls_back_to_safe_default(tmp_path: Path) -> None:
    """Si npm audit produit un stdout vide (cas où npm cassé), le script doit
    émettre un fallback JSON valide, jamais deux objets."""
    # Setup : un faux 'npm' qui retourne stdout vide + exit 1
    fake_bin = tmp_path / "fake_bin"
    fake_bin.mkdir()
    fake_npm = fake_bin / "npm"
    fake_npm.write_text(
        textwrap.dedent(
            """\
            #!/bin/bash
            exit 1
            """
        ),
        encoding="utf-8",
    )
    fake_npm.chmod(0o755)

    (tmp_path / "package.json").write_text("{}", encoding="utf-8")

    result = subprocess.run(
        ["bash", str(DEPS_SCAN), str(tmp_path)],
        capture_output=True,
        text=True,
        timeout=10,
        env={"PATH": f"{fake_bin}:/usr/bin:/bin"},
    )
    assert result.returncode == 0

    # Doit être un seul objet JSON valide (le fallback)
    data = json.loads(result.stdout)  # ne doit PAS lever
    assert "metadata" in data
    assert "vulnerabilities" in data["metadata"]
    # Le fallback indique "0 vulns" (faux mais sûr — sans data, on assume sûr)
    assert data["metadata"]["vulnerabilities"]["high"] == 0
