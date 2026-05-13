"""Priorise les questions Loi 25 manquantes par impact business + légal.

Logique de priorisation :
- Tier 1 (priorité 9-10) : RPP (responsable), purposes, data_collected — non
  négociables pour produire la politique de confidentialité
- Tier 2 (priorité 7-8) : retention, cookie_consent, third_party_services —
  exigés par les auto-fixes D8
- Tier 3 (priorité 5-6) : transfer hors QC, contact details — conditionnels
- Tier 4 (priorité 1-4) : champs cosmétiques ou inférables

Chaque question est associée à une estimation `estimated_mu_lift` (gain attendu
sur μ D8 si elle est répondue), qui permet de calculer le delta total.
"""

from __future__ import annotations

from typing import Any

_FIELD_PRIORITY = {
    "legal.rpp_email": (
        10,
        0.6,
        "Sans RPP identifié, la politique de confidentialité ne peut pas être générée (Loi 25 art. 8).",
    ),
    "legal.rpp_name": (10, 0.5, "Sans nom RPP, la politique reste anonyme et non opposable."),
    "legal.purposes": (9, 0.6, "Finalités de collecte = pilier de la transparence Loi 25."),
    "legal.data_collected": (
        9,
        0.6,
        "Types de renseignements personnels = obligatoire pour la politique.",
    ),
    "legal.rpp_title": (8, 0.2, "Titre RPP requis pour la politique de confidentialité."),
    "legal.cookie_consent": (
        8,
        0.4,
        "Mode de consentement (opt-in vs full-management) imposé par Loi 25.",
    ),
    "legal.retention": (7, 0.3, "Durée de conservation des données — exigée par art. 23."),
    "legal.third_party_services": (
        7,
        0.4,
        "Services tiers à déclarer (analytics, hébergeur, etc.).",
    ),
    "legal.transfer_outside_qc": (
        6,
        0.2,
        "Transfert hors Québec — déclencheur clause spécifique si oui.",
    ),
    "legal.transfer_countries": (6, 0.2, "Pays de transfert — requis si transfert hors QC."),
    "company.name": (5, 0.0, "Nom de l'entreprise — sans, le brief n'est même pas valide."),
    "company.address": (4, 0.0, "Adresse — utile pour mentions légales."),
    "company.email": (4, 0.0, "Courriel public — utile pour contact form."),
    "company.phone": (3, 0.0, "Téléphone — optionnel sauf domaine."),
    "company.neq": (3, 0.0, "NEQ — utile pour mentions légales."),
}

_DEFAULT_PRIORITY = (2, 0.1, "Champ supplémentaire de complétion.")


def _question_for(field: str, message: str) -> str:
    """Reformule le message en question UX-friendly."""
    if field == "legal.rpp_email":
        return "Quel est le courriel du responsable de la protection des renseignements personnels (RPP) ?"
    if field == "legal.rpp_name":
        return "Quel est le nom du RPP ?"
    if field == "legal.rpp_title":
        return "Quel est le titre / fonction du RPP ?"
    if field == "legal.purposes":
        return "Pour quelles finalités collectez-vous des renseignements personnels (livraison, marketing, support, etc.) ?"
    if field == "legal.data_collected":
        return "Quels types de renseignements personnels collectez-vous (nom, courriel, paiement, navigation, etc.) ?"
    if field == "legal.retention":
        return "Combien de temps conservez-vous ces renseignements ?"
    if field == "legal.cookie_consent":
        return (
            "Souhaitez-vous un bandeau cookies opt-in simple, ou une gestion granulaire complète ?"
        )
    if field == "legal.third_party_services":
        return "Quels services tiers utilisez-vous (hébergeur, analytics, paiement, emailing) ?"
    if field == "legal.transfer_outside_qc":
        return "Des renseignements sortent-ils du Québec (hébergeur, sous-traitant) ?"
    if field == "legal.transfer_countries":
        return "Vers quels pays ces renseignements sont-ils transférés ?"
    return message


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Retourne les gaps triés par priorité avec lift μ estimé."""
    gaps_raw = payload.get("gaps") or []
    gaps = [g for g in gaps_raw if isinstance(g, dict)]

    enriched: list[dict[str, Any]] = []
    for gap in gaps:
        field = str(gap.get("field", ""))
        message = str(gap.get("message", ""))
        label = gap.get("label") or field
        blocking = bool(gap.get("blocking", True))

        prio, lift, rationale = _FIELD_PRIORITY.get(field, _DEFAULT_PRIORITY)
        # Bonus de priorité si le gap est marqué bloquant côté legal-gap-checker
        if blocking and prio < 10:
            prio = min(10, prio + 1)

        enriched.append(
            {
                "field": field,
                "label": str(label),
                "priority_score": float(prio),
                "question": _question_for(field, message),
                "rationale": rationale,
                "blocking": blocking,
                "estimated_mu_lift": round(lift, 2),
            }
        )

    # Tri décroissant par priorité, puis par lift (tie-break)
    enriched.sort(key=lambda q: (-q["priority_score"], -q["estimated_mu_lift"]))

    blocking_count = sum(1 for q in enriched if q["blocking"])
    lifting_mu_delta = round(sum(q["estimated_mu_lift"] for q in enriched), 2)

    return {
        "module_id": "intake-question-prioritizer",
        "questions": enriched,
        "blocking_count": blocking_count,
        "lifting_mu_delta": lifting_mu_delta,
    }
