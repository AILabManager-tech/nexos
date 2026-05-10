"""NEXOS startup banner — ASCII art + phases overview rendered via Rich."""

from __future__ import annotations

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


def print_banner() -> None:
    _con = Console()

    ascii_art = Text()
    ascii_art.append("\n")
    ascii_art.append("  ███╗   ██╗███████╗██╗  ██╗ ██████╗ ███████╗\n", style="bold #8B6914")
    ascii_art.append("  ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔════╝\n", style="bold #C49A1A")
    ascii_art.append("  ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗\n", style="bold #F0C520")
    ascii_art.append("  ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║\n", style="bold #FFD700")
    ascii_art.append("  ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║\n", style="bold #FFE87C")
    ascii_art.append("  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝\n", style="bold white")
    ascii_art.append("\n")
    ascii_art.append("       Web Builder Autonome  ·  v4.0  ·  MARK SYSTEMS\n", style="dim white")

    phases = Text()
    phases.append("  PH0 ", style="bold magenta")
    phases.append("Discovery  ", style="dim white")
    phases.append("→  ", style="dim white")
    phases.append("PH1 ", style="bold blue")
    phases.append("Strategy  ", style="dim white")
    phases.append("→  ", style="dim white")
    phases.append("PH2 ", style="bold cyan")
    phases.append("Design\n", style="dim white")
    phases.append("  PH3 ", style="bold green")
    phases.append("Content    ", style="dim white")
    phases.append("→  ", style="dim white")
    phases.append("PH4 ", style="bold yellow")
    phases.append("Build     ", style="dim white")
    phases.append("→  ", style="dim white")
    phases.append("PH5 ", style="bold red")
    phases.append("QA + Deploy\n", style="dim white")

    soic = Text()
    soic.append("  SOIC gates  ", style="bold white")
    soic.append("μ ≥ 8.0  ", style="bold yellow")
    soic.append("·  ", style="dim")
    soic.append("48 agents  ", style="bold white")
    soic.append("·  ", style="dim")
    soic.append("Auto-Fix D4/D8  ", style="bold white")
    soic.append("·  ", style="dim")
    soic.append("Loi 25\n", style="bold white")

    combined = Text()
    combined.append_text(ascii_art)
    combined.append_text(phases)
    combined.append("\n")
    combined.append_text(soic)

    _con.print(
        Panel(
            combined,
            border_style="yellow",
            box=box.DOUBLE_EDGE,
            padding=(0, 2),
        )
    )
    _con.print()
