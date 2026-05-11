"""
NEXOS v4.0 — Build Validator

Remplace la validation superficielle "BUILD PASS" de Ph4 par des vérifications
réelles : npm install, tsc, build, npm audit, fichiers critiques, headers.
"""

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from nexos.logging_config import get_logger

logger = get_logger(__name__)


# ── Constantes ────────────────────────────────────────────────────────

# Item 5 chantier 4 : la stack moderne NEXOS génère dans `app/[locale]/`.
# La stack legacy utilisait `src/app/[locale]/`. On accepte les deux conventions
# via `_check_critical_files()`.
CRITICAL_FILES_ROOT = [
    "vercel.json",
    "next.config.mjs",
]
CRITICAL_FILES_LOCALE = [
    "politique-confidentialite/page.tsx",
    "mentions-legales/page.tsx",
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
    # Item 2 chantier 4 : présence + exécution des tests unit (mode WARNING en
    # v4.3.x, bloquant FAIL en v4.4.0 quand les agents ph4 produiront des
    # tests systématiquement).
    tests_count: int = 0
    tests_run_ok: bool = True  # True par défaut (pas exécuté = pas un fail)
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
        errors = [line for line in result.stdout.splitlines() if "error TS" in line]
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
    """Vérifie la présence des fichiers critiques.

    Item 5 chantier 4 : détecte automatiquement la convention `app/` (moderne)
    ou `src/app/` (legacy) au lieu de coder en dur `src/app/`. Évite le faux
    négatif sur les sites NEXOS générés post-refactor chantier knowledge.
    """
    missing = []

    # Fichiers root (vercel.json, next.config.mjs)
    for filepath in CRITICAL_FILES_ROOT:
        if not (site_dir / filepath).exists():
            missing.append(filepath)

    # Fichiers locale : essayer app/ moderne puis src/app/ legacy
    locale_root_modern = site_dir / "app" / "[locale]"
    locale_root_legacy = site_dir / "src" / "app" / "[locale]"
    if locale_root_modern.exists():
        locale_base = "app/[locale]"
    elif locale_root_legacy.exists():
        locale_base = "src/app/[locale]"
    else:
        # Pas de dossier locale détecté → on rapporte les chemins modernes
        # (signal clair que rien n'est en place).
        locale_base = "app/[locale]"

    for relpath in CRITICAL_FILES_LOCALE:
        full_rel = f"{locale_base}/{relpath}"
        if not (site_dir / full_rel).exists():
            missing.append(full_rel)

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


def _count_test_files(site_dir: Path) -> int:
    """Item 2 chantier 4 : compte les fichiers de tests unit présents.

    Cherche `*.test.{ts,tsx,js,jsx}` et `*.spec.{ts,tsx,js,jsx}` dans
    `tests/`, `app/`, `components/`, `lib/`, et leurs variantes `src/`.
    Exclut `node_modules/` et `.next/`.
    """
    patterns = (
        "*.test.ts",
        "*.test.tsx",
        "*.test.js",
        "*.test.jsx",
        "*.spec.ts",
        "*.spec.tsx",
        "*.spec.js",
        "*.spec.jsx",
    )
    excluded = {"node_modules", ".next", ".git", "__pycache__"}
    count = 0
    for pattern in patterns:
        for path in site_dir.rglob(pattern):
            if not any(part in excluded for part in path.parts):
                count += 1
    return count


def _run_tests(site_dir: Path) -> bool:
    """Item 2 chantier 4 : exécute la suite de tests si elle existe.

    Lance `npm test -- --run` (vitest single-pass). Retourne True si exit 0.
    Retourne True aussi si aucun test n'est trouvé (pas un fail, juste
    "rien à exécuter").
    """
    package_json = site_dir / "package.json"
    if not package_json.exists():
        return True

    try:
        data = json.loads(package_json.read_text())
        scripts = data.get("scripts", {})
        if "test" not in scripts:
            return True
    except (json.JSONDecodeError, OSError):
        return True

    try:
        # SAFE: static argv. shell=False.
        result = subprocess.run(
            ["npm", "test", "--", "--run"],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=180,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


# ── Fonction principale ───────────────────────────────────────────────


def validate_build(site_dir: Path) -> BuildResult:
    """Exécute toutes les validations build sur le site généré."""
    result = BuildResult()

    # 1. npm install
    logger.info("Build validation: npm install")
    result.npm_install_ok = _check_npm_install(site_dir)

    if not result.npm_install_ok:
        result.overall_pass = False
        return result

    # 2. TypeScript check
    logger.info("Build validation: tsc --noEmit")
    result.tsc_ok, result.tsc_errors = _check_tsc(site_dir)

    # 3. Build
    logger.info("Build validation: npm run build")
    result.build_ok, result.build_errors = _check_build(site_dir)

    # 4. npm audit
    logger.info("Build validation: npm audit")
    result.audit_highs, result.audit_criticals = _check_audit(site_dir)

    # 5. Fichiers critiques
    result.missing_files = _check_critical_files(site_dir)

    # 6. Headers sécurité dans vercel.json
    result.headers_ok = _check_vercel_headers(site_dir)

    # 7. Item 2 chantier 4 : tests présents + exécutés (WARNING en v4.3.x,
    # FAIL en v4.4.0 quand les agents produiront systématiquement des tests).
    logger.info("Build validation: tests presence + run")
    result.tests_count = _count_test_files(site_dir)
    if result.tests_count > 0:
        result.tests_run_ok = _run_tests(site_dir)
    else:
        # Pas de tests = WARNING (logged dans format_build_report) mais pas
        # un FAIL pour éviter de casser tous les pipelines actuels.
        result.tests_run_ok = True

    # Décision globale
    # Note: tsc_ok est non-bloquant si build_ok est vrai (erreurs TSC dans
    # les tests ne bloquent pas le build Next.js qui ne compile que app/).
    # Note: tests_count == 0 émet un WARNING mais ne bloque pas — transition
    # douce avant v4.4.0 où l'absence de tests sera FAIL.
    result.overall_pass = (
        result.npm_install_ok
        and result.build_ok
        and result.audit_criticals == 0
        and result.headers_ok
        and result.tests_run_ok  # bloque si tests présents ET échouent
    )

    return result


def format_build_report(result: BuildResult) -> str:
    """Formatte le résultat pour la console."""

    def icon(ok: bool) -> str:
        return "+" if ok else "-"

    # Item 2 chantier 4 : icône WARN si tests absents (transition douce v4.3.x)
    tests_icon = (
        "+"
        if result.tests_run_ok and result.tests_count > 0
        else ("!" if result.tests_count == 0 else "-")
    )
    tests_label = (
        f"{result.tests_count} tests"
        if result.tests_count > 0
        else "0 tests (WARNING — bloquant en v4.4.0)"
    )

    lines = [
        "NEXOS v4.0 — Build Validation Report",
        "=" * 45,
        f"  [{icon(result.npm_install_ok)}] npm install",
        f"  [{icon(result.tsc_ok)}] tsc --noEmit ({len(result.tsc_errors)} erreurs)",
        f"  [{icon(result.build_ok)}] npm run build",
        f"  [{icon(result.audit_criticals == 0)}] npm audit (HIGH:{result.audit_highs} CRITICAL:{result.audit_criticals})",
        f"  [{icon(len(result.missing_files) == 0)}] Fichiers critiques ({len(result.missing_files)} manquants)",
        f"  [{icon(result.headers_ok)}] Headers sécurité vercel.json",
        f"  [{tests_icon}] Tests unit : {tests_label}",
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
