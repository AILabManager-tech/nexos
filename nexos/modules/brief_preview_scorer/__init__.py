"""Estime un score SOIC partiel depuis un brief sans lancer le pipeline.

Heuristique déterministe :
- Chaque dimension D1-D9 a un score de base (ce que NEXOS livre par défaut)
- La dimension est pénalisée si le brief est incomplet sur les champs qui la concernent
- D8 (Loi 25) est cappée par la complétude du bloc `legal` — c'est la seule
  dimension où l'humain doit fournir de l'info (les autres sont assurées par
  les auto-fixes pipeline)
- μ pondéré selon les poids SOIC officiels (cf. soic_v3/dimensions.py)
"""

from __future__ import annotations

from typing import Any

# Poids SOIC officiels (extraits de soic_v3/dimensions.py).
_DIMENSION_WEIGHTS = {
    "D1": 1.0,
    "D2": 0.8,
    "D3": 0.9,
    "D4": 1.2,
    "D5": 1.0,
    "D6": 1.1,
    "D7": 0.9,
    "D8": 1.5,  # Loi 25, fortement pondérée
    "D9": 1.0,
}

_DIMENSION_NAMES = {
    "D1": "Architecture",
    "D2": "Documentation",
    "D3": "Tests",
    "D4": "Sécurité",
    "D5": "Performance",
    "D6": "Accessibilité",
    "D7": "SEO",
    "D8": "Conformité Loi 25",
    "D9": "Code Quality",
}

# Score de base par dimension — ce que NEXOS livre sur un setup nominal.
_DIMENSION_BASE_SCORES = {
    "D1": 8.5,  # Next.js App Router + structure cible
    "D2": 7.5,  # README + Loi 25 docs auto
    "D3": 7.0,  # tests générés par défaut
    "D4": 8.5,  # auto-fix D4 (headers, npm audit, CSP)
    "D5": 8.0,  # Next.js par défaut
    "D6": 7.5,  # Tailwind + lucide accessible
    "D7": 8.0,  # sitemap + robots auto-générés
    "D8": 5.0,  # plafond bas si legal vide → relevé par brief
    "D9": 8.0,  # ruff + tsc strict
}

_LEGAL_REQUIRED = (
    "rpp_name",
    "rpp_email",
    "rpp_title",
    "data_collected",
    "purposes",
    "retention",
    "cookie_consent",
    "third_party_services",
)

_DESIGN_HINTS = ("brand_archetype", "tone", "personality_6d", "preferred_patterns")
_CONTENT_HINTS = ("languages", "pages", "features")


def _completeness(value: Any) -> float:
    """Score 0-1 de complétude d'un champ."""
    if value is None:
        return 0.0
    if isinstance(value, str):
        return 1.0 if value.strip() else 0.0
    if isinstance(value, (list, tuple, set)):
        return 1.0 if value else 0.0
    if isinstance(value, dict):
        return 1.0 if value else 0.0
    return 1.0


def _legal_score(legal: dict[str, Any]) -> tuple[float, list[str]]:
    """Score D8 + liste des champs manquants."""
    if not legal:
        return 0.0, list(_LEGAL_REQUIRED)
    missing = [k for k in _LEGAL_REQUIRED if not _completeness(legal.get(k))]
    filled_ratio = 1 - (len(missing) / len(_LEGAL_REQUIRED))
    # Plafond 9.5/10 : on ne peut pas atteindre 10 sans audit humain réel
    score = round(filled_ratio * 9.5, 2)
    return score, missing


def _design_score(design: dict[str, Any]) -> float:
    """Bonus D1 + D6 si signaux design fournis."""
    if not design:
        return 0.0
    filled = sum(1 for k in _DESIGN_HINTS if _completeness(design.get(k)))
    return min(1.0, filled / len(_DESIGN_HINTS))


def _content_score(site: dict[str, Any]) -> float:
    if not site:
        return 0.0
    filled = sum(1 for k in _CONTENT_HINTS if _completeness(site.get(k)))
    return min(1.0, filled / len(_CONTENT_HINTS))


def _weighted_mu(dimensions: dict[str, float]) -> float:
    num = sum(score * _DIMENSION_WEIGHTS[d] for d, score in dimensions.items())
    den = sum(_DIMENSION_WEIGHTS[d] for d in dimensions)
    return round(num / den, 2) if den else 0.0


def _safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Retourne un score SOIC estimé + ventilation 9D + niveau de confiance."""
    brief = _safe_dict(payload.get("brief"))
    legal = _safe_dict(brief.get("legal"))
    site = _safe_dict(brief.get("site"))
    design = _safe_dict(brief.get("design"))
    company = _safe_dict(brief.get("company"))

    # D8 — score driven par le legal (c'est la dimension la plus
    # impactée par la qualité du brief).
    d8_score, missing_legal = _legal_score(legal)

    # D6/D1 — bonus jusqu'à +0.5 si design renseigné
    design_bonus = 0.5 * _design_score(design)

    # D7/D2 — bonus jusqu'à +0.5 si content/i18n renseigné
    content_bonus = 0.5 * _content_score(site)

    dimensions: dict[str, dict[str, Any]] = {}
    raw_scores: dict[str, float] = {}
    for d, base in _DIMENSION_BASE_SCORES.items():
        if d == "D8":
            score = d8_score
            rationale = (
                f"{len(missing_legal)} champ(s) Loi 25 manquant(s)"
                if missing_legal
                else "Bloc legal complet (audit humain final requis pour atteindre 10)"
            )
        elif d == "D1":
            score = min(10.0, base + design_bonus)
            rationale = (
                "Architecture Next.js standard + bonus design renseigné"
                if design_bonus
                else "Architecture Next.js standard"
            )
        elif d == "D6":
            score = min(10.0, base + design_bonus)
            rationale = "Tailwind + lucide accessible" + (
                " + signaux design" if design_bonus else ""
            )
        elif d == "D7":
            score = min(10.0, base + content_bonus)
            rationale = "sitemap + robots auto-générés" + (
                " + i18n renseigné" if content_bonus else ""
            )
        elif d == "D2":
            score = min(10.0, base + content_bonus)
            rationale = "README + Loi 25 auto" + (" + contenu renseigné" if content_bonus else "")
        else:
            score = base
            rationale = f"Score par défaut NEXOS pour {_DIMENSION_NAMES[d]}"

        raw_scores[d] = round(score, 2)
        dimensions[d] = {
            "score": round(score, 2),
            "name": _DIMENSION_NAMES[d],
            "rationale": rationale,
        }

    estimated_mu = _weighted_mu(raw_scores)

    # Confiance — proportion de blocs significatifs renseignés
    fields_filled = sum(
        _completeness(x) for x in (company.get("name") if company else None, legal, design, site)
    )
    confidence = round(fields_filled / 4, 2)

    gating_factors = [f"legal.{k}" for k in missing_legal]
    if not company or not _completeness(company.get("name")):
        gating_factors.insert(0, "company.name")

    return {
        "module_id": "brief-preview-scorer",
        "estimated_mu": estimated_mu,
        "dimensions": dimensions,
        "confidence": confidence,
        "gating_factors": gating_factors,
    }
