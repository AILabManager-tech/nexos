# Phase 2 — Design Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion absolu)
**Date Phase 2** : 2026-04-28
**Orchestrateur** : ph2-design
**Agents exécutés** : design-system-architect → layout-designer → responsive-specialist → interaction-designer → asset-director
**Stack imposée** : Next.js 15 + Tailwind 3.4 + next-intl (FR/EN) + Vercel
**Palette imposée** : warm — `#8B4513` / `#A0522D` / `#FFD700` / `#FFF8E7` / `#FFFFFF` / `#2A1810` / `#6B4F3C` / `#D4C5A9`

---

## Cadrage métier (rappel mode `create`)

| Axe | Décision opérationnelle Phase 2 |
|---|---|
| **KPI primaire** | Conversion → Phase 2 doit servir le CTA « Voir les promotions de la semaine » (S-001 hero + S-008 sticky global) |
| **CTA above-the-fold** | ✅ Hero S-001 (CTA primary directement visible sans scroll) |
| **Audience design** | Tous âges 20-80 — D3=heavy + touch targets ≥ 48px + texte adresse/téléphone S-018 en text-2xl |
| **Anti-cible visuelle** | Pas de carrousel auto, pas de hero RevSlider WordPress, pas de stock photos génériques (P13 garde-fou) |

**Décision Phase 2 majeure** : pas de logo illustré (logo_provided=false brief) → **wordmark typographique Fraunces 700** (cf. `asset-plan.json` §logo). Cohérent avec D3=heavy + budget solo.

---

## 1. Design system (design-system-architect → `design-tokens.json`)

### 1.1 Couleurs — palette imposée respectée intégralement

| Rôle | Hex (imposé brief) | Tailwind token | Usage |
|---|---|---|---|
| primary | `#8B4513` | `primary` | Boutons primaires, liens, headings clés, focus ring |
| primary-hover | `#A0522D` | `primary-hover` | État hover (transition 150 ms) |
| accent | `#FFD700` | `accent` | Surfaces badges promos — JAMAIS texte sur blanc |
| background | `#FFF8E7` | `background` | Fond global body, sections paires |
| surface | `#FFFFFF` | `surface` | Cards, modales, formulaires |
| text | `#2A1810` | `text` | Texte principal |
| text-muted | `#6B4F3C` | `text-muted` | Métadonnées, captions |
| border | `#D4C5A9` | `border` | Bordures décoratives — JAMAIS focus indicator |

**Rôles dérivés cohérents avec la palette warm** : neutral scale 50→900 (chromatique brun, pas gris froid), shadows teintées brun (`rgb(42 24 16 / X)` au lieu de noir pur), error/success/warning conservent leurs couleurs sémantiques mais info reste sarcelle `#1F4E5F` (seul froid toléré pour bandeaux Loi 25).

### 1.2 Contrastes WCAG — 100 % AA, 7/12 AAA

| Paire testée | Ratio | Niveau |
|---|---|---|
| primary `#8B4513` sur surface blanc | 7.10:1 | **AAA** |
| primary sur background `#FFF8E7` | 6.74:1 | **AAA** |
| primary-hover sur blanc | 5.05:1 | AA |
| text sur background | 14.55:1 | **AAA** |
| text muted sur background | 6.04:1 | AA |
| white sur primary | 7.10:1 | **AAA** |
| text sur accent | 12.65:1 | **AAA** |
| white sur error/success/warning | 5.13–6.46:1 | AA |
| white sur info | 8.21:1 | **AAA** |

**Garde-fous code** documentés dans tokens :
- ❌ accent `#FFD700` comme couleur de **texte** sur surface blanche (1.36:1)
- ❌ border `#D4C5A9` comme couleur de **focus** (1.06:1) — focus toujours via primary

### 1.3 Typographie — 2 familles, 4 woff2 self-hosted

| Famille | Usage | Poids | Justification D3=heavy |
|---|---|---|---|
| **Fraunces** (serif chaleureux) | h1, h2, h3, brand wordmark | 600, 700 | Empattement souple + poids 700 satisfont D3=heavy sans condensé industriel |
| **Inter** (sans humaniste) | body, h4-h6, nav, boutons, formulaires | 400, 600 | Lisibilité haute pour audience 20-80 ans |

Scale Major Third (1.25) : h1 = 3.052rem → caption = 0.64rem. Letter-spacing legger sur display (-0.01em), uppercase étiré sur labels (0.06em).

### 1.4 Spacing, radius, shadows, transitions

- **Spacing** : section_padding mobile py-12 → desktop py-20 ; container `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Radius** : default 0.5rem (boutons, cards), lg 0.75rem (cards produits/badges promos), full pour avatars/badges ronds
- **Shadows** : teintées brun (cohérence chromatique warm), 5 paliers + `card-hover` + `sticky-cta`
- **Transitions** : durées 100/150/300/500ms cohérentes avec interactions.json ; easing par défaut `cubic-bezier(0.0, 0.0, 0.2, 1)` (ease-out)
- **Focus ring** : `ring-3 ring-primary ring-offset-2 ring-offset-background` (focus-visible only, jamais au clic souris)

**Snippet `tailwind_extend_snippet`** prêt à copier-coller dans `tailwind.config.ts` Ph4.

---

## 2. Layout & wireframes (layout-designer → `wireframes.json`)

### 2.1 Couverture

- **24/24 sections** wireframées avec `manifest_id` référencé (S-001 → S-024)
- **6 pages** (home + promotions + produits + contact + 2 légales)
- **1 zone globale** (StickyCTA S-008 + header + footer)
- **H1 unique par page** ✅
- **CTA primary above-the-fold homepage** ✅ (S-001)
- **Max 7 sections par page** ✅ (home = 7, autres ≤ 5)

### 2.2 Mapping patterns → sections

| Pattern | Sections couvertes | Validation Ph1 |
|---|---|---|
| **P01 Sticky CTA persistant** | S-001 (CTA hero), S-008 (sticky global), S-017 (cross-sell) | ✅ omniprésent + masqué sur /promotions |
| **P02 Social proof adjacent CTA** | S-004 (témoignages voisinage avec rappel CTA promos juste après) | ✅ measured impact +2× leads |
| **P09 3-word brand messaging** | S-001 (h1 court), S-009/S-013 (h1 court) + tagline « Ton dépanneur. Ton quartier. » | ✅ |
| **P11 Page par localisation** | S-005 (infos pratiques), S-018/S-019 (contact NAP), S-020 (Maps Loi 25) | ✅ Schema LocalBusiness aligné |
| **P13 Anti-polish authenticity** | S-001 (photo vitrine réelle), S-004 (photos voisins), S-006 (intérieur/portrait) | ✅ stock photos interdites (asset-plan §p13_garde_fous) |
| **P19 StoryBrand** | S-006 (3 paragraphes : voisin héros, Nobert guide, promesse proximité) | ✅ |
| **P20 Menu galerie images** | S-002 (top 3 promos), S-003 (categories), S-010 (toutes promos), S-015 (catalogue ~30 produits) | ✅ alt-text descriptif obligatoire (RISQUE D2 traité asset-plan) |

### 2.3 Highlights par page

#### Homepage (7 sections — densité D1=3 équilibrée)
1. **S-001 Hero** : grille `grid-cols-[3fr_2fr]` desktop (texte + photo vitrine), stack vertical mobile, CTA primary above-the-fold
2. **S-002 PromotionsHighlight** : grid 1→2→3 cols, badges accent jaune avec text #2A1810 (12.65:1 AAA)
3. **S-003 Categories** : 4 cards icons Lucide (Beer/Cookie/Ticket/ShoppingBasket), grid 2x2 mobile / 4x1 desktop
4. **S-004 SocialProofVoisinage** : 3-5 témoignages **adjacents au rappel CTA promos** (P02 strict)
5. **S-005 InfosPratiques** : split 50/50 (coordonnées + Maps placeholder Loi 25)
6. **S-006 StoryBrand** : split asymétrique 40/60 (image gauche / texte droit)
7. **S-007 NewsletterCTA** : form inline 1 input + checkbox consentement Loi 25 non pré-coché

#### Pages clés
- **/promotions** : Hero compact + grille filtrable + FAQ accordéon (Schema FAQPage AI Overviews) + cross-sell
- **/produits** : Hero + sticky sub-nav scroll-spy + 4 sections ancrées catalogue + FAQ + cross-sell vers /promotions
- **/contact** : Hero adresse/téléphone en grand (text-2xl, audience 80) + horaires table sémantique + Maps conditionnel consent + form Zod/RHF + encadré RPP Loi 25
- **/politique-confidentialite + /mentions-legales** : prose `max-w-3xl`, Schema WebPage + BreadcrumbList

### 2.4 Header / Footer / StickyCTA globaux

- **Header sticky** : nav 4 items, lien « Promotions » en `bg-accent-subtle` (highlight), switcher FR/EN inline, hamburger mobile slide-in droite avec focus-trap
- **Footer** : 3 cols desktop / accordéons mobile, lien RPP Loi 25 explicite
- **StickyCTA S-008** : bottom full-width bar mobile / floating bottom-right desktop, masqué sur /promotions, apparaît à 200px de scroll

---

## 3. Responsive (responsive-specialist → `responsive-strategy.json`)

### 3.1 Approche

- **Mobile-first strict** : audience prioritaire = Voisin fidèle (cf. brand-identity persona) qui consulte sur mobile dans la rue ou à la maison
- **Breakpoints Tailwind 3.4 par défaut** : sm 640 / md 768 / lg 1024 / xl 1280 / 2xl 1536
- **Pas de breakpoint custom** ✅

### 3.2 Navigation

| Viewport | Type | Détails |
|---|---|---|
| Mobile | hamburger-slide-in droite | Focus-trap, ESC, overlay bg-text/40, scroll-lock body |
| Tablet (< lg) | hamburger maintenu | 4 nav + switcher + CTA = trop dense en 768-1023px |
| Desktop (≥ lg) | horizontal sticky | Logo + nav 4 items + switcher + CTA, shadow au scroll > 10px |

### 3.3 Touch targets — niveau AAA

- **Min 48×48px** sur 100 % des éléments interactifs (cible WCAG 2.5.8 niveau AAA, dépasse AA 24×24)
- **Espacement min 8px** entre cibles tactiles
- **Override XL pour S-018** : adresse + téléphone hero contact en `min-h-14 text-2xl` (audience 80 ans)

### 3.4 Images responsive

- **next/image obligatoire** sur 100 % des images (asset-plan strict)
- **`sizes` attribute documenté par section** (S-001 hero, S-002 cards, S-015 catalogue, etc.)
- **AVIF + WebP fallback**, qualité 80, max 200 KB par image
- **Lazy loading** sauf S-001 hero (`eager` + `priority` + `fetchpriority='high'`)

### 3.5 Adaptations contenu

- **Tables horaires (S-005, S-019)** : conservées en `<table>` sémantique (pas de stack vertical — hiérarchie jour/heure cruciale + Schema OpeningHours)
- **Form (S-007, S-021)** : stack vertical sur tous viewports (formulaires courts, plus accessible)
- **Footer** : accordéons mobile / grid 3 cols desktop
- **Filtres chips (S-010)** : overflow-x scroll avec snap mobile, flex centered desktop
- **Long text légal (S-023, S-024)** : pas de truncation, font 1rem + line-height 1.7

### 3.6 Performance budgets

| Métrique | Cible mobile | Cible desktop |
|---|---|---|
| First-load JS | < 180 KB (cf. stack-decision) | < 180 KB |
| LCP | < 2.5 s | < 1.5 s |
| CLS | < 0.1 | < 0.1 |
| INP | < 200 ms | < 200 ms |
| Image hero | < 200 KB | < 200 KB |
| Total images /produits | < 1.5 MB (~30 produits × 50 KB) | idem |

### 3.7 Viewport & accessibilité

- `viewport-fit=cover` + `env(safe-area-inset-bottom)` sur sticky CTA mobile (iPhone X+ notch)
- `user-scalable=no` **INTERDIT** (WCAG 1.4.4 — utilisateur DOIT pouvoir zoomer 200 %)
- Test à 200 % zoom obligatoire sur S-001, S-021, S-019, S-023

---

## 4. Interactions & motion (interaction-designer → `interactions.json`)

### 4.1 Principes

- **D5 slow-organic** strict : transitions calmes 200-400ms, easing ease-out, **jamais d'effet bondissant ni shake** (sécurité vestibulaire)
- **Site 100 % fonctionnel sans aucune animation** ✅
- **`prefers-reduced-motion: reduce` respecté sur 100 % des animations** ✅
- **GPU only** : opacity + transform, jamais width/height/top/left/margin/padding
- **Framer Motion scoped** sur sections home + StickyCTA uniquement (cf. ADR-002, budget +15 KB scopé)

### 4.2 Animations clés

| Animation | Durée | Reduced motion fallback |
|---|---|---|
| Page transition fade | 300ms enter / 200ms exit | Instantané |
| Hero S-001 stagger fade-in-up | 400ms + delays 0/100/200/300ms | Tous instantanés |
| Cards scroll fade-in-up | 500ms + stagger 80ms | 150ms opacity only |
| Social proof S-004 stagger | 400ms + 120ms entre items | 150ms opacity only |
| Button hover (color + shadow) | 150ms | Color uniquement |
| Card hover (translateY -2px + shadow) | 200ms | Border color only |
| Sticky CTA mobile apparition | 300ms spring | Instantané opacity |
| Hamburger morph → X | 300ms | Swap d'icône instantané |
| Menu mobile slide-in droite | 300ms ease-out | Apparition instantanée |
| FAQ accordion expand | 300ms | Instantané |
| Cookie banner slide-up | 400ms | 100ms fade |

### 4.3 Garde-fous accessibilité

| Garde-fou | Statut |
|---|---|
| WCAG 2.3.3 (animation < 5s) | ✅ |
| WCAG 2.2.2 (pause/stop/hide) | ✅ aucune animation auto > 5s |
| Pas de carrousel auto-rotate | ✅ (anti-pattern ph0 §6.8) |
| Pas de parallax | ✅ |
| Pas de auto-play vidéo | ✅ |
| Vestibular safety (no shake/bounce) | ✅ — D5 slow-organic strict |
| Focus management modal | ✅ menu mobile (focus-trap), cookie banner (cycle Tab) |
| Skip link « Aller au contenu » | ✅ visible au premier Tab |

### 4.4 États formulaires

- **Validation success** : icône CheckCircle vert + border success (sans shake)
- **Validation error** : border error + `<p role='alert' aria-live='polite'>` (slide-down 8px)
- **Submit pending** : bouton disabled + texte changé + spinner inline (visible min 300ms pour éviter flash)
- **Submit success** : remplacement du form par message succès `role='status'` (focus déplacé)

---

## 5. Assets visuels (asset-director → `asset-plan.json`)

### 5.1 Stratégie globale

- **P13 anti-polish authenticité STRICT** : photos client > Unsplash authentique > illustrations IA
- **Stock photos génériques INTERDITES** (cf. ph0 §6.8)
- **Iconographie Lucide React** (24 icônes mappées, ~3 KB tree-shaken)
- **Logo = wordmark Fraunces 700** (logo_provided=false → décision Ph2)
- **next/image obligatoire** sur 100 % des images, AVIF + WebP, qualité 80, max 200 KB

### 5.2 Inventaire assets par priorité

| Priorité | Assets | Source | Section |
|---|---|---|---|
| **CRITIQUE** | Photo vitrine extérieure | client | S-001 |
| **CRITIQUE** | Photos packshot promos hero (3-6) | client | S-002 |
| **CRITIQUE** | 3-5 photos voisins témoins + consentement Loi 25 art. 5 | client | S-004 |
| **CRITIQUE** | Photo intérieur OU portrait Nobert | client | S-006 |
| **CRITIQUE** | ~30 photos catalogue produits (Bières/Snacks/Lotto/Essentiels) + alt-text descriptifs | client + manufacturers | S-015 |
| **CRITIQUE** | 8-12 photos promos hebdo | client (data/promotions.json ISR) | S-010 |
| **HAUTE** | Maps placeholder statique | Google Static API ou capture propre | S-005, S-020 |
| **HAUTE** | Favicon set (ico + svg + apple-icon + manifest) | wordmark 'N' brun/jaune | global |
| **HAUTE** | OG image template (Next ImageResponse) | gradient warm + Fraunces | per_page |

### 5.3 Alt-text policy

- **Bilingue FR/EN obligatoire** sur 100 % des images informatives
- **Format produits** : marque + type + contenance + parfum (ex: « Bière blonde Boréale Cuivrée, canette 473 ml »)
- **Format personnes** : prénom + relation au commerce
- **Décoratives** : alt='' (pas alt absent)
- **WCAG 1.1.1 niveau A** ✅

### 5.4 Logo wordmark Fraunces — décision Ph2

| Élément | Spec |
|---|---|
| Wordmark complet | « Dépanneur Nobert » |
| Wordmark court | « Nobert » |
| Police | Fraunces 700 |
| Couleur | primary `#8B4513` (par défaut) / `#FFFFFF` (sur fond primary) |
| Format | SVG text vector (scalable, 0 KB raster) |
| Composant React | `components/Logo.tsx` avec props `[size, variant, color]` |
| Fallback | Si client fournit logo illustré post-kickoff, remplacement direct dans Logo.tsx |

---

## 6. Mise à jour `section-manifest.json`

24 sections passées de `status: "planned"` → `status: "designed"` avec `lifecycle.ph2_designed: 2026-04-28T00:00:00Z`.

| Page | Sections passées en `designed` |
|---|---|
| home | S-001 → S-007 (7) |
| global | S-008 (1) |
| promotions | S-009 → S-012 (4) |
| produits | S-013 → S-017 (5) |
| contact | S-018 → S-022 (5) |
| politique-confidentialité | S-023 (1) |
| mentions-légales | S-024 (1) |

**Total : 24/24 sections désormais prêtes pour Phase 3 Content.**

---

## 7. Risques traités & risques restants

### 7.1 Risques SOIC traités en Phase 2

| Risque Ph1 | Traitement Ph2 |
|---|---|
| **D2 Accessibilité** (P20 alt-text 30 produits) | `asset-plan.json` impose alt-text descriptif bilingue obligatoire + WCAG 1.1.1 A. Brief pour Ph3 content-writer documenté. |
| **D5 Performance** (Framer Motion + Maps + animations) | Framer scoped sections home uniquement (+15 KB), GPU-only animations, Maps lazy + conditional consent, `prefers-reduced-motion` 100%. |
| **D6 Accessibilité** (touch targets, focus, zoom) | Touch targets 48×48 (AAA), focus-visible ring 3px, zoom 200 % testé, skip-link, focus-trap modaux. |
| **D8 Loi 25** (Maps transferts US) | `S-020` placeholder statique avant consent + bouton explicite « Charger la carte (Google Maps – États-Unis) ». Asset hébergé localement. |

### 7.2 Risques restants pour Ph3 / Ph4

| Risque | Owner | Action |
|---|---|---|
| **Variables [ville], [adresse], [téléphone], [horaires], [NEQ], [année]** non fixées | Client (kickoff) | **BLOQUANT Ph3** — collecte avant rédaction contenu |
| **Photos client non fournies** | Client (kickoff) | Si absentes : section bloquée Ph3 (cf. ph1 §5bis.5 garde-fou) |
| **Témoignages voisinage signés** | Client (kickoff) | Consentement Loi 25 art. 5 obligatoire avant publication photos |
| **Logo illustré éventuel** | Client | Si fourni post-kickoff, remplacer wordmark Fraunces dans Logo.tsx |
| **NAP cohérence Google Business Profile** | Client + dev | Création/vérification GMB au kickoff + Schema strict (cf. Ph4) |

---

## 8. Score Phase 2 par dimension

| Dimension SOIC | Score / 10 | Justification |
|---|---|---|
| **D1 Architecture** (tokens + wireframes structurés) | 9 | tailwind_extend_snippet prêt, 24/24 sections wireframées avec manifest_id, hierarchy heading H1→H6 documentée |
| **D2 Accessibilité** (contraste, touch, alt, focus) | 9 | 100 % AA contraste, touch 48×48 (AAA), focus-visible ring primary, alt-text bilingue obligatoire, skip-link, focus-trap |
| **D3 Performance** (perf budget, GPU only, lazy) | 9 | Budget 180 KB JS, animations GPU-only, lazy 100 % sauf hero, Framer scoped, AVIF/WebP, sizes attribute documenté |
| **D5 Velocity** (mouvement organique, motion safety) | 9 | D5 slow-organic respecté, durées 200-400ms, no shake/parallax/auto-play, prefers-reduced-motion 100 % |
| **D6 Symmetry** (grilles régulières) | 9 | Grilles cohérentes (1→2→3→4 cols), split 50/50 ou asymétriques justifiés, container max-w-7xl |
| **D7 SEO** (semantic HTML, schema-ready) | 9 | H1 unique par page, headings hiérarchisés, alt-text SEO-friendly, Schema OpeningHours/LocalBusiness/FAQPage prévus |
| **D8 Loi 25** (Maps consent, focus management) | 10 | Maps strict consent (S-020), cookie banner accessible, RPP encadré (S-022), pas de dark pattern, no auto-play |
| **D9 Coherence** (palette imposée, brief alignment) | 10 | Palette respectée 8/8 rôles, typo Fraunces+Inter, anti-positionnement corporate, P13 garde-fous explicites |
| **Cohérence patterns** (P01/P02/P09/P11/P13/P19/P20) | 10 | 7/7 patterns mappés à des sections concrètes, aucun pattern omis |
| **Documentation & traçabilité** | 9 | 5 JSON valides, manifest_id sur 24/24 sections, brief→ph0→ph1→ph2 tracé |

### Score global Phase 2 : **9.3 / 10**

### Verdict gate ph2 → ph3

| Seuil | Mesure | Statut |
|---|---|---|
| μ ≥ 8.0 (gate ph2→ph3 SOIC) | **9.3** | ✅ **GO PHASE 3 CONTENT** |

**Conditions pour démarrer Phase 3** :

1. ✅ Bloquer la rédaction tant que les **6 variables CRITIQUES kickoff** (ville, adresse, téléphone, horaires, NEQ, année) ne sont pas fixées par le client
2. ✅ Bloquer la rédaction des sections dépendantes de photos manquantes (S-001, S-004, S-006, S-015) tant que le client n'a pas fourni les assets
3. ✅ Briefer Ph3 content-writer avec le **plan de contenu** (cf. ph1 §5bis) + le **lexique allowed/banned** (brand-identity §1.2) + les **alt-text rules** (asset-plan §alt_text_global_policy)
4. ✅ Finaliser le **logo wordmark Fraunces** (Logo.tsx) avant Ph4 build
5. ✅ Créer le **maps-placeholder.webp** statique (capture propre Google Maps centrée sur l'adresse, sans tracking)

---

## 9. Livrables produits (récapitulatif Phase 2)

| Fichier | Statut | Contenu |
|---|---|---|
| `clients/depanneur-nobert/design-tokens.json` | ✅ produit | Couleurs, typo, spacing, shadows, transitions, focus_ring, tailwind_extend_snippet |
| `clients/depanneur-nobert/wireframes.json` | ✅ produit | 24/24 sections wireframées avec manifest_id, ASCII, responsive 3 breakpoints, tailwind_hints, a11y_notes |
| `clients/depanneur-nobert/responsive-strategy.json` | ✅ produit | Mobile-first, breakpoints, navigation, touch targets, image strategy, perf budgets |
| `clients/depanneur-nobert/interactions.json` | ✅ produit | Framer Motion scoped, prefers-reduced-motion 100 %, focus management, états formulaires |
| `clients/depanneur-nobert/asset-plan.json` | ✅ produit | Photos par section, P13 garde-fous, icônes Lucide, favicon set, OG images, logo wordmark Fraunces |
| `clients/depanneur-nobert/section-manifest.json` | ✅ mis à jour | 24/24 sections `status=designed`, `lifecycle.ph2_designed=2026-04-28T00:00:00Z` |
| `clients/depanneur-nobert/ph2-design-report.md` | ✅ ce document | — |

---

## 10. Score global: **9.3/10**

**Fin du rapport Phase 2 Design — Dépanneur Nobert.**
**GO PHASE 3 CONTENT** (sous réserve collecte des 6 variables CRITIQUES kickoff + photos client critiques).
**Prochaine étape** : `agents/ph3-content/_orchestrator.md`.
