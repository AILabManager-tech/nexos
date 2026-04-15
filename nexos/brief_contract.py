"""Contrat canonique du brief NEXOS.

Normalise les variations historiques du brief et valide les champs
minimums requis par le runtime.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

VALID_MODES = {"create", "audit", "modify", "content", "analyze"}

CONSENT_MODE_MAP = {
    "opt-in (recommandé Loi 25)": "opt-in",
    "opt-out": "opt-out",
    "gestion complète (granulaire)": "full-management",
    "gestion complete (granulaire)": "full-management",
    "full-management": "full-management",
    "opt-in": "opt-in",
}

DATA_TYPE_MAP = {
    "téléphone": "telephone",
    "telephone": "telephone",
}

PURPOSE_MAP = {
    "communication": "formulaire-contact",
    "marketing": "infolettre",
    "commandes": "commandes",
    "analytics": "analytics",
}


def _clean_str(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value).strip() or None


def _clean_list(values: Any) -> list[str]:
    if not values:
        return []
    if not isinstance(values, list):
        values = [values]
    cleaned: list[str] = []
    for value in values:
        item = _clean_str(value)
        if item and item not in cleaned:
            cleaned.append(item)
    return cleaned


def _normalize_consent_mode(value: Any) -> str:
    consent_mode = _clean_str(value) or "opt-in"
    return CONSENT_MODE_MAP.get(consent_mode, consent_mode)


def _normalize_data_types(values: Any) -> list[str]:
    return [DATA_TYPE_MAP.get(item, item) for item in _clean_list(values)]


def _normalize_purposes(values: Any) -> list[str]:
    return [PURPOSE_MAP.get(item, item) for item in _clean_list(values)]


def normalize_brief(raw_brief: dict[str, Any], mode: str | None = None) -> dict[str, Any]:
    """Retourne un brief canonique et rétrocompatible."""
    brief = deepcopy(raw_brief or {})
    meta = brief.setdefault("_meta", {})
    resolved_mode = mode or meta.get("mode") or brief.get("mission", {}).get("mode") or "create"
    if resolved_mode not in VALID_MODES:
        resolved_mode = "create"

    client = brief.setdefault("client", {})
    company = brief.get("company", {}) if isinstance(brief.get("company"), dict) else {}
    legal = brief.get("legal", {}) if isinstance(brief.get("legal"), dict) else {}
    site = brief.get("site", {}) if isinstance(brief.get("site"), dict) else {}
    context = brief.get("context", {}) if isinstance(brief.get("context"), dict) else {}
    design = brief.get("design", {}) if isinstance(brief.get("design"), dict) else {}
    adaptive = brief.get("adaptive", {}) if isinstance(brief.get("adaptive"), dict) else {}
    mission = brief.get("mission", {}) if isinstance(brief.get("mission"), dict) else {}

    client_name = (
        _clean_str(client.get("name"))
        or _clean_str(brief.get("company_name"))
        or _clean_str(legal.get("company_name"))
        or _clean_str(company.get("name"))
        or _clean_str(brief.get("inputs", {}).get("client_name"))
    )
    client_slug = (
        _clean_str(client.get("slug"))
        or _clean_str(company.get("slug"))
        or _clean_str(brief.get("slug"))
    )

    rpp = legal.get("rpp", {}) if isinstance(legal.get("rpp"), dict) else {}
    company_address = _clean_str(legal.get("address")) or _clean_str(company.get("address"))
    company_phone = _clean_str(legal.get("phone")) or _clean_str(company.get("phone"))
    company_email = _clean_str(legal.get("email")) or _clean_str(company.get("email"))
    rpp_name = _clean_str(legal.get("rpp_name")) or _clean_str(rpp.get("name"))
    rpp_email = _clean_str(legal.get("rpp_email")) or _clean_str(rpp.get("email")) or company_email
    rpp_title = _clean_str(legal.get("rpp_title")) or _clean_str(rpp.get("title"))
    incident = legal.get("incident", {}) if isinstance(legal.get("incident"), dict) else {}

    normalized_legal = {
        "company_name": client_name,
        "neq": _clean_str(legal.get("neq")) or _clean_str(company.get("neq")),
        "address": company_address,
        "phone": company_phone,
        "email": company_email,
        "rpp_name": rpp_name,
        "rpp_email": rpp_email,
        "rpp_title": rpp_title,
        "rpp": {
            "name": rpp_name,
            "email": rpp_email,
            "title": rpp_title,
        },
        "data_collected": _normalize_data_types(
            legal.get("data_collected") or legal.get("data_types")
        ),
        "data_types": _normalize_data_types(legal.get("data_types") or legal.get("data_collected")),
        "purposes": _normalize_purposes(legal.get("purposes")),
        "retention": _clean_str(legal.get("retention")),
        "transfer_outside_qc": bool(legal.get("transfer_outside_qc", False)),
        "transfer_countries": _clean_list(legal.get("transfer_countries")),
        "third_parties": _clean_list(
            legal.get("third_parties") or legal.get("third_party_services")
        ),
        "third_party_services": _clean_list(
            legal.get("third_party_services") or legal.get("third_parties")
        ),
        "cookie_consent": _normalize_consent_mode(
            legal.get("cookie_consent") or legal.get("consent_mode")
        ),
        "consent_mode": _normalize_consent_mode(
            legal.get("consent_mode") or legal.get("cookie_consent")
        ),
        "incident_process": bool(
            legal.get("incident_process", incident.get("process_in_place", False))
        ),
        "incident_email": _clean_str(legal.get("incident_email"))
        or _clean_str(incident.get("notification_email"))
        or rpp_email,
        "incident": {
            "process_in_place": bool(
                legal.get("incident_process", incident.get("process_in_place", False))
            ),
            "notification_email": _clean_str(legal.get("incident_email"))
            or _clean_str(incident.get("notification_email"))
            or rpp_email,
        },
    }

    normalized_site = {
        "stack": _clean_str(site.get("stack")) or _clean_str(brief.get("stack")) or "nextjs",
        "type": _clean_str(site.get("type")) or "vitrine",
        "pages": _clean_list(site.get("pages")),
        "languages": _clean_list(site.get("languages")) or ["fr", "en"],
        "features": _clean_list(site.get("features")),
        "hosting": _clean_str(site.get("hosting")) or "Vercel",
        "domain": _clean_str(site.get("domain")),
        "existing_url": _clean_str(site.get("existing_url") or site.get("url") or brief.get("url")),
    }

    normalized = {
        "_meta": {
            "generator": "nexos-v3.0",
            "created_at": _clean_str(meta.get("created_at")),
            "mode": resolved_mode,
        },
        "client": {
            "name": client_name,
            "slug": client_slug,
        },
        "company_name": client_name,
        "company": {
            "name": client_name,
            "slug": client_slug,
            "neq": normalized_legal["neq"],
            "address": company_address,
            "phone": company_phone,
            "email": company_email,
        },
        "legal": normalized_legal,
        "site": normalized_site,
        "context": {
            "competitors": _clean_list(context.get("competitors")),
            "keywords_seo": _clean_list(context.get("keywords_seo")),
            "free_text": _clean_str(context.get("free_text")),
        },
        "design": {
            "palette": _clean_str(design.get("palette")),
            "typography": _clean_str(design.get("typography")),
            "style": _clean_str(design.get("style")),
            "logo_provided": bool(design.get("logo_provided", False)),
            "references": _clean_list(design.get("references")),
        },
        "adaptive": adaptive,
        "mission": mission,
    }
    return normalized


def validate_brief(brief: dict[str, Any]) -> list[str]:
    """Valide les champs minimums requis par le runtime NEXOS."""
    errors: list[str] = []
    meta = brief.get("_meta", {})
    client = brief.get("client", {})
    legal = brief.get("legal", {})
    site = brief.get("site", {})

    if meta.get("mode") not in VALID_MODES:
        errors.append("mode invalide")
    if not _clean_str(client.get("name")):
        errors.append("client.name requis")
    if not _clean_str(client.get("slug")):
        errors.append("client.slug requis")
    for field in (
        "company_name",
        "address",
        "phone",
        "email",
        "rpp_name",
        "rpp_email",
        "rpp_title",
        "retention",
    ):
        if not _clean_str(legal.get(field)):
            errors.append(f"legal.{field} requis")
    if "transfer_outside_qc" not in legal:
        errors.append("legal.transfer_outside_qc requis")
    if not _clean_str(legal.get("cookie_consent")):
        errors.append("legal.cookie_consent requis")
    if not _clean_str(site.get("type")):
        errors.append("site.type requis")
    if not _clean_list(site.get("pages")):
        errors.append("site.pages requis")
    if not _clean_list(site.get("languages")):
        errors.append("site.languages requis")
    return errors
