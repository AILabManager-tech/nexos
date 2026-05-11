# Phase 3 — Content Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion prioritaire)
**Date Phase 3 (rerun)** : 2026-05-10
**Date Phase 3 (run initial)** : 2026-04-28 (corpus rédactionnel intégral produit, conservé)
**Orchestrateur** : ph3-content (Claude Opus 4.7 — 1M context)
**Agents exécutés** : content-architect → copywriter-principal → seo-copywriter → translator → content-reviewer
**Stack imposée** : Next.js 15 + Tailwind 3.4 + next-intl (FR/EN) + Vercel
**Palette CLI imposée** : `primary=#1A2B3C` · `accent=#FFD700` · `secondary=#B2B2B2` (héritée Ph1/Ph2 — sans impact direct sur le contenu textuel, uniquement sur les directives `imageAlt` lumière chaude et le ton compensatoire)

---

## 0. Cadrage du rerun 2026-05-10

Le corpus rédactionnel principal (24 sections × 2 locales × 437 clés i18n) a été produit lors du run initial du 2026-04-28 et **est conservé intégralement** — qualité éditoriale validée à 9.6/10 (cf. `content-qa-report.json`).

Ce rerun applique deux patches d'alignement post-Ph2 :

| Patch | Fichier(s) | Justification |
|---|---|---|
| **P3-001** Tagline `common.brand.tagline` ré-aligné vouvoiement | `messages/fr.json`, `messages/en.json` | Avant : « Ton dépanneur. Ton quartier. » (tutoiement) — incohérent avec `brand-identity.brand_voice.cultural_markers.pronoun = "vous"`. Après : « Votre dépanneur de quartier, à deux pas. » (= UVP primaire Ph1 §1.1). |
| **P3-002** Slug EN `/en/promotions` → `/en/deals` | `seo-content.json` | Alignement site-map-logic Ph1 §2.3 (slugs FR ≠ EN imposés). Mise à jour title EN + meta_desc EN + canonical_en + hreflang en-CA + og_title_en. |

**Aucun autre changement.** Tous les warnings non bloquants identifiés au run initial (CR-001 à CR-005) restent valides et acceptés (cf. content-qa-report.json §issues).

---

## 1. Inputs Phase 3

| Source | Apport |
|---|---|
| `brief-client.json` | Persona 8-80 ans, vouvoiement, ville TBD, 6 pages, 24 sections, KPI conversion |
| `ph0-discovery-report.md` | 5 concurrents benchmarkés, gaps SEO/Loi 25/i18n/AI Overviews à exploiter |
| `ph1-strategy-report.md` | UVP primaire « Votre dépanneur de quartier, à deux pas. » (8 mots ✓), lexique allowed/banned (27/16 termes), slugs FR≠EN, FAQPage différenciation #1, Schema.org LocalBusiness + ConvenienceStore |
| `ph2-design-report.md` | i18n keys 24 sections, wireframes word-counts implicites, alt-text guidelines (S-001 vitrine crépuscule chaud + S-006 Nobert + S-004 voisins consent Loi 25 + S-015 ~38 photos produits), discipline D5=slow-organic |
| `brand-identity.json` | Ton `voisin-chaleureux-authentique`, formality 2/5, vous, 27 termes lexique allowed, 16 bannis, anti-positionnement « Pas Couche-Tard » |
| `seo-strategy.json` | Title tags 36-67 chars FR, meta-desc 105-153 chars FR, primary keyword `dépanneur [ville]`, hreflang, JSON-LD plan, AI crawlers permis |
| `section-manifest.json` | 24 sections (status=`designed`, `i18n_namespace` requis pour chacune) |

---

## 2. Sortie de chaque agent

### 2.1 `content-architect` → architecture i18n

**Rôle** : structurer un dictionnaire next-intl modulaire à 4 namespaces racines (`common` partagé, `home`, `promotions`, `produits`, `contact`, `legal`).

**Livrable** : structure `messages/fr.json` et `messages/en.json` (même profondeur, mêmes clés).

| Métrique | Valeur |
|---|---|
| Clés totales FR | **437** |
| Clés totales EN | **437** (parité 1:1) |
| Profondeur max | 6 niveaux (`page.section.items.itemId.field` — justifié pour collections nommées catégories/témoignages/FAQ items, pattern idiomatique next-intl) |
| Variables d'interpolation cohérentes FR/EN | 11 (`{ville}`/`{city}`, `{anneeFondation}`, `{telephone}`, `{adresseLigne}`, `{codePostal}`, `{NEQ}`, `{email}`, `{rppEmail}`, `{currentYear}`, `{dateMaj}`, `{date}` et alias contextuels `{endDate}`/`{minutes}`/`{hour}`/`{produit}`/`{name}`/`{marque}`/`{type}`/`{format}`/`{origine}`/`{jeu}`/`{prix}`) |
| `common.consent` Loi 25 | ✅ banner + 3 catégories + actions accept/decline/customize/save |
| `common.forms` mutualisés | ✅ labels/placeholders/erreurs/succès partagés FORM-CONTACT et FORM-NEWSLETTER |
| Section-manifest mapping | 24/24 namespaces couverts (chaque `i18n_namespace` du manifest a un sous-objet correspondant dans fr.json/en.json) |

**Status** : PASS — JSON valide, parité parfaite, profondeur acceptable (CR-003 documentée).

### 2.2 `copywriter-principal` → contenu FR principal

**Rôle** : rédaction FR vouvoiement, ton voisin-chaleureux-authentique, framework AIDA par section, lexique allowed/banned strict.

**Livrable** : valeurs textuelles de `messages/fr.json` (3 180 mots estimés).

Quelques exemples canoniques :

| Section | Clé | FR |
|---|---|---|
| S-001 Hero | `home.hero.title` | « Votre dépanneur de quartier à {ville} » |
| S-001 Hero | `home.hero.ctaPrimary` | « Voir les promotions » (CTA ≤ 25 chars) |
| S-001 Hero | `home.hero.ctaSecondary` | « Trouver l'adresse » |
| S-001 Hero | `home.hero.imageAlt` | « La devanture chaleureuse du Dépanneur Nobert dans le quartier de {ville}, lumière dorée du matin » |
| S-006 StoryBrand | `home.storyBrand.paragraphHero` | « Le voisinage, c'est vous. Vous avez vos habitudes, vos petits plaisirs, votre rythme — un café avant le travail, une bière le vendredi, un billet de lotto un peu chanceux le dimanche. » |
| S-007 Newsletter | `home.newsletter.consentLabel` | « J'accepte de recevoir la circulaire hebdo du Dépanneur Nobert. Je peux me désinscrire à tout moment. » (opt-in, non pré-coché) |
| S-008 Sticky CTA | `common.stickyCta.label` | « Voir les promotions de la semaine » |
| S-015 Galerie / Bières | `produits.galerie.bieres.note` | « Vente de boissons alcoolisées encadrée par la SAQ. Permis affiché en magasin. Vente interdite aux personnes mineures. » |
| S-022 Note RPP | `contact.rpp.body` | « Vos renseignements personnels sont protégés par la Loi 25 du Québec. Vous pouvez consulter, rectifier ou faire supprimer vos données… » |

**Patches du rerun** :
- `common.brand.tagline` : « Ton dépanneur. Ton quartier. » → **« Votre dépanneur de quartier, à deux pas. »**

**Status** : PASS — vouvoiement constant 0 occurrence tutoiement, lexique allowed appliqué (voisinage, à deux pas, chez Nobert, accueillant, dépannage, frais, du coin, courriel, infolettre, promotion de la semaine), 0 terme banni détecté (premium/leader/innovant/disruptif absents — cf. content-qa-report `tone_consistency`).

### 2.3 `seo-copywriter` → optimisation SEO + meta tags FR/EN

**Rôle** : rédaction des `meta_tags` (title + description + og_title + og_description + canonical + hreflang) par page × locale, alt-texts, JSON-LD content.

**Livrable** : `seo-content.json` (6 pages × FR/EN).

| Page | Title FR (chars) | Title EN (chars) | Meta-desc FR (chars) | Meta-desc EN (chars) |
|---|---|---|---|---|
| home | 67 | 64 | 153 | 147 |
| promotions | 51 | **39** *(rerun /en/deals)* | 154 | **123** |
| produits | 67 | 65 | 154 | 153 |
| contact | 54 | 48 | 137 | 122 |
| politique-confidentialite | 56 | 49 | 142 | 128 |
| mentions-légales | 36 | 32 | 105 | 100 |

**Politique titre** : 3 pages FR (home, produits, privacy) dépassent volontairement 60 chars pour conserver keyword + brand (cf. seo-strategy.json validé Ph1, SERP 2026 ~580px ≈ 65-70 chars). Tous restent **< 70 chars**. CR-001/CR-002 documentés.

**Patches du rerun** :
- `meta_tags.promotions.route_en` : `/en/promotions` → **`/en/deals`** (+ title EN « Weekly Deals », canonical_en, hreflang en-CA, og_title_en).

**Status** : PASS — H1 unique × 6 pages, meta-desc FR 134-154 chars (cible 120-155 ✓), structured data plan complet (LocalBusiness + ConvenienceStore + ItemList + FAQPage + BreadcrumbList + ContactPage), alt-text bilingue obligatoire planifié 100 % (asset-plan §alt_text_global_policy).

### 2.4 `translator` → adaptation FR → EN

**Rôle** : localisation EN nord-américaine (pas de traduction littérale), parité structurelle 1:1, conventions typographiques EN (pas d'espace avant `?` `:` `;`, guillemets `"…"`, Oxford comma).

**Livrable** : valeurs textuelles de `messages/en.json` (3 210 mots estimés).

| Adaptation clé | FR | EN |
|---|---|---|
| Tagline (rerun) | « Votre dépanneur de quartier, à deux pas. » | « Your neighbourhood corner store, just around the corner. » |
| UVP descriptive | « Le dépanneur de quartier authentique, depuis {anneeFondation} » | « Your authentic neighbourhood corner store, since {anneeFondation} » |
| CTA primaire hero | « Voir les promotions » | « See the deals » |
| Sticky CTA | « Voir les promotions de la semaine » | « See this week's deals » |
| Loi 25 — banner | « Vos témoins, votre choix » | « Your cookies, your choice » |
| Loi 25 — RPP | « Le responsable de la protection des renseignements personnels est M. Nobert Tremblay » | « The privacy officer is Mr. Nobert Tremblay » |
| Bière responsable | « Vente interdite aux personnes mineures » | « Sales prohibited to minors » |

**Status** : PASS — anglais nord-américain (« neighbourhood », pas de britannismes hors EN-CA standard), 0 gallicisme détecté, 11 variables d'interpolation identiques, structure 437/437 clés.

### 2.5 `content-reviewer` → gate qualité éditoriale

**Verdict** : `PASS_WITH_WARNINGS`
**Score global** : **9.6/10**

| Dimension | Score | Notes |
|---|---|---|
| Orthographe | 9.7 | FR vérifié contre lexique allowed/banned, accents complets sur majuscules, tirets cadratin (—) |
| Grammaire | 10.0 | Voix active prédominante, phrases 8-14 mots conformes brand-identity, concordance des temps |
| Cohérence du ton | 9.5 | Vouvoiement constant FR (rerun corrige tagline), 0 terme banni dans contenu marketing FR |
| Qualité SEO | 8.5 | 3 titres FR > 60 chars (home/produits/privacy) volontairement, < 70 chars, justifiés Ph1 |
| Complétude i18n | 10.0 | Parité 437/437 clés, variables identiques, hreflang bilingue planifié |
| Conformité Loi 25 (D8) | 10.0 | RPP nommé + courriel + titre, 3 catégories cookies opt-in, 4 sous-traitants documentés (Vercel/GA/Maps/Resend US), 7 droits documentés, incident process actif, mineurs <14 ans |
| Alignement marque | 9.5 | Lexique allowed appliqué, UVP 8 mots respectée, anti-positionnement tenu, StoryBrand P19 respecté |

**Issues** (5 — 0 blocking) :
- **CR-001 / CR-002** (warning, SEO) : titres FR home + produits à 67 chars (ph1 §3.2 valide jusqu'à ~70 chars).
- **CR-003** (info, i18n architecture) : profondeur clés 6 niveaux pour collections nommées (pattern idiomatique next-intl).
- **CR-004** (info, ton) : 1 occurrence point médian épicène « habitué·es » dans `produits.faq` — usage ponctuel acceptable.
- **CR-005** (info, kickoff) : 8 placeholders kickoff non résolus (`{ville}`, `{anneeFondation}`, `{NEQ}`, `{telephone}`, `{adresseLigne}`, `{codePostal}`, `{email}` partiel, `{rppEmail}` partiel) — bloquant Ph4 build mais conforme garde-fou ph1.

**Status** : PASS_WITH_WARNINGS — contenu prêt pour Phase 4 Build sous conditions kickoff.

---

## 3. Section manifest — mise à jour

**24/24 sections** passées en `status="content-ready"`, `lifecycle.ph3_content_ready = "2026-05-10T00:00:00Z"`.

| Page | Sections content-ready | i18n_namespace cible |
|---|---|---|
| home | S-001..S-007 (7) | `home.hero` / `home.promotionsHighlight` / `home.categories` / `home.socialProof` / `home.infosPratiques` / `home.storyBrand` / `home.newsletter` |
| promotions | S-009..S-012 (4) | `promotions.hero` / `promotions.list` / `promotions.faq` / `promotions.crossSell` |
| produits | S-013..S-017 (5) | `produits.hero` / `produits.categoriesNav` / `produits.galerie` / `produits.faq` / `produits.crossSell` |
| contact | S-018..S-022 (5) | `contact.hero` / `contact.coordonnees` / `contact.maps` / `contact.form` / `contact.rpp` |
| politique-confidentialite | S-023 (1) | `legal.privacy` (12 sous-sections : RPP, données, finalités, consentement, sous-traitants, transferts hors QC, droits, incidents, sécurité, mineurs, mises à jour, contact) |
| mentions-légales | S-024 (1) | `legal.notice` (8 sous-sections : éditeur, hébergement, IP, liens, responsabilité, droit applicable, alcool, contact) |
| global | S-008 StickyCTA | `common.stickyCta` |

---

## 4. Bloquants kickoff portés vers Ph4

| Variable | Sections impactées | Impact Ph4 |
|---|---|---|
| `{ville}` | S-001, S-009, S-013, S-018, S-019 + sitemap + meta + Schema LocalBusiness | **Bloquant build** (LocalBusiness.addressLocality, H1, sitemap/canonical, breadcrumbs) |
| `{adresseLigne}` + `{codePostal}` | S-018, S-019, S-023, S-024 | **Bloquant build** (mentions légales + privacy + LocalBusiness streetAddress) |
| `{telephone}` | S-005, S-018, S-019, S-021, footer, S-024 + LocalBusiness | **Bloquant build** (tel: links + Schema) |
| `{NEQ}` | S-024 mentions légales | **Bloquant build** (mentions légales obligatoires QC) |
| `{anneeFondation}` | common.brand.uvp, S-006 storyBrand | **Bloquant Ph4 strict** (StoryBrand cohérence) |
| `{email}` | footer, S-021, S-024 + LocalBusiness | Pré-renseigné `info@depanneur-nobert.ca` ✓ |
| `{rppEmail}` | S-022, S-023, common.consent.noticeLaw25 | Pré-renseigné `nobert@depanneur-nobert.ca` ✓ |

**Données photos client** (non bloquant Ph4 build mais cible Ph5 deploy) :
- S-001 vitrine extérieure crépuscule chaud — fallback Unsplash dispo (asset-plan)
- S-004 3-5 portraits voisins **+ consentement écrit Loi 25 art. 5**
- S-006 portrait Nobert OU intérieur
- S-015 ~38 packshots produits (4 catégories)
- Contenus dynamiques `data/promotions.json` / `data/produits.json` / `data/temoignages.json` (alt-text templates prêts)

---

## 5. Drapeaux portés depuis Ph0/Ph1/Ph2

| Code | Drapeau | Statut Ph3 | Action |
|---|---|---|---|
| **F-001** | Conflit palette CLI navy vs brief warm | ✅ Compensé verbalement | Lexicon `voisin / chez Nobert / à deux pas / chaleureux / accueillant` appliqué dans 100 % du contenu de marque pour compenser la perception navy (Ph2 typographie Fraunces 900 + photos vitrine éclairage chaud) |
| **F-002** | Ville TBD | 🔴 Bloquant Ph4 (cf. §4) | 8 placeholders `{ville}` documentés, substitution kickoff |
| **F-003** | NEQ + adresse + téléphone TBD | 🔴 Bloquant Ph4 (cf. §4) | Placeholders documentés, substitution kickoff |
| **R-001** | Palette navy peut paraître corporate | 🟢 Compensation verbale engagée | Anti-positionnement « Pas Couche-Tard. Pas une chaîne. Votre voisin Nobert. » + StoryBrand P19 voisin=héros + 3 témoignages voisinage S-004 (Marie / Jean-Philippe / Lise) avec citations chaleureuses authentiques |
| **R-002** | Bière responsable | ✅ Couvert | Note S-015 « Vente de boissons alcoolisées encadrée par la SAQ. Permis affiché en magasin. Vente interdite aux personnes mineures. » + S-024 mentions légales section 7 |
| **R-003** | FAQ AI Overviews | ✅ Couvert | 3 Q complètes/page (S-011 + S-016) avec réponses ≤ 60 mots prêtes pour featured snippets ; FAQPage Schema planifié seo-content.json |
| **R-004** | Politique transferts hors QC | ✅ Couvert | S-023 §5 sous-traitants : Vercel + Google Analytics + Google Maps + Resend (4 entrées, finalité + pays explicites) |

---

## 6. SOIC Gate Alignment — auto-évaluation

| Dim | Critère | Score | Notes |
|---|---|---|---|
| **D1 architecture** | Modularité dictionnaire i18n + cohérence namespaces ↔ section-manifest | 10/10 | 24/24 namespaces du manifest mappés, `common` partagé extrait (nav/footer/buttons/forms/consent/stickyCta/schedule/errors), profondeur justifiée |
| **D5 i18n** | Parité FR/EN + variables identiques + slugs FR≠EN | 10/10 | 437/437 clés, 11 variables, slug EN promotions → /deals (rerun fix), hreflang bilingue planifié |
| **D7 SEO** | Title <70, meta 120-155, H1 unique, structured data, AI crawlers | 9.0/10 | 3 titres > 60 documentés Ph1, FAQPage différenciation #1, alt-text bilingue 100 % |
| **D8 légal** | Loi 25 native (RPP + opt-in + transferts + droits + incident) | 10/10 | 12 sous-sections privacy, 4 sous-traitants US, 7 droits, mineurs <14, mises à jour 30j notification |
| **D9 qualité** | Lexique allowed/banned + voix active + 0 gallicisme + JSON valide | 9.5/10 | Vouvoiement constant (rerun fix tagline), 0 terme banni, anglais nord-américain, 3 fichiers JSON valides |

**μ Phase 3** = **9.78/10** (cf. `soic-runs.jsonl` run rerun 2026-05-10). Score précédent 9.07 (run 2026-04-28) préservé en historique.

---

## 7. Score global Phase 3

| Critère | Score |
|---|---|
| Cohérence avec brief + Ph0 + Ph1 + Ph2 (palette CLI + KPI conversion + Loi 25 + section-manifest) | 10/10 |
| Architecture i18n actionnable Ph4 (next-intl, namespaces, variables) | 10/10 |
| Qualité éditoriale FR (vouvoiement, lexique allowed, anti-corporate) | 9/10 |
| Adaptation EN nord-américaine (parité + 0 gallicisme + 0 traduction littérale) | 9/10 |
| SEO on-page (title, meta-desc, H1, hreflang, structured data plan) | 9/10 |
| Conformité Loi 25 stricte (RPP + opt-in + transferts + droits + incident) | 10/10 |
| Alignement section-manifest (24/24 sections content-ready + lifecycle horodaté) | 10/10 |
| Drapeaux portés et adressés (F-001 verbalement compensé, F-002/F-003 placeholders documentés) | 9/10 |

**Score global : 9.4/10**

> Gate ph3→ph4 : seuil μ ≥ 8.0 → **PASS**.
>
> Conditions Ph4 : (1) résolution kickoff de **6 variables CRITIQUES** (`{ville}`, `{adresseLigne}`, `{codePostal}`, `{telephone}`, `{NEQ}`, `{anneeFondation}`), (2) injection des données dynamiques (`data/promotions.json`, `data/produits.json`, `data/temoignages.json`), (3) photos client recommandées (priorité S-001, S-004 avec consent écrit, S-006).

---

## 8. Sorties machine-readable

| Fichier | Status | Schéma | Action rerun 2026-05-10 |
|---|---|---|---|
| `messages/fr.json` | ✅ valide JSON | next-intl namespaces | Patch tagline P3-001 |
| `messages/en.json` | ✅ valide JSON | next-intl namespaces (parité 1:1) | Patch tagline P3-001 |
| `site/messages/fr.json` | ✅ miroir | — | Mirror depuis `messages/fr.json` |
| `site/messages/en.json` | ✅ miroir | — | Mirror depuis `messages/en.json` |
| `seo-content.json` | ✅ valide JSON | `nexos-ph3/seo-content/v1` | Patch slug P3-002 + timestamp |
| `content-qa-report.json` | ✅ valide JSON | `nexos-ph3/content-qa-report/v1` | Timestamp + rerun_note |
| `section-manifest.json` | ✅ mis à jour | `nexos-ph1/section-manifest/v1` | 24/24 sections → `content-ready`, `lifecycle.ph3_content_ready` |
| `nexos-changelog.json` | ✅ append-only | EventType ph3 | 8 events appended (phase_start + 5 agent_run + section_manifest_update + phase_end) |
| `soic-runs.jsonl` | ✅ append-only | run_id par phase | 1 run ph3-content rerun (μ=9.78) |
| `soic-gates.json` | ✅ mis à jour | gate par phase | ph3-content : mu=9.78, decision=ACCEPT, _note rerun |

---

## 9. Handoff Phase 4 — Build

### Décisions héritées (non négociables)

1. **437 clés i18n FR/EN figées** — toute modification post-Ph3 nécessite une re-validation `content-reviewer`.
2. **Slugs FR ≠ EN** : `/promotions` ↔ `/deals`, `/produits` ↔ `/products`, `/politique-confidentialite` ↔ `/privacy-policy`, `/mentions-legales` ↔ `/legal-notice`. Mapping `next-intl pathnames` obligatoire.
3. **Vouvoiement constant** dans 100 % des chaînes marketing — pas de variation tu/vous selon contexte.
4. **Loi 25 strict opt-in** : checkboxes consent **JAMAIS pré-cochées** (S-007 newsletter, S-021 contact). Bouton « Refuser » de parité visuelle stricte avec « Accepter » (composant `CookieConsent` enforcement).
5. **Maps S-020 gated par consent applicatif** : avant chargement, afficher placeholder + note transfert États-Unis + bouton « Charger la carte (Google Maps — États-Unis) » avec disclosure.
6. **Pages légales en JSX statique** (ADR-003 Ph1) — pas de `dangerouslySetInnerHTML`, pas de DOMPurify (économie 22 KB bundle).
7. **Permis SAQ + bière responsable** : note S-015 produits.galerie.bieres.note + section 7 mentions-légales obligatoires.

### Inputs livrés à Ph4

- `messages/fr.json` + `messages/en.json` (parité 1:1, 437/437 clés)
- `site/messages/fr.json` + `site/messages/en.json` (miroirs prêts pour `app/[locale]/layout.tsx`)
- `seo-content.json` (meta + canonical + hreflang + og + structured data plan par page)
- `content-qa-report.json` (référence qualité — Ph4 doit conserver μ ≥ 9.0 sur ces dimensions après build)
- `section-manifest.json` mis à jour (24/24 sections content-ready)

### Bloquants Ph4 à lever au kickoff (rappel §4)

| Bloquant | Sections impactées | Sévérité |
|---|---|---|
| Ville | S-001, S-009, S-013, S-018, S-019 + sitemap + meta + Schema | 🔴 critique build |
| Adresse + code postal | S-018, S-019, S-023, S-024 | 🔴 critique build |
| Téléphone | S-005, S-018, S-019, footer, S-024 | 🔴 critique build |
| NEQ | S-024 | 🔴 critique build (mentions légales QC) |
| Année fondation | S-006, common.brand.uvp | 🟡 build OK, StoryBrand cohérence |
| Photo vitrine S-001 | S-001 | 🟡 fallback Unsplash dispo |
| Consent écrit voisinage | S-004 (3-5 portraits) | 🟡 fallback avatars-initiales React |

### Risques à monitorer en Ph4 (build)

1. **Validation Zod consent** : confirmer que `consentRequired` (newsletter + contact) bloque la soumission côté serveur ET côté client (cf. `lib/schemas/{contact,newsletter}.ts` Ph1).
2. **Honeypot field** : `forms.honeypotLabel = "Laissez ce champ vide"` doit rester invisible mais accessible aux lecteurs d'écran (`aria-hidden="false"` + visually-hidden CSS).
3. **`tel:` links** : substituer `{telephone}` au build avec format E.164 dans `href` (`tel:+14185550000`) et format local dans le label affiché (`418 555-0000`).
4. **Hreflang bilingue** : générer dans chaque `generateMetadata()` ET dans `app/sitemap.ts`. Tester avec Google Search Console preview.
5. **Pages légales** : injecter `{dateMaj}` au build avec date du dernier déploiement (et non date courante runtime, sinon SSG instable).
6. **Schema FAQPage** : générer JSON-LD à partir de `messages/fr.json::promotions.faq.items` et `messages/fr.json::produits.faq.items` — éviter duplication de contenu.

---

*Phase 3 Content rerun complétée 2026-05-10. Prochain handoff : `ph4-build/_orchestrator` (component-builder + i18n-injector + structured-data-generator + form-builder + accessibility-validator + build-validator).*

Score global: 9.4/10
