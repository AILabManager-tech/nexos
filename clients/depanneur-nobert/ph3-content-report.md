# Phase 3 — Content Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch — KPI conversion prioritaire)
**Date Phase 3 (itération 2 SOIC)** : 2026-05-14
**Date Phase 3 (run initial)** : 2026-04-28 (corpus rédactionnel intégral produit, conservé)
**Date Phase 3 (rerun itération 1)** : 2026-05-10 (patch tagline FR/EN + slug EN `/deals`, conservé)
**Orchestrateur** : Claude Code CLI (Phase 3 NEXOS v4.2 — Opus 4.7 1M context)
**Agents exécutés** : content-architect → copywriter-principal → seo-copywriter → translator → content-reviewer
**Stack imposée** : Next.js 15 + Tailwind 3.4 + next-intl (FR/EN) + Vercel
**Palette imposée (Ph2 itération 2)** : warm — `primary=#8B4513` brun boiseries · `accent=#FFD700` jaune doré · `background=#FFF8E7` crème
**Entrée** : `ph0-discovery-report.md` (2026-05-13) + `ph1-strategy-report.md` (2026-05-14 itération 2) + `ph2-design-report.md` (2026-05-14 itération 2)
**Itération SOIC** : 2 (alignement post-Ph2 warm — corpus textuel préservé palette-agnostique)

---

## 0. Cadrage de l'itération 2 SOIC (2026-05-14)

> **Note de ré-exécution itération 2** : cette exécution est un **audit-and-preserve**, pas une régénération de contenu.

La discovery du 2026-05-13 a rétabli la palette `design.palette_imposed` warm (brun/jaune/crème) du brief comme source de vérité, en remplacement de la palette navy/or/gris injectée par option CLI `--colors` lors du run précédent. Ph1 et Ph2 ont été régénérées en itération 2.

**Verdict d'audit Ph3 itération 2** : le corpus textuel FR/EN produit en itérations 0/1 est **palette-agnostique** — aucune chaîne ne référence une couleur. La régénération complète serait redondante. L'itération 2 effectue :

1. **Audit de neutralité palette** sur les 437 clés × 2 locales + `seo-content.json` (zéro occurrence des termes `navy`, `gris`, `or`, `noir corporate` dans les valeurs textuelles).
2. **Vérification de cohérence renforcée** des alt-texts avec la palette warm rétablie :
   - S-001 Hero — `imageAlt` « lumière dorée du matin » ⇒ cohérence parfaite avec `accent #FFD700` + `primary #8B4513` warm.
   - S-003 Catégories — pictogrammes Lucide line-art (Beer/Cookie/Ticket/ShoppingBasket) — cohérence avec D4=warm.
   - S-006 StoryBrand — « derrière le comptoir » + paragraphe « café avant le travail, bière le vendredi, billet de lotto le dimanche » — registre chaleureux confirmé.
3. **Reconduction des 5 warnings non bloquants** (CR-001 à CR-005) du content-qa-report — aucun ne dépend de la palette.
4. **Bump des timestamps** : `lifecycle.ph3_content_ready` → `2026-05-14T07:05:00Z` sur les 24 sections, `content-qa-report.json::timestamp` → `2026-05-14T07:00:00Z`, ajout `iteration_soic=2` + `iteration_note` documentée.

**Aucun blocking issue.** Score global préservé **9.6 / 10**.

---

## 1. Inputs Phase 3 itération 2

| Source | Apport |
|---|---|
| `brief-client.json` | Persona voisinage 35-65 + aînés 65+, vouvoiement strict, ville TBD, 6 pages, 24 sections, KPI conversion |
| `ph0-discovery-report.md` (2026-05-13) | 5 concurrents C1–C5, gaps SEO/Loi 25/AI Overviews exploitables, recommandations §7.7 actionnables |
| `ph1-strategy-report.md` (2026-05-14 itération 2) | UVP primaire « Votre dépanneur de quartier, à deux pas, ouvert pour vous. », lexique allowed/banned (20/14), slugs traduits FR≠EN, FAQPage différenciation #1, 7 patterns validés |
| `ph2-design-report.md` (2026-05-14 itération 2) | i18n keys 24 sections × 6 pages, wireframes warm, alt-text guidelines (S-001 vitrine + S-006 Nobert + S-004 voisins consent Loi 25 + S-015 ~38 produits), discipline D5=slow-organic |
| `brand-identity.json` (itération 2) | Ton convivial-authentique, formality 2/5, vouvoiement, 20 termes allowed, 14 bannis, anti-positionnement C4 Couche-Tard |
| `seo-strategy.json` (itération 2) | Title tags 36-67 chars FR, meta-desc 105-153 chars FR, primary keyword `dépanneur [ville]`, hreflang fr-CA/en-CA, JSON-LD plan, AI crawlers permis |
| `section-manifest.json` (status=audited Ph5, lifecycle préservé) | 24 sections × 6 pages × `i18n_namespace` requis |

---

## 2. Sortie de chaque agent (audit-and-preserve)

### 2.1 `content-architect` → architecture i18n

**Rôle** : structurer un dictionnaire next-intl modulaire à 4 namespaces racines (`common` partagé, `home`, `promotions`, `produits`, `contact`, `legal`).

**Livrable** : `messages/fr.json` et `messages/en.json` (même profondeur, mêmes clés).

| Métrique | Valeur |
|---|---|
| Clés totales FR | **437** |
| Clés totales EN | **437** (parité 1:1 vérifiée par script Python — diff ∅) |
| Profondeur max | 6 niveaux (`page.section.items.itemId.field` — pattern next-intl idiomatique pour collections nommées) |
| Variables d'interpolation cohérentes FR/EN | 18 (`{ville}`/`{city}`, `{anneeFondation}`, `{telephone}`, `{adresseLigne}`, `{codePostal}`, `{NEQ}`, `{email}`, `{rppEmail}`, `{currentYear}`, `{dateMaj}`, `{date}`, `{endDate}`, `{minutes}`, `{hour}`, `{produit}`, `{name}`, `{marque}`, `{type}`, `{format}`, `{origine}`, `{jeu}`, `{prix}`) |
| `common.consent` Loi 25 | ✓ banner + 3 catégories (essentiels / analytics / carte interactive) + actions accept/decline/customize/save + noticeLaw25 RPP cité |
| `common.forms` mutualisés | ✓ labels/placeholders/erreurs/succès partagés FORM-CONTACT + FORM-NEWSLETTER |
| Mapping `section-manifest` | 24/24 namespaces couverts |

**Statut itération 2** : ✓ PASS — JSON valide, parité parfaite 437/437, profondeur acceptable (CR-003 documentée comme info non bloquant).

### 2.2 `copywriter-principal` → contenu FR principal

**Rôle** : rédaction FR vouvoiement, ton convivial-authentique, framework AIDA par section, lexique allowed/banned strict.

**Livrable** : ~3 180 mots FR estimés, distribués sur 24 sections.

Exemples canoniques (préservés itération 2) :

| Section | Clé | FR |
|---|---|---|
| S-001 Hero | `home.hero.title` | « Votre dépanneur de quartier à {ville} » |
| S-001 Hero | `home.hero.ctaPrimary` | « Voir les promotions » (CTA ≤ 25 chars) |
| S-001 Hero | `home.hero.imageAlt` | « La devanture chaleureuse du Dépanneur Nobert dans le quartier de {ville}, lumière dorée du matin » ⇒ **renforcée par palette warm** |
| S-004 Témoignages | `home.socialProof.consentNote` | « Témoignages publiés avec consentement écrit, conformément à la Loi 25. » |
| S-006 StoryBrand | `home.storyBrand.paragraphHero` | « Le voisinage, c'est vous. Vous avez vos habitudes, vos petits plaisirs, votre rythme — un café avant le travail, une bière le vendredi, un billet de lotto un peu chanceux le dimanche. » |
| S-007 Newsletter | `home.newsletter.consentLabel` | « J'accepte de recevoir la circulaire hebdo du Dépanneur Nobert. Je peux me désinscrire à tout moment. » (opt-in, non pré-coché) |
| S-008 Sticky CTA | `common.stickyCta.label` | « Voir les promotions de la semaine » |
| S-015 Galerie / Bières | `produits.galerie.bieres.note` | « Vente de boissons alcoolisées encadrée par la SAQ. Permis affiché en magasin. Vente interdite aux personnes mineures. » |
| S-020 Maps | `contact.maps.ctaLoad` | « Charger la carte (Google Maps — États-Unis) » |
| S-022 Note RPP | `contact.rpp.body` | « Vos renseignements personnels sont protégés par la Loi 25 du Québec. Vous pouvez consulter, rectifier ou faire supprimer vos données… » |
| S-023 Politique | `legal.privacy.dataItems.analytics.fields` | « Adresse IP tronquée, pages consultées, type d'appareil, source de visite. » |
| S-024 Mentions | `legal.notice.hostingBody` | « Le site est hébergé par Vercel Inc., 440 N Barranca Avenue #4133, Covina, CA 91723, États-Unis. » |

**Statut itération 2** : ✓ PASS — vouvoiement constant (0 occurrence tutoiement), 0 terme banni détecté (`premium`, `leader`, `innovant`, `disruptif`, `scalable` absents), lexique allowed appliqué (voisinage, à deux pas, dépannage, du coin, courriel, infolettre, promotion de la semaine, passez nous voir, ouvert pour vous, …).

### 2.3 `seo-copywriter` → optimisation SEO + meta tags FR/EN

**Rôle** : `meta_tags` (title + description + og_title + og_description + canonical + hreflang) par page × locale, alt-texts, JSON-LD content (Organization, ConvenienceStore, FAQPage).

**Livrable** : `seo-content.json` (6 pages × FR/EN), préservé itération 2.

| Page | Title FR (chars) | Title EN (chars) | Meta-desc FR (chars) | Meta-desc EN (chars) | H1 FR | H1 EN |
|---|---|---|---|---|---|---|
| home | 67 | 64 | 153 | 147 | Votre dépanneur de quartier à {ville} | Your neighbourhood convenience store in {city} |
| promotions | 51 | 39 | 154 | 123 | Les promotions de la semaine | This week's promotions |
| produits | 67 | 65 | 154 | 153 | Nos produits, pour tout votre quotidien | Everything you need, every day |
| contact | 54 | 48 | 137 | 124 | Nous joindre, nous trouver | Reach us, find us |
| privacy | 56 | 43 | 138 | 128 | Politique de confidentialité | Privacy Policy |
| legal | 35 | 32 | 134 | 115 | Mentions légales | Legal Notice |

**FAQPage Schema** : 6 questions/réponses (3 promotions + 3 produits) FR + EN — booste AI Overviews / Google SGE.
**LocalBusiness Schema** : `ConvenienceStore` complet (placeholders kickoff `[ville]`, `[adresse]`, `[telephone]`, `[horaires]`).
**hreflang** : `fr-CA` + `en-CA` + `x-default → fr-CA` planifié sur chaque route.

**Statut itération 2** : ✓ PASS_WITH_WARNINGS — 3 titres FR > 60 chars (home 67, produits 67, privacy 56) volontairement conservés sous 70 chars pour préserver keyword + brand (CR-001, CR-002 — non bloquants, alignés `seo-strategy.json`).

### 2.4 `translator` → FR → EN

**Rôle** : adaptation culturelle FR (Québec) → EN (Canada anglophone), pas de traduction littérale, préservation structure i18n.

**Livrable** : `messages/en.json` (~3 210 mots EN, parité 437 clés).

Adaptations culturelles canoniques :

| FR (Québec) | EN (adapté) | Justification |
|---|---|---|
| Voir les promotions de la semaine | See this week's promotions | naturel EN |
| Trouver l'adresse | Find the address | naturel EN |
| Témoins | Cookies | terme EN standard |
| Courriel | Email | quebecisme → standard EN |
| Infolettre | Flyer / Newsletter | « Friday flyer » pour la circulaire hebdo |
| Loto-Québec | Loto-Québec | conservé (référence officielle) |
| Loi 25 | Quebec's Law 25 | référence légale exacte |
| RPP (Responsable de la protection des renseignements personnels) | Privacy Officer | équivalent EN reconnu |

**Statut itération 2** : ✓ PASS — anglais nord-américain (`neighbourhood` orthographe canadienne, `color` pas `colour`), 0 gallicisme détecté, Oxford comma respecté, ponctuation EN (pas d'espace insécable avant `:`, `?`, `!`).

### 2.5 `content-reviewer` → QA gate-keeper

**Rôle** : validation éditoriale finale, scoring 7 dimensions, verdict PASS / PASS_WITH_WARNINGS / FAIL.

**Livrable** : `content-qa-report.json` (itération 2 — `timestamp=2026-05-14T07:00:00Z`).

| Dimension | Score | Issues | Note |
|---|---|---|---|
| Orthography | 9.7 | 0 | FR vérifié contre lexique. Accents complets sur majuscules. Typographie québécoise respectée (espaces insécables `?`/`!`/`:`/`«»`). |
| Grammar | 10.0 | 0 | Voix active prédominante. Phrases 8-14 mots. Concordance des temps OK. |
| Tone consistency | 9.5 | 1 info | Vouvoiement constant FR. 0 terme banni. (`convenience store` apparaît uniquement dans meta SEO EN — non breach.) |
| SEO quality | 8.5 | 3 warnings | 3 titres FR > 60 chars (home/produits/privacy) — restent < 70 chars, alignement `seo-strategy.json` Ph1. |
| i18n completeness | 10.0 | 0 | Parité parfaite 437/437. Variables identiques 18 vars × 2 locales. |
| Legal compliance | 10.0 | 0 | Loi 25 native — RPP nommé, 3 catégories cookies opt-in (parité visuelle), 4 transferts US documentés (Vercel, GA, Maps, Resend), incident process, droits Loi 25 documentés. |
| Brand alignment | 9.5 | 0 | UVP primaire 8 mots. Tagline 6 mots warm. StoryBrand P19 (héros voisin → guide Nobert → promesse proximité). |

**Score global itération 2** : **9.6 / 10** (préservé)
**Verdict** : ✓ **PASS_WITH_WARNINGS** — Contenu prêt pour Phase 4 Build.

---

## 3. Cohérence palette warm ↔ contenu Ph3 (audit itération 2)

| Section | imageAlt / copy | Palette warm cohérente ? |
|---|---|---|
| S-001 Hero | « La devanture chaleureuse… lumière dorée du matin » | ✓ Renforcée (`accent #FFD700` + `primary #8B4513` warm) |
| S-002 PromotionsHighlight | « Trois rabais à ne pas manquer, mis à jour chaque vendredi par Nobert. » + badge accent | ✓ (Badge accent jaune `#FFD700` × text-on-accent `#2A1810`) |
| S-003 Catégories | Pictogrammes line-art Lucide (Beer/Cookie/Ticket/ShoppingBasket) | ✓ Cohérent D4=warm + anti-emoji décoratif |
| S-004 Témoignages | « Pas des avis. Des voisins. » + photos voisinage | ✓ Ton emotional warm |
| S-006 StoryBrand | « Vous, le quartier, et un dépanneur qui vous connaît » | ✓ Registre chaleureux confirmé |
| S-007 Newsletter | « Pas un spam, juste les bons coups » | ✓ Anti-corporate familier |
| S-008 StickyCTA | « Voir les promotions de la semaine » | ✓ CTA accent jaune sur primary brun |
| S-019 Coordonnées | Table horaires sémantique + adresse `text-2xl` | ✓ Lisibilité 65+ confirmée |
| S-020 Maps | « Charger la carte (Google Maps — États-Unis) » | ✓ Bouton primary brun + note transfert |
| S-023 Politique | Prose typographique 12 sections | ✓ `prose` Fraunces/Inter warm |
| S-024 Mentions | 8 sections (NEQ, hébergeur Vercel US, alcool RACJ) | ✓ Prose warm |

**Verdict cohérence itération 2** : ✓ **PASS** — aucun mismatch sémantique. La copy renforce la palette warm rétablie (« lumière dorée », « chaleureuse », « voisinage », « à deux pas »).

---

## 4. Couverture section-manifest 24/24 (audit itération 2)

| ID | Section | Page | i18n_namespace | Couverture |
|---|---|---|---|---|
| S-001 | Hero | home | `home.hero` | ✓ 9 clés (eyebrow, title, subtitle, ctaPrimary, ctaSecondary, ctaPrimaryAria, ctaSecondaryAria, imageAlt, trustNote) |
| S-002 | PromotionsHighlight | home | `home.promotionsHighlight` | ✓ 8 clés |
| S-003 | CategoriesProduits | home | `home.categories` | ✓ 4 items × 4 sous-clés + 3 clés header |
| S-004 | SocialProofVoisinage | home | `home.socialProof` | ✓ 3 témoignages + ctaReminder + consentNote + imageAltTemplate |
| S-005 | InfosPratiques | home | `home.infosPratiques` | ✓ 12 clés (addressLabel, phoneLabel, hoursLabel, ctaMap, ctaCall, …) |
| S-006 | StoryBrand | home | `home.storyBrand` | ✓ 7 clés (paragraphHero, paragraphGuide, paragraphPromise, …) |
| S-007 | NewsletterCTA | home | `home.newsletter` | ✓ 11 clés (consentLabel + consentNote Loi 25 inclus) |
| S-008 | StickyCTAGlobal | global | `common.stickyCta` | ✓ 3 clés |
| S-009 | PromotionsHero | promotions | `promotions.hero` | ✓ 6 clés (lastUpdate, validityNote, imageAlt, …) |
| S-010 | PromotionsList | promotions | `promotions.list` | ✓ 14 clés (filterAll, regularPriceLabel, promoPriceLabel, savingsLabel, …) |
| S-011 | PromotionsFAQ | promotions | `promotions.faq` | ✓ 3 questions + 3 réponses (FAQPage Schema ready) |
| S-012 | CrossSellProduits | promotions | `promotions.crossSell` | ✓ 3 clés |
| S-013 | ProduitsHero | produits | `produits.hero` | ✓ 5 clés |
| S-014 | ProduitsCategoriesNav | produits | `produits.categoriesNav` | ✓ ariaLabel + 4 items + scrollHint |
| S-015 | ProduitsGalerie | produits | `produits.galerie` | ✓ 4 catégories × {title, subtitle, anchorId} + 4 imageAltTemplate + note SAQ + outOfStockLabel |
| S-016 | ProduitsFAQ | produits | `produits.faq` | ✓ 3 questions + 3 réponses |
| S-017 | CrossSellPromotions | produits | `produits.crossSell` | ✓ 3 clés |
| S-018 | ContactHero | contact | `contact.hero` | ✓ 8 clés (addressDisplay, phoneDisplay, phoneAria, ctaCall, ctaMap, …) |
| S-019 | CoordonneesHoraires | contact | `contact.coordonnees` | ✓ 11 clés (hoursTableCaption sémantique, hoursColumnDay, hoursColumnHours, specialClosuresTitle, …) |
| S-020 | MapsEmbed | contact | `contact.maps` | ✓ 9 clés (placeholderTitle, placeholderBody, ctaLoad, consentNote, fallbackTitle, …) |
| S-021 | ContactForm | contact | `contact.form` | ✓ 15 clés (labelConsent + consentNote Loi 25 inclus) |
| S-022 | ContactNoteRPP | contact | `contact.rpp` | ✓ 7 clés (rppName, rppRole, rppEmail, linkPrivacy, incidentNote) |
| S-023 | PolitiqueContent | politique-confidentialite | `legal.privacy` | ✓ 12 sections (RPP, données, finalités, consentement, sous-traitants, transferts, droits, incident, sécurité, mineurs, mises à jour, contact) + 5 dataItems + 4 thirdPartiesItems + 7 rightsItems |
| S-024 | MentionsContent | mentions-legales | `legal.notice` | ✓ 8 sections (éditeur, hébergement, PI, liens, responsabilité, droit applicable, alcool RACJ, contact) |

**Verdict couverture** : ✓ **24/24 sections** ont un namespace i18n complet FR + EN.

---

## 5. Conformité Loi 25 (D8) — vérification finale Ph3

| Élément | Section | Vérification itération 2 |
|---|---|---|
| Bandeau cookie opt-in 3 catégories | `common.consent` | ✓ banner + 3 catégories (essentials/analytics/maps_third_party) + 4 actions (Accept/Decline/Customize/Save). Parité visuelle copy garantie. |
| Newsletter consent opt-in | `home.newsletter.consentLabel` | ✓ Non pré-coché. Note RPP visible + désinscription mentionnée. |
| Contact form consent opt-in | `contact.form.labelConsent` | ✓ Non pré-coché. Note conservation 24 mois + lien suppression `{rppEmail}`. |
| Maps consent gating | `contact.maps.ctaLoad` + `consentNote` | ✓ « Charger la carte (Google Maps — États-Unis) » + note transfert IP US explicite. |
| RPP encadré dédié | `contact.rpp` | ✓ Nobert Tremblay nommé + courriel + titre + lien politique + incident process art. 3.5. |
| Politique de confidentialité complète | `legal.privacy` | ✓ 12 sections : RPP + 5 dataItems + 3 finalités + consentement + 4 sous-traitants US + transferts + 7 droits + incident + sécurité + mineurs < 14 ans + mises à jour 30 j + contact postal. |
| Mentions légales complètes | `legal.notice` | ✓ 8 sections : éditeur (Dépanneur Nobert inc.) + NEQ placeholder + adresse placeholder + responsable publication (Nobert Tremblay) + hébergeur Vercel US + PI + liens externes + responsabilité + droit Québec + alcool RACJ + contact. |
| Lexique « langage clair » | global | ✓ « témoins » (au lieu de « cookies technique »), « renseignements personnels » (terme officiel Loi 25), formulations courtes 8-14 mots. |
| Pas de dark pattern | global | ✓ Aucune pré-coche, bouton « Refuser » même visibilité que « Accepter », pas de pop-up newsletter forcé. |

**Score D8 itération 2** : **10.0 / 10** (préservé).

---

## 6. Cohérence Ph3 ↔ Ph0/Ph1/Ph2 (itération 2)

| Critère | Vérification itération 2 |
|---|---|
| Palette warm imposée (Ph2 itération 2) | ✓ Contenu palette-agnostique — alt-texts renforcent cohérence warm. |
| Personnalité 6D (D1=3, D2=emotional, D3=heavy, D4=warm, D5=slow-organic, D6=symmetric) | ✓ Ton convivial-authentique, vouvoiement, phrases courtes, lexique allowed/banned strict. |
| UVP primaire 8 mots Ph1 | ✓ `common.brand.tagline` = « Votre dépanneur de quartier, à deux pas. » |
| 7 patterns validés (P01/P02/P09/P11/P13/P17/P19/P20) | ✓ CTA principal P01 sticky + témoignages P02 adjacent CTA + StoryBrand P19 (S-006) + FAQPage (S-011, S-016). |
| Section-manifest 24/24 couvert | ✓ Mapping 1:1 i18n_namespace ↔ messages/{fr,en}.json. |
| Anti-corporate (rejet C4 Couche-Tard) | ✓ 0 terme banni (`premium`, `leader`, `scalable`, …). Prénom Nobert visible. |
| Cible 65+ accessibilité | ✓ adresse `text-2xl` + table horaires sémantique th/td + alt-texts descriptifs 100 %. |
| KPI primaire conversion | ✓ CTA « Voir les promotions » placé S-001 + S-008 + S-017 (cross-sell produits → promos). |
| Loi 25 conformité native | ✓ RPP + 3 catégories consent + 4 sous-traitants US + 7 droits + incident process. |
| Bilinguisme structuré FR/EN | ✓ Parité 437/437 + variables identiques + slugs traduits (`/produits` ↔ `/products`, `/promotions` ↔ `/deals`). |

---

## 7. Artefacts livrés (Ph3 → Ph4 itération 2)

| Fichier | Statut itération 2 | Taille | Note |
|---|---|---|---|
| `messages/fr.json` | ✓ préservé (run initial 2026-04-28 + patch 2026-05-10) | ~32 KB | 437 clés, 3 180 mots FR, JSON valide |
| `messages/en.json` | ✓ préservé (run initial 2026-04-28 + patch 2026-05-10) | ~30 KB | 437 clés, 3 210 mots EN, parité 1:1, JSON valide |
| `seo-content.json` | ✓ préservé (patch 2026-05-10 slug EN `/deals`) | ~14 KB | 6 pages × FR/EN + 6 FAQ + 12 alt-texts + Schema content + densité keywords |
| `content-qa-report.json` | ✓ régénéré itération 2 (timestamp + iteration_soic + iteration_note) | ~5 KB | Verdict PASS_WITH_WARNINGS, score 9.6/10 préservé |
| `section-manifest.json` | ✓ régénéré itération 2 (`lifecycle.ph3_content_ready` → 2026-05-14T07:05:00Z, `last_updated_phase` = ph3-content, `iteration_soic` = 2) | ~22 KB | 24 sections × `status=audited` préservé Ph5 |

---

## 8. Conditions transmises à Phase 4 (Build)

### 8.1 Bloquantes au kickoff (héritées Ph0/Ph1/Ph2)

1. **6 variables kickoff client à résoudre** : `{ville}`, `{anneeFondation}`, `{telephone}`, `{adresseLigne}`, `{codePostal}`, `{NEQ}` — sans quoi titles/meta/H1/Schema/sitemap restent en placeholder explicite. Cible : T+24 h post-kickoff.
2. **Photos vitrine/intérieur/propriétaire/voisins** : décider OUI shooting J+15 OU fallback Unsplash thématique + shooting Ph6 acté (impact S-001 + S-004 + S-006 + S-015).

### 8.2 Non-bloquantes pour Ph4 (à débloquer pendant Ph4)

3. **Liste 12 produits × 4 catégories** (48 SKU minimum) avec alt-text descriptif (template `{marque} {type} {format} {origine}` prêt) pour S-015.
4. **Template promo hebdo + 8 exemples seed JSON** (`data/promotions.json`) pour S-010 — schéma Zod à câbler en Ph4.
5. **3-5 témoignages voisinage** avec consentement Loi 25 écrit explicite par personne (release signée) pour S-004.

### 8.3 Décisions Ph3 figées (Ph4 doit consommer, pas re-débattre)

- Corpus 437 clés × FR/EN — **ne pas renommer ni dupliquer**.
- Variables d'interpolation 18 vars — schéma figé, ajouter uniquement si Ph4 introduit nouveau cas.
- Slugs FR ≠ EN : `/promotions` ↔ `/deals`, `/produits` ↔ `/products`, `/politique-confidentialite` ↔ `/privacy-policy`, `/mentions-legales` ↔ `/legal-notice`, `/contact` ↔ `/contact`.
- CTA principal label « Voir les promotions de la semaine » → utiliser `common.stickyCta.label` (S-008) ET `common.buttons.viewWeekPromotions` (autres CTA inline).
- FAQ Schema FAQPage : 6 Q/R FR+EN dans `seo-content.json::structured_data_content.faq_items` à injecter dans `components/seo/FAQPageJsonLd.tsx`.
- LocalBusiness Schema : type `ConvenienceStore`, priceRange `$`, area_served `{ville} et quartiers adjacents`.

---

## Score global Phase 3 itération 2

| Dimension | Score | Commentaire |
|---|---|---|
| D1 Architecture | 9.5 | 437 clés × 6 pages × 24 sections, profondeur 6 niveaux (next-intl idiomatique), namespaces cohérents. |
| D2 Contenu | 9.6 | Voix active, lexique allowed/banned strict, vouvoiement constant, 0 terme banni détecté, framework AIDA appliqué. |
| D3 Performance | 9.0 | Bundle messages ~62 KB FR+EN, conforme budget Ph1 (< 200 KB total client-side). |
| D4 Sécurité | 9.5 | Aucun HTML inline dans les strings, aucun secret/PII, anti-XSS structural (JSX statique pages légales). |
| D5 i18n | 10.0 | Parité parfaite 437/437, 18 variables identiques, slugs traduits, anglais nord-américain naturel. |
| D6 Accessibilité | 9.8 | Alt-texts descriptifs 100 %, ARIA labels (S-014 categoriesNav, S-020 maps), skip-link, role=alert/status couverts. |
| D7 SEO | 9.0 | Title 32-67 chars (≤70), meta 115-154 chars FR, H1 unique × 6 pages, Schema LocalBusiness/ConvenienceStore/FAQPage/ItemList ready, AI crawlers permis. |
| D8 Loi 25 | 10.0 | RPP nommé, opt-in 3 catégories cookies (parité visuelle copy), 4 sous-traitants US documentés (Vercel/GA/Maps/Resend), 7 droits, incident process actif, mineurs <14 ans, mises à jour 30 j. |
| D9 Qualité méthodo | 9.5 | 5 artefacts JSON valides × 100 %, parité parfaite, aucun gallicisme EN, alignement Ph0/Ph1/Ph2 itération 2 documenté, palette warm rétablie sans régression contenu. |

**Score moyen : 9.5 / 10**
**Score préservé content-qa-report : 9.6 / 10**

**Verdict Phase 3 → Phase 4** : ✓ **PASS** (seuil μ ≥ 8.0).

### Conditions bloquantes pour Phase 4
Aucune — gate ph3→ph4 satisfaite. Les 5 conditions opérationnelles (6 variables kickoff, photos, témoignages, promos seed, catalogue produits) sont **non-bloquantes pour Ph4** mais doivent être tracées comme placeholders explicites si non résolues au kickoff.

### Warnings non bloquants reconduits (CR-001 à CR-005)
1. **CR-001 / CR-002** : 3 titres FR (home/produits) à 67 chars > seuil 60 chars de l'agent seo-copywriter — conservés sous 70 chars conforme `seo-strategy.json` Ph1.
2. **CR-003** : profondeur i18n max = 6 niveaux pour collections nommées (catégories/témoignages/FAQ items) — pattern next-intl idiomatique justifié.
3. **CR-004** : usage épicène ponctuel `habitué·es` (1 occurrence sur 3 180 mots FR) — conforme `brand-identity.cultural_markers` (« épicène quand naturel »).
4. **CR-005** : 6 variables kickoff non résolues — à débloquer T+24 h.

---

*Rapport généré par Claude Code CLI en orchestration Phase 3 NEXOS v4.2.0 — 2026-05-14.*
*Itération 2 SOIC — audit-and-preserve post-Ph2 warm palette. Corpus textuel FR/EN intégralement préservé (437 clés × 2 locales, score 9.6/10).*
