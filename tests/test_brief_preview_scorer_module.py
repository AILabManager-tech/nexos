"""Tests pour le module brief-preview-scorer."""

from __future__ import annotations

from nexos.modules.brief_preview_scorer import run


def test_empty_brief_low_score():
    out = run({"brief": {}})
    assert out["module_id"] == "brief-preview-scorer"
    assert out["dimensions"]["D8"]["score"] == 0.0
    assert out["confidence"] < 0.5
    assert "company.name" in out["gating_factors"]


def test_full_legal_high_d8():
    brief = {
        "company": {"name": "Test Corp"},
        "legal": {
            "rpp_name": "Jane Doe",
            "rpp_email": "rpp@test.ca",
            "rpp_title": "Directrice RH",
            "data_collected": ["nom", "courriel"],
            "purposes": ["livraison", "support"],
            "retention": "12 mois",
            "cookie_consent": "opt-in",
            "third_party_services": ["Vercel", "GA4"],
        },
    }
    out = run({"brief": brief})
    assert out["dimensions"]["D8"]["score"] >= 9.0
    assert out["gating_factors"] == []


def test_partial_legal_partial_d8():
    brief = {
        "company": {"name": "X"},
        "legal": {"rpp_name": "Y", "rpp_email": "z@a.ca"},
    }
    out = run({"brief": brief})
    assert 1.0 < out["dimensions"]["D8"]["score"] < 9.0
    assert "legal.purposes" in out["gating_factors"]


def test_mu_is_weighted():
    """Vérifie que μ pondéré croît significativement quand D8 est rempli."""
    legal_base = dict.fromkeys(("rpp_name", "rpp_email", "rpp_title", "retention"), "ok")
    full = run(
        {
            "brief": {
                "company": {"name": "X"},
                "legal": legal_base
                | {
                    "cookie_consent": "opt-in",
                    "data_collected": ["a"],
                    "purposes": ["b"],
                    "third_party_services": ["c"],
                },
            }
        }
    )
    empty = run({"brief": {"company": {"name": "X"}}})
    # D8 weight = 1.5 sur ~9 dimensions ⇒ delta théorique max ~1.5 sur μ pondéré
    assert full["estimated_mu"] > empty["estimated_mu"] + 1.0
    assert full["dimensions"]["D8"]["score"] > empty["dimensions"]["D8"]["score"]


def test_design_bonus_lifts_d1_d6():
    brief = {
        "company": {"name": "X"},
        "design": {
            "brand_archetype": "creator",
            "tone": "warm",
            "personality_6d": {"D1": 3},
            "preferred_patterns": ["P01"],
        },
    }
    out = run({"brief": brief})
    assert out["dimensions"]["D1"]["score"] > 8.5
    assert out["dimensions"]["D6"]["score"] > 7.5


def test_output_dimensions_have_required_keys():
    out = run({"brief": {}})
    for d in ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9"):
        assert d in out["dimensions"]
        assert {"score", "name", "rationale"} <= set(out["dimensions"][d].keys())
