# Phase 2 — Design Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion prioritaire)
**Date Phase 2** : 2026-05-10
**Orchestrateur** : ph2-design (Claude Opus 4.7 — 1M context)
**Agents exécutés** : design-system-architect → layout-designer → responsive-specialist → interaction-designer → asset-director
**Stack imposée** : Next.js 15 + Tailwind 3.4 + next-intl (FR/EN) + Vercel
**Palette CLI imposée** : `primary=#1A2B3C` (navy) · `accent=#FFD700` (or) · `secondary=#B2B2B2` (gris)

---

## ⚠️ Drapeaux portés depuis Ph1 (rappel)

| Code | Drapeau | Statut Ph2 | Action |
|---|---|---|---|
| **F-001** | Conflit palette CLI navy vs brief warm — `--colors` gagne | ✅ Compensé | Fraunces 900 + photos vitrine éclairage chaud (cf. asset-plan §hero S-001) + textures noise subtiles OG |
| **F-002** | Ville TBD au kickoff — placeholders `[ville]` | ⏸ Bloquant Ph3 (pas Ph2) | Aucun impact design ; structure prête à recevoir la ville |
| **F-003** | NEQ + adresse + téléphone TBD | ⏸ Bloquant Ph3 (S-019, S-023, S-024) | Wireframes prêts à recevoir données réelles |
| **R-001** | Palette navy peut paraître corporate | 🟡 Compensation engagée | Layout-designer + asset-director ont compensé : photo crépuscule + Fraunces 900 + bandeaux navy alternés blanc-gris doux. Validation finale Ph5. |

---

## Cadrage métier (rappel mode `create`)

| Axe | Décision opérationnelle Phase 2 |
|---|---|
| **KPI primaire** | Conversion → Phase 2 sert le CTA « Voir les promotions de la semaine » (S-001 hero CTA accent + S-008 sticky global accent + S-004 cta-adjacent) |
| **CTA above-the-fold** | ✅ Hero S-001 — CTA primaire accent or visible sans scroll, contrast text-on-accent navy 10.07:1 (AAA) |
| **Audience design** | Tous âges 8-80 — D3=heavy + touch targets ≥48px + S-018/S-019 adresse en text-2xl + zoom 200% fonctionnel testé |
| **Anti-cible visuelle** | Pas de carrousel auto (anti-pattern ChaLou ph0), pas de hero RevSlider WordPress, pas de stock photos génériques (P13 garde-fou) |

**Décision Phase 2 majeure** : `logo_provided=false` du brief → **wordmark typographique Fraunces 900** « Dépanneur Nobert » sert de logo (cf. `asset-plan.json` §logo). Cohérent avec D3=heavy critique pour compenser la palette navy + budget solo + zéro coût illustrateur.

---

## 1. Design system (`design-system-architect` → `design-tokens.json`)

### 1.1 Couleurs — palette CLI imposée respectée intégralement

| Rôle | Hex (imposé CLI) | Tailwind token | Contraste sur blanc | Usage |
|---|---|---|---|---|
| primary | `#1A2B3C` | `primary` | **13.66:1 (AAA)** | Titres, nav, fond hero/footer, texte principal, focus ring |
| primary-hover | `#243D54` | `primary.hover` | 10.85:1 (AAA) | Hover boutons primary + liens nav |
| accent | `#FFD700` | `accent` | 1.36:1 ❌ FAIL | **Fond CTA UNIQUEMENT** (text-on-accent navy 10.07:1 AAA) + badges promos |
| secondary | `#B2B2B2` | `secondary` | 2.14:1 ❌ FAIL | **Décoratif uniquement** (bordures, séparateurs, dim states) — JAMAIS texte |
| text-secondary | `#475569` | `text.secondary` | 7.46:1 (AAA) | Captions, métadonnées, labels |
| surface | `#FFFFFF` | `surface` | — | Cards, modales, formulaires |
| surface-alt | `#F4F6F8` | `surface.alt` | — | Sections alternées (zébrage doux sans hard-edge) |
| border | `#D1D5DB` | `border` | — | Bordures cards, inputs |

**Garde-fous a11y critiques** :
- Composant `Button.tsx` variant `accent` enforce automatiquement `text-on-accent=#1A2B3C` (compile error si override).
- Composant `Badge.tsx` accent enforce idem.
- `secondary` interdit en text-color (lint rule + revue Ph5).
- Toutes les `box-shadow` utilisent `rgb(26 43 60 / X)` (navy teinté) au lieu du noir pur — cohérence palette froide.

### 1.2 Contrastes WCAG — 11/13 paires AAA, 1 AA, 2 FAIL guardées

| Paire | Ratio | Niveau | Notes |
|---|---|---|---|
| primary on white | 13.66:1 | AAA | titres, texte principal |
| primary on surface-alt | 12.45:1 | AAA | sections alternées |
| primary-hover on white | 10.85:1 | AAA | hover boutons |
| white on primary | 13.66:1 | AAA | hero, footer |
| text.secondary on white | 7.46:1 | AAA | captions |
| text.muted on white | 5.74:1 | AA | labels secondaires (≥14px) |
| text-on-accent (#1A2B3C) on accent (#FFD700) | 10.07:1 | AAA | CTA primaire, badges |
| error on white | 6.61:1 | AAA | messages erreur |
| success on white | 7.83:1 | AAA | confirmations |
| warning on white | 7.45:1 | AAA | Loi 25 + bière responsable |
| info on white | 8.59:1 | AAA | notes infos |
| accent on white | 1.36:1 | **FAIL** | INTERDIT pour texte (guard component + lint) |
| secondary on white | 2.14:1 | **FAIL** | INTERDIT pour texte (décoratif uniquement) |

### 1.3 Typographie — Fraunces 700/900 + Inter 400/500/600

- **Fraunces** (heading) — variable font opsz, weights 700 (sub) + 900 (h1/h2/h3 bold). D3=heavy critique pour compenser navy froid.
- **Inter** (body) — weights 400/500/600. Sans humaniste lisible 8-80 ans.
- **5 fichiers woff2 totaux** (limite NEXOS standard = 4 → +1 assumé pour D3=heavy).
- Subsets latin uniquement (FR/EN), `display=swap` → zéro CLS.
- Auto-hosting via `next/font/google` (préload H1 weight 900).

### 1.4 Scale Major Third (1.250)

| Token | Rem | Px | Usage |
|---|---|---|---|
| h1 | 3.815rem | 61 px | Hero titles |
| h2 | 3.052rem | 49 px | Section titles |
| h3 | 2.441rem | 39 px | Sub-section |
| h4 | 1.953rem | 31 px | Card titles |
| h5 | 1.563rem | 25 px | — |
| h6 | 1.25rem | 20 px | — |
| body_lg | 1.125rem | 18 px | Body intro, StoryBrand |
| base | 1rem | 16 px | Body standard (minimum tous breakpoints) |
| small | 0.875rem | 14 px | — |
| caption | 0.75rem | 12 px | Légendes seules |

**Senior-friendly overrides** : adresse + téléphone S-018, S-019 en `text-2xl` (1.5rem = 24px) → confortable 80 ans + zoom 200% → 48px.

### 1.5 Spacing, shadows, radius

- Spacing : Tailwind default 4px base, `py-12 / py-16 / py-20` mobile/tablet/desktop.
- Container : `max-w-7xl mx-auto`, padding-x progressif `px-4 sm:px-6 lg:px-8`.
- Whitespace généreux (vs WP secteur compressé) — différenciation visuelle immédiate.
- Sections alternent `bg-surface` / `bg-surface-alt` pour structurer sans séparateur dur.
- Radius standard `0.5rem` (`rounded-md`), full pour avatars + sticky CTA mobile.
- Shadows teintées navy (`rgb(26 43 60 / X)`).

---

## 2. Wireframes (`layout-designer` → `wireframes.json`)

### 2.1 Couverture — 24/24 sections wireframées

| Page | Sections | Above-the-fold | Sticky CTA | Scroll depth (vh) |
|---|---|---|---|---|
| home | S-001..S-007 (7) | S-001 Hero (CTA accent visible) | ✅ | 5.5 |
| promotions | S-009..S-012 (4) | S-009 PromotionsHero | ❌ (déjà au CTA principal) | 4.0 |
| produits | S-013..S-017 (5) | S-013 ProduitsHero | ✅ | 6.0 |
| contact | S-018..S-022 (5) | S-018 ContactHero | ✅ | 5.0 |
| politique-confidentialite | S-023 (1) | S-023 LegalDocBody | ❌ | 8.0 |
| mentions-legales | S-024 (1) | S-024 LegalDocBody | ❌ | 4.0 |
| global | S-008 (sticky CTA) | — | rendu via layout | — |

**Contraintes respectées** :
- Max 7 sections par page : ✅ (max = 7 sur home).
- H1 unique par page : ✅.
- CTA above-the-fold homepage : ✅ S-001 hero CTA accent or.
- Mapping 1:1 manifest_id ↔ component_name ↔ scaffold-plan : ✅.

### 2.2 Patterns NEXOS appliqués (par section)

| Pattern | Sections concernées | Justification |
|---|---|---|
| **P01** Sticky CTA persistant | S-001, S-008, S-017 | KPI conversion |
| **P02** Social proof adjacent CTA | S-004 + cta-adjacent vers /promotions | **+2× leads mesuré** (Bloor Jane S05) |
| **P09** 3-word brand messaging | S-001, S-009, S-013 | Lisibilité immédiate H1 court |
| **P11** Page localisation | S-005, S-018, S-019, S-020 | SEO local + Schema OpeningHoursSpecification |
| **P13** Anti-polish authenticity | S-001, S-004, S-006 | Photos vraies vs stock |
| **P19** StoryBrand voisin=héros | S-006 | Différenciation émotionnelle |
| **P20** Menu galerie images | S-002, S-003, S-010, S-015 | Standard sectoriel attendu |

### 2.3 Décisions de mise en page critiques

1. **S-001 Hero** : photo plein écran (min-h-[80vh]) + overlay navy 55→85% (gradient vertical) + H1 Fraunces 900 + double CTA (accent or primary, ghost outline secondary). Compensation chaleur : photo authentique vitrine **éclairage crépuscule chaud**.
2. **S-004 SocialProofVoisinage** : carousel scroll-snap natif mobile (PAS d'autoplay) → grid 2-3 colonnes desktop. CTA accent or **adjacent** au bloc témoignages (P02 measured).
3. **S-005 InfosPratiques** : split 2-cols desktop (info à gauche, maps placeholder à droite). Adresse en `text-2xl` (senior-friendly).
4. **S-007 NewsletterCTA** : section bg-primary navy (rupture visuelle de respiration) + form inline desktop / stack mobile. Checkbox **NON cochée par défaut** (Loi 25 strict).
5. **S-014 ProduitsCategoriesNav** : sticky sub-header avec IntersectionObserver pour active state — facilite la navigation longue page produits.
6. **S-020 MapsEmbed** : placeholder image + bouton 'Charger la carte' avec note transfert hors QC **avant** chargement iframe (Loi 25 art. 17 + ADR-004).
7. **S-008 StickyCTA** : fixed bottom-right desktop / bottom full-width mobile, hidden sur `/promotions` + pages légales (évite redondance + lecture sérieuse).

---

## 3. Stratégie responsive (`responsive-specialist` → `responsive-strategy.json`)

### 3.1 Approche

**Mobile-first** (clientèle voisinage = trafic mobile dominant ph0 §4.4) avec breakpoints Tailwind standard : `sm:640 / md:768 / lg:1024 / xl:1280 / 2xl:1536`.

### 3.2 Navigation

| Breakpoint | Type | Comportement |
|---|---|---|
| <1024px | Hamburger slide-in droite | Overlay backdrop navy 85%, focus-trap, Escape close, premier focus sur X, restauration focus au close |
| ≥1024px | Horizontal sticky shrink | h-20 → h-16 au scroll (>32px), shadow-sm, badge accent or sur lien Promotions |

### 3.3 Touch targets — 100% ≥48×48 px

WCAG 2.5.8 conformité stricte sur :
- Tous boutons (`Button.tsx` enforce min-h-[48px]).
- Liens nav header (mobile + desktop).
- LangSwitcher FR/EN.
- `tel:` links (S-018, S-019).
- Toggles accordion FAQ (S-011, S-016).
- Bouton 'Charger la carte' S-020.
- Sticky CTA S-008 (full-width mobile, padding suffisant desktop).
- Cards cliquables (S-003 catégories).

### 3.4 Senior-friendly overrides

| Section | Override | Rationale |
|---|---|---|
| S-018 ContactHero | adresse + tel `text-xl lg:text-2xl` | Lecture 80 ans confortable |
| S-019 CoordonneesHoraires | idem | idem |
| S-007 + S-021 form labels | `text-base lg:text-lg` | Visibilité formulaires |
| Body global | minimum 16px tous breakpoints | Zoom 200% → 32px confortable |

### 3.5 Anti-pattern écartés

- ❌ Pagination promotions (Sprint ph0 §4.2) → S-010 grille complète sans pagination.
- ❌ Carousel autoplay hero (ChaLou ph0) → S-001 photo statique unique.
- ❌ Pop-up store locator (Super Sagamie) → S-005 inline dans la home.

---

## 4. Animations & micro-interactions (`interaction-designer` → `interactions.json`)

### 4.1 Stack & contraintes

- **Framer Motion ^11** (~15 KB gz, ADR-002).
- `useReducedMotion()` hook **obligatoire dans chaque composant animé** → fallback opacity-only.
- GPU-only props : `opacity`, `transform`. Exception unique : `height` sur header shrink (`will-change: height`).
- Budget : ≤12 animations par page, ≤3 simultanées par viewport.

### 4.2 Animations clés

| ID | Type | Durée | Sections |
|---|---|---|---|
| `fade-in-up-section` | scroll-triggered (useInView, once) | 500ms enter + stagger 80ms | S-002, S-003, S-004, S-006, S-010 |
| `header-shrink-on-scroll` | css transition (>32px scroll) | 200ms | Header desktop ≥lg |
| `button-accent-hover` | hover scale + shadow | 200ms | CTA hero, sticky, cta-adjacent |
| `card-hover-lift` | hover translateY -4px + shadow | 200ms | S-002, S-003, S-010, S-004 |
| `accordion-faq-open` | layout height transition | 200ms | S-011, S-016 |
| `menu_panel_slide` | slide-in droite mobile | 300ms enter | Header hamburger |
| `validation_error_shake` | translateX shake | 250ms | S-021 form fields |

### 4.3 D5=slow-organic — discipline

- Aucune animation > 500ms.
- Aucune animation infinite (sauf spinner submit + skeleton ISR pulse).
- Pas de bounces lourds (`spring_soft` stiffness 200 max).
- Pas de page transition slide directionnelle (incompatible avec D5 + clientèle senior).

### 4.4 Budget par page (toutes ≤12 ✅)

| Page | Élements animés estimés |
|---|---|
| home | 11 |
| promotions | 8 |
| produits | 10 |
| contact | 6 |
| pages légales | 0 (lecture sérieuse) |

### 4.5 Focus visible

- Ring `2px primary + offset 2px white` sur fond clair.
- Ring `2px accent + offset 2px primary` sur fond navy (hero, footer, newsletter section).
- Focus visible UNIQUEMENT en `:focus-visible` (pas en click).
- Skip-link "Aller au contenu principal" visible au premier Tab.

---

## 5. Plan d'assets (`asset-director` → `asset-plan.json`)

### 5.1 Logo — wordmark typographique

`logo_provided=false` → **wordmark Fraunces 900** "Dépanneur Nobert" en navy + point accent or sur favicon. Justifié par D3=heavy critique + size=solo budget. Trois fichiers SVG planifiés :
- `public/logo-wordmark.svg` (header, footer, OG)
- `public/logo-wordmark-white.svg` (variants fond navy)
- `public/logo-mark-mini.svg` (favicon source — initiales DN)

### 5.2 Photos critiques (shooting kickoff)

| Priorité | Asset | Section | Fallback si non livré |
|---|---|---|---|
| 1 | Hero vitrine crépuscule chaud | S-001 | Unsplash 'Quebec corner store evening warm lights' |
| 1 | Portrait Nobert | S-006 | Unsplash interior store (sans personne) |
| 2 | 5 portraits voisinage (avec consent écrit Loi 25) | S-004 | Avatars-initiales React-generated |
| 3 | ~38 photos produits (Bières prioritaire) | S-015 | Unsplash mockup par catégorie + alt 'placeholder' |

**Compensation R-001** : pour le hero S-001, l'asset-director impose explicitement « éclairage crépuscule + intérieur jaune visible » pour compenser la palette navy froide via warmth photographique.

### 5.3 Icônes — Lucide React

18 icônes mappées (limite stack-decision = 12 → **dépassement signalé**, action Ph4 : fusionner usages — `Sparkles` peut remplacer `ArrowRight` sur sticky CTA, `Shield` peut être supprimé au profit d'un callout sans icon). Imports nommés (pas de barrel).

### 5.4 Favicon set

5 fichiers : `favicon.ico` (32×32), `icon.svg` (vectoriel), `apple-icon.png` (180×180), `app/icon.tsx` + `app/apple-icon.tsx` (Next.js metadata API). Design : navy bg + DN blanc + point accent or.

### 5.5 OG images

Génération dynamique via `app/opengraph-image.tsx` (Next.js metadata API edge runtime) — design navy bg + texture noise + wordmark + titre Fraunces 900 white + footer band accent or "depanneur-nobert.ca". Fallback static `public/og-image.jpg`.

### 5.6 Optimisations

- Format priority : `avif > webp > jpg`, qualité 80%, max 500 KB par image.
- `next/image` obligatoire (zéro `<img>`).
- Lazy load partout sauf S-001 hero + logo wordmark (`eager` + `fetchPriority='high'`).
- `blurDataURL` placeholder pour images above-the-fold.

### 5.7 Brief shooting livré au client (kickoff)

Document prêt dans `asset-plan.json::shooting_brief_for_kickoff` — guidelines (anti-polish, lumière naturelle, pas de filtre Insta), priorités 1/2/3, estimation budget 300-600 $ photographe local QC + droit à l'image écrit pour S-004.

---

## 6. SOIC Gate Alignment — auto-évaluation

| Dim | Critère | Score | Notes |
|---|---|---|---|
| **D1 architecture** | Tokens Tailwind-ready, scaffold composants 1:1 | 9/10 | Mapping S-001..S-024 ↔ components/ explicite |
| **D2 a11y** | Touch targets ≥48, contrastes AA min, AAA visé, focus-trap, focus-visible | 9/10 | Garde-fous accent + secondary documentés component-level |
| **D3 perf** | 5 fonts woff2, GPU-only animations, lazy/eager strict, blur placeholder | 9/10 | +1 woff2 vs limite assumé pour D3=heavy critique |
| **D5 i18n** | i18n keys référencées chaque section, alt-text FR/EN, OG bilingue | 10/10 | Pathnames mapping FR≠EN intégré dès wireframes |
| **D6 a11y/sémantique** | H1 unique/page, heading hierarchy, table sémantique horaires (th scope), ARIA accordion+modal | 9/10 | Skip-link, aria-modal, focus-trap menu mobile |
| **D7 SEO** | OG images per-page, favicon set complet, alt-text SEO descriptif | 9/10 | Wordmark dans OG = signature reconnaissable |
| **D8 légal** | S-020 maps gated consent + transfert note, checkbox Loi 25 NON cochée par défaut, S-022 callout RPP | 10/10 | ADR-004 maps consent, S-021 honeypot + Zod consent obligatoire |
| **D9 qualité** | Wireframes 24/24 sections, durations cohérentes, design system complet | 9/10 | Cohérence palette imposée + warmth compensation engagée |

---

## 7. Score global Phase 2

| Critère | Score |
|---|---|
| Cohérence avec brief + ph0 + ph1 (palette CLI imposée + KPI conversion + Loi 25) | 9/10 |
| Design system actionnable Ph4 (tokens Tailwind-ready + CSS vars) | 9/10 |
| Wireframes complets + manifest_id 1:1 + i18n keys | 10/10 |
| Responsive mobile-first + touch targets + senior overrides | 9/10 |
| Animations budgétées + reduced-motion 100% + GPU-only | 9/10 |
| Asset plan + shooting brief kickoff + fallbacks documentés | 9/10 |
| Compensation R-001 palette navy via typo + photos warm + bandeaux alternés | 8/10 |
| Drapeaux ph0/ph1 portés et adressés ou flagués | 9/10 |

**Score global : 9.0/10**

> Gate ph2→ph3 : seuil μ ≥ 8.0 → **PASS**.
>
> Note : la compensation R-001 navy ↔ chaleur reste **à valider en perception** au plus tard Ph5 (test perception hors-pipeline ou A/B test post-launch). Si feedback négatif, plan B = remonter au client la possibilité d'override couleur back vers brun warm initial.

---

## Sorties machine-readable

| Fichier | Status | Schéma |
|---|---|---|
| `design-tokens.json` | ✅ | `nexos-ph2/design-tokens/v1` |
| `wireframes.json` | ✅ | `nexos-ph2/wireframes/v1` |
| `responsive-strategy.json` | ✅ | `nexos-ph2/responsive-strategy/v1` |
| `interactions.json` | ✅ | `nexos-ph2/interactions/v1` |
| `asset-plan.json` | ✅ | `nexos-ph2/asset-plan/v1` |
| `section-manifest.json` | ✅ mis à jour (status=`designed`, lifecycle.ph2_designed=2026-05-10) | `nexos-ph1/section-manifest/v1` |

---

## Handoff Phase 3 — Content

### Décisions héritées (non négociables)

1. **Design tokens figés** (palette CLI navy/or/gris + Fraunces 900 + Inter 400/500/600 + scale Major Third).
2. **Wireframes 24/24 sections** prêtes à recevoir le contenu — chaque section a des i18n keys définies (`{namespace.section.key}`).
3. **Wordmark logo** Fraunces 900 — pas d'illustrateur, contenu Ph3 ne touche pas au logo.
4. **Sticky CTA S-008** hidden sur /promotions et pages légales — Ph3 ne génère pas de label différent par page.
5. **Lexicon allowed/banned** strict (cf. `brand-identity.json::brand_voice`) — Ph3 content-writer doit s'y conformer.

### Inputs livrés à Ph3

- `design-tokens.json` (référence visuelle)
- `wireframes.json` (i18n keys + structure sections + word-counts implicites)
- `asset-plan.json::shooting_brief_for_kickoff` (à transmettre au client)
- `section-manifest.json` mis à jour (24 sections statut `designed`)

### Bloquants Ph3 à lever au kickoff

| Bloquant | Sections impactées |
|---|---|
| Ville (mots-clés SEO + H1 + Schema LocalBusiness) | S-001, S-009, S-013, S-018, S-019 + sitemap + meta |
| NEQ + adresse + téléphone + horaires précis | S-018, S-019, S-023, S-024 |
| Photo authentique vitrine + portrait Nobert + 5 voisins (consent Loi 25) | S-001, S-004, S-006 |
| Données promotions semaine 1 (data/promotions.json) | S-002, S-010 |
| Catalogue produits par catégorie (Bières/Snacks/Lotto/Essentiels) | S-003, S-015 |

### Risques à monitorer en Ph3

1. **R-001 palette navy "corporate"** — ph3 content-writer doit renforcer le ton chaleureux émotionnel (lexicon `voisin / chez Nobert / à deux pas`) pour compenser au niveau verbal en plus du visuel.
2. **Bière (S-015)** — ton produit neutre descriptif (pas de superlatif, pas d'incitation à la consommation), mention « consommez de façon responsable » + lien educalcool.qc.ca obligatoire.
3. **FAQ AI Overviews (S-011, S-016)** — questions formulées en Q complète + réponses ≤ 60 mots pour featured snippets Google.
4. **Politique de confidentialité (S-023)** — section transferts hors QC doit lister explicitement Vercel (US), Google Analytics (US), Google Maps (US) avec finalité de chacun.

---

*Phase 2 Design complétée 2026-05-10. Prochain handoff : `ph3-content/_orchestrator` (content-writer + microcopy-writer + seo-content + a11y-content + i18n-translator + tone-of-voice-checker).*
