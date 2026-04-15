# ADR 006 — Logging stdlib (au lieu de structlog / loguru)

- **Date** : 2026-04 (phase F du chantier `mise_a_niveau`)
- **Statut** : Accepté
- **Contexte** : 220 appels à `print()` dispersés dans le code à migrer vers un système de logging structuré. Choix à faire entre `logging` stdlib et libs externes (`structlog`, `loguru`).

## Décision

Utiliser **`logging` stdlib**. Zéro nouvelle dépendance. Format unifié, `context-adapter` custom pour injecter `client` / `phase` / `agent` dans chaque record.

## Raisons

1. **Zéro dep externe** — cohérent avec la discipline "minimiser la surface de dépendances" du chantier.
2. **Compatibilité native** avec tout le stack Python : `pytest caplog`, `uvicorn` access logs, `FastAPI` handlers, subprocess output streaming.
3. **Niveau configurable** via `NEXOS_LOG_LEVEL` (cf ADR 007 config centralisée / `nexos/config.py`).
4. **Format JSON optionnel** activable via env var — sans dép, en utilisant `logging.Formatter` custom.

## Conséquences

- ✅ Zéro dep externe ajoutée.
- ✅ Compatible pytest, uvicorn, FastAPI, subprocess out-of-the-box.
- ✅ `NEXOS_LOG_LEVEL=DEBUG` active tous les détails sans modification code.
- ❌ Moins ergonomique que `loguru` pour les cas avancés (sinks fichiers par niveau, rotation) — à adresser si besoin futur avec des handlers custom.

## Alternatives considérées

- **structlog** — rejeté, sur-dimensionné pour le besoin actuel. Intéressant si on passe à un backend d'observabilité (Loki, Datadog). À réévaluer si ce besoin émerge.
- **loguru** — rejeté, API non-standard (pas compatible avec les bibliothèques tierces qui attendent `logging.Logger`).

## Références

- `nexos/logging_config.py`
- Commit `f6452ec — refactor(chantier2-F): structured logging replaces 220 print() calls`
