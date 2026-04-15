# ADR 005 — Refactor `orchestrator.py` (god-object) en classes (v4.2)

- **Date** : 2026-04
- **Statut** : Accepté — phases **O** et **P** du chantier `mise_a_niveau`.
- **Contexte** : `orchestrator.py` = **1 710 lignes, 27 fonctions, 0 classe**. État implicite partagé via variables de module, coupling élevé avec SOIC et auto_fixer, impossible à tester unitairement, cognitive overhead important pour tout nouveau contributeur.

## Décision

Refactor en deux étapes :

### Phase O — Extraction en classes (même fichier)

Extraire **trois classes** avec responsabilités disjointes :

- `PipelineOrchestrator` — drive le flux `ph0 → ph5`, gère le contexte client, déclenche les transitions de phase.
- `GateEngine` — évalue les gates SOIC, interprète les seuils par transition, retourne verdict + dimension défaillante.
- `ConvergeLoop` — boucle de convergence (retry/auto-fix) pour les gates qui échouent.

### Phase P — Modularisation (fichiers séparés)

Éclater vers :

```
orchestrator/
├── __init__.py
├── pipeline.py       # PipelineOrchestrator
├── gates.py          # GateEngine
├── converge.py       # ConvergeLoop
└── main.py           # CLI entry + parse args
orchestrator.py       # ≤ 200 lignes, re-export pour backward compat
```

## Conséquences

- ✅ Testable unitairement (fixtures par classe, pas de monkey-patch global).
- ✅ Lisible par un nouveau contributeur en < 10 min (chaque fichier = 1 responsabilité).
- ❌ Risque de régression pendant le refactor — **filet de sécurité = test E2E phase I** (déjà en place).

## Invariants à préserver

- Interface CLI identique (`nexos create`, `nexos modify`, etc. — pas de breaking change user-facing).
- `nexos-changelog.json` continue à être appendé aux mêmes événements.
- Seuils SOIC inchangés (ADR 001).

## Références

- `orchestrator.py` (avant refactor)
- `tests/test_e2e_orchestrator.py` (filet phase I)
- `maintenance + upgrade/mise_a_niveau/PHASE_O_REFACTOR_ORCHESTRATOR_CLASSES.md`
- `maintenance + upgrade/mise_a_niveau/PHASE_P_REFACTOR_ORCHESTRATOR_MODULARISATION.md`
