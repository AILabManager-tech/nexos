"""Tests pour nexos.auto_fixer."""

import dataclasses
import json
import re
from pathlib import Path
from typing import ClassVar
from unittest.mock import patch

import pytest

from nexos.auto_fixer import (
    _VALID_SOIC_DIMENSIONS,
    DEFAULT_CSP,
    DRY_RUN_DESCRIBERS,
    FIXER_ORDER,
    REQUIRED_HEADERS,
    TEMPLATES_DIR,
    Fixer,
    FixReport,
    _contrast_ratio,
    _fix_cookie_consent,
    _fix_csp_middleware,
    _fix_legal_page,
    _fix_next_config,
    _fix_pa11y_contrast,
    _fix_privacy_page,
    _fix_readme,
    _fix_vercel_headers,
    _generate_legal_page_tsx,
    _harden_token_contrast,
    _hex_to_rgb,
    _inline_md_jsx,
    _markdown_to_jsx_children,
    _read_csp_from_vercel,
    _relative_luminance,
    auto_fix,
    describe_auto_fix,
    fixers_for_dimensions,
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
            csp_added=True,
            csp_middleware_added=True,
            readme_added=True,
            next_config_patched=True,
            privacy_page_added=True,
            legal_page_added=True,
        )
        assert r.total_fixes == 9


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


class TestReadCspFromVercel:
    """Lecture CSP depuis vercel.json — single source of truth (P4a)."""

    def test_returns_none_when_vercel_missing(self, tmp_path):
        assert _read_csp_from_vercel(tmp_path / "vercel.json") is None

    def test_returns_none_when_no_csp_header(self, tmp_path):
        path = tmp_path / "vercel.json"
        path.write_text(
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
        assert _read_csp_from_vercel(path) is None

    def test_returns_csp_value_when_present(self, tmp_path):
        custom_csp = "default-src 'self'; script-src 'self' 'nonce-xyz'"
        path = tmp_path / "vercel.json"
        path.write_text(
            json.dumps(
                {
                    "headers": [
                        {
                            "source": "/(.*)",
                            "headers": [{"key": "Content-Security-Policy", "value": custom_csp}],
                        }
                    ]
                }
            )
        )
        assert _read_csp_from_vercel(path) == custom_csp

    def test_returns_none_on_corrupted_json(self, tmp_path):
        path = tmp_path / "vercel.json"
        path.write_text("{ this is not valid json")
        assert _read_csp_from_vercel(path) is None


class TestFixCspMiddleware:
    """Création middleware.ts local pour aligner CSP dev sur prod (P4a)."""

    def _write_vercel_with_csp(self, site_dir, csp=DEFAULT_CSP):
        (site_dir / "vercel.json").write_text(
            json.dumps(
                {
                    "headers": [
                        {
                            "source": "/(.*)",
                            "headers": [{"key": "Content-Security-Policy", "value": csp}],
                        }
                    ]
                }
            )
        )

    def test_creates_middleware_when_csp_present(self, tmp_path):
        self._write_vercel_with_csp(tmp_path)
        report = FixReport()
        _fix_csp_middleware(tmp_path, report)
        middleware = tmp_path / "middleware.ts"
        assert middleware.exists()
        assert report.csp_middleware_added is True
        content = middleware.read_text()
        # Le middleware encode la CSP via json.dumps → guillemets doubles
        assert "Content-Security-Policy" in content
        assert "process.env.VERCEL" in content
        # CSP value présente (json.dumps préserve les guillemets simples)
        assert "'self'" in content

    def test_skips_when_vercel_has_no_csp(self, tmp_path):
        (tmp_path / "vercel.json").write_text(json.dumps({"headers": []}))
        report = FixReport()
        _fix_csp_middleware(tmp_path, report)
        assert not (tmp_path / "middleware.ts").exists()
        assert report.csp_middleware_added is False

    def test_skips_when_vercel_missing(self, tmp_path):
        report = FixReport()
        _fix_csp_middleware(tmp_path, report)
        assert not (tmp_path / "middleware.ts").exists()
        assert report.csp_middleware_added is False

    def test_skips_when_middleware_already_exists(self, tmp_path):
        self._write_vercel_with_csp(tmp_path)
        existing = tmp_path / "middleware.ts"
        existing.write_text("// builder custom middleware")
        report = FixReport()
        _fix_csp_middleware(tmp_path, report)
        # Le contenu existant n'est PAS écrasé (respect décision builder)
        assert existing.read_text() == "// builder custom middleware"
        assert report.csp_middleware_added is False

    def test_skips_when_src_middleware_exists(self, tmp_path):
        """Détecte aussi src/middleware.ts (convention Next.js alternative)."""
        self._write_vercel_with_csp(tmp_path)
        src_dir = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / "middleware.ts").write_text("// existing")
        report = FixReport()
        _fix_csp_middleware(tmp_path, report)
        assert not (tmp_path / "middleware.ts").exists()
        assert report.csp_middleware_added is False

    def test_csp_value_correctly_encoded_as_ts_literal(self, tmp_path):
        """Caractères spéciaux (guillemets, accents) correctement échappés."""
        tricky_csp = 'default-src "self"; report-uri /csp-report'
        self._write_vercel_with_csp(tmp_path, csp=tricky_csp)
        report = FixReport()
        _fix_csp_middleware(tmp_path, report)
        content = (tmp_path / "middleware.ts").read_text()
        # Les guillemets doubles dans la CSP doivent être échappés via json.dumps
        assert '\\"self\\"' in content


class TestFixReadme:
    """Tests _fix_readme (D5 — gain D2 documentation)."""

    def test_creates_readme_when_missing(self, tmp_path):
        report = FixReport()
        _fix_readme(tmp_path, {"company": {"name": "TestCo"}}, report)
        readme = tmp_path / "README.md"
        assert readme.exists()
        assert report.readme_added is True
        content = readme.read_text()
        assert "TestCo" in content
        assert "Next.js" in content
        assert "Loi 25" in content

    def test_skips_when_readme_exists(self, tmp_path):
        existing = tmp_path / "README.md"
        existing.write_text("# Custom builder README")
        report = FixReport()
        _fix_readme(tmp_path, {"company": {"name": "TestCo"}}, report)
        # Le README existant n'est PAS écrasé
        assert existing.read_text() == "# Custom builder README"
        assert report.readme_added is False

    def test_fallback_company_name(self, tmp_path):
        """Sans brief.company.name, utilise company_name top-level ou fallback."""
        report = FixReport()
        _fix_readme(tmp_path, {"company_name": "FromTopLevel"}, report)
        content = (tmp_path / "README.md").read_text()
        assert "FromTopLevel" in content

    def test_ultimate_fallback_no_name(self, tmp_path):
        """Brief vide → fallback générique 'Site web'."""
        report = FixReport()
        _fix_readme(tmp_path, {}, report)
        content = (tmp_path / "README.md").read_text()
        assert "Site web" in content


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


# ── P8.1 : pipeline + idempotence ────────────────────────────────────


class TestFixerOrder:
    """`FIXER_ORDER` est la source de vérité du pipeline auto-fix (P8.1).

    L'ordre est volontairement linéaire et hardcodé — pas de topo-sort. Ces
    tests verrouillent les invariants : noms exposés, dépendances entre
    fixers (csp après vercel_headers, csp_middleware après csp), et
    file-ownership pour les fichiers touchés par plusieurs fixers.
    """

    def test_fixer_order_is_a_list_of_fixers(self):
        assert isinstance(FIXER_ORDER, list)
        assert all(isinstance(f, Fixer) for f in FIXER_ORDER)
        # frozen=True : on ne peut pas muter un Fixer publié
        with pytest.raises(dataclasses.FrozenInstanceError):
            FIXER_ORDER[0].name = "mutated"  # type: ignore[misc]

    def test_fixer_names_are_unique_and_stable(self):
        names = [f.name for f in FIXER_ORDER]
        assert names == [
            "cookie_consent",
            "npm_audit",
            "vercel_headers",
            "csp",
            "csp_middleware",
            "next_config",
            "privacy_page",
            "legal_page",
            "readme",
            "pa11y_contrast",  # P8.6 — D6 contrast tokens
        ]
        assert len(set(names)) == len(names)

    def test_csp_runs_after_vercel_headers(self):
        """`_fix_csp` ajoute la CSP au bloc `/(.*)` créé par `_fix_vercel_headers`.
        Inverser l'ordre ferait sortir un warning « missing global headers block »."""
        names = [f.name for f in FIXER_ORDER]
        assert names.index("vercel_headers") < names.index("csp")

    def test_csp_middleware_runs_after_csp(self):
        """`_fix_csp_middleware` lit la CSP via `_read_csp_from_vercel` — le
        header doit déjà être présent au moment où le middleware est généré."""
        names = [f.name for f in FIXER_ORDER]
        assert names.index("csp") < names.index("csp_middleware")

    def test_vercel_json_is_shared_by_vercel_headers_then_csp(self):
        """Documenté explicitement : 2 fixers touchent vercel.json, dans cet ordre."""
        owners = [f.name for f in FIXER_ORDER if f.target == "vercel.json"]
        assert owners == ["vercel_headers", "csp"]

    def test_targets_are_non_empty_strings(self):
        for fixer in FIXER_ORDER:
            assert isinstance(fixer.target, str) and fixer.target.strip()

    def test_auto_fix_iterates_in_declared_order(self, tmp_path):
        """`auto_fix` doit appeler les fixers dans l'ordre de `FIXER_ORDER`,
        pas dans un ordre fonction-par-fonction codé en dur."""
        call_order: list[str] = []

        def _make_recorder(name: str):
            def _record(*_args, **_kwargs):
                call_order.append(name)

            return _record

        patches = [
            patch(f"nexos.auto_fixer._fix_{f.name}", _make_recorder(f.name)) for f in FIXER_ORDER
        ]
        client_dir = tmp_path / "client"
        client_dir.mkdir()
        site_dir = tmp_path / "site"
        site_dir.mkdir()

        for p in patches:
            p.start()
        try:
            auto_fix(site_dir, client_dir, brief={"company_name": "Test"})
        finally:
            for p in patches:
                p.stop()

        assert call_order == [f.name for f in FIXER_ORDER]


class TestFixerDimensions:
    """P8.3 — chaque Fixer porte sa dimension SOIC primaire, et le helper
    `fixers_for_dimensions()` permet de filtrer FIXER_ORDER pour le routing
    dimension-scoped déclenché par ENRICHED_RETRY (cf. PlateauDiagnosis).

    Invariants verrouillés :
    1. Chaque Fixer a une dimension non-vide ∈ {D1..D9}.
    2. Le mapping nom→dimension est figé (changement = breaking, doit être conscient).
    3. Le filtrage par dimension préserve l'ordre global de FIXER_ORDER.
    4. Les dimensions bloquantes D4 et D8 sont effectivement couvertes.
    """

    def test_every_fixer_has_a_dimension(self):
        for fixer in FIXER_ORDER:
            assert isinstance(fixer.dimension, str)
            assert fixer.dimension, f"Fixer {fixer.name!r} sans dimension"

    def test_fixer_dimensions_are_valid_soic(self):
        """Chaque dimension annotée doit être une vraie dimension SOIC (D1..D9).
        Détecte les fautes de frappe ("D04", "D-4", "d4") qui rendraient le
        fixer invisible au routing dimension-scoped."""
        for fixer in FIXER_ORDER:
            assert fixer.dimension in _VALID_SOIC_DIMENSIONS, (
                f"Fixer {fixer.name!r} : dimension {fixer.dimension!r} "
                f"hors {sorted(_VALID_SOIC_DIMENSIONS)}"
            )

    def test_fixer_dimensions_are_stable_mapping(self):
        """Mapping nom→dimension figé : tout changement ici doit être un acte
        conscient (et casser ce test rappelle de mettre à jour le routing
        ENRICHED_RETRY + la doc CLAUDE.md)."""
        mapping = {f.name: f.dimension for f in FIXER_ORDER}
        assert mapping == {
            "cookie_consent": "D8",
            "npm_audit": "D4",
            "vercel_headers": "D4",
            "csp": "D4",
            "csp_middleware": "D4",
            "next_config": "D4",
            "privacy_page": "D8",
            "legal_page": "D8",
            "readme": "D2",
            "pa11y_contrast": "D6",  # P8.6
        }

    def test_fixers_for_dimensions_d4_subset_in_global_order(self):
        """Filtrer sur D4 retourne les 5 fixers sécurité dans l'ordre déclaré
        de FIXER_ORDER (npm_audit puis vercel_headers puis csp etc.)."""
        names = [f.name for f in fixers_for_dimensions({"D4"})]
        assert names == ["npm_audit", "vercel_headers", "csp", "csp_middleware", "next_config"]

    def test_fixers_for_dimensions_d8_subset_in_global_order(self):
        """Filtrer sur D8 retourne les 3 fixers Loi 25 (cookie_consent d'abord
        car position globale 0, puis privacy_page, puis legal_page)."""
        names = [f.name for f in fixers_for_dimensions({"D8"})]
        assert names == ["cookie_consent", "privacy_page", "legal_page"]

    def test_fixers_for_dimensions_d2_subset(self):
        names = [f.name for f in fixers_for_dimensions({"D2"})]
        assert names == ["readme"]

    def test_fixers_for_dimensions_d6_subset(self):
        """P8.6 — D6 routing via pa11y_contrast (Tailwind palette tokens)."""
        names = [f.name for f in fixers_for_dimensions({"D6"})]
        assert names == ["pa11y_contrast"]

    def test_fixers_for_dimensions_multi_preserves_global_order(self):
        """Multi-dimensions : l'ordre global de FIXER_ORDER est préservé,
        pas l'ordre des dimensions demandées. Ex: D8 + D4 doit donner
        cookie_consent (idx 0) avant npm_audit (idx 1) etc."""
        names = [f.name for f in fixers_for_dimensions({"D8", "D4"})]
        assert names == [
            "cookie_consent",  # D8 mais position 0 dans FIXER_ORDER
            "npm_audit",
            "vercel_headers",
            "csp",
            "csp_middleware",
            "next_config",
            "privacy_page",
            "legal_page",
        ]

    def test_fixers_for_dimensions_unknown_returns_empty(self):
        """Dimension hors {D1..D9} ou non couverte : retourne [] sans erreur.
        Cas d'usage : plateau sur D5 (Performance) — aucun fixer disponible
        aujourd'hui, le call site logge le gap et continue sans crash.

        Gaps connus 2026-05-17 : D1, D3, D5, D7, D9 (D6 désormais couvert par
        `pa11y_contrast` P8.6 ; D2/D4/D8 historiquement couverts)."""
        assert fixers_for_dimensions({"DXX"}) == []
        assert fixers_for_dimensions({"D5"}) == []  # gap de couverture connu
        assert fixers_for_dimensions({"D1", "D3", "D7", "D9"}) == []

    def test_fixers_for_dimensions_empty_iterable_returns_empty(self):
        assert fixers_for_dimensions(set()) == []
        assert fixers_for_dimensions([]) == []
        assert fixers_for_dimensions(()) == []

    def test_blocking_dimensions_d4_d8_have_at_least_one_fixer(self):
        """Les dimensions bloquantes SOIC (cf. soic/converger.py _BLOCKING_DIMENSIONS)
        DOIVENT avoir au moins un fixer disponible. Sinon, un plateau bloquant
        sur D4 ou D8 ne pourrait jamais être auto-corrigé sans intervention LLM."""
        for blocking in ("D4", "D8"):
            assert fixers_for_dimensions({blocking}), (
                f"Dimension bloquante {blocking} sans fixer — régression critique P8.3"
            )

    def test_fixer_dimension_filtering_is_deterministic(self):
        """Deux appels successifs avec la même dimension retournent la même
        liste, même Fixer objects (frozen=True, donc identité préservée)."""
        a = fixers_for_dimensions({"D4"})
        b = fixers_for_dimensions({"D4"})
        assert a == b
        for fa, fb in zip(a, b, strict=True):
            assert fa is fb  # même instance Fixer (FIXER_ORDER est une const)


def _build_minimal_site(site_dir: Path) -> None:
    """Site Next.js minimal (App Router i18n) utilisé par les tests d'idempotence.

    Volontairement très réduit : juste de quoi laisser chaque fixer s'appliquer
    sans crasher (layout.tsx pour cookie consent, next.config.mjs pour le patch
    poweredByHeader, app/[locale] pour les pages légales).
    """
    locale_dir = site_dir / "app" / "[locale]"
    locale_dir.mkdir(parents=True)
    (locale_dir / "layout.tsx").write_text(
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
    (site_dir / "next.config.mjs").write_text(
        "const nextConfig = {\n  reactStrictMode: true,\n};\nexport default nextConfig;\n"
    )
    (site_dir / "package.json").write_text('{"name": "test-site", "version": "1.0.0"}\n')
    (site_dir / "components").mkdir()


@patch("nexos.auto_fixer._fix_npm_audit")
class TestIdempotence:
    """`auto_fix()` doit être idempotent : ré-appliquer le pipeline N fois sur
    le même site ne doit (a) ajouter aucun fix au-delà du premier passage,
    (b) ne pas dupliquer de contenu (headers, imports, balises JSX), et
    (c) laisser tous les fichiers bit-identiques entre run 2 et run N (P8.1).

    `_fix_npm_audit` est mocké globalement pour éviter un subprocess npm sur
    un site sans node_modules (subprocess capture l'erreur mais reste lent).
    """

    BRIEF: ClassVar[dict] = {
        "company_name": "TestCo",
        "legal": {
            "rpp_name": "Jean Test",
            "rpp_title": "DPO",
            "rpp_email": "rpp@test.example",
            "neq": "1234567890",
        },
    }

    def _setup(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        _build_minimal_site(site)
        client = tmp_path / "client"
        client.mkdir()
        return site, client

    def test_total_fixes_drops_to_zero_after_first_run(self, _mock_npm, tmp_path):
        site, client = self._setup(tmp_path)
        report1 = auto_fix(site, client, brief=self.BRIEF)
        report2 = auto_fix(site, client, brief=self.BRIEF)
        report3 = auto_fix(site, client, brief=self.BRIEF)
        assert report1.total_fixes >= 1, "Premier run doit appliquer au moins 1 fix"
        assert report2.total_fixes == 0, "Second run doit être no-op"
        assert report3.total_fixes == 0, "Troisième run doit aussi être no-op"

    def test_files_are_bit_identical_across_runs(self, _mock_npm, tmp_path):
        site, client = self._setup(tmp_path)
        auto_fix(site, client, brief=self.BRIEF)

        watched = [
            "vercel.json",
            "middleware.ts",
            "next.config.mjs",
            "app/[locale]/layout.tsx",
            "app/[locale]/politique-confidentialite/page.tsx",
            "app/[locale]/mentions-legales/page.tsx",
            "README.md",
        ]
        snapshots = {f: (site / f).read_bytes() for f in watched if (site / f).exists()}
        assert snapshots, "Au moins un fichier doit avoir été créé par le premier run"

        for _ in range(2):
            auto_fix(site, client, brief=self.BRIEF)

        for relpath, expected in snapshots.items():
            current = (site / relpath).read_bytes()
            assert current == expected, f"{relpath} a changé entre run 1 et run 3"

    def test_vercel_headers_no_duplicate_keys(self, _mock_npm, tmp_path):
        site, client = self._setup(tmp_path)
        for _ in range(3):
            auto_fix(site, client, brief=self.BRIEF)

        data = json.loads((site / "vercel.json").read_text())
        global_block = next(b for b in data["headers"] if b["source"] == "/(.*)")
        keys = [h["key"] for h in global_block["headers"]]
        assert len(keys) == len(set(keys)), (
            f"Headers dupliqués dans vercel.json après 3 passes : {keys}"
        )

    def test_csp_appears_exactly_once_in_vercel(self, _mock_npm, tmp_path):
        site, client = self._setup(tmp_path)
        for _ in range(3):
            auto_fix(site, client, brief=self.BRIEF)

        data = json.loads((site / "vercel.json").read_text())
        global_block = next(b for b in data["headers"] if b["source"] == "/(.*)")
        csp_headers = [
            h for h in global_block["headers"] if h["key"].lower() == "content-security-policy"
        ]
        assert len(csp_headers) == 1, f"CSP devrait apparaître 1 fois, vu {len(csp_headers)}"

    def test_cookie_consent_injected_exactly_once(self, _mock_npm, tmp_path):
        site, client = self._setup(tmp_path)
        for _ in range(3):
            auto_fix(site, client, brief=self.BRIEF)

        layout = (site / "app" / "[locale]" / "layout.tsx").read_text()
        assert layout.count("<CookieConsent") == 1, (
            "<CookieConsent /> doit apparaître exactement 1 fois"
        )
        assert layout.count("import { CookieConsent }") == 1, (
            "L'import CookieConsent doit apparaître exactement 1 fois"
        )

    def test_next_config_powered_by_added_once(self, _mock_npm, tmp_path):
        site, client = self._setup(tmp_path)
        for _ in range(3):
            auto_fix(site, client, brief=self.BRIEF)

        content = (site / "next.config.mjs").read_text()
        assert content.count("poweredByHeader: false") == 1
        assert "poweredByHeader: true" not in content

    def test_middleware_csp_value_matches_vercel(self, _mock_npm, tmp_path):
        """Le middleware.ts généré localement doit refléter la CSP de vercel.json
        (single source of truth). Re-runner ne doit pas désync les deux."""
        site, client = self._setup(tmp_path)
        for _ in range(3):
            auto_fix(site, client, brief=self.BRIEF)

        vercel_data = json.loads((site / "vercel.json").read_text())
        global_block = next(b for b in vercel_data["headers"] if b["source"] == "/(.*)")
        csp_in_vercel = next(
            h["value"] for h in global_block["headers"] if h["key"] == "Content-Security-Policy"
        )

        middleware = (site / "middleware.ts").read_text()
        # CSP encodée en JSON literal — guillemets simples préservés
        assert csp_in_vercel in middleware or json.dumps(csp_in_vercel)[1:-1] in middleware


@patch("nexos.auto_fixer._fix_npm_audit")
class TestAutoFixDimensions:
    """P8.3 — `auto_fix(..., dimensions=...)` ne déclenche QUE les fixers dont
    `Fixer.dimension` appartient à l'ensemble fourni. `dimensions=None` (défaut)
    conserve le comportement P8.1 (tous les fixers). `dimensions=set()` est
    distinct de `None` : explicitement aucun fixer.

    Cas d'usage primaire : routing déclenché par `PlateauDiagnosis.failing_dimensions`
    sur `Decision.ENRICHED_RETRY`. Si SOIC plateau sur D4 uniquement, seuls les
    5 fixers D4 s'exécutent — pas de bruit sur D2/D8.
    """

    BRIEF: ClassVar[dict] = {
        "company_name": "TestCo",
        "legal": {
            "rpp_name": "Jean Test",
            "rpp_title": "DPO",
            "rpp_email": "rpp@test.example",
            "neq": "1234567890",
        },
    }

    def _setup(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        _build_minimal_site(site)
        client = tmp_path / "client"
        client.mkdir()
        return site, client

    def test_dimensions_d4_only_touches_d4_files(self, _mock_npm, tmp_path):
        """Run dim-scoped D4 : vercel.json + middleware.ts + next.config.mjs
        sont touchés, MAIS aucun fichier D2 (README) ni D8 (cookie + pages
        légales) n'est créé."""
        site, client = self._setup(tmp_path)
        auto_fix(site, client, brief=self.BRIEF, dimensions={"D4"})

        # D4 — doivent exister
        assert (site / "vercel.json").exists(), "D4: vercel.json absent"
        assert (site / "middleware.ts").exists(), "D4: middleware.ts absent"
        next_config = (site / "next.config.mjs").read_text()
        assert "poweredByHeader: false" in next_config, "D4: next.config pas patché"

        # D8 — NE DOIVENT PAS exister
        assert not (
            site / "app" / "[locale]" / "politique-confidentialite" / "page.tsx"
        ).exists(), "D8 fuite : privacy page créée alors que dimensions={D4}"
        assert not (site / "app" / "[locale]" / "mentions-legales" / "page.tsx").exists(), (
            "D8 fuite : legal page créée alors que dimensions={D4}"
        )
        layout = (site / "app" / "[locale]" / "layout.tsx").read_text()
        assert "<CookieConsent" not in layout, "D8 fuite : cookie consent injecté"

        # D2 — NE DOIT PAS exister
        assert not (site / "README.md").exists(), "D2 fuite : README créé alors que dimensions={D4}"

    def test_dimensions_d8_only_touches_d8_files(self, _mock_npm, tmp_path):
        """Symétrique : dim-scoped D8 → cookie + pages légales, pas vercel.json
        ni README. Note : `_fix_csp_middleware` requiert vercel.json avec CSP
        donc en D8 isolé il ne fait rien — comportement attendu (skip défensif)."""
        site, client = self._setup(tmp_path)
        auto_fix(site, client, brief=self.BRIEF, dimensions={"D8"})

        # D8 — doivent exister
        assert (site / "app" / "[locale]" / "politique-confidentialite" / "page.tsx").exists(), (
            "D8: privacy page absente"
        )
        assert (site / "app" / "[locale]" / "mentions-legales" / "page.tsx").exists(), (
            "D8: legal page absente"
        )
        layout = (site / "app" / "[locale]" / "layout.tsx").read_text()
        assert "<CookieConsent" in layout, "D8: cookie consent absent"

        # D4 — NE DOIVENT PAS exister
        assert not (site / "vercel.json").exists(), "D4 fuite : vercel.json créé"
        assert not (site / "middleware.ts").exists(), "D4 fuite : middleware.ts créé"

        # D2 — NE DOIT PAS exister
        assert not (site / "README.md").exists(), "D2 fuite : README créé"

    def test_dimensions_none_preserves_p81_behavior(self, _mock_npm, tmp_path):
        """Rétrocompat : `dimensions=None` (défaut) doit donner exactement le
        même résultat que P8.1 — tous les fichiers de tous les fixers."""
        site, client = self._setup(tmp_path)
        report = auto_fix(site, client, brief=self.BRIEF, dimensions=None)

        # Tous les fichiers de toutes les dimensions doivent exister
        assert (site / "vercel.json").exists()  # D4
        assert (site / "middleware.ts").exists()  # D4
        assert (site / "app" / "[locale]" / "politique-confidentialite" / "page.tsx").exists()  # D8
        assert (site / "app" / "[locale]" / "mentions-legales" / "page.tsx").exists()  # D8
        assert (site / "README.md").exists()  # D2
        assert report.total_fixes >= 1

    def test_dimensions_empty_set_runs_nothing(self, _mock_npm, tmp_path):
        """`dimensions=set()` distinct de `None` : filtre explicite = aucun
        fixer. `total_fixes == 0`. Pas de fichier créé."""
        site, client = self._setup(tmp_path)
        report = auto_fix(site, client, brief=self.BRIEF, dimensions=set())

        assert report.total_fixes == 0
        assert not (site / "vercel.json").exists()
        assert not (site / "middleware.ts").exists()
        assert not (site / "README.md").exists()
        assert not (site / "app" / "[locale]" / "politique-confidentialite" / "page.tsx").exists()

    def test_dimensions_uncovered_d5_runs_nothing_without_crash(self, _mock_npm, tmp_path):
        """Plateau sur dimension non couverte (D5 Performance, D6 a11y, etc.)
        ne doit pas lever. Le call site logge le gap, la pipeline continue."""
        site, client = self._setup(tmp_path)
        report = auto_fix(site, client, brief=self.BRIEF, dimensions={"D5", "D6", "D9"})

        assert report.total_fixes == 0
        # Aucun fichier créé (D4/D8/D2 pas dans la liste)
        assert not (site / "vercel.json").exists()
        assert not (site / "README.md").exists()

    def test_dimensions_idempotent_dim_scoped(self, _mock_npm, tmp_path):
        """Idempotence dim-scoped : `auto_fix(dimensions={D4})` appelé 3x sur
        le même site reste bit-identique. Garantit qu'un plateau qui re-déclenche
        le hook sur la même dimension n'introduit aucune corruption."""
        site, client = self._setup(tmp_path)
        report1 = auto_fix(site, client, brief=self.BRIEF, dimensions={"D4"})
        vercel_snapshot = (site / "vercel.json").read_bytes()
        middleware_snapshot = (site / "middleware.ts").read_bytes()
        config_snapshot = (site / "next.config.mjs").read_bytes()

        report2 = auto_fix(site, client, brief=self.BRIEF, dimensions={"D4"})
        report3 = auto_fix(site, client, brief=self.BRIEF, dimensions={"D4"})

        assert report1.total_fixes >= 1
        assert report2.total_fixes == 0
        assert report3.total_fixes == 0
        assert (site / "vercel.json").read_bytes() == vercel_snapshot
        assert (site / "middleware.ts").read_bytes() == middleware_snapshot
        assert (site / "next.config.mjs").read_bytes() == config_snapshot

    def test_dimensions_combined_d4_d8_runs_both_subsets(self, _mock_npm, tmp_path):
        """Plateau sur 2 dimensions (cas typique : D4 + D8 ensemble) → les 2
        sous-ensembles s'exécutent dans l'ordre global de FIXER_ORDER."""
        site, client = self._setup(tmp_path)
        auto_fix(site, client, brief=self.BRIEF, dimensions={"D4", "D8"})

        # Les deux dimensions doivent être servies
        assert (site / "vercel.json").exists()  # D4
        assert (site / "middleware.ts").exists()  # D4
        assert (site / "app" / "[locale]" / "politique-confidentialite" / "page.tsx").exists()  # D8
        assert (site / "app" / "[locale]" / "mentions-legales" / "page.tsx").exists()  # D8

        # D2 reste exclu
        assert not (site / "README.md").exists()


class TestWcagContrastHelpers:
    """P8.6 — unit tests for the pure WCAG math: hex parsing, relative
    luminance, contrast ratio. These functions are the load-bearing
    primitives of `_fix_pa11y_contrast`. If any of them drift, the fixer
    silently produces wrong palette values."""

    def test_hex_to_rgb_six_digit(self):
        assert _hex_to_rgb("#000000") == (0.0, 0.0, 0.0)
        r, g, b = _hex_to_rgb("#FFFFFF")
        assert (r, g, b) == (1.0, 1.0, 1.0)

    def test_hex_to_rgb_three_digit_expands(self):
        """`#abc` is shorthand for `#aabbcc`."""
        r, g, b = _hex_to_rgb("#fff")
        assert (r, g, b) == (1.0, 1.0, 1.0)

    def test_hex_to_rgb_rejects_malformed(self):
        with pytest.raises(ValueError):
            _hex_to_rgb("#abcd")  # 4 digits, not a real hex

    def test_relative_luminance_extremes(self):
        """Black = 0.0, white = 1.0 — the reference points of the WCAG
        luminance formula. If these break, every contrast calc is wrong."""
        assert _relative_luminance((0.0, 0.0, 0.0)) == 0.0
        assert _relative_luminance((1.0, 1.0, 1.0)) == pytest.approx(1.0, abs=1e-6)

    def test_contrast_ratio_black_on_white_is_21(self):
        """Pure black on pure white = 21:1 (max contrast per WCAG)."""
        black = _hex_to_rgb("#000000")
        white = _hex_to_rgb("#FFFFFF")
        assert _contrast_ratio(black, white) == pytest.approx(21.0, abs=0.01)

    def test_contrast_ratio_is_symmetric(self):
        """contrast(a, b) == contrast(b, a) — the lighter color is
        determined internally, not by argument order."""
        a = _hex_to_rgb("#64748B")
        b = _hex_to_rgb("#0F172A")
        assert _contrast_ratio(a, b) == pytest.approx(_contrast_ratio(b, a))

    def test_contrast_ratio_vertex_pmo_failing_case(self):
        """Concrete anchor : vertex-pmo's `ink.muted` (#64748B) on
        `surface.DEFAULT` (#0F172A) MUST score below WCAG AA 4.5:1.
        That's why pa11y reports 18 errors on this site; if this test
        ever passes, our fix-target heuristic has drifted."""
        fg = _hex_to_rgb("#64748B")
        bg = _hex_to_rgb("#0F172A")
        ratio = _contrast_ratio(fg, bg)
        assert ratio < 4.5, f"Expected vertex-pmo ink.muted to fail AA, got {ratio:.2f}"

    def test_harden_already_compliant_returns_none(self):
        """If the fg already meets the buffer target, the hardener is a
        no-op — preserves design intent and ensures idempotence."""
        # White on black = 21:1, well above the 5.0 buffer
        assert _harden_token_contrast("#FFFFFF", "#000000") is None

    def test_harden_dark_bg_lightens_fg(self):
        """Dark background → the fixer must lift the foreground (raise V)
        until contrast clears the 5.0 buffer."""
        new_hex = _harden_token_contrast("#64748B", "#0F172A")
        assert new_hex is not None
        fg = _hex_to_rgb(new_hex)
        bg = _hex_to_rgb("#0F172A")
        assert _contrast_ratio(fg, bg) >= 5.0

    def test_harden_light_bg_darkens_fg(self):
        """Light background → the fixer must drop V to darken the
        foreground until contrast clears the 5.0 buffer."""
        # depanneur-nobert's historic problem : #8B7355 on a cream bg
        new_hex = _harden_token_contrast("#8B7355", "#FFF8E7")
        assert new_hex is not None
        fg = _hex_to_rgb(new_hex)
        bg = _hex_to_rgb("#FFF8E7")
        assert _contrast_ratio(fg, bg) >= 5.0


class TestFixPa11yContrast:
    """P8.6 — integration tests for the `_fix_pa11y_contrast` fixer.

    The fixer reads `tailwind.config.ts`, locates muted-role palette
    tokens, computes their contrast against the site's primary background,
    and rewrites any token below WCAG AA 4.5:1 to a value that clears 5.0:1.
    """

    def _write_palette(self, site_dir: Path, content: str) -> Path:
        config = site_dir / "tailwind.config.ts"
        config.write_text(content)
        return config

    def test_skip_when_tailwind_config_absent(self, tmp_path):
        """Site without tailwind.config.ts (e.g., CSS-vars-only palette)
        is out of scope for this commit — must skip cleanly."""
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)
        assert report.contrast_tokens_fixed == 0

    def test_skip_when_no_muted_token(self, tmp_path):
        """Palette without any muted-pattern token (`muted`, `subtle`,
        `tertiary`, `disabled`, `placeholder`) leaves nothing to harden."""
        self._write_palette(
            tmp_path,
            (
                "export default {\n"
                "  theme: { extend: { colors: {\n"
                "    surface: {\n"
                "      DEFAULT: '#0F172A'\n"
                "    },\n"
                "    primary: {\n"
                "      DEFAULT: '#3B82F6'\n"
                "    }\n"
                "  }}}\n"
                "};\n"
            ),
        )
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)
        assert report.contrast_tokens_fixed == 0

    # Realistic tailwind.config.ts skeleton — mirrors vertex-pmo + depanneur-nobert
    # convention : nested palette blocks, one token per line, single-quoted hexes.
    _DARK_PALETTE = (
        "export default {\n"
        "  theme: { extend: { colors: {\n"
        "    surface: {\n"
        "      DEFAULT: '#0F172A',\n"
        "      alt: '#1E293B'\n"
        "    },\n"
        "    ink: {\n"
        "      DEFAULT: '#F8FAFC',\n"
        "      muted: '#64748B'\n"
        "    }\n"
        "  }}}\n"
        "};\n"
    )

    _LIGHT_PALETTE = (
        "export default {\n"
        "  theme: { extend: { colors: {\n"
        "    background: {\n"
        "      DEFAULT: '#FFF8E7'\n"
        "    },\n"
        "    text: {\n"
        "      DEFAULT: '#2A1810',\n"
        "      muted: '#8B7355'\n"
        "    }\n"
        "  }}}\n"
        "};\n"
    )

    def test_skip_when_no_background_token(self, tmp_path):
        """Palette without a recognized background token (`surface`,
        `background`, `bg`, `body`) → cannot compute contrast → conservative skip."""
        self._write_palette(
            tmp_path,
            (
                "export default {\n"
                "  theme: { extend: { colors: {\n"
                "    text: {\n"
                "      muted: '#64748B'\n"
                "    }\n"
                "  }}}\n"
                "};\n"
            ),
        )
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)
        assert report.contrast_tokens_fixed == 0

    def test_skip_when_already_compliant(self, tmp_path):
        """If every muted token already meets the buffer (5.0:1), the file
        stays bit-identical (idempotent no-op)."""
        content = (
            "export default {\n"
            "  theme: { extend: { colors: {\n"
            "    surface: {\n"
            "      DEFAULT: '#0F172A'\n"
            "    },\n"
            "    ink: {\n"
            "      muted: '#CBD5E1'\n"  # ~12:1 on #0F172A
            "    }\n"
            "  }}}\n"
            "};\n"
        )
        config = self._write_palette(tmp_path, content)
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)
        assert report.contrast_tokens_fixed == 0
        assert config.read_text() == content  # bit-identical

    def test_fix_dark_theme_failing_muted(self, tmp_path):
        """Concrete vertex-pmo case : ink.muted #64748B on surface
        #0F172A scores ~4.0:1. The fixer must lift it to ≥ 4.5:1
        (target 5.0) and rewrite the line in place."""
        self._write_palette(tmp_path, self._DARK_PALETTE)
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)

        assert report.contrast_tokens_fixed == 1
        new_content = (tmp_path / "tailwind.config.ts").read_text()
        match = re.search(r"muted:\s*'(#[0-9a-fA-F]{6})'", new_content)
        assert match is not None, f"muted token lost from rewrite: {new_content}"
        new_hex = match.group(1)
        ratio = _contrast_ratio(_hex_to_rgb(new_hex), _hex_to_rgb("#0F172A"))
        assert ratio >= 4.5, f"Hardened value {new_hex} still fails AA: {ratio:.2f}"

    def test_fix_light_theme_failing_muted(self, tmp_path):
        """Symmetric : light cream background needs the muted token to be
        DARKER, not lighter (depanneur-nobert's historic case)."""
        self._write_palette(tmp_path, self._LIGHT_PALETTE)
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)

        assert report.contrast_tokens_fixed == 1
        new_content = (tmp_path / "tailwind.config.ts").read_text()
        match = re.search(r"muted:\s*'(#[0-9a-fA-F]{6})'", new_content)
        assert match is not None
        new_hex = match.group(1)
        ratio = _contrast_ratio(_hex_to_rgb(new_hex), _hex_to_rgb("#FFF8E7"))
        assert ratio >= 4.5

    def test_fix_idempotent_run_twice(self, tmp_path):
        """Running the fixer 2x must leave the file bit-identical after
        the first pass — anchor for the P8.1 idempotence invariant
        extended to D6 contrast tokens."""
        self._write_palette(tmp_path, self._DARK_PALETTE)
        report1 = FixReport()
        _fix_pa11y_contrast(tmp_path, report1)
        assert report1.contrast_tokens_fixed == 1
        snapshot = (tmp_path / "tailwind.config.ts").read_bytes()

        report2 = FixReport()
        _fix_pa11y_contrast(tmp_path, report2)
        assert report2.contrast_tokens_fixed == 0
        assert (tmp_path / "tailwind.config.ts").read_bytes() == snapshot

    def test_fix_preserves_other_tokens(self, tmp_path):
        """The fixer must NOT touch primary / accent / brand tokens —
        only muted-pattern ones. Verifies the conservative scope."""
        self._write_palette(
            tmp_path,
            (
                "export default {\n"
                "  theme: { extend: { colors: {\n"
                "    surface: {\n"
                "      DEFAULT: '#0F172A'\n"
                "    },\n"
                "    primary: {\n"
                "      DEFAULT: '#3B82F6'\n"
                "    },\n"
                "    accent: {\n"
                "      DEFAULT: '#F59E0B'\n"
                "    },\n"
                "    ink: {\n"
                "      muted: '#64748B'\n"
                "    }\n"
                "  }}}\n"
                "};\n"
            ),
        )
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)

        new_content = (tmp_path / "tailwind.config.ts").read_text()
        # primary + accent are untouched
        assert "'#3B82F6'" in new_content
        assert "'#F59E0B'" in new_content
        # surface (background) is untouched
        assert "'#0F172A'" in new_content
        # muted was rewritten (no longer the original failing value)
        assert "'#64748B'" not in new_content

    def test_fix_multiple_muted_tokens(self, tmp_path):
        """When several blocks expose a muted-role token (e.g., both
        `ink.muted` and `text.subtle`), the fixer must process each one
        independently and report the count correctly."""
        self._write_palette(
            tmp_path,
            (
                "export default {\n"
                "  theme: { extend: { colors: {\n"
                "    surface: {\n"
                "      DEFAULT: '#0F172A'\n"
                "    },\n"
                "    ink: {\n"
                "      muted: '#64748B'\n"
                "    },\n"
                "    text: {\n"
                "      subtle: '#475569'\n"
                "    }\n"
                "  }}}\n"
                "};\n"
            ),
        )
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)
        assert report.contrast_tokens_fixed == 2

    def test_fix_via_auto_fix_routing(self, tmp_path):
        """End-to-end via `auto_fix(dimensions={'D6'})` — verifies the
        P8.3 routing actually invokes pa11y_contrast and no other fixer."""
        site = tmp_path / "site"
        site.mkdir()
        self._write_palette(site, self._DARK_PALETTE)
        client = tmp_path / "client"
        client.mkdir()
        report = auto_fix(site, client, brief={"company_name": "TestCo"}, dimensions={"D6"})
        assert report.contrast_tokens_fixed == 1
        # D4/D8 fixers MUST NOT have run
        assert not (site / "vercel.json").exists()
        assert not (site / "README.md").exists()

    def test_p8_6_2_multi_bg_calibrates_against_worst_case(self, tmp_path):
        """P8.6.2 regression : palette with multiple bg tokens — the fixer
        must calibrate against the bg that yields the WORST contrast vs the
        muted token, not just the first bg found.

        Vertex-pmo's case : `surface.DEFAULT = #0F172A` (very dark) but
        `surface.alt = #1E293B`, `surface.raised = #334155` are progressively
        lighter. `ink.muted = #7689a4` had only 4.10:1 on `surface.alt` and
        was actually FAILING WCAG AA even though it passed on `surface.DEFAULT`.

        After P8.6.2, the hardened muted must clear 4.5:1 against ALL bgs
        in the palette — i.e., against `surface.raised` (worst case here).
        """
        palette_with_lighter_bgs = (
            "export default {\n"
            "  theme: { extend: { colors: {\n"
            "    surface: {\n"
            "      DEFAULT: '#0F172A',\n"
            "      alt: '#1E293B',\n"
            "      raised: '#334155'\n"
            "    },\n"
            "    ink: {\n"
            "      DEFAULT: '#F8FAFC',\n"
            "      muted: '#7689a4'\n"
            "    }\n"
            "  }}}\n"
            "};\n"
        )
        self._write_palette(tmp_path, palette_with_lighter_bgs)
        report = FixReport()
        _fix_pa11y_contrast(tmp_path, report)

        assert report.contrast_tokens_fixed == 1
        new_content = (tmp_path / "tailwind.config.ts").read_text()
        match = re.search(r"muted:\s*'(#[0-9a-fA-F]{6})'", new_content)
        assert match is not None
        new_hex = match.group(1)
        new_rgb = _hex_to_rgb(new_hex)
        # Must clear AA against EVERY bg in the palette (not just the first one)
        for bg in ("#0F172A", "#1E293B", "#334155"):
            ratio = _contrast_ratio(new_rgb, _hex_to_rgb(bg))
            assert ratio >= 4.5, (
                f"Hardened muted {new_hex} only achieves {ratio:.2f}:1 vs bg {bg} — "
                f"P8.6.2 regression : multi-bg calibration missed the worst case"
            )


# ── P9 D8 — dry-run describers parity with FIXER_ORDER ────────────────


class TestDryRunDescribers:
    """Invariants structurels : `DRY_RUN_DESCRIBERS` est la source de
    vérité du mode dry-run et doit rester synchronisé avec `FIXER_ORDER`.

    Découvert pendant P8.5 (mesure terrain vertex-pmo) : l'ancien
    `_dry_run_analysis` (cli_commands.py) hardcodait 6 checks et omettait
    `readme` (P8.1) et `pa11y_contrast` (P8.6). D8 ferme cette dérive en
    dérivant le dry-run depuis `FIXER_ORDER` via un registre testé.
    """

    def test_describers_cover_all_fixers(self):
        """Tout fixer dans FIXER_ORDER doit avoir un describer."""
        fixer_names = {f.name for f in FIXER_ORDER}
        describer_names = set(DRY_RUN_DESCRIBERS.keys())
        assert fixer_names == describer_names, (
            f"Missing describers: {fixer_names - describer_names} | "
            f"Stale describers: {describer_names - fixer_names}"
        )

    def test_describer_signature_returns_str_or_none(self, tmp_path):
        """Chaque describer doit retourner `str | None` sur site vide."""
        site = tmp_path / "site"
        site.mkdir()
        client = tmp_path / "client"
        client.mkdir()
        for name, describer in DRY_RUN_DESCRIBERS.items():
            result = describer(site, client, None)
            assert result is None or isinstance(result, str), (
                f"Describer {name!r} returned {type(result).__name__}, expected str | None"
            )

    def test_describe_auto_fix_returns_list_in_fixer_order(self, tmp_path):
        """Findings sortent dans l'ordre strict de FIXER_ORDER."""
        site = tmp_path / "site"
        site.mkdir()
        client = tmp_path / "client"
        client.mkdir()
        findings = describe_auto_fix(site, client, brief=None)
        assert isinstance(findings, list)
        assert all(isinstance(f, str) for f in findings)
        # Ordre vérifié : npm_audit (générique, toujours présent) doit être
        # à l'index correspondant à sa position dans FIXER_ORDER.
        fixer_index = {f.name: i for i, f in enumerate(FIXER_ORDER)}
        # On retrouve les findings dans l'ordre du FIXER_ORDER : pour chaque
        # paire de findings successifs, l'index du fixer source est croissant.
        last_seen_index = -1
        for finding in findings:
            matched_name = next(
                (
                    name
                    for name in DRY_RUN_DESCRIBERS
                    if name.replace("_", " ") in finding.lower() or name in finding
                ),
                None,
            )
            if matched_name is None:
                continue  # finding générique non rattachable, on skip
            assert fixer_index[matched_name] > last_seen_index, (
                f"Finding {finding!r} (fixer {matched_name}) hors ordre FIXER_ORDER"
            )
            last_seen_index = fixer_index[matched_name]


class TestDescriberParityCookieConsent:
    def test_describes_when_absent(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        result = DRY_RUN_DESCRIBERS["cookie_consent"](site, tmp_path / "c", None)
        assert result is not None
        assert "cookie" in result.lower() or "consent" in result.lower()

    def test_silent_when_present(self, tmp_path):
        # `_resolve_components_dir` choisit `site/components/` quand `site/app/`
        # existe (convention NEXOS flat), sinon `site/src/components/`. On
        # reproduit la convention flat pour que le scan trouve le banner.
        site = tmp_path / "site"
        (site / "app").mkdir(parents=True)
        components = site / "components" / "layout"
        components.mkdir(parents=True)
        (components / "CookieConsentBanner.tsx").write_text("export {}")
        result = DRY_RUN_DESCRIBERS["cookie_consent"](site, tmp_path / "c", None)
        assert result is None


class TestDescriberParityVercelHeaders:
    def test_describes_when_vercel_absent(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        result = DRY_RUN_DESCRIBERS["vercel_headers"](site, tmp_path / "c", None)
        assert result is not None
        assert "vercel" in result.lower()

    def test_describes_when_headers_missing(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        (site / "vercel.json").write_text(json.dumps({"headers": []}))
        result = DRY_RUN_DESCRIBERS["vercel_headers"](site, tmp_path / "c", None)
        assert result is not None
        assert "header" in result.lower()


class TestDescriberParityCsp:
    def test_describes_when_csp_absent(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        (site / "vercel.json").write_text(json.dumps({"headers": []}))
        result = DRY_RUN_DESCRIBERS["csp"](site, tmp_path / "c", None)
        assert result is not None
        assert "content-security-policy" in result.lower() or "csp" in result.lower()


class TestDescriberParityCspMiddleware:
    def test_describes_when_middleware_absent(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        result = DRY_RUN_DESCRIBERS["csp_middleware"](site, tmp_path / "c", None)
        assert result is not None
        assert "middleware" in result.lower() or "csp" in result.lower()


class TestDescriberParityNextConfig:
    def test_describes_when_poweredByHeader_missing(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        (site / "next.config.mjs").write_text("export default {}")
        result = DRY_RUN_DESCRIBERS["next_config"](site, tmp_path / "c", None)
        assert result is not None
        assert "poweredByHeader" in result or "powered" in result.lower()

    def test_silent_when_already_false(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        (site / "next.config.mjs").write_text("export default { poweredByHeader: false }")
        result = DRY_RUN_DESCRIBERS["next_config"](site, tmp_path / "c", None)
        assert result is None


class TestDescriberParityPrivacyPage:
    def test_describes_when_absent(self, tmp_path):
        site = tmp_path / "site"
        (site / "app").mkdir(parents=True)
        result = DRY_RUN_DESCRIBERS["privacy_page"](site, tmp_path / "c", None)
        assert result is not None
        assert (
            "confidentialité" in result.lower()
            or "privacy" in result.lower()
            or "politique" in result.lower()
        )


class TestDescriberParityLegalPage:
    def test_describes_when_absent(self, tmp_path):
        site = tmp_path / "site"
        (site / "app").mkdir(parents=True)
        result = DRY_RUN_DESCRIBERS["legal_page"](site, tmp_path / "c", None)
        assert result is not None
        assert "mentions" in result.lower() or "legal" in result.lower()


class TestDescriberParityReadme:
    """Le describer pivot pour P9 D8 — sans lui le dry-run mentait."""

    def test_describes_when_absent(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        result = DRY_RUN_DESCRIBERS["readme"](site, tmp_path / "c", None)
        assert result is not None
        assert "readme" in result.lower()

    def test_silent_when_present(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        (site / "README.md").write_text("# Existing")
        result = DRY_RUN_DESCRIBERS["readme"](site, tmp_path / "c", None)
        assert result is None


class TestDescriberParityPa11yContrast:
    """Le 2e describer pivot pour P9 D8 — anchor vertex-pmo.

    Le pattern multi-ligne (un token par ligne) reflète la convention
    réelle des sites NEXOS (vertex-pmo + depanneur-nobert), que la regex
    `_TAILWIND_TOKEN_LINE_RE` du fixer attend.
    """

    _LOW_CONTRAST = (
        "export default {\n"
        "  theme: { extend: { colors: {\n"
        "    surface: {\n"
        "      DEFAULT: '#0F172A'\n"
        "    },\n"
        "    ink: {\n"
        "      DEFAULT: '#F8FAFC',\n"
        "      muted: '#64748B'\n"
        "    }\n"
        "  }}}\n"
        "};\n"
    )

    def test_describes_when_low_contrast(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        (site / "tailwind.config.ts").write_text(self._LOW_CONTRAST)
        result = DRY_RUN_DESCRIBERS["pa11y_contrast"](site, tmp_path / "c", None)
        assert result is not None
        assert "contrast" in result.lower() or "wcag" in result.lower() or "muted" in result.lower()

    def test_silent_when_no_tailwind_config(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        result = DRY_RUN_DESCRIBERS["pa11y_contrast"](site, tmp_path / "c", None)
        assert result is None


class TestDescriberParityNpmAudit:
    """npm_audit n'a pas de détection statique → finding générique."""

    def test_always_reports_generic_finding(self, tmp_path):
        site = tmp_path / "site"
        site.mkdir()
        result = DRY_RUN_DESCRIBERS["npm_audit"](site, tmp_path / "c", None)
        assert result is not None
        assert "npm" in result.lower() or "audit" in result.lower()
