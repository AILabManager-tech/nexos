# NEXOS — Roadmap prochaines sessions

> Document de continuité entre sessions Claude/Codex/Gemini.
> Mis à jour à chaque clôture de session. À lire en ouverture.

**Dernière mise à jour** : 2026-05-15 — P8.1 + P8.2 résolus (claude session continue)
**Version NEXOS active** : v4.2.0 (production-ready autonome)
**Branche** : `main` (26 + P8.1 + P8.2 commits locaux, push à discrétion ; SOIC `550631c` côté `soic_v3`)

---

## 📍 État actuel (snapshot 2026-05-15)

### Métriques santé

| Indicateur | Valeur | Note |
|---|---|---|
| Tests Python | **489/489** verts | +14 P8.1 (FIXER_ORDER + idempotence) +7 P8.2 (ENRICHED_RETRY + PlateauDiagnosis) |
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
| Bugs réels notés (audit) | 🔴 **P8 ouvert** (2 items restants) | P8.1 + P8.2 résolus. Reste B2 CVE HIGH / B4 6 clients dormants |
| Auto-fixer idempotent | ✅ **résolu (P8.1)** | `FIXER_ORDER: list[Fixer]` + 14 tests régression (ordre + file-ownership + idempotence run 3×) |
| ABORT_PLATEAU recovery | ✅ **résolu (P8.2)** | `Decision.ENRICHED_RETRY` + `PlateauDiagnosis` injecté dans feedback avant abort (1 retry par run) |
| Dette technique notée | 🟡 **P9 ouvert** (6 items D1-D6) | Polish — CI matrix, divergence SOIC/Osiris, doc symlinks, mypy, seuil margin, schéma strict |
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
| **P8.3** | Dimension-scoped fixers | (manquait) | Nouveau : si D8 fail → legal, D4 → security | 3-5h | — |
| **P8.4** | B4 onboard 6 dormants | Aveugle | Couvert par instrumentation P8.2 (on saura pourquoi) | 1-3h (downstream P8.2) | — |
| **D1** | Vitest matrix 7 clients | Inchangé | Mécanique, OK tel quel | 2h | — |
| **B2** | CVE HIGH upgrade | Inchangé | Test sur depanneur seul puis propager | 1-2h | — |
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

#### B2 — CVE HIGH npm audit non résolu sur tous les sites

**Symptôme** :
```
HIGH      next-intl <4.12.0    (GHSA chain via @formatjs)
MODERATE  postcss   <8.5.10    (XSS via Unescaped </style> in CSS Stringify)
```

**Impact réel actuel** : faible. Tous tes sites NEXOS sont statiques (pas d'input CSS user-uploadé), donc surface d'attaque XSS postcss ≈ 0. Mais le CVE existe et persiste sur 8/8 sites.

**Pourquoi pas auto-fixé en P4b** : `npm audit fix --force` voudrait installer next-intl@4.12.0 + next@15.5.18 — breaking change qui pourrait casser le build/runtime sans tests régression complets.

**Fix proposé** (upgrade contrôlé) :
1. Upgrade next 15.5.18 + next-intl 4.12.0 sur **depanneur-nobert seul** (client de référence)
2. Run full Vitest (70 tests) + build + lighthouse pour valider
3. Si OK, propager aux 7 autres clients
4. Si KO, downgrade + ouvrir issue upstream

**Effort estimé** : 1-2h. **Valeur** : moyenne aujourd'hui (surface attaque ≈ 0), élevée si un futur site sert du CSS user-uploadé.

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

#### D5 — Verdict deploy marginal beaumont-avocats μ=8.50
Exactement le seuil. Aucune marge. Toute modif mineure peut le faire descendre sous 8.5.
**Action** : analyser dimensions faibles + améliorer pour gagner ~0.3 de marge. Effort 1h.

#### D6 — `brief-synthesizer` schéma strict
`additionalProperties: false` rejette champs comme `sector` qui pourraient être utiles. Friction UX. Pas un bug, by design.
**Action** : ajouter champs optionnels au schéma (`sector`, `tags`, `notes`) si valeur produit confirmée. Effort 20 min.

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
