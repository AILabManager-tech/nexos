"""
NEXOS v4.0 — Interactive session launcher for host CLIs.

Starts Codex, Claude, or Gemini in a NEXOS-oriented session so `nexos`
can act as an environment bootstrap, not only as a pipeline subcommand CLI.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from nexos.logging_config import get_logger

logger = get_logger(__name__)
console = Console()


def say(*args, **kwargs):
    # UX output: routes through module-level `console` (patchable in tests)
    # and avoids the `print(` lexical pattern at callsites.
    console.print(*args, **kwargs)


@dataclass(frozen=True)
class HostCLI:
    """Metadata for a supported interactive host CLI."""

    name: str
    binary: str


class MenuBack(Exception):  # noqa: N818 — control-flow signal, not an error (mirrors StopIteration)
    """Raised when the user requests to go back in the interactive menu."""


class MenuQuit(Exception):  # noqa: N818 — control-flow signal, not an error (mirrors StopIteration)
    """Raised when the user requests to quit the interactive menu."""


SUPPORTED_HOSTS: tuple[HostCLI, ...] = (
    HostCLI(name="codex", binary="codex"),
    HostCLI(name="claude", binary="claude"),
    HostCLI(name="gemini", binary="gemini"),
)

MODE_CHOICES: tuple[tuple[str, str], ...] = (
    ("create", "Creation complete d'un site"),
    ("audit", "Audit d'un site existant"),
    ("modify", "Modification ciblee"),
    ("content", "Redaction / traduction"),
    ("analyze", "Discovery seule"),
    ("converge", "Boucle de convergence SOIC"),
    ("knowledge", "Agent cognitif / synthese"),
    ("doctor", "Diagnostic systeme"),
    ("fix", "Auto-correction D4/D8"),
    ("report", "Rapport agrege client"),
)

HOST_PROFILES: dict[str, dict[str, str]] = {
    "codex": {
        "forces": "Execution technique, modifications de fichiers, refactor, validation locale.",
        "faiblesses": "Moins utile si le besoin est surtout editorial ou exploratoire.",
    },
    "claude": {
        "forces": "Structuration, cadrage, redaction, arbitrages produit, reformulation.",
        "faiblesses": "Moins naturel si tu veux surtout executer vite du code et des commandes.",
    },
    "gemini": {
        "forces": "Exploration, synthese large, ideation, comparaison d'options.",
        "faiblesses": "Moins centre sur le flux build / patch / verification locale stricte.",
    },
}

MODE_RECOMMENDATIONS: dict[str, tuple[str, str]] = {
    "create": (
        "codex",
        "Meilleur choix pour enchainer scaffold, edition, build et corrections dans le repo.",
    ),
    "audit": (
        "codex",
        "Le mode audit NEXOS repose sur des outils locaux, des scans et des artefacts de projet.",
    ),
    "modify": ("codex", "Le travail est cible sur le code existant, avec edition et verification."),
    "content": (
        "claude",
        "Plus adapte si la priorite est la qualite de redaction, de ton et de structure.",
    ),
    "analyze": ("gemini", "Utile si tu veux surtout explorer, comparer et cadrer avant d'agir."),
    "converge": (
        "codex",
        "Le mode convergence profite d'un agent oriente execution et reruns SOIC.",
    ),
    "knowledge": ("claude", "Bon equilibre pour synthese, abstraction et restitution lisible."),
    "doctor": (
        "codex",
        "Le diagnostic touche directement l'environnement local et les commandes du repo.",
    ),
    "fix": ("codex", "Le mode fix est un flux d'edition et de validation locale."),
    "report": (
        "claude",
        "Pertinent si tu veux une lecture plus narrative et interpretee des artefacts NEXOS.",
    ),
}


def _which(binary: str) -> bool:
    return shutil.which(binary) is not None


def _read_parent_command() -> str:
    """Best-effort parent process detection for host auto-selection."""
    try:
        # SAFE: static argv list, os.getppid() is an int. shell=False (default).
        result = subprocess.run(
            ["ps", "-o", "command=", "-p", str(os.getppid())],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        return ""
    return result.stdout.strip().lower()


def detect_host_cli(explicit_host: str | None = None) -> HostCLI:
    """Resolve the host CLI from explicit input, env, parent process, or availability."""
    if explicit_host:
        normalized = explicit_host.lower().strip()
        for host in SUPPORTED_HOSTS:
            if host.name == normalized:
                if not _which(host.binary):
                    raise RuntimeError(f"CLI hôte demandé introuvable: {host.binary}")
                return host
        raise RuntimeError(f"CLI hôte non supporté: {explicit_host}")

    env_host = os.environ.get("NEXOS_HOST_CLI")
    if env_host:
        return detect_host_cli(env_host)

    parent_command = _read_parent_command()
    for host in SUPPORTED_HOSTS:
        if host.binary in parent_command and _which(host.binary):
            return host

    for host in SUPPORTED_HOSTS:
        if _which(host.binary):
            return host

    raise RuntimeError("Aucun CLI hôte supporté trouvé (codex, claude, gemini).")


HOST_MANIFEST: dict[str, str] = {
    "claude": "CLAUDE.md",
    "codex": "AGENTS.md",
    "gemini": "GEMINI.md",
}


def build_session_prompt(nexos_root: Path, host_name: str) -> str:
    """Create the bootstrap instructions injected into the host CLI."""
    manifest_filename = HOST_MANIFEST.get(host_name, "CLAUDE.md")
    manifest_path = nexos_root / manifest_filename
    return f"""# NEXOS v4.0 — Bootstrap Session

Tu prends maintenant le poste actif dans la hiérarchie NEXOS pour ce workspace.
CLI hôte détecté: {host_name}
Racine NEXOS: {nexos_root}

Ordre d'autorité local à respecter:
1. {manifest_path}
2. agents/{{phase}}/_orchestrator.md
3. agents/{{phase}}/*.md
4. soic/
5. templates/ et tools/

Actions obligatoires immédiatement:
- Lire {manifest_path}
- Adopter explicitement l'identité NEXOS, pas celle d'un assistant générique
- Afficher un en-tête NEXOS court en ouverture
- Expliquer brièvement la hiérarchie active: ph0 → ph5, SOIC, tooling réel, auto-fix
- Demander ensuite l'objectif opératoire de la session si aucun objectif n'est fourni

Règles d'exécution:
- Tu es l'orchestrateur NEXOS en façade
- Tu places le CLI hôte comme moteur d'exécution dans la hiérarchie NEXOS
- Tu t'appuies sur les agents et manifests du dépôt avant d'improviser
- Si l'utilisateur tape seulement "nexos", considère que cette session bootstrap est l'intention
"""


def build_mode_session_prompt(nexos_root: Path, host_name: str, mode: str) -> str:
    """Create a bootstrap prompt enriched with the selected NEXOS mode."""
    base = build_session_prompt(nexos_root, host_name)
    recommendation = MODE_RECOMMENDATIONS.get(mode)
    recommendation_text = recommendation[1] if recommendation else ""
    return (
        f"{base}\n\n"
        f"Mode NEXOS sélectionné par l'utilisateur: {mode}\n"
        f"Pourquoi ce mode: {recommendation_text}\n\n"
        "Repere UX a conserver dans l'ouverture:\n"
        "- Afficher un rappel court: [Enter]=recommande | [b]=retour | [q]=quitter\n"
        "- Garder une ouverture sobre, orientee action, non marketing\n\n"
        "Ce que tu dois faire en premier:\n"
        f"- Confirmer que tu entres en mode `{mode}`\n"
        f"- Expliquer en 3 à 6 lignes comment NEXOS va traiter le mode `{mode}`\n"
        "- Poser la prochaine question strictement utile pour lancer le travail\n"
    )


def build_launcher_command(host: HostCLI, nexos_root: Path, prompt: str) -> list[str]:
    """Build the interactive command line for the selected host."""
    root = str(nexos_root)
    if host.name == "codex":
        return [host.binary, "--cd", root, prompt]
    if host.name == "claude":
        return [
            host.binary,
            "--add-dir",
            root,
            "--system-prompt",
            prompt,
            "Prends ta place dans NEXOS et annonce la hiérarchie active.",
        ]
    if host.name == "gemini":
        return [
            host.binary,
            "--include-directories",
            root,
            "--prompt-interactive",
            prompt,
        ]
    raise RuntimeError(f"CLI hôte non supporté: {host.name}")


def print_session_banner(host: HostCLI, nexos_root: Path) -> None:
    """Render a local bootstrap banner before handing control to the host CLI."""
    say(
        Panel(
            "[bold cyan]NEXOS v4.0[/]\n"
            f"Host CLI: [bold]{host.name}[/]\n"
            "Hiérarchie: ph0 → ph5 | SOIC | Tooling réel | Auto-Fix\n"
            "Raccourcis: [Enter]=recommande | [b]=retour | [q]=quitter\n"
            f"Workspace: {nexos_root}",
            title="[bold cyan]⚡ Session NEXOS[/]",
            border_style="cyan",
        )
    )


def _available_hosts() -> list[HostCLI]:
    return [host for host in SUPPORTED_HOSTS if _which(host.binary)]


def _prompt_choice(
    max_index: int,
    default_index: int | None = None,
    allow_back: bool = False,
) -> int:
    prompt_suffix = f" [{default_index}]" if default_index is not None else ""
    while True:
        raw = input(f"> {prompt_suffix} ").strip()
        if raw == "" and default_index is not None:
            return default_index
        lowered = raw.lower()
        if lowered == "q":
            raise MenuQuit()
        if lowered == "b" and allow_back:
            raise MenuBack()
        if raw.isdigit():
            value = int(raw)
            if 1 <= value <= max_index:
                return value
        hint = " `b` = retour," if allow_back else ""
        say(f"[yellow]Choix invalide. Entre un nombre de 1 a {max_index},{hint} `q` = quitter.[/]")


def _render_main_menu() -> str:
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("#", style="bold")
    table.add_column("Mode", style="bold white")
    table.add_column("Description", style="dim")
    for index, (mode, description) in enumerate(MODE_CHOICES, start=1):
        table.add_row(str(index), mode, description)

    say(
        Panel(
            table,
            title="[bold cyan]Menu principal NEXOS[/]",
            subtitle="Entree = recommandation | q = quitter",
            border_style="cyan",
        )
    )
    return MODE_CHOICES[_prompt_choice(len(MODE_CHOICES), default_index=1) - 1][0]


def _render_host_menu(selected_mode: str, hosts: list[HostCLI]) -> HostCLI:
    recommended_name, reason = MODE_RECOMMENDATIONS.get(
        selected_mode,
        ("codex", "Bon choix par defaut pour travailler dans le repo."),
    )
    say("")
    say(
        Panel(
            f"[bold]Mode choisi:[/] {selected_mode}\n"
            f"[bold]Recommendation NEXOS:[/] {recommended_name}\n"
            f"{reason}",
            title="[bold cyan]Selection du CLI hote[/]",
            subtitle="Entree = recommandation | b = retour | q = quitter",
            border_style="cyan",
        )
    )

    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("#", style="bold")
    table.add_column("CLI", style="bold white")
    table.add_column("Forces", style="green")
    table.add_column("Faiblesses", style="yellow")
    for index, host in enumerate(hosts, start=1):
        profile = HOST_PROFILES[host.name]
        marker = " (Recommande)" if host.name == recommended_name else ""
        table.add_row(
            str(index),
            f"{host.name}{marker}",
            profile["forces"],
            profile["faiblesses"],
        )

    say(table)
    recommended_index = next(
        (i for i, host in enumerate(hosts, start=1) if host.name == recommended_name),
        1,
    )
    return hosts[_prompt_choice(len(hosts), default_index=recommended_index, allow_back=True) - 1]


def _confirm_selection(selected_mode: str, host: HostCLI) -> str:
    """Show a final summary and let the user confirm or go back."""
    recommended_name, reason = MODE_RECOMMENDATIONS.get(
        selected_mode,
        ("codex", "Bon choix par defaut pour travailler dans le repo."),
    )
    profile = HOST_PROFILES[host.name]
    say("")
    say(
        Panel(
            f"[bold]Mode:[/] {selected_mode}\n"
            f"[bold]CLI hote:[/] {host.name}\n"
            f"[bold]Recommendation NEXOS:[/] {recommended_name}\n"
            f"[bold]Pourquoi:[/] {reason}\n"
            f"[bold]Forces du CLI choisi:[/] {profile['forces']}\n"
            f"[bold]Faiblesses du CLI choisi:[/] {profile['faiblesses']}",
            title="[bold cyan]Resume avant lancement[/]",
            subtitle="Entree = lancer | 2/b = changer le CLI | 3 = changer le mode | q = quitter",
            border_style="cyan",
        )
    )
    say("1. Lancer la session")
    say("2. Revenir au choix du CLI")
    say("3. Revenir au menu principal")
    try:
        choice = _prompt_choice(3, default_index=1, allow_back=True)
    except MenuBack:
        return "host"
    return {1: "launch", 2: "host", 3: "mode"}[choice]


def select_mode_and_host(explicit_host: str | None = None) -> tuple[str, HostCLI]:
    """Interactive front door: ask what to do, then which host CLI to use."""
    hosts = _available_hosts()
    if not hosts:
        raise RuntimeError("Aucun CLI hôte supporté trouvé (codex, claude, gemini).")

    try:
        while True:
            selected_mode = _render_main_menu()
            while True:
                try:
                    if explicit_host:
                        selected_host = detect_host_cli(explicit_host)
                    else:
                        selected_host = _render_host_menu(selected_mode, hosts)
                except MenuBack:
                    break

                action = _confirm_selection(selected_mode, selected_host)
                if action == "launch":
                    return selected_mode, selected_host
                if action == "mode":
                    break
                if explicit_host:
                    say("[yellow]CLI hote fixe via --host. Retour au menu principal.[/]")
                    break
    except MenuQuit:
        raise SystemExit(0) from None


def launch_session(
    nexos_root: Path,
    explicit_host: str | None = None,
    print_prompt_only: bool = False,
) -> int:
    """Launch an interactive host CLI already primed with the NEXOS bootstrap."""
    selected_mode, host = select_mode_and_host(explicit_host)
    prompt = build_mode_session_prompt(nexos_root, host.name, selected_mode)

    if print_prompt_only:
        say(prompt, markup=False)
        return 0

    print_session_banner(host, nexos_root)
    cmd = build_launcher_command(host, nexos_root, prompt)
    # SAFE: cmd is an argv list built by build_launcher_command from a
    # whitelisted host binary + static CLI flags + internal prompt template.
    # shell=False (default). No user string is shell-interpolated.
    result = subprocess.run(cmd, cwd=str(nexos_root), check=False)
    return result.returncode
