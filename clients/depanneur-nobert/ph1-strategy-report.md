# Phase 1 — Strategy Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Date Phase 1** : 2026-05-10
**Mode NEXOS** : `create` (création from scratch, KPI conversion prioritaire)
**Orchestrateur** : ph1-strategy (Claude Opus 4.7 — 1M context)
**Agents exécutés** : pattern-recommender → brand-strategist → information-architect → seo-strategist → solution-architect → scaffold-planner
**Stack imposé** : Next.js 15 + Tailwind 3.4 + next-intl + Vercel
**Type** : vitrine bilingue FR/EN, 6 pages, 24 sections (manifest préexistant conservé)
**Palette CLI imposée** : `primary=#1A2B3C` (navy) · `accent=#FFD700` (or) · `secondary=#B2B2B2` (gris)

---

## ⚠️ Drapeaux à porter en Ph2

Repris et confirmés depuis Phase 0 :

| Code | Drapeau | Bloquant | Action |
|---|---|---|---|
| **F-001** | Conflit palette CLI navy vs brief warm — `--colors` gagne, brief brun écarté | Non (Ph2 ajuste) | Compensation chaleur via D3=heavy (Fraunces 900) + photos vitrine éclairage chaud + textures bois subtiles backgrounds |
| **F-002** | Ville TBD au kickoff — placeholders `[ville]` partout (SEO + structured data + H1) | **Bloquant Ph3** | Récupérer la ville au kickoff client AVANT toute rédaction Ph3 |
| **F-003** | NEQ + adresse + téléphone + horaires = TBD | **Bloquant Ph3** (S-019, S-023, S-024) | Récupérer au kickoff. Templates Ph3 préparés avec placeholders |
| **R-001** | Palette navy peut paraître corporate vs registre voisinage | À monitorer Ph5 | Ph2 layout-designer doit valider le rendu chaleur via typo + photos. Plan B = remonter au client si test conversion faible |

---

## 0. Recommandation knowledge — `pattern-recommender`

> Sortie : `clients/depanneur-nobert/pattern-recommendation.json`
> Confiance : **0.55** (sector_mapping SEC-03 à 0.5 + règle d'or NON satisfaite — voir §0.4)

### 0.1 Secteur identifié

- **SEC-03** Restauration (proxy culturel pour commerce alimentaire de proximité)
- Le secteur dépanneur n'est **pas couvert directement** par les 6 taxonomies NEXOS — mapping SEC-03 retenu en chantier-K avec `sector_mapping_confidence=0.5`. L'agent traite ce client comme un **cas test de dégradation gracieuse** : recommandations cohérentes malgré l'ambiguïté sectorielle.

### 0.2 Top 3 patterns primaires

| Rang | ID | Nom | Rationale clé |
|---|---|---|---|
| 1 | **P02** | Social proof adjacente au CTA | Mesuré +2× leads (Bloor Jane S05) ; gap secteur (0/5 concurrents ph0). Section S-004 SocialProofVoisinage. |
| 2 | **P20** | Menu galerie images | Native tier 1 SEC-03 → catalogue produits (S-015) + grille promos (S-010). **Override §3.2** documenté (sinon évincé par troncature au profit de P17). |
| 3 | **P11** | Page par localisation | KPI conversion + mots-clés [ville] : SEO local + Schema.org LocalBusiness + NAP cohérent Google My Business. |

Patterns primaires complémentaires : P01 (sticky CTA), P08 (story-first), P09 (3-word messaging), P13 (anti-polish), P19 (StoryBrand voisin=héros).

### 0.3 Top 2 sites de référence

| Rang | ID | Site | URL | Patterns couverts |
|---|---|---|---|---|
| 1 | **S14** | La Semilla | https://lasemillanyc.com | P20 + P08 |
| 2 | **S12** | Gazzo | https://gazzo.dk | P13 anti-polish |

Sites complémentaires : S11 Noma (P08 minimalisme chaleureux), S15 Fiola (P08 narration), S30 Kollmann Electric (P13 industriel adapté).

### 0.4 Personnalité 6D proposée

| Dim | Valeur | Justification |
|---|---|---|
| D1 densité | **3 (medium)** | Équilibre catalogue + chaleur humaine (brief conservé) |
| D2 registre | **emotional** | 0/5 concurrents émotionnels — gap mesurable. Voisinage anti-corporate. |
| D3 typo weight | **heavy** | Compense la palette CLI navy froide via Fraunces 900 |
| D4 palette | **cold** | Forcé par §3.4 : palette CLI navy = dominance bleu. Override du brief warm initial. |
| D5 velocity | **slow-organic** | Transitions douces + prefers-reduced-motion + zéro parallax |
| D6 structure | **symmetric** | Rassurant, lisibilité tous âges (clientèle 8-80 ans) |

### 0.5 Règle d'or — opposition_check

| vs | Score | Pass |
|---|---|---|
| clinique-aura | 1/6 | ✗ |
| beaumont-avocats | 2/6 | ✗ |
| **electro-maitre-industriel** | **3/6** | ✗ (manque 1) |
| collectif-nova | 1/6 | ✗ |

**Résultat : `passes_rule_of_gold = false`** (max 3, seuil 4).

L'opposition la plus forte est obtenue vs `electro-maitre-industriel` (D2 emotional vs technical-warm + D5 slow-organic vs mechanical + D6 symmetric vs asymmetric-strong = 3/6). Il manquerait 1 dimension pour atteindre le seuil 4.

**Pour gagner la 4e opposition**, il faudrait shifter D1=3→1 (très aéré, non pertinent pour un dépanneur catalogue) OU shifter D5=slow-organic→still (retire la chaleur). Aucun shift n'est satisfaisant — la règle d'or reste **aspirationnelle** (cf. test-report §3.5 : règle d'or borderline pour clients à secteur ambigu). Le pipeline poursuit avec `passes=false` documenté.

### 0.6 Risques SOIC flaggés

| Dim | Risque |
|---|---|
| D8_legal | P11 → Schema.org LocalBusiness + NAP cohérent GMB. Adresse + ville TBD bloque la finalisation Ph3. |
| D8_legal | Maps embed S-020 + GA : transferts hors QC explicitement consentis (opt-in granulaire), bouton 'Charger la carte' avec note transfert. |
| D8_legal | **Bière vendue** : contenu produits ≠ publicité directe d'alcool sans avertissement responsable (Loi sur les permis d'alcool QC). Mention 'consommation responsable' sur S-015 Bières. |
| D5_perf | P20 + P13 → alt-text obligatoire chaque image, < 500 Ko via next/image, lazy-load par catégorie. |
| D2_a11y | **Palette CLI** : `#FFD700` sur blanc = 1.36:1 (FAIL). Restriction stricte : or = backgrounds CTA avec text-on-accent navy uniquement. |
| D6_seo | P09 + ville TBD : H1 et meta titles bloqués jusqu'au kickoff. Fallback Ph3 = templates avec placeholders. |

---

## 1. Positionnement & voix de marque — `brand-strategist`

> Sortie : `clients/depanneur-nobert/brand-identity.json`

### 1.1 UVP

- **Primary** : « **Votre dépanneur de quartier, à deux pas.** » (8 mots ✓)
- **Secondary** : « Promotions fraîches chaque vendredi. » · « Bières, snacks, lotto — l'essentiel du voisinage. » · « Le dépanneur où on connaît votre prénom. »

### 1.2 Voix de marque

- **Tone** : `voisin-chaleureux-authentique`
- **Formality level** : 2 sur 5 (vous respectueux QC commerce de proximité, ni familier forcé ni corporate)
- **Pronoun** : `vous` (clientèle 8-80 ans, standard QC commerce)
- **Lexique allowed** (27 termes) : voisinage, quartier, à deux pas, voisin/voisine, chez Nobert, accueillant, chaleureux, authentique, pratique, dépannage, fiable, local, ouvert, frais, du coin, sympathique, bienvenue, bonjour, traditionnel, familier, simple, généreux, populaire, courriel, infolettre, promotion de la semaine, …
- **Lexique banned** (16 termes) : leader, premium, expertise, écosystème, synergie, scalable, disruptif, innovant, paradigme, holistique, sur-mesure, élite, luxueux, exclusif, performant, …
- **Anti-positioning explicite** : « Pas Couche-Tard. Pas une chaîne. Votre voisin Nobert. »

### 1.3 Système couleurs (palette CLI imposée)

| Token | Hex | Contraste sur blanc | WCAG | Usage |
|---|---|---|---|---|
| primary | `#1A2B3C` | 13.66:1 | AAA | Titres, fond hero/footer, texte principal |
| primary-hover | `#243D54` | 10.85:1 | AAA | Hover boutons primaires |
| accent | `#FFD700` | 1.36:1 / 10.07:1 sur navy | AAA **on navy** | Fond CTA + badges promos UNIQUEMENT |
| secondary | `#B2B2B2` | 2.14:1 | FAIL pour texte | Bordures décoratives, séparateurs |
| text-secondary | `#475569` | 7.46:1 | AAA | Captions, labels (ardoise foncée) |
| text-on-accent | `#1A2B3C` | 10.07:1 | AAA | Texte sur fond or |
| error | `#B91C1C` | 6.61:1 | AAA | Validation Zod |
| success | `#166534` | 7.83:1 | AAA | Confirmations |
| warning | `#92400E` | 7.45:1 | AAA | Notes Loi 25 + transferts hors QC |

**Règle critique** : l'or `#FFD700` n'est JAMAIS utilisé pour du texte sur fond blanc. Reservé fonds CTA + badges (text-on-accent = navy = 10:1). Le gris `#B2B2B2` est borderline pour le décoratif uniquement.

### 1.4 Typographie

- **Font primary** (titres) : **Fraunces** weights 700/900 — serif chaleureux à fort contraste (compense la palette navy froide via D3=heavy)
- **Font secondary** (body) : **Inter** weights 400/500/600 — sans humaniste, lisibilité tous âges
- **Scale** : Major Third (1.250) — H1=3.815rem → caption=0.75rem
- **Total fichiers woff2** : 5 (limite 4 dépassée d'un cran assumée pour D3=heavy critique). Subsets latin, display=swap, zéro CLS.

### 1.5 Persona cible

Tous âges (8 à 80 ans), résidents du voisinage immédiat (rayon 1 km), fréquence quotidienne à hebdomadaire, panier 5-25 $. Recherche commodité + humanité. Évite chaînes par préférence éthique ou simple proximité.

---

## 2. Architecture de l'information — `information-architect`

> Sortie : `clients/depanneur-nobert/site-map-logic.json`

### 2.1 Arborescence (profondeur max = 1)

```
/                                       (S-001 à S-007 + StickyCTA)
├── /promotions   ↔ /deals              (S-009 à S-012 — ISR weekly)
├── /produits     ↔ /products           (S-013 à S-017 + sticky sub-header categories)
├── /contact      ↔ /contact            (S-018 à S-022)
├── /politique-confidentialite ↔ /privacy-policy   (S-023)
└── /mentions-legales ↔ /legal-notice   (S-024)
```

**Profondeur = 1, max-clicks-to-any-page = 1** (largement sous le seuil 3 NEXOS).

### 2.2 Navigation

- **Main nav (4 items)** : Accueil · **Promotions** *(highlight badge or)* · Produits · Contact
- **LangSwitcher** : header-right, FR/EN avec préservation route via `pathnames` mapping next-intl
- **Footer 3 colonnes** : Le dépanneur / Infos pratiques / Légal Loi 25 (incl. lien `Gérer mes cookies`)
- **CTA global S-008** : sticky bottom-right desktop / bottom-full-width mobile, hidden sur `/promotions` et pages légales

### 2.3 Slugs FR ≠ EN (à signaler à Vercel + Ph4)

| FR | EN |
|---|---|
| `/promotions` | `/deals` |
| `/produits` | `/products` |
| `/politique-confidentialite` | `/privacy-policy` |
| `/mentions-legales` | `/legal-notice` |

Mapping via `next-intl` `createSharedPathnamesNavigation`.

### 2.4 Formulaires (Loi 25 explicite)

| ID | Rétention | Consent | Endpoint |
|---|---|---|---|
| FORM-NEWSLETTER (S-007) | 12 mois | opt-in checkbox non cochée | POST `/api/newsletter` |
| FORM-CONTACT (S-021) | 6 mois post-réponse | opt-in checkbox non cochée | POST `/api/contact` (SMTP → nobert@…) |

Honeypot, rate-limit (1/IP/5 min news, 3/IP/h contact), validation Zod partagée client+server.

### 2.5 Tracking points (gating consentement)

5 events GA4 (`pageview`, `cta_promotions_click`, `newsletter_submit_success`, `phone_click`, `maps_load`) — tous gated sur `cookie_consent.analytics === true`. Aucun script tiers ne se charge avant opt-in granulaire.

### 2.6 Maillage interne

- **Hub pages** : `/` (homepage pivot) + `/promotions` (KPI conversion principal)
- **Cycle conversion** : Hero → /promotions → cross-sell → /produits → cross-sell → /promotions
- **0 page orpheline** (chaque route au moins linkée depuis main_nav ou cross-sell)

---

## 3. Plan SEO — `seo-strategist`

> Sortie : `clients/depanneur-nobert/seo-strategy.json`

### 3.1 Stratégie globale

- **Primary keyword** : `dépanneur [ville]` (placeholder kickoff)
- **Secondary** (6) : `dépanneur ouvert 24h [ville]`, `bière [ville]`, `loto québec [ville]`, `épicerie de quartier [ville]`, `snack froid chaud [ville]`, `dépanneur près de chez moi`
- **Long tail** (6) : `dépanneur ouvert maintenant [ville]`, `promotions dépanneur [ville] cette semaine`, `bière microbrasserie [ville] dépanneur`, etc.
- **Difficulté** : low (DR 5-25) — secteur faiblement digitalisé
- **Intent** : transactional (visite physique imminente) + informational (horaires)

### 3.2 Title + Meta (FR + EN, < 60 / 120-155 chars)

Toutes les pages ont `title_tag_fr/en` et `meta_desc_fr/en` redigés avec le placeholder `[ville]`. Exemples :

- **Home** : « Dépanneur Nobert | Votre dépanneur de quartier à [ville] » (53 chars FR)
- **Promotions** : « Promotions de la semaine | Dépanneur Nobert [ville] » (52 chars FR)
- **Produits** : « Bières, snacks, lotto, essentiels | Dépanneur Nobert » (53 chars FR)

### 3.3 Structured data (JSON-LD)

| Page | Schema |
|---|---|
| Site-wide | Organization · WebSite · BreadcrumbList |
| `/` | LocalBusiness (`@type: ConvenienceStore`) · OpeningHoursSpecification |
| `/promotions` | LocalBusiness · **FAQPage** · OfferCatalog |
| `/produits` | LocalBusiness · **FAQPage** · ItemList |
| `/contact` | LocalBusiness · OpeningHoursSpecification · ContactPage |

**Différenciation #1 AI Overviews** : 0/5 concurrents ph0 n'ont pas de FAQPage structurée → présence immédiate sur featured snippets QC dépanneur.

### 3.4 Sitemap + robots

- `app/sitemap.ts` dynamique avec hreflang fr/en/x-default
- `app/robots.ts` : **AI crawlers autorisés** (`GPTBot`, `Google-Extended`, `ClaudeBot`) — secteur sous-représenté dans les LLM, présence = avantage concurrentiel direct
- Priority : home 1.0 / promos 0.9 / produits 0.8 / contact 0.7 / légal 0.3

### 3.5 Bloqué par kickoff

| Item | Impact |
|---|---|
| Ville | Tous title/meta/H1/structured data |
| Adresse + NEQ | Mentions légales + LocalBusiness |
| Téléphone | tel: links + LocalBusiness |
| Horaires précis 7 jours | OpeningHoursSpecification + S-019 |

---

## 4. Stack technique — `solution-architect`

> Sortie : `clients/depanneur-nobert/stack-decision.json`

### 4.1 Stack core (imposé)

| Composant | Choix | Justification |
|---|---|---|
| Framework | Next.js 15.x App Router | brief.design.stack_imposed.framework |
| Langage | TypeScript 5 strict (+ noUncheckedIndexedAccess) | Standard NEXOS |
| CSS | **Tailwind 3.4** (vs 4.x) | ADR-001 — stabilité production |
| i18n | next-intl ^3.x avec `pathnames` mapping | Slugs FR ≠ EN |
| Tests | Vitest + RTL (pas e2e) | Budget solo |
| Deploy | Vercel | brief.site.hosting=vercel |

### 4.2 Additions optionnelles (8 deps prod)

- **Framer Motion** ^11 (15 KB) — ADR-002, scope limité ≤ 12 éléments animés/page, `useReducedMotion()` systématique
- **React Hook Form** ^7 + **Zod** ^3 + **@hookform/resolvers** — formulaires Loi 25 (~23 KB total)
- **lucide-react** — 12 icônes max, tree-shaking strict
- **DOMPurify** : EXCLU (ADR-003 — pages légales en JSX statique, économie 22 KB)

### 4.3 ADR Log (5 décisions documentées)

| ID | Titre |
|---|---|
| ADR-001 | Tailwind 3.4 plutôt que 4.x (stabilité prod) |
| ADR-002 | Framer Motion inclus malgré size=solo (P17 + D5 critiques) |
| ADR-003 | Pages légales en JSX statique (pas innerHTML, alignement fix A-006) |
| ADR-004 | Maps embed gated par consent applicatif (iframe natif, pas SDK) |
| ADR-005 | ISR weekly /promotions (revalidate=604800, regen vendredi) |

### 4.4 Sécurité

- `poweredByHeader: false`, `reactStrictMode: true`
- 6 headers HTTP via `vercel.json` (X-Frame-Options DENY, HSTS preload, Permissions-Policy, etc.)
- **CSP nonce-based** via middleware (default-src 'self', script-src 'self' 'nonce-{N}' GA tags, frame-src maps.google.com avec gating consent applicatif)
- Rate limiting `/api/newsletter` (1/IP/5 min), `/api/contact` (3/IP/h)
- Cible `npm audit` : 0 high/critical au build

### 4.5 Budget perf

- LCP < 2.5s (3.0s mobile 4G) · INP < 200ms · CLS < 0.1
- Bundle first-load < 250 KB · images max 500 KB · 5 fichiers fonts max
- Cible Lighthouse Performance ≥ 90

---

## 5. Scaffold — `scaffold-planner`

> Sortie : `clients/depanneur-nobert/scaffold-plan.json`
> **Section manifest préservé** : 24 sections (`audited`) du manifest existant conservées sans réécriture.

### 5.1 Arbre de fichiers (78 fichiers totaux)

```
depanneur-nobert-site/
├── app/
│   ├── [locale]/
│   │   ├── layout.tsx            # Header, Footer, CookieConsent, JSON-LD Org+WebSite
│   │   ├── page.tsx              # Home (S-001..S-007)
│   │   ├── promotions/page.tsx   # ISR weekly (S-009..S-012)
│   │   ├── produits/page.tsx     # (S-013..S-017)
│   │   ├── contact/page.tsx      # (S-018..S-022)
│   │   ├── politique-confidentialite/page.tsx  # JSX statique S-023
│   │   ├── mentions-legales/page.tsx           # JSX statique S-024
│   │   ├── not-found.tsx · error.tsx · loading.tsx
│   ├── api/newsletter/route.ts · api/contact/route.ts
│   ├── sitemap.ts · robots.ts
├── components/
│   ├── layout/    # Header, Footer, LangSwitcher, StickyCTA (S-008), CookieConsent
│   ├── sections/  # 23 composants 1:1 avec S-001..S-024 (LegalDocBody = 2 variants)
│   ├── ui/        # Button (variants primary/accent/ghost), Card, Badge, Input, Textarea, Checkbox
│   └── jsonld/    # LocalBusiness, FAQ, Breadcrumb, Organization
├── lib/
│   ├── analytics.ts (gating consent)
│   ├── cookie-consent.ts (Context + helpers)
│   ├── jsonld/{local-business,faq}.ts
│   ├── schemas/{contact,newsletter}.ts (Zod partagés client/server)
│   ├── rate-limit.ts · utils/{cn,format}.ts
├── i18n/{request,navigation}.ts (pathnames mapping FR/EN)
├── messages/{fr,en}.json (parité 1:1)
├── data/{promotions,produits,temoignages,horaires}.json
├── public/{favicon, og-image, hero-vitrine, maps-placeholder}
├── styles/globals.css
├── types/{brand,data}.ts
├── tests/{cookie-consent,contact-form,lang-switcher}.test.tsx
├── middleware.ts (next-intl + nonce CSP)
├── next.config.mjs · tailwind.config.ts · tsconfig.json · vercel.json
└── package.json · .env.example · .eslintrc.json · .gitignore · README.md
```

### 5.2 Mapping section → composant

24 sections du manifest → 23 fichiers de composant (LegalDocBody mutualisé S-023+S-024 via variant). Mapping complet dans `scaffold-plan.json::section_to_component_mapping`.

### 5.3 Section manifest

**Action Phase 1** : aucune. Le manifest existant (`section-manifest.json`, 24 sections, statut `audited`) est **conservé en l'état**. Mode `create` ne réécrit pas un manifest pré-existant. Les phases ultérieures (Ph2/Ph3/Ph4/Ph5) mettront à jour les `lifecycle.*` au besoin.

---

## Score global Phase 1

| Critère | Score | Note |
|---|---|---|
| Cohérence avec brief + ph0 (KPI conversion + Loi 25 + palette CLI) | 9/10 | Palette navy override appliqué proprement, compensation chaleur via typo + photos |
| Pattern recommendation knowledge-driven | 7/10 | Patterns alignés mais règle d'or NON satisfaite (max 3 oppositions, seuil 4) |
| Brand identity actionnable Ph2 | 9/10 | Tokens + contrastes WCAG AAA chiffrés + typo justifiée |
| IA + i18n + Loi 25 | 10/10 | Slugs FR≠EN, pathnames mapping, formulaires Loi 25 explicites, gating consent complet |
| SEO + structured data + AI Overviews | 9/10 | FAQPage différenciation #1, AI crawlers autorisés, blocage [ville] documenté |
| Stack + ADR + sécurité | 10/10 | 5 ADR documentés, CSP nonce-based, rate-limit, budget perf chiffré |
| Scaffold complet et 1:1 avec manifest | 10/10 | 78 fichiers, mapping S-001..S-024 → composants explicite |
| Risques flaggés au pipeline | 9/10 | F-001..F-003 + R-001 + 6 risques SOIC remontés |

**Score global : 9.1/10**

> Gate ph1→ph2 : seuil μ ≥ 8.0 → **PASS**.
>
> Note : la règle d'or non satisfaite (`opposition_check.passes_rule_of_gold = false`) est **documentée et acceptée** comme aspirationnelle (cf. pattern-recommender-test-report §3.5). Elle ne bloque pas le passage en Ph2 selon la convention de l'orchestrateur.

---

## Sorties machine-readable

| Fichier | Status |
|---|---|
| `pattern-recommendation.json` | ✅ valide JSON, schema `nexos-ph1/pattern-recommendation/v1` |
| `brand-identity.json` | ✅ valide JSON, schema `nexos-ph1/brand-identity/v1` |
| `site-map-logic.json` | ✅ valide JSON, schema `nexos-ph1/site-map-logic/v1` |
| `seo-strategy.json` | ✅ valide JSON, schema `nexos-ph1/seo-strategy/v1` |
| `stack-decision.json` | ✅ valide JSON, schema `nexos-ph1/stack-decision/v1` |
| `scaffold-plan.json` | ✅ valide JSON, schema `nexos-ph1/scaffold-plan/v1` |
| `section-manifest.json` | ✅ préservé (24 sections, statut `audited`) |

---

## Handoff Phase 2 — Design

### Décisions héritées (non négociables)

1. **Palette CLI navy/or/gris imposée** — primary `#1A2B3C` + accent `#FFD700` + secondary `#B2B2B2`. Compensation chaleur via Fraunces 900 + photos vitrine éclairage chaud + textures bois subtiles.
2. **Typographie** : Fraunces 700/900 (titres) + Inter 400/500/600 (body). Scale Major Third 1.250.
3. **Architecture i18n** : 6 pages × 2 locales avec slugs FR≠EN via `next-intl pathnames`.
4. **Hero S-001 statique** (pas vidéo, pas carousel — anti-patterns confirmés ph0).
5. **24 sections du manifest** — composants 1:1 fournis par scaffold-plan.

### Inputs pour Ph2 (design)

- `brand-identity.json` (tokens couleurs, typo, voix de marque)
- `site-map-logic.json` (routes, nav, formulaires, breadcrumbs)
- `pattern-recommendation.json` (patterns à appliquer + sites de référence à étudier)
- `section-manifest.json` (24 sections immutables)

### Risques à monitorer en Ph2

1. **R-001 palette navy "corporate"** — layout-designer doit valider que la chaleur typo + photos + textures compense la perception froide. Test perception au plus tard Ph5.
2. **Contraste accent or** — discipline stricte : or = backgrounds CTA + badges UNIQUEMENT, jamais texte sur blanc.
3. **Anti-pattern carousel** — Hero S-001 photo unique impactante, zéro carousel.
4. **Photos authentiques** — placeholder structurel Ph2, brief client pour shooting (priorité S-001, S-004, S-006, S-015).

---

*Phase 1 Strategy complétée 2026-05-10. Prochain handoff : `ph2-design/_orchestrator` (layout-designer + design-token-mapper + responsive-strategist + interaction-designer + asset-manager + visual-direction).*
