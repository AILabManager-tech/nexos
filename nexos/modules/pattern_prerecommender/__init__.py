"""Recommande des patterns web avant Ph1 en lisant la knowledge base NEXOS.

Lit `agents/knowledge/pattern-matrix.json` au runtime. Score chaque pattern
selon son `by_sector[sector_id]` (tier 1 = recommandation forte, tier 3 =
faible). Retourne le top-K.

Si le secteur est inconnu, on retourne les 3 patterns universels les plus
hauts en `tier_default`.

Mots-clés simples → mapping secteur. Suffisant pour un preview avant brief
définitif. La vraie classification est faite en Ph0/Ph1 par les agents LLM.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

# Mapping mots-clés FR/EN → secteur. Adaptable selon l'ajout de nouveaux SEC-XX.
_SECTOR_KEYWORDS = {
    "SEC-01": ("santé", "physio", "physiotherap", "clinique", "médical", "medical", "health"),
    "SEC-02": ("services", "professionnel", "consult", "agence", "agency", "cabinet"),
    "SEC-03": ("commerce", "boutique", "ecommerce", "shop", "épicerie", "restaurant", "depanneur"),
    "SEC-04": ("construction", "rénovation", "industrie", "manufacture", "fabrication"),
    "SEC-05": ("éducation", "formation", "école", "training", "academy"),
    "SEC-06": ("organisme", "communauté", "association", "ngo", "nonprofit"),
}


@lru_cache(maxsize=1)
def _load_pattern_matrix() -> dict[str, Any]:
    """Charge `agents/knowledge/pattern-matrix.json` depuis l'arborescence repo.

    Le module est dans `nexos/nexos/modules/pattern_prerecommender/` ;
    la KB est en `nexos/agents/knowledge/pattern-matrix.json` (4 parents).
    """
    here = Path(__file__).resolve()
    candidates = [
        here.parents[3] / "agents" / "knowledge" / "pattern-matrix.json",
        here.parents[2] / "agents" / "knowledge" / "pattern-matrix.json",
        Path.cwd() / "agents" / "knowledge" / "pattern-matrix.json",
    ]
    for c in candidates:
        if c.is_file():
            data: Any = json.loads(c.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
    raise FileNotFoundError(
        f"pattern-matrix.json introuvable. Cherché dans: {', '.join(str(c) for c in candidates)}"
    )


def _infer_sector(brief: dict[str, Any]) -> str | None:
    """Devine le secteur depuis le brief (description, mission, sector field)."""
    haystack_parts = []
    if isinstance(brief.get("company"), dict):
        haystack_parts.append(str(brief["company"].get("name") or ""))
    if isinstance(brief.get("mission"), dict):
        haystack_parts.append(json.dumps(brief["mission"], ensure_ascii=False).lower())
    if isinstance(brief.get("context"), dict):
        haystack_parts.append(json.dumps(brief["context"], ensure_ascii=False).lower())
    if isinstance(brief.get("site"), dict):
        haystack_parts.append(json.dumps(brief["site"], ensure_ascii=False).lower())
    if isinstance(brief.get("sector"), str):
        haystack_parts.append(brief["sector"].lower())

    haystack = " ".join(haystack_parts).lower()
    if not haystack.strip():
        return None

    best: tuple[str, int] | None = None
    for sec_id, keywords in _SECTOR_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in haystack)
        if score > 0 and (best is None or score > best[1]):
            best = (sec_id, score)
    return best[0] if best else None


def _score_patterns(
    matrix: dict[str, Any], sector_id: str | None, top_k: int
) -> list[dict[str, Any]]:
    """Retourne le top-K patterns scorés pour ce secteur."""
    patterns = matrix.get("patterns", [])

    scored: list[tuple[int, dict[str, Any]]] = []
    for p in patterns:
        by_sector = p.get("by_sector") or {}
        tier_default = p.get("tier_default") or 3
        # Lower tier = better (1 = strongest recommendation)
        if sector_id:
            raw = by_sector.get(sector_id)
            tier_for_sector = raw if isinstance(raw, int) else tier_default
        else:
            tier_for_sector = tier_default
        # Invert for sorting: higher score = better recommendation
        invert = 4 - int(tier_for_sector)
        scored.append((invert, p))

    scored.sort(key=lambda t: (-t[0], t[1].get("id", "")))

    out: list[dict[str, Any]] = []
    for invert, p in scored[:top_k]:
        tier = 4 - invert
        out.append(
            {
                "id": str(p.get("id", "")),
                "name": str(p.get("name", "")),
                "tier_score": tier,
                "rationale": (
                    f"Pattern tier {tier} pour secteur {sector_id}"
                    if sector_id
                    else f"Pattern universel tier {tier} (secteur non identifié)"
                ),
                "reference_sites": list(p.get("reference_sites") or []),
                "soic_dimensions_impacted": list(p.get("soic_dimensions_impacted") or []),
            }
        )

    return out


def run(payload: dict[str, Any]) -> dict[str, Any]:
    """Retourne top-K patterns recommandés depuis brief + secteur."""
    brief = payload.get("brief") if isinstance(payload.get("brief"), dict) else {}
    sector_id = payload.get("sector_id")
    top_k = int(payload.get("top_k", 3))

    if not sector_id:
        sector_id = _infer_sector(brief or {})

    matrix = _load_pattern_matrix()
    patterns = _score_patterns(matrix, sector_id, top_k)

    return {
        "module_id": "pattern-prerecommender",
        "patterns": patterns,
        "sector_id": sector_id,
        "fallback": sector_id is None,
    }
