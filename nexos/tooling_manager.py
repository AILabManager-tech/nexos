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

    # Verdict deploy
    lines.append("\n" + "=" * 50)
    ph5 = None
    if gates_path.exists():
        try:
            gates = json.loads(gates_path.read_text())
            ph5 = next((g for g in gates if g.get("phase") == "ph5-qa"), None)
        except json.JSONDecodeError:
            pass
    if ph5 and ph5.get("decision") == "ACCEPT" and ph5.get("mu", 0) >= 8.5:
        lines.append(f"Statut: DÉPLOYABLE — Ph5 μ={ph5['mu']:.2f} ≥ 8.5")
    elif ph5:
        lines.append(f"Statut: NON DÉPLOYABLE — Ph5 μ={ph5.get('mu', 0):.2f} < 8.5 ou non accepté")
    else:
        lines.append("Statut: PIPELINE INCOMPLET — Ph5 non atteinte")

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
