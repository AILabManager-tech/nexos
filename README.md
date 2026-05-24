# NEXOS v4.4 — Pipeline Web Autonome

> Pipeline web autonome avec quality gates SOIC — conforme Loi 25 Québec.
> Version **4.4.0** — voir [`CHANGELOG.md`](./CHANGELOG.md).
> Source de vérité version : fichier [`VERSION`](./VERSION) à la racine (lu par CI + scripts).

[![Tests](https://github.com/AILabManager-tech/nexos-v3/actions/workflows/test.yml/badge.svg)](https://github.com/AILabManager-tech/nexos-v3/actions/workflows/test.yml)
[![Lint](https://github.com/AILabManager-tech/nexos-v3/actions/workflows/lint.yml/badge.svg)](https://github.com/AILabManager-tech/nexos-v3/actions/workflows/lint.yml)
[![Security](https://github.com/AILabManager-tech/nexos-v3/actions/workflows/security.yml/badge.svg)](https://github.com/AILabManager-tech/nexos-v3/actions/workflows/security.yml)
[![codecov](https://codecov.io/gh/AILabManager-tech/nexos-v3/branch/main/graph/badge.svg)](https://codecov.io/gh/AILabManager-tech/nexos-v3)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

NEXOS est un systeme de creation et d'audit de sites web professionnels pilote par IA.
Il orchestre 56 agents specialises a travers 6 phases sequentielles avec quality gates SOIC (9 dimensions).

Objectif : **qualite premium des la premiere generation** (score SOIC >= 8.5/10).

## Knowledge-driven Design

NEXOS s'appuie maintenant sur une knowledge base exploitable en ph1-strategy:

- `agents/knowledge/web-patterns-reference.md` : 30 sites de reference et 20 patterns P01-P20
- `agents/knowledge/sector-references.json` : catalogue machine-readable des references
- `agents/knowledge/pattern-matrix.json` : matrice patterns x secteurs x impact SOIC
- `agents/knowledge/personality-dimensions.json` : 6 dimensions D1-D6 et regle d'or
- `agents/ph1-strategy/pattern-recommender.md` : recommandation patterns + references + 6D + opposition check

Regle d'or : deux clients configures avec des valeurs opposees sur >= 4 des 6 dimensions doivent sembler venir de deux agences differentes.

## Quick Start

```bash
# 1. Installer la commande CLI (venv + extras + pre-commit hooks)
bash install_nexos.sh --dev

# 2. Lancer l'accueil NEXOS interactif
nexos

# 3. Verifier que le systeme est operationnel
nexos doctor

# 4. Creer un site complet depuis un brief
nexos create --brief clients/.template/brief-client.json

# 5. Auditer un site existant
nexos audit --client-dir clients/mon-client --url https://example.com

# 6. Corriger automatiquement un client
nexos fix clients/mon-client
nexos fix clients/mon-client --dry-run   # apercu sans appliquer
```

Alternative Docker (voir `docs/docker.md`) :

```bash
docker compose up gateway                        # API :8000
docker compose run --rm nexos nexos doctor       # CLI one-shot
docker compose --profile dev up                  # hot-reload dev
```

`nexos` sans argument ouvre un accueil interactif :
1. Menu principal (`create`, `audit`, `modify`, etc.)
2. Selection du CLI hote (Claude Code, Codex, Gemini)
3. Recommandation + forces/faiblesses de chaque CLI selon le type de travail
4. Ecran de resume final avec confirmation ou retour arriere
5. Lancement du CLI choisi avec bootstrap NEXOS

Astuce : `Entree` accepte le choix recommande, `b` revient en arriere, `q` quitte.

## Prerequis

| Outil | Version min | Critique | Installation |
|-------|-------------|----------|-------------|
| Python | 3.10+ | Oui | systeme |
| Node.js | 20.0+ | Oui | https://nodejs.org |
| npm | inclus | Oui | inclus avec Node |
| Codex CLI | latest | Oui | `npm i -g @openai/codex` |
| Lighthouse | latest | Non | `npm i -g lighthouse` |
| pa11y | latest | Non | `npm i -g pa11y` |

Verifiez avec `nexos doctor` pour un diagnostic complet.

## Architecture

```
NEXOS v4.0 = Multi-phase x Quality Gates x Tooling Reel x Auto-Fix

                    orchestrator.py (1663 lignes)
                         |
          +--------------+--------------+
          |              |              |
     nexos/         agents/        templates/
   (10 modules)   (56 agents)    (39 fichiers)
   (5232 lignes)                 (5 stacks)
          |              |
  +-------+-------+     +-- ph0-discovery (6)
  |       |       |     +-- ph1-strategy  (6)
  | tooling_mgr   |     +-- ph2-design    (6)
  | build_valid    |     +-- ph3-content   (6)
  | auto_fixer     |     +-- ph4-build     (7)
  | cli_commands   |     +-- ph5-qa       (18)
  | brief_wizard   |     +-- site-update   (6)
  | agent_registry |     +-- knowledge
  | pipeline_config|
  | changelog      |
  | session_launcher|
  +-------+-------+
          |
     soic/ (symlink)
    Quality Gates 9D
```

## Modes d'operation

| Commande | Description |
|----------|-------------|
| `nexos create --brief <path>` | Creation complete ph0 -> ph5 |
| `nexos audit --client-dir <dir> --url <url>` | Audit site existant (ph5-qa) |
| `nexos modify --client-dir <dir>` | Modification ciblee |
| `nexos content --client-dir <dir>` | Redaction/traduction (ph3) |
| `nexos analyze --client-dir <dir>` | Discovery seule (ph0) |
| `nexos converge <dir> --target 8.5` | Boucle convergence SOIC |
| `nexos doctor` | Diagnostic systeme |
| `nexos fix <dir> [--dry-run]` | Auto-correction D4/D8 |
| `nexos report <dir>` | Rapport agrege client |

### Options transversales

| Option | Description |
|--------|-------------|
| `--stack nextjs\|nuxt\|astro\|fastapi` | Stack technique cible |
| `--profile web-nextjs\|web-generic\|api-fastapi\|code-python` | Profil SOIC |
| `--colors primary=#HEX accent=#HEX ...` | Palette de couleurs imposee |
| `--section S-NNN` | Cibler une section specifique (mode modify) |

## Pipeline de creation (mode `create`)

```
ph0-discovery -> ph1-strategy -> ph2-design -> ph3-content -> ph4-build -> ph5-qa
     |               |              |             |             |          |
   mu>=7.0        mu>=8.0       mu>=8.0       mu>=8.0     BUILD PASS  mu>=8.5
                                                               |
                                                         auto-fix si FAIL
                                                         (try-fix-retry)
```

Chaque transition est gardee par un quality gate SOIC (9 dimensions, score mu pondere).
Le threshold de deploiement est mu >= 8.5 a la sortie de ph5-qa.

### Quality Gates SOIC — 9 Dimensions

| Dim | Domaine | Poids |
|-----|---------|-------|
| D1 | Architecture | x1.0 |
| D2 | Documentation | x0.8 |
| D3 | Tests | x0.9 |
| D4 | Securite | x1.2 |
| D5 | Performance | x1.0 |
| D6 | Accessibilite | x1.1 |
| D7 | SEO | x1.0 |
| D8 | Conformite legale (Loi 25) | x1.1 |
| D9 | Code Quality | x0.9 |

D4 et D8 sont **bloquants** : un site ne peut pas etre deploye avec D8 < 7.0.

## Auto-Fix v4.0

Le module `nexos/auto_fixer.py` corrige automatiquement les problemes recurrents :

| Fix | Dimension | Description |
|-----|-----------|-------------|
| Cookie consent | D8 Loi 25 | Copie template + injection dans layout.tsx |
| npm audit fix | D4 Securite | Corrige les vulnerabilites connues |
| Vercel headers | D4 Securite | Ajoute les 6 headers requis |
| next.config | D4 Securite | `poweredByHeader: false` |
| Politique confidentialite | D8 Loi 25 | Genere la page depuis template + brief |
| Mentions legales | D8 Loi 25 | Genere la page depuis template + brief |

## Templates multi-stack

| Stack | Templates | Statut |
|-------|-----------|--------|
| `nextjs/` | 6 fichiers (next.config, tailwind, vercel, etc.) | Production |
| `nuxt/` | nuxt.config, tailwind, README | Production |
| `astro/` | astro.config, tailwind, README | Production |
| `fastapi/` | main.py, requirements.txt, README | Production |
| `generic/` | brief-schema, brief-intake, etc. | Production |

Templates securises additionnels : cookie-consent, privacy-policy, legal-mentions, sitemap, robots, og-image, ad-unit.

## Structure client

```
clients/{slug}/
+-- brief-client.json          # Brief client (donnees legales Loi 25)
+-- section-manifest.json      # Registre des sections (S-NNN)
+-- ph0-discovery-report.md    # Rapport phase 0
+-- ph1-strategy-report.md     # Rapport phase 1
+-- ph2-design-report.md       # Rapport phase 2
+-- ph3-content-report.md      # Rapport phase 3
+-- ph4-build-log.md           # Log de build
+-- ph5-qa-report.md           # Rapport QA final
+-- soic-gates.json            # Historique des quality gates
+-- nexos-changelog.json       # Audit trail append-only
+-- tooling/                   # Resultats scans (lighthouse, pa11y, etc.)
+-- site/                      # Code source du site
```

## Portfolio — Sites generes par NEXOS

| Projet | Secteur | Score SOIC | Tests | Lighthouse Perf |
|--------|---------|-----------|-------|-----------------|
| [Collectif Nova](https://github.com/AILabManager-tech/collectif-nova) | Agence creative, Montreal | 9.48 | 158 | 98 |
| [Clinique Aura](https://github.com/AILabManager-tech/clinique-aura) | Clinique multidisciplinaire, Sherbrooke | 9.47 | 131 | 96 |
| [Table de Marguerite](https://github.com/AILabManager-tech/table-de-marguerite) | Bistro gastronomique, Vieux-Quebec | 9.41 | 206 | 95 |
| [Beaumont Avocats](https://github.com/AILabManager-tech/beaumont-avocats) | Cabinet d'avocats, Quebec | 9.38 | 113 | 97 |
| [Vertex PMO](https://github.com/AILabManager-tech/vertex-pmo) | Gestion de projet, Gatineau-Ottawa | 9.23 | 111 | 87 |
| [Electro-Maitre](https://github.com/AILabManager-tech/electro-maitre-site) | Electricien industriel, Monteregie | 8.72 | — | — |

Tous les sites sont bilingues (FR/EN), conformes Loi 25 du Quebec, avec headers de securite complets.

## Stack technique par defaut

- **Framework** : Next.js 15+ (App Router)
- **Langage** : TypeScript 5 (strict mode)
- **CSS** : Tailwind CSS 3.4+ / 4
- **Tests** : Vitest + @testing-library/react
- **i18n** : next-intl (FR/EN minimum)
- **Icons** : Lucide React
- **Animations** : Framer Motion (avec prefers-reduced-motion)
- **Deploiement** : Vercel
- **Conformite** : Loi 25 du Quebec (obligatoire)

## Tooling CLI

Scans automatises avant Phase 5 :

```bash
tools/preflight.sh <URL> <CLIENT_DIR>
```

| Outil | Script | Description |
|-------|--------|-------------|
| Lighthouse | `lighthouse-scan.sh` | Performance, a11y, SEO, best practices |
| pa11y | `a11y-scan.sh` | WCAG 2.0 AA |
| Headers | `headers-scan.sh` | Verification headers securite |
| SSL | `ssl-scan.sh` | Certificat et configuration TLS |
| Dependencies | `deps-scan.sh` | npm audit vulnerabilites |

## Tests

13 fichiers de tests couvrant tous les modules `nexos/` :

```bash
cd nexos_v.3.0
python -m pytest tests/ -v
```

## Coordination multi-CLI

NEXOS supporte 3 CLI hotes. Les regles metier (securite, Loi 25, SOIC, phases) sont identiques.

| CLI | Fichier | Role |
|-----|---------|------|
| Claude Code | `CLAUDE.md` | Hote interactif (structuration, redaction, arbitrages) |
| Codex CLI | `AGENTS.md` | Moteur d'execution (generation de code) |
| Gemini CLI | `GEMINI.md` | Hote alternatif |

## Documentation

| Document | Description |
|----------|-------------|
| [CLAUDE.md](CLAUDE.md) | Specification architecturale complete |
| [CHANGELOG.md](CHANGELOG.md) | Historique des versions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guide de contribution |
| [INTEGRATION.md](INTEGRATION.md) | Design tokens et patches agents |
| [docs/api-reference.md](docs/api-reference.md) | Reference API modules nexos/ |
| [docs/architecture.md](docs/architecture.md) | Architecture detaillee |
| [docs/deployment.md](docs/deployment.md) | Guide de deploiement |
| [docs/troubleshooting.md](docs/troubleshooting.md) | Erreurs frequentes et solutions |
| [docs/CLI_GUIDE.md](docs/CLI_GUIDE.md) | Guide CLI complet |

## License

Propriete de Mark Systems. Voir [LICENSE](LICENSE).

---

# NEXOS v4.0 — Autonomous Web Pipeline

NEXOS is an AI-driven system for creating and auditing professional websites.
It orchestrates 56 specialized agents across 6 sequential phases with SOIC quality gates (9 dimensions).

Goal: **premium quality from the first generation** (SOIC score >= 8.5/10).

## Quick Start

```bash
# 1. Install the CLI command
bash install_nexos.sh

# 2. Launch the interactive NEXOS welcome screen
nexos

# 3. Verify the system is operational
nexos doctor

# 4. Create a complete site from a brief
nexos create --brief clients/.template/brief-client.json

# 5. Audit an existing site
nexos audit --client-dir clients/my-client --url https://example.com

# 6. Auto-fix a client project
nexos fix clients/my-client
nexos fix clients/my-client --dry-run   # preview without applying
```

## Key Features

- **56 specialized agents** across 6 phases (discovery, strategy, design, content, build, QA)
- **SOIC quality gates** between each phase (9 weighted dimensions, mu threshold)
- **Real CLI tooling** (Lighthouse, pa11y, curl, npm audit) before LLM agents
- **Auto-fix** for security (D4) and legal compliance (D8) issues
- **Multi-stack support**: Next.js, Nuxt, Astro, FastAPI
- **Quebec Law 25 compliance** built-in (cookie consent, privacy policy, legal notices)
- **Multi-CLI orchestration**: Claude Code, Codex CLI, Gemini CLI
- **Bilingual by default**: FR/EN with next-intl

## Pipeline

```
ph0-discovery -> ph1-strategy -> ph2-design -> ph3-content -> ph4-build -> ph5-qa
     |               |              |             |             |          |
   mu>=7.0        mu>=8.0       mu>=8.0       mu>=8.0     BUILD PASS  mu>=8.5
```

Each transition is guarded by a SOIC quality gate (9 dimensions, weighted mu score).
The deployment threshold is mu >= 8.5 at ph5-qa exit.

## Commands

| Command | Description |
|---------|-------------|
| `nexos create --brief <path>` | Full creation ph0 -> ph5 |
| `nexos audit --client-dir <dir> --url <url>` | Audit existing site (ph5-qa) |
| `nexos modify --client-dir <dir>` | Targeted modification |
| `nexos content --client-dir <dir>` | Content/translation only (ph3) |
| `nexos analyze --client-dir <dir>` | Discovery only (ph0) |
| `nexos converge <dir> --target 8.5` | SOIC convergence loop |
| `nexos doctor` | System diagnostics |
| `nexos fix <dir> [--dry-run]` | Auto-fix D4/D8 standalone |
| `nexos report <dir>` | Aggregated client report |

## Portfolio — Sites Generated by NEXOS

| Project | Sector | SOIC Score | Tests | Lighthouse Perf |
|---------|--------|-----------|-------|-----------------|
| [Collectif Nova](https://github.com/AILabManager-tech/collectif-nova) | Creative agency, Montreal | 9.48 | 158 | 98 |
| [Clinique Aura](https://github.com/AILabManager-tech/clinique-aura) | Multidisciplinary clinic, Sherbrooke | 9.47 | 131 | 96 |
| [Table de Marguerite](https://github.com/AILabManager-tech/table-de-marguerite) | Gastronomic bistro, Old Quebec | 9.41 | 206 | 95 |
| [Beaumont Avocats](https://github.com/AILabManager-tech/beaumont-avocats) | Law firm, Quebec City | 9.38 | 113 | 97 |
| [Vertex PMO](https://github.com/AILabManager-tech/vertex-pmo) | Project management, Gatineau-Ottawa | 9.23 | 111 | 87 |
| [Electro-Maitre](https://github.com/AILabManager-tech/electro-maitre-site) | Industrial electrician, Monteregie | 8.72 | — | — |

All sites are bilingual (FR/EN), Quebec Law 25 compliant, with full security headers.

## Default Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **Language**: TypeScript 5 (strict mode)
- **CSS**: Tailwind CSS 3.4+ / 4
- **Testing**: Vitest + @testing-library/react
- **i18n**: next-intl (FR/EN minimum)
- **Icons**: Lucide React
- **Animations**: Framer Motion (with prefers-reduced-motion)
- **Deployment**: Vercel
- **Compliance**: Quebec Law 25 (mandatory)

## Architecture

- `orchestrator.py` — Central engine (1663 lines)
- `nexos/` — 10 augmentation modules (5232 lines total)
- `agents/` — 56 specialized agents in 6 phases + site-update
- `templates/` — 39 files across 5 stacks (nextjs, nuxt, astro, fastapi, generic)
- `soic/` — Quality gate engine (9 dimensions, profiles, convergence)
- `tools/` — 9 CLI scanning scripts (Lighthouse, pa11y, headers, SSL, deps)
- `tests/` — 13 test files

## License

Property of Mark Systems. See [LICENSE](LICENSE).
