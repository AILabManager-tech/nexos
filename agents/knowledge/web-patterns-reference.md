---
id: knowledge/web-patterns-reference
version: 1.0.0
created: 2026-04-16
source: NEXOS_PLATFORM/NEXOS_Web_Patterns_Reference.md
consumed_by:
  - agents/ph1-strategy/pattern-recommender.md
  - agents/ph2-design/*
  - agents/ph5-qa/*
scope: "30 sites de référence, 20 patterns P01-P20, 6 dimensions de personnalité, 6 secteurs"
---

# NEXOS — Référentiel Patterns Web

## 0. Usage rapide

> **Comment lire ce document (pour un agent)** : chaque pattern a un ID `P01`–`P20`. Chaque site a un ID `S01`–`S30`. Chaque dimension a un ID `D1`–`D6`. Chaque secteur a un ID `SEC-01`–`SEC-06`. Ces IDs sont stables et utilisés dans `pattern-matrix.json`, `sector-references.json`, `personality-dimensions.json`, et par `agents/ph1-strategy/pattern-recommender.md`.
>
> **Conventions de lecture** :
> - `D1-D6` dans ce document = **dimensions de personnalité visuelle** (density, register, typo_weight, palette_temp, motion_speed, layout).
> - `D1-D8` ailleurs dans NEXOS = **dimensions SOIC d'évaluation** (UX, Accessibilité, Contenu, Sécurité, Performance, SEO, i18n, Légal). À ne pas confondre.
> - Les citations en bloc `>` sont **verbatim** de la source primaire. Ne pas reformuler.

## 1. Scope & règle d'or

Ce référentiel agrège 30 sites web réels analysés par NEXOS pour nourrir la bibliothèque de patterns du pipeline de création (ph0 → ph5). Chaque site est catégorisé dans un secteur, chaque pattern extrait est typé (tier 1/2/3), et chaque dimension de personnalité visuelle est discrétisée pour permettre des choix combinatoires différenciants.

**Règle d'or (verbatim)** :

> "Deux sites configurés avec valeurs opposées sur ≥ 4 des 6 dimensions de personnalité doivent sembler venir de deux agences différentes."

Cette règle est le critère de différenciation NEXOS : quand on génère un nouveau site, il doit s'opposer à au moins un site existant sur 4+ dimensions. L'algorithme de test vit dans `personality-dimensions.json → opposition_test`.

## 2. Secteurs couverts

| Secteur ID | Nom                          | Client NEXOS cible            | Nb sites ref |
|------------|------------------------------|-------------------------------|--------------|
| SEC-01     | Santé / Physiothérapie       | clinique-aura                 | 5            |
| SEC-02     | Agence créative              | collectif-nova                | 5            |
| SEC-03     | Restauration                 | table-de-marguerite           | 5            |
| SEC-04     | Gestion de projet / SaaS     | vertex-pmo                    | 5            |
| SEC-05     | Juridique                    | beaumont-avocats              | 5            |
| SEC-06     | Électrique industriel        | electro-maitre-industriel     | 5            |

**Total** : 6 secteurs × 5 sites = 30 sites S01–S30.

## 3. Les 6 dimensions de personnalité (D1–D6)

### D1 · Densité visuelle

**Type** : ordinal (échelle 1→5)
**Échelle** :
- `1` — très aéré, whitespace massif (luxe, spa, beauté)
- `2` — aéré (restaurant, studio créatif)
- `3` — équilibré (agence, conseil)
- `4` — dense (juridique, institutionnel)
- `5` — très dense, information riche (industrie, B2B technique)

**Exemples NEXOS** : Clinique Aura = `1`, Electro-Maître = `5`.

### D2 · Registre émotionnel

**Type** : categorical
**Valeurs discrètes** : `emotional` | `technical` | `technical-warm` | `emotional-cold`

- `emotional` — chaleur humaine, organique, textures
- `technical` — précision, data, interfaces, froid
- `technical-warm` — technicité + palette chaude (construction, artisanat)
- `emotional-cold` — connexion humaine teintée de distance professionnelle (santé corporate)

**Exemples NEXOS** : Clinique Aura = `emotional`, Beaumont = `technical`, Electro-Maître = `technical-warm`.

### D3 · Poids typographique

**Type** : categorical
**Valeurs discrètes** : `light` | `medium` | `heavy` | `contrasted`

- `light` — fins et espacés (300, tracking large)
- `medium` — neutre lisible (500)
- `heavy` — condensé gras (700–900)
- `contrasted` — mélange extrêmes (200 + 700 en alternance)

**Exemples NEXOS** : Beaumont Avocats = `light`, Electro-Maître = `heavy`, Collectif Nova = `contrasted`.

### D4 · Température de palette

**Type** : categorical
**Valeurs discrètes** : `warm` | `cold` | `industrial` | `variable`

- `warm` — ivoire, crème, brun, ambre, terracotta
- `cold` — bleu marine, quasi-noir, cyan, indigo
- `industrial` — noir pur + un accent saturé (jaune, orange)
- `variable` — custom properties CSS, palette contextuelle

**Exemples NEXOS** : Clinique Aura = `warm`, Beaumont = `cold`, Electro-Maître = `industrial`, Collectif Nova = `variable`.

### D5 · Vélocité du mouvement

**Type** : categorical
**Valeurs discrètes** : `still` | `slow-organic` | `fast-purposeful` | `mechanical`

- `still` — presque aucune animation (juridique, institutionnel)
- `slow-organic` — transitions longues, spring physics (beauté, gastronomie)
- `fast-purposeful` — vif et précis (SaaS, tech)
- `mechanical` — rapide et sans fioritures (construction, industrie)

**Exemples NEXOS** : Beaumont = `still`, Clinique Aura = `slow-organic`, Mark Systems = `fast-purposeful`, Electro-Maître = `mechanical`.

### D6 · Structure spatiale

**Type** : categorical
**Valeurs discrètes** : `symmetric` | `asymmetric-soft` | `asymmetric-strong` | `editorial`

- `symmetric` — centré, grilles régulières
- `asymmetric-soft` — un élément légèrement hors case
- `asymmetric-strong` — chevauchements intentionnels, débordements
- `editorial` — layout libre, position absolue, cascade

**Exemples NEXOS** : Beaumont = `symmetric`, Clinique Aura = `asymmetric-soft`, Electro-Maître = `asymmetric-strong`, Collectif Nova = `editorial`.

### Matrice d'opposition (test règle d'or)

Exemple canonique — **Clinique Aura vs Electro-Maître** :

| Dim | Clinique Aura         | Electro-Maître             | Opposés ? |
|-----|-----------------------|----------------------------|-----------|
| D1  | 1 (aéré)              | 5 (très dense)             | ✓         |
| D2  | emotional             | technical-warm             | ✓         |
| D3  | light                 | heavy                      | ✓         |
| D4  | warm (ivoire)         | industrial (noir + ambre)  | ✓         |
| D5  | slow-organic          | mechanical                 | ✓         |
| D6  | asymmetric-soft       | asymmetric-strong          | ✓ (partiel) |

**Score** : 6/6 opposées → test passé largement. Le seuil est de 4/6 ; ces deux configs sont volontairement aux antipodes.

**Matrice 6D pour les 6 clients NEXOS** :

| Client                  | D1 | D2              | D3         | D4         | D5              | D6                  |
|-------------------------|----|-----------------|------------|------------|-----------------|---------------------|
| clinique-aura           | 1  | emotional       | light      | warm       | slow-organic    | asymmetric-soft     |
| table-de-marguerite     | 2  | emotional       | contrasted | warm       | slow-organic    | asymmetric-soft     |
| beaumont-avocats        | 4  | technical       | light      | cold       | still           | symmetric           |
| mark-systems            | 3  | technical       | contrasted | cold       | fast-purposeful | symmetric           |
| electro-maitre          | 5  | technical-warm  | heavy      | industrial | mechanical      | asymmetric-strong   |
| collectif-nova          | 3  | technical-warm  | contrasted | variable   | fast-purposeful | editorial           |

## 4. Les 20 patterns universels (P01–P20)

> Gabarit : contexte, structure, règles impératives (verbatim), anti-patterns, sites ref, métrique mesurée, dimensions SOIC impactées, tier (1 = universel / 2 = sectoriel / 3 = premium).

### P01 · Sticky CTA persistant

**Tier** : 1 (universel)
**Secteurs forts** : SEC-01 Santé, SEC-05 Juridique, SEC-06 Trades
**SOIC impacté** : D1 UX (conversion), D2 Accessibilité (toujours visible)

**Contexte** : Maximiser la conversion en gardant l'action primaire visible à tout instant du scroll.

**Structure** :
- Bouton CTA dans header persistant OU coin fixe (sup-droit / inf-droit)
- Visible sur **chaque** page
- Label verbal d'action clair ("Prendre RDV", "Demander un devis", "Get a Quote")
- Accessibilité : `aria-label`, contraste AA minimum, focus-visible

**Règle impérative (verbatim)** :
> "CTA booking permanent dans le header (visible sur chaque page)" — Twin Boro

**Anti-patterns** :
- CTA qui disparaît au scroll sans raison
- Multi-CTA concurrents dans le header
- Label vague ("En savoir plus") en CTA primaire

**Sites de référence** : S01 Twin Boro (twinboro.com), S03 Athletix (athletixrehab.com)

**Métrique mesurée** : —

---

### P02 · Social proof adjacente au CTA

**Tier** : 1 (universel)
**Secteurs forts** : Tous
**SOIC impacté** : D1 UX, D3 Contenu

**Contexte** : Témoignages/avis placés **immédiatement** à côté du CTA (pas derrière un scroll) pour multiplier le taux de conversion. La proximité spatiale est la clef.

**Structure** :
- Carousel 10–15 témoignages OU bloc fixe 3 témoignages
- Adjacent spatial au bouton d'action
- Photo + citation + nom + rôle/ville
- Source vérifiable (Google Reviews, LinkedIn, nom complet)

**Règle impérative (verbatim)** :
> "Carousel 15 témoignages adjacents au bouton booking (proximity = conversion)" — Bloor Jane

**Anti-patterns** :
- Témoignages relégués au footer
- Témoignages anonymes sans photo
- Texte générique ("Super service !")
- > "Ne jamais séparer social proof et CTA"

**Sites de référence** : S05 Bloor Jane Physio (bloorjanephysio.com), S17 Monday.com

**Métrique mesurée** : **45 → 101 leads/mois (+2×)** après mise en place (Bloor Jane) ; 2× conversions Hudgell Solicitors (S25).

---

### P03 · Color-coded navigation

**Tier** : 2 (sectoriel)
**Secteurs forts** : SEC-05 Juridique, multi-service
**SOIC impacté** : D1 UX, D6 SEO (IA claire)

**Contexte** : Chaque service/domaine a sa couleur distinctive — navigation intuitive sans lire.

**Structure** :
- Palette de N couleurs (une par domaine)
- Couleur reprise dans le header de la page de domaine, dans la carte du menu, dans les CTA associés
- Contraste AA respecté pour chaque couleur sur blanc et noir
- Fallback texte pour lecteurs d'écran (aria-label, pas de couleur seule comme signal)

**Règle impérative (verbatim)** :
> "Chaque service/section a sa couleur distinctive" — Hudgell

**Anti-patterns** :
- 8+ couleurs → chaos visuel
- Contraste AAA négligé pour les couleurs de nav
- Couleur seule comme signal (violation WCAG)

**Sites de référence** : S25 Hudgell Solicitors (hudgellsolicitors.co.uk)

**Métrique mesurée** : Design doublant les conversions year-over-year (Hudgell)

---

### P04 · Hero vidéo émotionnelle

**Tier** : 3 (premium)
**Secteurs forts** : SEC-02 Créatif, SEC-03 Resto, SEC-01 Santé sportive
**SOIC impacté** : D1 UX, D5 Performance (poids vidéo), D8 Légal (RGPD autoplay)

**Contexte** : Vidéo hero montrant des **personnes réelles** (pas stock) pour créer une connexion émotionnelle instantanée. Filtre aussi la clientèle cible dans les niches (ex : athlètes Athletix).

**Structure** :
- Vidéo MP4 ou WebM compressée (<2 Mo pour LCP)
- Autoplay muet + loop
- Poster image pour fallback / loading
- Pas de son automatique (RGPD + UX)
- Alternative image pour `prefers-reduced-motion: reduce`
- Phrases en overlay si texte

**Règle impérative (verbatim)** :
> "Vidéo hero émotionnelle — personnes réelles, pas corporate — authentique" — Pixelflakes

**Anti-patterns** :
- > "PAS de stock footage" — Pixelflakes
- Vidéo autoplay avec son
- Vidéo > 5 Mo qui casse le LCP
- Absence de fallback pour `reduced-motion`

**Sites de référence** : S10 Pixelflakes (pixelflakes.com), S03 Athletix (athletixrehab.com)

**Métrique mesurée** : —

---

### P05 · Single-page scroll

**Tier** : 2 (sectoriel)
**Secteurs forts** : PME, boutiques, startups, cabinets boutique
**SOIC impacté** : D1 UX, D6 SEO (page unique = une seule cible SEO)

**Contexte** : Tout le contenu du site sur une seule page, sections ancorées via `#hash`. Format accessible, rapide à consommer, idéal PME.

**Structure** :
- Navigation interne par anchors (`#services`, `#team`, `#contact`)
- Sections distinctes visuellement (couleurs alternées ou séparateurs)
- Hero → preuves → offre → CTA → contact
- Single-page SPA OU HTML pur (pas obligatoirement JS)
- Scroll-spy pour highlight de la nav active

**Règle impérative (verbatim)** :
> "Single-page format — tout visible en un scroll" — Bend Law Group

**Anti-patterns** :
- Page > 10 000 px de haut (fatigue scroll)
- Pas d'ancres nommées → impossible de partager un lien profond
- SEO sacrifié (une seule URL = une seule cible)

**Sites de référence** : S24 Bend Law Group (bendlawgroup.com)

**Métrique mesurée** : —

---

### P06 · Grayscale → Color reveal

**Tier** : 3 (premium visuel)
**Secteurs forts** : Portfolios, SEC-06 Trades, construction
**SOIC impacté** : D1 UX (engagement), D5 Performance (CSS hover = gratuit)

**Contexte** : Images/cards présentées en noir et blanc, révélation en couleur au hover. Effet visuel simple CSS mais impactant, applicable à toute galerie de projets.

**Structure** :
- `filter: grayscale(100%)` sur l'image par défaut
- `transition: filter 0.3s ease-out`
- `filter: grayscale(0%)` au `:hover` et `:focus-visible`
- Alternative `prefers-reduced-motion: reduce` → désactive la transition (pas l'état)
- Support tactile : maintenir activé après tap

**Règle impérative (verbatim)** :
> "Cards projets avec effet grayscale → couleur au hover" — Puckett Electric

**Anti-patterns** :
- Transition trop longue (> 500ms) qui ralentit le scan
- Effet appliqué à des photos où le N&B tue le message (ex : food porn)
- Oubli du focus state (clavier)

**Sites de référence** : S27 Puckett Electric (puckettelectric.com)

**Métrique mesurée** : —

---

### P07 · Multi-template portfolio

**Tier** : 2 (sectoriel)
**Secteurs forts** : SEC-02 Créatif, agences multi-service
**SOIC impacté** : D1 UX, D3 Contenu, D6 SEO (pages distinctes)

**Contexte** : Chaque catégorie de service du portfolio a **son propre design**. Montre la polyvalence de l'agence en 4+ templates différents — le site **est** la démo.

**Structure** :
- N landing pages portfolio (N = nombre de catégories, typiquement 3–5)
- Chaque page a sa propre typo, palette, layout
- Navigation racine reste cohérente (couleur neutre)
- Un design system de base partagé (composants de base) mais overrides forts par catégorie

**Règle impérative (verbatim)** :
> "4 pages portfolio avec 4 templates design DIFFÉRENTS" — RyuCreative

**Anti-patterns** :
- Design uniforme qui dit "on fait tout" sans démontrer
- Inconsistance sur la nav racine (utilisateur perdu)
- Perf cassée par 4× tout le CSS

**Sites de référence** : S09 RyuCreative (ryucreative.com)

**Métrique mesurée** : —

---

### P08 · Story-first design

**Tier** : 3 (premium narratif)
**Secteurs forts** : SEC-03 Resto premium, SEC-02 Créatif, agences boutique
**SOIC impacté** : D1 UX, D3 Contenu

**Contexte** : Narrative (histoire, philosophie, parcours) placée **avant** les features / services / menu. Pour positionnements premium ou destination, l'histoire EST le produit.

**Structure** :
- Long-form copy en hero ou section 1 (400–800 mots)
- Photos éditoriales : humains, processus, terroir (pas produit brut)
- Typo serif élégante ou sans-serif premium
- Scroll lent, whitespace généreux
- CTA de réservation / contact placé après l'investissement émotionnel

**Règle impérative (verbatim)** :
> "Story-first design — le parcours et la philosophie avant le menu" — Fiola

**Anti-patterns** :
- Histoire rédigée en corporate-speak ("Notre mission est de…")
- Photos stock qui tuent l'authenticité
- Longueur sans substance (> 1500 mots)

**Sites de référence** : S15 Fiola (fioladc.com), S11 Noma (noma.dk), S20 Clay (clay.global)

**Métrique mesurée** : —

---

### P09 · 3-word brand messaging

**Tier** : 1 (universel)
**Secteurs forts** : SEC-03 Food, retail, SaaS produit
**SOIC impacté** : D1 UX, D3 Contenu, D6 SEO (tagline = meta)

**Contexte** : L'offre entière résumée en **3 mots** (parfois 4). Mémorable, instantané, reconnaissable.

**Structure** :
- Tagline de 3 mots en hero (display bold, très grande taille)
- Alignement avec la personnalité et le produit
- Répétée en meta-description
- Souvent rythme ternaire (adjectif + adjectif + nom/point de différenciation)

**Règle impérative (verbatim)** :
> "Crispy, Juicy, Aloha" — Ma'ono (3 mots qui vendent)

**Anti-patterns** :
- Tagline abstraite ("Innovative solutions for modern businesses")
- 3 mots techniques qui ne disent rien au client final
- Police trop fine pour un impact instantané

**Sites de référence** : S13 Ma'ono (maono.com)

**Métrique mesurée** : —

---

### P10 · Démo interactive hero

**Tier** : 3 (premium SaaS)
**Secteurs forts** : SEC-04 SaaS, Tech
**SOIC impacté** : D1 UX, D5 Performance (JS lourd possible)

**Contexte** : Au lieu d'un screenshot statique, le hero montre le **produit en action** — faux dashboard animé, données qui bougent, interactions possibles. Conversion supérieure à toute image.

**Structure** :
- UI factice mais fonctionnelle (HTML/CSS/JS léger, pas l'app réelle)
- Animation loop ou triggered au scroll
- Responsive (mobile : screenshot animé simplifié)
- Skeleton fallback sur slow connection
- Pas de données personnelles réelles dans la démo

**Règle impérative (verbatim)** :
> "Démo interactive DANS le hero (pas juste un screenshot)" — Monday.com

**Anti-patterns** :
- JS lourd qui casse le LCP (> 3s)
- Données réelles exposées dans la démo
- Démo qui diffère tellement du produit réel que c'est trompeur

**Sites de référence** : S17 Monday.com (monday.com)

**Métrique mesurée** : —

---

### P11 · Page par localisation

**Tier** : 2 (sectoriel)
**Secteurs forts** : SEC-01 Santé multi-locations, SEC-06 Trades multi-villes
**SOIC impacté** : D6 SEO (SEO local), D1 UX

**Contexte** : Une page dédiée par ville / succursale / clinique. Clef du SEO local — chaque page cible une géographie distincte avec NAP (Name, Address, Phone) et contenu unique.

**Structure** :
- URL type `/locations/montreal` ou `/clinics/toronto-bloor`
- H1 avec nom de la ville / succursale
- NAP complet (adresse, téléphone, heures)
- Carte Google embedded
- Reviews locales (Google Reviews API ou manuel)
- Contenu unique par page (pas duplicate content)
- Schema.org `LocalBusiness` + `GeoCoordinates`

**Règle impérative (verbatim)** :
> "Page localisation dédiée par clinique (SEO local)" — Twin Boro

**Anti-patterns** :
- > "Pas duplicate content" — SEO multi-locations (règle verbatim)
- NAP incohérent entre la page et Google My Business
- Schema.org omis

**Sites de référence** : S01 Twin Boro (twinboro.com), S02 Ivy Rehab (ivyrehab.com)

**Métrique mesurée** : —

---

### P12 · Premium palette shift

**Tier** : 2 (repositionnement)
**Secteurs forts** : SEC-06 Trades, services "blue collar"
**SOIC impacté** : D1 UX (perception qualité)

**Contexte** : Utiliser une palette **non-conventionnelle pour le secteur**. Dans un marché où tout le monde utilise bleu/blanc, passer au dark teal ou au noir + or repositionne instantanément en premium. Le design fait le pricing.

**Structure** :
- Palette primaire contre-intuitive (dark teal vs bleu corporate, noir + or vs blanc + bleu)
- Images de projets luxe / détaillées (pas photos d'équipe en uniforme)
- Typo display premium (bold, espacée)
- Signature couleur = reconnaissance de marque

**Règle impérative (verbatim)** :
> "Palette dark teal : positionnement premium dans un secteur typiquement 'blue collar'" — Gibbs Electric

**Anti-patterns** :
- Cliché de secteur respecté → aucune différenciation
- Palette "chic" mais incohérente avec le produit (prix low-cost)
- Contraste AA sacrifié pour l'esthétique

**Sites de référence** : S26 Gibbs Electric (gibbselectric.com), S27 Puckett Electric (palette rouge vif)

**Métrique mesurée** : —

---

### P13 · Anti-polish authenticity

**Tier** : 3 (positionnement)
**Secteurs forts** : SEC-03 Resto artisanal, SEC-02 Créatif
**SOIC impacté** : D1 UX, D3 Contenu

**Contexte** : Design **volontairement brut** — imperfections assumées, photos documentaires (pas studio), typo manuscrite. Contre-pattern puissant pour se différencier des sites "trop léchés".

**Structure** :
- Photos style documentaire / imperfection assumée
- Typo handwritten ou imperfect (Caveat, Patrick Hand, fonts custom)
- Layout avec débordements / rotations légères
- Palette naturelle (terre, crème) + pops inattendus
- Copy conversationnelle ("On fait ça depuis X, venez voir")

**Règle impérative (verbatim)** :
> "Aesthetic intentionnellement 'imparfait'" — Gazzo

**Anti-patterns** :
- Faux anti-polish (photos retouchées pour paraître brutes)
- Navigation sacrifiée au nom de l'esthétique
- Tailles de texte illisibles (< 14px) au nom de la personnalité

**Sites de référence** : S12 Gazzo (gazzo.dk), S30 Kollmann Electric (minimalist trade)

**Métrique mesurée** : —

---

### P14 · Industry code-breaking

**Tier** : 2 (contextuel marché saturé)
**Secteurs forts** : Tous — quand le secteur est saturé visuellement
**SOIC impacté** : D1 UX (mémorabilité)

**Contexte** : Quand toute l'industrie utilise le même template visuel (juridique = marine + or, santé = bleu + blanc, trades = bleu + jaune), **casser les codes** devient un avantage compétitif. Applicable à tout secteur avec conventions rigides.

**Structure** :
- Identifier les 3 codes visuels dominants du secteur
- Proposer une alternative cohérente (pas aléatoire)
- Structure d'info canonique préservée (l'utilisateur doit reconnaître un cabinet d'avocats, même en rose)
- Justification dans le brand-book (pourquoi cette rupture)

**Règle impérative (verbatim)** :
> "Design qui break the mold du juridique traditionnel" — BD&P

**Anti-patterns** :
- Rupture gratuite (aucune cohérence avec le positionnement)
- Rupture qui sacrifie la lisibilité ou la confiance
- Rupture en surface (couleur seulement) sans cohérence structurelle

**Sites de référence** : S23 BD&P (bdplaw.com), S21 Bick Law LLP (bicklawllp.com), S29 Green Electrical (animations dans un secteur statique)

**Métrique mesurée** : —

---

### P15 · Gamified navigation

**Tier** : 3 (premium expérientiel)
**Secteurs forts** : SEC-02 Créatif, portfolios, expérientiel
**SOIC impacté** : D1 UX, D2 Accessibilité (fallback critique), D5 Performance

**Contexte** : L'utilisateur **contrôle l'exploration** — navigation par déplacement, clavier, WebGL, avatar 3D. Extrême du spectre "interactif". Pas réplicable partout mais mémorable.

**Structure** :
- Interaction primaire au-delà du scroll (flèches clavier, drag, WebGL)
- Loading screen qui engage (pas d'attente passive)
- Fallback **obligatoire** : version accessible (liste de liens) pour clavier only, lecteur d'écran, `prefers-reduced-motion`
- Son optionnel (jamais autoplay)
- Performances : mesurer TTI, Three.js < 500ko

**Règle impérative (verbatim)** :
> "Navigation gamifiée — l'acte de browser = exploration" — Bruno Simon

**Anti-patterns** :
- Pas de fallback → exclusion clavier / lecteur d'écran (violation WCAG)
- WebGL > 2Mo → mobile cassé
- Navigation "astucieuse" qui perd l'utilisateur sans carte

**Sites de référence** : S07 Bruno Simon (bruno-simon.com), S08 Space Cowboys (spacewcowboys.com)

**Métrique mesurée** : —

---

### P16 · Legacy authority visuals

**Tier** : 2 (sectoriel)
**Secteurs forts** : SEC-06 Trades, corporate legacy, SEC-05 Juridique méga-cabinet
**SOIC impacté** : D1 UX, D3 Contenu

**Contexte** : Communiquer l'ancienneté par **des visuels** (flotte, bâtiments, photos historiques, stats de résultats) plutôt que par du texte. Le patrimoine visible crée la confiance instantanée.

**Structure** :
- Hero ou section dédiée avec photos : flotte, warehouse, bâtiment, fondateurs
- Stats chiffrées (années, verdicts, projets livrés) en grand format
- Timeline optionnelle
- Certifications / licences visibles

**Règle impérative (verbatim)** :
> "Heritage 100 ans communiqué visuellement (fleet, warehouse)" — Louis Shiffman

**Anti-patterns** :
- Photos stock anonymes (aucune crédibilité)
- Stats non sourcées
- Pages "À propos" perdues dans la nav (patrimoine caché)

**Sites de référence** : S28 Louis Shiffman Electric (shiffmanelectric.com), S22 Quinn Emanuel (quinnemanuel.com)

**Métrique mesurée** : IMA Awards 496/500 (Quinn Emanuel — signal de qualité objective)

---

### P17 · Scroll-triggered animations

**Tier** : 1 (universel)
**Secteurs forts** : Tous
**SOIC impacté** : D1 UX, D2 Accessibilité (`prefers-reduced-motion`), D5 Performance

**Contexte** : Éléments qui apparaissent / s'animent au défilement. Créé par Intersection Observer, pas JS lourd. Dans les secteurs visuellement homogènes, ces animations créent un écart de perception de qualité massif.

**Structure** :
- `IntersectionObserver` (pas de library nécessaire)
- Transitions CSS pures (opacity + translateY)
- Durée 200–600ms, easing naturel
- `@media (prefers-reduced-motion: reduce)` → désactive les transitions
- Seulement à l'entrée (pas toggle au scroll up)
- Pas sur le hero (élément critique LCP)

**Règle impérative (verbatim)** :
> "Animation CSS légère (fade-in au scroll, pas de JS lourd)" — Ivy Rehab

**Anti-patterns** :
- Framer Motion sur 100+ éléments → CLS catastrophique
- Parallax lourd au scroll (layout thrashing)
- Animation au scroll bidirectionnel (désoriente)
- Absence de `prefers-reduced-motion`

**Sites de référence** : S02 Ivy Rehab (ivyrehab.com), S10 Pixelflakes (pixelflakes.com), S29 Green Electrical (greenelectrical.ie)

**Métrique mesurée** : —

---

### P18 · Micro-univers sections

**Tier** : 3 (premium multi-offre)
**Secteurs forts** : SEC-02 Créatif multi-projet, complexes, hôtels, restaurants expérientiels
**SOIC impacté** : D1 UX, D6 SEO (pages par univers = SEO distinct)

**Contexte** : Chaque partie du business a son propre monde visuel dans le même site. Architecture modulaire où chaque section/room/projet est un micro-site avec identité propre.

**Structure** :
- Page racine avec cohérence de navigation
- Sections enfants avec CSS variables override (couleurs, typos, animations propres)
- Nav globale toujours visible (ancrage)
- Transitions entre univers (fade, curtain, dissolve)
- Shared design tokens (spacing, radius) pour cohérence invisible

**Règle impérative (verbatim)** :
> "Chaque projet a son propre univers visuel" — Cappen Studio

**Anti-patterns** :
- Nav globale qui disparaît dans certains univers (utilisateur perdu)
- 6+ univers radicalement différents → cacophonie
- CSS qui fuite entre univers (bugs de style)

**Sites de référence** : S06 Cappen Studio (cappen.com), S08 Space Cowboys (spacewcowboys.com)

**Métrique mesurée** : —

---

### P19 · StoryBrand messaging

**Tier** : 2 (sectoriel B2B)
**Secteurs forts** : SEC-04 SaaS B2B, services pro, agences
**SOIC impacté** : D1 UX, D3 Contenu

**Contexte** : Structure de messaging héritée du framework StoryBrand de Donald Miller. Le client est le héros, vous êtes le guide. Applicable à tout PME B2B qui veut convertir.

**Structure** (5 étapes canoniques) :
1. **Problème** du client — ouverture (hero)
2. **Guide** (votre marque) avec autorité / empathie
3. **Plan** clair (3 étapes simples)
4. **Action** (CTA explicite)
5. **Résultat** (transformation du client — métriques si possibles)

**Règle impérative (verbatim)** :
> "StoryBrand framework appliqué — conversion B2B" — Bop Design

**Anti-patterns** :
- Agence héroïsée (le client doit être le héros)
- Plan en 10 étapes (trop → friction)
- Résultat abstrait ("satisfaction garantie")

**Sites de référence** : S19 Bop Design (bopdesign.com), S16 Monograph (SaaS niche A&E)

**Métrique mesurée** : 420 % augmentation de trafic (case study Bop Design)

---

### P20 · Menu galerie images

**Tier** : 2 (sectoriel restauration)
**Secteurs forts** : SEC-03 Restauration
**SOIC impacté** : D1 UX, D5 Performance (images optimisées)

**Contexte** : Au lieu de lister les plats en texte ou PDF téléchargeable, les montrer en **images**. Navigation visuelle directe, conversion émotionnelle.

**Structure** :
- Grid responsive d'images (3 col desktop, 2 col tablet, 1 col mobile)
- `next/image` avec `sizes` précis (poids < 100ko par image)
- Nom du plat + prix en overlay ou caption
- Filtre par catégorie (entrées, plats, desserts) optionnel
- Clic/tap ouvre un modal / page détail avec ingrédients + allergènes

**Règle impérative (verbatim)** :
> "Menu en format galerie d'images (pas PDF, pas HTML pur)" — La Semilla

**Anti-patterns** :
- PDF téléchargeable comme seul menu (SEO nul, mobile cassé)
- Images > 500ko chacune → CLS + LCP catastrophiques
- Pas d'alt-text sur les plats (accessibilité + SEO)

**Sites de référence** : S14 La Semilla (lasemillanyc.com)

**Métrique mesurée** : —

---

## 5. Les 30 sites de référence (S01–S30)

### SEC-01 · Santé / Physiothérapie

**S01 · Twin Boro Physical Therapy**
- **URL** : https://twinboro.com
- **Style** : Multi-location healthcare, gold standard UX
- **Patterns primaires** : P01 (sticky CTA), P02 (social proof), P11 (pages localisation)
- **6D approx** : D1=3, D2=emotional-cold, D3=medium, D4=cold, D5=still, D6=symmetric
- **Note NEXOS** : Référence absolue santé multi-cliniques. Pages enfant SEO-optimisées par ville, profils thérapeutes détaillés, carousel Google Reviews.

**S02 · Ivy Rehab Network**
- **URL** : https://ivyrehab.com
- **Style** : Network animation-light, SEO massive
- **Patterns primaires** : P17 (scroll animations), P11 (pages localisation)
- **6D approx** : D1=3, D2=emotional-cold, D3=medium, D4=cold, D5=slow-organic, D6=symmetric
- **Note NEXOS** : Animations performantes sans sacrifice de vitesse. Benchmark pour sites à grand volume de pages (500+) qui restent rapides.

**S03 · Athletix Rehab**
- **URL** : https://athletixrehab.com
- **Style** : Clinique sportive spécialisée, branding intense
- **Patterns primaires** : P04 (vidéo hero), P01 (sticky CTA), P12 (palette noire + rouge/orange)
- **6D approx** : D1=3, D2=emotional, D3=heavy, D4=industrial, D5=fast-purposeful, D6=asymmetric-strong
- **Note NEXOS** : Vidéo hero filtre la clientèle cible (athlètes). Pattern réplicable pour tout business de niche voulant qualifier ses visiteurs dès le hero.

**S04 · Stride Sports Physiotherapy**
- **URL** : https://stridesportsphysio.ca
- **Style** : Mobile-first rigoureux, croissance organique
- **Patterns primaires** : P05 (single-page proche), P11 (pages localisation)
- **6D approx** : D1=3, D2=emotional-cold, D3=medium, D4=cold, D5=still, D6=symmetric
- **Note NEXOS** : Cas d'école de croissance organique (0 → #1 local SEO → 4 cliniques). Pattern pour PME santé qui démarrent de zéro.

**S05 · Bloor Jane Physiotherapy**
- **URL** : https://bloorjanephysio.com
- **Style** : Clinique urbaine Toronto, proximity conversion
- **Patterns primaires** : P02 (social proof adjacente — canonique)
- **6D approx** : D1=2, D2=emotional, D3=medium, D4=warm, D5=slow-organic, D6=asymmetric-soft
- **Note NEXOS** : Pattern "social proof adjacente au CTA". Placement proximity double les conversions. **Métrique : 45 → 101 leads/mois (+2×)**.

### SEC-02 · Agence créative

**S06 · Cappen Studio**
- **URL** : https://cappen.com
- **Style** : Scroll immersif, ambient experience (Miami / São Paulo)
- **Patterns primaires** : P18 (micro-univers), P17 (scroll animations)
- **6D approx** : D1=2, D2=technical-warm, D3=contrasted, D4=variable, D5=slow-organic, D6=editorial
- **Note NEXOS** : Architecture modulaire où chaque case study est un micro-univers. Pattern pour agences montrant la diversité sans perdre la cohérence globale.

**S07 · Bruno Simon Portfolio**
- **URL** : https://bruno-simon.com
- **Style** : Portfolio WebGL 3D, navigation voiture
- **Patterns primaires** : P15 (gamified navigation)
- **6D approx** : D1=1, D2=emotional, D3=light, D4=variable, D5=fast-purposeful, D6=editorial
- **Note NEXOS** : Extrême du spectre "interactif". Pas réplicable tel quel, mais le concept "navigation = expérience" est un pattern puissant. Référence plafond interactivité. Awwwards SOTM Janvier 2026.

**S08 · Space Cowboys**
- **URL** : https://spacewcowboys.com
- **Style** : Gamified case studies, VR-like showroom (NYC)
- **Patterns primaires** : P15 (gamified), P18 (micro-univers)
- **6D approx** : D1=1, D2=technical-warm, D3=heavy, D4=industrial, D5=fast-purposeful, D6=editorial
- **Note NEXOS** : L'utilisateur contrôle physiquement l'exploration des projets. Navigation clavier (flèches). Applicable à tout portfolio qui veut être mémorable.

**S09 · RyuCreative**
- **URL** : https://ryucreative.com
- **Style** : Images dispersées hero + portfolio catégorisé 4 templates (LA)
- **Patterns primaires** : P07 (multi-template portfolio)
- **6D approx** : D1=2, D2=emotional, D3=contrasted, D4=variable, D5=slow-organic, D6=asymmetric-strong
- **Note NEXOS** : Chaque catégorie de service a son propre design, montrant la polyvalence. Réplicable pour toute agence multi-service. Branding féminin assumé.

**S10 · Pixelflakes**
- **URL** : https://pixelflakes.com
- **Style** : Vidéo rires/sourires + kinetic typography + gradient design
- **Patterns primaires** : P04 (vidéo émotionnelle), P17 (scroll animations)
- **6D approx** : D1=2, D2=emotional, D3=contrasted, D4=variable, D5=fast-purposeful, D6=asymmetric-soft
- **Note NEXOS** : Humanisation par la vidéo. Le visiteur ressent ce que serait de travailler avec l'équipe. Pattern puissant pour PME de services.

### SEC-03 · Restauration

**S11 · Noma**
- **URL** : https://noma.dk
- **Style** : Minimalisme absolu, images saisonnières (Copenhague)
- **Patterns primaires** : P08 (story-first), P13 (anti-polish / minimal)
- **6D approx** : D1=1, D2=emotional, D3=light, D4=warm, D5=still, D6=symmetric
- **Note NEXOS** : Le minimalisme comme luxe. Zéro bruit visuel. L'image saisonnière est un pattern programmatique réplicable. Restaurant Michelin fermé mais référence éternelle.

**S12 · Gazzo**
- **URL** : https://gazzo.dk
- **Style** : Raw, playful, anti-polish (Copenhague)
- **Patterns primaires** : P13 (anti-polish authenticity — canonique)
- **6D approx** : D1=3, D2=emotional, D3=contrasted, D4=warm, D5=slow-organic, D6=asymmetric-soft
- **Note NEXOS** : Site volontairement brut pour communiquer l'authenticité artisanale. Contre-pattern puissant vs sites "trop léchés" dans le food.

**S13 · Ma'ono**
- **URL** : https://maono.com
- **Style** : Jaune bold + photo hero surdimensionnée (Seattle Hawaiian)
- **Patterns primaires** : P09 (3-word messaging "Crispy, Juicy, Aloha"), P12 (palette bold signature)
- **6D approx** : D1=2, D2=emotional, D3=heavy, D4=industrial, D5=fast-purposeful, D6=symmetric
- **Note NEXOS** : 3-word brand messaging. Le produit parle en 3 mots. Couleur signature bold = reconnaissance instantanée.

**S14 · La Semilla**
- **URL** : https://lasemillanyc.com
- **Style** : Plant-based latin, menu galerie images (NYC)
- **Patterns primaires** : P20 (menu galerie), P14 (industry code-breaking — restaurant design-forward)
- **6D approx** : D1=2, D2=emotional, D3=contrasted, D4=warm, D5=slow-organic, D6=editorial
- **Note NEXOS** : Menu en format galerie d'images. La typo quirky comme branding primaire — la police EST l'identité.

**S15 · Fiola (Fabio Trabocchi)**
- **URL** : https://fioladc.com
- **Style** : Fine dining italien, story-first, lottery booking (Washington DC)
- **Patterns primaires** : P08 (story-first)
- **6D approx** : D1=1, D2=emotional, D3=light, D4=warm, D5=slow-organic, D6=symmetric
- **Note NEXOS** : Story-first restaurant. Pour les restaurants destination, l'histoire EST le produit. Long-form copy célèbre le journey. Applicable à tout business premium/expérientiel.

### SEC-04 · Gestion de projet / SaaS

**S16 · Monograph**
- **URL** : https://monograph.com
- **Style** : SaaS niche verticale pour architectes/ingénieurs
- **Patterns primaires** : P19 (StoryBrand messaging niche)
- **6D approx** : D1=3, D2=technical, D3=medium, D4=cold, D5=fast-purposeful, D6=symmetric
- **Note NEXOS** : Tout le messaging est pour UNE audience. Pas "project management" générique mais "for A&E firms". Pattern puissant pour tout SaaS B2B niche.

**S17 · Monday.com**
- **URL** : https://monday.com
- **Style** : SaaS grand public, démo interactive
- **Patterns primaires** : P10 (démo interactive hero), P02 (social proof logos Fortune 500)
- **6D approx** : D1=3, D2=emotional, D3=medium, D4=variable, D5=fast-purposeful, D6=symmetric
- **Note NEXOS** : Démo interactive dans le hero — produit en action, pas screenshot. Conversion supérieure à toute image statique. CTA "Get Started" répété 10+ fois.

**S18 · Productive.io**
- **URL** : https://productive.io
- **Style** : SaaS all-in-one, angle profitabilité
- **Patterns primaires** : P19 (StoryBrand, angle financier)
- **6D approx** : D1=4, D2=technical, D3=medium, D4=cold, D5=fast-purposeful, D6=symmetric
- **Note NEXOS** : Au lieu de vendre la gestion de projet, vendre la profitabilité. Le reframing du bénéfice change tout le messaging. Applicable à tout SaaS B2B.

**S19 · Bop Design**
- **URL** : https://bopdesign.com
- **Style** : Agence B2B conversion-first
- **Patterns primaires** : P19 (StoryBrand), P02 (case studies métrisés)
- **6D approx** : D1=3, D2=technical, D3=heavy, D4=cold, D5=fast-purposeful, D6=symmetric
- **Note NEXOS** : StoryBrand framework universel. Structure : problème → guide → plan → action → résultat. Case studies avec métriques concrètes (420 % trafic).

**S20 · Clay**
- **URL** : https://clay.global
- **Style** : Agence design premium (SF)
- **Patterns primaires** : P08 (story-first), P17 (scroll fluides)
- **6D approx** : D1=1, D2=emotional-cold, D3=light, D4=cold, D5=slow-organic, D6=symmetric
- **Note NEXOS** : Quality signals implicites — l'exécution du site EST l'argument. Pas de badges, pas de "10 raisons". Whitespace comme élément de luxe. Pour agences visant le haut de gamme.

### SEC-05 · Juridique

**S21 · Bick Law LLP**
- **URL** : https://bicklawllp.com
- **Style** : Cabinet droit environnemental, animations mono→couleur
- **Patterns primaires** : P14 (code-breaking jur), P17 (scroll animations)
- **6D approx** : D1=3, D2=emotional, D3=light, D4=warm, D5=slow-organic, D6=symmetric
- **Note NEXOS** : Design = message. La spécialisation environnementale est communiquée par les visuels (nature) plutôt que par le texte. Nominé Webby Award.

**S22 · Quinn Emanuel**
- **URL** : https://quinnemanuel.com
- **Style** : Méga-cabinet (1200+ avocats, 34 bureaux)
- **Patterns primaires** : P16 (legacy authority — verdicts milliards), P02 (stats résultats)
- **6D approx** : D1=5, D2=technical, D3=heavy, D4=cold, D5=still, D6=symmetric
- **Note NEXOS** : Information architecture à grande échelle. Comment organiser 1000+ entités de manière navigable. IMA Awards 496/500. Blueprint pour tout site avec catalogue volumineux.

**S23 · BD&P (Burnet Duckworth & Palmer)**
- **URL** : https://bdplaw.com
- **Style** : Cabinet mid-size Calgary, parallax + code-breaking
- **Patterns primaires** : P14 (code-breaking), P17 (parallax)
- **6D approx** : D1=3, D2=technical, D3=medium, D4=cold, D5=slow-organic, D6=asymmetric-soft
- **Note NEXOS** : Casse volontairement les codes visuels juridiques. Quand toute l'industrie utilise le même template, le casser = avantage compétitif. Applicable à tout secteur à conventions rigides.

**S24 · Bend Law Group**
- **URL** : https://bendlawgroup.com
- **Style** : Single-page scroll, ciblé startups (SF)
- **Patterns primaires** : P05 (single-page)
- **6D approx** : D1=2, D2=emotional, D3=medium, D4=warm, D5=slow-organic, D6=asymmetric-soft
- **Note NEXOS** : Single-page legal. Prouve qu'un cabinet peut être accessible avec une seule page bien structurée. Parfait pour cabinets boutique et PME de services professionnels.

**S25 · Hudgell Solicitors**
- **URL** : https://hudgellsolicitors.co.uk
- **Style** : Cabinet multi-spécialités UK, color-coded par domaine
- **Patterns primaires** : P03 (color-coded navigation), P04 (vidéo / podcasts)
- **6D approx** : D1=4, D2=emotional, D3=medium, D4=variable, D5=slow-organic, D6=symmetric
- **Note NEXOS** : Color-coding par domaine → navigation intuitive sans lire. Podcasts + vidéos + articles comme canaux alternatifs. **Design a doublé les conversions YoY**. Digital Impact Award.

### SEC-06 · Électrique industriel

**S26 · Gibbs Electric Company**
- **URL** : https://gibbselectric.com
- **Style** : Entrepreneur luxe, dark teal premium (San Diego)
- **Patterns primaires** : P12 (premium palette shift)
- **6D approx** : D1=2, D2=technical-warm, D3=heavy, D4=cold, D5=slow-organic, D6=asymmetric-soft
- **Note NEXOS** : Premium trade positioning. Palette non-conventionnelle (dark teal vs bleu/blanc) repositionne instantanément un business trade comme premium. **Le design fait le pricing.**

**S27 · Puckett Electric**
- **URL** : https://puckettelectric.com
- **Style** : Parallax + grayscale→couleur hover (rouge vif primaire)
- **Patterns primaires** : P06 (grayscale→couleur), P12 (palette mémorable)
- **6D approx** : D1=3, D2=technical-warm, D3=heavy, D4=industrial, D5=fast-purposeful, D6=asymmetric-soft
- **Note NEXOS** : Grayscale-to-color hover reveal. Les projets en N&B se révèlent au survol. Effet CSS simple mais impactant, applicable à toute galerie. Rouge vif unique dans l'électrique.

**S28 · Louis Shiffman Electric**
- **URL** : https://shiffmanelectric.com
- **Style** : Legacy 100 ans NYC, fleet + warehouse (contractor + fournisseur)
- **Patterns primaires** : P16 (legacy authority)
- **6D approx** : D1=4, D2=technical, D3=medium, D4=cold, D5=still, D6=symmetric
- **Note NEXOS** : Double positionnement contractor + supplier (rare). Legacy communiquée par flotte + entrepôt + photos historiques. Le patrimoine visible crée la confiance instantanée.

**S29 · Green Electrical**
- **URL** : https://greenelectrical.ie
- **Style** : Animations scroll dans un secteur statique (Irlande)
- **Patterns primaires** : P17 (scroll animations), P14 (code-breaking trades)
- **6D approx** : D1=3, D2=technical-warm, D3=medium, D4=warm, D5=fast-purposeful, D6=asymmetric-soft
- **Note NEXOS** : Animated trade site. Les animations scroll (que les concurrents n'utilisent jamais) créent un écart de perception de qualité massif dans un secteur visuellement homogène.

**S30 · Kollmann Electric**
- **URL** : https://kollmannelectric.com
- **Style** : Minimaliste pur, white space dominant
- **Patterns primaires** : P13 (anti-polish minimal), P14 (code-breaking by restraint)
- **6D approx** : D1=1, D2=technical, D3=light, D4=cold, D5=still, D6=symmetric
- **Note NEXOS** : Quand tous les concurrents surchargent leurs pages, le minimalisme radical devient le signal de qualité premium. Less = more = confiance. Pattern "minimalist trade".

## 6. Matrice patterns × secteurs (tier recommandé)

| Pattern                         | SEC-01 Santé | SEC-02 Créatif | SEC-03 Resto | SEC-04 SaaS | SEC-05 Jur | SEC-06 Trades |
|---------------------------------|:-:|:-:|:-:|:-:|:-:|:-:|
| P01 Sticky CTA                  | **1** | 2 | 2 | 2 | **1** | **1** |
| P02 Social proof adjacente      | **1** | 2 | 2 | **1** | **1** | **1** |
| P03 Color-coded navigation      | 3 | 2 | 3 | 2 | **1** | 3 |
| P04 Hero vidéo émotionnelle     | 2 | **1** | 2 | 3 | 3 | 3 |
| P05 Single-page scroll          | 3 | 2 | 3 | 3 | 2 | 2 |
| P06 Grayscale→Color reveal      | 3 | **1** | 3 | 3 | 3 | **1** |
| P07 Multi-template portfolio    | 3 | **1** | 3 | 2 | 3 | 3 |
| P08 Story-first design          | 3 | 2 | **1** | 2 | 3 | 3 |
| P09 3-word brand messaging      | 2 | 2 | **1** | **1** | 2 | 2 |
| P10 Démo interactive hero       | 3 | 2 | 3 | **1** | 3 | 3 |
| P11 Page par localisation       | **1** | 3 | 2 | 3 | 2 | **1** |
| P12 Premium palette shift       | 2 | 2 | 2 | 2 | 2 | **1** |
| P13 Anti-polish authenticity    | 3 | 2 | **1** | 3 | 3 | 2 |
| P14 Industry code-breaking      | 2 | 2 | 2 | 2 | **1** | 2 |
| P15 Gamified navigation         | 3 | **1** | 3 | 3 | 3 | 3 |
| P16 Legacy authority visuals    | 2 | 3 | 3 | 3 | 2 | **1** |
| P17 Scroll-triggered animations | **1** | **1** | **1** | **1** | **1** | **1** |
| P18 Micro-univers sections      | 3 | 2 | 3 | 3 | 3 | 3 |
| P19 StoryBrand messaging        | 2 | 2 | 3 | **1** | 2 | 2 |
| P20 Menu galerie images         | — | 3 | **1** | 3 | — | 3 |

**Lecture** : `1` = hautement recommandé (tier 1 universel ou tier sectoriel fort) · `2` = contextuel (tier 2) · `3` = optionnel premium (tier 3) · `—` = non applicable.

## 7. Anti-patterns transverses (à éviter TOUS SECTEURS)

**Citations verbatim (sources à indiquer)** :
- > "PAS de stock footage" — Pixelflakes (S10)
- > "Pas de bruit visuel" — Clay (S20) / Noma (S11)
- > "Pas duplicate content" — SEO multi-locations (règle générale)
- > "Ne jamais séparer social proof et CTA" — Bloor Jane (S05)

**Anti-patterns courants à refuser en Ph2/Ph3** :
- Stock photos "team smiling" interchangeables — tue la crédibilité
- Carousel testimonials sans source vérifiable (nom + photo + rôle)
- CTA disparaît au scroll sans raison ergonomique
- Framer Motion appliqué à 100+ éléments → CLS catastrophique
- WebGL / 3D sans fallback accessible (violation WCAG)
- PDF téléchargeable comme seule source (menu, tarifs, etc.) — SEO nul, mobile cassé
- Video hero autoplay **avec son** → UX et RGPD
- Animation omise sur `prefers-reduced-motion: reduce` → violation WCAG 2.3.3

## 8. Checklist d'audit NEXOS (dérivée)

### Phase 1 — Universels (tier 1, s'appliquent à tout projet)
- [ ] P01 Sticky CTA présent, accessible (aria-label, focus-visible, contraste AA)
- [ ] P02 Social proof adjacente au CTA primaire (pas reléguée au footer)
- [ ] P17 Animations scroll via IntersectionObserver, **avec** `prefers-reduced-motion: reduce`
- [ ] P09 3-word brand messaging ou équivalent percutant en hero
- [ ] Hero value prop lisible en < 5 s
- [ ] LCP < 2.5 s (budget Lighthouse)

### Phase 2 — Secteur (selon SEC-XX du brief)
- [ ] Patterns tier 1 du secteur appliqués (voir matrice §6)
- [ ] 6D assignée et cohérente avec le client NEXOS cible
- [ ] Au moins 1 pattern sectoriel clef documenté dans `ph1-strategy-report.md`

### Phase 3 — Différenciation / Premium (optionnel tier 3)
- [ ] Test règle d'or : le site s'oppose à ≥ 4 dimensions par rapport à un autre client NEXOS existant
- [ ] Pas de duplication stricte d'un site de référence (inspiration OK, copie NON)
- [ ] Si P15 ou P18 utilisés : fallbacks accessibilité vérifiés
- [ ] Budget perf respecté malgré les effets premium

## 9. Liens avec agents NEXOS consommateurs

| Agent                                        | Usage de cette knowledge                                           |
|----------------------------------------------|--------------------------------------------------------------------|
| `agents/ph1-strategy/pattern-recommender.md` | Source primaire : matrice §6 + sites ref §5 + 6D §3 (Phase D produira cet agent) |
| `agents/ph1-strategy/brand-strategist.md`    | 6D §3 pour positionnement palette / typo / motion                  |
| `agents/ph2-design/*`                        | Patterns visuels : P04, P06, P07, P12, P17, P18                    |
| `agents/ph3-content/*`                       | Patterns messaging : P08, P09, P19, P20                            |
| `agents/ph5-qa/*`                            | Checklist d'audit §8, anti-patterns §7                             |

## 10. Changelog interne du référentiel

| Version | Date       | Auteur           | Changes                                                                          |
|---------|------------|------------------|----------------------------------------------------------------------------------|
| 1.0.0   | 2026-04-16 | NEXOS phase B    | Création initiale depuis `NEXOS_Web_Patterns_Reference.md` + feed + contexte.txt |
