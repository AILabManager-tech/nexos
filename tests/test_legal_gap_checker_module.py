"""Tests du module legal-gap-checker."""

from __future__ import annotations

from nexos.module_registry import ModuleRegistry


def _complete_brief() -> dict:
    return {
        "client": {"name": "Client Test", "slug": "client-test"},
        "company": {
            "name": "Client Test",
            "address": "123 rue Test, Montréal",
            "phone": "514-555-0000",
            "email": "info@example.ca",
            "neq": "1234567890",
        },
        "legal": {
            "rpp_name": "Jean Test",
            "rpp_email": "rpp@example.ca",
            "rpp_title": "Responsable protection des renseignements personnels",
            "data_collected": ["nom", "courriel", "telephone"],
            "purposes": ["communication", "analytics"],
            "retention": "24 mois",
            "transfer_outside_qc": False,
            "third_party_services": ["Vercel", "Plausible"],
            "consent_mode": "opt-in",
            "incident_process": True,
            "incident_email": "rpp@example.ca",
        },
        "site": {
            "type": "vitrine",
            "pages": ["accueil", "contact"],
            "languages": ["fr", "en"],
        },
    }


def test_legal_gap_checker_accepts_complete_brief() -> None:
    registry = ModuleRegistry()

    output = registry.run("legal-gap-checker", {"brief": _complete_brief()})

    assert output["ready_for_pipeline"] is True
    assert output["blocking_count"] == 0
    assert output["gaps"] == []
    assert output["next_questions"] == []


def test_legal_gap_checker_reports_missing_legal_fields() -> None:
    registry = ModuleRegistry()

    output = registry.run(
        "legal-gap-checker",
        {
            "brief": {
                "client": {"name": "Client Incomplet", "slug": "client-incomplet"},
                "legal": {},
                "site": {"type": "vitrine", "pages": ["accueil"], "languages": ["fr"]},
            }
        },
    )

    fields = {gap["field"] for gap in output["gaps"]}
    assert output["ready_for_pipeline"] is False
    assert output["blocking_count"] == len(output["gaps"])
    assert "legal.rpp_name" in fields
    assert "legal.retention" in fields
    assert "legal.data_collected" in fields
    assert "legal.purposes" in fields
    assert output["next_questions"][0]["required"] is True


def test_legal_gap_checker_rejects_opt_out_cookie_consent() -> None:
    registry = ModuleRegistry()
    brief = _complete_brief()
    brief["legal"]["consent_mode"] = "opt-out"

    output = registry.run("legal-gap-checker", {"brief": brief})

    assert output["ready_for_pipeline"] is False
    assert any(gap["field"] == "legal.cookie_consent" for gap in output["gaps"])


def test_legal_gap_checker_requires_transfer_countries_when_needed() -> None:
    registry = ModuleRegistry()
    brief = _complete_brief()
    brief["legal"]["transfer_outside_qc"] = True

    output = registry.run("legal-gap-checker", {"brief": brief})

    assert output["ready_for_pipeline"] is False
    assert any(gap["field"] == "legal.transfer_countries" for gap in output["gaps"])
