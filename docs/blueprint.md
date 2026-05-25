# NEXOS v3.0 — BLUEPRINT ARCHITECTURE

```
PROJET    : NEXOS v3.0 — Web Builder Autonome Premium
AUTEUR    : Claude Opus 4.6 × Gear-code
DATE      : 2026-02-14
STATUT    : Blueprint pré-implémentation
OBJECTIF  : Score audit ≥ 85/100 dès la première génération
```

---

## 1. PHILOSOPHIE

NEXOS v2 = **1 appel CLI, 1 session, 6 phases dans le même contexte**.
Résultat : 60/100.

NEXOS v3.0 = **N appels ciblés, tooling réel pré/post, quality gates SOIC entre chaque phase**.
Cible : ≥85/100 au premier run.

### Principes fondateurs

| # | Principe | Conséquence |
|---|----------|-------------|
| 1 | **Mesurer avant de juger** | Tooling CLI réel (Lighthouse, testssl, curl, npm audit, pa11y) AVANT l'agent LLM |
| 2 | **Un agent = un domaine** | Pas de "site-auditor" omniscient. 22+ agents spécialisés |
| 3 | **Gate-keep entre phases** | SOIC μ ≥ 8.0 requis pour passer à la phase suivante |
| 4 | **Session courte, contexte riche** | Chaque phase = 1 appel CLI dédié avec le feed des phases précédentes |
| 5 | **Zéro estimation** | Remplacer "~2.5s LCP estimé" par la mesure Lighthouse réelle |

---

## 2. ARCHITECTURE GLOBALE

```
┌──────────────────────────────────────────────────────────────────┐
│                      NEXOS v3.0 ORCHESTRATOR                     │
│                    orchestrator.py (Python 3.12)                  │
├──────────┬──────────┬──────────┬──────────┬──────────┬──────────┤
│  PHASE 0 │ PHASE 1  │ PHASE 2  │ PHASE 3  │ PHASE 4  │ PHASE 5  │
│ DISCOVERY│ STRATEGY │ DESIGN   │ CONTENT  │ BUILD    │ QA+DEPLOY│
│ 6 agents │ 5 agents │ 5 agents │ 5 agents │ 5 agents │ 22+agents│
│          │          │          │          │          │ + TOOLING │
├──────────┴──────────┴──────────┴──────────┴──────────┴──────────┤
│                    QUALITY GATES (SOIC v3.0)                     │
│            μ = mean(D1..D9) — Gate ≥ 8.0 entre phases            │
├─────────────────────────────────────────────────────────────────-┤
│                    TOOLING LAYER (CLI natif)                     │
│  lighthouse · testssl.sh · curl · npm audit · pa11y · osiris     │
├──────────────────────────────────────────────────────────────────┤
│                    RUNTIME                                        │
│  Claude Code CLI (Pro Max OAuth) — --dangerously-skip-permissions │
└──────────────────────────────────────────────────────────────────┘
```

---

## 3. ARBORESCENCE CIBLE

```
~/nexos/
├── CLAUDE.md                        # Manifest — source de vérité
├── .mcp.json                        # Serveurs MCP actifs
├── orchestrator.py                  # Orchestrateur maître (multi-phase)
├── nexos.py                         # GUI launcher (PyQt6 / Rich TUI)
│
├── agents/                          # 48 agents spécialisés
│   ├── ph0-discovery/               # Phase 0 — Analyse sectorielle
│   │   ├── _orchestrator.md
│   │   ├── web-scout.md             # Scraping concurrence (WebFetch)
│   │   ├── tech-inspector.md        # Stack detector
│   │   ├── ux-analyst.md            # UX patterns benchmark
│   │   ├── content-evaluator.md     # Audit contenu existant
│   │   └── design-critic.md         # Benchmark design
│   │
│   ├── ph1-strategy/                # Phase 1 — Architecture stratégique
│   │   ├── _orchestrator.md
│   │   ├── brand-strategist.md
│   │   ├── information-architect.md
│   │   ├── seo-strategist.md
│   │   ├── solution-architect.md     # Stack selection + justification
│   │   └── scaffold-planner.md       # Plan de fichiers
│   │
│   ├── ph2-design/                  # Phase 2 — Design system
│   │   ├── _orchestrator.md
│   │   ├── design-system-architect.md # Palette, typo, spacing
│   │   ├── layout-designer.md        # Wireframes textuels
│   │   ├── interaction-designer.md   # Animations, transitions
│   │   ├── responsive-specialist.md
│   │   └── asset-director.md         # Images, icônes, favicons
│   │
│   ├── ph3-content/                 # Phase 3 — Rédaction
│   │   ├── _orchestrator.md
│   │   ├── copywriter-principal.md
│   │   ├── seo-copywriter.md
│   │   ├── content-architect.md      # Structure des messages i18n
│   │   ├── translator.md             # FR → EN (+ autres)
│   │   └── content-reviewer.md       # Gate-keeper contenu
│   │
│   ├── ph4-build/                   # Phase 4 — Génération de code
│   │   ├── _orchestrator.md
│   │   ├── project-bootstrapper.md   # npx create-next-app + config
│   │   ├── component-builder.md      # Composants React/Tailwind
│   │   ├── page-assembler.md         # Assembly pages + layouts
│   │   ├── integration-engineer.md   # API routes, chatbot, forms
│   │   └── build-validator.md        # Gate-keeper build (tsc, vitest)
│   │
│   ├── ph5-qa/                      # Phase 5 — QA exhaustive (22+ agents)
│   │   ├── _orchestrator.md          # Coordonne l'audit final
│   │   │
│   │   │# ── Audit Performance ──
│   │   ├── lighthouse-runner.md      # Exécute lighthouse CLI réel
│   │   ├── bundle-analyzer.md        # Analyse taille chunks
│   │   ├── image-optimizer.md        # Scan images (format, poids, alt)
│   │   ├── css-purger.md             # CSS inutilisé
│   │   ├── cache-strategy.md         # Headers cache
│   │   │
│   │   │# ── Audit Sécurité ──
│   │   ├── security-headers.md       # Vérifie via curl -I réel
│   │   ├── ssl-auditor.md            # testssl.sh ou équivalent
│   │   ├── xss-scanner.md            # dangerouslySetInnerHTML, sanitisation
│   │   ├── dep-vulnerability.md      # npm audit
│   │   ├── csp-generator.md          # Génère CSP + vercel.json
│   │   │
│   │   │# ── Audit SEO ──
│   │   ├── seo-meta-auditor.md       # Title, desc, OG, canonical, hreflang
│   │   ├── jsonld-generator.md       # Structured data
│   │   ├── sitemap-validator.md      # Cohérence sitemap/robots
│   │   ├── broken-link-checker.md    # Liens internes + externes
│   │   │
│   │   │# ── Audit Accessibilité ──
│   │   ├── a11y-auditor.md           # pa11y wrapper + WCAG 2.2
│   │   ├── color-contrast-fixer.md   # Ratios AA/AAA
│   │   ├── keyboard-nav-tester.md    # Tab order, skip-links, focus
│   │   │
│   │   │# ── Audit Code ──
│   │   ├── test-coverage-gap.md      # Fichiers non testés
│   │   ├── typo-fixer.md             # Orthographe FR/EN
│   │   │
│   │   │# ── Audit Conformité ──
│   │   ├── legal-compliance.md       # Loi 25 QC, RGPD, mentions légales
│   │   │
│   │   │# ── Gate-keepers ──
│   │   ├── deploy-master.md          # Déploiement Vercel
│   │   └── visual-qa.md              # Rapport final consolidé
│   │
│   └── site-update/                 # Pipeline modification (inchangé)
│       ├── _pipeline.md
│       ├── repo-manager.md
│       ├── site-auditor.md           # Appelle ph5-qa en sous-traitance
│       ├── site-modifier.md
│       ├── qa-reviewer.md
│       └── deployer.md
│
├── tools/                           # Tooling CLI pré-agent
│   ├── preflight.sh                 # Script maître pré-audit
│   ├── lighthouse-scan.sh           # lighthouse $URL --output json
│   ├── headers-scan.sh              # curl -sI $URL → JSON
│   ├── ssl-scan.sh                  # testssl.sh --json $URL
│   ├── a11y-scan.sh                 # pa11y $URL --reporter json
│   ├── deps-scan.sh                 # npm audit --json
│   ├── osiris-scan.sh               # python ../../osiris/scanner.py $URL (sibling)
│   └── parse-results.py             # Agrège tous les JSON → feed agent
│
├── soic/                            # Moteur SOIC v3.0 intégré
│   ├── gate.py                      # Quality gate entre phases
│   ├── dimensions.py                # 9 dimensions + calcul μ
│   ├── evaluate.py                  # Évaluation objective (tool-verified)
│   └── report.py                    # Rapport SOIC JSON/Markdown
│
├── templates/                       # Templates & références
│   ├── brief-intake.md              # Formulaire brief client
│   ├── brief-schema.json            # Schéma JSON du brief
│   ├── audit-template.md            # Template rapport audit 12 sections
│   ├── next-config.template.mjs     # Config Next.js sécurisée par défaut
│   ├── vercel-headers.template.json # Headers sécu + cache complets
│   ├── tailwind.template.config.ts  # Tailwind avec design tokens
│   └── tsconfig.template.json       # TypeScript strict
│
├── _toolbox/                        # Bibliothèque de référence (read-only)
│   ├── 01_next_templates/           # 12 configs
│   ├── 02_ui_components/            # 26 composants
│   ├── 03_tailwind_configs/         # Configs TW
│   ├── 04_hooks/                    # 6 hooks custom
│   ├── 05_utils/                    # 14 utilitaires TS
│   ├── 06_agents/                   # Agents de référence
│   ├── 09_animations/               # Keyframes, Aurora, Parallax
│   ├── 11_stores/                   # Patterns Zustand
│   ├── 12_services/                 # storage, export
│   └── 13_references/               # Code source mark-systems (i18n 10 langues)
│
├── clients/                         # Dossiers projet par client
│   └── {slug}/
│       ├── brief-client.json
│       ├── ph0-discovery-report.md
│       ├── ph1-strategy-report.md
│       ├── ph2-design-report.md
│       ├── ph3-content-report.md
│       ├── ph4-build-log.md
│       ├── ph5-qa-report.md
│       ├── soic-gates.json          # Historique des gates
│       ├── tooling/                 # Résultats bruts des outils
│       │   ├── lighthouse.json
│       │   ├── headers.json
│       │   ├── npm-audit.json
│       │   ├── pa11y.json
│       │   └── osiris.json
│       └── site/                    # Code source généré (le livrable)
│           └── ...
│
├── logs/                            # Logs horodatés
├── docs/                            # Documentation
│   ├── architecture.md
│   └── web-orchestrator.md
│
└── soic -> ../soic_v3                       # Symlink relatif vers soic_v3 sibling
                                              # (osiris résolu via sibling auto-détecté
                                              # par tools/osiris-scan.sh, pas de symlink)
```

---

## 4. ORCHESTRATEUR v3.0 — FLUX D'EXÉCUTION

### 4.1 Mode CREATE (nouveau site)

```
┌─────────────────────────────────────────────────────────────┐
│ 1. BRIEF INTAKE                                              │
│    GUI/TUI → brief-client.json                               │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PHASE 0 — DISCOVERY (1 appel CLI dédié)                   │
│    ┌─ web-scout → scrape 5 concurrents (WebFetch)            │
│    ├─ tech-inspector → identifier stacks concurrence         │
│    ├─ ux-analyst → benchmark UX patterns                     │
│    ├─ content-evaluator → analyser contenu existant (si migr)│
│    └─ design-critic → benchmark design                       │
│    OUTPUT → ph0-discovery-report.md                          │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ ★ SOIC GATE 0→1 : μ(discovery) ≥ 7.0                        │
│   D1=Complétude données, D2=Sources vérifiables,             │
│   D3=Analyse concurrentielle, D4=Insights actionnables       │
│   FAIL → re-run ph0 avec feedback                            │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PHASE 1 — STRATEGY (1 appel CLI, feed: ph0 report)       │
│    ┌─ brand-strategist → positionnement, voix, palette       │
│    ├─ information-architect → IA, navigation, routes         │
│    ├─ seo-strategist → mots-clés, meta, structured data     │
│    ├─ solution-architect → stack (Next.js 15+, deps)         │
│    └─ scaffold-planner → arbre de fichiers complet           │
│    OUTPUT → ph1-strategy-report.md + scaffold-plan.json      │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ ★ SOIC GATE 1→2 : μ(strategy) ≥ 8.0                         │
│   D1=Architecture cohérente, D2=SEO plan complet,            │
│   D3=Stack justifiée, D4=Scaffold réaliste                   │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. PHASE 2 — DESIGN (1 appel CLI, feed: ph0+ph1)            │
│    ┌─ design-system-architect → tokens, palette, typo        │
│    ├─ layout-designer → wireframes textuels par page         │
│    ├─ interaction-designer → animations, transitions         │
│    ├─ responsive-specialist → breakpoints strategy           │
│    └─ asset-director → plan images, icônes, favicons         │
│    OUTPUT → ph2-design-report.md + design-tokens.json        │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ ★ SOIC GATE 2→3 : μ(design) ≥ 8.0                           │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. PHASE 3 — CONTENT (1 appel CLI, feed: ph0+ph1+ph2)       │
│    ┌─ copywriter-principal → rédaction FR                    │
│    ├─ seo-copywriter → optimisation SEO in-text              │
│    ├─ content-architect → structure messages/fr.json          │
│    ├─ translator → FR → EN (+ autres locales)                │
│    └─ content-reviewer → GATE qualité éditoriale             │
│    OUTPUT → messages/{locale}.json + contenu validé          │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ ★ SOIC GATE 3→4 : μ(content) ≥ 8.0                          │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. PHASE 4 — BUILD (1 appel CLI, feed: scaffold + design     │
│    + content)                                                 │
│    ┌─ project-bootstrapper → npx create-next-app + configs   │
│    │   (next.config, tailwind, tsconfig, vercel.json headers) │
│    ├─ component-builder → composants React + Tailwind        │
│    ├─ page-assembler → pages, layouts, routes                │
│    ├─ integration-engineer → API routes, chatbot, forms      │
│    └─ build-validator → tsc --noEmit + npm run build         │
│    OUTPUT → site/ complet + ph4-build-log.md                 │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ ★ SOIC GATE 4→5 : BUILD PASS (0 erreurs tsc, build OK)      │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. TOOLING PREFLIGHT (Python — AUCUN LLM)                    │
│    ┌─ npm audit --json → deps-scan                           │
│    ├─ lighthouse $URL --output json → perf/a11y/seo/bp       │
│    ├─ curl -sI $URL → headers HTTP bruts                     │
│    ├─ pa11y $URL --reporter json → accessibilité WCAG        │
│    ├─ testssl.sh $URL --json → SSL/TLS grade                 │
│    └─ osiris-scanner → sobriété web score                    │
│    OUTPUT → clients/{slug}/tooling/*.json                    │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ 8. PHASE 5 — QA EXHAUSTIVE (22+ agents, feed: tooling réel) │
│    Chaque agent reçoit les JSON de tooling + le code source  │
│    ┌─ PERF: lighthouse-runner, bundle-analyzer, image-opt,   │
│    │        css-purger, cache-strategy                        │
│    ├─ SÉCU: security-headers, ssl-auditor, xss-scanner,      │
│    │        dep-vulnerability, csp-generator                  │
│    ├─ SEO:  seo-meta-auditor, jsonld-generator,              │
│    │        sitemap-validator, broken-link-checker            │
│    ├─ A11Y: a11y-auditor, color-contrast-fixer,              │
│    │        keyboard-nav-tester                               │
│    ├─ CODE: test-coverage-gap, typo-fixer                    │
│    ├─ LEGAL: legal-compliance (Loi 25, RGPD)                 │
│    └─ GATE: visual-qa (consolidation rapport final)          │
│                                                               │
│    OUTPUT → ph5-qa-report.md (12 sections, score /100)       │
└────────────────────┬────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────────────┐
│ ★ SOIC GATE FINALE : μ(QA) ≥ 8.5                            │
│   PASS → deploy-master (vercel --prod)                       │
│   FAIL → boucle corrective automatique (max 3 itérations)   │
│          orchestrator identifie dimensions faibles,           │
│          re-lance les agents concernés avec correctifs        │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Boucle corrective SOIC

```python
# Pseudo-code de la boucle corrective
for iteration in range(1, MAX_ITER + 1):
    scores = run_phase5_qa(client_dir)
    mu = mean(scores.values())

    if mu >= 8.5:
        deploy(client_dir)
        break

    # Identifier les 3 dimensions les plus faibles
    weak = sorted(scores.items(), key=lambda x: x[1])[:3]

    for dim, score in weak:
        agent = DIMENSION_TO_AGENT[dim]
        # Re-lance uniquement l'agent ciblé avec feedback
        run_agent(agent, feedback=f"Score {dim}={score}. Corrections requises.")

    # Re-run tooling après corrections
    run_preflight_tooling(client_dir)
```

### 4.3 Mode AUDIT (site existant)

```
Brief (URL + scope) → TOOLING PREFLIGHT → PHASE 5 QA (22 agents)
                                         → rapport 12 sections
```

**Différence avec v2** : L'audit reçoit les **mesures réelles** des outils CLI, pas des estimations LLM.

### 4.4 Mode MODIFY (modification ciblée)

```
Brief (repo + changements) → repo-manager (clone)
                           → site-auditor (appelle ph5-qa)
                           → site-modifier (applique changements)
                           → qa-reviewer (re-audit ciblé)
                           → deployer
```

---

## 5. ORCHESTRATEUR PYTHON — CHANGEMENTS MAJEURS vs v2

### 5.1 Multi-appel au lieu de mono-appel

```python
# v2 : UN appel pour tout
cmd = ["claude", "--dangerously-skip-permissions", "-p", MEGA_PROMPT]

# v3 : UN appel PAR PHASE avec contexte cumulatif
for phase in ["ph0", "ph1", "ph2", "ph3", "ph4"]:
    prompt = build_phase_prompt(phase, client_dir)
    result = run_claude_cli(prompt, cwd=client_dir)
    save_phase_output(phase, result, client_dir)

    gate_score = run_soic_gate(phase, client_dir)
    if gate_score < GATE_THRESHOLD[phase]:
        handle_gate_failure(phase, gate_score, client_dir)
```

### 5.2 Tooling layer intégré

```python
# Nouveau dans v3 : exécution d'outils CLI natifs
def run_preflight_tooling(client_dir: Path, url: str):
    """Exécute les outils de mesure AVANT les agents LLM."""
    tooling_dir = client_dir / "tooling"
    tooling_dir.mkdir(exist_ok=True)

    tools = [
        ("lighthouse", f"lighthouse {url} --output json --output-path {tooling_dir}/lighthouse.json --chrome-flags='--headless --no-sandbox'"),
        ("headers",    f"curl -sI {url} | python tools/parse-headers.py > {tooling_dir}/headers.json"),
        ("npm-audit",  f"cd {client_dir}/site && npm audit --json > {tooling_dir}/npm-audit.json"),
        ("pa11y",      f"pa11y {url} --reporter json > {tooling_dir}/pa11y.json"),
        ("osiris",     f"python ~/osiris-scanner/scanner.py {url} --format json > {tooling_dir}/osiris.json"),
    ]

    for name, cmd in tools:
        try:
            subprocess.run(cmd, shell=True, timeout=60, capture_output=True)
            console.print(f"  [green]✓[/] {name}")
        except Exception as e:
            console.print(f"  [yellow]⚠[/] {name}: {e}")
```

### 5.3 Prompt builder enrichi

```python
def build_phase_prompt(phase: str, client_dir: Path) -> str:
    """Construit le prompt pour une phase avec TOUT le contexte nécessaire."""
    parts = []

    # 1. Agent directive
    agent_path = NEXOS_ROOT / f"agents/{phase}/_orchestrator.md"
    parts.append(f"Lis {agent_path} et adopte le rôle d'orchestrateur {phase}.")

    # 2. Brief client
    brief_path = client_dir / "brief-client.json"
    parts.append(f"Le brief client est dans {brief_path}. Lis-le.")

    # 3. Feed des phases précédentes (contexte cumulatif)
    for prev_phase in get_previous_phases(phase):
        report = client_dir / f"{prev_phase}-report.md"
        if report.exists():
            parts.append(f"Le rapport de {prev_phase} est dans {report}. Lis-le pour le contexte.")

    # 4. Tooling data (pour ph5 uniquement)
    if phase == "ph5-qa":
        tooling_dir = client_dir / "tooling"
        if tooling_dir.exists():
            parts.append(f"Les résultats de tooling réel sont dans {tooling_dir}/. "
                        f"Lis CHAQUE fichier JSON. Ce sont des MESURES RÉELLES, "
                        f"pas des estimations. Base ton audit sur ces données.")

    # 5. Output path
    output = client_dir / f"{phase}-report.md"
    parts.append(f"Écris ton rapport dans {output}")

    return "\n".join(parts)
```

---

## 6. AGENTS — PROVENANCE & ADAPTATIONS

### 6.1 Matrice de sourcing

| Phase | Agent | Source | Adaptation requise |
|-------|-------|--------|--------------------|
| **ph0** | web-scout | NEXOS v2 | Aucune |
| **ph0** | tech-inspector | NEXOS v2 | Aucune |
| **ph0** | ux-analyst | NEXOS v2 | Aucune |
| **ph0** | content-evaluator | NEXOS v2 | Aucune |
| **ph0** | design-critic | NEXOS v2 | Aucune |
| **ph1** | brand-strategist | NEXOS v2 | Aucune |
| **ph1** | information-architect | NEXOS v2 | Aucune |
| **ph1** | seo-strategist | NEXOS v2 | Aucune |
| **ph1** | solution-architect | NEXOS v2 | Forcer Next.js 15+ par défaut |
| **ph1** | scaffold-planner | NEXOS v2 | Output JSON strict |
| **ph2** | design-system-architect | NEXOS v2 | Intégrer _toolbox/03_tailwind |
| **ph2** | layout-designer | NEXOS v2 | Aucune |
| **ph2** | interaction-designer | NEXOS v2 | Utiliser _toolbox/09_animations |
| **ph2** | responsive-specialist | NEXOS v2 | Aucune |
| **ph2** | asset-director | NEXOS v2 | Aucune |
| **ph3** | copywriter-principal | NEXOS v2 | Aucune |
| **ph3** | seo-copywriter | NEXOS v2 | Aucune |
| **ph3** | content-architect | NEXOS v2 | Aucune |
| **ph3** | translator | NEXOS v2 | Aucune |
| **ph3** | content-reviewer | NEXOS v2 | Aucune |
| **ph4** | project-bootstrapper | NEXOS v2 | **Majeur** — intégrer templates sécurisés |
| **ph4** | component-builder | NEXOS v2 | Utiliser _toolbox/02_ui_components |
| **ph4** | page-assembler | NEXOS v2 | Aucune |
| **ph4** | integration-engineer | NEXOS v2 | Aucune |
| **ph4** | build-validator | NEXOS v2 | Aucune |
| **ph5** | lighthouse-runner | **WinterPulse** | Adapter de JO → générique |
| **ph5** | bundle-analyzer | **WinterPulse** | Adapter de JO → générique |
| **ph5** | image-optimizer | **WinterPulse** | Aucune |
| **ph5** | css-purger | **WinterPulse** | Aucune |
| **ph5** | cache-strategy | **WinterPulse** | Aucune |
| **ph5** | security-headers | **WinterPulse** (csp-header) | **Majeur** — alimenter par curl réel |
| **ph5** | ssl-auditor | **Nouveau** | Créer — wrapper testssl.sh |
| **ph5** | xss-scanner | **WinterPulse** | Aucune |
| **ph5** | dep-vulnerability | **WinterPulse** | Aucune |
| **ph5** | csp-generator | **WinterPulse** | Aucune |
| **ph5** | seo-meta-auditor | **WinterPulse** | Aucune |
| **ph5** | jsonld-generator | **WinterPulse** | Aucune |
| **ph5** | sitemap-validator | **WinterPulse** (enricher) | Renommer + adapter |
| **ph5** | broken-link-checker | **WinterPulse** | Aucune |
| **ph5** | a11y-auditor | **WinterPulse** | **Majeur** — alimenter par pa11y réel |
| **ph5** | color-contrast-fixer | **WinterPulse** | Aucune |
| **ph5** | keyboard-nav-tester | **WinterPulse** | Aucune |
| **ph5** | test-coverage-gap | **WinterPulse** | Aucune |
| **ph5** | typo-fixer | **WinterPulse** | Aucune |
| **ph5** | legal-compliance | **Nouveau** | Créer — Loi 25 QC + RGPD |
| **ph5** | deploy-master | NEXOS v2 | Aucune |
| **ph5** | visual-qa | NEXOS v2 | **Majeur** — consolidateur rapport 12 sections |

### 6.2 Résumé sourcing

| Source | Agents repris | Adaptations majeures |
|--------|---------------|----------------------|
| NEXOS v2 (ph0-ph4) | 25 | 2 (bootstrapper, scaffold) |
| WinterPulse audit | 17 | 3 (headers, a11y, lighthouse) |
| Nouveau | 2 | ssl-auditor, legal-compliance |
| **TOTAL** | **44** | 7 à modifier |

---

## 7. TEMPLATES SÉCURISÉS PAR DÉFAUT

### 7.1 next.config.template.mjs

L'erreur de Émilie Poirier (0 headers sécu) ne se reproduira jamais :

```javascript
// Chaque site NEXOS v3.0 part avec ces headers
const securityHeaders = [
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
  // CSP généré dynamiquement par csp-generator agent
];
```

### 7.2 vercel.json template

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
        { "key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()" }
      ]
    },
    {
      "source": "/_next/static/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

### 7.3 Checklist bootstrapper

Le `project-bootstrapper` agent DOIT vérifier avant de passer :

```markdown
## Checklist Bootstrap (Gate Ph4 entry)
- [ ] Next.js ≥ 15.0 (pas de version avec CVE connues)
- [ ] TypeScript strict mode
- [ ] Tailwind v4 ou v3.4+
- [ ] vercel.json avec TOUS les headers sécu
- [ ] next.config avec poweredByHeader: false
- [ ] .gitignore complet
- [ ] Politique de confidentialité placeholder
- [ ] Mentions légales placeholder
- [ ] Bandeau cookie/consentement composant
- [ ] DOMPurify installé si chatbot prévu
- [ ] Rate limiting middleware si API routes prévues
```

---

## 8. SOIC v3.0 — QUALITY GATES

### 8.1 Dimensions par mode

| Dimension | CREATE | AUDIT | Description |
|-----------|--------|-------|-------------|
| D1 | Architecture / Modularité | idem | Structure fichiers, séparation concerns |
| D2 | Documentation | idem | CLAUDE.md, README, commentaires |
| D3 | Tests | idem | Couverture, qualité assertions |
| D4 | Sécurité | idem | Headers, XSS, CVE, CSRF |
| D5 | Performance | idem | CWV, bundle, cache, images |
| D6 | Accessibilité | idem | WCAG 2.2 AA, contraste, clavier |
| D7 | SEO | idem | Meta, structured data, sitemap |
| D8 | Conformité légale | idem | Loi 25, RGPD, mentions |
| D9 | Code Quality | idem | TypeScript strict, linting, conventions |

### 8.2 Évaluation objective (tool-verified)

```python
# SOIC v3.0 : scores basés sur des MESURES, pas des jugements LLM
def evaluate_from_tooling(tooling_dir: Path) -> dict[str, float]:
    scores = {}

    # D5 Performance — basé sur Lighthouse réel
    lh = json.load(open(tooling_dir / "lighthouse.json"))
    scores["D5"] = lh["categories"]["performance"]["score"] * 10

    # D6 Accessibilité — basé sur pa11y réel
    pa11y = json.load(open(tooling_dir / "pa11y.json"))
    errors = len([i for i in pa11y if i["type"] == "error"])
    scores["D6"] = max(0, 10 - errors * 0.5)  # -0.5 par erreur WCAG

    # D4 Sécurité — basé sur headers réels
    headers = json.load(open(tooling_dir / "headers.json"))
    required = ["x-content-type-options", "x-frame-options",
                "referrer-policy", "permissions-policy",
                "strict-transport-security", "content-security-policy"]
    present = sum(1 for h in required if h in headers)
    scores["D4_headers"] = (present / len(required)) * 10

    # D4 Sécurité — basé sur npm audit réel
    audit = json.load(open(tooling_dir / "npm-audit.json"))
    high_vulns = audit.get("metadata", {}).get("vulnerabilities", {}).get("high", 0)
    scores["D4_deps"] = max(0, 10 - high_vulns * 2)

    scores["D4"] = (scores["D4_headers"] + scores["D4_deps"]) / 2

    # D7 SEO — basé sur Lighthouse SEO
    scores["D7"] = lh["categories"]["seo"]["score"] * 10

    return scores
```

### 8.3 Seuils de gate

| Transition | Seuil μ | Conséquence si FAIL |
|------------|---------|---------------------|
| ph0 → ph1 | ≥ 7.0 | Re-run ph0 avec feedback |
| ph1 → ph2 | ≥ 8.0 | Re-run ph1 |
| ph2 → ph3 | ≥ 8.0 | Re-run ph2 |
| ph3 → ph4 | ≥ 8.0 | Re-run ph3 |
| ph4 → tooling | BUILD PASS | Fix build errors |
| tooling → ph5 | Automatique | Toujours passer |
| ph5 → deploy | ≥ 8.5 | Boucle corrective (max 3 iter) |

---

## 9. DÉPENDANCES CLI À INSTALLER

```bash
# Tooling QA (sur la machine de développement)
npm install -g lighthouse         # Performance + SEO + A11Y + BP
npm install -g pa11y              # Accessibilité WCAG
pip install osiris-scanner        # Ou symlink existant

# Optionnel mais recommandé
sudo apt install testssl.sh       # Audit SSL/TLS
npm install -g broken-link-checker # Liens cassés

# Déjà installé (vérifié)
# claude (Claude Code CLI — Pro Max OAuth)
# node 20+ / npm
# python 3.12
# curl
# git
```

---

## 10. PLAN D'IMPLÉMENTATION

### Phase A — Fondations (jour 1-2)

| # | Tâche | Effort | Bloquant ? |
|---|-------|--------|------------|
| A1 | Créer `~/nexos/` avec arborescence complète | 15 min | Oui |
| A2 | Copier les 25 agents ph0-ph4 depuis nexos-v2 | 10 min | Oui |
| A3 | Adapter + copier les 17 agents WinterPulse → ph5-qa | 2h | Oui |
| A4 | Créer 2 agents manquants (ssl-auditor, legal-compliance) | 1h | Oui |
| A5 | Écrire `orchestrator.py` v3 (multi-phase + gates) | 3h | Oui |
| A6 | Écrire les scripts `tools/*.sh` (preflight tooling) | 1h | Oui |
| A7 | Écrire `soic/gate.py` + `soic/evaluate.py` | 2h | Oui |
| A8 | Copier `_toolbox/` depuis WinterPulse | 15 min | Non |
| A9 | Créer templates sécurisés (next.config, vercel.json, etc.) | 1h | Oui |
| A10 | Écrire CLAUDE.md v3 (manifest complet) | 1h | Oui |

### Phase B — Intégration (jour 3-4)

| # | Tâche | Effort |
|---|-------|--------|
| B1 | Adapter `nexos.py` GUI pour le nouveau workflow | 2h |
| B2 | Tester mode CREATE sur un brief fictif | 2h |
| B3 | Tester mode AUDIT sur winterpulse.club | 1h |
| B4 | Calibrer les seuils SOIC sur 3 sites réels | 2h |
| B5 | Installer tooling CLI manquant (lighthouse, pa11y) | 30 min |

### Phase C — Validation (jour 5)

| # | Tâche | Effort |
|---|-------|--------|
| C1 | Générer un site complet avec NEXOS v3 | 4h |
| C2 | Auditer le résultat avec NEXOS v3 mode audit | 30 min |
| C3 | Comparer score vs l'audit Émilie Poirier (60/100) | 30 min |
| C4 | Documenter les leçons apprises | 1h |

**Effort total estimé : ~20-25 heures**

---

## 11. CE QUI N'EST PAS DANS v3.0 (SCOPE EXPLICITE)

| Hors scope | Raison |
|------------|--------|
| AINOVA_BRAIN intégré directement | Complexité disproportionnée. SOIC gate.py suffit. |
| ToT explorer | Pas nécessaire pour du web building |
| 13 agents Python AINOVA | Overkill — les agents .md via Claude Code sont plus flexibles |
| MCP servers complets | 11/16 non fonctionnels. Ne pas importer de dette technique. |
| Docker/Kubernetes | NEXOS est un outil local, pas un service cloud |
| PostgreSQL/pgvector | Pas de BDD nécessaire pour du web building |

**Philosophie** : Prendre le **concept** de SOIC (quality gates objectifs) et les **agents spécialisés** de WinterPulse, sans importer la complexité infra d'AINOVA OS.

---

## 12. MÉTRIQUES DE SUCCÈS

| Métrique | v2 (actuel) | v3 (cible) |
|----------|-------------|------------|
| Score audit premier run | 60/100 | ≥ 85/100 |
| Headers sécu présents | 1/10 | 10/10 |
| CVE HIGH dans deps | 4 | 0 |
| Conformité légale | 20/100 | ≥ 80/100 |
| Accessibilité WCAG | 62/100 | ≥ 80/100 |
| SEO score | 52/100 | ≥ 85/100 |
| Temps total création | ~8 min | ~25-40 min (qualité > vitesse) |
| Données mesurées vs estimées | 0% | ≥ 60% |

---

*Blueprint NEXOS v3.0 — 2026-02-14*
*Prêt pour implémentation Phase A.*
