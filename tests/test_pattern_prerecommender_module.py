"""Tests pour le module pattern-prerecommender."""

from __future__ import annotations

from nexos.modules.pattern_prerecommender import run


def test_explicit_sector_returns_top_k():
    out = run({"sector_id": "SEC-01", "top_k": 3})
    assert out["module_id"] == "pattern-prerecommender"
    assert out["sector_id"] == "SEC-01"
    assert out["fallback"] is False
    assert len(out["patterns"]) == 3
    for p in out["patterns"]:
        assert {"id", "name", "tier_score", "rationale"} <= set(p.keys())


def test_unknown_sector_triggers_fallback():
    out = run({"brief": {"company": {"name": "Foo"}}})
    # Aucun mot-clé reconnu → fallback
    assert out["fallback"] is True
    assert out["sector_id"] is None
    assert len(out["patterns"]) > 0


def test_infer_sector_from_keywords():
    brief = {
        "company": {"name": "Clinique Aura"},
        "context": {"summary": "Une clinique de physiothérapie à Longueuil."},
    }
    out = run({"brief": brief})
    assert out["sector_id"] == "SEC-01"
    assert out["fallback"] is False


def test_infer_sector_commerce():
    brief = {
        "company": {"name": "Dépanneur Nobert"},
        "context": {"summary": "Petite épicerie de quartier."},
    }
    out = run({"brief": brief})
    assert out["sector_id"] == "SEC-03"


def test_top_k_respected():
    out = run({"sector_id": "SEC-01", "top_k": 5})
    assert len(out["patterns"]) == 5


def test_patterns_sorted_by_relevance():
    """Les patterns retournés doivent être triés par tier (1 = plus pertinent)."""
    out = run({"sector_id": "SEC-01", "top_k": 5})
    tiers = [p["tier_score"] for p in out["patterns"]]
    assert tiers == sorted(tiers)
