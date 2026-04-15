"""
NEXOS v3.0 Orchestrator — Multi-phase avec quality gates SOIC
"""

import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

# NEXOS v4.0 augmentation modules
try:
    from nexos.tooling_manager import ensure_tooling
    from nexos.build_validator import validate_build
    from nexos.auto_fixer import auto_fix
    from nexos.brief_wizard import interactive_brief
    from nexos.brief_contract import normalize_brief, validate_brief
    _NEXOS_V4 = True
except ImportError:
    _NEXOS_V4 = False

try:
    from nexos.changelog import log_event, EventType
    _HAS_CHANGELOG = True
except ImportError:
    _HAS_CHANGELOG = False

try:
    from audit_toolkit.scanner import run_full_audit as _run_source_audit
    from audit_toolkit.config import AuditConfig as _ToolkitConfig
    _HAS_AUDIT_TOOLKIT = True
except ImportError:
    _HAS_AUDIT_TOOLKIT = False

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from nexos.logging_config import get_logger

logger = get_logger(__name__)
console = Console()


def say(*args, **kwargs):
    # UX output: routes through module-level `console` (patchable in tests)
    # and avoids the `print(` lexical pattern at callsites.
    console.print(*args, **kwargs)

NEXOS_ROOT = Path(__file__).parent.resolve()
CLIENTS_DIR = NEXOS_ROOT / "clients"
AGENTS_DIR = NEXOS_ROOT / "agents"
TOOLS_DIR = NEXOS_ROOT / "tools"
LOGS_DIR = NEXOS_ROOT / "logs"

# ── Quality gate thresholds (resolved from SOICProfile) ──────────────────────
# GATE_THRESHOLDS dict removed in R2 refactor — thresholds now live in
# SOICProfile.config.phase_thresholds. Use _get_default_profile() to access.
def _get_default_profile():
    """Lazy-load the default SOICProfile to avoid import-time side effects."""
    from soic.profile import get_profile
    return get_profile("web-nextjs")

_STACK_PROFILE_MAP = {
    "nextjs": "web-nextjs", "nuxt": "web-generic",
    "astro": "web-generic", "fastapi": "api-fastapi",
    "generic": "web-generic",
}

def _resolve_profile(stack=None, profile_name=None):
    """Resolve a SOICProfile from --stack or --profile CLI args."""
    from soic.profile import get_profile
    if profile_name:
        return get_profile(profile_name)
    if stack:
        return get_profile(_STACK_PROFILE_MAP.get(stack, "web-generic"))
    return None

# ── Phase sequence (legacy fallback — prefer PipelineConfig.from_brief()) ────
PHASES_CREATE = [
    "ph0-discovery", "ph1-strategy", "ph2-design",
    "ph3-content", "ph4-build", "ph5-qa"
]

PHASES_MAP = {
    "create":  PHASES_CREATE,
    "audit":   ["ph5-qa"],
    "modify":  ["site-update"],
    "content": ["ph3-content"],
    "analyze": ["ph0-discovery"],
}


def slugify(name: str) -> str:
    """Convertit un nom en slug kebab-case (supporte Unicode composé)."""
    slug = unicodedata.normalize("NFC", name).lower().strip()
    # Décomposer en NFD pour séparer les accents, puis retirer les diacritiques
    slug = unicodedata.normalize("NFD", slug)
    slug = "".join(c for c in slug if unicodedata.category(c) != "Mn")
    slug = re.sub(r'[^a-z0-9]+', '-', slug).strip('-')
    return slug


def generate_brief(mode: str, answers: dict, free_text: str = "") -> Path:
    """Génère le brief-client.json et retourne le chemin du dossier client."""
    timestamp = datetime.now().isoformat()
    client_name = answers.get("client_name", f"projet-{datetime.now().strftime('%Y-%m-%d')}")
    slug = slugify(client_name)

    client_dir = CLIENTS_DIR / slug
    client_dir.mkdir(parents=True, exist_ok=True)
    (client_dir / "tooling").mkdir(exist_ok=True)
    (client_dir / "site").mkdir(exist_ok=True)

    brief = {
        "_meta": {
            "generator": "nexos-v3.0",
            "created_at": timestamp,
            "mode": mode,
        },
        "client": {"name": client_name, "slug": slug},
        "mission": {
            "mode": mode,
            "phases": PHASES_MAP[mode],
        },
        "inputs": answers,
        "context_libre": free_text,
    }

    brief_path = client_dir / "brief-client.json"
    brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    say(f"[green]✓[/] Brief généré : {brief_path}")

    if _HAS_CHANGELOG:
        log_event(client_dir, EventType.BRIEF_CREATED, agent="orchestrator",
                  details={"slug": slug, "mode": mode})

    return client_dir


def generate_brief_from_wizard(mode: str, brief_data: dict) -> Path:
    """Crée le dossier client et écrit le brief généré par le wizard interactif."""
    brief_data = normalize_brief(brief_data, mode=mode)
    errors = validate_brief(brief_data)
    if errors:
        raise ValueError(f"Brief wizard invalide: {', '.join(errors)}")
    slug = brief_data["client"]["slug"]
    client_dir = CLIENTS_DIR / slug
    client_dir.mkdir(parents=True, exist_ok=True)
    (client_dir / "tooling").mkdir(exist_ok=True)
    (client_dir / "site").mkdir(exist_ok=True)

    # Ajouter la mission au brief
    brief_data["mission"] = {
        "mode": mode,
        "phases": PHASES_MAP[mode],
    }

    brief_path = client_dir / "brief-client.json"
    brief_path.write_text(
        json.dumps(brief_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    say(f"[green]✓[/] Brief wizard généré : {brief_path}")
    return client_dir


def load_runtime_brief(brief_path: Path, mode: str | None = None) -> dict:
    """Charge, normalise et valide un brief avant exécution."""
    brief_data = json.loads(brief_path.read_text())
    normalized = normalize_brief(brief_data, mode=mode)
    errors = validate_brief(normalized)
    if errors:
        raise ValueError(f"Brief invalide ({brief_path}): {', '.join(errors)}")
    return normalized


def _format_color_directive(color_overrides: dict[str, str]) -> str:
    """Format color overrides into a prompt directive for the LLM agent.

    Args:
        color_overrides: Dict mapping role names to hex values,
                         e.g. {"primary": "#1A2B3C", "accent": "#FFD700"}

    Returns:
        A prompt block that constrains the agent to use these exact colors.
    """
    lines = [
        "\n# 🎨 PALETTE IMPOSÉE — Couleurs obligatoires",
        "Les couleurs ci-dessous sont des ORDRES du client, pas des suggestions.",
        "Tu DOIS utiliser ces valeurs hex EXACTES dans brand-identity, design-tokens,",
        "tailwind.config et tous les composants. Ne jamais les modifier ni les remplacer.",
        "Les rôles non listés restent à ta discrétion (cohérents avec la palette imposée).",
        "",
        "| Rôle | Hex | CSS Variable | Tailwind |",
        "|------|-----|-------------|----------|",
    ]
    for role, hex_val in color_overrides.items():
        css_var = f"--color-{role}"
        tw_class = role
        lines.append(f"| {role} | {hex_val} | {css_var} | {tw_class} |")
    lines.append("")
    return "\n".join(lines)


def _format_mode_intake_directive(brief: dict | None, phase: str) -> str | None:
    """Résume mission.intake et impose les règles de travail liées au mode."""
    if not brief:
        return None

    mission = brief.get("mission", {}) if isinstance(brief.get("mission"), dict) else {}
    intake = mission.get("intake", {}) if isinstance(mission.get("intake"), dict) else {}
    mode = mission.get("mode") or brief.get("_meta", {}).get("mode")
    if not intake and not mode:
        return None

    lines = ["# CADRAGE MÉTIER PRIORITAIRE"]
    if mode:
        lines.append(f"Mode NEXOS: {mode}")

    preferred_keys = [
        ("business_goal", "Objectif business"),
        ("primary_cta", "CTA principal"),
        ("success_metric", "Indicateur de succès"),
        ("content_readiness", "État des contenus"),
        ("delivery_window", "Délai cible"),
        ("existing_url", "URL de référence"),
        ("audit_scope", "Périmètre audit"),
        ("audit_goal", "Question d'audit"),
        ("requested_changes", "Changements demandés"),
        ("sections_in_scope", "Sections en scope"),
        ("must_preserve", "À préserver"),
        ("target_pages", "Pages ciblées"),
        ("content_goal", "Objectif éditorial"),
        ("tone", "Ton souhaité"),
        ("source_materials", "Matière source"),
        ("analysis_questions", "Questions d'analyse"),
        ("geography", "Zone géographique"),
        ("expected_output", "Sortie attendue"),
    ]
    for key, label in preferred_keys:
        value = intake.get(key)
        if value:
            if isinstance(value, list):
                value = ", ".join(str(item) for item in value)
            lines.append(f"- {label}: {value}")

    mode_rules = {
        "create": [
            "Traite ce travail comme une création from scratch orientée résultat business.",
            "Priorise le CTA principal, la clarté de l'offre et l'indicateur de succès du client.",
        ],
        "audit": [
            "Ne propose pas un rebuild générique: réponds d'abord à la question d'audit et au périmètre demandé.",
            "Distingue clairement constats, preuves, risques et priorités d'action.",
        ],
        "modify": [
            "Travaille comme une intervention ciblée sur un existant, pas comme une refonte totale.",
            "Respecte strictement les sections en scope et les éléments à préserver.",
        ],
        "content": [
            "Produis le contenu en fonction des pages ciblées, du ton souhaité et de la matière source disponible.",
            "Ne dérive pas vers des décisions design ou build non nécessaires à la mission éditoriale.",
        ],
        "analyze": [
            "Cadre l'analyse autour des questions de recherche demandées et de la zone géographique ciblée.",
            "La sortie doit correspondre explicitement au format attendu par le client.",
        ],
    }
    for rule in mode_rules.get(mode, []):
        lines.append(f"- {rule}")

    phase_rules = {
        "ph0-discovery": "Utilise ce cadrage pour orienter la découverte et éviter les analyses hors sujet.",
        "ph1-strategy": "Les décisions stratégiques doivent découler du cadrage métier ci-dessus.",
        "ph2-design": "Les choix de design doivent servir l'objectif business et le CTA, pas une esthétique arbitraire.",
        "ph3-content": "Le contenu doit rester aligné au ton, aux pages ciblées et au but métier.",
        "ph4-build": "Le build doit respecter le scope réel de la mission et éviter les ajouts hors mandat.",
        "ph5-qa": "Évalue la qualité par rapport au cadrage demandé, pas seulement selon une checklist générique.",
        "site-update": "N'interviens que sur le périmètre demandé; le reste du site est présumé stable.",
    }
    if phase in phase_rules:
        lines.append(f"- {phase_rules[phase]}")

    return "\n".join(lines)


def _normalize_text_for_match(text: str) -> str:
    """Normalise un texte pour matching tolérant aux accents/casse."""
    normalized = unicodedata.normalize("NFD", text.lower())
    normalized = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", normalized).strip()


def _extract_intake_signals(intake: dict) -> list[tuple[str, list[str]]]:
    """Extrait des signaux textuels qui doivent apparaître dans le rapport."""
    keys = {
        "audit_goal": "question d'audit",
        "requested_changes": "changements demandés",
        "must_preserve": "éléments à préserver",
        "content_goal": "objectif éditorial",
        "tone": "ton souhaité",
        "analysis_questions": "questions d'analyse",
        "expected_output": "sortie attendue",
        "business_goal": "objectif business",
        "primary_cta": "cta principal",
    }
    signals: list[tuple[str, list[str]]] = []
    for key, label in keys.items():
        value = intake.get(key)
        if not value:
            continue
        if isinstance(value, list):
            text = " ".join(str(item) for item in value)
        else:
            text = str(value)
        words = [word for word in _normalize_text_for_match(text).split() if len(word) >= 4]
        if words:
            signals.append((label, words[:4]))
    return signals


def _validate_phase_against_intake(phase: str, content: str, brief: dict | None) -> list[str]:
    """Détecte les rapports qui ignorent le cadrage de mission."""
    if not brief:
        return []
    mission = brief.get("mission", {}) if isinstance(brief.get("mission"), dict) else {}
    intake = mission.get("intake", {}) if isinstance(mission.get("intake"), dict) else {}
    if not intake:
        return []

    content_norm = _normalize_text_for_match(content)
    issues: list[str] = []

    # Soft requirement: at least some core intake signals are acknowledged in report text.
    matched_signal = False
    for label, words in _extract_intake_signals(intake):
        if any(word in content_norm for word in words):
            matched_signal = True
        else:
            issues.append(f"rapport ne reprend pas le cadrage '{label}'")

    # Mode/phase-specific hard guards.
    mode = mission.get("mode") or brief.get("_meta", {}).get("mode")
    if mode == "modify" and phase == "site-update":
        scope = intake.get("sections_in_scope")
        if scope:
            scope_words = [w for w in _normalize_text_for_match(str(scope)).split() if len(w) >= 4]
            if scope_words and not any(word in content_norm for word in scope_words):
                issues.append("rapport modify ne mentionne pas les sections en scope")
    if mode == "audit" and phase == "ph5-qa":
        scope = intake.get("audit_scope")
        if isinstance(scope, list):
            if not any(_normalize_text_for_match(str(item)) in content_norm for item in scope):
                issues.append("rapport audit ne mentionne pas le périmètre demandé")
    if mode == "content" and phase == "ph3-content":
        target_pages = intake.get("target_pages")
        if target_pages:
            page_words = [w for w in _normalize_text_for_match(str(target_pages)).split() if len(w) >= 4]
            if page_words and not any(word in content_norm for word in page_words):
                issues.append("rapport content ne mentionne pas les pages ciblées")

    if not matched_signal and _extract_intake_signals(intake):
        issues.append("rapport semble générique par rapport au cadrage mission.intake")

    # Keep signal, but avoid overwhelming duplicates.
    deduped: list[str] = []
    for issue in issues:
        if issue not in deduped:
            deduped.append(issue)
    return deduped


def build_phase_prompt(phase: str, client_dir: Path, stack: str = "nextjs", site_type: str = "vitrine",
                       target_sections: list[str] | None = None,
                       color_overrides: dict[str, str] | None = None) -> str:
    """Construit le prompt pour une phase avec contexte cumulatif."""
    parts = []

    # 1. Agent directive
    agent_path = AGENTS_DIR / phase / "_orchestrator.md"
    if phase == "site-update":
        agent_path = AGENTS_DIR / "site-update" / "_pipeline.md"
    parts.append(f"Lis {agent_path} et adopte le rôle décrit.")

    # 1b. Agent filtering (v4.0) — inject filtered agent list into prompt
    if _NEXOS_V4 and phase not in ("site-update",):
        try:
            from nexos.agent_registry import AgentRegistry
            registry = AgentRegistry(AGENTS_DIR)
            agents = registry.get_agents_for_phase(phase, site_type=site_type, stack=stack)
            if agents:
                agent_list = "\n".join(
                    f"  - {a.id} ({a.path.name}) [priority={a.priority}]"
                    for a in agents
                )
                parts.append(
                    f"\n# Agents filtrés (stack={stack}, type={site_type}) :\n{agent_list}\n"
                    f"Exécute CHAQUE agent listé ci-dessus."
                )
        except Exception:
            pass  # Fallback silencieux

    # 1c. Section manifest — inject section context into prompt
    manifest_path = client_dir / "section-manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            all_sections = manifest.get("sections", [])
            section_count = manifest.get("total_sections", 0)

            # Targeted sections: filter and enrich
            if target_sections:
                target_ids = set(target_sections)
                filtered = [s for s in all_sections if s["id"] in target_ids]
                targeted_details = []
                for s in filtered:
                    targeted_details.append(
                        f"  {s['id']} | page={s['page']} | name={s['name']} | "
                        f"component={s.get('component_name', '?')} | "
                        f"i18n={s.get('i18n_namespace', '?')} | "
                        f"description={s.get('description', '')}"
                    )
                if targeted_details:
                    parts.append(
                        f"\n# MODIFICATIONS CIBLÉES — Sections S-NNN\n"
                        f"⚠ Ne modifier QUE les sections suivantes (sur {section_count} total) :\n"
                        + "\n".join(targeted_details)
                        + f"\n\nLe fichier section-manifest.json dans {client_dir} contient les détails complets. Lis-le.\n"
                    )
            else:
                sections_summary = []
                for s in all_sections:
                    sections_summary.append(
                        f"  {s['id']} | {s['page']}.{s['name']} | {s['status']} | {s.get('component_name', '?')}"
                    )
                if sections_summary:
                    parts.append(
                        f"\n# Section Manifest ({section_count} sections) :\n"
                        f"Le fichier section-manifest.json dans {client_dir} contient le registre "
                        f"de toutes les sections. Lis-le.\nResume :\n"
                        + "\n".join(sections_summary[:30])
                        + "\n"
                    )
        except (json.JSONDecodeError, KeyError):
            pass

    # 1d. Color overrides — inject color palette directive into prompt
    if color_overrides:
        parts.append(_format_color_directive(color_overrides))

    # 2. Brief client
    brief_path = client_dir / "brief-client.json"
    parts.append(f"Le brief client est dans {brief_path}. Lis-le.")
    if brief_path.exists():
        try:
            brief_data = load_runtime_brief(brief_path)
            intake_directive = _format_mode_intake_directive(brief_data, phase)
            if intake_directive:
                parts.append(intake_directive)
        except Exception:
            pass

    # 3. Feed des phases précédentes
    phase_reports = {
        "ph0-discovery": [],
        "ph1-strategy":  ["ph0-discovery-report.md"],
        "ph2-design":    ["ph0-discovery-report.md", "ph1-strategy-report.md"],
        "ph3-content":   ["ph0-discovery-report.md", "ph1-strategy-report.md", "ph2-design-report.md"],
        "ph4-build":     ["ph1-strategy-report.md", "ph2-design-report.md", "ph3-content-report.md"],
        "ph5-qa":        ["ph4-build-log.md"],
    }

    for report_name in phase_reports.get(phase, []):
        report_path = client_dir / report_name
        if report_path.exists():
            parts.append(f"Lis {report_path} pour le contexte de la phase précédente.")

    # 4. Tooling data (pour ph5 uniquement)
    if phase == "ph5-qa":
        tooling_dir = client_dir / "tooling"
        if tooling_dir.exists() and any(tooling_dir.iterdir()):
            parts.append(
                f"Les résultats de tooling réel sont dans {tooling_dir}/. "
                f"Lis CHAQUE fichier JSON. Ce sont des MESURES RÉELLES, "
                f"pas des estimations. Base ton audit sur ces données."
            )

    # 5. Output
    output_map = {
        "ph0-discovery": "ph0-discovery-report.md",
        "ph1-strategy":  "ph1-strategy-report.md",
        "ph2-design":    "ph2-design-report.md",
        "ph3-content":   "ph3-content-report.md",
        "ph4-build":     "ph4-build-log.md",
        "ph5-qa":        "ph5-qa-report.md",
        "site-update":   "site-update-report.md",
    }
    output_file = output_map.get(phase, f"{phase}-report.md")
    parts.append(f"Écris ton rapport dans {client_dir / output_file}")

    return "\n".join(parts)


def run_preflight_tooling(client_dir: Path, url: str) -> bool:
    """Exécute les outils CLI de mesure AVANT les agents LLM."""
    say("\n[bold cyan]⚡ TOOLING PREFLIGHT[/]")

    preflight_script = TOOLS_DIR / "preflight.sh"
    if not preflight_script.exists():
        say("[yellow]⚠ tools/preflight.sh non trouvé — skip tooling[/]")
        return True

    try:
        result = subprocess.run(
            ["bash", str(preflight_script), url, str(client_dir)],
            cwd=str(NEXOS_ROOT),
            timeout=120,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            say("[green]✓[/] Tooling preflight terminé")
        else:
            say(f"[yellow]⚠[/] Tooling preflight partiel (code {result.returncode})")
            if result.stderr:
                say(f"[dim]{result.stderr[:500]}[/]")
        return True
    except subprocess.TimeoutExpired:
        say("[yellow]⚠ Tooling timeout (120s) — skip[/]")
        return True
    except Exception as e:
        say(f"[red]✗ Tooling error: {e}[/]")
        return True  # Non-bloquant


def run_soic_gate(phase: str, client_dir: Path, profile=None) -> tuple[bool, float]:
    """Exécute le quality gate SOIC pour une phase."""
    from soic.gate import evaluate_gate

    p = profile or _get_default_profile()
    threshold = p.config.phase_thresholds.get(phase)
    if threshold is None:
        # Phase 4 = BUILD PASS (binaire)
        build_log = client_dir / "ph4-build-log.md"
        if build_log.exists():
            content = build_log.read_text()
            passed = "BUILD PASS" in content or "build réussi" in content.lower()
            return passed, 10.0 if passed else 0.0
        return True, 10.0  # Assume pass si pas de log

    try:
        mu = evaluate_gate(phase, client_dir)
        passed = mu >= threshold
        return passed, mu
    except Exception as e:
        say(f"[yellow]⚠ SOIC gate error: {e} — FAIL (score inconnu)[/]")
        return False, 0.0


_CODEX_CLI_TIMEOUT = 1800  # 30 minutes par phase


def run_codex_cli(prompt: str, cwd: str, log_path: Path) -> int:
    """Lance Codex CLI avec le prompt et capture la sortie.

    Timeout: 30 minutes par défaut pour éviter un blocage indéfini.
    """
    cmd = ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox", "-"]

    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Preserve runtime environment for Codex execution.
    env = os.environ.copy()

    process = None
    try:
        process = subprocess.Popen(
            cmd, cwd=cwd, env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
        )
        if process.stdin:
            try:
                process.stdin.write(prompt)
                process.stdin.close()
            except BrokenPipeError:
                # Process exited early; stdout/stderr will still provide context.
                pass

        deadline = time.monotonic() + _CODEX_CLI_TIMEOUT

        with open(log_path, "w", encoding="utf-8") as log:
            log.write(f"# NEXOS v3.0 Log\n")
            log.write(f"# Date: {datetime.now().isoformat()}\n")
            log.write(f"# Prompt:\n{prompt}\n\n---\n\n")

            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                # Check timeout between lines
                if time.monotonic() > deadline:
                    say(
                        f"\n[red]⚠ Codex CLI timeout ({_CODEX_CLI_TIMEOUT // 60}min) — interruption[/]"
                    )
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                    return 124  # Standard timeout exit code

        process.wait(timeout=30)
        return process.returncode

    except FileNotFoundError:
        say(
            "[red bold]Codex CLI non trouvé.[/]\n"
            "Installe-le avec: [cyan]npm install -g @openai/codex[/]"
        )
        return 1
    except KeyboardInterrupt:
        say("\n[yellow]⚠ Interrompu par l'utilisateur[/]")
        if process:
            process.terminate()
        return 130
    except subprocess.TimeoutExpired:
        say("\n[red]⚠ Codex CLI process.wait() timeout — kill[/]")
        if process:
            process.kill()
        return 124


def run_claude_cli(prompt: str, cwd: str, log_path: Path) -> int:
    """Compat shim: historical API kept for legacy imports/scripts."""
    return run_codex_cli(prompt, cwd, log_path)


# ── Preflight scan config ────────────────────────────────────────────────────

_SCAN_SCRIPTS: list[tuple[str, str, int]] = [
    # (script_name, output_filename, timeout_seconds)
    ("lighthouse-scan.sh", "lighthouse.json", 60),
    ("a11y-scan.sh", "a11y.json", 60),
    ("headers-scan.sh", "headers.json", 30),
    ("ssl-scan.sh", "ssl.json", 30),
]

_PREFLIGHT_TOTAL_TIMEOUT = 300  # 5 minutes


def _find_free_port() -> int:
    """Find a free TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def run_preflight(site_dir: Path, client_dir: Path) -> dict[str, Path]:
    """Build the site, start a local server, run scan scripts, stop the server.

    Returns a dict mapping tool names to their output JSON paths.
    Missing scripts are logged and skipped (gates will be NOT_EXECUTED).
    """
    results: dict[str, Path] = {}
    tooling_dir = client_dir / "tooling"
    tooling_dir.mkdir(exist_ok=True)

    # 1. Verify build dir
    if not (site_dir / "package.json").exists():
        say(f"[yellow]⚠ Pas de package.json dans {site_dir} — skip preflight[/]")
        return results

    # 2. Build if needed
    next_dir = site_dir / ".next"
    if not next_dir.exists():
        say("[cyan]  Building site (npm run build)...[/]")
        try:
            subprocess.run(
                ["npm", "run", "build"], cwd=str(site_dir),
                timeout=180, capture_output=True, text=True,
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            say(f"[yellow]⚠ Build failed: {e} — skip preflight[/]")
            return results

    # 3. Start local Next.js server
    port = _find_free_port()
    local_url = f"http://localhost:{port}"
    say(f"[cyan]  Starting Next.js on port {port}...[/]")
    server_proc = None
    try:
        server_proc = subprocess.Popen(
            ["npx", "next", "start", "-p", str(port)],
            cwd=str(site_dir),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            preexec_fn=os.setsid,
        )
        # Wait for server to be ready
        for _ in range(30):
            time.sleep(1)
            try:
                with socket.create_connection(("localhost", port), timeout=1):
                    break
            except OSError:
                continue
        else:
            say("[yellow]⚠ Server did not start in 30s — skip preflight[/]")
            return results

        say(f"[green]  ✓ Server ready at {local_url}[/]")

        # 4. Run scan scripts
        preflight_start = time.monotonic()
        for script_name, output_file, timeout in _SCAN_SCRIPTS:
            elapsed = time.monotonic() - preflight_start
            if elapsed >= _PREFLIGHT_TOTAL_TIMEOUT:
                say("[yellow]⚠ Preflight total timeout (5min) — stopping scans[/]")
                break

            script_path = TOOLS_DIR / script_name
            if not script_path.exists():
                say(f"[dim]  ⊘ {script_name} not found — skip[/]")
                continue

            output_path = tooling_dir / output_file
            try:
                proc = subprocess.run(
                    ["bash", str(script_path), local_url, str(tooling_dir)],
                    cwd=str(NEXOS_ROOT), timeout=timeout,
                    capture_output=True, text=True,
                )
                # Write stdout to output file if script produced output
                if proc.stdout and proc.stdout.strip():
                    output_path.write_text(proc.stdout, encoding="utf-8")
                if output_path.exists() and output_path.stat().st_size > 0:
                    results[script_name] = output_path
                    say(f"[green]  ✓ {script_name} → {output_file}[/]")
                else:
                    say(f"[yellow]  ⚠ {script_name} ran but no output[/]")
            except subprocess.TimeoutExpired:
                say(f"[yellow]  ⚠ {script_name} timeout ({timeout}s)[/]")
            except Exception as e:
                say(f"[yellow]  ⚠ {script_name} error: {e}[/]")

        # 5. Deps scan (doesn't need running server)
        deps_script = TOOLS_DIR / "deps-scan.sh"
        if deps_script.exists():
            try:
                subprocess.run(
                    ["bash", str(deps_script), str(site_dir), str(client_dir)],
                    cwd=str(NEXOS_ROOT), timeout=30,
                    capture_output=True, text=True,
                )
                deps_out = tooling_dir / "deps.json"
                if deps_out.exists():
                    results["deps-scan.sh"] = deps_out
                    say(f"[green]  ✓ deps-scan.sh → deps.json[/]")
            except Exception as e:
                say(f"[yellow]  ⚠ deps-scan.sh error: {e}[/]")

    finally:
        # 6. Kill server
        if server_proc is not None:
            try:
                os.killpg(os.getpgid(server_proc.pid), signal.SIGTERM)
                server_proc.wait(timeout=5)
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.killpg(os.getpgid(server_proc.pid), signal.SIGKILL)
                except ProcessLookupError:
                    pass
            say("[dim]  Server stopped[/]")

    say(f"[cyan]  Preflight: {len(results)}/{len(_SCAN_SCRIPTS)+1} scans completed[/]")
    return results


# ── RerunContext (CORRECTION 7) ──────────────────────────────────────────────

@dataclass
class RerunContext:
    """Encapsulates all state needed to re-run a phase with SOIC feedback.

    Replaces the closure approach for testability and robustness.
    """

    phase: str
    client_dir: Path
    site_dir: Optional[Path]
    url: Optional[str]
    timestamp: str
    stack: str = "nextjs"
    site_type: str = "vitrine"

    def rerun(self, phase: str, feedback: str, iteration: int) -> bool:
        """Re-execute the phase with SOIC feedback injected.

        Signature matches RerunCallback: (phase, feedback, iteration) -> bool.
        """
        # Re-run preflight tooling for QA phase
        if phase == "ph5-qa" and self.site_dir is not None:
            run_preflight(self.site_dir, self.client_dir)
        elif phase == "ph5-qa" and self.url:
            run_preflight_tooling(self.client_dir, self.url)

        rerun_prompt = build_phase_prompt(phase, self.client_dir, stack=self.stack, site_type=self.site_type)
        rerun_prompt += f"\n\n# SOIC FEEDBACK — Iteration {iteration + 1}\n{feedback}"
        rerun_log = LOGS_DIR / f"{self.timestamp}_{phase}_iter{iteration + 1}.log"
        return run_codex_cli(rerun_prompt, str(NEXOS_ROOT), rerun_log) == 0


KNOWLEDGE_DIR = NEXOS_ROOT / "output" / "knowledge"

OUTPUT_MAP = {
    "ph0-discovery": "ph0-discovery-report.md",
    "ph1-strategy":  "ph1-strategy-report.md",
    "ph2-design":    "ph2-design-report.md",
    "ph3-content":   "ph3-content-report.md",
    "ph4-build":     "ph4-build-log.md",
    "ph5-qa":        "ph5-qa-report.md",
    "site-update":   "site-update-report.md",
}


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

    # Check for error patterns in the first 2000 chars
    head = content[:2000]
    match = _ERROR_PATTERNS.search(head)
    if match:
        say(
            f"[red]✗ Phase {phase} rapport contient une erreur : {match.group()!r}[/]"
        )
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
        say(
            f"[red]✗ Phase {phase} rapport hors cadrage mission.intake : {intake_issues[0]}[/]"
        )
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


def run_pipeline(mode: str, client_dir: Path, url: Optional[str] = None, profile=None,
                  target_sections: list[str] | None = None,
                  color_overrides: dict[str, str] | None = None):
    """Exécute le pipeline complet pour un mode donné."""
    # Resolve phases via PipelineConfig (dynamic) or PHASES_MAP (fallback)
    brief_path = client_dir / "brief-client.json"
    brief = None
    if brief_path.exists():
        brief = load_runtime_brief(brief_path, mode=mode)

    try:
        from nexos.pipeline_config import PipelineConfig
        pipeline_cfg = PipelineConfig.from_brief(brief, mode, nexos_root=NEXOS_ROOT)
        if target_sections:
            pipeline_cfg.target_sections = target_sections
        if color_overrides:
            pipeline_cfg.color_overrides = color_overrides
        phases = pipeline_cfg.phases
    except Exception:
        pipeline_cfg = None
        phases = PHASES_MAP[mode]

    # Auto-resolve profile from pipeline stack if not provided
    if profile is None and pipeline_cfg is not None and pipeline_cfg.stack != "nextjs":
        profile = _resolve_profile(stack=pipeline_cfg.stack) or _get_default_profile()
    if profile is None:
        profile = _get_default_profile()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    gate_history = []

    # NEXOS v4.0 — Vérification tooling au démarrage
    if _NEXOS_V4:
        ensure_tooling(interactive=False)

    say(Panel(
        f"[bold]Mode:[/] {mode}\n"
        f"[bold]Client:[/] {client_dir.name}\n"
        f"[bold]Phases:[/] {' → '.join(phases)}",
        title="[bold cyan]⚡ NEXOS v4.0[/]",
        border_style="cyan",
    ))

    if _HAS_CHANGELOG:
        log_event(client_dir, EventType.PIPELINE_START, agent="orchestrator",
                  details={"mode": mode, "phases": phases})

    for i, phase in enumerate(phases):
        say(f"\n[bold]{'━'*60}[/]")
        say(f"[bold cyan]PHASE {i}: {phase.upper()}[/]")
        say(f"[bold]{'━'*60}[/]\n")

        if _HAS_CHANGELOG:
            log_event(client_dir, EventType.PHASE_START, phase=phase, agent="orchestrator")

        # Detect site directory for preflight
        site_dir = client_dir / "site"
        if not (site_dir / "package.json").exists():
            site_dir = None

        # NEXOS v4.0 — Auto-fix D4/D8 avant QA (garantir compliance)
        if phase == "ph5-qa" and _NEXOS_V4 and site_dir:
            brief_path = client_dir / "brief-client.json"
            brief = load_runtime_brief(brief_path, mode=mode) if brief_path.exists() else None
            fix_report = auto_fix(site_dir, client_dir, brief)
            if fix_report.total_fixes > 0:
                say(f"[cyan]  Auto-fix: {fix_report.total_fixes} corrections appliquées[/]")

        # Preflight tooling avant ph5
        if phase == "ph5-qa":
            say("[bold cyan]⚡ PREFLIGHT TOOLING[/]")
            if site_dir is not None:
                run_preflight(site_dir, client_dir)
            elif url:
                run_preflight_tooling(client_dir, url)
            else:
                say("[yellow]⚠ Pas de site_dir ni URL — preflight skip[/]")

        # NEXOS v4.0 — Audit Toolkit source-code scan (post-preflight)
        if phase == "ph5-qa" and _HAS_AUDIT_TOOLKIT and site_dir:
            say("[bold cyan]🔍 AUDIT TOOLKIT — Source Code Scan[/]")
            try:
                toolkit_config = _ToolkitConfig(
                    target_url=url or "",
                    source_path=str(site_dir),
                )
                audit_report = _run_source_audit(str(site_dir), url or "", toolkit_config)
                # Save results
                tooling_dir = client_dir / "tooling"
                tooling_dir.mkdir(exist_ok=True)
                import json
                from audit_toolkit.report import generate_json
                (tooling_dir / "audit-toolkit.json").write_text(
                    json.dumps(generate_json(audit_report), indent=2, ensure_ascii=False),
                    encoding="utf-8",
                )
                say(
                    f"  μ={audit_report.composite_score}/10 | "
                    f"{audit_report.total_issues} issues | "
                    f"CRITICAL/HIGH: {len(audit_report.critical_issues)}"
                )
                dims = audit_report.to_dimension_scores()
                if dims:
                    dim_str = " ".join(f"{k}={v}" for k, v in sorted(dims.items()))
                    say(f"  Dimensions: {dim_str}")
                if _HAS_CHANGELOG:
                    log_event(client_dir, EventType.TOOLING_COMPLETE,
                              phase=phase, agent="audit_toolkit",
                              details={"composite_score": audit_report.composite_score,
                                       "total_issues": audit_report.total_issues,
                                       "dimensions": dims})
            except Exception as e:
                say(f"[yellow]⚠ Audit Toolkit error: {e}[/]")
                if _HAS_CHANGELOG:
                    log_event(client_dir, EventType.TOOLING_ERROR,
                              phase=phase, agent="audit_toolkit",
                              details={"error": str(e)})

        # Resolve stack/site_type from pipeline config
        _stack = pipeline_cfg.stack if pipeline_cfg else "nextjs"
        _site_type = pipeline_cfg.site_type if pipeline_cfg else "vitrine"

        # Construire le prompt
        prompt = build_phase_prompt(phase, client_dir, stack=_stack, site_type=_site_type,
                                    target_sections=pipeline_cfg.target_sections if pipeline_cfg else None,
                                    color_overrides=pipeline_cfg.color_overrides if pipeline_cfg else None)
        log_path = LOGS_DIR / f"{timestamp}_{phase}.log"

        # Exécuter Codex CLI
        returncode = run_codex_cli(prompt, str(NEXOS_ROOT), log_path)

        if returncode != 0:
            say(f"[red]✗ Phase {phase} échouée (code {returncode})[/]")
            if _HAS_CHANGELOG:
                log_event(client_dir, EventType.PHASE_FAIL, phase=phase, agent="orchestrator",
                          details={"returncode": returncode})
            break

        # Vérifier que l'output existe et est valide
        if phase in OUTPUT_MAP:
            if not verify_phase_output(phase, client_dir):
                say(f"[red]✗ Phase {phase} n'a pas produit de rapport valide — ARRÊT[/]")
                if _HAS_CHANGELOG:
                    log_event(client_dir, EventType.PHASE_FAIL, phase=phase, agent="orchestrator",
                              details={"reason": "missing_output"})
                break

        # Quality gate with convergence loop
        phase_thresholds = profile.config.phase_thresholds
        if phase in phase_thresholds or phase == "ph4-build":
            threshold = phase_thresholds.get(phase)

            # Phase 4 = BUILD PASS (binary check, no convergence)
            if threshold is None:
                if _NEXOS_V4 and site_dir:
                    # NEXOS v4.0 — Validation build réelle
                    from nexos.build_validator import format_build_report
                    build_result = validate_build(site_dir)
                    build_ok = build_result.overall_pass
                    if not build_ok:
                        # Tenter auto-fix puis re-valider
                        say("[cyan]  Build FAIL — tentative auto-fix...[/]")
                        brief_path = client_dir / "brief-client.json"
                        brief = load_runtime_brief(brief_path, mode=mode) if brief_path.exists() else None
                        fix_report = auto_fix(site_dir, client_dir, brief)
                        say(f"[cyan]  Auto-fix: {fix_report.total_fixes} corrections[/]")
                        if _HAS_CHANGELOG:
                            log_event(client_dir, EventType.AUTOFIX_END, phase=phase,
                                      agent="auto_fixer", details=_fix_report_to_dict(fix_report))
                        build_result = validate_build(site_dir)
                        build_ok = build_result.overall_pass
                    say(format_build_report(build_result))
                    if _HAS_CHANGELOG:
                        evt = EventType.BUILD_PASS if build_ok else EventType.BUILD_FAIL
                        log_event(client_dir, evt, phase=phase, agent="build_validator")
                else:
                    # Fallback v3.0 — vérification textuelle
                    build_log = client_dir / "ph4-build-log.md"
                    if build_log.exists():
                        content = build_log.read_text()
                        build_ok = "BUILD PASS" in content or "build réussi" in content.lower()
                    else:
                        build_ok = True
                gate_history.append({
                    "phase": phase, "mu": 10.0 if build_ok else 0.0,
                    "threshold": "BUILD_PASS", "converged": build_ok,
                    "iterations": 1, "decision": "ACCEPT" if build_ok else "FAIL",
                    "timestamp": datetime.now().isoformat(),
                })
                if not build_ok:
                    say(f"[red]✗ BUILD FAIL — ARRÊT[/]")
                    break
                say(f"[green]✓ BUILD PASS[/]")
                continue

            # Convergence loop via PhaseIterator
            from soic.iterator import PhaseIterator
            from soic.persistence import RunStore

            store = RunStore(client_dir)
            iterator = PhaseIterator(
                phase=phase, client_dir=str(client_dir),
                max_iter=4, store=store, site_dir=str(site_dir) if site_dir else None,
                profile=profile,
            )

            ctx = RerunContext(
                phase=phase,
                client_dir=client_dir,
                site_dir=site_dir,
                url=url,
                timestamp=timestamp,
                stack=_stack,
                site_type=_site_type,
            )

            def _on_iteration(iteration: int, result) -> None:
                """Display iteration progress."""
                decision = result.decision.value
                mu = result.report.mu
                cov = result.report.coverage
                say(
                    f"  [bold]Iteration {iteration}:[/] μ={mu:.2f} "
                    f"(coverage={cov:.0%}) → {decision}"
                )

            say(f"\n[bold cyan]🔄 SOIC Convergence Loop ({phase})[/]")
            loop = iterator.run(rerun_phase=ctx.rerun, on_iteration=_on_iteration)

            gate_history.append({
                "phase": phase,
                "mu": loop.final_mu,
                "threshold": threshold,
                "converged": loop.converged,
                "iterations": loop.total_iterations,
                "decision": loop.final_decision.value,
                "abort_reason": loop.abort_reason,
                "timestamp": datetime.now().isoformat(),
            })

            if _HAS_CHANGELOG:
                gate_evt = EventType.SOIC_GATE_PASS if loop.converged else EventType.SOIC_GATE_FAIL
                log_event(client_dir, gate_evt, phase=phase, agent="soic",
                          details={"mu": loop.final_mu, "threshold": threshold,
                                   "iterations": loop.total_iterations})

            if loop.converged:
                say(
                    f"[green]✓ SOIC GATE: μ={loop.final_mu:.2f} ≥ {threshold} "
                    f"— ACCEPT ({loop.total_iterations} iter)[/]"
                )
            else:
                say(
                    f"[red]✗ SOIC GATE: μ={loop.final_mu:.2f} < {threshold} "
                    f"— {loop.final_decision.value} ({loop.total_iterations} iter)[/]"
                )
                if loop.abort_reason:
                    say(f"[red]  Raison: {loop.abort_reason}[/]")
                break

    # Sauvegarder l'historique des gates (enrichi avec convergence)
    gates_path = client_dir / "soic-gates.json"
    gates_path.write_text(json.dumps(gate_history, indent=2), encoding="utf-8")

    if _HAS_CHANGELOG:
        log_event(client_dir, EventType.PIPELINE_END, agent="orchestrator",
                  details={"gates": len(gate_history), "mode": mode})

    say(Panel(
        f"[green]Pipeline terminé[/]\n"
        f"[dim]Client: {client_dir}[/]\n"
        f"[dim]Gates: {len(gate_history)} évaluées[/]",
        title="[bold green]✓ NEXOS v3.0 TERMINÉ[/]",
        border_style="green",
    ))


# ── Converge mode ────────────────────────────────────────────────────────────

def run_converge(
    client_dir: Path,
    target: float = 8.5,
    max_iter: int = 4,
    timeout_minutes: int = 15,
    url: Optional[str] = None,
    dry_run: bool = False,
    profile=None,
) -> None:
    """Run the SOIC convergence loop on an existing client directory.

    Default: full autonomous loop — evaluate → correct → re-evaluate → repeat.
    With --dry-run: evaluate once, produce report + corrective plan, touch nothing.
    """
    from soic import GateEngine, PhaseIterator, Converger, FeedbackRouter
    from soic.persistence import RunStore
    from soic.report import generate_report_v2

    if profile is None:
        profile = _get_default_profile()

    phase = "ph5-qa"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Create a profile copy with overridden threshold (immutable)
    converge_profile = type(profile)(
        name=f"{profile.name}@converge",
        config=profile.config.with_threshold(phase, target),
        parent=profile,
    )

    # Detect site directory
    site_dir = client_dir
    if (client_dir / "site" / "package.json").exists():
        site_dir = client_dir / "site"
    elif not (client_dir / "package.json").exists():
        site_dir = None

    say(Panel(
        f"[bold]Mode:[/] converge\n"
        f"[bold]Client:[/] {client_dir.name}\n"
        f"[bold]Target:[/] μ ≥ {target}\n"
        f"[bold]Max iterations:[/] {max_iter}\n"
        f"[bold]Timeout:[/] {timeout_minutes}min\n"
        f"[bold]Mode:[/] {'DRY-RUN (evaluate only)' if dry_run else 'AUTONOMOUS (correct + re-evaluate)'}",
        title="[bold cyan]🔄 NEXOS SOIC Convergence[/]",
        border_style="cyan",
    ))

    if dry_run:
        # ── Single evaluation mode ──────────────────────────────────────────
        say(f"\n[bold cyan]⚡ Evaluation SOIC — {phase}[/]\n")

        # Preflight if site available
        if site_dir is not None and (site_dir / "package.json").exists():
            say("[bold cyan]⚡ PREFLIGHT TOOLING[/]")
            run_preflight(site_dir, client_dir)
        elif url:
            say("[bold cyan]⚡ PREFLIGHT TOOLING (URL)[/]")
            run_preflight_tooling(client_dir, url)

        engine = GateEngine(
            phase=phase,
            client_dir=str(client_dir),
            site_dir=str(site_dir) if site_dir else str(client_dir),
            profile=converge_profile,
        )
        report = engine.run_all_gates(iteration=1)

        # Report
        report_txt = generate_report_v2(report, config=converge_profile.config)
        say(report_txt)

        # Save report
        report_path = client_dir / "soic-converge-report.txt"
        report_path.write_text(report_txt, encoding="utf-8")

        # Feedback
        router = FeedbackRouter(config=converge_profile.config)
        if report.fail_count > 0:
            feedback = router.generate(report)
            say(f"\n[bold yellow]{'━'*60}[/]")
            say("[bold yellow]PLAN DE CONVERGENCE[/]")
            say(f"[bold yellow]{'━'*60}[/]\n")
            say(feedback)

            full_feedback = router.generate_full(report)
            feedback_path = client_dir / "soic-converge-feedback.md"
            feedback_path.write_text(full_feedback, encoding="utf-8")
            say(f"\n[dim]Feedback complet sauvegardé: {feedback_path}[/]")

        # Convergence assessment
        converger = Converger(phase=phase, max_iter=max_iter, config=converge_profile.config)
        decision = converger.decide(report, iteration=1)
        summary = converger.get_summary(decision, iteration=1)

        say(f"\n[bold]{'━'*60}[/]")
        if decision.value == "ACCEPT":
            say(
                f"[bold green]✓ CONVERGED — μ={report.mu:.2f} ≥ {target}[/]\n"
                f"[green]{summary}[/]"
            )
        else:
            delta = target - report.mu
            say(
                f"[bold red]✗ NOT CONVERGED — μ={report.mu:.2f} < {target} (Δ={delta:.2f})[/]\n"
                f"[red]{summary}[/]"
            )
            say(
                f"\n[dim]Pour lancer la correction automatique :[/]\n"
                f"[cyan]  nexos converge {client_dir} --target {target} "
                f"--max-iter {max_iter} --timeout {timeout_minutes}[/]"
            )
        say(f"[bold]{'━'*60}[/]")

        # Save to persistence
        store = RunStore(client_dir)
        store.save_run(report)

    else:
        # ── Full convergence loop with Codex CLI rerun ─────────────────────
        store = RunStore(client_dir)
        iterator = PhaseIterator(
            phase=phase,
            client_dir=str(client_dir),
            max_iter=max_iter,
            store=store,
            site_dir=str(site_dir) if site_dir else None,
            timeout_minutes=timeout_minutes,
            profile=converge_profile,
        )

        ctx = RerunContext(
            phase=phase,
            client_dir=client_dir,
            site_dir=site_dir,
            url=url,
            timestamp=timestamp,
        )

        def _on_iteration(iteration: int, result) -> None:
            mu = result.report.mu
            cov = result.report.coverage
            dec = result.decision.value
            dur = result.duration_s
            say(
                f"  [bold]Iteration {iteration}:[/] μ={mu:.2f} "
                f"(coverage={cov:.0%}, {dur:.0f}s) → {dec}"
            )
            if result.feedback and dec == "ITERATE":
                for line in result.feedback.split("\n")[:5]:
                    if line.strip():
                        say(f"    [dim]{line}[/]")

        say(f"\n[bold cyan]🔄 Convergence Loop — target μ ≥ {target}[/]\n")
        loop = iterator.run(rerun_phase=ctx.rerun, on_iteration=_on_iteration)

        # Final report
        if loop.iterations:
            last_report = loop.iterations[-1].report
            report_txt = generate_report_v2(last_report, config=converge_profile.config)
            report_path = client_dir / "soic-converge-report.txt"
            report_path.write_text(report_txt, encoding="utf-8")

        say(f"\n[bold]{'━'*60}[/]")
        if loop.converged:
            say(
                f"[bold green]✓ CONVERGED — μ={loop.final_mu:.2f} ≥ {target} "
                f"in {loop.total_iterations} iteration(s)[/]"
            )
        else:
            say(
                f"[bold red]✗ NOT CONVERGED — μ={loop.final_mu:.2f} < {target} "
                f"after {loop.total_iterations} iteration(s)[/]\n"
                f"[red]  Reason: {loop.abort_reason or loop.final_decision.value}[/]"
            )
        say(f"[bold]{'━'*60}[/]")

    # No threshold restore needed — converge_profile is an immutable copy


# ── Knowledge agents ─────────────────────────────────────────────────────────

VALID_TYPES = ("dev-perso", "technique", "fiction", "academique", "business", "philosophie")
VALID_OBJECTIFS = ("appliquer", "partager", "memoriser", "decider")
VALID_NIVEAUX = ("express", "complet", "approfondi")


def run_knowledge_agent(
    agent_id: str,
    source: str,
    content_type: str = "technique",
    objectif: str = "appliquer",
    niveau: str = "complet",
    score_only: Optional[Path] = None,
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
            verdict_style = "green" if result.mu >= 7.5 else ("yellow" if result.mu >= 6.0 else "red")
            table.add_row("[bold]μ pondéré[/]", "", f"[bold {verdict_style}]{result.mu:.2f}/10 — {result.verdict}[/]")
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

    # Lire le template de l'agent
    agent_path = AGENTS_DIR / "knowledge" / "hexabrief.md"
    if not agent_path.exists():
        say(f"[red]✗ Agent introuvable: {agent_path}[/]")
        return

    # Construire le prompt
    prompt_parts = [
        f"Lis {agent_path} et adopte le rôle décrit.",
        f"",
        f"PARAMETRES:",
        f"  TEXTE_OU_REFERENCE: {source}",
        f"  TYPE: {content_type}",
        f"  OBJECTIF: {objectif}",
        f"  NIVEAU: {niveau}",
        f"",
        f"TEMPLATE DE SORTIE: Lis {NEXOS_ROOT / 'templates' / 'book-summary-template.md'}",
        f"Remplis TOUS les placeholders {{{{...}}}} avec du contenu réel.",
        f"Ne laisse AUCUN placeholder non rempli.",
        f"",
        f"Écris le résumé complet dans {output_path}",
    ]
    prompt = "\n".join(prompt_parts)

    say(Panel(
        f"[bold]Agent:[/] HexaBrief Book Summarizer\n"
        f"[bold]Source:[/] {source}\n"
        f"[bold]Type:[/] {content_type} | [bold]Objectif:[/] {objectif} | [bold]Niveau:[/] {niveau}\n"
        f"[bold]Output:[/] {output_path}",
        title="[bold cyan]📚 NEXOS Knowledge — HexaBrief[/]",
        border_style="cyan",
    ))

    # Exécuter Codex CLI
    log_path = LOGS_DIR / f"{timestamp}_hexabrief_{source_slug}.log"
    returncode = run_codex_cli(prompt, str(NEXOS_ROOT), log_path)

    if returncode != 0:
        say(f"[red]✗ HexaBrief échoué (code {returncode})[/]")
        return

    # Vérifier l'output
    if not output_path.exists() or output_path.stat().st_size < 200:
        say(f"[red]✗ Résumé non généré ou trop court[/]")
        return

    say(f"[green]✓ Résumé généré: {output_path}[/]")

    # Auto-scoring
    say(f"\n[bold cyan]📊 Auto-scoring HexaBrief...[/]\n")
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
        table.add_row("[bold]μ pondéré[/]", "", f"[bold {verdict_style}]{result.mu:.2f}/10 — {result.verdict}[/]")
        say(table)

        if result.verdict == "REJECT":
            say("[red]⚠ Le résumé ne passe pas le seuil minimum. Relancer avec un niveau plus élevé.[/]")
        elif result.verdict == "REVISE":
            say("[yellow]⚠ Le résumé nécessite des corrections. Vérifier les sections faibles.[/]")
    except ImportError:
        say("[yellow]⚠ Module scoring non disponible — skip auto-scoring[/]")
    except Exception as e:
        say(f"[yellow]⚠ Scoring error: {e}[/]")


# ── Entry point ──────────────────────────────────────────────────────────────
def _print_banner():
    from rich.console import Console
    from rich.text import Text
    from rich.panel import Panel
    from rich.columns import Columns
    from rich import box
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

    _con.print(Panel(
        combined,
        border_style="yellow",
        box=box.DOUBLE_EDGE,
        padding=(0, 2),
    ))
    _con.print()


def main(argv: list[str] | None = None) -> int:
    """NEXOS orchestrator entry point.

    Accepts an optional argv list (defaults to sys.argv[1:]) and returns the
    process exit code. Extracted from the legacy `if __name__ == "__main__":`
    block so that `nexos_cli.py` can import and call it without exec().
    """
    _print_banner()
    import argparse

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
    sp_session.add_argument("--host", choices=["codex", "claude", "gemini"],
                            help="CLI hôte à lancer explicitement")
    sp_session.add_argument("--print-prompt", action="store_true",
                            help="Afficher uniquement le prompt bootstrap")

    # Pipeline modes
    for mode in ["create", "audit", "modify", "content", "analyze"]:
        sp = subparsers.add_parser(mode)
        sp.add_argument("--client-dir", type=Path, help="Dossier client existant")
        sp.add_argument("--url", type=str, help="URL du site (pour audit/preflight)")
        sp.add_argument("--brief", type=str, help="Chemin vers brief-client.json")
        sp.add_argument("--name", type=str, help="Nom du client (pour génération rapide)")
        sp.add_argument("-i", "--interactive", action="store_true",
                        help="Lancer le wizard interactif pour générer le brief")
        sp.add_argument("--stack", choices=["nextjs", "nuxt", "astro", "fastapi", "generic"],
                        help="Stack technique (résout le profil SOIC automatiquement)")
        sp.add_argument("--profile", type=str, help="Profil SOIC (ex: web-nextjs, api-fastapi)")
        sp.add_argument("--colors", nargs="*", metavar="ROLE=#HEX",
                        help="Palette couleurs (ex: primary=#1A2B3C accent=#FFD700)")
        if mode == "modify":
            sp.add_argument("--section", nargs="*", metavar="S-NNN",
                            help="Sections ciblées par ID (ex: S-001 S-003)")

    # Knowledge mode
    sp_know = subparsers.add_parser(
        "knowledge",
        help="Agents cognitifs (résumé, analyse, synthèse)",
        description="Exécute un agent knowledge NEXOS (hors pipeline web).",
    )
    sp_know.add_argument("agent", type=str, help="ID de l'agent (ex: hexabrief)")
    sp_know.add_argument("--source", type=str, required=True,
                         help="Texte source ou 'Titre — Auteur'")
    sp_know.add_argument("--type", type=str, default="technique",
                         choices=VALID_TYPES, dest="content_type",
                         help="Type de contenu (défaut: technique)")
    sp_know.add_argument("--objectif", type=str, default="appliquer",
                         choices=VALID_OBJECTIFS,
                         help="Objectif de lecture (défaut: appliquer)")
    sp_know.add_argument("--niveau", type=str, default="complet",
                         choices=VALID_NIVEAUX,
                         help="Profondeur du résumé (défaut: complet)")
    sp_know.add_argument("--score-only", type=Path, default=None,
                         help="Évaluer un résumé existant (path vers .md)")

    # Converge mode
    sp_conv = subparsers.add_parser(
        "converge",
        help="Boucle de convergence SOIC",
        description="Évalue un client via SOIC et produit un plan de convergence.",
    )
    sp_conv.add_argument("client_dir", type=Path, help="Dossier client à évaluer")
    sp_conv.add_argument("--target", type=float, default=8.5, help="Score μ cible (défaut: 8.5)")
    sp_conv.add_argument("--max-iter", type=int, default=4, help="Itérations max (défaut: 4)")
    sp_conv.add_argument("--timeout", type=int, default=15, help="Timeout global en minutes (défaut: 15)")
    sp_conv.add_argument("--url", type=str, help="URL du site (pour preflight)")
    sp_conv.add_argument("--dry-run", action="store_true", help="Évaluer sans corriger (rapport uniquement)")
    sp_conv.add_argument("--stack", choices=["nextjs", "nuxt", "astro", "fastapi", "generic"],
                         help="Stack technique (résout le profil SOIC automatiquement)")
    sp_conv.add_argument("--profile", type=str, help="Profil SOIC (ex: web-nextjs, api-fastapi)")

    # NEXOS v4.0 — Doctor
    subparsers.add_parser("doctor", help="Diagnostic système (outils, templates, SOIC)")

    # NEXOS v4.0 — Fix
    sp_fix = subparsers.add_parser("fix", help="Auto-correction D4/D8 sur un client")
    sp_fix.add_argument("client_dir", type=Path, help="Dossier client à corriger")
    sp_fix.add_argument("--dry-run", action="store_true", help="Analyser sans appliquer")

    # NEXOS v4.0 — Report
    sp_report = subparsers.add_parser("report", help="Rapport agrégé d'un client")
    sp_report.add_argument("client_dir", type=Path, help="Dossier client à analyser")

    args = parser.parse_args(argv)

    if not args.mode:
        from nexos.session_launcher import launch_session
        return int(launch_session(NEXOS_ROOT) or 0)

    if args.mode == "session":
        from nexos.session_launcher import launch_session
        return int(launch_session(
            NEXOS_ROOT,
            explicit_host=args.host,
            print_prompt_only=args.print_prompt,
        ) or 0)

    # NEXOS v4.0 — commandes standalone
    if args.mode == "doctor":
        if _NEXOS_V4:
            from nexos.cli_commands import run_doctor
            run_doctor()
        else:
            say("[red]nexos doctor requiert les modules v4.0 (nexos/)[/]")
        return 0
    elif args.mode == "fix":
        if _NEXOS_V4:
            from nexos.cli_commands import run_fix
            run_fix(args.client_dir, dry_run=args.dry_run)
        else:
            say("[red]nexos fix requiert les modules v4.0 (nexos/)[/]")
        return 0
    elif args.mode == "report":
        if _NEXOS_V4:
            from nexos.cli_commands import run_report
            run_report(args.client_dir)
        else:
            say("[red]nexos report requiert les modules v4.0 (nexos/)[/]")
        return 0

    if args.mode == "knowledge":
        run_knowledge_agent(
            agent_id=args.agent,
            source=args.source,
            content_type=args.content_type,
            objectif=args.objectif,
            niveau=args.niveau,
            score_only=args.score_only,
        )
    elif args.mode == "converge":
        run_converge(
            client_dir=args.client_dir,
            target=args.target,
            max_iter=args.max_iter,
            timeout_minutes=args.timeout,
            url=args.url,
            dry_run=args.dry_run,
        )
    else:
        if hasattr(args, "client_dir") and args.client_dir:
            client_dir = args.client_dir
        elif hasattr(args, "brief") and args.brief and not getattr(args, "interactive", False):
            brief_path = Path(args.brief)
            brief_data = load_runtime_brief(brief_path, mode=args.mode)
            client_dir = generate_brief_from_wizard(args.mode, brief_data)
        elif _NEXOS_V4:
            from nexos.brief_wizard import generate_minimal_brief
            if getattr(args, "name", None):
                say(f"[cyan]ℹ Génération rapide du brief pour : {args.name}[/]")
                brief_data = generate_minimal_brief(args.name, args.mode)
                client_dir = generate_brief_from_wizard(args.mode, brief_data)
            elif getattr(args, "interactive", False) or sys.stdin.isatty():
                brief_data = interactive_brief(args.mode)
                client_dir = generate_brief_from_wizard(args.mode, brief_data)
            else:
                say("[red]Erreur: --client-dir, --brief ou --name requis (non-TTY)[/]")
                return 1
        else:
            say("[red]Erreur: --client-dir ou --brief requis[/]")
            say("[dim]Astuce : lancez nexos create en terminal pour le wizard interactif[/]")
            return 1

        # Resolve SOIC profile: --profile > --stack > brief > default
        cli_profile = _resolve_profile(
            stack=getattr(args, "stack", None),
            profile_name=getattr(args, "profile", None),
        )
        if cli_profile is None:
            brief_path = client_dir / "brief-client.json"
            if brief_path.exists():
                brief_data = load_runtime_brief(brief_path)
                brief_stack = brief_data.get("stack") or brief_data.get("site", {}).get("stack")
                if brief_stack:
                    cli_profile = _resolve_profile(stack=brief_stack)

        # Parse --colors if provided
        _raw_colors = getattr(args, "colors", None)
        _color_overrides = None
        if _raw_colors:
            from nexos.pipeline_config import parse_color_args
            try:
                _color_overrides = parse_color_args(_raw_colors)
                say(f"[cyan]🎨 Palette couleurs : {_color_overrides}[/]")
            except ValueError as e:
                say(f"[red]Erreur --colors : {e}[/]")
                return 1

        run_pipeline(args.mode, client_dir, url=getattr(args, "url", None), profile=cli_profile,
                     target_sections=getattr(args, "section", None),
                     color_overrides=_color_overrides)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
