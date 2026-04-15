"""Tests du contrat canonique des briefs NEXOS."""

from nexos.brief_contract import normalize_brief, validate_brief


def test_normalize_legacy_wizard_shape():
    brief = normalize_brief(
        {
            "_meta": {"generator": "nexos-v4.0-wizard", "mode": "create"},
            "client": {"name": "Test Corp", "slug": "test-corp"},
            "company": {
                "address": "123 Rue Test",
                "phone": "514-555-0000",
                "email": "info@test.com",
                "neq": "1234567890",
            },
            "legal": {
                "rpp": {
                    "name": "Jean Test",
                    "email": "rpp@test.com",
                    "title": "RPP",
                },
                "data_collected": ["nom", "courriel", "téléphone"],
                "purposes": ["communication", "analytics"],
                "retention": "24 mois",
                "transfer_outside_qc": True,
                "third_party_services": ["Vercel (hébergement)"],
                "consent_mode": "opt-in (recommandé Loi 25)",
                "incident": {"process_in_place": False, "notification_email": "rpp@test.com"},
            },
            "site": {
                "stack": "nextjs",
                "type": "vitrine",
                "pages": ["accueil"],
                "languages": ["fr"],
            },
        }
    )
    assert brief["_meta"]["generator"] == "nexos-v3.0"
    assert brief["legal"]["rpp_name"] == "Jean Test"
    assert brief["legal"]["cookie_consent"] == "opt-in"
    assert "telephone" in brief["legal"]["data_collected"]
    assert "formulaire-contact" in brief["legal"]["purposes"]


def test_validate_brief_reports_missing_fields():
    errors = validate_brief(
        normalize_brief(
            {
                "client": {"name": "X", "slug": "x"},
                "legal": {},
                "site": {"type": "vitrine", "pages": ["accueil"], "languages": ["fr"]},
            }
        )
    )
    assert "legal.address requis" in errors
    assert "legal.rpp_name requis" in errors
