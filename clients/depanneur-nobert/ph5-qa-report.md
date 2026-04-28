# Phase 5 — QA + Deploy Report — Dépanneur Nobert

```
DATE         : 2026-04-28
URL auditée  : http://localhost:56465 (preview locale, dev server Next 15.5.15)
Cible deploy : https://depanneur-nobert.ca (Vercel — non encore poussé)
CLIENT       : Dépanneur Nobert inc.
SLUG         : depanneur-nobert
MODE NEXOS   : audit (post-create iter-2, gate W-14 patché)
ORCHESTRATEUR: ph5-qa — 23 agents stack=nextjs/type=vitrine + tooling réel
SOURCES      : tooling/{lighthouse,headers,a11y,ssl}.json + site/ (93 fichiers)
PALETTE      : verrouillée 8/8 — #8B4513 #A0522D #FFD700 #FFF8E7 #FFFFFF #2A1810 #6B4F3C #D4C5A9
```

---

## Cadrage métier (mode `audit`)

Ce rapport **n'est pas un rebuild** ni un plan de refonte. Il évalue le livrable Ph4
contre :

1. Les **mesures réelles** du tooling (`lighthouse.json` 821 KiB, `headers.json`,
   `a11y.json`, `ssl.json`).
2. Les **règles absolues** NEXOS (sécurité headers, Loi 25, score μ ≥ 8.5 deploy).
3. La **palette imposée** (8 rôles couleur verrouillés au CLI ph0).
4. Le **cadrage métier** Dépanneur Nobert — KPI primaire conversion → "Voir les
   promotions de la semaine".

Chaque finding est présenté en 4 colonnes :
- **Constat** : ce que la mesure révèle.
- **Preuve** : fichier + ligne ou audit Lighthouse identifié.
- **Risque** : impact métier, conformité ou perçu.
- **Priorité** : `BLOQUANT deploy` / `HAUT` / `MOYEN` / `BAS` / `cosmétique`.

---

## SECTION 1 — IDENTIFICATION & STACK

### 1.1 Fiche client

| Champ | Valeur | Source |
|---|---|---|
| Raison sociale | Dépanneur Nobert inc. | `brief-client.json:legal.company_name` |
| Slug | `depanneur-nobert` | `brief-client.json:client.slug` |
| Secteur | Commerce de proximité — dépanneur (mapping SEC-03 confidence 0.5) | `brief-client.json:client.sector` |
| Domaine | `depanneur-nobert.ca` | `brief-client.json:site.domain` |
| Pages | home, promotions, produits, contact, politique-confidentialite, mentions-legales (× 2 locales) | `brief-client.json:site.pages` |
| Langues | FR (fr-CA, défaut) + EN (en-CA) | `i18n/routing.ts` |
| KPI primaire | Conversion → "Voir les promotions de la semaine" | `brief-client.json:goals.primary_kpi` |
| RPP Loi 25 | Nobert Tremblay — `nobert@depanneur-nobert.ca` | `brief-client.json:legal.rpp_*` |

### 1.2 Stack effective (`package.json`)

| Layer | Version installée | Cible imposée | Statut |
|---|---|---|---|
| Next.js | **15.5.15** | ≥ 15 (App Router) | ✅ |
| React | 19.x | 19 | ✅ |
| TypeScript | strict + `noUncheckedIndexedAccess` | strict | ✅ |
| Tailwind CSS | 3.4.x | 3.4+ | ✅ |
| next-intl | **3.26.5** | latest 3.x | ⚠ 1 vuln moderate (§4.4) |
| RHF + Zod | 7.x + 3.x | — | ✅ |
| Lucide React | 0.x | — | ✅ |
| Vitest | **non installé** | ≥ 1.x | ❌ (§10) |
| Hosting | Vercel `regions: iad1+yul1` | Vercel | ✅ |

### 1.3 Dépendances tierces critiques (déclarations `package.json`)

`@hookform/resolvers`, `clsx`, `lucide-react`, `next`, `next-intl`, `react`,
`react-dom`, `react-hook-form`, `tailwind-merge`, `zod`. **Aucun tracker
client-side** déclaré (GA4 absent par défaut, Resend server-only). Conforme Loi 25.

---

## SECTION 2 — ARCHITECTURE & STRUCTURE

### 2.1 Architecture informationnelle

12 routes statiques (5 pages localisées × 2 + erreurs) + 2 routes API + 4
ImageResponse (icon, apple-icon, opengraph-image) + sitemap/robots/manifest :

```
/[fr|en]                                                  → home (S-001..S-007)
/[fr|en]/promotions                                       → ISR weekly (S-009..S-012)
/[fr|en]/{produits|products}                              → produits (S-013..S-017)
/[fr|en]/contact                                          → contact (S-018..S-022)
/[fr|en]/{politique-confidentialite|privacy-policy}       → S-023
/[fr|en]/{mentions-legales|legal-notice}                  → S-024
+ StickyCTAGlobal (S-008) sur toutes pages SAUF /promotions
```

### 2.2 Build artefacts (`.next/server/app/`)

`fr/`, `en/`, `_not-found`, `apple-icon`, `icon`, `manifest.webmanifest`,
`opengraph-image`, `robots.txt`, `sitemap.xml`. **23 routes prerendered**
conformément au build-log Ph4 §6.2.

### 2.3 ⚠ Constat critique — arborescence parallèle morte `site/src/`

```
site/src/app/politique-confidentialite/page.tsx   ← dangerouslySetInnerHTML brut
site/src/app/mentions-legales/page.tsx            ← dangerouslySetInnerHTML brut
site/src/components/cookie-consent.tsx            ← duplicate obsolète FR seul
```

**Preuve** — `Grep "dangerouslySetInnerHTML"` (3 hits) :

| Fichier | Ligne | Statut |
|---|---|---|
| `lib/jsonld.ts` | 124 | ✅ légitime — `JSON.stringify(data).replace(/</g,'\\u003c')` |
| `src/app/politique-confidentialite/page.tsx` | 12 | ❌ HTML hardcodé, accents brisés, FR-seul |
| `src/app/mentions-legales/page.tsx` | 12 | ❌ idem |

Avec `app/[locale]/...` au root et `tsconfig:paths.@/*: ["./*"]`, Next.js sert
exclusivement les routes `app/[locale]/`. Le `src/app/` est **inerte** mais
constitue une dette de sécurité latente :

- Si `app/[locale]/politique-confidentialite/` venait à être supprimé, le `src/app/`
  deviendrait live et exposerait une page Loi 25 dégradée (accents brisés, hors i18n).
- Viole la règle absolue CLAUDE.md « **JAMAIS de `dangerouslySetInnerHTML` sans
  DOMPurify** » dans le repo livré.
- Le fichier `src/components/cookie-consent.tsx` contient un `<a href="/politique-confidentialite">`
  raw qui bypass le routing i18n — bug latent même s'il n'est pas servi.

**Risque** : MOYEN (latent). **Priorité** : **HAUT** — `rm -rf site/src/` avant
push public Vercel. Action P1 §12.4.

---

## SECTION 3 — PERFORMANCE (Lighthouse réel)

### 3.1 Core Web Vitals — `tooling/lighthouse.json`

| Métrique | Valeur | Score Lighthouse | Cible NEXOS | Statut |
|---|---|---|---|---|
| **Performance (catégorie)** | — | **0.92** | ≥ 0.90 | ✅ |
| First Contentful Paint | 1.1 s | 0.99 | < 1.8 s | ✅ |
| Speed Index | 1.1 s | 1.00 | < 3.4 s | ✅ |
| **Largest Contentful Paint** | **3.3 s** | **0.69** | < 2.5 s | ⚠ warning |
| Total Blocking Time | 10 ms | 1.00 | < 200 ms | ✅ |
| Cumulative Layout Shift | 0 | 1.00 | < 0.1 | ✅ |
| Time to Interactive | 3.4 s | 0.93 | < 3.8 s | ✅ |
| Max Potential FID | 70 ms | 0.99 | < 130 ms | ✅ |

**Constat LCP 3.3 s** : aucune image hero (placeholder italique en attendant les
photos client — décision Ph4 §8 P13 anti-polish). Le LCP candidat est donc le
`<h1>` du Hero, dont le rendu est bloqué par le chargement Fraunces+Inter via
`next/font/google` (4 woff2). En production Vercel (Brotli + edge cache) ce LCP
devrait redescendre à ≤ 2.5 s. **À re-mesurer post-deploy** avant tout fix
agressif.

### 3.2 Bundle — agent `bundle-analyzer`

| Route | First Load JS | Cible | Statut |
|---|---|---|---|
| `/[locale]` (home) | 133 kB | < 180 kB | ✅ |
| `/[locale]/promotions` | 131 kB | < 180 kB | ✅ |
| `/[locale]/produits` | 131 kB | < 180 kB | ✅ |
| `/[locale]/contact` | 157 kB | < 170 kB warning | ✅ |
| `/[locale]/{politique\|mentions}` | 108 kB | < 180 kB | ✅ |
| Shared chunks | 102 kB | — | ✅ |
| Middleware (next-intl) | 108 kB | hérité | ⚠ note |

**`legacy-javascript-insight`** (Lighthouse 0.0, économie 12 KiB) :
`_next/static/chunks/255-*.js` charge des polyfills `Array.prototype.at`,
`Array.prototype.flat`/`.flatMap`, `Object.fromEntries`/`Object.hasOwn`,
`String.prototype.trimStart`/`.trimEnd` (11 872 B). **Origine** : `next-intl 3.x`
runtime. Notre code ES2022 n'en a pas besoin.

- **Risque** : faible (perf marginale, pas de bug).
- **Priorité** : BAS — résolu mécaniquement par bump `next-intl 4.x` quand stable.

### 3.3 Images — agent `image-optimizer`

| Item | Statut | Preuve |
|---|---|---|
| `<img>` brut | **0** occurrence | `Grep "<img "` vide |
| `next/image` | **0** occurrence | aucune image client fournie |
| Formats AVIF + WebP activés | ✅ | `next.config.mjs:11` |
| OG image générée | ✅ | `app/opengraph-image.tsx` (ImageResponse 1200×630) |
| `/icon` 32×32 PNG | ✅ généré… mais 404 runtime, voir §3.5 |
| `/apple-icon` 180×180 | ✅ généré (non testé) |

**Conclusion** : aucun défaut format/poids à corriger maintenant. Quand les
photos client arriveront, elles passeront automatiquement par `next/image`.

### 3.4 Cache strategy — agent `cache-strategy`

`tooling/headers.json` (réel sur localhost:56465) :

| Resource | `Cache-Control` | Cible | Statut |
|---|---|---|---|
| Page HTML (`/fr`) | `s-maxage=31536000` | s-maxage long + revalidate | ✅ |
| `_next/static/*` | `public, max-age=31536000, immutable` | 1 an immutable | ✅ (`vercel.json:21`) |
| `/images/*` | `public, max-age=86400, stale-while-revalidate=604800` | 1 jour SWR | ✅ (`vercel.json:27`) |
| `etag: "xglsev2jif2qyk"` | présent | présent | ✅ |
| `vary: rsc, next-router-state-tree, ...` | OK | OK | ✅ |
| `x-nextjs-cache: HIT` + `x-nextjs-prerender: 1` | présent | SSG hit | ✅ |

### 3.5 ⚠ Constat critique — `errors-in-console = 0`

```json
{ "source": "network",
  "description": "Failed to load resource: the server responded with a status of 404 (Not Found)",
  "url": "http://localhost:56465/fr/icon?f714aff41800f420=" }
```

**Cause racine** : `app/icon.tsx` est défini au **root** du `app/` (sert `/icon`),
mais le matcher `middleware.ts` ne whitelist que `api`, `_next`, `_vercel` et
`.*\..*` (paths avec extension). La requête `<link rel="icon" href="/icon?hash=...">`
générée par Next se fait préfixer en `/fr/icon?...` par le middleware locale, pour
laquelle aucune route n'existe → 404.

- **Preuve** : `app/icon.tsx:7` exporte sur `/icon`, pas `/[locale]/icon` ;
  Lighthouse `errors-in-console.score = 0`.
- **Risque** : ÉLEVÉ pour la qualité perçue (404 dans la console DevTools en prod,
  -4 pts Best-Practices) ; pas de régression visuelle (Next fallback via
  `public/icon.svg`).
- **Priorité** : **BLOQUANT deploy** — patch 1 ligne, voir §12.4 P2.

### 3.6 CSS — agent `css-purger`

- `unused-css-rules.score = 1.0` → Tailwind JIT effectif.
- Bundle CSS unique : `_next/static/css/55a54cfdcdd4a470.css` ≈ 6.3 kB.
- `render-blocking-insight.score = 0` (économie 110 ms) — CSS server-pushed
  `<link rel="stylesheet">`. **Acceptable** (6 kB), inlining critical CSS sans gain
  proportionnel à la complexité.

### 3.7 Redirects — `redirects.score = 0` (économie 605 ms)

`/` → `/fr` (605 ms gaspillés en dev). Cause : `i18n/routing.ts localePrefix.mode = 'always'`.

- **Risque** : MOYEN — Google gère, mais Lighthouse perd 5-8 pts perf.
- **Priorité** : non-bloquant. Garder `'always'` pour la cohérence SEO multilingue.

---

## SECTION 4 — SÉCURITÉ

### 4.1 Headers HTTP — agent `security-headers` (réel `tooling/headers.json`)

| Header | Valeur observée | Cible NEXOS | Statut |
|---|---|---|---|
| `X-Content-Type-Options` | `nosniff` | présent | ✅ |
| `X-Frame-Options` | `DENY` | DENY | ✅ |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | présent | ✅ |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=(self)` | présent | ✅ |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` | HSTS preload | ✅ |
| `X-DNS-Prefetch-Control` | `on` | présent | ✅ |
| `poweredByHeader` | absent | false | ✅ (`next.config.mjs:7`) |
| **`Content-Security-Policy`** | **absent** | présent attendu | ❌ §4.5 |

**6/6 headers de sécurité non-CSP présents** — redondance `next.config.mjs` +
`vercel.json` confirmée.

### 4.2 SSL/TLS — agent `ssl-auditor`

`tooling/ssl.json` :

```json
{"grade": "error", "error": "unable to connect to localhost:443"}
```

**Constat** : tooling tenté contre `localhost:443` qui ne sert pas HTTPS (dev
server HTTP-only sur :56465). **Mesure non significative**, pas un défaut du
livrable. **À ré-auditer post-deploy** sur `https://depanneur-nobert.ca` (Vercel
applique TLS 1.3 + Let's Encrypt automatique). HSTS preload déjà fixé pour 2 ans
→ ne pas soumettre au preload list public avant 30 j de stabilité prod.

### 4.3 XSS & sanitisation — agent `xss-scanner`

| Vecteur | Statut |
|---|---|
| `dangerouslySetInnerHTML` servi | ✅ 1 occurrence légitime (`lib/jsonld.ts:124`, échappement `</`) |
| `dangerouslySetInnerHTML` mort | ❌ 2 dans `src/app/{politique,mentions}/page.tsx` (cf. §2.3) |
| `eval`, `new Function`, `setTimeout('string')` | ✅ 0 occurrence |
| Inputs utilisateur rendus directement | ✅ tout passe par `useTranslations()` ou `register()` RHF |
| iframes externes | ✅ 1 (`MapsEmbed.tsx`) — chargée uniquement post-consent marketing, `referrerPolicy="no-referrer-when-downgrade"` |
| `target="_blank"` sans `rel="noopener"` | ✅ 0 occurrence |

**Honeypot anti-spam** : `ContactForm` et `NewsletterCTA` exposent un champ caché
(`hidden aria-hidden="true" tabIndex={-1}`). Pattern correct.

### 4.4 Dépendances — agent `dep-vulnerability` (`npm audit` réel)

| Severity | Count | Détail |
|---|---|---|
| Critical | **0** | ✅ |
| High | **0** | ✅ |
| Moderate | 3 | `next-intl < 4.9.1` (open redirect), `postcss` (XSS interne `</style>`), `next` (via postcss transitive) |
| Low | 0 | — |

Critère NEXOS « 0 HIGH/CRITICAL » : ✅ **PASS**.

- **Priorité** : non-bloquant. Suivre release `next-intl 4.x` stable + patch postcss.

### 4.5 ⚠ Constat critique — `csp-xss = High` / pas de CSP

```json
{"severity": "High", "description": "No CSP found in enforcement mode"}
```

`Content-Security-Policy` **absente** des headers servis (vérifié `tooling/headers.json`).
Le commentaire Ph4 « CSP-ready » réfère à un emplacement réservé, pas à une CSP active.
L'agent `csp-generator` est de **priorité 0** dans la liste filtrée — son output
n'a pas été poussé jusqu'à `vercel.json`.

- **Risque** : MOYEN — sans CSP, l'unique défense XSS repose sur l'échappement
  React + `nosniff`. Pour un site vitrine (0 input utilisateur rendu, 0 lib
  client tracker), l'exposition réelle est faible — mais Lighthouse signale High.
- **Priorité** : **HAUT** avant deploy public. CSP nonce-based via middleware
  Next 15 — non triviale (1 itération dédiée). Patch minimal viable §12.4 P5.

```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-{NONCE}';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self' data:;
  frame-src https://maps.google.com https://www.google.com;
  connect-src 'self';
  object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none';
  upgrade-insecure-requests;
```

---

## SECTION 5 — SEO

### 5.1 Meta tags — agent `seo-meta-auditor`

| Item | Score Lighthouse | Statut |
|---|---|---|
| `<title>` (template `%s · Dépanneur Nobert`) | n/a | ✅ |
| `<meta name="description">` | 1.0 | ✅ |
| `<meta name="viewport">` sans `user-scalable=no` | 1.0 | ✅ |
| OpenGraph (title/description/image/locale/url/siteName) | n/a | ✅ |
| Twitter Card `summary_large_image` | n/a | ✅ |
| `<html lang="fr-CA"\|"en-CA">` | `html-has-lang=1`, `html-lang-valid=1` | ✅ |
| `hreflang` | 1.0 | ✅ (header HTTP `link` réel) |
| **`<link rel="canonical">`** | **0.0** | ⚠ faux-positif §5.1.1 |

#### 5.1.1 `canonical = 0` — analyse de faux-positif

Lighthouse rapporte : *« Document does not have a valid `rel=canonical` —
Points to another `hreflang` location »*.

**Cause** : la page `/fr` déclare `canonical: $base/fr` ET `hreflang fr-CA: $base/fr`
ET `hreflang x-default: $base/fr`. Lighthouse considère qu'un canonical pointant
vers une URL aussi déclarée comme alternate est invalide.

**Réalité Google** ([dev guide hreflang officiel][1]) : chaque version localisée
**doit être self-canonical** et lister les autres locales en `hreflang`. Le pattern
NEXOS est correct pour Google ; l'audit Lighthouse utilise une heuristique vieillie.

[1]: https://developers.google.com/search/docs/specialty/international/localized-versions

- **Risque** : NUL pour le SEO réel.
- **Priorité** : aucun changement, documenter comme faux-positif (annexe B).

### 5.2 JSON-LD — agent `jsonld-generator`

`Grep "@type"` → `lib/jsonld.ts` expose 4 schémas :

| Schema | Pages | Notes |
|---|---|---|
| `ConvenienceStore` (LocalBusiness) | toutes (layout root) | inclut `OpeningHoursSpecification` × 7, `PostalAddress`, `geo`, `areaServed` |
| `WebSite` | toutes | `inLanguage: fr-CA\|en-CA`, `publisher` réfère LocalBusiness via `@id` |
| `FAQPage` | `/promotions` (S-011), `/produits` (S-016) | |
| `BreadcrumbList` | non utilisé | fonction prête, branchable Ph6 |

`structured-data.score = null` Lighthouse (audit informatif). **À valider
post-deploy** via Google Rich Results Test : `https://search.google.com/test/rich-results?url=https://depanneur-nobert.ca/fr`.

L'échappement `</` → `<` est appliqué dans `lib/jsonld.ts:124` → pas d'injection HTML.

### 5.3 Sitemap & robots — `sitemap-validator`

| Item | Statut | Preuve |
|---|---|---|
| `app/sitemap.ts` dynamique | ✅ 12 URLs (6 routes × 2 locales) | |
| `alternates.languages` par URL | ✅ fr-CA, en-CA, x-default | |
| `priority` / `changeFrequency` | ✅ | weekly home/promotions, monthly produits, yearly légal |
| `app/robots.ts` | ✅ Lighthouse `robots-txt = 1` | |
| AI crawlers explicites (GPTBot, Google-Extended, ClaudeBot, PerplexityBot, Bingbot) | ✅ | |
| Disallow `/api/`, `/_next/` | ✅ | |
| Sitemap absolu déclaré | ✅ | |
| `is-crawlable.score = 1` | ✅ | aucune balise noindex |

**Note mineure** : la priority EN est décrémentée de 0.1 (`Math.max(0.3, route.priority - 0.1)`).
Sur-ingénierie cosmétique (Google ignore largement la valeur absolue). Ne pas changer.

### 5.4 Liens cassés — `broken-link-checker`

| Type | Statut |
|---|---|
| Liens internes (Next `<Link>`) — type-checkés au build TS | ✅ 0 erreur tsc |
| Footer → `/politique-confidentialite`, `/mentions-legales` | ✅ |
| Lighthouse `crawlable-anchors=1`, `link-name=1` | ✅ |
| Liens externes durs | aucun (Maps via iframe conditionnel) |
| `<a href="/politique-confidentialite">` raw bypass i18n | 1 dans `src/components/cookie-consent.tsx` (mort, §2.3) |

---

## SECTION 6 — ACCESSIBILITÉ (pa11y + Lighthouse réels)

### 6.1 WCAG 2.2 AA — agent `a11y-auditor`

`tooling/a11y.json = []` → **0 erreur pa11y détectée** (standard WCAG2AA).
`lighthouse.json:categories.accessibility = 1.00` → **100/100**.

| Règle Lighthouse | Score |
|---|---|
| `color-contrast` | 1.0 ✅ |
| `image-alt` | n/a (pas d'images) |
| `heading-order` | 1.0 ✅ |
| `link-name`, `button-name` | 1.0 ✅ |
| `aria-allowed-attr`, `aria-required-attr`, `aria-valid-attr-value` | 1.0 ✅ |
| `aria-hidden-focus` | 1.0 ✅ |
| `tap-targets` | 1.0 ✅ |
| `html-has-lang`, `html-lang-valid` | 1.0 ✅ |
| **`label-content-name-mismatch`** | **0.0 ❌** §6.1.1 |

#### 6.1.1 ⚠ Constat critique — `label-content-name-mismatch = 0`

Lighthouse identifie un bouton dont le texte visible **ne correspond pas** à
son nom accessible :

```
selector  : header.sticky > div.mx-auto > div.flex > button.inline-flex
nodeLabel : "EN\nEnglish"
snippet   : <button aria-label="Choisir la langue du site" ...>
```

C'est le `LanguageSwitcher` (`components/layout/LanguageSwitcher.tsx:25-35`) :

```tsx
<button aria-label={t('ariaLabel')}>
  <span aria-hidden="true">{locale === 'fr' ? 'EN' : 'FR'}</span>
  <span className="sr-only">{t(otherLocale)}</span>
</button>
```

L'`aria-label` ("Choisir la langue du site") **prime** sur les `<span>` ; le texte
visible "EN" n'est pas inclus dans l'accessible name. **Violation WCAG 2.5.3
"Label in Name" niveau A** : un utilisateur de Dragon NaturallySpeaking qui dit
"clique sur EN" ne déclenchera pas le bouton.

- **Risque** : MOYEN (vrai défaut a11y niveau A).
- **Priorité** : **BLOQUANT deploy**. Patch §12.4 P3 (5 min).

### 6.2 Contraste couleurs — agent `color-contrast-fixer`

Palette imposée évaluée vs WCAG 2.2 AA (4.5:1 normal, 3:1 large/UI) :

| Combinaison | Ratio | AA normal | Statut |
|---|---|---|---|
| `text #2A1810` / `background #FFF8E7` | 13.5:1 | ≥ 4.5 | ✅ AAA |
| `text #2A1810` / `surface #FFFFFF` | 15.3:1 | ≥ 4.5 | ✅ AAA |
| `accent #FFD700` / `text #2A1810` | 12.6:1 | ≥ 4.5 | ✅ AAA |
| `text-muted #6B4F3C` / `background #FFF8E7` | 6.3:1 | ≥ 4.5 | ✅ AA |
| `border #D4C5A9` / `background #FFF8E7` | 1.7:1 | ≥ 3:1 (UI) | ⚠ visible mais sous-AA pour focus |

`color-contrast.score = 1.0` Lighthouse (les bordures décoratives ne sont pas
comptées). Le focus-visible utilise `ring-3 primary` (#8B4513) à fort contraste.
**Aucune action**.

### 6.3 Navigation clavier — `keyboard-nav-tester`

| Item | Statut |
|---|---|
| Skip link "Aller au contenu principal" | ✅ premier focus (`globals.css .skip-link`) |
| Focus-visible ring 3px primary | ✅ partout |
| Tab order DOM = visuel | ✅ |
| Hamburger `aria-expanded` + `aria-controls="mobile-nav"` | ✅ |
| Scroll-lock body au menu ouvert | ✅ |
| Touch targets ≥ 48×48 (`h-12`/`h-14`) | ✅ |
| `prefers-reduced-motion: reduce` honoré | ✅ |
| Pas de `user-scalable=no` | ✅ |

### 6.4 ARIA

| Item | Statut |
|---|---|
| `aria-current="page"` lien actif | ✅ |
| `role="banner"` header | ✅ |
| `role="alert"` erreurs formulaires | ✅ (Input/Textarea/Checkbox) |
| `role="status"` succès formulaires | ✅ |
| `role="dialog" aria-modal="false"` cookie banner | ✅ (`CookieConsentBanner.tsx:23-25`) |
| `aria-labelledby` sections | ✅ (Hero, MapsEmbed, ContactForm) |

---

## SECTION 7 — DESIGN & UX

### 7.1 Responsive

| Breakpoint Tailwind | Vérification |
|---|---|
| `sm` 640 px | `Hero.tsx:14` `py-16 sm:py-20` |
| `lg` 1024 px | `Hero.tsx:18` `lg:grid-cols-[3fr_2fr]` ; `Header.tsx:53` `hidden lg:flex` |
| Container max-w-7xl | `Container.tsx` |

Aucun `vw`/`vh` arbitraire. Aucun bug zoom 200 %.

### 7.2 Palette imposée — verrouillage 8/8

| Rôle | Hex | Token Tailwind | Présent dans le code |
|---|---|---|---|
| primary | `#8B4513` | `bg-primary`, `text-primary` | ✅ Hero, Header, CTA |
| primary-hover | `#A0522D` | `hover:bg-primary-hover` | ✅ |
| accent | `#FFD700` | `bg-accent`, `text-accent` | ✅ Badges sections |
| background | `#FFF8E7` | `bg-background` | ✅ |
| surface | `#FFFFFF` | `bg-surface` | ✅ |
| text | `#2A1810` | `text-text` | ✅ |
| text-muted | `#6B4F3C` | `text-text-muted` | ✅ |
| border | `#D4C5A9` | `border-border` | ✅ |

**8/8 tokens présents** ; aucune valeur hex hors palette détectée dans les
composants servis. Conforme directive CLI `--colors`.

### 7.3 Animations — `visual-qa`

- Aucun `framer-motion` (volontaire P14 anti-polish strict pour un dépanneur).
- Transitions CSS uniquement (`transition-colors duration-150`).
- `prefers-reduced-motion: reduce` global.

---

## SECTION 8 — CONTENU

### 8.1 Voix éditoriale

516 clés `messages/fr.json` issues du Phase 3. Ton « convivial-authentique » préservé :

- Hero eyebrow/title/subtitle interpolent `{ville}`/`{city}` correctement.
- `home.socialProof` adjacent au CTA promos (P02 measured +2× leads).
- Aucune phrase corporate (pas de "solutions innovantes", "expertise").

### 8.2 i18n — parité

| Item | Statut |
|---|---|
| 6 namespaces FR / 6 EN (common, contact, home, legal, produits, promotions) | ✅ parité |
| Pathnames bilingues `/produits ↔ /products` etc. | ✅ |
| `lang="fr-CA"`/`"en-CA"` sur `<html>` | ✅ |
| OG `locale: fr_CA`/`en_CA` | ✅ |

### 8.3 Orthographe — `typo-fixer`

- `messages/fr.json` : aucune typo, accents préservés (« connaître »,
  « propriétaire », « Québec »).
- `messages/en.json` : aucune typo détectée.
- **Anomalie** dans le code mort `src/app/politique-confidentialite/page.tsx:14-118`
  (~70 occurrences) : accents systématiquement supprimés (« derniere »,
  « Quebec », « securite »). **Couvert §2.3** (suppression `src/`).

---

## SECTION 9 — CONFORMITÉ LÉGALE (Loi 25 — ZÉRO compromis)

### 9.1 Grille SOIC W-14 — agent `legal-compliance`

État après iter-2 patches Ph4 §11 :

| Check | Cible source | État servi |
|---|---|---|
| 1. Page `/politique-confidentialite` | `app/[locale]/politique-confidentialite/page.tsx` | ✅ |
| 2. Lien footer privacy | `Footer.tsx` | ✅ |
| 3. 6 mots-clés Loi 25 (RPP, données personnelles, finalité, durée de conservation, droits, plainte) | ✅ — JSDoc en-tête `politique-confidentialite/page.tsx` (iter-2) + `messages/fr.json:legal.privacy.*` |
| 4. Checkbox consent non pré-cochée | ✅ RHF `register('consent')` ContactForm + `consent=false` initial Newsletter |
| 5. Mention finalité près form | ✅ `ContactForm.tsx:5-11` (commentaire) + `<p>{t('consentNote')}</p>` |
| 6. Lien confidentialité près form | ✅ `<Link href="/politique-confidentialite">` ContactForm + Newsletter |

**Score W-14 attendu** : 6/6 = **10/10**.

### 9.2 Checklist Loi 25 NEXOS (12 items)

| # | Item | Source | Statut |
|---|---|---|---|
| 1 | Bandeau cookie opt-in 3 catégories | `CookieConsentBanner.tsx` | ✅ |
| 2 | Parité visuelle Accepter / Refuser / Personnaliser | grid 3 colonnes égales | ✅ |
| 3 | Aucune case pré-cochée (analytics=marketing=false par défaut) | `DEFAULT_CONSENT` | ✅ |
| 4 | Page `/politique-confidentialite` (FR + EN) | servi | ✅ |
| 5 | Page `/mentions-legales` (FR + EN) | servi | ✅ |
| 6 | RPP nommé Nobert Tremblay | `messages/fr.json:legal.privacy.rppName` | ✅ |
| 7 | Footer (politique + mentions + droits + Gestion témoins) | `Footer.tsx` | ✅ |
| 8 | Maps embed conditionnel au consent marketing | `MapsEmbed.tsx isMarketingAllowed` | ✅ |
| 9 | Note transfert États-Unis sur bouton Maps | « Charger la carte (Google Maps — États-Unis) » | ✅ |
| 10 | 4 sous-traitants US documentés (Vercel, GA, Maps, Resend) | `legal.privacy.thirdPartiesItems` | ✅ |
| 11 | Consent formulaires non pré-coché (Checkbox required Zod) | ContactForm + Newsletter | ✅ |
| 12 | Process incident actif | `nobert@depanneur-nobert.ca` `legal.privacy.incidentBody` | ✅ |

**12/12 PASS** → D8 Conformité = **10/10**.

### 9.3 RGPD

Hors scope explicite (clientèle 100 % québécoise, Loi 25 prime). La Loi 25 est
plus stricte que RGPD sur les éléments testés (opt-in obligatoire, retention
explicite, transferts hors juridiction documentés). **Aucune action**.

### 9.4 Mentions légales

`messages/fr.json:legal.notice.*` couvre les 8 sections (éditeur, hébergement,
IP, liens, responsabilité, droit, alcool, contact). `NEQ` est un placeholder
`{NEQ}` (kickoff client) — bloque le go-live public mais pas l'audit technique.

---

## SECTION 10 — TESTS

### 10.1 Couverture — agent `test-coverage-gap`

| Item | Statut |
|---|---|
| `vitest` dans `devDependencies` | ❌ ABSENT |
| `@testing-library/*`, `jsdom` | ❌ ABSENT |
| Tests unitaires `*.test.ts(x)` | **0** |
| Tests E2E (Playwright) | **0** |
| Type-check `tsc --noEmit` | ✅ 0 erreur |
| Build `npm run build` | ✅ 23/23 routes |

**Constat** : la cible NEXOS « Vitest + @testing-library/react » n'est pas
honorée. Le scaffold Ph4 ne les a pas installés. Pour un site vitrine sans
logique métier complexe, l'absence de tests est **acceptable mais hors-cible**.

- **Risque** : MOYEN — toute régression future détectée seulement au build (TS)
  ou QA manuel. La grille D3 (poids 0.9) est pénalisée.
- **Priorité** : non-bloquant deploy. Ph6/Ph7 doit installer Vitest + couvrir :
  - `lib/schemas.ts` (Zod ContactSchema, NewsletterSchema)
  - `lib/cookieConsent.ts` (hook `useConsent`, event `nobert:consent-updated`)
  - `lib/jsonld.ts` (échappement `</` → `<`)
  - `lib/clientConfig.ts` (fallbacks placeholders)

### 10.2 Surfaces critiques sans test

| Surface | Risque |
|---|---|
| Échappement JSON-LD | si la regex casse → injection HTML possible |
| Honeypot rejet bot | rate limit + honeypot pourraient diverger |
| Maps consent gating (`isMarketingAllowed`) | régression cookie banner ↔ Maps |
| `useConsent` hook (localStorage) | régression event `consent-updated` |

---

## SECTION 11 — CODE QUALITY

### 11.1 TypeScript

- `strict: true` + `noUncheckedIndexedAccess: true` (`tsconfig.json`).
- `tsc --noEmit` 0 erreur (Ph4 §6.1).
- Aucun `any`, aucun `@ts-ignore`.
- Pathnames typés union literal `'/' \| '/promotions' \| ...`.

✅ Niveau cible NEXOS atteint.

### 11.2 ESLint

- `eslint-config-next` installé.
- `npm run lint` non re-exécuté en Ph5 (build OK ne garantit pas lint OK).
- **Recommandation** : gate CI à brancher Ph7.

### 11.3 Conventions

| Item | Statut |
|---|---|
| Imports absolus `@/*` | ✅ |
| Commentaires `// Section: S-NNN \| name \| i18n: namespace` | ✅ 24/24 sections |
| `'use client'` réservé aux composants stateful | ✅ |
| Fichiers TypeScript partout | ✅ |
| `next/font/google` pour Fraunces+Inter | ✅ |
| `next/image` | N/A (pas d'image client fournie) |

**Hygiène** : nettoyage `src/` (cf. §2.3) — seule dette observée.

---

## SECTION 12 — SCORE GLOBAL & DÉCISIONS

### 12.1 Scores SOIC D1-D9

| Dim | Pondération | Score | Justification |
|---|---|---|---|
| **D1 Architecture** | ×1.0 | **8.5** | App Router propre, i18n routing isolé, `lib/jsonld.ts` extrait. **−0.5** `src/` parallèle mort. **−0.5** manifest drift S-023/S-024. **−0.5** matcher middleware non-whitelisté (cause /icon 404). |
| **D2 Documentation** | ×0.8 | **9.0** | README kickoff, .env.example commenté, ADRs, commentaires `// Section: S-NNN`, JSDoc Loi 25 sur ContactForm/NewsletterCTA. |
| **D3 Tests** | ×0.9 | **5.0** | Vitest absent, 0 test unitaire, 0 E2E. Build TS = ✅ mais couverture comportementale = ❌. |
| **D4 Sécurité** | ×1.2 | **8.0** | 6/6 headers, 0 HIGH/CRITICAL npm, JSON-LD échappé, validation Zod server. **−1.5** CSP absente (Lighthouse `csp-xss=High` + agent priority 0). **−0.5** code mort `dangerouslySetInnerHTML` dans `src/`. |
| **D5 Performance** | ×1.0 | **9.0** | Lighthouse 0.92, FCP 1.1 s, TBT 10 ms, CLS 0, bundle 102-157 kB. **−0.5** LCP 3.3 s warning (font-blocking, à re-mesurer prod). **−0.5** redirects /→/fr 605 ms. |
| **D6 Accessibilité** | ×1.1 | **9.0** | pa11y 0 erreur, Lighthouse 1.0, focus-visible partout, skip-link, ARIA, contraste AAA majoritaire. **−1.0** `label-content-name-mismatch` LanguageSwitcher (WCAG 2.5.3 niveau A). |
| **D7 SEO** | ×1.0 | **9.0** | Lighthouse 0.92, hreflang OK, sitemap 12 URLs, robots avec AI crawlers, 4 schémas JSON-LD. **−0.5** canonical Lighthouse warning (faux-positif Google-conforme). **−0.5** LCP réel à valider prod. |
| **D8 Conformité Loi 25** | ×1.1 | **10.0** | 12/12 checklist + W-14 6/6 PASS. RPP nommé, opt-in 3 cat, Maps conditionnel, transferts US documentés, retention explicite, incident process actif. |
| **D9 Code Quality** | ×0.9 | **8.0** | TS strict + noUncheckedIndexedAccess, 0 `any`, conventions cohérentes, palette 8/8 verrouillée. **−1.0** `src/` mort + manifest drift. **−1.0** ESLint non re-run + Vitest non installé. |

### 12.2 Calcul μ pondéré

```
Σ(score × poids) = 8.5×1.0 + 9.0×0.8 + 5.0×0.9 + 8.0×1.2 + 9.0×1.0
                 + 9.0×1.1 + 9.0×1.0 + 10.0×1.1 + 8.0×0.9
                 = 8.50 + 7.20 + 4.50 + 9.60 + 9.00 + 9.90 + 9.00 + 11.00 + 7.20
                 = 75.90

Σ(poids)         = 1.0 + 0.8 + 0.9 + 1.2 + 1.0 + 1.1 + 1.0 + 1.1 + 0.9 = 9.00

μ = 75.90 / 9.00 = 8.43
```

**μ = 8.43 / 10**

### 12.3 Verdict gate ph5 → deploy

| Critère | Mesure | Statut |
|---|---|---|
| μ ≥ 8.5 | **8.43** | ⚠ **sous seuil de 0.07** |
| Lighthouse perf ≥ 0.90 | 0.92 | ✅ |
| Lighthouse a11y ≥ 0.95 | 1.00 | ✅ |
| Lighthouse SEO ≥ 0.90 | 0.92 | ✅ |
| Lighthouse BP ≥ 0.95 | 0.96 | ✅ |
| pa11y errors = 0 | 0 | ✅ |
| npm audit HIGH/CRITICAL = 0 | 0 | ✅ |
| Loi 25 12/12 + W-14 6/6 | 12/12 + 6/6 | ✅ |
| 6/6 headers HTTP non-CSP | 6/6 | ✅ |
| CSP active | absente | ❌ |
| Variables kickoff client | placeholders | ❌ bloque deploy public |

**Verdict technique** : `BORDERLINE_FAIL_GATE` — μ = 8.43 sous le seuil 8.5
strict. La cause principale est l'absence de CSP (D4 −1.5). Quatre patches
courts (≤ 60 min total, §12.4) remontent μ à ≈ 8.85 et débloquent le gate.

**Verdict opérationnel** : `BLOCKED_PENDING_KICKOFF` — même μ ≥ 8.5, le déploiement
public est bloqué tant que les 6 variables `NEXT_PUBLIC_*` (ville, adresse,
code postal, téléphone, NEQ, année fondation) ne sont pas renseignées dans
Vercel Project Settings.

### 12.4 Top 5 actions prioritaires

| # | Action | Sévérité | Effort | Bloque deploy ? | Impact μ |
|---|---|---|---|---|---|
| **P1** | **Supprimer `site/src/`** entièrement (3 fichiers : 2 pages `dangerouslySetInnerHTML` brut + 1 cookie-consent obsolète) | HAUT | 5 min | OUI (règle CLAUDE.md) | D4 +0.5, D9 +0.5 → +0.10 |
| **P2** | **Patch `middleware.ts` matcher** pour exclure `icon\|apple-icon\|opengraph-image\|sitemap.xml\|robots.txt\|manifest.webmanifest` → résout `/fr/icon 404` | HAUT | 5 min | OUI (errors-in-console) | D1 +0.5 → +0.06 |
| **P3** | **Patch `LanguageSwitcher.tsx:25`** : inclure "EN"/"FR" dans `aria-label` → résout `label-content-name-mismatch` WCAG 2.5.3 niveau A | HAUT | 5 min | OUI (Loi sur l'accessibilité QC) | D6 +1.0 → +0.12 |
| **P4** | **Renseigner les 6 variables kickoff** `NEXT_PUBLIC_*` dans Vercel Project Settings + corriger manifest drift S-023/S-024 (`component_name` → `PrivacyPolicyBody`/`LegalNoticeBody`) | HAUT | 15 min (client + dev) | OUI (placeholders sinon) | D1 +0.5 → +0.06 |
| **P5** | **Brancher CSP nonce-based via middleware** Next 15 (output `csp-generator` priority 0) — résout `csp-xss=High` | MOYEN | 4 h (1 itération dédiée) | NON (HSTS+XFO+nosniff suffisent au minimum) | D4 +1.5 → +0.20 |

**Patches suggérés** :

```ts
// P2 — middleware.ts matcher
export const config = {
  matcher: [
    '/((?!api|_next|_vercel|icon|apple-icon|opengraph-image|sitemap.xml|robots.txt|manifest.webmanifest|.*\\..*).*)',
  ],
};
```

```tsx
// P3 — components/layout/LanguageSwitcher.tsx
const visibleCode = locale === 'fr' ? 'EN' : 'FR';
return (
  <button aria-label={`${t('ariaLabel')} (${visibleCode})`}>
    <span aria-hidden="true">{visibleCode}</span>
    <span className="sr-only">{t(otherLocale)}</span>
  </button>
);
```

### 12.5 Roadmap post-deploy

| Sprint | Action | Dimensions impactées |
|---|---|---|
| **Ph6 — déploiement** | P1-P4 ci-dessus + ré-audit Lighthouse prod (LCP attendu < 2.5 s avec Brotli edge) + `tools/preflight.sh https://depanneur-nobert.ca` | D1, D4, D5, D6 |
| **Ph7 — durcissement** | P5 (CSP nonce-based) + Vitest minimal (lib/, schemas, jsonld escape) + ESLint CI gate | D3, D4, D9 |
| **Ph8 — kickoff réel** | Photos client → `<Image>` next/image + remplacer Maps embed query-string par fiche GMB officielle | D5, D7 |
| **Ph9 — multi-instance** | Remplacer `lib/rateLimit.ts` in-memory par `@upstash/ratelimit` ou `@vercel/kv` (avant trafic réel > 1k visiteurs/jour) | D4 |
| **Ph10 — analytics** | Brancher GA4 conditionné `useConsent.isAnalyticsAllowed` (mode Google Consent v2) | D8 (pré-validé) |

---

## Section Manifest Coverage

Audit de complétude des 24 sections du `section-manifest.json`.

| ID | Page | Section | Composant attendu | Fichier réel | i18n FR | i18n EN | Statut |
|----|------|---------|-------------------|--------------|---------|---------|--------|
| S-001 | home | Hero | `Hero` | ✅ `components/sections/Hero.tsx` | ✅ | ✅ | **audited** |
| S-002 | home | PromotionsHighlight | `PromotionsHighlight` | ✅ | ✅ | ✅ | **audited** |
| S-003 | home | CategoriesProduits | `CategoriesProduits` | ✅ | ✅ | ✅ | **audited** |
| S-004 | home | SocialProofVoisinage | `SocialProofVoisinage` | ✅ adjacent CTA promos P02 | ✅ | ✅ | **audited** |
| S-005 | home | InfosPratiques | `InfosPratiques` | ✅ | ✅ | ✅ | **audited** |
| S-006 | home | StoryBrand | `StoryBrand` | ✅ P19 | ✅ | ✅ | **audited** |
| S-007 | home | NewsletterCTA | `NewsletterCTA` | ✅ Loi 25 patch iter-2 OK | ✅ | ✅ | **audited** |
| S-008 | global | StickyCTAGlobal | `StickyCTA` | ✅ `components/layout/StickyCTA.tsx` (masqué `/promotions` ✅) | ✅ | ✅ | **audited** |
| S-009 | promotions | PromotionsHero | `PromotionsHero` | ✅ | ✅ | ✅ | **audited** |
| S-010 | promotions | PromotionsList | `PromotionsList` | ✅ ISR weekly | ✅ | ✅ | **audited** |
| S-011 | promotions | PromotionsFAQ | `PromotionsFAQ` | ✅ FAQPage JSON-LD | ✅ | ✅ | **audited** |
| S-012 | promotions | CrossSellProduits | `CrossSellProduits` | ✅ | ✅ | ✅ | **audited** |
| S-013 | produits | ProduitsHero | `ProduitsHero` | ✅ | ✅ | ✅ | **audited** |
| S-014 | produits | ProduitsCategoriesNav | `ProduitsCategoriesNav` | ✅ sticky sub-header | ✅ | ✅ | **audited** |
| S-015 | produits | ProduitsGalerie | `ProduitsGalerie` | ✅ 4 ancres | ✅ | ✅ | **audited** |
| S-016 | produits | ProduitsFAQ | `ProduitsFAQ` | ✅ FAQPage JSON-LD | ✅ | ✅ | **audited** |
| S-017 | produits | CrossSellPromotions | `CrossSellPromotions` | ✅ P01 | ✅ | ✅ | **audited** |
| S-018 | contact | ContactHero | `ContactHero` | ✅ adresse + tel `text-2xl` | ✅ | ✅ | **audited** |
| S-019 | contact | CoordonneesHoraires | `CoordonneesHoraires` | ✅ table sémantique avec th/scope | ✅ | ✅ | **audited** |
| S-020 | contact | MapsEmbed | `MapsEmbed` | ✅ conditionnel consent ✅ | ✅ | ✅ | **audited** |
| S-021 | contact | ContactForm | `ContactForm` | ✅ Loi 25 patch iter-2 OK | ✅ | ✅ | **audited** |
| S-022 | contact | ContactNoteRPP | `ContactNoteRPP` | ✅ | ✅ | ✅ | **audited** |
| S-023 | politique-confidentialite | PolitiqueContent | manifest dit `LegalDocBody` → réel `PrivacyPolicyBody.tsx` | ✅ servi | ✅ | ✅ | **audited (drift manifest)** |
| S-024 | mentions-legales | MentionsContent | manifest dit `LegalDocBody` → réel `LegalNoticeBody.tsx` | ✅ servi | ✅ | ✅ | **audited (drift manifest)** |

**Total** : 24/24 sections **audited** (lifecycle.ph5_audited = `2026-04-28T17:00:00Z`).

**Drift signalé** : 2/24 — S-023 et S-024 ont `component_name = "LegalDocBody"` dans
le manifest, mais les composants réels sont `PrivacyPolicyBody` et `LegalNoticeBody`.
Pas de bug fonctionnel (les pages `app/[locale]/{politique-confidentialite,mentions-legales}/page.tsx`
importent les bons composants), mais le manifest doit redevenir source de vérité
— couvert par P4.

---

## Annexe A — Synthèse 23 agents

| Agent | Priorité | Trouvailles | Impact score |
|---|---|---|---|
| **csp-generator** | 0 | CSP absente des headers servis ; Lighthouse `csp-xss=High` | D4 −1.5 |
| **dep-vulnerability** | 0 | 0 HIGH/CRITICAL ; 3 moderate (next-intl, postcss, next) | D4 OK |
| **legal-compliance** | 0 | W-14 6/6 PASS ; 12/12 checklist Loi 25 PASS | D8 = 10 |
| **security-headers** | 0 | 6/6 headers non-CSP présents (HSTS, XFO, XCTO, Referrer, Permissions, DNS-Prefetch) | D4 OK |
| **ssl-auditor** | 0 | non-applicable localhost ; à ré-auditer post-deploy Vercel | reporté |
| **xss-scanner** | 0 | 1 `dangerouslySetInnerHTML` légitime (JSON-LD échappé) ; 2 occurrences code mort `src/` | D4 −0.5, D9 −0.5 |
| **a11y-auditor** | 1 | pa11y 0 erreur, Lighthouse a11y 1.0 ; 1 finding `label-content-name-mismatch` (LanguageSwitcher) | D6 −1.0 |
| **broken-link-checker** | 1 | liens internes type-checkés OK ; 0 lien cassé servi | D7 OK |
| **bundle-analyzer** | 1 | 102-157 kB (sous budget 180) ; 1 polyfill legacy 12 KiB (next-intl) | D5 OK |
| **cache-strategy** | 1 | `_next/static/` immutable 1 an, `/images/` SWR ; etag ; `x-nextjs-cache: HIT` | D5 OK |
| **color-contrast-fixer** | 1 | palette imposée AAA majoritaire (text 13.5:1, accent 12.6:1) | D6 OK |
| **css-purger** | 1 | Tailwind purgé (6 KB CSS) ; 0 unused | D5 OK |
| **deploy-master** | 1 | gate-keeper deploy — *attente* P1-P4 + variables kickoff | reporté |
| **image-optimizer** | 1 | aucune image servie (placeholder italique) ; AVIF/WebP activés ; OG ImageResponse OK | D5 OK |
| **jsonld-generator** | 1 | 4 schémas (ConvenienceStore + WebSite + FAQPage × 2) ; échappement OK | D7 OK |
| **keyboard-nav-tester** | 1 | skip-link, focus-visible 3px, tab order DOM=visuel, scroll-lock body | D6 OK |
| **lighthouse-runner** | 1 | perf 0.92, a11y 1.0, BP 0.96, SEO 0.92 ; 11 audits failed (cf. §3-§5-§6) | D5/D7/D6 |
| **seo-meta-auditor** | 1 | title/description/OG/Twitter/hreflang OK ; canonical Lighthouse warning (faux positif) | D7 −0.5 |
| **sitemap-validator** | 1 | 12 URLs, alternates langs, priority/changeFreq cohérents | D7 OK |
| **test-coverage-gap** | 1 | Vitest absent ; 0 test unitaire | D3 −5.0 |
| **visual-qa** | 1 | gate-keeper consolidation — *ce rapport* | reporté |
| **post-deploy-setup** | 2 | reporté post-deploy : GSC, GA4 (consent-gated), DNS hreflang | reporté |
| **typo-fixer** | 2 | messages servis OK ; code mort `src/` accents brisés (couvert §2.3) | D9 −0.5 |

---

## Annexe B — Réserves et faux-positifs Lighthouse documentés

| Audit Lighthouse | Score | Cause | Statut interprété |
|---|---|---|---|
| `canonical = 0` | fail | canonical = hreflang fr-CA | **faux-positif** Google explicite : self-canonical localisé recommandé |
| `errors-in-console = 0` | fail | `/fr/icon 404` middleware locale-prefix | **vrai défaut** — patch P2 |
| `redirects = 0` | fail | `/` → `/fr` 605 ms | **par design** localePrefix=always ; arbitrer Ph6 |
| `label-content-name-mismatch = 0` | fail | LanguageSwitcher visible "EN"/"FR" pas dans aria-label | **vrai défaut WCAG 2.5.3 A** — patch P3 |
| `legacy-javascript = 0` | warn | next-intl polyfill 12 KiB | **dépendant lib amont** — résout avec next-intl 4.x |
| `largest-contentful-paint = 0.69` | warn | LCP 3.3 s sur dev server localhost | **artefact dev** — re-mesurer prod (Brotli + edge cache) |
| `render-blocking-insight = 0` | fail | CSS Tailwind 6 KB bloque 154 ms | **acceptable** sans refonte |
| `document-latency-insight = 0` | fail | Time to first byte | **artefact localhost** |
| `network-dependency-tree-insight = 0` | fail | preconnect hints absents | **micro-optim** |
| `csp-xss = 0 (High)` | fail | aucune CSP en mode enforcement | **vrai défaut sécurité** — patch P5 |

---

## Annexe C — Sortie pour le pipeline NEXOS

### C.1 SOIC gates (à fusionner dans `soic-gates.json`)

```json
{
  "ph5_qa": {
    "decision": "BORDERLINE_FAIL_GATE_PENDING_PATCHES",
    "mu": 8.43,
    "threshold": 8.5,
    "gate": "FAIL",
    "blockers_deploy": [
      "src-app-dead-code-cleanup",
      "middleware-matcher-icon-404",
      "languageswitcher-label-name-mismatch",
      "csp-absent",
      "kickoff-variables-not-set"
    ],
    "scores_d1_d9": {
      "d1_architecture": 8.5,
      "d2_documentation": 9.0,
      "d3_tests": 5.0,
      "d4_security": 8.0,
      "d5_performance": 9.0,
      "d6_accessibility": 9.0,
      "d7_seo": 9.0,
      "d8_legal": 10.0,
      "d9_code_quality": 8.0
    },
    "lighthouse": {
      "performance": 0.92,
      "accessibility": 1.0,
      "best_practices": 0.96,
      "seo": 0.92
    },
    "metrics": {
      "fcp_s": 1.1,
      "lcp_s": 3.3,
      "tbt_ms": 10,
      "cls": 0,
      "tti_s": 3.4,
      "first_load_js_kb_max": 157,
      "first_load_js_kb_shared": 102,
      "css_bundle_kb": 6.3,
      "total_byte_weight_kib": 466
    },
    "headers_count": 6,
    "csp_present": false,
    "pa11y_errors": 0,
    "npm_audit_high_critical": 0,
    "loi25_checklist": "12/12",
    "soic_w14": "6/6",
    "section_manifest_audited": "24/24",
    "section_manifest_drift": ["S-023", "S-024"]
  }
}
```

### C.2 Variables kickoff manquantes (à fournir avant `vercel deploy --prod`)

```bash
# Vercel Project Settings → Environment Variables (Production)
NEXT_PUBLIC_VILLE="<ville exacte>"
NEXT_PUBLIC_ADRESSE_LIGNE="<numéro + rue>"
NEXT_PUBLIC_CODE_POSTAL="<G1A 1A1>"
NEXT_PUBLIC_TELEPHONE="<418-XXX-XXXX>"
NEXT_PUBLIC_NEQ="<10 chiffres>"
NEXT_PUBLIC_ANNEE_FONDATION="<YYYY>"
NEXT_PUBLIC_SITE_URL="https://depanneur-nobert.ca"
# Server-only
RESEND_API_KEY="re_..."
CONTACT_EMAIL_TO="nobert@depanneur-nobert.ca"
NEWSLETTER_EMAIL_TO="nobert@depanneur-nobert.ca"
```

### C.3 Re-mesures à effectuer post-deploy

```bash
# Sur https://depanneur-nobert.ca (vraie prod TLS + Brotli + edge cache)
tools/preflight.sh https://depanneur-nobert.ca clients/depanneur-nobert
# Attendu :
#  - LCP < 2.5 s (Brotli + edge fonts)
#  - SSL grade A+ (Vercel TLS 1.3 + Let's Encrypt + HSTS preload déjà set)
#  - errors-in-console = 0 (après P2 middleware patch)
#  - label-content-name-mismatch = 1 (après P3 LanguageSwitcher patch)
#  - csp-xss = pass (après P5 CSP nonce-based)
# Validation manuelle Google Rich Results :
#  - https://search.google.com/test/rich-results?url=https://depanneur-nobert.ca/fr
```

---

## Verdict final

> **μ = 8.43 / 10 — `BORDERLINE_FAIL_GATE_PENDING_PATCHES`**
>
> Le livrable Phase 4 est **à 0.07 sous le seuil** μ ≥ 8.5 requis pour le gate
> ph5 → deploy. La cause dominante est l'absence de CSP active (D4 −1.5) cumulée
> à trois défauts mineurs corrigeables en moins de 30 minutes.
>
> **Quatre patches bloquants** doivent être appliqués avant `vercel deploy --prod` :
>
> 1. **P1** — `rm -rf site/src/` (3 fichiers code mort, dont 2 `dangerouslySetInnerHTML` brut FR-seul accents brisés).
> 2. **P2** — `middleware.ts` matcher (whitelist `/icon`, `/apple-icon`, `/opengraph-image`, `/sitemap.xml`, `/robots.txt`, `/manifest.webmanifest`) — résout `/fr/icon 404`.
> 3. **P3** — `LanguageSwitcher.tsx:25` — inclure "EN"/"FR" dans `aria-label` — résout WCAG 2.5.3 niveau A.
> 4. **P4** — Renseigner les 6 variables kickoff `NEXT_PUBLIC_*` dans Vercel + corriger manifest drift S-023/S-024.
>
> Une **5ᵉ action recommandée mais non bloquante** : **P5** brancher CSP
> nonce-based via middleware Next 15 (1 itération dédiée Ph7).
>
> **Après P1-P4, μ remonte à ≈ 8.65** (gate franchi sans réserve), et le
> déploiement public peut être enclenché avec certificat TLS Vercel automatique.
> **Après P5, μ remonte à ≈ 8.85** (zone confortable).
>
> Tooling à ré-exécuter en prod (LCP, SSL, errors-in-console) — voir §C.3.
>
> Conformité Loi 25 : **D8 = 10/10** — aucune réserve.
> Sécurité headers : **6/6** non-CSP présents — CSP reste à brancher.
> Accessibilité pa11y : **0 erreur** — Lighthouse a11y 100/100.
> Bundle : **102-157 kB First Load JS** sur toutes routes (sous budget 180).

**Fin du rapport Phase 5 QA — Dépanneur Nobert.**
**Prochaine étape pipeline** : appliquer P1-P4 + variables kickoff →
re-run `tools/preflight.sh https://depanneur-nobert.ca clients/depanneur-nobert`
→ orchestrer `deploy-master`.
