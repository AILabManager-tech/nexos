# Phase 4 — Build Log — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion prioritaire)
**Date Phase 4 (rerun)** : 2026-05-10
**Date Phase 4 (run initial)** : 2026-04-28 (build initial préservé en historique soic-runs.jsonl)
**Orchestrateur** : ph4-build (Claude Opus 4.7 — 1M context)
**Agents exécutés** : project-bootstrapper → component-builder → page-assembler → integration-engineer → seo-asset-generator → build-validator
**Stack imposée** : Next.js 15.5.15 + React 19 + Tailwind 3.4.16 + next-intl 3.26.5 + Vercel
**Palette CLI imposée** : `primary=#1A2B3C` · `accent=#FFD700` · `secondary=#B2B2B2`

---

## 0. Cadrage du rerun 2026-05-10

Le code source du site (`clients/depanneur-nobert/site/`) a été produit lors du run Ph4 initial du **2026-04-28** (μ=9.84, 23 routes générées). Ce rerun applique deux **patches d'alignement post-Ph2/Ph3** :

| Patch | Fichiers touchés | Justification |
|---|---|---|
| **P4-001** Réalignement palette CLI navy/or/gris | `tailwind.config.ts`, `styles/globals.css`, `app/icon.tsx`, `app/apple-icon.tsx`, `app/opengraph-image.tsx`, `app/manifest.ts` | Le build initial 2026-04-28 utilisait la palette brune **du brief warm initial** (`#8B4513`/`#FFF8E7`/`#D4C5A9`). La palette imposée par CLI `--colors` (Ph1 §1.3 + Ph2 §1.1) est navy/or/gris (`#1A2B3C`/`#FFD700`/`#B2B2B2`). Le `design-tokens.json` et `brand-identity.json` étaient déjà alignés navy ; seuls les artefacts CSS/images du site avaient gardé l'ancien thème. Réalignement intégral pour cohérence visuelle stricte avec Ph2 design report. |
| **P4-002** Slug EN promotions `/promotions` → `/deals` | `i18n/routing.ts`, `app/sitemap.ts`, `app/[locale]/promotions/page.tsx` | Alignement `seo-content.json` Ph3 (rerun P3-002) + `site-map-logic.json` Ph1 §2.3. Mise à jour pathnames mapping next-intl + sitemap.ts route_en + canonical_en + hreflang en-CA. |

Aucun composant React, aucun message i18n, aucune logique métier touchés. Les patches sont purement infrastructurels (config + assets statiques).

---

## 1. Inputs Phase 4

| Source | Apport |
|---|---|
| `brief-client.json` | Section `legal` (RPP Nobert Tremblay, courriels, retention, transferts hors QC) + stack imposé (Next.js + Tailwind + next-intl + Vercel) |
| `ph1-strategy-report.md` | `brand-identity.json` (palette navy/or/gris, Fraunces/Inter), `site-map-logic.json` (slugs FR≠EN), `scaffold-plan.json` (78 fichiers), `stack-decision.json` (5 ADR), `seo-strategy.json` |
| `ph2-design-report.md` | `design-tokens.json` (tokens Tailwind-ready), `wireframes.json` (24 sections), `responsive-strategy.json`, `interactions.json`, `asset-plan.json` |
| `ph3-content-report.md` | `messages/fr.json` + `messages/en.json` (437/437 clés parité), `seo-content.json` (meta + hreflang), `content-qa-report.json` (μ=9.78) |
| `section-manifest.json` | 24 sections statut `content-ready` à passer en `built` |

---

## 2. Sortie de chaque agent

### 2.1 `project-bootstrapper` → infrastructure

**Verdict** : PASS

- **package.json** : Next.js `15.5.15`, React `19.0.0`, next-intl `3.26.5`, Tailwind `3.4.16`, react-hook-form `7.54.0`, zod `3.24.1`, @hookform/resolvers `3.9.1`, lucide-react `0.468.0`, clsx `2.1.1`, tailwind-merge `2.5.5`. DevDeps : typescript `5.7.2`, eslint `8.57.1`, postcss `8.4.49`, autoprefixer `10.4.20`. Engine : node `>=20.10.0`.
- **tsconfig.json** : `strict: true`, `noUncheckedIndexedAccess: true`, `moduleResolution: bundler`, alias `@/*`, plugin `next`.
- **next.config.mjs** : `poweredByHeader: false`, `reactStrictMode: true`, `compress: true`, `images.formats: [avif, webp]`, headers HTTP redondés (defense-in-depth + vercel.json).
- **vercel.json** : 6 headers sécu présents (X-Content-Type-Options, X-Frame-Options DENY, Referrer-Policy strict-origin-when-cross-origin, Permissions-Policy camera=()/microphone=()/geolocation=(self), X-DNS-Prefetch-Control on, HSTS max-age=63072000 includeSubDomains preload). Cache control optimisé `_next/static` + `images`.
- **tailwind.config.ts** *(P4-001 patch)* : palette CLI navy/or/gris alignée — `primary` (#1A2B3C/hover #243D54/active #142231/subtle #E5E9ED), `accent` (#FFD700/foreground #1A2B3C — enforce text-on-accent), `secondary` (#B2B2B2 — décoratif uniquement, FAIL pour texte par construction), `text` (default #1A2B3C, muted #475569 AAA 7.46:1), `background` (#FFFFFF, alt #F4F6F8). Shadows teintées navy `rgb(26 43 60 / X)`.
- **styles/globals.css** *(P4-001 patch)* : CSS vars `--color-primary: #1a2b3c`, `--color-accent: #ffd700`, `--color-secondary: #b2b2b2`, `--color-background: #ffffff`. Skip-link + prefers-reduced-motion préservés.

### 2.2 `component-builder` → 23 fichiers components/sections + UI atoms

**Verdict** : PASS

| Catégorie | Fichiers | Mapping section-manifest |
|---|---|---|
| Layout | `Header.tsx`, `Footer.tsx`, `LanguageSwitcher.tsx`, `Logo.tsx`, `StickyCTA.tsx`, `CookieConsentBanner.tsx`, `CookieSettingsButton.tsx` | S-008 StickyCTA + footer/header globaux |
| Sections home | `Hero.tsx`, `PromotionsHighlight.tsx`, `CategoriesProduits.tsx`, `SocialProofVoisinage.tsx`, `InfosPratiques.tsx`, `StoryBrand.tsx`, `NewsletterCTA.tsx` | S-001..S-007 |
| Sections promotions | `PromotionsHero.tsx`, `PromotionsList.tsx`, `PromotionsFAQ.tsx`, `CrossSellProduits.tsx` | S-009..S-012 |
| Sections produits | `ProduitsHero.tsx`, `ProduitsCategoriesNav.tsx`, `ProduitsGalerie.tsx`, `ProduitsFAQ.tsx`, `CrossSellPromotions.tsx` | S-013..S-017 |
| Sections contact | `ContactHero.tsx`, `CoordonneesHoraires.tsx` (+ `HoursTable.tsx` helper), `MapsEmbed.tsx`, `ContactForm.tsx`, `ContactNoteRPP.tsx` | S-018..S-022 |
| Sections légales | `PrivacyPolicyBody.tsx`, `LegalNoticeBody.tsx` (JSX statique — ADR-003) | S-023, S-024 |
| UI atoms | `Button.tsx` (variants primary/secondary/ghost — enforce text-on-accent via tailwind tokens), `Card.tsx`, `Badge.tsx`, `Input.tsx`, `Textarea.tsx`, `Checkbox.tsx`, `Container.tsx`, `Section.tsx` | shared |

**Notes** :
- Toutes les sections consomment leurs i18n keys via `useTranslations(<namespace>)` — namespaces alignés au section-manifest (`home.hero`, `promotions.list`, etc.).
- Pas de `dangerouslySetInnerHTML` hors `lib/jsonld.ts:124` (échappement `<` → `<` standard JSON-LD — ADR-003).
- Toutes les couleurs des composants passent par les tokens Tailwind (`bg-primary`, `text-accent-foreground`, `border-border`, etc.) — donc le P4-001 patch (config tokens) propage automatiquement la palette navy/or/gris à tous les composants sans modification individuelle.

### 2.3 `page-assembler` → 6 pages × 2 locales + utilitaires

**Verdict** : PASS

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
├── sitemap.ts (P4-002 — slug EN /deals)
├── robots.ts (AI crawlers GPTBot/Google-Extended/ClaudeBot/PerplexityBot autorisés)
├── opengraph-image.tsx (P4-001 — navy gradient + or + tagline UVP Ph1)
├── icon.tsx + apple-icon.tsx (P4-001 — navy bg + or N)
└── manifest.ts (P4-001 — theme_color #1A2B3C, background_color #FFFFFF)
```

**i18n routing** : `i18n/routing.ts` (next-intl `defineRouting`), `localePrefix: always`, pathnames mapping FR≠EN explicite (`/promotions`↔`/deals`, `/produits`↔`/products`, `/politique-confidentialite`↔`/privacy-policy`, `/mentions-legales`↔`/legal-notice`).

### 2.4 `integration-engineer` → API routes + formulaires + Maps consent

**Verdict** : PASS

| Composant | Détail |
|---|---|
| `lib/schemas.ts` | Zod schemas FORM-CONTACT (name, email, phone optional, message ≤ 2000, honeypot, consent) + FORM-NEWSLETTER (email, consent, honeypot) — partagés client/server |
| `lib/rateLimit.ts` | In-memory Map rate limit — `/api/newsletter` 1/IP/5min, `/api/contact` 3/IP/h |
| `lib/email.ts` | SMTP wrapper pour `/api/contact` → `nobert@depanneur-nobert.ca` (placeholder kickoff) |
| `lib/cookieConsent.ts` | React Context + helpers `useConsent()` (categories essentials/analytics/marketing) avec persistance localStorage et événement `consent-changed` |
| `lib/jsonld.ts` | Builders LocalBusiness (`@type: ConvenienceStore`, OpeningHoursSpecification) + WebSite + FAQPage + Breadcrumb. Helper `jsonLdScriptProps` avec échappement `<` → `<` |
| `lib/clientConfig.ts` | Config client — variables d'env `NEXT_PUBLIC_*` avec placeholders `{ville}`, `{adresseLigne}`, `{codePostal}`, `{telephone}`, `{NEQ}`, `{anneeFondation}` (kickoff bloquants documentés Ph3) |
| `MapsEmbed.tsx` | ADR-004 — placeholder image + bouton « Charger la carte (Google Maps - États-Unis) » avec note transfert hors QC. Iframe injectée seulement après click consent applicatif. |

**Pas d'intégrations supplémentaires** : pas de chatbot, pas d'AdSense (hors scope brief). Pas de DOMPurify (ADR-003 — pages légales JSX statique, économie 22 KB).

### 2.5 `seo-asset-generator` → SEO + structured data

**Verdict** : PASS

| Asset | Statut | Notes |
|---|---|---|
| `app/sitemap.ts` | PASS | Sitemap dynamique 12 URLs (6 routes × FR/EN) avec hreflang fr-CA/en-CA/x-default, priorities 1.0/0.9/0.7/0.7/0.3/0.3 conformes seo-strategy Ph1 §3.4. P4-002 — route EN promotions `deals`. |
| `app/robots.ts` | PASS | Robots dynamique. **AI crawlers autorisés explicitement** (GPTBot, Google-Extended, ClaudeBot, PerplexityBot, Bingbot) — différenciation #1 secteur sous-représenté LLM (Ph1 §3.4). Disallow `/api/`, `/_next/`. Sitemap référencé. |
| `app/opengraph-image.tsx` | PASS | OG 1200×630 généré dynamiquement, navy gradient `#1A2B3C → #243D54`, mark or `#FFD700` + wordmark blanc + tagline UVP « Votre dépanneur de quartier, à deux pas. » + sub-text or. |
| `app/icon.tsx` | PASS | Favicon 32×32 navy bg + or N (Fraunces-style). |
| `app/apple-icon.tsx` | PASS | Apple icon 180×180 navy bg + or N. |
| `app/manifest.ts` | PASS | Web app manifest — theme_color `#1A2B3C`, background_color `#FFFFFF`, start_url `/fr`, display standalone. |
| JSON-LD layout-level | PASS | `buildLocalBusinessSchema(locale)` + `buildWebSiteSchema(locale)` injectés dans `[locale]/layout.tsx` via `jsonLdScriptProps()`. |
| Per-page metadata | PASS | Chaque page implémente `generateMetadata({ params })` avec title/description/og/canonical/alternates.languages (hreflang bilingue strict). |
| FAQ JSON-LD | PASS | `PromotionsFAQ.tsx` (S-011) + `ProduitsFAQ.tsx` (S-016) génèrent leur Schema.org FAQPage à partir des items i18n — différenciation AI Overviews Ph1 §3.3. |

### 2.6 `build-validator` → validation finale

**Verdict** : **BUILD PASS**

| Check | Résultat | Détail |
|---|---|---|
| `tsc --noEmit` | ✅ PASS | 0 erreurs (strict + noUncheckedIndexedAccess) |
| `next build` | ✅ PASS | 23 routes générées (12 pages + 11 ressources auxiliaires). Compilation 2.0s. |
| Pages statiques (SSG) | ✅ 12/12 | 6 pages × FR/EN (home, promotions, produits, contact, politique-confidentialite, mentions-legales) |
| Pages prérendues (SSG-isr) | ✅ | `[locale]/promotions` ISR weekly (revalidate=1w, expire=1y) |
| Routes dynamiques | ✅ 2 | `/api/contact`, `/api/newsletter` |
| First Load JS shared | ✅ 102 KB | Sous le budget 250 KB |
| Largest route | ⚠️ 162 KB | `/[locale]/contact` — RHF + Zod + form. Sous budget mais à monitorer Ph5. |
| `npm audit` HIGH/CRITICAL | ✅ 0 | 0 vuln HIGH/CRITICAL |
| `npm audit` moderate | ⚠️ 3 | next-intl ≤4.9.1 (open redirect + prototype pollution), postcss <8.5.10 (XSS via `</style>`). Non-bloquant Ph4 (seuil = HIGH/CRITICAL). À ré-évaluer Ph5 après prod-only audit. |
| `vercel.json` headers | ✅ 6/6 | XCTO, XFO DENY, RP, PP, X-DNS, HSTS preload |
| `next.config.mjs` `poweredByHeader: false` | ✅ | + reactStrictMode |
| Cookie consent intégré layout | ✅ | `CookieConsentBanner.tsx` dans `[locale]/layout.tsx` ligne 122 |
| Page `/politique-confidentialite` (FR) + `/privacy-policy` (EN) | ✅ | JSX statique (pas innerHTML), RPP **Nobert Tremblay** nommé, sous-traitants Vercel/GA/Maps documentés, transferts hors QC explicites |
| Page `/mentions-legales` (FR) + `/legal-notice` (EN) | ✅ | JSX statique, NEQ placeholder kickoff, hébergeur Vercel États-Unis documenté |
| Footer liens légaux | ✅ | politique-confidentialite + mentions-legales + RPP (contact) + CookieSettingsButton |
| `dangerouslySetInnerHTML` | ✅ | 1 occurrence dans `lib/jsonld.ts:124` (échappement `<` → `<` standard JSON-LD). 0 hors structured data. |
| Sitemap + robots dans `app/` | ✅ | `/sitemap.xml` + `/robots.txt` générés via Next 15 metadata API |
| OG image + favicon set + JSON-LD Org+WebSite | ✅ | Tous présents et alignés palette navy/or |

**Avertissement non-bloquant** : `metadataBase property in metadata export is not set` lors du SSG → fallback `http://localhost:3000` pour résolution OG/Twitter. **Cause** : layout root définit `metadataBase` via `getClientConfig().baseUrl` mais les sub-pages avec leur propre `generateMetadata` n'héritent pas systématiquement en Next 15 build. **Action Ph5** : ajouter `metadataBase` explicite dans chaque sub-page `generateMetadata` ou s'assurer que `NEXT_PUBLIC_SITE_URL` est défini en build kickoff (placeholder par défaut `https://depanneur-nobert.ca`). Non-bloquant Ph4 — fallback localhost s'applique uniquement quand env vide.

---

## 3. Section manifest — mise à jour

24/24 sections passées en `status="built"`, `lifecycle.ph4_built = "2026-05-10T00:00:00Z"`.
`last_updated_phase = "ph4-build"`.

---

## 4. Drapeaux portés depuis Ph0/Ph1/Ph2/Ph3

| Code | Drapeau | Statut Ph4 | Action |
|---|---|---|---|
| **F-001** | Conflit palette CLI navy vs brief warm | 🟢 **Résolu Ph4 P4-001** | Tailwind config + globals.css + icons + OG + manifest réalignés sur palette CLI imposée. Composants utilisent les tokens, propagation auto. |
| **F-002** | Ville TBD au kickoff | 🔴 Bloquant déploiement (pas Ph4 build) | 8 placeholders `{ville}` rendus tels quels via `clientConfig.ts` — fallback explicite `{ville}` dans HTML jusqu'à fourniture env `NEXT_PUBLIC_VILLE`. |
| **F-003** | NEQ + adresse + téléphone TBD | 🔴 Bloquant déploiement (pas Ph4 build) | Placeholders rendus via `clientConfig.ts` — fournis kickoff via env `NEXT_PUBLIC_ADRESSE_LIGNE`, `NEXT_PUBLIC_CODE_POSTAL`, `NEXT_PUBLIC_TELEPHONE`, `NEXT_PUBLIC_NEQ`, `NEXT_PUBLIC_ANNEE_FONDATION`. |
| **R-001** | Palette navy peut paraître corporate | 🟡 Compensation engagée Ph2/Ph3, validation Ph5 | Compensation Fraunces 700+ via `next/font/google` + photos vitrine éclairage chaud (asset-plan, fallback Unsplash) + lexique chaleureux dans messages. Test perception Ph5. |
| **R-002** | Bière responsable | ✅ Couvert Ph3, intégré Ph4 | Note S-015 + section 7 mentions-légales (LegalNoticeBody.tsx) — i18n keys `produits.galerie.bieres.note` et `legal.notice.alcohol.*`. |
| **R-003** | FAQ AI Overviews | ✅ Couvert Ph3, intégré Ph4 | `PromotionsFAQ.tsx` + `ProduitsFAQ.tsx` génèrent JSON-LD FAQPage Schema.org dynamique. |
| **R-004** | Politique transferts hors QC | ✅ Couvert Ph3, intégré Ph4 | `PrivacyPolicyBody.tsx` consomme `legal.privacy.subProcessors` (Vercel + GA + Maps + Resend) avec finalité + pays explicites. |

Nouveaux drapeaux Ph4 :

| Code | Drapeau | Sévérité | Action |
|---|---|---|---|
| **W-001** | `metadataBase` non hérité par sub-pages → fallback localhost en SSG sans env | 🟡 Non-bloquant Ph4 | Ph5 : (1) définir `NEXT_PUBLIC_SITE_URL=https://depanneur-nobert.ca` au build kickoff, OU (2) ajouter `metadataBase` explicite dans chaque sub-page `generateMetadata`. |
| **W-002** | 3 vulns moderate npm audit (next-intl ≤4.9.1, postcss <8.5.10) | 🟡 Non-bloquant Ph4 (seuil HIGH/CRITICAL) | Ph5 : ré-évaluer en prod-only audit, considérer upgrade next-intl 4.x (breaking change — vérifier impact pathnames API). |

---

## 5. SOIC Gate Alignment — auto-évaluation

| Dim | Critère | Score | Notes |
|---|---|---|---|
| **D1 architecture** | Pages × locales × sections × composants alignés section-manifest 1:1 | 10/10 | 6 pages × 2 = 12 routes, 24 sections → 23 fichiers components/sections, 8 UI atoms, 7 layout, mapping explicite scaffold-plan honoré |
| **D2 a11y** | Fraunces+Inter via next/font, focus-visible rings, skip-link, prefers-reduced-motion | 9.0/10 | Compensation R-001 navy via Fraunces 700+ effective. accent + secondary FAIL pour texte enforced via tokens. |
| **D4 sécurité** | 6 headers vercel.json + poweredBy=false + 0 HIGH/CRITICAL audit + JSON-LD échappé | 9.75/10 | -0.25 pour 3 moderate audit (W-002) |
| **D5 i18n** | Pathnames mapping FR≠EN, 437/437 clés, hreflang bilingue chaque page+sitemap | 10/10 | P4-002 patch slug EN /deals appliqué |
| **D7 SEO** | Sitemap dynamique + robots AI-crawlers + OG dynamique + JSON-LD LocalBusiness/WebSite/FAQPage | 9.5/10 | -0.5 pour W-001 metadataBase fallback |
| **D8 légal Loi 25** | CookieConsentBanner opt-in 3 catégories + politique-confidentialite RPP nommé + mentions-legales + footer 4 liens + Maps gated consent | 10/10 | RPP Nobert Tremblay + sous-traitants Vercel/GA/Maps documentés. ADR-004 maps consent applicatif. |
| **D9 qualité** | tsc 0 erreurs + next build PASS + tests Vitest scaffold | 10/10 | Build 2.0s, 23 pages générées, 0 type error |

**μ Phase 4 (rerun)** = **9.75/10** (cf. `soic-runs.jsonl` run `ph4r2510`).

> Score précédent run initial 2026-04-28 (μ=9.84) préservé en historique. Le rerun corrige deux divergences post-Ph2/Ph3 sans régression fonctionnelle.

---

## 6. Score global Phase 4

| Critère | Score |
|---|---|
| Cohérence avec brief + Ph0..Ph3 (palette CLI + KPI conversion + Loi 25 + section-manifest) | 10/10 |
| Infrastructure sécurisée (headers, poweredBy, audit, JSX statique légal) | 9/10 |
| Conformité Loi 25 native (RPP + opt-in + transferts + droits + maps gated) | 10/10 |
| Build PASS (tsc + next build + 23 pages SSG + ISR weekly promotions) | 10/10 |
| SEO assets complets (sitemap, robots AI, OG, favicon, JSON-LD per-page) | 9/10 |
| Alignement palette CLI navy/or/gris (Ph2 design tokens) | 10/10 |
| Slugs FR≠EN (P4-002 — promotions/deals + produits/products + privacy + legal) | 10/10 |
| Drapeaux portés et adressés (F-001 résolu, W-001/W-002 documentés non-bloquants) | 9/10 |

**Score global : 9.5/10**

> Gate ph4→tooling : **BUILD PASS**.
>
> Conditions Ph5 : (1) résoudre 6 placeholders kickoff via env `NEXT_PUBLIC_*` (`VILLE`, `ADRESSE_LIGNE`, `CODE_POSTAL`, `TELEPHONE`, `NEQ`, `ANNEE_FONDATION`), (2) confirmer `NEXT_PUBLIC_SITE_URL` pour résoudre W-001 metadataBase, (3) lancer `tools/preflight.sh` (Lighthouse + pa11y + headers-scan + osiris).

---

## 7. Sorties machine-readable

| Fichier | Status | Action rerun 2026-05-10 |
|---|---|---|
| `site/tailwind.config.ts` | ✅ PATCHED | P4-001 — palette CLI navy/or/gris |
| `site/styles/globals.css` | ✅ PATCHED | P4-001 — CSS vars navy/or/gris/blanc |
| `site/app/icon.tsx` | ✅ PATCHED | P4-001 — navy bg + or N |
| `site/app/apple-icon.tsx` | ✅ PATCHED | P4-001 — navy bg + or N |
| `site/app/opengraph-image.tsx` | ✅ PATCHED | P4-001 — navy gradient + tagline UVP vouvoiement |
| `site/app/manifest.ts` | ✅ PATCHED | P4-001 — theme_color #1A2B3C, description vouvoiement |
| `site/i18n/routing.ts` | ✅ PATCHED | P4-002 — pathnames `/promotions` en: `/deals` |
| `site/app/sitemap.ts` | ✅ PATCHED | P4-002 — route_en `deals` |
| `site/app/[locale]/promotions/page.tsx` | ✅ PATCHED | P4-002 — canonical_en + hreflang en-CA `/en/deals` |
| `section-manifest.json` | ✅ MIS À JOUR | 24/24 sections → `status: built`, `lifecycle.ph4_built: 2026-05-10`, `last_updated_phase: ph4-build` |
| `nexos-changelog.json` | ✅ APPENDED | 11 events Ph4 rerun (phase_start, 5×agent_run, build_pass, auto_fix, section_manifest_update, soic_gate_pass, phase_end) |
| `soic-runs.jsonl` | ✅ APPENDED | 1 run `ph4r2510` (μ=9.75, 14/14 gates PASS) |
| `soic-gates.json` | ✅ MIS À JOUR | ph4-build → mu=9.5, timestamp=2026-05-10, decision=ACCEPT, _note rerun |

---

## 8. Handoff Phase 4-tooling → Phase 5 — QA

### Décisions héritées (non négociables)

1. **Build artefacts dans `site/`** : ne pas régénérer en Ph5 sans cause majeure. La Ph5 audit le build existant.
2. **Palette CLI navy/or/gris stricte** — toute régression vers warm brown brief = défaut Ph5.
3. **Pages légales JSX statique** (ADR-003) — pas de DOMPurify, pas de innerHTML.
4. **Maps gated par consent applicatif** (ADR-004) — bouton « Charger la carte » obligatoire avant iframe.
5. **AI crawlers explicitement autorisés** dans robots.ts — différenciation Ph1 §3.4 maintenue.

### Inputs livrés à Ph4-tooling/Ph5

- `site/.next/` (build statique 23 pages)
- `site/package.json` + `site/package-lock.json` (deps verrouillées)
- `section-manifest.json` (24/24 statut `built`)
- `nexos-changelog.json` audit trail Ph4
- `soic-gates.json` + `soic-runs.jsonl` historique gates

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

1. **Lighthouse Performance** : cible ≥ 90. Risque W-001 metadataBase + 162 KB route contact. Mesurer LCP/INP/CLS sur build prod kickoff.
2. **pa11y / axe-core** : cible 0 violation critical. Vérifier focus-visible rings sur fond navy + contrastes accent dans contexte réel.
3. **headers-scan** : cible 100% (6 headers + CSP). Vérifier vercel.json appliqué post-deploy.
4. **npm audit prod-only** : ré-évaluer 3 moderate (next-intl, postcss). Décider si upgrade nécessaire.
5. **Test perception R-001 navy** : valider que la compensation chaleur (typo + photos + lexique) tient en perception réelle.

---

*Phase 4 Build rerun complétée 2026-05-10. Prochain handoff : `tools/preflight.sh` (Lighthouse + pa11y + headers + osiris) → `ph5-qa/_orchestrator`.*

Score global: BUILD PASS (9.5/10)
