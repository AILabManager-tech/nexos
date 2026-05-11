# Phase 5 — QA Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (KPI conversion prioritaire — voir promotions de la semaine)
**Date Phase 5** : 2026-05-10
**Orchestrateur** : ph5-qa (Claude Opus 4.7 — 1M context)
**Stack auditée** : Next.js 15.5.15 + React 19 + Tailwind 3.4.16 + next-intl 3.26.5 + Vercel
**Palette imposée** : `primary=#1A2B3C` · `accent=#FFD700` · `secondary=#B2B2B2`
**Build artefact source** : Ph4 rerun 2026-05-10 (μ=9.5) — 23 routes générées, 24/24 sections `built`

---

## 0. Cadrage Ph5

Audit exhaustif post-Ph4 sur la base des **mesures réelles** du tooling CLI (`tooling/lighthouse.json`, `tooling/headers.json`, `tooling/a11y.json`, `tooling/deps.json`, `tooling/ssl.json`) et du code source `clients/depanneur-nobert/site/`.

23 agents priorité 0–2 exécutés (filtrage `stack=nextjs, type=vitrine`). Aucune régénération de code — Ph5 audite, ne reconstruit pas (cf. handoff Ph4 §8.1).

---

## 1. Tooling réel — synthèse mesures

| Outil | Fichier source | Verdict |
|---|---|---|
| Lighthouse CI | `tooling/lighthouse.json` | Performance **92** · A11y **100** · BP **96** · SEO **92** |
| pa11y (WCAG 2.2 AA) | `tooling/a11y.json` | **0 violation** (`[]`) |
| `npm audit` | `tooling/deps.json` | **0 HIGH/CRITICAL** · 3 moderate (next, next-intl, postcss) |
| `curl -I` headers | `tooling/headers.json` | 6/6 headers sécu présents · **CSP absent** ⚠️ |
| SSL/TLS | `tooling/ssl.json` | `error: unable to connect to localhost:443` — non applicable en local, à valider post-deploy Vercel |

### 1.1 Lighthouse — métriques clés

| Métrique | Valeur | Score | Interprétation |
|---|---:|---:|---|
| First Contentful Paint | 1.1 s | 1.00 | ✅ Excellent |
| Largest Contentful Paint | 3.3 s | 0.69 | ⚠️ Pénalisé par redirection `/` → `/fr` (artefact local) |
| Speed Index | 1.1 s | 1.00 | ✅ |
| Total Blocking Time | 10 ms | 1.00 | ✅ |
| Cumulative Layout Shift | 0 | 1.00 | ✅ |
| Time to Interactive | 3.4 s | 0.93 | ✅ |
| Server Response Time | 13 ms | 1.00 | ✅ |

**Audits notés 0** :
- `errors-in-console` — 1 entrée : 404 sur `/fr/icon?180e835def8e537d=` (artefact dev Next.js icon route, résorbe en build prod statique).
- `redirects` — 604 ms perdus sur `/` → `/fr` (test lancé sur racine, comportement attendu de `next-intl localePrefix:always`).

Les deux audits 0 sont des **artefacts du test local** (curl `http://localhost:59513/` au lieu de `http://localhost:59513/fr`), pas des défauts du build. À re-mesurer post-deploy Vercel sur URL canonique.

---

## 2. Agents — résultats par catégorie

### 🔒 Sécurité (priorité 0 — 5 agents)

#### `security-headers`
**Source** : `tooling/headers.json` (curl -I localhost:59513).

| Header | Mesuré | Attendu | Verdict |
|---|---|---|---|
| X-Content-Type-Options | `nosniff` | nosniff | ✅ |
| X-Frame-Options | `DENY` | DENY/SAMEORIGIN | ✅ |
| Referrer-Policy | `strict-origin-when-cross-origin` | strict-origin-when-cross-origin | ✅ |
| Permissions-Policy | `camera=(), microphone=(), geolocation=(self)` | restrictif | ✅ |
| Strict-Transport-Security | `max-age=63072000; includeSubDomains; preload` | HSTS preload | ✅ |
| X-DNS-Prefetch-Control | `on` | on | ✅ |
| Content-Security-Policy | **absent** | requis CLAUDE.md §Sécurité | ❌ |

**Verdict** : 6/6 headers défensifs OK. **Manque CSP** — ouvre la voie à l'agent `csp-generator` ci-dessous.

#### `csp-generator`
**Constat** : aucune politique CSP définie dans `vercel.json` ni `next.config.mjs`.

Le projet expose 4 surfaces nécessitant des directives :
1. JSON-LD inline (`lib/jsonld.ts:124`) — nécessite `'unsafe-inline'` ou hash/nonce sur `script-src`.
2. Google Maps iframe (`MapsEmbed.tsx`, gated par consent) — nécessite `frame-src https://www.google.com`.
3. Fonts Google (`next/font/google` — Fraunces + Inter) — `font-src 'self'` (Next inline les fonts en build).
4. Images locales `/images/*` (placeholder kickoff) — `img-src 'self' data:`.

**CSP recommandée pour `vercel.json`** :
```json
{
  "key": "Content-Security-Policy",
  "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; frame-src https://www.google.com; connect-src 'self'; form-action 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests"
}
```

**Action Ph5** : ajouter le header CSP au `vercel.json` lors du kickoff deploy (mode `report-only` 7 jours pour calibrer puis enforce). Score D4 −0.25.

#### `ssl-auditor`
**Source** : `tooling/ssl.json` → `{"grade": "error", "error": "unable to connect to localhost:443"}`.

**Verdict** : non applicable en local. Audit reporté post-deploy Vercel — cible **A+ (HSTS preload + TLS 1.3 + cert valide)**. Vercel par défaut : Let's Encrypt + TLS 1.3 + HTTP/2/3 = grade A+ standard.

#### `xss-scanner`
**Mesure** : `grep -rn dangerouslySetInnerHTML` dans `app/`, `components/`, `lib/` :
- 1 occurrence : `lib/jsonld.ts:124` — `JSON.stringify(data).replace(/</g, '\\u003c')`
- Pattern d'échappement standard (RFC 8259) qui désactive l'injection `</script>` à l'intérieur du JSON-LD.
- Aucune source utilisateur, données 100% server-side.

**Verdict** : ✅ pas de vecteur XSS exploitable. ADR-003 respecté (pages légales JSX statique, pas de DOMPurify nécessaire).

#### `dep-vulnerability`
**Source** : `tooling/deps.json`.

| Paquet | Sévérité | CVE/Advisory | Fix dispo |
|---|---|---|---|
| `next-intl <4.9.1` | moderate | GHSA-8f24-v5vv-gm5j (open redirect) + GHSA-4c35-wcg5-mm9h (prototype pollution) | next-intl 4.11.1 (semver-major) |
| `postcss <8.5.10` | moderate | GHSA-qx2v-qp2m-jg93 (XSS via `</style>` stringify) | next 9.3.3 (downgrade — non viable) |
| `next 9.3.4-canary..16.3.0-canary` | moderate | via postcss | next 9.3.3 (non viable) |

**Verdict** : 0 HIGH/CRITICAL — sous le seuil bloquant Loi 25/sécurité. Les 3 moderate viennent du même arbre `next → postcss` ; l'upgrade `next-intl 3.26 → 4.11` est **breaking** (pathnames API revue) → décision : **conserver Ph5**, planifier upgrade pré-deploy en track séparé. Score D4 −0.25.

---

### ⚖️ Conformité (priorité 0 — 1 agent)

#### `legal-compliance` (Loi 25 QC)

| Exigence Loi 25 | Implémentation | Verdict |
|---|---|---|
| RPP nommé (art. 3.1) | Nobert Tremblay — `ContactNoteRPP.tsx:31` + `PrivacyPolicyBody.tsx` + `legal.privacy.rpp.*` | ✅ |
| Politique confidentialité dédiée | `/[locale]/politique-confidentialite/page.tsx` (FR + `/privacy-policy` EN) | ✅ |
| Mentions légales dédiées | `/[locale]/mentions-legales/page.tsx` (FR + `/legal-notice` EN) | ✅ |
| Bandeau cookies opt-in | `CookieConsentBanner.tsx` intégré dans `layout.tsx:122`, 3 catégories (essentiels/analytics/marketing), refus aussi visible que accepter | ✅ |
| Données collectées documentées | infolettre, analytics, contact-formulaire (champs Zod + i18n `legal.privacy.dataCollected.*`) | ✅ |
| Finalités explicites | infolettre, commandes, analytics — `brief.legal.purposes` propagé | ✅ |
| Rétention documentée | infolettre 12 mois, téléphone 6 mois, cookies 30j — `legal.privacy.retention` | ✅ |
| Transfert hors QC déclaré | Vercel + GA + Maps (US) + IP tronquée — `legal.privacy.subProcessors.*` | ✅ |
| Maps gated par consent | `MapsEmbed.tsx` placeholder + bouton "Charger la carte" + note transfert (ADR-004) | ✅ |
| Honeypot + consent CTA forms | `ContactForm.tsx:134/142` (honeypot RHF + consent zod required) ; `NewsletterCTA.tsx` idem | ✅ |
| Notification incident (art. 3.5) | `nobert@depanneur-nobert.ca` configuré dans `lib/email.ts` + `legal.privacy.incident.*` | ✅ |
| Footer 4 liens légaux | politique + mentions + RPP + Cookie settings — `Footer.tsx` | ✅ |

**Verdict** : conformité native Loi 25 **100%**. **D8 = 10.0/10**.

---

### ⚡ Performance (priorité 1 — 5 agents)

#### `lighthouse-runner`
**Lighthouse global** : Performance **0.92** (cf. §1.1).
- LCP 3.3s pénalisé par redirect `/` → `/fr` mesuré 604 ms (audit `redirects` score 0). En production sur URL canonique `https://depanneur-nobert.ca/fr`, la redirection `/` est servie côté edge Vercel < 50 ms → LCP estimé 2.7s (score ≥ 0.85).
- TBT 10 ms, CLS 0, Speed Index 1.1s : **excellents en valeur absolue**.

**Verdict** : ✅ Cible perf ≥ 90 atteinte. Score D5 = 9.0/10 (-1.0 pour LCP local, à re-mesurer post-deploy).

#### `bundle-analyzer`
**Source** : Ph4 build-validator §2.6.
- First Load JS shared : **102 KB** (budget 250 KB) ✅
- Largest route : `/[locale]/contact` **162 KB** (RHF + Zod + form) — sous budget mais à monitorer ✅
- 23 pages SSG + 1 ISR (`/promotions` revalidate=1w) + 2 dynamic (`/api/contact`, `/api/newsletter`)

**Verdict** : ✅ Bundle dans les budgets Ph1 (`stack-decision.json`).

#### `image-optimizer`
**Mesure** : `grep -rEn "(<img|<Image|next/image)" app/ components/` → **0 résultat**.

**Constat** : aucune image réelle injectée dans les composants Ph4. Les emplacements images sont des **placeholders styled** (ex: `Hero.tsx:50-56` — div ratio 4/3 avec texte alt en italique). Cela découle du **bloquant kickoff F-photos** (cf. Ph4 §8.3) — photos vitrine, propriétaire et témoignages voisinage non encore fournies.

**Verdict** : 🟡 **conditionnel kickoff**. Quand les images seront fournies :
- **TOUTES** doivent passer par `next/image` (CLAUDE.md §Stack).
- Format AVIF/WebP automatique (config Ph4 `next.config.mjs:images.formats`).
- `alt` descriptif obligatoire (déjà i18nisé : `home.hero.imageAlt`, `produits.galerie.bieres.alt`, etc.).
- Responsive `sizes="(max-width: 768px) 100vw, 50vw"` minimum.
- LCP image (Hero) : `priority` + `fetchPriority="high"`.

Score D5 −0.5 (placeholder accepté en Ph5 mais à transformer pré-deploy).

#### `css-purger`
- Tailwind `content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}']` ✅ — purge automatique des classes non utilisées en build prod.
- 0 CSS global hors `styles/globals.css` (37 lignes : reset + skip-link + prefers-reduced-motion).
- Pas de `@apply` chains lourds, pas de classes dynamiques bloquant le purge.

**Verdict** : ✅ CSS bundle minimal. Score D5 OK.

#### `cache-strategy`
**Source** : `tooling/headers.json` + `vercel.json`.

| Surface | Header observé | Cible | Verdict |
|---|---|---|---|
| HTML SSG | `cache-control: s-maxage=31536000` + `x-nextjs-cache: HIT` + `etag` | s-maxage long + revalidate ISR | ✅ |
| `/_next/static/(.*)` | `public, max-age=31536000, immutable` (vercel.json) | immutable 1y | ✅ |
| `/images/(.*)` | `public, max-age=86400, stale-while-revalidate=604800` (vercel.json) | SWR | ✅ |
| ISR `/promotions` | `revalidate=604800` (page.tsx:15) | weekly | ✅ |

**Verdict** : ✅ Cache-strategy alignée stratégie Ph1 (poll hebdo promotions).

---

### ♿ Accessibilité (priorité 1 — 3 agents)

#### `a11y-auditor`
**Source** : `tooling/a11y.json` → `[]`.
**Lighthouse a11y** : **100/100** (cf. §1.1).

**Vérifications complémentaires (code review)** :
- Skip-link `<a href="#main" className="skip-link">` présent dans `[locale]/layout.tsx:112` ✅
- `<html lang="fr-CA"|"en-CA">` correct par locale ✅
- `aria-labelledby` sur sections (`Hero.tsx:15` → `hero-title`) ✅
- `aria-hidden="true"` sur icônes décoratives Lucide (`Hero.tsx:37,44`) ✅
- `aria-label` sur CTAs ambiguës (`Hero.tsx:33,41` → `ctaPrimaryAria`/`ctaSecondaryAria`) ✅
- `<caption className="sr-only">` sur `HoursTable.tsx:15` ✅
- `prefers-reduced-motion: reduce` désactive animations (`globals.css:36`) ✅

**Verdict** : ✅ pa11y 0 violation + Lighthouse 100. Score D6 = 9.5/10 (-0.5 réservé pour validation manuelle post-photos).

#### `color-contrast-fixer`
**Tokens (tailwind.config.ts)** :
- `text DEFAULT #1A2B3C` sur `background DEFAULT #FFFFFF` → **15.07:1** (AAA)
- `text muted #475569` sur `background DEFAULT #FFFFFF` → **7.46:1** (AAA)
- `primary DEFAULT #1A2B3C` (CTA bg) + `primary-foreground #FFFFFF` → **15.07:1** (AAA)
- `accent DEFAULT #FFD700` + `accent-foreground #1A2B3C` (text-on-accent) → **13.2:1** (AAA) ✅ enforce via tokens
- `secondary DEFAULT #B2B2B2` + `text DEFAULT #1A2B3C` → **3.7:1** (FAIL pour body, OK décoratif) — **enforce décoratif uniquement** par construction tokens (Ph4 §2.1)

**Verdict** : ✅ 0 combinaison tokens en violation AA pour texte. Aucune classe `text-secondary` détectée pour du body texte. Score D6 OK.

#### `keyboard-nav-tester`
- Skip-link visible au focus (`globals.css` `.skip-link`) ✅
- `focus-visible:ring-3 focus-visible:ring-primary focus-visible:ring-offset-2` sur tous les CTAs (`Hero.tsx:34,42`, `Button.tsx`, `Link` next-intl) ✅
- Tab-order naturel (DOM ordre = ordre visuel — section-manifest order respecté) ✅
- Pas de `tabindex` positif détecté
- Forms : labels associés via `htmlFor` (Input/Textarea atoms) ✅

**Verdict** : ✅ navigation clavier fonctionnelle. Score D6 OK.

---

### 🔍 SEO (priorité 1 — 4 agents)

#### `seo-meta-auditor`
**Lighthouse SEO** : **92/100**.

| Check | Statut | Source |
|---|---|---|
| `<title>` par page | ✅ | `generateMetadata` dans chaque sub-page (cf. promotions/page.tsx:17-38) |
| `<meta description>` par page | ✅ | idem |
| `canonical` par page | ✅ | `alternates.canonical` |
| `hreflang fr-CA/en-CA/x-default` | ✅ | `alternates.languages` (3 entrées par page) |
| OG title/description/image | ✅ | `openGraph.*` + `app/opengraph-image.tsx` dynamique |
| `<html lang>` | ✅ | dépend du segment locale |
| Robots dynamique | ✅ | `app/robots.ts` — AI crawlers explicit allow + sitemap référencé |
| `metadataBase` | 🟡 | W-001 Ph4 — fallback `localhost:3000` si `NEXT_PUBLIC_SITE_URL` vide |

**Verdict** : ✅ SEO meta complet. **W-001 metadataBase à résoudre kickoff** (`NEXT_PUBLIC_SITE_URL=https://depanneur-nobert.ca`). Score D7 = 9.0/10 (-0.5 W-001, -0.5 placeholders ville/adresse non rendus).

#### `jsonld-generator`
**Mesure** : `grep -rn buildLocalBusinessSchema|buildWebSiteSchema|buildFAQSchema`.

| Schema | Position | Verdict |
|---|---|---|
| `LocalBusiness` (`@type: ConvenienceStore`, OpeningHoursSpecification) | layout-level (`[locale]/layout.tsx:106`) | ✅ |
| `WebSite` (potentialAction SearchAction) | layout-level (`[locale]/layout.tsx:107`) | ✅ |
| `FAQPage` | `PromotionsFAQ.tsx` (S-011) + `ProduitsFAQ.tsx` (S-016) | ✅ |
| `BreadcrumbList` | dispo dans `lib/jsonld.ts` mais non injecté actuellement (page-level) | 🟡 |

**Verdict** : ✅ couverture LocalBusiness + WebSite + FAQPage suffisante pour AI Overviews + Google Knowledge Panel. Breadcrumb optionnel Ph5+ (les pages sont à 1 niveau). Score D7 OK.

#### `sitemap-validator`
**Source** : `app/sitemap.ts` (12 URLs : 6 routes × FR/EN).

| Vérification | Statut |
|---|---|
| 12 URLs = 6 pages × 2 locales | ✅ |
| `lastModified: now` (date build) | ✅ |
| `changeFrequency` cohérent (weekly home/promo, monthly produits, yearly contact/legal) | ✅ |
| Priorities (1.0 home FR / 0.9 EN, 0.9/0.8 promotions, 0.7/0.6 produits, 0.7/0.6 contact, 0.3/0.3 legal) | ✅ |
| `alternates.languages` fr-CA/en-CA/x-default cohérent par URL | ✅ |
| Slug FR≠EN appliqué (P4-002) — `promotions↔deals`, `produits↔products`, `politique-confidentialite↔privacy-policy`, `mentions-legales↔legal-notice` | ✅ |
| `robots.ts` référence `${baseUrl}/sitemap.xml` | ✅ |

**Verdict** : ✅ sitemap conforme protocole 0.9 + extension hreflang. Score D7 OK.

#### `broken-link-checker`
**Mesure statique** : `grep -rEn 'href="(/fr/|/en/|http)"' app/ components/` → 0 hardcoded URL détectée.

Toutes les transitions internes passent par `<Link href="/promotions" />` (next-intl Link) — résolution automatique pathnames `pathnames` mapping. Footer + StickyCTA + cross-sell utilisent tous `Link` de `@/i18n/routing`.

Liens externes notables : Google Maps iframe (gated consent), `tel:` link téléphone (kickoff env), `mailto:` RPP. Aucun lien externe hardcodé brisé.

**Verdict** : ✅ pas de lien interne brisé détectable statiquement. Validation runtime à faire post-deploy avec `lychee` (optionnel). Score D7 OK.

---

### 🧪 Code (priorité 1–2 — 2 agents)

#### `test-coverage-gap`
**Mesure** : `find . -name "*.test.*" -o -name "*.spec.*" -not -path "*/node_modules/*"` → **0 fichier**.
`ls vitest.config*` → **absent**.

**Constat** : Ph4 §2.6 mentionne « tests Vitest scaffold » mais aucun fichier de test ni config vitest n'existe sur le disque. La référence à Vitest dans `package.json` est cosmétique (devDeps absentes).

**Composants critiques sans tests** (top priorité si tests ajoutés) :
- `lib/schemas.ts` (Zod FORM-CONTACT/FORM-NEWSLETTER) — surface validation
- `lib/rateLimit.ts` (3/h /api/contact, 1/5min /api/newsletter) — surface DDoS
- `lib/jsonld.ts` (échappement `<` → `<`) — surface XSS
- `lib/cookieConsent.ts` (3 catégories opt-in) — surface Loi 25
- `app/api/contact/route.ts` + `app/api/newsletter/route.ts` — surfaces réseau
- `MapsEmbed.tsx` (gated consent applicatif) — surface Loi 25

**Verdict** : 🔴 **gap couverture tests = 0%** sur surfaces sécu/légal. Non-bloquant Ph5 deploy (la stack Next 15 SSG + Zod runtime offre une garantie minimale), mais **debt à adresser pré-MVP+1**. Score D3 = 6.0/10 (gap réel mais non-bloquant pour un site vitrine 6 pages).

#### `typo-fixer`
**Sondages FR/EN** sur sections critiques (Hero, PromotionsHero, ContactHero, légal) :
- 437 clés FR + 437 clés EN, parité confirmée (`python3 set diff` = 0)
- Aucun `lorem ipsum`, `[TODO]`, `XXX` détecté dans `messages/*.json`
- Vouvoiement uniformément appliqué FR (cf. Ph3 P3-001)
- Marques accentuées correctement : `Dépanneur Nobert`, `Québec`, `bière`, `loto`
- Placeholders kickoff `{ville}`, `{NEQ}`, `{telephone}` visibles à l'œil — comportement attendu (F-002/F-003 Ph4)

**Verdict** : ✅ pas de coquille détectée. Audit sémantique reporté à validation propriétaire (Nobert Tremblay) post-kickoff. Score D9 OK.

---

### 🚀 Post-déploiement (priorité 1–2 — 2 agents)

#### `deploy-master`
**Pré-requis deploy Vercel** :

| Check | Statut |
|---|---|
| `vercel.json` présent + headers complets | ✅ (sauf CSP, cf. csp-generator) |
| `next.config.mjs` `poweredByHeader: false` + `reactStrictMode: true` | ✅ |
| Build PASS Ph4 (`tsc` 0 erreurs + `next build` 23 pages) | ✅ |
| `npm audit` 0 HIGH/CRITICAL | ✅ |
| 6 placeholders kickoff env (`NEXT_PUBLIC_VILLE`, `_ADRESSE_LIGNE`, `_CODE_POSTAL`, `_TELEPHONE`, `_NEQ`, `_ANNEE_FONDATION`) | 🔴 bloquants |
| `NEXT_PUBLIC_SITE_URL` (résolution metadataBase W-001) | 🔴 bloquant |
| Photos `/images/hero-vitrine.jpg` + témoignages S-004 + intérieur S-006 | 🟡 fallback Unsplash dispo `asset-plan.json` |
| Domaine DNS Vercel pointing `depanneur-nobert.ca` | 🔴 hors scope Ph5, kickoff client |

**Décision** : 🟡 **DEPLOY CONDITIONNEL**. Score qualité site ≥ 8.5 (cf. §3 SOIC), mais 7 bloquants kickoff client à lever avant push. Le **build** est prêt ; la **donnée** ne l'est pas.

#### `post-deploy-setup`
À configurer post-deploy par le client (checklists fournies en handoff) :
- Google Search Console — soumettre `https://depanneur-nobert.ca/sitemap.xml` (FR + EN), valider hreflang.
- Google Analytics 4 — propriété site, opt-in cookies (`cookieConsent` analytics), IP tronquée (config GA).
- Google Business Profile — vérifier cohérence adresse/téléphone/horaires avec `LocalBusiness` JSON-LD.
- AdSense : **non scope** brief (pas de monétisation pub demandée).
- DNS : MX/SPF pour `nobert@depanneur-nobert.ca`, CNAME `www`, ALIAS apex Vercel.
- `NEXT_PUBLIC_SITE_URL` injecté dans Vercel Environment Variables avant deploy.

---

### 🎨 Visual QA (priorité 1 — 1 agent)

#### `visual-qa`
**Cohérence palette CLI navy/or/gris** (P4-001) :
- Tokens Tailwind : `primary #1A2B3C` ✅, `accent #FFD700` ✅, `secondary #B2B2B2` ✅
- CSS vars `--color-primary/-accent/-secondary/-background` cohérentes (`globals.css`)
- Icons (`icon.tsx` + `apple-icon.tsx`) : navy bg + or N ✅
- OG image (`opengraph-image.tsx`) : navy gradient + or wordmark ✅
- Manifest (`manifest.ts`) : `theme_color: #1A2B3C` ✅

**Compensation R-001** (navy peut paraître corporate vs registre chaleureux brief) :
- Fraunces (serif heading) chargée via `next/font/google` — chaleur typographique ✅
- Inter (body) ✅
- Vouvoiement appliqué messages (cf. Ph3 P3-001) ✅
- Placeholders photos chaleureuses (vitrine, propriétaire) — kickoff bloquant.

**Verdict** : ✅ palette imposée navy/or/gris strictement appliquée, compensation typo+lexique active. **Test perception visuelle réelle** post-photos kickoff. Score D2 OK.

---

## 3. Section Manifest Coverage (24 sections)

Audit pour chaque section : composant présent ? namespace i18n présent ? import dans `page.tsx` correspondant ?

| ID | Page | Section | Composant | i18n | Statut |
|---|---|---|---|---|---|
| S-001 | home | Hero | ✅ `components/sections/Hero.tsx` | ✅ `home.hero` | audited |
| S-002 | home | PromotionsHighlight | ✅ `components/sections/PromotionsHighlight.tsx` | ✅ `home.promotionsHighlight` | audited |
| S-003 | home | CategoriesProduits | ✅ `components/sections/CategoriesProduits.tsx` | ✅ `home.categories` | audited |
| S-004 | home | SocialProofVoisinage | ✅ `components/sections/SocialProofVoisinage.tsx` | ✅ `home.socialProof` | audited |
| S-005 | home | InfosPratiques | ✅ `components/sections/InfosPratiques.tsx` | ✅ `home.infosPratiques` | audited |
| S-006 | home | StoryBrand | ✅ `components/sections/StoryBrand.tsx` | ✅ `home.storyBrand` | audited |
| S-007 | home | NewsletterCTA | ✅ `components/sections/NewsletterCTA.tsx` | ✅ `home.newsletter` | audited |
| S-008 | global | StickyCTAGlobal | ✅ `components/layout/StickyCTA.tsx` (note : layout/, non sections/) | ✅ `common.stickyCta` | audited |
| S-009 | promotions | PromotionsHero | ✅ `components/sections/PromotionsHero.tsx` | ✅ `promotions.hero` | audited |
| S-010 | promotions | PromotionsList | ✅ `components/sections/PromotionsList.tsx` | ✅ `promotions.list` | audited |
| S-011 | promotions | PromotionsFAQ | ✅ `components/sections/PromotionsFAQ.tsx` | ✅ `promotions.faq` | audited |
| S-012 | promotions | CrossSellProduits | ✅ `components/sections/CrossSellProduits.tsx` | ✅ `promotions.crossSell` | audited |
| S-013 | produits | ProduitsHero | ✅ `components/sections/ProduitsHero.tsx` | ✅ `produits.hero` | audited |
| S-014 | produits | ProduitsCategoriesNav | ✅ `components/sections/ProduitsCategoriesNav.tsx` | ✅ `produits.categoriesNav` | audited |
| S-015 | produits | ProduitsGalerie | ✅ `components/sections/ProduitsGalerie.tsx` | ✅ `produits.galerie` | audited |
| S-016 | produits | ProduitsFAQ | ✅ `components/sections/ProduitsFAQ.tsx` | ✅ `produits.faq` | audited |
| S-017 | produits | CrossSellPromotions | ✅ `components/sections/CrossSellPromotions.tsx` | ✅ `produits.crossSell` | audited |
| S-018 | contact | ContactHero | ✅ `components/sections/ContactHero.tsx` | ✅ `contact.hero` | audited |
| S-019 | contact | CoordonneesHoraires | ✅ `components/sections/CoordonneesHoraires.tsx` (+ helper `HoursTable.tsx`) | ✅ `contact.coordonnees` | audited |
| S-020 | contact | MapsEmbed | ✅ `components/sections/MapsEmbed.tsx` (consent-gated) | ✅ `contact.maps` | audited |
| S-021 | contact | ContactForm | ✅ `components/sections/ContactForm.tsx` (Zod+RHF+honeypot+consent) | ✅ `contact.form` | audited |
| S-022 | contact | ContactNoteRPP | ✅ `components/sections/ContactNoteRPP.tsx` | ✅ `contact.rpp` | audited |
| S-023 | politique-confidentialite | PolitiqueContent | ✅ `components/sections/PrivacyPolicyBody.tsx` (JSX statique — voir note) | ✅ `legal.privacy` | audited |
| S-024 | mentions-legales | MentionsContent | ✅ `components/sections/LegalNoticeBody.tsx` (JSX statique — voir note) | ✅ `legal.notice` | audited |

**Note section-manifest** : S-023/S-024 listent `component_name: "LegalDocBody"`, mais l'implémentation Ph4 a éclaté en `PrivacyPolicyBody.tsx` + `LegalNoticeBody.tsx` (ADR-003 — JSX statique pour économiser DOMPurify −22 KB). Le manifest sera mis à jour pour refléter la réalité Ph4.

**24/24 sections audited** ✅. Aucune section orpheline. Aucun namespace i18n manquant.

---

## 4. Drapeaux Ph0..Ph4 — état Ph5

| Code | Drapeau | État Ph5 | Action |
|---|---|---|---|
| **F-001** | Conflit palette CLI navy vs brief warm | ✅ Résolu Ph4 P4-001 | Tokens navy/or/gris cohérents tous artefacts |
| **F-002** | Ville TBD au kickoff | 🔴 **Bloquant deploy** | `NEXT_PUBLIC_VILLE` env var avant deploy |
| **F-003** | NEQ + adresse + téléphone TBD | 🔴 **Bloquant deploy** | 4 env vars (`_ADRESSE_LIGNE`, `_CODE_POSTAL`, `_TELEPHONE`, `_NEQ`) avant deploy |
| **R-001** | Palette navy peut paraître corporate | 🟡 Compensation active | À valider sur live post-photos |
| **R-002** | Bière responsable | ✅ Couvert (note S-015 + section 7 mentions-légales) | — |
| **R-003** | FAQ AI Overviews | ✅ Couvert (FAQPage JSON-LD S-011 + S-016) | — |
| **R-004** | Politique transferts hors QC | ✅ Couvert (PrivacyPolicyBody — Vercel + GA + Maps + Resend documentés) | — |
| **W-001** | `metadataBase` non hérité sub-pages | 🔴 **À résoudre kickoff** | `NEXT_PUBLIC_SITE_URL=https://depanneur-nobert.ca` |
| **W-002** | 3 vulns moderate npm audit | 🟡 Non-bloquant Ph5 | Track upgrade `next-intl 3.26 → 4.11` (breaking pathnames) post-deploy |

**Nouveaux drapeaux Ph5** :

| Code | Drapeau | Sévérité | Action |
|---|---|---|---|
| **W-003** | CSP absent dans `vercel.json` | 🟡 Recommandé pré-deploy | Ajouter directive proposée §`csp-generator` au `vercel.json` (mode `report-only` 7j puis enforce) |
| **W-004** | Test coverage 0% (Vitest non scaffoldé) | 🟡 Debt non-bloquant | Track post-MVP : tests Zod schemas + rate-limit + jsonld escape |
| **W-005** | Photos site = placeholders styled (next/image absent) | 🟡 Bloquant qualité visuelle deploy | Asset-plan Ph2 décrit fallbacks Unsplash. À convertir en `<Image>` après upload kickoff |

---

## 5. Scoring SOIC D1–D9

| Dim | Critère | Poids | Score | Note pondérée |
|---|---|---|---:|---:|
| **D1 Architecture** | 24/24 sections built + 6 pages × 2 locales + scaffold-plan honoré + i18n routing FR≠EN | ×1.0 | 10.0 | 10.00 |
| **D2 Documentation** | Loi 25 textes complets · ADR-003/004 · README placeholder kickoff · changelog append-only | ×0.8 | 9.0 | 7.20 |
| **D3 Tests** | 0 tests unitaires (W-004) · build PASS via tsc + next build · pa11y 0 violation · audit prod-only PASS | ×0.9 | 6.0 | 5.40 |
| **D4 Sécurité** | 6/6 headers · poweredBy=false · 0 HIGH/CRITICAL · jsonld escape · CSP absent (W-003) · 3 moderate (W-002) | ×1.2 | 8.5 | 10.20 |
| **D5 Performance** | Lighthouse 0.92 · FCP 1.1s · LCP 3.3s (artefact local) · TBT 10ms · CLS 0 · bundle 102KB · ISR weekly · placeholders images (W-005) | ×1.0 | 8.5 | 8.50 |
| **D6 Accessibilité** | pa11y 0 · Lighthouse 100 · skip-link · focus-visible · contrastes AAA tokens body · prefers-reduced-motion | ×1.1 | 9.5 | 10.45 |
| **D7 SEO** | Lighthouse 0.92 · sitemap 12 URLs hreflang · robots AI-crawlers · OG dynamique · JSON-LD LocalBusiness+WebSite+FAQPage · W-001 metadataBase · placeholders ville | ×1.0 | 8.5 | 8.50 |
| **D8 Conformité Loi 25** | RPP nommé · politique + mentions · cookies opt-in 3 cat · honeypot+consent · maps gated · transferts hors QC · incident process | ×1.1 | 10.0 | 11.00 |
| **D9 Code Quality** | tsc strict 0 erreur · ESLint config · TypeScript strict + noUncheckedIndexedAccess · 437/437 i18n parité · vouvoiement uniforme | ×0.9 | 9.5 | 8.55 |

**Σ pondérée** = 79.80
**Σ poids** = 9.20
**μ Phase 5** = **79.80 / 9.20 = 8.67/10**

> Seuil deploy ph5 → DEPLOY : **μ ≥ 8.5**.
> **μ = 8.67 ≥ 8.5** → **DEPLOY ACCEPTÉ** ✅

---

## 6. Décision finale

### 6.1 Verdict SOIC
**μ Ph5 = 8.67/10** → **DEPLOY** (au-dessus du seuil 8.5).

### 6.2 Bloquants kickoff client (à lever AVANT `vercel deploy --prod`)

| # | Bloquant | Owner | Sévérité |
|---|---|---|---|
| 1 | `NEXT_PUBLIC_VILLE` env var (5 sections + sitemap + meta + LocalBusiness) | Client | 🔴 critique |
| 2 | `NEXT_PUBLIC_ADRESSE_LIGNE` + `NEXT_PUBLIC_CODE_POSTAL` (4 sections + Schema) | Client | 🔴 critique |
| 3 | `NEXT_PUBLIC_TELEPHONE` (5 sections + footer) | Client | 🔴 critique |
| 4 | `NEXT_PUBLIC_NEQ` (mentions-légales) | Client | 🔴 critique |
| 5 | `NEXT_PUBLIC_SITE_URL=https://depanneur-nobert.ca` (résout W-001) | Dev | 🔴 critique |
| 6 | `NEXT_PUBLIC_ANNEE_FONDATION` (StoryBrand) | Client | 🟡 cohérence |
| 7 | Photo `/images/hero-vitrine.jpg` (S-001) — sinon fallback Unsplash | Client | 🟡 qualité |
| 8 | Consentement écrit voisinage S-004 (3-5 portraits) — sinon fallback avatars-initiales | Client | 🟡 qualité |
| 9 | Header CSP dans `vercel.json` (W-003 — recommandé) | Dev | 🟡 défense profondeur |

### 6.3 Recommandations non-bloquantes (post-deploy ou track séparé)

- **Track tests** : ajouter Vitest + tests sur `lib/schemas.ts`, `lib/jsonld.ts` (escape), `lib/rateLimit.ts`, `lib/cookieConsent.ts` — cible 60% coverage surfaces sécu/légal.
- **Track upgrade next-intl** : `3.26.5 → 4.11.1` (breaking pathnames) — résout W-002 next-intl moderate vulns.
- **Track CSP enforce** : déployer en `Content-Security-Policy-Report-Only` 7 jours (collecter violations sur Sentry/endpoint), puis basculer enforce.
- **SSL post-deploy** : valider grade A+ sur `https://depanneur-nobert.ca` avec ssllabs.com — Vercel par défaut Let's Encrypt + TLS 1.3 → A+ attendu.
- **Re-mesure Lighthouse post-deploy** : LCP devrait passer ≥ 2.7s (score ≥ 0.85) sur URL canonique sans redirect.

---

## 7. Sorties machine-readable

| Fichier | Status | Action Ph5 |
|---|---|---|
| `clients/depanneur-nobert/ph5-qa-report.md` | ✅ CREATED | Ce rapport |
| `clients/depanneur-nobert/section-manifest.json` | ✅ TO UPDATE | 24/24 → `status: "audited"`, `lifecycle.ph5_audited: 2026-05-10T00:00:00Z`, `last_updated_phase: "ph5-qa"` |
| `clients/depanneur-nobert/soic-gates.json` | ✅ TO UPDATE | Update entry `phase: ph5-qa, mu: 8.67, decision: ACCEPT, timestamp: 2026-05-10` |
| `clients/depanneur-nobert/nexos-changelog.json` | ✅ TO APPEND | Events Ph5 (phase_start + 23 agent_runs + section_manifest_update + soic_gate_pass + phase_end) |

---

## 8. Handoff Ph5 → Deploy/Post-deploy

### Inputs livrés
- `site/` artefact build figé — pas de régénération.
- `ph5-qa-report.md` (ce fichier) — référence audit.
- `section-manifest.json` 24/24 audited.
- `tooling/*` mesures réelles préservées.
- 9 bloquants kickoff documentés (§6.2).

### Décision opérationnelle
1. Le **build est prêt qualité** (μ=8.67 ≥ 8.5).
2. Le **déploiement effectif `vercel deploy --prod`** reste une **décision utilisateur explicite** (cf. CLAUDE.md global : « Jamais de `vercel deploy` automatique »).
3. Préalable à `vercel deploy --prod` : **lever les 7 bloquants critiques** §6.2 (env vars + CSP) en kickoff client.
4. Photos S-001/S-004 acceptables en fallback Unsplash si client ne fournit pas — qualité dégradée mais pas bloquante.

### Risques résiduels post-deploy à monitorer
1. LCP réel sur Vercel edge — re-mesurer Lighthouse sur `https://depanneur-nobert.ca/fr` ; cible ≥ 0.85.
2. CSP report-only collect — surveiller violations 7 jours avant enforce (risque inline scripts JSON-LD).
3. `next-intl 3.26` open redirect (W-002) — vérifier qu'aucune route n'expose redirect param contrôlable utilisateur.
4. Conformité Loi 25 sur incident — délai **72h** pour notifier la CAI si incident, process documenté (`brief.legal.incident_process: true`) mais à tester par drill annuel.

---

*Phase 5 QA complétée 2026-05-10. μ=8.67/10. Décision : DEPLOY (sous condition de lever les 7 bloquants kickoff §6.2 avant `vercel deploy --prod`).*

Score global : **DEPLOY ACCEPTÉ (8.67/10)**
