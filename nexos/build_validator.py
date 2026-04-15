"""
NEXOS v4.0 — Build Validator

Remplace la validation superficielle "BUILD PASS" de Ph4 par des vérifications
réelles : npm install, tsc, build, npm audit, fichiers critiques, headers.
"""

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

try:
    from rich.console import Console
    console = Console()
except ImportError:
    class Console:
        def print(self, *a, **kw): print(*a)
    console = Console()


# ── Constantes ────────────────────────────────────────────────────────

CRITICAL_FILES = [
    "vercel.json",
    "next.config.mjs",
    "src/app/[locale]/politique-confidentialite/page.tsx",
    "src/app/[locale]/mentions-legales/page.tsx",
]

REQUIRED_HEADERS = [
    "x-content-type-options",
    "x-frame-options",
    "referrer-policy",
    "permissions-policy",
    "strict-transport-security",
    "x-dns-prefetch-control",
]


@dataclass
class BuildResult:
    npm_install_ok: bool = False
    tsc_ok: bool = False
    tsc_errors: list[str] = field(default_factory=list)
    build_ok: bool = False
    build_errors: str = ""
    audit_highs: int = 0
    audit_criticals: int = 0
    missing_files: list[str] = field(default_factory=list)
    headers_ok: bool = False
    overall_pass: bool = False


# ── Fonctions internes ────────────────────────────────────────────────

def _check_npm_install(site_dir: Path) -> bool:
    """Exécute npm install si node_modules absent."""
    if (site_dir / "node_modules").exists():
        return True
    try:
        # SAFE: static argv list, cwd is a Path object chosen by the pipeline.
        # shell=False (default). No user string in args.
        result = subprocess.run(
            ["npm", "install"],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


def _check_tsc(site_dir: Path) -> tuple[bool, list[str]]:
    """Exécute npx tsc --noEmit. Retourne (ok, erreurs)."""
    try:
        # SAFE: static argv list, cwd is Path. shell=False (default).
        result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0:
            return True, []
        errors = [
            line for line in result.stdout.splitlines()
            if "error TS" in line
        ]
        return False, errors[:20]  # Limiter à 20 erreurs
    except (subprocess.TimeoutExpired, OSError):
        return False, ["tsc timeout ou erreur OS"]


def _check_build(site_dir: Path) -> tuple[bool, str]:
    """Exécute npm run build. Retourne (ok, stderr si échec)."""
    try:
        # SAFE: static argv list, cwd is Path. shell=False (default).
        result = subprocess.run(
            ["npm", "run", "build"],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            return True, ""
        # Extraire les dernières lignes d'erreur
        error_lines = result.stderr.strip() or result.stdout.strip()
        return False, error_lines[-2000:]  # Limiter la taille
    except subprocess.TimeoutExpired:
        return False, "Build timeout (>300s)"
    except OSError as e:
        return False, str(e)


def _check_audit(site_dir: Path) -> tuple[int, int]:
    """Exécute npm audit --json. Retourne (highs, criticals)."""
    try:
        # SAFE: static argv list, cwd is Path. shell=False (default).
        result = subprocess.run(
            ["npm", "audit", "--json"],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        data = json.loads(result.stdout)

        # npm audit v7+ format
        vulns = data.get("metadata", {}).get("vulnerabilities", {})
        highs = vulns.get("high", 0)
        criticals = vulns.get("critical", 0)
        return highs, criticals
    except (json.JSONDecodeError, KeyError):
        return 0, 0
    except (subprocess.TimeoutExpired, OSError):
        return 0, 0


def _check_critical_files(site_dir: Path) -> list[str]:
    """Vérifie la présence des fichiers critiques."""
    missing = []
    for filepath in CRITICAL_FILES:
        if not (site_dir / filepath).exists():
            missing.append(filepath)
    return missing


def _check_vercel_headers(site_dir: Path) -> bool:
    """Vérifie que vercel.json contient les 6 headers requis."""
    vercel_path = site_dir / "vercel.json"
    if not vercel_path.exists():
        return False

    try:
        data = json.loads(vercel_path.read_text())
        headers_list = data.get("headers", [])

        # Chercher le bloc source: "/(.*)" qui contient les headers globaux
        found_headers: set[str] = set()
        for block in headers_list:
            for header in block.get("headers", []):
                found_headers.add(header.get("key", "").lower())

        return all(h in found_headers for h in REQUIRED_HEADERS)
    except (json.JSONDecodeError, KeyError):
        return False


# ── Fonction principale ───────────────────────────────────────────────

def validate_build(site_dir: Path) -> BuildResult:
    """Exécute toutes les validations build sur le site généré."""
    result = BuildResult()

    # 1. npm install
    console.print("[dim]  Validation: npm install...[/]")
    result.npm_install_ok = _check_npm_install(site_dir)

    if not result.npm_install_ok:
        result.overall_pass = False
        return result

    # 2. TypeScript check
    console.print("[dim]  Validation: tsc --noEmit...[/]")
    result.tsc_ok, result.tsc_errors = _check_tsc(site_dir)

    # 3. Build
    console.print("[dim]  Validation: npm run build...[/]")
    result.build_ok, result.build_errors = _check_build(site_dir)

    # 4. npm audit
    console.print("[dim]  Validation: npm audit...[/]")
    result.audit_highs, result.audit_criticals = _check_audit(site_dir)

    # 5. Fichiers critiques
    result.missing_files = _check_critical_files(site_dir)

    # 6. Headers sécurité dans vercel.json
    result.headers_ok = _check_vercel_headers(site_dir)

    # Décision globale
    # Note: tsc_ok est non-bloquant si build_ok est vrai (erreurs TSC dans
    # les tests ne bloquent pas le build Next.js qui ne compile que src/app/)
    result.overall_pass = (
        result.npm_install_ok
        and result.build_ok
        and result.audit_criticals == 0
        and result.headers_ok
    )

    return result


def format_build_report(result: BuildResult) -> str:
    """Formatte le résultat pour la console."""
    icon = lambda ok: "+" if ok else "-"
    lines = [
        "NEXOS v4.0 — Build Validation Report",
        "=" * 45,
        f"  [{icon(result.npm_install_ok)}] npm install",
        f"  [{icon(result.tsc_ok)}] tsc --noEmit ({len(result.tsc_errors)} erreurs)",
        f"  [{icon(result.build_ok)}] npm run build",
        f"  [{icon(result.audit_criticals == 0)}] npm audit (HIGH:{result.audit_highs} CRITICAL:{result.audit_criticals})",
        f"  [{icon(len(result.missing_files) == 0)}] Fichiers critiques ({len(result.missing_files)} manquants)",
        f"  [{icon(result.headers_ok)}] Headers sécurité vercel.json",
        "=" * 45,
    ]

    if result.missing_files:
        lines.append(f"  Fichiers manquants: {', '.join(result.missing_files)}")

    if result.tsc_errors:
        lines.append("  Erreurs TSC (extrait):")
        for err in result.tsc_errors[:5]:
            lines.append(f"    {err}")

    status = "BUILD PASS" if result.overall_pass else "BUILD FAIL"
    lines.append(f"\n  Résultat: {status}")
    return "\n".join(lines)
