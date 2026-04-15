"""Vérifie que l'entry point CLI fonctionne après refactor (chantier2 phase B).

Protège contre la régression du pattern `exec(open(...).read())` qui était
dangereux et compliquait la compréhension du flux d'exécution.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI = REPO_ROOT / "nexos_cli.py"


def test_cli_file_exists() -> None:
    assert CLI.exists(), f"nexos_cli.py manquant: {CLI}"


def test_cli_does_not_use_exec_open_read() -> None:
    """Interdit le retour de l'anti-pattern exec(open(...).read()).

    On analyse l'AST pour ignorer les mentions du pattern dans les docstrings
    (utiles pour documenter la régression évitée) et ne détecter que les
    vrais appels `exec(...)` dans le code exécutable.
    """
    content = CLI.read_text(encoding="utf-8")
    tree = ast.parse(content, filename=str(CLI))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name) and func.id == "exec":
                pytest_msg = (
                    f"Appel exec() détecté dans {CLI} ligne {node.lineno}. "
                    "Le pattern exec(open(...).read()) est interdit "
                    "depuis chantier2 phase B."
                )
                raise AssertionError(pytest_msg)


def test_cli_help_runs() -> None:
    """`nexos --help` doit terminer rapidement sans crasher violemment."""
    result = subprocess.run(
        [sys.executable, str(CLI), "--help"],
        capture_output=True,
        timeout=30,
        check=False,
    )
    assert result.returncode in (0, 1, 2), (
        f"nexos --help exited {result.returncode}. "
        f"stderr (tronqué): {result.stderr.decode('utf-8', errors='replace')[:500]}"
    )
    output = (result.stdout + result.stderr).decode("utf-8", errors="replace")
    assert "usage" in output.lower() or "nexos" in output.lower(), (
        "La sortie de --help ne ressemble pas à de l'aide argparse."
    )
