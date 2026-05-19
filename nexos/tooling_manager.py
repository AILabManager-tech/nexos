"""
NEXOS v4.0 — Tooling Manager

Vérifie que les outils CLI requis sont installés avant de lancer le pipeline.
Dégradation gracieuse pour les outils optionnels (lighthouse, pa11y).
"""

import re
import subprocess
from pathlib import Path

from nexos.logging_config import get_logger

logger = get_logger(__name__)


# ── Outils requis ────────────────────────────────────────────────────

REQUIRED_TOOLS: dict[str, dict] = {
    "node": {
        "cmd": ["node", "--version"],
        "min_version": "20.0.0",
        "install": "https://nodejs.org",
        "critical": True,
    },
    "npm": {
        "cmd": ["npm", "--version"],
        "min_version": None,
        "install": "inclus avec node",
        "critical": True,
    },
    "codex": {
        "cmd": ["codex", "--version"],
        "min_version": None,
        "install": "npm i -g @openai/codex",
        "critical": False,
    },
    "lighthouse": {
        "cmd": ["lighthouse", "--version"],
        "min_version": None,
        "install": "npm i -g lighthouse",
        "critical": False,
    },
    "pa11y": {
        "cmd": ["pa11y", "--version"],
        "min_version": None,
        "install": "npm i -g pa11y",
        "critical": False,
    },
    "claude": {
        "cmd": ["claude", "--version"],
        "min_version": None,
        "install": "npm i -g @anthropic-ai/claude-code",
        "critical": True,
    },
    "gemini": {
        "cmd": ["gemini", "--version"],
        "min_version": None,
        "install": "npm i -g @anthropic-ai/gemini-cli ou https://github.com/google-gemini/gemini-cli",
        "critical": False,
    },
}


def _parse_version(version_str: str) -> tuple[int, ...]:
    """Extrait les composants numériques d'une version (ex: 'v20.11.1' → (20, 11, 1))."""
    match = re.search(r"(\d+(?:\.\d+)*)", version_str)
    if not match:
        return (0,)
    return tuple(int(x) for x in match.group(1).split("."))


def check_tool(name: str) -> tuple[bool, str | None]:
    """Vérifie si un outil est installé. Retourne (disponible, version)."""
    if name not in REQUIRED_TOOLS:
        return False, None

    tool = REQUIRED_TOOLS[name]
    try:
        # SAFE: tool["cmd"] comes from the REQUIRED_TOOLS constant (hardcoded
        # static argv lists like ["node", "--version"]). shell=False (default).
        result = subprocess.run(
            tool["cmd"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        version_str = result.stdout.strip() or result.stderr.strip()

        # Vérifier version minimale si spécifiée
        if tool["min_version"] and version_str:
            current = _parse_version(version_str)
            minimum = _parse_version(tool["min_version"])
            if current < minimum:
                return False, version_str

        return True, version_str
    except FileNotFoundError:
        return False, None
    except subprocess.TimeoutExpired:
        return False, None
    except OSError:
        return False, None


def ensure_tooling(interactive: bool = True) -> dict[str, bool]:
    """
    Vérifie tous les outils requis.

    Si interactive=True, affiche un rapport et propose d'installer les manquants.
    Si interactive=False, affiche warnings/erreurs et retourne le statut.

    Lève RuntimeError si un outil critique manque (node, npm, codex).
    """
    results: dict[str, bool] = {}
    missing_critical: list[str] = []
    missing_optional: list[str] = []

    for name, tool in REQUIRED_TOOLS.items():
        available, _version = check_tool(name)
        results[name] = available

        if not available:
            if tool["critical"]:
                missing_critical.append(name)
                logger.error("Critical tool missing: %s — install: %s", name, tool["install"])
            else:
                missing_optional.append(name)
                logger.warning("Optional tool missing: %s — install: %s", name, tool["install"])

    if missing_critical:
        raise RuntimeError(
            f"Outils critiques manquants: {', '.join(missing_critical)}. "
            "Installez-les avant de lancer le pipeline."
        )

    if missing_optional and interactive:
        logger.info("Optional tools missing — interactive install prompt")
        for name in missing_optional:
            tool = REQUIRED_TOOLS[name]
            try:
                answer = input(f"  Installer {name} ? [O/n] ").strip().lower()
                if answer in ("", "o", "oui", "y", "yes"):
                    logger.info("Installing %s via npm -g", name)
                    # SAFE: `name` is a key of REQUIRED_TOOLS (a hardcoded
                    # constant), never user-supplied. argv list + shell=False.
                    subprocess.run(
                        ["npm", "i", "-g", name],
                        timeout=120,
                        check=True,
                    )
                    results[name] = True
                    logger.info("%s installed", name)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                logger.warning("Install failed for %s: %s", name, e)

    return results


def _check_templates() -> list[tuple[str, bool]]:
    """Vérifie la présence des templates critiques."""
    from pathlib import Path

    templates_dir = Path(__file__).parent.parent / "templates"
    critical_templates = [
        "vercel-headers.template.json",
        "cookie-consent-component.tsx",
        "privacy-policy-template.md",
        "legal-mentions-template.md",
        "brief-intake.md",
        "brief-schema.json",
        "next-config.template.mjs",
    ]
    return [(t, (templates_dir / t).exists()) for t in critical_templates]


def _check_soic_engine() -> tuple[bool, str]:
    """Vérifie que le moteur SOIC est accessible."""
    from pathlib import Path

    soic_dir = Path(__file__).parent.parent / "soic"
    if not soic_dir.exists():
        return False, "symlink soic/ absent"
    try:
        # Vérifier qu'on peut importer le module
        import importlib.util

        spec = importlib.util.spec_from_file_location("soic", soic_dir / "__init__.py")
        if spec is None:
            return False, "soic/__init__.py introuvable"
        return True, str(soic_dir.resolve())
    except Exception as e:
        return False, str(e)


def _count_clients() -> tuple[int, list[str]]:
    """Compte les clients et identifie ceux avec un site/."""
    from pathlib import Path

    clients_dir = Path(__file__).parent.parent / "clients"
    if not clients_dir.exists():
        return 0, []
    all_clients = [
        d.name for d in clients_dir.iterdir() if d.is_dir() and not d.name.startswith(".")
    ]
    with_site = [
        name
        for name in all_clients
        if (clients_dir / name / "site" / "package.json").exists()
        or (clients_dir / name / "package.json").exists()
    ]
    return len(all_clients), with_site


def doctor_client_report(slug: str) -> str:
    """Diagnostic ciblé sur un client (pour `nexos doctor --client <slug>`).

    Inventorie l'état du client : brief, site, SOIC gates, tooling outputs,
    dernier pipeline event. Vise à répondre "ce client est-il déployable ?"
    sans scanner toute la plateforme. Audit dette 2026-05-15 item K.
    """
    import json

    from nexos.config import settings

    client_dir = (
        Path(settings.clients_dir) / slug
        if hasattr(settings, "clients_dir")
        else Path("clients") / slug
    )
    if not client_dir.is_dir():
        return f"NEXOS Doctor — Client `{slug}`\n{'=' * 50}\n\nErreur: client introuvable ({client_dir})"

    lines = [f"NEXOS Doctor — Client `{slug}`", "=" * 50]

    # Brief
    brief_path = client_dir / "brief-client.json"
    lines.append("\n  BRIEF")
    lines.append("  " + "-" * 46)
    if brief_path.exists():
        try:
            brief = json.loads(brief_path.read_text())
            company = (
                brief.get("company", {}).get("name")
                or brief.get("identite", {}).get("nom_entreprise")
                or "?"
            )
            lines.append(f"  [+] brief-client.json OK — {company}")
        except json.JSONDecodeError:
            lines.append("  [-] brief-client.json CORROMPU")
    else:
        lines.append("  [-] brief-client.json MANQUANT")

    # Site Next.js
    lines.append("\n  SITE")
    lines.append("  " + "-" * 46)
    site_dir = client_dir / "site"
    if (site_dir / "package.json").exists():
        try:
            pkg = json.loads((site_dir / "package.json").read_text())
            next_ver = pkg.get("dependencies", {}).get("next", "?")
            lines.append(f"  [+] site/package.json OK — next@{next_ver}")
        except json.JSONDecodeError:
            lines.append("  [-] package.json CORROMPU")
    else:
        lines.append("  [-] site/ ABSENT ou sans package.json")

    # SOIC gates
    lines.append("\n  SOIC GATES")
    lines.append("  " + "-" * 46)
    gates_path = client_dir / "soic-gates.json"
    if gates_path.exists():
        try:
            gates = json.loads(gates_path.read_text())
            for g in gates if isinstance(gates, list) else []:
                phase = g.get("phase", "?")
                mu = g.get("mu", 0)
                thr = g.get("threshold", 0)
                dec = g.get("decision", "?")
                icon = "+" if dec == "ACCEPT" and mu >= thr else "-"
                lines.append(f"  [{icon}] {phase:18s} μ={mu:.2f}  seuil={thr:.1f}  {dec}")
        except json.JSONDecodeError:
            lines.append("  [-] soic-gates.json CORROMPU")
    else:
        lines.append("  [-] soic-gates.json MANQUANT (pipeline pas exécuté)")

    # Tooling outputs
    lines.append("\n  TOOLING (preflight)")
    lines.append("  " + "-" * 46)
    tooling = client_dir / "tooling"
    expected = [
        "lighthouse.json",
        "a11y.json",
        "deps.json",
        "headers.json",
        "ssl.json",
        "osiris.json",
    ]
    if tooling.is_dir():
        for name in expected:
            f = tooling / name
            if f.exists():
                size = f.stat().st_size
                lines.append(f"  [+] {name:20s} {size:6d}o")
            else:
                lines.append(f"  [-] {name:20s} MANQUANT")
    else:
        lines.append("  [-] tooling/ MANQUANT (preflight pas exécuté)")

    # Deploy decision multi-axes (P9 D2 + extension + extension²)
    # — SOIC + Osiris + Lighthouse + npm audit + pa11y
    lines.append("\n  DEPLOY DECISION (5 axes)")
    lines.append("  " + "-" * 46)
    try:
        from nexos.deploy_decision import evaluate_deploy_decision

        decision = evaluate_deploy_decision(client_dir)
        icon_for = {"PASS": "+", "FAIL": "-", "UNKNOWN": "?"}

        soic_mu_str = f"{decision.soic_mu:.2f}" if decision.soic_mu is not None else "—"
        osiris_score_str = (
            f"{decision.osiris_score:.1f}" if decision.osiris_score is not None else "—"
        )
        osiris_grade_str = decision.osiris_grade or "—"
        lh_perf_str = (
            f"{decision.lighthouse_perf:.0f}" if decision.lighthouse_perf is not None else "—"
        )
        npm_high_str = "—" if decision.npm_audit_high is None else str(decision.npm_audit_high)
        npm_crit_str = (
            "—" if decision.npm_audit_critical is None else str(decision.npm_audit_critical)
        )

        lines.append(
            f"  [{icon_for[decision.soic_verdict]}] SOIC       μ={soic_mu_str:6s} "
            f"(≥{decision.soic_threshold:.1f})   → {decision.soic_verdict}"
        )
        lines.append(
            f"  [{icon_for[decision.osiris_verdict]}] Osiris     score={osiris_score_str:6s} ({osiris_grade_str}) "
            f"(≥{decision.osiris_threshold:.1f}) → {decision.osiris_verdict}"
        )
        lines.append(
            f"  [{icon_for[decision.lighthouse_verdict]}] Lighthouse perf={lh_perf_str:>3s}/100 "
            f"(≥{decision.lighthouse_threshold:.0f})   → {decision.lighthouse_verdict}"
        )
        lines.append(
            f"  [{icon_for[decision.npm_audit_verdict]}] npm audit  high={npm_high_str} crit={npm_crit_str} "
            f"(≤{decision.npm_audit_threshold} HIGH+CRIT) → {decision.npm_audit_verdict}"
        )
        pa11y_err_str = "—" if decision.pa11y_errors is None else str(decision.pa11y_errors)
        pa11y_warn_str = (
            "—" if decision.pa11y_warnings_count is None else str(decision.pa11y_warnings_count)
        )
        lines.append(
            f"  [{icon_for[decision.pa11y_verdict]}] pa11y      errors={pa11y_err_str} warns={pa11y_warn_str} "
            f"(≤{decision.pa11y_threshold} errors)   → {decision.pa11y_verdict}"
        )
        joint_icon = "+" if decision.joint_verdict == "ACCEPT" else "-"
        blockers_str = ", ".join(decision.blockers) if decision.blockers else "—"
        lines.append(
            f"  [{joint_icon}] Joint      {decision.joint_verdict} (blockers: {blockers_str})"
        )
        for w in decision.warnings:
            lines.append(f"  [!] {w}")
    except Exception as exc:  # doctor doit jamais crasher
        lines.append(f"  [!] deploy_decision indisponible ({type(exc).__name__})")

    # Verdict deploy (legacy summary — gardé pour compat doctor --all-clients)
    lines.append("\n" + "=" * 50)
    ph5 = None
    if gates_path.exists():
        try:
            gates = json.loads(gates_path.read_text())
            ph5 = _latest_phase_gate(gates, "ph5-qa")
        except json.JSONDecodeError:
            pass
    if ph5 and ph5.get("decision") == "ACCEPT" and ph5.get("mu", 0) >= 8.5:
        lines.append(f"Statut: DÉPLOYABLE — Ph5 μ={ph5['mu']:.2f} ≥ 8.5")
    elif ph5:
        lines.append(f"Statut: NON DÉPLOYABLE — Ph5 μ={ph5.get('mu', 0):.2f} < 8.5 ou non accepté")
    else:
        lines.append("Statut: PIPELINE INCOMPLET — Ph5 non atteinte")

    return "\n".join(lines)


def _latest_phase_gate(gates: list, phase: str) -> dict | None:
    """Retourne la DERNIÈRE entrée d'une phase dans `soic-gates.json` (P9 D9).

    Le fichier est append-only : chaque run produit une nouvelle entrée.
    Pour le verdict deploy d'un client, on veut toujours le run le plus
    récent. Le pattern `next((g for g in gates if g.get("phase") == phase))`
    retournait la PREMIÈRE entrée et faisait mentir doctor pour tout client
    multi-runs (découvert pendant P8.5 vertex-pmo : run 4 ACCEPT μ=9.00
    invisible derrière run 1 ABORT_PLATEAU μ=7.91).

    Cohérent avec `orchestrator/score_injection.py:_load_latest_gate`.
    """
    if not isinstance(gates, list):
        return None
    matching = [g for g in gates if isinstance(g, dict) and g.get("phase") == phase]
    return matching[-1] if matching else None


def _client_status_row(slug: str) -> dict[str, str]:
    """Snapshot une-ligne d'un client (utilisé par doctor_all_clients_report).

    Retourne un dict avec : slug, brief, site, gates_count, ph5_mu, ph5_decision,
    deploy_status. Toutes les valeurs sont des strings prêtes à afficher.
    """
    import json
    from pathlib import Path

    client_dir = Path("clients") / slug
    row: dict[str, str] = {
        "slug": slug,
        "brief": "—",
        "site": "—",
        "gates": "—",
        "ph5_mu": "—",
        "deploy": "—",
    }

    if not client_dir.is_dir():
        return row

    # Brief
    brief_path = client_dir / "brief-client.json"
    if brief_path.exists():
        try:
            json.loads(brief_path.read_text())
            row["brief"] = "ok"
        except json.JSONDecodeError:
            row["brief"] = "corrupt"
    else:
        row["brief"] = "missing"

    # Site
    if (client_dir / "site" / "package.json").exists():
        row["site"] = "ok"
    else:
        row["site"] = "missing"

    # Gates + Ph5
    gates_path = client_dir / "soic-gates.json"
    if gates_path.exists():
        try:
            gates = json.loads(gates_path.read_text())
            if isinstance(gates, list):
                row["gates"] = str(len(gates))
                ph5 = _latest_phase_gate(gates, "ph5-qa")
                if ph5:
                    mu = ph5.get("mu", 0)
                    decision = ph5.get("decision", "?")
                    row["ph5_mu"] = f"{mu:.2f}"
                    if decision == "ACCEPT" and mu >= 8.5:
                        row["deploy"] = "READY"
                    elif decision == "ACCEPT":
                        row["deploy"] = "BELOW (μ<8.5)"
                    else:
                        row["deploy"] = decision
        except json.JSONDecodeError:
            row["gates"] = "corrupt"

    return row


def doctor_all_clients_report() -> str:
    """Rapport tabulaire de tous les clients (un par ligne).

    Visibilité opérationnelle : voir d'un coup d'œil quels clients sont prêts
    à déployer, lesquels ont un brief manquant, lesquels n'ont pas tourné le
    pipeline.
    """
    from pathlib import Path

    clients_dir = Path("clients")
    if not clients_dir.is_dir():
        return "NEXOS Doctor — All Clients\nErreur: dossier clients/ introuvable"

    slugs = sorted(
        d.name for d in clients_dir.iterdir() if d.is_dir() and not d.name.startswith(("_", "."))
    )

    rows = [_client_status_row(slug) for slug in slugs]

    # Largeurs colonnes
    slug_w = max((len(r["slug"]) for r in rows), default=10)
    slug_w = max(slug_w, len("Client"))

    lines = [
        f"NEXOS v4.2 — Doctor All Clients ({len(rows)} client{'s' if len(rows) != 1 else ''})",
        "=" * (slug_w + 60),
    ]
    # Deploy column : 14 chars couvre "ABORT_PLATEAU" (13) sans wrap
    header = f"  {'Client':<{slug_w}}  {'Brief':<8}  {'Site':<8}  {'Gates':<6}  {'Ph5 μ':<7}  {'Deploy':<14}"
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))

    deployable_count = 0
    for row in rows:
        if row["deploy"] == "READY":
            deployable_count += 1
        deploy_str = row["deploy"][:14]  # Truncate défensif si verdict custom > 14 chars
        lines.append(
            f"  {row['slug']:<{slug_w}}  {row['brief']:<8}  {row['site']:<8}  "
            f"{row['gates']:<6}  {row['ph5_mu']:<7}  {deploy_str:<14}"
        )

    lines.append("")
    lines.append(f"  Déployables (Ph5 μ ≥ 8.5 + ACCEPT) : {deployable_count}/{len(rows)}")

    return "\n".join(lines)


def doctor_report() -> str:
    """Retourne un rapport complet de l'état du système (pour `nexos doctor`)."""
    lines = ["NEXOS v4.0 — Doctor Report", "=" * 50]

    # Section 1: Outils CLI
    lines.append("\n  OUTILS CLI")
    lines.append("  " + "-" * 46)
    for name, tool in REQUIRED_TOOLS.items():
        available, version = check_tool(name)
        status = "OK" if available else "MANQUANT"
        icon = "+" if available else "-"
        version_display = version or "N/A"
        critical_tag = " [CRITIQUE]" if tool["critical"] else ""

        lines.append(f"  [{icon}] {name:12s} {version_display:20s} {status}{critical_tag}")

        if available and tool["min_version"] and version:
            current = _parse_version(version)
            minimum = _parse_version(tool["min_version"])
            if current < minimum:
                lines.append(f"      ATTENTION: version {version} < minimum {tool['min_version']}")

    # Section 2: Templates
    lines.append("\n  TEMPLATES")
    lines.append("  " + "-" * 46)
    templates = _check_templates()
    for name, exists in templates:
        icon = "+" if exists else "-"
        status = "OK" if exists else "MANQUANT"
        lines.append(f"  [{icon}] {name:40s} {status}")

    # Section 3: SOIC Engine
    lines.append("\n  SOIC ENGINE")
    lines.append("  " + "-" * 46)
    soic_ok, soic_info = _check_soic_engine()
    icon = "+" if soic_ok else "-"
    lines.append(f"  [{icon}] soic/  {soic_info}")

    # Section 4: Clients
    lines.append("\n  CLIENTS")
    lines.append("  " + "-" * 46)
    total, with_site = _count_clients()
    lines.append(f"  Total: {total} clients | {len(with_site)} avec site/")
    if with_site:
        for name in sorted(with_site):
            lines.append(f"    - {name}")

    # Résumé
    lines.append("\n" + "=" * 50)
    tools_ok = all(check_tool(n)[0] for n in REQUIRED_TOOLS)
    templates_ok = all(ok for _, ok in templates)
    if tools_ok and templates_ok and soic_ok:
        lines.append("Statut: SYSTEME OPERATIONNEL")
    else:
        problems = []
        if not tools_ok:
            missing = [n for n in REQUIRED_TOOLS if not check_tool(n)[0]]
            problems.append(f"outils: {', '.join(missing)}")
        if not templates_ok:
            missing_t = [n for n, ok in templates if not ok]
            problems.append(f"templates: {', '.join(missing_t)}")
        if not soic_ok:
            problems.append(f"soic: {soic_info}")
        lines.append(f"Statut: PROBLEMES DETECTES — {'; '.join(problems)}")

    return "\n".join(lines)
