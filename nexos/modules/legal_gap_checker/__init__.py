"""Détecte les champs Loi 25 manquants avant lancement du pipeline."""

from __future__ import annotations

from typing import Any

from nexos.brief_contract import normalize_brief, validate_brief

_LEGAL_FIELD_LABELS = {
    "legal.company_name": "Dénomination sociale",
    "legal.address": "Adresse de l'entreprise",
    "legal.phone": "Téléphone de contact",
    "legal.email": "Courriel de contact",
    "legal.rpp_name": "Nom du RPP",
    "legal.rpp_email": "Courriel du RPP",
    "legal.rpp_title": "Titre du RPP",
    "legal.retention": "Durée de conservation",
    "legal.transfer_outside_qc": "Transfert hors Québec",
    "legal.transfer_countries": "Pays de transfert",
    "legal.cookie_consent": "Mode de consentement cookies",
    "legal.data_collected": "Renseignements collectés",
    "legal.purposes": "Finalités de collecte",
    "legal.third_party_services": "Services tiers",
}


def _clean_list(value: Any) -> list[str]:
    if not value:
        return []
    if not isinstance(value, list):
        value = [value]
    return [str(item).strip() for item in value if str(item).strip()]


def _gap(
    field: str, message: str, *, severity: str = "error", blocking: bool = True
) -> dict[str, Any]:
    return {
        "field": field,
        "label": _LEGAL_FIELD_LABELS.get(field, field),
        "severity": severity,
        "blocking": blocking,
        "message": message,
    }


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Retourne les écarts Loi 25 bloquants et les prochaines questions à poser."""
    raw_brief = payload.get("brief")
    if not isinstance(raw_brief, dict):
        raw_brief = payload

    mode = str(payload.get("mode") or raw_brief.get("_meta", {}).get("mode") or "create")
    brief = normalize_brief(raw_brief, mode=mode)
    legal = brief.get("legal", {})

    gaps: list[dict[str, Any]] = []
    for error in validate_brief(brief):
        if error.startswith("legal."):
            field = error.removesuffix(" requis")
            gaps.append(_gap(field, error))

    if not _clean_list(legal.get("data_collected")):
        gaps.append(_gap("legal.data_collected", "Types de renseignements collectés requis"))
    if not _clean_list(legal.get("purposes")):
        gaps.append(_gap("legal.purposes", "Finalités de collecte requises"))
    if not _clean_list(legal.get("third_party_services")):
        gaps.append(
            _gap(
                "legal.third_party_services",
                "Services tiers requis, au minimum l'hébergeur et les outils analytics",
            )
        )

    consent_mode = str(legal.get("cookie_consent") or "")
    if consent_mode and consent_mode not in {"opt-in", "full-management"}:
        gaps.append(
            _gap(
                "legal.cookie_consent",
                "Consentement cookies incompatible avec la règle NEXOS: opt-in requis",
            )
        )

    if legal.get("transfer_outside_qc") and not _clean_list(legal.get("transfer_countries")):
        gaps.append(
            _gap(
                "legal.transfer_countries",
                "Pays de transfert requis quand des données sortent du Québec",
            )
        )

    next_questions = [
        {
            "field": gap["field"],
            "question": gap["message"],
            "required": gap["blocking"],
        }
        for gap in gaps
    ]

    blocking_count = sum(1 for gap in gaps if gap["blocking"])
    return {
        "module_id": "legal-gap-checker",
        "ready_for_pipeline": blocking_count == 0,
        "blocking_count": blocking_count,
        "gaps": gaps,
        "next_questions": next_questions,
    }
