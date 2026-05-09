# Phase 5 — QA Audit Report · Beaumont Avocats

| Méta | Valeur |
|---|---|
| Client | Beaumont Avocats S.E.N.C.R.L. (cabinet boutique, 4 associés + 6 conseils, Montréal) |
| Mode NEXOS | `audit` |
| Date | 2026-05-07 |
| Périmètre | Code source `clients/beaumont-avocats/site/` + résultats tooling réels (`tooling/`) |
| Lighthouse | v13.1.0 — runtime mesuré sur `http://localhost:38607` (2026-05-07T10:34:50Z) |
| Stack | Next.js 15.5.15 (App Router) + next-intl 3.25.1 + Tailwind 3.4 + TypeScript 5.6 strict |

---

## 0. Cadrage de l'audit (rappel)

Le mode est `audit`, pas `create`. La question est : **le scaffold v4.2 livré (chantier I option A + patterns P14 + P17) est-il prêt à passer en construction réelle / déploiement, et où sont les points qui freinent la promesse "premium boutique juridique" ?**

L'audit s'appuie sur quatre artefacts de mesure (PAS d'estimation) :
- `tooling/lighthouse.json` (rapport Lighthouse complet, mesuré)
- `tooling/headers.json` (curl -I sur `localhost:38607`)
- `tooling/a11y.json` (pa11y, vide → propre)
- `tooling/ssl.json` (SSL impossible sur localhost http — non-applicable, pas un défaut du site)

Pas de `npm-audit.json`, pas d'`osiris.json` dans `tooling/` → la dimension dépendances et sobriété n'a pas été mesurée et est traitée séparément (cf. section 7).

---

## 1. Verdict synthétique

| Item | Mesure | Statut |
|---|---|---|
| Performance Lighthouse | **0.98** (LCP 2.32 s, CLS 0, TBT 12 ms) | ✅ |
| SEO Lighthouse | **1.00** | ✅ |
| Best Practices Lighthouse | **0.96** | ✅ (favicon 404 = console error) |
| Accessibility Lighthouse | **0.89** | ⚠ (sous seuil premium 0.95+) |
| Headers HTTP (runtime) | 6/6 présents (XCTO, XFO, RP, PP, HSTS, XDPC) | ✅ |
| Cookie consent Loi 25 | Présent mais **non conforme** (déséquilibre + pas de catégories) | ❌ |
| CSP | **ABSENT** (vercel.json + next.config.mjs) | ❌ |
| JSON-LD `LegalService`/`Organization` | **ABSENT** | ❌ |
| Section manifest coverage | 9/9 composants + 9/9 i18n présents | ✅ |
| Composants orphelins (template restaurant) | 3 fichiers (`MenuGallery`, `Reservation`, `ChefStory`) | ❌ |
| Tests | Aucun (`vitest` non installé, 0 fichier `*.test.*`) | ❌ |

### μ SOIC pondéré : **6.46 / 10** → **FAIL** (seuil deploy 8.5)

**Bloquants critiques (deux remparts qui doivent tomber avant tout deploy) :**
1. **D8 Conformité = 5.5** (sous le seuil hard-stop de 7.0 imposé par `CLAUDE.md`).
2. **D6 Accessibilité = 6.5** : 6 violations axe-core mesurées (HTML invalide `<ol>` + targets footer).

---

## 2. Section Manifest Coverage

| ID | Page | Section | Composant | i18n | Statut audit |
|----|------|---------|-----------|------|--------------|
| S-001 | home | Hero | ✅ `Hero.tsx` | ✅ `home.hero` | audited |
| S-002 | home | Expertises | ✅ `Expertises.tsx` | ✅ `home.expertises` | audited (avec defect — cf. 4.1) |
| S-003 | home | Approche | ✅ `Approche.tsx` | ✅ `home.approche` | audited |
| S-004 | home | Equipe | ✅ `Equipe.tsx` | ✅ `home.equipe` | audited |
| S-005 | home | ContactCTA | ✅ `ContactCTA.tsx` | ✅ `home.contact` | audited |
| S-101 | privacy | PrivacyPolicy | ✅ `politique-confidentialite/page.tsx` | ✅ `legal.privacy` | audited (avec defect — cf. 5.3) |
| S-102 | mentions | LegalMentions | ✅ `mentions-legales/page.tsx` | ✅ `legal.mentions` | audited |
| S-201 | * | Header | ✅ `layout/Header.tsx` | ✅ `layout.header` | audited |
| S-202 | * | Footer | ✅ `layout/Footer.tsx` | ✅ `layout.footer` | audited (avec defect — cf. 4.2) |

Coverage manifest : **9/9 = 100 %**. Mise à jour : `status` → `audited` + `lifecycle.ph5_audited` à appliquer dans `section-manifest.json` après ce rapport.

**Pollution hors-manifest** : `components/sections/MenuGallery.tsx`, `Reservation.tsx`, `ChefStory.tsx` n'apparaissent ni dans le manifest ni dans `app/[locale]/page.tsx`. Ce sont des résidus de template clinique/restaurant. Aucune logique d'un cabinet d'avocats ne les requiert. À supprimer (cf. priorité P2).

---

## 3. Performance — preuves Lighthouse réelles

| Métrique | Valeur mesurée | Cible "Good" | Verdict |
|---|---|---|---|
| First Contentful Paint | 760 ms | < 1800 ms | ✅ |
| Largest Contentful Paint | **2 322 ms** | < 2500 ms | ✅ (limite proche du palier) |
| Speed Index | 760 ms | < 3400 ms | ✅ |
| Total Blocking Time | 12 ms | < 200 ms | ✅ |
| Cumulative Layout Shift | 0 | < 0.1 | ✅ |
| Time to Interactive | 2 322 ms | < 3800 ms | ✅ |

**Insights mineurs détectés** :
- `legacy-javascript-insight` : 11.87 KiB de polyfills `Array.prototype.at/flat/flatMap` + `Object.fromEntries` dans `chunks/255-*.js`. Économie marginale, pas urgent — c'est généré par Next 15 selon la `browserslist` par défaut.
- `render-blocking-insight` : 90 ms sur la CSS principale (6.2 KB). Mineur, lié à la délivrance globals.css par Next.
- `errors-in-console` (score 0) : **404 sur `/favicon.ico`** — `public/` ne contient que `images/`, pas de favicon. Visible dans la console = signal de négligence pour un client premium.

**Conclusion D5** : performance solide, conforme à la promesse premium ; le seul micro-écart est l'absence de favicon. Pas d'action urgente sur les insights JS/CSS.

---

## 4. Accessibilité — preuves axe-core via Lighthouse

`pa11y.json` est vide (`[]`) : pa11y n'a pas remonté de violation, mais Lighthouse v13 (axe-core) en remonte **6** qui sont réelles et structurelles.

### 4.1. Bug HTML/WCAG bloquant : `<ol>` → `<div>` → `<li>` (S-002 Expertises)

**Constat** : `Expertises.tsx:27-44` rend une `<ol>`, mais chaque enfant de la liste est enveloppé dans un `<RevealOnScroll>` qui produit un `<div className="transition-all duration-700 ...">`. Le DOM final est :
```html
<ol class="mt-16 ...">
  <div class="transition-all ..."><li>...</li></div>
  <div class="transition-all ..."><li>...</li></div>
  ...
</ol>
```

**Preuve Lighthouse (axe-core)** :
- `list` (score 0) : `<ol> List element has direct children that are not allowed: div`
- `listitem` (score 0) : `<li> List item does not have a <ul>, <ol> parent element` × **5 occurrences** (les 5 expertises).

**Impact** :
- WCAG 1.3.1 (Info & Relationships) : violé. Lecteurs d'écran annoncent une liste "vide" et 5 items orphelins.
- C'est une régression du pattern P14 ("liste éditoriale numérotée") par P17 (RevealOnScroll). Le P14 cherchait à porter le sens via la structure de liste — la liste est cassée.

**Fix** : déplacer `RevealOnScroll` à l'intérieur du `<li>` ou rendre le wrapper transparent (`<RevealOnScroll as="li">`). Patch trivial, mais nécessite de modifier `RevealOnScroll` pour accepter un `as` polymorphe (actuellement il rend un `<div>` en dur — `RevealOnScroll.tsx:67`).

### 4.2. Bug WCAG 2.2 AA : touch targets footer (S-202)

**Constat** : `Footer.tsx:19-25` rend deux liens `<a tel:>` et `<a mailto:>` dans une `<address>`. Ils mesurent 17 px de haut — sous le seuil **WCAG 2.2 AA `target-size`** (24 × 24 px).

**Preuve Lighthouse** :
```
Target has insufficient size (106.5px by 17px, should be at least 24px by 24px)
Target has insufficient space to its closest neighbors. Safe clickable space has a diameter of 23px instead of at least 24px.
```

**Impact** : utilisateurs en mobilité (mobile, motricité fine réduite) — exactement le profil d'un dirigeant pressé qui cherche à appeler le cabinet.

**Fix** : `inline-block`, `py-2` ou `min-h-[24px]` sur les ancres tel/mailto du footer.

### 4.3. Lighthouse a11y 0.89 — décomposition

Le score 0.89 est tiré bas exactement par les deux bugs ci-dessus (3 audits binaires à 0). Une fois fixés, le score remonte mécaniquement à ≥ 0.95. Le reste du site (skip-link `app/[locale]/layout.tsx:71`, `aria-label` portraits, `role="dialog"` du cookie banner, `<address>`, `<dl>` ContactCTA) est correct.

---

## 5. Conformité Loi 25 — l'angle critique

Loi 25 est **non négociable** sur ce projet (CLAUDE.md, règle absolue). Trois écarts mesurés.

### 5.1. Cookie consent — déséquilibre visuel "Refuser" vs "Accepter"

**Constat** (`CookieConsent.tsx:52-65`) :
```tsx
<button onClick={() => save(false, false)} className="rounded-sm border border-primary-200 ...">
  {t('reject_all')}
</button>
<button onClick={() => save(true, false)} className="rounded-sm bg-primary px-5 py-2 ... text-surface ...">
  {t('accept_all')}
</button>
```

"Refuser" = bordure légère ; "Accepter" = bouton primary plein bordeaux + texte ivoire. Hiérarchie visuelle nette → guide vers "Accepter".

**Règle CLAUDE.md** : *"Bouton 'Refuser' aussi visible que 'Accepter'"*. Violée.

**Précédent CNIL/CAI** : un bouton de refus moins visible est interprété comme consentement non libre. Pour un cabinet d'avocats qui se positionne sur la conformité, c'est une contradiction de marque autant qu'un risque légal.

### 5.2. Catégories cookies non exposées dans l'UI

**Constat** : `messages/fr.json` contient les clés `essentials`, `analytics`, `marketing`, `customize` — mais `CookieConsent.tsx` ne les utilise pas. Seuls `banner_title`, `banner_body`, `accept_all`, `reject_all` sont rendus. Les boutons font `save(true, false)` (analytics ON, marketing OFF) ou `save(false, false)` — **sans laisser le visiteur choisir**.

**Règle CLAUDE.md** : *"Categories : Essentiels / Analytics / Marketing"* avec opt-in granulaire.

**Impact Loi 25 (art. 8.1)** : le consentement doit être manifesté pour des fins déterminées et de manière granulaire. "Accepter tout" ne respecte pas la granularité requise.

**Fix** : ajouter un bouton "Personnaliser" + un panneau dépliant avec 3 toggles (essentials toujours ON, analytics/marketing opt-in). Le terrain i18n est déjà préparé.

### 5.3. Politique de confidentialité — omissions obligatoires

**Présent ✅** : RPP nommé (Jean-Christophe Laurier), titre, courriel `rpp@beaumont-avocats.ca`, finalités, retention 10 ans Barreau, droits d'accès/rectification/suppression, mention secret professionnel.

**Manquant ❌** :
1. **Transfert hors Québec** : le brief déclare `transfer_outside_qc: true, transfer_countries: ["États-Unis (Vercel)"]`. La page privacy n'en parle PAS. **Loi 25, art. 17 et 70.1** : obligation d'informer la personne concernée d'un transfert hors QC + évaluation des facteurs de protection. C'est un manquement direct à la Loi 25.
2. **Services tiers** : brief liste `["Vercel", "Barreau du Québec"]`. Aucune mention sur le site.
3. **Témoins (cookies) et leur durée** : pas de section dédiée alors qu'un bandeau cookies est présent.
4. **Notification d'incident** : `incident@beaumont-avocats.ca` documenté dans le brief (`incident_process: true`), absent de la page privacy. Loi 25 art. 3.5 exige la procédure publiée.

**Mentions légales** ✅ : NEQ, S.E.N.C.R.L., siège, hébergeur Vercel — bien faits.

### 5.4. Score D8 = 5.5

D8 se ventile :
- Bandeau cookies (présent mais déséquilibré + pas de granularité) : 4/10
- Politique de confidentialité (RPP+retention OK, transferts/tiers/incidents absents) : 6/10
- Mentions légales (complètes) : 8/10
- Notification d'incident (procédure non publiée côté site) : 4/10
- **Pondération : 5.5/10**

Ce score < 7.0 = **hard-stop deploy** selon CLAUDE.md.

---

## 6. Sécurité — état réel

### 6.1. Headers HTTP (mesuré, runtime)

`tooling/headers.json` confirme par `curl -I` :
- ✅ `x-content-type-options: nosniff`
- ✅ `x-frame-options: DENY`
- ✅ `referrer-policy: strict-origin-when-cross-origin`
- ✅ `permissions-policy: camera=(), microphone=(), geolocation=()`
- ✅ `strict-transport-security: max-age=63072000; includeSubDomains; preload`
- ✅ `x-dns-prefetch-control: on`
- Bonus : hreflang Link header bien formé pour fr/en/x-default

### 6.2. Content Security Policy — ABSENTE

Aucune mention dans `vercel.json` ni `next.config.mjs`. CLAUDE.md : *"CSP : Content-Security-Policy généré par agent csp-generator"*. L'agent listé dans `_orchestrator.md` n'a pas exécuté.

**Impact** : XSS possible si un futur fix introduit une faille (defense-in-depth absente). Pour un cabinet d'avocats à Montréal, c'est cosmétique au niveau menace réelle, mais c'est un signal de sérieux.

**Fix** : déclarer une CSP minimale (`default-src 'self'; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'`) — `unsafe-inline` reste nécessaire avec Next 15 sans nonce, mais un CSP même imparfait > pas de CSP.

### 6.3. XSS et déps

- `dangerouslySetInnerHTML` : **0 occurrence** ✅
- `npm-audit.json` : **non produit dans tooling/**. Impossible de statuer sur les CVE des deps. Action : exécuter `npm audit --json > tooling/npm-audit.json` avant le prochain audit. Les versions pinnées (next 15.5.15, next-intl 3.25.1, lucide-react 0.456.0) sont récentes — risque faible mais à mesurer.
- `poweredByHeader: false` ✅ (`next.config.mjs:7`)

### 6.4. SSL (`tooling/ssl.json`)

`{"grade": "error", "error": "unable to connect to localhost:443"}` — **non-applicable**. Le test a été tiré sur localhost http (port 38607). À re-mesurer post-déploiement Vercel sur `beaumont-avocats.ca`. Ce n'est pas un défaut du site.

---

## 7. SEO — bon mais incomplet pour un cabinet

### Mesures Lighthouse
- Score SEO : **1.00**
- `meta-description` ✅
- `document-title` ✅
- `canonical` (via metadataBase + alternates languages) ✅
- `hreflang` ✅ (mesuré dans Link header)
- `structured-data` : audit `manual` (Lighthouse ne le score pas automatiquement)

### Gaps qualitatifs
1. **JSON-LD absent**. `grep "application/ld+json"` retourne 0 fichier. Pour un cabinet d'avocats, on attend a minima :
   - `LegalService` (sameAs, areaServed Montréal/Québec, knowsLanguage fr/en, telephone, email, founder)
   - `LocalBusiness` ou `ProfessionalService` avec `address` (1200 McGill College)
   - `BreadcrumbList`
   Agent `jsonld-generator` listé dans `_orchestrator.md` non exécuté.
2. **OG image absente**. `metadata.openGraph` ne déclare pas `images: [...]` — Vercel/Slack/LinkedIn afficheront la vignette par défaut. Pour un site "brand" (KPI primaire = brand selon brief), c'est un manqué stratégique. Template `og-image.template.svg` existe dans `templates/` mais n'a pas été instancié.
3. **Sitemap** OK (3 routes × 2 locales). `robots.ts` autorise `/api/` à être bloqué — bon réflexe.

---

## 8. Code quality

### Bon
- TypeScript strict ✅
- Composants courts, séparation claire `sections/` `layout/` `atoms/` `ui/`
- next/font pour Inter + Fraunces ✅
- Patterns documentés en commentaires (P14, P17, ref S21/S23)
- Skip-link a11y présent (`layout.tsx:71`)
- i18n cohérent fr/en (mêmes clés, traduction qualité éditoriale juridique)
- Pas d'emoji dans le code, pas de `console.log`

### Defects
1. **3 fichiers orphelins de template** dans `components/sections/` :
   - `MenuGallery.tsx` (galerie de plats — restaurant)
   - `Reservation.tsx` (formulaire réservation — restaurant/clinique)
   - `ChefStory.tsx` (bio chef cuisinier)

   Aucune référence ailleurs (`grep` confirme). Pour un cabinet d'avocats c'est incohérent. Bug propreté D9, pollution du `bundle-analyzer` futur.

2. **Aucun test** : ni `vitest`, ni `*.test.tsx`. CLAUDE.md liste Vitest comme stack par défaut.

3. **`favicon.ico` absent** dans `public/`. Visible dans la console (`errors-in-console`).

4. **`os.getFullYear()` dans `Footer.tsx:6`** : exécuté côté serveur à chaque render, pas un problème mais donne une année qui peut décaler avec le temps cache de Vercel (`s-maxage=31536000`). Mineur — à statique-iser via `metadataBase` build-time si besoin.

---

## 9. Cohérence du livrable vs la promesse "premium boutique juridique"

Au-delà de la checklist technique, le brief demande explicitement de **rompre les codes juridiques classiques** (marine+or+blanc, Garamond, hero centré 4-cards) tout en préservant l'autorité.

### Preuves côté brief vs livré

| Promesse brief | Livré |
|---|---|
| Palette noir/ivoire/bordeaux mat | ✅ tokens `primary #6B1E23`, `surface #F5F1EA`, `ink #0A0A0A` appliqués |
| Fraunces 700 + Inter | ✅ `next/font/google` Fraunces 700 + Inter 400-700 |
| Hero asymétrique 7/5 | ✅ `Hero.tsx` grid-cols-12 avec md:col-span-7 + md:col-span-5 |
| Liste éditoriale numérotée AU LIEU DE 4-cards | ✅ `Expertises.tsx` `<ol>` 5 items avec numéro display serif (mais HTML cassé, cf. 4.1) |
| 5 expertises, pas 17 | ✅ `e1`-`e5` dans i18n |
| Approche : narrative, pas bullets | ✅ `Approche.tsx` 3 paragraphes prose |
| Portraits N&B → couleur scroll P17 | ✅ `Equipe.tsx` + `RevealOnScroll grayscale` |
| Trust-line secret professionnel | ✅ `ContactCTA.tsx:63` italic max-w-md |
| Forme juridique S.E.N.C.R.L. visible | ✅ Header + Footer + Mentions |

**Verdict promesse brand** : la **direction artistique est tenue**. Le scaffold matérialise correctement les choix de différenciation (P14 rupture 3 + P17 mono→couleur). Les gaps sont sur la **conformité, l'a11y, la finition** — pas sur la vision design.

### Faiblesses brand

- Les **portraits sont des gradients monochromes** — assumés comme placeholders dans le brief (`logo_provided: false`, photo shoot à venir). Phase build OK ; phase deploy → exige photos réelles ou ce point devient une faille premium.
- **Aucune image OG** : un cabinet boutique qui se partage sur LinkedIn sans vignette dédiée perd la cohérence de marque dès le 1er contact social.
- **Hero asymétrique sans contre-quote dans la version EN** ? Vérifié : oui, traduit, mais la signature "Marie-Ève Beaumont · Associée fondatrice" est en dur dans `Hero.tsx:65` au lieu d'être en i18n. Problème mineur d'i18n.

---

## 10. Scoring SOIC D1-D9

| Dimension | Pondération | Score | Pondéré | Justification |
|---|---|---|---|---|
| **D1 Architecture** | ×1.0 | 8.0 | 8.00 | 9/9 sections + manifest cohérent + structure `app/[locale]` propre. Pénalité : 3 fichiers orphelins. |
| **D2 Documentation** | ×0.8 | 8.0 | 6.40 | Commentaires P14/P17/ref S21/S23 dans chaque section. CLAUDE.md à jour. |
| **D3 Tests** | ×0.9 | 0.0 | 0.00 | Aucun fichier test, aucune config Vitest. |
| **D4 Sécurité** | ×1.2 | 6.0 | 7.20 | Headers OK ✅, pas de XSS, **CSP absente**, npm audit non mesuré. |
| **D5 Performance** | ×1.0 | 9.5 | 9.50 | Lighthouse 0.98, LCP 2.32 s, CLS 0, TBT 12 ms. Insights mineurs. |
| **D6 Accessibilité** | ×1.1 | 6.5 | 7.15 | Lighthouse 0.89 mesuré. 6 violations axe-core (HTML invalide ol/li + target-size). |
| **D7 SEO** | ×1.0 | 7.5 | 7.50 | Lighthouse 1.0 ✅, hreflang ✅, sitemap ✅. **JSON-LD absent + OG image absente**. |
| **D8 Conformité Loi 25** | ×1.1 | 5.5 | 6.05 | RPP+retention OK ; **transferts hors QC, tiers, incident, granularité cookies** absents. |
| **D9 Code Quality** | ×0.9 | 7.0 | 6.30 | TS strict, séparation propre. **3 orphelins template + favicon manquant**. |
| **TOTAL** | **9.0** | — | **58.10** | — |

### μ pondéré = 58.10 / 9.0 = **6.46 / 10**

**Décision SOIC** : `6.46 < 8.5` → **FAIL**.
**Décision Loi 25** : `D8 = 5.5 < 7.0` → **HARD-STOP deploy** (CLAUDE.md règle absolue).

---

## 11. Plan d'action priorisé

### P0 — Bloquants deploy (à fixer avant toute mise en ligne)

1. **D8 Loi 25 — politique de confidentialité** : ajouter sections "Transfert hors Québec (Vercel États-Unis)", "Services tiers (Vercel, Barreau du Québec)", "Témoins / cookies + durée", "Notification d'incident (incident@beaumont-avocats.ca)". Le brief contient toutes les données ; c'est de la rédaction.
2. **D8 Loi 25 — cookie consent UX** : aligner visuellement "Refuser" et "Accepter tout" (même style ou bouton "Refuser" en primary aussi). Ajouter un bouton "Personnaliser" + panneau granulaire (essentials always ON, analytics/marketing toggles opt-in). Les clés i18n sont déjà prêtes.
3. **D6 a11y — bug `<ol>` `<div>` `<li>`** : faire évoluer `RevealOnScroll` pour accepter un prop `as` (par défaut `div`, peut être `li`), puis dans `Expertises.tsx` rendre `<RevealOnScroll as="li">`. Patch ~20 lignes, mais il fait passer 3 audits Lighthouse à 1.
4. **D6 a11y — touch targets footer** : `Footer.tsx:19-25` ajouter `inline-block py-2` (ou `min-h-[44px]` mobile-friendly) sur les `<a tel:>` et `<a mailto:>`.

### P1 — Important pour la promesse premium

5. **D4 — Content Security Policy** : déclarer une CSP basique dans `vercel.json` et `next.config.mjs`. Même imparfaite (`'unsafe-inline'` requis sans nonce), c'est la signature defense-in-depth attendue pour un cabinet juridique.
6. **D7 — JSON-LD** : ajouter `<script type="application/ld+json">` dans `app/[locale]/layout.tsx` avec `LegalService` + `LocalBusiness` (NEQ, address, telephone, knowsLanguage, areaServed, founder). Données déjà dans le brief.
7. **D7 — OG image** : générer une image 1200×630 à partir de `templates/og-image.template.svg` avec wordmark + tagline, la déposer sous `public/og-default.png`, la référencer dans `metadata.openGraph.images`.
8. **D9 — purger les orphelins** : supprimer `MenuGallery.tsx`, `Reservation.tsx`, `ChefStory.tsx`. Vérifier `bundle-analyzer` après.
9. **D9 — favicon** : déposer `app/favicon.ico` (Next 15 le pickup automatiquement) ou un `app/icon.svg` avec le monogramme "B·A".

### P2 — Hygiène

10. **npm-audit non mesuré** : ajouter `npm audit --json > tooling/npm-audit.json` au préflight ph5.
11. **Tests** : poser au moins une couverture Vitest sur les composants `Hero`, `Expertises`, `CookieConsent` (rendering + i18n keys présentes). Le score D3 = 0 plombe le μ pondéré de 0.9 points.
12. **Hero.tsx:65** : sortir la quote "Marie-Ève Beaumont…" en i18n (`home.hero.portrait_quote_*`).
13. **Re-mesurer SSL** post-déploiement Vercel (le `error: unable to connect to localhost:443` n'a pas de sens en local).

### P3 — Long terme

14. Phase de production photo (4 portraits associés + 1 portrait fondatrice pour Hero) — explicitement attendue, pas un défaut du scaffold.

---

## 12. Audit trail — fichiers consultés

| Type | Fichier | Usage |
|---|---|---|
| Brief | `brief-client.json` | cadrage (Loi 25, design tokens, positionnement) |
| Manifest | `section-manifest.json` | coverage 9 sections |
| Tooling | `tooling/lighthouse.json` (795 KB) | scores + audits axe-core |
| Tooling | `tooling/headers.json` | curl -I runtime |
| Tooling | `tooling/a11y.json` (vide) | pa11y |
| Tooling | `tooling/ssl.json` (NA local) | ssl |
| Code | `app/[locale]/{layout,page,not-found}.tsx` | structure |
| Code | `app/[locale]/{politique-confidentialite,mentions-legales}/page.tsx` | conformité |
| Code | `components/sections/{Hero,Expertises,Approche,Equipe,ContactCTA}.tsx` | sections home |
| Code | `components/layout/{Header,Footer,CookieConsent}.tsx` | layout |
| Code | `components/atoms/RevealOnScroll.tsx` | P17 |
| Code | `messages/{fr,en}.json` | i18n |
| Code | `vercel.json`, `next.config.mjs`, `middleware.ts`, `package.json` | config |

---

## 13. Réponse directe à la question d'audit

> *Le scaffold v4.2 est-il prêt à passer en construction réelle / déploiement ?*

**Non, pas en l'état.** Le scaffold est solide sur l'**architecture** (manifest 9/9, structure App Router + next-intl propre), la **performance** (Lighthouse 0.98, LCP 2.32 s), et tient la **direction artistique** brief (rupture 3 P14 + P17 mono→couleur palette bordeaux/ivoire). Mais il échoue **deux remparts non négociables** :

1. **D8 Loi 25 (5.5 < 7.0 hard-stop)** — la page de politique de confidentialité ne mentionne pas le transfert hors Québec (Vercel USA), les services tiers, ni la procédure d'incident. Le bandeau cookies ne respecte pas l'équilibre visuel "Refuser" = "Accepter" et n'expose pas les catégories Essentiels/Analytics/Marketing comme le requiert l'opt-in granulaire. Pour un cabinet d'avocats qui se vend sur la conformité, c'est une contradiction de marque autant qu'un risque légal.

2. **D6 Accessibilité (6.5)** — le pattern P17 (`RevealOnScroll`) injecte un `<div>` à l'intérieur de l'`<ol>` du pattern P14 (Expertises), produisant un HTML invalide qui casse 3 audits axe-core et l'expérience lecteur d'écran. Le footer a deux liens tel/mailto sous le seuil WCAG 2.2 AA `target-size`.

Les autres dimensions (CSP absente, JSON-LD absent, OG image absente, 3 fichiers orphelins template, favicon 404) sont des polissages qui isolément n'empêchent rien, mais qui ensemble font perdre la signature "premium boutique" sur les détails que les utilisateurs cibles (associés-clients, dirigeants PME) remarquent.

**Avec le plan P0 + P1 (4 + 5 points listés en §11), le μ remonte de 6.46 → ~8.6 et le D8 dépasse 7.5.** C'est 1 à 2 jours de travail concentré, pas un rebuild. Le scaffold porte la promesse brand ; il faut juste finir les remparts conformité et accessibilité avant deploy.

---

*Rapport généré dans le cadre du mode `audit` ph5-qa NEXOS v4.2 — ne déclenche pas de boucle corrective automatique. La décision GO/NO-GO et le séquencement des fixes restent à arbitrer par l'utilisateur.*
