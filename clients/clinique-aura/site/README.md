# Clinique Aura — site web

Site vitrine bilingue (FR/EN) de la Clinique Aura inc. (Montréal). Stack : Next.js 15 (App Router) + TypeScript strict + Tailwind 3.4 + next-intl 3.25 + Lucide React. Hébergement Vercel, domaine `clinique-aura.ca`.

Généré et opéré par le pipeline NEXOS v4.2 (mode `create` puis `audit`). Les sections livrées sont catalogues dans `../section-manifest.json`. Le brief est dans `../brief-client.json`. Les patterns appliqués (P02 social proof adjacent CTA, P04 hero émotionnel) viennent de `agents/knowledge/web-patterns-reference.md`.

## Structure

- `app/[locale]/` — pages localisées (home, politique-confidentialite, mentions-legales) + `layout.tsx` (metadata, fonts, providers next-intl)
- `app/sitemap.ts` / `app/robots.ts` — SEO discovery
- `components/sections/` — sections de page (Hero, ServicesOverview, TestimonialsAdjacentCta, ContactCta alias)
- `components/layout/` — Header, Footer, CookieConsent (Loi 25 opt-in)
- `messages/{fr,en}.json` — strings i18n FR/EN
- `i18n/` — config routing next-intl
- `tailwind.config.ts` — palette warm (ivoire, ambre, terre de Sienne)
- `next.config.mjs` / `vercel.json` — config Next + headers HTTP de sécurité

## Scripts npm

| Commande | Effet |
|---|---|
| `npm run dev` | serveur dev Next sur port libre (`PORT=20001 npm run dev` recommandé, plage NEXOS) |
| `npm run build` | build de production Next (incluse dans la gate ph4) |
| `npm run start` | serveur prod (statique) |
| `npm run lint` | `next lint` (eslint-config-next) |
| `npm run typecheck` | `tsc --noEmit` (TS strict, `noUncheckedIndexedAccess`) |

## Conformité Loi 25 (Québec)

- Bandeau cookies opt-in (`components/layout/CookieConsent.tsx`) — refuser aussi visible qu'accepter, 0 cookie tiers tant que consentement = false
- Politique de confidentialité dédiée (`/politique-confidentialite`) avec RPP nommé (Dr. Sophie Tremblay), finalités, rétention, droits
- Mentions légales (`/mentions-legales`) avec NEQ, hébergeur (Vercel US), courriel d'incident
- Données collectées et finalités déclarées dans `brief-client.json::legal`

## Déploiement

Déploiement Vercel via la gate `deploy-master` du pipeline NEXOS (μ SOIC ≥ 8.5 requis). Headers de sécurité (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `Strict-Transport-Security`) imposés par `vercel.json`. CSP à compléter (cf. `../ph5-qa-report.md`, P1.5).

## Audit qualité

Le rapport d'audit le plus récent vit dans `../ph5-qa-report.md`. Les mesures réelles (Lighthouse, pa11y, headers, ssl, npm-audit) sont dans `../tooling/`.
