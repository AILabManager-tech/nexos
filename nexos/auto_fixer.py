"""
NEXOS v4.0 — Auto Fixer

Corrige automatiquement les problèmes D4 (Sécurité) et D8 (Loi 25) récurrents :
- Cookie consent absent
- Vulnérabilités npm
- Headers sécurité manquants dans vercel.json
- poweredByHeader dans next.config
- Pages légales (politique confidentialité, mentions légales)
"""

import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from nexos.brief_contract import normalize_brief
from nexos.logging_config import get_logger

logger = get_logger(__name__)

try:
    from nexos.changelog import log_event, EventType
    _HAS_CHANGELOG = True
except ImportError:
    _HAS_CHANGELOG = False

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"

REQUIRED_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "X-DNS-Prefetch-Control": "on",
    "Strict-Transport-Security": "max-age=63072000; includeSubDomains; preload",
}


def _template_value(value, fallback: str) -> str:
    """Garantit une valeur chaîne sûre pour les templates."""
    if value is None:
        return fallback
    if isinstance(value, list):
        return "\n".join(str(item) for item in value) if value else fallback
    text = str(value).strip()
    return text or fallback


@dataclass
class FixReport:
    cookie_consent_added: bool = False
    npm_audit_fixed: int = 0
    vercel_headers_fixed: bool = False
    next_config_patched: bool = False
    privacy_page_added: bool = False
    legal_page_added: bool = False

    @property
    def total_fixes(self) -> int:
        count = 0
        if self.cookie_consent_added:
            count += 1
        if self.npm_audit_fixed > 0:
            count += 1
        if self.vercel_headers_fixed:
            count += 1
        if self.next_config_patched:
            count += 1
        if self.privacy_page_added:
            count += 1
        if self.legal_page_added:
            count += 1
        return count


# ── Fix functions ─────────────────────────────────────────────────────

def _fix_cookie_consent(site_dir: Path, report: FixReport):
    """
    Copie cookie-consent-component.tsx si absent, injecte dans layout.tsx.

    Stratégie :
    1. Chercher un fichier contenant "cookie" ET "consent" dans src/components/
    2. Si absent → copier le template NEXOS
    3. Lire le layout.tsx principal (locale ou racine)
    4. Si <CookieConsent pas dans le layout → ajouter import + composant
    """
    components_dir = site_dir / "src" / "components"

    # 1. Chercher un fichier cookie consent existant et résoudre son import path
    consent_file: Path | None = None
    if components_dir.exists():
        for f in components_dir.rglob("*"):
            if f.is_file() and "cookie" in f.name.lower() and "consent" in f.name.lower():
                consent_file = f
                break

    # 2. Copier le template si absent
    if consent_file is None:
        template_src = TEMPLATES_DIR / "cookie-consent-component.tsx"
        if not template_src.exists():
            return
        components_dir.mkdir(parents=True, exist_ok=True)
        consent_file = components_dir / "cookie-consent.tsx"
        shutil.copy2(template_src, consent_file)
        logger.info("cookie-consent.tsx copied to src/components/")

    # 3. Trouver le layout.tsx principal
    layout_candidates = [
        site_dir / "src" / "app" / "[locale]" / "layout.tsx",
        site_dir / "src" / "app" / "layout.tsx",
    ]
    layout_path = None
    for candidate in layout_candidates:
        if candidate.exists():
            layout_path = candidate
            break

    if layout_path is None:
        return

    layout_content = layout_path.read_text()

    # 4. Vérifier si CookieConsent est déjà injecté
    if "<CookieConsent" in layout_content:
        return

    # 5. Construire l'import path basé sur le fichier réel trouvé
    # Ex: src/components/legal/CookieConsent.tsx → @/components/legal/CookieConsent
    relative = consent_file.relative_to(site_dir / "src")
    import_path = "@/" + str(relative).replace(".tsx", "").replace(".ts", "")
    import_line = f'import {{ CookieConsent }} from "{import_path}";\n'

    # Insérer l'import après le dernier import existant
    last_import_idx = -1
    lines = layout_content.split("\n")
    for i, line in enumerate(lines):
        if line.strip().startswith("import "):
            last_import_idx = i

    if last_import_idx >= 0:
        lines.insert(last_import_idx + 1, import_line.rstrip())
    else:
        lines.insert(0, import_line.rstrip())

    layout_content = "\n".join(lines)

    # 6. Injecter <CookieConsent /> juste avant </body>
    if "</body>" in layout_content:
        layout_content = layout_content.replace(
            "</body>",
            "        <CookieConsent />\n      </body>",
        )
        layout_path.write_text(layout_content)
        report.cookie_consent_added = True
        logger.info("CookieConsent injected into layout.tsx")


def _fix_npm_audit(site_dir: Path, report: FixReport):
    """Exécute npm audit fix pour corriger les vulnérabilités."""
    try:
        # SAFE: static argv list, cwd is Path. shell=False (default).
        result = subprocess.run(
            ["npm", "audit", "fix"],
            cwd=site_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        # Compter les vulns corrigées depuis la sortie
        output = result.stdout or ""
        # Chercher "fixed X of Y" dans la sortie npm
        match = re.search(r"fixed\s+(\d+)\s+of", output)
        if match:
            report.npm_audit_fixed = int(match.group(1))
        elif result.returncode == 0:
            # npm audit fix a réussi, mais pas de vulns à fixer
            report.npm_audit_fixed = 0
    except (subprocess.TimeoutExpired, OSError):
        pass


def _fix_vercel_headers(site_dir: Path, report: FixReport):
    """Assure que vercel.json existe avec les 6 headers sécurité."""
    vercel_path = site_dir / "vercel.json"
    template_path = TEMPLATES_DIR / "vercel-headers.template.json"

    if not vercel_path.exists():
        # Copier le template entier
        if template_path.exists():
            shutil.copy2(template_path, vercel_path)
            report.vercel_headers_fixed = True
            logger.info("vercel.json created from template")
        return

    # Charger le JSON existant
    try:
        data = json.loads(vercel_path.read_text())
    except json.JSONDecodeError:
        # JSON corrompu → remplacer par template
        if template_path.exists():
            shutil.copy2(template_path, vercel_path)
            report.vercel_headers_fixed = True
        return

    # Trouver ou créer le bloc headers global "/(.*)"
    headers_list = data.setdefault("headers", [])
    global_block = None
    for block in headers_list:
        if block.get("source") == "/(.*)":
            global_block = block
            break

    if global_block is None:
        global_block = {"source": "/(.*)", "headers": []}
        headers_list.insert(0, global_block)

    # Vérifier chaque header requis
    existing_keys = {
        h.get("key", "").lower()
        for h in global_block.get("headers", [])
    }

    added = False
    for key, value in REQUIRED_HEADERS.items():
        if key.lower() not in existing_keys:
            global_block["headers"].append({"key": key, "value": value})
            added = True

    if added:
        vercel_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        report.vercel_headers_fixed = True
        logger.info("Security headers added to vercel.json")


def _fix_next_config(site_dir: Path, report: FixReport):
    """Assure poweredByHeader: false dans next.config.mjs."""
    config_path = site_dir / "next.config.mjs"
    if not config_path.exists():
        config_path = site_dir / "next.config.js"
    if not config_path.exists():
        config_path = site_dir / "next.config.ts"
    if not config_path.exists():
        return

    content = config_path.read_text()

    if "poweredByHeader" in content:
        # Déjà présent — vérifier qu'il est bien false
        if "poweredByHeader: true" in content or "poweredByHeader:true" in content:
            content = re.sub(
                r"poweredByHeader\s*:\s*true",
                "poweredByHeader: false",
                content,
            )
            config_path.write_text(content)
            report.next_config_patched = True
            logger.info("poweredByHeader switched to false")
        return

    # Ajouter poweredByHeader: false après le premier { du nextConfig
    # Chercher le pattern "const nextConfig = {" ou "const config = {"
    pattern = r"(const\s+\w+Config\s*=\s*\{)"
    match = re.search(pattern, content)
    if match:
        insert_pos = match.end()
        content = content[:insert_pos] + "\n  poweredByHeader: false," + content[insert_pos:]
        config_path.write_text(content)
        report.next_config_patched = True
        logger.info("poweredByHeader: false added to next.config")


def _fix_privacy_page(site_dir: Path, brief: dict, report: FixReport):
    """Génère la page politique-confidentialite si absente."""
    # Chercher dans les variantes de chemins
    target_dirs = [
        site_dir / "src" / "app" / "[locale]" / "politique-confidentialite",
        site_dir / "src" / "app" / "politique-confidentialite",
    ]

    for target_dir in target_dirs:
        if (target_dir / "page.tsx").exists():
            return  # Déjà présent

    template_path = TEMPLATES_DIR / "privacy-policy-template.md"
    if not template_path.exists():
        return

    # Déterminer le répertoire cible (préférer la structure i18n)
    locale_app = site_dir / "src" / "app" / "[locale]"
    if locale_app.exists():
        target_dir = locale_app / "politique-confidentialite"
    else:
        target_dir = site_dir / "src" / "app" / "politique-confidentialite"

    target_dir.mkdir(parents=True, exist_ok=True)

    # Lire et remplir le template
    template = template_path.read_text()
    legal = brief.get("legal", {})
    replacements = {
        "{{COMPANY_NAME}}": _template_value(brief.get("company_name", legal.get("company_name")), "[Nom entreprise]"),
        "{{RPP_NAME}}": _template_value(legal.get("rpp_name"), "[Nom du RPP]"),
        "{{RPP_TITLE}}": _template_value(legal.get("rpp_title"), "[Titre du RPP]"),
        "{{RPP_EMAIL}}": _template_value(legal.get("rpp_email"), "[courriel@example.com]"),
        "{{DATE}}": datetime.now().strftime("%Y-%m-%d"),
        "{{DATA_TYPES}}": _template_value(legal.get("data_types"), "- Nom, prenom, courriel\n- Adresse IP\n- Donnees de navigation"),
        "{{PURPOSES}}": _template_value(legal.get("purposes"), "- Fournir nos services\n- Ameliorer l'experience utilisateur\n- Communications marketing (avec consentement)"),
        "{{RETENTION_PERIOD}}": _template_value(legal.get("retention"), "24 mois apres la derniere interaction"),
        "{{ADDRESS}}": _template_value(legal.get("address"), "[Adresse]"),
        "{{THIRD_PARTIES}}": _template_value(legal.get("third_parties"), "- Google Analytics (analytique)\n- Vercel (hebergement)"),
        "{{TRANSFER_SECTION}}": _template_value(legal.get("transfer"), "Certaines donnees peuvent etre traitees par des services heberges hors du Quebec (ex : Vercel, Google). Nous nous assurons que ces transferts respectent les exigences de la Loi 25."),
        "{{INCIDENT_EMAIL}}": _template_value(legal.get("incident_email") or legal.get("rpp_email"), "[courriel@example.com]"),
        "{{PHONE}}": _template_value(legal.get("phone"), "[Telephone]"),
        "{{EMAIL}}": _template_value(legal.get("email") or legal.get("rpp_email"), "[courriel@example.com]"),
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    # Générer le page.tsx React qui affiche le markdown
    page_tsx = _generate_legal_page_tsx(template, "Politique de confidentialite")
    (target_dir / "page.tsx").write_text(page_tsx)
    report.privacy_page_added = True
    logger.info("Privacy policy page generated")


def _fix_legal_page(site_dir: Path, brief: dict, report: FixReport):
    """Génère la page mentions-legales si absente."""
    target_dirs = [
        site_dir / "src" / "app" / "[locale]" / "mentions-legales",
        site_dir / "src" / "app" / "mentions-legales",
    ]

    for target_dir in target_dirs:
        if (target_dir / "page.tsx").exists():
            return

    template_path = TEMPLATES_DIR / "legal-mentions-template.md"
    if not template_path.exists():
        return

    locale_app = site_dir / "src" / "app" / "[locale]"
    if locale_app.exists():
        target_dir = locale_app / "mentions-legales"
    else:
        target_dir = site_dir / "src" / "app" / "mentions-legales"

    target_dir.mkdir(parents=True, exist_ok=True)

    template = template_path.read_text()
    legal = brief.get("legal", {})
    replacements = {
        "{{COMPANY_NAME}}": _template_value(brief.get("company_name", legal.get("company_name")), "[Nom entreprise]"),
        "{{NEQ}}": _template_value(legal.get("neq"), "[NEQ]"),
        "{{ADDRESS}}": _template_value(legal.get("address"), "[Adresse]"),
        "{{PHONE}}": _template_value(legal.get("phone"), "[Telephone]"),
        "{{EMAIL}}": _template_value(legal.get("email"), "[courriel@example.com]"),
        "{{HOSTING_PROVIDER}}": _template_value(legal.get("hosting_provider"), "Vercel Inc."),
        "{{HOSTING_ADDRESS}}": _template_value(legal.get("hosting_address"), "340 S Lemon Ave #4133, Walnut, CA 91789, USA"),
        "{{RPP_NAME}}": _template_value(legal.get("rpp_name"), "[Nom du RPP]"),
        "{{RPP_TITLE}}": _template_value(legal.get("rpp_title"), "[Titre du RPP]"),
        "{{RPP_EMAIL}}": _template_value(legal.get("rpp_email"), "[courriel@example.com]"),
    }

    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    page_tsx = _generate_legal_page_tsx(template, "Mentions legales")
    (target_dir / "page.tsx").write_text(page_tsx)
    report.legal_page_added = True
    logger.info("Legal mentions page generated")


def _generate_legal_page_tsx(markdown_content: str, title: str) -> str:
    """Génère un page.tsx Next.js qui rend du contenu légal en HTML statique."""
    # Convertir le markdown en HTML basique (headings, paragraphes, listes)
    html = _markdown_to_html(markdown_content)
    # Échapper les backticks et ${} pour le template literal
    html = html.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

    return f'''import type {{ Metadata }} from "next";

export const metadata: Metadata = {{
  title: "{title}",
}};

export default function Page() {{
  return (
    <main className="max-w-3xl mx-auto px-4 py-12">
      <article
        className="prose prose-gray max-w-none"
        dangerouslySetInnerHTML={{{{
          __html: `{html}`,
        }}}}
      />
    </main>
  );
}}
'''


def _markdown_to_html(md: str) -> str:
    """Conversion markdown simplifiée → HTML (headings, listes, paragraphes, bold)."""
    lines = md.split("\n")
    html_lines: list[str] = []
    in_list = False

    for line in lines:
        stripped = line.strip()

        # Headings
        if stripped.startswith("## "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h2>{_inline_md(stripped[3:])}</h2>")
        elif stripped.startswith("### "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h3>{_inline_md(stripped[4:])}</h3>")
        elif stripped.startswith("# "):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<h1>{_inline_md(stripped[2:])}</h1>")
        elif stripped.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{_inline_md(stripped[2:])}</li>")
        elif stripped == "":
            if in_list:
                html_lines.append("</ul>")
                in_list = False
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{_inline_md(stripped)}</p>")

    if in_list:
        html_lines.append("</ul>")

    return "\n".join(html_lines)


def _inline_md(text: str) -> str:
    """Convertit **bold** et *italic* en HTML inline."""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


# ── Fonction principale ───────────────────────────────────────────────

def auto_fix(site_dir: Path, client_dir: Path, brief: dict | None = None) -> FixReport:
    """
    Applique tous les auto-fixes D4/D8.

    Args:
        site_dir: Répertoire du site Next.js (contient package.json)
        client_dir: Répertoire client NEXOS (contient brief-client.json)
        brief: Brief client pré-chargé. Si None, tente de lire brief-client.json.
    """
    report = FixReport()

    # Charger le brief si non fourni
    if brief is None:
        brief_path = client_dir / "brief-client.json"
        if brief_path.exists():
            try:
                brief = normalize_brief(json.loads(brief_path.read_text()))
            except json.JSONDecodeError:
                brief = {}
        else:
            brief = {}
    else:
        brief = normalize_brief(brief)

    logger.info("Auto-fix D4/D8 starting")

    if _HAS_CHANGELOG:
        log_event(client_dir, EventType.AUTOFIX_START, agent="auto_fixer")

    _fix_cookie_consent(site_dir, report)
    _fix_npm_audit(site_dir, report)
    _fix_vercel_headers(site_dir, report)
    _fix_next_config(site_dir, report)
    _fix_privacy_page(site_dir, brief, report)
    _fix_legal_page(site_dir, brief, report)

    if _HAS_CHANGELOG:
        _log_applied_fixes(client_dir, report)

    logger.info("Auto-fix complete: %d fix(es)", report.total_fixes)
    return report


def _log_applied_fixes(client_dir: Path, report: FixReport) -> None:
    """Log chaque fix appliqué individuellement dans le changelog."""
    fixes = []
    if report.cookie_consent_added:
        fixes.append({"fix": "cookie_consent", "target": "layout.tsx"})
    if report.npm_audit_fixed > 0:
        fixes.append({"fix": "npm_audit", "vulns_fixed": report.npm_audit_fixed})
    if report.vercel_headers_fixed:
        fixes.append({"fix": "vercel_headers", "target": "vercel.json"})
    if report.next_config_patched:
        fixes.append({"fix": "next_config", "target": "next.config"})
    if report.privacy_page_added:
        fixes.append({"fix": "privacy_page", "target": "politique-confidentialite"})
    if report.legal_page_added:
        fixes.append({"fix": "legal_page", "target": "mentions-legales"})

    for fix_detail in fixes:
        log_event(client_dir, EventType.AUTOFIX_APPLIED, agent="auto_fixer", details=fix_detail)
