# La Table de Marguerite — Site web

Site vitrine bilingue (FR/EN) du restaurant bistronomique **La Table de Marguerite**, scaffolé via NEXOS v4.2 (chantier G option A, patterns P08 + P20).

## Stack

- **Framework** : Next.js 15.5.15 (App Router, RSC)
- **Langage** : TypeScript 5.6 (strict)
- **i18n** : next-intl 3.25 — locales `fr` (défaut) et `en`
- **CSS** : Tailwind 3.4 — palette warm éditorial-bistronomique (vin burgundy + ocre doré + crème)
- **Icônes** : lucide-react
- **Hébergement** : Vercel
- **Domaine** : `table-de-marguerite.ca`

## Scripts

```bash
npm run dev         # serveur dev (port 3000)
npm run build       # build production
npm run start       # serveur production
npm run lint        # ESLint (next/core-web-vitals + jsx-a11y)
npm run typecheck   # tsc --noEmit
```

## Structure

```
site/
├── app/
│   ├── [locale]/                  # routes localisées FR/EN
│   │   ├── layout.tsx             # racine i18n + skip-link + Header/Footer/CookieConsent
│   │   ├── page.tsx               # home (Hero + ChefStory + MenuGallery + Reservation)
│   │   ├── politique-confidentialite/page.tsx
│   │   ├── mentions-legales/page.tsx
│   │   └── not-found.tsx
│   ├── globals.css                # tailwind base + tokens
│   ├── sitemap.ts                 # sitemap multilingue (next/metadata)
│   └── robots.ts                  # robots.txt (next/metadata)
├── components/
│   ├── layout/                    # Header, Footer, CookieConsent (S-201/S-202)
│   └── sections/                  # Hero, ChefStory, MenuGallery, Reservation (S-001..S-004)
├── i18n/                          # routing next-intl + request loader
├── messages/                      # fr.json, en.json
├── public/images/                 # SVG placeholders (à remplacer par photos AVIF/WebP)
├── tailwind.config.ts             # palette + tokens
├── next.config.mjs                # headers sécurité (HSTS, X-Frame-Options, etc.)
├── vercel.json                    # headers + cache (statics 1 an, images 1 jour SWR)
└── middleware.ts                  # redirection locale next-intl
```

## Sections (registre)

Le fichier `clients/table-de-marguerite/section-manifest.json` (à la racine du client, hors `site/`) liste les 8 sections du site avec leur ID, page, namespace i18n et statut. Une modification ciblée se fait via `nexos modify --client-dir clients/table-de-marguerite --section S-NNN`.

## Conformité Loi 25

- Bandeau de consentement opt-in (`components/layout/CookieConsent.tsx`) : aucun cookie analytique avant choix utilisateur.
- Page **politique de confidentialité** complète avec RPP identifié (`info@table-de-marguerite.ca` / `rpp@table-de-marguerite.ca`).
- Page **mentions légales** avec NEQ + adresse + hébergeur Vercel.
- Aucun transfert de données hors Québec autre que Vercel (US, infrastructure) et Resend (UE, courriels) — documentés dans la politique.

## Accessibilité

- Cible WCAG 2.2 AA. Vérification réelle via `pa11y` dans `clients/.../tooling/a11y.json`.
- Contrastes vérifiés ligne 4-9 de `tailwind.config.ts` (≥ 4.5:1 pour tous les rôles texte sur leurs surfaces respectives).
- Skip-link au focus dans `app/[locale]/layout.tsx`.

## Performance

Cible Lighthouse ≥ 95 sur les 4 axes. Budget bundle : tous les chunks < 250 Ko. Mesure réelle dans `clients/.../tooling/lighthouse.json` (perf 99 / a11y 92 / best-practices 96 / SEO 100 au 2026-05-07).

## Déploiement

Pas de déploiement automatique. La décision de `vercel deploy` est **manuelle** et appartient à l'opérateur (cf. NEXOS gate `ph5→deploy` exige μ ≥ 8.5 SOIC).

---
_NEXOS v4.2 scaffold — généré 2026-04-16, dernière revue Phase 5 le 2026-05-07._
