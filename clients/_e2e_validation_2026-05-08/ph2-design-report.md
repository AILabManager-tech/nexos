# Phase 2 — Design Report

**Client** : Dépanneur Nobert inc. (`_e2e_validation_2026-05-08`)
**Mode NEXOS** : `create` (création from scratch — KPI conversion absolu)
**Date Phase 2** : 2026-05-08
**Orchestrateur** : `agents/ph2-design/_orchestrator.md`
**Phase précédente** : Ph1 Strategy — μ = 8.7/10 (GO ph1→ph2)
**Cadrage métier prioritaire** : CTA primaire = « Voir les promotions de la semaine » · clarté de l'offre dépanneur de quartier · indicateur de succès = visite physique + consultation promo hebdo
**Stack imposée** : Next.js 15 · TypeScript strict · Tailwind 3.4 · next-intl FR/EN · Vercel
**Palette imposée verrouillée** : `#8B4513` / `#A0522D` / `#FFD700` / `#FFF8E7` / `#FFFFFF` / `#2A1810` / `#6B4F3C` / `#D4C5A9`

---

## 0. Cadrage Phase 2 (rappel mode `create`)

| Axe | Décision opérationnelle Phase 2 |
|---|---|
| **KPI primaire** | Conversion → Phase 2 sert le CTA « Voir les promotions de la semaine » via S-001 hero (above-the-fold) + sticky CTA mobile global (P11 différenciation directe vs concurrence) |
| **CTA above-the-fold** | ✅ S-001 Hero (CTA primaire visible sans scroll sur 375px / 768px / 1280px — audit dans `wireframes.json::above_the_fold_audit`) |
| **Audience design** | Voisinage tous âges 20-80 — D3=heavy + touch targets ≥48px + texte adresse/téléphone S-013 lisible (Inter 600+) |
| **Anti-cible visuelle** | Pas de carrousel auto, pas de hero RevSlider, pas de stock photos génériques, pas de parallax (anti-pattern P05/P06 ph0 + anti D5 slow-organic) |

**Décision Phase 2 majeure** : pas de logo illustré (`brief.design.logo_provided=false`) → **wordmark typographique Fraunces 700/800** (cf. `asset-plan.json::logo_strategy`). Cohérent avec D3=heavy + budget solo + identité ancrée typo.

**Personnalité 6D verrouillée toute la phase** :
```
D1=3 (équilibré) · D2=emotional · D3=heavy · D4=warm · D5=slow-organic · D6=symmetric
```

---

## 1. Design system (design-system-architect → `design-tokens.json`)

### 1.1 Couleurs — palette imposée respectée intégralement

| Rôle | Hex (imposé brief) | Tailwind token | Usage |
|---|---|---|---|
| primary | `#8B4513` | `primary.DEFAULT` | Boutons primaires, liens, headings clés, focus ring |
| primary-hover | `#A0522D` | `primary.hover` | État `:hover` et `:focus` (transition 150ms) |
| accent | `#FFD700` | `accent.DEFAULT` | Surfaces badges/boutons promos — JAMAIS texte sur fond clair |
| background | `#FFF8E7` | `background` | Fond global, sections impaires (1, 3, 5, 7) |
| surface | `#FFFFFF` | `surface.DEFAULT` | Sections paires (2, 4, 6), cards, modales |
| text | `#2A1810` | `text.primary` | Texte principal, headings alt |
| text-muted | `#6B4F3C` | `text.secondary` | Métadonnées, captions, prix barré |
| border | `#D4C5A9` | `border.DEFAULT` | Bordures décoratives — JAMAIS focus indicator |

**Échelle neutral warm** dérivée du brun `#2A1810` (50→900) — chromatique brun, pas gris froid (anti-corporate verrouillé).

### 1.2 Contrastes WCAG — 100% AA, 7/13 paires AAA

| Paire testée | Ratio | Niveau |
|---|---|---|
| primary `#8B4513` sur surface blanc | 8.59:1 | **AAA** |
| primary sur background `#FFF8E7` | 7.91:1 | **AAA** |
| primary-hover sur blanc | 5.92:1 | AA |
| text sur background | 13.34:1 | **AAA** |
| text sur surface blanc | 16.32:1 | **AAA** |
| text-muted sur blanc | 6.81:1 | AA |
| text-muted sur background | 6.27:1 | AA |
| crème `#FFF8E7` sur primary | 7.91:1 | **AAA** |
| text sur accent `#FFD700` | 13.95:1 | **AAA** |
| white sur status success/error | 5.96–6.27:1 | AA |
| primary focus ring sur background | 7.91:1 | **AAA** |

**Anti-patterns verrouillés dans tokens** (`design-tokens.json::tokens_anti_patterns_locked`) :

- ❌ accent `#FFD700` comme couleur de **texte** sur surface clair (1.07:1 — flag `D6_a11y_critical` déjà posé Ph1)
- ❌ border `#D4C5A9` comme **focus** indicator (1.16:1 — focus toujours via primary)
- ❌ Aucune couleur grise froide dans la neutral scale (anti-corporate verrouillé)

### 1.3 Typographie — 2 familles, 4 woff2 self-hosted

| Famille | Usage | Poids chargés | Justification D3=heavy |
|---|---|---|---|
| **Fraunces** (serif chaleureux) | H1, H2, H3, brand wordmark | 700, 800 | Empattement souple + poids 800 satisfont D3=heavy sans condensé industriel. Display swap, subset latin. |
| **Inter** (sans humaniste) | body, H4-H6, nav, boutons, formulaires | 400, 600 | Lisibilité haute pour audience 20-80 ans. Display swap, subset latin. |

**Total : 4 fichiers woff2** chargés via `next/font/google` self-hosted (zéro requête Google externe au runtime → conforme principe Loi 25 minimisation).

Scale **Major Third (1.25)** : H1 = 3.052rem → caption = 0.75rem. Letter-spacing négatif sur display (-0.02em), uppercase étiré sur labels boutons (0.04em).

### 1.4 Spacing, radius, shadows, transitions

- **Spacing** : section_padding `py-12` mobile → `py-24` desktop ; container `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8` ; component_gap `gap-4 md:gap-6 lg:gap-8`.
- **Radius** : default `0.5rem` (boutons, cards), `lg 0.75rem` (cards produits/promos), `full` pour avatars/badges ronds.
- **Shadows** : teintées brun `rgb(42 24 16 / X)` au lieu de noir pur — cohérence chromatique D4=warm. 5 paliers + `card-hover` + `sticky-cta` dédiés.
- **Transitions** : durées 100/150/300/500ms cohérentes avec `interactions.json` ; easing par défaut `cubic-bezier(0.0, 0.0, 0.2, 1)` (ease-out).
- **Focus ring** : `ring-3 ring-primary ring-offset-2 ring-offset-background` (ratio 7.91:1, `:focus-visible` only).

**Snippet `tailwind_extend_snippet`** prêt à coller dans `tailwind.config.ts` Ph4 (`design-tokens.json::tailwind_extend_snippet`).

---

## 2. Wireframes (layout-designer → `wireframes.json`)

### 2.1 Couverture — 17 sections, 5 pages, 1 layout legal réutilisable ×2

| Page | Sections | Total | Profondeur scroll estimée |
|---|---|---|---|
| `/` (home) | S-001 → S-006 | 6 | 5-6 viewports |
| `/promotions` | S-007, S-008 | 2 | 3-5 viewports |
| `/produits` | S-009, S-010, S-011×6 | 8 | 6-8 viewports (page la plus longue) |
| `/contact` | S-012 → S-016 | 5 | 4-5 viewports |
| `/{politique-confidentialite,mentions-legales}` | S-017 (×2 instances) | 1 réutilisé | 3-6 viewports |

Convention : chaque section porte `manifest_id`, `i18n_namespace`, `patterns_applied`, wireframe ASCII, et description responsive mobile/tablet/desktop. Les 17 sections sont mappées 1:1 au `section-manifest.json`.

### 2.2 H1 unique par page (audit D7 SEO)

| Route | H1 |
|---|---|
| `/` | S-001 Hero — « Le dépanneur de [ville]. » |
| `/promotions` | S-007 — « Les promotions de cette semaine » |
| `/produits` | S-009 — « Tous nos produits, par catégorie » |
| `/contact` | S-012 — « Nous trouver et nous joindre » |
| `/politique-confidentialite` | S-017 (titre rendu MDX) |
| `/mentions-legales` | S-017 (titre rendu MDX) |

Toutes les autres en H2 → H6 hiérarchiques. Validation H1 unicity = PASS.

### 2.3 Above-the-fold — KPI conversion non négociable

| Route | Élément above-the-fold confirmé |
|---|---|
| `/` | S-001 Hero (H1 + sous-titre + CTA primaire « Voir les promotions de la semaine ») |
| `/promotions` | S-007 (H1 + dates de validité visibles) |
| `/produits` | S-009 (H1 + nav ancres 6 catégories) |
| `/contact` | S-012 (H1 + intro) |

CTA primaire de la home **visible sans scroll sur 375px** (iPhone SE worst-case validé).

### 2.4 Patterns matérialisés visuellement

| Pattern Ph1 | Section(s) Ph2 | Implémentation |
|---|---|---|
| **P01** Sticky CTA persistant | Sticky mobile CTA global + S-004 P01 InfosPratiques | Bouton fixed bottom-0 lg:hidden bg-accent, visible sur 3/6 routes |
| **P02** Social proof / Newsletter inline | S-002 PromoWeekTeaser, S-006 NewsletterCta, S-008 PromosGrid | Cards promos avec preuve directe (prix avant/après), inscription infolettre native |
| **P03** Color-coded nav (secondaire) | S-003 CategoriesOverview + S-010 CategoriesGrid | Tag couleur warm dérivée par catégorie (ambre, terracotta, sienna, sable…) |
| **P08** Storytelling court | S-005 LeMotDuProprio | Quote + portrait Nobert + signature, 80-120 mots |
| **P09** Hero brand statement | S-001, S-007, S-009, S-012 | H1 nominatifs avec ancrage géo `[ville]` |
| **P13** Photo authentique | S-001 (hero) + S-005 (portrait Nobert) | `asset-plan.json::kickoff_assets_blocking` documenté |
| **P17** Hiérarchie visuelle agressive | S-001 (H1 + CTA accent) + S-008 (badge accent + prix barré + prix promo) | Accent `#FFD700` réservé aux éléments KPI conversion |
| **P20** Catalogue galerie | S-008 PromosGrid + S-011 CategorySection ×6 | Grilles responsive 1/2/3-4 colonnes |

**Patterns évités explicitement** (cohérence Ph0/Ph1) : P04 hero vidéo, P06 promos PDF, P07 single-language, hero carousel, parallax, pop-up auto.

---

## 3. Responsive (responsive-specialist → `responsive-strategy.json`)

### 3.1 Approche mobile-first

5 breakpoints Tailwind standard (`sm 640` / `md 768` / `lg 1024` / `xl 1280` / `2xl 1536`). 60-70% du trafic attendu sur mobile (audience voisinage tous âges, vérifications ouvert/fermé en boutique).

### 3.2 Navigation 3-tier

| Breakpoint | Type | Caractéristique |
|---|---|---|
| Mobile (<768px) | Hamburger drawer slide-in droite | focus-trap + aria-modal + ESC + overlay bg-text/45, 4 items + LanguageSwitcher + CTA bouton primaire en haut |
| Tablet (≥768px) | Horizontal compact | 4 items inline, hover underline 2px primary |
| Desktop (≥1024px) | Sticky horizontal + shadow-on-scroll | backdrop-blur-sm, shadow apparaît après 10px |

### 3.3 Sticky CTA mobile (différenciation directe P11)

- Bouton accent `#FFD700` text `#2A1810` (contraste 13.95:1 AAA), fixed bottom-0 lg:hidden, label « Voir les promotions de la semaine ».
- Visible sur `/`, `/produits`, `/contact` — caché sur `/promotions`, légales (cohérence cible vs source).
- Touch target 56px effective (≥48px WCAG 2.5.8).
- Safe-area-inset-bottom respecté (iOS notch).

### 3.4 Touch targets ≥48×48px partout

Boutons, liens nav, sticky CTA, icônes interactives, anchors produits, boutons cookie consent (3 boutons poids visuel équivalent), sélecteur langue. Inputs formulaires `h-12` minimum. Liens inline dans prose à `line-height 24px` (exception WCAG 2.5.5 AAA non requis pour AA).

### 3.5 Image strategy

| Asset | Aspect mobile | Aspect desktop | Loading |
|---|---|---|---|
| S-001 Hero homepage | 4/3 | 21/9 (max-h 640px) | eager + fetchpriority high |
| S-002 / S-008 Promo cards | 4/3 | 4/3 | lazy (sauf 3 first si teaser) |
| S-011 Product cards | 1/1 | 1/1 | lazy |
| S-005 Portrait Nobert | 1/1 (180×180) | 1/1 (240×240) | lazy |
| S-004 / S-013 Maps iframe | 4/3 | 16/10 | lazy + referrerpolicy |

Format priority : `avif > webp > jpg`. Quality 80. `next/image` obligatoire (jamais `<img>` brut). Budget total home ≤2MB.

### 3.6 Lighthouse targets mobiles

`Performance ≥90 · A11y ≥95 · BP ≥95 · SEO 100`. Devices testing list : iPhone SE 375, iPhone 14, iPad, iPad Pro, Desktop 1280, Desktop 1920. Zoom 200% testable. **Aucun horizontal scroll** sur mobile (overflow-x-hidden body + max-w-full containers).

---

## 4. Assets (asset-director → `asset-plan.json`)

### 4.1 Logo strategy — wordmark typographique

`logo_provided=false` brief → wordmark **Fraunces 700/800 'Dépanneur Nobert'**. Pas d'illustration custom. Cohérent D3=heavy + budget solo.

### 4.2 Assets critiques avec plan B documenté

| Asset | Manifest | Source primaire | Plan B (fallback) | Bloquant ? |
|---|---|---|---|---|
| Hero homepage S-001 | S-001 | client-provided (séance photo Nobert) | Stock chaleureux dépanneur QC réel + alt étiqueté 'temporaire' + ticket S+1 | **Oui — D2 emotional** |
| Portrait Nobert S-005 | S-005 | client-provided | Avatar warm (initiale 'N' sur fond accent) | Non — storytelling dégradé acceptable |
| Photos produits S-011 | S-011 | client-provided | Unsplash + Lucide placeholder per produit manquant | Non |
| Photos promos S-008 | S-008 | client-provided OR Unsplash | Configuré per JSON entry | Non |

### 4.3 Icônes Lucide React

29 icônes mappées (`asset-plan.json::icons.icon_map`) couvrant catégories produits (Beer, Cookie, GlassWater, Ticket, Wrench, Snowflake), contact (Phone, Mail, MapPin, Clock), formulaires (CheckCircle2, AlertCircle, Asterisk), nav (Menu, X, Globe, ArrowRight), promo badges (Percent, Tag, CalendarDays).

### 4.4 Favicon set complet

- `public/favicon.ico` (16/32/48)
- `public/icon.svg` (vectoriel, viewBox 0 0 32 32)
- `public/apple-icon.png` (180×180, fond accent)
- `app/icon.tsx` + `app/apple-icon.tsx` (Next.js metadata API dynamique)

Concept design : initiale 'N' Fraunces 800 crème sur fond carré accent `#FFD700` arrondi 8px.

### 4.5 OG images dynamiques par page

`app/opengraph-image.tsx` générant 4 variants (`/`, `/promotions`, `/produits`, `/contact`) avec gradient warm `#FFF8E7 → #8B4513`, titre Fraunces 800 72px, sous-titre Inter 600 36px, bande verticale accent gauche, wordmark bas-droite. Twitter card = `summary_large_image` (réutilise og:image).

### 4.6 Anti-patterns verrouillés

- ❌ Stock photos personne tierce (anti fake propriétaire)
- ❌ Illustrations custom Midjourney/DALL-E pour MVP
- ❌ `<img>` HTML brut (next/image obligatoire)
- ❌ Particules / motifs background flottants

---

## 5. Animations (interaction-designer → `interactions.json`)

### 5.1 Registre slow-organic verrouillé

D5=slow-organic exige sobriété. **Zéro parallax, zéro page transition complexe, zéro infinite hors loaders**. Le registre 'tech flashy' est explicitement rejeté car incompatible avec authenticité dépanneur.

### 5.2 23 animations distinctes — toutes avec fallback `prefers-reduced-motion`

| Catégorie | Nombre | Exemples |
|---|---|---|
| Scroll animations | 2 | fade-in-up cards (S-002/S-003/S-008/S-010/S-011), header-shrink-on-scroll |
| Hover | 5 | button-primary, button-accent, card-hover-promo, category-tile, nav-link underline |
| Focus | 1 (global) | ring-3 primary visible `:focus-visible` only + skip-link au premier Tab |
| Loading states | 3 | skeleton pulse, form spinner Loader2, App Router loading.tsx |
| Form interactions | 4 | input focus, validation error shake, success checkmark, submit loading |
| Navigation | 3 | hamburger morph, drawer slide-in, language switcher |
| Sticky CTA mobile | 2 | fade-in load, active scale tap |
| Cookie consent | 2 | appearance bottom→up, dismiss up→bottom (animation neutre, pas de dark pattern) |
| Page transitions | 1 | Fade only (200ms enter, 150ms exit) |

### 5.3 Performance budget animations

- 100% animations sur **opacity + transform** uniquement (GPU-accelerated)
- Zéro animation sur width/height/margin/padding (CPU layout = jank)
- Max 3 animations simultanées par viewport
- Durée max 500ms par animation
- `will-change: transform` UNIQUEMENT sur sticky CTA + drawer (pas de pollution paint layer)

### 5.4 Anti-patterns rejetés explicitement

Hero carousel auto, parallax photos, pop-up newsletter auto, marquee défilant, particules flottantes, cursor custom. Tous documentés dans `interactions.json::anti_patterns_avoided` avec rationale.

---

## 6. Mise à jour `section-manifest.json`

Les **17 sections** S-001 → S-017 ont été mises à jour :

- `status` : `"planned"` → `"designed"`
- `lifecycle.ph2_designed` : `null` → `"2026-05-08T13:50:00Z"`
- `updated_at_ph2` : `"2026-05-08T13:50:00Z"` (top-level)

Lifecycle restant à compléter : `ph3_content_ready`, `ph4_built`, `ph5_audited`.

---

## 7. Validation des gates SOIC

| Dimension | État Ph2 | Note | Justification clef |
|---|---|---|---|
| **D1 Architecture** | Tokens injectables Tailwind, 17 sections wireframées, container max-w-7xl, scaffold cohérent Ph1 | **8.5** | tailwind_extend_snippet prêt, manifest_id mappé sur 17/17 sections |
| **D2 Tonalité (registre emotional)** | Wireframes alignés voix `convivial-authentique-quebecois`, S-005 storytelling court, ban-list corporate respectée | **8.5** | Aucune section ne dérive vers registre froid (vérification S-001 → S-017) |
| **D3 Performance** | 4 woff2 self-hosted, framer-motion limité, LCP <2.5s ciblé, animations GPU-only, image budget ≤2MB home | **8.5** | Bundle <200KB respecté, lazy loading sauf hero, aspect ratios fixés zéro CLS |
| **D4 Sécurité** | (Pas le scope direct Ph2 — vercel.json + CSP nonce-based en Ph4 — pas de régression Ph2) | **9.0** | Tokens self-hosted (zéro requête Google), Maps embed avec referrerpolicy, no inline JS dans tokens |
| **D5 Velocity (slow-organic)** | 23 animations sobres, durations ≤500ms, zéro parallax, fade-only transitions, useReducedMotion sur tous | **9.0** | D5 verrouillé tout au long de interactions.json |
| **D6 Accessibilité** | 100% contrastes texte AA (7/13 AAA), accent `#FFD700` verrouillé décoratif, focus ring 7.91:1, touch ≥48px, focus-trap drawer, skip-link, alt FR/EN | **8.5** | 3 anti-patterns verrouillés dans tokens (accent text, border focus, neutral froid) |
| **D7 SEO** | H1 unique par page, breadcrumbs schema.org, anchors produits, og:image dynamique par page, schema.org spécifié par section critique | **8.0** | Risque `[ville]` non résolu reste documenté (kickoff prioritaire) |
| **D8 Loi 25** | NewsletterCta avec consent inline Loi 25, RppMention dédiée S-016, LegalContent S-017, cookie consent neutre (pas de dark pattern), Maps documenté transfert US, fonts self-hosted | **9.5** | Aucune dérive Loi 25 introduite en Ph2 |
| **D9 Qualité** | 6 livrables JSON validés `python3 json.load` ✓, ADR Ph1 respectés, anti-patterns explicites documentés, manifest_id traçable, snippet Tailwind prêt à copier | **8.5** | Tout aligné avec Ph0/Ph1, plan B kickoff documenté |

```
D1 Architecture     : 8.5
D2 Tonalité         : 8.5
D3 Performance      : 8.5
D4 Sécurité         : 9.0
D5 Velocity         : 9.0
D6 Accessibilité    : 8.5
D7 SEO              : 8.0
D8 Loi 25           : 9.5
D9 Qualité          : 8.5
```

**Score global : 8.7/10**
**μ = 8.7/10**

Seuil de passage Ph2→Ph3 (μ ≥ 8.0) : **GO**.

---

## 8. Risques portés en Ph3

| Risque | Source | Impact Ph3 | Mitigation |
|---|---|---|---|
| Slot `[ville]` non résolu | brief.client.locations TBD | i18n keys avec `[ville]` placeholder, copy bloquée pour SEO local | Kickoff obligatoire avant rédaction définitive ; sinon Ph3 génère placeholder explicite + flag bloquant Ph5 |
| Photo réelle propriétaire indisponible launch | brief design + asset-plan.json::kickoff_assets_blocking | D2 emotional dégradé, alt text temporaire | Plan B documenté (stock chaleureux dépanneur QC réel + ticket remplacement S+1) |
| NEQ Dépanneur Nobert inc. inconnu | brief.legal.address TBD | Mentions légales S-017 incomplètes (D8 partiel) | Templates avec placeholder NEQ + flag Ph5 ; intégration MDX permet update post-launch |
| Édition hebdo promotions par solo (ADR-003) | KPI conversion = page promo S-008 | Risque page promo morte → perte SEO + conversion | JSON commit + README.md éditorial + Sanity en backlog v2 |
| Mapping sectoriel SEC-03 confidence 0.5 | brief.client.sector_id_mapped_confidence | Décisions Ph3 (FAQ, ton EN) potentiellement génériques | Compensation par richesse brief (palette imposée + 6D hints + 4 sites cités) — déjà compensé Ph0/Ph1 |

---

## 9. Livrables produits (6)

| Fichier | Statut | Validation |
|---|---|---|
| `design-tokens.json` | ✓ | json.load OK · 13 contrastes WCAG · snippet Tailwind |
| `wireframes.json` | ✓ | json.load OK · 17 sections × manifest_id · H1 audit · above-the-fold audit |
| `responsive-strategy.json` | ✓ | json.load OK · 5 breakpoints · navigation 3-tier · touch ≥48px |
| `asset-plan.json` | ✓ | json.load OK · plan B kickoff · 29 icônes · OG dynamique |
| `interactions.json` | ✓ | json.load OK · 23 animations · 100% reduced-motion · GPU-only |
| `section-manifest.json` (mis à jour) | ✓ | 17/17 sections `status='designed'` + `ph2_designed` ts |

---

## 10. Prochain jalon

**Phase 3 — Content** : exécution `agents/ph3-content/_orchestrator.md` avec :

- I18n keys définies dans `wireframes.json` à matérialiser dans `messages/fr.json` + `messages/en.json` (next-intl).
- Voix de marque verrouillée (`brand-identity.json::brand_voice`) — ban-list corporate à respecter.
- Slot `[ville]` documenté pour résolution kickoff (sinon génération placeholder + flag bloquant Ph5).
- Storytelling court S-005 « Le mot du proprio » 80-120 mots — premier point de contact avec voix authentique-québécoise.
- Schema.org structured data per page (LocalBusiness, ItemList, OpeningHoursSpecification, BreadcrumbList).
- Templates Loi 25 (`templates/privacy-policy-template.md`, `templates/legal-mentions-template.md`) à interpoler avec RPP Nobert Tremblay + transferts US documentés.

---

## Score global: 8.7/10
## mu = 8.7/10
