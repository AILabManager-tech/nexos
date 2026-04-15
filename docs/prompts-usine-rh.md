# L'USINE RH — PROMPTS DE PRODUCTION OPTIMISÉS
```
PROJET    : L'USINE RH / HR FACTORY — Site Web + Logo
CLIENTE   : Émilie Poirier, CRHA
DATE      : 2026-02-14
AUTEUR    : Gear-code × Claude Opus 4.6
```

---

## 1. PROMPT NEXOS v3.0 / CLAUDE-CLI

> **Usage** : Coller dans `brief-client.json` ou passer en argument `--prompt` à l'orchestrateur NEXOS v3.0.
> **Runtime** : `claude --dangerously-skip-permissions --model claude-sonnet-4-5-20250929`

```markdown
# BRIEF CLIENT — L'USINE RH

## IDENTITÉ
- **Nom légal** : L'Usine RH / HR Factory
- **Fondatrice** : Émilie Poirier, CRHA
- **Email professionnel** : e.poirier@usinerh.ca
- **Téléphone** : 514-582-1490
- **LinkedIn** : https://www.linkedin.com/in/emilie-poirier-crha-1b408a48/
- **Localisation** : Région de Montréal, QC, Canada
- **Domaines** : usinerh.ca (principal), hrfactory.ca (redirect), usinerh.com (redirect)
- **Hébergement** : Vercel (compte existant du développeur)

## NICHE & POSITIONNEMENT
- **Clientèle** : PME 10-50 employés dans les secteurs **manufacturier**, **construction**, **usinage**, **entrepôt/logistique**
- **Offre** : Consultation RH opérationnelle — diagnostic, implantation de processus, coaching de superviseurs/contremaîtres
- **Différenciateur** : Émilie parle le langage du plancher ET du bureau. Elle est au même niveau que les "gars de shop", pas au-dessus. Camaraderie, pas corporatif.
- **Ton de voix** : Direct, franc, zéro bullshit corporatif. Québécois authentique. Comme une collègue qui dit les vraies affaires autour d'un café dans le break room.

## DIRECTION ESTHÉTIQUE — CRITIQUE

### Palette de couleurs
- **Primaire** : Bleu industriel profond (#1B3A5C → #2A5F8F) — la cliente aime les "teintes de bleu"
- **Secondaire** : Ambre/orange sécurité industrielle (#D4760A → #F5A623) — accents, CTA, highlights
- **Accent danger** : Rouge-rouille (#8B2500 → #C0392B)
- **Neutres** : Charbon (#1A1A1A), acier brossé (#3A3A3A → #5C5C5C), béton (#E8E4E0)
- **INTERDIT** : Jaune vif banderole plastique, argenté brillant plastique, rose, violet, pastel

### Typographie
- **Titres** : Police stencil/industrielle heavy (ex: Oswald Black, Bebas Neue, Black Ops One, ou Impact modifié) — CAPS LOCK, letter-spacing large
- **Corps** : Sans-serif condensée lisible (Barlow Condensed, Roboto Condensed) — rappel signalétique usine
- **Chiffres/Stats** : Monospace ou display weight (Russo One, Orbitron) — effet tableau de bord

### Textures & Matériaux (CSS)
- Acier brossé ÉRAFLÉ (pas chromé brillant — matte, rayé, vécu)
- Brique rouge-rouille vieillie (vraie texture, pas clip-art)
- Grille métallique perforée (pattern subtil en fond)
- Béton brut (grain, imperfections)
- Rivets RÉALISTES (radial-gradient avec ombres inset, pas des cercles flat)
- AUCUNE banderole jaune/noire de chantier (trop cliché, supprimé)
- AUCUNE plaque argentée qui a l'air plastique

### Ambiance photographique (Unsplash / stock directives)
Les images DOIVENT alterner entre 3 registres, en boucle :

1. **INDUSTRIE LOURDE** (40% des visuels)
   - Métal en fusion / coulée de fonderie (lueur orange sur fond sombre)
   - Étincelles de soudure / meulage
   - Engrenages massifs, machinerie CNC, presses hydrauliques
   - Entrepôts avec rayonnage bleu (comme la photo inspirationnelle)
   - Chantiers de construction actifs
   - **SÉCURITÉ** visible : casques, lunettes, gants, bottes, vestes haute-visibilité

2. **HUMAINS AU TRAVAIL — CAMARADERIE** (40% des visuels)
   - Groupes mixtes (H/F, diversité) souriants ENSEMBLE — pas des poses corporate
   - Scènes de bureau avec écrans montrant données/graphiques/dashboards
   - Femme leader debout PARMI le groupe (même niveau, pas devant/au-dessus)
   - Travailleurs en EPI qui rient / tape dans la main / fist bump
   - Réunion informelle dans un break room d'usine
   - Contremaître + employé de bureau côte à côte
   - **RESPECT MUTUEL** visible dans le body language

3. **DONNÉES & ÉVOLUTION** (20% des visuels)
   - Écrans/moniteurs avec graphiques, KPI, tableaux de bord
   - Tableaux blancs avec plans/organigrammes
   - Ambiance "contrôle de mission" — écrans multiples, données en temps réel
   - Symbolique d'évolution : flèches ascendantes, processus structurés

### Animations & Effets
- Particules d'étincelles de soudure (canvas, orange/ambre, flottant vers le haut)
- Engrenages qui tournent (SVG animé, très subtils, opacité 3-6%)
- Parallax sur les sections avec fond industriel
- Hover sur les cartes : légère élévation + ombre portée accentuée
- Transitions entre sections : séparateur de type "poutre I-beam" en acier
- Counter animés au scroll pour les stats
- Curseur personnalisé optionnel : réticule industriel

### CE QUI EST EXPLICITEMENT INTERDIT
- [ ] Banderoles jaune/noir "hazard tape" — cliché, on les retire
- [ ] Plaque métallique argentée plastique — on veut de l'acier MATTE éraflé
- [ ] Esthétique "jouet" / enfantin / clip-art
- [ ] Photos stock génériques de personnes en costume cravate
- [ ] Polices serif élégantes (pas un cabinet d'avocat)
- [ ] Fond blanc uni (toujours une texture ou profondeur)
- [ ] Emojis comme icônes principales (utiliser des SVG/icônes solides)

## STRUCTURE DU SITE (5 pages)

### Page 1 : Accueil
- Hero section : fond fonderie/métal en fusion, overlay léger (30-40% max)
- Logo L'USINE RH en 3D acier éraflé sur texture brique rouille, de biais, gros rivets
- Tagline principale : "Pour des RH qui marchent aussi fort que votre production"
- Tagline secondaire : "Je diagnostique. J'implante. Je coache."
- 2 CTA : "Appel découverte gratuit" (primaire) + "Voir mes services" (secondaire)
- Stats animées : 15+ ans XP, 50+ PME, 5-50 employés
- Section "Problèmes" : 3 cartes (Proprio débordé, Superviseur sans formation, PME en croissance)
- CTA banner intermédiaire

### Page 2 : Services
- Approche en 3 étapes : Diagnostic (2-3 sem) → Implantation (8-12 sem) → Coaching (3-6 mois)
- Études de cas : 3 onglets (Manufacturier 35 emp, Services pro 22 emp, Construction 48 emp) avec avant/après
- Chaque étude : stat badge (ex: "-55% roulement")

### Page 3 : Diagnostic interactif
- Quiz 5 questions : évaluer maturité RH (score 🔴🟡🟢)
- Calculateur de coûts : 3 sliders (employés, salaire, taux de roulement) → coût estimé en temps réel
- Formule : roulement coûte 33% du salaire annuel par départ

### Page 4 : Mythes RH
- 8 cartes flip click-to-reveal, grille 4 colonnes
- Fond : fonderie visible (overlay 35-40%)
- Engrenages animés en arrière-plan
- Mythes : "Les RH c'est pour les grosses cie", "Un bon salaire suffit", "Évaluations inutiles", "Je connais mon monde", "Pas le temps", "Formation = dépense", "Bon employé = pas de feedback", "Roulement = normal"

### Page 5 : Contact
- Infos : Émilie Poirier, e.poirier@usinerh.ca, 514-582-1490, LinkedIn
- Formulaire 6 champs → mailto:e.poirier@usinerh.ca (opérationnel)
- Témoignage client
- Carte OpenStreetMap (Montréal, marker 45.5017, -73.5673)
- Photo professionnelle d'Émilie (à intégrer quand fournie)

### Éléments transversaux
- Navigation fixe avec logo + liens + toggle FR/EN + CTA
- Bilingue complet (FR/EN)
- Footer 3 colonnes (marque, navigation, contact)
- Responsive mobile-first
- Séparateurs entre sections : poutre I-beam en acier ou ligne de rivets

## SLOGANS APPROUVÉS (à utiliser dans le contenu)
- "L'Usine RH : simplifier les RH, amplifier l'impact."
- "L'Usine RH : la mécanique RH, sans les complications."
- "Pour des RH qui marchent aussi fort que votre production."

## SEO & TECHNIQUE
- Next.js 15+ / TypeScript / Tailwind v4
- Vercel deployment (domaine usinerh.ca)
- Structured data JSON-LD (LocalBusiness)
- Meta OG pour partage social
- Sitemap XML + robots.txt
- Headers sécurité complets (CSP, HSTS, X-Frame-Options, etc.)
- Loi 25 Québec : bandeau consentement cookies
- Score Lighthouse cible : ≥ 85/100 sur les 4 catégories
```

---

## 2. PROMPT LEONARDO.AI — LOGO PROFESSIONNEL

> **Usage** : Copier-coller dans Leonardo.ai. Utiliser le modèle **Leonardo Phoenix** ou **SDXL** avec guidance scale 7-8.

### Prompt A — Logo principal (emblème)

```
Professional industrial logo design for "L'USINE RH" (HR Factory), a human resources consulting firm specializing in manufacturing and construction SMBs.

Design elements:
- A hardhat viewed from the front, made of BRUSHED STEEL with visible scratches and wear marks, not plastic, not shiny — matte industrial metal finish
- Inside or overlaid on the hardhat: a subtle gear mechanism and a human head silhouette in profile, suggesting the fusion of industrial machinery and human intelligence
- The hardhat has a small front-facing badge area with "RH" embossed in the metal
- Behind the hardhat: faint suggestion of factory smokestacks or I-beam structure
- Color palette: deep industrial blue (#1B3A5C) as dominant, warm amber (#D4760A) for accent highlights, dark charcoal (#1A1A1A) for contrast
- Rusty red-brick texture element as subtle background accent
- The overall feel should be HEAVY, INDUSTRIAL, PROFESSIONAL — like a union logo meets a modern tech company
- NOT cute, NOT cartoonish, NOT clip-art — this should look like it was stamped into steel

Style: vector logo, clean edges, professional branding, industrial aesthetic, dark background version, suitable for both light and dark backgrounds
Negative prompt: cartoon, toy, childish, plastic, shiny chrome, 3D render, photorealistic, gradient mesh, watercolor, sketch, anime
```

### Prompt B — Logotype alternatif (texte seul avec traitement)

```
Professional industrial logotype for "L'USINE RH" text, heavy metal typography style.

Design:
- Text "L'USINE RH" in bold industrial stencil font with steel plate texture
- Letters appear CUT from brushed steel with visible scratches and patina
- "L'USINE" in deep blue steel (#1B3A5C), "RH" in warm amber/orange steel (#D4760A)
- Rivets (2-3) flanking the text on each side, realistic metallic finish with specular highlights
- Subtle red-rust brick wall texture visible behind/around the text
- A single small gear icon integrated into the apostrophe of "L'USINE" or replacing the dot-like element
- Bottom: thin I-beam steel line as underline
- Aged metal look — NOT new, NOT polished, but well-maintained industrial equipment aesthetic

Style: logo design, typography, industrial branding, steel texture, flat background, vector-ready
Negative prompt: 3D text, chrome, plastic, neon, glow effects, futuristic, sci-fi, cartoon, handwritten
```

### Prompt C — Icône/favicon (simple)

```
Minimalist industrial icon, a single gear with a human head silhouette integrated into the center negative space. Deep blue steel (#1B3A5C) gear, amber (#D4760A) accent on one gear tooth. Clean vector style, suitable as favicon at 32x32px and app icon at 512x512px. Dark charcoal background. Professional, heavy, industrial feel. NOT cute or cartoonish.

Style: icon design, minimalist, industrial, vector, clean
Negative prompt: detailed, complex, realistic, 3D, cartoon, toy
```

### Paramètres Leonardo.ai recommandés

| Paramètre | Valeur |
|-----------|--------|
| Modèle | Leonardo Phoenix 1.0 ou SDXL 1.0 |
| Dimensions | 1024×1024 (carré pour logo) |
| Guidance Scale | 7.5 |
| Steps | 30-40 |
| Nombre d'images | 4 (pour sélection) |
| Alchemy | ON |
| PhotoReal | OFF (on veut du vecteur/flat) |
| Contraste | High |
| Seed | random |

### Post-traitement recommandé
1. Sélectionner le meilleur des 4
2. Upscale 4x dans Leonardo
3. Exporter PNG transparent
4. Vectoriser dans Vectorizer.ai ou Inkscape (trace bitmap)
5. Générer les variantes : fond sombre, fond clair, monochrome, favicon

---

## 3. PROMPT CLAUDE-CLI — EXÉCUTION DIRECTE (single-shot)

> **Usage** : Si NEXOS v3 n'est pas encore opérationnel, ce prompt peut être passé directement à `claude` en CLI pour générer le site en un appel.

```bash
claude --dangerously-skip-permissions -p "

# MISSION
Génère un site web complet pour L'USINE RH en UN SEUL fichier index.html autonome (HTML + CSS + JS inline, zéro dépendance externe sauf Google Fonts et images Unsplash).

# CONTRAINTES TECHNIQUES ABSOLUES
- Fichier unique index.html, déployable par simple upload
- Zero framework, zero build step — vanilla HTML/CSS/JS
- Google Fonts via <link> : Black Ops One, Barlow Condensed, Russo One, Oswald
- Images via Unsplash URL directes (hot-link)
- Responsive mobile-first
- Bilingue FR/EN avec toggle (objet JS i18n)
- 5 pages via routing JS (hash ou state)
- Formulaire mailto:e.poirier@usinerh.ca opérationnel
- OpenStreetMap iframe (Montréal)
- Canvas étincelles de soudure (particules orange/ambre)

# PALETTE
- Bleu industriel profond : #1B3A5C (dominant)
- Ambre sécurité : #D4760A, #F5A623 (CTA, accents)
- Rouge rouille : #8B2500 (danger, alertes)
- Charbon : #1A1A1A, #0D0D0D (fonds)
- Acier : #3A3A3A, #5C5C5C (cartes, bordures)
- Béton : #E8E4E0 (texte clair quand nécessaire)

# TEXTURES CSS REQUISES
- Acier brossé MATTE éraflé (repeating-linear-gradient subtil)
- Fond brique rouille (image Unsplash, brightness réduit)
- Rivets réalistes (radial-gradient avec ombres inset)
- Grille métallique perforée (radial-gradient dots pattern)
- PAS de banderole jaune/noire hazard tape
- PAS de plaque argentée plastique

# LOGO HERO
- Texte 'L'USINE RH' en 3D CSS : perspective, rotateY(-4deg), rotateX(2deg)
- Texture acier brossé éraflé sur les lettres (gradient + background-clip:text)
- 'L'USINE' en bleu industriel, 'RH' en ambre
- 6+ rivets (18px, réalistes) autour de la plaque
- Texture brique rouille derrière la plaque (image Unsplash, 40% opacité)
- Shine sweep animé (linear-gradient mobile)

# IMAGES UNSPLASH (thèmes à chercher pour chaque section)
- Hero : molten metal foundry, steel mill, sparks
- Pain points : welding sparks blue light
- Services : industrial factory interior
- Mythes : foundry pouring molten metal
- Contact : manufacturing plant team
- Background overlays : 30-45% opacité MAX (on veut VOIR la fonderie)

# ENGRENAGES SVG ANIMÉS
- 3-5 engrenages positionnés en absolute sur les sections
- Rotation et contre-rotation CSS (25-35s linear infinite)
- Opacité 4-6% — subtils mais présents
- Couleur : bleu industriel

# SÉPARATEURS
- Entre sections : ligne de rivets horizontale OU poutre I-beam stylisée
- PAS de banderole hazard tape

# CONTENU
[inclure ici le contenu i18n complet FR/EN identique au brief ci-dessus]

# STRUCTURE
Page 1: Accueil (hero + pain points + CTA banner)
Page 2: Services (3 étapes + études de cas)
Page 3: Diagnostic (quiz 5 questions + calculateur coûts)
Page 4: Mythes RH (8 cartes flip, grille 4 colonnes)
Page 5: Contact (infos + formulaire + map + témoignage)
Footer: 3 colonnes, copyright

# QUALITY GATES
- [ ] Toutes les sections rendue visuellement
- [ ] Toggle FR/EN fonctionnel
- [ ] Quiz interactif avec score
- [ ] Calculateur avec sliders
- [ ] Formulaire mailto opérationnel
- [ ] Map OSM visible
- [ ] Canvas étincelles actif
- [ ] Responsive < 768px
- [ ] Aucun jaune hazard tape
- [ ] Aucun argenté plastique
- [ ] Palette bleu industriel respectée

" --output /home/claude/clients/usinerh/index.html
```

---

## 4. DIRECTION ARTISTIQUE CONSOLIDÉE (Référence)

### Mood Board Textuel

```
REGISTRE VISUEL : "Fonderie RH"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MATÉRIAUX          LUMIÈRE              ÉMOTION
─────────          ───────              ───────
Acier éraflé       Lueur ambre fonderie Fierté ouvrière
Brique rouille     Néon bleu atelier    Camaraderie brute
Béton coulé        Étincelles soudure   Respect mutuel
Grille perforée    LED écrans/données   Confiance évolutive
Poutre I-beam      Spot industriel      Sérieux accessible

PERSONNES                              INTERDIT
─────────                              ────────
Femme leader PARMI le groupe           Costume-cravate
Gars d'usine qui sourient              Salle de conférence blanche
Mixité bureau + shop floor             Poignée de main stock
Casque + blazer côte à côte            Infographie pastel
EPI + écran de données                 Logo enfantin/clip-art
Fist bump entre collègues              Banderole jaune/noire
                                       Plaque argentée plastique
```

### Différence clé vs V2 (version précédente)

| Élément | V2 (ancienne) | V3 (nouvelle) |
|---------|---------------|---------------|
| Palette dominante | Orange/noir | **Bleu industriel** + ambre accent |
| Séparateurs | Hazard tape jaune/noir | Poutre I-beam / ligne de rivets |
| Plaque logo | Argenté chromé/plastique | Acier brossé matte ÉRAFLÉ |
| Overlay fond | 50-80% noir | **30-45% max** — on voit la fonderie |
| Vibe générale | Chantier de construction | **Fonderie/usine métallurgique** |
| Icônes | Emojis | SVG solides industriels |
| Ton | "Tough guy" | **"Je suis comme vous les boys"** + données |
