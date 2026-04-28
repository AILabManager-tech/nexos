# Phase 3 — Content Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion absolu)
**Date Phase 3** : 2026-04-28
**Orchestrateur** : ph3-content
**Agents exécutés** : copywriter-principal → seo-copywriter → content-architect → translator → content-reviewer
**Stack imposée** : Next.js 15 + Tailwind 3.4 + next-intl (FR/EN) + Vercel
**Palette imposée** : warm — `#8B4513` / `#A0522D` / `#FFD700` / `#FFF8E7` / `#FFFFFF` / `#2A1810` / `#6B4F3C` / `#D4C5A9`

---

## Cadrage métier (rappel mode `create`)

| Axe | Décision opérationnelle Phase 3 |
|---|---|
| **KPI primaire** | Conversion → tout le contenu pousse vers « Voir les promotions de la semaine » (S-001 hero + S-008 sticky + cross-sell S-017) |
| **Voix imposée** | `convivial-authentique`, vouvoiement universel, phrases 8-14 mots, lexique allowed/banned brand-identity §1.2 strictement appliqué |
| **Audience** | Voisin fidèle (primaire) + Visiteur ponctuel + Résident senior — lisibilité D3=heavy, audience 20-80 ans |
| **Anti-cible textuelle** | Aucun mot du lexique banni : `premium`, `leader du marché`, `innovant`, `on-the-go`, `convenience store` (FR), `client final`, `consommateur`, `engagement`, `synergies`, etc. — tous ABSENTS du contenu marketing FR |
| **Bilinguisme** | FR primaire (>90% trafic), EN secondaire (touristes/anglophones) — parité 516/516 clés i18n |
| **Loi 25** | RPP nommé Nobert Tremblay, 4 sous-traitants US documentés (Vercel, Google Analytics, Google Maps, Resend), opt-in 3 catégories cookies, 7 droits couverts, incident process actif |

**Décision Phase 3 majeure** : la rédaction **conserve les 6 variables kickoff** (`{ville}`, `{anneeFondation}`, `{telephone}`, `{adresseLigne}`, `{codePostal}`, `{NEQ}`) en **placeholders d'interpolation next-intl** plutôt qu'injecter du contenu synthétique. Conforme garde-fou ph1 §5bis.5 (« si une donnée manque, signaler la dépendance plutôt que d'inventer »).

---

## 1. Production éditoriale FR (copywriter-principal → `messages/fr.json`)

### 1.1 Couverture

| Page | Sections rédigées | Mots FR estimés | Conformité voix |
|---|---|---|---|
| `/` Accueil | S-001 → S-007 (7) | ~720 | ✅ vouvoiement, lexique allowed appliqué |
| Global StickyCTA + cookie banner + nav + footer | S-008 + common.* (6 namespaces) | ~280 | ✅ |
| `/promotions` | S-009 → S-012 (4) | ~380 | ✅ |
| `/produits` | S-013 → S-017 (5) | ~520 | ✅ |
| `/contact` | S-018 → S-022 (5) | ~340 | ✅ |
| `/politique-confidentialite` | S-023 (1) | ~620 | ✅ Loi 25 templated |
| `/mentions-legales` | S-024 (1) | ~320 | ✅ Loi 25 templated |
| **Total FR** | **24/24 sections** | **~3 180 mots** | ✅ |

### 1.2 Application stricte du lexique brand-identity

**Lexique allowed déployé** (occurrences sur le contenu FR rédigé) :

| Terme | Occurrences | Sections clés |
|---|---|---|
| voisinage / voisin | 14 | S-004, S-006, common.footer, home.socialProof |
| à deux pas | 4 | S-001, common.brand.promise, S-005 |
| chaleureux / accueillant | 3 | meta home, S-001 (alt), S-009 |
| quartier | 11 | S-001, S-006, common.brand.tagline |
| service personnel | 2 | S-001, S-006 |
| passez voir / passer voir | 2 | meta home, S-002 |
| circulaire | 4 | S-002, S-007, common.consent |
| depuis [année] | 3 | S-001 trustNote, common.brand.uvp, S-006 |
| fidélité / habitude | 4 | S-006, common.brand.tagline (subtext) |

**Lexique banni** : aucun terme banni détecté dans le contenu marketing FR (cf. `content-qa-report.json` §scores.tone_consistency = 9.5).

### 1.3 Application AIDA par section critique

| Section | Attention | Intérêt | Désir | Action |
|---|---|---|---|---|
| **S-001 Hero** | H1 « Votre dépanneur de quartier à {ville} » + photo vitrine warm | Subtitle « Promotions hebdo, bières, lotto, snacks » | Trust note « Ouvert pour vous, du lundi au dimanche » | CTA primary « Voir les promotions » + secondary « Trouver l'adresse » |
| **S-002 PromotionsHighlight** | Eyebrow « Cette semaine » + badge accent | Top 3 promos cards avec dates | Mention « mises à jour chaque vendredi par Nobert » | CTA « Voir toutes les promotions » |
| **S-004 SocialProofVoisinage** | « Pas des avis. Des voisins. » (rupture sémantique) | 3 témoignages prénom + rôle voisinage + citation 1 phrase | Identification 30-65 / 60-80 / parents | CTA reminder adjacent « Profitez des promotions » |
| **S-006 StoryBrand** | « Vous, le quartier, et un dépanneur qui vous connaît » | 3 paragraphes : vous/Nobert/promesse (cadre P19) | « Pas de chaîne, pas de cartes de fidélité, pas de slogans » | CTA « Voir les promotions de la semaine » |
| **S-007 Newsletter** | « Pas un spam, juste les bons coups » | Subtitle « courriel court, le vendredi matin » | « désinscription en un clic » | CTA « M'inscrire à la circulaire » |

---

## 2. Optimisation SEO (seo-copywriter → `seo-content.json`)

### 2.1 Meta tags par page (longueurs validées)

| Page | Title FR (chars) | Meta desc FR (chars) | H1 FR | Schema |
|---|---|---|---|---|
| `/` | 67 ⚠️ | 153 ✅ | « Votre dépanneur de quartier à {ville} » | LocalBusiness, ConvenienceStore, WebSite, Organization |
| `/promotions` | 51 ✅ | 154 ✅ | « Les promotions de la semaine » | LocalBusiness, ItemList, Offer, BreadcrumbList |
| `/produits` | 67 ⚠️ | 154 ✅ | « Nos produits, pour tout votre quotidien » | LocalBusiness, ItemList, Product, BreadcrumbList |
| `/contact` | 54 ✅ | 137 ✅ | « Nous joindre, nous trouver » | LocalBusiness, ConvenienceStore, PostalAddress, OpeningHoursSpecification, ContactPoint, BreadcrumbList |
| `/politique-confidentialite` | 56 ✅ | 138 ✅ | « Politique de confidentialité » | WebPage, BreadcrumbList |
| `/mentions-legales` | 35 ✅ | 134 ✅ | « Mentions légales » | WebPage, BreadcrumbList |

⚠️ 2 titres FR à 67 chars dépassent le seuil 60 chars de la fiche `seo-copywriter` mais restent dans le contrat 70 chars de `seo-strategy.json` (Ph1) — Google rend ~580 px ≈ 65-70 chars en 2026. Décision : conserver les valeurs Ph1 pour préserver keyword + brand. Documenté en CR-001 et CR-002 du QA.

### 2.2 Densité de mots-clés (page principale)

| Page | Keyword primaire | Occurrences | Mots / page | Densité | Statut |
|---|---|---|---|---|---|
| `/` | `dépanneur {ville}` | 6 | 480 | 1.25 % | optimal |
| `/promotions` | `promotions dépanneur {ville}` | 5 | 380 | 1.31 % | optimal |
| `/produits` | `bière dépanneur {ville}` | 4 | 520 | 0.77 % | optimal (LSI compense : microbrasserie, lotto, snacks, essentiels) |
| `/contact` | `dépanneur {ville} adresse` | 5 | 320 | 1.56 % | optimal |

Aucun keyword stuffing. Variations LSI naturelles : `bière du coin`, `microbrasserie québécoise`, `lotto québec`, `snack froid chaud`, `circulaire`, `voisinage`.

### 2.3 Alt-text policy

- **100 % des images informatives** ont un alt-text bilingue planifié (cf. `seo-content.json §alt_texts` — 12 entrées dont 5 templates pour collections).
- **Format produits catalogue (S-015)** : templates `{marque} {type}, format {format}, microbrasserie {origine}` en FR / EN — résolus build-time par injection `data/produits.json`.
- **Format témoignages (S-004)** : template `Portrait de {name}, voisin et client fidèle du Dépanneur Nobert` — résolu après collecte des consentements écrits Loi 25 art. 5.
- **Filename convention** : `kebab-case` sans accents (ex: `biere-ipa-la-souche-750ml.webp`).
- **Décoratives** : `alt=""` (pas alt absent).

### 2.4 FAQ Schema-ready

6 paires Q/A bilingues prêtes pour `FAQPage` JSON-LD :
- `/promotions` : durée, réservation, livraison
- `/produits` : commandes spéciales, commandes téléphone, permis SAQ

Boost AI Overviews + Google « People also ask » sur les requêtes voisinage type « Quel dépanneur livre à {ville} ? » → réponse cohérente extractible.

---

## 3. Architecture i18n (content-architect → `messages/fr.json` structuré)

### 3.1 Namespaces principaux

```
common.brand          (5 clés)   ← name, shortName, tagline, uvp, promise
common.nav            (9 clés)   ← navigation FR/EN + ARIA
common.footer         (12 clés)  ← 3 colonnes + RPP + copyright
common.buttons        (12 clés)  ← CTA réutilisables
common.forms          (17 clés)  ← labels + validations + states
common.consent        (16 clés)  ← cookie banner + 3 catégories
common.stickyCta      (3 clés)   ← S-008
common.languageSwitcher (3 clés)
common.schedule       (15 clés)  ← jours + états dynamiques
common.errors         (6 clés)   ← 404 + erreur générique
home.*                (7 sections × ~10 clés)
promotions.*          (4 sections)
produits.*            (5 sections)
contact.*             (5 sections)
legal.privacy.*       (12 sections + 5 dataItems + 4 thirdPartiesItems + 7 rightsItems)
legal.notice.*        (8 sections)
```

**Total** : 516 clés FR (parfaitement reflétées en EN).

### 3.2 Conformité content-architect

| Critère | Statut | Note |
|---|---|---|
| JSON syntaxiquement valide (`jq .`) | ✅ | FR + EN + SEO content |
| Toutes les clés en camelCase | ✅ | 516/516 FR, 516/516 EN |
| Profondeur max | ⚠️ 6 | Dépasse seuil 4 du fichier agent — choix architectural pour collections nommées (catégories, témoignages, FAQ items, dataItems Loi 25). Justifié CR-003 dans QA. |
| Namespace `common` complet | ✅ | nav, footer, buttons, forms, consent, stickyCta, languageSwitcher, schedule, errors, brand |
| `meta` SEO par page | ✅ | home, promotions, produits, contact, legal.privacy, legal.notice (6/6) |
| Variables `{name}` simples | ✅ | Aucune double accolade détectée |
| Aucune valeur > 500 chars | ✅ | Plus longue valeur = 461 chars (legal.privacy.intro) |
| Zero duplication | ✅ | Strings communes extraites dans `common.*` (ex: succès formulaire identique form/contact/newsletter → 3 instances justifiées car contexte distinct, mais bouton « Envoyer » centralisé) |
| Variables d'interpolation cohérentes FR↔EN | ✅ | 516/516 placeholders identiques |

### 3.3 Mapping i18n_namespace ↔ section-manifest

24 sections du `section-manifest.json` ont leur namespace i18n complet :

| Section | i18n_namespace manifest | Clés présentes |
|---|---|---|
| S-001 Hero | `home.hero` | ✅ 12 clés (eyebrow, title, subtitle, ctaPrimary, ctaSecondary, *Aria, imageAlt, trustNote) |
| S-002 PromotionsHighlight | `home.promotionsHighlight` | ✅ 9 clés |
| S-003 CategoriesProduits | `home.categories` | ✅ items × 4 |
| S-004 SocialProofVoisinage | `home.socialProof` | ✅ items × 3 + consentNote |
| S-005 InfosPratiques | `home.infosPratiques` | ✅ |
| S-006 StoryBrand | `home.storyBrand` | ✅ 3 paragraphes P19 |
| S-007 NewsletterCTA | `home.newsletter` | ✅ |
| S-008 StickyCTAGlobal | `common.stickyCta` | ✅ |
| S-009 → S-012 promotions | `promotions.{hero,list,faq,crossSell}` | ✅ 4/4 |
| S-013 → S-017 produits | `produits.{hero,categoriesNav,galerie,faq,crossSell}` | ✅ 5/5 |
| S-018 → S-022 contact | `contact.{hero,coordonnees,maps,form,rpp}` | ✅ 5/5 |
| S-023 PolitiqueContent | `legal.privacy` | ✅ 12 sections + dataItems + thirdParties + rights |
| S-024 MentionsContent | `legal.notice` | ✅ 8 sections |

**Statut sections** : 24/24 passées de `designed` → `content-ready` avec `lifecycle.ph3_content_ready = 2026-04-28T00:00:00Z`.

---

## 4. Localisation FR → EN (translator → `messages/en.json`)

### 4.1 Approche

- **Localisation, pas traduction littérale** : adaptation culturelle nord-américaine (cf. fiche translator §regles-de-traduction).
- **Tagline 3-mots adaptée** : `Ton dépanneur. Ton quartier.` → `Your store. Your block.` (préserve la rythmique et l'ancrage urbain anglophone).
- **Termes Loi 25 conservés** : `Quebec's Law 25`, `Privacy Officer` (titre RPP), `Régie des alcools, des courses et des jeux` non traduit (entité gouvernementale).
- **Anglicismes québécois** : « courriel » → « email » ; « clavardage » → non utilisé (pas de chat). « lotto » conservé (équivalent EN courant).
- **Anglais nord-américain** : `colour` → `color`, `neighbourhood` conservé (acceptable CA-EN, et plus chaleureux que `neighborhood`).
- **Oxford comma** : appliqué dans les listes (`beer, snacks, and lotto`).

### 4.2 Vérifications EN

| Critère | Statut |
|---|---|
| Toutes les clés FR présentes en EN | ✅ 516/516 |
| Aucune clé supplémentaire EN | ✅ 0 |
| Variables d'interpolation identiques | ✅ |
| Anglais nord-américain (CA-EN) | ✅ |
| Pas de gallicisme détecté | ✅ |
| Termes Loi 25 traduits correctement | ✅ |
| Title tags EN < 70 chars | ✅ 32-65 chars |
| Meta desc EN 115-153 chars | ✅ |
| Tonalité préservée (vouvoiement → professional you) | ✅ |

### 4.3 Adaptation des CTAs

| FR | EN | Rationale |
|---|---|---|
| Voir les promotions | View promotions | Direct, action-oriented |
| Voir les promotions de la semaine | See this week's promotions | Calque rythme FR, idiome EN |
| Trouver l'adresse | Find the address | OK |
| Charger la carte (Google Maps — États-Unis) | Load the map (Google Maps — United States) | Préserve la transparence Loi 25 |
| M'inscrire à la circulaire | Sign me up for the flyer | « Flyer » plutôt que « weekly newsletter » pour rester proche de l'esprit « circulaire de quartier » |
| Appeler | Call us | Plus engageant en EN |
| Aller au contenu principal (skip-link) | Skip to main content | Standard a11y |

---

## 5. Verdict éditorial (content-reviewer → `content-qa-report.json`)

### 5.1 Scores SOIC

| Dimension | Score / 10 | Justification |
|---|---|---|
| **Orthography** | 9.7 | Accents complets sur majuscules, tirets cadratin —, typographie québécoise respectée, 0 faute détectée |
| **Grammar** | 10.0 | Voix active prédominante, accord parfait, concordance des temps |
| **Tone consistency** | 9.5 | Vouvoiement constant, lexique banni absent, registre `convivial-authentique` tenu sur 24/24 sections |
| **SEO quality** | 8.5 | 3 warnings titres > 60 chars (mais < 70), meta desc dans la fenêtre, H1 unique × 6, densité 0.77-1.56 % (optimal) |
| **i18n completeness** | 10.0 | Parité 516/516, variables identiques |
| **Legal compliance** | 10.0 | Loi 25 native sur tous les axes (RPP, opt-in, transferts, droits, incident, mineurs) |
| **Brand alignment** | 9.5 | Lexique allowed appliqué, UVP 7-mots, tagline 3-mots, anti-positionnement tenu, P19 respecté |

### 5.2 Score global Phase 3

**Overall score : 9.6 / 10** — `verdict: PASS_WITH_WARNINGS`.

### 5.3 Issues

| ID | Sévérité | Type | Localisation | Décision |
|---|---|---|---|---|
| CR-001 | warning | seo_quality | meta_tags.home.title_fr (67 chars) | Conserver — alignement seo-strategy.json Ph1 |
| CR-002 | warning | seo_quality | meta_tags.produits.title_fr (67 chars) | Conserver — idem |
| CR-003 | info | i18n_architecture | Profondeur clés > 4 (collections nommées) | Conserver — pattern next-intl idiomatique |
| CR-004 | info | tone_consistency | « habitué·es » (1 occurrence) | Conserver — épicène ponctuel autorisé brand-identity §cultural_markers |
| CR-005 | info | kickoff_dependency | Variables {ville}, etc. | Résolution kickoff Ph4 — conforme garde-fou ph1 §5bis.5 |

**Aucun blocking issue.**

---

## 6. Risques & dépendances pour Phase 4

### 6.1 Variables encore à fixer (BLOQUANT déploiement Ph5, pas Ph4 build)

| Variable | Impact si absente | Owner | Priorité |
|---|---|---|---|
| 🟠 `{ville}` | Tous les meta tags, H1, H2, alt-text, Schema LocalBusiness | Client (kickoff) | **CRITIQUE** |
| 🟠 `{adresseLigne}` + `{codePostal}` | Schema PostalAddress, common.footer, S-005, S-018, S-019, mentions légales | Client | **CRITIQUE** |
| 🟠 `{telephone}` | tel: link, common.footer, S-018 hero, FAQ produits, ContactPoint Schema | Client | **CRITIQUE** |
| 🟠 `{horaires}` (data) | Table S-019, Schema OpeningHoursSpecification, common.schedule | Client | **CRITIQUE** |
| 🟠 `{NEQ}` | Mentions légales S-024 | Client | **CRITIQUE** |
| 🟠 `{anneeFondation}` | UVP, S-006 paragraphGuide, meta produits | Client | **HAUTE** |
| 🟡 Photos vitrine, intérieur, propriétaire | Alt-text templated, P13 anti-polish strict | Client | **HAUTE** |
| 🟡 3-5 témoignages voisinage signés (Loi 25 art. 5) | items voisin1/2/3 actuels = template — à remplacer par les vrais avec consentement écrit | Client | **CRITIQUE** (P02) |
| 🟡 Catalogue produits (~30) | data/produits.json | Client + manufacturers | **CRITIQUE** (P20) |
| 🟡 Promos hebdo (~6-10) | data/promotions.json (ISR weekly) | Client | **CRITIQUE** (KPI) |
| 🟡 Logo wordmark Fraunces (Logo.tsx) | common.brand.name + favicon | Décision Ph4 (déjà ADR Ph2) | HAUTE |

### 6.2 Risques SOIC Ph3 traités

| Risque amont | Traitement Ph3 |
|---|---|
| **D2 Accessibilité** (alt-text 30 produits) | Templates bilingues prêts (`{marque} {type}, format {format}, microbrasserie {origine}`) — résolution data-driven Ph4 |
| **D7 SEO** (NAP cohérence GMB) | Schema LocalBusiness/ConvenienceStore/PostalAddress/OpeningHoursSpecification/ContactPoint planifiés ; NAP texte aligné via variables uniques `{adresseLigne}`, `{telephone}`, `{horaires}` (single source of truth) |
| **D8 Loi 25** (transferts US documentés) | 4 sous-traitants explicités (Vercel, Google Analytics, Google Maps, Resend) avec service + pays + finalité — politique-confidentialite §5 thirdPartiesItems |
| **D8 Loi 25** (témoignages photos) | `home.socialProof.consentNote` ajouté : « Témoignages publiés avec consentement écrit, conformément à la Loi 25 » + ajout dans content-qa-report image_assets_pending |
| **D9 Confidence sectorielle SEC-03** | Lexique allowed/banned aligne sur registre commerce de proximité (et non gastro Restauration) — pas de risque éditorial résiduel |

### 6.3 Risques restants pour Phase 4

| Risque | Owner | Action Ph4 |
|---|---|---|
| Résolution interpolation `{variable}` | dev | Pipeline Ph4 doit substituer les placeholders au build (env vars + JSON config client) ou laisser next-intl gérer en runtime |
| Charge contenu Loi 25 (≥ 700 mots /privacy) | dev | Verify rendering avec `prose max-w-3xl` + line-height 1.7 (cf. responsive-strategy §3.5) |
| FAQ Schema implementation | dev | Wire FAQPage JSON-LD avec items de `seo-content.json §faq_items` |
| Alt-text dynamic resolution | dev | Helper `resolveAltText(template, data)` dans `lib/altText.ts` pour produits/promos/témoignages |

---

## 7. Score Phase 3 par dimension SOIC

| Dimension | Score / 10 | Justification |
|---|---|---|
| **D1 Architecture** (i18n modulaire, namespaces cohérents) | 9 | 516 clés organisées en 6 page-namespaces + common × 10 sous-namespaces, mapping 24/24 manifest, séparation FR/EN propre |
| **D2 Accessibilité** (alt-text, ARIA, skip-link, errors) | 10 | Alt-text bilingue 100% planifié, ARIA labels nav/CTA, skip-link, role=alert/status sur formulaires |
| **D3 Performance contenu** (longueurs raisonnables, no bloat) | 9 | Sections courtes, valeurs i18n max 461 chars, FAQ ciblée, Loi 25 dense mais structurée |
| **D5 i18n / Velocity** (parité FR/EN, structure scalable) | 10 | Parité 516/516, scalable pour ajout es/zh, conventions next-intl ICU prêtes |
| **D6 Symmetry / SEO** (titles/meta uniformes) | 9 | Pattern title cohérent (« {Sujet} — Dépanneur Nobert {ville} »), meta dans la fenêtre 134-154 |
| **D7 SEO** (mots-clés naturels, Schema, hreflang) | 9 | Densité 0.77-1.56 %, LSI variations naturelles, 6 schemas structurés, hreflang FR-CA/EN-CA/x-default sur 6/6 routes |
| **D8 Loi 25** (RPP, opt-in, transferts, droits, incident) | 10 | Tous les éléments natifs : RPP nommé, 3 catégories cookies opt-in, 4 sous-traitants US, 7 droits, incident art. 3.5, mineurs <14, mises à jour 30 jours |
| **D9 Cohérence brand-identity** (voix, lexique, anti-corp) | 10 | Lexique allowed appliqué, banni absent, vouvoiement constant, anti-positionnement chaîne tenu, StoryBrand P19 respecté |
| **Cohérence patterns** (P01/P02/P09/P11/P13/P19/P20) | 10 | 7/7 patterns reflétés dans le contenu : sticky CTA omniprésent (P01), témoignages adjacents au CTA (P02), tagline 3-mots (P09), NAP P11, P13 voix anti-polish, P19 cadre StoryBrand, P20 alt-text galerie |
| **Documentation & traçabilité** | 9 | 4 JSON valides (fr, en, seo-content, qa-report), manifest mis à jour 24/24, brief→ph0→ph1→ph2→ph3 tracé |

### 7.1 Score global Phase 3 : **9.5 / 10**

### 7.2 Verdict gate ph3 → ph4

| Seuil | Mesure | Statut |
|---|---|---|
| μ ≥ 8.0 (gate ph3→ph4 SOIC) | **9.5** | ✅ **GO PHASE 4 BUILD** |

---

## 8. Conditions pour démarrer Phase 4

1. ✅ **Bloquer le build final** tant que les 6 variables CRITIQUES kickoff (`{ville}`, `{adresseLigne}`, `{codePostal}`, `{telephone}`, horaires, `{NEQ}`) ne sont pas fournies par le client. La pipeline Ph4 peut démarrer le scaffold + composants en parallèle, mais le déploiement Ph5 reste bloqué.
2. ✅ **Collecter les data-driven assets** : `data/produits.json` (~30), `data/promotions.json` (~6-10 pour la circulaire de la semaine), `data/temoignages.json` (3-5 voisins avec consentements écrits Loi 25 art. 5), `data/horaires.json`.
3. ✅ **Implémenter la résolution `{variable}`** : choix recommandé = next-intl `t('home.hero.title', { ville: process.env.NEXT_PUBLIC_VILLE })` côté composant, alimenté par `lib/clientConfig.ts` qui lit un JSON config par environnement.
4. ✅ **Brancher Schema JSON-LD** depuis `seo-content.json §structured_data_content` + injection des variables résolues à runtime via `lib/jsonld.ts`.
5. ✅ **Composer le helper `resolveAltText(template, data)`** pour les images produits/promos/témoignages (templates fournis dans `seo-content.json §alt_texts`).
6. ✅ **Valider Rich Results** sur Google Schema Validator + Schema.org validator avant deploy Ph5 (LocalBusiness, FAQPage, ItemList, BreadcrumbList).
7. ✅ **Conserver les warnings titres > 60 chars** (CR-001, CR-002) — décision documentée Ph1, ne pas raccourcir au détriment du keyword.

---

## 9. Livrables produits (récapitulatif Phase 3)

| Fichier | Statut | Validateur |
|---|---|---|
| `clients/depanneur-nobert/messages/fr.json` | ✅ produit | JSON valide, 516 clés, lexique allowed/banned respecté |
| `clients/depanneur-nobert/messages/en.json` | ✅ produit | JSON valide, 516 clés, parité FR↔EN parfaite, anglais CA-EN naturel |
| `clients/depanneur-nobert/seo-content.json` | ✅ produit | JSON valide, 6 meta tags, 6 heading_optimization, 12 alt_texts (5 templates), 6 FAQ Q/A, Schema LocalBusiness |
| `clients/depanneur-nobert/content-qa-report.json` | ✅ produit | JSON valide, verdict PASS_WITH_WARNINGS, 0 blocking issue, score 9.6 |
| `clients/depanneur-nobert/section-manifest.json` | ✅ mis à jour | 24/24 sections `status=content-ready`, `lifecycle.ph3_content_ready=2026-04-28T00:00:00Z` |
| `clients/depanneur-nobert/ph3-content-report.md` | ✅ ce document | — |

---

## 10. Score global: **9.5/10**

**Fin du rapport Phase 3 Content — Dépanneur Nobert.**
**GO PHASE 4 BUILD** (sous réserve résolution des 6 variables CRITIQUES kickoff + assets data-driven : produits, promotions, témoignages signés, horaires).
**Prochaine étape** : `agents/ph4-build/_orchestrator.md`.
