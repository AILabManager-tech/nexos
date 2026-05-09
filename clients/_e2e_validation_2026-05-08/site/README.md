# Dépanneur Nobert — Site web

Site vitrine bilingue (FR/EN) pour **Dépanneur Nobert inc.** — dépanneur de quartier au Québec.
Généré et audité par la plateforme NEXOS v4.2 (mode `create`, KPI primaire `conversion`).

## Stack

- **Next.js 15.5.18** (App Router, Server Components par défaut, SSG strict)
- **TypeScript 5.7** strict (`noUncheckedIndexedAccess`)
- **Tailwind CSS 3.4** + tokens design-system NEXOS (palette `warm` imposée par le brief)
- **next-intl 3.26** (FR/EN, pathnames localisés `/produits` ↔ `/products`, etc.)
- **react-hook-form 7 + zod 3** pour les formulaires
- **Vitest 2** pour les tests unitaires (`npm test`)
- **Vercel** pour le déploiement (headers HTTP + CSP dans `vercel.json`)

## Routes (12 URLs SSG)

| FR | EN | Sections (manifest) |
|---|---|---|
| `/` | `/en` | S-001 → S-006 |
| `/promotions` | `/en/promotions` | S-007, S-008, S-006 |
| `/produits` | `/en/products` | S-009, S-010, S-011 ×6 catégories |
| `/contact` | `/en/contact` | S-012 → S-016 |
| `/politique-confidentialite` | `/en/privacy-policy` | S-017 |
| `/mentions-legales` | `/en/legal-notice` | S-017 |

## Conformité Loi 25 (Québec)

- `CookieConsent` opt-in 3 catégories (essentiels / analytics / marketing) monté dans `app/[locale]/layout.tsx`. Par défaut, seuls les cookies essentiels sont actifs.
- RPP nommé visible (footer + section S-016 page contact) : Nobert Tremblay, courriel rpp.
- Pages `/politique-confidentialite` et `/mentions-legales` rendues à partir des templates NEXOS, placeholders interpolés depuis `brief-client.json::legal`.
- Formulaires `ContactForm` + `NewsletterCta` :
  - Mention de finalité explicite + lien vers la politique de confidentialité au-dessus du formulaire.
  - Checkbox de consentement jamais pré-cochée (validation Zod `z.literal(true)`).
  - Honeypot + rate-limit (`/api/contact` 3/h, `/api/newsletter` 5/h).

## Sécurité

7 headers HTTP appliqués via `vercel.json` (production) :
`X-Content-Type-Options: nosniff` · `X-Frame-Options: DENY` · `Referrer-Policy: strict-origin-when-cross-origin` · `Permissions-Policy: camera=(), microphone=(), geolocation=()` · `X-DNS-Prefetch-Control: on` · `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` · **CSP restrictive** (default-src 'self', frame-src google.com/maps.google.com, etc.).

`next.config.mjs` applique 6 headers en local-dev (CSP exclusive à Vercel volontairement, pour ne pas casser HMR).

`poweredByHeader: false`. Aucun `dangerouslySetInnerHTML` sauf JSON-LD (`components/seo/JsonLd.tsx`). API keys server-side uniquement.

## Accessibilité

- Skip-to-content + drawer mobile `Header` avec `Escape` + focus-trap léger.
- Focus ring `:focus-visible` 3px primary contraste 7.91:1.
- Touch targets ≥ 48px sur tous les CTA.
- `prefers-reduced-motion` respecté globalement (`styles/globals.css`).
- `eslint-plugin-jsx-a11y` activé.
- Audit `pa11y` Phase 5 : 1 anomalie résiduelle documentée (`ph5-qa-report.md` § a11y).

## SEO

- `app/sitemap.ts` dynamique (12 URLs, `alternates.languages` FR/EN).
- `app/robots.ts` (`Allow: /` + `Disallow: /api/`).
- `buildMetadata()` (`lib/seo.ts`) génère par page : title, description, canonical, alternates languages FR/EN/x-default, OpenGraph locale-aware, Twitter card.
- JSON-LD `Organization` + `WebSite` (layout root) + `LocalBusiness` + `ConvenienceStore` + `OpeningHoursSpecification` + `GeoCoordinates` (home + contact).

## Scripts

```bash
npm run dev          # Next dev sur http://localhost:20005
npm run build        # next build (SSG 19 pages)
npm run start        # next start prod sur :20005
npm run lint         # next lint
npm run type-check   # tsc --noEmit
npm test             # vitest run (tests unitaires lib/)
npm run test:watch   # vitest watch mode
```

## Structure

```
app/                      # App Router (layouts, pages, API routes, sitemap, robots)
components/
  layout/                 # Header, Footer, CookieConsent, StickyMobileCta, etc.
  sections/               # 17 sections (S-001 → S-017), data-manifest-id
  seo/                    # JsonLd
  ui/                     # Button, Card, Container, Input, Section, etc.
i18n/                     # routing.ts, request.ts (next-intl)
lib/                      # utils, format, schemas (zod), rate-limit, seo, structured-data
messages/                 # fr.json, en.json (next-intl)
public/                   # favicon, og-image, images
site/data/                # site-info.json, horaires.json, promotions.json, products-categories.json
styles/                   # globals.css
tests/                    # vitest specs (lib/)
types/                    # promotion.ts, product.ts, site-info.ts
```

## Statut Phase 5

Voir `../ph5-qa-report.md` pour l'audit complet (Lighthouse, pa11y, npm audit, headers réels, section-manifest coverage).

## Bloquants kickoff (avant déploiement final)

1. Slot `[ville]` à résoudre (search-and-replace dans `messages/{fr,en}.json` + `site/data/site-info.json::city`).
2. Photo réelle propriétaire à fournir → remplacer `public/images/hero-nobert.jpg`.
3. NEQ + adresse + téléphone réels → `site/data/site-info.json`.
4. Choix ESP/SMTP pour persistance newsletter + contact → swap des fonctions `POST` dans `app/api/{newsletter,contact}/route.ts` (contrat HTTP stable, zéro rebuild applicatif).
