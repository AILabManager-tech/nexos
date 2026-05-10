"""Tests pour nexos.auto_fixer."""

import json
from unittest.mock import patch

from nexos.auto_fixer import (
    REQUIRED_HEADERS,
    TEMPLATES_DIR,
    FixReport,
    _fix_cookie_consent,
    _fix_legal_page,
    _fix_next_config,
    _fix_privacy_page,
    _fix_vercel_headers,
    _generate_legal_page_tsx,
    _inline_md_jsx,
    _markdown_to_jsx_children,
    auto_fix,
)


class TestFixReport:
    def test_empty_report(self):
        r = FixReport()
        assert r.total_fixes == 0

    def test_all_fixes(self):
        r = FixReport(
            cookie_consent_added=True,
            npm_audit_fixed=5,
            vercel_headers_fixed=True,
            next_config_patched=True,
            privacy_page_added=True,
            legal_page_added=True,
        )
        assert r.total_fixes == 6


class TestFixVercelHeaders:
    def test_creates_from_template(self, tmp_path):
        report = FixReport()
        _fix_vercel_headers(tmp_path, report)
        vercel_path = tmp_path / "vercel.json"

        if TEMPLATES_DIR.exists():
            assert vercel_path.exists() == report.vercel_headers_fixed

    def test_adds_missing_headers(self, tmp_path):
        vercel_path = tmp_path / "vercel.json"
        vercel_path.write_text(
            json.dumps(
                {
                    "headers": [
                        {
                            "source": "/(.*)",
                            "headers": [{"key": "X-Frame-Options", "value": "DENY"}],
                        }
                    ]
                }
            )
        )

        report = FixReport()
        _fix_vercel_headers(tmp_path, report)

        assert report.vercel_headers_fixed is True
        data = json.loads(vercel_path.read_text())
        keys = {h["key"].lower() for block in data["headers"] for h in block.get("headers", [])}
        for required in REQUIRED_HEADERS:
            assert required.lower() in keys

    def test_no_change_if_complete(self, tmp_path):
        vercel_path = tmp_path / "vercel.json"
        vercel_path.write_text(
            json.dumps(
                {
                    "headers": [
                        {
                            "source": "/(.*)",
                            "headers": [
                                {"key": k, "value": v} for k, v in REQUIRED_HEADERS.items()
                            ],
                        }
                    ]
                }
            )
        )

        report = FixReport()
        _fix_vercel_headers(tmp_path, report)
        assert report.vercel_headers_fixed is False


class TestFixNextConfig:
    def test_adds_powered_by_header(self, tmp_path):
        config = tmp_path / "next.config.mjs"
        config.write_text("const nextConfig = {\n  images: {},\n};\n")

        report = FixReport()
        _fix_next_config(tmp_path, report)

        assert report.next_config_patched is True
        assert "poweredByHeader: false" in config.read_text()

    def test_fixes_true_to_false(self, tmp_path):
        config = tmp_path / "next.config.mjs"
        config.write_text("const nextConfig = {\n  poweredByHeader: true,\n};\n")

        report = FixReport()
        _fix_next_config(tmp_path, report)

        content = config.read_text()
        assert "poweredByHeader: false" in content
        assert "poweredByHeader: true" not in content

    def test_no_change_if_already_false(self, tmp_path):
        config = tmp_path / "next.config.mjs"
        config.write_text("const nextConfig = {\n  poweredByHeader: false,\n};\n")

        report = FixReport()
        _fix_next_config(tmp_path, report)
        assert report.next_config_patched is False

    def test_no_config_file(self, tmp_path):
        report = FixReport()
        _fix_next_config(tmp_path, report)
        assert report.next_config_patched is False


class TestFixCookieConsent:
    def test_copies_template_and_injects(self, tmp_path):
        # Créer structure minimale
        components = tmp_path / "src" / "components"
        components.mkdir(parents=True)
        layout_dir = tmp_path / "src" / "app" / "[locale]"
        layout_dir.mkdir(parents=True)
        layout = layout_dir / "layout.tsx"
        layout.write_text(
            'import "./globals.css";\n'
            "export default function Layout({ children }) {\n"
            "  return (\n"
            "    <html>\n"
            "      <body>\n"
            "        {children}\n"
            "      </body>\n"
            "    </html>\n"
            "  );\n"
            "}\n"
        )

        report = FixReport()
        _fix_cookie_consent(tmp_path, report)

        # Vérifier que le template a été copié
        consent_file = components / "cookie-consent.tsx"
        if TEMPLATES_DIR.exists() and (TEMPLATES_DIR / "cookie-consent-component.tsx").exists():
            assert consent_file.exists()
            # Vérifier l'injection dans layout
            content = layout.read_text()
            assert "<CookieConsent" in content
            assert "import { CookieConsent }" in content
            assert report.cookie_consent_added is True

    def test_skips_if_already_present(self, tmp_path):
        components = tmp_path / "src" / "components"
        components.mkdir(parents=True)
        (components / "cookie-consent.tsx").write_text("export function CookieConsent() {}")

        layout_dir = tmp_path / "src" / "app"
        layout_dir.mkdir(parents=True)
        layout = layout_dir / "layout.tsx"
        layout.write_text(
            'import { CookieConsent } from "@/components/cookie-consent";\n'
            "<body>\n  {children}\n  <CookieConsent />\n</body>\n"
        )

        report = FixReport()
        _fix_cookie_consent(tmp_path, report)
        assert report.cookie_consent_added is False


class TestFixLegalPages:
    def test_privacy_page_created(self, tmp_path):
        locale_dir = tmp_path / "src" / "app" / "[locale]"
        locale_dir.mkdir(parents=True)

        report = FixReport()
        brief = {"company_name": "TestCo", "legal": {"rpp_name": "Jean Test"}}
        _fix_privacy_page(tmp_path, brief, report)

        page = locale_dir / "politique-confidentialite" / "page.tsx"
        if TEMPLATES_DIR.exists() and (TEMPLATES_DIR / "privacy-policy-template.md").exists():
            assert page.exists()
            assert report.privacy_page_added is True
            content = page.read_text()
            assert "TestCo" in content

    def test_legal_page_created(self, tmp_path):
        locale_dir = tmp_path / "src" / "app" / "[locale]"
        locale_dir.mkdir(parents=True)

        report = FixReport()
        brief = {"company_name": "TestCo", "legal": {"neq": "12345"}}
        _fix_legal_page(tmp_path, brief, report)

        page = locale_dir / "mentions-legales" / "page.tsx"
        if TEMPLATES_DIR.exists() and (TEMPLATES_DIR / "legal-mentions-template.md").exists():
            assert page.exists()
            assert report.legal_page_added is True

    def test_skips_if_exists(self, tmp_path):
        page_dir = tmp_path / "src" / "app" / "[locale]" / "politique-confidentialite"
        page_dir.mkdir(parents=True)
        (page_dir / "page.tsx").write_text("existing")

        report = FixReport()
        _fix_privacy_page(tmp_path, {}, report)
        assert report.privacy_page_added is False


class TestMarkdownToJsx:
    def test_heading(self):
        assert "<h1>" in _markdown_to_jsx_children("# Title")
        assert "<h2>" in _markdown_to_jsx_children("## Sub")
        assert "<h3>" in _markdown_to_jsx_children("### Sub2")

    def test_list(self):
        jsx = _markdown_to_jsx_children("- item 1\n- item 2")
        assert "<ul>" in jsx
        assert "<li>item 1</li>" in jsx
        assert "</ul>" in jsx

    def test_bold(self):
        assert "<strong>bold</strong>" in _inline_md_jsx("**bold**")

    def test_italic(self):
        assert "<em>italic</em>" in _inline_md_jsx("*italic*")

    def test_paragraph(self):
        jsx = _markdown_to_jsx_children("Just a paragraph.")
        assert "<p>Just a paragraph.</p>" in jsx

    def test_jsx_special_chars_escaped(self):
        """Les caractères qui casseraient la syntaxe JSX (`<`, `>`, `{`, `}`,
        `&`) doivent être échappés en HTML entities, sinon le fichier produit
        ne compile pas."""
        jsx = _inline_md_jsx("a < b > c & d {x} {y}")
        assert "<" not in jsx.replace("&lt;", "")
        assert ">" not in jsx.replace("&gt;", "")
        assert "{" not in jsx.replace("&#123;", "")
        assert "}" not in jsx.replace("&#125;", "")
        assert "&amp;" in jsx

    def test_bold_with_special_chars_inside(self):
        """L'escape doit s'appliquer avant la conversion bold, pour que les
        tags JSX ne soient pas eux-mêmes échappés."""
        jsx = _inline_md_jsx("**a < b**")
        assert "<strong>a &lt; b</strong>" in jsx


class TestGenerateLegalPageTsx:
    def test_no_dangerously_set_inner_html(self):
        """Régression A-006 niveau 3 : le générateur ne doit JAMAIS émettre
        `dangerouslySetInnerHTML` (viol CLAUDE.md règle XSS)."""
        page = _generate_legal_page_tsx("# Politique\n\nDu texte.", "Politique")
        assert "dangerouslySetInnerHTML" not in page

    def test_xss_payload_neutralized(self):
        """Si un brief client contient un payload XSS, le tag <script> doit
        être échappé en entities HTML, pas rendu comme un élément exécutable."""
        page = _generate_legal_page_tsx(
            "# Page\n\n<script>alert('xss')</script>",
            "Page",
        )
        assert "<script>alert" not in page
        assert "&lt;script&gt;" in page

    def test_jsx_braces_escaped(self):
        """Un `{...}` dans le contenu textuel ne doit pas être interprété
        comme expression JSX."""
        page = _generate_legal_page_tsx("# T\n\nVoir {COMPANY}.", "T")
        assert "Voir &#123;COMPANY&#125;." in page

    def test_metadata_title_quotes_escaped(self):
        page = _generate_legal_page_tsx("# T", 'Title with "quotes"')
        assert 'title: "Title with \\"quotes\\""' in page

    def test_includes_article_wrapper(self):
        page = _generate_legal_page_tsx("# T", "T")
        assert '<article className="prose prose-gray max-w-none">' in page
        assert "</article>" in page


class TestAutoFix:
    @patch("nexos.auto_fixer._fix_legal_page")
    @patch("nexos.auto_fixer._fix_privacy_page")
    @patch("nexos.auto_fixer._fix_next_config")
    @patch("nexos.auto_fixer._fix_vercel_headers")
    @patch("nexos.auto_fixer._fix_npm_audit")
    @patch("nexos.auto_fixer._fix_cookie_consent")
    def test_calls_all_fixers(self, m1, m2, m3, m4, m5, m6, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        site_dir = tmp_path / "site"
        site_dir.mkdir()

        auto_fix(site_dir, client_dir, brief={"company_name": "Test"})

        m1.assert_called_once()
        m2.assert_called_once()
        m3.assert_called_once()
        m4.assert_called_once()
        m5.assert_called_once()
        m6.assert_called_once()

    def test_loads_brief_from_file(self, tmp_path):
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        brief_path = client_dir / "brief-client.json"
        brief_path.write_text(json.dumps({"company_name": "FromFile"}))

        site_dir = tmp_path / "site"
        site_dir.mkdir()

        # Should not raise — brief loaded from file
        report = auto_fix(site_dir, client_dir, brief=None)
        assert isinstance(report, FixReport)
