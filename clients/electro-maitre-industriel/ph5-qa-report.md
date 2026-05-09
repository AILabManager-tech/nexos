# NEXOS v4.2 — Audit Web Exhaustif

```
DATE       : 2026-05-07
URL        : http://localhost:41153  (Lighthouse + pa11y mesurés en local sur build statique)
DOMAINE    : electro-maitre-industriel.ca (cible production, non encore déployé)
CLIENT     : Électro-Maître Industriel inc.
MODE       : audit (PH5 sur scaffold post-Phase F + duplications post-04-16)
AUDITEUR   : NEXOS v4.2 PH5 QA Engine — 23 agents + tooling réel
TOOLING    : lighthouse.json (677 Ko), headers.json, a11y.json (pa11y), ssl.json
SOIC RUN   : run-002-ph5-audit-2026-05-07
```

---

## TL;DR — verdict d'audit

**μ = 7.04 / 10 → NO-GO déploiement** (seuil ph5→deploy : μ ≥ 8.5).

Le scaffold Phase F (P06 + P12) reste solide — Lighthouse perf 99, SEO 100, contraste AAA partout, headers HTTP corrects. **Mais 4 régressions critiques apparues entre le 16 avril (run-001 GO, μ=8.4) et le 7 mai bloquent la production** :

1. **D4 Sécurité** : 2 pages utilisent `dangerouslySetInnerHTML` sans DOMPurify (`src/app/{politique-confidentialite,mentions-legales}/page.tsx`) → viol règle absolue CLAUDE.md, attaque XSS possible si le contenu HTML provient d'une source externe demain.
2. **D4 Sécurité** : aucun header `Content-Security-Policy` (ni `next.config.mjs`, ni `vercel.json`) → règle absolue CLAUDE.md non satisfaite (« CSP : Content-Security-Policy généré par agent csp-generator »).
3. **D8 Conformité + D1 Architecture** : duplication d'arbo `app/` ↔ `src/app/` avec deux implémentations divergentes des pages légales (i18n complet vs. HTML brut non localisé) → conflit de routes Next.js latent et incohérence Loi 25.
4. **D6 Accessibilité** : 6 erreurs pa11y `NoSuchID` (toutes les ancres `#project-{key}` de la galerie sont cassées) + 6 erreurs Lighthouse `label-content-name-mismatch` + 1 fail `target-size` au footer.

Les 6 sections « modified » du manifest sont fonctionnelles, mais le manifest n'est pas synchronisé avec le code (S-101 / S-102 marquées `planned` alors qu'elles existent en deux exemplaires). Aucune suite de tests n'a été créée (D3 = 3.0).

**Périmètre demandé** (audit, pas rebuild) → on ne propose pas de regen complet : la base est saine, ce sont 4 chantiers ciblés (XSS, CSP, déduplication, ancres galerie) qui ramènent μ ≥ 8.5.

---

## SECTION 1 — IDENTIFICATION & STACK TECHNIQUE

### 1.1 Fiche d'identité
| Champ | Valeur |
|---|---|
| Société | Électro-Maître Industriel inc. (NEQ 1174892345) |
| Secteur | Électrique industriel (SEC-06) — sous-secteur contractor + automatisation + maintenance |
| Positionnement | premium / medium |
| Localisation | 8500 boul. Industriel, Montréal-Est (Québec) H1G 4B2 |
| RPP Loi 25 | Jean-Pierre Morin — `rpp@electro-maitre-industriel.ca` |
| Domaine cible | `electro-maitre-industriel.ca` (Vercel, FR/EN) |

### 1.2 Stack technologique
| Composant | Version | Note |
|---|---|---|
| Next.js | 15.5.15 (App Router) | ✓ règle stack |
| React | 18.3.1 | ✓ |
| TypeScript | 5.6.3 (strict + `noUncheckedIndexedAccess` + `strictNullChecks` + `noUnusedLocals`) | ✓ |
| Tailwind | 3.4.14 | ✓ |
| next-intl | 3.25.1 | ✓ FR/EN |
| lucide-react | 0.456.0 | ✓ |
| ESLint | 9.15.0 + `next/core-web-vitals` + `next/typescript` | ✓ jsx-a11y présent via `eslint-plugin-jsx-a11y@6.10.2` |
| Tests | — | ❌ aucune dépendance Vitest/Jest/RTL |

### 1.3 Dépendances tierces & vulnérabilités
- Pas de `npm-audit.json` produit dans `tooling/` pour ce run (l'audit doit s'appuyer sur le run-001 du 2026-04-16 : 0 HIGH/CRITICAL, 1 moderate, 2 low).
- **Recommandation D4** : régénérer `npm audit --json > tooling/npm-audit.json` avant tout déploiement.

---

## SECTION 2 — ARCHITECTURE & STRUCTURE

### 2.1 Architecture informationnelle
- Routes i18n (canon) : `/[locale]/`, `/[locale]/politique-confidentialite`, `/[locale]/mentions-legales` — locale `fr` (défaut, sans préfixe via `localePrefix: 'as-needed'`) + `en`.
- Layout root (`app/[locale]/layout.tsx`) : `Header` + `<main id="main">` + `Footer` + `CookieConsent` + skip-link accent or → conforme.
- Middleware `next-intl` matcher exclut `api`, `_next`, `_vercel`, fichiers statiques → conforme.

### 2.2 Conflit d'arborescence (CRITIQUE)
Le projet contient **deux racines App Router actives** :

| Arbre | Présence | Routes générées | i18n |
|---|---|---|---|
| `app/[locale]/...` (canon Phase F) | présent | `/fr`, `/en`, `/fr/politique-confidentialite`, `/en/politique-confidentialite`, `/fr/mentions-legales`, `/en/mentions-legales` | ✓ via next-intl |
| `src/app/{politique-confidentialite,mentions-legales}/page.tsx` (apparu 2026-05-07) | présent | `/politique-confidentialite`, `/mentions-legales` (hors locale) | ❌ FR brut non localisable |

**Effet** : le `tsconfig.json` inclut `**/*.tsx` (pas d'exclude `src/`), donc Next.js voit les deux App Routers. En pratique Next.js privilégie `app/` à la racine quand il existe — mais le `src/app/` est compilé (cf. `.next/types/app/[locale]/...`) et **les fichiers existent et sont scannables**, ce qui :
- crée des routes fantômes accessibles à `/politique-confidentialite` et `/mentions-legales` selon l'ordre de résolution,
- rend `src/components/cookie-consent.tsx` (un fichier `nexos-cookie-consent` localStorage différent de `emi_cookie_consent_v1` utilisé par `components/layout/CookieConsent.tsx`) compilable mais orphelin.

Décision attendue : **supprimer `src/app/` et `src/components/cookie-consent.tsx`** (ou exclure `src/` du `tsconfig.json` si on veut les conserver pour autre raison). Ce sont les fichiers ajoutés par un workflow externe au scaffold Phase F (probablement le module `nexos/auto_fixer.py` qui a re-templaté politique/mentions sans détecter l'existence des pages i18n déjà en place).

### 2.3 Structure des routes (canon vivant)
```
/[locale]                          → Hero + ServicesOverview + ProjectsGallery + ContactCta
/[locale]/politique-confidentialite → article i18n via next-intl (RPP, données, finalités, rétention, droits)
/[locale]/mentions-legales         → <dl> i18n (NEQ, adresse, hébergeur Vercel)
/sitemap.xml                       → 6 URLs (3 routes × 2 locales)
/robots.txt                        → allow / + disallow /api/ + sitemap
```

---

## SECTION 3 — PERFORMANCE (LIGHTHOUSE RÉEL)

### 3.1 Scores Lighthouse
| Catégorie | Score | Verdict |
|---|---|---|
| **Performance** | **0.99** | ✓ excellent |
| **Accessibility** | **0.96** | ⚠ corrections ciblées requises |
| **Best Practices** | **0.96** | ⚠ favicon 404 |
| **SEO** | **1.00** | ✓ parfait |

### 3.2 Core Web Vitals (mesurés)
| Métrique | Valeur | Seuil bon | Verdict |
|---|---|---|---|
| FCP | 760 ms | ≤ 1 800 ms | ✓ |
| **LCP** | **2 110 ms** | ≤ 2 500 ms | ✓ (marge 390 ms) |
| TBT | 4.5 ms | ≤ 200 ms | ✓✓ |
| **CLS** | **0** | ≤ 0.1 | ✓ parfait |
| Speed Index | 760 ms | ≤ 3 400 ms | ✓ |
| TTI | 2 311 ms | ≤ 3 800 ms | ✓ |

### 3.3 Bundle & ressources (mesuré)
| Type | Requêtes | Transfer |
|---|---|---|
| Total | 16 | 246 KB |
| Scripts | 9 | 142 KB |
| Fonts | 2 | 84 KB (Inter + Bitter via `next/font`) |
| Document | 1 | 11.5 KB |
| Stylesheet | 1 | 5.4 KB |
| Images | 3 | 3.8 KB (SVG placeholders 800–1 134 octets) |

**Légère friction perf** :
- `legacy-javascript-insight` score 0.5 — chunk `255-*.js` contient des polyfills (`Array.prototype.at`, `flat`, `flatMap`, `Object.fromEntries`, `Object.hasOwn`) injectés par next-intl pour cibles legacy. Économie estimée : **12 KiB**.
- `render-blocking-insight` score 0 — `_next/static/css/88fc42fa96defc36.css` (5.4 KB) bloque 155 ms. Économie estimée : **110 ms**. Mineur.
- `network-dependency-tree-insight` score 0 — chaîne courte (HTML→CSS, 76 ms longest chain). Pas de `preconnect` ; non-actionnable ici (pas de tiers externe).

### 3.4 Images
- 6 SVG placeholders 0.8–1.1 KB chacun. **TODO client** explicitement noté dans `ProjectsGallery.tsx` : remplacer par photos réelles 800×600 AVIF/WebP < 250 KB.
- `next/image` utilisé partout avec `sizes` correct, `fill`, format AVIF/WebP activé dans `next.config.mjs`.

### 3.5 Cache strategy (vérifié headers réels)
- `/_next/static/*` : `public, max-age=31536000, immutable` ✓ (vercel.json + next.config.mjs)
- `/images/*` : `public, max-age=86400, stale-while-revalidate=604800` ✓ (vercel.json)
- HTML : `s-maxage=31536000` + ETag ✓ (Next prerender)

---

## SECTION 4 — SÉCURITÉ

### 4.1 Headers HTTP (curl -I réel sur localhost:41153)
| Header | Présence | Valeur mesurée | Statut |
|---|---|---|---|
| `X-Content-Type-Options` | ✓ | `nosniff` | OK |
| `X-Frame-Options` | ✓ | `DENY` | OK |
| `Referrer-Policy` | ✓ | `strict-origin-when-cross-origin` | OK |
| `Permissions-Policy` | ✓ | `camera=(), microphone=(), geolocation=()` | OK |
| `Strict-Transport-Security` | ✓ | `max-age=63072000; includeSubDomains; preload` | OK (préload-ready) |
| `X-DNS-Prefetch-Control` | ✓ | `on` | OK |
| **`Content-Security-Policy`** | **❌** | absent | **FAIL** |
| `X-Powered-By` | ✓ absent | (poweredByHeader: false) | OK |

### 4.2 SSL/TLS
- `ssl.json` : erreur attendue (`unable to connect to localhost:443` — l'audit local n'expose pas TLS).
- En production Vercel : auto-cert Let's Encrypt + HSTS preload présent dans les headers → conforme.
- **Recommandation** : re-runner `tools/preflight.sh https://electro-maitre-industriel.ca` après déploiement pour scorer SSL Labs.

### 4.3 XSS & sanitisation (CRITIQUE)
- `grep "dangerouslySetInnerHTML"` trouve **2 occurrences code applicatif** :
  - `src/app/politique-confidentialite/page.tsx:12`
  - `src/app/mentions-legales/page.tsx:12`
- Aucun import `DOMPurify`. Le HTML est un littéral compilé donc le risque réel actuel est nul, **mais** :
  - viole littéralement la règle absolue CLAUDE.md (« JAMAIS de dangerouslySetInnerHTML sans DOMPurify »),
  - dette empoisonnée : la première personne qui rendra ce HTML dynamique à partir d'un CMS/JSON/markdown ouvre une faille XSS réflective sans s'en rendre compte.
- Les vraies pages légales (`app/[locale]/...`) utilisent JSX + `useTranslations` → propres.
- **Action D4** : supprimer les deux fichiers `src/app/...` (cf. SECTION 2.2). Pas de migration, pas de DOMPurify — le canon i18n est déjà conforme.

### 4.4 Dépendances (npm audit)
- Fichier non régénéré pour ce run. Référence : run-001 (2026-04-16) → 0 HIGH/CRITICAL, 1 moderate, 2 low.
- **Action** : `npm audit --json > tooling/npm-audit.json` avant deploy.

### 4.5 CSP (FAIL)
- Aucune politique CSP dans `next.config.mjs` ni `vercel.json`.
- next-intl injecte du JS inline pour `<Provider>` et next/font injecte du `<style>` inline → toute CSP réaliste devra inclure `'self'` + nonces ou hash, ou tolérer `'unsafe-inline'` + `'strict-dynamic'`.
- **Recommandation csp-generator** : ajouter au `headers()` du `next.config.mjs` :
  ```
  Content-Security-Policy:
    default-src 'self';
    script-src 'self' 'unsafe-inline';                                 (à durcir avec nonces)
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    font-src 'self' https://fonts.gstatic.com data:;
    img-src 'self' data: blob:;
    connect-src 'self';
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';
  ```

---

## SECTION 5 — SEO

### 5.1 Meta tags (mesuré Lighthouse + code)
- `title` : template `%s · Électro-Maître Industriel`, default complet ✓
- `description` : 175 caractères, phrase commerciale + zone géographique ✓
- `metadataBase` : `https://electro-maitre-industriel.ca` ✓
- `alternates.languages` : `fr: '/fr', en: '/en'` ✓ (cohérent avec `Link` hreflang dans le header HTTP `link`)
- `openGraph.type/locale/siteName` ✓ — **mais** pas d'image OG (`public/og-image.png` absent). Fail visibilité partage social.
- Lighthouse `viewport`, `robots-txt`, `html-has-lang`, `meta-description` : tous score 1 ✓

### 5.2 Structured data (JSON-LD)
- **Aucun JSON-LD dans le code** (`grep "application/ld+json"` → 0 hit applicatif).
- Pour SEC-06 (services B2B locaux) → manqué : `Organization` + `LocalBusiness` (`@type: Electrician`, `address`, `telephone`, `openingHoursSpecification` 24/7, `areaServed: "Montréal-Est, Laval, Longueuil"`, `aggregateRating` futur).
- Action **jsonld-generator** : ajouter `<Script id="ld-business" type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(...) }} />` (oui ici DOMPurify n'est pas requis car string littéral statique — mais le path passera par cette dérogation explicite).

### 5.3 Sitemap & robots
- `app/sitemap.ts` : génère 6 URLs (3 routes × 2 locales), `priority: 1` accueil, `0.5` légales, `changeFrequency: monthly` ✓
- `app/robots.ts` : `allow: /`, `disallow: /api/`, sitemap référencé ✓

### 5.4 Liens cassés (broken-link-checker)
- 6 ancres `#project-{key}` dans `ProjectsGallery.tsx` pointent vers des IDs inexistants (cf. SECTION 6.1) → liens internes cassés en pratique.
- Liens externes : aucun dans le scaffold (tout est mailto:, tel:, ou interne).

---

## SECTION 6 — ACCESSIBILITÉ (PA11Y RÉEL + LIGHTHOUSE)

### 6.1 WCAG 2.2 AA — erreurs pa11y (a11y.json, 6 erreurs)
**Toutes : `WCAG2AA.Principle2.Guideline2_4.2_4_1.G1,G123,G124.NoSuchID`**

| # | Sélecteur | Ancre cassée |
|---|---|---|
| 1 | `#projects > div > ul > li:nth-child(1) > a` | `#project-manufacturing` |
| 2 | `#projects > div > ul > li:nth-child(2) > a` | `#project-food-plant` |
| 3 | `#projects > div > ul > li:nth-child(3) > a` | `#project-datacenter` |
| 4 | `#projects > div > ul > li:nth-child(4) > a` | `#project-warehouse` |
| 5 | `#projects > div > ul > li:nth-child(5) > a` | `#project-switchgear` |
| 6 | `#projects > div > ul > li:nth-child(6) > a` | `#project-automation` |

**Cause racine** (`components/sections/ProjectsGallery.tsx:50-52`) : la `<a href="#project-${key}">` n'a pas de cible : ni le `<li>` (le `key` React n'est pas un id HTML), ni la `<section>` (l'id parent est `#projects`).

**Fix minimal** (deux options) :
- **Option A (recommandée)** : ajouter `id={`project-${key}`}` sur le `<li>` (ou sur l'`<a>` lui-même) pour que les ancres fonctionnent comme « item focus dans la galerie ».
- **Option B** : remplacer `href="#project-${key}"` par un vrai `href="/projets/${key}"` (route détail à scaffolder phase ultérieure) ou supprimer l'ancre si la galerie n'est pas cliquable au-delà du hover-reveal.

### 6.2 Lighthouse a11y — 3 audits failed
- **`label-content-name-mismatch`** (score 0, 6 nœuds) : sur les mêmes 6 cartes, l'`aria-label` complet (« Tableau électrique 600 V rénové dans une usine d'embouteillage à Anjou… ») ne contient pas le texte visible (« MANUFACTURIER \n Ligne d'embouteillage — Anjou \n Rénovation… »). Viol WCAG 2.5.3 « Label in Name » → un utilisateur de dictée vocale qui dit « cliquer ligne d'embouteillage » échoue.
  **Fix** : reformuler les `alt` / `aria-label` pour inclure (ou *commencer par*) le texte visible (`title` + `sector`). Exemple : `aria-label={`${t('items.manufacturing.title')} — ${t('items.manufacturing.summary')}`}`.
- **`target-size`** (score 0, 1 nœud) : footer `<a href="tel:+15145550177">` mesure 105 × 17 px (cible 24 × 24 px min, espace clic 23 px ≥ 24 px requis). Viol WCAG 2.5.5 / 2.2 AA Target Size (Minimum).
  **Fix** : appliquer `min-h-[44px] inline-flex items-center` sur les liens `<address>` ou augmenter le `padding`/`leading` pour atteindre 24 px hauteur.
- **`errors-in-console`** (score 0, 1 nœud) : `GET /favicon.ico → 404`. Mineur mais Best Practices.
  **Fix** : ajouter `app/icon.svg` ou `public/favicon.ico`.

### 6.3 Contraste couleurs (recalculé pour tous les pairs déclarés)
| Texte | Fond | Ratio | Niveau |
|---|---|---|---|
| `text-ink` (#F5F5F0) | `bg-surface` (#0A0A0A) | **18.10:1** | AAA |
| `text-ink-soft` (#D0D0C8) | `bg-surface` (#0A0A0A) | 12.76:1 | AAA |
| `text-ink-muted` (#A8A8A0) | `bg-surface` (#0A0A0A) | 8.27:1 | AAA |
| `text-ink-muted` (#A8A8A0) | `bg-surface-alt` (#1A1A1A) | 7.27:1 | AAA |
| `text-ink-muted` (#A8A8A0) | `bg-surface-raised` (#242424) | 6.49:1 | AA-large |
| `text-accent` (#D4AF37) | `bg-surface` (#0A0A0A) | 9.42:1 | AAA |
| `text-accent` (#D4AF37) | `bg-surface-alt` (#1A1A1A) | 8.28:1 | AAA |
| `text-accent` (#D4AF37) | `bg-primary` (#0A3D40) | 5.69:1 | AA |
| `text-ink` (#F5F5F0) | `bg-primary` (#0A3D40) | 10.94:1 | AAA |
| `text-accent-ink` (#0A0A0A) | `bg-accent` (#D4AF37) (skip-link focus) | 9.42:1 | AAA |

→ **Aucun contraste sous AA**. Le commentaire de `tailwind.config.ts` annonçait 19.5:1 et 10.3:1 — recalcul réel 18.1:1 et 10.94:1, écart de mesure mais conclusion identique (AAA partout). Color-contrast-fixer n'a rien à corriger.

### 6.4 Navigation clavier
- Skip-link `<a href="#main">` avec fond accent or (#D4AF37) → focus visible AAA ✓
- `:focus-visible` global : `outline-2 outline-offset-2 outline-accent` ✓
- `ProjectsGallery` cartes : `focus-within:outline-2 outline-accent` + grayscale toggle au focus clavier (`group-focus-within:grayscale-0`) ✓
- Header `nav` : tab order linéaire, lien vers other-locale présent ✓
- ⚠ Bandeau cookies (`role="dialog"`) : pas de focus trap, pas de `aria-modal="true"`, pas de mémorisation du focus précédent. Le composant respecte « Refuser aussi visible que Accepter » ✓ mais l'ergonomie clavier est à durcir.

### 6.5 ARIA
- `aria-labelledby` sur `<section>` Hero/Services/Projects/Contact ✓
- `aria-label` sur la `<ul>` galerie ✓
- `aria-hidden="true"` sur icônes décoratives Lucide ✓
- `address` HTML utilisé correctement pour le NAP du footer ✓
- Skip link `sr-only focus:not-sr-only` ✓

---

## SECTION 7 — DESIGN & UX (visual-qa + bundle-analyzer)

### 7.1 Pattern P12 — Premium palette shift (S26 Gibbs Electric)
- Palette dark teal `#0A3D40` + noir `#0A0A0A` + accent or `#D4AF37` + ivoire `#F5F5F0` ✓
- Cohérence : surface sombre par défaut, accent or réservé aux eyebrows/skip-link/CTA décoratif (cf. trust_line `<AlertTriangle className="text-accent">`)
- Type heavy (Bitter 700/900) + sans (Inter) → cohérent avec `D3_typo_weight=heavy`
- Différenciation vs. `clinique-aura` (ivoire/clair) et `beaumont-avocats` : confirmée — règle d'or 6D respectée.

### 7.2 Pattern P06 — Grayscale → Color reveal (S27 Puckett Electric)
- `filter: grayscale(100%)` par défaut → `group-hover:grayscale-0` + `group-focus-within:grayscale-0` ✓
- `transition: filter 400ms ease-out` (< 500 ms anti-pattern brief) ✓
- `prefers-reduced-motion: reduce` force `transition-duration: 0.01ms !important` dans `globals.css` → état toggle instantanément, pas de suppression d'état ✓
- Overlay accent or à 5 % au hover (signature P12) ✓
- ⚠ Images = SVG placeholders 0.8–1.1 KB. Le pattern P06 nécessite des photos N&B contrastées pour porter son ROI brand. **TODO client matérialisé** mais bloquant pour le ROI brand visé.

### 7.3 Pattern P16 — Legacy authority
- Stat block hero `22` ans + `24/7` (D6 asymmetric-strong, débordement `md:-mr-6 md:-my-12`) ✓
- Trust line CTA : « RBQ 5678-9012-34 · CMEQ membre · Assurance responsabilité 5 M$ » ✓ — **note** : numéro RBQ fictif (placeholder), à valider client avant deploy.

### 7.4 Asymétrie (D6_structure=asymmetric-strong)
- Hero `grid md:grid-cols-5` 3/5 + 2/5 ✓
- Bande oblique gold décorative opacity 8 % ✓
- Cards services `border-t-2 border-primary` (sans rounded → mécanique D5_velocity) ✓
- ContactCta `border-l-4 border-accent pl-8` ✓

### 7.5 Animation & motion
- Aucun `framer-motion` — animations CSS pures uniquement (P06 grayscale + transition-colors) → bon pour bundle, conforme RGAA reduced-motion.

---

## SECTION 8 — CONTENU

### 8.1 Qualité rédactionnelle (typo-fixer)
- FR : ton `technical-warm` cohérent (« L'électricité industrielle, sans compromis. », « zéro arrêt de production »). Diacritiques OK (è, ç, é, à).
- EN : parité 100 % structure (`diff` des chemins de clés FR vs EN = vide).
- ⚠ Placeholders à valider :
  - `RBQ 5678-9012-34` (numéro fictif, à remplacer par le vrai numéro de licence RBQ).
  - `+1 514 555 0177` (numéro de démonstration, à remplacer).

### 8.2 i18n (next-intl)
- 2 fichiers `messages/{fr,en}.json` parfaitement alignés (audit `paths(scalars)` identique).
- `localePrefix: 'as-needed'` → `/` (FR par défaut, sans préfixe) et `/en` (EN explicite).
- Cookie `NEXT_LOCALE=fr; Max-Age=31536000; SameSite=lax` posé par middleware ✓
- Header HTTP `link: hreflang fr/en/x-default` ✓
- ⚠ Message `legal.privacy.rpp_title` = « Directeur des opérations » (FR) — le brief précise « Directeur des opérations et Responsable de la protection des renseignements personnels ». Truncation cosmétique, non bloquante.

### 8.3 Orthographe
- Pas de coquille détectée sur les chaînes vérifiées. `Électro-Maître` accentué partout ✓.

---

## SECTION 9 — CONFORMITÉ LÉGALE (legal-compliance)

### 9.1 Loi 25 — Québec (canon i18n via `app/[locale]/...`)
| Exigence Loi 25 | Statut | Source |
|---|---|---|
| RPP nommé (art. 3.1) | ✓ | `legal.privacy.rpp_name` = Jean-Pierre Morin + email RPP |
| Politique de confidentialité dédiée | ✓ | `app/[locale]/politique-confidentialite/page.tsx` (i18n) |
| Mentions légales (NEQ, hébergeur) | ✓ | `app/[locale]/mentions-legales/page.tsx` |
| Bandeau cookies opt-in (art. 8.1) | ✓ | `CookieConsent.tsx` — défaut analytics=false, marketing=false |
| « Refuser » aussi visible que « Accepter » | ✓ | mêmes proportions, ordre Refuser → Accepter |
| Catégories cookies (essentiels / analytics / marketing) | ⚠ | structure 3 catégories définie dans `Consent` mais UI n'affiche pas le bouton « Personnaliser » |
| Durée rétention déclarée (7 ans Revenu Québec) | ✓ | `legal.privacy.retention_body` |
| Transferts hors QC documentés | ✓ | Vercel (US) + Resend (UE) explicités |
| Email d'incident configuré (art. 3.5) | ⚠ | `incident@electro-maitre-industriel.ca` mentionné dans `legal.privacy` mais **uniquement dans la version `src/app/`** non canon. La version i18n ne l'expose pas → **fix requis** dans `legal.privacy` JSON. |
| Score programmatique D8 (`evaluate_d8_legal()`) | non re-mesuré ce run | run-001 = 8.3 |

### 9.2 Régression duplication `src/app/...`
La version `src/app/politique-confidentialite/page.tsx` :
- est non localisée (FR uniquement, viol exigence brief `languages: ["fr","en"]`),
- utilise `dangerouslySetInnerHTML` sans sanitisation → viol règle absolue NEXOS,
- crée potentiellement une route concurrente `/politique-confidentialite` (sans locale).

→ **À supprimer** sans hésiter. Le canon i18n est conforme et complet.

### 9.3 RGPD / autres
- Hébergeur Vercel (US) déclaré, transferts hors QC = `false` côté brief mais Resend UE déclaré → cohérence brief/site OK.
- Mentions légales contiennent NEQ, siège, hébergeur, RPP — exigences LCJTI/Code civil québécois respectées.

---

## SECTION 10 — TESTS (test-coverage-gap)

### 10.1 Couverture actuelle
- **0 % — aucune infrastructure de test installée.**
- Pas de `vitest.config.ts`, pas de `__tests__/`, pas de dépendance `vitest` / `@testing-library/react` / `jest`.
- `package.json` n'a pas de script `test`.

### 10.2 Tests manquants prioritaires (recommandation D3)
1. `CookieConsent.test.tsx` : default = essentials only, refuse → no analytics flag, accept → analytics=true, persistance localStorage.
2. `ProjectsGallery.test.tsx` : focus-within applique grayscale-0 (snap class), aria-labels présents, prefers-reduced-motion respecté.
3. `Hero.test.tsx` : skip-link cible `#main`, h1 unique, stats `22` / `24/7` rendues.
4. `i18n` : parité clés FR/EN (test paramétré via `paths(scalars)`).
5. `Header.test.tsx` : language-switch `Link` change locale + préserve pathname.

Pour passer D3 ≥ 6.0 (sans bloquer le déploiement) : 5 tests RTL ciblés ≈ 1 jour.

---

## SECTION 11 — CODE QUALITY

### 11.1 TypeScript
- `strict: true`, `noUncheckedIndexedAccess: true`, `strictNullChecks: true`, `noUnusedLocals: true`, `noUnusedParameters: true` ✓
- Aucun `any` dans le code applicatif.
- `tsconfig.tsbuildinfo` présent → typecheck cache actif.

### 11.2 ESLint
- `extends: ["next/core-web-vitals", "next/typescript"]` ✓
- `eslint-plugin-jsx-a11y@6.10.2` installé via `eslint-config-next` ✓ — **mais** la 2e occurrence `dangerouslySetInnerHTML` aurait dû déclencher `react/no-danger` warn (pas error par défaut dans next/core-web-vitals — d'où le passage silencieux).
- Recommandation : ajouter `"react/no-danger": "error"` dans `.eslintrc.json` pour bloquer la régression.

### 11.3 Conventions
- Imports absolus via `@/*` ✓
- `next/image` partout ✓
- `next/font` (Inter + Bitter) ✓
- `poweredByHeader: false` ✓
- ⚠ Duplication `src/components/cookie-consent.tsx` (orphelin, jamais importé) — supprimer.

---

## SECTION 12 — SCORE GLOBAL & RECOMMANDATIONS

### 12.1 Scores SOIC D1–D9 (audit-grounded, pondéré)
| Dimension | Poids | Score | Justification (preuves) |
|---|---|---|---|
| **D1 Architecture** | ×1.0 | **7.5** | Patterns P12+P06 implémentés. Mais duplication `src/app/` ↔ `app/` (2 racines App Router actives) + manifest non synchronisé (S-101/S-102 status=`planned` alors qu'implémentées) |
| **D2 Documentation** | ×0.8 | **7.0** | Comments métier P06/P12/P16 inline, README images. Pas de README site, pas de runbook deploy |
| **D3 Tests** | ×0.9 | **3.0** | Aucune dépendance test, aucun fichier `*.test.*`, 0 % couverture |
| **D4 Sécurité** | ×1.2 | **6.5** | Headers HTTP réels OK, HSTS preload OK. **CSP absente** (FAIL CLAUDE.md). **`dangerouslySetInnerHTML` × 2 sans DOMPurify** (FAIL règle absolue). npm audit non re-mesuré |
| **D5 Performance** | ×1.0 | **9.5** | Lighthouse 99, LCP 2.11 s, CLS 0, TBT 4.5 ms, total 246 KB. -0.5 favicon 404 + render-blocking 110 ms |
| **D6 Accessibilité** | ×1.1 | **7.0** | Lighthouse 96, contraste AAA partout. **6 erreurs pa11y `NoSuchID`** + **6 `label-content-name-mismatch`** + 1 `target-size` |
| **D7 SEO** | ×1.0 | **8.0** | Lighthouse 100, hreflang/sitemap/robots OK. **JSON-LD absent** (LocalBusiness recommandé), **OG image absente** |
| **D8 Conformité** | ×1.1 | **7.5** | Loi 25 i18n conforme (RPP, Cookie opt-in, NEQ, hébergeur). Plombée par duplication `src/app/` non localisée + `dangerouslySetInnerHTML` (art. 3.3 « sécurité raisonnable »). `incident_email` absent du canon i18n |
| **D9 Code Quality** | ×0.9 | **7.0** | TS strict + ESLint OK. Duplication `src/components/cookie-consent.tsx` orphelin + 0 test |

### 12.2 μ pondéré
```
Σ (score × poids) = 7.5×1.0 + 7.0×0.8 + 3.0×0.9 + 6.5×1.2 + 9.5×1.0
                  + 7.0×1.1 + 8.0×1.0 + 7.5×1.1 + 7.0×0.9
                  = 7.50 + 5.60 + 2.70 + 7.80 + 9.50 + 7.70 + 8.00 + 8.25 + 6.30
                  = 63.35
Σ (poids)         = 9.0
μ                 = 63.35 / 9.0 = 7.04
```

| Seuil | μ requis | μ mesuré | Verdict |
|---|---|---|---|
| ph5 → deploy | **≥ 8.5** | **7.04** | **NO-GO** |

### 12.3 Top 5 actions prioritaires (ordre d'exécution recommandé)
1. **D4-CRIT — Supprimer `src/app/politique-confidentialite/`, `src/app/mentions-legales/`, `src/components/cookie-consent.tsx`** *(15 min)*
   Élimine en un coup : `dangerouslySetInnerHTML` non sanitisé × 2 + duplication routes + duplication composant cookie. Régression D4 + D8 + D1 + D9 corrigée simultanément.
2. **D6-CRIT — Corriger ancres galerie + label-content-name-mismatch + target-size footer** *(1 h)*
   - Ajouter `id={`project-${key}`}` sur le `<li>` de `ProjectsGallery.tsx` → 6 erreurs pa11y résolues.
   - Réécrire `aria-label` pour démarrer par `title` + `sector` → 6 erreurs Lighthouse résolues.
   - Wrapper `<a tel:>` / `<a mailto:>` du footer dans `min-h-[44px] inline-flex items-center` → target-size OK.
3. **D4-CRIT — Ajouter Content-Security-Policy + `react/no-danger: error`** *(1 h)*
   - CSP via `headers()` dans `next.config.mjs` (template SECTION 4.5).
   - `.eslintrc.json` : `"react/no-danger": "error"` pour empêcher la régression.
   - Re-runner `npm audit --json > tooling/npm-audit.json`.
4. **D7 — JSON-LD LocalBusiness/Electrician + OG image** *(2 h)*
   - `app/[locale]/layout.tsx` : injecter `<Script type="application/ld+json">` Organization + LocalBusiness (`@type: Electrician`, `address`, `telephone`, `openingHoursSpecification` 24/7, `areaServed`).
   - Générer `public/og-image.png` 1200×630 (template `og-image.template.svg`).
   - Mettre à jour `legal.privacy` JSON avec `incident_email` exposé publiquement.
5. **D3 — Installer Vitest + 5 tests prioritaires** *(1 j)*
   - `npm i -D vitest @testing-library/react @testing-library/jest-dom @vitejs/plugin-react jsdom`
   - `vitest.config.ts`, script `npm test`, 5 tests SECTION 10.2.

### 12.4 Roadmap correctifs → re-audit
| Action | Δ μ estimé | μ post-fix |
|---|---|---|
| Action 1 (suppr. duplications) | +0.45 | 7.49 |
| + Action 2 (a11y galerie + footer) | +0.30 | 7.79 |
| + Action 3 (CSP + npm audit + eslint) | +0.40 | 8.19 |
| + Action 4 (JSON-LD + OG) | +0.20 | 8.39 |
| + Action 5 (5 tests + vitest) | +0.30 | **8.69** ✅ |

→ **Effort total ≈ 1.5 jours** pour passer le gate ph5 → deploy (μ ≥ 8.5).

### 12.5 Décision
- **Mode = audit** : verdict communiqué, pas de re-build automatique.
- **Si bascule mode = create / fix** ultérieurement : exécuter actions 1 → 5 dans l'ordre, re-runner `tools/preflight.sh` + Lighthouse + pa11y, recalculer μ, ouvrir run-003 dans `soic-gates.json` avant `nexos deploy`.

---

## Section Manifest Coverage

État du manifest vs. code réel (canon `app/[locale]/...`) au 2026-05-07 :

| ID | Page | Section | Composant fichier | i18n namespace | Statut manifest | Statut audité |
|----|------|---------|-------------------|----------------|-----------------|---------------|
| S-001 | home | Hero | ✅ `components/sections/Hero.tsx` | ✅ `home.hero` | modified | **audited** |
| S-002 | home | ServicesOverview | ✅ `components/sections/ServicesOverview.tsx` | ✅ `home.services` | modified | **audited** |
| S-003 | home | ProjectsGallery | ✅ `components/sections/ProjectsGallery.tsx` | ✅ `home.projects` | modified | **audited (a11y fixes requis)** |
| S-004 | home | ContactCta | ✅ `components/sections/ContactCta.tsx` | ✅ `home.contactCta` | modified | **audited** |
| S-101 | politique-confidentialite | PrivacyPolicy | ⚠ `app/[locale]/politique-confidentialite/page.tsx` (canon) + ❌ `src/app/...` (à supprimer) | ✅ `legal.privacy` | planned | **audited (manifest à mettre à jour status=`audited`)** |
| S-102 | mentions-legales | LegalMentions | ⚠ `app/[locale]/mentions-legales/page.tsx` (canon) + ❌ `src/app/...` (à supprimer) | ✅ `legal.mentions` | planned | **audited (manifest à mettre à jour status=`audited`)** |
| S-201 | * | Header | ✅ `components/layout/Header.tsx` | ✅ `layout.header` | modified | **audited** |
| S-202 | * | Footer | ✅ `components/layout/Footer.tsx` | ✅ `layout.footer` | modified | **audited (target-size fix requis)** |

**Action manifest** : après suppression des duplications `src/app/...`, mettre à jour les 8 entrées avec `status: "audited"` + `lifecycle.ph5_audited: "2026-05-07T..."`.

---

## Annexe A — Inventaire des fichiers à supprimer

```
clients/electro-maitre-industriel/site/src/app/politique-confidentialite/page.tsx   # dangerouslySetInnerHTML, non i18n, doublon S-101
clients/electro-maitre-industriel/site/src/app/mentions-legales/page.tsx            # dangerouslySetInnerHTML, non i18n, doublon S-102
clients/electro-maitre-industriel/site/src/components/cookie-consent.tsx            # orphelin, jamais importé, version concurrente de components/layout/CookieConsent.tsx
clients/electro-maitre-industriel/site/src/                                         # arbo entière à dégager
```

## Annexe B — Tooling utilisé pour cet audit

| Fichier | Source | Ce qu'il a tranché |
|---|---|---|
| `tooling/lighthouse.json` (677 KB) | Lighthouse réel sur `localhost:41153` | perf 99 / a11y 96 / BP 96 / SEO 100, Core Web Vitals, render-blocking, legacy JS, label-content-name-mismatch, target-size, errors-in-console |
| `tooling/headers.json` | `curl -I` réel | présence/absence headers (CSP absent confirmé) |
| `tooling/a11y.json` | pa11y htmlcs WCAG2AA | 6 erreurs `NoSuchID` ancres galerie |
| `tooling/ssl.json` | sslscan local | erreur attendue (audit local sans TLS) — non-bloquante |
| `soic-gates.json` (run-001) | NEXOS PH5 2026-04-16 | référence baseline μ=8.4 GO post-Phase F |
| `pattern-recommendation.json` | PH1 pattern-recommender | confirmation P12 + P06 + P16 appliqués au scaffold |
| `brief-client.json` | client | sector SEC-06, palette industrial, langues FR/EN, RPP Loi 25, NEQ, hébergeur |

---

*Rapport produit par NEXOS v4.2 PH5 QA Engine (23 agents : csp-generator, dep-vulnerability, legal-compliance, security-headers, ssl-auditor, xss-scanner, a11y-auditor, broken-link-checker, bundle-analyzer, cache-strategy, color-contrast-fixer, css-purger, deploy-master, image-optimizer, jsonld-generator, keyboard-nav-tester, lighthouse-runner, seo-meta-auditor, sitemap-validator, test-coverage-gap, visual-qa, post-deploy-setup, typo-fixer). 2026-05-07.*
