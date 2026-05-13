"""Tests du module utile brief-synthesizer."""

from __future__ import annotations

from nexos.module_registry import ModuleRegistry


def _valid_payload() -> dict:
    return {
        "mode": "create",
        "company": {
            "name": "Dépanneur Nobert",
            "address": "123 rue Test, Montréal",
            "phone": "514-555-0000",
            "email": "info@nobert.ca",
            "neq": "1234567890",
        },
        "legal": {
            "rpp_name": "Jean Nobert",
            "rpp_email": "rpp@nobert.ca",
            "rpp_title": "Responsable protection des renseignements personnels",
            "data_collected": ["nom", "courriel", "telephone"],
            "purposes": ["communication"],
            "retention": "24 mois",
            "transfer_outside_qc": False,
            "third_party_services": ["Vercel"],
            "consent_mode": "opt-in",
            "incident_process": True,
            "incident_email": "rpp@nobert.ca",
        },
        "site": {
            "type": "vitrine",
            "pages": ["accueil", "services", "contact"],
            "languages": ["fr", "en"],
        },
    }


def test_brief_synthesizer_outputs_pipeline_ready_brief() -> None:
    registry = ModuleRegistry()

    output = registry.run("brief-synthesizer", _valid_payload())

    assert output["ready_for_pipeline"] is True
    assert output["validation_errors"] == []
    assert output["brief"]["client"]["slug"] == "depanneur-nobert"
    assert output["brief"]["legal"]["cookie_consent"] == "opt-in"


def test_brief_synthesizer_reports_legal_gaps() -> None:
    registry = ModuleRegistry()
    payload = {"company": {"name": "Client Incomplet"}}

    output = registry.run("brief-synthesizer", payload)

    assert output["ready_for_pipeline"] is False
    assert "legal.rpp_name requis" in output["validation_errors"]
    assert "legal.retention requis" in output["validation_errors"]
