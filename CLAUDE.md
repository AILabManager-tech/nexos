# NEXOS v4.2 — Web Builder Autonome Premium

**Version** : 4.2.0
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

## SYMLINKS

```
core-v3 → ~/projects/ai/ainova-os-v3
osiris  → ~/osiris-scanner
```
