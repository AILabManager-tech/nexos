"""Vérification des outputs de phase et conversion des reports d'auto-fix."""

from __future__ import annotations

import re
from pathlib import Path

from ._shared import OUTPUT_MAP, say
from .brief import load_runtime_brief
from .prompts import _validate_phase_against_intake

_ERROR_PATTERNS = re.compile(
    r"(?i)(^error:|^fatal:|traceback \(most recent|"
    r"command not found|permission denied|ENOENT|EACCES|"
    r"^✗ .*(échoué|failed|erreur))",
    re.MULTILINE,
)


def verify_phase_output(phase: str, client_dir: Path) -> bool:
    """Vérifie que la phase a produit un output valide.

    Checks:
    - Le fichier existe
    - Taille >= 500 octets
    - Le contenu ne contient pas de patterns d'erreur critiques
    """
    if phase not in OUTPUT_MAP:
        say(f"[yellow]⚠ Phase {phase} non reconnue dans OUTPUT_MAP — skip validation[/]")
        return True

    output_file = client_dir / OUTPUT_MAP[phase]
    if not output_file.exists():
        say(f"[red]✗ Phase {phase} n'a pas produit de rapport ({output_file.name})[/]")
        return False

    content = output_file.read_text(encoding="utf-8", errors="replace")
    size = len(content.encode("utf-8"))

    if size < 500:
        say(f"[red]✗ Phase {phase} rapport trop court ({size} octets < 500)[/]")
        return False

    head = content[:2000]
    match = _ERROR_PATTERNS.search(head)
    if match:
        say(f"[red]✗ Phase {phase} rapport contient une erreur : {match.group()!r}[/]")
        return False

    brief = None
    brief_path = client_dir / "brief-client.json"
    if brief_path.exists():
        try:
            brief = load_runtime_brief(brief_path)
        except Exception:
            brief = None
    intake_issues = _validate_phase_against_intake(phase, content, brief)
    if intake_issues:
        say(f"[red]✗ Phase {phase} rapport hors cadrage mission.intake : {intake_issues[0]}[/]")
        return False

    say(f"[green]✓ Phase {phase} rapport valide ({size} octets)[/]")
    return True


def _fix_report_to_dict(report) -> dict:
    """Convertit un FixReport en dict pour le changelog."""
    d: dict = {"total_fixes": report.total_fixes}
    if report.cookie_consent_added:
        d["cookie_consent"] = True
    if report.npm_audit_fixed > 0:
        d["npm_audit_fixed"] = report.npm_audit_fixed
    if report.vercel_headers_fixed:
        d["vercel_headers"] = True
    if report.next_config_patched:
        d["next_config"] = True
    if report.privacy_page_added:
        d["privacy_page"] = True
    if report.legal_page_added:
        d["legal_page"] = True
    return d


__all__ = ["_fix_report_to_dict", "verify_phase_output"]
