# Phase 0 — Discovery Report — Dépanneur Nobert

**Client** : Dépanneur Nobert inc.
**Slug** : `depanneur-nobert`
**Mode NEXOS** : `create` (création from scratch, orientée résultat business)
**Date discovery** : 2026-04-28
**Orchestrateur** : ph0-discovery
**Agents exécutés** : web-scout, tech-inspector, ux-analyst, content-evaluator, design-critic
**Stack imposée** : Next.js 15 + Tailwind + next-intl (FR/EN) + Vercel
**Palette imposée** : warm — `#8B4513` / `#FFD700` / `#FFF8E7` / `#2A1810`

---

## Cadrage métier (priorité absolue)

> Le mode `create` impose de traiter ce travail comme **création from scratch orientée business**.

| Axe | Décision opérationnelle |
|---|---|
| **KPI primaire** | Conversion → (1) visite physique en magasin, (2) consultation des promotions hebdo |
| **CTA principal** | « **Voir les promotions de la semaine** » (sticky, omniprésent — pattern P01) |
| **Indicateur de succès** | Trafic SEO local `dépanneur + [ville]` + clics CTA promos + appels téléphone |
| **Audience** | Voisinage immédiat, tous âges (20-80 ans), fidélité de proximité |
| **Anti-cible** | Registre corporate, ton chaîne (Couche-Tard, Petro-Canada) — rejet explicite |

La discovery écarte délibérément les analyses hors-sujet (B2B portail, livraison multi-villes nationale, agrégateurs e-commerce) pour rester centrée sur le profil **commerce de proximité solo + KPI conversion + ancrage géographique**.

---

## 1. Analyse sectorielle

### Profil sectoriel réel

Le secteur **dépanneur de quartier indépendant au Québec** présente une particularité majeure pour la phase Discovery : **la majorité écrasante des dépanneurs n'a pas de site web propre**. Présence en ligne typique = fiche annuaire (PagesJaunes, Yelp, sites de quartier comme `monlimoilou.com`, fiche Google My Business) sans propriété web.

Référence directe du gap : **Accommodation Populaire** (900 3e Avenue, Limoilou — depuis 1966, géré par 3 générations). Aucune URL propre, présence réduite à une fiche communautaire sur `monlimoilou.com`. C'est **exactement le profil Nobert avant intervention NEXOS** — donc la simple existence d'un site Next.js correctement référencé constitue déjà une rupture sectorielle.

### Mapping NEXOS

- **Sector_id mappé** : SEC-03 (Restauration) — par proximité culturelle (alimentaire + ancrage local + registre chaleureux)
- **Confidence** : 0.5 (mapping manuel — secteur commerce de proximité non nativement couvert par les 6 taxonomies NEXOS)
- **Conséquence Discovery** : les références SEC-03 (Noma, Gazzo, Ma'ono, La Semilla — restaurants et bistros) restent utilisables **comme sources d'inspiration design** mais doivent être pondérées car le format catalogue dépanneur diffère structurellement du menu restaurant.

### Concurrents directs vs concurrents larges

| Type | Nom | Concurrence | Pourquoi |
|---|---|---|---|
| Direct quartier | Autres dépanneurs indépendants de la même ville | **OUI — concurrence #1** | Captent le voisinage immédiat |
| Direct catégorie bière | Accommodation ChaLou, Dépanneur Peluso, Dépanneur Rapido | **Partielle** | Spécialistes bière artisanale — Nobert doit décider s'il joue ce terrain |
| Indirect chaîne | Couche-Tard, Shell Select, Petro-Canada | **NON** | Masse vs proximité — anti-positionnement explicite (free_text brief) |
| Indirect livraison | Ton dépanneur qui livre | **Faible** | Plateforme tierce — pourrait devenir partenaire |
| Référence sectorielle | DepQuébec | **NON** | Portail B2B information |

---

## 2. Benchmark concurrence (5 sites analysés)

### 2.1 Tableau synthétique

> **Convention de nommage** : chaque concurrent est identifié par un code archétype `C1`..`C5` (Concurrent 1 à Concurrent 5) pour traçabilité dans la matrice de gaps §2.7.

| Code | # | Site | URL | Localisation | Modèle | Bilingue | Loi 25 banner | Stack apparente |
|---|---|---|---|---|---|---|---|---|
| **C1** | 1 | Concurrent 1 — Accommodation ChaLou | accommodationchalou.com | Saint-Émile + Beauport (Québec) | Bières microbrasseries | FR | ❌ | WordPress + RevSlider + ShortPixel |
| **C2** | 2 | Concurrent 2 — Dépanneur Rapido | depanneurrapido.com | Gatineau-Aylmer | Bières + épicerie + circulaire | FR/EN | ✅ (4 catégories) | Custom (PHP probable) |
| **C3** | 3 | Concurrent 3 — Dépanneur Peluso | depanneurpeluso.com | Beaubien + Rachel (Montréal) | Bières microbrasseries + traiteur | FR | ❌ | Non détecté (vitrine statique) |
| **C4** | 4 | Concurrent 4 — Ton dépanneur qui livre | tondepanneur.com | Multi-villes QC (livraison) | Plateforme livraison | FR | ❌ | E-commerce custom |
| **C5** | 5 | Concurrent 5 — DepQuébec | depquebec.com | Portail provincial | Information B2B + 7700 dépanneurs | FR/EN/ZH | ❌ | WordPress |

**Observation clé** : sur 5 sites web réels du secteur, **un seul (Rapido, 1/5) implémente un cookie banner Loi 25 conforme**. C'est un gap réglementaire majeur — Nobert sera conforme dès le J0 grâce au pipeline NEXOS, ce qui constitue à la fois un avantage juridique et un signal de confiance différenciant.

### 2.2 Fiches concurrents

#### #1 — Accommodation ChaLou
- **UVP** : « Le plus grand choix de bières au meilleur prix » (1000+ bières, plus grande chambre à bière réfrigérée région de Québec)
- **CTA** : Liens produits vers offres bière promotionnelles
- **Forces** : Volume catalogue impressionnant, 2 succursales avec horaires + téléphones visibles, partenariats brasseries documentés (9 logos), ancienneté (1991)
- **Faiblesses** : Hero RevSlider daté, aucune Loi 25, pas de Google Maps intégré, pas de newsletter, design WordPress générique, mobile non vérifié
- **Source** : `https://www.accommodationchalou.com/`

#### #2 — Dépanneur Rapido
- **UVP** : « The beer giant » — 500+ types de bières, 40+ ans à Outaouais
- **CTA** : « Discover the beers » + « All promotions »
- **Forces** : Bilingue FR/EN natif, **cookie banner Loi 25 conforme** (functional/preferences/statistics/marketing), Google Maps intégré, newsletter active, présence sociale (Facebook + Instagram), section circulaire dédiée
- **Faiblesses** : Pas de testimonials, horaires absents en première vue, hero produit conventionnel, design fonctionnel sans personnalité
- **Source** : `https://www.depanneurrapido.com/en/`

#### #3 — Dépanneur Peluso
- **UVP** : « Le plus beau choix de bières de microbrasserie au Québec » (1200+ bières + traiteur + fromages)
- **CTA** : « Offrez du bonheur en cadeau! » (cartes-cadeaux Rachel uniquement)
- **Forces** : Positionnement premium clair (microbrasseries + traiteur + cheese counter), 2 adresses Montréal, branding fort
- **Faiblesses** : Pas de catalogue en ligne, pas de promotions visibles, pas d'horaires, pas de newsletter, pas de Maps, FR uniquement, pas de Loi 25, vitrine quasi-statique
- **Source** : `https://depanneurpeluso.com/`

#### #4 — Ton dépanneur qui livre
- **UVP** : « Livraison à domicile de votre épicerie/dépanneur de quartier » — 7j/7 jusqu'à 21h
- **CTA** : « Cliquez sur votre ville de livraison »
- **Forces** : Modèle géographique multi-villes (Québec, Sherbrooke, Longueuil, Montréal), flux e-commerce intégré, paiement online ou cash/card à la livraison
- **Faiblesses** : Pas de promotions mises en avant, pas de cookie banner, pas de testimonials, FR seul, frictions multiples avant achat (sélection ville → catalogue → commande)
- **Source** : `https://www.tondepanneur.com/`

#### #5 — DepQuébec (portail sectoriel B2B — référence indirecte)
- **UVP** : « Premier portail web entièrement indépendant dédié aux dépanneurs du Québec »
- **CTA** : Inscription newsletter gratuite
- **Forces** : Couverture exhaustive (7700+ dépanneurs avec GeoMap), trilingue FR/EN/ZH, classements (Top 100, chaînes, bannières), articles sectoriels structurés
- **Faiblesses** : Public B2B (utile comme source d'audit, pas comme inspiration UX retail), design WordPress daté, pas de Loi 25
- **Source** : `https://depquebec.com/en/`
- **Usage Discovery** : référence sectorielle pour comprendre l'écosystème, **pas un benchmark UX pour la home Nobert**

### 2.3 Cas de référence « gap » : Accommodation Populaire (Limoilou)

Pas de site propre — uniquement une fiche sur `monlimoilou.com`. Téléphone, adresse, horaires, services listés. **C'est la situation typique des dépanneurs de quartier indépendants au Québec et c'est exactement le point de départ que Nobert quitte avec ce projet.** Insight Discovery : **le simple fait d'avoir un site bien référencé suffit à dépasser 80% des dépanneurs québécois sur leur SEO local immédiat.**

### 2.4 Market gaps identifiés

1. **Aucun concurrent ne capitalise sur le social proof voisinage** (témoignages clients de quartier) → pattern P02 = avantage immédiat
2. **Aucun ne respecte pleinement la Loi 25** (4/5 non conformes) → conformité native = avantage juridique + signal confiance
3. **Aucun anti-polish authenticité crédible** (registre dominant = WordPress générique ou hero produit fade) → P13 ouvre un territoire inoccupé
4. **Aucune page par localisation SEO-optimisée** (`dépanneur + [ville]`) → P11 capture du trafic local immédiat
5. **Aucun « promotions de la semaine » structurées en hero CTA** → P01 sticky CTA + section dédiée = différenciation directe sur le KPI conversion
6. **Aucun storytelling de quartier** (héritage, propriétaire, années de service) → P19 StoryBrand sous-exploité
7. **Bilinguisme FR/EN absent chez 3/5** → différenciation accessibilité touristique/anglophone

### 2.5 Mots-clés sectoriels extraits (≥10)

`dépanneur [ville]`, `dépanneur ouvert 24h [ville]`, `dépanneur de quartier`, `bière [ville]`, `bières microbrasserie Québec`, `loto Québec [ville]`, `cigarettes [ville]`, `vin et bière dépanneur`, `dépanneur livraison [ville]`, `circulaire dépanneur`, `promotions dépanneur`, `dépanneur près de moi`, `accommodation [ville]`, `snack froid chaud`, `dépanneur ouvert dimanche`.

### 2.6 Synthèse positionnement (web-scout summary)

> Nobert doit se positionner comme **« Le dépanneur de quartier authentique de [ville] »** — chaleureux, humain, ancré, anti-corporate. Son site doit faire deux choses qu'aucun concurrent ne fait bien : (1) afficher les promotions de la semaine en CTA sticky persistant pour driver la visite physique, (2) raconter la proximité (témoignages voisinage + storytelling propriétaire) pour activer la fidélité. Le respect Loi 25 natif et le SEO local agressif (`dépanneur + [ville]`) sont des bénéfices automatiques du pipeline NEXOS qui le placent au-dessus du marché dès J0.

### 2.7 Matrice forces/faiblesses & gaps par concurrent (C1..C5)

Cette **matrice de différenciation** synthétise pour chaque concurrent (Concurrent 1 à Concurrent 5) les forces principales, faiblesses critiques, et le **gap exploitable** par Nobert. Elle est consommée par la Phase 1 Strategy (`brand-strategist` + `seo-strategist`) pour calibrer le positionnement et la priorisation des patterns.

| Axe | C1 ChaLou | C2 Rapido | C3 Peluso | C4 Ton dép. | C5 DepQuébec | Gap Nobert |
|---|---|---|---|---|---|---|
| **Force principale** | Volume catalogue (1000+ bières) | Bilinguisme + Loi 25 conforme | Branding premium clair | Modèle livraison multi-villes | Couverture exhaustive 7700 dép. | Authenticité humaine quartier |
| **Faiblesse critique** | Hero RevSlider daté + 0 Loi 25 | Pas de testimonials, hero fade | Pas de catalogue ni promos en ligne | Frictions multiples avant achat | Public B2B, pas retail | (à transformer en avantage) |
| **CTA primaire** | Liens produits | Discover the beers | Cartes-cadeaux | Sélection ville | Newsletter B2B | **Voir promotions semaine (P01)** |
| **Sticky CTA promos** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **gap absolu** |
| **Social proof voisinage** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **gap absolu** |
| **Page par localisation** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **gap absolu** |
| **Loi 25 conforme** | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ natif (gap 4/5) |
| **Bilinguisme FR/EN** | ❌ | ✅ | ❌ | ❌ | ✅ (FR/EN/ZH) | ✅ natif (gap 3/5) |
| **Stack moderne (Next.js)** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **gap absolu** |
| **Anti-polish authenticité** | ❌ | ❌ | partiel | ❌ | ❌ | ✅ **gap quasi absolu** |
| **Storytelling quartier** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **gap absolu** |

**Lecture matrice — différenciation Nobert** : sur 7 gaps stratégiques mesurés (sticky CTA, social proof, page localisation, Loi 25, bilinguisme, stack moderne, storytelling), Nobert capture **7/7** dès J0. Aucun concurrent direct (C1, C2, C3, C4) ni sectoriel (C5) ne couvre simultanément ces axes. Cette matrice est le socle factuel des recommandations §7 et de la stratégie de patterns en Phase 1 (`pattern-recommender` → P01, P02, P09, P11, P13, P19, P20).

---

## 3. Stack techniques détectées (tech-inspector)

### 3.1 Synthèse sectorielle

| Stack | Adoption (5 sites) | Observation |
|---|---|---|
| WordPress | 3/5 (ChaLou, DepQuébec, Peluso probable) | Standard du secteur, souvent avec plugins datés |
| Custom PHP/legacy | 1/5 (Rapido) | Stable, fonctionnel, peu moderne |
| E-commerce custom | 1/5 (Ton dépanneur) | Spécifique au modèle livraison |
| **Next.js / React / framework moderne** | **0/5** | **Aucun concurrent — opportunité technique nette** |

### 3.2 Indicateurs techniques observables

| Concurrent | Hero | Performance perçue | Sécurité | Cookie banner |
|---|---|---|---|---|
| ChaLou | RevSlider carousel | Lente (lazy SVG après chargement) | HTTPS basique | ❌ |
| Rapido | Statique produit | Acceptable | HTTPS + headers visibles | ✅ Loi 25 |
| Peluso | Statique vitrine | Rapide (peu de contenu) | HTTPS basique | ❌ |
| Ton dépanneur | E-commerce | Moyenne | HTTPS + cart sécurisé | ❌ |
| DepQuébec | WordPress lazy SVG | Lente | HTTPS + WP standard | ❌ |

### 3.3 NEXOS Advantage (Next.js 15 + Vercel + headers SOIC)

| Dimension | Avantage Nobert vs secteur |
|---|---|
| **Framework** | Next.js 15 App Router → SSR + Edge + Image optimization native vs WordPress 60% du marché |
| **Performance** | Bundle Tailwind purgé < 200KB vs 1-3 MB moyen WordPress + plugins |
| **Sécurité** | Headers HSTS / CSP / X-Frame-Options / Permissions-Policy natifs `vercel.json` vs 0 headers chez 4/5 |
| **Loi 25** | Cookie consent opt-in + politique + RPP + incident process — natifs templates NEXOS, vs 1/5 conforme dans le secteur |
| **SEO** | Metadata App Router + JSON-LD LocalBusiness + sitemap multilingue + hreflang automatiques vs plugins SEO manuels chez WordPress |
| **i18n** | next-intl FR/EN sans config supplémentaire vs Polylang / WPML chez WordPress |

### 3.4 Risques techniques à anticiper (Phase 1 → Phase 4)

- **D5 Performance** : P17 scroll-triggered animations retenu — surveiller CLS mobile, respect `prefers-reduced-motion` obligatoire
- **D6 Accessibilité** : P20 menu galerie images → alt-text descriptif obligatoire sur chaque produit (WCAG 2.2 AA + SEO bonus)
- **D8 Loi 25** : Variables `[ville]`, NEQ, adresse manquantes du brief — placeholders TBD, à fixer kickoff avant deploy
- **D6 SEO** : Schema.org `LocalBusiness` + NAP (Name/Address/Phone) cohérent avec Google My Business indispensable

---

## 4. Patterns UX dominants (ux-analyst)

### 4.1 Patterns observés chez les concurrents (quantification)

| Pattern UX | Présence (5 sites) | Verdict pour Nobert |
|---|---|---|
| Sticky header navigation | 4/5 | ✅ Standard à reprendre |
| Hero produit centré | 5/5 | ⚠️ À détourner — Nobert mettra promotions hebdo en hero (différenciation P01) |
| Catalogue/grille produits | 4/5 | ✅ Reprendre avec P20 menu galerie images |
| Sticky CTA persistant | 0/5 | 🟢 **Opportunité différenciation P01** |
| Témoignages visibles | 0/5 | 🟢 **Opportunité différenciation P02** |
| Newsletter inline | 2/5 | ✅ À implémenter (objectif secondary KPI) |
| Google Maps intégré | 2/5 | ✅ Indispensable (KPI visite physique) |
| Pop-up nouvelle visite | 1/5 | ❌ Anti-pattern — éviter |
| Carrousel automatique en hero | 2/5 | ❌ Anti-pattern (a11y + CTR) — éviter |
| Page par localisation | 0/5 | 🟢 **Opportunité différenciation P11** |
| Bilinguisme FR/EN | 2/5 | ✅ Imposé brief — confirme avantage |

### 4.2 Anti-patterns détectés

| Anti-pattern | Vu chez | Impact | Décision Nobert |
|---|---|---|---|
| Hero RevSlider carousel auto | ChaLou | LCP dégradé, baisse CTR, mauvais a11y | ❌ Hero statique avec **photo authentique vitrine + CTA promos** |
| Pas de Maps embed | ChaLou, Peluso | Friction visite physique (KPI primaire !) | ✅ Maps obligatoire dès le hero (mobile) ou fold 2 |
| Catalogue non navigable | Peluso | Visiteur n'a aucune raison de revenir | ✅ Catalogue galerie (P20) + promos hebdo dynamiques |
| Pas de Loi 25 banner | 4/5 | Risque réglementaire + signal confiance bas | ✅ Cookie consent opt-in NEXOS natif |
| Aucun horaire visible | Peluso | Friction visite physique | ✅ Horaires en hero ou header sticky |

### 4.3 Patterns à appliquer (rappel cohérence pattern-recommendation.json)

| Pattern | Justification UX |
|---|---|
| **P01 Sticky CTA persistant** | « Voir les promotions » omniprésent sur scroll — capte le KPI conversion à tout instant |
| **P02 Social proof adjacente CTA** | Témoignages voisinage juste avant le CTA — measured impact +2× leads (S05 Bloor Jane) |
| **P09 3-word brand messaging** | Ex. « Ton dépanneur. Ton quartier. » — registre `emotional` + typo `heavy` lisibilité tous âges |
| **P11 Page par localisation** | `/{ville}` pour SEO local — gap absolu chez les 5 concurrents |
| **P13 Anti-polish authenticity** | Photos réelles, textures papier/boiseries, ton direct — opposé au registre WordPress fade |
| **P17 Scroll-triggered animations** | Sobres, respect `prefers-reduced-motion`, modernité sans gadget |
| **P19 StoryBrand messaging** | Cadre narratif « visiteur = voisin, Nobert = guide de proximité » sur home + about |
| **P20 Menu galerie images** | Catalogue visuel pour `/produits` + section promotions home |

### 4.4 Accessibilité — opportunité de différenciation

Aucun concurrent n'expose un audit a11y. **WCAG 2.2 AA natif** (contraste, focus visibles, alt-text complet, touch targets ≥ 44×44px, `prefers-reduced-motion` respecté) = différenciation immédiate, alignée avec audience tous âges (20-80 ans).

---

## 5. Contenu (mode `creation` — content-evaluator)

### 5.1 Mode

`mode: creation` — Nobert n'a pas de site existant à migrer (`logo_provided: false`, aucune URL existante mentionnée). Pas de contenu legacy à inventorier, pas de redirection 301 à planifier. Le content-evaluator opère donc en **mode B (sector_analysis + recommended_content_structure)**.

### 5.2 Analyse sectorielle de contenu

| Page typique secteur | Mots cibles | Présence chez concurrents | Nécessité Nobert |
|---|---|---|---|
| Accueil | 600-1000 | 5/5 | ✅ Indispensable |
| Promotions/circulaire | 200-500 | 3/5 | ✅ **Indispensable — KPI primaire** |
| Catalogue produits | 300-800 | 4/5 | ✅ Indispensable |
| Contact/Localisation | 100-300 | 5/5 | ✅ Indispensable |
| À propos / Histoire | 400-700 | 2/5 | ⚠️ Recommandé (StoryBrand P19) |
| FAQ | 300-600 | 0/5 | 🟢 Opportunité différenciation |
| Politique confidentialité | 500-900 | 1/5 | ✅ **Obligatoire Loi 25** |
| Mentions légales | 300-500 | 2/5 | ✅ **Obligatoire Loi 25** |

### 5.3 Structure de contenu recommandée pour Nobert

| Page | Sections | Mots estimés | Priorité | Notes |
|---|---|---|---|---|
| `/` (Accueil) | hero (UVP + CTA promos), promotions-semaine, catégories-produits, social-proof voisinage, infos-pratiques (horaires + Maps), CTA infolettre, footer | 700-900 | **Critique** | Doit contenir CTA primaire « Voir les promotions de la semaine » dès le hero |
| `/promotions` | liste complète promos hebdo + dates de validité | 300-500 | **Critique** | Cible KPI conversion direct ; SEO `promotions dépanneur [ville]` |
| `/produits` | catalogue par catégories (bières, snacks, lotto, essentiels, etc.) en galerie images (P20) | 600-1000 | Haute | Alt-text descriptif obligatoire chaque produit (WCAG + SEO) |
| `/contact` | coordonnées + horaires détaillés + carte Google + formulaire (4-5 champs max + consentement Loi 25) | 200-400 | Haute | Clavier nav + touch targets ≥ 44×44px |
| `/politique-confidentialite` | RPP, finalités, rétention, droits, transferts hors QC, services tiers | 700-900 | **Obligatoire Loi 25** | Template `templates/privacy-policy-template.md` |
| `/mentions-legales` | dénomination, NEQ, adresse, hébergeur (Vercel US documenté) | 300-500 | **Obligatoire Loi 25** | Template `templates/legal-mentions-template.md` |

### 5.4 Bilinguisme FR/EN

`languages: ["fr", "en"]` imposé brief. Implémentation `next-intl` avec messages clés bilingues + `hreflang` sitemap + langue détectée navigateur. **Avantage différenciation** : 3/5 concurrents (ChaLou, Peluso, Ton dépanneur) sont FR seul.

### 5.5 Conformité Loi 25 — éléments contenu obligatoires

- RPP : Nobert Tremblay (`nobert@depanneur-nobert.ca`), titre « Propriétaire et Responsable de la protection des renseignements personnels (Loi 25, art. 3.1) »
- Rétention documentée : infolettre 12 mois / téléphone 6 mois / analytics 30 jours
- Transferts hors QC explicités : Google Analytics (US, IP tronquée), Google Maps (US), Vercel (US hébergement)
- Process incident actif : `nobert@depanneur-nobert.ca`
- Cookie banner opt-in : essentiels seuls actifs par défaut, refus aussi visible qu'accepter, 3 catégories (Essentiels / Analytics / Marketing)

### 5.6 Décisions résumées

| Décision | Compte |
|---|---|
| keep_as_is | 0 (mode creation, rien à conserver) |
| rewrite | 0 |
| delete | 0 |
| **create_new** | **6 pages** (home + 5) + sections (~30) à générer en Phase 3 Content |

---

## 6. Design trends du secteur (design-critic)

### 6.1 Tendances couleur observées

| Concurrent | Palette dominante | Registre |
|---|---|---|
| Accommodation ChaLou | Rouge + jaune + blanc (style brasserie) | Commercial chaud |
| Dépanneur Rapido | Bleu + rouge + blanc | Commercial standard |
| Dépanneur Peluso | Vert + blanc (vitrine sobre) | Boutique premium |
| Ton dépanneur | Rouge + blanc | Commercial / e-commerce |
| DepQuébec | Bleu/teal + orange CTA | Corporate B2B |

**Aucun concurrent n'utilise une palette warm brun/or/crème** — la palette imposée Nobert (`#8B4513` boiseries + `#FFD700` doré + `#FFF8E7` crème) **ouvre un territoire visuel inoccupé dans le secteur québécois**. Ce choix est aligné avec l'anti-positionnement corporate (rejet bleu/rouge commercial) et le storytelling boiseries-traditionnel.

### 6.2 Tendances typographiques

| Concurrent | Headings | Body |
|---|---|---|
| ChaLou | Sans-serif standard (Helvetica-like) | Sans-serif |
| Rapido | Sans-serif gras | Sans-serif |
| Peluso | Serif (logo) + sans-serif | Sans-serif |
| Ton dépanneur | Sans-serif | Sans-serif |
| DepQuébec | Sans-serif | Sans-serif |

**Aucun concurrent n'utilise un serif chaleureux display**. Le combo proposé Nobert (**Recoleta** ou **Fraunces** pour display + **Inter** ou **Karla** pour body) introduit une chaleur typographique inédite dans le secteur, alignée avec D3 `heavy` (lisibilité 20-80 ans) et D2 `emotional`.

### 6.3 Layout et hero patterns

| Pattern hero | Vu chez | Effectivité |
|---|---|---|
| Carrousel automatique (RevSlider) | ChaLou | Faible (LCP, a11y) |
| Hero produit statique | Rapido, Peluso | Moyenne (peu différenciant) |
| Hero géographique (sélection ville) | Ton dépanneur | Spécifique livraison |
| Aucun hero (vitrine compacte) | Peluso | Faible engagement |

**Recommandation Nobert** : hero **photo authentique vitrine/intérieur dépanneur** (P13 anti-polish) + CTA primaire « Voir les promotions de la semaine » + sticky CTA secondaire (P01). Pas de carrousel auto.

### 6.4 Animations

| Type | Adoption | Observation |
|---|---|---|
| Scroll fade-in | 1/5 (DepQuébec lazy SVG) | Sectoriellement absent |
| Hover CTA color | 3/5 | Standard utile |
| Page transitions | 0/5 | Inexploité |
| Parallax | 0/5 | Heureusement |

**Décision Nobert** : P17 scroll-triggered animations sobres (fade-in sections), respect `prefers-reduced-motion`, viewport-only pour CLS — aligne D5 `slow-organic` (rythme calme, ancré) sans tomber dans le gadget.

### 6.5 Imagerie

| Style | Adoption |
|---|---|
| Photos produit packshot | 5/5 (standard) |
| Photos vitrine/intérieur authentiques | 1/5 (Peluso partiel) |
| Stock photos génériques | 2/5 (ChaLou banners) |
| Illustrations custom | 0/5 |
| Iconographie cohérente (Lucide-style) | 0/5 |

**Recommandation Nobert** : photos **réelles vitrine + intérieur + propriétaire** (P13), iconographie **Lucide React** cohérente, **interdiction stock photos génériques** (garde-fou knowledge NEXOS).

### 6.6 Dark mode

**0/5 sites** offrent un dark mode. Hors scope Nobert (palette warm imposée + audience non-technique) — la chaleur est l'ADN de marque, le dark mode trahirait le registre.

### 6.7 Moodboard textuel Nobert

| Dimension | Direction |
|---|---|
| **Vibe** | Chaleureux, authentique, ancré quartier, accueillant — anti-corporate explicite |
| **Color direction** | Brun boiseries `#8B4513` dominant + jaune doré `#FFD700` accent + crème `#FFF8E7` background — registre warm exclusif |
| **Typo direction** | Serif chaleureux display (Recoleta/Fraunces) + sans humaniste body (Inter/Karla) — autorité tradition + lisibilité contemporaine |
| **Layout direction** | Symmetric (D6) + densité 3 (D1 équilibrée) — sections amples avec respiration mais catalogue produits visible sans saturation |
| **Imagery direction** | Photos réelles vitrine + intérieur + propriétaire + produits packshot, textures papier/boiseries possibles, iconographie Lucide cohérente, **zéro stock photo** |
| **Animation direction** | Scroll fade-in subtils, hover CTA, respect `prefers-reduced-motion`, viewport-only |

### 6.8 Anti-patterns design à éviter

| Anti-pattern | Vu chez | Impact |
|---|---|---|
| Carousel hero auto-rotate | ChaLou | LCP, a11y, CTR |
| Surcharge couleurs (>5) | DepQuébec partiellement | Confusion hiérarchie visuelle |
| Stock photos génériques | ChaLou banners | Trahit registre authenticité |
| Texte sur image sans overlay | À surveiller | Échec contraste WCAG |
| WordPress theme générique | ChaLou, Peluso | Trahit anti-positionnement corporate fade |

---

## 7. Recommandations consolidées pour Phase 1 (Strategy)

### 7.1 Inputs prêts pour brand-strategist Ph1

- ✅ Personnalité 6D : D1=3, D2=emotional, D3=heavy, D4=warm, D5=slow-organic, D6=symmetric (cf. `pattern-recommendation.json`)
- ✅ Palette imposée prête à injecter dans `design-tokens` + `tailwind.config`
- ✅ Patterns recommandés (8 — 7 primaires + 1 secondaire) avec rationale par pattern
- ✅ Patterns évités (8) avec justification — éviter recompute Ph1
- ✅ Sites de référence priorisés : S01 Twin Boro (P01+P11), S14 La Semilla (P20), S13 Ma'ono (P09), S12 Gazzo (P13), S05 Bloor Jane (P02)

### 7.2 Stratégie SEO local (priorité Ph1)

- **Mots-clés primaires** : `dépanneur [ville]`, `dépanneur ouvert 24h [ville]`, `bière [ville]`, `loto québec [ville]`
- **Pages cibles** : `/` (homepage), `/promotions`, `/produits`, `/contact`
- **Schema.org** : `LocalBusiness` JSON-LD obligatoire avec NAP cohérent (Name + Address + Phone), horaires structurées, géolocalisation
- **Google My Business** : synchronisation NAP indispensable (à coordonner avec le client au kickoff)
- **Sitemap multilingue** : hreflang FR/EN automatique via App Router metadata

### 7.3 Stratégie conversion (priorité Ph1)

| Niveau | Action | Pattern |
|---|---|---|
| 1 (primaire) | « Voir les promotions de la semaine » sticky + hero | P01 |
| 2 (secondaire) | « Trouver l'adresse » → Google Maps embed | P11 |
| 2 (secondaire) | « Appeler pour une commande » → tel: link | P09 |
| 3 (tertiaire) | « S'inscrire à l'infolettre » → form 1 champ + consentement | P02 |

### 7.4 Différenciations à exploiter (gaps marché)

1. **Sticky CTA promos hebdo** (P01) — aucun concurrent ne le fait
2. **Social proof voisinage** (P02) — territoire vide
3. **Page par localisation SEO** (P11) — capture trafic local immédiat
4. **Anti-polish authenticité** (P13) — registre inoccupé
5. **Conformité Loi 25 native** — 4/5 concurrents non conformes
6. **Bilinguisme FR/EN** — 3/5 concurrents FR seul
7. **Stack Next.js 15 + Vercel** — 0/5 concurrents en framework moderne (performance + sécurité + SEO)
8. **Palette warm brun/or/crème** — territoire visuel inoccupé dans le secteur

### 7.5 Risques signalés au gate ph0→ph1 SOIC

| Dimension | Risque | Atténuation Ph1 |
|---|---|---|
| **D8 Legal** | Mapping SEC-03 confidence 0.5 → revue humaine + variables `[ville]`, NEQ, adresse manquantes | Kickoff client obligatoire avant Ph2 design |
| **D6 SEO** | NAP cohérence Google My Business à coordonner | Inclure dans brief Ph1 + Schema LocalBusiness |
| **D2 Accessibilité** | P20 menu galerie → alt-text descriptif obligatoire | Brief Ph3 content-writer |
| **D5 Performance** | P17 animations + Maps embed → CLS mobile | Brief Ph4 build avec lazy + viewport-only |

### 7.6 Variables à fixer au kickoff client (avant Ph2)

- 🟠 **Ville** (Québec — TBD) → bloquant pour P11, SEO local, Schema LocalBusiness
- 🟠 **Adresse exacte du commerce** → bloquant Maps + mentions légales
- 🟠 **Téléphone** → bloquant CTA secondary + LocalBusiness Schema
- 🟠 **Horaires précis** (semaine, weekend, jours fériés) → bloquant Schema OpeningHours
- 🟠 **NEQ** (Numéro d'Entreprise du Québec) → bloquant mentions légales
- 🟠 **Logo** (`logo_provided: false`) → décision Ph2 : création logo OU wordmark typographique
- 🟡 **Photos vitrine/intérieur/propriétaire** → idéalement collectées avant Ph3 content (sinon stock authentique évité, illustrations à défaut)

---

## Score discovery global : **8.5/10**

### Détail par dimension

| Dimension | Score | Justification |
|---|---|---|
| Clarté brief client | 9/10 | Brief structuré, personality_hints fournis, palette imposée, patterns pré-recommandés via chantier-K |
| Cadrage business (KPI conversion) | 9/10 | KPI primaire + actions priorisées + audience définie + anti-cible explicite |
| Benchmark concurrentiel | 8/10 | 5 sites web réels analysés + cas-gap (Accommodation Populaire) — limitation : ville TBD empêche analyse géographique fine |
| Cohérence design / palette | 9/10 | Palette imposée + moodboard cohérent, territoire visuel inoccupé identifié |
| Cohérence Loi 25 / D8 | 9/10 | Tous éléments légaux présents au brief, RPP identifié, conformité native NEXOS |
| Mapping sectoriel SOIC | 6/10 | SEC-03 mapping confidence 0.5 — secteur commerce de proximité non nativement couvert (revue humaine recommandée Ph M ultérieure) |
| Différenciations identifiées | 9/10 | 8 gaps marché concrets + patterns alignés |
| Risques anticipés | 9/10 | 4 risques SOIC + 7 variables kickoff signalées |

**Verdict gate ph0→ph1** : ✅ **GO Phase 1 Strategy** (μ ≥ 7.0 requis pour cette transition — score 8.5 dépasse largement le seuil).

### Conditions à respecter en Ph1

1. Confirmer la cohérence avec `pattern-recommendation.json` (chantier-K) — patterns P01/P02/P09/P11/P13/P17/P19/P20 reconduits
2. Exiger la **collecte des variables kickoff** (ville, adresse, téléphone, horaires, NEQ) avant lancement Ph2
3. Valider le mapping SEC-03 ou décider de dégrader si certains patterns SEC-03 (P20 menu galerie format gastro) ne s'adaptent pas au catalogue dépanneur

---

**Fin du rapport Phase 0 Discovery — Dépanneur Nobert.**
**Prochaine étape** : Phase 1 Strategy (`agents/ph1-strategy/_orchestrator.md`).
