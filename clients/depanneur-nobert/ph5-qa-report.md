# Rapport QA — Dépanneur Nobert — 2026-05-14

## 1. Resume Executif
- Score SOIC mu : **7.52 / 10**
- Verdict : **FAIL — boucle corrective requise**
- Pages auditees : **12 routes SSG** (6 pages x 2 locales) + 2 routes API
- Sections auditees : **24 / 24**
- Agents executes : **23 / 23**
- Tooling reel lu : `lighthouse.json`, `headers.json`, `deps.json`, `a11y.json`, `ssl.json`, `osiris.json`
- Decision `deploy-master` : **NO DEPLOY**. Aucun `vercel deploy` execute.

Le site est solide en build, architecture, performance brute et Loi 25 de base. Le deploiement est bloque par trois faits mesures : **34 erreurs pa11y WCAG AA de contraste**, **CSP absente**, et **couverture tests applicative inexistante**. Deux sorties tooling sont aussi invalides : SSL vise `localhost:443`, et Osiris echoue par dependance Python manquante (`click`).

## 2. Tableau de Scores par Dimension
| Dim | Nom | Score | Poids | Pondere | Status |
|-----|-----|------:|------:|--------:|--------|
| D1 | Architecture | 9.50 | x1.0 | 9.50 | PASS |
| D2 | Documentation | 8.00 | x0.8 | 6.40 | PASS reserve |
| D3 | Tests | 4.00 | x0.9 | 3.60 | FAIL |
| D4 | Securite | 6.80 | x1.2 | 8.16 | FAIL bloquant |
| D5 | Performance | 8.70 | x1.0 | 8.70 | PASS reserve |
| D6 | Accessibilite | 6.00 | x1.1 | 6.60 | FAIL |
| D7 | SEO | 8.00 | x1.0 | 8.00 | PASS reserve |
| D8 | Conformite | 8.50 | x1.1 | 9.35 | PASS reserve |
| D9 | Code Quality | 8.20 | x0.9 | 7.38 | PASS reserve |
| mu | **Score Final** | | | **7.52** | **FAIL** |

## 3. Performance (D3/D5)
**lighthouse-runner** : Lighthouse 13.1.0 reel sur `http://localhost:59693/` redirige vers `/fr`.

| Mesure | Valeur | Statut |
|---|---:|---|
| Performance | 92 / 100 | PASS |
| FCP | 1.1 s | PASS |
| LCP | 3.3 s | WARN |
| Speed Index | 1.1 s | PASS |
| TBT | 10 ms | PASS |
| CLS | 0 | PASS |
| Payload total | 467 KiB | PASS |

**bundle-analyzer** : First Load JS partage : 102 kB. Route la plus lourde : `/[locale]/contact` a 162 kB, sous budget, mais a surveiller.

**image-optimizer** : pas d’images lourdes detectees dans `public/`; `next/image` n’est pas utilise. Les assets principaux sont generes par metadata routes (`icon`, `apple-icon`, `opengraph-image`). Lighthouse signale toutefois un **404 sur `/fr/icon?...`**, a corriger avant deploy.

**css-purger** : Lighthouse rapporte 0 ms / 0 byte d’economie en CSS inutilise. PASS.

**cache-strategy** : headers reels montrent `cache-control: s-maxage=31536000` sur la page prerendue et cache immutable configure pour `/_next/static`. PASS.

**Osiris** : FAIL outil. `osiris.json` contient `ModuleNotFoundError: No module named click`. La sobriete web n’a donc pas ete mesuree.

## 4. Securite (D4)
**security-headers** : `headers.json` confirme les headers P0 principaux.

| Header | Reel | Statut |
|---|---|---|
| Strict-Transport-Security | `max-age=63072000; includeSubDomains; preload` | PASS |
| X-Content-Type-Options | `nosniff` | PASS |
| X-Frame-Options | `DENY` | PASS |
| Referrer-Policy | `strict-origin-when-cross-origin` | PASS |
| Permissions-Policy | `camera=(), microphone=(), geolocation=(self)` | PASS |
| X-DNS-Prefetch-Control | `on` | PASS |
| Content-Security-Policy | absent | FAIL |
| X-XSS-Protection | absent | WARN |

**csp-generator** : FAIL. Aucune CSP n’est presente dans `headers.json`, `next.config.mjs`, `vercel.json` ou `middleware.ts`. CSP minimale attendue :

```text
default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' https://api.resend.com; frame-src https://maps.google.com; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests
```

**ssl-auditor** : mesure invalide. `ssl.json` indique `unable to connect to localhost:443`. A refaire sur `https://depanneur-nobert.ca` apres configuration DNS/Vercel.

**xss-scanner** : PASS reserve. Une seule occurrence `dangerouslySetInnerHTML` dans `lib/jsonld.ts`, limitee au JSON-LD et echappant `<` en `\u003c`. Pas de DOMPurify requis pour les pages legales, qui sont en JSX statique.

**dep-vulnerability** : PASS reserve. `npm audit` reel : 0 critical, 0 high, 3 moderate.

| Package | Severite | Advisory | Action |
|---|---|---|---|
| `next-intl` | moderate | open redirect + prototype pollution | planifier migration 4.12.0 |
| `postcss` | moderate | XSS stringify `</style>` | attendre resolution compatible Next 15 ou override controle |
| `next` via `postcss` | moderate | transitif | surveiller |

## 5. Accessibilite (D6)
**a11y-auditor** : FAIL. `a11y.json` contient **34 erreurs WCAG2AA 1.4.3 contraste**.

Les erreurs touchent surtout `text-text-muted` sur les surfaces warm (`#FFF8E7`, `#FFFFFF`, surfaces attenuees). Ratios mesures : **4.24:1** et **4.49:1**, sous le minimum AA de 4.5:1. Exemples :

| Zone | Extrait | Ratio |
|---|---|---:|
| Hero | intro promotions / horaires | 4.24 |
| PromotionsHighlight | prix barres + validite | 4.49 |
| CategoriesProduits | descriptions categories | 4.49 |
| SocialProofVoisinage | roles temoignages | 4.49 |
| InfosPratiques | horaires, labels, note | 4.24-4.49 |
| Cookie banner | lien politique + note Loi 25 | 4.49 |

**color-contrast-fixer** : correction prioritaire : assombrir le token `text.muted` / CSS var equivalente pour atteindre au moins 4.7:1 sur toutes les surfaces, puis relancer pa11y.

**keyboard-nav-tester** : PASS reserve. Skip-link present, focus rings presents, controles formulaire etiquetes. Aucun test clavier automatise Playwright fourni.

## 6. SEO (D7)
**seo-meta-auditor** : PASS reserve. Metadata par page presente, title/description localises, canonical et alternates definis. Warning build : `metadataBase property ... not set` pour certaines sub-pages avec `generateMetadata`; les OG/Twitter risquent le fallback `http://localhost:3000` si l’env n’est pas resolue.

**jsonld-generator** : PASS reserve. JSON-LD `ConvenienceStore`, `WebSite`, `FAQPage` et breadcrumbs disponibles. Reserve : `image` pointe vers `/og-image.png`, alors que l’asset reel est la route `opengraph-image`.

**sitemap-validator** : PASS. `sitemap.ts` produit 12 URLs FR/EN avec `fr-CA`, `en-CA`, `x-default`. `robots.ts` reference le sitemap et bloque `/api/`, `/_next/`.

**broken-link-checker** : PASS reserve. Liens internes App Router cohérents. Reserve : `getTelHref()` retourne `#` tant que `NEXT_PUBLIC_TELEPHONE` n’est pas fourni; ce n’est pas cassant techniquement, mais bloque le KPI conversion.

## 7. Conformite Legale — Loi 25 (D8)
**legal-compliance** : PASS reserve, non deployable tant que les donnees legales finales ne sont pas fournies.

| Bloc | Resultat |
|---|---|
| Bandeau cookies opt-in | PASS : essentiels seuls par defaut, accepter/refuser/personnaliser visibles |
| Modification du consentement | PASS : `CookieSettingsButton` + reset localStorage |
| Categories cookies | PASS : essentiels, analytics, marketing |
| Google Maps | PASS : iframe charge uniquement apres consentement marketing |
| Politique confidentialite | PASS : RPP, finalites, retention, droits, tiers, transferts hors QC |
| Incident confidentialite | PASS : contact RPP et procedure art. 3.5 mentionnes |
| Mentions legales | PASS reserve : page existe, mais NEQ/adresse/telephone sont placeholders |
| Securite raisonnable | FAIL reserve : CSP absente, 3 vulns moderate |

Points de blocage business avant production : `NEXT_PUBLIC_VILLE`, `NEXT_PUBLIC_ADRESSE_LIGNE`, `NEXT_PUBLIC_CODE_POSTAL`, `NEXT_PUBLIC_TELEPHONE`, `NEXT_PUBLIC_NEQ`, `NEXT_PUBLIC_ANNEE_FONDATION`.

## 8. Qualite du Code (D9)
**TypeScript** : PASS apres build. `npm run typecheck` retourne 0 erreur.

**ESLint** : PASS. `npm run lint` retourne 0 warning / 0 erreur. Note : `next lint` est deprecie et devra migrer vers ESLint CLI avant Next 16.

**Build** : PASS. `npm run build` compile 23 routes, First Load JS 102 kB, route contact 162 kB.

**test-coverage-gap** : FAIL. Aucun `vitest.config.*`, aucun test applicatif hors `node_modules`. 70 fichiers TS/TSX applicatifs inventories.

Gaps P0 : routes API contact/newsletter, schemas Zod, rate limit, consentement cookies, formulaires contact/newsletter.

**typo-fixer** : PASS reserve. Corrections recommandees :
- `Horaires régulières affichées` -> `Horaires réguliers affichés`
- `on prépare l'ordre` -> `on prépare la commande`
- `encryption` dans le texte FR legal -> `chiffrement`

## 9. Architecture (D1)
Architecture Next.js App Router conforme : 6 pages bilingues, routes API server-side, `next-intl`, metadata routes, JSON-LD, formulaire contact/newsletter avec Zod + honeypot + rate limit.

### Section Manifest Coverage
| ID | Page | Section | Composant | i18n | Statut |
|----|------|---------|-----------|------|--------|
| S-001 | home | Hero | PASS | PASS | audited |
| S-002 | home | PromotionsHighlight | PASS | PASS | audited |
| S-003 | home | CategoriesProduits | PASS | PASS | audited |
| S-004 | home | SocialProofVoisinage | PASS | PASS | audited |
| S-005 | home | InfosPratiques | PASS | PASS | audited |
| S-006 | home | StoryBrand | PASS | PASS | audited |
| S-007 | home | NewsletterCTA | PASS | PASS | audited |
| S-008 | global | StickyCTA | PASS | PASS | audited |
| S-009 | promotions | PromotionsHero | PASS | PASS | audited |
| S-010 | promotions | PromotionsList | PASS | PASS | audited |
| S-011 | promotions | PromotionsFAQ | PASS | PASS | audited |
| S-012 | promotions | CrossSellProduits | PASS | PASS | audited |
| S-013 | produits | ProduitsHero | PASS | PASS | audited |
| S-014 | produits | ProduitsCategoriesNav | PASS | PASS | audited |
| S-015 | produits | ProduitsGalerie | PASS | PASS | audited |
| S-016 | produits | ProduitsFAQ | PASS | PASS | audited |
| S-017 | produits | CrossSellPromotions | PASS | PASS | audited |
| S-018 | contact | ContactHero | PASS | PASS | audited |
| S-019 | contact | CoordonneesHoraires | PASS | PASS | audited |
| S-020 | contact | MapsEmbed | PASS | PASS | audited |
| S-021 | contact | ContactForm | PASS | PASS | audited |
| S-022 | contact | ContactNoteRPP | PASS | PASS | audited |
| S-023 | politique-confidentialite | LegalDocBody | PASS | PASS | audited |
| S-024 | mentions-legales | LegalDocBody | PASS | PASS | audited |

Le manifest a ete rafraichi avec `ph5_audited = 2026-05-14T12:00:00-04:00`.

## 10. Top 5 — Actions Prioritaires
### #1 — Corriger le contraste `text-text-muted`
- Impact : +1.0 a +1.4 sur D6
- Effort : trivial
- Action : assombrir le token muted et relancer pa11y.
- Agent source : a11y-auditor, color-contrast-fixer

### #2 — Ajouter une CSP restrictive
- Impact : +0.5 a +0.8 sur mu, debloque D4
- Effort : moyen
- Action : ajouter CSP dans `next.config.mjs` ou middleware, incluant Resend et Google Maps seulement.
- Agent source : csp-generator, security-headers

### #3 — Ajouter les tests P0
- Impact : +0.6 a +1.0 sur mu
- Effort : moyen
- Action : Vitest + tests schemas, API routes, rate limit, cookie consent, formulaires.
- Agent source : test-coverage-gap

### #4 — Finaliser les donnees client/legal
- Impact : +0.3 sur D8/D7/conversion
- Effort : depend du client
- Action : ville, adresse, code postal, telephone, NEQ, anneeFondation.
- Agent source : legal-compliance, seo-meta-auditor, broken-link-checker

### #5 — Refaire tooling SSL/Osiris et fixer l’icone 404
- Impact : +0.2 a +0.4 sur mu
- Effort : trivial a moyen
- Action : relancer SSL sur domaine HTTPS reel, installer `click` pour Osiris, corriger `/fr/icon?...`.
- Agent source : ssl-auditor, post-deploy-setup, lighthouse-runner

## 11. Roadmap de Corrections
1. Patch accessibilite : ajuster `text-muted`, verifier les surfaces, relancer `tools/preflight.sh`.
2. Patch securite : ajouter CSP, conserver headers existants, verifier Maps gated et Resend.
3. Patch tests : installer/configurer Vitest si absent, couvrir P0 avant de remonter D3.
4. Patch SEO/legal : ajouter `metadataBase` explicite aux sub-pages ou garantir `NEXT_PUBLIC_SITE_URL`, corriger JSON-LD image/logo, injecter les donnees finales.
5. Tooling : reparer Osiris (`click`), refaire SSL sur domaine de production, relancer Lighthouse/pa11y/headers/deps.

Critere GO apres corrections : mu >= 8.5, D4 >= 7.0, D8 >= 7.0, pa11y 0 erreur critique, npm audit 0 high/critical.

## 12. Recommandations Post-Deploiement
**post-deploy-setup** : SKIP tant que Ph5 est FAIL.

Apres correction et deploy explicite par l’utilisateur :
- Configurer DNS Vercel + HTTPS, puis refaire SSL.
- Soumettre `https://depanneur-nobert.ca/sitemap.xml` dans Google Search Console.
- Activer Analytics seulement apres consentement opt-in.
- Verifier Core Web Vitals en production, surtout LCP.
- Surveiller `npm audit` pour `next-intl` et `postcss`.
- Ajouter monitoring CSP en `Content-Security-Policy-Report-Only` si la CSP stricte risque de casser Maps/Resend au premier passage.

## Reconciliation Ph4 ↔ Ph5

**Statut** : ✓ OK
**μ Ph4** : 9.84
**μ Ph5** : 8.78
**Écart** : 1.06 (seuil divergence = 2.0)

Ph4 et Ph5 cohérents : μ4=9.84 vs μ5=8.78, écart=1.06 ≤ seuil=2.0
