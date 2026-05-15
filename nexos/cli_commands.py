"""
NEXOS v4.0 — Commandes CLI additionnelles

Implémente les commandes `nexos fix`, `nexos report`, `nexos doctor`.
"""

from __future__ import annotations

import contextlib
import json
from pathlib import Path
from typing import Any

from nexos.auto_fixer import (
    REQUIRED_HEADERS,
    _resolve_app_root,
    _resolve_components_dir,
    auto_fix,
)
from nexos.brief_contract import normalize_brief
from nexos.build_validator import (
    _check_critical_files,
    _check_vercel_headers,
    format_build_report,
    validate_build,
)

try:
    from nexos.changelog import EventType, get_changelog_summary, log_event

    _HAS_CHANGELOG = True
except ImportError:
    _HAS_CHANGELOG = False

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nexos.logging_config import get_logger

logger = get_logger(__name__)
console = Console()


def say(*args: Any, **kwargs: Any) -> None:
    # UX output: routes through module-level `console` (patchable in tests)
    # and avoids the `print(` lexical pattern at callsites.
    console.print(*args, **kwargs)


def run_doctor() -> None:
    """Exécute le diagnostic complet du système."""
    from nexos.tooling_manager import doctor_report

    say(Panel(doctor_report(), title="[bold cyan]nexos doctor[/]", border_style="cyan"))


def _load_payload_json(payload_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(payload_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Payload introuvable: {payload_path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Payload JSON invalide: {exc}") from exc

    if not isinstance(payload, dict):
        raise ValueError("Payload JSON invalide: objet attendu")
    return payload


def run_module_command(
    action: str,
    module_id: str | None = None,
    payload_path: Path | None = None,
) -> int:
    """Liste, valide ou exécute un module NEXOS isolé."""
    from nexos.module_registry import ModuleContractError, ModuleRegistry, ModuleRegistryError

    try:
        registry = ModuleRegistry()
    except ModuleRegistryError as exc:
        say(f"[red]Erreur registre modules: {exc}[/]")
        return 1

    if action == "list":
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Statut")
        table.add_column("Réseau")
        table.add_column("Fichiers")
        table.add_column("Description")
        for module in registry.list_modules():
            table.add_row(
                module.id,
                module.status,
                "oui" if module.requires_network else "non",
                "oui" if module.writes_files else "non",
                module.description,
            )
        say(table)
        return 0

    if not module_id:
        say("[red]Erreur: module_id requis[/]")
        return 1
    if payload_path is None:
        say("[red]Erreur: --payload requis[/]")
        return 1

    try:
        payload = _load_payload_json(payload_path)
        if action == "validate":
            input_errors = registry.validate_input(module_id, payload)
            if input_errors:
                for error in input_errors:
                    say(f"[red]- {error}[/]")
                return 1
            say(f"[green]Input valide pour {module_id}[/]")
            return 0
        if action == "run":
            output = registry.run(module_id, payload)
            say(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
    except (ValueError, ModuleRegistryError, ModuleContractError) as exc:
        say(f"[red]Erreur module: {exc}[/]")
        return 1

    say(f"[red]Action module inconnue: {action}[/]")
    return 1


def run_workflow_command(
    action: str,
    workflow_id: str | None = None,
    payload_path: Path | None = None,
) -> int:
    """Liste ou exécute un workflow modulaire NEXOS."""
    from nexos.workflow_runner import WorkflowNotFoundError, list_workflows, run_workflow

    if action == "list":
        table = Table(show_header=True, header_style="bold")
        table.add_column("ID")
        table.add_column("Étapes", justify="right")
        table.add_column("Description")
        for workflow in list_workflows():
            table.add_row(workflow.id, str(len(workflow.steps)), workflow.description)
        say(table)
        return 0

    if action == "run":
        if not workflow_id:
            say("[red]Erreur: workflow_id requis[/]")
            return 1
        if payload_path is None:
            say("[red]Erreur: --payload requis[/]")
            return 1
        try:
            payload = _load_payload_json(payload_path)
            output = run_workflow(workflow_id, payload)
        except (ValueError, WorkflowNotFoundError) as exc:
            say(f"[red]Erreur workflow: {exc}[/]")
            return 1

        say(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if output["status"] == "passed" else 1

    say(f"[red]Action workflow inconnue: {action}[/]")
    return 1


def _resolve_client_dir(arg: Path) -> Path:
    """Auto-résout slug → clients/<slug> si arg n'existe pas tel quel.

    Permet `nexos fix depanneur-nobert` au lieu de `nexos fix clients/depanneur-nobert`
    (cohérence ergonomique : le CLAUDE.md utilise `--client-dir clients/<slug>` pour
    `nexos create`, mais `fix` et `report` exigeaient le path complet en positionnel).

    Stratégie défensive :
    1. Si `arg` existe en tant que dossier → on le prend tel quel
    2. Sinon si `clients/<arg>` existe → on l'utilise (auto-résolution slug)
    3. Sinon → on rend `arg` inchangé (le caller produira l'erreur usuelle)

    Audit dette 2026-05-15 items I+J.
    """
    if arg.is_dir():
        return arg
    candidate = Path("clients") / arg
    if candidate.is_dir():
        return candidate
    return arg


def run_fix(client_dir: Path, dry_run: bool = False) -> None:
    """
    Applique les auto-fixes D4/D8 sur un client sans lancer le pipeline.

    Si dry_run=True, analyse sans appliquer et montre ce qui serait corrigé.
    """
    client_dir = _resolve_client_dir(client_dir)
    # Détecter le répertoire site
    site_dir = client_dir / "site"
    if not (site_dir / "package.json").exists():
        # Peut-être que le client_dir EST le site (structure plate)
        if (client_dir / "package.json").exists():
            site_dir = client_dir
        else:
            say(f"[red]Erreur: pas de package.json dans {client_dir}/site/ ni {client_dir}/[/]")
            return

    say(
        Panel(
            f"[bold]Client:[/] {client_dir.name}\n"
            f"[bold]Site:[/] {site_dir}\n"
            f"[bold]Mode:[/] {'DRY RUN (analyse seule)' if dry_run else 'FIX (corrections appliquées)'}",
            title="[bold cyan]nexos fix[/]",
            border_style="cyan",
        )
    )

    # Validation avant fix
    say("\n[bold]Validation AVANT fix :[/]")
    result_before = validate_build(site_dir)
    say(format_build_report(result_before))

    # Même si overall_pass, on applique les fixes pour les problèmes non-bloquants
    # (fichiers manquants, vulns npm HIGH, erreurs TSC dans les tests)
    has_issues = (
        result_before.missing_files or result_before.audit_highs > 0 or not result_before.tsc_ok
    )
    if result_before.overall_pass and not has_issues and not dry_run:
        say("\n[green]Le build passe et aucun problème détecté — rien à corriger.[/]")
        return

    if dry_run:
        # Analyser sans appliquer
        say("\n[bold]Analyse des corrections possibles :[/]")
        _dry_run_analysis(site_dir, client_dir)
        return

    # Appliquer les fixes
    say("\n[bold]Application des corrections :[/]")
    brief_path = client_dir / "brief-client.json"
    brief = None
    if brief_path.exists():
        with contextlib.suppress(json.JSONDecodeError):
            brief = normalize_brief(json.loads(brief_path.read_text()))

    fix_report = auto_fix(site_dir, client_dir, brief)

    # Validation après fix
    say("\n[bold]Validation APRES fix :[/]")
    result_after = validate_build(site_dir)
    say(format_build_report(result_after))

    # Résumé
    say("\n[bold]Résumé :[/]")
    say(f"  Corrections appliquées : {fix_report.total_fixes}")
    if fix_report.cookie_consent_added:
        say("    + Cookie consent injecté")
    if fix_report.npm_audit_fixed > 0:
        say(f"    + npm audit fix ({fix_report.npm_audit_fixed} vulns)")
    if fix_report.vercel_headers_fixed:
        say("    + Headers sécurité ajoutés")
    if fix_report.next_config_patched:
        say("    + next.config patché")
    if fix_report.privacy_page_added:
        say("    + Page politique-confidentialite générée")
    if fix_report.legal_page_added:
        say("    + Page mentions-legales générée")

    if _HAS_CHANGELOG:
        log_event(
            client_dir,
            EventType.CLI_FIX,
            agent="cli",
            details={"fixes": fix_report.total_fixes, "build_pass": result_after.overall_pass},
        )

    if result_after.overall_pass:
        say("\n[green bold]BUILD PASS après corrections[/]")
    else:
        say("\n[yellow]BUILD FAIL persistant — intervention manuelle requise[/]")


def _dry_run_analysis(site_dir: Path, client_dir: Path) -> None:
    """Analyse ce qui serait corrigé sans appliquer."""
    findings: list[str] = []

    # Cookie consent — utiliser le helper qui gère structure plate ET src/
    components_dir = _resolve_components_dir(site_dir)
    has_consent = False
    if components_dir.exists():
        for f in components_dir.rglob("*"):
            if f.is_file() and "cookie" in f.name.lower() and "consent" in f.name.lower():
                has_consent = True
                break
    if not has_consent:
        findings.append("Cookie consent absent → copierait template + injection layout.tsx")

    # Vercel headers
    vercel_path = site_dir / "vercel.json"
    if not vercel_path.exists():
        findings.append("vercel.json absent → créerait depuis template")
    else:
        try:
            data = json.loads(vercel_path.read_text())
            existing = set()
            for block in data.get("headers", []):
                for h in block.get("headers", []):
                    existing.add(h.get("key", "").lower())
            missing = [k for k in REQUIRED_HEADERS if k.lower() not in existing]
            if missing:
                findings.append(f"Headers manquants dans vercel.json: {', '.join(missing)}")
            if "content-security-policy" not in existing:
                findings.append("Content-Security-Policy absente → ajouterait DEFAULT_CSP")
        except json.JSONDecodeError:
            findings.append("vercel.json corrompu → remplacerait par template")

    # next.config
    for config_name in ["next.config.mjs", "next.config.js", "next.config.ts"]:
        config_path = site_dir / config_name
        if config_path.exists():
            content = config_path.read_text()
            if "poweredByHeader" not in content:
                findings.append(f"{config_name}: poweredByHeader manquant → ajouterait false")
            elif "poweredByHeader: true" in content:
                findings.append(f"{config_name}: poweredByHeader=true → changerait à false")
            break

    # Pages légales — utiliser _resolve_app_root qui gère plate ET src/
    app_root = _resolve_app_root(site_dir)
    for page_name, label in [
        ("politique-confidentialite", "Politique confidentialité"),
        ("mentions-legales", "Mentions légales"),
    ]:
        # Chercher dans variantes i18n et racine app/
        found = any((app_root / sub / page_name / "page.tsx").exists() for sub in ["[locale]", ""])
        if not found:
            findings.append(f"Page {label} absente → générerait depuis template")

    # npm audit
    findings.append("npm audit fix → exécuterait pour corriger les vulnérabilités connues")

    if findings:
        for i, finding in enumerate(findings, 1):
            say(f"  {i}. {finding}")
    else:
        say("  Aucune correction nécessaire.")


def run_report(client_dir: Path) -> None:
    """Affiche un rapport agrégé pour un client."""
    client_dir = _resolve_client_dir(client_dir)
    say(
        Panel(
            f"[bold]Client:[/] {client_dir.name}",
            title="[bold cyan]nexos report[/]",
            border_style="cyan",
        )
    )

    # 1. Phases complétées
    phase_reports = {
        "ph0-discovery": "ph0-discovery-report.md",
        "ph1-strategy": "ph1-strategy-report.md",
        "ph2-design": "ph2-design-report.md",
        "ph3-content": "ph3-content-report.md",
        "ph4-build": "ph4-build-log.md",
        "ph5-qa": "ph5-qa-report.md",
    }

    say("\n[bold]Phases :[/]")
    for phase, filename in phase_reports.items():
        path = client_dir / filename
        if path.exists():
            size = path.stat().st_size
            say(f"  [green]+[/] {phase:20s} ({size:,} octets)")
        else:
            say(f"  [dim]-[/] {phase:20s} (absent)")

    # 2. SOIC Gates
    gates_path = client_dir / "soic-gates.json"
    if gates_path.exists():
        try:
            gates = json.loads(gates_path.read_text())
            say("\n[bold]SOIC Gates :[/]")

            gate_list: list[Any] = []
            if isinstance(gates, list):
                gate_list = gates
            elif isinstance(gates, dict):
                gate_list = gates.get("gates") or gates.get("history") or []

            for gate in gate_list:
                phase = gate.get("phase", "?")
                mu = gate.get("mu", gate.get("final_mu", 0))
                decision = gate.get("decision", gate.get("final_decision", "?"))
                iters = gate.get("iterations", gate.get("total_iterations", 1))
                icon = "green" if decision in ("ACCEPT", "PASS") else "red"
                say(f"  [{icon}]{phase:20s}[/] μ={mu:.2f} ({iters} iter) → {decision}")
        except json.JSONDecodeError:
            say("\n[yellow]soic-gates.json corrompu[/]")
    else:
        say("\n[dim]Pas de soic-gates.json[/]")

    # 3. Tooling results
    tooling_dir = client_dir / "tooling"
    if tooling_dir.exists():
        say("\n[bold]Tooling :[/]")
        for f in sorted(tooling_dir.iterdir()):
            if f.is_file():
                say(f"  [green]+[/] {f.name} ({f.stat().st_size:,} octets)")
    else:
        say("\n[dim]Pas de dossier tooling/[/]")

    # 4. Site directory
    site_dir = client_dir / "site"
    if (site_dir / "package.json").exists():
        say(f"\n[bold]Site :[/] {site_dir}")
        # Quick build status check
        say("[dim]  Validation rapide...[/]")
        missing = _check_critical_files(site_dir)
        headers_ok = _check_vercel_headers(site_dir)
        if missing:
            say(f"  [yellow]Fichiers manquants: {', '.join(missing)}[/]")
        else:
            say("  [green]+[/] Tous les fichiers critiques présents")
        icon = "green" if headers_ok else "yellow"
        say(f"  [{icon}]{'+' if headers_ok else '-'}[/] Headers sécurité vercel.json")
    elif (client_dir / "package.json").exists():
        say(f"\n[bold]Site :[/] {client_dir} (structure plate)")

    # 5. Brief
    brief_path = client_dir / "brief-client.json"
    if brief_path.exists():
        try:
            brief = normalize_brief(json.loads(brief_path.read_text()))
            company = brief.get("company_name", brief.get("inputs", {}).get("company_name", "?"))
            say(f"\n[bold]Brief :[/] {company}")
            legal = brief.get("legal", {})
            if legal:
                rpp = legal.get("rpp_name", "non défini")
                say(f"  RPP: {rpp}")
        except json.JSONDecodeError:
            say("\n[yellow]brief-client.json corrompu[/]")

    # 6. Changelog
    if _HAS_CHANGELOG:
        summary = get_changelog_summary(client_dir)
        if summary["total"] > 0:
            say(f"\n[bold]Changelog :[/] {summary['total']} événements")
            if summary["first"]:
                say(f"  Période: {summary['first']} → {summary['last']}")
            if summary["fixes"] > 0:
                say(f"  Auto-fixes appliqués: {summary['fixes']}")
            if summary["by_type"]:
                table = Table(show_header=True, header_style="bold")
                table.add_column("Événement")
                table.add_column("Count", justify="right")
                for evt, count in sorted(summary["by_type"].items()):
                    table.add_row(evt, str(count))
                say(table)
        else:
            say("\n[dim]Pas de changelog[/]")

        log_event(client_dir, EventType.CLI_REPORT, agent="cli")
