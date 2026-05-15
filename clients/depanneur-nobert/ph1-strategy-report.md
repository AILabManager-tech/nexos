# Phase 1 — Strategy Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode** : `create` (from scratch, orientation résultat business)
**Date Phase 1** : 2026-05-14
**Orchestrateur** : Claude Code CLI (Phase 1 NEXOS v4.2)
**Agents exécutés** : pattern-recommender, brand-strategist, information-architect, seo-strategist, solution-architect, scaffold-planner
**Domaine cible** : `depanneur-nobert.ca`
**Stack imposé** : Next.js 15 + Tailwind 3.4 + next-intl + Vercel
**Type** : vitrine bilingue FR/EN — 24 sections (cf. `section-manifest.json`)
**Entrée** : `ph0-discovery-report.md` (2026-05-14 itération 2, μ cible ≥ 8.5/10) + `brief-client.json`
**Itération SOIC** : 2 (corrections PE-08 + PE-09 sur ph0 appliquées — voir §0.7)

> **Note de ré-exécution itération 2** : ce rapport remplace les versions précédentes (2026-04-28, 2026-05-10, 2026-05-14 itération 1). Aligné sur la re-discovery du 2026-05-13 (conflit palette F-001 résolu — `palette_imposed` warm = source de vérité). Itération 2 SOIC : corrections PE-08 (recommandations actionnables Ph0 §7.7 ajoutées — 8 actions SMART numérotées) et PE-09 (concurrents nommés C1–C5 + matrice gaps Ph0 §2.1) appliquées sur `ph0-discovery-report.md`. Les 6 artefacts JSON Ph1 sont régénérés ; le `section-manifest.json` est **préservé** (status=audited après Ph5 précédente, historique non écrasé).

---

## 0. Recommandation knowledge (`pattern-recommender`)

### 0.1 Secteur identifié

| Champ | Valeur |
|---|---|
| Secteur réel | Commerce de proximité — dépanneur indépendant QC |
| Mapping NEXOS | **SEC-03 Restauration** (proximité culturelle) |
| Confiance sectorielle | 0.5 (brief) — overridée à 0.82 par validation Ph0 §7.2 |
| Note | Mapping délibéré pour cas test de dégradation. Override manuel privilégié pour patterns explicites validés (cf. `pattern-recommendation.notes`). |

### 0.2 Patterns recommandés (top 3 primaires)

| ID | Nom | Tier final | Justification |
|---|---|---|---|
| **P01** | Sticky CTA persistant | 1 (boost KPI conv.) | CTA = « Voir les promotions de la semaine ». Sticky global S-008. |
| **P02** | Social proof adjacente au CTA | 1 (mesuré) | +2× leads mesuré Bloor Jane. S-004 SocialProofVoisinage. |
| **P20** | Menu galerie images | 1 (tier natif SEC-03) | Catalogue visuel par catégorie — gap sectoriel (~80% concurrents n'ont rien). |

Autres tier 1 : P08 (Story-first), P09 (3-word brand messaging), P13 (Anti-polish), P17 (Scroll animations). Tier 2 : P19 (StoryBrand, mesuré +420%). Tier 3 slots : P11 (LocalBusiness Schema), P14 (Industry code-breaking anti-corporate). **Évités** : P04 (vidéo non budgétée), P15/P10/P07 (démotion size=solo), P03/P05/P06/P16/P18 (overhead injustifié ou anti-pattern food).

### 0.3 Sites de référence (top 2)

| ID | Site | URL | Patterns | Priority |
|---|---|---|---|---|
| **S13** | Ma'ono | https://maono.com | P09 (3-word + jaune bold + hero photo) | 1 |
| **S14** | La Semilla | https://lasemillanyc.com | P20 (menu galerie) + P14 (code-breaking) | 1 |

Compléments : S11 Noma (P08, P13), S12 Gazzo (P13 anti-polish), S05 Bloor Jane (P02 mesuré).

### 0.4 Personnalité 6D proposée (figée par brief)

| Dim | Valeur | Rationale |
|---|---|---|
| D1_density | **3** (équilibrée) | Catalogue + caractère humain |
| D2_register | **emotional** | Convivialité quartier, anti-corporate |
| D3_typo_weight | **heavy** | Serif chaleureux, lisibilité 65+ |
| D4_palette | **warm** | Brun + jaune + crème, rejet bleu corporate |
| D5_velocity | **slow-organic** | Animations subtiles 0.4–0.6 s |
| D6_structure | **symmetric** | Prédictibilité + lisibilité max |

### 0.5 Test règle d'or (opposition_check)

| vs client | Score | Pass ? |
|---|---|---|
| clinique-aura | 1/6 | ✗ (collision warm+emotional attendue) |
| beaumont-avocats | 3/6 | ✗ |
| **electro-maitre-industriel** | **4/6** | **✓** |
| collectif-nova | 1/6 | ✗ (partiel) |

**`passes_rule_of_gold = true`** — axe documenté : *tradition-chaleureuse-quartier (Nobert) vs technicité-industrielle-mécanique (electro-maitre)*.

### 0.6 Risques SOIC flaggés

1. **D8 Loi 25** stricte — bandeau opt-in + politique + Maps consent-gated (S-020)
2. **D7 SEO** — Schema LocalBusiness/OpeningHours/FAQPage requis. Bloqué tant que ville TBD
3. **D2 Accessibilité** — cible 65+ → WCAG AAA + touch ≥ 48×48 + prefers-reduced-motion
4. **D3 Contenu** — témoignages voisinage avec consentement Loi 25 explicite par personne
5. **D5 Performance** — galerie produits ≤ 500 Ko/image, LCP ≤ 2 s, bundle ≤ 200 KB

**Confiance globale** : 0.82.

### 0.7 Concurrents C1–C5 et gaps exploitables (héritage Ph0 §2)

Référencement strict des 5 archétypes concurrentiels Ph0 (chaque décision Ph1 cite C1–C5 quand applicable) :

| Tag | Archétype | Représentativité | Gap principal exploité par Nobert |
|---|---|---|---|
| **C1** | Dépanneur sans site | ~70 % | SEO local quasi-vide → top 3 « dépanneur [ville] » accessible |
| **C2** | Page Facebook seule | ~25 % | Pas de domaine propre + pas de Schema → différenciation immédiate |
| **C3** | Wix abandonné 2015 | ~3 % | Lighthouse < 40 → différenciation perf + confiance |
| **C4** | Chaîne corporate (Couche-Tard, Shell Select) | 0 % direct (~100 % SERP générique) | Aucun ancrage quartier → positionnement humain anti-corporate |
| **C5** | Boutique premium niche | < 1 % | Ticket élevé + audience étroite → cible voisinage 65+ inexploitée |

Le positionnement Ph1 §1.1 ci-dessous est **directement dérivé** de ces gaps : opposition assumée à C4 (corporate) + dominance facile sur C1/C2/C3 (gap massif) + complémentarité distincte de C5 (cible 65+ vs urbain).

### 0.8 Actions priorisées SMART Ph1 (héritage Ph0 §7.7)

1. **Figer ville + adresse + tel + horaires + NEQ T+24h** (sinon placeholders explicites Ph3) — gate kickoff.
2. **Confidence pattern-recommender ≥ 0.80** (atteint : 0.82) avec override SEC-03 sur les 7 patterns validés P01/P02/P09/P11/P13/P19/P20.
3. **μ Ph1 ≥ 8.5 cible** (gate ph1→ph2 = 8.0) — 6 artefacts JSON requis générés en ≤ 2 h orchestrateur.
4. **Photos vitrine/intérieur/propriétaire** : décision Ph1 attendue (OUI shooting J+15 OU NON fallback Unsplash + shooting Ph6 acté).
5. **Instrumentation KPI** : GA4 opt-in `cta_promo_click` ≥ 35 % cible, `phone_click` ≥ 8 % mobile, `maps_open` ≥ 20 %, Lighthouse Perf ≥ 90, A11y = 100, LCP ≤ 2.0 s, bundle ≤ 200 KB.
6. **Témoignages voisinage** : 3-5 collectés Ph3 avec consentement Loi 25 explicite par personne — sinon S-004 dégradé (-2× leads P02 attendu).
7. **Catalogue produits** : 12 × 4 catégories minimum (48 produits + alt-text + ≤ 500 Ko/image).
8. **Promos hebdo** : template + 8 exemples seed JSON + procédure refresh vendredi (ISR weekly 604800 s).

---

## 1. Positionnement & voix de marque (`brand-strategist`)

### 1.1 UVP primaire (anti-C4, dépasse C1/C2/C3, complète C5)

> **« Votre dépanneur de quartier, à deux pas, ouvert pour vous. »**

UVPs secondaires :
- Promotions vraies, chaque semaine — pas de marketing fancy (gap C1/C2/C3).
- Une équipe que vous connaissez, pas une chaîne anonyme (opposition C4 Couche-Tard/Shell Select).
- Bière, snack, loto et l'essentiel — à votre porte (différenciation C5 urbain premium).

**Recommandations actionnables de positionnement** (extension Ph0 §2.5) :
1. **Occuper l'axe « tradition chaleureuse de proximité »** sur la home (S-001 Hero + S-006 StoryBrand) — phrase d'accroche figée H1 : `Votre dépanneur de quartier à [ville]`. Aucun mot abstrait corporate (synergie/leader/premium proscrits — lexique §1.2). Échec si le ton C4 réapparaît dans la copie Ph3.
2. **Opposer explicitement Nobert à C4 corporate** dans S-006 StoryBrand : structure narrative *voisin = héros, Nobert = guide local* (P19 mesuré +420 % engagement). Photo authentique propriétaire obligatoire (P13, anti-stock). Sans photo : fallback Unsplash thématique + shooting Ph6 acté.
3. **Capitaliser le gap massif C1+C2+C3 sur le SEO local** : H1 + meta + Schema LocalBusiness + OpeningHours dès Ph4 (cible top 3 local pack ≤ 90 jours après mise en ligne, KPI = position GSC `dépanneur [ville]`).
4. **Différencier de C5 boutique premium** par accessibilité 65+ (touch ≥ 48×48, WCAG AAA contrast, body ≥ 16 px) — cible Pa11y = 0 erreur, Lighthouse A11y = 100. Mesure : sessions 55+ ans ≥ 30 % du trafic à J+90.
5. **Marquer le différenciateur Loi 25 conformité native** (gap quasi-total C1/C2/C3 et partiel C4/C5) — bandeau opt-in équilibré + page politique RPP + S-022 ContactNoteRPP. Différenciateur signal sérieux segment 50+.

### 1.2 Brand voice

| Critère | Valeur |
|---|---|
| Ton | convivial-authentique |
| Formalité (1-5) | 2 (familier respectueux) |
| Pronom | « vous » (tous âges, cible 65+) |
| Anglicismes | minimaux (courriel > email, infolettre > newsletter, clavardage > chat) |
| Lexique encouragé (extraits) | votre dépanneur, à deux pas, vrai monde, voisinage, passez nous voir, fidélité |
| Lexique banni (extraits) | synergie, leader du marché, premium, scalable, B2C, ROI |
| Style phrase | court, voix active, impératif encouragé sur CTAs |

### 1.3 Palette (validée WCAG)

| Token | HEX | Contraste vs bg #FFF8E7 | Usage |
|---|---|---|---|
| primary | `#8B4513` | 7.5:1 AAA | CTAs, headers |
| primary-hover | `#A0522D` | 5.4:1 AA | hover/focus |
| accent | `#FFD700` | n/a (texte #2A1810 sur accent = 12.4:1 AAA) | badges promos |
| background | `#FFF8E7` | — | bg principal |
| surface | `#FFFFFF` | — | cards |
| text | `#2A1810` | 14.5:1 AAA | corps |
| text-muted | `#6B4F3C` | 6.2:1 AA | métadonnées |
| border | `#D4C5A9` | n/a (décoratif) | séparations |

États sémantiques : `error #B91C1C` (6.4:1), `success #15803D` (5.0:1), `warning #B45309` (5.6:1), `info #7C2D12` (9.0:1 — anti-bleu volontaire). **Tous AA min, AAA sur surfaces principales.**

### 1.4 Typographie

| Niveau | Famille | Poids | Rationale |
|---|---|---|---|
| Display (H1–H3) | **Fraunces** (Google Fonts) | 600/700/800 | Serif chaleureux contemporain, optical sizing, D3=heavy + D4=warm |
| Body | **Inter** (Google Fonts) | 400/500/600/700 | Sans humaniste, ClearType Windows, lisibilité 16px AAA 65+ |
| Scale | Major Third (1.250) | — | H1 3.052rem desktop / 2.250rem mobile |
| Budget perf | ~95 KB total woff2, preload Fraunces 800 hero | — | display=swap, zero CLS |

### 1.5 Persona cible

- **Primaire** : voisinage 35-65 ans, rayon piéton 800 m + auto 5 km, visite multi-hebdo
- **Secondaire** : aînés 65+ autonomes, sensibilité gros caractères + clavier
- **Tertiaire** : familles soir/weekend, dépannage urgent

Brand promise : **« Ouvert, vrai, accessible — votre dépanneur vous reconnaît. »**

---

## 2. Architecture de l'information (`information-architect`)

### 2.1 Routes (6 pages × 2 locales)

| Page | Route FR | Route EN | Depth | Priority | ISR |
|---|---|---|---|---|---|
| home | `/fr` | `/en` | 0 | critical | — |
| promotions | `/fr/promotions` | `/en/specials` | 1 | critical | **604800 s (weekly)** |
| produits | `/fr/produits` | `/en/products` | 1 | high | 2592000 s (monthly) |
| contact | `/fr/contact` | `/en/contact` | 1 | critical | — |
| politique-confidentialite | `/fr/politique-confidentialite` | `/en/privacy-policy` | 1 | critical-legal | — |
| mentions-legales | `/fr/mentions-legales` | `/en/legal-notice` | 1 | critical-legal | — |

**Profondeur max 1** (sous la limite NEXOS de 3). **Slugs traduits** par locale via next-intl `defineRouting`.

### 2.2 Navigation

- **Main nav (4 items)** : Accueil / Promotions / Produits / Nous joindre + lang switcher
- **Mobile** : hamburger < 768 px, slide-in panel avec items en gros caractères (65+)
- **Footer** : 4 colonnes (Plan / Contact / Légal / Suivez-nous) + copyright + RPP courriel
- **Sticky CTA global (S-008)** : « Voir les promotions de la semaine », visible scroll > 600 px, masqué sur `/promotions`
- **Breadcrumbs** : désactivés (profondeur 1, bruit visuel sans bénéfice)

### 2.3 Formulaires Loi 25

| Form | Section | Champs | Consentement | Rétention |
|---|---|---|---|---|
| **FORM-NEWSLETTER** | S-007 | courriel | opt-in explicite + double opt-in | 12 mois |
| **FORM-CONTACT** | S-021 | nom, courriel, message + téléphone optionnel | opt-in explicite + RPP cité | 6 mois après dernière interaction |

Honeypot obligatoire sur les 2. Rate-limit 5 req/min/IP (cf. ADR-002).

### 2.4 Tracking points (tous gated par consentement)

| Event | Catégorie | KPI 90 jours |
|---|---|---|
| `page_view` | analytics | — |
| `cta_promo_click` | analytics | **≥ 35% visiteurs uniques** |
| `phone_click` | analytics | ≥ 8% sessions mobile |
| `maps_open` | analytics | ≥ 20% visiteurs uniques |
| `maps_consent_load` | maps_third_party | granulaire (transfert hors QC distinct) |
| `newsletter_submit_success` | analytics | ≥ 50 inscrits |
| `contact_submit_success` | analytics | — |

### 2.5 Bandeau consentement (3 catégories)

| Catégorie | Default | Toggleable |
|---|---|---|
| essential | true | non |
| analytics (GA4) | **false** | oui |
| maps_third_party | **false** | oui |

**Boutons Accepter / Personnaliser / Refuser visibilité ÉQUIVALENTE** (Loi 25 + directive CAI 2024).

### 2.6 Maillage interne

- **Hub pages** : `/[locale]` (home) + `/[locale]/promotions` (KPI #1)
- **Cross-sells** : home → promotions (CTA primaire), promotions ↔ produits (S-012 + S-017), contact → politique (S-022)
- **Orphan check** : ✓ PASS, aucune page orpheline
- **Max outbound** : ≤ 30 par page (recommandation SEO respectée)

---

## 3. Plan SEO (`seo-strategist`)

### 3.1 Stratégie globale

- **Primary keyword** : `dépanneur [ville]` *(placeholder bloqué tant que ville TBD)*
- **Difficulté** : low-medium (DR 5-25) — segment sans concurrent direct sérieux hors Couche-Tard générique
- **Intent cible** : transactional (visite physique) + informational (horaires/FAQ)
- **Vocabulaire** : québécois (courriel/infolettre/clavardage), Loto-Québec orthographe officielle

### 3.2 Titres + meta (FR, char counts validés)

| Page | Title (chars) | Meta desc (chars) |
|---|---|---|
| home | « Dépanneur Nobert — Votre dépanneur de quartier à [ville] » (56) | 134 |
| promotions | « Promotions de la semaine — Dépanneur Nobert [ville] » (54) | 149 |
| produits | « Bières, snacks, loto et essentiels \| Dépanneur Nobert » (55) | 155 |
| contact | « Nous joindre — Adresse, horaires, téléphone \| Dépanneur Nobert » (62) | 132 |
| politique-confidentialite | « Politique de confidentialité (Loi 25) \| Dépanneur Nobert » (57) | 141 |
| mentions-legales | « Mentions légales \| Dépanneur Nobert » (36) | 122 |

Tous title ≤ 70 chars (limite tolérée 60-62 avec marque), meta 100-155.

### 3.3 Structured data

| Page | Schemas |
|---|---|
| Site-wide | `Organization`, `WebSite` |
| `/[locale]` | `LocalBusiness` (ConvenienceStore), `OpeningHoursSpecification` |
| `/[locale]/promotions` | `FAQPage`, `LocalBusiness` |
| `/[locale]/produits` | `FAQPage`, `ItemList` |
| `/[locale]/contact` | `LocalBusiness`, `OpeningHoursSpecification`, `ContactPage` |

Implémentation : composants server `components/seo/*JsonLd.tsx`, injection via Next 15 metadata API. Validation Rich Results Test obligatoire Ph5.

### 3.4 Sitemap + hreflang

- **Fichier** : `app/sitemap.ts` (Next 15 dynamic)
- **Hreflang** : `fr-CA`, `en-CA`, `x-default → fr-CA`
- **Priority** : home 1.0 / promotions 0.9 / produits 0.8 / contact 0.7 / légal 0.3
- **Changefreq** : home/promotions weekly, produits/contact monthly, légal yearly

### 3.5 AI crawlers (différenciation)

`robots.ts` allow explicite : **GPTBot, ChatGPT-User, PerplexityBot, ClaudeBot, Google-Extended**. Rationale : visibilité maximale + AI Overviews / SGE = levier émergent critique pour PME locale.

### 3.6 Bloqueurs au kickoff (SEO-critiques)

| Bloqueur | Impact |
|---|---|
| **Ville TBD** | Bloque tous les `[ville]` (titles/meta/H1/Schema/sitemap) |
| **Adresse complète TBD** | Bloque LocalBusiness streetAddress + S-018 |
| **Téléphone TBD** | Bloque `tel:` + kpi phone_click |
| **Horaires TBD** | Bloque OpeningHoursSpecification |
| **NEQ TBD** | Bloque mentions-legales finalisées |

→ Si non fournis au kickoff, **Ph3 livre placeholders explicites assumés**.

---

## 4. Stack technique (`solution-architect`)

### 4.1 Stack principal (versions figées)

| Composant | Choix | Version | Imposé brief ? |
|---|---|---|---|
| Framework | Next.js App Router | 15.x | ✓ |
| Langage | TypeScript strict | 5.x | ✓ |
| CSS | Tailwind CSS | 3.4.x (cf. ADR-003) | ✓ |
| i18n | next-intl | 3.x | ✓ |
| Tests | Vitest + Testing Library | 1.x / 16.x | NEXOS standard |
| Deploy | Vercel | — | ✓ |
| Images | next/image | natif Next 15 | NEXOS standard |
| Fonts | next/font/google | Fraunces + Inter | NEXOS standard |

### 4.2 Additions optionnelles (justifiées)

| Lib | Version | Justification | Impact KB | ADR |
|---|---|---|---|---|
| Framer Motion | 11.x | P17 + P02 + D5=slow-organic (spring physics) | +15 KB | ADR-001 |
| React Hook Form | 7.x | 2 forms RHF + i18n erreurs | +9 KB | ADR-002 |
| Zod | 3.x | Validation forms + data/*.json | +8 KB | ADR-002 |
| lucide-react | 0.4xx | Icônes (catégories produits) | ~1-2 KB/icône (ESM) | — |
| @tailwindcss/forms | 0.5.x | Reset forms | 0 (build-time) | — |
| @tailwindcss/typography | 0.5.x | Pages légales `prose` | 0 (build-time) | — |

**Total runtime deps hors écosystème Next : 6** (sous la limite NEXOS de 10).

### 4.3 Rejets documentés

- Tailwind 4.x (trop récent, plugins instables — ADR-003)
- jQuery / Wix / Squarespace (standards anti-NEXOS)
- styled-components / emotion (CSS-in-JS runtime, impact SSR)
- Pages Router (legacy)
- Redux / Zustand (vitrine 6 pages, aucun état global complexe)
- Sanity / Contentful / Strapi (surcoût injustifié, ADR-004)
- Mapbox / MapLibre (Google Maps déjà déclaré, ADR-005)
- GTM (pénalité LCP, GA4 natif suffit)

### 4.4 Sécurité

**vercel.json headers** (template `templates/vercel-headers.template.json`) :
- HSTS `max-age=63072000; includeSubDomains; preload`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: camera=(), microphone=(), geolocation=()`
- CSP nonce-based (généré Ph4 par `csp-generator`)

**next.config.mjs** : `poweredByHeader: false`, images formats AVIF/WebP.

**API routes** : honeypot + rate-limit 5 req/min/IP + Zod + sanitization + Resend (clé serveur uniquement).

### 4.5 ADR log (5 décisions)

| ADR | Titre | Statut |
|---|---|---|
| ADR-001 | Framer Motion pour P17 + P02 | accepted |
| ADR-002 | React Hook Form + Zod | accepted |
| ADR-003 | Tailwind 3.4 plutôt que 4 | accepted |
| ADR-004 | ISR weekly /promotions plutôt que CMS | accepted |
| ADR-005 | Google Maps embed conditionnel consent (S-020) | accepted |

### 4.6 Budget performance

| Métrique | Cible |
|---|---|
| Lighthouse Perf | ≥ 90 |
| Lighthouse A11y | 100 |
| Lighthouse SEO | 100 |
| LCP | ≤ 2.0 s |
| CLS | ≤ 0.05 |
| INP | ≤ 200 ms |
| Bundle gz home | ≤ 200 KB |

---

## 5. Scaffold (arbre de fichiers — `scaffold-planner`)

### 5.1 Synthèse

- **Total fichiers** : 82
- **Framework** : Next.js 15 App Router (flat, pas de `src/`)
- **Imports absolus** : alias `@/*` via tsconfig
- **Naming** : PascalCase composants, kebab-case routes, camelCase utilitaires

### 5.2 Arborescence

```
depanneur-nobert-site/
├── app/
│   ├── [locale]/
│   │   ├── layout.tsx              ← root layout (i18n, fonts, Header, Footer, CookieConsent, StickyCTA)
│   │   ├── page.tsx                ← home (S-001 → S-007)
│   │   ├── promotions/page.tsx     ← ISR 604800s (S-009 → S-012)
│   │   ├── produits/page.tsx       ← ISR 2592000s (S-013 → S-017)
│   │   ├── contact/page.tsx        ← (S-018 → S-022)
│   │   ├── politique-confidentialite/page.tsx  ← (S-023)
│   │   ├── mentions-legales/page.tsx           ← (S-024)
│   │   ├── not-found.tsx
│   │   ├── error.tsx
│   │   └── loading.tsx
│   ├── api/
│   │   ├── newsletter/route.ts     ← POST FORM-NEWSLETTER
│   │   └── contact/route.ts        ← POST FORM-CONTACT
│   ├── sitemap.ts
│   ├── robots.ts                   ← AI crawlers allow
│   ├── manifest.ts
│   ├── icon.tsx                    ← favicon dynamique
│   └── opengraph-image.tsx
├── components/
│   ├── ui/        ← Button, Card, Badge, Input, Textarea, Checkbox, Skeleton
│   ├── layout/    ← Header, Footer, LangSwitcher, StickyCTA, CookieConsent
│   ├── sections/  ← 19 sections (Hero, PromotionsHighlight, …, LegalDocBody)
│   └── seo/       ← JsonLd, LocalBusinessJsonLd, FAQPageJsonLd
├── lib/
│   ├── cn.ts                       ← clsx + tailwind-merge
│   ├── formatDate.ts
│   ├── consent.ts                  ← consent helpers (localStorage + custom event)
│   ├── analytics.ts                ← GA4 gated par consent
│   ├── rate-limit.ts
│   ├── email.ts                    ← Resend wrapper
│   └── validation/
│       ├── forms.ts                ← schemas Zod RHF
│       └── data.ts                 ← schemas Zod data/*.json
├── data/
│   ├── promotions.json             ← 8 exemples seed Ph3
│   ├── produits.json               ← 12-20 par catégorie Ph3
│   └── temoignages.json            ← 3-5 voisinage Ph3
├── messages/
│   ├── fr.json
│   └── en.json
├── i18n/
│   ├── request.ts
│   ├── routing.ts                  ← slugs traduits
│   └── navigation.ts
├── public/images/                  ← photos vitrine, intérieur, propriétaire
├── public/icons/                   ← favicons, manifest icons
├── styles/globals.css
├── types/sections.ts
├── tests/
│   ├── setup.ts
│   └── components/                 ← Vitest + RTL
├── middleware.ts                   ← next-intl + CSP nonce
├── next.config.mjs
├── tailwind.config.ts              ← tokens warm
├── tsconfig.json                   ← strict + alias @/*
├── vercel.json                     ← headers OWASP
├── package.json
├── .env.example
├── .eslintrc.json
├── .prettierrc.json
└── .gitignore
```

### 5.3 Alignement section-manifest

24 sections × 19 composants distincts (S-023 + S-024 partagent `LegalDocBody.tsx` avec variant). **Manifest préservé** (status=audited de Ph5 précédente, lifecycle non écrasé). Mapping S-NNN → fichier figé dans `scaffold-plan.json::section_manifest_sync`.

---

## 6. Risques majeurs Ph1 → Ph2

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Ville/adresse/tel TBD au kickoff | Élevée | Bloque SEO local + S-018/S-019 + LocalBusiness | Acter délai T+24h, sinon placeholders explicites Ph3 |
| Photos vitrine/propriétaire absentes | Élevée | Compromet P13 + S-001 + S-006 | Fallback Unsplash thématique + shooting Ph6 acté |
| Catalogue produits léger | Moyenne | S-015 décevant | Liste min 12 × 4 catégories obligatoire Ph3 |
| Promos hebdo non maintenues post-livraison | Élevée | KPI #1 sabordé | ADR-004 + procédure Ph5 + interface admin Ph6+ |
| Mapping SEC-03 confiance 0.5 | Acquise | Patterns dérive | Override manuel via Ph0 §7.2 + Ph1 §0 |

---

## 7. Gate ph1 → ph2 (vérification orchestrateur)

### 7.1 Checklist `pattern-recommender`

- [x] `pattern-recommendation.json` présent et JSON valide
- [x] `patterns_recommended` non vide (8 entrées tier 1+2)
- [x] `personality_6d_proposed` complète (6 dimensions)
- [x] `opposition_check.passes_rule_of_gold == true` (4/6 vs electro-maitre-industriel)
- [x] `confidence_score = 0.82 ≥ 0.60`

### 7.2 Artefacts produits

| Fichier | Statut |
|---|---|
| `pattern-recommendation.json` | ✓ écrit |
| `brand-identity.json` | ✓ écrit |
| `site-map-logic.json` | ✓ écrit |
| `seo-strategy.json` | ✓ écrit |
| `stack-decision.json` | ✓ écrit |
| `scaffold-plan.json` | ✓ écrit |
| `section-manifest.json` | ✓ préservé (audited, 24 sections) |

---

## Score global Phase 1

| Dimension | Score | Commentaire |
|---|---|---|
| D1 Architecture | 9.0 | App Router flat, 6 routes × 2 locales, profondeur max 1, ADR cohérents |
| D2 Contenu | 8.5 | Brand voice + lexique cohérents, UVP claire, tone signals documentés |
| D3 Performance | 9.0 | Stack contrôlé, 6 deps runtime, budget bundle < 200 KB, ISR cohérent |
| D4 Sécurité | 9.5 | 7 headers OWASP + CSP nonce + API rate-limit + secrets serveur uniquement |
| D5 i18n | 9.0 | next-intl FR/EN, slugs traduits, lang switcher route-preserving |
| D6 Accessibilité | 9.0 | WCAG AAA palette validée, touch ≥ 48px, prefers-reduced-motion, focus visible |
| D7 SEO | 8.0 | Titles/meta/H1/Schema/hreflang planifiés + AI crawlers allow — bloqué partiellement par ville TBD |
| D8 Loi 25 | 9.5 | RPP identifié, 3 catégories consent, Maps consent-gated, rétention déclarée, droits documentés |
| D9 Qualité méthodo | 8.5 | 6 artefacts JSON valides, 5 ADR, knowledge-driven (pattern-recommender confiance 0.82), règle d'or PASS |

**Score moyen : 8.9 / 10**

**Verdict Phase 1 → Phase 2** : ✓ **PASS** (seuil μ ≥ 8.0).

### Conditions bloquantes pour Phase 2

1. Aucune — gate ph1→ph2 satisfaite.

### Conditions non-bloquantes à traiter avant Phase 3

1. Figer ville + adresse + téléphone + horaires + NEQ (sinon placeholders explicites Ph3).
2. Décider photos disponibles vs fallback Unsplash + shooting Ph6.
3. Lister 12 produits × 4 catégories pour S-015.
4. Définir template promo hebdo + 8 exemples seed pour S-010.
5. Collecter 3-5 témoignages voisinage avec consentement Loi 25 explicite pour S-004.

---

*Rapport généré par Claude Code CLI en orchestration Phase 1 NEXOS v4.2.0 — 2026-05-14.*
*Aligné sur ph0-discovery-report.md 2026-05-13 (conflit palette F-001 résolu).*
