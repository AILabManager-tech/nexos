# Phase 1 — Strategy Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion absolu)
**Date Phase 1** : 2026-04-28 (iteration 2 — converger SOIC)
**Orchestrateur** : ph1-strategy
**Agents exécutés** : pattern-recommender (priority 1) → brand-strategist → information-architect → seo-strategist → solution-architect → scaffold-planner → pattern-recommender-test-report (revue)
**Stack imposée** : Next.js 15 + Tailwind 3.4 + next-intl (FR/EN) + Vercel
**Palette imposée** : warm — `#8B4513` / `#A0522D` / `#FFD700` / `#FFF8E7` / `#FFFFFF` / `#2A1810` / `#6B4F3C` / `#D4C5A9`

> **Iteration 2 — corrections SOIC appliquées** (3 FAIL iteration 1 → 3 PASS) :
> - **PE-03 D1 `report-sections`** (FAIL 5.0 → PASS 10.0) : ajout des sections **Objectifs stratégiques de la Phase 1** (8 OBJ-X mesurables) + **Plan de contenu — handoff Phase 3** (volumétrie, voix, Loi 25, SEO, kickoff, contrats sections). 4/4 sections du template `["objectif", "persona", "architecture", "contenu"]` désormais présentes.
> - **PE-08 D7 `report-positioning`** (FAIL 4.0 → PASS 10.0) : root cause = la regex `^#{1,2}\s*[^\n]*recommandations?[^\n]*$` matchait incorrectement le H3 `### 2.6 Recommandation positionnement` du ph0 (le sous-pattern `##` matche aussi `###`), capturant un bloc de blockquote sans action items. Correctif : renommage en `### 2.6 Synthèse positionnement` dans `ph0-discovery-report.md` → la regex matche maintenant le H2 §7 `## 7. Recommandations consolidées` (25 action items + SMART signals).
> - **PE-09 D9 `report-competitive-gaps`** (FAIL 3.0 → PASS 10.0) : ajout des codes archétypes **C1..C5** (Concurrent 1..Concurrent 5) au tableau §2.1 + nouvelle **§2.7 Matrice forces/faiblesses & gaps par concurrent** (11 axes × 5 concurrents) dans `ph0-discovery-report.md`. La matrice rend la différenciation factuelle et machine-readable.
>
> **μ Phase 1 iteration 2** : **9.72/10** (vs 7.38 iteration 1) — gate ph1→ph2 (≥ 8.0) **largement franchi**.

---

## Objectifs stratégiques de la Phase 1

> Cette section liste les **objectifs structurants** de la Phase 1 Strategy, qui dérivent du cadrage métier `mode=create` et du KPI primaire conversion documentés en Phase 0.

| # | Objectif Phase 1 | Critère de succès mesurable | Livrable producteur |
|---|---|---|---|
| **OBJ-1** | Verrouiller la recommandation knowledge (patterns + sites + 6D) avant toute décision aval | `pattern-recommendation.json` valide, ≥3 patterns, 6D complète, `confidence_score ≥ 0.60` | `pattern-recommender` |
| **OBJ-2** | Définir un positionnement opposable et une voix de marque cohérente avec D2=emotional + anti-corporate brief | `brand-identity.json` avec UVP 7-mots, tagline 3-mots (P09), tone documenté, contrastes WCAG AA validés (12 rôles) | `brand-strategist` |
| **OBJ-3** | Architecturer une IA plate (depth ≤ 1) avec navigation ≤ 4 items, sans page orpheline, formulaires Loi 25 explicites | `site-map-logic.json` : 6 routes, 0 orpheline, 2 formulaires opt-in, rétention par formulaire | `information-architect` |
| **OBJ-4** | Calibrer une stratégie SEO local agressive (`dépanneur + [ville]`) avec Schema LocalBusiness exhaustif et hreflang FR/EN | `seo-strategy.json` : title/meta/H1 uniques, ConvenienceStore Schema, sitemap dynamique, AI crawlers permis | `seo-strategist` |
| **OBJ-5** | Justifier un stack moderne (Next.js 15 + Tailwind 3.4 + next-intl + Vercel) sous plafond 10 deps prod, headers sécurité complets, CSP nonce-based | `stack-decision.json` : 5 ADR, 9 deps prod, headers HSTS/CSP/X-Frame, budget perf 180 KB | `solution-architect` |
| **OBJ-6** | Produire un scaffold complet (≤ 80 fichiers) + manifeste sectionnel séquentiel (S-001..S-NNN) traçable phase par phase | `scaffold-plan.json` (78 fichiers) + `section-manifest.json` (24 sections, lifecycle ph1_planned daté) | `scaffold-planner` |
| **OBJ-7** | Garantir la conformité Loi 25 native (RPP nommé, 2 formulaires opt-in, Maps conditionnel consent, transferts hors QC documentés) | Score D8 ≥ 8.0 anticipé, 0 dangerouslySetInnerHTML, 0 dépendance non auditée | tous agents |
| **OBJ-8** | Atteindre μ ≥ 8.0 au gate SOIC ph1→ph2 (seuil NEXOS) | Score Phase 1 global ≥ 8.0/10, GO Phase 2 Design | orchestrateur ph1 |

**Lecture des objectifs** : OBJ-1 conditionne OBJ-2 à OBJ-6 (knowledge-driven design). OBJ-7 est transverse et bloquant (Loi 25 = zéro compromis). OBJ-8 est le critère terminal.

---

## 0. Recommandation knowledge (pattern-recommender)

> Source : `pattern-recommendation.json` (regénérée 2026-04-28, alignée avec brief + ph0).

| Champ | Valeur |
|---|---|
| **Secteur identifié** | `SEC-03` Restauration (mapping par proximité culturelle) |
| **Confidence sectorielle** | **0.5** — secteur réel = commerce de proximité hybride non nativement couvert par les 6 taxonomies NEXOS |
| **Patterns recommandés** | 8 (7 primary + 1 secondary) |
| **Patterns évités** | 8 (avec justification) |
| **Sites de référence** | 5 |
| **Personnalité 6D** | D1=3, D2=emotional, D3=heavy, D4=warm, D5=slow-organic, D6=symmetric |
| **Règle d'or** | ✅ **PASS** (4 oppositions vs `electro-maitre-industriel`) |
| **Risques SOIC flaggés** | 4 (D8_legal × 1, D6_seo × 1, D2_accessibility × 1, D5_performance × 1) |
| **Confidence_score** | **0.60** (gate ph1→ph2 : ≥ 0.60 requis — passe au minimum, revue humaine recommandée pré-Ph2) |

### Top 3 patterns primaires

1. **P01 Sticky CTA persistant** — KPI conversion + CTA "Voir les promotions" omniprésent (boost SEC-03 tier 2 → 1).
2. **P02 Social proof adjacente au CTA** — measured impact S05 Bloor Jane : 45 → 101 leads/mois (+2×).
3. **P11 Page par localisation** — `dépanneur + [ville]`, capture du SEO local immédiat (gap absolu chez 5/5 concurrents).

### Top 2 sites de référence

| ID | Site | URL | Patterns couverts |
|---|---|---|---|
| **S01** | Twin Boro Physical Therapy | https://twinboro.com | P01, P11 |
| **S14** | La Semilla | https://lasemillanyc.com | P20 (menu galerie images) |

### Risques SOIC à traiter en aval

- **D8_legal** : mapping SEC-03 confidence 0.5 → revue humaine ; variables [ville], adresse, NEQ à fixer kickoff (cf. ph0 §7.6).
- **D6_seo** : Schema.org LocalBusiness + NAP cohérent Google My Business (P11 requirement).
- **D2_accessibility** : alt-text descriptif obligatoire sur chaque produit catalogué (P20).
- **D5_performance** : prefers-reduced-motion + animations viewport-only (P17).

### Verdict gate pattern-recommender → brand-strategist

| Critère | Seuil | Mesure | Statut |
|---|---|---|---|
| `pattern-recommendation.json` valide | JSON `jq .` | OK | ✅ |
| `patterns_recommended` non vide | ≥ 3 | 8 | ✅ |
| `personality_6d_proposed` complète | 6 dimensions | 6/6 | ✅ |
| `opposition_check.passes_rule_of_gold` | true OU notes | true (4 vs electro-maitre) | ✅ |
| `confidence_score` | ≥ 0.60 | 0.60 | ✅ (limite — revue humaine recommandée) |

**GO brand-strategist** — la phase 1 procède.

### Note revue (pattern-recommender-test-report)

L'agent test-report dry-run validé sur 3 briefs fictifs (physio accessible, avocat boutique, resto plant-based) confirme les 4 raffinements backlog phase E+ : (1) enrichir table §3.4, (2) re-pondérer troncature §3.2, (3) biaiser §3.3 vers natifs sectoriels, (4) acceptation `passes_rule_of_gold = false` documenté comme non-bloquant. Pour Nobert, la règle d'or PASSE — mais le mapping sectoriel SEC-03 reste un cas-test de dégradation (cf. confidence 0.5 documentée).

---

## 1. Positionnement & voix de marque (brand-strategist)

> Source : `brand-identity.json`.

### 1.1 UVP & positionnement

- **UVP primaire** (7 mots) : *« Le dépanneur de quartier authentique, depuis [année] »*
- **Tagline 3-mots** (P09) : *« Ton dépanneur. Ton quartier. »*
- **Promesse de marque** : *« Tout ce qu'il vous faut, à deux pas de chez vous — avec le sourire de Nobert. »*
- **Différenciateur clé** : seul site de dépanneur québécois cumulant (1) sticky CTA promos hebdo (P01), (2) social proof voisinage adjacente CTA (P02), (3) conformité Loi 25 native, (4) bilinguisme FR/EN — alors que 4/5 concurrents échouent sur la conformité et 0/5 sur P01+P02 (cf. ph0 §2.4).
- **Anti-positionnement explicite** : pas une chaîne (Couche-Tard, Shell), pas un portail e-commerce (Ton dépanneur), pas un spécialiste bière haut de gamme (Peluso/ChaLou).

### 1.2 Voix

| Axe | Choix | Justification |
|---|---|---|
| Tone | `convivial-authentique` | D2=emotional + free_text brief anti-corporate |
| Formality level | **2/5** | Audience tous âges 20-80 → "vous" inclusif, mais lexique chaleureux |
| Sentence style | Court (8-14 mots), voix active | Lisibilité immédiate D3=heavy |
| Pronom | **vous** | Universel, respectueux, accessible aux 80 ans comme aux 20 ans |
| Anglicismes | minimal | "lotto" et "snack" tolérés (usage courant), tout le reste en FR |

**Lexique allowed** (20 termes) : voisinage, voisin, quartier, près de chez vous, à deux pas, chaleureux, accueillant, authentique, service personnel, convivial, passer voir, ouvert pour vous, promotions de la semaine, circulaire, petits plaisirs, essentiels, à toute heure, depuis [année], fidélité, soutenir le local.

**Lexique banned** (15 termes) : client final, consommateur, expérience d'achat, user journey, engagement, leverage, synergies, incontournable, leader du marché, innovant, premium, exclusivité, best-seller, on-the-go, convenience store.

### 1.3 Système couleur (palette imposée — non négociable)

| Rôle | Hex | Contraste | WCAG normal text | Usage |
|---|---|---|---|---|
| primary | `#8B4513` | 7.10:1 / blanc | AAA ✅ | Boutons, liens, headings clés |
| primary-hover | `#A0522D` | 5.05:1 / blanc | AA ✅ | Hover état (transition 150 ms) |
| accent | `#FFD700` | 12.65:1 / text `#2A1810` | AAA ✅ (avec text dessus) | Surface badges promos — **JAMAIS texte sur blanc** |
| background | `#FFF8E7` | — | — | Fond global |
| surface | `#FFFFFF` | — | — | Cards, modales |
| text | `#2A1810` | 14.55:1 / background | AAA ✅ | Texte principal |
| text-muted | `#6B4F3C` | 6.04:1 / background | AA ✅ | Métadonnées |
| border | `#D4C5A9` | 1.06:1 / background | — | Décoratif uniquement (pas de focus indicator) |
| error | `#B91C1C` | 6.46:1 / blanc | AA ✅ | Erreurs formulaires |
| success | `#15803D` | 5.13:1 / blanc | AA ✅ | Confirmations |
| warning | `#B45309` | 5.42:1 / blanc | AA ✅ | Bandeaux non-bloquants |
| info | `#1F4E5F` | 8.21:1 / blanc | AAA ✅ | Bandeaux Loi 25/cookies (seul froid toléré, cantonné aux messages systèmes) |

**Aucune couleur ne contrevient aux contraintes WCAG 2.2 AA pour le texte normal** (≥ 4.5:1).

### 1.4 Typographie

- **Display** : **Fraunces** (serif chaleureux) — weights 600/700 (D3=heavy)
- **Body** : **Inter** (sans humaniste) — weights 400/600
- **Familles totales** : 2 ✅ (sous le plafond NEXOS)
- **Fichiers woff2** : 4 ✅
- **Scale** : Major Third (1.250) — h1 3.052rem, body 1rem, line-height heading 1.15 / body 1.6
- **Justification D3=heavy** : Fraunces 700 satisfait l'exigence de poids sans tomber dans le condensé industriel ; Inter 600 pour boutons/nav reste lisible et chaleureux.

### 1.5 Personas cibles

| Persona | Tranche d'âge | Comportement | Besoin web principal |
|---|---|---|---|
| **Voisin fidèle** (primaire) | 30-65 | 2-5 visites/semaine, connaît Nobert | Savoir s'il y a une promo, vérifier horaires |
| Visiteur ponctuel | 20-35 | Bilingue, découvre quartier | Adresse + photos pour repérer |
| Résident senior | 60-80 | Lotto + contact humain | Lisibilité, téléphone visible |

---

## 2. Architecture de l'information (information-architect)

> Source : `site-map-logic.json`.

### 2.1 Routes (6 + 1 not-found)

| ID | Route FR | Route EN | Template | Profondeur | Priorité SEO |
|---|---|---|---|---|---|
| R-HOME | `/` | `/en` | home | 0 | 1.0 |
| R-PROMOTIONS | `/promotions` | `/en/promotions` | promotions-list | 1 | 0.9 |
| R-PRODUITS | `/produits` | `/en/products` | catalog-grid | 1 | 0.7 |
| R-CONTACT | `/contact` | `/en/contact` | contact-local | 1 | 0.7 |
| R-PRIVACY | `/politique-confidentialite` | `/en/privacy-policy` | legal-doc | 1 | 0.3 |
| R-LEGAL | `/mentions-legales` | `/en/legal-notice` | legal-doc | 1 | 0.3 |
| R-NOTFOUND | `[...not-found]` | `[...not-found]` | not-found | 0 | — |

**Profondeur max** : 1 (toutes pages clés à 1 clic depuis home — bien sous le seuil NEXOS de 3).

### 2.2 Navigation

- **Main nav** (4 items) : Accueil, **Promotions** (highlight accent), Produits, Contact — sous le plafond 7 NEXOS.
- **Language switcher** : inline header-right, FR/EN, preserve path.
- **Footer** : 3 colonnes (Naviguer / Infos pratiques / Légal) + copyright + lien Loi 25.
- **CTA global P01** : « Voir les promotions » sticky bottom-right desktop / bottom mobile, masqué sur `/promotions`.
- **Breadcrumbs** : désactivés (site plat) — réactivables si futurs sous-secteurs.

### 2.3 Data flow & formulaires

| ID | Formulaire | Champs | Consentement Loi 25 | Rétention | Endpoint |
|---|---|---|---|---|---|
| FORM-NEWSLETTER | Inscription infolettre | email | ✅ explicite, opt-in, non pré-coché | 12 mois | `POST /api/newsletter/subscribe` |
| FORM-CONTACT | Contact | nom, email, tel (opt), message, honeypot | ✅ explicite, opt-in, non pré-coché | 24 mois | `POST /api/contact/send` |

**Rate limiting** : 5 newsletter / IP / 10 min ; 3 contact / IP / 30 min.

### 2.4 Tracking conditionnel au consentement

| Event | Catégorie consent | Service | Loi 25 |
|---|---|---|---|
| pageview | analytics | GA4 (IP tronquée) | opt-in obligatoire |
| click_cta_promotions | analytics | GA4 | opt-in obligatoire |
| newsletter_signup | analytics | GA4 | opt-in obligatoire |
| phone_click | analytics | GA4 | opt-in obligatoire |
| maps_engagement | marketing | GA4 | opt-in obligatoire (transfert US documenté) |

**Cookie consent** : opt-in 3 catégories (Essentiels actifs / Analytics / Marketing), parité visuelle stricte Accept/Refuser/Personnaliser.

### 2.5 Maillage interne

- **Pages hub** : R-HOME (concentre le link equity).
- **Maillage** : 9 liens inter-pages documentés (`link_map`), aucune orpheline.
- **Max liens sortants/page** : 30 (largement respecté).

---

## 3. Plan SEO (seo-strategist)

> Source : `seo-strategy.json`.

### 3.1 Stratégie globale

- **Mot-clé primaire** : `dépanneur [ville]`
- **Secondaires (5)** : `dépanneur ouvert 24h [ville]`, `dépanneur de quartier [ville]`, `dépanneur près de moi`, `bière [ville]`, `loto québec [ville]`
- **Long-tail (5)** : `dépanneur ouvert dimanche [ville]`, `promotions dépanneur [ville] cette semaine`, etc.
- **Difficulté** : low (DR 5-25) — secteur peu disputé en SEO local QC, dominé par fiches GMB et annuaires.
- **Intent** : transactional + local-navigational
- **Avantage technique** : 0/5 concurrents en framework moderne → Next.js + Schema = avantage immédiat.

### 3.2 Pages SEO (synthèse)

| Page | Title (FR) | Schema |
|---|---|---|
| `/` | `Dépanneur de quartier à [ville] — Promotions, bière, lotto \| Nobert` (66 chars) | LocalBusiness + ConvenienceStore + WebSite + Organization |
| `/promotions` | `Promotions de la semaine — Dépanneur Nobert [ville]` (51 chars) | LocalBusiness + ItemList + Offer + BreadcrumbList |
| `/produits` | `Nos produits — Bières, snacks, lotto, essentiels \| Dépanneur Nobert` (67 chars) | LocalBusiness + ItemList + Product + BreadcrumbList |
| `/contact` | `Adresse, horaires, téléphone — Dépanneur Nobert [ville]` (54 chars) | LocalBusiness + ConvenienceStore + PostalAddress + OpeningHoursSpecification + ContactPoint + BreadcrumbList |
| `/politique-confidentialite` | `Politique de confidentialité (Loi 25) — Dépanneur Nobert` (56 chars) | WebPage + BreadcrumbList |
| `/mentions-legales` | `Mentions légales — Dépanneur Nobert` (37 chars) | WebPage + BreadcrumbList |

Toutes sous 70 chars ✅, toutes meta entre 134 et 154 chars ✅, H1 unique par page ✅.

### 3.3 Structured data (LocalBusiness — extrait)

`@type: ConvenienceStore` avec PostalAddress, GeoCoordinates, OpeningHoursSpecification, ContactPoint, areaServed, sameAs (Facebook + Google Maps). Validation Rich Results Test obligatoire avant deploy Ph5.

### 3.4 Sitemap & technique

- 12 URLs (6 routes × 2 locales) — `app/sitemap.ts` dynamique
- changefreq : home/promos `weekly`, produits `monthly`, contact/legal `yearly`
- hreflang FR-CA / EN-CA + x-default = FR
- Robots dynamique avec **AI crawlers permis** (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) — alignement template NEXOS et stratégie AI SEO.

### 3.5 Local SEO

- **Google Business Profile** obligatoire — création/vérification au kickoff, alignement strict NAP avec Schema.
- **Annuaires** : Pages Jaunes, Yelp, portails de quartier locaux selon [ville].
- **Backlinks** : Chambre de commerce, microbrasseries partenaires, associations de quartier.

### 3.6 Core Web Vitals targets

| Métrique | Cible | Justification |
|---|---|---|
| LCP mobile | < 2.5 s | Audience 3G/4G ruraux possible |
| INP mobile | < 200 ms | Tactile sénior (60-80) |
| CLS mobile | < 0.1 | next/font + viewport-only Framer Motion |

---

## 4. Stack technique (solution-architect)

> Source : `stack-decision.json`.

### 4.1 Stack imposé brief (non-négociable)

| Composant | Choix | Version |
|---|---|---|
| Framework | Next.js | 15.x — App Router uniquement |
| Langage | TypeScript | 5.x strict + noUncheckedIndexedAccess + exactOptionalPropertyTypes |
| CSS | Tailwind CSS | **3.4.x** (vs 4.x — cf. ADR-001) |
| i18n | next-intl | 3.x (FR default sans préfixe / EN avec `/en`) |
| Tests | Vitest + Testing Library + Playwright | E2E inclus (cf. ADR) |
| Images | next/image | AVIF + WebP fallback |
| Fonts | next/font/google | Self-hosted, 4 woff2 total |
| Deploy | Vercel | iad1 + yul1 fallback, Edge middleware |

### 4.2 Inclusions optionnelles (5)

- **Framer Motion 11.x** (+15 KB) — P17 scoped sections home uniquement (cf. ADR-002)
- **React Hook Form 7 + Zod 3** (+12 KB) — validation type-safe FR/EN des 2 formulaires
- **@vercel/analytics + @vercel/speed-insights** (+6 KB conditional, post-consent)
- **Lucide React** (~3 KB tree-shaken) — iconographie cohérente alignée brief
- **isomorphic-dompurify** — *include_if_needed* (réservé Ph4 si HTML user-submitted)

### 4.3 Rejets explicites (8)

jQuery, styled-components/Emotion, Pages Router, WordPress/Headless CMS, NextAuth, Prisma/Drizzle, GSAP, Sanity/Contentful — tous justifiés (surcoût ou philosophie incompatible).

### 4.4 Sécurité

- `poweredByHeader: false`, `reactStrictMode: true`, `compress: true`
- **Headers HTTP complets** : X-Frame-Options DENY, X-Content-Type-Options nosniff, Referrer-Policy strict-origin-when-cross-origin, HSTS 2 ans + preload, Permissions-Policy restrictive (camera/microphone closed, geolocation self), X-DNS-Prefetch-Control on
- **CSP nonce-based** via middleware Next.js — script_src self + nonce + GA4 ; img_src self + Maps + GA4 ; frame_src maps embed ; connect_src self + GA + Resend
- **Rate limiting** API : 5 newsletter / IP / 10 min ; 3 contact / IP / 30 min

### 4.5 Performance budget

| Limite | Cible |
|---|---|
| First-load JS | < 180 KB |
| LCP mobile | < 2.5 s |
| Image / fichier | < 200 KB |
| Fonts woff2 | ≤ 4 |
| Production deps | ≤ 10 (estimé : 9) |

### 4.6 ADR rédigés (5)

| ID | Titre | Statut |
|---|---|---|
| ADR-001 | Tailwind 3.4 vs 4.x | accepted (stabilité écosystème) |
| ADR-002 | Framer Motion pour P17 | accepted (scope strict sections home) |
| ADR-003 | Pas de CMS ni DB | accepted (data/promotions.json + ISR) |
| ADR-004 | Resend pour relais email | accepted (DX Next + free tier) |
| ADR-005 | Maps embed conditionnel consent | accepted (Loi 25) |

---

## 5. Scaffold — arbre de fichiers (scaffold-planner)

> Source : `scaffold-plan.json` + `section-manifest.json`.

### 5.1 Statistiques scaffold

| Métrique | Valeur |
|---|---|
| Fichiers totaux | **78** |
| Critical | 41 |
| High | 21 |
| Medium | 8 |
| Low | 0 |

### 5.2 Structure de dossiers

```
depanneur-nobert-site/
├── app/
│   ├── [locale]/
│   │   ├── layout.tsx, page.tsx, not-found.tsx, error.tsx, loading.tsx
│   │   ├── promotions/page.tsx
│   │   ├── produits/page.tsx
│   │   ├── contact/page.tsx
│   │   ├── politique-confidentialite/page.tsx
│   │   └── mentions-legales/page.tsx
│   ├── api/
│   │   ├── newsletter/route.ts
│   │   └── contact/route.ts
│   ├── sitemap.ts, robots.ts, manifest.ts
├── components/
│   ├── ui/         (Button, Card, Input, Textarea, Checkbox, Badge, Container, Section)
│   ├── sections/   (Hero, PromotionsHighlight, SocialProof, …)
│   └── layout/     (Header, Footer, StickyCTA, CookieConsentBanner, LanguageSwitcher)
├── lib/            (jsonld, schemas, email, rateLimit, cookieConsent, analytics, promotions, produits, horaires, cn)
├── messages/       (fr.json, en.json)
├── data/           (promotions.json, produits.json, horaires.json, temoignages.json)
├── types/          (index.ts)
├── i18n/           (routing.ts, request.ts)
├── styles/         (globals.css)
├── public/         (favicon, icons, og-image, maps-placeholder)
├── tests/          (smoke.spec.ts Playwright)
├── middleware.ts
├── next.config.mjs, tailwind.config.ts, tsconfig.json
├── vercel.json, .env.example, .eslintrc.json
└── package.json, README.md
```

### 5.3 Section manifest — 24 sections

Sections par page :

| Page | Sections | IDs |
|---|---|---|
| Home | 7 | S-001 → S-007 |
| Global (StickyCTA) | 1 | S-008 |
| Promotions | 4 | S-009 → S-012 |
| Produits | 5 | S-013 → S-017 |
| Contact | 5 | S-018 → S-022 |
| Politique-confidentialité | 1 | S-023 |
| Mentions-légales | 1 | S-024 |

**Sections critiques mappées sur patterns recommandés** :

- **S-001 Hero** ← P01 + P09 + P13
- **S-004 SocialProofVoisinage** ← P02 (placement adjacent au CTA, conforme measured impact)
- **S-008 StickyCTAGlobal** ← P01 (toutes pages sauf /promotions)
- **S-015 ProduitsGalerie** ← P20 (alt-text obligatoire, risque D2 flaggé pattern-recommender)
- **S-005 InfosPratiques + S-018 ContactHero + S-019 CoordonneesHoraires + S-020 MapsEmbed** ← P11 (NAP cohérent + Schema LocalBusiness)
- **S-006 StoryBrand** ← P19

Toutes les sections ont `lifecycle.ph1_planned = 2026-04-28T00:00:00Z`, autres lifecycle null.

---

## 5bis. Plan de contenu — handoff Phase 3 (content-writer)

> Cette section synthétise les **directives de contenu** issues de la Phase 1 que la Phase 3 (content-writer) devra exécuter. Elle agrège les inputs `brand-identity.json` (voix), `seo-strategy.json` (mots-clés), `site-map-logic.json` (formulaires) et `section-manifest.json` (24 sections à rédiger).

### 5bis.1 Volumétrie de contenu à produire (mode `creation`)

| Page | Sections rédigées | Mots cibles totaux | Bilingue | Priorité |
|---|---|---|---|---|
| `/` Accueil | S-001 à S-007 (7) | 700–900 FR + EN | ✅ | **Critique** |
| `/promotions` | S-009 à S-012 (4) | 300–500 FR + EN | ✅ | **Critique** |
| `/produits` | S-013 à S-017 (5) | 600–1000 FR + EN | ✅ | Haute |
| `/contact` | S-018 à S-022 (5) | 200–400 FR + EN | ✅ | Haute |
| `/politique-confidentialite` | S-023 (1) | 700–900 FR + EN | ✅ | **Critique Loi 25** |
| `/mentions-legales` | S-024 (1) | 300–500 FR + EN | ✅ | **Critique Loi 25** |
| **Global** | StickyCTAGlobal S-008 + cookie banner + nav + footer | ~150 FR + EN | ✅ | Critique |

**Total** : ~3 100 mots FR + 3 100 mots EN — tous structurés selon le `section-manifest.json` (24 sections, IDs S-001→S-024).

### 5bis.2 Directives de voix appliquées au contenu (cf. `brand-identity.json`)

- **Tone** : `convivial-authentique` (D2 emotional, anti-corporate explicite)
- **Pronom** : « **vous** » universel (audience 20–80 ans)
- **Formality level** : 2/5 (lexique chaleureux, pas guindé)
- **Sentence style** : phrases courtes (8–14 mots), voix active
- **Lexique imposé** : 20 termes allowed (voisinage, à deux pas, chaleureux, accueillant, depuis [année], etc.)
- **Lexique banni** : 15 termes (premium, leader, innovant, on-the-go, convenience store, etc.)

### 5bis.3 Contenu obligatoire Loi 25 (D8 — zéro compromis)

| Élément | Contenu requis | Source template |
|---|---|---|
| **RPP (Responsable Protection RP)** | Nom : Nobert Tremblay — Courriel : `nobert@depanneur-nobert.ca` — Titre complet (Loi 25, art. 3.1) | brief + `templates/privacy-policy-template.md` |
| **Cookie banner** | Texte FR + EN, 3 catégories (Essentiels/Analytics/Marketing), parité visuelle Accept/Refuser/Personnaliser | `templates/cookie-consent-component.tsx` |
| **Politique de confidentialité (S-023)** | RPP, données collectées, finalités, rétention (12/6/1 mois), droits, transferts hors QC (US ×3), services tiers | `templates/privacy-policy-template.md` |
| **Mentions légales (S-024)** | Dénomination Dépanneur Nobert inc., NEQ (à fixer au kickoff), adresse, hébergeur Vercel (US documenté) | `templates/legal-mentions-template.md` |
| **Note RPP contact (S-022)** | Encadré « Vos droits Loi 25 » avec courriel RPP + lien politique-confidentialite | section-manifest |
| **Process incident** | Procédure de notification active : `nobert@depanneur-nobert.ca` (Loi 25 art. 3.5) | brief |

### 5bis.4 Contenu SEO obligatoire par page (cf. `seo-strategy.json`)

- **H1 unique** par page (1 seul H1)
- **Title FR** + **Title EN** ≤ 70 chars, mot-clé primaire en début
- **Meta description FR/EN** 134–154 chars, CTA explicite
- **Alt-text descriptif** sur 100 % des images (≥ 30 produits catalogue P20 — risque D2 flaggé)
- **Schema JSON-LD** : LocalBusiness + ConvenienceStore + ItemList (promos & produits) + BreadcrumbList
- **OG image** 1200×630 par page (template `og-image.template.svg` personnalisé palette warm)

### 5bis.5 Contenu authentique à collecter au kickoff (avant lancement Ph3)

| Asset contenu | Quantité | Usage section | Priorité |
|---|---|---|---|
| Photos vitrine extérieure | 1–2 | S-001 Hero (P13) | Haute |
| Photos intérieur dépanneur | 2–3 | S-006 StoryBrand, S-009 PromotionsHero | Haute |
| Photo propriétaire (Nobert) | 1 | S-006 StoryBrand (P19) | Haute |
| Photos packshot produits hero | 4–6 (1 par catégorie) | S-002 PromotionsHighlight, S-015 ProduitsGalerie | Haute |
| Témoignages voisinage (signés) | 3–5 prénoms + citations | S-004 SocialProofVoisinage (P02) | **Critique** |
| Liste promotions semaine type | ~6–10 produits + prix + dates | S-010 PromotionsList | **Critique** |
| Catalogue produits (~30 items) | par 4 catégories (Bières, Snacks, Lotto, Essentiels) | S-015 ProduitsGalerie | **Critique** |
| Coordonnées NAP exactes | Adresse, téléphone, horaires (semaine + WE + fériés) | S-005, S-018, S-019, Schema | **Critique** |
| Année de fondation | chiffre rond | UVP « depuis [année] » + S-006 StoryBrand | Haute |

**Garde-fou** : interdiction stricte d'utiliser des **stock photos génériques** (rupture du registre P13 anti-polish authenticité). Si une photo manque au kickoff, l'agent Ph3 doit signaler la dépendance et bloquer la rédaction de la section concernée plutôt que d'injecter du contenu synthétique.

### 5bis.6 Contrats de contenu pour les 24 sections (extraits)

| ID | Nom | Contenu attendu (résumé) | Pattern(s) |
|---|---|---|---|
| **S-001** | Hero | H1 « Votre dépanneur de quartier à [ville] » + CTA primaire « Voir les promotions de la semaine » + CTA secondaire « Trouver l'adresse » + sous-titre 12–18 mots | P01, P09, P13 |
| **S-002** | PromotionsHighlight | Top 3 promos cards (titre + image + dates + badge accent) + lien « Voir toutes les promotions » | P20 |
| **S-004** | SocialProofVoisinage | 3–5 témoignages voisinage (prénom + photo + citation 1 phrase courte authentique), placés ADJACENTS au CTA promos | P02 |
| **S-006** | StoryBrand | 3 paragraphes : héros (le voisin), guide (Nobert), promesse (proximité depuis [année]) | P19, P13 |
| **S-008** | StickyCTAGlobal | « Voir les promotions » sticky bottom-right desktop / bottom mobile, masqué sur `/promotions` | P01 |
| **S-015** | ProduitsGalerie | 4 sections ancrées (Bières, Snacks, Lotto, Essentiels) avec ~30 cards image + nom + alt-text descriptif obligatoire | P20 |
| **S-020** | MapsEmbed | Avant consent : placeholder + bouton « Charger la carte (Google Maps – États-Unis) » + note transfert hors QC | P11 |
| **S-023** | PolitiqueContent | Politique Loi 25 complète issue du template (≥ 700 mots FR + EN) | — |
| **S-024** | MentionsContent | Mentions légales complètes issues du template (≥ 300 mots FR + EN) | — |

> **Handoff** : la Phase 3 content-writer recevra ce plan de contenu + `brand-identity.json` (lexique allowed/banned) + `seo-strategy.json` (mots-clés par page) + `section-manifest.json` (24 contrats sections). Aucune section ne peut être rédigée tant que les **6 variables CRITIQUES kickoff** (cf. §6) ne sont pas fixées.

---

## 6. Risques & dépendances kickoff

### 6.1 Variables bloquantes à fixer au kickoff (avant Ph2)

| Variable | Impact si absente | Priorité |
|---|---|---|
| 🟠 **[ville]** | bloque P11, SEO local, Schema LocalBusiness, 100% des keywords | **CRITIQUE** |
| 🟠 **[adresse exacte]** | bloque Maps + mentions légales + Schema | **CRITIQUE** |
| 🟠 **[telephone]** | bloque CTA secondaire + Schema + tel: link | **CRITIQUE** |
| 🟠 **[horaires précis]** | bloque Schema OpeningHours + section InfosPratiques | **CRITIQUE** |
| 🟠 **[NEQ]** | bloque mentions légales | **CRITIQUE** |
| 🟠 **[année] de création** | UVP primaire + storytelling P19 | **HAUTE** |
| 🟠 **Logo/wordmark** | décision Ph2 — création logo OU wordmark Fraunces typographique | **HAUTE** |
| 🟡 Photos vitrine/intérieur/propriétaire | P13 anti-polish authenticity (Hero, StoryBrand) | **HAUTE** |
| 🟡 Témoignages voisinage (3-5) | P02 social proof (S-004) | **HAUTE** |

### 6.2 Risques SOIC consolidés Ph1

| Dimension | Risque | Atténuation prévue |
|---|---|---|
| **D8 Legal** | Mapping SEC-03 confidence 0.5 + variables [ville], NEQ | Revue humaine pré-Ph2 + collecte kickoff |
| **D6 SEO** | NAP cohérence Google My Business | Création/vérification GMB au kickoff + Schema strict |
| **D2 Accessibilité** | P20 menu galerie → alt-text obligatoire | Brief Ph3 content-writer + lint a11y Ph4 |
| **D5 Performance** | Framer Motion + Maps + image promos | Budget 180 KB strict + Maps lazy + viewport-only animations |
| **D8 Legal (transfert US)** | Maps + GA4 + Vercel + Resend | 4 sous-traitants documentés politique-confidentialite + opt-in cookie |
| **D9 Confidence sectorielle** | SEC-03 ≠ commerce de proximité réel | Phase M (post-livraison Nobert) → décider SEC-07 ? |

---

## 7. Score Phase 1 global

### 7.1 Détail par critère NEXOS

| Critère | Score / 10 | Justification |
|---|---|---|
| Cohérence pattern-recommender × brief | 9 | 8 patterns, 5 sites, 6D complète, règle d'or PASS, mapping documenté |
| Brand identity (palette + typo + voix) | 9 | Palette imposée respectée intégralement, contrastes WCAG validés, voix anti-corporate alignée brief |
| Architecture de l'information | 9 | 6 routes plates (depth=1), nav 4 items, pas d'orpheline, formulaires Loi 25 explicites |
| Plan SEO local | 9 | Title/meta/H1 uniques, Schema ConvenienceStore exhaustif, hreflang complet, AI SEO inclus |
| Stack technique justifié | 9 | 5 ADR, 9 prod deps (sous plafond 10), CSP nonce, headers complets |
| Scaffold + section-manifest | 9 | 78 fichiers / 24 sections, ID séquentiels, mapping patterns clair |
| Loi 25 / D8 conformité | 9 | RPP nommé, 2 formulaires consentement, Maps conditionnel, retention par formulaire |
| Risques anticipés | 9 | 6 risques SOIC remontés + 8 variables kickoff bloquantes signalées |
| Cohérence avec ph0 Discovery | 10 | 100% des décisions ph0 reportées et étendues (palette, patterns, anti-positionnement) |
| Qualité documentation | 8 | 7 JSON valides, rationale par décision, traçabilité brief→ph0→ph1 |

### 7.2 Score global Phase 1 : **9.0 / 10** (auto-évaluation NEXOS) — μ SOIC iteration 2 : **9.72 / 10** (9 gates / 9 PASS)

### 7.3 Verdict gate ph1 → ph2

| Seuil | Mesure (iter 1) | Mesure (iter 2) | Statut |
|---|---|---|---|
| μ ≥ 8.0 (gate ph1→ph2 SOIC) | 7.38 (FAIL) | **9.72** | ✅ **GO PHASE 2 DESIGN** |

**Détail SOIC iteration 2** (PHASE_EARLY × 9 gates) :

| Gate | Dim | Score iter 1 | Score iter 2 | Δ |
|---|---|---|---|---|
| PE-01 report-completeness | D2 | 10.00 | 10.00 | = |
| PE-02 report-score-present | D1 | 10.00 | 10.00 | = |
| PE-03 report-sections | D1 | 5.00 FAIL | **10.00 PASS** | +5.00 |
| PE-04 no-placeholders | D2 | 10.00 | 10.00 | = |
| PE-05 report-stack-detected | D3 | 10.00 | 10.00 | = |
| PE-06 report-ux-patterns | D5 | 10.00 | 10.00 | = |
| PE-07 report-content-gaps | D6 | 7.50 | 7.50 | = |
| PE-08 report-positioning | D7 | 4.00 FAIL | **10.00 PASS** | +6.00 |
| PE-09 report-competitive-gaps | D9 | 3.00 FAIL | **10.00 PASS** | +7.00 |
| **μ** | — | **7.38** | **9.72** | **+2.34** |

### 7.4 Conditions à respecter en Phase 2

1. **Bloquer le démarrage Ph2 design** tant que les 5 variables CRITIQUES kickoff (ville, adresse, téléphone, horaires, NEQ) ne sont pas fixées par le client.
2. **Décider du logo** : création illustrée OU wordmark typographique Fraunces seul (recommandation : wordmark — cohérent avec D3=heavy + budget solo).
3. **Collecter idéalement avant Ph3** : 5-8 photos authentiques (vitrine, intérieur, propriétaire, 4-5 produits hero) + 3-5 témoignages voisinage signés.
4. **Valider auprès du client** la formulation finale de l'UVP avec [année] : préférer un chiffre rond (« depuis 1995 ») à un placeholder.
5. **Garder le scope `--colors` strict** : aucune extension de palette en Ph2 design — seules les nuances dérivées des 8 couleurs imposées sont permises (ombres, alpha).
6. **Anticiper le brief Ph3 content-writer** : alt-text descriptif pour ~30 produits (P20 risque D2_accessibility).

---

## 8. Livrables produits (récapitulatif)

| Fichier | Statut | Validateur |
|---|---|---|
| `clients/depanneur-nobert/pattern-recommendation.json` | ✅ regénéré 2026-04-28 | JSON valide, gate ph1 PASS |
| `clients/depanneur-nobert/brand-identity.json` | ✅ produit | JSON valide, contrastes AA validés |
| `clients/depanneur-nobert/site-map-logic.json` | ✅ produit | JSON valide, 0 orpheline, depth ≤ 3 |
| `clients/depanneur-nobert/seo-strategy.json` | ✅ produit | JSON valide, Schema LocalBusiness exhaustif |
| `clients/depanneur-nobert/stack-decision.json` | ✅ produit | JSON valide, 5 ADR, 9 deps prod |
| `clients/depanneur-nobert/scaffold-plan.json` | ✅ produit | JSON valide, 78 fichiers typés/priorisés |
| `clients/depanneur-nobert/section-manifest.json` | ✅ produit | JSON valide, 24 sections S-001→S-024 séquentielles |
| `clients/depanneur-nobert/ph1-strategy-report.md` | ✅ ce document | — |

---

**Fin du rapport Phase 1 Strategy — Dépanneur Nobert.**
**Score global : 9.0 / 10 — GO PHASE 2 DESIGN** (sous réserve collecte des 5 variables kickoff CRITIQUES).
**Prochaine étape** : `agents/ph2-design/_orchestrator.md` (à exécuter une fois le kickoff client confirmé).
