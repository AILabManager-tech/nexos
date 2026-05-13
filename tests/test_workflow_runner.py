"""Tests des workflows modulaires NEXOS."""

from __future__ import annotations

from nexos.workflow_runner import list_workflows, run_workflow


def _valid_intake() -> dict:
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


def test_lists_intake_preflight_workflow() -> None:
    workflows = list_workflows()

    assert [workflow.id for workflow in workflows] == ["intake-preflight", "saas-preview"]


def test_intake_preflight_workflow_passes_with_valid_payload() -> None:
    output = run_workflow("intake-preflight", _valid_intake())

    assert output["status"] == "passed"
    assert [step["module_id"] for step in output["steps"]] == [
        "brief-synthesizer",
        "legal-gap-checker",
    ]
    assert output["final_output"]["ready_for_pipeline"] is True


def test_intake_preflight_workflow_reports_legal_gaps() -> None:
    payload = {"company": {"name": "Client Incomplet"}}

    output = run_workflow("intake-preflight", payload)

    assert output["status"] == "passed"
    assert output["final_output"]["ready_for_pipeline"] is False
    assert output["final_output"]["blocking_count"] > 0
