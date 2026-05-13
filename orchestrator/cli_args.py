"""Parsing des arguments CLI NEXOS (argparse)."""

from __future__ import annotations

import argparse
from pathlib import Path

from ._shared import VALID_NIVEAUX, VALID_OBJECTIFS, VALID_TYPES


def build_parser() -> argparse.ArgumentParser:
    """Construit le parser argparse complet pour tous les modes NEXOS."""
    parser = argparse.ArgumentParser(
        prog="nexos",
        description="NEXOS v4.0 Orchestrator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""modes:
  session   Lance un CLI hôte (Codex/Claude/Gemini) en mode NEXOS
  create    Création complète d'un site (ph0 → ph5)
  audit     Audit d'un site existant (ph5-qa)
  modify    Modification ciblée
  content   Rédaction/traduction seule (ph3)
  analyze   Discovery seule (ph0)
  converge  Boucle de convergence SOIC sur un client existant
  doctor    Diagnostic système (outils, templates, SOIC)
  module    Registre modulaire NEXOS (list, validate, run)
  workflow  Workflows modulaires NEXOS
  fix       Auto-correction D4/D8 sur un client
  report    Rapport agrégé d'un client""",
    )

    subparsers = parser.add_subparsers(dest="mode", help="Mode d'opération")

    # Interactive session bootstrap
    sp_session = subparsers.add_parser(
        "session",
        help="Lance un CLI hôte en mode NEXOS",
        description="Démarre Codex, Claude ou Gemini avec le bootstrap NEXOS.",
    )
    sp_session.add_argument(
        "--host", choices=["codex", "claude", "gemini"], help="CLI hôte à lancer explicitement"
    )
    sp_session.add_argument(
        "--print-prompt", action="store_true", help="Afficher uniquement le prompt bootstrap"
    )

    # Pipeline modes
    for mode in ["create", "audit", "modify", "content", "analyze"]:
        sp = subparsers.add_parser(mode)
        sp.add_argument("--client-dir", type=Path, help="Dossier client existant")
        sp.add_argument("--url", type=str, help="URL du site (pour audit/preflight)")
        sp.add_argument("--brief", type=str, help="Chemin vers brief-client.json")
        sp.add_argument("--name", type=str, help="Nom du client (pour génération rapide)")
        sp.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="Lancer le wizard interactif pour générer le brief",
        )
        sp.add_argument(
            "--stack",
            choices=["nextjs", "nuxt", "astro", "fastapi", "generic"],
            help="Stack technique (résout le profil SOIC automatiquement)",
        )
        sp.add_argument("--profile", type=str, help="Profil SOIC (ex: web-nextjs, api-fastapi)")
        sp.add_argument(
            "--colors",
            nargs="*",
            metavar="ROLE=#HEX",
            help="Palette couleurs (ex: primary=#1A2B3C accent=#FFD700)",
        )
        if mode == "modify":
            sp.add_argument(
                "--section",
                nargs="*",
                metavar="S-NNN",
                help="Sections ciblées par ID (ex: S-001 S-003)",
            )

    # Knowledge mode
    sp_know = subparsers.add_parser(
        "knowledge",
        help="Agents cognitifs (résumé, analyse, synthèse)",
        description="Exécute un agent knowledge NEXOS (hors pipeline web).",
    )
    sp_know.add_argument("agent", type=str, help="ID de l'agent (ex: hexabrief)")
    sp_know.add_argument(
        "--source", type=str, required=True, help="Texte source ou 'Titre — Auteur'"
    )
    sp_know.add_argument(
        "--type",
        type=str,
        default="technique",
        choices=VALID_TYPES,
        dest="content_type",
        help="Type de contenu (défaut: technique)",
    )
    sp_know.add_argument(
        "--objectif",
        type=str,
        default="appliquer",
        choices=VALID_OBJECTIFS,
        help="Objectif de lecture (défaut: appliquer)",
    )
    sp_know.add_argument(
        "--niveau",
        type=str,
        default="complet",
        choices=VALID_NIVEAUX,
        help="Profondeur du résumé (défaut: complet)",
    )
    sp_know.add_argument(
        "--score-only", type=Path, default=None, help="Évaluer un résumé existant (path vers .md)"
    )

    # Converge mode
    sp_conv = subparsers.add_parser(
        "converge",
        help="Boucle de convergence SOIC",
        description="Évalue un client via SOIC et produit un plan de convergence.",
    )
    sp_conv.add_argument("client_dir", type=Path, help="Dossier client à évaluer")
    sp_conv.add_argument("--target", type=float, default=8.5, help="Score μ cible (défaut: 8.5)")
    sp_conv.add_argument("--max-iter", type=int, default=4, help="Itérations max (défaut: 4)")
    sp_conv.add_argument(
        "--timeout", type=int, default=15, help="Timeout global en minutes (défaut: 15)"
    )
    sp_conv.add_argument("--url", type=str, help="URL du site (pour preflight)")
    sp_conv.add_argument(
        "--dry-run", action="store_true", help="Évaluer sans corriger (rapport uniquement)"
    )
    sp_conv.add_argument(
        "--stack",
        choices=["nextjs", "nuxt", "astro", "fastapi", "generic"],
        help="Stack technique (résout le profil SOIC automatiquement)",
    )
    sp_conv.add_argument("--profile", type=str, help="Profil SOIC (ex: web-nextjs, api-fastapi)")

    subparsers.add_parser("doctor", help="Diagnostic système (outils, templates, SOIC)")

    sp_module = subparsers.add_parser("module", help="Registre modulaire NEXOS")
    module_subparsers = sp_module.add_subparsers(dest="module_action", required=True)
    module_subparsers.add_parser("list", help="Lister les modules disponibles")
    sp_module_validate = module_subparsers.add_parser(
        "validate", help="Valider un payload JSON contre le contrat input d'un module"
    )
    sp_module_validate.add_argument("module_id", type=str, help="ID du module")
    sp_module_validate.add_argument("--payload", type=Path, required=True, help="Payload JSON")
    sp_module_run = module_subparsers.add_parser("run", help="Exécuter un module")
    sp_module_run.add_argument("module_id", type=str, help="ID du module")
    sp_module_run.add_argument("--payload", type=Path, required=True, help="Payload JSON")

    sp_workflow = subparsers.add_parser("workflow", help="Workflows modulaires NEXOS")
    workflow_subparsers = sp_workflow.add_subparsers(dest="workflow_action", required=True)
    workflow_subparsers.add_parser("list", help="Lister les workflows disponibles")
    sp_workflow_run = workflow_subparsers.add_parser("run", help="Exécuter un workflow")
    sp_workflow_run.add_argument("workflow_id", type=str, help="ID du workflow")
    sp_workflow_run.add_argument("--payload", type=Path, required=True, help="Payload JSON")

    sp_fix = subparsers.add_parser("fix", help="Auto-correction D4/D8 sur un client")
    sp_fix.add_argument("client_dir", type=Path, help="Dossier client à corriger")
    sp_fix.add_argument("--dry-run", action="store_true", help="Analyser sans appliquer")

    sp_report = subparsers.add_parser("report", help="Rapport agrégé d'un client")
    sp_report.add_argument("client_dir", type=Path, help="Dossier client à analyser")

    return parser


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse les arguments CLI."""
    return build_parser().parse_args(argv)


__all__ = ["build_parser", "parse_cli_args"]
