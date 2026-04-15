"""Tests pour nexos.brief_wizard — wizard interactif de génération de brief."""

import json
from unittest.mock import patch

import pytest

from nexos.brief_wizard import (
    LEGAL_PAGES,
    PAGE_PRESETS,
    SITE_TYPES,
    _ask_adaptive,
    _ask_mode_intake,
    _assemble_brief,
    _slugify,
    interactive_brief,
)

# ── Constantes ────────────────────────────────────────────────────────────────


class TestConstants:
    def test_page_presets_cover_all_types(self):
        """Chaque type de site doit avoir un preset de pages."""
        for t in SITE_TYPES:
            assert t in PAGE_PRESETS, f"Type '{t}' manquant dans PAGE_PRESETS"

    def test_page_presets_have_accueil_and_contact(self):
        """Tous les presets doivent inclure accueil et contact."""
        for t, pages in PAGE_PRESETS.items():
            assert "contact" in pages, f"'contact' manquant dans preset '{t}'"
            # accueil ou landing pour application
            assert any(p in pages for p in ("accueil", "landing")), (
                f"Page d'accueil manquante dans preset '{t}'"
            )

    def test_legal_pages(self):
        assert "politique-confidentialite" in LEGAL_PAGES
        assert "mentions-legales" in LEGAL_PAGES

    def test_site_types_non_empty(self):
        assert len(SITE_TYPES) >= 4


# ── Slugify ───────────────────────────────────────────────────────────────────


class TestSlugify:
    def test_basic_name(self):
        assert _slugify("Mon Entreprise") == "mon-entreprise"

    def test_accented_name(self):
        assert _slugify("Émilie Poirier RH") == "emilie-poirier-rh"

    def test_special_chars(self):
        assert _slugify("L'Atelier du Bois!") == "l-atelier-du-bois"

    def test_single_word(self):
        assert _slugify("NEXOS") == "nexos"


# ── Assemblage du brief ──────────────────────────────────────────────────────


class TestAssembleBrief:
    @pytest.fixture
    def sample_inputs(self):
        return {
            "company": {
                "name": "Test Corp",
                "slug": "test-corp",
                "neq": "1234567890",
                "address": "123 Rue Test, Montréal",
                "phone": "514-555-0000",
                "email": "info@test.com",
            },
            "site": {
                "stack": "nextjs",
                "type": "vitrine",
                "pages": [
                    "accueil",
                    "services",
                    "contact",
                    "politique-confidentialite",
                    "mentions-legales",
                ],
                "features": ["formulaire-contact", "analytics"],
                "languages": ["fr", "en"],
                "hosting": "Vercel",
                "domain": "test-corp.ca",
            },
            "adaptive": {},
            "legal": {
                "rpp": {"name": "Jean Test", "email": "rpp@test.com", "title": "RPP"},
                "data_collected": ["nom", "courriel"],
                "purposes": ["communication"],
                "retention": "24 mois",
                "transfer_outside_qc": True,
                "transfer_countries": ["États-Unis"],
                "third_party_services": ["Vercel (hébergement)"],
                "consent_mode": "opt-in (recommandé Loi 25)",
                "incident": {"process_in_place": False, "notification_email": "rpp@test.com"},
            },
            "design": {
                "palette": "#1a1a2e",
                "typography": "Inter",
                "style": "minimaliste",
                "logo_provided": True,
                "references": [],
            },
            "context": {
                "competitors": [],
                "keywords_seo": ["test", "dev"],
                "free_text": None,
            },
        }

    def test_brief_has_required_keys(self, sample_inputs):
        brief = _assemble_brief(
            "create",
            sample_inputs["company"],
            sample_inputs["site"],
            sample_inputs["adaptive"],
            sample_inputs["legal"],
            sample_inputs["design"],
            sample_inputs["context"],
        )
        assert "_meta" in brief
        assert "client" in brief
        assert "legal" in brief
        assert "site" in brief
        assert "design" in brief
        assert "context" in brief
        assert "adaptive" in brief

    def test_meta_generator(self, sample_inputs):
        brief = _assemble_brief(
            "create",
            sample_inputs["company"],
            sample_inputs["site"],
            sample_inputs["adaptive"],
            sample_inputs["legal"],
            sample_inputs["design"],
            sample_inputs["context"],
        )
        assert brief["_meta"]["generator"] == "nexos-v3.0"
        assert brief["_meta"]["mode"] == "create"
        assert brief["site"]["stack"] == "nextjs"

    def test_brief_flattens_legal_fields(self, sample_inputs):
        brief = _assemble_brief(
            "create",
            sample_inputs["company"],
            sample_inputs["site"],
            sample_inputs["adaptive"],
            sample_inputs["legal"],
            sample_inputs["design"],
            sample_inputs["context"],
        )
        assert brief["legal"]["company_name"] == "Test Corp"
        assert brief["legal"]["rpp_name"] == "Jean Test"
        assert brief["legal"]["cookie_consent"] == "opt-in"
        assert brief["legal"]["third_parties"] == ["Vercel (hébergement)"]

    def test_mode_intake_populates_mission_and_existing_url(self, sample_inputs):
        brief = _assemble_brief(
            "audit",
            sample_inputs["company"],
            sample_inputs["site"],
            sample_inputs["adaptive"],
            sample_inputs["legal"],
            sample_inputs["design"],
            sample_inputs["context"],
            {"existing_url": "https://example.com", "audit_goal": "Trouver les blocages"},
        )
        assert brief["mission"]["intake"]["audit_goal"] == "Trouver les blocages"
        assert brief["site"]["existing_url"] == "https://example.com"

    def test_client_slug(self, sample_inputs):
        brief = _assemble_brief(
            "create",
            sample_inputs["company"],
            sample_inputs["site"],
            sample_inputs["adaptive"],
            sample_inputs["legal"],
            sample_inputs["design"],
            sample_inputs["context"],
        )
        assert brief["client"]["slug"] == "test-corp"
        assert brief["client"]["name"] == "Test Corp"

    def test_brief_is_json_serializable(self, sample_inputs):
        brief = _assemble_brief(
            "audit",
            sample_inputs["company"],
            sample_inputs["site"],
            sample_inputs["adaptive"],
            sample_inputs["legal"],
            sample_inputs["design"],
            sample_inputs["context"],
        )
        # Should not raise
        json.dumps(brief, ensure_ascii=False)


# ── Logique adaptative ────────────────────────────────────────────────────────


class TestAdaptiveLogic:
    @patch("nexos.brief_wizard._safe_ask")
    def test_ecommerce_asks_payment(self, mock_ask):
        """Le type ecommerce doit demander le fournisseur de paiement."""
        mock_ask.side_effect = [
            "Stripe",  # payment_provider
            "20",  # product_count
            True,  # shipping
            "Québec",  # shipping_zones
            True,  # inventory
        ]
        result = _ask_adaptive("ecommerce", [])
        assert result["payment_provider"] == "Stripe"
        assert result["shipping"] is True
        assert result["inventory"] is True

    @patch("nexos.brief_wizard._safe_ask")
    def test_ecommerce_no_shipping(self, mock_ask):
        """Si pas de livraison, pas de question zones."""
        mock_ask.side_effect = [
            "PayPal",  # payment_provider
            "5",  # product_count
            False,  # shipping = No
            False,  # inventory
        ]
        result = _ask_adaptive("ecommerce", [])
        assert result["shipping"] is False
        assert "shipping_zones" not in result

    @patch("nexos.brief_wizard._safe_ask")
    def test_portfolio_asks_display(self, mock_ask):
        mock_ask.side_effect = ["grille", True]
        result = _ask_adaptive("portfolio", [])
        assert result["display_mode"] == "grille"

    @patch("nexos.brief_wizard._safe_ask")
    def test_blog_asks_frequency(self, mock_ask):
        mock_ask.side_effect = ["hebdomadaire", False, True]
        result = _ask_adaptive("blog", [])
        assert result["publish_frequency"] == "hebdomadaire"

    @patch("nexos.brief_wizard._safe_ask")
    def test_application_with_auth(self, mock_ask):
        mock_ask.side_effect = [
            True,  # auth_required
            ["email/password", "Google"],  # auth_methods
            "admin, user",  # user_types
            False,  # realtime
        ]
        result = _ask_adaptive("application", [])
        assert result["auth_required"] is True
        assert "Google" in result["auth_methods"]

    @patch("nexos.brief_wizard._safe_ask")
    def test_newsletter_feature_adds_provider(self, mock_ask):
        mock_ask.side_effect = ["Resend"]
        result = _ask_adaptive("vitrine", ["infolettre"])
        assert result["newsletter_provider"] == "Resend"

    @patch("nexos.brief_wizard._safe_ask")
    def test_analytics_feature_adds_provider(self, mock_ask):
        mock_ask.side_effect = ["Plausible"]
        result = _ask_adaptive("vitrine", ["analytics"])
        assert result["analytics_provider"] == "Plausible"

    def test_vitrine_no_features_empty(self):
        """Vitrine sans features spéciales = dict vide."""
        result = _ask_adaptive("vitrine", [])
        assert result == {}


class TestModeIntake:
    @patch("nexos.brief_wizard._safe_ask")
    def test_audit_mode_intake(self, mock_ask):
        mock_ask.side_effect = [
            "https://example.com",
            ["seo", "performance"],
            "Identifier les priorites",
        ]
        result = _ask_mode_intake("audit")
        assert result["existing_url"] == "https://example.com"
        assert "seo" in result["audit_scope"]


# ── Wizard interactif (flux complet mocké) ────────────────────────────────────


class TestInteractiveBrief:
    @patch("nexos.brief_wizard.sys")
    def test_non_tty_raises(self, mock_sys):
        """Le wizard doit refuser de se lancer hors terminal."""
        mock_sys.stdin.isatty.return_value = False
        with pytest.raises(RuntimeError, match="TTY"):
            interactive_brief("create")
