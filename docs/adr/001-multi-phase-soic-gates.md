# ADR 001 — Pipeline multi-phase avec quality gates SOIC

- **Date** : 2026-02 (rétrospectif)
- **Statut** : Accepté
- **Contexte** : Un pipeline unique de génération web produisait des résultats incohérents. Difficile de diagnostiquer à quelle étape une régression qualité apparaissait.

## Décision

Découper le pipeline en **6 phases séquentielles** — `ph0 discovery`, `ph1 strategy`, `ph2 design`, `ph3 content`, `ph4 build`, `ph5 qa`. Chaque transition de phase passe par un **gate SOIC** (seuil μ configurable dans `soic/gate.py`). L'échec d'une gate déclenche `auto_fix` + retry.

## Seuils

| Transition | Seuil μ |
|---|---|
| ph0 → ph1 | 7.0 |
| ph1 → ph2 | 8.0 |
| ph2 → ph3 | 8.0 |
| ph3 → ph4 | 8.0 |
| ph4 → tooling | BUILD PASS |
| ph5 → deploy | 8.5 |

## Conséquences

- ✅ Diagnostic fin (quelle phase a dégradé μ).
- ✅ Modularité : ajouter un mode `audit` = utiliser `ph5` uniquement ; `content` = `ph3` uniquement.
- ❌ Complexité accrue — 46+ agents à maintenir au lieu d'un prompt monolithique.
- ❌ Overhead temps — ~10 appels CLI par pipeline `create`.

## Alternatives considérées

- **Pipeline unique + LLM judge** — rejeté (non déterministe, μ non mesurable).
- **2 phases (brief → output)** — insuffisant pour détecter les régressions par dimension (D1–D8).

## Références

- `agents/ph<N>-*/_orchestrator.md`
- `nexos/config.py`
- `soic/gate.py`, `soic/evaluate.py`
