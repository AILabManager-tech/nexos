# Rapport QA — Dépanneur Nobert — 2026-05-15

## 1. Résumé Exécutif

- Mode NEXOS : **audit** (post-build itération 2 SOIC warm)
- Score SOIC μ : **8.39 / 10**
- Verdict : **FAIL — boucle corrective requise** (seuil deploy ph5→deploy : μ ≥ 8.5)
- Pages auditées : **12 routes SSG** (6 pages × 2 locales) + 2 routes API
- Sections auditées : **24 / 24** (toutes `audited` au manifest)
- Agents exécutés : **23 / 23**
- Tooling réel lu : `lighthouse.json`, `headers.json`, `deps.json`, `a11y.json`, `ssl.json`, `osiris.json`
- Décision `deploy-master` : **NO DEPLOY** (aucun `vercel deploy` exécuté, conformément aux hard-stops du projet)

**Progrès depuis la Ph5 précédente (2026-05-14)** :
- ✅ **pa11y `a11y.json = []`** : les 34 erreurs WCAG 2.2 AA 1.4.3 contraste sont **résolues** (commit `ecbfa0f` — token `text.muted` `#8B7355 → #7A6447`, ratio passé de 4.49:1 à ≥ 5.0:1 sur fond crème/blanc/muted).
- ✅ **Lighthouse Accessibility = 100/100** (était 92), Performance reste **92/100**, Best Practices **96/100**, SEO **92/100**.
- ✅ **Vitest installé** + suite minimale 13 tests / 3 fichiers (`cn`, `cookieConsent`, `rateLimit`) — D3 sort de l'absence totale.
- ⚠️ **Vitest introduit 4 moderate dev-only** dans `npm audit` (vitest/esbuild/vite/@vitest/mocker), portant le total à **8 moderate** (vs. 3 avant). Aucune HIGH/CRITICAL (0/0).

**Blocages persistants** :
- ❌ **CSP toujours absente** des `headers.json`/`next.config.mjs`/`vercel.json`/`middleware.ts` — non conforme `CLAUDE.md > Sécurité` (« CSP générée par agent csp-generator »).
- ❌ **Tests P0 manquants** : routes API contact/newsletter, schemas Zod, formulaires, MapsEmbed consent applicatif, JSON-LD. La suite actuelle ne couvre que des utilitaires.
- ⚠️ **Lighthouse 4 audits FAIL** : `errors-in-console` (404 sur `/fr/icon?…`), `canonical` (W-001 metadataBase fallback localhost), `label-content-name-mismatch` (LanguageSwitcher), `redirects` (605 ms `/` → `/fr`).
- ⚠️ **Tooling SSL/Osiris invalides** : `ssl.json` cible `localhost:443` (refus connexion), `osiris.json` échec CLI `--format` non reconnu — non bloquant audit local, à refaire post-deploy.

Le site reste **solide en architecture, Loi 25, build et perf brute**. Les deux pénalités structurantes (CSP, tests P0) tirent μ sous le seuil 8.5. Effort de levée estimé : **2-3 h** (CSP via vercel.json + 5-7 tests P0 Vitest).

## 2. Tableau de Scores par Dimension

| Dim | Nom | Score | Poids | Pondéré | Statut |
|-----|-----|------:|------:|--------:|--------|
| D1 | Architecture | 9.50 | ×1.0 | 9.50 | PASS |
| D2 | Documentation | 8.00 | ×0.8 | 6.40 | PASS réserve |
| D3 | Tests | 6.00 | ×0.9 | 5.40 | FAIL réserve |
| D4 | Sécurité | 7.50 | ×1.2 | 9.00 | FAIL bloquant (CSP) |
| D5 | Performance | 8.70 | ×1.0 | 8.70 | PASS réserve |
| D6 | Accessibilité | 9.50 | ×1.1 | 10.45 | PASS |
| D7 | SEO | 8.50 | ×1.0 | 8.50 | PASS réserve |
| D8 | Conformité Loi 25 | 9.00 | ×1.1 | 9.90 | PASS |
| D9 | Code Quality | 8.50 | ×0.9 | 7.65 | PASS |
| **μ** | **Score Final** | | | **8.39** | **FAIL** |

Calcul : Σ pondéré 75.50 / Σ poids 9.0 = **8.39**.

## 3. Performance (D5)

**lighthouse-runner** — Lighthouse réel sur `http://localhost:55191/` (redirige vers `/fr`).

| Métrique | Valeur | Score | Statut |
|---|---:|---:|---|
| Performance globale | — | **92 / 100** | PASS |
| First Contentful Paint | 1.1 s | 1.0 | PASS |
| Largest Contentful Paint | **3.3 s** | 0.69 | **WARN** (cible ≤ 2.5 s mobile, 4.0 s desktop) |
| Speed Index | 1.1 s | 1.0 | PASS |
| Total Blocking Time | 10 ms | 1.0 | PASS |
| Cumulative Layout Shift | 0 | 1.0 | PASS |
| Time to Interactive | 3.4 s | 0.93 | PASS |

**Causes LCP dégradée** (insights Lighthouse) :
- `redirects` : 605 ms gaspillés sur `/` → `/fr` (middleware next-intl `localePrefix: always` — par design).
- `render-blocking-insight` : 154 ms sur `/_next/static/css/e122078f7401b51c.css` (6.4 KB).
- `network-dependency-tree-insight` + `document-latency-insight` : 50 ms latence document initial.
- `legacy-javascript-insight` : score 0.5 (polyfills Next.js par défaut, non actionnable sans config babel custom).

**bundle-analyzer** — First Load JS partagé : **102 KB**. Route la plus lourde : `/[locale]/contact` à 162 KB (RHF + Zod + ContactForm). Sous le budget 250 KB. À surveiller si ajout de chatbot / AdSense.

**image-optimizer** — Aucune image lourde détectée dans `site/public/`. `next/image` n'est pas utilisé (placeholders kickoff). Les assets sont des metadata routes (`icon`, `apple-icon`, `opengraph-image`) — toutes maintenant warm (P4i2-002).
- ⚠️ **404 sur `/fr/icon?f714aff41800f420=`** détecté par Lighthouse (`errors-in-console`). À investiguer : probablement query string non gérée par la route `icon.tsx` quand consommée depuis le rendu locale-prefixé.

**css-purger** — Lighthouse `unused-css-rules` rapporte 0 ms / 0 byte d'économie. Tailwind purge actif via JIT. **PASS**.

**cache-strategy** — Headers réels conformes :
- Page prérendue : `cache-control: s-maxage=31536000`, `x-nextjs-cache: HIT`, `etag` présent, `x-nextjs-prerender: 1`.
- Configuration `vercel.json` injecte cache immutable sur `/_next/static/*` et `/images/*`.
**PASS**.

**osiris-runner** — **FAIL outil** (non bloquant). `osiris.json` : `osiris scan failed after 3 attempts — exit 2: No such option: --format`. L'outil CLI a évolué et le wrapper preflight n'est plus aligné. Sobriété web non mesurée — à corriger côté tooling NEXOS, pas côté site.

## 4. Sécurité (D4)

**security-headers** — `headers.json` (curl -I réel) confirme 6/7 headers attendus.

| Header | Valeur réelle | Statut |
|---|---|---|
| Strict-Transport-Security | `max-age=63072000; includeSubDomains; preload` | PASS |
| X-Content-Type-Options | `nosniff` | PASS |
| X-Frame-Options | `DENY` | PASS |
| Referrer-Policy | `strict-origin-when-cross-origin` | PASS |
| Permissions-Policy | `camera=(), microphone=(), geolocation=(self)` | PASS |
| X-DNS-Prefetch-Control | `on` | PASS |
| **Content-Security-Policy** | **absent** | **FAIL** |

**csp-generator** — **FAIL bloquant**. Aucune CSP dans `headers.json`, `next.config.mjs`, `vercel.json` ou `middleware.ts`. CSP minimale recommandée :

```text
default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self';
connect-src 'self';
frame-src https://www.google.com https://maps.google.com;
object-src 'none';
base-uri 'self';
form-action 'self';
frame-ancestors 'none';
upgrade-insecure-requests;
```

Notes d'application :
- `frame-src` couvre l'iframe Google Maps (ADR-004 — gated par consent applicatif).
- `style-src 'unsafe-inline'` requis tant que Next.js inline le critical CSS / styles inline composants Tailwind. Retirer dès passage à nonce-based.
- Aucun script tiers actuellement (pas de GA, AdSense, chatbot) — `connect-src 'self'` suffit.
- Déployer en `Content-Security-Policy-Report-Only` au premier passage pour valider sans casser Maps consent.

**ssl-auditor** — **mesure invalide**. `ssl.json` indique `unable to connect to localhost:443`. À refaire sur `https://depanneur-nobert.ca` post-DNS Vercel.

**xss-scanner** — **PASS réserve**.
- Une seule occurrence `dangerouslySetInnerHTML` : `site/lib/jsonld.ts:124` — limitée au JSON-LD avec échappement `<` → `<` (ADR-003).
- Pages légales (`PrivacyPolicyBody.tsx`, `LegalNoticeBody.tsx`) en JSX statique — pas de `innerHTML`, pas de DOMPurify requis.
- Aucun composant ne ré-injecte du contenu utilisateur sans encodage (formulaires : Zod + sanitisation côté API uniquement).

**dep-vulnerability** — `deps.json` (npm audit réel) :

| Sévérité | Count | Direct vs Transitif |
|---|---:|---|
| critical | **0** | — |
| high | **0** | — |
| moderate | 8 | 4 direct, 4 transitif |
| low | 0 | — |
| info | 0 | — |

| Package | Sévérité | Source | Action |
|---|---|---|---|
| `next` (15.5.18) | moderate | via `postcss` transitif | surveiller — bump patch déjà effectué (GHSA-8h8q-6873-q5fj HIGH résolu en Ph4 P4i2-003) |
| `next-intl` (≤4.9.1) | moderate | open redirect + prototype pollution | planifier migration 4.12.0 (semver-major, vérifier pathnames API) |
| `postcss` (<8.5.10) | moderate | XSS stringify `</style>` | attendre alignement Next 15 ou override contrôlé |
| `vitest` (≤3.0.0-beta.4) | moderate | dev-only (nouveau commit `dd0417c`) | bump vers vitest 4.x (semver-major, mineur impact sur la suite minimale actuelle) |
| `@vitest/mocker`, `esbuild`, `vite` | moderate | transitifs vitest, dev-only | résolus par bump vitest |

**Vulns prod-bloquantes** : 0. Les 4 nouvelles modérées sont strictement dev (dépendances Vitest), n'atteignent pas le bundle livré. Recommandation : `npm audit --omit=dev` post-Ph5 pour confirmer la photo production-only.

## 5. SEO (D7)

**seo-meta-auditor** — **PASS réserve**.
- Chaque page a son `generateMetadata` avec `title`, `description` localisés, `alternates.canonical`, `alternates.languages` (hreflang `fr-CA`/`en-CA`).
- ⚠️ **Lighthouse `canonical` FAIL** — explicable par W-001 (le test tourne sur `http://localhost:55191` avec `NEXT_PUBLIC_SITE_URL` non défini → `metadataBase` fallback `http://localhost:3000`, donc le canonical pointe vers un host différent du host courant, ce qui invalide l'audit). À lever en build prod avec `NEXT_PUBLIC_SITE_URL=https://depanneur-nobert.ca`.
- ⚠️ Lighthouse SEO global 92/100 (vs 100 attendu) — pénalité principale = canonical ci-dessus.

**jsonld-generator** — **PASS réserve**.
- `ConvenienceStore` (LocalBusiness), `WebSite`, `FAQPage` (PromotionsFAQ + ProduitsFAQ), `BreadcrumbList` — tous présents.
- Réserve : champ `image` du LocalBusiness pointe vers `/og-image.png` (fichier statique), alors que l'asset réel est la route `app/opengraph-image.tsx`. Aligner sur `${baseUrl}/opengraph-image` ou ajouter un fichier statique miroir.

**sitemap-validator** — **PASS**. `app/sitemap.ts` produit 12 URLs (6 routes × FR/EN) avec hreflang `fr-CA`/`en-CA`/`x-default`. Slugs EN distincts (`/deals`, `/products`, `/privacy-policy`, `/legal-notice`) corrects. `app/robots.ts` référence sitemap, bloque `/api/` et `/_next/`, autorise explicitement `GPTBot`/`Google-Extended`/`ClaudeBot`/`PerplexityBot`/`Bingbot` (différenciation Ph1 §3.4).

**broken-link-checker** — **PASS réserve**.
- Liens internes App Router cohérents (i18n routing pathnames).
- ⚠️ `getTelHref()` retourne `#` tant que `NEXT_PUBLIC_TELEPHONE` n'est pas fourni — non cassant techniquement, mais bloque le KPI conversion « Appeler ».
- ⚠️ `getMapsHref()` similaire pour adresse + code postal.

## 6. Accessibilité (D6)

**a11y-auditor** — **PASS**. `a11y.json = []` : **0 violation pa11y** sur l'URL auditée. Les 34 erreurs WCAG 2.2 AA 1.4.3 contraste de la Ph5 précédente sont résolues par le commit `ecbfa0f` (token `text.muted` `#8B7355 → #7A6447`, ratio passé de 4.24-4.49:1 à ≥ 5.0:1 sur les surfaces warm).

**color-contrast-fixer** — **PASS**. Tokens finaux mesurés :

| Combinaison | Ratio | Norme |
|---|---:|---|
| `text` `#2A1810` / `background` `#FFF8E7` | 14.5:1 | AAA |
| `text-secondary` `#6B4F3C` / `#FFF8E7` | 6.2:1 | AA / AAA texte large |
| `text-muted` `#7A6447` / `#FFF8E7` (post-fix) | ≥ 5.0:1 | AA |
| `text-on-accent` `#2A1810` / `accent` `#FFD700` | 12.4:1 | AAA |
| `text-on-primary` `#FFFFFF` / `primary` `#8B4513` | 7.3:1 | AAA |

**Lighthouse Accessibility** : **100 / 100**. Une seule alerte non bloquante :
- `label-content-name-mismatch` (WCAG 2.5.3) — `LanguageSwitcher` `<button aria-label="Choisir la langue du site">` mais texte visible = « EN English » (`<span>EN</span>` + `<span class="sr-only">English</span>`). L'aria-label devrait commencer par le texte visible. **Fix** : remplacer `aria-label={t('ariaLabel')}` par une variante incluant `EN` ou `FR` selon `otherLocale`, ex. `aria-label={\`${otherLocale.toUpperCase()} — ${t('ariaLabel')}\`}` ou supprimer `aria-label` au profit du `sr-only` seul (le bouton aura alors « EN English » comme nom accessible, conforme).

**keyboard-nav-tester** — **PASS réserve**.
- Skip-link `<a href="#main">` présent dans `[locale]/layout.tsx`, couleurs warm conformes.
- Focus rings warm `ring-primary` partout (Button, Input, Textarea, Checkbox, LanguageSwitcher, links).
- `prefers-reduced-motion` honoré globalement (`styles/globals.css`) — Framer Motion non installé, animations Tailwind only.
- ⚠️ Aucun test Playwright clavier automatisé — couvert manuellement Ph5 mais à automatiser dans D3.

## 7. Conformité Légale — Loi 25 (D8)

**legal-compliance** — **PASS réserve** (déploiement bloqué uniquement par les placeholders kickoff, pas par la conformité).

| Bloc | Résultat |
|---|---|
| Bandeau cookies opt-in 3 catégories | PASS — essentiels seuls par défaut, boutons Accepter/Refuser/Personnaliser équipondérés |
| Modification du consentement | PASS — `CookieSettingsButton` footer + reset localStorage + événement `consent-changed` |
| Catégories cookies | PASS — essentiels / analytics / marketing étanches |
| Google Maps gated | PASS — placeholder + bouton « Charger la carte (Google Maps - États-Unis) » avant iframe (ADR-004) |
| Politique de confidentialité | PASS — RPP **Nobert Tremblay** nommé, finalités, rétention (12 mois infolettre / 6 mois commandes / 30 j cookies), droits accès/rectification/suppression, sous-traitants Vercel/GA/Maps, transferts hors QC explicites |
| Incident de confidentialité | PASS — `nobert@depanneur-nobert.ca` et procédure art. 3.5 mentionnés |
| Mentions légales | PASS réserve — page existe, NEQ/adresse/téléphone en placeholders kickoff |
| Sécurité raisonnable (art. 10) | FAIL réserve — CSP absente, 4 moderate prod restantes |

**Bloquants business avant production** (rappel Ph4 §8) :
- `NEXT_PUBLIC_VILLE` (S-001, S-009, S-013, S-018, S-019, sitemap, JSON-LD)
- `NEXT_PUBLIC_ADRESSE_LIGNE` + `NEXT_PUBLIC_CODE_POSTAL` (S-018, S-019, S-024, JSON-LD)
- `NEXT_PUBLIC_TELEPHONE` (S-005, S-018, S-019, footer, S-024)
- `NEXT_PUBLIC_NEQ` (S-024)
- `NEXT_PUBLIC_ANNEE_FONDATION` (S-006 StoryBrand)
- `NEXT_PUBLIC_SITE_URL` (résolution canonical W-001)

Ces placeholders **n'invalident pas la conformité Loi 25** (la conformité est dans la structure, le RPP nommé, et les processus documentés) — ils bloquent uniquement la qualité éditoriale du site live.

## 8. Qualité du Code (D9)

**TypeScript** — **PASS**. `tsc --noEmit` retourne 0 erreur (strict + `noUncheckedIndexedAccess`).

**ESLint** — **PASS**. `npm run lint` (next lint) retourne 0 warning / 0 erreur. Note : `next lint` est déprécié et devra migrer vers ESLint CLI avant Next 16.

**Build** — **PASS**. `npm run build` compile 23 routes (12 SSG + 2 API + 9 metadata assets) en 3.8 s. First Load JS shared 102 KB.

**test-coverage-gap** — **PARTIAL** (auparavant FAIL).
- Suite Vitest active : `site/__tests__/cn.test.ts` + `cookieConsent.test.ts` + `rateLimit.test.ts` (commit `dd0417c`, 13 tests / 3 fichiers).
- Couverture utilitaires : ✅ `cn` helper, ✅ `cookieConsent` Context, ✅ `rateLimit` Map.
- **Gaps P0 restants** :
  - Routes API `/api/contact` + `/api/newsletter` (Zod schemas, honeypot, rate-limit intégré, SMTP wrapper)
  - Schemas Zod `FORM-CONTACT` + `FORM-NEWSLETTER` (validation FR/EN messages)
  - `MapsEmbed` consent gating (iframe injectée seulement après click)
  - `LanguageSwitcher` navigation cross-locale (pathnames FR≠EN)
  - JSON-LD builders (LocalBusiness, WebSite, FAQPage, échappement `<`)
- **Gaps P1** : composants formulaires (ContactForm, NewsletterCTA), Header navigation mobile, CookieConsentBanner UI.

**typo-fixer** — **PASS réserve**. Corrections recommandées (reconduit Ph5 précédente) :
- `messages/fr.json` : « Horaires régulières affichées » → « Horaires réguliers affichés »
- `messages/fr.json` : « on prépare l'ordre » → « on prépare la commande »
- `messages/fr.json` : « encryption » (texte légal) → « chiffrement »

## 9. Architecture (D1)

Architecture Next.js 15.5.18 App Router conforme :
- 6 pages × 2 locales = 12 routes SSG (+ ISR weekly sur `/promotions`).
- 2 routes API server-side (`/api/contact`, `/api/newsletter`) avec Zod + honeypot + rate-limit.
- i18n via `next-intl` 3.26.5, pathnames mapping FR≠EN strict (`/promotions`↔`/deals`, `/produits`↔`/products`, `/politique-confidentialite`↔`/privacy-policy`, `/mentions-legales`↔`/legal-notice`).
- Metadata routes natives (`sitemap.ts`, `robots.ts`, `icon.tsx`, `apple-icon.tsx`, `opengraph-image.tsx`, `manifest.ts`).
- 23 composants sections + 8 UI atoms + 7 layout — palette propagée via tokens Tailwind warm.

### Section Manifest Coverage

24 / 24 sections présentes, composants ET i18n namespaces vérifiés. Toutes au statut `audited`, `lifecycle.ph5_audited = 2026-05-15T08:00:00-04:00`.

| ID | Page | Section | Composant | i18n | Statut |
|----|------|---------|-----------|------|--------|
| S-001 | home | Hero | ✅ Hero.tsx | ✅ home.hero | audited |
| S-002 | home | PromotionsHighlight | ✅ PromotionsHighlight.tsx | ✅ home.promotionsHighlight | audited |
| S-003 | home | CategoriesProduits | ✅ CategoriesProduits.tsx | ✅ home.categories | audited |
| S-004 | home | SocialProofVoisinage | ✅ SocialProofVoisinage.tsx | ✅ home.socialProof | audited |
| S-005 | home | InfosPratiques | ✅ InfosPratiques.tsx | ✅ home.infos | audited |
| S-006 | home | StoryBrand | ✅ StoryBrand.tsx | ✅ home.story | audited |
| S-007 | home | NewsletterCTA | ✅ NewsletterCTA.tsx | ✅ home.newsletter | audited |
| S-008 | global | StickyCTA | ✅ StickyCTA.tsx | ✅ common.stickyCta | audited |
| S-009 | promotions | PromotionsHero | ✅ PromotionsHero.tsx | ✅ promotions.hero | audited |
| S-010 | promotions | PromotionsList | ✅ PromotionsList.tsx | ✅ promotions.list | audited |
| S-011 | promotions | PromotionsFAQ | ✅ PromotionsFAQ.tsx | ✅ promotions.faq | audited |
| S-012 | promotions | CrossSellProduits | ✅ CrossSellProduits.tsx | ✅ promotions.crossSell | audited |
| S-013 | produits | ProduitsHero | ✅ ProduitsHero.tsx | ✅ produits.hero | audited |
| S-014 | produits | ProduitsCategoriesNav | ✅ ProduitsCategoriesNav.tsx | ✅ produits.categoriesNav | audited |
| S-015 | produits | ProduitsGalerie | ✅ ProduitsGalerie.tsx | ✅ produits.galerie | audited |
| S-016 | produits | ProduitsFAQ | ✅ ProduitsFAQ.tsx | ✅ produits.faq | audited |
| S-017 | produits | CrossSellPromotions | ✅ CrossSellPromotions.tsx | ✅ produits.crossSell | audited |
| S-018 | contact | ContactHero | ✅ ContactHero.tsx | ✅ contact.hero | audited |
| S-019 | contact | CoordonneesHoraires | ✅ CoordonneesHoraires.tsx | ✅ contact.coordonnees | audited |
| S-020 | contact | MapsEmbed | ✅ MapsEmbed.tsx | ✅ contact.maps | audited |
| S-021 | contact | ContactForm | ✅ ContactForm.tsx | ✅ contact.form | audited |
| S-022 | contact | ContactNoteRPP | ✅ ContactNoteRPP.tsx | ✅ contact.rpp | audited |
| S-023 | politique-confidentialite | LegalDocBody | ✅ PrivacyPolicyBody.tsx | ✅ legal.privacy | audited |
| S-024 | mentions-legales | LegalDocBody | ✅ LegalNoticeBody.tsx | ✅ legal.notice | audited |

## 10. Top 5 — Actions Prioritaires

### #1 — Ajouter une CSP restrictive (déblocage D4)
- Impact : **+0.6 à +0.9 sur μ**, débloque D4 (CSP est la dernière pièce manquante de la sécurité raisonnable Loi 25 art. 10)
- Effort : **moyen** (45 min)
- Action : injecter `Content-Security-Policy` dans `vercel.json` (et redonder dans `next.config.mjs` headers async pour dev). Déployer en `Content-Security-Policy-Report-Only` au premier passage si crainte de casser Maps consent (`frame-src https://www.google.com https://maps.google.com`).
- Agents source : `csp-generator`, `security-headers`

### #2 — Ajouter les tests P0 (renforcement D3)
- Impact : **+0.3 à +0.5 sur μ**
- Effort : **moyen** (1 h 30 min)
- Action : 5 fichiers de tests Vitest minimum — `route-contact.test.ts`, `route-newsletter.test.ts`, `schemas.test.ts` (Zod), `mapsEmbed.test.tsx` (consent gating), `jsonld.test.ts` (échappement).
- Agent source : `test-coverage-gap`

### #3 — Corriger les 4 audits Lighthouse FAIL
- Impact : **+0.2 sur D5 + D6 + D7**
- Effort : **trivial à moyen**
- Actions :
  1. `errors-in-console` 404 `/fr/icon` → investiguer le double-rendering icon.tsx vs sub-path locale.
  2. `canonical` FAIL → définir `NEXT_PUBLIC_SITE_URL` au build kickoff (résout aussi W-001 metadataBase).
  3. `label-content-name-mismatch` → ajuster `aria-label` du `LanguageSwitcher` pour inclure le texte visible (`EN` ou `FR`).
  4. `redirects` `/` → `/fr` 605 ms : compromis par design (next-intl `localePrefix: always`), accepter ou activer `localeDetection` côté middleware pour redirect 308 plus rapide.
- Agents source : `lighthouse-runner`, `keyboard-nav-tester`, `seo-meta-auditor`

### #4 — Finaliser les données client/legal (déblocage déploiement)
- Impact : **0 sur μ technique**, mais bloque le déploiement éditorial
- Effort : **dépend du client**
- Action : fournir 6 variables d'env `NEXT_PUBLIC_*` au kickoff (ville, adresse, code postal, téléphone, NEQ, année fondation) + `NEXT_PUBLIC_SITE_URL`. Optionnel : photo `/images/hero-vitrine.jpg`, consentement écrit voisinage S-004.
- Agents source : `legal-compliance`, `seo-meta-auditor`, `broken-link-checker`

### #5 — Réparer tooling SSL + Osiris + bumper vitest
- Impact : **+0.1 sur D4/D5** (visibilité métrique, pas qualité site)
- Effort : **trivial**
- Actions :
  1. SSL : refaire mesure sur `https://depanneur-nobert.ca` post-DNS Vercel (côté tooling NEXOS, pas site).
  2. Osiris : aligner wrapper `tools/preflight.sh` sur la nouvelle CLI scanner.py (`--format` obsolète).
  3. Vitest : `npm install vitest@4 --save-dev` pour purger 4 moderate dev-only de l'audit.
- Agents source : `ssl-auditor`, `osiris-runner`, `dep-vulnerability`

## 11. Roadmap de Corrections

**Boucle corrective P5→P5'** (estimation 2 h 30 min) :

1. **CSP** : ajouter le bloc CSP dans `vercel.json` `headers` (45 min). Redéployer build local, relancer `tools/preflight.sh`, vérifier `headers.json` contient `content-security-policy`.
2. **Tests P0** : créer les 5 fichiers Vitest listés (1 h 30 min). Relancer `npm test`, viser ≥ 35 tests passants.
3. **Lighthouse fixes** : corriger LanguageSwitcher aria-label + canonical via env (15 min). Relancer Lighthouse, viser SEO ≥ 95 + A11y maintenu à 100.
4. **Re-run preflight + audit** : `tools/preflight.sh <URL> clients/depanneur-nobert`, recalculer μ.

**Critère GO après corrections** :
- μ ≥ 8.5
- D4 ≥ 8.0 (CSP présent)
- D6 = 9.5+ (a11y maintenu, label fixé)
- D8 ≥ 8.5 (sécurité raisonnable incluant CSP)
- pa11y 0 erreur (déjà OK)
- npm audit prod-only 0 HIGH/CRITICAL (déjà OK)

## 12. Recommandations Post-Déploiement

**post-deploy-setup** — **SKIP** tant que Ph5 est FAIL. À exécuter après μ ≥ 8.5 et déploiement explicite utilisateur :

1. **DNS + HTTPS** : configurer `depanneur-nobert.ca` sur Vercel, vérifier certificat Let's Encrypt actif, refaire `ssl-auditor`.
2. **Google Search Console** : soumettre `https://depanneur-nobert.ca/sitemap.xml`, vérifier indexation FR + EN.
3. **Analytics** : activer GA seulement après opt-in cookie analytics (déjà gated par `useConsent()`).
4. **Core Web Vitals** : monitorer LCP en production (cible ≤ 2.5 s sur mobile 4G). Le 3.3 s local est surévalué par redirect `/` → `/fr` — en prod, l'utilisateur arrive directement sur `/fr` via détection middleware.
5. **CSP Report-Only → Enforced** : après 7 j de report-only sans violation, bascule en `Content-Security-Policy` strict.
6. **npm audit hebdomadaire** : surveiller `next-intl` 4.x stable et `postcss` ≥ 8.5.10.
7. **Test perception palette warm** : validation auprès du voisinage cible 35-65 (Ph2 itération 2 demande).

## Réconciliation Ph4 ↔ Ph5

| Mesure | Ph4 (itération 2) | Ph5 (2026-05-15) | Écart |
|---|---:|---:|---:|
| μ | 9.85 | **8.39** | **1.46** |
| D4 Sécurité | 9.75 | 7.50 | 2.25 |
| D6 Accessibilité | 9.50 (estim.) | 9.50 (mesuré) | 0 |
| D3 Tests | 10.0 (estim. build pass) | 6.0 (mesuré P0 vides) | 4.0 |

**Statut** : ✓ OK (écart < 2.0 sur la μ globale, conforme seuil divergence NEXOS).

**Cause principale du delta** : Ph4 mesure le build (compilation, headers vercel.json déclarés, scaffold Vitest présent) ; Ph5 mesure la réalité opérationnelle (CSP absente du runtime, tests P0 manquants, 4 audits Lighthouse FAIL). C'est précisément le rôle du quality gate ph4→ph5 : transformer les promesses build en preuves runtime.

## Verdict Final

- **μ = 8.39** (seuil deploy 8.5)
- **Decision `deploy-master`** : **NO DEPLOY**
- **Boucle corrective P5'** requise — durée estimée 2 h 30 min, bénéfice attendu Δμ ≈ +0.9 → μ' ≈ 9.3
- **Aucune action destructive exécutée** (pas de `vercel deploy`, pas de `git push`, pas de modification site/ hors lecture)

Le manifest a été conservé tel quel (24/24 sections statut `audited`, `last_updated_phase: ph5-qa`) — pas de régression statut. `nexos-changelog.json` à appender côté pipeline si exécuté en mode automatisé.

## Reconciliation Ph4 ↔ Ph5

**Statut** : ✓ OK
**μ Ph4** : 9.84
**μ Ph5** : 9.11
**Écart** : 0.73 (seuil divergence = 2.0)

Ph4 et Ph5 cohérents : μ4=9.84 vs μ5=9.11, écart=0.73 ≤ seuil=2.0
