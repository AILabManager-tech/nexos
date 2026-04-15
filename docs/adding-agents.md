# Contribuer un agent NEXOS

Ce guide explique comment ajouter un nouvel agent au pipeline NEXOS.

## Où vivent les agents

Tous les agents sont des fichiers Markdown placés dans :

```
agents/<phase>/<slug>.md
```

où `<phase>` ∈ `ph0-discovery | ph1-strategy | ph2-design | ph3-content | ph4-build | ph5-qa | site-update | knowledge`.

Chaque phase contient aussi un `_orchestrator.md` qui liste l'ordre d'exécution et les dépendances entre agents.

## Structure d'un agent

Front-matter YAML **obligatoire** en tête de fichier :

```yaml
---
id: <slug>                 # kebab-case, unique (ex: csp-generator)
phase: ph4-build           # une des phases listées ci-dessus
tags: [security, i18n]     # domaines (ux, seo, security, i18n, a11y, perf, content, legal…)
stack: ["*"]               # ["*"] | ["nextjs"] | ["astro"] | ["fastapi"] — filtrage stack
site_types: ["*"]          # ["*"] | ["vitrine", "ecommerce", "portfolio", "saas", "blog"]
required: true             # true = bloquant, false = best-effort
priority: 0                # 0 = toujours, 1 = souvent, 2 = rare
---
```

Corps du fichier (sections recommandées) :

```markdown
# Agent · <Nom humain lisible>

## Rôle
[2-3 lignes : ce que l'agent produit, dans quelle phase, pour qui.]

## Entrées
[Liste des fichiers lus (brief, rapports de phases précédentes) et variables attendues.]

## Sortie
[Nom du fichier produit dans `clients/<slug>/` + schéma JSON strict si applicable.]

## Prompt
[Le prompt envoyé au CLI hôte. Structuré en ROLE, CONTEXT, MISSION, OUTPUT FORMAT.]

## Invariants / garde-fous
[Ce que l'agent NE DOIT JAMAIS faire, ne jamais inventer, ne jamais contredire.]
```

## Étapes pour créer un nouvel agent

1. **Cloner un agent similaire**
   Choisir le `agents/ph<N>-*/_orchestrator.md` de la phase cible et un agent existant de la même phase comme **template stylistique**.
2. **Nommer**
   Slug en `kebab-case`, descriptif (`csp-generator`, `i18n-translator`, **pas** `agent-12`).
3. **Rédiger le prompt**
   Niveau **runbook** (grade A+). Exemples concrets, schemas JSON stricts, invariants explicites.
4. **Mettre à jour `_orchestrator.md`**
   Lister le nouvel agent dans le flux de la phase (ordre + dépendances avec les autres agents).
5. **Vérifier l'enregistrement**
   `nexos/agent_registry.py` découvre les agents automatiquement via glob. Valider avec :
   ```bash
   nexos doctor
   ```
6. **Tester**
   Lancer sur un client fictif (`clients/.template/`) et vérifier que la sortie produit bien le fichier attendu au bon endroit.
7. **Documenter**
   Entrée dans `CHANGELOG.md` + **commit isolé** (un agent = un commit).

## Checklist qualité A+

- [ ] Front-matter YAML complet (tous les champs obligatoires renseignés).
- [ ] Prompt structuré (ROLE / CONTEXT / MISSION / OUTPUT FORMAT).
- [ ] Schema JSON strict pour la sortie si l'agent produit du JSON.
- [ ] ≥ 1 exemple de sortie attendue, dans le prompt.
- [ ] Invariants / garde-fous explicites (ex. "ne jamais utiliser `dangerouslySetInnerHTML`").
- [ ] Aucune règle métier qui contredit `CLAUDE.md` / `AGENTS.md` / `GEMINI.md`.
- [ ] Si outil externe requis (Lighthouse, pa11y, curl) : mentionné **+ fallback documenté** si absent.
- [ ] Entrée dans `_orchestrator.md` de la phase cible.
- [ ] Testé sur au moins un client fictif.

## Règles absolues rappelées

- **Loi 25** — un agent qui touche aux cookies, données utilisateur, formulaires, analytics doit se coordonner avec `auto_fixer` (cf [ADR 003](./adr/003-auto-fix-d4-d8.md)).
- **Sécurité** — jamais de clé API côté client, jamais de `dangerouslySetInnerHTML` sans DOMPurify, headers HTTP obligatoires.
- **UsineRH** — interdiction triple niveau ; aucun agent ne doit lister, scanner, référencer UsineRH ou ses variantes.

## Voir aussi

- [ADR 001 — Pipeline multi-phase SOIC](./adr/001-multi-phase-soic-gates.md)
- [ADR 002 — Multi-CLI](./adr/002-multi-cli-hosting.md)
- [`CLAUDE.md`](../CLAUDE.md), [`AGENTS.md`](../AGENTS.md), [`GEMINI.md`](../GEMINI.md)
