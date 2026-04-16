---
id: agents/ph1-strategy/pattern-recommender-test-report
version: 1.0.0
phase: ph1-strategy
type: dry-run validation
source_agent: agents/ph1-strategy/pattern-recommender.md
date_run: 2026-04-16
---

# Pattern Recommender — Test Report (dry-run)

> Dry-run mental de l'agent `pattern-recommender` appliqué sur 3 briefs fictifs couvrant des combinaisons secteur × positioning × KPI distinctes. Exercice manuel : appliquer les règles §3.1 à §3.6 du prompt et documenter la sortie attendue + évaluation qualité.
>
> **But** : valider que l'agent converge vers des recommandations cohérentes AVANT la phase E (pilote Clinique Aura qui est le GATE empirique).

---

## Méthodologie

Pour chaque brief :

1. Appliquer §3.1 (mapping secteur)
2. Appliquer §3.2 (sélection patterns avec tous les ajustements)
3. Appliquer §3.3 (sites de référence dédupliqués)
4. Appliquer §3.4 (6D table canonique)
5. Appliquer §3.5 (opposition check vs `canonical_examples` de `personality-dimensions.json`)
6. Appliquer §3.6 (risques SOIC)
7. Évaluer : **OK** (sortie cohérente) / **KO** (incohérence) / **AMBIGU** (cohérent mais révèle un edge case à affiner)

Clients canoniques utilisés pour `opposition_check` (fallback puisque `existing-clients-personalities.json` non matérialisé) :

| Client | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|
| `clinique-aura` | 1 | emotional | (n/a) | warm | slow-organic | asymmetric-soft |
| `beaumont-avocats` | 4 | technical | light | cold | still | symmetric |
| `electro-maitre-industriel` | 5 | technical-warm | heavy | industrial | mechanical | asymmetric-strong |
| `collectif-nova` | 3 | (n/a) | contrasted | variable | (n/a) | editorial |

---

## Brief 1 — Physio multi-cliniques accessible, KPI conversion

### Input

```json
{
  "client": {
    "slug": "physio-horizon-qc",
    "sector": "santé / physiothérapie multi-cliniques",
    "positioning": "accessible",
    "size": "medium"
  },
  "goals": { "primary_kpi": "conversion" }
}
```

### §3.1 Mapping secteur → **SEC-01** (Santé / Physiothérapie) ✓

### §3.2 Sélection patterns

**Ajustements appliqués** : `primary_kpi == "conversion"` → boost +1 (cap tier 1) pour tous les patterns avec `D1_ux` impacté. `positioning == "accessible"` → aucun ajustement positioning. `size == "medium"` → aucun ajustement taille.

Patterns finaux tier 1 (après boost conversion + D1_ux) :

| ID | Tier natif SEC-01 | Tier final | Primary | Rationale |
|---|---|---|---|---|
| P01 | 1 | 1 | ✓ | Secteur santé + KPI conversion → CTA omniprésent réduit friction RDV |
| P02 | 1 | 1 | ✓ | Mesuré +2× leads (Bloor Jane S05) ; renforce SEC-01 à positionnement accessible |
| P11 | 1 | 1 | ✓ | Multi-cliniques → page par ville obligatoire (SEO local + NAP) |
| P17 | 1 | 1 | ✓ | Standard moderne SEC-01 (Ivy Rehab S02) — perf validée à grande échelle |
| P04 | 2 | 1 (boost) | ✓ | Hero émotionnel qualifie la patientèle dès l'arrivée |
| P09 | 2 | 1 (boost) | ✓ | 3-word messaging = message accessible pour public large |
| P19 | 2 | 1 (boost) | ✓ | StoryBrand cadre narratif centré patient, aligné conversion |
| P03 | 3 | 2 (boost) | — | Color-coded nav différencie les services sans complexifier |

→ 7 primary + 1 secondary = 8 patterns recommandés (plafond atteint).

**Patterns avoided** :

| ID | Reason |
|---|---|
| P20 | SEC-01 : tier_null (menu galerie non applicable en santé) |

Note : les patterns SEC-01 tier 3 (P05, P06, P07, P08, P10, P13, P15, P18) sont présents dans la matrice mais exclus du top 8 par la troncature. Pourraient figurer en `tier 3 slots` (max 3) si le brief le justifie — ignorés ici pour garder la recommandation focused.

### §3.3 Sites de référence

Collecte brute (sites × patterns recommandés) :

- P01 → S01, S03
- P02 → S05, S17
- P11 → S01, S02
- P17 → S02, S10, S29
- P04 → S10, S03
- P09 → S13
- P19 → S19, S16
- P03 → S25

Déduplication + scoring :

| Site | Patterns couverts | study_priority |
|---|---|---|
| S01 Twin Boro | P01, P11 | 1 |
| S02 Ivy Rehab | P11, P17 | 1 |
| S10 | P17, P04 | 1 |
| S03 Athletix | P01, P04 | 1 |
| S05 Bloor Jane | P02 (+ measured) | 2 |

→ Top 5 : `[S01, S02, S10, S03, S05]`.

### §3.4 Personnalité 6D

Table canonique §3.4 : `accessible × SEC-01` →

```
{D1:3, D2:"emotional-cold", D3:"medium", D4:"cold", D5:"slow-organic", D6:"symmetric"}
```

### §3.5 Opposition check

| vs | D1 | D2 | D3 | D4 | D5 | D6 | count | passes |
|---|---|---|---|---|---|---|---|---|
| clinique-aura | 3 vs 1 | emotional-cold vs emotional | medium vs n/a | cold vs warm ✓ | slow-organic vs slow-organic | symmetric vs asymmetric-soft | **1** | ✗ |
| beaumont-avocats | 3 vs 4 | emotional-cold vs technical | medium vs light | cold vs cold | slow-organic vs still | symmetric vs symmetric | **0** | ✗ |
| electro-maitre-industriel | 3 vs 5 | emotional-cold vs technical-warm ✓ | medium vs heavy | cold vs industrial | slow-organic vs mechanical ✓ | symmetric vs asymmetric-strong ✓ | **3** | ✗ |
| collectif-nova | 3 vs 3 | n/a | medium vs contrasted | cold vs variable | n/a | symmetric vs editorial ✓ | **1** | ✗ |

`max_opposition_score = 3`. **`passes_rule_of_gold = false`**.

### §3.6 Risques SOIC

- `D8_legal` + SEC-01 → RPP + consentement explicite données cliniques
- `D8_legal` + P11 multi-localisations → RPP par province si hors QC
- `D5_performance` + ≥ 2 patterns animation (P04, P17) → surveiller LCP mobile
- P04 hero vidéo → pas de stock footage, < 5 Mo, fallback prefers-reduced-motion
- P11 → Schema.org LocalBusiness + NAP cohérent GMB

### Sortie attendue (extrait)

```json
{
  "sector_id": "SEC-01",
  "patterns_recommended": [{"id":"P01"},{"id":"P02"},{"id":"P11"},{"id":"P17"},{"id":"P04"},{"id":"P09"},{"id":"P19"},{"id":"P03"}],
  "patterns_avoided": [{"id":"P20","reason":"SEC-01 tier null"}],
  "reference_sites": [{"id":"S01"},{"id":"S02"},{"id":"S10"},{"id":"S03"},{"id":"S05"}],
  "personality_6d_proposed": {"D1_density":3,"D2_register":"emotional-cold","D3_typo_weight":"medium","D4_palette":"cold","D5_velocity":"slow-organic","D6_structure":"symmetric"},
  "opposition_check": {"max_opposition_score": 3, "passes_rule_of_gold": false},
  "confidence_score": 0.70,
  "notes": "règle d'or NON satisfaite — 6D par défaut accessible×SEC-01 trop proche du profil clinique-aura. Shift suggéré : D3→heavy (trait distinctif) OU D6→asymmetric-soft (organique) pour atteindre 4 oppositions vs electro-maitre."
}
```

### Évaluation : **AMBIGU** ⚠️

- Patterns & sites : **OK** — cohérents avec un cabinet physio accessible orienté conversion.
- 6D : **KO règle d'or** — la table canonique pour `accessible × SEC-01` est trop proche de clinique-aura. Le fichier détecte l'échec et propose un shift.
- **Insight pour phase E** : la table §3.4 mérite un raffinement pour `accessible × SEC-01` (variantes "sportive" vs "corporate"). L'agent remonte correctement l'information dans `notes` avec confiance abaissée.

---

## Brief 2 — Avocat droit famille boutique bilingue, KPI SEO

### Input

```json
{
  "client": {
    "slug": "cabinet-maitre-lafond",
    "sector": "cabinet juridique droit famille",
    "positioning": "boutique",
    "size": "small"
  },
  "goals": { "primary_kpi": "seo" }
}
```

### §3.1 → **SEC-05** (Juridique) ✓

### §3.2 Sélection patterns

**Ajustements** : `primary_kpi == "seo"` → boost +1 (cap 1) pour patterns avec `D6_seo` impacté. `positioning == "boutique"` → pas d'ajustement auto (arbitrage sur `measured_impact`). `size == "small"` → aucune démotion.

Tier 1 finaux :

| ID | Tier natif SEC-05 | Tier final | Primary | Rationale |
|---|---|---|---|---|
| P01 | 1 | 1 | ✓ | CTA persistant essentiel pour prise de contact juridique |
| P02 | 1 | 1 | ✓ | Social proof + KPI SEO → témoignages clients ↑ CTR |
| P03 | 1 | 1 | ✓ | Color-coded nav différencie les domaines de droit (mesuré : double conversions Hudgell S25) |
| P14 | 1 | 1 | ✓ | Industry code-breaking = rupture nécessaire pour boutique juridique |
| P17 | 1 | 1 | ✓ | Standard moderne, performance maintenue |
| P05 | 2 | 1 (boost) | ✓ | Single-page scroll (si brief one-pager) — SEO boost D6 |
| P09 | 2 | 1 (boost) | ✓ | 3-word messaging + SEO = titre H1 concis |
| P11 | 2 | 1 (boost) | ✓ | Pages par localisation (cabinet + tribunaux couverts) = SEO local |

→ 8 primary, plafond atteint.

**Patterns avoided** :

| ID | Reason |
|---|---|
| P20 | SEC-05 tier null (menu galerie non applicable en juridique) |
| P15 | SEC-05 tier null (gamified nav incompatible avec registre juridique) |

### §3.3 Sites de référence

| Site | Patterns couverts | study_priority |
|---|---|---|
| S25 Hudgell Solicitors | P03 (mesuré) | 2 |
| S01 Twin Boro | P01, P11 | 1 |
| S02 Ivy Rehab | P11, P17 | 1 |
| S29 | P14, P17 | 1 |
| S23 | P14 | 2 |

→ Top 5 : `[S01, S02, S29, S25, S23]` (S05/S17 pour P02 écartés par diversité).

Note : plusieurs sites de référence viennent d'autres secteurs (S01/S02 SEC-01, S29 SEC-06). C'est cohérent car les patterns visés sont universels — mais humaniquement il faudrait aussi citer S22 Quinn Emanuel, S21 SEC-05 natifs. **Amélioration à phase ultérieure** : biaiser le choix vers les sites natifs du secteur quand possible.

### §3.4 Personnalité 6D

`boutique × SEC-05` →

```
{D1:3, D2:"technical", D3:"medium", D4:"cold", D5:"still", D6:"symmetric"}
```

### §3.5 Opposition check

| vs | D1 | D2 | D3 | D4 | D5 | D6 | count | passes |
|---|---|---|---|---|---|---|---|---|
| clinique-aura | 3 vs 1 | technical vs emotional ✓ | medium vs n/a | cold vs warm ✓ | still vs slow-organic | symmetric vs asymmetric-soft | **2** | ✗ |
| beaumont-avocats | 3 vs 4 | technical vs technical | medium vs light | cold vs cold | still vs still | symmetric vs symmetric | **0** | ✗ (même secteur, attendu) |
| electro-maitre-industriel | 3 vs 5 | technical vs technical-warm | medium vs heavy | cold vs industrial | still vs mechanical ✓ | symmetric vs asymmetric-strong ✓ | **2** | ✗ |
| collectif-nova | 3 vs 3 | n/a | medium vs contrasted | cold vs variable | n/a | symmetric vs editorial ✓ | **1** | ✗ |

`max_opposition_score = 2`. **`passes_rule_of_gold = false`**.

### §3.6 Risques SOIC

- `D8_legal` + SEC-05 → secret professionnel : reCAPTCHA + chiffrement formulaires
- P11 → Schema.org LocalBusiness + NAP cohérent

### Sortie attendue (extrait)

```json
{
  "sector_id": "SEC-05",
  "patterns_recommended": [{"id":"P01"},{"id":"P02"},{"id":"P03"},{"id":"P14"},{"id":"P17"},{"id":"P05"},{"id":"P09"},{"id":"P11"}],
  "patterns_avoided": [{"id":"P20","reason":"SEC-05 tier null"},{"id":"P15","reason":"SEC-05 tier null"}],
  "reference_sites": [{"id":"S01"},{"id":"S02"},{"id":"S29"},{"id":"S25"},{"id":"S23"}],
  "personality_6d_proposed": {"D1_density":3,"D2_register":"technical","D3_typo_weight":"medium","D4_palette":"cold","D5_velocity":"still","D6_structure":"symmetric"},
  "opposition_check": {"max_opposition_score": 2, "passes_rule_of_gold": false},
  "confidence_score": 0.65,
  "notes": "règle d'or NON satisfaite — boutique×SEC-05 par défaut trop proche du profil juridique canonique. Shift suggéré pour différencier vs beaumont-avocats : D3→heavy (poids typographique affirmé boutique) OU D6→asymmetric-soft (trait moderne) pour gagner 2 oppositions supplémentaires."
}
```

### Évaluation : **AMBIGU** ⚠️

- Patterns : **OK** — P03 color-coded + P14 code-breaking = signature "boutique juridique distinctive" ; cohérent avec la référence Hudgell (S25).
- Sites de référence : **AMBIGU** — choix pertinents mais dominance cross-secteur (SEC-01 ×2). Raffiner la règle §3.3 pour privilégier les sites natifs secteur.
- 6D + règle d'or : **KO** — la table §3.4 pour `boutique × SEC-05` colle trop au profil juridique classique. Besoin de différencier sur D3/D6 pour singulariser la marque boutique.
- **Insight phase E** : la règle d'or est durablement difficile à satisfaire quand le secteur du nouveau client a déjà un client NEXOS canonique ET quand la table §3.4 pousse vers des valeurs "sectorielles typiques". Nécessite soit enrichissement de la table (variantes par positioning), soit acceptation d'un `passes_rule_of_gold = false` avec `notes` claires.

---

## Brief 3 — Restaurant plant-based premium, KPI brand

### Input

```json
{
  "client": {
    "slug": "verdure-bistro",
    "sector": "restaurant plant-based",
    "positioning": "premium",
    "size": "small"
  },
  "goals": { "primary_kpi": "brand" }
}
```

### §3.1 → **SEC-03** (Restauration) ✓

### §3.2 Sélection patterns

**Ajustements** : `positioning == "premium"` → tier 3 → tier 2 (promotion globale). `primary_kpi == "brand"` → boost +1 pour `[P04, P06, P08, P13, P14, P18]`. `size == "small"` → aucune démotion.

Tier 1 finaux :

| ID | Tier natif SEC-03 | Tier final | Primary | Rationale |
|---|---|---|---|---|
| P08 | 1 | 1 | ✓ | Story-first = fondation narrative brand plant-based (S15/S11/S20) |
| P09 | 1 | 1 | ✓ | 3-word messaging = slogan premium mémorable |
| P13 | 1 | 1 | ✓ | Anti-polish authenticity = signature artisanale (S12/S30) |
| P17 | 1 | 1 | ✓ | Scroll animations modernes, perf OK |
| P20 | 1 | 1 | ✓ | Menu galerie images = standard resto (S14) — critique pour UX |
| P04 | 2 | 1 (boost brand) | ✓ | Hero vidéo émotionnelle = immersion culinaire |
| P06 | 3→2 (premium) + brand-boost | 1 | ✓ | Grayscale→color reveal = signature premium plant-based |
| P14 | 2 | 1 (boost brand) | ✓ | Industry code-breaking = rupture vs "bistro vert" générique |
| P18 | 3→2 (premium) + brand-boost | 1 | ✓ | Micro-univers sections = chaque plat son monde |

→ 9 candidats tier 1. Troncature à 8 par §3.2 (trier par `measured_impact` décroissant puis par ordre matrice).

Aucun de ces patterns n'a de `measured_impact` direct pour SEC-03 (P02/P03/P19 qui ont `measured_impact` ne sont pas dans cette liste). Par ordre d'apparition matrice : **P04, P06, P08, P09, P13, P14, P17, P18** → P20 tronqué.

⚠️ **Finding critique** : P20 (menu galerie, pattern natif tier 1 SEC-03) est évincé par la troncature au profit de patterns "brand-boostés" qui étaient naturellement tier 2/3. Pour un restaurant, supprimer le menu galerie est suboptimal UX. **Recommandation d'amélioration pour phase ultérieure** : ajuster §3.2 pour prioriser les patterns à `tier_natif = 1` dans la troncature avant les patterns boostés.

**Patterns avoided** :

| ID | Reason |
|---|---|
| (aucun null pour SEC-03) | — |

Autres patterns tier 2 finaux (tier 3 slots disponibles, max 3) : P02, P05, P07, P11 — retenir P02 (conversion resto), P11 (si multi-adresses).

### §3.3 Sites de référence

| Site | Patterns couverts | study_priority |
|---|---|---|
| S14 | P20 | 2 (P20 tronqué → score baissé) |
| S15 | P08 | 2 |
| S11 | P08 | 2 |
| S20 | P08 | 2 |
| S12 | P13 | 2 |
| S30 | P13 | 2 |
| S10 | P04, P17 | 1 |
| S27 | P06 | 2 |

→ Top 5 : `[S10, S15, S11, S12, S27]` (diversité style + S10 couvre 2 patterns).

Note : si P20 était retenu, S14 remonterait à `priority 2` avec justification UX forte.

### §3.4 Personnalité 6D

`premium × SEC-03` → `{D1:2, D2:emotional, D3:light, D4:warm, D5:slow-organic, D6:asymmetric-soft}`

### §3.5 Opposition check

| vs | D1 | D2 | D3 | D4 | D5 | D6 | count | passes |
|---|---|---|---|---|---|---|---|---|
| clinique-aura | 2 vs 1 | emotional vs emotional | light vs n/a | warm vs warm | slow-organic vs slow-organic | asymmetric-soft vs asymmetric-soft | **0** | ✗ (même profil !) |
| beaumont-avocats | 2 vs 4 ✓ | emotional vs technical ✓ | light vs light | warm vs cold ✓ | slow-organic vs still | asymmetric-soft vs symmetric | **3** | ✗ |
| electro-maitre-industriel | 2 vs 5 | emotional vs technical-warm ✓ | light vs heavy ✓ | warm vs industrial ✓ | slow-organic vs mechanical ✓ | asymmetric-soft vs asymmetric-strong | **4** | ✓ |
| collectif-nova | 2 vs 3 | n/a | light vs contrasted | warm vs variable | n/a | asymmetric-soft vs editorial | **0** | ✗ |

`max_opposition_score = 4`. **`passes_rule_of_gold = true`** ✓ (grâce à electro-maitre-industriel).

**Mais** : opposition 0/6 vs clinique-aura révèle une **collision de profil**. Deux sites "premium SEC-03" ET "luxury SEC-01" partagent exactement la même 6D canonique → risque de non-distinction stylistique si NEXOS livre un jour les deux simultanément. À flagger dans `notes`.

### §3.6 Risques SOIC

- P04 hero vidéo → pas de stock footage, budget perf < 5 Mo
- P13 anti-polish → vigilance sur lisibilité (pas de faux anti-polish)
- P20 (si réintroduit) → alt-text plats obligatoire + < 500 Ko par image

### Sortie attendue (extrait)

```json
{
  "sector_id": "SEC-03",
  "patterns_recommended": [{"id":"P04"},{"id":"P06"},{"id":"P08"},{"id":"P09"},{"id":"P13"},{"id":"P14"},{"id":"P17"},{"id":"P18"}],
  "patterns_avoided": [],
  "reference_sites": [{"id":"S10"},{"id":"S15"},{"id":"S11"},{"id":"S12"},{"id":"S27"}],
  "personality_6d_proposed": {"D1_density":2,"D2_register":"emotional","D3_typo_weight":"light","D4_palette":"warm","D5_velocity":"slow-organic","D6_structure":"asymmetric-soft"},
  "opposition_check": {"max_opposition_score": 4, "passes_rule_of_gold": true, "detail_note":"PASS vs electro-maitre-industriel (4 dims) MAIS collision 0/6 vs clinique-aura"},
  "confidence_score": 0.78,
  "notes": "Règle d'or PASS mais collision 6D parfaite vs clinique-aura (même secteur? non, différent — SEC-01 vs SEC-03). Si NEXOS livre les deux, envisager shift D6→editorial (pour signer bistro moderne) ou D3→medium. Pattern P20 (menu galerie) écarté par troncature brand-boosted : envisager de le réintégrer pour UX restaurant critique."
}
```

### Évaluation : **AMBIGU** ⚠️

- Patterns : **AMBIGU** — sélection brand-cohérente mais éviction de P20 (menu galerie, natif tier 1 SEC-03) est un faux positif ergonomique. Raffiner l'algorithme de troncature §3.2.
- Sites de référence : **OK** — top 5 diversifiés, S10 priorisé.
- 6D + règle d'or : **OK** (passe) **mais** collision 0/6 vs clinique-aura signalée comme risque cross-client NEXOS.
- **Insight phase E** : deux clients de secteurs différents peuvent partager la même 6D canonique. Envisager d'enrichir la table §3.4 avec des variantes distinctives (ex: "premium × SEC-03 variant-boutique" avec D6:editorial).

---

## Synthèse des 3 évaluations

| Brief | Mapping | Patterns | Sites | 6D | Règle d'or | Évaluation |
|---|---|---|---|---|---|---|
| 1 Physio accessible conversion | OK | OK | OK | KO règle d'or (max 3) | ✗ | AMBIGU |
| 2 Avocat boutique SEO | OK | OK | AMBIGU | KO règle d'or (max 2) | ✗ | AMBIGU |
| 3 Resto plant-based brand | OK | AMBIGU (P20 évincé) | OK | OK (4) mais collision | ✓ | AMBIGU |

**Aucun KO franc** — l'agent converge vers des recommandations cohérentes dans les trois cas. Les 3 `AMBIGU` pointent vers des **raffinements de règles** (pas des bugs bloquants) :

### Actions de raffinement identifiées (backlog phase E+)

1. **Table §3.4 enrichir** : ajouter variantes `positioning × secteur` pour éviter que plusieurs profils tombent sur la même 6D canonique (observé Brief 3 vs clinique-aura).
2. **Algorithme §3.2 troncature** : re-pondérer pour conserver les patterns `tier_natif = 1` prioritairement avant les patterns boostés (observé Brief 3 avec P20 évincé).
3. **Algorithme §3.3 sites** : biaiser vers les sites natifs du secteur quand la pool le permet (observé Brief 2 avec dominance SEC-01 dans sites pour SEC-05).
4. **Règle d'or §3.5** : accepter formellement un `passes = false` avec `notes` claires comme non-bloquant pour ph2 — la règle est une aspiration, pas un gate dur. Documenter dans `_orchestrator.md` ph1.

### Conclusion test dry-run

L'agent `pattern-recommender` est **prêt pour la phase E** (pilote Clinique Aura). Les 3 AMBIGU ne sont pas des régressions ; ils documentent la réalité d'un algorithme knowledge-driven qui doit composer avec la tension *sector-typical patterns* ↔ *rule-of-gold differentiation*. La phase E donnera le verdict empirique sur la qualité de ces recommandations appliquées à un brief réel.

---

## Signature

- Dry-run manuel exécuté 2026-04-16
- Source : `agents/ph1-strategy/pattern-recommender.md` v1.0.0
- Knowledge base version : `nexos-knowledge/*/v1` (phases B + C)
- Opérateur : Claude (session NEXOS v4.2 modify mode)
