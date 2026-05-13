"""Tests end-to-end pour le workflow `saas-preview`."""

from __future__ import annotations

from nexos.workflow_runner import run_workflow


def test_saas_preview_workflow_runs_to_completion():
    payload = {
        "company": {
            "name": "Clinique Aura",
            "slug": "clinique-aura",
            "email": "info@clinique-aura.ca",
        },
        "legal": {
            "rpp_name": "Jane Doe",
            "rpp_email": "rpp@clinique-aura.ca",
            "rpp_title": "Directrice clinique",
            "data_collected": ["nom", "courriel", "dossier médical"],
            "purposes": ["prise de rendez-vous", "suivi clinique"],
            "retention": "5 ans",
            "cookie_consent": "opt-in",
            "third_party_services": ["Vercel", "Calendly"],
        },
        "context": {"summary": "Clinique de physiothérapie multi-sites à Longueuil."},
    }
    result = run_workflow("saas-preview", payload)
    assert result["status"] == "passed"
    assert len(result["steps"]) == 5

    # Étape 3 : scorer
    scorer = next(s for s in result["steps"] if s["id"] == "brief-preview-scorer")
    assert scorer["output"]["module_id"] == "brief-preview-scorer"
    assert scorer["output"]["estimated_mu"] >= 7.5  # legal complet
    assert "D8" in scorer["output"]["dimensions"]

    # Étape 4 : prioritizer (legal complet, mais legal-gap-checker peut signaler
    # encore quelques champs cosmétiques type company.address)
    prioritizer = next(s for s in result["steps"] if s["id"] == "intake-question-prioritizer")
    assert prioritizer["output"]["blocking_count"] <= 5

    # Étape 5 : prerecommender → SEC-01 santé
    prerec = next(s for s in result["steps"] if s["id"] == "pattern-prerecommender")
    assert prerec["output"]["sector_id"] == "SEC-01"
    assert len(prerec["output"]["patterns"]) == 3


def test_saas_preview_with_incomplete_brief():
    payload = {"company": {"name": "Minimal"}}
    result = run_workflow("saas-preview", payload)
    assert result["status"] == "passed"
    scorer_out = next(s for s in result["steps"] if s["id"] == "brief-preview-scorer")["output"]
    assert scorer_out["estimated_mu"] < 7.5
    assert len(scorer_out["gating_factors"]) > 0

    prio_out = next(s for s in result["steps"] if s["id"] == "intake-question-prioritizer")[
        "output"
    ]
    assert prio_out["blocking_count"] > 0
    # rpp_email doit être en tête car non renseigné
    assert prio_out["questions"][0]["field"] == "legal.rpp_email"
