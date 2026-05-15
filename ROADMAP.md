# NEXOS — Roadmap prochaines sessions

> Document de continuité entre sessions Claude/Codex/Gemini.
> Mis à jour à chaque clôture de session. À lire en ouverture.

**Dernière mise à jour** : 2026-05-15 — P1 (Item N) résolu (claude session continue)
**Version NEXOS active** : v4.2.0 (production-ready autonome)
**Branche** : `main` (3 commits locaux pré-P1 + commits P1 à venir — à push manuellement)

---

## 📍 État actuel (snapshot 2026-05-15)

### Métriques santé

| Indicateur | Valeur | Note |
|---|---|---|
| Tests Python | **423/423** verts | +10 tests `test_score_injection.py` (P1) |
| Tests Vitest depanneur-nobert | **13/13** verts | seed initial posé |
| Build site depanneur-nobert | **PASS** | npm audit 0/0 |
| Lighthouse depanneur-nobert | a11y 100, perf 92, BP 96, SEO 92 | mesures empiriques |
| Pa11y depanneur-nobert | **0 erreurs** | vs 34 contraste avant fix |
| Clients actifs | 18 total · 8 complets brief+gates+site | cf `nexos doctor` |
| Pipeline NEXOS complet | OK pour `create` · 🔴 **`audit` cassé** (cf P2) | |
| Divergence agent Ph5 / SOIC | ✅ **résolue (P1)** | SOIC = source de vérité unique via placeholders |

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

### 🟠 P2 — Crash `nexos audit` exit 1 silencieux

**Découvert** : 2026-05-15 en relançant Ph5 sur depanneur-nobert
**Status** : mode `audit` cassé pour TOUS les clients

**Symptôme**
```bash
$ python3 nexos_cli.py audit --client-dir clients/depanneur-nobert --url ...
# preflight ✓, puis exit 1 sans stack trace visible (stderr supprimé qq part)
```

**Pourquoi c'est P2** : un des 7 modes officiels de NEXOS (`create`, `audit`, `modify`, `content`, `analyze`, `knowledge`, `converge`) n'est plus fonctionnel. Si l'utilisateur veut auditer un site existant sans relancer toute la création, il doit contourner manuellement (preflight + lecture artefacts).

**Plan d'investigation**
1. Re-lancer `nexos audit` au **foreground** (pas en background) avec `2>&1 | tee` pour capturer toute la stack
2. Si stderr toujours supprimé, instrumenter ponctuellement `orchestrator/phases.py` avec un try/except global
3. Probablement dans l'invocation subprocess de claude CLI (cf `nexos/session_launcher.py:425` — pas de timeout par design mais peut crasher si claude refuse)
4. Vérifier que l'auto-fix appelé au début de Ph5 (`phases.py:122-129`) ne plante pas

**Critère de succès**
- `nexos audit --client-dir clients/depanneur-nobert` termine sans erreur
- Soit le mode produit un verdict Ph5 + écrit soic-gates, soit il documente clairement pourquoi il abort
- Test e2e ajouté

**Fichiers à toucher (probables)**
- `orchestrator/phases.py` (audit dispatch + invocation Ph5)
- `nexos/session_launcher.py` (subprocess claude)
- `tests/test_e2e_orchestrator.py` (couverture audit mode)

**Effort estimé** : 30-60 min

---

### 🟡 P3 — NEXOS utilise des ports dans la zone éphémère interdite

**Découvert** : 2026-05-15 lors du tooling preflight
**Status** : viole la règle d'allocation `CLAUDE.md` user

**Symptôme** : NEXOS a démarré un serveur Next.js sur **port 55191**. Cette plage (32768-60999) est explicitement **interdite** par `~/.claude/CLAUDE.md` user (zone éphémère kernel). La zone allouée pour NEXOS est **20000-20999** (sous-bloc engine : 20100-20199).

**Pourquoi c'est P3** : ça fonctionne (pas de crash) mais viole une convention machine documentée. Risque de collision avec d'autres process système, et incohérence avec les ports utilisés manuellement (20000-20099 pour tests éphémères).

**Plan**
1. Identifier le code NEXOS qui démarre le serveur Next pour preflight → `orchestrator/preflight.py:135` (subprocess Popen `npx next start -p $port`)
2. Voir comment le port est pioché (probablement random ou auto via Next)
3. Forcer un picker dans 20100-20199 avec retry sur conflit
4. Si possible créer un helper `tools/alloc-port.sh` qui implémente l'algo défini dans CLAUDE.md user (premier libre dans sous-bloc, purge cyclique si plein)

**Critère de succès**
- Pipeline preflight démarre toujours dans 20100-20199
- Erreur explicite si toute la zone est saturée
- Documentation mise à jour dans `docs/runbook.md`

**Fichiers à toucher**
- `orchestrator/preflight.py`
- Nouveau : `tools/alloc-port.sh` (selon design CLAUDE.md user)
- Tests : couverture range port

**Effort estimé** : 30 min (sans alloc-port.sh) · 1h30 (avec alloc-port.sh générique)

---

### 🟢 P4 — Polish (à faire après P1+P2+P3)

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

**P1 résolu 2026-05-15.** Le verdict deploy/no-deploy s'appuie désormais sur SOIC déterministe via placeholders, sans divergence possible avec l'agent.

**Prochain focus : P2 (crash `nexos audit` exit 1 silencieux).** 30-60 min. Sans ça, impossible d'auditer un site existant sans relancer toute la création, ce qui bloque la propagation des fixes aux 17 autres clients (P4b).

Une fois P2 réparé : P3 (zone ports) reste rapide (30 min), puis P4 (polish) en priorisant P4b propagation 17 clients (maintenant safe avec P1 résolu).

P3 (ports) peut attendre — c'est moins urgent, c'est de la conformité de convention.

P4 (polish) : pas avant que P1+P2 soient clos.

**Critère de "session prochaine = succès"** :
- P1 résolu : décision documentée sur source de vérité Ph5
- Tests régression couvrant le cas divergence
- ROADMAP.md mis à jour (P1 marqué clos, nouveaux items s'il y en a)
- 0 push autonome — utilisateur valide explicitement
