"""Agents cognitifs (knowledge): HexaBrief summary + auto-scoring."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from rich.panel import Panel
from rich.table import Table

from ._shared import AGENTS_DIR, KNOWLEDGE_DIR, LOGS_DIR, NEXOS_ROOT, say
from .brief import slugify
from .cli_runner import run_codex_cli


def run_knowledge_agent(
    agent_id: str,
    source: str,
    content_type: str = "technique",
    objectif: str = "appliquer",
    niveau: str = "complet",
    score_only: Path | None = None,
) -> None:
    """Execute a knowledge agent (HexaBrief, etc.)."""

    if agent_id != "hexabrief":
        say(f"[red]Agent knowledge inconnu: {agent_id}[/]")
        say("[dim]Agents disponibles: hexabrief[/]")
        return

    # ── Score-only mode: évaluer un résumé existant ──
    if score_only is not None:
        say(f"\n[bold cyan]📊 HexaBrief SCORING — {score_only.name}[/]\n")
        try:
            from soic.knowledge_scoring import evaluate_hexabrief

            result = evaluate_hexabrief(score_only)

            table = Table(title="HexaBrief Scoring", border_style="cyan")
            table.add_column("Dimension", style="bold")
            table.add_column("Poids", justify="center")
            table.add_column("Score", justify="center")
            table.add_row("S1 Fidélité", "×1.2", f"{result.s1_fidelite:.1f}/10")
            table.add_row("S2 Densité", "×1.0", f"{result.s2_densite:.1f}/10")
            table.add_row("S3 Actionnabilité", "×1.1", f"{result.s3_actionnabilite:.1f}/10")
            table.add_row("S4 Esprit critique", "×1.1", f"{result.s4_esprit_critique:.1f}/10")
            table.add_row("S5 Mémorisabilité", "×1.0", f"{result.s5_memorisabilite:.1f}/10")
            table.add_row("", "", "")
            verdict_style = (
                "green" if result.mu >= 7.5 else ("yellow" if result.mu >= 6.0 else "red")
            )
            table.add_row(
                "[bold]μ pondéré[/]",
                "",
                f"[bold {verdict_style}]{result.mu:.2f}/10 — {result.verdict}[/]",
            )
            say(table)
        except FileNotFoundError as e:
            say(f"[red]✗ {e}[/]")
        except Exception as e:
            say(f"[red]✗ Erreur scoring: {e}[/]")
        return

    # ── Generation mode: produire un résumé via Codex CLI ──
    KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    source_slug = slugify(source)[:60]
    output_path = KNOWLEDGE_DIR / f"{source_slug}-summary.md"

    agent_path = AGENTS_DIR / "knowledge" / "hexabrief.md"
    if not agent_path.exists():
        say(f"[red]✗ Agent introuvable: {agent_path}[/]")
        return

    prompt_parts = [
        f"Lis {agent_path} et adopte le rôle décrit.",
        "",
        "PARAMETRES:",
        f"  TEXTE_OU_REFERENCE: {source}",
        f"  TYPE: {content_type}",
        f"  OBJECTIF: {objectif}",
        f"  NIVEAU: {niveau}",
        "",
        f"TEMPLATE DE SORTIE: Lis {NEXOS_ROOT / 'templates' / 'book-summary-template.md'}",
        "Remplis TOUS les placeholders {{...}} avec du contenu réel.",
        "Ne laisse AUCUN placeholder non rempli.",
        "",
        f"Écris le résumé complet dans {output_path}",
    ]
    prompt = "\n".join(prompt_parts)

    say(
        Panel(
            f"[bold]Agent:[/] HexaBrief Book Summarizer\n"
            f"[bold]Source:[/] {source}\n"
            f"[bold]Type:[/] {content_type} | [bold]Objectif:[/] {objectif} | [bold]Niveau:[/] {niveau}\n"
            f"[bold]Output:[/] {output_path}",
            title="[bold cyan]📚 NEXOS Knowledge — HexaBrief[/]",
            border_style="cyan",
        )
    )

    log_path = LOGS_DIR / f"{timestamp}_hexabrief_{source_slug}.log"
    returncode = run_codex_cli(prompt, str(NEXOS_ROOT), log_path)

    if returncode != 0:
        say(f"[red]✗ HexaBrief échoué (code {returncode})[/]")
        return

    if not output_path.exists() or output_path.stat().st_size < 200:
        say("[red]✗ Résumé non généré ou trop court[/]")
        return

    say(f"[green]✓ Résumé généré: {output_path}[/]")

    say("\n[bold cyan]📊 Auto-scoring HexaBrief...[/]\n")
    try:
        from soic.knowledge_scoring import evaluate_hexabrief

        result = evaluate_hexabrief(output_path)

        table = Table(title="HexaBrief Scoring", border_style="cyan")
        table.add_column("Dimension", style="bold")
        table.add_column("Poids", justify="center")
        table.add_column("Score", justify="center")
        table.add_row("S1 Fidélité", "×1.2", f"{result.s1_fidelite:.1f}/10")
        table.add_row("S2 Densité", "×1.0", f"{result.s2_densite:.1f}/10")
        table.add_row("S3 Actionnabilité", "×1.1", f"{result.s3_actionnabilite:.1f}/10")
        table.add_row("S4 Esprit critique", "×1.1", f"{result.s4_esprit_critique:.1f}/10")
        table.add_row("S5 Mémorisabilité", "×1.0", f"{result.s5_memorisabilite:.1f}/10")
        table.add_row("", "", "")
        verdict_style = "green" if result.mu >= 7.5 else ("yellow" if result.mu >= 6.0 else "red")
        table.add_row(
            "[bold]μ pondéré[/]",
            "",
            f"[bold {verdict_style}]{result.mu:.2f}/10 — {result.verdict}[/]",
        )
        say(table)

        if result.verdict == "REJECT":
            say(
                "[red]⚠ Le résumé ne passe pas le seuil minimum. Relancer avec un niveau plus élevé.[/]"
            )
        elif result.verdict == "REVISE":
            say("[yellow]⚠ Le résumé nécessite des corrections. Vérifier les sections faibles.[/]")
    except ImportError:
        say("[yellow]⚠ Module scoring non disponible — skip auto-scoring[/]")
    except Exception as e:
        say(f"[yellow]⚠ Scoring error: {e}[/]")


__all__ = ["run_knowledge_agent"]
