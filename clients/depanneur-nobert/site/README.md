# Dépanneur Nobert — Site

Site Next.js 15 (App Router) bilingue FR/EN, généré par NEXOS v4.2 (mode `create`).

## Démarrage

```bash
npm install
cp .env.example .env.local   # remplir les variables kickoff
npm run dev                  # http://localhost:3000
```

## Variables d'environnement (kickoff)

Avant le déploiement Vercel, fournir les valeurs réelles dans `.env.local` :

| Variable | Usage |
|---|---|
| `NEXT_PUBLIC_VILLE` | Ville utilisée dans les H1, meta et Schema |
| `NEXT_PUBLIC_ADRESSE_LIGNE` | Adresse civique (ex. `123 rue Principale`) |
| `NEXT_PUBLIC_CODE_POSTAL` | Code postal |
| `NEXT_PUBLIC_TELEPHONE` | Téléphone affiché + tel: link |
| `NEXT_PUBLIC_NEQ` | NEQ pour mentions légales |
| `NEXT_PUBLIC_ANNEE_FONDATION` | Année dans UVP + storytelling |
| `RESEND_API_KEY` | Clé Resend (envois courriels) |

Sans ces variables, les placeholders `{ville}`, `{telephone}`, etc. apparaissent dans
le rendu — comportement volontaire (Ph3 garde-fou : interdiction d'inventer du contenu).

## Scripts

- `npm run dev` — serveur de développement
- `npm run build` — build production
- `npm run start` — serveur production
- `npm run typecheck` — `tsc --noEmit`
- `npm run lint` — ESLint

## Procédure update circulaire (Nobert-friendly)

1. Ouvrir `data/promotions.json`.
2. Ajouter ou modifier les entrées (titre fr/en, prix, dates `validFrom` et `validUntil`).
3. `git commit && git push` — Vercel revalide la page `/promotions` automatiquement.

## Stack

- Next.js 15 + React 19 + TypeScript strict
- Tailwind CSS 3.4 (palette warm imposée)
- next-intl 3 (FR + EN)
- React Hook Form + Zod (formulaires)
- Resend (envoi courriels server-side)
- Lucide React (iconographie)

## Sécurité / Loi 25

- Headers HTTP : HSTS, X-Frame-Options DENY, CSP-ready, Referrer-Policy strict
- Cookie consent opt-in (3 catégories) avant tout tracking
- Politique de confidentialité + mentions légales conformes Loi 25
- RPP : Nobert Tremblay (`nobert@depanneur-nobert.ca`)
