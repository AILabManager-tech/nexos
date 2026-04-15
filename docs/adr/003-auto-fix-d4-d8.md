# ADR 003 — Auto-fix automatique pour Sécurité (D4) et Loi 25 (D8)

- **Date** : 2026-03
- **Statut** : Accepté
- **Contexte** : Certaines exigences (headers HTTP, cookie consent, pages légales) sont déterministes et répétitives. Leur absence = échec gate. Les faire corriger par un LLM à chaque pipeline = gaspillage de tokens + risque de dérive (une virgule mal placée suffit à casser le JSON de `vercel.json`).

## Décision

Créer `nexos/auto_fixer.py` avec **6 fixes déterministes** :

1. Cookie consent component (`cookie-consent-component.tsx` → `components/`)
2. `npm audit fix` (vulnérabilités non-breaking)
3. Vercel headers (`vercel-headers.template.json` → `vercel.json`)
4. `next.config.mjs` sécurisé (`poweredByHeader=false`, CSP, etc.)
5. Politique de confidentialité (`privacy-policy-template.md` → `app/politique-confidentialite/page.tsx`)
6. Mentions légales (`legal-mentions-template.md` → `app/mentions-legales/page.tsx`)

Exécuté automatiquement **avant `ph5`** et **après échec `ph4`**. Pattern **try-fix-retry** (1 tentative max, pas de boucle infinie).

## Conséquences

- ✅ Loi 25 appliquée systématiquement (0 compromis sur D8).
- ✅ Réduction significative des cycles LLM — économie tokens + temps.
- ✅ Traçabilité : chaque fix append un événement `AUTO_FIX_APPLIED` au `nexos-changelog.json`.
- ❌ Duplication de logique LLM / auto-fixer si les règles Loi 25 évoluent — l'auto_fixer devient source de vérité déterministe.

## Alternatives considérées

- **LLM-only** — rejeté (non déterministe sur exigences légales, risque juridique).
- **Validation-only (fail fast)** — rejeté (pas d'auto-correction = friction utilisateur).

## Références

- `nexos/auto_fixer.py`
- `templates/cookie-consent-component.tsx`, `vercel-headers.template.json`, `privacy-policy-template.md`, `legal-mentions-template.md`
- `soic/evaluate.py::evaluate_d8_legal`
