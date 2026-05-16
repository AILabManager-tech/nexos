"""Tests: le package orchestrator expose le bon API (phase P chantier2).

Valide trois propriétés du refactor de `orchestrator.py` (~2244 L) en
package `orchestrator/` :
1. Les symboles publics historiques restent importables par les mêmes
   chemins (`import orchestrator`, `from orchestrator.pipeline import …`).
2. Les re-exports du package pointent sur les mêmes objets que les
   sous-modules (pas de duplication).
3. Les tailles de fichier restent sous les seuils indicatifs définis
   dans PHASE_P_REFACTOR_ORCHESTRATOR_MODULARISATION.md.
"""

from __future__ import annotations

import pathlib


def test_package_imports() -> None:
    import orchestrator

    assert hasattr(orchestrator, "main")
    assert hasattr(orchestrator, "PipelineOrchestrator")
    assert hasattr(orchestrator, "GateEngine")
    assert hasattr(orchestrator, "ConvergeLoop")
    assert hasattr(orchestrator, "run_pipeline")
    assert hasattr(orchestrator, "build_phase_prompt")


def test_shim_module_reexports() -> None:
    """L'import historique `from orchestrator import X` est préservé."""
    import orchestrator as o
    from orchestrator.gates import GateEngine
    from orchestrator.pipeline import PipelineOrchestrator

    assert o.PipelineOrchestrator is PipelineOrchestrator
    assert o.GateEngine is GateEngine


def test_submodules_are_importable() -> None:
    """Les sous-modules ciblés par le refactor sont tous importables."""
    import importlib

    for submodule in (
        "orchestrator.banner",
        "orchestrator.brief",
        "orchestrator.cli_args",
        "orchestrator.cli_runner",
        "orchestrator.converge",
        "orchestrator.gates",
        "orchestrator.gates_persistence",
        "orchestrator.knowledge",
        "orchestrator.main",
        "orchestrator.phases",
        "orchestrator.pipeline",
        "orchestrator.preflight",
        "orchestrator.prompts",
        "orchestrator.verify",
    ):
        importlib.import_module(submodule)


def test_file_sizes_targets() -> None:
    """Seuils indicatifs — phase P modularisation."""
    pkg = pathlib.Path(__file__).resolve().parent.parent / "orchestrator"
    sizes = {p.name: len(p.read_text().splitlines()) for p in pkg.glob("*.py")}

    # Seuils des modules "coeur" ciblés par le refactor.
    assert sizes.get("__init__.py", 0) <= 150
    assert sizes.get("main.py", 0) <= 200
    assert sizes.get("pipeline.py", 0) <= 250
    assert sizes.get("gates.py", 0) <= 200
    assert sizes.get("converge.py", 0) <= 200
    # phases.py contient run_pipeline + run_converge (legacy procédural,
    # iso-comportement). Plafond relâché successivement :
    #   620  — chantier 4 (A-002 barrière quiescence ph4 + reconciliation)
    #   640  — P8.3 intégration hook on_enriched_retry (dimension-scoped
    #          auto-fix). Le callback factory `make_plateau_auto_fix_hook`
    #          extrait l'essentiel du code dans `orchestrator/plateau_recovery.py`
    #          pour limiter la croissance — seuls les arguments d'instanciation
    #          + commentaire restent ici (~12 lignes nettes).
    # Cible finale ≤500 quand run_pipeline aura été décomposé en phases-as-classes.
    assert sizes.get("phases.py", 0) <= 640
    # cli_args.py: argparse complet pour tous les modes.
    assert sizes.get("cli_args.py", 0) <= 200

    # Le shim orchestrator.py est remplacé par le package — s'il subsiste,
    # il doit rester un re-export mince (garde-fou historique).
    shim = pkg.parent / "orchestrator.py"
    if shim.exists():
        shim_lines = len(shim.read_text().splitlines())
        assert shim_lines <= 80, f"orchestrator.py shim trop gros : {shim_lines} lignes"
