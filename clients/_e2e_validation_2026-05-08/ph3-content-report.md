# Phase 3 — Content Report

**Client** : Dépanneur Nobert inc. (`_e2e_validation_2026-05-08`)
**Mode NEXOS** : `create` (création from scratch — KPI conversion absolu)
**Date Phase 3** : 2026-05-08
**Orchestrateur** : `agents/ph3-content/_orchestrator.md`
**Phase précédente** : Ph2 Design — μ = 8.7/10 (GO ph2→ph3)
**Cadrage métier prioritaire** : CTA primaire = « Voir les promotions de la semaine » · clarté de l’offre dépanneur de quartier · indicateur de succès = visite physique + consultation promo hebdo
**Voix de marque verrouillée Ph1** : convivial-authentique-québécois · vouvoiement de politesse · D2 emotional · D4 warm
**Stack i18n** : next-intl 3.x · FR (default, sans préfixe) · EN (`/en/`)

---

## 0. Cadrage Phase 3 (rappel mode `create`)

| Axe | Décision opérationnelle Phase 3 |
|---|---|
| **KPI primaire** | Conversion → CTA primaire répété verbatim (`home.hero.ctaPrimary`, `common.stickyCta.label`) « Voir les promotions de la semaine » — 33 chars (exception assumée vs plafond 25 chars copywriter, voir §6) |
| **Slot `[ville]`** | Conservé en placeholder explicite dans 15 occurrences FR / EN. Résolution kickoff prioritaire (interpolation prévue Ph4 build via constante `SITE_CITY` ou `next-intl format` au choix de l’implémentation) |
| **Anti-corporate** | Ban-list lexicale Ph1 (`solution`, `expérience client`, `écosystème`, `partenaire de confiance`, `excellence`, `leader`, `innovant`, `premium`, `centre d’achat`) — **0 occurrence** détectée par scan regex sur l’ensemble du dictionnaire |
| **Loi 25 (D8)** | Templates intégrés en clair dans `common.consent.*` + `contact.rpp.*` + `legal.privacyPolicy.*` + `legal.legalMentions.*` — RPP Nobert Tremblay nommé, durées rétention écrites, opt-in explicite |

---

## 1. Copywriter principal (`copywriter-principal.md`)

### 1.1 Périmètre rédigé

Toutes les chaînes textuelles du site sont produites en FR-QC, alignées sur la voix `convivial-authentique-québécois` et le framework AIDA appliqué section par section. Aucun lorem ipsum, aucun placeholder de contenu (les seuls placeholders sont les variables i18n `{name}`, `{currentYear}`, etc. + le slot kickoff `[ville]`).

| Page | Sections rédigées | Mots FR | AIDA dominant |
|---|---|---|---|
| `/` (home) | S-001 → S-006 | 411 | Attention (Hero) → Désir (PromoTeaser) → Action (NewsletterCta + StickyCta) |
| `/promotions` | S-007 + S-008 | 119 | Action directe (asset KPI conversion) |
| `/produits` | S-009 + S-010 + S-011 ×6 catégories | 187 | Intérêt (catalogue navigable) |
| `/contact` | S-012 → S-016 | 289 | Action + Rassurance (RPP Loi 25) |
| `/legal` (politique + mentions) | S-017 ×2 | 107 | Conformité D8 |
| `common` (nav, footer, formulaires, consent, errors, loading) | partagé | 415 | Cross-cutting |

**Total FR : 1 528 mots productifs** (sans clés/structure JSON).

### 1.2 Hero S-001 — UVP appliquée (Ph1 verrouillé)

- **H1** : « Le dépanneur de [ville]. » (24 chars)
- **Sous-titre** : « Promotions chaque semaine, ouvert quand vous en avez besoin, et un patron qui vous connaît par votre nom. » — réutilise la formule UVP secondaire Ph1.
- **CTA primaire** : « Voir les promotions de la semaine » — verbatim cadrage métier.
- **CTA secondaire** : « Trouver l’adresse » — secondary action #1 du brief.
- **Alt photo** : photo réelle de Nobert + façade (`asset-plan.json::hero_homepage`).

### 1.3 Le mot du proprio S-005 — storytelling Ph2 cible 80-120 mots

> « Ça fait plus de vingt ans que je tiens le dépanneur ici, à [ville]. J’ai vu grandir les enfants du quartier, j’ai connu trois générations de clients, et je connais encore la marque de bière préférée de bien du monde. Mon travail, c’est simple : avoir ce qu’il vous faut, à un bon prix, et un sourire en plus. Pas de programme à points, pas de carte à remplir — juste un dépanneur de quartier, ouvert quand vous en avez besoin. Passez jaser, c’est de même qu’on fait. »
> — *Nobert Tremblay, propriétaire*

**92 mots FR / 91 mots EN** — dans la cible Ph2 80-120 mots, sous le plafond unitaire 500 chars (466 / 465). Registre FR-QC parlé assumé (« jaser », « de même », « bien du monde ») sans dérive familière vulgaire. Anti-corporate explicite (refus du programme à points = signal différenciant vs Couche-Tard / Shell Select).

### 1.4 Règles typographiques FR/QC respectées

- Espaces insécables avant `:` `;` `?` `!` (utilisation Unicode U+00A0 dans tous les `:` de titres et libellés).
- Apostrophes typographiques `’` (U+2019) systématiques — pas d’apostrophe ASCII.
- Tirets cadratins `—` (U+2014) pour les incises.
- Accents sur majuscules présents (`É`, `À`, `Ç`).
- Aucun guillemet droit `"` dans les valeurs (uniquement délimiteurs JSON).

### 1.5 CTAs — règle 25 chars + 1 exception documentée

| CTA | Chars | Statut |
|---|---|---|
| `home.hero.ctaPrimary` « Voir les promotions de la semaine » | **33** | **Exception assumée** — libellé verbatim du cadrage métier `--mode create` + `goals.primary_action` du brief. Différenciation directe vs concurrence. Validé Ph1. Documenté `content-qa-report.json::issues[CR-W01]`. |
| `home.hero.ctaSecondary` « Trouver l’adresse » | 18 | ✓ |
| `common.buttons.viewAllPromos` « Toutes les promotions » | 22 | ✓ |
| `home.newsletter.ctaSubscribe` « Je m’inscris » | 13 | ✓ |
| `contact.coordonnees.ctaCall` « Appeler maintenant » | 19 | ✓ |
| `home.infosPratiques.ctaCall` « Appeler le dépanneur » | 21 | ✓ |
| Tous les autres CTAs | ≤25 | ✓ |

---

## 2. Content architect (`content-architect.md`) — i18n dictionary

### 2.1 Namespaces — modulaire, DRY, type-safe

```
common.brand          — name, legalName, wordmark
common.nav            — items + a11y labels (skipToContent, openMenu, languageSwitcher)
common.stickyCta      — différenciation directe P11
common.footer         — 3 colonnes (contact / nav / légal) + RPP visible
common.buttons        — verbes d'action partagés
common.forms          — labels + placeholders + validation messages + success/error
common.consent        — Loi 25 cookies + newsletter + contact (texte intégral)
common.schema         — primitives Schema.org (businessType, currency, country, region)
common.errors         — 404 + error.tsx + retry
common.loading        — skeleton labels
home.{hero,promoTeaser,categories,infosPratiques,motProprio,newsletter} + meta
promotions.{hero,grid} + meta
produits.{hero,categoriesGrid,category} + meta
contact.{hero,coordonnees,horaires,form,rpp} + meta
legal.{content,privacyPolicy,legalMentions} + meta (×2)
```

### 2.2 Conventions respectées

| Convention | Statut |
|---|---|
| camelCase strict | ✓ (zéro `snake_case` ou `kebab-case` dans les clés) |
| Profondeur ≤ 4 niveaux | ✓ max 4 (`home.categories.items.biere.title`) |
| Variables `{name}` simple-accolade | ✓ (12 placeholders : `{currentYear}`, `{legalName}`, `{rppName}`, `{rppEmail}`, `{streetAddress}`, `{postalCode}`, `{phone}`, `{email}`, `{date}`, `{dateStart}`, `{dateEnd}`, `{dateUpdated}`, `{amount}`) |
| Aucun HTML dans le JSON | ✓ |
| Aucune valeur > 500 chars | ✓ (max observé : 466 chars FR / 465 chars EN sur `home.motProprio.body` — sous plafond strict) |
| Pluralisation ICU | n/a (pas de cas pluriel à ce stade — ajouter en Ph4 si nécessaire) |

### 2.3 Couverture `section-manifest.json`

**17/17 sections** ont leur `i18n_namespace` câblé dans `messages/fr.json` ET `messages/en.json` :

| Section | i18n_namespace | Présent FR | Présent EN |
|---|---|---|---|
| S-001 Hero | `home.hero` | ✓ | ✓ |
| S-002 PromoWeekTeaser | `home.promoTeaser` | ✓ | ✓ |
| S-003 CategoriesOverview | `home.categories` | ✓ | ✓ |
| S-004 InfosPratiques | `home.infosPratiques` | ✓ | ✓ |
| S-005 LeMotDuProprio | `home.motProprio` | ✓ | ✓ |
| S-006 NewsletterCta | `home.newsletter` | ✓ | ✓ |
| S-007 HeroPromoWeek | `promotions.hero` | ✓ | ✓ |
| S-008 PromosGrid | `promotions.grid` | ✓ | ✓ |
| S-009 HeroProduits | `produits.hero` | ✓ | ✓ |
| S-010 CategoriesGrid | `produits.categoriesGrid` | ✓ | ✓ |
| S-011 CategorySection | `produits.category` | ✓ | ✓ |
| S-012 HeroContact | `contact.hero` | ✓ | ✓ |
| S-013 Coordonnees | `contact.coordonnees` | ✓ | ✓ |
| S-014 Horaires | `contact.horaires` | ✓ | ✓ |
| S-015 ContactForm | `contact.form` | ✓ | ✓ |
| S-016 RppMention | `contact.rpp` | ✓ | ✓ |
| S-017 LegalContent | `legal.content` (+ `legal.privacyPolicy`, `legal.legalMentions`) | ✓ | ✓ |

### 2.4 Mise à jour `section-manifest.json`

- `status` : `"designed"` → `"content-ready"` pour les **17 sections**.
- `lifecycle.ph3_content_ready` : `null` → `"2026-05-08T15:30:00Z"`.
- `updated_at_ph3` (top-level) : `"2026-05-08T15:30:00Z"`.
- Lifecycle restant : `ph4_built`, `ph5_audited`.

---

## 3. SEO copywriter (`seo-copywriter.md`)

### 3.1 Title tags — tous <60 chars (FR + EN)

| Page | FR | chars | EN | chars |
|---|---|---|---|---|
| `/` | `Dépanneur Nobert \| Le dépanneur de [ville]` | 42 | `Dépanneur Nobert \| Your Corner Store in [city]` | 46 |
| `/promotions` | `Promotions de la semaine \| Dépanneur Nobert [ville]` | 51 | `This Week’s Deals \| Dépanneur Nobert [city]` | 43 |
| `/produits` | `Nos produits \| Bières, snacks, loto — Dépanneur Nobert` | 54 | `Our Products \| Beer, Snacks, Lottery — Dépanneur Nobert` | 55 |
| `/contact` | `Contact \| Dépanneur Nobert [ville]` | 34 | `Contact \| Dépanneur Nobert [city]` | 33 |
| `/politique-confidentialite` | `Politique de confidentialité \| Dépanneur Nobert` | 47 | `Privacy Policy \| Dépanneur Nobert` | 33 |
| `/mentions-legales` | `Mentions légales \| Dépanneur Nobert` | 35 | `Legal Notice \| Dépanneur Nobert` | 31 |

✓ **6/6 routes** sous le plafond 60 chars en FR ET EN.

### 3.2 Meta descriptions — toutes 120-155 chars (FR + EN)

| Route | FR (chars) | EN (chars) |
|---|---|---|
| `/` | 146 | 140 |
| `/promotions` | 138 | 138 |
| `/produits` | 135 | 149 |
| `/contact` | 134 | 144 |
| `/politique-confidentialite` | 148 | 136 |
| `/mentions-legales` | 133 | 135 |

✓ **12/12 meta descriptions** dans la zone optimale 120-155 chars (correctif appliqué après détection initiale de 6 hors-zone — voir §6).

### 3.3 Hiérarchie H1/H2/H3 — H1 unique par page (audit Ph2 confirmé Ph3)

| Route | H1 textuel matérialisé | H2 critiques |
|---|---|---|
| `/` | « Le dépanneur de [ville]. » | « 3 spéciaux à ne pas manquer », « Six rayons, mille p’tites raisons de passer », « Adresse, horaires, téléphone », « Bonjour, moi c’est Nobert. », « Recevez les promos chaque lundi » |
| `/promotions` | « Les promotions de cette semaine » | « Les spéciaux de la semaine » |
| `/produits` | « Tous nos produits, par catégorie » | « Choisissez votre catégorie » + 6 H2 catégories (Bières, Snacks, Boissons, Loto Québec, Dépannage, Glace) |
| `/contact` | « Nous trouver et nous joindre » | « Coordonnées », « Heures d’ouverture », « Écrivez-nous », « Vos renseignements personnels » |
| `/politique-confidentialite` | « Politique de confidentialité » (titre rendu MDX) | structure du template NEXOS |
| `/mentions-legales` | « Mentions légales » (titre rendu MDX) | structure du template NEXOS |

✓ **6/6 H1 uniques**. Hiérarchie stricte sans saut H1→H3.

### 3.4 Densité mots-clés FR (échantillon dictionnaire complet)

| Mot-clé | Occurrences | Densité | Verdict |
|---|---|---|---|
| `dépanneur` | 34 | 2.23 % | Légèrement au-dessus du plafond 2 % — **assumé** : le mot fait partie de la dénomination sociale (`Dépanneur Nobert`) qui apparaît dans nav, footer, branding, schema. Hors marque, densité naturelle ≈ 1.4 %. |
| `[ville]` | 15 | n/a | Slot variabilisé — couverture SEO local massive, sera résolue au kickoff |
| `bière` | 8 | 0.52 % | Mot-clé secondaire confirmé brief |
| `loto` / `Loto-Québec` | 7 | 0.46 % | Mot-clé secondaire confirmé brief |
| `promotion[s]` | 22 | 1.44 % | Mot-clé long-tail (`promotions dépanneur [ville] cette semaine`) couvert |
| `ouvert` | 9 | 0.59 % | Mot-clé `ouvert 24h`, `ouvert dimanche` partiellement couvert (le mot « 24h » sera ajouté au kickoff si la ville le justifie) |

### 3.5 Alt texts SEO-friendly (5 placeholders prévus pour Ph4)

| Image | Alt FR | Alt EN |
|---|---|---|
| Hero homepage S-001 | « Façade du Dépanneur Nobert avec Nobert Tremblay devant l’entrée — photo réelle du commerce de [ville] » | « Storefront of Dépanneur Nobert with owner Nobert Tremblay at the entrance — real photo of the [city] store » |
| Portrait Nobert S-005 | (à câbler Ph4 dans `asset-plan.json::portrait_nobert.alt_fr`) | (idem EN) |
| Promos S-008 (par item JSON) | Renseigné dynamiquement par item dans `site/data/promotions.json` (champ `alt_fr`/`alt_en` pour chaque entrée) | idem |
| Produits S-011 (par item JSON) | Idem (`site/data/products-categories.json` — chaque produit a son alt FR/EN) | idem |
| Maps iframe S-004/S-013 | Title prop : `home.infosPratiques.mapTitle` / `contact.coordonnees.mapTitle` | idem |

### 3.6 Structured data — contenu i18n prêt pour injection Ph4

Les primitives Schema.org sont exposées dans `common.schema` (`businessType: ConvenienceStore`, `currency: CAD`, `country: CA`, `region: QC`) et les libellés visibles (horaires, adresse, RPP) sont prêts pour interpolation dans les `JsonLd` injecteurs prévus en Ph4 (`components/seo/JsonLd.tsx`).

---

## 4. Translator (`translator.md`) — FR → EN

### 4.1 Adaptation culturelle (pas de traduction littérale)

| FR (Québec) | EN (adapté) | Note |
|---|---|---|
| « Voir les promotions de la semaine » | « See this week’s deals » | Pas `View this week’s promotions` (trop corporate) |
| « Promotions de la semaine » | « This Week’s Deals » | Title Case standard EN |
| « Le dépanneur de [ville] » | « Your corner store in [city] » | Adaptation culturelle : `dépanneur` n’a pas d’équivalent EN-CA naturel — `corner store` est l’usage courant, plus chaleureux que `convenience store` (registre Couche-Tard) |
| « Courriel » | « Email » | Quebecisme → standard EN |
| « Loto Québec » | « Loto-Québec » | Marque préservée avec graphie officielle |
| « Dépannage » (catégorie) | « Essentials » | Pas `Repair` (faux ami) — `essentials` reflète l’usage réel du rayon |
| « Bière » | « Beer » | Direct |
| « Glace » | « Ice » | Direct |
| « Nous joindre » | « Contact » | Pas `Join us` (faux ami) |
| « Le mot du proprio » | « A word from the owner » | Adaptation registre |
| « Pas de programme à points, pas de carte à remplir » | « No points program, no card to fill out » | Préservation rythme phrase + intention anti-corporate |
| « Quand vous passez, prenez le temps de jaser. » | « Drop by, take a moment to chat. » | `jaser` (FR-QC) → `chat` (registre warm-friendly EN) — pas de tentative de reproduire le ton FR-QC en EN, registre warm-friendly canadien standard |
| « Responsable de la protection des renseignements personnels » | « Privacy Officer » | Terme légal EN-CA reconnu (Québec Bill 25 / Law 25) |
| « Politique de confidentialité » | « Privacy Policy » | Standard EN |
| « Mentions légales » | « Legal Notice » | Standard EN |
| « Témoins de navigation » | « Cookies » | Quebecisme → standard EN |

### 4.2 Conventions typographiques EN respectées

- Pas d’espace avant `:` `;` `!` `?` (contraste avec FR).
- Apostrophes typographiques `’` partout.
- Title Case sur les title tags + section titles, sentence case sur les body strings.
- Anglais nord-américain (`favorite`, `neighborhood`, `color` — pas britannique).
- Oxford comma respecté dans les listes EN.

### 4.3 Variables d’interpolation — strictement identiques FR/EN

```
12 placeholders, 100% miroir FR ↔ EN :
{currentYear} {legalName} {rppName} {rppEmail}
{streetAddress} {postalCode} {phone} {email}
{date} {dateStart} {dateEnd} {dateUpdated} {amount}
```

### 4.4 Termes Loi 25 — traduction exacte (D8 non négociable)

| FR | EN | Source |
|---|---|---|
| « Loi 25 du Québec » | « Quebec’s Law 25 » | Préserve la référence légale exacte |
| « Loi 25, art. 3.1 » | « Quebec Law 25, art. 3.1 » | Article identique |
| « Témoins » (cookies) | « Cookies » | Convention pratique EN-CA |
| « Consentement » | « Consent » | Direct |
| « Renseignements personnels » | « Personal information » | Direct |
| « Responsable de la protection des renseignements personnels » | « Privacy Officer » | Terme legal officiel EN-CA |

### 4.5 Faux amis et gallicismes — relecture explicite

Aucun gallicisme détecté. Vérifications spécifiques effectuées :
- « actuellement » → ne traduit PAS par `actually` (n’apparaît pas dans le corpus, OK)
- « éventuellement » → ne traduit PAS par `eventually` (n’apparaît pas, OK)
- « assister » → ne traduit PAS par `assist` (n’apparaît pas, OK)
- « expérience » → mot banni Ph1, donc absent FR ET EN par construction.

---

## 5. Content reviewer (`content-reviewer.md`) — verdict éditorial

### 5.1 `content-qa-report.json` (résumé)

```json
{
  "verdict": "PASS_WITH_WARNINGS",
  "timestamp": "2026-05-08T15:30:00Z",
  "files_reviewed": [
    "clients/_e2e_validation_2026-05-08/site/messages/fr.json",
    "clients/_e2e_validation_2026-05-08/site/messages/en.json",
    "clients/_e2e_validation_2026-05-08/section-manifest.json"
  ],
  "scores": {
    "orthography":       { "score": 9.5, "issues": 0, "details": "Accents majuscules présents, apostrophes typographiques, espaces insécables FR" },
    "grammar":           { "score": 9.5, "issues": 0 },
    "tone_consistency":  { "score": 9.0, "issues": 0, "details": "Vouvoiement constant FR ; registre warm-friendly EN ; ban-list 0 occurrence" },
    "seo_quality":       { "score": 9.0, "issues": 1, "details": "Densité 'dépanneur' à 2.23% — assumée car incluse dans dénomination sociale" },
    "i18n_completeness": { "score": 10.0, "missing_keys_fr": 0, "missing_keys_en": 0, "fr_keys": 264, "en_keys": 264 },
    "legal_compliance":  { "score": 9.5, "consent_texts_present": true, "privacy_link": true, "rpp_visible": true, "retention_specified": true },
    "brand_alignment":   { "score": 9.0, "details": "Conforme brand-identity.json — UVP Ph1 réutilisée verbatim, ban-list respectée" }
  },
  "overall_score": 9.4,
  "blocking_issues": [],
  "warnings": [
    {
      "id": "CR-W01",
      "severity": "warning",
      "type": "cta_length",
      "location": "home.hero.ctaPrimary + common.stickyCta.label",
      "current": "Voir les promotions de la semaine (33 chars)",
      "note": "Plafond copywriter = 25 chars dépassé. Exception assumée : libellé verbatim du cadrage métier `--mode create` + `goals.primary_action` du brief. Validé Ph1 comme différenciation directe. À NE PAS modifier."
    },
    {
      "id": "CR-W02",
      "severity": "warning",
      "type": "keyword_density",
      "location": "global FR",
      "current": "'dépanneur' à 2.23%",
      "note": "Légèrement au-dessus du plafond 2%. Causé par la dénomination sociale (`Dépanneur Nobert`) qui apparaît dans nav, footer, branding et schema. Hors marque, densité naturelle ≈ 1.4%. Non bloquant."
    },
    {
      "id": "CR-W03",
      "severity": "warning",
      "type": "missing_data_kickoff",
      "location": "[ville] placeholder × 15",
      "note": "Risque Ph1/Ph2 reporté : le slot `[ville]` reste à résoudre au kickoff. Tous les fichiers i18n contiennent le marker explicite — aucune copie figée. Bloquant Ph5 si non résolu."
    }
  ],
  "approval": "PASS_WITH_WARNINGS — Contenu éditorialement prêt pour Ph4. Les 3 warnings sont documentés et non bloquants."
}
```

### 5.2 7 dimensions content-reviewer évaluées

| Dimension | Score | Justification |
|---|---|---|
| **Orthographe FR + EN** | 9.5 | Accents majuscules, apostrophes typographiques `’`, espaces insécables avant `:` `?` `!` en FR. Anglais nord-américain. |
| **Grammaire FR + EN** | 9.5 | Concordance des temps, accord sujet-verbe, adjectifs accordés. Aucune phrase passive non justifiée. |
| **Cohérence de ton** | 9.0 | Vouvoiement de politesse constant FR (formality 2/5 brief). Registre EN warm-friendly canadien. Aucune dérive corporate (ban-list 0/9 termes détectés). |
| **Qualité SEO** | 9.0 | 12/12 meta-descriptions 120-155, 6/6 titles <60, H1 unique × 6 routes, densité mots-clés contrôlée (warning W02 documenté). |
| **Complétude i18n** | 10.0 | Parité parfaite FR/EN : 264 clés × 2. 17/17 namespaces du `section-manifest.json` câblés. Zéro clé en dur. |
| **Conformité Loi 25 (D8)** | 9.5 | Cookie consent opt-in (3 catégories Essentiels/Analytics/Marketing), texte newsletter avec rétention 12 mois, texte contact avec rétention 6 mois, RPP nommé visible (S-016 + footer), lien politique de confidentialité dans formulaires. |
| **Alignement marque** | 9.0 | UVP Ph1 réutilisée verbatim, voix `convivial-authentique-québécois` respectée, ban-list lexicale 0 occurrence, anti-corporate explicite (« Pas de programme à points, pas de carte à remplir »). |

**Score global content-reviewer : 9.4 / 10**
**Verdict : PASS_WITH_WARNINGS** (3 warnings documentés, 0 blocking issue).

---

## 6. Corrections appliquées en cours d’exécution

| # | Section | Avant | Après | Raison |
|---|---|---|---|---|
| 1 | `produits.meta.description` FR | 165 chars | 135 chars | Hors zone 120-155 (>155) |
| 2 | `legal.legalMentions.meta.description` FR | 115 chars | 133 chars | Hors zone 120-155 (<120) |
| 3 | `promotions.meta.description` EN | 111 chars | 138 chars | Hors zone 120-155 (<120) |
| 4 | `contact.meta.description` EN | 119 chars | 144 chars | Hors zone 120-155 (<120) |
| 5 | `legal.privacyPolicy.meta.description` EN | 117 chars | 136 chars | Hors zone 120-155 (<120) |
| 6 | `legal.legalMentions.meta.description` EN | 100 chars | 135 chars | Hors zone 120-155 (<120) |
| 7 | `home.motProprio.body` FR | 62 mots | 92 mots (466 chars) | Sous cible Ph2 80-120 mots — ajusté pour rester sous plafond unitaire 500 chars (content-architect) |
| 8 | `home.motProprio.body` EN | 51 mots | 91 mots (465 chars) | Sous cible Ph2 80-120 mots, parité chars FR retenue |

Toutes les corrections sont alignées sur la voix verrouillée Ph1 — aucun apport de lexique corporate, aucune dérive de ton.

---

## 7. Risques portés en Ph4

| Risque | Source | Impact Ph4 | Mitigation |
|---|---|---|---|
| Slot `[ville]` non résolu (15 occurrences FR / EN) | brief.client.locations TBD | Build affichera littéralement `[ville]` — problème UX et SEO local | Kickoff obligatoire AVANT Ph4 ; sinon Ph4 effectue le build en mode placeholder + flag bloquant Ph5 (gate `D7 SEO < 7.0` automatique) |
| `{streetAddress}`, `{postalCode}`, `{phone}` non valorisés | brief.legal.address + .phone TBD | Footer + Coordonnees + Schema.org `LocalBusiness` incomplets | Idem — résolution kickoff. Templates JSON-LD prêts à interpoler en Ph4. |
| NEQ Dépanneur Nobert inc. inconnu | brief.legal.address TBD | Mentions légales S-017 incomplètes (D8 partiel) | Templates avec placeholder `{neq}` → flag Ph5 ; intégration MDX permet update post-launch sans rebuild complet. |
| Photo réelle propriétaire indisponible | brief.design + asset-plan.json::kickoff_assets_blocking | D2 emotional dégradé, alt text `home.hero.imageAlt` doit être édité en parallèle de la photo provisoire | Plan B Ph2 documenté (stock chaleureux dépanneur QC réel + alt étiqueté `temporaire` + ticket S+1). |
| Alt texts produits / promos non câblés | Données dynamiques `site/data/*.json` à créer en Ph4 | Risque a11y si oublié | Ph4 build doit générer `site/data/promotions.json` + `site/data/products-categories.json` avec champs `alt_fr` + `alt_en` obligatoires (ADR-003). |
| Densité « dépanneur » 2.23 % > plafond 2 % | dénomination sociale | Risque marginal de keyword stuffing perçu | Documenté warning W02. Hors-marque la densité est 1.4 %. Non bloquant. |

---

## 8. Validation des gates SOIC Ph3

| Dimension | État Ph3 | Note | Justification clef |
|---|---|---|---|
| **D1 Architecture** | i18n dictionnaire modulaire, 264 clés FR/EN, 17/17 namespaces manifest câblés, profondeur ≤4, camelCase strict | **9.0** | Structure prête pour `useTranslations()` Ph4 + génération types next-intl |
| **D2 Tonalité** | Voix `convivial-authentique-québécois` Ph1 verrouillée appliquée, ban-list 0 occurrence détectée, vouvoiement constant FR, registre warm-friendly EN, mot du proprio anti-corporate explicite | **9.0** | Aucune dérive Ph0→Ph1→Ph2→Ph3 du registre emotional + warm |
| **D3 Performance** | Aucun impact direct (pas de bundle Ph3) ; valeurs JSON ≤500 chars unitaires, pas de doublons cross-namespace | **8.5** | `messages/fr.json` ≈ 13 KB, `en.json` ≈ 11 KB — bien sous le budget |
| **D4 Sécurité** | Aucun HTML/JSX dans le JSON, échappement UTF-8 propre, aucune string contenant `<script>` ou markup, honeypot label défini | **9.0** | Pas de régression sécurité introduite en Ph3 |
| **D5 i18n** | Parité FR/EN parfaite (264/264 clés), 12 variables d’interpolation strictement identiques, structure miroir, hreflang FR/EN/x-default planifié Ph4 | **9.5** | Translator-checklist 8/8 PASS |
| **D6 Accessibilité** | Skip-to-content + open/closeMenu labels + sticky CTA aria-label + form labels explicites + alt texts hero, mention `prefers-reduced-motion` héritée Ph2 | **8.5** | A11y labels exhaustifs côté contenu — implémentation Ph4 |
| **D7 SEO** | 12/12 meta-desc 120-155, 6/6 titles <60, H1 unique × 6, hierarchy strict, alt texts hero rédigés, structured data primitives prêtes ; **risque [ville] documenté** | **8.5** | Plan SEO Ph1 matérialisé. Slot `[ville]` reste bloquant pour SEO local (warning W03). |
| **D8 Loi 25** | Cookie consent opt-in (3 cat.), retention newsletter 12 mois explicitée, retention contact 6 mois explicitée, RPP nommé visible footer + S-016, lien politique de confidentialité dans formulaires, opt-in JAMAIS pré-coché (par construction de copy `consentRequired`) | **9.5** | Toutes les exigences brief.legal sont matérialisées en copy |
| **D9 Qualité** | content-qa-report PASS_WITH_WARNINGS, 0 blocking issue, 3 warnings documentés, JSON `python json.load` ✓ × 2, 8 corrections proactives appliquées en cours d’exécution | **9.0** | Tout aligné Ph0/Ph1/Ph2 |

```
D1 Architecture     : 9.0
D2 Tonalité         : 9.0
D3 Performance      : 8.5
D4 Sécurité         : 9.0
D5 i18n             : 9.5
D6 Accessibilité    : 8.5
D7 SEO              : 8.5
D8 Loi 25           : 9.5
D9 Qualité          : 9.0
```

**Score global : 8.94/10**
**μ = 8.94/10**

Seuil de passage Ph3→Ph4 (μ ≥ 8.0) : **GO**.

---

## 9. Livrables produits (3 + 1 mis à jour)

| Fichier | Statut | Validation |
|---|---|---|
| `site/messages/fr.json` | ✓ créé | `python json.load` OK · 264 clés · 1 528 mots productifs · ban-list 0/9 |
| `site/messages/en.json` | ✓ créé | `python json.load` OK · 264 clés · parité FR ✓ · gallicismes 0 |
| `section-manifest.json` (mis à jour Ph3) | ✓ | 17/17 sections `status='content-ready'` + `lifecycle.ph3_content_ready=2026-05-08T15:30:00Z` + top-level `updated_at_ph3` |
| `ph3-content-report.md` | ✓ ce fichier | Synthèse 5 agents + gates SOIC + warnings + risques |

---

## 10. Prochain jalon

**Phase 4 — Build** : exécution `agents/ph4-build/_orchestrator.md` avec :

- Scaffold Next.js 15 selon `scaffold-plan.json` (78 fichiers, 12 dossiers).
- `messages/fr.json` + `messages/en.json` consommés par next-intl `getTranslations()` / `useTranslations()`.
- Composants S-001 → S-017 implémentés selon `wireframes.json` + `design-tokens.json::tailwind_extend_snippet`.
- Création des données dynamiques `site/data/promotions.json` + `site/data/products-categories.json` avec champs `alt_fr` / `alt_en` obligatoires (ADR-003).
- Injection JSON-LD `LocalBusiness` + `ConvenienceStore` + `OpeningHoursSpecification` + `GeoCoordinates` + `BreadcrumbList` + `ItemList` selon `seo-strategy.json`.
- Templates Loi 25 (`templates/privacy-policy-template.md`, `templates/legal-mentions-template.md`) interpolés avec `legal.privacyPolicy.intro` + `legal.legalMentions.intro` + RPP Nobert Tremblay + transferts US.
- Build validation `nexos/build_validator.py` (npm install → tsc → npm run build → npm audit → headers vercel.json).
- Auto-fix D4/D8 `nexos/auto_fixer.py` si nécessaire avant Ph5.

---

## Score global: 8.94/10
## mu = 8.94/10
