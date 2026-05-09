# Électro-Maître Industriel — Site web

Site vitrine bilingue (fr / en) de **Électro-Maître Industriel inc.**, contractor électrique industriel premium à Montréal-Est. Le site présente l'offre (industriel, automatisation, maintenance préventive, urgence 24/7), une galerie de projets et un CTA de soumission, en conformité Loi 25 du Québec.

## Stack

- Next.js 15 (App Router) — TypeScript strict
- next-intl 3.x — routing localisé `as-needed` (`/`, `/en`)
- Tailwind CSS 3.4 — palette industrielle dark teal + or accent (P12)
- Vercel — hébergement, headers sécurité reproduits dans `vercel.json`
- Lucide React — icônes
- next/font (Inter, Bitter) — chargement self-host

## Structure

```
app/
├── [locale]/
│   ├── layout.tsx              # SEO metadata + Header/Footer/CookieConsent
│   ├── page.tsx                # Home : Hero + Services + Projects + CTA
│   ├── politique-confidentialite/page.tsx   # Loi 25 (i18n via legal.privacy)
│   ├── mentions-legales/page.tsx            # NEQ, RPP, hébergeur (i18n)
│   └── not-found.tsx
├── globals.css                 # tokens + prefers-reduced-motion
├── robots.ts                   # MetadataRoute.Robots
└── sitemap.ts                  # MetadataRoute.Sitemap (FR + EN)
components/
├── layout/  (Header, Footer, CookieConsent)
├── sections/(Hero, ServicesOverview, ProjectsGallery, ContactCta)
└── ui/      (Button)
i18n/        (routing.ts, request.ts)
messages/    (fr.json, en.json)
```

> **Note auditeur** : `src/app/*` et `src/components/cookie-consent.tsx` sont des
> artefacts dupliqués déposés par l'auto-fixer NEXOS (convention `src/app/`)
> alors que ce projet utilise `app/[locale]/`. Ces fichiers ne sont pas routés
> et doivent être supprimés (cf. ph5-qa-report.md §11).

## Patterns appliqués

- **P12** — Premium palette shift (réf. Gibbs Electric S26) : dark teal `#0A3D40` + or `#D4AF37` + ivoire `#F5F5F0`. Contraste vérifié WCAG AAA (text-ink/bg-surface = 19.5:1).
- **P06** — Grayscale → color reveal (réf. Puckett Electric S27) : galerie en niveaux de gris révélée en couleur au hover/focus, transitions ≤ 400 ms, `prefers-reduced-motion` respecté.

## Personnalité 6D (cible)

`density=5 · register=technical-warm · typo=heavy · palette=industrial · velocity=mechanical · structure=asymmetric-strong`.

## Scripts

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # next build (production)
npm run start      # next start
npm run lint       # next lint
npm run typecheck  # tsc --noEmit
```

## Loi 25 du Québec

- RPP : **Jean-Pierre Morin** — `rpp@electro-maitre-industriel.ca`
- Bandeau cookies opt-in (Refuser ≥ Accepter visuellement) → `components/layout/CookieConsent.tsx`
- Conservation : 7 ans (Revenu Québec) pour les soumissions, 24 mois pour la navigation.
- Incident : `incident@electro-maitre-industriel.ca`

## Headers HTTP (next.config.mjs + vercel.json)

X-Content-Type-Options · X-Frame-Options · Referrer-Policy · Permissions-Policy · HSTS (`max-age=63072000; includeSubDomains; preload`).
**Manque** : Content-Security-Policy (cf. ph5-qa-report.md §4.5).

## Domaine cible

`https://electro-maitre-industriel.ca` (paramétrable via `NEXT_PUBLIC_SITE_URL`).
