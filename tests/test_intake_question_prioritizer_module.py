"""Tests pour le module intake-question-prioritizer."""

from __future__ import annotations

from nexos.modules.intake_question_prioritizer import run


def test_empty_gaps_returns_empty():
    out = run({"gaps": []})
    assert out["module_id"] == "intake-question-prioritizer"
    assert out["questions"] == []
    assert out["blocking_count"] == 0
    assert out["lifting_mu_delta"] == 0.0


def test_rpp_email_top_priority():
    gaps = [
        {"field": "legal.retention", "message": "retention requis", "blocking": True},
        {"field": "legal.rpp_email", "message": "rpp email requis", "blocking": True},
        {"field": "legal.transfer_outside_qc", "message": "transfer requis", "blocking": False},
    ]
    out = run({"gaps": gaps})
    # Tri décroissant : rpp_email doit être en première position
    assert out["questions"][0]["field"] == "legal.rpp_email"
    assert out["questions"][0]["priority_score"] == 10


def test_blocking_boosts_priority():
    """Un gap bloquant gagne +1 sur sa priorité de base."""
    gaps_blocking = [{"field": "legal.cookie_consent", "message": "", "blocking": True}]
    gaps_non_blocking = [{"field": "legal.cookie_consent", "message": "", "blocking": False}]
    blk = run({"gaps": gaps_blocking})
    non = run({"gaps": gaps_non_blocking})
    assert blk["questions"][0]["priority_score"] > non["questions"][0]["priority_score"]


def test_blocking_count():
    gaps = [
        {"field": "legal.rpp_email", "message": "", "blocking": True},
        {"field": "legal.transfer_outside_qc", "message": "", "blocking": False},
        {"field": "legal.purposes", "message": "", "blocking": True},
    ]
    out = run({"gaps": gaps})
    assert out["blocking_count"] == 2


def test_lifting_mu_delta_sums():
    gaps = [
        {"field": "legal.rpp_email", "message": "", "blocking": True},
        {"field": "legal.purposes", "message": "", "blocking": True},
    ]
    out = run({"gaps": gaps})
    # rpp_email lift=0.6, purposes lift=0.6 → delta ≈ 1.2
    assert 1.0 <= out["lifting_mu_delta"] <= 1.5


def test_question_is_human_friendly():
    gaps = [{"field": "legal.rpp_email", "message": "rpp email requis", "blocking": True}]
    out = run({"gaps": gaps})
    q = out["questions"][0]["question"]
    assert "courriel" in q.lower() or "email" in q.lower()
    assert "?" in q


def test_unknown_field_uses_default_priority():
    gaps = [{"field": "legal.some_new_field", "message": "Texte libre", "blocking": False}]
    out = run({"gaps": gaps})
    # Priorité par défaut = 2 (pas de boost car non-blocking)
    assert out["questions"][0]["priority_score"] == 2
