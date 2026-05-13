# NEXOS — CHANGELOG

## [Chantier 5 — Phase A] — 2026-05-11→13

### Added
- **`nexos/module_registry.py`** : registre modulaire avec discovery via `manifest.json`, validation JSON Schema Draft 2020-12 input/output, exécution `registry.run(module_id, payload)` avec erreurs typées (`ModuleNotFoundError`, `ModuleContractError`).
- **`nexos/workflow_runner.py`** : composition déclarative de modules en workflows, contexte step-to-step, trace par étape.
- **3 modules opérationnels** : `hello` (canari), `brief-synthesizer` (intake → brief canonique), `legal-gap-checker` (détection champs Loi 25 manquants + `next_questions`).
- **1 workflow** : `intake-preflight` (brief-synthesizer → legal-gap-checker).
- **Sous-commandes CLI** : `nexos module list/validate/run`, `nexos workflow list/run`.
- **`jsonschema>=4.0`** promu en dependency runtime.
- **13 nouveaux tests** (`test_module_registry`, `test_workflow_runner`, `test_brief_synthesizer_module`, `test_legal_gap_checker_module`).

### Pushed
- `e36fcbe` feat(modules) — registre + workflow runner + 3 modules
- `2c545b2` feat(cli) — sous-commandes nexos module/workflow

Cf. `../_etat_des_lieux/14_chantier_5_modularisation.md`.

## [4.3.0] — 2026-05-10

### Added (Chantier 4 — dette pipeline structurelle, 11 items)
- **Item 1** : `W-18 CumulativeLayoutShiftGate` côté SOIC + intégration côté Ph4 (commit `993a762`). Bloque CLS > 0.25, FAIL > 0.5.
- **Item 2** : `build_validator._count_test_files()` + `_run_tests()` (mode WARNING en v4.3.x, FAIL en v4.4.0). Commit `f9f1150`.
- **Item 3** : `orchestrator/reconciliation.py` — filet défensif WARNING si écart μ Ph4↔Ph5 > 2 pts. Commit `e5450cf`.
- **Item 4** : `tools/osiris-scan.sh` réécrit avec timeout + 3 retries backoff + budget 5min. Commit `9418037`.
- **Item 5** : `_check_critical_files()` détecte `app/` moderne **et** `src/app/` legacy. Commit `88e09e0`.
- **A-002** : `orchestrator/ph4_sync.py` barrière quiescence FS. Commit `9be746c`.
- **A-003** : `gate_display.format_gate_result()` distingue ABORT/REJECT. Commit `02e28b9`.
- **A-004** : `detect_rate_limit_in_log()` + retry/pivot Claude→Codex. Commit `f0b861b`.
- **A-008** : regex PE-02 étendue (5 labels + markdown bold). Commit `3a11987` + soic_v3 `a52b171`.
- **A-009** : RFC fixture drift + scripts freeze/audit Phase 1. Commit `3645c4e`.
- **A-010** : deps-scan validation JSON avant émission. Commit `2276467`.

### Fixed
- Pipeline **honnête** : Ph4 ne ment plus silencieusement, reconciliation Ph4↔Ph5 catch les divergences, rate-limit Claude → retry/pivot Codex au lieu de FAIL.

### Tests
- Passage 285 → 373 tests verts (+88 régression).

### Pushed
- 11 commits sur `origin/main` 2026-05-13 (rattrapage du push différé)
- Tag `v4.3.0` poussé

## [4.2.2] — 2026-05-10

### Added (Chantier mode B — pipeline end-to-end)
- Pipeline `nexos create --client-dir clients/depanneur-nobert --stack nextjs` validé from scratch (μ ph5 = 9.47).
- `BUG_NEXOS_HEADERS_SCAN_DUPLICATE_KEY` (A-007) fix dédup bash + 3 tests (`bae3c20`).
- `BUG_NEXOS_SOIC_GATES_OVERWRITE` (A-005) extraction `gates_persistence.py` + 12 tests (`6bbbec1`).
- `BUG_NEXOS_PH5_AUTO_FIXER` (A-006) JSX natif + 12 tests dont neutralisation XSS (`07142c7`).
- `CHANTIER_CLOS.md` + `rapport-final-chantier.md` produits.

### Pushed
- Tag `v4.2.2` (commit `0950a4f`) poussé 2026-05-13.

## [4.2.1] — 2026-04-20

### Added
- Documentation knowledge-driven synchronisee dans `README.md`, `AGENTS.md`, `CLAUDE.md` et `GEMINI.md`
- Cas client complet `clients/depanneur-nobert/site/` avec routes FR/EN, pages legales Loi 25, APIs `contact` et `newsletter`, `robots.txt` et `sitemap.xml`

### Fixed
- `clients/depanneur-nobert/site` : scaffold incomplet corrige pour permettre `next build`
- `clients/depanneur-nobert/site` : dependances Next.js / next-intl / vitest mises a jour pour ramener `npm audit` a `0 vulnerabilites`

### Internal
- Chantier knowledge base A->N rapproche d'un etat clos avec evidence build, audit et livrables finaux de phase
- Le cas `depanneur-nobert` confirme l'usage de `pattern-recommender` et la differenciation 6D sur un create end-to-end

## [4.2.0] — 2026-04-15

### Fixed (Pilier 1 — Déblocages critiques)
- **A · Symlink soic/** : pointait vers `/home/jarvis/...` inexistant → réparé en `../soic_v3`. Tests d'import ajoutés.
- **B · nexos_cli.py exec()** : remplacé par `import orchestrator` + `runpy.run_path` fallback. Audit défensif des 9 `subprocess.*` du package `nexos/`.
- **C · Deps manquantes** : FastAPI/Pydantic/uvicorn déclarées en `[api]` extra. Lockfile généré. Extras `wizard`, `dev`, `api`, `all`.

### Changed (Pilier 2 — Hygiène)
- **D · Archivage** (hors-git, NEXOS_PLATFORM/ n'est pas versionné) : `nexos_dashboard_v0/v1/v2/`, 3 `.jsx` orphelins, `deploy/` (VPS mort), `run_audit.py`, `reports/`, `.reports/` → `NEXOS_PLATFORM/archive/` avec README. Racine passée de 22 → 13 entrées (≤ 13 requis). Voir `mise_a_niveau/phase-D-report.md`.
- **E · Chemins paramétrés** : plus aucun `/home/jarvis/` dans le code actif. Nouveau module `nexos/config.py` avec `Settings` immutable basé sur variables d'env. `.env.example` refait, portable.

### Added (Pilier 3 — Qualité)
- **F · Logging structuré** : 220 `print()` migrés vers `logging` stdlib. Nouveau `nexos/logging_config.py` avec `get_logger` + `bind_context`. Level pilotable via `NEXOS_LOG_LEVEL`.
- **G · Lint** : `ruff` + `ruff format` + `pre-commit` configurés. Hooks : trailing-whitespace, eof-fixer, check-yaml/json, no-commit-to-branch, ruff, forbid-usinerh.
- **H · Type-checking** : `mypy` config + `py.typed` marker. Couverture type hints 100 % sur `nexos/`. `brief_wizard.py` typé.
- **I · Tests** : `conftest.py` centralisé. Coverage 55 % → 73 %. Nouveau test E2E orchestrator (`nexos create --dry-run`). Markers `e2e` + `integration`. Pre-push hook pytest-fast.

### Added (Pilier 4 — Reprod/Deploy)
- **J · Dockerfile** multi-stage (builder + runtime), user non-root, image < 800 MB, labels OCI. `.dockerignore` + build wrapper.
- **K · docker-compose** : services `nexos` / `gateway` / `soic-eval` avec profiles default/cli/api/dev/soic. Override dev avec hot reload uvicorn.
- **L · install_nexos.sh robuste** : preflight checks (Python 3.10+, Node 20+, git), flags `--dev` / `--no-venv` / `--no-precommit`, venv auto, pre-commit install. Nouveau `uninstall_nexos.sh`.

### Added (Pilier 5 — CI/CD + Doc)
- **M · GitHub Actions** : 4 workflows (test + lint + security + docker) avec matrix Python 3.10-3.12, coverage fail_under 70, pip-audit, bandit, image size guard.
- **N · Documentation** : README racine `NEXOS_PLATFORM/`, 6 ADR (multi-phase, multi-CLI, auto-fix, knowledge, refactor, logging), `adding-agents.md`, `runbook.md`, `env.md`.

### Refactored (Pilier 6 — Architecture)
- **O · Orchestrator P1** : 3 classes extraites (`PipelineOrchestrator`, `GateEngine`, `ConvergeLoop`). Dataclasses `GateResult`, `PhaseRun`, `PipelineContext`. Enum `PhaseStatus`.
- **P · Orchestrator P2** : éclaté en package `orchestrator/` (main, pipeline, gates, converge, phases, cli_args). `orchestrator.py` devient un shim ≤ 80 L. À iso-comportement.

### Internal
- Chantier géré en 17 phases isolées (A → Q), dossier `maintenance + upgrade/mise_a_niveau/`.
- 16 commits `chantier2-*` dans `nexos_v.3.0/` + D hors-git (archive/ à la racine NEXOS_PLATFORM non versionnée).
- Chaque phase = 1 commit rollbackable indépendamment.
- Filet de sécurité : test E2E orchestrator (phase I) + CI (phase M) actifs avant le refactor (phases O + P).

### Metrics gagnées
- `nexos doctor` : tous les outils critiques OK
- Coverage tests : 55 % → 73 %
- Type hint coverage : 25 % → 100 % (sur `nexos/`)
- `print()` dans `nexos/` : 220 → ≤ 15 (tolérés, UX/contrat)
- Lignes `orchestrator.py` : 1710 → ≤ 80 (shim) + ~1100 L répartis dans le package
- Versions fichiers : `pyproject.toml` avec lockfile, versions bornées
- Docker image : fonctionnelle, < 800 MB
- 0 `/home/jarvis/` dans code actif
- Triple verrou UsineRH (settings.json + CLAUDE.md + pre-commit hook)

### Compatibility
- `from orchestrator import main` continue de fonctionner (shim)
- Anciens CLI args préservés
- JSON outputs (soic-gates, pattern-recommendation, etc.) inchangés
- Fichiers clients existants compatibles

---

## [4.0.0] - 2026-02-28 — Pipeline Augmentation (Sprint 1 + 2)

### Nouveau package `nexos/`

Trois modules d'augmentation qui se branchent sur `orchestrator.py` via le flag `_NEXOS_V4`.
Retrocompatibilite totale : si `nexos/` est absent, l'orchestrateur fonctionne en mode v3.0.

#### Sprint 1 — Modules de base
- **A01** : `nexos/tooling_manager.py` — Verification des outils CLI (node, npm, claude, lighthouse, pa11y) avec degradation gracieuse pour les optionnels
- **A02** : `nexos/build_validator.py` — Remplace la validation superficielle "BUILD PASS" par des verifications reelles (npm install, tsc, build, audit, fichiers critiques, headers)
- **A03** : `nexos/auto_fixer.py` — Auto-correction D4/D8 : injection cookie consent, npm audit fix, vercel headers, next.config, generation pages legales

#### Sprint 2 — Commandes CLI
- **A04** : `nexos/cli_commands.py` — Nouvelles commandes standalone
- **CMD** : `nexos doctor` — Diagnostic systeme complet (outils, templates, SOIC engine, clients)
- **CMD** : `nexos fix <client_dir> [--dry-run]` — Auto-correction D4/D8 sans lancer le pipeline
- **CMD** : `nexos report <client_dir>` — Rapport agrege (phases, SOIC gates, tooling, brief)

### Fichiers modifies
- `orchestrator.py` — Imports v4.0 conditionnels, tooling check au demarrage, auto-fix avant ph5, validation build reelle a ph4, 3 nouvelles commandes CLI (doctor/fix/report)
- `nexos/tooling_manager.py:doctor_report()` — Enrichi avec sections templates, SOIC engine, clients

### Fichiers crees
- `nexos/__init__.py` — Package v4.0.0
- `nexos/tooling_manager.py` — 230 lignes
- `nexos/build_validator.py` — 238 lignes
- `nexos/auto_fixer.py` — 478 lignes
- `nexos/cli_commands.py` — 260 lignes
- `pyproject.toml` — Config projet Python (rich>=13.0, pytest>=8.0)

### Tests
- `tests/test_tooling_manager.py` — 16 tests (check_tool, ensure_tooling, doctor_report)
- `tests/test_build_validator.py` — 13 tests (BuildResult, fichiers critiques, headers, audit)
- `tests/test_auto_fixer.py` — 17 tests (FixReport, vercel headers, next.config, cookie consent, pages legales)
- `tests/test_cli_commands.py` — 11 tests (doctor, fix, fix --dry-run, report)
- **Total : 57 tests, tous passent**

---

## [3.0.1] - 2026-02-16 — Stabilisation Loi 25

### Corrections de bugs
- **B05** : `orchestrator.py` — `process = None` initialise avant try/except pour eviter NameError
- **B08** : `orchestrator.py` — `import re` et `import unicodedata` deplaces en haut du fichier
- **B08b** : `soic/gate.py` — `import re` deplace en haut du fichier
- **B08-unicode** : `slugify()` reecrit avec `unicodedata.normalize(NFD)` pour support complet des accents

### Nouvelles fonctionnalites
- **A05** : `orchestrator.py` — `verify_phase_output()` verifie que chaque phase produit un rapport valide (>500 chars)
- **D8-eval** : `soic/evaluate.py` — `evaluate_d8_legal()` evalue programmatiquement la conformite legale (6 points)
- **D8-fix** : D8 n'est plus fixe a 5.0 par defaut — score 0.0 si aucun element de conformite trouve

### Templates crees
- `templates/cookie-consent-component.tsx` — Composant React bandeau consentement Loi 25
- `templates/privacy-policy-template.md` — Template politique de confidentialite avec placeholders
- `templates/legal-mentions-template.md` — Template mentions legales avec placeholders

### Fichiers modifies
- `templates/brief-intake.md` — Reecrit avec section Loi 25 complete (RPP, donnees, finalites, retention, transfert, consentement, incidents)
- `templates/brief-schema.json` — Reecrit avec validation Loi 25 (champs required: rpp, data_collected, purposes, etc.)
- `agents/ph5-qa/legal-compliance.md` — Reecrit avec 28 points de verification (A1-E2)
- `agents/ph4-build/_orchestrator.md` — Renforce avec integration templates Loi 25, remplacement placeholders, checklist BUILD PASS elargie
- `CLAUDE.md` — Section conformite legale etendue avec toutes les exigences Loi 25

### Tests
- `tests/briefs/plomberie-qc.json` — Brief test complet avec donnees legales Loi 25
- Validation end-to-end : orchestrator charge le brief, slugify, build_phase_prompt, SOIC gates, D8 evaluation
- `orchestrator.py` compile sans erreur
- `soic/` compile sans erreur

### Documentation
- `STABILISATION_AUDIT.md` — Audit initial des 16 fichiers (incohérences, references cassees, lacunes Loi 25)
- `CHANGELOG.md` — Ce fichier
