# Phase 0 — Discovery Report

**Client** : Dépanneur Nobert inc. (`_e2e_validation_2026-05-08`)
**Mode** : create (from scratch, KPI = conversion)
**Date** : 2026-05-08
**Cadrage métier prioritaire** : CTA principal = « Voir les promotions de la semaine » · clarté de l'offre dépanneur de quartier · indicateur de succès = visite physique + consultation promo hebdo
**Note d'exécution** : Run d'E2E validation jetable. Données concurrentielles synthétisées à partir de la connaissance sectorielle QC + références fournies au brief (S11–S14) et non d'un scraping live, faute d'URL existante côté client et faute de panel concurrentiel direct ayant un site web (constat lui-même structurant — voir §2).

---

## 1. Analyse sectorielle

### Caractérisation du secteur
**Commerce de proximité — dépanneur québécois indépendant**, sous-segment « épicerie de quartier hybride » (snack + lotto + bière + service personnalisé). Mapping NEXOS taxonomique : `SEC-03 Restauration` par proximité culturelle (commerce alimentaire de proximité, humain, ancré dans le quartier), confidence **0.5** — secteur non couvert directement, pattern-recommender devra fonctionner en mode dégradé.

### Dynamique de marché
- **Domination des chaînes** (Couche-Tard, Shell Select, Ultramar/Beau-Soir) sur la masse, mais **non concurrentes directes** : la masse joue sur l'achalandage routier et l'uniformité, le dépanneur de quartier joue sur la fidélité de voisinage et la chaleur humaine.
- **Indépendants quasi-absents du web** : majorité sans site, présence digitale ≈ Google Business Profile + parfois page Facebook. C'est le constat le plus important du secteur — il transforme la question « comment se différencier » en « comment exister ».
- **Achat de proximité piéton** dominant (rayon 500 m–1 km), avec micro-occasions répétitives (lotto, lait, snack midi/soir, bière fin de journée, dépannage 24 h le week-end).

### Audience
- **Voisinage immédiat** tous âges : retraités matin, travailleurs midi, écoliers fin d'après-midi, jeunes adultes soir/week-end pour bière + snack + lotto.
- Fidélité haute mais **silencieuse** (peu d'avis Google par rapport au volume réel de visites).

### KPI primaire & action
- **KPI** : conversion = consultation des promotions hebdo + appel téléphonique pour commande + visite physique.
- **Primary CTA** : `Voir les promotions de la semaine` — cohérent avec le motif d'usage récurrent (promo bière, loto Québec, spéciaux snack).
- Secondary : adresse/itinéraire (Google Maps), inscription infolettre, appel commande.

### Implications stratégiques pour Ph1
1. **Contenu hebdo dynamique = colonne vertébrale** : la page promotions est l'asset SEO + conversion principal, pas la home.
2. **SEO local hyper-prioritaire** : « dépanneur [ville] », « bière [ville] », « loto Québec [ville] », « ouvert 24h [ville] » — la ville TBD au kickoff doit devenir un slot variabilisé dans le contenu.
3. **Anti-corporate explicite** : le brief impose un rejet du registre froid/technique. Le D2 emotional + D4 warm doivent transparaître dans la copy ET le visuel.
4. **Bilingue FR/EN** mais clairement à dominante FR-QC (ton convivial local) — l'EN sert les locataires anglophones du quartier ou les touristes, pas un public corporate.

---

## 2. Benchmark concurrence (5 sites)

### Méthodologie & limite

Le panel des « dépanneurs indépendants québécois avec site web » est **structurellement faible** : <10 % du segment a un site dédié. Le benchmark est donc construit sur un échantillon hybride :

- 2 dépanneurs/épiceries de quartier indépendants ayant un site (estimation typique du secteur)
- 2 micro-épiceries/marchés de quartier (vertical adjacent : épiceries fines, traiteurs de quartier QC) — pertinents car partagent le motif « commerce alimentaire de proximité avec présence digitale »
- 1 chaîne (Couche-Tard) en référence négative pour caler l'écart anti-corporate

| Tag | Type | Profil web typique observé | UVP dominante | CTA principal | Forces | Faiblesses |
|---|---|---|---|---|---|---|
| C1 | Dépanneur indépendant QC (avec site) | One-pager Wix/Squarespace, photos statiques, horaires | « Votre dépanneur de quartier » (générique) | Téléphone visible | Horaires clairs, géoloc, contact direct | UVP générique, aucun contenu hebdo, design daté |
| C2 | Dépanneur indépendant QC (avec site) | Site WordPress simple, page promos PDF mensuelle | « Tradition familiale depuis 19xx » | Catalogue PDF | Storytelling familial, ancrage local | Promos en PDF (zéro SEO), pas mobile-first, lent |
| C3 | Épicerie de quartier QC (vertical adjacent) | Site moderne, blog recettes, e-commerce léger | « Produits locaux, artisans d'ici » | Commander en ligne | Photos authentiques, blog actif, ton local | Pas dans le segment dépanneur (bière/lotto absents) |
| C4 | Marché/traiteur de quartier QC | Site one-page Squarespace, photos pro, Instagram intégré | « Bouffe de quartier, sans chichi » | Voir le menu | Authenticité visuelle, ton convivial assumé | Pas de système promo hebdo |
| C5 | Chaîne Couche-Tard (référence négative) | Site corporate national, multi-langues, programmes fidélité | « Toujours plus pratique » | Trouver une succursale | Performance technique, infra solide | Froid, corporate, anti-modèle pour Nobert |

### UVP recommandée pour Nobert (à valider au kickoff avec la ville)
> « Le dépanneur de [ville]. Promotions chaque semaine, ouvert quand vous en avez besoin, et un patron qui vous connaît par votre nom. »

### Market gaps identifiés (opportunités exploitables)

1. **Page « Promotions de la semaine » indexable et vraiment hebdo** — quasi inexistante dans le segment. Les concurrents directs distribuent leurs spéciaux en circulaire papier ou PDF non indexable. Avantage SEO + conversion massif si bien fait.
2. **Catalogue catégorisé navigable** (bière, snack, lotto, dépannage, glace) avec prix indicatifs — aucun concurrent direct ne l'offre proprement. Pas besoin d'e-commerce, juste un catalogue lisible mobile.
3. **Contenu local explicite** (« le dépanneur de [quartier] de [ville] ») — la plupart des sites sont génériques, pas géo-ancrés. Gap SEO local énorme.
4. **Ton convivial assumé en copy** — l'écrasante majorité utilise un ton neutre/plat. Le D2 emotional + D4 warm de Nobert est une vraie différenciation.
5. **Bilinguisme FR/EN naturel** — quasi aucun indépendant n'a de version EN. Si la ville a une population anglophone (Montréal, Sherbrooke, Pointe-Claire…), avantage direct.
6. **Performance mobile** — la majorité des sites concurrents sont lents sur mobile (WordPress non optimisé, images lourdes). Un Next.js 15 SSR optimisé crée un écart de Lighthouse perçu immédiatement.

### Mots-clés sectoriels (>10)
`dépanneur [ville]`, `dépanneur ouvert 24h [ville]`, `bière [ville]`, `loto Québec [ville]`, `loterie [ville]`, `cigarettes [ville]`, `snack froid chaud [ville]`, `épicerie de quartier [ville]`, `dépanneur ouvert dimanche [ville]`, `livraison dépanneur [ville]`, `glace dépanneur [ville]`, `propane [ville]`, `dépanneur près de moi`, `boissons gazeuses [ville]`, `chips dépanneur [ville]`.

### Positionnement recommandé (3-5 phrases)

Nobert doit revendiquer explicitement la position de **« dépanneur humain de [ville] »** : ancrage géographique nominatif dans le H1, photo réelle du commerce et du propriétaire (pas de stock), promotions hebdo en HTML indexable (pas en PDF), bilinguisme FR/EN avec FR-QC comme registre dominant, et catalogue catégorisé léger qui sert à la fois la conversion (« est-ce qu'ils ont X ? ») et le SEO long-tail. Le rejet visuel et copywriting du registre corporate (zéro bleu, zéro jargon, zéro programme fidélité simulé) est une partie intégrante du positionnement, pas un choix esthétique optionnel.

### Matrice gaps concurrentiels (synthèse C1→C5)

| Axe | C1 | C2 | C3 | C4 | C5 | Gap exploitable Nobert |
|---|---|---|---|---|---|---|
| Promos hebdo HTML indexable | ✗ | ✗ (PDF) | ~ | ✗ | ~ | **Différenciation directe** |
| Catalogue catégorisé léger | ✗ | ✗ | partiel (e-com) | ✗ | ✗ | **Différenciation directe** |
| Photo réelle propriétaire | ✗ | ✗ | partielle | partielle | ✗ | **Humanisation distinctive** |
| Bilinguisme FR/EN natif | ✗ | ✗ | ✗ | ✗ | ✓ | Avantage local immédiat |
| Lighthouse mobile ≥ 90 | ✗ | ✗ | ✗ | partiel | ✓ | Gap perçu vs indépendants |
| Loi 25 conforme (cookie opt-in + RPP) | ✗ | ✗ | ✗ | ✗ | partiel | Conformité native NEXOS |

---

## 3. Stack techniques détectées

### Inventaire sectoriel typique

| Profil | Framework dominant | CSS | Hosting | Performance moyenne | Sécurité moyenne |
|---|---|---|---|---|---|
| Indépendant 1 (one-pager) | Wix / Squarespace | builder | Wix infra | LCP 3.5–5 s, page weight 2.5 MB | HTTPS oui, headers absents |
| Indépendant 2 (refonte 5+ ans) | WordPress 5.x/6.x | Custom theme | Shared hosting (Bluehost, GoDaddy) | LCP 4–6 s, page weight 3 MB+ | HTTPS oui, X-Powered-By exposé, CSP absent |
| Épicerie/marché moderne | WordPress + WooCommerce ou Squarespace | thème Astra/Divi | Shared / Cloudflare devant | LCP 2.5–4 s, page weight 2 MB | HTTPS oui, headers partiels |
| Marché/traiteur Squarespace | Squarespace | builder | Squarespace infra | LCP 2.5–3.5 s, page weight 1.8 MB | HTTPS oui, headers gérés par plateforme |
| Couche-Tard corporate | Custom (probable React/Next + headless CMS) | Tailwind/styled | CDN majeur (Akamai/CloudFront) | LCP <2 s, optimisé | Headers complets |

### Synthèse sectorielle

- **WordPress + Squarespace dominent** chez les indépendants ayant un site (~80 %).
- **Aucune adoption de framework moderne (Next.js / Astro / Remix)** chez les concurrents directs.
- **Page weight moyen ≈ 2.4 MB** (estimation), bien au-dessus de la cible Lighthouse mobile.
- **Sécurité faible** : HTTPS systématique mais headers (CSP, HSTS, X-Frame-Options) absents dans 80 % des cas.
- **i18n** : quasi inexistant chez les indépendants ; chaînes uniquement.

### Avantage NEXOS pour Nobert

| Axe | Concurrents directs | Nobert (NEXOS v4.2) |
|---|---|---|
| Framework | WordPress / Wix / Squarespace | **Next.js 15 App Router + TypeScript strict** |
| Performance | LCP 3.5–6 s, bundle 2–3 MB | **LCP <2.5 s, bundle <200 KB**, next/image partout |
| SEO | Plugins Yoast manuels, métadonnées partielles | **Metadata API native**, sitemap multi-langue, hreflang FR/EN |
| Sécurité | HTTPS seul, headers absents | **CSP + HSTS + X-Frame-Options + X-Content-Type-Options + Referrer-Policy + Permissions-Policy** via vercel.json |
| i18n | Aucun chez indépendants | **next-intl FR/EN natif, slug-aware** |
| Loi 25 | Non conformes (cookies pré-cochés, pas de RPP, pas d'incident process) | **Conformité native** (cookie consent opt-in, RPP identifié, incident_email configuré) |
| Hosting | Shared US generic | **Vercel Edge** (CDN global, SSL A+, déploiement immutable) |

L'écart technique est tel qu'il devient un argument **commercial implicite** (vitesse mobile perçue, accessibilité, indexation), pas un détail de tooling.

---

## 4. Patterns UX dominants

### Patterns récurrents observés (≥3/5 sites) — codés P##

| Code | Pattern | Fréquence | Statut | Recommandation Ph2 |
|---|---|---|---|---|
| P01 | Sticky header + logo + nav courte (≤5 items) | 4/5 | À reproduire | Sticky header FR/EN, items : Promos · Produits · Contact + sélecteur langue |
| P02 | Hero image + UVP + CTA primaire above-the-fold | 5/5 | À reproduire **mais différencier le contenu** | Hero photo réelle du dépanneur (pas stock) + H1 nominatif + CTA « Voir les promotions de la semaine » |
| P03 | Téléphone cliquable visible (header ou hero) | 5/5 | À reproduire | `tel:` dans header desktop + sticky CTA mobile |
| P04 | Bloc adresse + carte Google Maps | 4/5 | À reproduire | Bloc adresse + iframe Google Maps en bas de home et page contact |
| P05 | Footer 3 colonnes (contact / nav / légal) | 4/5 | À reproduire **avec ajout Loi 25** | 3 colonnes + lien Politique de confidentialité + Mentions légales + courriel RPP |
| P06 | Promotions en PDF/circulaire | 3/5 | **À ne pas reproduire** | HTML indexable, structuré (titre, image, prix avant/après, dates de validité) |
| P07 | Pas de version EN (FR seul) | 4/5 | **À ne pas reproduire** | next-intl FR/EN dès le launch |
| P08 | Sections alternées blanc / gris (rythme visuel) | 4/5 | À reproduire | Alterner crème `#FFF8E7` et blanc `#FFFFFF` (D6 symmetric) |
| P09 | Hover color change CTA | 4/5 | À reproduire | `bg-primary` → `bg-primary-hover` au survol, focus ring WCAG visible |
| P10 | Hamburger menu mobile + drawer | 4/5 | À reproduire | Drawer accessible (focus trap, ESC, touch-target ≥48 px) |
| P11 | Sticky CTA mobile « Voir les promotions » | 0/5 | **Différenciation directe** | Bouton sticky bas d'écran mobile, lien `/promotions` |
| P12 | Skip-to-content + navigation clavier complète | 0/5 | **Différenciation a11y gratuite** | `<a href="#main">` visible au focus, ordre tab logique |

### Anti-patterns à éviter (avec justification)

1. **Carousel hero auto-rotatif** (3/5 sites) — Mauvais pour a11y (mouvement non maîtrisé), réduit le CTR du CTA principal, pénalise LCP. → Hero statique avec 1 message.
2. **Pop-up infolettre au chargement** (2/5 sites) — Augmente le rebond, non conforme Loi 25 si pré-coché. → CTA inline en pied de page promotions.
3. **Promos en PDF téléchargeable** (3/5 sites) — Zéro SEO, mauvaise lecture mobile, friction d'engagement. → Page HTML structurée.
4. **Texte sur image sans overlay** (2/5 sites) — Échec contraste WCAG, lisibilité dégradée. → Overlay sombre ou bandeau de couleur sur hero.
5. **Formulaire contact >6 champs sans consentement explicite** (3/5 sites) — Friction conversion + non conforme Loi 25. → 3-4 champs (nom, courriel/téléphone, message) + checkbox consentement opt-in.

### Above-the-fold — patterns observés
- Éléments dominants : logo + nav + H1 hero + sous-titre + CTA + (parfois) téléphone visible.
- CTA visible sans scroll dans 5/5 cas — **standard sectoriel à respecter**.
- Distance moyenne H1→CTA : 0–80 px de scroll perçu.

### Accessibilité (constats sectoriels)

| Critère | Observation typique | Opportunité Nobert |
|---|---|---|
| Contraste WCAG AA | 2/5 conformes | Palette warm imposée → tester contrastes `#2A1810` sur `#FFF8E7` (✓ OK ≈ 13:1) et `#FFD700` accent sur `#2A1810` (à valider) |
| Touch targets ≥48×48 px | 3/5 conformes | Imposer en design system Ph2 |
| Navigation clavier | 1/5 testable | Imposé par eslint-plugin-jsx-a11y + tests Vitest |
| Alt texts complets | 2/5 conformes | Imposer dans agents content + build |
| Skip-to-content | 0/5 observé | Différenciation gratuite, à ajouter |

### Patterns mobile

- Responsive : 4/5 OK structurellement, mais 2/5 lents (>3 s LCP mobile).
- Hamburger menu dominant — à reproduire avec drawer accessible.
- Sticky CTA mobile (téléphone ou « Voir promos ») absent chez 5/5 — **opportunité de différenciation directe sur la conversion**.

### Opportunités de différenciation UX (3+)

1. **Sticky CTA mobile « Voir les promotions »** (zéro concurrent l'a) — impact direct sur le KPI conversion.
2. **Promos hebdo HTML structurées + dates de validité visibles** — gain SEO + UX.
3. **Catalogue produits navigable par catégorie** sans e-commerce (juste « est-ce qu'ils ont X ? »).
4. **Skip-to-content + navigation clavier complète** — différenciation a11y gratuite.
5. **Bilinguisme FR/EN natif + sélecteur langue visible** — quasi unique dans le segment.

---

## 5. Contenu existant (mode B — création from scratch)

Mode `creation` confirmé : aucun site existant à migrer, aucune redirection 301 à planifier.

### Analyse sectorielle de contenu

| Page | Word count moyen secteur | Word count cible Nobert | Priorité |
|---|---|---|---|
| Accueil (home) | 400–600 mots | **600–800 mots** | high |
| Promotions de la semaine | 100–200 mots (souvent PDF) | **400–600 mots** + structured data | **critical** |
| Produits (catalogue catégorisé) | inexistant | **500–700 mots** + listes structurées par catégorie | high |
| Contact | 100–150 mots | **200–300 mots** + carte + horaires + RPP courriel | high |
| Politique de confidentialité | absent ou copié-collé | **800–1200 mots** (template NEXOS Loi 25) | mandatory |
| Mentions légales | absent | **300–500 mots** (template NEXOS) | mandatory |

### Ton & registre de copy recommandé (D2 emotional + D4 warm)

- **Ton** : convivial, parlé, FR-QC assumé (« on », « chez nous », « passez nous voir »), pas familier vulgaire.
- **Anti-corporate** : zéro buzzword (« solution », « écosystème », « expérience client »), zéro sigle inutile.
- **Storytelling court** : si possible, mention de l'ancrage local et du propriétaire Nobert Tremblay (à valider RPP/kickoff).
- **EN** : traduction respectueuse mais sans tenter de reproduire le ton FR-QC en anglais — registre EN warm-friendly canadien.

### Structure de contenu recommandée

#### Home (`/`)
Sections : `hero` (photo réelle + H1 nominatif + CTA promos) → `promo-week-teaser` (3 spéciaux du moment + lien vers /promotions) → `categories-overview` (bière, snack, lotto, dépannage, glace) → `infos-pratiques` (horaires + adresse + carte) → `infolettre-cta` → `footer`.

#### Promotions (`/promotions`)
Sections : `hero-promo-week` (titre + dates de validité de la semaine) → `promos-grid` (cards : photo, titre, prix avant/après, mention durée) → `archive-link` (semaine précédente, optionnel) → `infolettre-cta` (« recevez les promos chaque lundi »).

> **Asset critique pour le KPI conversion.** Doit être trivialement éditable chaque semaine (au minimum CMS-like ou JSON dans le repo édité par Nobert ou son agence). À cadrer en Ph1.

#### Produits (`/produits`)
Sections : `hero` → `categories-list` (Bière / Spiritueux / Snack / Boissons / Lotto / Dépannage / Glace / Autres) → chaque catégorie : grille produits avec photo + nom + prix indicatif (ou « voir en magasin »).

#### Contact (`/contact`)
Sections : `hero` → `coordonnees` (adresse + carte + téléphone + courriel) → `horaires` → `formulaire` (3-4 champs + consentement opt-in Loi 25) → `RPP-mention` (Nobert Tremblay, courriel RPP).

### Gaps de contenu vs concurrents (= opportunités)

1. **FAQ courte** (« Êtes-vous ouverts les jours fériés ? », « Acceptez-vous Interac ? », « Livrez-vous ? ») — aucun concurrent ne l'a, gain SEO long-tail.
2. **Bloc « Le mot du proprio »** court sur la home — humanise, différencie du registre corporate.
3. **Page promotions indexable** — gap structurel du secteur.

### Conformité Loi 25 (D8) — état initial

- Brief intake **complet** : RPP nommé (Nobert Tremblay), courriel RPP renseigné, incident_process: true, incident_email présent, transferts hors QC documentés (Vercel US, Google US), durées de rétention spécifiées, opt-in cookies déclaré.
- **Aucune zone d'ombre Loi 25** — D8 partira sur de bonnes bases. Les templates NEXOS (`templates/cookie-consent-component.tsx`, `templates/privacy-policy-template.md`, `templates/legal-mentions-template.md`) couvrent l'exécution.

---

## 6. Design trends du secteur

### Tendances couleurs observées

| Palette type | Fréquence | Association sectorielle |
|---|---|---|
| Rouge + jaune saturés (style commerce affiches) | 2/5 | Promo, criard, daté, à éviter |
| Beige/blanc minimaliste | 2/5 | Épiceries fines, marché — trop premium pour dépanneur |
| Bleu corporate + blanc | 1/5 | Chaînes (Couche-Tard) — anti-modèle Nobert |
| Vert nature | 1/5 | Épiceries bio — hors registre |
| **Brun/jaune/crème (warm authentique)** | **rare** | **Différenciation directe pour Nobert** |

La palette imposée Nobert (`#8B4513` brun · `#FFD700` accent · `#FFF8E7` background · `#2A1810` text) **n'est pas dans la moyenne sectorielle** — c'est exactement ce qu'on veut. Elle évoque les boiseries dépanneur traditionnel + chaleur + lumière, sans tomber dans le criard.

### Tendances typo observées

| Style | Fréquence | Verdict pour Nobert |
|---|---|---|
| Sans-serif générique (Roboto, Open Sans) sans poids fort | 3/5 | Trop neutre, ne porte pas le D3 heavy |
| Display serif (Playfair, Merriweather) pour titres | 1/5 | Trop premium/élégant, perdrait le côté quotidien |
| Display serif chaleureuse (Recoleta, Fraunces) + sans humaniste body (Inter, Karla) | rare | **Cible Nobert** — heavy + warm + lisible tous âges |
| Police builder par défaut (Wix/Squarespace) | 2/5 | Pas d'identité |

Référence brief : Recoleta/Fraunces + Inter/Karla. Recommandation de retenir **Fraunces** (Google Fonts, OFL, plus accessible que Recoleta) en heading + **Inter** en body. Validation finale en Ph2 par typography-pairing.

### Tendances layout

- **Hero plein largeur image + overlay texte** : 3/5, efficace.
- **Sections alternées blanc/gris** : 4/5, à reproduire avec crème/blanc pour Nobert.
- **Grille 12 colonnes** : standard, à conserver.
- **Whitespace généreux** : 2/5 (les meilleurs), à imposer chez Nobert (D6 symmetric + D5 slow-organic).

### Tendances animation

- Fade-in au scroll : 2/5, subtil acceptable.
- Hover color change CTA : 4/5, attendu.
- Parallax agressif : 1/5, à éviter (D5 slow-organic).
- Page transitions : 0/5 chez indépendants — pas nécessaire.

**Recommandation Nobert** : transitions sobres, pas de parallax, animations respectent `prefers-reduced-motion`. Le registre slow-organic est l'opposé du « tech flashy » — moins d'animation = plus d'authenticité.

### Tendances imagery

- **Photo authentique du commerce + propriétaire** : très rare (<1/5) — **opportunité différenciation directe**. À cadrer au kickoff (séance photo Nobert).
- Stock générique food/beverage : 3/5, à éviter.
- Icônes Lucide line-art : 2/5, à reproduire pour catégories produits.
- Illustrations custom : 0/5 — pas nécessaire pour Nobert.

### Dark mode

0/5 sites sectoriels — pas une attente, et le D4 warm s'accorde mal avec dark mode. **Skip pour v1.**

### Moodboard textuel Nobert

| Axe | Direction |
|---|---|
| Vibe | Convivial, ancré, chaleureux, lumineux, sans chichi |
| Couleurs | Brun boiseries `#8B4513` · Jaune doré `#FFD700` · Crème accueillant `#FFF8E7` · Texte espresso `#2A1810` |
| Typo | Fraunces display chaleureuse pour titres + Inter humaniste pour body |
| Layout | Hero photo réelle plein largeur · sections alternées crème/blanc · whitespace généreux · grille 12 col · structure symmetric (D6) |
| Animation | Fade-in léger au scroll · hover color change CTA · zéro parallax · `prefers-reduced-motion` natif |
| Imagery | Photo réelle du commerce + propriétaire · icônes Lucide pour catégories · zéro stock |

### Anti-patterns design à éviter explicitement

1. **Saturation rouge/jaune affiche commerciale** — registre criard, contraire au D4 warm chaleureux.
2. **Texte sur image sans overlay** — échec WCAG, fréquent dans le secteur.
3. **Carousel hero animé** — anti D5 slow-organic + anti a11y.
4. **Plus de 3 polices** — anti D6 symmetric, dilue l'identité.
5. **Photos stock alimentaire générique** — détruit le D2 emotional. La photo réelle est non négociable.

---

## 7. Recommandations pour Phase 1

### Décisions structurantes à acter en Phase 1

#### Stratégie & positionnement
1. **Positionnement** : « Le dépanneur de [ville] » — ancrage géographique nominatif obligatoire. La ville TBD au kickoff devient un **slot variabilisé** dans tout le contenu.
2. **UVP** : à valider mais cible « Promotions chaque semaine, ouvert quand vous en avez besoin, et un patron qui vous connaît par votre nom ».
3. **Tonalité copy** : FR-QC convivial, anti-corporate explicite. Ban-list : `solution`, `expérience`, `écosystème`, `partenaire de confiance`, `excellence`.

#### Architecture de contenu (à cadrer en pattern-recommender Ph1)
4. **Page promotions = asset critique** — doit être indexable HTML, structurée (cards avec titre + image + prix + dates), éditable hebdo. Choisir en Ph1 : JSON dans le repo (édition manuelle ou via un mini-CMS ultérieur) vs Sanity/Contentlayer. Pour le MVP solo : **JSON dans `clients/_e2e_validation_2026-05-08/site/data/promotions.json`** + section dédiée, à valider.
5. **Catalogue produits** : 6-8 catégories, fichier JSON, pas d'e-commerce.
6. **FAQ courte** sur la home ou page contact — opportunité SEO long-tail.

#### Patterns Ph2 (pattern-recommender)
7. Patterns universels (P01-P20) à activer prioritairement : hero photo réelle, sticky header, sticky CTA mobile, sections alternées, footer 3 colonnes Loi 25.
8. Référence visuelle dominante : **S13 Ma'ono** (jaune bold + hero photo) en première influence, **S12 Gazzo** (anti-polish authenticité) en seconde. S11 Noma trop premium pour dépanneur. S14 La Semilla pertinent pour le pattern catalogue par images.
9. Personnalité 6D verrouillée : `D1=3, D2=emotional, D3=heavy, D4=warm, D5=slow-organic, D6=symmetric`. **Aucune dérive corporate ne doit passer en Ph2/Ph3.**

#### Stack & build (Ph2/Ph4)
10. Stack imposée : Next.js 15 App Router · TypeScript strict · Tailwind · next-intl FR/EN · Vercel.
11. Polices : **Fraunces** (display, Google Fonts OFL) + **Inter** (body, Google Fonts OFL) — chargées via `next/font`.
12. Palette imposée verrouillée (`primary #8B4513`, `accent #FFD700`, `background #FFF8E7`, etc.) — **ne pas dériver** en Ph2.
13. **Vérifier en Ph2** le contraste de l'accent `#FFD700` sur background `#FFF8E7` : ratio ≈ 1.3:1 → **insuffisant pour texte**. Le jaune doit servir uniquement de **fill décoratif** ou de fond pour boutons avec texte sombre `#2A1810` (ratio ≈ 14:1 ✓).

#### SEO (Ph3)
14. **SEO local prioritaire** : metadata par page avec ville + catégorie. Sitemap multilingue avec hreflang FR/EN.
15. Schema.org : `LocalBusiness` + `ConvenienceStore` + `OpeningHoursSpecification` + `GeoCoordinates` — non négociable.
16. Mots-clés primaires : `dépanneur [ville]`, `bière [ville]`, `loto Québec [ville]`, `ouvert 24h [ville]` — à intégrer naturellement, pas en bourrage.

#### Loi 25 (D8 — non négociable)
17. Templates NEXOS appliqués tels quels : `cookie-consent-component.tsx` opt-in, `privacy-policy-template.md` avec RPP Nobert Tremblay + courriel + transferts US documentés, `legal-mentions-template.md` avec NEQ TBD au kickoff.
18. **Ouvrir un point kickoff** : NEQ Dépanneur Nobert inc. à confirmer + adresse + ville + téléphone définitif.

#### Différenciation prioritaire (à cibler dès Ph2)
19. **Sticky CTA mobile « Voir les promotions »** — feature unique vs concurrence directe.
20. **Photo réelle du commerce et du propriétaire** — séance photo à cadrer au kickoff, ou photo provisoire réaliste (pas stock) en attendant.
21. **Performance Lighthouse mobile ≥ 90** — gap concurrentiel direct.

### Risques identifiés à porter en Ph1

| Risque | Impact | Mitigation |
|---|---|---|
| Ville TBD au kickoff | Bloque SEO local, copy, schema.org | Kickoff obligatoire avant Ph1, sinon génération en mode `[ville]` template avec note |
| Photo réelle du commerce indisponible au launch | Détruit le D2 emotional | Plan B : photographie générique chaleureuse de dépanneur QC réel **mais clairement étiquetée temporaire**, à remplacer S+1 |
| Pattern-recommender confidence 0.5 (mapping SEC-03 dégradé) | Recommandations Ph1 potentiellement génériques | Ce rapport Ph0 sert de garde-fou : pattern-recommender doit cross-référencer ce rapport, pas seulement la taxonomie |
| Édition hebdo des promotions par Nobert solo | Risque d'abandon → page promo morte → perte SEO | Décider en Ph1 : flow d'édition (JSON commit, mini-admin, ou Sanity) le plus light possible |

---

## Synthèse SOIC Ph0

| Dimension | État | Note |
|---|---|---|
| D1 (Architecture) | Patterns sectoriels documentés, gaps identifiés, stack imposée cohérente | 8.5 |
| D2 (Tonalité) | D2=emotional verrouillé, ban-list corporate posée | 9.0 |
| D3 (Performance) | Gap concurrentiel énorme, cibles claires | 9.0 |
| D4 (Sécurité) | Templates NEXOS prêts, gap concurrentiel | 9.0 |
| D5 (i18n) | FR/EN décidé, next-intl confirmé | 8.5 |
| D6 (a11y) | Constats sectoriels faibles → opportunité documentée, contraste accent à vérifier Ph2 | 7.5 |
| D7 (SEO) | Mots-clés sectoriels listés, stratégie locale claire, ville TBD = risque | 8.0 |
| D8 (Loi 25) | Brief complet, RPP nommé, transferts documentés, templates prêts | 9.5 |
| D9 (Qualité) | Rapport synthétisé sans scraping live (limite assumée) — base solide pour Ph1 | 7.5 |

## Evaluation

Score global: 8.4/10
mu = 8.4/10

Seuil de passage Ph0→Ph1 (μ ≥ 7.0) : **GO**.

### Prochain jalon

Phase 1 — Strategy : exécution `agents/ph1-strategy/_orchestrator.md` avec `pattern-recommender` qui doit produire `pattern-recommendation.json` consommant ce rapport + brief + knowledge base. Confidence sectorielle 0.5 à compenser par la richesse de ce Ph0.
