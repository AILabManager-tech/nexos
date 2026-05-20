"""Synthétise un intake réduit en brief canonique NEXOS."""

from __future__ import annotations

import re
import unicodedata
from typing import Any

from nexos.brief_contract import normalize_brief, validate_brief


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug or "client"


def _dict_value(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Retourne un brief canonique et son état de validation."""
    mode = str(payload.get("mode") or "create")
    company = _dict_value(payload, "company")
    legal = _dict_value(payload, "legal")
    site = _dict_value(payload, "site")
    design = _dict_value(payload, "design")
    context = _dict_value(payload, "context")

    company_name = str(company.get("name") or payload.get("company_name") or "").strip()
    slug = str(company.get("slug") or "").strip() or _slugify(company_name)

    raw_brief = {
        "_meta": {"mode": mode, "generator": "nexos-module-brief-synthesizer"},
        "client": {"name": company_name, "slug": slug},
        "company": {
            "name": company_name,
            "slug": slug,
            "neq": company.get("neq"),
            "address": company.get("address"),
            "phone": company.get("phone"),
            "email": company.get("email"),
        },
        "legal": legal,
        "site": {
            "stack": site.get("stack", "nextjs"),
            "type": site.get("type", "vitrine"),
            "pages": site.get("pages", ["accueil", "contact"]),
            "languages": site.get("languages", ["fr", "en"]),
            "features": site.get("features", []),
            "hosting": site.get("hosting", "Vercel"),
            "domain": site.get("domain"),
            "existing_url": site.get("existing_url"),
        },
        "design": design,
        "context": context,
        "adaptive": _dict_value(payload, "adaptive"),
        "mission": _dict_value(payload, "mission"),
        "sector": payload.get("sector"),
        "tags": payload.get("tags", []),
    }

    brief = normalize_brief(raw_brief, mode=mode)
    validation_errors = validate_brief(brief)
    return {
        "module_id": "brief-synthesizer",
        "brief": brief,
        "validation_errors": validation_errors,
        "ready_for_pipeline": not validation_errors,
    }
