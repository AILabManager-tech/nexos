# Phase 1 — Strategy Report

**Client** : Dépanneur Nobert inc. (`_e2e_validation_2026-05-08`)
**Mode** : create (KPI primaire = conversion)
**Date** : 2026-05-08
**Cadrage métier prioritaire** : CTA primaire = « Voir les promotions de la semaine » · clarté de l'offre dépanneur de quartier · indicateur de succès = visite physique + consultation promo hebdo
**Phase précédente** : Ph0 Discovery — μ = 8.4/10 (GO ph0→ph1)

---

## 0. Recommandation knowledge (pattern-recommender)

**Secteur identifié** : `SEC-03 Restauration` (mapping de proximité culturelle, le secteur réel — commerce de proximité / dépanneur québécois — n'est pas couvert directement par les 6 taxonomies NEXOS).
**Confidence sectorielle** : 0.5 (brief) → confidence agent finale : **0.72** (compensée par la richesse exceptionnelle du brief).

### Top 3 patterns primaires (sur 8 retenus)

| Rang | Pattern | Tier final | Rationale courte |
|---|---|---|---|
| 1 | **P02 — Social proof adjacente au CTA** | 1 (mesuré +2× leads Bloor Jane S05) | Témoignages voisinage à côté du CTA « Voir les promotions » |
| 2 | **P01 — Sticky CTA persistant** | 1 (boost KPI conversion) | CTA atteignable à tout scroll mobile |
| 3 | **P20 — Menu galerie images** | 1 (SEC-03 natif tier 1) | Catalogue catégorisé : gap concurrentiel direct ph0 |

Patterns primaires retenus : **P01, P02, P08, P09, P13, P17, P20** + secondaire **P03** (color-coded nav).

Patterns évités explicitement : **P04** (hero vidéo — brief impose photo réelle), **P05** (single-page — brief liste 6 pages distinctes), **P07/P10/P15** (size=solo, démotion automatique §3.2.4), **P11** (single location).

### Top 2 sites de référence

| Site | URL | Patterns couverts | Lien brief |
|---|---|---|---|
| **S13 Ma'ono** | https://maono.com | P09 (3-word brand) | Cité dans `brief.design.references` |
| **S14 La Semilla** | https://lasemillanyc.com | P20 (menu galerie) | Cité dans `brief.design.references` |

Les 5 sites retenus (S13, S14, S12, S11, S05) sont **tous SEC-03 natifs** et 4/5 sont cités explicitement dans le brief — alignement parfait avec l'intention design du client.

### Personnalité 6D proposée

```
D1_density       = 3   (équilibré, ancré brief.personality_hints)
D2_register      = emotional (chaleur convivialité — verrouillé brief)
D3_typo_weight   = heavy (lisibilité tous âges + Fraunces — verrouillé brief)
D4_palette       = warm (forcé par constraints.palette_imposed brun + jaune doré + crème)
D5_velocity      = slow-organic (transitions sobres, prefers-reduced-motion)
D6_structure    = symmetric (sections alternées + grille 12 col)
```

### Règle d'or d'opposition

| vs client NEXOS | Score opposition | Verdict |
|---|---|---|
| clinique-aura (SEC-01) | 0/6 | FAIL (D2/D4/D5 communs) |
| beaumont-avocats (SEC-05) | 3/6 | FAIL |
| **electro-maitre-industriel (SEC-06)** | **4/6** | **PASS** ✓ |
| collectif-nova (SEC-02) | 1/6 | FAIL |
| table-de-marguerite (SEC-03) | n/a | données 6D incomplètes |

→ `passes_rule_of_gold = true` via electro-maitre-industriel (opposition sur D2, D4, D5, D6).

### Risques SOIC flaggés

1. **D8 Loi 25** — couvert par templates NEXOS, vérifier intégration Ph2/Ph4
2. **D7 SEO** — slot `[ville]` non résolu = bloquant SEO local, kickoff prioritaire
3. **D5 Performance** — cumul P17 + photos catalogue → surveiller LCP mobile <2.5s
4. **D2 Accessibilité** — accent `#FFD700` interdit comme couleur de texte (contraste 1.07:1) — usage exclusivement décoratif, déjà flagué Ph0
5. **D1 UX** — édition hebdo promotions par solo = risque d'abandon, choix MVP = JSON commit (ADR-003)

### Gate pattern-recommender

- ✅ `pattern-recommendation.json` présent et JSON valide
- ✅ `patterns_recommended` non vide (8 entrées)
- ✅ `personality_6d_proposed` complète (6 dimensions)
- ✅ `opposition_check.passes_rule_of_gold == true`
- ✅ `confidence_score = 0.72 ≥ 0.60`

→ **GATE PASS** vers brand-strategist.

---

## 1. Positionnement & voix de marque

### UVP primaire (12 mots)
> « Le dépanneur de [ville]. Promos chaque semaine, ouvert quand vous en avez besoin. »

### UVP secondaires
- « Bières froides, lotos, snack et dépannage — chez nous, depuis toujours. »
- « Le patron vous connaît, les promos tiennent leurs promesses. »
- « Votre dépanneur de quartier — pas une chaîne, pas un détour. »

### Brand voice
- **Tone** : convivial-authentique-quebecois
- **Formality** : 2/5 (tutoiement de politesse, pas familier vulgaire)
- **Voix active** systématique. Phrases courtes. FR-QC parlé assumé (« passez nous voir », « chez nous », « on vous attend »).
- **Lexicon banned (extrait)** : `solution`, `expérience client`, `écosystème`, `partenaire de confiance`, `excellence`, `leader`, `innovant`, `premium`, `centre d'achat`. Renforce l'anti-corporate explicite du brief.

### Système couleur (palette imposée respectée + contrastes WCAG calculés)

| Token | HEX | Contraste sur fond | Usage |
|---|---|---|---|
| primary | `#8B4513` | 8.59:1 / 7.91:1 | H1-H3, liens, fonds boutons primaires |
| primary_hover | `#A0522D` | 5.92:1 | États :hover/:focus |
| accent | `#FFD700` | **1.07:1 sur blanc — INTERDIT comme texte** | EXCLUSIVEMENT badges/fills/boutons avec texte `#2A1810` (ratio 13.95:1 ✓) |
| background | `#FFF8E7` | base | Sections impaires |
| surface | `#FFFFFF` | base | Sections paires |
| text_primary | `#2A1810` | 16.32:1 / 13.34:1 | Body, headings |
| text_secondary | `#6B4F3C` | 6.81:1 | Captions, métadonnées |
| border | `#D4C5A9` | n/a (non-text) | Séparateurs |
| error | `#B91C1C` | 6.27:1 | Erreurs formulaires |
| success | `#2F6F4E` | 5.96:1 | Confirmations |

→ Tous contrastes **texte** ≥ 4.5:1 (WCAG AA). Accent `#FFD700` flagué `D6_a11y_critical` dans `brand-identity.json::color_system.accent.constraint_flag`.

### Typographie

- **Heading** : Fraunces (Google Fonts OFL) — display chaleureuse, accord D3=heavy + D2=emotional
- **Body** : Inter (Google Fonts OFL) — humaniste, lisible tous âges
- **Scale** : Major Third (1.25)
- **Loading** : `next/font/google` self-hosted, `display: swap`, subset latin, max 4 fichiers woff2 (Fraunces 700/800 + Inter 400/600)

---

## 2. Architecture de l'information

### Routes (FR + EN)

| Route FR | Route EN | Profondeur | Priorité |
|---|---|---|---|
| `/` | `/en` | 0 | critical |
| `/promotions` | `/en/promotions` | 1 | critical |
| `/produits` | `/en/products` | 1 | high |
| `/contact` | `/en/contact` | 1 | high |
| `/politique-confidentialite` | `/en/privacy-policy` | 1 (footer) | mandatory |
| `/mentions-legales` | `/en/legal-mentions` | 1 (footer) | mandatory |

Profondeur max = 1 → toutes pages clés en ≤ 1 clic depuis la home (gate D7 SEO ✓).

### Navigation

- **main_nav** : 4 items (Accueil · Promotions · Produits · Contact) + LanguageSwitcher inline. Sous le plafond max 7 ✓.
- **Sticky CTA mobile** : « Voir les promotions de la semaine » → `/promotions`. **Différenciation directe** vs concurrence (5/5 absent, ph0 §4 P11).
- **Footer 3 colonnes** : Le dépanneur · Coordonnées · Légal (RPP visible).
- **SkipToContent** + drawer mobile accessible (focus trap, ESC, touch ≥48px).

### Data flow & formulaires

| Form | Champs | Consentement Loi 25 | Rétention |
|---|---|---|---|
| **Newsletter** | email + checkbox opt-in | texte explicite FR/EN, désinscription documentée | 12 mois (brief.legal) |
| **Contact** | nom, courriel/tel, message, checkbox + honeypot | texte explicite FR/EN | 6 mois (brief.legal) |

Rate limit : 5/h pour newsletter, 3/h pour contact (anti-spam). Tracking GA4 default `denied`, activé seulement après consentement granulaire opt-in.

### Maillage interne

- **Hub pages** : `/` (entrée brand+SEO) + `/promotions` (pivot conversion)
- **Orphan check** : PASS (toutes pages ≥ 1 lien entrant)
- 12 entrées dans `link_map`, max 30 liens sortants par page

---

## 3. Plan SEO

### Stratégie globale

- **Primary keyword** : `dépanneur [ville]` (slot variabilisé — résolution kickoff)
- **Secondary** : `dépanneur ouvert 24h [ville]`, `bière [ville]`, `loto Québec [ville]`, `épicerie de quartier [ville]`
- **Long-tail** : `promotions dépanneur [ville] cette semaine`, `dépanneur près de moi [ville]`, etc.
- **Difficulté** : low (DR 5-25) sur la longue traîne géo-locale, medium-low sur le primary
- **Intent** : transactional (visite) + informational (horaires, dispo) + navigational (adresse)

### Structured data plan

| Page | Schema.org |
|---|---|
| `/` | `LocalBusiness` + `ConvenienceStore` + `OpeningHoursSpecification` + `GeoCoordinates` + `PostalAddress` |
| `/promotions` | `BreadcrumbList` + `ItemList` + `Offer` |
| `/produits` | `BreadcrumbList` + `ItemList` + `OfferCatalog` |
| `/contact` | `LocalBusiness` + `ContactPoint` + `OpeningHoursSpecification` + `GeoCoordinates` + `BreadcrumbList` |
| `/politique-confidentialite`, `/mentions-legales` | `BreadcrumbList` |

Site-wide : `Organization` + `WebSite` + `BreadcrumbList`. Validation obligatoire Google Rich Results Test avant Ph5.

### Title tags & meta (extraits, tous validés <60 chars title et 92-137 chars meta)

- `/` FR : `Dépanneur Nobert | Le dépanneur de [ville]` (47 chars)
- `/promotions` FR : `Promotions de la semaine | Dépanneur Nobert [ville]` (53 chars)
- `/produits` FR : `Nos produits | Bières, snacks, loto — Dépanneur Nobert` (56 chars)

### Hreflang & sitemap

- **Hreflang** : FR (sans préfixe) / EN (`/en/`) / x-default = FR
- **Sitemap** : `app/sitemap.ts` dynamique, priorities 1.0 (home) → 0.9 (promos) → 0.8 (produits) → 0.7 (contact) → 0.3 (légal)
- **Robots** : `app/robots.ts` Allow:/ + Disallow:/api/ + Sitemap link

### Risques bloquants SEO

- **Slot `[ville]` non résolu** → SEO local inopérant. Kickoff prioritaire avant Ph3 ; sinon Ph3 génère avec placeholder explicite + flag bloquant Ph5.
- **NEQ inconnu** → mentions légales incomplètes (D8 partiel).

---

## 4. Stack technique (justifié)

### Stack imposé respecté (brief.design.stack_imposed)

| Composant | Choix | Justification |
|---|---|---|
| Framework | **Next.js 15.x App Router** | SSR/SSG, metadata API, sitemap dynamique |
| Langage | **TypeScript 5.x strict** + `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` | Type safety obligatoire (catalogue + promos JSON typés) |
| CSS | **Tailwind 3.4.x** (vs 4.x — ADR-001) | Stabilité écosystème, parité autres clients NEXOS |
| i18n | **next-intl 3.x** (FR/EN, default FR, prefix-as-needed) | Aligné brief, type-safe |
| Tests | **Vitest 1.x + @testing-library/react** | Rapide ESM, tests sur composants critiques |
| Lint | ESLint + `eslint-plugin-jsx-a11y` (obligatoire) | D6 a11y identifié faible secteur en ph0 |
| Deploy | **Vercel** | Aligné brief.site.hosting |
| Fonts | Fraunces + Inter via `next/font/google` | Self-host, zéro layout shift, conforme Loi 25 (pas de requête Google) |
| Icons | `lucide-react` | Tree-shakable, line-art SEC-03 |

### Optionnels inclus (avec garde-fous)

| Package | Impact bundle | ADR |
|---|---|---|
| **framer-motion** 11.x | +15-20KB gz | ADR-002 — limité aux sections principales, `useReducedMotion()` obligatoire |
| **react-hook-form** + **zod** | +10-12KB gz | Formulaires Loi 25 type-safe |

### Rejetés explicitement

- jQuery, styled-components, Pages Router, Wix/Squarespace, GTM direct sans consent gate, next-themes (pas de dark mode v1 — ADR-004)

### Sécurité

- `next.config.mjs` : `poweredByHeader: false`, `reactStrictMode: true`
- `vercel.json` : X-Frame-Options DENY, HSTS preload, Permissions-Policy strict, X-Content-Type-Options nosniff, Referrer-Policy strict-origin-when-cross-origin, **CSP nonce-based** (généré par agent `csp-generator` Ph4)
- **Rate limiting** middleware sur `/api/newsletter` (5/h) et `/api/contact` (3/h)
- **Cookies** opt-in via `templates/cookie-consent-component.tsx` (default=denied)

### ADR adoptés (5)

1. **ADR-001** — Tailwind 3.4 retenu vs 4.x (stabilité écosystème)
2. **ADR-002** — Framer Motion inclus avec garde-fous stricts
3. **ADR-003** — Promotions hebdo via JSON commit (pas de CMS pour MVP solo)
4. **ADR-004** — Pas de dark mode v1
5. **ADR-005** — API keys côté server uniquement (Google Maps via iframe, GA4 measurement_id en NEXT_PUBLIC_ chargé après consentement)

### Performance budget

- LCP mobile <2.5s · INP <200ms · CLS <0.1
- Bundle initial JS <200KB gz
- Images ≤500KB par photo, fonts ≤150KB total
- Lighthouse mobile : Performance ≥90, A11y ≥95, BP ≥95, SEO 100

### Dépendances

- 9 deps prod (sous plafond 10) : next, react, react-dom, next-intl, framer-motion, lucide-react, react-hook-form, @hookform/resolvers, zod
- 0 vulnérabilité HIGH/CRITICAL tolérée (`npm audit` au build)

---

## 5. Scaffold (arbre de fichiers)

### Vue d'ensemble

- **78 fichiers** au total, organisés en 12 dossiers
- **17 sections** identifiées et tracées dans `section-manifest.json` (S-001 → S-017)
- Convention Next.js 15 flat (pas de `src/`), max 1 niveau de sous-dossiers dans `components/`

### Structure de dossiers

```
depanneur-nobert-site/
├── app/[locale]/         (pages + layouts + special files)
│   ├── promotions/       (page critique KPI conversion)
│   ├── produits/
│   ├── contact/
│   ├── politique-confidentialite/
│   └── mentions-legales/
├── app/api/              (newsletter, contact)
├── components/
│   ├── layout/           (Header, Footer, StickyMobileCta, MobileDrawer, SkipToContent, CookieConsent)
│   ├── sections/         (S-001 à S-017 — 17 composants)
│   ├── ui/               (Button, Card, Input, Textarea, Checkbox, Badge, Container, Section, Icon)
│   └── seo/              (JsonLd injecteur)
├── i18n/                 (next-intl config)
├── lib/                  (utils, format, promotions, products, seo, structured-data, consent, rate-limit, schemas)
├── messages/             (fr.json, en.json)
├── public/               (favicons, OG, photos hero/produits)
├── site/data/            (promotions, products-categories, horaires, site-info — single source of truth)
├── styles/               (globals.css)
├── tests/                (components, lib, api)
└── types/                (promotion, product, site-info, i18n)
```

### Sections critiques (extraits du `section-manifest.json`)

| ID | Page | Section | Patterns | Priorité |
|---|---|---|---|---|
| S-001 | home | Hero | P09, P13, P17 | critical |
| S-002 | home | PromoWeekTeaser | P02, P20 | critical |
| S-004 | home | InfosPratiques | P01 | critical |
| S-007 | promotions | HeroPromoWeek | P09 | critical |
| S-008 | promotions | PromosGrid | P02, P17, P20 | critical (asset KPI conversion) |
| S-013 | contact | Coordonnees | P01 | critical |
| S-014 | contact | Horaires | — | critical |
| S-015 | contact | ContactForm | — | critical |
| S-016 | contact | RppMention | — | mandatory |
| S-017 | legal | LegalContent | — | mandatory |

Le détail complet des 17 sections est dans `section-manifest.json` — chaque section porte ses dimensions SOIC, ses patterns appliqués, son lifecycle (planned/designed/content_ready/built/audited), et son `i18n_namespace`.

### Fichiers obligatoires NEXOS — checklist

- ✅ `next.config.mjs`, `tsconfig.json`, `tailwind.config.ts`, `postcss.config.js`, `package.json`, `.eslintrc.json`, `.env.example`, `.gitignore`, `vercel.json`
- ✅ `middleware.ts`, `i18n/request.ts`
- ✅ `app/[locale]/layout.tsx`, `page.tsx`, `not-found.tsx`, `error.tsx`, `loading.tsx`
- ✅ `messages/fr.json`, `messages/en.json`
- ✅ `app/sitemap.ts`, `app/robots.ts`
- ✅ `components/ui/Button.tsx`, `Card.tsx`, `Input.tsx`
- ✅ `components/layout/Header.tsx`, `Footer.tsx`, `CookieConsent.tsx`

### Asset critique flagué kickoff

- `public/images/hero-nobert.jpg` — **photo réelle propriétaire/dépanneur** (non négociable D2 emotional). Plan B documenté ph0 : photo provisoire chaleureuse étiquetée temporaire si kickoff manqué, à remplacer S+1.

---

## Validation des gates SOIC

| Dimension | État Ph1 | Note |
|---|---|---|
| **D1 Architecture** | Stack cohérent App Router + scaffold structuré + 17 sections tracées | 8.5 |
| **D2 Accessibilité** | jsx-a11y obligatoire + SkipToContent + drawer focus trap + accent `#FFD700` flagué non-text-only ; contrastes 4.5:1+ partout (sauf accent contrôlé) | 8.5 |
| **D3 Performance** | Bundle <200KB, framer-motion encadré (ADR-002), fonts ≤150KB, LCP <2.5s ciblé, photos ≤500KB | 8.5 |
| **D4 Sécurité** | Headers complets vercel.json + CSP nonce-based prévue + rate limiting API routes + poweredByHeader=false + API keys server-only (ADR-005) | 9.0 |
| **D5 i18n** | next-intl + 100% routes mappées FR/EN + hreflang planifié + middleware | 9.0 |
| **D6 Structure** | symmetric verrouillé, sections alternées surface/surface_alt, grille 12 col | 8.5 |
| **D7 SEO** | Plan complet (title/meta/H1/structured data/sitemap/robots/hreflang) ; **risque [ville] non résolu** documenté | 8.0 |
| **D8 Loi 25** | Templates NEXOS + RPP visible + cookies opt-in + consent texts FR/EN + retention documentée + RppMention section dédiée | 9.5 |
| **D9 Qualité** | 7 livrables JSON validés `jq` ✓ + 5 ADR + ban-list lexique + UVP <12 mots + tests Vitest planifiés | 8.5 |

---

## Risques portés en Ph2

| Risque | Source | Impact | Mitigation |
|---|---|---|---|
| Slot `[ville]` non résolu | brief.client.locations TBD | SEO local + JSON-LD + copy paralysés | Kickoff obligatoire avant Ph3 |
| NEQ inconnu | brief.legal.address TBD | Mentions légales incomplètes (D8) | Templates avec placeholder + flag Ph5 |
| Photo réelle propriétaire indisponible launch | brief design | D2 emotional dégradé | Photo provisoire flag temporaire S+1 |
| Édition hebdo promos solo (ADR-003) | KPI conversion = page promo | Risque de page morte → perte SEO | JSON commit + doc `README.md` éditoriale + Sanity en backlog |
| Mapping sectoriel SEC-03 confidence 0.5 | brief.client.sector_id_mapped_confidence | Recommandations potentiellement génériques | Compensation par richesse brief (palette imposée + 6D hints + 4 sites cités) |

---

## Évaluation

```
D1 Architecture  : 8.5
D2 Accessibilité : 8.5
D3 Performance   : 8.5
D4 Sécurité      : 9.0
D5 i18n          : 9.0
D6 Structure     : 8.5
D7 SEO           : 8.0
D8 Loi 25        : 9.5
D9 Qualité       : 8.5
```

**Score global : 8.7/10**
**μ = 8.7/10**

Seuil de passage Ph1→Ph2 (μ ≥ 8.0) : **GO**.

---

## Livrables produits (7)

| Fichier | Statut | Validé `jq` |
|---|---|---|
| `pattern-recommendation.json` | ✓ | ✓ |
| `brand-identity.json` | ✓ | ✓ |
| `site-map-logic.json` | ✓ | ✓ |
| `seo-strategy.json` | ✓ | ✓ |
| `stack-decision.json` | ✓ | ✓ |
| `scaffold-plan.json` (78 fichiers) | ✓ | ✓ |
| `section-manifest.json` (17 sections S-001→S-017) | ✓ | ✓ |

### Note sur `pattern-recommender-test-report.md`

Le test-report existant (`agents/ph1-strategy/pattern-recommender-test-report.md`) est un dry-run statique de l'agent contre 3 briefs fictifs (physio, avocat, resto plant-based). Cette exécution Ph1 s'inscrit dans la lignée des évaluations « AMBIGU » documentées : règle d'or PASS via opposition cross-secteur (electro-maitre), brief riche compensant un mapping sectoriel dégradé. Aucun nouvel artifact de test-report n'est produit ici (document = base de connaissance, pas livrable runtime).

---

## Prochain jalon

**Phase 2 — Design** : exécution `agents/ph2-design/_orchestrator.md` avec :

- Ancrage 6D verrouillé (`D1=3, D2=emotional, D3=heavy, D4=warm, D5=slow-organic, D6=symmetric`)
- Palette imposée verrouillée (zéro dérive corporate tolérée)
- Patterns prioritaires P01, P02, P08, P09, P13, P17, P20 (+ P03 secondaire) à matérialiser visuellement
- Vérification active du contraste accent `#FFD700` (déjà flagué `D6_a11y_critical`)
- Section-manifest.json mis à jour : `lifecycle.ph2_designed = <timestamp>` pour les 17 sections après la passe design.
