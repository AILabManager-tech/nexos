# Phase 5 — QA Audit Report

```
DATE     : 2026-05-09
URL      : http://localhost:37015/  (build local servi par next start, audit pré-deploy)
CLIENT   : E2E Validation Test (depanneur clone) — slug `_e2e_validation_2026-05-08`
MODE     : audit (pas de rebuild — audit du build Ph4)
AUDITEUR : NEXOS v4.2 — Phase 5 QA (23 agents + tooling réel)
```

> **Cadrage métier (rappel)** — KPI primaire conversion (« Voir les promotions de la semaine »), positionnement accessible/chaleureux, anti-corporate. Ce client est tagué **« test jetable » (cf. brief `_meta.phase_origin`)** : il valide le pipeline `nexos create` end-to-end. Les recommandations ci-dessous portent sur la qualité réelle du code livré, pas sur un déploiement effectif.

---

## TL;DR

| Indicateur | Valeur réelle (mesure tooling) | Verdict |
|---|---|---|
| Lighthouse Performance | **0.76** | ⚠ borderline (LCP 2.6 s OK, **CLS 0.502 critique**) |
| Lighthouse Accessibility | **1.00** | ✅ |
| Lighthouse Best Practices | **1.00** | ✅ |
| Lighthouse SEO | **0.92** | ⚠ meta-description manquant à la racine |
| pa11y WCAG 2.2 AA | **1 erreur** (`H25.1.NoTitleEl` sur `/`) | ⚠ — divergence avec Lighthouse, à investiguer |
| Headers HTTP runtime | 6/7 (CSP absent en local) | ⚠ — CSP n'est appliqué que sur Vercel CDN |
| `npm audit` | 0 HIGH/CRITICAL · **8 moderate** dont 2 prod direct (next-intl) | ⚠ |
| Tests unitaires | **0 test écrit** (`tests/{components,api,lib}/` vides) | ❌ régression vs claim Ph4 D3=8.5 |
| Section Manifest | 17/17 sections built + i18n présents | ✅ |
| Loi 25 (D8) | CookieConsent opt-in + RPP nommé + politique + mentions + finalité dans forms | ✅ |
| `[ville]` slot | 15 occurrences i18n + `site-info.json::city = "[ville]"` non résolues | ❌ bloquant pré-prod |

**μ recalculé = 6.79 / 10** ⟶ **NO DEPLOY** (seuil 8.5).

Verdict cohérent avec le statut « test jetable » du client. Le build est techniquement publiable mais **3 régressions réelles** invalident la note Ph4 auto-déclarée (9.06) :
1. CLS 0.502 (Footer post-hydration) — non mesurable au build, révélé par Lighthouse.
2. Aucun test écrit malgré 78 fichiers livrés.
3. Couverture tooling SSL impossible (audit local) → la couverture sécurité n'est validable qu'après deploy Vercel.

---

## SECTION 1 — IDENTIFICATION & STACK TECHNIQUE

### 1.1 Fiche d'identité
- Client : Dépanneur Nobert inc. (test E2E)
- Slug : `_e2e_validation_2026-05-08`
- Stack : Next.js 15.5.18 · TypeScript 5.7 strict · Tailwind 3.4.17 · next-intl 3.26.3 · React 19.0.0 · Vercel
- Pages : 6 routes × 2 locales = 12 pages SSG + 2 API routes + sitemap + robots = **19 pages prérendues**
- Bundle JS partagé : 102 KB gz (sous plafond 200 KB) ✓

### 1.2 Stack technologique
**Constat** — Stack imposée respectée à la lettre. `next/font` self-hosted (Fraunces 700/800 + Inter 400/600), `poweredByHeader: false`, App Router avec segment `[locale]`, pathnames localisés FR/EN.

### 1.3 Dépendances tierces (cf. `tooling/deps.json`)
| Package | Version installée | Statut |
|---|---|---|
| next | ^15.5.18 | ✅ post-bump CVE GHSA-3h52 + GHSA-67rr |
| next-intl | ^3.26.3 | ⚠ **2 vuln moderate** (open-redirect + prototype pollution) — fix = bump majeur 4.x |
| vitest | ^2.1.8 | ⚠ chaîne dev (esbuild, vite, vite-node) — 6 vuln moderate transitive |
| postcss (transitive via next) | < 8.5.10 | ⚠ XSS via `</style>` unescape (moderate) |
| react / react-dom | 19.0.0 | ✅ |
| framer-motion | ^11.11.17 | ✅ |
| zod | ^3.24.1 | ✅ |

**Total** : 568 dépendances · 36 prod / 497 dev / 108 optional / 10 peer.

---

## SECTION 2 — ARCHITECTURE & STRUCTURE

### 2.1 Architecture informationnelle
6 pages (home / promotions / produits / contact / politique-confidentialite / mentions-legales) × 2 locales. Structure cohérente avec brief.site.pages.

### 2.2 Analyse navigation
- Header sticky desktop + drawer mobile (focus-trap + ESC).
- Sticky CTA mobile (P11) caché sur `/promotions` (anti-doublon).
- Footer 3 colonnes : adresse + RPP visible + liens politique/mentions + bouton réinitialiser consentement.
- Skip-to-content présent.

### 2.3 Structure des routes
```
app/[locale]/{layout,page,loading,not-found,error}.tsx
app/[locale]/{contact,produits,promotions,politique-confidentialite,mentions-legales}/page.tsx
app/api/{contact,newsletter}/route.ts
app/{sitemap,robots}.ts
```
**Constat** — Architecture App Router flat conforme au scaffold-plan Ph1. 78 fichiers livrés, alignés. Aucun fichier hors-scope détecté.

---

## SECTION 3 — PERFORMANCE (LIGHTHOUSE RÉEL)

### 3.1 Core Web Vitals (mesure Lighthouse mobile, `tooling/lighthouse.json`)
| Métrique | Mesure | Seuil "good" | Statut |
|---|---|---|---|
| FCP (First Contentful Paint) | 0.9 s | ≤ 1.8 s | ✅ |
| LCP (Largest Contentful Paint) | **2.6 s** | ≤ 2.5 s | ⚠ borderline (score 0.88) |
| TTI (Time to Interactive) | 3.1 s | ≤ 3.8 s | ✅ |
| TBT (Total Blocking Time) | 10 ms | ≤ 200 ms | ✅ |
| Speed Index | 0.9 s | ≤ 3.4 s | ✅ |
| **CLS (Cumulative Layout Shift)** | **0.502** | ≤ 0.1 | ❌ **CRITIQUE** (score 0.16) |
| Server response time | 100 ms | — | ✅ |
| Total byte weight | 714 KiB | ≤ 1.6 MiB | ✅ |

**Constat critique — CLS 0.502 (5×× le seuil "poor" 0.25)**
- **Preuve** (`audits.layout-shifts.details`) : layout shift unique de 502 ms, ancré sur `body.min-h-screen > footer.border-t` (`<footer class="border-t border-border bg-surface-alt">`). Le `boundingRect` du footer passe de `top=6418, bottom=7080` après hydration : la page croît verticalement de ~660 px **après** rendu initial.
- **Cause racine probable** : montage post-hydration de composants client dans le layout (`StickyMobileCta`, `CookieConsent`, sticky CTA mobile). Ces composants sont fixed/absolute mais l'hydratation peut décaler les sections en flux jusqu'à ce que le footer atteigne sa position finale, ou le contenu Hero (image priorité) rapatrie la mesure tardivement.
- **Risque produit** : pénalité Google ranking (CWV failed), expérience utilisateur mobile dégradée — texte qui saute pendant la lecture.

### 3.2 Bundle analysis
- First Load JS shared : 102 KB gz · max page 159 KB gz (Home, qui charge `JsonLd LocalBusiness` + `NewsletterCta` client + `StickyCta`).
- **Unused JS détecté** : `chunks/603-0280051b9dee1624.js` — 26.7 KB transmis dont **22 KB inutilisés** (82.4 %). Économie estimée 21 KB / 150 ms.
- Legacy JavaScript : 12 KB économisables (script Polyfill).

### 3.3 Images
- Hero : `next/image` avec `priority`, `sizes` correct, `fill` + `aspect-[4/3]` lg:`aspect-[21/9]`.
- Toutes les images placeholders (PNG 1×1 cream à extension `.jpg`). **Risque** : LCP réel post-déploiement va dépendre de la photo réelle Nobert — si non-optimisée (>200 KB, non-WebP), le score perf chute.
- Image alt text : Lighthouse `image-alt` = 1 ✅.

### 3.4 Cache strategy
- `Cache-Control: private, no-cache, no-store, max-age=0, must-revalidate` sur le HTML — **désactive bfcache** (Lighthouse `bf-cache` = 0, 2 raisons : `MainResourceHasCacheControlNoStore` + `JsNetworkRequestReceivedCacheControlNoStoreResource`).
- `vercel.json` configure correctement `_next/static/*` (1 an immutable) et `images/*` (24h + SWR 7j).
- Render-blocking CSS : `7fe88ee229ad5d06.css` 5.9 KB / 158 ms blocking.
- Cache-insight : 17 KB économisables sur lifetimes statiques.

---

## SECTION 4 — SÉCURITÉ

### 4.1 Headers HTTP (curl -I réel, `tooling/headers.json`)
| Header | Présent runtime | vercel.json | Verdict |
|---|---|---|---|
| `X-Content-Type-Options: nosniff` | ✅ | ✅ | OK |
| `X-Frame-Options: DENY` | ✅ | ✅ | OK |
| `Referrer-Policy: strict-origin-when-cross-origin` | ✅ | ✅ | OK |
| `Permissions-Policy: camera=(), microphone=(), geolocation=()` | ✅ | ✅ | OK |
| `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` | ✅ | ✅ | OK (préchargé HSTS 2 ans) |
| `X-DNS-Prefetch-Control: on` | ✅ | ✅ | OK |
| **`Content-Security-Policy`** | ❌ **ABSENT** au runtime local | ✅ déclaré | ⚠ **non auditable avant deploy Vercel** |

**Constat** — La CSP déclarée dans `vercel.json` (`default-src 'self'; script-src 'self' 'unsafe-inline'; ...`) est appliquée par le CDN Vercel uniquement. Sur `next start` local, aucune CSP n'est émise. Cela signifie :
1. La règle absolue NEXOS « CSP TOUJOURS présente » est respectée **uniquement post-deploy**, pas en local.
2. La CSP elle-même contient `'unsafe-inline'` sur `script-src` et `style-src` — nécessaire pour Next.js inline scripts mais à durcir avec un nonce dynamique en post-deploy si possible.
3. La validation effective de CSP exigera un re-run du tooling sur l'URL Vercel (`https://depanneur-nobert.vercel.app`).

### 4.2 SSL/TLS (`tooling/ssl.json`)
**Constat** — `{"grade": "error", "error": "unable to connect to localhost:443"}`. Audit local sans HTTPS — **non applicable**. SSL ne sera auditable que post-deploy.

### 4.3 XSS & sanitisation
- **Audit code** : `dangerouslySetInnerHTML` utilisé **uniquement** dans `components/seo/JsonLd.tsx:10` pour injecter `application/ld+json` (vérifié via grep — toutes les autres occurrences sont des types React internes). ✅
- Formulaires : Zod schemas pour `/api/contact` et `/api/newsletter` + honeypot champ `hp` + rate-limit (3 et 5 req/h).
- Pas de `eval`, pas d'injection HTML utilisateur.

### 4.4 Dépendances (`tooling/deps.json` — npm audit réel)
**8 vulnérabilités moderate, 0 high, 0 critical.**

| Package | Sévérité | Direct ? | Avis | Action |
|---|---|---|---|---|
| `next-intl` | moderate | **prod direct** | open-redirect (GHSA-8f24) + prototype pollution (GHSA-4c35) | Bump → 4.11.1 (semver-major, à tester pour API change : `hasLocale` indispo en 3.26 → dispo en 4.x) |
| `next` (via postcss XSS GHSA-qx2v) | moderate | **prod direct** | postcss < 8.5.10 | `npm audit fix --force` ou attendre Next 16 |
| `vitest` + `@vitest/mocker` + `vite` + `vite-node` + `esbuild` | moderate | dev | chaîne dev — esbuild dev-server cross-origin (GHSA-67mh) | Bump vitest 2.1.8 → 4.1.5 (semver-major) |

**Verdict** — La règle absolue NEXOS (« 0 HIGH/CRITICAL ») est respectée. Mais 2 moderate **direct prod** (next-intl, next) sont des dettes à porter explicitement. Le bump next-intl 3 → 4 est non-trivial (changement d'API documenté Ph4 §3.2).

### 4.5 CSP
Voir 4.1 — déclaration vercel.json correcte, application post-deploy uniquement.

---

## SECTION 5 — SEO

### 5.1 Meta tags
**Constat critique — `meta-description` absent** (Lighthouse audit `meta-description` score 0).
- **Preuve** : la mesure Lighthouse a été faite sur `http://localhost:37015/` (URL racine). Le middleware next-intl **rewrite** vers `/fr` (`x-middleware-rewrite: /fr` dans `headers.json`), mais Lighthouse ne détecte pas la `<meta name="description">` dans le head retourné.
- **Cause probable** : la metadata du segment `[locale]/page.tsx` est résolue côté serveur via `generateMetadata` qui consomme `t('description')` — la chaîne est présente dans `messages/fr.json::home.meta.description` (« Le dépanneur de [ville]. Promotions chaque semaine, bières, snacks, loto Québec et dépannage… »). Mais elle contient le placeholder `[ville]` non résolu, ce qui pourrait expliquer un comportement Next.js (validation interne ?) ou — plus probablement — un effet de la cascade de metadata (layout root + page) lors d'un rewrite middleware.
- **Action** : remplacer `rewrite` par `redirect 308` de `/` vers `/fr` (recommandation next-intl 4.x), ou re-mesurer Lighthouse sur `/fr` directement (URL canonique).
- **Note** — `document-title` Lighthouse = 1 ✅ donc le `<title>` est bien présent. La divergence ne porte que sur la meta description.

### 5.2 Structured data (JSON-LD)
- Layout root injecte `Organization` + `WebSite`.
- Home injecte `LocalBusiness` + `ConvenienceStore` + `OpeningHoursSpecification` + `GeoCoordinates`.
- Contact reproduit `LocalBusiness` + `PostalAddress` + `ContactPoint`.
- ⚠ **Risque** — `addressLocality = "[ville]"` non résolu. Schema.org parsable mais valeur non-géolocalisable. Impact direct sur Google Knowledge Graph et Rich Results.

### 5.3 Sitemap & robots
- `app/sitemap.ts` : 12 URLs (6 routes × 2 locales) avec `alternates.languages` FR/EN. ✅
- `app/robots.ts` : `Allow: /` + `Disallow: /api/` + Sitemap link. ✅
- Lighthouse `robots-txt` = 1 ✅.

### 5.4 Liens cassés
- Audit code : tous les `Link` next-intl pointent vers des routes existantes (`/promotions`, `/produits`, `/contact`, `/politique-confidentialite`, `/mentions-legales`).
- ⚠ Lien cassé externe potentiel : `iframe` Google Maps avec `[ville]` placeholder — non résolvable côté Google.

---

## SECTION 6 — ACCESSIBILITÉ (PA11Y RÉEL)

### 6.1 WCAG 2.2 AA (`tooling/a11y.json`)
**1 erreur pa11y** :
```json
{"code":"WCAG2AA.Principle2.Guideline2_4.2_4_2.H25.1.NoTitleEl",
 "type":"error",
 "message":"A title should be provided for the document, using a non-empty title element in the head section.",
 "context":"<head><meta charset=\"utf-8\"><meta nam...</head>",
 "selector":"html > head"}
```

**Constat — divergence pa11y vs Lighthouse** : Lighthouse `document-title` = 1 (passe), pa11y déclare l'absence de `<title>`. Le `context` retourné est tronqué après `<meta nam...`, suggérant que pa11y a capturé un head **partiel** (rendu pre-hydration ?) ou un état avant que Next.js termine le streaming SSR. Lighthouse mesure post-rendu complet, pa11y semble plus précoce.

**Hypothèse de cause** : pa11y a cliblé `/` (URL racine) et la réponse middleware-rewrite a renvoyé une page transitoire dont le `<head>` était partiel au moment de l'analyse. C'est une **race condition d'audit**, pas une régression a11y du code.

**Action recommandée** :
1. Re-runner pa11y sur `http://localhost:37015/fr` (URL canonique non-rewritée) pour confirmer.
2. Si l'erreur persiste, ajouter un `<title>` statique dans le layout root en plus du système de metadata (fallback hard).

### 6.2 Contraste couleurs
- Lighthouse `color-contrast` = 1 ✅.
- Audit Ph2 confirmait : `text #2A1810` sur `background #FFF8E7` = 12.94:1 (AAA), `primary #8B4513` sur background = 7.91:1 (AAA). Accent `#FFD700` jamais utilisé comme texte (uniquement decoratif) — conforme.

### 6.3 Navigation clavier
Audit code (Hero, Header, Footer, CookieConsent) :
- `focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2` partout sur les CTA.
- `min-h-[48px]` touch targets.
- `SkipToContent` présent dans le layout.
- Drawer mobile : focus-trap + ESC handler (cf. build log §1.2).
- CookieConsent : `role="dialog" aria-modal="true" aria-label`.

### 6.4 ARIA
- Aucune dérive : `aria-hidden` sur les icônes Lucide décoratives, `aria-label` sur dialog, `<main id="main">` ciblé par SkipToContent.

---

## SECTION 7 — DESIGN & UX

### 7.1 Responsive
- Grilles Tailwind `sm:grid-cols-2 lg:grid-cols-3` cohérentes.
- Hero `aspect-[4/3]` mobile, `lg:aspect-[21/9]` desktop.
- StickyMobileCta visible mobile uniquement.

### 7.2 Design system cohérence
Palette imposée appliquée fidèlement (`tailwind.config.ts` reproduit le snippet Ph2) :
- Primary `#8B4513` ✅
- Accent `#FFD700` ✅
- Background `#FFF8E7` ✅
- Surface `#FFFFFF` / Surface-alt présent.
- Pas de bleu corporate détecté.

Typographie warm respectée : Fraunces (display) + Inter (body), self-hosted.

### 7.3 Animations & motion
- `prefers-reduced-motion` global dans `styles/globals.css` (désactive transitions/animations).
- Framer Motion présent en deps mais peu invoqué (audit code à confirmer pour usages spécifiques).

---

## SECTION 8 — CONTENU

### 8.1 Qualité rédactionnelle
Voix Ph3 conservée : ton convivial-authentique-québécois sans mots de la ban-list. Risque W02 Ph3 (densité « dépanneur » 2.23 % > 2 %) reporté — **non bloquant**.

### 8.2 i18n
- next-intl 3.26 + middleware FR/EN.
- Pathnames localisés : `/produits` ↔ `/products`, `/politique-confidentialite` ↔ `/privacy-policy`, `/mentions-legales` ↔ `/legal-notice`.
- `messages/fr.json` namespaces : `common`, `home` (6 sub), `promotions` (3), `produits` (4), `contact` (6), `legal` (3) — toutes sections du manifest couvertes.
- `alternates.languages` FR/EN/x-default sur toutes les pages via `buildMetadata()`.

### 8.3 Orthographe
**Constat ciblé** : 15 occurrences de `[ville]` literal dans `messages/{fr,en}.json` + 1 dans `site/data/site-info.json::city`. C'est **intentionnel** (kickoff bloquant documenté Ph4 §3.3) mais doit être résolu **avant prod**.

---

## SECTION 9 — CONFORMITÉ LÉGALE

### 9.1 Loi 25 (Québec) ✅
| Exigence | Évidence |
|---|---|
| Bandeau cookies opt-in 3 catégories | `components/layout/CookieConsent.tsx` — défaut `analytics: false, marketing: false`, bouton « Refuser tout » présent |
| RPP nommé visible | `Footer.tsx` ligne RPP (Nobert Tremblay) + `RppMention.tsx` (S-016) |
| Page politique de confidentialité | `app/[locale]/politique-confidentialite/page.tsx` (FR + EN alias `/privacy-policy`) |
| Page mentions légales | `app/[locale]/mentions-legales/page.tsx` (FR + EN alias `/legal-notice`) |
| Mention finalité près des formulaires | `ContactForm.tsx` + `NewsletterCta.tsx` — `purposeNotice` ajouté en itération 2 |
| Lien confidentialité près des formulaires | idem — `Link` next-intl vers `/politique-confidentialite` |
| Checkbox consentement non pré-cochée | Aucun `defaultChecked` détecté — RHF + Zod literal `true` |
| Incident process / RPP email | `nobert@depanneur-nobert.ca` configuré |

**Score D8 projeté** : 9.5/10 (correctifs W-14 itération 2 maintenus). Manque uniquement la résolution `streetAddress`/`postalCode`/`phone`/`neq` pour atteindre 10.0.

### 9.2 RGPD
Pas une cible (clientèle Québec uniquement). Les transferts hors-QC (Vercel US, Google Analytics US, Google Maps US) sont documentés conformément à la Loi 25 (équivalent suffisant).

### 9.3 Mentions légales
Template NEXOS interpolé avec `brief.legal.*`. Placeholders `{streetAddress}`, `{postalCode}`, `{phone}`, `{neq}` non valorisés (risque Ph4).

---

## SECTION 10 — TESTS

### 10.1 Couverture
**Constat catastrophique** : `tests/{components,api,lib}/` existent mais **vides** (aucun fichier `.test.ts`/`.test.tsx`). Le script `vitest run` retourne 0 test.

### 10.2 Tests manquants
Critique pour KPI conversion (Hero CTA), API routes (Loi 25), formulaires (consentement) :
- `Hero.test.tsx` — vérifier rendu CTA primaire + lien `/promotions`.
- `NewsletterCta.test.tsx` — Zod consent literal `true` + honeypot ignoré.
- `ContactForm.test.tsx` — idem + 4 champs.
- `api/newsletter.test.ts` — rate-limit 5/h, 429 + Retry-After.
- `api/contact.test.ts` — rate-limit 3/h.
- `lib/seo.test.ts` — buildMetadata canonicals + alternates.
- `lib/structured-data.test.ts` — JSON-LD Organization + LocalBusiness.

**Score D3 réel** : 2.0/10 (vs claim Ph4 8.5). C'est la **plus grosse régression** vs le build log.

---

## SECTION 11 — CODE QUALITY

### 11.1 TypeScript
- `tsc --noEmit` : 0 erreur (Ph4 confirmé).
- `tsconfig.json` strict + `noUncheckedIndexedAccess`.
- 78 fichiers source, types dédiés `types/{promotion,product,site-info}.ts`.

### 11.2 ESLint
- `eslint-config-next` + `eslint-plugin-jsx-a11y`.
- Aucun warning bloquant signalé Ph4.

### 11.3 Conventions
- Imports absolus via `@/`.
- `useTranslations()` partout — 0 chaîne en dur (vérifié Ph4 §1.2).
- `data-manifest-id="S-NNN"` présent sur toutes les sections (audit code Hero confirme).
- Documentation : aucun README dans `site/` — reporté Ph5 backlog mais non livré ici. Dette D2 réelle.

---

## Section Manifest Coverage

Audit des 17 sections — fichier composant + namespace i18n + import dans `page.tsx`.

| ID | Page | Section | Composant | i18n | Statut audit |
|----|------|---------|-----------|------|--------------|
| S-001 | home | Hero | ✅ `Hero.tsx` | ✅ `home.hero` | audited |
| S-002 | home | PromoWeekTeaser | ✅ | ✅ `home.promoTeaser` | audited |
| S-003 | home | CategoriesOverview | ✅ | ✅ `home.categories` | audited |
| S-004 | home | InfosPratiques | ✅ | ✅ `home.infosPratiques` | audited |
| S-005 | home | LeMotDuProprio | ✅ | ✅ `home.motProprio` | audited |
| S-006 | home | NewsletterCta | ✅ | ✅ `home.newsletter` | audited |
| S-007 | promotions | HeroPromoWeek | ✅ | ✅ `promotions.hero` | audited |
| S-008 | promotions | PromosGrid | ✅ | ✅ `promotions.grid` | audited |
| S-009 | produits | HeroProduits | ✅ | ✅ `produits.hero` | audited |
| S-010 | produits | CategoriesGrid | ✅ | ✅ `produits.categoriesGrid` | audited |
| S-011 | produits | CategorySection | ✅ | ✅ `produits.category` | audited |
| S-012 | contact | HeroContact | ✅ | ✅ `contact.hero` | audited |
| S-013 | contact | Coordonnees | ✅ | ✅ `contact.coordonnees` | audited |
| S-014 | contact | Horaires | ✅ | ✅ `contact.horaires` | audited |
| S-015 | contact | ContactForm | ✅ | ✅ `contact.form` | audited |
| S-016 | contact | RppMention | ✅ | ✅ `contact.rpp` | audited |
| S-017 | legal | LegalContent | ✅ | ✅ `legal.content` | audited |

**17/17 sections audited** — aucun composant manquant, aucun namespace i18n manquant. Manifest mis à jour : `lifecycle.ph5_audited = "2026-05-09T06:30:00Z"`, `status = "audited"`.

---

## SECTION 12 — SCORE GLOBAL & RECOMMANDATIONS

### 12.1 Scores par dimension (SOIC D1-D9)

| Dim | Domaine | Note Ph4 (claim) | Note Ph5 (réelle) | Δ | Justification Ph5 |
|-----|---------|------------------|-------------------|---|-------------------|
| **D1** Architecture (×1.0) | Build SSG 19 pages, scaffold strict, 17 sections built | 9.0 | **9.0** | 0 | Aucune régression structurelle |
| **D2** Documentation (×0.8) | README absent, ADR/runbook documentés monorepo | (n/a) | **6.0** | — | Pas de README site/, déclarations dans changelog uniquement |
| **D3** Tests (×0.9) | Vitest configuré, suite annoncée | 8.5 | **2.0** | **−6.5** | **0 fichier de test écrit** |
| **D4** Sécurité (×1.2) | 7 headers + CSP vercel.json, 0 H/C, audit local sans HTTPS/CSP | 9.5 | **7.5** | −2.0 | CSP non auditable avant deploy + 2 prod-direct moderate vulns |
| **D5** Performance (×1.0) | Bundle OK, claim sous plafonds Ph1 | 8.5 | **5.0** | **−3.5** | **CLS 0.502 critique**, LCP 2.6 s borderline, perf 0.76 |
| **D6** Accessibilité (×1.1) | jsx-a11y, focus-visible, prefers-reduced-motion | 9.0 | **7.5** | −1.5 | pa11y 1 erreur (NoTitleEl) — divergence à investiguer ; Lighthouse a11y = 1.0 |
| **D7** SEO (×1.0) | Sitemap + robots + JSON-LD + buildMetadata | 8.5 | **6.5** | −2.0 | meta-description manquant à `/`, `[ville]` non résolu (15 occurrences) |
| **D8** Loi 25 (×1.1) | CookieConsent + RPP + politique + mentions + finalité forms | 9.5 | **9.5** | 0 | Conservé itération 2 — manque uniquement `{streetAddress}` et co. |
| **D9** Code Quality (×0.9) | TS strict, ESLint, 0 erreur build | 8.5 | **7.0** | −1.5 | Pas de tests, pas de README, sinon nickel |

### 12.2 μ global

```
Σ (note × poids) = 9.0×1.0 + 6.0×0.8 + 2.0×0.9 + 7.5×1.2 + 5.0×1.0 + 7.5×1.1 + 6.5×1.0 + 9.5×1.1 + 7.0×0.9
                = 9.00 + 4.80 + 1.80 + 9.00 + 5.00 + 8.25 + 6.50 + 10.45 + 6.30
                = 61.10
Σ poids        = 1.0 + 0.8 + 0.9 + 1.2 + 1.0 + 1.1 + 1.0 + 1.1 + 0.9 = 9.00
μ              = 61.10 / 9.00 = 6.79 / 10
```

**μ = 6.79 / 10**

| Seuil | Valeur | Verdict |
|---|---|---|
| Deploy (μ ≥ 8.5) | 6.79 | ❌ **NO DEPLOY** |
| Boucle corrective (μ < 8.5) | 6.79 | ✅ ré-itération requise OU acceptation du statut « test jetable » |

> **Note métier** — ce client est explicitement tagué **« E2E validation pipeline nexos create — test jetable »** dans `brief-client.json::_meta.phase_origin`. Le verdict NO DEPLOY ne contredit pas le succès du test E2E pipeline : il **mesure honnêtement** la qualité réelle du build et révèle 3 régressions vs auto-claim Ph4. C'est précisément le rôle du Phase 5 audit.

### 12.3 Top 5 actions prioritaires

| # | Action | Dim | Effort | Impact |
|---|--------|-----|--------|--------|
| **P1** | **Corriger CLS 0.502** (FOOTER) — réserver hauteur explicite pour StickyMobileCta + CookieConsent (ex. `pb-[88px]` sur `<main>` quand sticky CTA visible mobile, `min-h-[160px]` sur le bandeau cookie pre-hydration via SSR-safe placeholder). Re-mesurer Lighthouse. | D5 | M | μ +0.4 (D5 5→8) |
| **P2** | **Écrire 6 tests minimaux** : `Hero.test.tsx`, `NewsletterCta.test.tsx`, `ContactForm.test.tsx`, `api/newsletter.test.ts`, `api/contact.test.ts`, `lib/seo.test.ts`. Cible coverage critical-path 60 %. | D3 | M | μ +0.5 (D3 2→7) |
| **P3** | **Résoudre `[ville]` + `streetAddress`/`postalCode`/`phone`/`neq`** au kickoff via search-and-replace dans `messages/{fr,en}.json` + `site/data/site-info.json`. **Bloquant pré-prod**. | D7+D8 | S | μ +0.2 (D7 6.5→8.5, D8 9.5→10) |
| **P4** | **Re-mesurer Lighthouse + pa11y sur `/fr`** (URL canonique, pas `/`) après remplacement du middleware `rewrite` par `redirect 308`. Élimine les 2 incohérences meta-description et NoTitleEl. | D6+D7 | S | μ +0.2 |
| **P5** | **Bumper next-intl 3.26 → 4.11.1** (semver-major) pour fixer les 2 vulns moderate prod direct (open-redirect + prototype pollution). Adapter `routing.ts` (`hasLocale`) et tester pathnames localisés. | D4 | M | μ +0.2 (D4 7.5→9.0) |

**μ post-correctifs P1-P5 projeté : ~8.3** — toujours sous le seuil 8.5, donc une 6ᵉ itération sur D2 (README) + D9 (lint warnings résiduels) serait nécessaire pour atteindre DEPLOY.

### 12.4 Roadmap corrections

**Itération 3 — correctifs critiques (1-2 j)** :
1. Fix CLS Footer (P1) — adjust layout reservations, re-run Lighthouse.
2. Écrire 6 tests P2 — `vitest run` doit reporter coverage > 0.
3. Résoudre placeholders kickoff (P3) — search-replace.

**Itération 4 — durcissement (1 j)** :
4. `redirect 308` `/` → `/fr` à la place du `rewrite` (P4).
5. Bump next-intl 4.x (P5).

**Itération 5 — finition (½ j)** :
6. Écrire `site/README.md` (D2 → 8.5).
7. Re-runner full preflight + lighthouse + pa11y → cible μ ≥ 8.5.

**Décision opérationnelle pour ce client précis** : étant donné le statut « test jetable », **archiver le client tel quel** sans appliquer les itérations 3-5. Le rapport documente les écarts pour informer la **boucle d'amélioration du pipeline NEXOS lui-même**, pas ce client.

---

## Décisions transverses pour le pipeline NEXOS (recommandations Ph0+)

L'audit révèle 3 trous systémiques dans le pipeline `nexos create`, à corriger **côté pipeline**, pas côté client :

1. **Ph4 `build-validator` ne mesure pas le CLS** — il valide BUILD PASS uniquement (compilation, audit, types). La régression CLS 0.502 a été invisible jusqu'à Ph5. **Action** : ajouter à `nexos/build_validator.py` un step Lighthouse léger post-build qui block si CLS > 0.25.
2. **Ph4 ne vérifie pas que `tests/` contient au moins N tests** — un livrable « 78 fichiers » avec 0 test passe BUILD PASS. **Action** : ajouter règle `tests_min_count >= 5` dans le validator.
3. **`auto_fixer.py` ne touche pas au `[ville]` placeholder** — alors que c'est documenté comme bloquant pré-prod. **Action** : ajouter un fix `auto_fixer::resolve_brief_placeholders` qui fail-fast si des placeholders subsistent et que `brief-client.json::client.locations` est résolu.

Ces 3 améliorations devraient être trackées comme **chantier d'amélioration pipeline NEXOS v4.3** (séparé de ce client).

---

## Verdict final

```
μ = 6.79 / 10
verdict = NO DEPLOY
status = "test jetable" — verdict honoré sans application des correctifs (archivage)
section_manifest = 17/17 audited
```

**Phase 5 close** — section-manifest.json mis à jour, changelog logué, audit livré.
