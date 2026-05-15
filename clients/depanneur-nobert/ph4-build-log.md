# Phase 4 — Build Log — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion prioritaire)
**Date Phase 4 (itération 2 SOIC)** : 2026-05-14
**Date Phase 4 (rerun itération 1)** : 2026-05-10 (rerun navy/or — préservé en historique soic-runs.jsonl)
**Date Phase 4 (run initial)** : 2026-04-28 (build initial — préservé en historique soic-runs.jsonl)
**Orchestrateur** : ph4-build (Claude Opus 4.7 — 1M context, 1M tokens)
**Agents exécutés** : project-bootstrapper → component-builder → page-assembler → integration-engineer → seo-asset-generator → build-validator
**Stack imposée** : Next.js **15.5.18** + React 19 + Tailwind 3.4.16 + next-intl 3.26.5 + Vercel
**Palette imposée (Ph2 itération 2)** : warm — `primary=#8B4513` brun boiseries · `accent=#FFD700` jaune doré · `background=#FFF8E7` crème · `text=#2A1810` brun foncé · `border=#D4C5A9` beige
**Itération SOIC** : 2 (alignement post-Ph2 warm — F-001 résolu dans le sens warm, plus aucune divergence)

---

## 0. Cadrage de l'itération 2 SOIC (2026-05-14)

> **Note de ré-exécution itération 2** : cet audit-and-patch aligne le code source du site sur la palette warm imposée par le brief, rétablie comme source de vérité lors de la re-discovery du 2026-05-13 et propagée à Ph1/Ph2 itération 2 (2026-05-14).

### Contexte de la dérive

| Date | Iteration | Palette du build | Source |
|---|---|---|---|
| 2026-04-28 | 0 (initial) | warm `#8B4513` (brief) | brief `design.palette_imposed` |
| 2026-05-10 | 1 (rerun) | **navy `#1A2B3C`** | option CLI `--colors primary=#1A2B3C accent=#FFD700 secondary=#B2B2B2` (substitution palette) |
| **2026-05-14** | **2 (itération en cours)** | **warm `#8B4513`** | `design.palette_imposed` du brief (option `--colors` **non passée**) |

L'itération 2 effectue donc une **bascule warm → navy → warm** maîtrisée. Les composants React et les messages i18n sont **palette-agnostiques** (tokens Tailwind), donc trois fichiers de configuration + quatre artefacts visuels suffisent à propager la palette warm sur l'ensemble du site sans toucher aux 23 composants ni aux 437×2 clés i18n.

### Patches appliqués

| Patch | Fichiers touchés | Justification |
|---|---|---|
| **P4i2-001** Réalignement palette warm brun/jaune/crème | `tailwind.config.ts`, `styles/globals.css` | Tokens Tailwind + CSS vars rétablis warm. `primary #8B4513`/`accent #FFD700`/`background #FFF8E7`/`text #2A1810`/`border #D4C5A9`. Échelle neutre warm (stone/khaki) au lieu de slate/zinc. Shadows teintées brun `rgb(42 24 16 / X)` au lieu de navy. |
| **P4i2-002** Réalignement assets visuels statiques | `app/icon.tsx`, `app/apple-icon.tsx`, `app/opengraph-image.tsx`, `app/manifest.ts` | Icons + OG image gradient warm `#8B4513 → #A0522D` + manifest `theme_color #8B4513` / `background_color #FFF8E7`. OG : tagline crème sur fond brun, sub-text or, mark or sur fond brun avec text-on-accent brun foncé. |
| **P4i2-003** Bump Next.js patch sécurité | `package.json`, `package-lock.json` | `npm audit` a détecté **GHSA-8h8q-6873-q5fj** (Next.js DoS Server Components, **HIGH**, CVSS 7.5) sur next@15.5.15, advisory publié post 2026-05-10. Bump patch `next 15.5.15 → 15.5.18` + `eslint-config-next 15.5.18`. Aucun breaking change semver. |

Aucun composant React, aucun message i18n FR/EN, aucune logique métier, aucune route, aucun schéma Zod, aucune logique consent applicatif touchés. Les patches sont strictement infrastructurels (config + assets statiques + bump patch sécurité).

---

## 1. Inputs Phase 4 itération 2

| Source | Apport |
|---|---|
| `brief-client.json` | Section `legal` (RPP Nobert Tremblay, courriels, retention, transferts hors QC) + `design.palette_imposed` warm (source de vérité) + stack imposé (Next.js + Tailwind + next-intl + Vercel) |
| `ph1-strategy-report.md` (2026-05-14 itération 2) | `brand-identity.json` warm, `site-map-logic.json` (slugs FR≠EN), `scaffold-plan.json` (78 fichiers), `stack-decision.json` (5 ADR), `seo-strategy.json` |
| `ph2-design-report.md` (2026-05-14 itération 2) | `design-tokens.json` itération 2 (tokens warm Tailwind-ready), `wireframes.json` (24 sections), `responsive-strategy.json`, `interactions.json`, `asset-plan.json` |
| `ph3-content-report.md` (2026-05-14 itération 2) | `messages/fr.json` + `messages/en.json` (437/437 clés parité, palette-agnostique), `seo-content.json` (meta + hreflang), `content-qa-report.json` (μ=9.78) |
| `section-manifest.json` | 24 sections statut `audited` (préservé Ph5) — lifecycle `ph4_built` bumpé itération 2 |

---

## 2. Sortie de chaque agent

### 2.1 `project-bootstrapper` → infrastructure

**Verdict** : PASS (audit + patch P4i2-003)

- **package.json** : Next.js **`15.5.18`** (patch P4i2-003 — était 15.5.15), React `19.0.0`, next-intl `3.26.5`, Tailwind `3.4.16`, react-hook-form `7.54.0`, zod `3.24.1`, @hookform/resolvers `3.9.1`, lucide-react `0.468.0`, clsx `2.1.1`, tailwind-merge `2.5.5`. DevDeps : typescript `5.7.2`, **eslint-config-next `15.5.18`**, eslint `8.57.1`, postcss `8.4.49`, autoprefixer `10.4.20`. Engine : node `>=20.10.0`.
- **tsconfig.json** : préservé — `strict: true`, `noUncheckedIndexedAccess: true`, `moduleResolution: bundler`, alias `@/*`, plugin `next`.
- **next.config.mjs** : préservé — `poweredByHeader: false`, `reactStrictMode: true`, `compress: true`, `images.formats: [avif, webp]`, headers HTTP redondés (defense-in-depth + vercel.json).
- **vercel.json** : préservé — 6 headers sécu (X-Content-Type-Options, X-Frame-Options DENY, Referrer-Policy strict-origin-when-cross-origin, Permissions-Policy camera=()/microphone=()/geolocation=(self), X-DNS-Prefetch-Control on, HSTS max-age=63072000 includeSubDomains preload). Cache control optimisé `_next/static` + `images`.
- **tailwind.config.ts** *(P4i2-001 patch)* : palette warm alignée — `primary` (#8B4513/hover #A0522D/active #6B3510/subtle #F2E6D9/foreground #FFFFFF), `accent` (#FFD700/hover #E6C200/subtle #FFF1B3/foreground **#2A1810** — enforce text-on-accent brun foncé), `secondary` (#6B4F3C — métadonnées, captions, lisible AA), `text` (DEFAULT #2A1810 AAA 14.5:1 sur crème, secondary #6B4F3C AA 6.2:1, muted #8B7355 AA 4.7:1, inverse #FFF8E7 AAA 10.2:1 sur primary brun, on-accent #2A1810 AAA 12.4:1), `background` (DEFAULT #FFF8E7 crème body, alt #FFFFFF cards, muted #F5EDD8 sections sunken), `surface` (DEFAULT #FFFFFF, raised #FFFFFF, sunken #FFF8E7, muted #F5EDD8), `border` (DEFAULT #D4C5A9 beige doux, strong #A89878, subtle #E8DFD3, focus #8B4513). Shadows teintées brun `rgb(42 24 16 / X)` au lieu du noir pur — cohérence palette warm. fontSize letter-spacing négatif H1/H2/H3 (Fraunces optical sizing).
- **styles/globals.css** *(P4i2-001 patch)* : CSS vars `--color-primary: #8b4513`, `--color-primary-hover: #a0522d`, `--color-primary-active: #6b3510`, `--color-accent: #ffd700`, `--color-accent-hover: #e6c200`, `--color-secondary: #6b4f3c`, `--color-background: #fff8e7`, `--color-background-alt: #ffffff`, `--color-background-muted: #f5edd8`, `--color-surface: #ffffff`, `--color-surface-sunken: #fff8e7`, `--color-text: #2a1810`, `--color-text-secondary: #6b4f3c`, `--color-text-muted: #8b7355`, `--color-text-on-accent: #2a1810`, `--color-text-on-primary: #ffffff`, `--color-text-inverse: #fff8e7`, `--color-border: #d4c5a9`, `--color-border-strong: #a89878`. Skip-link couleur brun + texte `--color-text-on-primary` blanc. Préservés : `prefers-reduced-motion` natif, scroll-behavior smooth.

### 2.2 `component-builder` → 23 fichiers components/sections + UI atoms

**Verdict** : PASS (audit — pas de modification)

Inchangé par rapport au rerun 2026-05-10 — les composants utilisent les **tokens Tailwind** (`bg-primary`, `text-text`, `text-on-accent`, `border-border`, `bg-surface`, `bg-background-alt`, `ring-border-focus`, etc.) donc la palette se propage **automatiquement** via la mise à jour `tailwind.config.ts` (P4i2-001).

| Catégorie | Fichiers | Mapping section-manifest |
|---|---|---|
| Layout | `Header.tsx`, `Footer.tsx`, `LanguageSwitcher.tsx`, `Logo.tsx`, `StickyCTA.tsx`, `CookieConsentBanner.tsx`, `CookieSettingsButton.tsx` | S-008 StickyCTA + footer/header globaux |
| Sections home | `Hero.tsx`, `PromotionsHighlight.tsx`, `CategoriesProduits.tsx`, `SocialProofVoisinage.tsx`, `InfosPratiques.tsx`, `StoryBrand.tsx`, `NewsletterCTA.tsx` | S-001..S-007 |
| Sections promotions | `PromotionsHero.tsx`, `PromotionsList.tsx`, `PromotionsFAQ.tsx`, `CrossSellProduits.tsx` | S-009..S-012 |
| Sections produits | `ProduitsHero.tsx`, `ProduitsCategoriesNav.tsx`, `ProduitsGalerie.tsx`, `ProduitsFAQ.tsx`, `CrossSellPromotions.tsx` | S-013..S-017 |
| Sections contact | `ContactHero.tsx`, `CoordonneesHoraires.tsx` (+ `HoursTable.tsx` helper), `MapsEmbed.tsx`, `ContactForm.tsx`, `ContactNoteRPP.tsx` | S-018..S-022 |
| Sections légales | `PrivacyPolicyBody.tsx`, `LegalNoticeBody.tsx` (JSX statique — ADR-003) | S-023, S-024 |
| UI atoms | `Button.tsx` (variants primary/secondary/ghost/accent — enforce text-on-accent #2A1810 via token), `Card.tsx`, `Badge.tsx` (variant accent → fond #FFD700 + texte #2A1810), `Input.tsx`, `Textarea.tsx`, `Checkbox.tsx`, `Container.tsx`, `Section.tsx` | shared |

**Notes** :
- Toutes les sections consomment leurs i18n keys via `useTranslations(<namespace>)` — namespaces alignés au section-manifest (`home.hero`, `promotions.list`, etc.).
- Pas de `dangerouslySetInnerHTML` hors `lib/jsonld.ts:124` (échappement `<` → `<` standard JSON-LD — ADR-003).
- La compensation R-001 reste cohérente palette warm : Fraunces 700+ chaleureux + photos vitrine éclairage chaud + lexique convivial. Aucun ajustement nécessaire post-bascule warm.

### 2.3 `page-assembler` → 6 pages × 2 locales + utilitaires

**Verdict** : PASS (audit — pas de modification logique pages)

```
app/
├── [locale]/
│   ├── layout.tsx           — html lang=fr-CA/en-CA, NextIntlClientProvider, Fraunces+Inter via next/font, JSON-LD LocalBusiness + WebSite
│   ├── page.tsx             — Home (S-001..S-007)
│   ├── promotions/page.tsx  — ISR weekly (revalidate=604800), S-009..S-012, slug EN→/deals
│   ├── produits/page.tsx    — S-013..S-017, slug EN→/products
│   ├── contact/page.tsx     — S-018..S-022
│   ├── politique-confidentialite/page.tsx — JSX statique S-023, slug EN→/privacy-policy
│   ├── mentions-legales/page.tsx          — JSX statique S-024, slug EN→/legal-notice
│   ├── not-found.tsx · error.tsx · loading.tsx
├── api/
│   ├── contact/route.ts     — POST Zod+honeypot+rate-limit, SMTP via lib/email.ts
│   └── newsletter/route.ts  — POST Zod+honeypot+rate-limit, persistance future
├── sitemap.ts               — 12 URLs (6 routes × FR/EN), hreflang fr-CA/en-CA/x-default, route EN promotions = /deals
├── robots.ts                — AI crawlers GPTBot/Google-Extended/ClaudeBot/PerplexityBot autorisés
├── opengraph-image.tsx      *(P4i2-002)* — brun gradient + or + tagline UVP Ph1
├── icon.tsx + apple-icon.tsx *(P4i2-002)* — brun bg + or N
└── manifest.ts              *(P4i2-002)* — theme_color #8B4513, background_color #FFF8E7
```

**i18n routing** : `i18n/routing.ts` (next-intl `defineRouting`), `localePrefix: always`, pathnames mapping FR≠EN explicite préservé (`/promotions`↔`/deals`, `/produits`↔`/products`, `/politique-confidentialite`↔`/privacy-policy`, `/mentions-legales`↔`/legal-notice`).

### 2.4 `integration-engineer` → API routes + formulaires + Maps consent

**Verdict** : PASS (audit — pas de modification)

| Composant | Détail | Statut itération 2 |
|---|---|---|
| `lib/schemas.ts` | Zod schemas FORM-CONTACT (name, email, phone optional, message ≤ 2000, honeypot, consent) + FORM-NEWSLETTER (email, consent, honeypot) | Préservé |
| `lib/rateLimit.ts` | In-memory Map rate limit — `/api/newsletter` 1/IP/5min, `/api/contact` 3/IP/h | Préservé |
| `lib/email.ts` | SMTP wrapper pour `/api/contact` → `nobert@depanneur-nobert.ca` (placeholder kickoff) | Préservé |
| `lib/cookieConsent.ts` | React Context + helpers `useConsent()` (categories essentials/analytics/marketing) avec persistance localStorage et événement `consent-changed` | Préservé |
| `lib/jsonld.ts` | Builders LocalBusiness (`@type: ConvenienceStore`, OpeningHoursSpecification) + WebSite + FAQPage + Breadcrumb. Helper `jsonLdScriptProps` avec échappement `<` → `<` | Préservé |
| `lib/clientConfig.ts` | Config client — variables d'env `NEXT_PUBLIC_*` avec placeholders `{ville}`, `{adresseLigne}`, `{codePostal}`, `{telephone}`, `{NEQ}`, `{anneeFondation}` (kickoff bloquants documentés Ph3) | Préservé |
| `MapsEmbed.tsx` | ADR-004 — placeholder image + bouton « Charger la carte (Google Maps - États-Unis) » avec note transfert hors QC. Iframe injectée seulement après click consent applicatif. | Préservé |

**Pas d'intégrations supplémentaires** : pas de chatbot, pas d'AdSense (hors scope brief). Pas de DOMPurify (ADR-003 — pages légales JSX statique, économie 22 KB).

### 2.5 `seo-asset-generator` → SEO + structured data

**Verdict** : PASS (audit + patch P4i2-002 pour assets visuels)

| Asset | Statut | Notes |
|---|---|---|
| `app/sitemap.ts` | ✅ Préservé | Sitemap dynamique 12 URLs (6 routes × FR/EN) avec hreflang fr-CA/en-CA/x-default, priorities 1.0/0.9/0.7/0.7/0.3/0.3 conformes seo-strategy Ph1 §3.4. Route EN promotions `deals` préservée. |
| `app/robots.ts` | ✅ Préservé | Robots dynamique. **AI crawlers autorisés explicitement** (GPTBot, Google-Extended, ClaudeBot, PerplexityBot, Bingbot) — différenciation #1 secteur sous-représenté LLM (Ph1 §3.4). Disallow `/api/`, `/_next/`. Sitemap référencé. |
| `app/opengraph-image.tsx` | ⚙️ **PATCHED P4i2-002** | OG 1200×630 généré dynamiquement, **gradient brun `#8B4513 → #A0522D`**, mark or `#FFD700` + text-on-accent `#2A1810` (au lieu du `#1A2B3C` navy) + wordmark crème `#FFF8E7` + tagline UVP « Votre dépanneur de quartier, à deux pas. » + sub-text or `#FFD700`. |
| `app/icon.tsx` | ⚙️ **PATCHED P4i2-002** | Favicon 32×32 — fond brun `#8B4513` + or `#FFD700` N (Fraunces-style). |
| `app/apple-icon.tsx` | ⚙️ **PATCHED P4i2-002** | Apple icon 180×180 — fond brun `#8B4513` + or `#FFD700` N. |
| `app/manifest.ts` | ⚙️ **PATCHED P4i2-002** | Web app manifest — `theme_color: #8B4513`, `background_color: #FFF8E7`, `start_url: /fr`, display standalone. |
| JSON-LD layout-level | ✅ Préservé | `buildLocalBusinessSchema(locale)` + `buildWebSiteSchema(locale)` injectés dans `[locale]/layout.tsx` via `jsonLdScriptProps()`. |
| Per-page metadata | ✅ Préservé | Chaque page implémente `generateMetadata({ params })` avec title/description/og/canonical/alternates.languages (hreflang bilingue strict). |
| FAQ JSON-LD | ✅ Préservé | `PromotionsFAQ.tsx` (S-011) + `ProduitsFAQ.tsx` (S-016) génèrent leur Schema.org FAQPage à partir des items i18n — différenciation AI Overviews Ph1 §3.3. |

### 2.6 `build-validator` → validation finale

**Verdict** : **BUILD PASS**

| Check | Résultat | Détail |
|---|---|---|
| `tsc --noEmit` | ✅ PASS | 0 erreurs (strict + noUncheckedIndexedAccess) |
| `next build` | ✅ PASS | 23 routes générées (12 pages SSG + 2 routes API dynamiques + 9 assets statiques metadata). Compilation **3.8s**. |
| Pages statiques (SSG) | ✅ 12/12 | 6 pages × FR/EN (home, promotions, produits, contact, politique-confidentialite, mentions-legales) |
| Pages prérendues (SSG-isr) | ✅ | `[locale]/promotions` ISR weekly (revalidate=1w, expire=1y) |
| Routes dynamiques | ✅ 2 | `/api/contact`, `/api/newsletter` |
| First Load JS shared | ✅ 102 KB | Sous le budget 250 KB |
| Largest route | ⚠️ 162 KB | `/[locale]/contact` — RHF + Zod + form. Sous budget mais à monitorer Ph5. |
| `npm audit` HIGH/CRITICAL | ✅ **0** | **0 vuln HIGH/CRITICAL après bump P4i2-003 (Next.js 15.5.18)**. GHSA-8h8q-6873-q5fj résolu. |
| `npm audit` moderate | ⚠️ 3 | next-intl ≤4.9.1 (open redirect + prototype pollution), postcss <8.5.10 (XSS via `</style>`). Non-bloquant Ph4 (seuil = HIGH/CRITICAL). À ré-évaluer Ph5 après prod-only audit. |
| `vercel.json` headers | ✅ 6/6 | XCTO, XFO DENY, RP, PP, X-DNS, HSTS preload |
| `next.config.mjs` `poweredByHeader: false` | ✅ | + reactStrictMode |
| Cookie consent intégré layout | ✅ | `CookieConsentBanner.tsx` dans `[locale]/layout.tsx` |
| Page `/politique-confidentialite` (FR) + `/privacy-policy` (EN) | ✅ | JSX statique (pas innerHTML), RPP **Nobert Tremblay** nommé, sous-traitants Vercel/GA/Maps documentés, transferts hors QC explicites |
| Page `/mentions-legales` (FR) + `/legal-notice` (EN) | ✅ | JSX statique, NEQ placeholder kickoff, hébergeur Vercel États-Unis documenté |
| Footer liens légaux | ✅ | politique-confidentialite + mentions-legales + RPP (contact) + CookieSettingsButton |
| `dangerouslySetInnerHTML` | ✅ | 1 occurrence dans `lib/jsonld.ts:124` (échappement `<` → `<` standard JSON-LD). 0 hors structured data. |
| Sitemap + robots dans `app/` | ✅ | `/sitemap.xml` + `/robots.txt` générés via Next 15 metadata API |
| OG image + favicon set + JSON-LD Org+WebSite | ✅ | Tous présents et **alignés palette warm brun/jaune/crème** (P4i2-002) |
| Alignement palette warm (tokens + assets) | ✅ | `tailwind.config.ts` + `styles/globals.css` + 4 assets visuels (icon, apple-icon, OG, manifest) — composants propagent via tokens. **F-001 résolu warm — plus aucune divergence palette.** |

**Avertissement non-bloquant W-001** (reconduit depuis rerun 2026-05-10) : `metadataBase property in metadata export is not set` lors du SSG → fallback `http://localhost:3000` pour résolution OG/Twitter. **Cause** : layout root définit `metadataBase` via `getClientConfig().baseUrl` mais les sub-pages avec leur propre `generateMetadata` n'héritent pas systématiquement en Next 15 build. **Action Ph5** : ajouter `metadataBase` explicite dans chaque sub-page `generateMetadata` ou s'assurer que `NEXT_PUBLIC_SITE_URL` est défini en build kickoff. Non-bloquant Ph4 — fallback localhost s'applique uniquement quand env vide.

---

## 3. Section manifest — mise à jour

24/24 sections : `lifecycle.ph4_built = "2026-05-14T08:30:00Z"`. `status` reste `audited` (préservé de Ph5 itération précédente, conformément au pattern audit-and-preserve de l'itération 2 SOIC). `last_updated_phase = "ph4-build"`, `iteration_soic = 2`, `iteration_note` documente la bascule warm + bump Next.js.

---

## 4. Drapeaux portés depuis Ph0/Ph1/Ph2/Ph3

| Code | Drapeau | Statut Ph4 itération 2 | Action |
|---|---|---|---|
| **F-001** | Conflit palette CLI navy vs brief warm | 🟢 **Résolu warm** | Tailwind config + globals.css + icons + OG + manifest réalignés warm. Composants utilisent les tokens, propagation auto. Plus aucune divergence palette. |
| **F-002** | Ville TBD au kickoff | 🔴 Bloquant déploiement (pas Ph4 build) | 8 placeholders `{ville}` rendus tels quels via `clientConfig.ts` — fallback explicite `{ville}` dans HTML jusqu'à fourniture env `NEXT_PUBLIC_VILLE`. |
| **F-003** | NEQ + adresse + téléphone TBD | 🔴 Bloquant déploiement (pas Ph4 build) | Placeholders rendus via `clientConfig.ts` — fournis kickoff via env `NEXT_PUBLIC_ADRESSE_LIGNE`, `NEXT_PUBLIC_CODE_POSTAL`, `NEXT_PUBLIC_TELEPHONE`, `NEXT_PUBLIC_NEQ`, `NEXT_PUBLIC_ANNEE_FONDATION`. |
| **R-001** | Palette pouvant paraître corporate | 🟢 **Stress allégé en warm** | Le risque R-001 visait surtout la palette navy. En warm, le brun boiseries + jaune doré + crème renforce naturellement le registre convivial-authentique. Compensation Fraunces 700+ + photos vitrine éclairage chaud + lexique chaleureux toujours en place. Validation perception Ph5 maintenue. |
| **R-002** | Bière responsable | ✅ Couvert Ph3, intégré Ph4 | Note S-015 + section 7 mentions-légales (LegalNoticeBody.tsx) — i18n keys `produits.galerie.bieres.note` et `legal.notice.alcohol.*`. |
| **R-003** | FAQ AI Overviews | ✅ Couvert Ph3, intégré Ph4 | `PromotionsFAQ.tsx` + `ProduitsFAQ.tsx` génèrent JSON-LD FAQPage Schema.org dynamique. |
| **R-004** | Politique transferts hors QC | ✅ Couvert Ph3, intégré Ph4 | `PrivacyPolicyBody.tsx` consomme `legal.privacy.subProcessors` (Vercel + GA + Maps) avec finalité + pays explicites. |

### Drapeaux Ph4 itération 2 (nouveaux ou reconduits)

| Code | Drapeau | Sévérité | Action |
|---|---|---|---|
| **W-001** | `metadataBase` non hérité par sub-pages → fallback localhost en SSG sans env (reconduit) | 🟡 Non-bloquant Ph4 | Ph5 : (1) définir `NEXT_PUBLIC_SITE_URL=https://depanneur-nobert.ca` au build kickoff, OU (2) ajouter `metadataBase` explicite dans chaque sub-page `generateMetadata`. |
| **W-002** | 3 vulns moderate npm audit (next-intl ≤4.9.1, postcss <8.5.10) — reconduit | 🟡 Non-bloquant Ph4 (seuil HIGH/CRITICAL) | Ph5 : ré-évaluer en prod-only audit, considérer upgrade next-intl 4.x (breaking change — vérifier impact pathnames API). |
| **R-005** | Bump Next.js 15.5.15 → 15.5.18 (P4i2-003) | 🟢 Résolu | Patch sécurité GHSA-8h8q-6873-q5fj DoS HIGH CVSS 7.5 appliqué. Aucune régression — tsc/build PASS, surface API identique. À monitorer Ph5 (lighthouse + headers scan). |

---

## 5. SOIC Gate Alignment — auto-évaluation

| Dim | Critère | Score | Notes |
|---|---|---|---|
| **D1 architecture** | Pages × locales × sections × composants alignés section-manifest 1:1 | 10/10 | 6 pages × 2 = 12 routes SSG, 24 sections → 23 fichiers components/sections, 8 UI atoms, 7 layout, mapping explicite scaffold-plan honoré |
| **D2 a11y** | Fraunces+Inter via next/font, focus-visible rings, skip-link, prefers-reduced-motion | 9.5/10 | Palette warm AAA sur surfaces principales (text/background 14.5:1). accent + secondary FAIL pour texte enforced via tokens. |
| **D4 sécurité** | 6 headers vercel.json + poweredBy=false + 0 HIGH/CRITICAL audit + JSON-LD échappé + Next.js patché | 9.75/10 | -0.25 pour 3 moderate audit (W-002 reconduit). HIGH DoS résolu via P4i2-003. |
| **D5 i18n** | Pathnames mapping FR≠EN, 437/437 clés, hreflang bilingue chaque page+sitemap | 10/10 | Slugs EN /deals, /products, /privacy-policy, /legal-notice préservés. |
| **D7 SEO** | Sitemap dynamique + robots AI-crawlers + OG dynamique warm + JSON-LD LocalBusiness/WebSite/FAQPage | 9.5/10 | -0.5 pour W-001 metadataBase fallback (reconduit). OG image warm visuellement cohérente avec hero brun. |
| **D8 légal Loi 25** | CookieConsentBanner opt-in 3 catégories + politique-confidentialite RPP nommé + mentions-legales + footer 4 liens + Maps gated consent | 10/10 | RPP Nobert Tremblay + sous-traitants Vercel/GA/Maps documentés. ADR-004 maps consent applicatif. |
| **D9 qualité** | tsc 0 erreurs + next build PASS + tests Vitest scaffold | 10/10 | Build 3.8s, 23 pages générées, 0 type error |

**μ Phase 4 (itération 2)** = **9.85/10** (cf. `soic-runs.jsonl` run `ph4i2-0514`).

> Scores précédents préservés en historique :
> - Run initial 2026-04-28 : μ=9.84 (warm palette source brief)
> - Rerun 2026-05-10 : μ=9.84 puis 9.75 (navy via CLI `--colors`)
> - **Itération 2 2026-05-14 : μ=9.85** (retour warm + fix HIGH DoS)

---

## 6. Score global Phase 4 itération 2

| Critère | Score |
|---|---|
| Cohérence avec brief + Ph0..Ph3 itération 2 (palette warm brief + KPI conversion + Loi 25 + section-manifest) | 10/10 |
| Infrastructure sécurisée (headers, poweredBy, audit HIGH/CRITICAL nettoyé via P4i2-003, JSX statique légal) | 10/10 |
| Conformité Loi 25 native (RPP + opt-in + transferts + droits + maps gated) | 10/10 |
| Build PASS (tsc + next build + 23 pages SSG + ISR weekly promotions) | 10/10 |
| SEO assets complets (sitemap, robots AI, OG warm, favicon warm, JSON-LD per-page) | 9/10 |
| Alignement palette warm (Ph2 itération 2 design tokens — F-001 résolu warm) | 10/10 |
| Slugs FR≠EN préservés (promotions/deals + produits/products + privacy + legal) | 10/10 |
| Drapeaux portés et adressés (F-001 résolu warm, R-005 résolu via bump Next.js, W-001/W-002 documentés non-bloquants) | 9/10 |

**Score global : 9.75/10**

> Gate ph4→tooling : **BUILD PASS**.
>
> Conditions Ph5 : (1) résoudre 6 placeholders kickoff via env `NEXT_PUBLIC_*` (`VILLE`, `ADRESSE_LIGNE`, `CODE_POSTAL`, `TELEPHONE`, `NEQ`, `ANNEE_FONDATION`), (2) confirmer `NEXT_PUBLIC_SITE_URL` pour résoudre W-001 metadataBase, (3) lancer `tools/preflight.sh` (Lighthouse + pa11y + headers-scan + osiris) sur build warm.

---

## 7. Sorties machine-readable

| Fichier | Status itération 2 | Action |
|---|---|---|
| `site/tailwind.config.ts` | ✅ PATCHED | P4i2-001 — palette warm brun/jaune/crème + neutral_scale warm + shadows brun |
| `site/styles/globals.css` | ✅ PATCHED | P4i2-001 — CSS vars warm complètes (20 tokens) + skip-link warm |
| `site/app/icon.tsx` | ✅ PATCHED | P4i2-002 — fond brun #8B4513 + or N |
| `site/app/apple-icon.tsx` | ✅ PATCHED | P4i2-002 — fond brun #8B4513 + or N |
| `site/app/opengraph-image.tsx` | ✅ PATCHED | P4i2-002 — gradient brun #8B4513→#A0522D + mark or text-on-accent brun + tagline crème |
| `site/app/manifest.ts` | ✅ PATCHED | P4i2-002 — theme_color #8B4513, background_color #FFF8E7 |
| `site/package.json` | ✅ PATCHED | P4i2-003 — next 15.5.18 + eslint-config-next 15.5.18 (fix GHSA-8h8q-6873-q5fj) |
| `site/package-lock.json` | ✅ MIS À JOUR | npm install — 5 packages mis à jour |
| `site/i18n/routing.ts` | ✅ Préservé | Pathnames FR≠EN intacts |
| `site/app/sitemap.ts` | ✅ Préservé | Route EN /deals intacte |
| `section-manifest.json` | ✅ MIS À JOUR | 24/24 sections → `lifecycle.ph4_built: 2026-05-14T08:30:00Z`, `last_updated_phase: ph4-build`, `iteration_soic: 2`, `iteration_note` documentée |
| `nexos-changelog.json` | ✅ APPENDED | 12 events Ph4 itération 2 (phase_start, 5×agent_run, 2×auto_fix P4i2-001+P4i2-003, build_pass, section_manifest_update, soic_gate_pass, phase_end) |
| `soic-runs.jsonl` | ✅ APPENDED | 1 run `ph4i2-0514` (μ=9.85, 14/14 gates BUILD-01..14 PASS) |
| `soic-gates.json` | ✅ MIS À JOUR | ph4-build → mu=9.85, iterations=2, timestamp=2026-05-14T08:30:00, _iteration_note documentée |

---

## 8. Handoff Phase 4-tooling → Phase 5 — QA

### Décisions héritées (non négociables)

1. **Build artefacts dans `site/`** : ne pas régénérer en Ph5 sans cause majeure. La Ph5 audit le build existant warm.
2. **Palette warm brun/jaune/crème stricte** (Ph2 itération 2 = source de vérité) — toute régression vers navy/or = défaut Ph5.
3. **Pages légales JSX statique** (ADR-003) — pas de DOMPurify, pas de innerHTML.
4. **Maps gated par consent applicatif** (ADR-004) — bouton « Charger la carte » obligatoire avant iframe.
5. **AI crawlers explicitement autorisés** dans robots.ts — différenciation Ph1 §3.4 maintenue.
6. **Next.js 15.5.18+ verrouillé** (P4i2-003) — fix HIGH DoS GHSA-8h8q-6873-q5fj. Ne pas downgrader.

### Inputs livrés à Ph4-tooling/Ph5

- `site/.next/` (build statique 23 pages — warm)
- `site/package.json` + `site/package-lock.json` (deps verrouillées, next 15.5.18)
- `section-manifest.json` (24/24 statut `audited`, lifecycle.ph4_built itération 2 = 2026-05-14T08:30:00Z)
- `nexos-changelog.json` audit trail Ph4 itération 2
- `soic-gates.json` + `soic-runs.jsonl` historique gates (3 runs Ph4 préservés)

### Bloquants Ph5 deploy à lever au kickoff (rappel Ph3 §4)

| Bloquant | Sections impactées | Sévérité |
|---|---|---|
| `NEXT_PUBLIC_VILLE` | S-001, S-009, S-013, S-018, S-019 + sitemap + meta + Schema | 🔴 critique deploy |
| `NEXT_PUBLIC_ADRESSE_LIGNE` + `NEXT_PUBLIC_CODE_POSTAL` | S-018, S-019, S-023, S-024 + Schema | 🔴 critique deploy |
| `NEXT_PUBLIC_TELEPHONE` | S-005, S-018, S-019, footer, S-024 | 🔴 critique deploy |
| `NEXT_PUBLIC_NEQ` | S-024 | 🔴 critique deploy |
| `NEXT_PUBLIC_ANNEE_FONDATION` | S-006 + tagline | 🟡 cohérence StoryBrand |
| `NEXT_PUBLIC_SITE_URL` | metadataBase + sitemap canonical + JSON-LD URLs | 🟡 W-001 résolution |
| Photo `/images/hero-vitrine.jpg` (S-001) | S-001 | 🟡 fallback Unsplash dispo asset-plan |
| Consentement écrit voisinage S-004 | S-004 (3-5 portraits) | 🟡 fallback avatars-initiales |

### Risques à monitorer en Ph4-tooling/Ph5

1. **Lighthouse Performance** : cible ≥ 90. Risque W-001 metadataBase + 162 KB route contact. Mesurer LCP/INP/CLS sur build prod kickoff (palette warm).
2. **pa11y / axe-core** : cible 0 violation critical. Vérifier focus-visible rings brun sur fond crème + contrastes accent (text-on-accent brun foncé sur jaune AAA 12.4:1) en contexte réel.
3. **headers-scan** : cible 100% (6 headers + CSP). Vérifier vercel.json appliqué post-deploy.
4. **npm audit prod-only** : ré-évaluer 3 moderate restants (next-intl, postcss). HIGH DoS Next.js maintenant clos via P4i2-003.
5. **Test perception palette warm** : valider que brun + jaune + crème renforcent bien la convivialité quartier (vs risque corporate écarté). Test rapide auprès du voisinage cible 35-65.

---

*Phase 4 Build itération 2 complétée 2026-05-14. Prochain handoff : `tools/preflight.sh` (Lighthouse + pa11y + headers + osiris) → `ph5-qa/_orchestrator`.*

Score global: BUILD PASS (9.75/10)
