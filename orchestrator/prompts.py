"""Construction du prompt envoyé à Codex CLI pour chaque phase.

- `build_phase_prompt()`: assemble agent + brief + feed phases précédentes + tooling.
- `_format_color_directive()`: injecte la palette imposée.
- `_format_mode_intake_directive()`: résume mission.intake + impose règles du mode.
- `_validate_phase_against_intake()`: détecte les rapports génériques.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from ._shared import _NEXOS_V4, AGENTS_DIR, say
from .brief import load_runtime_brief


def _format_color_directive(color_overrides: dict[str, str]) -> str:
    """Format color overrides into a prompt directive for the LLM agent."""
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


def _format_mode_intake_directive(
    brief: dict | None,
    phase: str,
    mode_override: str | None = None,
) -> str | None:
    """Résume mission.intake et impose les règles de travail liées au mode.

    Le `mode_override` (passé par la commande CLI via `build_phase_prompt`) est
    prioritaire sur le mode déclaré dans le brief : la commande CLI est la
    source de vérité, le brief n'est qu'une suggestion.
    """
    if not brief:
        return None

    mission = brief.get("mission", {}) if isinstance(brief.get("mission"), dict) else {}
    intake = mission.get("intake", {}) if isinstance(mission.get("intake"), dict) else {}
    mode = mode_override or mission.get("mode") or brief.get("_meta", {}).get("mode")
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

    matched_signal = False
    for label, words in _extract_intake_signals(intake):
        if any(word in content_norm for word in words):
            matched_signal = True
        else:
            issues.append(f"rapport ne reprend pas le cadrage '{label}'")

    mode = mission.get("mode") or brief.get("_meta", {}).get("mode")
    if mode == "modify" and phase == "site-update":
        scope = intake.get("sections_in_scope")
        if scope:
            scope_words = [w for w in _normalize_text_for_match(str(scope)).split() if len(w) >= 4]
            if scope_words and not any(word in content_norm for word in scope_words):
                issues.append("rapport modify ne mentionne pas les sections en scope")
    if mode == "audit" and phase == "ph5-qa":
        scope = intake.get("audit_scope")
        if isinstance(scope, list) and not any(
            _normalize_text_for_match(str(item)) in content_norm for item in scope
        ):
            issues.append("rapport audit ne mentionne pas le périmètre demandé")
    if mode == "content" and phase == "ph3-content":
        target_pages = intake.get("target_pages")
        if target_pages:
            page_words = [
                w for w in _normalize_text_for_match(str(target_pages)).split() if len(w) >= 4
            ]
            if page_words and not any(word in content_norm for word in page_words):
                issues.append("rapport content ne mentionne pas les pages ciblées")

    if not matched_signal and _extract_intake_signals(intake):
        issues.append("rapport semble générique par rapport au cadrage mission.intake")

    deduped: list[str] = []
    for issue in issues:
        if issue not in deduped:
            deduped.append(issue)
    return deduped


def build_phase_prompt(
    phase: str,
    client_dir: Path,
    stack: str = "nextjs",
    site_type: str = "vitrine",
    target_sections: list[str] | None = None,
    color_overrides: dict[str, str] | None = None,
    mode: str | None = None,
) -> str:
    """Construit le prompt pour une phase avec contexte cumulatif.

    Le paramètre `mode` reflète la commande CLI invoquée (`create` / `audit` /
    `modify` / `content` / `analyze`). S'il est fourni, il est la source de
    vérité pour le cadrage injecté dans le prompt et passe outre tout `mode`
    obsolète présent dans le brief client. S'il est `None`, le mode est lu
    depuis le brief (rétrocompatibilité avec les appels directs sans CLI).
    """
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
                    f"  - {a.id} ({a.path.name}) [priority={a.priority}]" for a in agents
                )
                parts.append(
                    f"\n# Agents filtrés (stack={stack}, type={site_type}) :\n{agent_list}\n"
                    f"Exécute CHAQUE agent listé ci-dessus."
                )
        except Exception as e:
            say(
                f"[yellow]⚠ AgentRegistry failed for {phase} ({type(e).__name__}: {e}) — prompt without agents list[/]"
            )

    # 1c. Section manifest — inject section context into prompt
    manifest_path = client_dir / "section-manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            all_sections = manifest.get("sections", [])
            section_count = manifest.get("total_sections", 0)

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
            brief_data = load_runtime_brief(brief_path, mode=mode)
            intake_directive = _format_mode_intake_directive(brief_data, phase, mode_override=mode)
            if intake_directive:
                parts.append(intake_directive)
        except Exception as e:
            say(
                f"[yellow]⚠ intake directive failed for {phase} ({type(e).__name__}: {e}) — prompt without intake cadrage[/]"
            )

    # 3. Feed des phases précédentes
    phase_reports = {
        "ph0-discovery": [],
        "ph1-strategy": ["ph0-discovery-report.md"],
        "ph2-design": ["ph0-discovery-report.md", "ph1-strategy-report.md"],
        "ph3-content": [
            "ph0-discovery-report.md",
            "ph1-strategy-report.md",
            "ph2-design-report.md",
        ],
        "ph4-build": ["ph1-strategy-report.md", "ph2-design-report.md", "ph3-content-report.md"],
        "ph5-qa": ["ph4-build-log.md"],
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
        "ph1-strategy": "ph1-strategy-report.md",
        "ph2-design": "ph2-design-report.md",
        "ph3-content": "ph3-content-report.md",
        "ph4-build": "ph4-build-log.md",
        "ph5-qa": "ph5-qa-report.md",
        "site-update": "site-update-report.md",
    }
    output_file = output_map.get(phase, f"{phase}-report.md")
    parts.append(f"Écris ton rapport dans {client_dir / output_file}")

    return "\n".join(parts)


__all__ = [
    "_validate_phase_against_intake",
    "build_phase_prompt",
]
