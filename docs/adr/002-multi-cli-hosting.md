# ADR 002 — Multi-CLI hosting (Claude Code, Codex, Gemini)

- **Date** : 2026-03
- **Statut** : Accepté
- **Contexte** : Dépendre d'un seul LLM provider = risque de discontinuité (coût, rate limits, changements d'API, disponibilité régionale).

## Décision

Abstraire l'exécution des agents derrière `session_launcher`, qui lance **Codex**, **Claude Code** ou **Gemini** selon la config du mode/phase. Les règles métier sont dupliquées dans :

- `CLAUDE.md` (Claude Code — hôte interactif, arbitrages produit)
- `AGENTS.md` (Codex — moteur d'exécution pipeline)
- `GEMINI.md` (Gemini — alternative provider)

Contenu identique pour la couche "règles absolues" ; rôle et style d'interaction diffèrent.

## Conséquences

- ✅ Redondance provider — bascule possible en cas d'incident.
- ✅ A/B testing possible entre LLMs sur une même phase.
- ❌ **Trois fichiers à maintenir synchronisés** — divergence facile.
- ❌ Nuances de prompting (Claude verbeux vs Codex concis) non uniformisables par simple copie.

## Suivi

- Automatiser la sync `CLAUDE.md / AGENTS.md / GEMINI.md` pour la section "règles absolues" (script TBD).
- Ajouter un test CI qui diff les trois fichiers et flagge toute divergence sur la section commune.

## Références

- `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`
- `nexos/session_launcher.py`
