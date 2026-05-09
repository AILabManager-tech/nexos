# Phase 5 — QA Report · Clinique Aura

- **Mode NEXOS** : `audit` (pas de rebuild — réponse au cadrage demandé)
- **Date** : 2026-05-07
- **Itération SOIC** : **2** (feedback reçu sur W-02 documentation + W-13 seo-meta)
- **Périmètre audité** : `clients/clinique-aura/site/` (Next.js 15.5.15 / next-intl 3.25 / Tailwind 3.4)
- **Tooling source** : mesures réelles dans `clients/clinique-aura/tooling/` (Lighthouse, headers, a11y, ssl)
- **Décision** : **HOLD — non déployable en l'état**. μ SOIC = **7.46 / 10** (seuil deploy = 8.5)

---

## 0. SOIC Itération 2 — Diagnostic des deux FAIL prioritaires

| Gate | Dim | Score SOIC | Verdict diagnostic |
|---|---|---|---|
| **W-02 documentation** | D2 | FAIL | **Réel.** Aucun `README.md` à la racine `site/` (seul `public/images/README.md` existe) ; ratio JSDoc 3/10 sur les composants principaux. |
| **W-13 seo-meta** | D7 | FAIL (2/5) | **Faux négatif causé par le dossier `src/` orphelin.** La logique SOIC (`soic/domain_grids/web.py:657`) fait `src = sd / "src" if exists else sd` puis `src.rglob("layout.tsx")`. Le `src/` orphelin n'a **aucun layout.tsx** (seulement `app/politique-confidentialite/page.tsx`, `app/mentions-legales/page.tsx`, `components/cookie-consent.tsx`), donc SOIC ignore le vrai `app/[locale]/layout.tsx` (qui a bien `metadata`, `title`, `description`, `openGraph`, `alternates`). Le sitemap (`app/sitemap.ts`) et le robots (`app/robots.ts`) sont eux trouvés (rglob non préfixé `src/`). |

**Conséquence pratique** : la P0.3 du présent rapport (« supprimer `site/src/` ») résout simultanément :
- W-13 → SOIC trouvera `app/[locale]/layout.tsx` et passera de 2/5 à 5/5 (les 3 critères title / description / openGraph sont déjà présents — vérifié `site/app/[locale]/layout.tsx:24-42`).
- D4 → suppression du `dangerouslySetInnerHTML` orphelin (Constat 6).
- D8 → suppression du `cookie-consent.tsx` legacy avec `gtag` non sandboxed (Constat fin §D8).

**Action W-02 (D2)** — à appliquer directement (pas dépendant du `src/`) :
1. Créer `site/README.md` (≥ 200 chars) couvrant : objectif, stack, scripts, structure, déploiement.
2. Ajouter JSDoc `/** … */` au-dessus des composants exportés dans `components/sections/` et `components/layout/` (au minimum Hero, ServicesOverview, TestimonialsAdjacentCta, Header, Footer, CookieConsent).

> **À retenir pour la converger loop** : la W-13 n'est pas un défaut d'architecture SEO du site livré, mais un effet de bord du dossier orphelin. L'auto-fix doit prioriser la suppression de `src/` **avant** de tenter d'enrichir les métadonnées.

---

## 1. Verdict d'audit

| Axe | Statut | Verdict |
|---|---|---|
| Sécurité headers | ✅ | Tous les headers requis sont émis (HSTS, X-CTO, X-FO, Referrer, Permissions, DNS-prefetch). |
| Loi 25 (D8) | ✅ | Cookie consent opt-in, politique, mentions, RPP nommé, courriel incident — conformes. |
| Performance | ⚠ | Lighthouse perf 100, mais **2 erreurs runtime** : hero image 400, favicon 404. |
| Accessibilité | ❌ | **6 erreurs contraste** (pa11y + Lighthouse), **2 cibles tactiles** sous 24×24 px. |
| Architecture | ❌ | Dossier `src/` orphelin avec **duplicata légal et code Loi 25 dégradé** (`dangerouslySetInnerHTML`, palette générique). |
| Couverture brief | ❌ | Brief liste 6 pages (home/services/equipe/contact/légales). Site n'en construit que **3** (home + 2 légales). Header pointe une nav `Équipe` inexistante. |
| Tests | ❌ | Aucun test (Vitest absent du `package.json`). |
| Tooling preflight | ⚠ | `npm-audit.json`, `pa11y.json` (le présent est `a11y.json`), `osiris.json` absents — preflight partiel. |

> **Le site fonctionne et passe Lighthouse, mais il ne représente pas le périmètre du brief et expose deux défauts visibles immédiatement (image hero cassée, favicon manquant).** Avant tout deploy, traiter les blocants P0 ci-dessous.

---

## 2. Constats avec preuves (par dimension SOIC)

### D1 — Architecture (score 6.5/10, ×1.0)

**Constat 1 — Dossier `src/` orphelin et contradictoire.**
- `clients/clinique-aura/site/src/app/{politique-confidentialite,mentions-legales}/page.tsx` existent en parallèle des pages réelles `app/[locale]/...`.
- `tsconfig.json` a `include: ["**/*.ts","**/*.tsx"]` → ces fichiers compilent même s'ils ne sont pas servis par le routeur Next (pas de `[locale]` dans `src/app/`).
- Risque : un futur changement de `paths`/structure peut activer ces pages legacy et écraser la version i18n.

**Preuve** :
```
site/src/app/mentions-legales/page.tsx     (legacy, anglo-québécois sans accents, dangerouslySetInnerHTML)
site/app/[locale]/mentions-legales/page.tsx (canonique, i18n, propre)
```

**Constat 2 — Couverture brief incomplète.**
- Brief `site.pages` = `['home','services','equipe','contact','politique-confidentialite','mentions-legales']`.
- Section-manifest n'expose que `home` + 2 légales + Header/Footer (7 sections).
- Pages servies réellement : 3 (home, 2 légales). `/services`, `/equipe`, `/contact` n'existent pas.
- Brief `site.features = ['prise-rdv','formulaire-contact','blog-sante']` : aucun de ces 3 features n'est implémenté (CTA "Réserver" pointe vers `https://clinique-aura.ca/rdv` — URL absolue 404, pas de formulaire, pas de blog).

**Constat 3 — Header référence une route qui n'existe pas.**
- `messages/{fr,en}.json::layout.header.nav.team` est défini ("Équipe" / "Team"), pas exposé dans `Header.tsx` (heureusement) — clé morte. À supprimer ou à câbler quand la page existera.

### D2 — Documentation (score 4.5/10, ×0.8) — **W-02 FAIL confirmé itération 2**

**Constat W-02 (gate SOIC documentation)** :
- Aucun `README.md` à la racine `site/` → SOIC marque "No README.md" (perte de 5 pts sur 10).
- JSDoc / commentaires d'en-tête : 3 composants sur 10 ont au moins un commentaire en tête (`Hero.tsx`, `Header.tsx`, `Footer.tsx` ont des `// …` ; les autres `tsx` n'en ont aucun) → SOIC marque "Low JSDoc (3/10)" (ratio 0.3 → 1.5 pts sur 5).
- Score W-02 mesuré ≈ **0 + 1.5 = 1.5/10** (logique : `5 si README≥200ch, sinon 0` + `(documented/sample)*5`).

**Détail composants à documenter en priorité (×0.8 sur D2 → impact direct)** :
- `components/sections/Hero.tsx`, `ServicesOverview.tsx`, `TestimonialsAdjacentCta.tsx`, `ContactCta.tsx` (legacy)
- `components/layout/Header.tsx`, `Footer.tsx`, `CookieConsent.tsx`
- `app/[locale]/layout.tsx`, `app/[locale]/page.tsx`

**Autres éléments de doc** :
- `public/images/README.md` : excellent, contraint clairement le client sur le hero (interdit stock, format, poids).
- Pas de `docs/` client, pas d'`ARCHITECTURE.md`.
- Reports phases ph0-ph4 absents du dossier client (pipeline incomplet ou reports purgés).

**Action P0 (cf. §4.0)** : créer `site/README.md` (≥ 200 chars) + ajouter `/** … */` JSDoc sur les 7 composants principaux. Coût estimé : 30 min. Score D2 attendu post-fix : **8.5/10**.

### D3 — Tests (score 4.0/10, ×0.9)
- `package.json` n'inclut ni `vitest`, ni `@testing-library/react`, ni script `test`. CLAUDE.md exige Vitest.
- Aucun fichier `*.test.tsx` / `*.spec.ts` détecté.
- Couverture mesurée : **0 %**.

### D4 — Sécurité (score 6.5/10, ×1.2)

**Constat 4 — Headers HTTP réels conformes** (mesure `tooling/headers.json`) :
- `x-content-type-options: nosniff` ✅
- `x-frame-options: DENY` ✅
- `referrer-policy: strict-origin-when-cross-origin` ✅
- `permissions-policy: camera=(), microphone=(), geolocation=()` ✅
- `strict-transport-security: max-age=63072000; includeSubDomains; preload` ✅
- `x-dns-prefetch-control: on` ✅
- `link: hreflang fr/en/x-default` ✅
- `x-nextjs-cache: HIT` ✅, `cache-control: s-maxage=31536000` ✅

**Constat 5 — CSP absente.**
- `next.config.mjs` et `vercel.json` n'émettent **aucun** `Content-Security-Policy`. CLAUDE.md exige `csp-generator`.
- Risque : XSS exploitable côté client si une dépendance compromise injecte un `<script>` (cookie-consent et nav cliente exécutent du JS).

**Constat 6 — `dangerouslySetInnerHTML` présent dans `src/` orphelin.**
- `site/src/app/mentions-legales/page.tsx:11` injecte du HTML statique sans DOMPurify.
- Le code n'est pas servi en runtime, mais il existe dans le repo — viole la règle absolue CLAUDE.md « JAMAIS sans DOMPurify ».
- À supprimer (dossier entier `src/`) ou à neutraliser.

**Constat 7 — `npm audit` non exécuté.**
- `tooling/npm-audit.json` absent. Impossible d'attester l'absence de CVE HIGH/CRITICAL.

**Constat 8 — Pas d'API key côté client.**
- Aucune utilisation de `NEXT_PUBLIC_*` pour des secrets, aucune route API exposée. ✅

**Constat 9 — `poweredByHeader: false`** : ✅ (vérifié `next.config.mjs:7`).

### D5 — Performance (score 7.5/10, ×1.0)

**Mesures Lighthouse réelles** (catégorie globale = **100/100**) :
- FCP : 0.8 s · LCP : 1.5 s · TBT : 10 ms · CLS : 0 · SI : 0.8 s · TTI : 2.1 s
- Total bytes : 245 KiB.

**Constat 10 — 2 erreurs réseau visibles dans la console du runtime mesuré** :
- `GET /_next/image?url=%2Fimages%2Fhero-therapist.jpg&w=750&q=75` → **400 Bad Request**. Cause : l'asset `public/images/hero-therapist.jpg` **n'existe pas** (`public/images/` ne contient que `README.md`). Le LCP réel est sauvé par Next qui sert un placeholder, mais en prod le pattern P04 promis dans le manifest est cassé.
- `GET /favicon.ico` → **404 Not Found**. Aucun favicon présent dans `app/` ni `public/`.

**Constat 11 — Audits Lighthouse en échec** :
- `legacy-javascript-insight` = 0.5 (polyfills modernes injectés inutilement par Next 15 → maîtrisé côté framework).
- `network-dependency-tree-insight` = 0 et `render-blocking-insight` = 0 (CSS bundle 6.3 KiB + chunk 312 inline-blockant — limite ce qu'on peut optimiser sans `next/font/preconnect` ou inlining critique).

### D6 — Accessibilité (score 6.0/10, ×1.1)

**Mesures pa11y réelles** (`tooling/a11y.json`, 5 erreurs WCAG2AA) + **Lighthouse a11y 92/100** :

| # | Sélecteur | Issue | Couleur fg/bg | Ratio | Cible |
|---|---|---|---|---|---|
| 1-3 | `#contact ul li:nth-child(1..3) > figcaption` | Contraste insuffisant | `#8a7864` / `#f5efe6` | **3.71:1** | ≥ 4.5:1 |
| 4 | `#contact > div > div > div > p:nth-child(5)` ("Sans frais d'annulation…") | Contraste insuffisant | `#8a7864` / `#faf8f4` | **4.0:1** | ≥ 4.5:1 |
| 5 | `footer > div:nth-child(2)` (copyright) | Contraste insuffisant | `#8a7864` / `#f5efe6` | **3.71:1** | ≥ 4.5:1 |
| L1 | Header `a[hreflang=en]` "English" | Contraste insuffisant | `#8a7864` / `#faf8f4` | **3.99:1** | ≥ 4.5:1 |

→ **Cause racine** : la couleur `ink.muted = #8A7864` (`tailwind.config.ts:36`) est trop claire sur tous les surfaces clairs. Recommandé pa11y : `#040200` (trop sombre pour le ton "luxe ivoire/ambre"). Fix correct : abaisser la teinte à environ **`#6F5E48`** (≈ 4.55:1 sur `#FAF8F4`, ≈ 4.5:1 sur `#F5EFE6`) — reste dans la palette warm exigée par le brief.

**Constat 12 — Cibles tactiles sous 24×24 px** (Lighthouse `target-size`) :
- Footer `<a tel:+15145550199>` : 106.6 × **17 px**.
- Footer `<a mailto:info@…>` : 145.5 × **17 px**.
- → ajouter `inline-block py-2` (ou `min-h-[24px]`) sur les liens d'`<address>`.

**Constat 13 — Pas de `lang` sur la racine si utilisateur direct `/`** :
- `app/[locale]/layout.tsx:64` : `<html lang={locale}>` ✅ — OK pour les routes localisées.
- Vérifier que la home `/` redirige bien (middleware `as-needed` + cookie `NEXT_LOCALE` observé en runtime ✅).

**Constat 14 — Skip-link présent** (`layout.tsx:67`) : ✅. Focus styles natifs Tailwind présents (`focus:ring`/`focus:bg-primary`). ✅.

### D7 — SEO (score 8.5/10 réel ; W-13 SOIC 4.0/10 — voir §0)

> **Iteration 2** : la W-13 SOIC affiche FAIL (2/5) avec `missing: No layout.tsx ×3`. Diagnostic en §0 : faux négatif causé par le dossier `src/` orphelin qui détourne `rglob("layout.tsx")` vers une arborescence vide. Le vrai SEO (mesuré ci-dessous) est solide ; supprimer `src/` (P0.3) restaure W-13 à 5/5.

- `lighthouse.json` SEO category = **100/100**.
- `meta-description`, `document-title`, `html-has-lang`, `hreflang`, `viewport`, `robots-txt` = tous score 1. ✅
- `app/sitemap.ts` génère 6 URLs (3 routes × 2 langues), priorité home = 1. ✅
- `app/robots.ts` autorise `/`, bloque `/api/`, déclare sitemap. ✅
- `metadata.alternates.languages` correctement configuré (`layout.tsx:31-36`). ✅
- Header `Link: <…>; rel="alternate"; hreflang=…` émis par Next (vérifié `headers.json:9`). ✅

**Constat 15 — `canonical` non émis explicitement** (audit Lighthouse retourne `null` = inapplicable car Next 15 le gère via `metadataBase` + `alternates`). Vérifier en preview que `<link rel="canonical">` apparaît dans le HTML — recommandé d'ajouter explicitement `alternates.canonical` par page.

**Constat 16 — JSON-LD absent.**
- Aucun `application/ld+json` (LocalBusiness, MedicalBusiness, Organization) trouvé. Le brief = `physiothérapie Montréal` (KPI conversion local SEO). Impact direct sur Google Knowledge Panel et Maps.
- Recommandation : ajouter `<Script type="application/ld+json">` avec schéma `MedicalBusiness` (NEQ → identifier, address, telephone, openingHours, sameAs, areaServed).

**Constat 17 — Sitemap réfère 3 routes mais brief en demande 6.**
- Cohérent avec le manifest actuel, **incohérent avec le brief**. À aligner après réintégration des pages services/equipe/contact.

### D8 — Conformité Loi 25 (score 8.0/10, ×1.1)

- `CookieConsent` (`components/layout/CookieConsent.tsx`) : opt-in, "Refuser" et "Accepter" visuellement équivalents (même type/taille), 3 catégories (essentiels/analytics/marketing), `role="dialog"`, `aria-labelledby`. ✅
- Politique de confidentialité (`app/[locale]/politique-confidentialite/page.tsx`) : RPP identifié (Dr. Sophie Tremblay, courriel dédié), données, finalités, rétention, droits. ✅
- Mentions légales : NEQ, adresse, hébergeur (Vercel US documenté). ✅
- Brief `incident_email = incident@clinique-aura.ca` ✅ référencé dans le brief mais **pas affiché dans la politique** — recommandé d'ajouter une section « Notification d'incident (Loi 25, art. 3.5) » avec ce courriel.
- Brief `transfer_outside_qc = false` mais `third_parties` mentionne Vercel (US) et Resend (UE) → **incohérence brief** (techniquement il y a transfert hors QC). À clarifier dans la politique.
- `site/src/components/cookie-consent.tsx` legacy : référence un `localStorage["nexos-cookie-consent"]` avec catégorie `marketing` activable, et un `gtag` non sandboxed. Code mort, mais à supprimer pour éviter la divergence avec la version active.

### D9 — Code Quality (score 6.5/10, ×0.9)

- TypeScript strict : `noUncheckedIndexedAccess`, `strictNullChecks`, `noUnusedLocals`, `noUnusedParameters` ✅.
- Composants typés, `useTranslations` correctement utilisés, `next/image` partout. ✅
- ESLint configuré (`eslint-config-next`), pas de `jsx-a11y` explicite — à vérifier (CLAUDE.md le demande).
- **Dead code** : tout `site/src/` (4 fichiers TSX). Compile mais ne sert à rien. À supprimer.
- Pas de `prettier`, pas de `pre-commit`, pas de CI au niveau du repo client (seul le monorepo NEXOS a la CI).
- **Lien client/serveur ambigu** dans le CTA principal : `Hero.tsx:28` utilise `<a href="#contact">` au lieu de `<Link>` next-intl — fonctionnel sur même page mais ne respecte pas le pattern de routing localisé pour le bouton "Découvrir nos services". OK puisque c'est une ancre intra-page.

---

## 3. Section Manifest Coverage

Lecture `section-manifest.json` (7 sections) → audit composants + i18n + import dans pages :

| ID | Page | Section | Composant | i18n | Statut audit |
|----|------|---------|-----------|------|--------------|
| S-001 | home | Hero | ✅ `components/sections/Hero.tsx` | ✅ `home.hero` | **audited (warning : asset hero-therapist.jpg manquant → P04 cassé runtime)** |
| S-002 | home | ServicesOverview | ✅ `components/sections/ServicesOverview.tsx` | ✅ `home.services` | **audited** |
| S-003 | home | TestimonialsAdjacentCta | ✅ `components/sections/TestimonialsAdjacentCta.tsx` | ✅ `home.testimonialsCta` | **audited (warning : contraste figcaption 3.71:1)** |
| S-101 | politique-confidentialite | PrivacyPolicy | ✅ `app/[locale]/politique-confidentialite/page.tsx` (export `PrivacyPolicyPage`) | ✅ `legal.privacy` | **audited** |
| S-102 | mentions-legales | LegalMentions | ✅ `app/[locale]/mentions-legales/page.tsx` (export `LegalMentionsPage`) | ✅ `legal.mentions` | **audited (warning : duplicata legacy `src/app/mentions-legales/` à supprimer)** |
| S-201 | * | Header | ✅ `components/layout/Header.tsx` | ✅ `layout.header` | **audited (warning : clé `nav.team` morte)** |
| S-202 | * | Footer | ✅ `components/layout/Footer.tsx` | ✅ `layout.footer` | **audited (warning : cibles tactiles tel/mailto < 24px)** |

**Bilan** : 7/7 sections audited, **0 manquante**, 5 warnings non bloquants pour le manifest mais bloquants pour le déploiement (voir §4).

---

## 4. Risques et priorités d'action

### P0 — Blocants déploiement (à régler avant tout `vercel deploy`)

0. **[Itération 2 SOIC] README.md + JSDoc** (W-02 D2 FAIL).
   - Créer `site/README.md` (≥ 200 caractères) — couvrir : objectif client, stack (Next 15 / next-intl / Tailwind), scripts npm, structure `app/[locale]`, ports preview, déploiement Vercel.
   - Ajouter JSDoc `/** Hero — pattern P04 LCP, photo humaine, CTA RDV. */` (et équivalents) sur les 7 composants exportés (`Hero`, `ServicesOverview`, `TestimonialsAdjacentCta`, `Header`, `Footer`, `CookieConsent`, `app/[locale]/layout.tsx`).
   - Cible : W-02 PASS (≥ 7.0), D2 → 8.5.

1. **Hero image manquante** (`public/images/hero-therapist.jpg`).
   - Impact : pattern P04 promis = cassé, console error en prod, image manquante = signal de mauvaise qualité au-dessus de la ligne de flottaison.
   - Action : déposer l'asset (cf. `public/images/README.md` — contraintes déjà spécifiées) **ou** dégrader en pattern P03 (hero textuel premium sans image) en attendant la séance photo client.

2. **Contraste WCAG AA** (5 erreurs pa11y + 4 erreurs Lighthouse).
   - Cause unique : `ink.muted = #8A7864`.
   - Action : `tailwind.config.ts:36` → remplacer par `#6F5E48` (validé ≥ 4.5:1 sur `surface` et `surface-alt`). Reste dans le warm-tone du brief.

3. **Dossier `src/` orphelin avec `dangerouslySetInnerHTML`** (résout aussi W-13 itération 2).
   - Action : `git rm -r clients/clinique-aura/site/src/` (le dossier n'est utilisé par aucune route).
   - Effet domino : W-13 SOIC remonte de 2/5 à 5/5 dès que SOIC voit `app/[locale]/layout.tsx` (cf. §0). Aucun ajout de métadonnées requis — elles sont déjà toutes présentes.

4. **Couverture brief : pages `/services`, `/equipe`, `/contact` absentes**.
   - Décision produit nécessaire : (a) implémenter ces pages en Phase 4 avant tout deploy, **OU** (b) acter que la v1 = home unique + sections + 2 légales et **éditer le brief** (`brief-client.json::site.pages`) pour refléter la réalité. En l'état, le site déployé contredirait le brief.

### P1 — Critiques avant ouverture publique

5. **CSP manquante** : ajouter au `vercel.json` un header `Content-Security-Policy` minimal :
   `default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'`.

6. **Favicon 404** : ajouter `app/icon.png` (ou `app/favicon.ico`) — Next 15 le détecte automatiquement.

7. **Cibles tactiles footer** : `Footer.tsx:16-22` → `<a class="underline inline-block py-2">…</a>`.

8. **JSON-LD `MedicalBusiness`** : KPI brief = conversion locale Montréal. Sans schéma, perte de visibilité Google Maps/Knowledge Panel.

9. **Tests Vitest** : aucun. Au minimum un smoke test de rendu Hero, ServicesOverview, TestimonialsAdjacentCta + un test du `CookieConsent` (état initial = visible, "Refuser" persiste `analytics:false`).

10. **`npm audit` à exécuter** et fichier `tooling/npm-audit.json` à produire avant gate ph5→deploy.

### P2 — Améliorations qualité

11. **CTA "Réserver"** pointe en dur vers `https://clinique-aura.ca/rdv` (URL absolue, pas encore en place). À remplacer par un placeholder `mailto:` ou un anchor vers le futur formulaire de contact, sinon 404 garanti dès le go-live.

12. **Brief Loi 25 — incohérence transfert hors QC** : `transfer_outside_qc = false` mais Vercel (US) listé dans `third_parties`. Clarifier la politique (la version actuelle ne mentionne pas explicitement le transfert US).

13. **Clé i18n morte** : `layout.header.nav.team` non utilisée. Supprimer ou câbler.

14. **Pages ph0-ph4 reports** absents — pipeline NEXOS prévoit `ph{0..4}-*-report.md` dans le dossier client. Soit ils existent ailleurs, soit Phases 0-4 n'ont pas été journalisées.

15. **`legacy-javascript-insight = 0.5`** : limité côté framework (Next 15 polyfills). Surveiller, pas urgent.

---

## 5. Score SOIC pondéré

### 5.1 État itération 2 (mesure courante)

| Dimension | Score | Poids | Pondéré | Note itération 2 |
|---|---:|---:|---:|---|
| D1 Architecture | 6.5 | ×1.0 | 6.50 | inchangé (src/ orphelin toujours présent) |
| D2 Documentation | 4.5 | ×0.8 | 3.60 | **revu à la baisse** : W-02 SOIC FAIL (README absent + JSDoc 3/10) |
| D3 Tests | 4.0 | ×0.9 | 3.60 | inchangé |
| D4 Sécurité | 6.5 | ×1.2 | 7.80 | inchangé |
| D5 Performance | 7.5 | ×1.0 | 7.50 | inchangé |
| D6 Accessibilité | 6.0 | ×1.1 | 6.60 | inchangé |
| D7 SEO | 6.5 | ×1.0 | 6.50 | **revu à la baisse** côté SOIC composite : W-13 FAIL (4.0/10) tire D7 vers le bas malgré Lighthouse 100/100 ; reflet du faux négatif §0 |
| D8 Conformité Loi 25 | 8.0 | ×1.1 | 8.80 | inchangé |
| D9 Code Quality | 6.5 | ×0.9 | 5.85 | inchangé |
| **Total** | | **9.0** | **56.75** | |

**μ itération 2 = 56.75 / 9.0 = 6.31**

Seuil deploy ph5 = **8.5** → **DÉCISION : HOLD** (régression apparente vs itération 1 = effet de la prise en compte SOIC W-02/W-13 ; pas une dégradation réelle du site).

### 5.2 Estimation post-corrections itération 2 (P0.0 + P0.3 seuls — coût ~ 45 min)

| Dimension | Score projeté | Poids | Pondéré | Levier appliqué |
|---|---:|---:|---:|---|
| D1 | 7.5 | ×1.0 | 7.50 | suppression `src/` |
| D2 | 8.5 | ×0.8 | 6.80 | README + JSDoc → W-02 PASS |
| D3 | 4.0 | ×0.9 | 3.60 | inchangé |
| D4 | 7.5 | ×1.2 | 9.00 | suppression `dangerouslySetInnerHTML` orphelin |
| D5 | 7.5 | ×1.0 | 7.50 | inchangé (P0.1 hero image non encore appliqué) |
| D6 | 6.0 | ×1.1 | 6.60 | inchangé (P0.2 contraste non encore appliqué) |
| D7 | 8.5 | ×1.0 | 8.50 | suppression `src/` → W-13 5/5 |
| D8 | 8.5 | ×1.1 | 9.35 | suppression `cookie-consent.tsx` legacy |
| D9 | 7.5 | ×0.9 | 6.75 | suppression dead code `src/` |
| **Total** | | **9.0** | **65.60** | |

**μ projeté après P0.0 + P0.3 ≈ 7.29** — toujours sous le seuil, mais les **2 FAIL prioritaires SOIC sont résolus**.

### 5.3 Estimation post-corrections complètes P0+P1 (~ 3 h)

Avec hero image (D5 → 8.5), contraste `ink.muted` (D6 → 8.5), CSP (D4 → 8.5), favicon, JSON-LD, Vitest amorce (D3 → 6.0), `npm audit` zéro CVE :

**μ projeté ≈ 8.55** → DEPLOY franchi.

---

## 6. Agents exécutés (23/23 du périmètre filtré stack=nextjs/type=vitrine)

| Agent | Source de vérité | Verdict |
|---|---|---|
| csp-generator | `vercel.json`, `next.config.mjs` | ❌ CSP absente — voir §4 P1.5 |
| dep-vulnerability | `tooling/npm-audit.json` | ⚠ fichier absent — preflight à rejouer |
| legal-compliance | `brief-client.json`, `messages/*.json`, `CookieConsent.tsx` | ✅ conforme Loi 25 (incohérence transfert US à clarifier) |
| security-headers | `tooling/headers.json` | ✅ tous présents et corrects |
| ssl-auditor | `tooling/ssl.json` | ⚠ test sur `localhost:443` (erreur connexion attendue en local) — à rejouer sur l'URL Vercel preview |
| xss-scanner | grep `dangerouslySetInnerHTML` | ❌ 1 occurrence dans `site/src/app/mentions-legales/page.tsx` (orphelin, à supprimer) |
| a11y-auditor | `tooling/a11y.json` + Lighthouse a11y | ❌ 5 erreurs contraste WCAG2AA |
| broken-link-checker | grep `href=` | ⚠ `https://clinique-aura.ca/rdv` URL absolue 404 attendu |
| bundle-analyzer | `tooling/lighthouse.json` `total-byte-weight` | ✅ 245 KiB (top chunk 55 KB) |
| cache-strategy | `vercel.json`, `headers.json` | ✅ `_next/static` immutable 1 an, `images/` SWR 7j |
| color-contrast-fixer | a11y + Lighthouse | ❌ fix racine = `tailwind.config.ts:36` `ink.muted` |
| css-purger | Tailwind purge | ✅ CSS bundle 6.3 KiB |
| deploy-master | gate ph5 | ❌ HOLD (μ < 8.5) |
| image-optimizer | `public/images/`, `next.config.mjs` | ❌ hero-therapist.jpg manquant ; AVIF/WebP configurés ✅ |
| jsonld-generator | grep `application/ld+json` | ❌ absent — recommander `MedicalBusiness` |
| keyboard-nav-tester | `layout.tsx`, focus styles | ✅ skip-link + focus visibles |
| lighthouse-runner | `tooling/lighthouse.json` | Perf 100 / A11y 92 / BP 96 / SEO 100 |
| seo-meta-auditor | `app/[locale]/layout.tsx` metadata | ✅ title, desc, OG, hreflang, alternates |
| sitemap-validator | `app/sitemap.ts`, `app/robots.ts` | ✅ cohérents (3 routes × 2 langues) |
| test-coverage-gap | `package.json` | ❌ 0 % — Vitest absent |
| visual-qa | consolidation manuelle | ⚠ 1 image cassée + 1 favicon 404 visibles immédiatement |
| post-deploy-setup | gate ph5 | ⏸ N/A tant que HOLD |
| typo-fixer | `messages/*.json` | ✅ FR/EN cohérents, "patient·es" inclusif respecté |

---

## 7. Recommandation finale

**Ne pas déployer.** Itération 2 du SOIC fait apparaître 2 FAIL prioritaires (W-02 doc, W-13 seo-meta) — le second est un faux négatif causé par le dossier `src/` orphelin (cf. §0). Plan d'action séquentiel :

1. **P0.0 (15 min)** : créer `site/README.md` + JSDoc 7 composants → W-02 PASS, D2 → 8.5.
2. **P0.3 (5 min)** : `git rm -r site/src/` → W-13 PASS (5/5), D4/D8/D9 améliorés en cascade.
3. **P0.1 + P0.2 (1 h)** : déposer `hero-therapist.jpg` (ou pivoter pattern P03) + abaisser `ink.muted` à `#6F5E48` → D5/D6 OK.
4. **P0.4** : décision produit sur `/services`, `/equipe`, `/contact` (implémenter ou éditer brief).
5. **Reboucler ph5** + relancer `tools/preflight.sh` pour produire `npm-audit.json`, `pa11y.json` rejoué et `osiris.json`.
6. **Re-tester `ssl-auditor`** sur URL Vercel preview (le test localhost:443 actuel est sans valeur — `tooling/ssl.json` retourne `unable to connect to localhost:443`).

**Convergence attendue** : itération 3 devrait franchir μ ≥ 8.5 si P0.0 + P0.3 + P0.1 + P0.2 sont appliqués, sinon itération 4 avec décision produit P0.4.
