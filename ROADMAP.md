# NEXOS — Roadmap prochaines sessions

> Document de continuité entre sessions Claude/Codex/Gemini.
> Mis à jour à chaque clôture de session. À lire en ouverture.

**Dernière mise à jour** : 2026-05-18 — B2 résolu (CVE HIGH next-intl/postcss) + P9 D5 résolu (beaumont μ 8.50 → 9.46) (claude, tungsten)
**Version NEXOS active** : v4.2.0 (production-ready autonome)
**Branche** : `main` — 4 commits B2 pushed (`56c8320`, `46e93fa`, `e51e98e`, `bac4297`) + 1 commit D5 local (`b275094`) ; SOIC `9b9e123` côté `soic_v3`

---

## 📍 État actuel (snapshot 2026-05-16)

### Métriques santé

| Indicateur | Valeur | Note |
|---|---|---|
| Tests Python | **562/562** verts | +29 P8.3 + 21 P8.6 + 18 P9 D8 + 1 P9 D9 + 4 P9 D7 (preflight.sh path) |
| Tests Vitest depanneur-nobert | **70/70** verts | +57 tests P4c (schemas + libs + email + clientConfig) + P5 (API contact + newsletter) |
| Tests Vitest depanneur-nobert | **70/70** verts (était 13/13) | étendu en P4c + P5 |
| Build site depanneur-nobert | **PASS** | npm audit 0/0 |
| Lighthouse depanneur-nobert | a11y 100, perf 92, BP 96, SEO 92 | mesures empiriques |
| Pa11y depanneur-nobert | **0 erreurs** | vs 34 contraste avant fix |
| Clients actifs | 18 total · 8 complets brief+gates+site | cf `nexos doctor` |
| Pipeline NEXOS complet | OK pour `create` · ✅ **`audit` fonctionnel** (P2 résolu) | |
| Divergence agent Ph5 / SOIC | ✅ **résolue (P1)** | SOIC = source de vérité unique via placeholders |
| Silent failure paths | ✅ **3 nettoyés (P2)** | PipelineConfig + AgentRegistry + intake directive |
| Ports hors zone CLAUDE.md | ✅ **résolu (P3)** | `nexos.port_allocator` + `tools/alloc-port.sh` — NEXOS_ENGINE 20100-20199 |
| Osiris API désynchronisée | ✅ **résolu (P7)** | `osiris-scan.sh` adapté à `--url --output report`, scan production OK |
| Bugs réels notés (audit) | 🟡 **P8 ouvert** (1 item restant) | P8.1 + P8.2 + B2 résolus. Reste B4 6 clients dormants |
| CVE HIGH next-intl/postcss | ✅ **résolu (B2) 2026-05-18** | next 15.5.15 → 15.5.18 + next-intl 3.25.1 → 4.12.0 + postcss 8.4.49 → 8.5.10 sur 6 clients (pilote vertex-pmo `56c8320` + batch 4 clients `46e93fa` + collectif-nova on-disk). mark_systems_demo hors scope (déjà next 16.2.3). vertex-pmo μ 9.00 → 9.10 (+0.10). |
| Auto-fixer idempotent | ✅ **résolu (P8.1)** | `FIXER_ORDER: list[Fixer]` + 14 tests régression (ordre + file-ownership + idempotence run 3×) |
| ABORT_PLATEAU recovery | ✅ **résolu (P8.2)** | `Decision.ENRICHED_RETRY` + `PlateauDiagnosis` injecté dans feedback avant abort (1 retry par run) |
| Dimension-scoped fixers | ✅ **résolu (P8.3)** | `Fixer.dimension` + `auto_fix(dimensions=)` + `on_enriched_retry` hook + `orchestrator/plateau_recovery.py` factory — routing déterministe D4/D8 sur plateau |
| Fixer D6 contraste WCAG | ✅ **résolu (P8.6)** | `_fix_pa11y_contrast` — WCAG helpers stdlib + détection background + harden V (HSV) jusqu'à 5.0:1. Validé sur vrai vertex-pmo : 3.75:1 → 5.00:1 |
| Dette technique notée | 🟡 **P9 ouvert** (5 items) · ✅ D5 + D7 + D8 + D9 résolus | D5 (beaumont marge) fermé 2026-05-18 par effet de bord post-B2 (μ 8.50 → 9.46). Reste D1 Vitest matrix, D2 Osiris dimension SOIC, D3 doc symlinks, D4 mypy, D6 schéma strict. |
| Audit Mark Systems public | 🟢 **Session 1 faite 2026-05-17** | Next 15.5.18 ; analytics conditionnel au consentement ; liens privacy localisés ; tests 34/34 ; build PASS ; npm audit HIGH/CRITICAL = 0 |
| Propagation fixes 7 clients | ✅ **résolu (P4b)** | CSP + headers propagés à beaumont/clinique-aura/collectif-nova/electro-maitre/mark_systems_demo/table-de-marguerite/vertex-pmo |
| Hardening tools/*.sh | ✅ **résolu (P4d)** | 5 scans (deps/headers/ssl/lighthouse/a11y) toujours exit 0 + JSON valide |
| CSP middleware dev local | ✅ **résolu (P4a)** | `_fix_csp_middleware` génère middleware.ts aligné prod (single source vercel.json) |
| Vitest étendu | ✅ **résolu (P4c + P5)** | 70/70 (vs 13/13) — schemas Zod, libs, email, clientConfig, API handlers |
| Doctor multi-clients | ✅ **résolu (P4e)** | `nexos doctor --all-clients` rapport tabulaire 16 clients |
| Silent excepts init | ✅ **résolu (P6)** | logging_config.py + verify.py — finit le travail P2 |
| Headers cohérence 8 sites | ✅ **vérifié audit post-P4** | 7 headers identiques (CSP/HSTS/Frame/Content-Type/Referrer/Permissions/DNS-Prefetch) |

### Travail accompli session 2026-05-15

**16 commits sur `nexos_v.3.0/main`** (13 poussés sur origin, 3 locaux) :

```
a59f5a4 docs(cli): codify ROADMAP.md session discipline as mandatory rule   [local]
7413158 docs(roadmap): add ROADMAP.md — continuity doc between sessions      [local]
021e1be fix(tools): preflight pa11y writes to a11y.json with proper config   [local]
973be85 test(e2e): update _fake_doctor signature for --client kwarg
dd0417c test(depanneur-nobert): seed minimal Vitest suite (13 tests / 3 files)
ecadb8b fix(depanneur-nobert): contrast text.muted #8B7355 → #7A6447 (WCAG AA)
0c6f1fa feat(doctor): add --client <slug> for targeted client diagnosis
fe93c69 state(depanneur-nobert): rerun pipeline 2026-05-14 — Ph5 FAIL μ=7.52
71dd5a1 feat(cli): auto-resolve client slug to clients/<slug> in fix/report
48f71c4 docs(session_launcher): document intentional no-timeout in CLI exec
b0dd9d5 fix(auto-fixer): compact JSON writer for vercel.json (item E)
cf455b3 fix(tools): osiris-scan.sh produces valid JSON on retry failure
4f1d04a fix(cli): _dry_run_analysis use auto_fixer path helpers
4910f19 fix(depanneur-nobert): add CSP to vercel.json
96a0cc2 feat(auto-fixer): add _fix_csp() — D4 CSP coverage
```

**1 commit sur `soic_v3/main`** (local, pas de remote) :
```
695b78d feat(domain_grids): integrate audit_toolkit gates via AUDIT_TOOLKIT set
```

### Découvertes structurelles

1. **NEXOS est plus propre qu'attendu** : zéro TODO/FIXME/HACK dans le code, 413 tests, infrastructure solide. La dette réelle est concentrée sur l'**intégrité** (pipeline qui ment/diverge), pas sur la structure.

2. **Pattern utile** : ouvrir chaque session avec `nexos doctor` global + `nexos doctor --client <slug>` ciblé. Donne un checkpoint factuel en 5 secondes.

3. **Règle absolue tenue** : aucun `git push` automatique. L'utilisateur valide explicitement. Le harness Claude Code refuse même les push, ce qui constitue une 2e ligne de défense.

---

## 🎯 Items dette ouverts (priorisés)

### ✅ P1 — Item N : Divergence agent Ph5 vs SOIC (RÉSOLU 2026-05-15)

**Statut** : ✅ Résolu — SOIC = source de vérité unique pour μ Ph5

**Cause racine identifiée** : l'agent Ph5 LLM calculait son propre μ subjectif via une grille D1-D9 documentée dans `agents/ph5-qa/_orchestrator.md`, alors que SOIC `GateEngine` calculait le sien via 17 gates déterministes (`soic/domain_grids/web.py`) sur les mêmes dimensions mais avec règles différentes. Les deux scores finissaient dans le même `ph5-qa-report.md` :
- Corps du rapport : score agent (ex: 8.39 / 7.52)
- Section "Reconciliation Ph4 ↔ Ph5" bas du rapport : score SOIC (ex: 9.11 / 8.78)

`deploy-master` et `Converger.decide()` se basent sur le score SOIC depuis `soic-gates.json` — c'était déjà de facto la source de vérité du pipeline, mais l'agent l'ignorait.

**Décision documentée** (cf `CLAUDE.md` section "Source de vérité Ph5") :
- **SOIC = source de vérité unique** pour μ et verdict ACCEPT/FAIL
- L'agent Ph5 rédige le rapport **qualitatif** uniquement
- Substitution des placeholders en post-traitement Python

**Implémentation** (Option C — placeholders + injection post-SOIC) :
- `orchestrator/score_injection.py` : module qui substitue `[[SOIC_MU]]`, `[[SOIC_VERDICT]]`, `[[SOIC_THRESHOLD]]`, `[[SOIC_DIM_SCORES_TABLE]]`, `[[SOIC_D1]]`..`[[SOIC_D9]]` avec les valeurs lues depuis `soic-gates.json` + `soic-runs.jsonl`
- Branché dans `orchestrator/phases.py:run_pipeline()` après `save_gate_history()` et avant `run_reconciliation_step()`
- `agents/ph5-qa/_orchestrator.md` : nouvelle section "Scoring — SOIC = source de vérité unique" qui interdit à l'agent de calculer son propre μ
- Tests régression : `tests/test_score_injection.py` (10 tests, dont `test_report_mu_matches_gates_mu_exactly` qui ancre le cas concret depanneur-nobert 9.10925 → "9.11")
- Idempotent : rapports existants sans placeholders (ex: depanneur-nobert 2026-05-15) ne sont pas modifiés

**Validation** :
- 423/423 tests Python verts (413 baseline + 10 nouveaux)
- ruff check + format : all clean

**Commits** : à venir dans cette session (3 commits atomiques prévus — feat module + integration + docs roadmap)

**Rapports antérieurs (depanneur-nobert)** : le rapport actuel `clients/depanneur-nobert/ph5-qa-report.md` reste tel quel (codé en dur 8.39 / 9.11). Il sera régénéré au prochain run Ph5 avec les placeholders et n'aura plus de divergence. Pas de migration rétroactive nécessaire.

**Effort réel** : 2h30 (investigation 45 min + module + tests 60 min + integration + docs 45 min)

---

### ✅ P2 — Crash `nexos audit` exit 1 silencieux (RÉSOLU 2026-05-15 par effet de bord)

**Statut** : ✅ Résolu — bug ROADMAP non reproductible aujourd'hui + 3 silent failure paths nettoyés défensivement

**Test reproduction** (2026-05-15) :
```bash
$ timeout 90 python3 -u nexos_cli.py audit --client-dir clients/depanneur-nobert --url http://localhost:20003
# Pipeline tourne propre : auto-fix OK → preflight 6/6 scans OK → "Using claude CLI" → timeout 90s (subprocess en attente)
# EXIT=124 (timeout du test, pas du pipeline). Aucun "exit 1 silencieux".
```

Le subprocess claude a un timeout interne de 30 min (`_CODEX_CLI_TIMEOUT = 1800` dans `cli_runner.py:15`) — design intentionnel documenté par commit `48f71c4` (no-timeout dans session_launcher).

**Cause probable du fix par effet de bord** :
- `cc30880` : Claude CLI uses -p mode + unsets ANTHROPIC_API_KEY for OAuth → résout "Invalid API key" qui causait probablement l'exit 1 immédiat
- `f0b861b` : rate limit retry/pivot Claude→Codex (A-004) → couvre cas où claude refuse pour cause de rate limit
- `8daf3d1` : switch default LLM host claude (default avant était codex potentiellement absent)

**Action préventive — 3 bugs latents fixés** (commit `a92adb8`) :

Audit ciblé des patterns "silent failure" sur la chaîne `audit` (auto-fix → preflight → audit_toolkit → build_prompt → cli_runner) a identifié 3 `except Exception: pass` sans log :

1. `orchestrator/phases.py:66` — fallback silencieux `PipelineConfig.from_brief` → `PHASES_MAP`
2. `orchestrator/prompts.py:257` — fallback silencieux AgentRegistry → prompt sans liste d'agents
3. `orchestrator/prompts.py:316` — fallback silencieux intake directive → prompt sans cadrage métier

Chaque except logge maintenant un warning `say([yellow]⚠ ... — fallback ...)` avec type + message exception. Aucun changement de comportement, juste visibility.

**Validation** : 423/423 tests Python verts, ruff check + format clean, pre-commit hooks tous passés.

**Files touched** : `orchestrator/phases.py`, `orchestrator/prompts.py`

**Si le bug réapparaît** : les nouveaux warnings yellow rendront maintenant visible la cause exacte du fallback silencieux. Re-ouvrir P2 si nécessaire.

**Effort réel** : 45 min (audit grep + classification + 3 edits + tests + commit)

---

### ✅ P3 — Zone ports interdite (RÉSOLU 2026-05-15)

**Statut** : ✅ Résolu — `nexos.port_allocator` + `tools/alloc-port.sh` actifs ; preflight pioche dans NEXOS_ENGINE (20100-20199)

**Cause racine** : `orchestrator/preflight.py::_find_free_port` faisait `socket.bind(("", 0))` ce qui laisse le kernel piocher dans la zone éphémère (`/proc/sys/net/ipv4/ip_local_port_range` = 32768-60999) — explicitement interdite par `~/.claude/CLAUDE.md` user. Symptôme observé : Next.js démarré sur port 55191.

**Implémentation** (Option B — helper Python + wrapper bash, validé en début de session) :
- `nexos/port_allocator.py` (146 lignes) : 12 sous-blocs nommés constants (NEXOS_TESTS, NEXOS_ENGINE, NEXOS_SCRAPING, NEXOS_CYBERSEC, NEXOS_BUFFER, GENESIS_*, GENCORE, SAAS, CYBERSEC_LABS, AUDIT_TOOLKIT, GLOBAL_BUFFER), garde-fou `FORBIDDEN_RANGES` validé au load, `allocate_port()` séquentiel premier libre, `purge_subblock()` explicite SIGTERM (jamais déclenchée par allocate), `is_port_free()` via `socket.bind`. Stdlib pure, pas de deps.
- `tools/alloc-port.sh` (160 lignes) : wrapper bash, sortie JSON parsable, `--list`, `--purge`, `--help`, exit codes 0-4 (success / invalid args / unknown subblock / saturated / forbidden zone). Inputs via env vars (safe contre shell injection).
- `orchestrator/preflight.py::_find_free_port` : délègue à `allocate_port(NEXOS_ENGINE)`. Si saturé → `say([red])` + skip preflight gracieux + hint vers `--purge`.
- Tests régression : `tests/test_port_allocator.py` (21 tests dont `test_no_subblock_overlaps_forbidden_zones` garde-fou constantes, `test_preflight_find_free_port_uses_nexos_engine` ancre le contrat P3).
- Documentation : nouvelle section "Allocation des ports" dans `docs/runbook.md` (usage Python + CLI + incidents + diagnostic).

**Validation** :
- 444/444 tests Python verts (423 baseline + 20 nouveaux port_allocator + 1 régression preflight)
- ruff check + format : clean
- Smoke-tests CLI : `--help`, `--list`, `NEXOS_ENGINE` → 20100, `NEXOS_BUFFER` → 20900, sous-bloc inconnu → exit 2 JSON

**Décisions clés** (cf début de session) :
- Pas de purge automatique (règle CLAUDE.md user) — `--purge` reste 100% explicite
- Sous-bloc saturé = erreur claire, jamais de retombée vers zone éphémère
- Validation `FORBIDDEN_RANGES` au load du module = garde-fou si une constante dérive un jour

**Commits** : à venir dans cette session (4 commits atomiques prévus — feat port_allocator + tests, feat alloc-port.sh, fix preflight + test régression, docs roadmap/runbook/journal)

**Effort réel** : ~1h30 (design API + module Python + tests + wrapper bash + patch preflight + docs)

---

### ✅ P4 — Polish (RÉSOLU 2026-05-15 — tous sous-items a, b, c, d, e)

**Statut** : ✅ Résolu en mode autonome session continue. Tous les 5 sous-items P4 fermés + 2 nouveaux items P5/P6 identifiés et résolus dans la foulée.

#### ✅ P4b (résolu) — Propagation fixes aux 7 clients candidats
7 commits atomiques (beaumont-avocats, clinique-aura, collectif-nova, electro-maitre-industriel, mark_systems_demo, table-de-marguerite, vertex-pmo). Chaque `nexos fix` a appliqué la CSP via `_fix_csp` (D4 coverage). mark_systems_demo a aussi reçu X-DNS-Prefetch-Control + refresh package-lock.json. Aucun BUILD FAIL. HIGH npm audit restant = next-intl/postcss CVE breaking-change, laissé tel quel.

#### ✅ P4d (résolu) — Hardening tools/*.sh
5 scans hardenés selon pattern osiris-scan.sh : `set -uo pipefail`, toujours exit 0 + JSON valide (même en erreur), stderr capturé via tempfile et inclus dans JSON erreur (diagnostic préservé), timeout explicite via `timeout` cmd avec env var override (`DEPS_TIMEOUT_S`, `HEADERS_TIMEOUT_S`, etc.), erreurs encodées via `python3 -c` pour échappement correct (guillemets/accents/newlines). Test régression `test_headers_scan_unreachable_url_emits_error_json` mis à jour (exit 0 + JSON erreur). 5 scripts touchés : deps, headers, ssl, lighthouse, a11y.

#### ✅ P4a (résolu) — Middleware CSP pour aligner dev sur prod
Nouveau `_fix_csp_middleware(site_dir, report)` dans `nexos/auto_fixer.py`. Crée `middleware.ts` Next.js qui sert la CSP en LOCAL uniquement (next dev/start) via check `process.env.VERCEL !== '1'`. Single source of truth = vercel.json (CSP lue via `_read_csp_from_vercel`). Skip si middleware.ts existe (respect décision builder), skip si src/middleware.ts existe (convention alternative), skip si vercel.json sans CSP. Échappement TS literal via `json.dumps`. 11 tests régression dans `TestReadCspFromVercel` + `TestFixCspMiddleware`.

#### ✅ P4c (résolu) — Vitest étendu
57 nouveaux tests Vitest sur depanneur-nobert (passe de 13/13 à 70/70) :
- `schemas.test.ts` (22 tests) — Zod Contact + Newsletter (email, consent Loi 25, honeypot, phone regex anti-injection, locale enum)
- `promotions.test.ts` (7 tests) — `vi.useFakeTimers` pour filtrage actif, tri validUntil ascendant, top limit, getLastUpdate format
- `email.test.ts` (4 tests) — sendEmail avec/sans RESEND_API_KEY, mock fetch, replyTo optionnel
- `clientConfig.test.ts` (7 tests) — placeholders Ph3, env override, getTelHref nettoyage
- `produits.test.ts` (3 tests) — catégories canoniques + filtrage
- `horaires.test.ts` (2 tests) — structure HoraireJour
- `api-contact.test.ts` (6 tests) — handler POST integration (cf P5)
- `api-newsletter.test.ts` (6 tests) — handler POST integration (cf P5)

Config vitest.config.ts étendue avec alias `@/*` pour matcher tsconfig.json.

#### ✅ P4e (résolu) — `nexos doctor --all-clients`
Nouveau flag `--all-clients` qui produit un rapport tabulaire de tous les clients (one row par client) avec colonnes : Brief, Site, Gates count, Ph5 μ, Deploy verdict (READY / BELOW (μ<8.5) / ACCEPT / REJECT / ABORT_PLATEAU). Footer "Déployables (Ph5 μ ≥ 8.5 + ACCEPT) : X/Y". Skip les dossiers `_*` (archives) et `.*` (cache). Snapshot 2026-05-15 : 2/16 déployables (beaumont-avocats μ=8.50, depanneur-nobert μ=9.11). 10 tests dans `TestDoctorAllClients`.

**Effort réel P4 total** : ~3h30 en mode autonome (vs estimé 4-5h batch séquentiel).

---

### ✅ P5 — API integration tests (RÉSOLU 2026-05-15)

**Statut** : ✅ Identifié à l'audit post-P4 + résolu dans la foulée

12 tests intégration sur handlers POST `/api/contact` + `/api/newsletter` :
- Payload valide → 200 ok:true
- Body non-JSON → 400 invalid_json
- Zod invalide → 400 validation + issues
- Honeypot rempli → Zod max(0) fail → 400
- Rate limit : seuil dépassé → 429
- Avec RESEND_API_KEY → body Resend conforme (reply_to, subject, mention Loi 25, locale propagée)

**Pourquoi P5** : ces handlers manipulent PII + consent Loi 25, doivent être verrouillés contre régressions. Mock `Request` minimal (handlers utilisent uniquement headers + .json()) + mock fetch global + cleanup RESEND_API_KEY entre tests + IPs distinctes par test pour éviter pollution LRU rate limiter.

---

### ✅ P6 — Log silent excepts initialization (RÉSOLU 2026-05-15)

**Statut** : ✅ Finit le travail P2 (3 silent paths nettoyés → 5 maintenant)

2 silent excepts restants identifiés à l'audit post-P4 :
- `nexos/logging_config.py:71` (get_logger bootstrap) — settings.log_level invalide ou import circulaire → fallback INFO silencieux. Maintenant : `sys.stderr.write` direct (logger pas encore configuré, donc pas `logging.warning`).
- `orchestrator/verify.py:55` (parse brief-client.json) — JSON corrompu ou schéma invalide → brief=None silencieux. Maintenant : `say([yellow] ⚠ ...)` avec type + message.

Comportement inchangé sinon. Plus de fallback aveugle.

---

### ✅ P7 — Fix osiris-scan.sh API désynchronisée (RÉSOLU 2026-05-15)

**Statut** : ✅ Résolu — Osiris remarche en pipeline, score réel mesuré

**Cause racine** : L'API du scanner Osiris a changé sans que `tools/osiris-scan.sh` soit mis à jour. Tous les `osiris.json` clients étaient des JSON erreur "No such option: --format" depuis un certain temps. Le hardening P4d (P3 session) sauvait la pipeline du crash mais NEXOS tournait à l'aveugle sur l'axe sobriété/sécurité externe.

**Diff API** :
- Ancienne : `scanner.py <URL> --format json` (URL positional + flag JSON)
- Nouvelle : `scanner.py --url <URL> --output report --mode fast` → écrit `reports/<domain>_<date>.json` (relatif CWD)

**Fix** : refactor `tools/osiris-scan.sh` (commit `209fd2e`) :
- URL via `--url` (kwarg)
- Scanner exécuté depuis WORK_DIR temporaire (`mktemp -d`)
- Capture du JSON généré dans `WORK_DIR/reports/`
- Cleanup via `trap EXIT`
- Pattern P4d conservé : exit 0 + JSON valide + retry + budget
- Nouvelle env var : `OSIRIS_MODE` (fast|deep)

**Validation prod** : scan depanneur-nobert remarche, score 4.0/10 "Critique" sur 5 axes (S/R/V/A/E). 6/6 tests `test_osiris_scan.py` verts (2 fake scanners mis à jour pour matcher nouvelle API).

**Découverte intéressante** : SOIC μ=9.11 (READY) ↔ Osiris 4.0/10 (Critique) — les deux moteurs mesurent des choses différentes. Cf D2 dans P9.

---

### ✅ Quick wins D3 + D4 + D6 + B1 + D5 (RÉSOLUS 2026-05-15 session continue)

**Commits locaux non poussés** :
- `0778398` chore: D3 + D4 + D6 + B1 Osiris deps externes — symlinks doc fixés, mypy via venv, brief-synthesizer sector/tags/notes, Osiris venv + symlinks ressources (axes Intrusion + Légalité activés, 8/8 axes mesurés au lieu de 6/8)
- `653a7ce` chore(gitignore): ignore Osiris runtime artifacts
- `9471e18` state(depanneur-nobert): sync runtime snapshot
- `5e05951` ci(hardening): Vitest job matrix client sites
- D5 : `_fix_readme(site_dir, brief, report)` ajouté dans `nexos/auto_fixer.py` + propagation 3 clients (beaumont/collectif-nova/vertex-pmo). Mesure beaumont : μ 6.82 → 7.32 (+0.50).

468/468 tests Python verts, 70/70 Vitest depanneur-nobert.

---

### 🔄 P8/P9 — REPLAN POST-CODEX CONSULT (2026-05-15)

**Codex consult session `019e2baf`** (challenge mode) a invalidé 2 hypothèses Claude :

#### Q1 Refactor `auto_fixer.py` Protocol+toposort → **REJETÉ**
Codex : "your proposed Protocol + applies + topo sort is architectural ceremony for a file that still has only one real execution path. The current problem is not lack of plugin architecture; it is hidden coupling and weak observability."

**Vrai problème** : `_fix_vercel_headers` + `_fix_csp` + `_fix_csp_middleware` touchent vercel.json. Aucun test d'idempotence ne vérifie qu'on peut re-run `auto_fix()` N fois sans corruption.

**Approche revisée** (1-2h vs 4-6h Protocol) :
```python
FIXER_ORDER: list[tuple[str, Callable]] = [
    ("cookie_consent", _fix_cookie_consent),
    ("npm_audit", _fix_npm_audit),
    ("vercel_headers", _fix_vercel_headers),
    ("csp", _fix_csp),
    ("csp_middleware", _fix_csp_middleware),  # requires csp
    ("next_config", _fix_next_config),
    ("privacy_page", _fix_privacy_page),
    ("legal_page", _fix_legal_page),
    ("readme", _fix_readme),
]
```
+ tests d'idempotence (run 3x = même résultat) + tests file-ownership (qui touche quoi).

#### Q2 ABORT_PLATEAU recovery → **REJETÉ stratégie C mix**
Codex : "switching models is a weak hypothesis until you know why plateau happens. If the SOIC failure is caused by missing structured inputs, bad validator incentives, impossible thresholds, or phase prompts that do not expose exact failing assertions, another model will likely produce different-looking failure with the same score."

**4e option ratée par Claude — dimension-scoped remediation** : si D8 (Loi 25) échoue, router vers legal fixer. Si D4 (sécurité), vers security fixer. **Pas re-run la phase entière**.

**Approche revisée** (6-9h structurée) :
1. **Instrumentation plateau** (2-4h) : log plateau cause par dimension, failed assertions, phase, output diff
2. **Enriched retry seule** (3-5h) : injecter SOIC findings dans le prompt next phase
3. **Dimension-scoped fixers** : extension auto_fixer pour les dimensions échouant régulièrement
4. **Switch model = mesuré fallback** après 10-20 plateau samples observés

#### Plan révisé pour prochaine session

| # | Item | Avant Codex | Après Codex | Effort | Statut |
|---|---|---|---|---|---|
| **P8.1** | Refactor `auto_fixer.py` | Protocol toposort | FIXER_ORDER tuple + idempotency tests | 1-2h | ✅ résolu 2026-05-15 |
| **P8.2** | B3 ABORT_PLATEAU | Stratégie C mix | Instrumentation cause + 1 enriched retry | 2-4h | ✅ résolu 2026-05-15 |
| **P8.3** | Dimension-scoped fixers | (manquait) | Nouveau : si D8 fail → legal, D4 → security | 3-5h | ✅ résolu 2026-05-16 |
| **P8.4** | B4 onboard 6 dormants | Aveugle | Couvert par instrumentation P8.2 (on saura pourquoi) | 1-3h (downstream P8.2) | — |
| **P8.5** | Mesure terrain plateau routing | (nouveau) | Relancer vertex-pmo, mesurer si P8.3+P8.6 débloquent | 30 min → 2h | ✅ résolu 2026-05-17 (vertex-pmo READY μ=9.00 ; 3 bugs latents découverts en chaîne + fixés : D8, D9, P8.6.2 follow-up noté) |
| **P8.6** | Fixer D6 contraste WCAG | (découvert P8.5) | `_fix_pa11y_contrast` — WCAG helpers + harden V tokens muted | 2-3h | ✅ résolu 2026-05-17 |
| **D1** | Vitest matrix 7 clients | Inchangé | Mécanique, OK tel quel | 2h | — |
| **B2** | CVE HIGH upgrade | Inchangé | Pilote vertex-pmo + batch 5 clients | 1-2h | ✅ résolu 2026-05-18 (pilote `56c8320` + batch `46e93fa`) |
| **D2** | Osiris dimension D10 SOIC | Inchangé | Pondération SOIC + Osiris | 2-3h | — |

**Économie nette estimée** : ~5h de scaffolding évitées, redirigées vers valeur observable (instrumentation + idempotency).

---

### ✅ P8.1 — Refactor `auto_fixer.py` FIXER_ORDER + idempotence (RÉSOLU 2026-05-15)

**Statut** : ✅ Résolu — pipeline explicite + 14 tests régression

**Cause racine** : `auto_fix()` enchaînait 9 appels `_fix_*` codés en dur sans (a) source de vérité unique sur l'ordre/dépendances entre fixers, (b) tests d'idempotence garantissant qu'un re-run ne corrompe pas vercel.json / layout.tsx / middleware.ts. Trois fixers touchent `vercel.json` (`vercel_headers`, `csp`, et `csp_middleware` en lecture) sans contrat explicite sur l'ordre.

**Décision** (suite challenge Codex `019e2baf`) : pas de Protocol+toposort architectural — `FIXER_ORDER: list[Fixer]` linéaire suffit. Le vrai gap est l'observabilité et les invariants idempotence, pas la pluggabilité.

**Implémentation** :
- `nexos/auto_fixer.py` :
  - `Fixer` dataclass `frozen=True` (`name`, `target`, `apply: Callable[[Path, dict, FixReport], None]`)
  - `FIXER_ORDER` : 9 fixers ordonnés, dépendances commentées (csp après vercel_headers, csp_middleware après csp)
  - `auto_fix()` simplifié → `for fixer in FIXER_ORDER: fixer.apply(...)`
  - Adapters lambda uniformisent les signatures sans toucher les `_fix_*` sous-jacents (résolution de nom Python tardive → monkeypatching préservé)
- `tests/test_auto_fixer.py` :
  - `TestFixerOrder` (7 tests) — noms stables, frozen immutability, csp après vercel_headers, csp_middleware après csp, file-ownership `vercel.json`, `auto_fix` itère bien dans l'ordre déclaré
  - `TestIdempotence` (7 tests, `_fix_npm_audit` mocké) — run 3× : `total_fixes==0` à partir du 2e, fichiers bit-identiques run 1↔3, headers vercel.json sans doublon, CSP exactement 1×, `<CookieConsent />` injecté 1×, `poweredByHeader: false` 1×, CSP middleware/vercel cohérents

**Validation** : 482/482 tests Python verts (468 baseline + 14 nouveaux), ruff check + format clean.

**Effort réel** : ~45 min (refactor 15 min + tests 25 min + ruff fixes 5 min).

---

### ✅ P8.6 — Fixer D6 contraste WCAG (`_fix_pa11y_contrast`) — RÉSOLU 2026-05-17

**Statut** : ✅ Résolu — premier vrai fixer dimension D6 (Accessibilité). Ferme le gap découvert pendant la mesure terrain P8.5 sur vertex-pmo.

**Cause racine** : Pa11y a remonté 18 erreurs WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail sur vertex-pmo, toutes du même type (contraste insuffisant), toutes pointant vers `text-ink-muted`. Cause unique : token `ink.muted: '#64748B'` sur background `surface.DEFAULT: '#0F172A'` = 3.75:1 (sous le seuil WCAG AA 4.5:1). Pattern identique à l'incident historique depanneur-nobert (`text.muted` #8B7355 → #7A6447, 34 → 0 erreurs en mai 2026).

**Décision** :
- **Scope conservateur** : ne toucher QUE les tokens dont le nom matche `muted`, `subtle`, `tertiary`, `disabled`, `placeholder`. Pas de risque de toucher `primary`, `accent`, `brand`.
- **Pas de support CSS variables** (`globals.css --color-*`) dans ce commit — reporté à P8.6.2 si besoin terrain. Tous les clients NEXOS actuels utilisent le pattern Tailwind nested palette.
- **Buffer cible 5.0:1** (au-dessus du 4.5:1 minimum WCAG AA) — laisse une marge pour les ajustements design futurs sans retomber sous le seuil.
- **Préservation HSV** : on déplace V uniquement, hue + saturation intacts → l'intention "muted" visuelle est conservée (vs un blanchiment naïf qui détruirait la hiérarchie).

**Implémentation** (1 commit atomique `43def6d`) :
- `nexos/auto_fixer.py` :
  - 6 helpers WCAG stdlib (pas de deps) : `_hex_to_rgb`, `_rgb_to_hex`, `_relative_luminance` (WCAG 2.1), `_contrast_ratio`, `_rgb_to_hsv` / `_hsv_to_rgb` (colorsys), `_harden_token_contrast`
  - Algorithme `_harden_token_contrast` : détecte direction (lighten/darken selon luminance bg), boucle 50× pas de 0.02 sur V jusqu'à atteindre 5.0:1 ou bailout (palette structurellement hostile, ex: noir sur noir)
  - `_TAILWIND_TOKEN_LINE_RE` regex line-by-line pour patch en place (préserve commentaires, indentation, autres tokens)
  - `_extract_palette_token_lines` groupe les indices par nom de token
  - `_fix_pa11y_contrast` : skip défensifs (config absent / no muted / no bg / already compliant) puis patch in-place + report.contrast_tokens_fixed
- Ajouté à `FIXER_ORDER` en fin (aucune dépendance), `dimension="D6"`
- `FixReport.contrast_tokens_fixed: int` + log changelog `target=tailwind.config.ts` + `tokens_fixed=N`

**Validation terrain** (run dry-run sur vrai vertex-pmo, sans modifier le client) :
- Avant : `ink.muted #64748B` / `surface #0F172A` = **3.75:1** ❌
- Après : `ink.muted #7689a4` / `surface #0F172A` = **5.00:1** ✅ (buffer cible atteint exactement)

**Tests régression** (21 nouveaux, 539/539 verts) :
- `TestWcagContrastHelpers` (10) : hex parsing (3 + 6 digits, malformed), luminance extremes (black=0, white=1), contraste black-on-white=21:1, symétrie, ancrage cas vertex-pmo (#64748B sur #0F172A < 4.5), harden no-op si déjà conforme, harden lighten sur bg sombre, harden darken sur bg clair
- `TestFixPa11yContrast` (10) : skip défensifs (config absent / no muted token / no background / already compliant), fix dark theme (anchor vertex-pmo), fix light theme (anchor depanneur-nobert historique), idempotence run 2× bit-identique, préservation primary/accent/surface intacts, multi-muted tokens (count = 2), routing P8.3 dimensions={"D6"}
- 3 tests mis à jour pour refléter le nouveau fixer : `test_fixer_names_are_unique_and_stable`, `test_fixer_dimensions_are_stable_mapping`, `test_logs_coverage_gap_when_no_fixer_matches` (D6 maintenant couvert → gaps connus = D1/D3/D5/D7/D9)

**Routing déterministe activé** : grâce à P8.3, dès qu'un futur plateau remontera `failing_dimensions=("D6",)`, le hook `make_plateau_auto_fix_hook` appellera automatiquement `auto_fix(dimensions={"D6"})` qui invoquera `_fix_pa11y_contrast`. Aucun wiring supplémentaire requis.

**Limites assumées (transparence)** :
- Couvre uniquement `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail` (contraste texte).
- Ne touche PAS aux 9 autres types d'erreurs WCAG (alt manquants, ARIA, focus visible, etc.).
- Palettes CSS variables (`--color-*` dans globals.css) non couvertes — P8.6.2 follow-up si besoin terrain.

**Mesure terrain à faire (post-merge)** : relancer le pipeline `nexos audit` sur vertex-pmo après push pour confirmer que (a) le fixer s'exécute en condition réelle dans le hook P8.3, (b) le pa11y post-fix descend bien à 0 erreur contraste, (c) μ Ph5 monte au-dessus du seuil 8.5 et débloque ACCEPT.

**Effort réel** : ~2h30 (investigation gates + a11y.json + palette 30 min + 6 helpers + fixer 1h + 21 tests 45 min + fix régressions 15 min + ROADMAP).

---

### ✅ P8.3 — Dimension-scoped fixers : routing déterministe sur plateau (RÉSOLU 2026-05-16)

**Statut** : ✅ Résolu — `PlateauDiagnosis.failing_dimensions` route maintenant vers les fixers NEXOS pertinents avant le rerun LLM, fermant la boucle ouverte par P8.2.

**Cause racine** : P8.2 avait livré l'instrumentation (`PlateauDiagnosis` + `ENRICHED_RETRY`) mais le signal `failing_dimensions` n'était consommé QUE pour enrichir le prompt LLM. Aucun fixer déterministe n'était déclenché. Sur un plateau D4 (sécurité) ou D8 (Loi 25), NEXOS demandait au LLM de corriger des problèmes que ses propres fixers savaient faire en quelques millisecondes.

**Décision** (validée utilisateur 3 carrefours architecturaux) :
- **A1. Champ `dimension: str` sur `Fixer`** (vs sous-package nexos/fixers/ ou dict externe) — `FIXER_ORDER` reste source de vérité unique
- **C1. Hook `on_enriched_retry` dans `PhaseIterator`** (vs étendre signature de RerunCallback) — SOIC reste pur, NEXOS branche son auto-fixer via callback
- **Mécanisme seul, pas de nouveaux fixers spéculatifs** — D1/D3/D5/D6/D7/D9 restent gaps connus à combler en P8.5+ si plateaux terrain les révèlent

**Implémentation** (4 commits atomiques) :

1. **`9830c0d`** — `feat(auto-fixer): add dimension field to Fixer + fixers_for_dimensions() (P8.3)`
   - `Fixer` dataclass frozen gagne `dimension: str` validé contre `_VALID_SOIC_DIMENSIONS = {D1..D9}`
   - Mapping figé : D2 readme | D4 npm_audit, vercel_headers, csp, csp_middleware, next_config | D8 cookie_consent, privacy_page, legal_page
   - `fixers_for_dimensions(dims)` filtre en préservant l'ordre global de `FIXER_ORDER` (invariants P8.1 préservés par construction)
   - 11 tests : chaque Fixer a dimension valide, mapping figé, ordre préservé multi-dim, D4 et D8 (bloquantes) ont ≥ 1 fixer, déterminisme

2. **`527c670`** — `feat(auto-fixer): support dimensions= filter in auto_fix() (P8.3)`
   - `auto_fix(..., dimensions: Iterable[str] | None = None)` — `None` (défaut) = rétrocompat P8.1 (tous fixers)
   - `dimensions=set()` distinct de `None` (filtre explicite = 0 fixer)
   - Changelog `AUTOFIX_START` porte `details={"scope": [...], "fixer_count": N}` quand un sous-ensemble est demandé
   - 7 tests : D4 seul ne touche pas D8 (et vice versa), `dimensions=None` rétrocompat, `set()` no-op, idempotence dim-scoped (run 3× bit-identique), dimensions non couvertes → 0 fix sans crash

3. **`9b9e123`** côté `soic_v3` — `feat(iterator): on_enriched_retry hook for dimension-scoped recovery (P8.3)`
   - Type alias `EnrichedRetryHook = Callable[[PlateauDiagnosis], None]`
   - `PhaseIterator.__init__` accepte `on_enriched_retry: EnrichedRetryHook | None = None`
   - Appelé dans `run()` exactement quand `Decision.ENRICHED_RETRY` fire, AFTER `diagnose_plateau()` et BEFORE `rerun_phase()`
   - SOIC reste pur : aucun import de `nexos.*`, le hook est un callback boundary

   `225a6b6` côté `nexos_v.3.0` — `test(soic): cover on_enriched_retry hook + tighten auto_fix type hints (P8.3)`
   - 5 tests dans `tests/test_soic/test_iterator.py` (`TestEnrichedRetryHookInvocation`) : hook 1 fois sur plateau, optional (None preserve P8.2), pas appelé sur ACCEPT/ITERATE/ABORT_*, appelé avant rerun_phase, même diagnosis que feedback_router
   - Fix annotation mypy `selected: list[Fixer]` + `scope: list[str]` dans `auto_fix()` (régression introduite au commit 2)

4. **`a457b3e`** — `feat(orchestrator): wire dimension-scoped auto_fix on SOIC plateau (P8.3)`
   - **Nouveau module `orchestrator/plateau_recovery.py`** (149 lignes) avec factory `make_plateau_auto_fix_hook(phase, site_dir, client_dir, mode, say, brief_loader)` — captures state via args explicites (pas de closure trap B023)
   - `orchestrator/phases.py` appelle la factory en construisant `PhaseIterator(...)`. Ajout net ~12 lignes côté phases.py grâce à l'extraction
   - Seuil `test_file_sizes_targets phases.py` relâché 620 → 640 avec note explicite P8.3 (cible long terme ≤ 500 via phases-as-classes inchangée)
   - 6 tests `tests/test_plateau_recovery.py` (`TestPlateauHookDefensive` + `TestPlateauHookHappyPath`) : skip si site_dir None, skip si failing_dimensions vide, coverage_gap log + 0 fix pour D5/D6/D9, happy path D4+D8 (auto_fix appelé avec bons args), brief_loader pas appelé si brief absent, log "5 fixer(s)" pour plateau D4

**Validation** :
- 518/518 tests Python verts (489 baseline + 11 + 7 + 5 + 6 = +29 nouveaux)
- ruff check + format + mypy clean
- Modularité préservée : `orchestrator/plateau_recovery.py` = module dédié unit-testable isolé du pipeline complet
- Couplage unidirectionnel maintenu : `soic/` n'importe rien de `nexos/`, l'orchestrator passe le callback construit côté NEXOS

**Branches défensives implémentées** :
- `site_dir is None` → log "pas de site_dir" + return (cas ph0-discovery)
- `diagnosis.failing_dimensions = ()` → log "diagnostic vide" + return
- Aucun fixer pour les dimensions reportées (D1/D3/D5/D6/D7/D9) → log "coverage gap" + changelog event `coverage_gap: true`, pas d'appel `auto_fix`
- Happy path → `auto_fix(dimensions=failing_dimensions)` + changelog `trigger=plateau`

**Mesure terrain à faire (P8.5 candidat)** : relancer `collectif-nova` (μ=8.05) et `vertex-pmo` (μ=7.91) pour vérifier que le routing dim-scoped débloque effectivement leur plateau historique. Si le plateau persiste, instrumenter les `failing_dimensions` réelles pour identifier les fixers manquants (signal direct pour P8.5+).

**Effort réel** : ~3h (design 30 min + 4 commits 2h + test/lint cycle + ROADMAP).

---

### ✅ P8.2 — ABORT_PLATEAU recovery : ENRICHED_RETRY + PlateauDiagnosis (RÉSOLU 2026-05-15)

**Statut** : ✅ Résolu — un plateau ne s'écrase plus en silence, le converger donne une 2e chance avec diagnostic injecté

**Cause racine** : `Converger._is_plateau()` détectait correctement la stagnation (2 deltas mu ≤ 0 + fail count non décroissant) mais `decide()` retournait immédiatement `ABORT_PLATEAU` sans (a) exposer pourquoi (dimensions stagnantes, assertions failed), (b) donner au prompt suivant une dernière chance avec ce diagnostic en contexte. NEXOS abandonnait collectif-nova (μ=8.05) et vertex-pmo (μ=7.91) sans la moindre instrumentation actionnable.

**Décision** (suite challenge Codex `019e2baf`) : pas de switch model (hypothèse rejetée — "another model will likely produce different-looking failure with the same score" sans diagnostic). Au lieu de ça, instrumentation + 1 enriched retry informationnel. Si le retry plateau aussi → `ABORT_PLATEAU` cette fois pour de vrai.

**Implémentation** (côté `soic_v3` commit `550631c`) :
- `soic/converger.py` :
  - Nouveau `Decision.ENRICHED_RETRY`
  - Dataclasses frozen `FailingAssertion` (gate_id, name, dimension, score, evidence) + `PlateauDiagnosis` (iteration, mu_trajectory, fail_trajectory, failing_dimensions, failing_assertions, phase) avec `to_dict()` JSON-safe
  - Flag interne `_enriched_retry_used` (re-armé par `reset()`)
  - `_build_diagnosis()` snapshot les failing gates + trajectoires au moment de la détection
  - `diagnose_plateau()` méthode publique pour le consommateur (iterator + feedback router)
  - `get_summary()` étendu avec un message dédié pour `ENRICHED_RETRY`
- `soic/feedback_router.py` :
  - `FeedbackRouter.generate_with_plateau_context(report, diagnosis)` : préfixe markdown explicite (trajectoire mu, fail count, dimensions bloquantes, assertions échec individuelles) devant le feedback corrective standard
- `soic/iterator.py` :
  - `SOICIterator` + `PhaseIterator` : sur `ENRICHED_RETRY`, enrichissent le feedback via `diagnose_plateau()` et **continuent le loop** (`ENRICHED_RETRY` n'est pas dans `stop_decisions`)

**Tests régression** (côté `nexos_v.3.0` — `tests/test_soic/test_converger.py`) :
- `test_first_plateau_yields_enriched_retry` — 3 points → ENRICHED_RETRY
- `test_second_plateau_yields_abort` — 4e point identique → ABORT_PLATEAU (retry consommé)
- `test_enriched_retry_offered_once_per_lifecycle` — `reset()` ré-arme le flag
- `test_diagnose_plateau_returns_none_before_plateau` — pas de diagnostic prématuré
- `test_diagnose_plateau_captures_failing_dimensions` — extrait D4 + D8 + assertions W-05, W-14
- `test_diagnose_plateau_to_dict_is_json_safe` — round-trip JSON propre
- `test_summary_for_enriched_retry_is_informative` — message visible CLI
- `test_feedback_router_with_plateau_context` — préfixe diagnostic + feedback standard

Mise à jour de `test_plateau_detected` existant pour aligner sur la nouvelle sémantique (1er plateau = ENRICHED_RETRY au lieu de ABORT_PLATEAU).

**Validation** : 489/489 tests Python verts (482 baseline P8.1 + 7 nouveaux P8.2), ruff check + format clean.

**Effort réel** : ~1h45 (cartographie 15 min + converger 20 min + iterator + feedback_router 15 min + tests 35 min + ruff + commits 20 min).

**Prochaines étapes liées (non faites cette session)** :
- P8.3 dimension-scoped fixers — extension auto_fixer qui route D8 fail → legal fixer, D4 → security fixer (réutilise `PlateauDiagnosis.failing_dimensions` comme signal)
- Mesure terrain : relancer collectif-nova et vertex-pmo pour vérifier que ENRICHED_RETRY débloque effectivement le plateau

---

### 🔴 P8 — Bugs réels à corriger (NOTÉS 2026-05-15, replan post-Codex)

**Statut** : 🔴 Identifiés à l'audit post-stabilisation. **Aucun bloquant pour exploitation actuelle.**

#### B1 — Osiris : 2 axes en échec côté scanner externe

**Symptôme** :
```
ERREUR Intrusion : Blocklist introuvable : blocklists/trackers.json
ERREUR Légalité : No module named 'playwright'
```

**Impact** : Score Osiris partiel 6/8 axes (au lieu de 8/8). NEXOS reçoit JSON valide mais incomplet. Dimensions Intrusion (I) et Légalité (L) absentes des mesures.

**Cause** : Deps externes du scanner Osiris manquantes côté `/home/gear-code/02_projects/NEXOS_PLATFORM/osiris/`. Hors scope NEXOS strictement, mais bloque la mesure complète.

**Fix proposé** :
```bash
cd /home/gear-code/02_projects/NEXOS_PLATFORM/osiris
pip install playwright && playwright install chromium
# + récupérer blocklists/trackers.json (probablement repo externe Osiris)
```

**Effort estimé** : 30 min. **Valeur** : élevée (gain de 2 axes critiques sur la mesure de chaque site).

---

#### ✅ B2 — CVE HIGH npm audit (RÉSOLU 2026-05-18)

**Statut** : ✅ Résolu — 6 clients alignés sur stack patchée + 1 client hors scope documenté.

**Stack patchée** (versions exactes, convention repo) :
- next `15.5.15` → `15.5.18`
- next-intl `3.25.1` → `4.12.0` (major, mais API client `useTranslations` rétrocompatible avec usage NEXOS)
- postcss `8.4.49` → `8.5.10` (patch XSS `</style>`)

**Approche tungsten** (pilote + batch + check-in user) :
1. Pilote vertex-pmo (commit `56c8320`) : upgrade + build + audit + serve localhost:20100 + preflight + SOIC re-eval → run 5 persisté `ACCEPT μ=9.10` (vs baseline run 4 `μ=9.00`, +0.10)
2. **Check-in user** entre pilote et batch (règle N3 strict ROADMAP)
3. Batch 4 clients trackés (commit `46e93fa`) : clinique-aura, beaumont-avocats, electro-maitre-industriel, table-de-marguerite — boucle `npm install` + pin exact + `npm install --package-lock-only` + `npm run build` + `npm audit --audit-level=high` — 5/5 PASS (collectif-nova upgrade on-disk mais ignored par `.gitignore:23`)

**Validation post-upgrade** :
- vertex-pmo : npm audit HIGH `1 → 0` ; Lighthouse perf `92 → 99` ; SOIC `D4 9.33 → 10.00` ; μ `9.00 → 9.10`
- 5 autres clients : `npm run build` PASS, `npm audit --audit-level=high` exit 0 — patterns Next 15 (`params: Promise<>`) déjà migrés en sessions antérieures, pas de fix code requis pour next-intl 3→4 (API `useTranslations` client compatible)
- 562/562 tests Python verts (aucune régression)
- `nexos doctor --all-clients` : 3/16 déployables (vertex-pmo `μ=9.10`, beaumont-avocats `μ=8.50`, depanneur-nobert `μ=9.11`)

**Hors scope** :
- **mark_systems_demo** : déjà sur `next 16.2.3` (plus récent que 15.5.18). 1 HIGH CVE résiduel sur next 16 (advisories GHSA-* non liés à postcss/formatjs) que `npm audit fix` ne peut pas résoudre automatiquement. **Follow-up B2.1** : aligner mark_systems_demo sur la dernière 16.x patchée ou downgrade vers 15.5.18.
- **depanneur-nobert** : hors stack NEXOS depuis 2026-05-17 (déménagé vers `/home/gear-code/01_business/clients/03_Depanneur_Nobert/04_livrables/site-web/`). À traiter dans son emplacement business si tracké git séparément.

**Effort réel** : ~1h45 (baseline + pilote + check-in + batch + validation + ROADMAP).

---

#### B3 — ABORT_PLATEAU bloque 2 clients sans recovery automatique

**Symptôme** :
```
collectif-nova : μ=8.05 décision=ABORT_PLATEAU
vertex-pmo     : μ=7.91 décision=ABORT_PLATEAU
```

**Comportement actuel** : SOIC Converger détecte un plateau (μ ne progresse plus après N itérations) et abandonne. C'est volontaire — évite les boucles infinies coûteuses en tokens.

**Trou de couverture** : aucune stratégie de recovery automatique. NEXOS dit "non" sans dire "voici comment débloquer". Pour ces 2 clients, humain doit intervenir manuellement.

**Fix proposé** : ajouter `Converger.recover_from_plateau()` qui essaie séquentiellement :
1. Re-générer la phase avec un modèle LLM différent (claude → codex → gemini)
2. Re-prompt avec contexte enrichi (afficher les findings SOIC précédents)
3. Si rien ne marche après 2 stratégies, vrai ABORT_PLATEAU avec changelog explicite

**Effort estimé** : 2-3h (logique Converger + tests). **Valeur** : élevée pour autonomie totale (sinon NEXOS reste manuel sur ~25% des clients).

---

#### B4 — 6 clients dormants (brief OK, pipeline jamais exécuté)

**Clients concernés** :
```
iusine, jokeresthetique, la-villa-du-sous-marin,
l-usine-rh, l-usinerh, nexos-platform-industrial, usine-rh
```

**Symptôme** : Ces clients ont un `brief-client.json` mais pas de `site/`, pas de `soic-gates.json`. Le pipeline a soit jamais été lancé, soit a échoué silencieusement sans laisser de trace exploitable.

**Cause probable** : Sessions antérieures où le pipeline a été interrompu. Manque de logging de l'échec dans changelog.

**Fix proposé** :
1. Lancer `nexos create --client-dir clients/<slug>` un par un sur les 7 dormants
2. Logger explicitement les échecs (P2 + P6 ont déjà nettoyé les silent paths)
3. Pour chaque échec, classer la cause (timeout LLM, rate limit, brief incomplet, modèle CLI absent)

**Effort estimé** : 1-3h selon taux de succès. **Valeur** : moyenne (récupère 7 clients en pipeline actif).

---

### 🟡 P9 — Dette technique (notée 2026-05-15)

**Statut** : 🟡 Polish / amélioration. Zero blocage opérationnel.

#### D1 — CI Vitest matrix limitée à 1 client sur 8
J'ai ajouté Vitest dans CI hier (commit `5e05951`) avec matrix `client: [depanneur-nobert]`. Les 7 autres clients : aucune protection régression UI/Zod/API en CI.
**Action** : propager les 70 tests Vitest aux 7 autres clients, étendre matrix. Effort ~2h.

#### D2 — Divergence SOIC interne vs Osiris externe
depanneur-nobert : SOIC μ=9.11 (READY) ↔ Osiris 4.0/10 (Critique). Les deux mesurent des choses différentes (technique NEXOS vs santé opérationnelle réelle). NEXOS est aveugle à ce qu'Osiris mesure.
**Action** : intégrer Osiris score comme dimension SOIC D10 (ou pondérer μ par Osiris). Effort 2-3h.

#### D3 — Doc obsolète CLAUDE.md (symlinks)
```
osiris  → ~/osiris-scanner   # n'existe pas
core-v3 → ~/projects/ai/ainova-os-v3   # n'existe pas
```
Le script `osiris-scan.sh` a un fallback sibling qui marche. Mais la doc ment.
**Action** : corriger CLAUDE.md ou créer les symlinks. Effort 10 min.

#### D4 — mypy installation inconsistante
`python3 -m mypy` retourne "No module named mypy" en CLI direct. Mais `pytest tests/test_mypy_clean.py` passe (via venv). Inconsistance environnement.
**Action** : `pip install mypy` au niveau système OU documenter activation venv. Effort 5 min.

#### ✅ D5 — Verdict deploy marginal beaumont (RÉSOLU 2026-05-18 par effet de bord)
Baseline 7 mai était μ=8.5014 pile. Marge cible 0.3.

**Mesure live post-B2** (build localhost:20100 + preflight + GateEngine) :
- **μ = 9.4562 ACCEPT** (+0.95 vs baseline, **>3× la cible 0.3**)
- coverage 0.889 (+0.007), fail_count = 0
- Toutes les dimensions ≥ 8.5 sauf D8 (7.67 — cap structurel cookie_consent 7.0 + Loi 25 RPP keywords manquants, à fixer par template-update plutôt que fixer auto)

**Sources du gain** :
- README.md ajouté hors-session entre mai-7 et mai-18 → D2 `3.5 → 8.5`
- `app/[locale]/layout.tsx` ajouté hors-session → D7 `7.0 → 10.0`
- P4b CSP/headers propagation (15 mai) → D4 `9.44 → 10.0` (W-06)
- B2 upgrade (18 mai) → D4 W-05 npm-audit `8.0 → 10.0`

Aucun fixer NEXOS appliqué cette session — la marge était déjà acquise. Run 2 persisté `soic-gates.json` + `soic-runs.jsonl`. Commit `b275094`.

#### D6 — `brief-synthesizer` schéma strict
`additionalProperties: false` rejette champs comme `sector` qui pourraient être utiles. Friction UX. Pas un bug, by design.
**Action** : ajouter champs optionnels au schéma (`sector`, `tags`, `notes`) si valeur produit confirmée. Effort 20 min.

#### ✅ D7 — `tools/preflight.sh` chemin relatif cassé (RÉSOLU 2026-05-17)

**Cause racine** : `TOOLING_DIR="$CLIENT_DIR/tooling"` (ligne 12) était relatif au cwd. Puis ligne 44 `cd "$SITE_DIR"` changeait le cwd. Ligne 45 `npm audit --json > "$TOOLING_DIR/npm-audit.json"` cherchait à écrire dans `<SITE_DIR>/<CLIENT_DIR>/tooling/npm-audit.json` (path résolu relativement au nouveau cwd) qui n'existait pas. Le `|| true` masquait l'erreur, le script affichait `✓`, et `npm-audit.json` n'était jamais écrit. Découvert audit Mark Systems 2026-05-17, **reproduit en direct pendant P8.5 vertex-pmo** (preflight loggé `ligne 45: clients/vertex-pmo/tooling/npm-audit.json: Aucun fichier ou dossier de ce nom`).

**Décision** : résoudre `CLIENT_DIR` / `TOOLING_DIR` / `TOOLS_DIR` en **chemins absolus** via `realpath` dès l'entête, avant tout `cd`. Approche moins invasive que remplacer le bloc npm par `tools/deps-scan.sh` (qui aurait demandé un test d'intégration plus large).

**Implémentation** (1 commit atomique) :
- `tools/preflight.sh` : `mkdir -p "$CLIENT_DIR_RAW"` (cohérence : créer si absent avant realpath) + `realpath` sur `CLIENT_DIR` et `TOOLS_DIR`. Commentaire D7 inline pour traçabilité.
- `tests/test_preflight_sh.py` (nouveau, 4 tests) :
  - `test_npm_audit_json_written_with_relative_client_dir` — fixture relative + mock npm via PATH override → assert `npm-audit.json` existe et JSON valide
  - `test_no_redirection_error_in_stderr` — garde-fou anti-régression : aucun "Aucun fichier ou dossier" / "No such file or directory" sur stderr
  - `test_preflight_exit_code_zero_on_partial_tools` — pattern hardening P4d préservé
  - `test_tooling_dir_created_inside_client_dir` — `tooling/` créé sous CLIENT_DIR, pas sous SITE_DIR

**Validation** : 562/562 tests Python verts (558 baseline + 4 D7). ruff clean (import sort autocorrigé).

**Effort réel** : ~25 min (test guard 10 min + fix bash 2 min + correction test pour reproduire le bug avec path relatif 5 min + ruff format + ROADMAP 8 min). Estimation initiale 20 min tenue.

---

#### ✅ D9 — `nexos doctor` lisait la 1ère entrée `soic-gates.json` au lieu de la dernière (RÉSOLU 2026-05-17)

**Cause racine** : `nexos/tooling_manager.py:316` et `:375` utilisaient `next((g for g in gates if g.get("phase") == "ph5-qa"), None)` qui retourne la **première** entrée matchant. Pour tout client ayant plus d'un run Ph5 (audit re-évalué), doctor affichait un μ + verdict **périmé**. Découvert pendant P8.5 vertex-pmo : persistance run 4 ACCEPT μ=9.00 invisible derrière run 1 ABORT_PLATEAU μ=7.91. Le bon pattern existait déjà dans `orchestrator/score_injection.py:_load_latest_gate` (`matching[-1]`), mais avait été dupliqué à l'envers dans tooling_manager.

**Décision** : extraire un helper local `_latest_phase_gate(gates, phase) -> dict | None` (cohérent avec `_load_latest_gate`, sans créer de dépendance tooling_manager → orchestrator), remplacer les 2 instances. Test régression in vivo sur fixture multi-runs.

**Implémentation** (1 commit atomique) :
- `nexos/tooling_manager.py` : nouveau helper `_latest_phase_gate` + 2 remplacements de `next(...)`
- `tests/test_tooling_manager.py` : `test_client_status_row_picks_latest_gate_when_multi_runs` — fixture avec [ABORT_PLATEAU μ=7.91 mai 7, ACCEPT μ=9.00 mai 17] → assertion row['ph5_mu']='9.00' + row['deploy']='READY'

**Validation in vivo** : `nexos doctor --all-clients` affiche désormais vertex-pmo `μ=9.00 READY` (vs `μ=7.91 ABORT_PLATEAU` avant fix). Déployables 2/16 → 3/16.

**558/558 tests verts** (557 baseline + 1 D9). ruff clean.

**Effort réel** : ~20 min (TDD red + helper + remplacement + test + lint).

---

#### ✅ D8 — `_dry_run_analysis` désynchronisé de `FIXER_ORDER` (RÉSOLU 2026-05-17)

**Cause racine** : `nexos/cli_commands.py:_dry_run_analysis()` hardcodait 6 checks (cookie_consent + vercel_headers + csp + next_config + privacy_page + legal_page + générique npm_audit). Depuis P8.1 (`readme` ajouté mai 15) et P8.6 (`pa11y_contrast` ajouté ce matin), 2 fixers de `FIXER_ORDER` étaient invisibles au dry-run et 1 (`csp_middleware`) aussi. Découvert pendant P8.5 mesure terrain vertex-pmo : `nexos fix --dry-run` annonçait 1 fix (npm audit) alors que le fix réel en appliquait 1 (pa11y_contrast). Aucun garde-fou anti-dérive.

**Décision** : refactor pour faire de `FIXER_ORDER` la source unique de vérité aussi en mode dry-run, via un registre `DRY_RUN_DESCRIBERS: dict[str, Callable]` parité 1:1 + test invariant. Cohérent avec la décision Codex P8.1 (pas de Protocol+toposort architectural — registre testé suffit).

**Implémentation** (1 commit atomique) :
- `nexos/auto_fixer.py` :
  - 10 fonctions `_describe_*` read-only répliquant la logique de détection des `_fix_*` correspondants (skip défensifs identiques, jamais d'effet de bord)
  - `DRY_RUN_DESCRIBERS: dict[str, Callable[[Path, Path, dict | None], str | None]]` mapping name → describer
  - `describe_auto_fix(site_dir, client_dir, brief) -> list[str]` itère `FIXER_ORDER` et délègue (KeyError immédiat si fixer sans describer = fail-fast)
- `nexos/cli_commands.py` :
  - `_dry_run_analysis` passe de 64 lignes hardcodées à 12 lignes thin wrapper
  - Imports nettoyés : suppression `REQUIRED_HEADERS`, `_resolve_app_root`, `_resolve_components_dir` (plus utilisés directement)
- Tests régression (18 nouveaux, 557/557 verts) :
  - `TestDryRunDescribers` (3) — invariants structurels : parité ensembles `set(DRY_RUN_DESCRIBERS) == {f.name for f in FIXER_ORDER}`, signature `str | None`, ordre des findings = ordre FIXER_ORDER
  - 11 classes `TestDescriberParity*` (15 tests) — pour chaque describer, fixture "besoin" → finding ≠ None, fixture "ok" → None (sauf npm_audit générique)

**Validation in vivo sur vertex-pmo** :
- Avant D8 : dry-run liste 1 finding (`npm audit fix → exécuterait...`)
- Après D8 : dry-run liste 3 findings (npm_audit + csp_middleware + pa11y_contrast 1 token sous WCAG AA 4.5:1 sur bg #0F172A) — exactement ce que le fix réel appliquerait
- Inventaire `nexos doctor --all-clients` inchangé (16 clients, 2/16 déployables)

**Pourquoi ça résiste à la dérive future** : `describe_auto_fix` fait `DRY_RUN_DESCRIBERS[fixer.name]` (lookup direct sans `.get()` ni fallback). Tout fixer ajouté à `FIXER_ORDER` sans son describer lève `KeyError` au premier appel, et le test `test_describers_cover_all_fixers` échoue avant même la mise en exécution.

**Effort réel** : ~1h30 (design + test guard 30 min + 10 describers 20 min + refactor cli + fix bug `_contrast_ratio` signature + tests fixtures alignées sur convention multi-ligne 20 min + lint + doctor + ROADMAP 20 min).

---

### 🟢 Items P4 archivés (référence historique)

#### P4a — Étendre `_fix_csp` à `next.config.mjs`
**Pourquoi pas plus haut** : la CSP est déjà servie en prod via `vercel.json`. Le manque en local est cosmétique (juste pour passer preflight headers-scan local). Polish-pour-polish.

**Plan** : ajouter logique regex défensive dans `nexos/auto_fixer.py:_fix_csp` qui patch aussi `next.config.mjs` ou crée un middleware Next dédié. Risque : regex fragile sur le bloc `async headers()`.

**Effort** : 30 min · **Valeur** : faible

#### P4b — Propager les fixes aux 17 autres clients
**À faire après P1** uniquement (sans P1, on propage à l'aveugle).

**Clients candidats** (brief+gates+site présents) :
- beaumont-avocats
- clinique-aura
- collectif-nova
- electro-maitre-industriel
- mark_systems_demo
- table-de-marguerite
- vertex-pmo

**Plan** : script bash `for client in <liste>; do nexos fix $client; done` + commit groupé par client (un commit par client pour traçabilité).

**Effort** : 1h batch · **Valeur** : moyenne

#### P4c — Étendre tests Vitest (composants UI, routes API, schémas Zod)
**Plan** : ajouter @testing-library/react + jsdom, tests sur :
- CookieConsentBanner (rendu + interactions)
- Formulaires Contact/Newsletter (validation Zod + submit)
- Routes API (handlers + rate limit)
- Util `produits.ts`, `promotions.ts`, `horaires.ts`

**Effort** : 2-3h · **Valeur** : moyenne (qualité long-terme)

#### P4d — Hardening `tools/*.sh`
Le pattern osiris-scan (JSON cassé) attrapé cette session suggère que d'autres scripts shell peuvent avoir la même dette : `deps-scan.sh`, `ssl-scan.sh`, `headers-scan.sh`. À auditer chacun pour :
- Émission JSON valide même en cas d'erreur (via `python3 -c` au lieu d'interpolation bash)
- Timeouts explicites
- Stderr non supprimé en cas d'échec
- Échappement des inputs URL/path

**Effort** : 1h · **Valeur** : moyenne (robustesse pipeline)

#### P4e — Mode `nexos doctor --all-clients` détaillé
Étendre la commande `nexos doctor --client <slug>` ajoutée cette session pour supporter `--all-clients` qui produit un rapport tabulaire de tous les clients à la fois (un par ligne, état brief/site/gates/deploy).

**Effort** : 30 min · **Valeur** : moyenne (visibilité opérationnelle)

---

## 📋 Workflow type d'une session NEXOS

### Ouverture (5 min)

```bash
cd /home/gear-code/02_projects/NEXOS_PLATFORM/nexos_v.3.0

# 1. Checkpoint git
git status
git log --oneline -10
git fetch origin && git log origin/main..HEAD --oneline   # commits locaux non poussés

# 2. Checkpoint NEXOS
python3 nexos_cli.py doctor                                # plateforme globale
python3 nexos_cli.py doctor --client depanneur-nobert      # cas test focus

# 3. Relire le roadmap
cat ROADMAP.md

# 4. Vérifier tests verts AVANT de toucher
python3 -m pytest tests/ -q --tb=no
```

### Exécution

- **Une priorité à la fois** : P1, ou P2, ou P3. Pas de mélange.
- **Commits atomiques** par sous-étape (`feat:` / `fix:` / `test:` / `docs:`).
- **Pre-commit hooks tiennent** : ruff check, ruff format, JSON valid, EOF, secrets, UsineRH guard.
- **Pas de `git push` autonome** (règle absolue).
- **Pas de `vercel deploy` autonome** (règle absolue).

### Clôture (10 min)

```bash
# 1. Tests verts
python3 -m pytest tests/ -q --tb=no
cd clients/<cas-test>/site && npm test -- --run && cd -

# 2. Build verts si site touché
cd clients/<cas-test>/site && npm run build && cd -

# 3. Status propre
git status

# 4. Update ROADMAP.md
#    - Marquer les items terminés (status, date, commits SHA)
#    - Ajouter les items dette découverts en chemin
#    - Mettre à jour "Dernière mise à jour" et "État actuel"

# 5. Commit du roadmap
git add ROADMAP.md
git commit -m "docs(roadmap): update post session YYYY-MM-DD"

# 6. Récap pré-push à l'utilisateur (jamais push autonome)
git log origin/main..HEAD --oneline
git diff origin/main..HEAD --stat | tail -10
```

---

## 🚫 Anti-patterns à éviter

1. **Re-lancer Ph5 LLM pour "avoir le score officiel"** avant P1 résolu — verdict douteux, n'apporte aucune information utile.

2. **Pousser `git push`/`vercel deploy` sans confirmation explicite** en bloc isolé — règle absolue documentée dans `~/.claude/CLAUDE.md` user.

3. **Yak shaving** : démarrer P1 et bifurquer sur P4 en chemin parce qu'on tombe sur un truc intéressant. Si une nouvelle dette est découverte, **la noter dans ROADMAP.md** mais ne pas la fixer dans la même session.

4. **Yes-mannerie** : accepter une instruction utilisateur sans la challenger quand elle viole une règle absolue de l'utilisateur lui-même. Cf session 2026-05-15 — `git push` refusé même sur "Go fais-le", repris uniquement quand l'utilisateur l'a lancé manuellement.

5. **Propager aveuglément aux 17 autres clients** avant que P1 (divergence Ph5/SOIC) soit résolu. Sinon tu propages des changements dont tu ne peux pas valider l'impact réel.

6. **`rm -rf` non-essentiel** — bloqué par le harness mais aussi par la règle absolue. Préférer cleanup ciblé.

7. **Tester sur le mauvais build/serveur** : NEXOS sert le build figé au démarrage. Si tu modifies code source pendant qu'un serveur tourne, le serveur sert l'ancien build. Toujours rebuild + restart sur **nouveau port** quand tu veux valider.

---

## 📚 Références techniques

### Fichiers clés (cartographie rapide)

| Fonction | Fichier |
|---|---|
| CLI entry point | `nexos_cli.py` |
| Argparse global | `orchestrator/cli_args.py` |
| Dispatch modes | `orchestrator/main.py` |
| Run pipeline | `orchestrator/phases.py:run_pipeline` |
| Preflight tooling | `orchestrator/preflight.py` |
| Auto-fixer D4/D8 | `nexos/auto_fixer.py` |
| Build validator | `nexos/build_validator.py` |
| Commandes CLI standalone | `nexos/cli_commands.py` |
| Doctor reports | `nexos/tooling_manager.py:doctor_report, doctor_client_report` |
| Changelog événementiel | `nexos/changelog.py` |
| Session launcher (claude/codex CLI) | `nexos/session_launcher.py` |
| SOIC evaluator | `soic_v3/evaluate.py` (symlink `soic/`) |
| SOIC converger | `soic_v3/converger.py` |
| Templates | `templates/*.json|*.tsx|*.md` |
| Tools shell | `tools/*.sh` |
| Agents Ph0→Ph5 | `agents/{ph0,ph1,ph2,ph3,ph4,ph5}-*/` |
| Knowledge base | `agents/knowledge/` |

### Commandes utiles

```bash
# Diagnostic
nexos doctor                                    # plateforme
nexos doctor --client <slug>                    # client ciblé

# Auto-fix
nexos fix <slug>                                # auto-résolu vers clients/<slug>
nexos fix <slug> --dry-run                      # analyse seule

# Rapports
nexos report <slug>                             # agrégé client

# Pipeline
nexos create --client-dir clients/<slug> --stack nextjs
nexos audit --client-dir clients/<slug> --url http://localhost:20003  # 🔴 cassé (P2)
nexos modify --client-dir clients/<slug> --section S-NNN

# Modules NEXOS isolés
nexos module list
nexos workflow list

# Tests
python3 -m pytest tests/ -q --tb=no                          # NEXOS
cd clients/<slug>/site && npm test -- --run                  # site

# Build site
cd clients/<slug>/site && npm run build

# Tooling preflight manuel (sans pipeline complet)
bash tools/preflight.sh http://localhost:<port> clients/<slug>
```

### Règles absolues (rappel utilisateur)

Source : `~/.claude/CLAUDE.md` user (gear-code)

- **Jamais `git push` autonome** — décisions utilisateur explicites
- **Jamais `vercel deploy` autonome** — idem
- **Jamais `--no-verify` git commit** sans demande explicite
- **Jamais modification raccourcis clavier** sans confirmation
- **Jamais `rm -rf` hors paths autorisés**
- **Jamais suppression `.env` ou credentials**
- **Pas de yes-mannerie** : challenger plutôt qu'accommoder. Seul critère = est-ce que ça fonctionne à la fin ?
- **Pas de scaffolding sans fonctionnement** : avant chaque ajout, « ça fait fonctionner un projet, ou ça documente juste une exécution ? »

### Zones de ports autorisées (NEXOS_PLATFORM)

Source : `~/.claude/CLAUDE.md` user — section "Allocation des ports"

- **Zone NEXOS** : 20000-20999
  - 20000-20099 : tests éphémères (sites Next preview, builds locaux)
  - 20100-20199 : pipeline engine (gateway, soic-eval, services internes)
  - 20200-20299 : scraping & automation
  - 20300-20399 : cybersec NEXOS interne
  - 20900-20999 : buffer ad-hoc NEXOS
- **🚫 Interdit** : 0-1023 (privilégiés), 32768-60999 (zone éphémère kernel)
- **Buffer global** : 29000-29999 (one-shot tous projets)

### Stack par défaut (NEXOS sites clients)

- Next.js 15+ App Router · TypeScript 5 strict
- Tailwind CSS 3.4+ · Vitest 2
- next-intl FR/EN · next/image · next/font
- Lucide React · Framer Motion (avec prefers-reduced-motion)
- Déploiement Vercel · Loi 25 Québec enforcée

---

## 🗓️ Historique des sessions notables

### 2026-05-18 — P9 D5 résolu : beaumont marge μ 8.50 → 9.46 (claude, tungsten)
- Cible : sécuriser ~0.3 marge au-dessus du seuil 8.5 pour beaumont-avocats (baseline mai-7 μ=8.5014 pile, sans buffer pour régression).
- Méthode : build localhost:20100 (post-B2 batch), `tools/preflight.sh`, `GateEngine.run_all_gates()` (méthode B P8.5).
- Résultat surprise : **μ=9.4562 ACCEPT**, gain de +0.95 (3× la cible). Marge déjà largement acquise sans aucun fixer additionnel.
- Sources du gain reconstituées via diff dimensionnel vs run 1 :
  - D2 documentation `3.5 → 8.5` : README.md ajouté hors-session entre mai-7 et mai-18
  - D7 SEO meta `7.0 → 10.0` : `app/[locale]/layout.tsx` + sitemap + robots ajoutés hors-session
  - D4 sécurité `9.44 → 10.0` : P4b CSP/headers propagation (15 mai) + B2 npm-audit (18 mai)
  - D6 a11y `9.45` : `a11y.json = []` (0 erreurs WCAG, beaumont a probablement été touché par `_fix_pa11y_contrast` P8.6 ou n'a jamais eu le problème vertex-pmo)
- D8 reste à 7.67 (cap structurel cookie_consent 7.0 + W-14 RPP keywords incomplets), mais n'impacte pas la marge. Pas de fixer auto (template content, pas refactor code).
- Run 2 persisté `soic-runs.jsonl` + `soic-gates.json`. Commit `b275094` (4 fichiers, 170+).
- Doctor confirme : 4/16 déployables (vertex-pmo μ=9.10, beaumont μ=9.46, depanneur-nobert μ=9.11, et un 4e à valider — mais sur l'effective list au moment du run il y avait 3). Note : depanneur-nobert site=missing (déménagé) — doctor reflète encore l'ancien soic-gates.
- Pattern méthodo : **mesurer avant d'agir**. La task `D5 step 2 (analyser dimensions faibles)` + `step 3 (sécuriser via fixers)` ont été marquées completed-skip parce que step 1 a montré que le travail était déjà fait. Eviter de propose-fix par défaut quand la mesure suffit.
- Effort réel ~20 min (vs estimé 1h) — gain net 40 min libéré pour la suite.

### 2026-05-18 — B2 résolu : CVE HIGH next-intl/postcss upgrade (claude, tungsten N3)
- Cible : 6 clients NEXOS production set (vertex-pmo en pilote + 5 batch). Plan tungsten roadmap suivi à la lettre (pilote + check-in user + batch).
- **Pilote vertex-pmo** (commit `56c8320`) : `npm install next@15.5.18 next-intl@4.12.0 postcss@8.5.10` puis pin exact (retirer `^`) puis `npm install --package-lock-only`. Build PASS du premier coup — patterns Next 15 (`params: Promise<>`) déjà migrés. Lighthouse perf saute de 92 → 99. `npm audit --audit-level=high` exit 0.
- **Re-mesure SOIC live** (méthode B P8.5) : serveur sur localhost:20100, `tools/preflight.sh` regénère tooling/, `GateEngine.run_all_gates()` recalcule. Run 5 persisté dans `soic-runs.jsonl` + `soic-gates.json` : `μ=9.10 ACCEPT` (vs baseline run 4 `μ=9.00 ACCEPT`). Gain : W-05 npm-audit `FAIL 8.0 → PASS 10.0` (1 HIGH → 0), D4 dim `9.33 → 10.00`.
- **Check-in user** posé via `AskUserQuestion` entre pilote et batch (règle N3 ROADMAP). Validation explicite "Go batch — 6 clients en boucle".
- **Batch propagation** (commit `46e93fa`) : 4 clients trackés (clinique-aura, beaumont-avocats, electro-maitre-industriel, table-de-marguerite) + collectif-nova on-disk (gitignored `.gitignore:23`). Boucle bash uniformisée : install + pin exact + relock + build + audit. 5/5 PASS — aucun client n'a cassé sur next-intl 3→4 ou Next 15.5.18.
- **Hors scope identifié** : `mark_systems_demo` déjà sur `next 16.2.3` (plus récent que cible 15.5.18). 1 HIGH CVE résiduel non-corrigeable par `npm audit fix`. Documenté en follow-up B2.1 (aligner sur 16.x patchée ou downgrade 15.5.18).
- Discovery utile : `npm audit --audit-level=high` retourne exit 0 même avec 1 HIGH si pas de fix auto disponible — pas un substitut à la lecture du metadata `vulnerabilities.high`. À retenir pour B2.1.
- Validation finale : `nexos doctor --all-clients` confirme 3/16 déployables (vertex-pmo `μ=9.10`, beaumont-avocats `μ=8.50`, depanneur-nobert `μ=9.11`) — aucune régression. 562/562 tests Python verts.
- Pre-commit hook a refusé `tooling/lighthouse.json` (528 KB > 500 KB) — pattern identique à P8.5 baseline. Lighthouse JSON non-commitable, gardé local pour audit forensique.
- Effort réel ~1h45 (baseline 15 min + pilote upgrade+build+audit 20 min + SOIC re-eval + commit 25 min + check-in user 5 min + batch 5 clients 30 min + commit batch + ROADMAP 20 min). Estimation roadmap 3-4h dépassée largement à la baisse grâce au pilote propre.

### 2026-05-17 — Mark Systems Session 1 : sécurité + consentement réel (codex)
- Cible : `/home/gear-code/02_projects/mark-systems-site/web-version`.
- Sécurité : `npm audit fix` + upgrade contrôlé `next`/`eslint-config-next` vers `15.5.18` (versions exactes). HIGH/CRITICAL passent à 0 ; reste 2 MODERATE `postcss` embarqués par Next, sans correctif npm acceptable (`npm audit fix --force` propose une régression vers Next 9.3.3).
- Conformité : nouveau `src/lib/consent.ts` + `src/components/compliance/ConsentAnalytics.tsx`; Vercel Analytics / Speed Insights ne sont rendus que si consentement analytics explicite. Preconnect Vercel analytics retiré du layout avant consentement.
- i18n légal : liens `/fr/privacy` hardcodés remplacés par liens localisés (`/${locale}/privacy`) dans contact, brief wizard, navigation wizard et cookie consent.
- Compat Next 15 : pages/layout `[locale]` adaptés au contrat `params: Promise<{ locale: string }>` ; `contact/page.tsx` utilise `getTranslations` côté serveur.
- Validation : `npm test` 34/34, `npm run build` PASS, `npm audit --audit-level=high` PASS.
- Note session : le repo NEXOS affichait des suppressions massives non liées dans `clients/depanneur-nobert/site`; non touchées.

### 2026-05-17 — P9 D7 résolu : preflight.sh chemin absolu (claude, tungsten N2)
- Bug reproduit en direct pendant P8.5 vertex-pmo : `ligne 45: clients/vertex-pmo/tooling/npm-audit.json: Aucun fichier ou dossier de ce nom` — même message d'erreur que sur Mark Systems le matin du 17 mai. Cause unique : `TOOLING_DIR` relatif + `cd "$SITE_DIR"` ligne 44 → la redirection cherche un path inexistant.
- Test guard d'abord (TDD red) : nouveau `tests/test_preflight_sh.py` avec 4 tests qui appellent `bash preflight.sh` en subprocess, mock npm via PATH override, vérifient `npm-audit.json` écrit + stderr propre. Erreur "Aucun fichier ou dossier" reproduite exactement comme en prod avant fix.
- Fix bash : `mkdir -p "$CLIENT_DIR_RAW"` (création préalable nécessaire pour realpath) puis `realpath` sur `CLIENT_DIR` + `TOOLS_DIR`. 3 lignes modifiées, commentaire D7 inline.
- 562/562 tests verts (558 baseline + 4 D7). ruff clean (import sort autocorrigé).
- Petite leçon méthodologique : ma 1ère version du test passait parce que je passais `str(client)` absolu — le bug ne se déclenche QUE sur path relatif. J'ai dû modifier le test pour reproduire l'usage réel (`cwd=tmp_path` + `client_factice` relatif). Le test guard est aussi important que le fix : sans test fidèle au bug, on ne sait pas qu'on a vraiment fixé.
- Effort réel ~25 min (vs 20 min estimé), discipline tungsten maintenue.

### 2026-05-17 — P8.5 résolu : mesure terrain vertex-pmo READY μ=9.00 (claude, tungsten strict)
- **Résultat** : vertex-pmo passe de ABORT_PLATEAU μ=7.91 (mai 7) à ACCEPT μ=9.00 → **3e client déployable** (depanneur-nobert, beaumont-avocats, vertex-pmo).
- **Méthode B (validée par user)** : `tools/preflight.sh http://localhost:20100` (build + serve vertex-pmo en local) + invocation directe `soic.gate_engine.GateEngine.run_all_gates()` pour recalculer le score. Pas de coût LLM. Plus tungsten que `nexos audit` complet (qui invoque codex Ph5 et coûte tokens).
- **Validation routing P8.3 + fixer P8.6 in vivo** : `nexos fix clients/vertex-pmo` a appliqué 1 fix (`ink.muted #64748B → #7689a4` via `_fix_pa11y_contrast`). pa11y empirique sur localhost:20100 : **18 → 11 erreurs WCAG** (-39%, gain D6 +1.75).
- **Dimensions vs baseline mai 7** :
  - D2 doc 3.50 → 8.50 (+5.0) — README.md ajouté hors session entre mai 7 et 17
  - D6 a11y 5.10 → 6.85 (+1.75) — fixer P8.6 livre exactement ce qu'il promettait sur `surface.DEFAULT` (3.75:1 → 5.00:1)
  - D7 SEO 7.00 → 10.00 (+3.0) — layout.tsx + sitemap.ts + metadata ajoutés hors session
  - D4 sécu 9.44 → 9.33 (-0.11) — npm-audit FAIL 1 HIGH (CVE next-intl, c'est B2)
  - **μ pondéré 7.91 → 9.00 (+1.09)**, coverage 0.88 → 0.89
- **Persistance audit trail** : nouvelle entrée run 4 `soic-runs.jsonl` (run_id `336b7689`) + nouvelle entrée `soic-gates.json` (`decision: ACCEPT`). Le verdict deploy est désormais cohérent entre code et état officiel.
- **Limite documentée (P8.6.2 follow-up à créer)** : 11 erreurs G18 résiduelles toutes sur `text-ink-muted` utilisé sur `surface.alt #1E293B` (bg plus clair que `surface.DEFAULT`). Le fixer P8.6 cible un seul bg de référence. Sur `surface.alt`, contraste 4.10:1 (toujours < 4.5:1). Pour fermer complètement D6, créer P8.6.2 — extension multi-background : calibrer sur le bg le PLUS clair de la palette (pire cas), garantit conformité partout.
- **3 bugs latents découverts en chaîne pendant cette tâche** (chaîne tungsten « zéro bug en arrière ») :
  - D8 (`_dry_run_analysis` désynchronisé de FIXER_ORDER) → fixé immédiatement, commit `8459098`
  - D9 (doctor lit la 1ère entrée gates au lieu de la dernière) → fixé immédiatement, commit `42b546a`
  - P8.6.2 (fixer multi-background) → ajouté en backlog (impact terrain mesuré, urgence basse — vertex-pmo déjà READY malgré 11 erreurs)
- **Bonus découvert** : D7 SEO (W-13 gap historique signalé dans P8.3 ROADMAP) était déjà résolu hors session. Le fixer P8.7 spéculatif évoqué dans P8.5 design n'est plus urgent — créer un fixer SEO uniquement quand un vrai client le déclenchera en plateau.
- Files committed : `clients/vertex-pmo/{site/tailwind.config.ts, soic-gates.json, soic-runs.jsonl, nexos-changelog.json, tooling/}` (état terrain mesuré et persisté).
- Effort réel : ~2h (vs 30 min estimé) — dérive justifiée par 3 bugs latents fixés en chaîne, chacun avec son commit atomique. Méthode tungsten respectée intégralement (TDD pour D8/D9, audit terrain réel, articulation tracée).

### 2026-05-17 — P9 D9 résolu : doctor lit la dernière entrée gates (claude, tungsten strict)
- Bug en chaîne découvert pendant P8.5 vertex-pmo : après avoir persisté `soic-gates.json` avec une nouvelle entrée run 4 ACCEPT μ=9.00, `nexos doctor` continuait d'afficher run 1 ABORT_PLATEAU μ=7.91. Cause : `next((g for g in gates if g.get("phase") == "ph5-qa"))` retourne la première entrée matchant.
- Pattern existait déjà correctement dans `orchestrator/score_injection.py:_load_latest_gate` (`matching[-1]`) — duplication à l'envers dans tooling_manager (dette historique).
- Fix : extract `_latest_phase_gate(gates, phase)` helper local + remplacement des 2 instances (lignes 316 + 375).
- Test régression `test_client_status_row_picks_latest_gate_when_multi_runs` avec fixture multi-runs [mai 7 ABORT, mai 17 ACCEPT] → assert dernière entrée lue.
- Validation in vivo : doctor affiche désormais vertex-pmo `μ=9.00 READY`, déployables 2/16 → 3/16. Tests 558/558 verts.
- Confirmation [[feedback_zero_bug_left_behind]] : un bug découvert pendant tâche X (P8.5) sur le chemin critique de validation = fix immédiat avant de continuer. P8.5 ne pouvait pas committer un état que doctor ne refléterait pas.
- Effort réel ~20 min (TDD red + helper + remplacement + test + lint + ROADMAP).

### 2026-05-17 — P9 D8 résolu : describers dry-run parité FIXER_ORDER (claude, tungsten strict)
- Découverte pendant préparation P8.5 : `nexos fix clients/vertex-pmo --dry-run` annonçait 1 finding (npm_audit générique) alors que le vrai `auto_fix()` allait appliquer pa11y_contrast (P8.6) et potentiellement readme (P8.1). `_dry_run_analysis` (cli_commands.py:313) hardcodait 6 checks, désynchronisé du `FIXER_ORDER` depuis P8.1 (15 mai) et P8.6 (17 mai matin). Aucun garde-fou anti-dérive.
- Décision tungsten (anti-yes-mannerie) : pause P8.5, fix D8 d'abord. Un dry-run menteur invalide la méthodologie « design + validation avant impl ». Cf [[feedback_zero_bug_left_behind]] créée à cette occasion.
- Approche : registre `DRY_RUN_DESCRIBERS: dict[str, Callable]` parité 1:1 avec `FIXER_ORDER` + test invariant `set(DRY_RUN_DESCRIBERS) == {f.name for f in FIXER_ORDER}`. KeyError immédiat si futur fixer ajouté sans describer (fail-fast intégré). Cohérent avec Codex P8.1 (registre testé > Protocol architectural).
- 10 describers ajoutés à `nexos/auto_fixer.py` (cookie_consent, npm_audit, vercel_headers, csp, csp_middleware, next_config, privacy_page, legal_page, readme, pa11y_contrast) répliquant les conditions de détection des `_fix_*` correspondants en read-only strict.
- `describe_auto_fix(site_dir, client_dir, brief) -> list[str]` itère FIXER_ORDER. `_dry_run_analysis` passe de 64 lignes hardcodées à 12 lignes thin wrapper.
- Bug latent attrapé en cours : `_describe_pa11y_contrast` passait `match.group("hex")` (str) à `_contrast_ratio` qui attend `tuple[float, float, float]` → ValueError silencieuse au test. Fix par `_hex_to_rgb()` avant + try/except défensif (cohérent avec les fixers existants).
- Validation in vivo vertex-pmo : dry-run liste maintenant 3 findings (npm_audit + csp_middleware + pa11y_contrast `1 token muted sous WCAG AA 4.5:1 sur bg #0F172A → durcirait jusqu'à 5.0:1`) — exactement ce que le fix réel appliquerait.
- Tests régression : 18 nouveaux (3 invariants TestDryRunDescribers + 15 parité TestDescriberParity*), **557/557 verts** (539 baseline + 18 D8). ruff format + check clean. mypy via venv OK (CLI direct = dette D4 connue).
- Articulation tungsten : impossible d'ajouter un futur fixer en P8.X sans (a) son describer (KeyError runtime) ET (b) son entrée DRY_RUN_DESCRIBERS (test invariant rouge). Double protection.
- Effort réel ~1h30 (design + test guard 30 min + 10 describers 20 min + refactor cli + fix `_contrast_ratio` signature + fixtures alignées convention multi-ligne 20 min + lint + doctor + ROADMAP 20 min).

### 2026-05-17 — P8.6 résolu : fixer D6 contraste WCAG (claude, mode rigoureux continu)
- Découverte critique pendant P8.5 (mesure terrain) : vertex-pmo a déjà tous les fichiers W-13 (sitemap.ts, robots.ts, metadata) et W-02 (README) que le plan P8.6 initial voulait créer. Le plateau historique D7=7.0/D2=3.5 était obsolète. Le seul vrai bloqueur restant = 18 erreurs pa11y W-10, toutes du même type contraste sur le token `text-ink-muted`.
- Pivot du plan : au lieu des 4 fixers D6+D7 spéculatifs, livrer 1 fixer ciblé `_fix_pa11y_contrast` qui résout la cause racine universelle (palette Tailwind avec token muted à contraste insuffisant).
- Architecture pure-stdlib : 6 helpers WCAG (hex_to_rgb, relative_luminance WCAG 2.1, contrast_ratio, rgb_to_hsv via colorsys, harden_token_contrast). Algorithme : déplacer V (HSV) par pas de 0.02 dans la direction opposée à la luminance du fond, jusqu'à atteindre 5.0:1 (buffer au-dessus du seuil AA 4.5:1). Préserve hue + saturation → l'intention "muted" visuelle reste.
- Détection background : sondes `surface` / `background` / `bg` / `body` en priorité, lit le `DEFAULT` du bloc. Couvre les conventions de vertex-pmo (dark theme `surface.DEFAULT`) et depanneur-nobert (light theme `background.DEFAULT`).
- Validation terrain (dry-run sur vrai `clients/vertex-pmo/site/tailwind.config.ts`) : ink.muted `#64748B` → `#7689a4`, contraste passe de **3.75:1 à 5.00:1** (buffer cible atteint exactement).
- Wiring P8.3 automatique : `dimension="D6"` sur le Fixer → `fixers_for_dimensions({"D6"})` retourne `[pa11y_contrast]` → hook `_plateau_auto_fix` l'appelle dès qu'un futur plateau remonte D6 dans `failing_dimensions`.
- Tests régression : 21 nouveaux (TestWcagContrastHelpers 10 + TestFixPa11yContrast 10 + sous-ensemble D6 routing). 3 tests existants mis à jour (mapping figé étendu + coverage gap utilise désormais D5/D7/D9 puisque D6 est couvert).
- Limites assumées : couvre uniquement WCAG2AA.Principle1.Guideline1_4.1_4_3.G18 (contraste texte), pas alt/ARIA/focus. CSS variables `--color-*` non couvertes (P8.6.2 follow-up si besoin).
- Commit `43def6d` (3 fichiers, 626+/6-). 539/539 tests Python verts. ruff + format + mypy + pre-commit clean.
- Effort réel ~2h30 (investigation 30 min + helpers + fixer 1h + 21 tests 45 min + fix régressions + ROADMAP 15 min).

### 2026-05-17 — Audit public Mark Systems (codex)
- Cible : `https://www.marksystems.ca/` + source locale `/home/gear-code/02_projects/mark-systems-site/web-version`.
- Résultats : Lighthouse `performance 94`, `accessibility 91`, `best-practices 100`, `seo 100`; build Next PASS; Vitest `34/34`.
- Blocages : pa11y `12` erreurs WCAG (6 contrastes `text-txt-tertiary`, 6 liens icône sans nom accessible), `npm audit` = `1 critical`, `8 high`, `5 moderate`, `1 low`.
- Conformité : headers prod solides (CSP/HSTS/XFO/nosniff/referrer/permissions), privacy + mentions légales publiques présentes; source locale fourni ne correspond pas exactement au déploiement public observé.
- Dette NEXOS découverte : `tools/preflight.sh` casse l'écriture `npm-audit.json` après `cd "$SITE_DIR"` avec un `TOOLING_DIR` relatif. Ajouté en P9/D7.

### 2026-05-16 — P8.3 résolu : dimension-scoped auto-fix on plateau (claude, mode rigoureux)
- Cause racine identifiée : P8.2 surfaçait `PlateauDiagnosis.failing_dimensions` mais le signal alimentait UNIQUEMENT le prompt LLM enrichi. Aucun fixer déterministe NEXOS n'était déclenché — alors qu'on a déjà 5 fixers D4 (sécurité) et 3 fixers D8 (Loi 25) qui pourraient corriger en quelques millisecondes ce que le LLM doit réécrire sur plateau.
- Design proposé + validé utilisateur sur 3 carrefours architecturaux (3 AskUserQuestion) :
  - A1 : champ `dimension: str` sur `Fixer` (vs sous-package nexos/fixers/ ou dict externe) — `FIXER_ORDER` reste source de vérité unique, invariants P8.1 préservés par construction
  - C1 : hook `on_enriched_retry` dans `PhaseIterator` (vs étendre signature RerunCallback) — SOIC reste pur, NEXOS branche son auto-fixer via callback boundary
  - Mécanisme seul, pas de nouveaux fixers spéculatifs D1/D3/D5/D6/D7/D9 — couverture étendue uniquement si plateaux terrain le justifient (P8.5+)
- Implémentation 4 commits atomiques :
  - `9830c0d` `feat(auto-fixer): add dimension field to Fixer + fixers_for_dimensions()` — mapping figé D2/D4/D8 + 11 tests (TestFixerDimensions)
  - `527c670` `feat(auto-fixer): support dimensions= filter in auto_fix()` — param `dimensions: Iterable[str] | None = None`, `None` rétrocompat P8.1 + 7 tests (TestAutoFixDimensions)
  - `9b9e123` côté `soic_v3` : `feat(iterator): on_enriched_retry hook` — type alias `EnrichedRetryHook`, hook appelé après `diagnose_plateau()` avant `rerun_phase()`. `225a6b6` côté nexos : 5 tests + fix mypy annotation
  - `a457b3e` `feat(orchestrator): wire dimension-scoped auto_fix on SOIC plateau` — nouveau module `orchestrator/plateau_recovery.py` (149 lignes) avec factory `make_plateau_auto_fix_hook(...)`. Captures via args explicites (pas de closure trap B023). 6 tests (TestPlateauHookDefensive + TestPlateauHookHappyPath). Seuil `phases.py` 620 → 640 justifié.
- Branches défensives implémentées et toutes testées : `site_dir is None`, `failing_dimensions=()`, dimensions non couvertes (D1/D3/D5/D6/D7/D9) → log `coverage_gap`, happy path D4+D8
- 518/518 tests Python verts (489 baseline + 29 P8.3), ruff + format + mypy clean
- Modularité strictement préservée : `orchestrator/plateau_recovery.py` = module dédié unit-testable, couplage `soic/ → ∅` maintenu (zéro import nexos côté SOIC)
- Effort réel ~3h (design + investigation 45 min, 4 commits + tests 2h, ROADMAP 15 min)

### 2026-05-15 — P8.2 résolu : ENRICHED_RETRY + PlateauDiagnosis (claude)
- Cause racine identifiée : `Converger.decide()` retournait `ABORT_PLATEAU` direct dès détection plateau (2 deltas mu ≤ 0 + fail count non décroissant), sans diagnostic ni 2e chance. NEXOS abandonnait silencieusement collectif-nova et vertex-pmo.
- Décision Codex-aligned (`019e2baf`) : pas de switch model, instrumentation + 1 enriched retry informationnel
- Nouveau `Decision.ENRICHED_RETRY` + dataclass `PlateauDiagnosis` (trajectoire mu/fail, failing_dimensions, failing_assertions[FailingAssertion]) + flag `_enriched_retry_used` ré-armé par `reset()`
- `FeedbackRouter.generate_with_plateau_context()` produit un préfixe markdown explicite devant le feedback corrective standard
- `PhaseIterator` + `SOICIterator` handle `ENRICHED_RETRY` en enrichissant le feedback sans break le loop. Re-plateau → ABORT_PLATEAU pour de vrai
- 7 nouveaux tests régression + mise à jour test plateau existant (1er plateau = ENRICHED_RETRY)
- Commit `550631c` côté `soic_v3` (3 fichiers, 225+/38-)
- 489/489 tests Python verts, ruff clean
- Effort réel ~1h45 vs estimé 2-4h

### 2026-05-15 — P8.1 résolu : FIXER_ORDER + idempotence auto_fixer (claude)
- Refactor post-codex challenge (`019e2baf`) : pas de Protocol+toposort (rejeté ceremony), simple `FIXER_ORDER: list[Fixer]` linéaire avec dépendances commentées + tests d'invariants
- `Fixer` dataclass frozen (`name`, `target`, `apply`) — file-ownership de chaque fixer est métadonnée explicite, plus implicite
- Adapters lambda uniformisent signature `(site_dir, brief, report)` sans toucher les `_fix_*` (résolution tardive Python → monkeypatching préservé)
- `auto_fix()` : 9 lignes codées en dur → boucle `for fixer in FIXER_ORDER`
- 14 nouveaux tests : `TestFixerOrder` (ordre + immutabilité + file-ownership vercel.json) + `TestIdempotence` (run 3× = bit-identique, headers/CSP/CookieConsent/poweredByHeader pas de doublon)
- 482/482 tests Python verts, ruff clean
- Effort réel ~45 min vs estimé 1-2h

### 2026-05-15 — P4 + P5 + P6 résolus mode autonome (claude session continue)
**Mode** : Autonome qualité-first sur instruction explicite utilisateur ("fait tout, ne pose pas de questions, code de la meilleure qualité"). Règle absolue git push respectée.

**Travail effectué — 14 commits atomiques sur main** :
- P4b : 7 commits clients (CSP/headers propagation) — beaumont/clinique-aura/collectif-nova/electro-maitre/mark_systems_demo/table-de-marguerite/vertex-pmo
- P4d : 1 commit `df3a3fd` — hardening 5 tools/*.sh selon pattern osiris-scan.sh
- P4a : 1 commit `a85e71d` — `_fix_csp_middleware` + 11 tests
- P4e : 1 commit `19f6e00` — `nexos doctor --all-clients` + 10 tests
- P4c : 1 commit `4781539` — 57 tests Vitest (schemas/promotions/email/clientConfig/produits/horaires)
- P5  : 1 commit — 12 tests API contact + newsletter integration
- P6  : 1 commit `921d8c9` — log 2 silent excepts init (finit P2)

**Audit post-P4 conduit** :
- ✅ 0 TODOs/FIXMEs/HACK dans le code
- ✅ Headers sécurité 100% cohérents 8 clients (7 headers identiques)
- ✅ Loi 25 components présents tous clients (cookie/privacy/legal)
- ⚠ 2 silent excepts init identifiés → résolus en P6
- ⚠ API handlers PII/consent non testés → résolus en P5
- ✅ mypy clean, ruff clean, type coverage > 60%

**Métriques finales** :
- 464/464 tests Python (423 baseline + 21 P3 + 10 P4a + 10 P4e)
- 70/70 tests Vitest depanneur-nobert (13 baseline + 45 P4c + 12 P5)
- 13 commits locaux pré-session (P1+P2+P3+docs) + 14 commits session = 27 non poussés total
- Backup `~/backups/nexos_v.3.0/2026-05-15_*_P3_ports.tar.gz` + nouveau backup post-P6 prévu

**Pattern méthodo retenu** : audit ciblé après chaque batch de fixes révèle plus de dette que prévu. Item P4 a généré P5 + P6. Pattern à reproduire : code → tests → audit → docs → commit, en cycle.

### 2026-05-15 — P3 résolu : zone ports interdite, helper port_allocator (claude session continue)
- Cause racine identifiée : `socket.bind(("", 0))` dans `orchestrator/preflight.py::_find_free_port` retombe dans 32768-60999 (zone éphémère kernel, interdite par `~/.claude/CLAUDE.md` user)
- Décision validée en début de session : Option B (helper Python + wrapper bash), pas un simple patch in-place
- `nexos/port_allocator.py` créé : 12 sous-blocs constants nommés (NEXOS_TESTS/ENGINE/SCRAPING/CYBERSEC/BUFFER + GENESIS + GENCORE + SAAS + CYBERSEC_LABS + AUDIT_TOOLKIT + GLOBAL_BUFFER), `FORBIDDEN_RANGES` validé au load (0-1023, 32768-60999), `allocate_port` séquentiel premier libre, `purge_subblock` SIGTERM 100% explicite, `is_port_free` via socket.bind
- `tools/alloc-port.sh` créé : wrapper bash JSON-parsable, `--list`, `--purge`, `--help`, exit codes 0-4, inputs via env vars (safe shell injection)
- `orchestrator/preflight.py::_find_free_port` délégué à `allocate_port(NEXOS_ENGINE)` ; saturé → say red + skip preflight + hint `--purge`
- 21 tests régression dans `tests/test_port_allocator.py` dont garde-fou constantes + ancre contrat preflight P3 = NEXOS_ENGINE
- Documentation : section "Allocation des ports" dans `docs/runbook.md` (usage Python + CLI + incidents + diagnostic)
- 444/444 tests Python verts, ruff check + format clean

### 2026-05-15 — P2 résolu : audit silent failure paths (claude session continue)
- Bug ROADMAP « exit 1 silencieux » non reproductible — déjà résolu par effet de bord (probable : `cc30880` Claude OAuth fix, `f0b861b` rate-limit retry, ou `48f71c4` no-timeout doc)
- Audit défensif ciblé : 9 patterns « silent failure » examinés sur chaîne audit (auto-fix → preflight → audit_toolkit → build_prompt → cli_runner)
- 3 bugs latents identifiés et fixés (`a92adb8`) — chaque `except Exception: pass` sans log remplacé par `say([yellow]⚠ ... — fallback ...)` :
  - `phases.py:66` PipelineConfig → PHASES_MAP
  - `prompts.py:257` AgentRegistry → prompt sans agents
  - `prompts.py:316` intake directive → prompt sans cadrage
- 5 patterns examinés et acceptés (cli_runner return 1 avec say, verify.py return False avec say, auto_fixer except spécifiques, etc.)
- 1 amélioration suggérée mais skip (preflight Next server stderr=DEVNULL → log file) — yak shaving sans bug réel
- 423/423 tests verts, ruff clean

### 2026-05-15 — P1 résolu : divergence agent Ph5 vs SOIC (claude session continue)
- Cause racine identifiée : agent calcule sa propre grille D1-D9 indépendamment de SOIC GateEngine déterministe (qui pilote déjà `Converger.decide()` + `deploy-master`)
- Décision documentée dans `CLAUDE.md` : SOIC = source de vérité unique
- Module `orchestrator/score_injection.py` créé : substitue 5 placeholders (`[[SOIC_MU]]`, `[[SOIC_VERDICT]]`, `[[SOIC_THRESHOLD]]`, `[[SOIC_DIM_SCORES_TABLE]]`, `[[SOIC_D1]]`..`[[SOIC_D9]]`) avec valeurs lues depuis `soic-gates.json` + `soic-runs.jsonl`. Idempotent, tolère JSON corrompu.
- 10 tests régression `tests/test_score_injection.py` (dont `test_report_mu_matches_gates_mu_exactly` ancre concrète depanneur-nobert 9.10925 → "9.11")
- Agent Ph5 orchestrator instruit de ne plus calculer μ (nouvelle section "Scoring — SOIC = source de vérité unique")
- Branchement post-SOIC dans `phases.py:run_pipeline` entre `save_gate_history` et `run_reconciliation_step`
- pyproject.toml : `tests/* per-file-ignores += RUF001` (cohérent avec `orchestrator/*`)
- 423/423 tests verts, ruff check + format all clean

### 2026-05-15 — Doctor + audit dette + codification discipline (claude)
- 16 commits nexos_v.3.0 + 1 commit soic_v3
- Audit dette : 13 items, 8 réels, 5 faux positifs ou cosmétiques
- Découvertes : item N (divergence Ph5/SOIC), crash audit, port hors zone
- Fix racine osiris-scan.sh JSON cassé attrapé en passant
- Mode `nexos doctor --client` ajouté
- depanneur-nobert : 34 → 0 erreurs WCAG AA contraste (palette `text.muted` corrigé), 0 → 13 tests Vitest
- **ROADMAP.md créé** (commit `7413158`) comme doc de continuité multi-CLI
- **Discipline session codifiée** dans CLAUDE.md / AGENTS.md / GEMINI.md (commit `a59f5a4`) avec autorité équivalente aux règles absolues
- Préflight pa11y → `a11y.json` fixé (mismatch silencieux découvert en re-validant les fixes contraste)
- Conclusion méthodologique : la dette réelle est d'**intégrité** (pipeline qui ment), pas de structure. Item N reste P1 pour prochaine session.

### Sessions antérieures (extraites CHANGELOG.md)
- 2026-05-13 — Chantier 4 dette pipeline (11 items, tag v4.3.0)
- 2026-05-10 — Chantier mode B (depanneur-nobert end-to-end μ Ph5=9.47)
- 2026-04-15 — Chantier maintenance + upgrade (17 phases, v4.2.0)

---

## 🧭 Préparation détaillée — P8.4 + B2.1 (terrain prêt 2026-05-18)

> Point d'entrée pour la prochaine session Claude/Codex/Gemini. Lire cette section
> AVANT de coder. Aliases shell prêts : `P8.4`, `nexos-attack --help`.

### ✅ B2 — CVE HIGH next-intl + postcss (RÉSOLU 2026-05-18)

Voir entrée historique 2026-05-18. Pilote `56c8320` + batch `46e93fa`. 6 clients alignés sur next 15.5.18 / next-intl 4.12.0 / postcss 8.5.10. vertex-pmo μ 9.00 → 9.10.

### 🟠 B2.1 — mark_systems_demo : 1 HIGH CVE next 16.2.3 résiduel (~1-2h)

**Découvert** : pendant batch B2, `mark_systems_demo` était hors scope car déjà sur next 16.2.3 (plus récent que cible 15.5.18). `npm audit` montre 1 HIGH CVE (advisories GHSA-* sur next 16.x : DoS Server Components, Middleware bypass, XSS App Router, etc.). `npm audit fix` ne propose pas de fix automatique.

**2 stratégies possibles** :
- **Aligner vers 16.x patchée** : trouver la dernière 16.x sans CVE (probablement 16.3.x ou 16.4.x si publiée). Reste sur next 16, demande update de `params: Promise<>` si l'API change.
- **Downgrade vers 15.5.18** : aligne sur le reste du stack NEXOS. Plus simple, mais c'est un downgrade qui peut casser des features 16.x (Cache Components, etc.).

**Pré-requis avant d'attaquer** : check si mark_systems_demo a un site/ utilisable (cf `nexos doctor --client mark_systems_demo`) et identifier les usages spécifiques next 16 (Cache Components, segments, etc.).

---

### 🟣 P8.4 — Onboard 6 clients dormants (N3 par client, ~3-6h par session)

**Périmètre** : 6 clients avec brief OK mais sans site (pipeline jamais exécuté ou
échec silencieux). Aliases shell : `P8.4`.

**Liste exacte** (vérifier au démarrage avec `nexos doctor --all-clients`) :
```
iusine                    brief=ok site=missing
jokeresthetique           brief=missing → exclure ou créer brief
la-villa-du-sous-marin    brief=ok site=missing (1 gate présente)
l-usine-rh                brief=ok site=missing
l-usinerh                 brief=ok site=missing
nexos-platform-industrial brief=missing → exclure
usine-rh                  brief=ok site=missing
```

**Décision stratégique** : prioriser les 5 qui ont un brief (iusine, la-villa-du-sous-marin, l-usine-rh, l-usinerh, usine-rh). Les 2 sans brief (jokeresthetique, nexos-platform-industrial) demandent une discussion utilisateur avant — sont-ils encore actifs ou archives ?

**Plan d'attaque tungsten — 1 client à la fois** :
1. **Avant** (par client) :
   - Snapshot `clients/<slug>/brief-client.json` (vérifier validité schéma)
   - Lire `clients/<slug>/nexos-changelog.json` si présent (peut révéler pourquoi le pipeline a échoué la dernière fois)
   - Estimer coût LLM : pipeline complet 6 phases × codex = 50-200k tokens par client (selon complexité brief)
2. **Pendant** (par client) :
   - `nexos create --client-dir clients/<slug>` (timeout étendu, ~10-30 min par phase)
   - Surveiller les phases : PH0 discovery → PH1 strategy → PH2 design → PH3 content → PH4 build → PH5 QA+deploy
   - Si phase échoue : capturer `failing_dimensions` via SOIC, voir si fixer existe (P8.3 routing), sinon noter le gap
3. **Après** (par client) :
   - `nexos doctor --client <slug>` détaillé
   - μ doit être ≥ 8.5 avec decision=ACCEPT pour client READY
   - Si plateau persistant → analyser via `soic-runs.jsonl` les dimensions stagnantes
   - **Commit atomique par client**
   - ROADMAP update incrémentale (nombre de dormants restants)
   - **Check-in user obligatoire après chaque client** (N3 × N clients)

**Critères d'acceptance par client** :
- [ ] Site built (`npm run build` PASS)
- [ ] SOIC μ ≥ 8.5 ACCEPT
- [ ] Tooling complet (`tools/preflight.sh` produit 6 JSON valides)
- [ ] Pages légales Loi 25 présentes (privacy + mentions + cookie consent)

**Items P8.4 doublons potentiels** (à investiguer dès le démarrage) : `l-usine-rh`, `l-usinerh`, `usine-rh`, `USINE_RH_industrielle` — quatre slugs très proches. Vérifier avec user : ce sont 4 clients différents ou 4 itérations d'un même client à dédupliquer ? Si dédup, P8.4 = en réalité 3 clients (iusine + la-villa + 1 usine-rh consolidé) → effort réduit.

**Risque coût LLM** : si tous les 5-6 clients tournent à 200k tokens chacun = 1-1.2M tokens total. À budgéter avec user avant de démarrer la session.

---

## 🎯 Pour la session prochaine — recommandation finale

**P1 + P2 + P3 + P4 + P5 + P6 résolus 2026-05-15.** Toute la dette identifiée + 2 items P5/P6 dégagés à l'audit sont clos. Pipeline NEXOS production-ready autonome avec :
- Score Ph5 déterministe via SOIC (P1)
- 5 silent failure paths nettoyés (P2 + P6)
- Allocation ports conforme convention machine (P3)
- 8 sites clients alignés sécurité + Loi 25 (P4b)
- Tooling scripts robustes (P4d)
- CSP single source vercel.json + middleware dev (P4a)
- Tests coverage Vitest x5 (P4c + P5)
- Doctor multi-clients (P4e)
- 464/464 Python + 70/70 Vitest verts

**Critère "qualité code maximale" atteint** sur le scope identifié. Prochaines pistes possibles si nouvelle session :

1. **Propagation tests Vitest 7 autres clients** (~2h) — répliquer les 70 tests depanneur-nobert sur beaumont/clinique-aura/etc. Effort élevé, valeur défensive long-terme.
2. **next-intl + postcss breaking upgrade** (~30 min, risque moyen) — fixer les CVE HIGH npm audit sur tous les clients via `npm audit fix --force` (next 15.5.18 / next-intl 4.12.0). Nécessite re-tester chaque site.
3. **Type hint coverage push 80%** (~1h) — actuellement >60%, polish.
4. **CI GitHub Actions** — déjà partiellement présent, vérifier robustesse + ajouter Vitest aux jobs.
5. **Réveil d'un client dormant** (iusine, jokeresthetique, nexos-platform-industrial, etc. — ont brief mais pas de site/) — lancer `nexos create --client-dir clients/<slug>` pour générer leur site.

**Critère "session prochaine = succès"** :
- Identifier une priorité concrète dans la liste ci-dessus (ou découverte fraîche via `nexos doctor --all-clients`)
- Cycle code → tests → audit → docs → commits atomiques maintenu
- 0 push autonome — utilisateur valide explicitement
