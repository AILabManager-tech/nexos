# Collectif Nova — Site

Site Next.js 15 (App Router) bilingue FR/EN, généré par NEXOS v4.2.

## Démarrage

```bash
npm install
cp .env.example .env.local   # remplir les variables kickoff si présent
npm run dev                  # http://localhost:3000
```

## Scripts

- `npm run dev` — serveur de développement
- `npm run build` — build production
- `npm run start` — serveur production
- `npm run typecheck` — `tsc --noEmit` (TypeScript strict)
- `npm run lint` — ESLint
- `npm test` — Vitest (si configuré)

## Stack

- **Framework** : Next.js 15+ (App Router)
- **TypeScript** : strict mode (`noUncheckedIndexedAccess`, `strictNullChecks`)
- **CSS** : Tailwind CSS
- **i18n** : next-intl FR/EN
- **Déploiement** : Vercel

## Conformité Loi 25 Québec

Le site inclut :
- Bandeau cookies opt-in (`components/layout/CookieConsent.tsx`)
- Politique de confidentialité (`app/[locale]/politique-confidentialite/`)
- Mentions légales (`app/[locale]/mentions-legales/`)
- RPP (Responsable de la Protection des Renseignements personnels) configuré dans `brief-client.json`

## Sécurité (headers prod)

Configurés dans `vercel.json` (servis par Vercel CDN) :
- Content-Security-Policy
- Strict-Transport-Security
- X-Content-Type-Options, X-Frame-Options
- Referrer-Policy, Permissions-Policy

## Pipeline NEXOS

Ce site a été généré par le pipeline NEXOS v4.2 (6 phases ph0→ph5, 48 agents
spécialisés, quality gates SOIC μ ≥ 8.0). Les rapports de pipeline sont dans
`../soic-gates.json`, `../ph5-qa-report.md`, `../nexos-changelog.json`.

---

_Généré par `nexos fix` → `_fix_readme()` (D5 ROADMAP). Régénéré au prochain
`nexos fix` si supprimé._
