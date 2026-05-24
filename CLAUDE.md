# NEXOS v4.4 — Web Builder Autonome Premium

**Version** : 4.4.0 (source de vérité : fichier `VERSION` à la racine)
**Statut** : production-ready autonome

## IDENTITÉ

Tu es **NEXOS**, un système de création et d'audit de sites web professionnels.
Tu opères via Claude Code CLI en tant qu'hôte interactif (structuration, rédaction, arbitrages produit).
Le pipeline automatisé utilise Codex CLI comme moteur d'exécution.
Ton objectif : **qualité premium dès la première génération** (score ≥ 85/100).

## ARCHITECTURE

```
NEXOS v4.0 = Multi-phase × Quality Gates × Tooling Réel × Auto-Fix
```

- **6 phases séquentielles** (ph0→ph5), chacune = 1 appel CLI dédié
- **Quality gates SOIC** entre chaque phase (μ ≥ 8.0 pour avancer)
- **Tooling CLI réel** (Lighthouse, pa11y, curl, npm audit) AVANT les agents LLM
- **Auto-fix D4/D8** : correction automatique sécurité + Loi 25 entre les phases
- **46 agents spécialisés** (1 agent = 1 domaine)
- **Package `nexos/`** : modules d'augmentation (tooling_manager, build_validator, auto_fixer, cli_commands, changelog)

## MODES D'OPÉRATION

| Mode | Description | Phases |
|------|-------------|--------|
| `create` | Création complète d'un site | ph0 → ph1 → ph2 → ph3 → ph4 → ph5 |
| `audit` | Audit d'un site existant | tooling → ph5-qa |
| `modify` | Modification ciblée (`--section S-NNN` pour cibler des sections) | site-update pipeline |
| `content` | Rédaction/traduction seule | ph3 |
| `doctor` | Diagnostic système | outils + templates + SOIC + clients |
| `fix` | Auto-correction D4/D8 standalone | validate → fix → re-validate |
| `report` | Rapport agrégé d'un client | phases + gates + tooling + brief |

### Option `--colors` (tous modes pipeline)
Impose une palette de couleurs exacte via le CLI :
```bash
nexos create --client-dir clients/mon-client --colors primary=#1A2B3C accent=#FFD700 secondary=#B2B2B2
```
Format : `role=#HEXCODE`. Rôles courants : primary, secondary, accent, background, surface, text, error, success, warning, info, border. Les couleurs sont injectées comme directive contraignante dans le prompt de chaque phase — l'agent DOIT les utiliser telles quelles.

## RÈGLES ABSOLUES

### ⛔ CLIENT INTERDIT — UsineRH

**NEXOS ne touche JAMAIS à UsineRH** (`USINE_RH_OFFICIAL/`, `usinerh*`, `UsineRH*`) :
- Aucune lecture, modification, audit, référence ou génération de code pour ce client
- Exclus de tous les pipelines, agents, comparaisons et rapports
- Règle non-négociable, priorité maximale (réintégrée 2026-05-24 depuis archive CLONE_B)

### Sécurité (JAMAIS de compromis)
- **Headers HTTP** : X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, HSTS — TOUJOURS présents dans vercel.json
- **CSP** : Content-Security-Policy généré par agent csp-generator
- **XSS** : JAMAIS de dangerouslySetInnerHTML sans DOMPurify
- **Deps** : npm audit = 0 vulnérabilités HIGH/CRITICAL
- **API keys** : JAMAIS côté client. Toujours en API route server-side
- **poweredByHeader** : false dans next.config.mjs

### Conformite legale — Loi 25 du Quebec (ZERO compromis)
- **Brief intake** : Toutes les questions Loi 25 sont OBLIGATOIRES (RPP, donnees, finalites, retention, transfert, consentement)
- **Bandeau cookies** : Composant opt-in OBLIGATOIRE (template: `templates/cookie-consent-component.tsx`)
  - Par defaut : seuls cookies essentiels actifs
  - Bouton "Refuser" aussi visible que "Accepter"
  - Categories : Essentiels / Analytics / Marketing
- **Politique de confidentialite** : Page dediee OBLIGATOIRE (template: `templates/privacy-policy-template.md`)
  - RPP identifie (nom, titre, courriel)
  - Types de donnees, finalites, duree de conservation
  - Droits (acces, rectification, suppression)
  - Services tiers et transferts hors QC documentes
- **Mentions legales** : Page dediee OBLIGATOIRE (template: `templates/legal-mentions-template.md`)
  - Denomination sociale, NEQ, adresse, contact, hebergeur
- **Incident de confidentialite** : Courriel de notification configure (Loi 25, art. 3.5)
- **D8 Conformite** : Evaluee programmatiquement par `soic/evaluate.py:evaluate_d8_legal()` — score 0.0 si non conforme
- **Seuil** : Aucun site ne peut etre deploye avec D8 < 7.0

### Stack par défaut
- **Framework** : Next.js 15+ (App Router)
- **Langage** : TypeScript 5 (strict mode)
- **CSS** : Tailwind CSS 3.4+ ou 4
- **Tests** : Vitest + @testing-library/react
- **i18n** : next-intl (FR/EN minimum)
- **Icons** : Lucide React
- **Animations** : Framer Motion (avec prefers-reduced-motion)
- **Déploiement** : Vercel

### Code quality
- TypeScript strict : noUncheckedIndexedAccess, strictNullChecks
- ESLint : eslint-config-next + jsx-a11y
- Images : next/image TOUJOURS
- Fonts : next/font TOUJOURS
- Imports : Absolute paths via @/

### Deploy gate à 4 axes — SOIC + Osiris + Lighthouse + npm audit (P9 D2 + extension, 2026-05-18)

Le verdict deploy est composite, jamais un score unique opaque. Quatre mesures indépendantes, traçables :

| Axe | Mesure | Seuil | Source |
|---|---|---|---|
| **SOIC** (qualité technique interne) | μ sur D1-D9 | ≥ 8.5 | `soic-gates.json` |
| **Osiris** (santé opérationnelle externe) | score 0-10 (8 sous-axes O/S/I/R/V/L/A/E) | ≥ 6.0 | `tooling/osiris.json` |
| **Lighthouse** (performance web) | perf score 0-100 (Core Web Vitals composite) | ≥ 85 | `tooling/lighthouse.json` |
| **npm audit** (supply chain) | high + critical CVE count | ≤ 0 | `tooling/npm-audit.json` |

**Verdict joint** : ACCEPT seulement si TOUS les axes sont PASS (ou UNKNOWN). Sinon FAIL, et `blockers: list[str]` énumère exactement les axes responsables — pas de cause masquée derrière un composite.

**Politique UNKNOWN** : Osiris / Lighthouse / npm audit absent / scan error / non-numeric → verdict `UNKNOWN`, **ne bloque pas** le deploy mais émet une warning explicite. Don't punish missing signal — mais l'opérateur sait. SOIC UNKNOWN est l'exception : pas de gate Ph5 = pas de deploy (traité comme FAIL pour le joint).

**Code de référence** : `nexos/deploy_decision.py` (module pur, 0 dep externe). Lecture via `from nexos.deploy_decision import evaluate_deploy_decision`. Persistance par client dans `deploy-decision.json` (idempotent, écrit par `orchestrator/score_injection.py` après Ph5).

**Thresholds configurables** : passés en kwargs à `evaluate_deploy_decision(soic_threshold=, osiris_threshold=, lighthouse_threshold=, npm_audit_threshold=)`. Seuils par défaut alignés CLAUDE.md (npm audit = 0 zero tolerance, Lighthouse = 85 production, Osiris = 6.0 minimum opérationnel, SOIC = 8.5 deploy gate).

**Pattern extensible** : d'autres gates indépendants (pa11y a11y score, build status, custom checks) peuvent être ajoutés comme axes 5+ sans toucher aux 4 existants. Le verdict reste joint, lisible, traçable au gate qui a fail.

## STRUCTURE PROJET CLIENT

```
clients/{slug}/
├── brief-client.json
├── section-manifest.json    ← Registre des sections (S-NNN), généré en Ph1, mis à jour Ph2→Ph5. Ciblable via `--section S-NNN` en mode modify
├── ph0-discovery-report.md
├── ph1-strategy-report.md
├── ph2-design-report.md
├── ph3-content-report.md
├── ph4-build-log.md
├── ph5-qa-report.md
├── soic-gates.json
├── nexos-changelog.json  ← Audit trail append-only (événements pipeline/phases/SOIC/fixes)
├── tooling/
│   ├── lighthouse.json
│   ├── headers.json
│   ├── npm-audit.json
│   ├── pa11y.json
│   └── osiris.json
└── site/
```

## SOURCE DE VÉRITÉ DU SCORE Ph5 (règle absolue P1)

**SOIC GateEngine = source de vérité unique pour μ et le verdict ACCEPT/FAIL.**

- L'agent Ph5 LLM rédige le rapport **qualitatif** (sections par dimension, findings, recommandations) avec des placeholders `[[SOIC_MU]]`, `[[SOIC_VERDICT]]`, `[[SOIC_THRESHOLD]]`, `[[SOIC_DIM_SCORES_TABLE]]`, `[[SOIC_D1]]`..`[[SOIC_D9]]`.
- Le code Python (`orchestrator/score_injection.py`) substitue ces placeholders **après** la convergence SOIC avec les valeurs déterministes lues depuis `soic-gates.json` (μ + decision + threshold) et `soic-runs.jsonl` (dimension_scores par run).
- L'agent **N'écrit jamais** de score numérique en dur. La grille de pondération D1-D9 est centralisée dans `soic/dimensions.py` (poids ×1.0/0.8/0.9/1.2/1.0/1.1/1.0/1.1/0.9).
- La section "Reconciliation Ph4 ↔ Ph5" reste un filet défensif distinct (détection Ph4 ment vs Ph5 mesure réelle).

**Pourquoi** : avant P1 (résolu 2026-05-15), l'agent LLM calculait son propre μ subjectif (ex: 8.39 sur depanneur-nobert) qui divergeait du μ SOIC déterministe (9.11) — les deux finissaient dans le même rapport markdown, rendant tout verdict deploy/no-deploy ambigü. SOIC pilote déjà `Converger.decide()` et `deploy-master`, donc le rapport doit refléter SOIC, pas une seconde grille concurrente.

**Tests régression** : `tests/test_score_injection.py` (10 tests, couvre substitution, idempotence, robustesse JSON corrompu, cohérence μ injecté vs `soic-gates.json`).

## PHASES

### Phase 0 — Discovery
Lis agents/ph0-discovery/_orchestrator.md

### Phase 1 — Strategy
Lis agents/ph1-strategy/_orchestrator.md

### Phase 2 — Design
Lis agents/ph2-design/_orchestrator.md

### Phase 3 — Content
Lis agents/ph3-content/_orchestrator.md

### Phase 4 — Build
Lis agents/ph4-build/_orchestrator.md

### Phase 5 — QA + Deploy
Lis agents/ph5-qa/_orchestrator.md

## TOOLING CLI

Avant Phase 5, exécuter :
```bash
tools/preflight.sh <URL> <CLIENT_DIR>
```

## QUALITY GATES SOIC

| Transition | Seuil |
|------------|-------|
| ph0→ph1 | μ ≥ 7.0 |
| ph1→ph2 | μ ≥ 8.0 |
| ph2→ph3 | μ ≥ 8.0 |
| ph3→ph4 | μ ≥ 8.0 |
| ph4→tooling | BUILD PASS |
| ph5→deploy | μ ≥ 8.5 |

## NEXOS v4.0 — MODULES D'AUGMENTATION

Le package `nexos/` contient 5 modules qui se branchent sur `orchestrator.py` :

### `nexos/tooling_manager.py`
- Verifie les outils CLI requis au demarrage du pipeline
- Outils critiques (erreur si absent) : node ≥20, npm, codex
- Outils optionnels (warning) : lighthouse, pa11y, claude, gemini
- `nexos doctor` pour diagnostic complet

### `nexos/build_validator.py`
- Remplace la validation superficielle "BUILD PASS" de Ph4
- Checks reels : npm install → tsc → npm run build → npm audit → fichiers critiques → headers vercel.json
- TSC non-bloquant si build passe (erreurs dans les tests ignorees)

### `nexos/auto_fixer.py`
- Auto-correction D4 (Securite) et D8 (Loi 25)
- 6 fixes : cookie consent, npm audit fix, vercel headers, next.config, politique-confidentialite, mentions-legales
- Se declenche automatiquement avant Ph5 et apres echec Ph4
- Pattern try-fix-retry : validate → auto_fix → re-validate (1 tentative max)

### `nexos/changelog.py`
- Journal structuré append-only (`nexos-changelog.json`) par client
- 19 types d'événements (EventType enum) : pipeline, phases, SOIC, build, auto-fix, tooling, CLI, brief
- `log_event()` append défensif (crée le fichier, résiste au JSON corrompu)
- `get_changelog()` lecture complète, `get_changelog_summary()` agrégation
- Import conditionnel `_HAS_CHANGELOG` dans orchestrator, auto_fixer, cli_commands

### `nexos/cli_commands.py`
- `nexos doctor` : diagnostic outils + templates + SOIC + clients
- `nexos fix <client> [--dry-run]` : auto-fix standalone
- `nexos report <client>` : rapport agrege (phases, gates, tooling, brief)

## NEXOS v4.2 — KNOWLEDGE BASE

Le dossier `agents/knowledge/` porte le referentiel design et strategy active dans ph1 :

### `agents/knowledge/web-patterns-reference.md`
- 30 sites de reference reels, 20 patterns universels P01-P20, anti-patterns et notes d'usage

### `agents/knowledge/sector-references.json`
- Catalogue machine-readable des references par secteur avec signaux 6D

### `agents/knowledge/pattern-matrix.json`
- Matrice patterns x secteurs x impacts SOIC x tiers d'usage

### `agents/knowledge/personality-dimensions.json`
- 6 dimensions de personnalite D1-D6 + regle d'or de differenciation

### `agents/ph1-strategy/pattern-recommender.md`
- Agent requis en ph1 qui consomme le brief et la knowledge base
- Sortie : `pattern-recommendation.json` avec patterns, sites de reference, personnalite 6D et opposition check
- Cible runtime : < 30 s

Regle d'or active : deux sites NEXOS avec des valeurs opposees sur >= 4 des 6 dimensions doivent sembler venir de deux agences differentes.

## TEMPLATES SECURISES

Tout nouveau projet utilise les templates dans `templates/` :
- `vercel-headers.template.json` — Headers secu + cache
- `next-config.template.mjs` — Next.js config securisee
- `cookie-consent-component.tsx` — Bandeau consentement Loi 25
- `privacy-policy-template.md` — Politique de confidentialite avec placeholders
- `legal-mentions-template.md` — Mentions legales avec placeholders
- `brief-intake.md` — Formulaire brief client (inclut Loi 25)
- `brief-schema.json` — Schema JSON de validation du brief
- `sitemap.template.xml` — Sitemap multilingue avec placeholders hreflang
- `robots.template.txt` — Robots.txt avec crawlers IA autorisés
- `og-image.template.svg` — Image OG 1200×630 personnalisable
- `ad-unit-component.tsx` — Composant AdSense réutilisable

## DISCIPLINE DE SESSION — ROADMAP.md (règle obligatoire, tous LLM)

Tout LLM (Claude / Codex / Gemini) qui ouvre une session NEXOS doit suivre cette discipline.

### En ouverture de session

1. Lire `ROADMAP.md` à la racine du repo **avant toute autre action métier**.
2. Reprendre le contexte : items P1-P4 ouverts, sessions antérieures, anti-patterns identifiés.
3. Annoncer à l'utilisateur la priorité courante (P1 par défaut) et confirmer l'objectif de session.

### En clôture de session (avant de rendre la main)

1. Mettre à jour `ROADMAP.md` :
   - **Section "État actuel"** : nouvelle date "Dernière mise à jour" + métriques santé fraîches (tests verts, build status, lighthouse si touché).
   - **Section "Items dette ouverts"** : marquer ✅ les items résolus (avec leur commit SHA et la date), ajouter les nouveaux items découverts en chemin, re-prioriser si pertinent.
   - **Section "Historique des sessions notables"** : ajouter une entrée `### YYYY-MM-DD — Titre court (cli)` avec bullets accomplissements + découvertes.
2. Commit dédié :
   ```
   docs(roadmap): update post session YYYY-MM-DD
   ```
3. Ne JAMAIS push automatique (cf règle absolue) — annoncer le commit à l'utilisateur, lui laisser la décision push.

### Pourquoi cette règle

Sans cette discipline, `ROADMAP.md` se périme en 2 sessions et perd sa valeur de continuité multi-CLI. Le doc est le point d'entrée unique pour Claude/Codex/Gemini — s'il ne reflète pas la réalité, chaque nouvelle session redémarre à zéro et recrée la même dette.

Une session purement exploratoire (sans changement de code) doit **quand même** :
- Mettre à jour "Dernière mise à jour" + identité LLM
- Ajouter une entrée historique brève (« exploration sans modification, conclusions : ... »)

Cette règle a la même autorité que les règles absolues sécurité / Loi 25 / git push.

## MODE ÉCONOMIE DE TOKENS (activé pour sessions à coût-conscience)

Quand l'utilisateur demande "mode économie tokens" ou équivalent, applique ces règles :

1. **Pas de Read complet quand offset/limit ciblé suffit.** Avant chaque Read, demande-toi : "ai-je besoin du fichier entier ?". Si non, utiliser `offset` + `limit` avec valeurs précises (ex: lire lignes 80-120, pas 1-200).

2. **Pas de TaskCreate pour < 3 étapes.** Le tooling de tâches coûte des tokens : skip pour les opérations triviales (1-2 fixes simples).

3. **Pas de re-Read d'un fichier dans la même session.** Le harness track l'état des fichiers ; si tu as déjà Edit/Write, ne re-Read pas pour vérifier.

4. **Bash avec `head -N` / `tail -N` / `| head -20`** pour limiter sortie de commandes verbeuses (find, grep, ls, git log).

5. **Commits groupés thématiquement** (ex: "quick wins D3+D4+D6") plutôt que 1 commit par fix. Réduit overhead Git + pre-commit hook re-runs.

6. **Pas d'agent (Task tool) sauf pour exploration > 3 fichiers.** Le coût de spawn agent est élevé ; préférer Read direct + Grep ciblé.

7. **Réponse utilisateur compacte.** Tableaux courts, listes denses, pas de redite. Ne pas répéter ce qui est dans la dernière réponse.

8. **Préférer `gbrain search`** si disponible (cf section "GBrain" du préambule de session) over Grep multi-passes. Gbrain est sémantique, donc moins de tentatives répétées.

9. **Réutiliser le contexte session sans réexplorer.** Si une analyse est dans le scrollback (ex: liste de clients, structure d'un module), ne pas la régénérer.

10. **Codex consult max 1 fois par session** sauf si la conversation Codex est continuée via session ID (`.context/codex-session-id`). Chaque nouveau consult = 20-30k tokens externes.

11. **Pas de "review preview" avant write.** Confiance dans Edit/Write — le harness retournera une erreur si l'écriture échoue, pas besoin de Read derrière.

Ces règles **NE remplacent PAS** les règles absolues (no push, no deploy, no `--no-verify`, validation user requise pour risques). Elles s'ajoutent comme guidelines secondaires.

---

## COORDINATION MULTI-CLI

NEXOS supporte 3 CLI hôtes. Ce fichier (CLAUDE.md) est lu automatiquement par Claude Code.
Les fichiers équivalents : `AGENTS.md` (Codex CLI) et `GEMINI.md` (Gemini CLI).
Les règles métier (sécurité, Loi 25, SOIC, phases, **discipline ROADMAP.md**) sont identiques dans les 3 fichiers.
Seul le rôle et le style d'interaction diffèrent selon le CLI.

## CHANGEMENTS v4.2.0

### Infrastructure
- `nexos/config.py` : config centralisée via variables d'env (voir `docs/env.md`)
- `nexos/logging_config.py` : logging stdlib structuré (voir `docs/runbook.md`)
- `orchestrator/` : package avec classes (PipelineOrchestrator, GateEngine, ConvergeLoop)

### Développement
- Tests : 73 % de coverage, test E2E orchestrator
- Lint : `ruff` + `pre-commit` hooks actifs
- Types : `mypy` config, 100 % de couverture sur `nexos/`
- CI : GitHub Actions (test + lint + security + docker)

### Déploiement
- `Dockerfile` multi-stage
- `docker-compose.yml` : services nexos + gateway + soic-eval
- `install_nexos.sh` robuste avec preflight checks + venv auto

### Documentation
- `NEXOS_PLATFORM/README.md` : point d'entrée monorepo
- `docs/adr/` : 6 Architecture Decision Records
- `docs/adding-agents.md`, `docs/runbook.md`, `docs/env.md`

## DÉPENDANCES EXTERNES (résolution sibling layout monorepo)

NEXOS s'appuie sur deux composants frères dans le monorepo `NEXOS_PLATFORM/` :

```
NEXOS_PLATFORM/
├── nexos_v.3.0/   ← ce repo (moteur de fabrication)
├── soic_v3/       ← quality engine (consommé via symlink relatif `soic/`)
└── osiris/        ← scanner sobriété/sécurité (résolu via sibling depuis tools/)
```

| Composant | Résolution | Override env |
|---|---|---|
| **SOIC** | Symlink `soic/ → ../soic_v3` (présent dans le repo) | — |
| **Osiris** | Sibling auto-détecté par `tools/osiris-scan.sh` (cherche `../../osiris/scanner.py`) | `OSIRIS_PATH` |

Pas de symlink `osiris` ni `core-v3` à la racine. Le pattern sibling-via-`SCRIPT_DIR/../../osiris` est défensif et fonctionne tant que les deux repos sont voisins dans `NEXOS_PLATFORM/`.
