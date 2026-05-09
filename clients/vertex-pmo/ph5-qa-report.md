# Vertex PMO — Phase 5 QA Report (Itération 3)

**Mode** : `audit`
**Date** : 2026-05-07
**Build audité** : `clients/vertex-pmo/site/` (Next.js 15.5.15 + next-intl 3.25)
**Tooling source** : `clients/vertex-pmo/tooling/` (Lighthouse 12, pa11y htmlcs, curl headers)

---

## TL;DR

| Décision | μ SOIC | Lighthouse perf / a11y / BP / SEO | a11y errors |
|---|---|---|---|
| **NO-GO** (boucle corrective requise) | **7.29** (< 8.5) | 0.98 / 0.92 / 0.96 / 1.00 | **18** WCAG 2 AA |

**Trois constats principaux**, par ordre de priorité d'action :

1. **D6 — Contrast `text-ink-muted` (RÉEL, bloquant)** : 18 erreurs pa11y confirmées par Lighthouse `color-contrast` (score 0). Toutes proviennent du token `--ink-muted: #64748B` (slate-500) sur surfaces sombres `#0F172A` / `#1E293B` → ratios 3.07–3.75:1, sous le seuil 4.5:1.
2. **D4/D9 — Pollution `src/` avec `dangerouslySetInnerHTML` (RÉEL, urgent)** : non listé dans le feedback SOIC mais découvert pendant l'audit. Trois fichiers `src/app/politique-confidentialite/page.tsx`, `src/app/mentions-legales/page.tsx`, `src/components/cookie-consent.tsx` injectent du HTML brut. Code mort (Next utilise `app/` top-level), mais viole la règle absolue NEXOS « JAMAIS de `dangerouslySetInnerHTML` sans DOMPurify » et déclenchera tout audit ESLint/SAST.
3. **D7 — FAIL SOIC `seo-meta` est un FAUX POSITIF** : le checker prétend « No layout.tsx » mais le fichier existe à `app/[locale]/layout.tsx` avec metadata complet (title template, description, OG, alternates FR/EN, metadataBase). `app/sitemap.ts` et `app/robots.ts` existent aussi. La FAIL SOIC vient probablement d'un scanner qui cherche `app/layout.tsx` à la racine sans descendre dans `[locale]/`. **À corriger côté agent SOIC, pas côté site.**

---

## 1 — Constats vs feedback SOIC Itération 3

### [D6/W-10] pa11y-a11y — VALIDÉ (HAUTE)

**Preuves** (`tooling/a11y.json`, 18 entrées, toutes `WCAG2AA.Principle1.Guideline1_4.1_4_3.G18.Fail`) :

| # | Selector | Ratio constaté | Seuil | Section |
|---|---|---|---|---|
| 1 | `#top > div:nth-child(2) > p:nth-child(5)` (« Déjà utilisé par 120 PME… ») | 3.75:1 | 4.5:1 | Hero trust line |
| 2-3 | `#demo > div:nth-child(1) > p:nth-child(2)` + KPI labels | 3.07:1 | 4.5:1 | InteractiveDemo descriptif |
| 4-12 | `#demo > div:nth-child(2)` colonnes Kanban (À planifier / En cours / Livré + tags `NRN`/`CNC`/`SSR`/`FDV`/`BH`/`CPL`) | 3.07–3.75:1 | 4.5:1 | InteractiveDemo cards |
| 13-15 | `#demo > div:nth-child(3)` KPI captions (Marge moyenne, Heures récupérées, sous-textes) | 3.07:1 | 4.5:1 | InteractiveDemo KPIs |
| 16 | `#cta > div:nth-child(2) > p:nth-child(5)` (« Essai gratuit 14 jours… ») | 3.07:1 | 4.5:1 | CTA trust line |
| 17-18 | Footer (`hours` + copyright) | 3.07:1 | 4.5:1 | Footer |

**Cause racine unique** : token `--ink-muted: #64748B` (slate-500). Cf. `tailwind.config.ts` + `app/globals.css`.

**Diagnostic** : le design « cold SaaS dark » du brief impose une hiérarchie visuelle entre `ink` (titre), `ink-soft` (corps) et `ink-muted` (légendes). La recommandation pa11y `#feffff`/`#fefeff` casserait cette hiérarchie. Le bon correctif est de relever `--ink-muted` à **`#94A3B8`** (slate-400) → ratio ≈ 5.0:1 sur `#0F172A` et 4.7:1 sur `#1E293B`. Préserve la sensation « muted » sans franchir le seuil AA.

**Action** : modifier `tailwind.config.ts` (token `ink.muted`) et/ou `app/globals.css`. Re-run pa11y attendu : 0 erreur.

### [D2/W-02] documentation — VALIDÉ (NORMALE)

**Preuve** : `ls clients/vertex-pmo/site/README.md` → fichier absent. Lighthouse n'évalue pas la doc, mais SOIC D2 le requiert (200+ chars).

**Action** : créer `site/README.md` (stack, scripts npm, structure, notes Loi 25). Pas de JSDoc requis sur les composants si commentaires-ancres existent (le code en a déjà : Hero `// Structure StoryBrand P19…`, layout `// 2 familles Google Fonts seulement…`).

### [D7/W-13] seo-meta — FAUX POSITIF (NORMALE → fermable)

**Preuves contraires** :

- `app/[locale]/layout.tsx:30-48` exporte un `metadata` Next 15 complet :
  - `metadataBase: new URL('https://vertex-pmo.com')`
  - `title.default` + `title.template`
  - `description`
  - `alternates.languages = { fr: '/fr', en: '/en' }`
  - `openGraph: { type, locale: 'fr_CA', siteName }`
- `app/sitemap.ts:1-18` génère 6 URLs (FR + EN × 3 routes).
- `app/robots.ts:1-12` configure `userAgent *` + sitemap.
- Lighthouse SEO score : **1.00** (100/100) — preuve indépendante que les balises sont correctement émises.
- Headers HTTP `link: <…>; rel="alternate"; hreflang="fr"…` confirmés dans `tooling/headers.json`.

**Hypothèse de bug SOIC** : l'agent `seo-meta-auditor` cherche `app/layout.tsx` à la racine, sans gérer le pattern `[locale]/layout.tsx` propre à next-intl. Le message « No layout.tsx » répété 3 fois pour 3 critères distincts (title / description / openGraph) confirme un scan de fichier qui retourne `null`, pas une analyse du contenu.

**Action recommandée** : corriger le sélecteur de l'agent SOIC pour reconnaître `app/[locale]/layout.tsx` ou `app/(*)/layout.tsx`. **Aucune action sur le site.** Si la pression est de débloquer le gate sans toucher l'agent : ajouter un `app/layout.tsx` minimal qui ne fait que `return children` (Next 15 l'accepte avec un `[locale]` segment) — solution de contournement, pas de fond.

---

## 2 — Constats additionnels (non listés par SOIC mais réels)

### 🔴 D4/D9 — `src/` pollution + `dangerouslySetInnerHTML`

**Fichiers concernés** (untracked d'après `git status`) :

```
clients/vertex-pmo/site/src/app/politique-confidentialite/page.tsx   (123 lignes, dangerouslySetInnerHTML)
clients/vertex-pmo/site/src/app/mentions-legales/page.tsx            (dangerouslySetInnerHTML)
clients/vertex-pmo/site/src/components/cookie-consent.tsx            (kebab-case duplicat de CookieConsent.tsx)
```

**Statut runtime** : code mort. Next 15 utilise `app/` top-level (pas de `srcDir` configuré). `tsconfig.json` `paths: { "@/*": ["./*"] }` ne pointe pas dans `src/`. Les routes actives sont `app/[locale]/...`.

**Pourquoi c'est grave malgré le code mort** :
1. Violation explicite de la règle absolue NEXOS (`CLAUDE.md` § Sécurité) : « JAMAIS de `dangerouslySetInnerHTML` sans DOMPurify ». Aucune sanitisation ici.
2. `tsconfig.json` `include: ["**/*.tsx"]` → tsc et `next lint` parcourent ces fichiers. Une règle ESLint `react/no-danger` (eslint-plugin-react v7+) les ferait échouer.
3. Pollue la lecture du dépôt et trompera tout audit SAST (osiris-scan, npm audit, etc.).
4. Provient probablement de l'auto-fixer D8 qui a généré une 2e copie au lieu de réutiliser les pages canoniques `app/[locale]/{politique-confidentialite,mentions-legales}/page.tsx`. **Bug à reporter dans `nexos/auto_fixer.py`**.

**Action** : `rm -rf clients/vertex-pmo/site/src/` (supprimer le répertoire entier). Les pages canoniques sont déjà dans `app/[locale]/` et utilisent `useTranslations` proprement (pas de HTML brut).

### 🟡 D9 — Sections orphelines (autre client)

`components/sections/MenuGallery.tsx`, `Reservation.tsx`, `ChefStory.tsx` — vestiges d'un template restauration (probablement Table de Marguerite). Non importés par `app/[locale]/page.tsx` (qui ne référence que Hero / ProblemSolution / HowItWorks / CTA). Non listés dans `section-manifest.json`.

**Action** : supprimer ces 3 fichiers. Pas d'impact runtime ni bundle (tree-shaking), mais signal de scaffold paresseux.

### 🟡 D5 — Console error : favicon 404

**Preuve** (`lighthouse.json` audit `errors-in-console`) :

```
http://localhost:59547/favicon.ico → 404 Not Found
```

`public/` ne contient que `images/`. Aucun `favicon.ico` ni `app/icon.{png,svg}`. C'est l'unique cause du score `errors-in-console: 0` qui fait tomber Best-Practices à 0.96 au lieu de 1.0.

**Action** : ajouter `app/icon.svg` (Vertex.PMO mark) + `app/apple-icon.png`. Next 15 les sert automatiquement.

### 🟡 D6 — Touch target Footer

**Preuve** (`lighthouse.json` audit `target-size: 0`) :

```
Footer <a href="tel:+15145550189">  → 106.6×17 px (besoin 24×24)
Footer <a href="mailto:hello@…"> → 154.4×17 px (besoin 24×24)
Espace inter-cibles : 23 px (besoin ≥ 24 px)
```

Cause : classe `text-xs` sur `<address>` + lignes simples séparées par `<br />`. Ergonomie tactile mobile.

**Action** : passer le bloc address à `text-sm` (16 px → ~24 px de hauteur de ligne) ou ajouter `inline-block py-1` sur les `<a>` pour atteindre 24 px de hauteur cible. Pas un bloqueur a11y au sens WCAG 2.2 AA strict (Target Size 2.5.8 est AAA), mais Lighthouse l'évalue.

### 🟢 D5 — Render-blocking CSS (mineur)

`/_next/static/css/121c703814f0968b.css` (6.2 KB) → 154 ms savings estimés. Trop petit pour justifier une optimisation. Lighthouse perf 0.98 le tolère.

---

## 3 — Tooling réel (mesures, pas estimations)

### Lighthouse 12 (mobile, throttled)

| Catégorie | Score |
|---|---|
| Performance | 0.98 |
| Accessibility | 0.92 |
| Best Practices | 0.96 |
| SEO | 1.00 |

**Audits FAIL ou partiels** :

| Audit | Score | Note |
|---|---|---|
| `errors-in-console` | 0 | favicon 404 (cf. § 2) |
| `color-contrast` | 0 | 18 violations (cf. § 1) |
| `target-size` | 0 | Footer tel/mailto (cf. § 2) |
| `render-blocking-insight` | 0 | 154 ms savings, 6.2 KB CSS |
| `legacy-javascript-insight` | 0.5 | 12 KiB JS legacy |
| `largest-contentful-paint` | 0.93 | LCP = 2.3 s (objectif < 2.5 s : OK) |
| `interactive` | 0.99 | TTI = 2.3 s |

### Headers HTTP (`tooling/headers.json`, curl localhost:59547)

| Header | Valeur | Verdict |
|---|---|---|
| `X-Content-Type-Options` | `nosniff` | ✅ |
| `X-Frame-Options` | `DENY` | ✅ |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | ✅ |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | ✅ |
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` | ✅ |
| `link` (hreflang FR/EN/x-default) | présent | ✅ |
| `Content-Security-Policy` | ABSENT | ⚠ recommandé (l'orchestrateur mentionne un agent `csp-generator` à activer) |
| `set-cookie` (`NEXT_LOCALE`) | `SameSite=Lax`, sans `Secure` | ⚠ acceptable en localhost, à vérifier en prod (Vercel injecte `Secure` automatiquement sur HTTPS) |

### SSL (`tooling/ssl.json`)

```
{ "grade": "error", "error": "unable to connect to localhost:443" }
```

**Faux signal** : test exécuté contre `localhost` qui n'écoute pas en TLS. Non bloquant — Vercel gère TLS en production. À ne pas comptabiliser dans D4.

### npm audit

**Absent** dans `tooling/`. À régénérer (`npm audit --json > tooling/npm-audit.json`) avant tout déploiement. Hypothèse : 0 vulnérabilité H/C (deps minimales : next 15.5.15, react 18.3.1, next-intl 3.25.1, lucide-react 0.456).

---

## 4 — Section Manifest Coverage

| ID | Page | Section | Composant | i18n | page.tsx import | Statut |
|----|------|---------|-----------|------|-----------------|--------|
| S-001 | home | Hero | ✅ `components/sections/Hero.tsx` | ✅ `home.hero` | ✅ | audited |
| S-002 | home | InteractiveDemo | ✅ `components/sections/InteractiveDemo.tsx` | ✅ `home.demo` | ✅ (in-Hero) | audited |
| S-003 | home | ProblemSolution | ✅ `components/sections/ProblemSolution.tsx` | ✅ `home.problem` | ✅ | audited |
| S-004 | home | HowItWorks | ✅ `components/sections/HowItWorks.tsx` | ✅ `home.howItWorks` | ✅ | audited |
| S-005 | home | CTA | ✅ `components/sections/CTA.tsx` | ✅ `home.cta` | ✅ | audited |
| S-101 | politique-confidentialite | PrivacyPolicyPage | ✅ `app/[locale]/politique-confidentialite/page.tsx` | ✅ `legal.privacy` | ✅ | audited |
| S-102 | mentions-legales | LegalMentionsPage | ✅ `app/[locale]/mentions-legales/page.tsx` | ✅ `legal.mentions` | ✅ | audited |
| S-201 | * | Header | ✅ `components/layout/Header.tsx` | ✅ `layout.header` | ✅ (in layout.tsx) | audited |
| S-202 | * | Footer | ✅ `components/layout/Footer.tsx` | ✅ `layout.footer` | ✅ (in layout.tsx) | audited |

**Couverture : 9/9 (100 %)**. Toutes les sections déclarées sont câblées. Aucun écart manifest ↔ code source.

---

## 5 — Loi 25 / D8 (zéro compromis NEXOS)

| Exigence | État | Preuve |
|---|---|---|
| RPP nommé (nom + titre + courriel) | ✅ | brief : « Marie Chen, Chef de la sécurité et RPP, rpp@vertex-pmo.com » + S-101 |
| Politique de confidentialité dédiée | ✅ | `app/[locale]/politique-confidentialite/page.tsx` (FR/EN via i18n) |
| Mentions légales dédiées (NEQ, adresse, hébergeur) | ✅ | NEQ 1179042311, 1470 Peel Mtl, Vercel + AWS ca-central-1 |
| Bandeau cookies opt-in (Refuser aussi visible que Accepter) | ✅ | `components/layout/CookieConsent.tsx` (Refuser et Tout accepter) |
| Catégories cookies (Essentiels / Analytics / Marketing) | ✅ | i18n `cookies.{categories,essentials,analytics,marketing}` |
| Transferts hors QC documentés | ✅ | brief.legal.transfer_countries + politique § 9 |
| Courriel d'incident configuré | ✅ | `incident@vertex-pmo.com` |
| Données collectées + finalités + rétention | ✅ | brief.legal exhaustif (rétention 90 j post-résiliation, logs 12 mois) |

**Verdict D8** : conforme. **Score 9.0/10** (–1.0 pour absence de page « Gérer mes témoins » accessible à tout moment depuis le footer — le bandeau apparaît seulement à la première visite et ne se rouvre pas via lien permanent).

---

## 6 — Scoring SOIC D1–D9

| Dim | Pondération | Score | Détail |
|---|---|---|---|
| D1 Architecture | ×1.0 | **8.0** | App Router propre + 9 sections câblées + i18n FR/EN. Pénalité : pollution `src/` et orphelines `MenuGallery/Reservation/ChefStory`. |
| D2 Documentation | ×0.8 | **5.0** | Pas de README. Code commenté correctement (StoryBrand annotations). |
| D3 Tests | ×0.9 | **3.0** | Aucun test. Pas de Vitest configuré dans `package.json`. Acceptable pour scaffold mais SOIC pénalise. |
| D4 Sécurité | ×1.2 | **7.5** | Headers ✅, `poweredByHeader: false` ✅, pas de clé API client. **–2.5** pour `dangerouslySetInnerHTML` dans `src/` (code mort mais viole la règle absolue). CSP absent (–0.5 marginal). npm audit non régénéré. |
| D5 Performance | ×1.0 | **9.5** | Lighthouse 0.98, LCP 2.3 s, TTI 2.3 s. Render-blocking 154 ms négligeable. |
| D6 Accessibilité | ×1.1 | **6.5** | Lighthouse 0.92. **18 erreurs contraste** (token muted) + target-size footer. Skip-link, aria-labels, role='img' sur InteractiveDemo : OK. |
| D7 SEO | ×1.0 | **9.5** | Lighthouse 1.00. Layout / sitemap / robots / hreflang tous présents et corrects. La FAIL SOIC est un faux positif. |
| D8 Conformité | ×1.1 | **9.0** | Loi 25 OK sur tous les axes critiques. –1.0 pour pas de gestion témoins permanente accessible post-consentement. |
| D9 Code Quality | ×0.9 | **6.5** | TS strict + `noUncheckedIndexedAccess` + `noUnusedLocals`. Pénalisé par 3 sections orphelines + duplicat `src/` non nettoyés. |

**μ pondéré** = (8.0×1.0 + 5.0×0.8 + 3.0×0.9 + 7.5×1.2 + 9.5×1.0 + 6.5×1.1 + 9.5×1.0 + 9.0×1.1 + 6.5×0.9) / 9.0
= (8.0 + 4.0 + 2.7 + 9.0 + 9.5 + 7.15 + 9.5 + 9.9 + 5.85) / 9.0
= **65.6 / 9.0 ≈ 7.29**

**Seuil ph5 → deploy : μ ≥ 8.5 → ❌ NO-GO** (déficit ≈ 1.21 pts).

---

## 7 — Plan de remédiation (ordre d'exécution)

Priorisé par ratio impact/effort. Estimations chaque ligne ≤ 30 min sauf indication.

| # | Action | Dim impactées | Δμ estimé |
|---|---|---|---|
| 1 | `rm -rf clients/vertex-pmo/site/src/` (supprimer scaffolding mort + `dangerouslySetInnerHTML`) | D4 +1.5, D9 +1.0 | +0.30 |
| 2 | Supprimer `MenuGallery.tsx`, `Reservation.tsx`, `ChefStory.tsx` (sections orphelines restaurant) | D9 +1.0, D1 +0.5 | +0.15 |
| 3 | Recalibrer `--ink-muted: #94A3B8` dans `tailwind.config.ts` (et vérifier sur `surface-alt`) → cible 0 erreur pa11y | D6 +2.5 | +0.31 |
| 4 | Créer `site/README.md` (200+ chars : stack, scripts, routes, notes Loi 25) | D2 +3.0 | +0.27 |
| 5 | Ajouter `app/icon.svg` Vertex.PMO (résout favicon 404 → `errors-in-console`) | D5 +0.3, D4 +0.2 | +0.06 |
| 6 | Footer : passer address en `text-sm` + `inline-block py-1` sur tel/mailto (target-size) | D6 +0.5 | +0.06 |
| 7 | Régénérer `tooling/npm-audit.json` (vérification avant push) | D4 +0.5 | +0.07 |
| 8 | (Optionnel) Ajouter CSP via meta ou `next.config.headers` | D4 +0.5 | +0.07 |
| 9 | (Optionnel) Lien permanent « Gérer mes témoins » dans footer + handler qui rouvre `CookieConsent` | D8 +1.0 | +0.12 |
| 10 | (Côté agent SOIC, pas le site) Patcher `seo-meta-auditor` pour reconnaître `app/[locale]/layout.tsx` | — | reclassement FAIL → PASS |

**μ projeté après #1–#7** : 7.29 + 1.22 ≈ **8.51** → **GATE OK (juste)**.
**μ projeté après #1–#9** : ≈ **8.70** → marge confortable.

---

## 8 — Décision

**❌ NO-GO déploiement Vercel.** Boucle corrective Itération 4 requise avec actions #1–#7 minimum.

L'audit confirme 2 des 3 corrections SOIC (D6 contraste, D2 README) et **rejette** la 3e (D7 seo-meta = bug du checker). Surtout, l'audit identifie **2 risques additionnels non listés par SOIC** : pollution `src/` avec `dangerouslySetInnerHTML` (rouge sécurité) et 3 sections orphelines d'un autre client. Sans action #1, le déploiement enverrait du code violant explicitement la règle absolue NEXOS, même si dormant.

**Handoff** :
- Itération 4 doit traiter actions #1–#7 dans l'ordre.
- Re-run pa11y + lighthouse + curl headers + `npm audit --json` avant nouvelle évaluation SOIC.
- L'équipe agents SOIC doit corriger `seo-meta-auditor` (action #10) pour éviter la même FAIL faux-positif sur les prochains clients next-intl.
