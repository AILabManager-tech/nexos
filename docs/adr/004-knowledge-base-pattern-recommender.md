# ADR 004 — Knowledge base + pattern-recommender (v4.1)

- **Date** : 2026-04 (planifié)
- **Statut** : **Proposed** — chantier knowledge **en stand-by** jusqu'à la fin du chantier `mise_a_niveau` (v4.2.0).
- **Contexte** : Les sites générés par NEXOS se ressemblent trop (même hero, mêmes cards, même palette neutre). Aucune variable d'identité visuelle n'est capturée explicitement dans le brief, et les agents retombent sur des "défauts" partagés.

## Décision planifiée

Introduire `agents/knowledge/` contenant :

- **30 sites de référence** (cartographie patterns réels, par secteur).
- **20 patterns** canoniques (hero typés, layouts cards, navs, etc.).
- **6 dimensions de personnalité visuelle** (ex. sobriété ↔ audace, densité ↔ respiration, chaleur ↔ neutralité…).

Un nouvel agent `pattern-recommender` exécuté en **`ph1`** consomme cette knowledge et produit `pattern-recommendation.json`, consommé par `ph2 design` comme directive contraignante.

## Règle d'or

Deux clients configurés **opposés** sur ≥ 4 des 6 dimensions doivent produire des sites qui semblent **venir d'agences différentes**. Test de validation à bâtir : comparaison visuelle deux-par-deux par un évaluateur indépendant.

## Conséquences attendues

- ✅ Différenciation visible, mesurable, auditable.
- ❌ Complexité `ph1` augmentée (nouvelle sortie + gate).
- ❌ Maintenance du référentiel — les patterns vieillissent ; plan de révision trimestrielle à prévoir.

## Statut chantier

Détails dans `maintenance + upgrade/chantier d'enrichissement de la base de connaissances NEXOS/` (phases A→N, en stand-by).

## Références

- `NEXOS_Web_Patterns_Reference.md` (30 sites, racine monorepo)
- `Modèles de sites web par secteur — Feed NEXOS.md`
