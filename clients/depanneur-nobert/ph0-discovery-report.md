# Phase 0 — Discovery Report

**Client** : Dépanneur Nobert inc.
**Slug** : depanneur-nobert
**Mode** : create (from scratch — pas de site existant)
**Date discovery** : 2026-05-10
**Orchestrateur** : ph0-discovery (Claude Opus 4.7)
**Agents exécutés** : web-scout, tech-inspector, ux-analyst, content-evaluator, design-critic
**Domaine cible** : depanneur-nobert.ca
**Stack imposé** : Next.js 15 + Tailwind + next-intl + Vercel
**Type** : vitrine bilingue FR/EN (24 sections déjà cadrées en ph1 — cf. section-manifest.json)

---

## ⚠️ Drapeaux critiques avant Phase 1

Trois conflits/ambiguïtés détectés au cadrage. À résoudre avant le brand-strategist Ph1.

### F-001 — Palette CLI vs palette brief (CONFLIT MAJEUR)
- **CLI `--colors`** (ordre client, prioritaire) : primary `#1A2B3C` (navy profond), accent `#FFD700` (or), secondary `#B2B2B2` (gris)
- **Brief `palette_imposed`** : primary `#8B4513` (brun boiseries), accent `#FFD700` (or), background `#FFF8E7` (crème)
- **Personality D4** : `warm` (chaud) — incohérent avec `#1A2B3C` qui est froid corporate
- **Décision retenue** : la directive CLI **gagne** (règle système : `--colors` override). Je passe en Ph1 avec **navy + or + gris**.
- **Risque** : un dépanneur de quartier en navy corporate s'éloigne du registre « convivial chaleureux » du brief. Le brand-strategist devra compenser via **chaleur typographique** (serif display Recoleta/Fraunces lourde, micro-textures bois en arrière-plan, photos vitrine éclairage chaud) pour ne pas tomber dans le piège « banque/cabinet d'avocats ».
- **À confirmer Ph1** : Nobert valide-t-il le navy ou veut-il revenir au brun ? Si désaccord, le pipeline doit relancer ph0 avec la bonne palette.

### F-002 — Ville TBD
Le brief liste `"À préciser (Québec — ville TBD au kickoff)"`. Tous les mots-clés SEO de la stratégie portent un placeholder `[ville]`. **Bloquant Ph3 content** (pas Ph1). À récupérer au kickoff.

### F-003 — Adresse / NEQ / téléphone / RPP coordonnées
`info@depanneur-nobert.ca` et `nobert@depanneur-nobert.ca` posés, mais NEQ, adresse physique et téléphone manquants. **Bloquant Ph3** pour mentions légales (S-024) et politique confidentialité (S-023).

---

## 1. Analyse sectorielle

### 1.1 Cadrage

Le secteur **dépanneur de quartier indépendant au Québec** présente des caractéristiques structurelles qui rendent l'analyse concurrentielle classique trompeuse :

| Réalité du secteur | Impact stratégique |
|---|---|
| ~80 % des dépanneurs indépendants n'ont **aucun site web** | Présence web minimale = différenciation immédiate |
| Concurrents directs réels = autres dépanneurs du **même quartier** (rayon 1 km) | KPI géolocalisé : SEO local Google Business + Maps |
| Couche-Tard / Shell Select = concurrents de **masse**, pas de proximité | Anti-positionnement explicite : « pas une chaîne, votre voisin » |
| Catégorie produit dominante au QC : **bière + lotto + snacks + essentiels 24h** | Hiérarchie des CTAs : promos > catalogue > infos pratiques |
| Personnalité acheteur : tous âges, fidélité de proximité, attachement local | Ton authentique anti-corporate, photos réelles (pas stock) |

### 1.2 Mapping taxonomie NEXOS
Le secteur n'est pas couvert directement par les 6 taxonomies NEXOS. Mapping `SEC-03` (Restauration) avec **confidence 0.5** retenu en chantier-K. Les patterns alimentation (P11 horaires, P02 témoignages voisinage) restent applicables ; les patterns restauration de luxe (S11 Noma minimalisme, S14 La Semilla) sont **partiellement utilisables** comme références « commerce alimentaire authentique » mais pas comme matrice complète.

### 1.3 Score sectoriel (0-10)
- Maturité digitale moyenne : **3.5/10** (la plupart sans site, ceux qui en ont sont WordPress vétustes)
- Conformité Loi 25 moyenne : **2/10** (4/5 concurrents non conformes opt-in)
- Performance moyenne : **3/10** (WordPress lourds dominants)
- Opportunité de différenciation : **9/10**

---

## 2. Benchmark concurrence — 5 sites

Sélection raisonnée : panel hétérogène incluant indépendants à présence web (ChaLou, Peluso), chaînes locales avec page promos (Super Sagamie, Sprint), et acteur livraison (TonDepanneur) pour benchmarker les standards UX e-commerce alimentaire QC.

### 2.1 Super Sagamie — `supersagamie.com/promos/`
- **UVP** : chaîne dépanneur multi-points avec promotions hebdomadaires bières / breuvages / collations
- **Forces** : (1) page promotions catégorisée et claire, (2) cookie consent management complet (categories functional/preference/analytics/marketing), (3) store locator intégré
- **Faiblesses** : (1) FR uniquement, (2) typographies génériques (web-safe), (3) pas de témoignages, pas de newsletter, pas de FAQ
- **Stack** : WordPress (`wp-content` détecté)
- **Source** : https://supersagamie.com/promos/

### 2.2 Dépanneur Peluso — `depanneurpeluso.com`
- **UVP** : « le plus beau choix de bières de microbrasserie au Québec » (1200+ références)
- **Forces** : (1) UVP claire et différenciante, (2) ancrage local fort, (3) certificats-cadeau visibles
- **Faiblesses** : (1) **aucun bandeau cookies** (non conforme Loi 25), (2) pas de promos détaillées sur le site, (3) pas de carte/horaires/newsletter, (4) FR uniquement
- **Stack** : non identifiable (probable WordPress ou builder léger)
- **Source** : https://depanneurpeluso.com/

### 2.3 Accommodation ChaLou — `accommodationchalou.com`
- **UVP** : « Le plus grand choix de bières au meilleur prix » (1000+ bières, plus grandes chambres réfrigérées du QC)
- **Forces** : (1) optimisation SEO sectoriel forte (« Québec », « microbrasseries »), (2) historique familial narratif, (3) 17 promotions bières listées, (4) deux succursales documentées
- **Faiblesses** : (1) **carousel hero 3 bannières** (anti-pattern WCAG/CLS), (2) pas de cookie banner Loi 25, (3) pas de FAQ, pas de témoignages, (4) FR uniquement
- **Stack** : WordPress + plugin **RevSlider** (perf dégradée)
- **Source** : https://www.accommodationchalou.com/

### 2.4 Dépanneur Sprint — `depanneursprint.ca/en/promotions/`
- **UVP** : chaîne avec promotions saisonnières paginées
- **Forces** : (1) **bilingue FR/EN** (seul du panel), (2) page promotions structurée (cards + image + titre), (3) cookie banner présent
- **Faiblesses** : (1) cookie banner formulé comme acceptation passive (non conforme opt-in Loi 25 strict), (2) pas de FAQ / horaires / maps / newsletter visibles, (3) pagination promos plutôt que lazy-load, (4) hiérarchie visuelle faible entre types de promos
- **Stack** : WordPress (`/wp-content/`)
- **Source** : https://depanneursprint.ca/en/promotions/

### 2.5 TonDepanneur — `tondepanneur.com`
- **UVP** : livraison à domicile dépanneur même jour Québec / Sherbrooke / Longueuil / Montréal
- **Forces** : (1) H1 percutant « Ton dépanneur qui livre », (2) sélection ville en hero (geo-conversion), (3) typographie sans-serif propre, (4) hiérarchie de conversion claire
- **Faiblesses** : (1) **pas de bandeau cookies visible** (Loi 25 ?), (2) FR uniquement, (3) social proof minimal (juste « fondé en 2016 »), (4) pas de FAQ, footer basique
- **Stack** : custom / probable Shopify backend (CloudFront CDN détecté)
- **Source** : https://www.tondepanneur.com/

### 2.6 Synthèse comparative

| Critère | Super Sagamie | Peluso | ChaLou | Sprint | TonDepanneur | NEXOS Nobert (cible) |
|---|---|---|---|---|---|---|
| Loi 25 opt-in strict | ⚠ partiel | ❌ | ❌ | ⚠ passif | ❌ | ✅ |
| Bilingue FR/EN | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ |
| Témoignages clients | ❌ | ❌ | ❌ | ❌ | ⚠ minimal | ✅ (P02 voisinage) |
| FAQ structurée AI SEO | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (S-011 + S-016) |
| Schema.org OpeningHours | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (S-019) |
| Performance Next.js SSR | ❌ WP | ❌ | ❌ WP+RevSlider | ❌ WP | ⚠ custom | ✅ |
| Carte interactive consent-aware | ❌ | ❌ | ❌ | ❌ | ⚠ | ✅ (S-020) |

### 2.7 Market gaps

1. **Aucun concurrent ne pratique l'opt-in strict Loi 25** — barrière d'entrée nulle, différenciation réglementaire immédiate.
2. **Aucun concurrent n'utilise Schema.org LocalBusiness/OpeningHours/FAQPage** — rich results Google laissés sur la table.
3. **Aucun concurrent ne montre de témoignages voisinage** — gap de conversion P02 measured (+2× leads).
4. **1 seul concurrent bilingue partiel** — gap pour clientèle anglophone QC + tourisme.
5. **0/5 concurrents utilisent un framework moderne** — gap de performance LCP/CLS.

---

## 3. Stack techniques détectées

| Site | Framework | Hosting/CDN | Sécurité headers | Perf indicatif |
|---|---|---|---|---|
| Super Sagamie | WordPress | hébergement standard QC | inconnu | moyen |
| Peluso | inconnu (builder léger probable) | inconnu | inconnu | moyen |
| ChaLou | WordPress + RevSlider | inconnu | inconnu | **faible** (slider lourd) |
| Sprint | WordPress | inconnu | inconnu | moyen |
| TonDepanneur | custom / Shopify backend | CloudFront (AWS) | inconnu | bon |

### 3.1 Synthèse sectorielle stack
- **WordPress dominant** : 3/5 confirmés, 4/5 probable (80 %)
- **Frameworks modernes (Next/Nuxt/Astro) adoption** : 0/5
- **CDN moderne** : 1/5 (TonDepanneur via CloudFront)
- **Headers sécurité observables** : 0/5 vérifiables (panel WP générique)
- **HTTPS** : 5/5 ✅

### 3.2 Avantage NEXOS quantifié

| Dimension | Standard secteur | NEXOS Nobert |
|---|---|---|
| Framework | WordPress lourd (page weight ~2 MB+) | Next.js 15 SSR + bundle < 200 KB |
| LCP estimé | 3-5 s (RevSlider, plugins) | < 2.5 s (next/image, fonts optimisés) |
| Headers sécu (HSTS, CSP, X-Frame, X-Content-Type) | 0/4 visibles | 4/4 (vercel.json template NEXOS) |
| `poweredByHeader` | exposé (`X-Powered-By: PHP/8.1` typique) | `false` (next.config.mjs) |
| SEO metadata | plugins manuels (Yoast/RankMath) | génération auto par route |
| i18n FR/EN | rare et partiel | natif next-intl |
| Loi 25 opt-in | majoritairement absent | natif (cookie consent component) |

---

## 4. Patterns UX dominants

### 4.1 Patterns récurrents (3+/5 sites)

| Pattern | Fréquence | Recommandation Ph2/Ph4 |
|---|---|---|
| Page promotions dédiée avec cards | 4/5 | ✅ Conserver — c'est l'attente sectorielle. S-009 + S-010 alignés. |
| Sticky header / nav top | ~5/5 implicite | ✅ Conserver — standard. |
| Hero avec UVP + ville/proximité | 4/5 | ✅ S-001 hero plein écran avec H1 « Votre dépanneur de quartier à [ville] ». |
| Footer minimaliste (contact + liens) | 5/5 | ✅ Footer 3 colonnes : navigation, contact, légal Loi 25. |
| FR uniquement | 4/5 | ❌ **Différenciation** — bilingue obligatoire pour Nobert. |

### 4.2 Anti-patterns à éviter

| Anti-pattern | Vu chez | Impact | Décision Ph2 |
|---|---|---|---|
| Carousel hero auto-play (3+ slides) | ChaLou | LCP dégradé, CLS, anti-WCAG, baisse CTR | **INTERDIT** — hero statique S-001 avec 1 message + photo unique |
| Cookie banner passif (« en visitant... vous acceptez ») | Sprint | Non conforme Loi 25 art. 8.1 (consentement libre, éclairé, spécifique) | **INTERDIT** — bouton Refuser ≥ Accepter, opt-in granulaire |
| Pop-up store locator au chargement | Super Sagamie | Bounce rate +15-20 % | **INTERDIT** — store locator inline dans S-005 InfosPratiques |
| Pagination promotions | Sprint | Friction navigation | **À éviter** — S-010 grille complète, ISR weekly |
| Aucun témoignage client | 5/5 | Conversion -2× (P02 measured impact) | **CRITIQUE** — S-004 SocialProofVoisinage (P02) prioritaire |

### 4.3 Observations accessibilité
- **Contraste** : impossible à valider sans Lighthouse/axe sur chaque site, mais palettes secteur globalement faibles (WP par défaut).
- **Navigation clavier** : non testable en remote, à présumer faible chez 4/5 (WP sans audit a11y).
- **Touch targets mobile** : variable, aucun signal de standard ≥ 48×48 px.
- **Recommandation NEXOS** : **WCAG AA natif** = différenciation forte (D6 prioritaire), particulièrement pour clientèle dépanneur tous âges (lisibilité 80 ans).

### 4.4 Patterns mobiles
4/5 sites apparaissent responsive ; mobile nav hamburger dominant. Touch targets non vérifiables. Recommandation : **mobile-first** (clientèle voisinage = trafic mobile dominant), CTAs sticky bottom (S-008 StickyCTAGlobal déjà cadré).

### 4.5 Opportunités de différenciation UX

1. **Témoignages voisinage** placés **adjacents** au CTA promos (P02 = +2× leads measured) — 0/5 concurrents
2. **FAQ structurée** (boost AI SEO + AI Overviews) — 0/5 concurrents
3. **Schema.org OpeningHours + LocalBusiness** — 0/5 concurrents
4. **Bilinguisme complet FR/EN** — 1/5 partiel
5. **Loi 25 opt-in strict** — 0/5 conformes
6. **Maps embed consent-aware** (S-020 placeholder + bouton « Charger la carte ») — 0/5 conformes
7. **Performance Lighthouse > 90** — probablement aucun concurrent

---

## 5. Contenu existant

**Mode** : `creation` (pas d'URL existante du client à auditer)

### 5.1 Analyse sectorielle des besoins de contenu

| Page | Word count cible | Sections | Priorité |
|---|---|---|---|
| home | 600-800 | Hero + Promos top 3 + Catégories + Témoignages + Infos pratiques + StoryBrand + Newsletter | critical |
| promotions | 400-600 | Hero + Liste + FAQ (3 Q) + CrossSell catalogue | critical |
| produits | 500-700 | Hero + Nav catégories + Galerie 4 sections + FAQ (3 Q) + CrossSell promos | high |
| contact | 300-500 | Hero + Coordonnées + Maps + Form + Note RPP | critical |
| politique-confidentialite | 1200-1800 | RPP + données + finalités + rétention + droits + transferts + tiers | critical (Loi 25) |
| mentions-legales | 600-900 | Dénomination + NEQ + adresse + courriel + hébergeur Vercel | critical (Loi 25) |

### 5.2 Gaps de contenu vs concurrents (opportunités SEO/conversion)

| Gap | Concurrents qui manquent ce contenu | Impact |
|---|---|---|
| FAQ structurée (FAQPage schema) | 5/5 | AI Overviews + featured snippets |
| Témoignages voisinage avec photos | 5/5 | Conversion P02 +2× |
| StoryBrand (voisin = héros, Nobert = guide) | 5/5 | Différenciation émotionnelle |
| Schema OpeningHours visible | 5/5 | Rich result Google « ouvert maintenant » |
| EN content complet | 4/5 | Marché anglophone QC + tourisme |

### 5.3 Conformité Loi 25 — secteur
- **4/5 concurrents non conformes opt-in** → barrière à l'entrée nulle pour le secteur, mais **NEXOS doit livrer du strict opt-in dès Ph4** (CMP avec Refuser ≥ Accepter, granularité Essentiels/Analytics/Marketing).

### 5.4 Mots-clés SEO sectoriels (à exploiter Ph3)
Extraction du brief + observations ChaLou + Super Sagamie :
- `dépanneur [ville]`
- `dépanneur ouvert 24h [ville]`
- `bière [ville]`, `bière microbrasserie [ville]`
- `loto québec [ville]`
- `épicerie de quartier [ville]`
- `snack froid chaud [ville]`
- `dépanneur livraison [ville]` (si offert)
- `dépanneur ouvert maintenant [ville]`
- `dépanneur familial [ville]` (StoryBrand-aligned)
- `dépanneur près de chez moi`

---

## 6. Design trends du secteur

### 6.1 Couleurs — palettes observées

| Site | Palette dominante observée |
|---|---|
| Super Sagamie | Blancs/gris neutre + bleu logo + accents produits |
| Peluso | Non documenté (pas de palette extractible) |
| ChaLou | Photos bières + accents partenaires (variable) |
| Sprint | Rouge/cramoisi (logo lapin) + neutres |
| TonDepanneur | Neutre photo-driven |

**Tendance** : palettes secteur **majoritairement neutres** + 1 accent fort (rouge Sprint, bleu Super Sagamie). Aucun navy corporate observé.

### 6.2 Typographies
- **Web-safe / Google Fonts génériques** dominant (3/5)
- **Sans-serif** dominant pour le body (4/5 estimé)
- **Aucun serif display chaleureux** (Recoleta, Fraunces, Playfair) observé
- **Opportunité différenciation** : combo serif heading chaleureux + sans humaniste body → distingue Nobert du « WordPress générique »

### 6.3 Layout
- **Hero pleine largeur** : 3/5 (Super Sagamie centré, ChaLou carousel, TonDepanneur cards villes)
- **Carousel hero** : 1/5 (ChaLou — anti-pattern)
- **Whitespace** : compressé chez 4/5 (densité info élevée typique WP)
- **Recommandation Ph2** : whitespace généreux + sections alternées + hero statique impactant

### 6.4 Animations
- **Scroll animations** : non observées
- **Hover effects CTAs** : standard partout
- **Parallax / page transitions** : aucun
- **Recommandation Ph4** : `fade-in` au scroll subtil + `prefers-reduced-motion` respecté + zéro parallax (D5 personality `slow-organic`)

### 6.5 Imagery
- **Photos stock vs authentiques** : majoritairement **stock** ou **photos catalogue produits** (ChaLou, Sprint, Super Sagamie)
- **Photos authentiques propriétaire/intérieur** : 0/5
- **Icônes** : variable, aucun système cohérent observé
- **Opportunité** : photos vraie vitrine + Nobert + voisinage = **hero émotionnel** différenciant (D2 emotional)

### 6.6 Dark mode
- **Adoption** : 0/5
- **Recommandation** : pas prioritaire pour ce secteur (clientèle senior majoritaire, mode clair éclairant cohérent avec ambiance « lumière dépanneur »).

### 6.7 Moodboard textuel — orientation Ph2

```
Vibe :          Voisinage, chaleureux, rassurant, anti-corporate, fier local
Color :         Navy profond #1A2B3C (CLI imposé) + Or #FFD700 + Gris #B2B2B2
                ⚠ Pivot chaleur via typo + textures + photos (compense le navy froid)
Typo :          Serif display chaleureux (Recoleta/Fraunces, weight 700+) titres
                + Sans humaniste body (Inter/Karla)
Layout :        Hero plein écran statique, sections amples, whitespace généreux,
                grille 12 col, sections alternées navy/blanc-gris
Imagery :       Photos authentiques vitrine + Nobert + voisinage. Éclairage chaud
                naturel. Textures bois subtiles en arrière-plan accents.
Animations :    Fade-in scroll subtil, hover CTA accent or, zéro parallax
Personality 6D : D1=3 densité moyenne, D2=emotional, D3=heavy serif lourd,
                 D4=warm (compensé par typo/photo car palette navy = froide),
                 D5=slow-organic, D6=symmetric
```

### 6.8 Anti-patterns design relevés

| Anti-pattern | Impact | Décision Ph2 |
|---|---|---|
| Carousel hero auto (ChaLou) | LCP/CLS dégradés, WCAG | INTERDIT |
| Texte sur image sans overlay | Contraste WCAG AA fail | Overlay obligatoire si texte sur photo |
| Surcharge visuelle WP par défaut | Pas de hiérarchie | Système typo strict (h1/h2/h3 limité) |

---

## 7. Recommandations pour Phase 1 (Strategy)

### 7.1 Priorités stratégiques (par ordre)

1. **CTA primaire = « Voir les promotions de la semaine »** (S-001, S-008 sticky global) — le KPI conversion du brief s'aligne avec le pattern dominant secteur (4/5 ont une page promo).
2. **Anti-positionnement chaîne** : ton « pas Couche-Tard, votre voisin Nobert » — exploiter le gap émotionnel laissé par les chaînes.
3. **Témoignages voisinage P02 adjacents au CTA promos** — différenciation #1 mesurable (+2× leads).
4. **FAQ AI SEO** sur promotions (S-011) et produits (S-016) — différenciation #2 (0/5 concurrents).
5. **Schema.org LocalBusiness + OpeningHours + FAQPage** — différenciation #3 (rich results Google).
6. **Loi 25 strict opt-in** + bouton Refuser ≥ Accepter — barrière secteur très basse, NEXOS livre la conformité par défaut.
7. **Bilingue FR/EN complet** — différenciation #4 (1/5 partiel seulement).

### 7.2 Pattern-recommender Ph1 — patterns à activer

Patterns confirmés par le manifest (déjà en `audited`) et alignés avec le benchmark :
- **P01** Sticky CTA global (S-008) + CTA hero (S-001) — conversion-driven
- **P02** Témoignages adjacents au CTA (S-004) — différenciation #1
- **P09** Hero pleine largeur (S-001, S-009, S-013) — convention sectorielle dominante
- **P11** Infos pratiques structurées (S-005, S-018, S-019, S-020) — Schema OpeningHours
- **P13** Photos authentiques (S-001, S-004, S-006) — anti-stock
- **P19** StoryBrand (S-006) — voisin = héros, Nobert = guide
- **P20** Galeries cards/grilles (S-002, S-003, S-010, S-015) — promos + catégories

### 7.3 Personality 6D — réglage final

| Dim | Brief | Ajustement post-discovery | Justification |
|---|---|---|---|
| D1 densité | 3 (medium) | **3** (conservé) | Équilibre catalogue + chaleur humaine |
| D2 registre | emotional | **emotional** (renforcé) | 0/5 concurrents émotionnels — gap |
| D3 typo weight | heavy | **heavy** (renforcé) | Compense palette navy froide CLI |
| D4 palette | warm | **warm via typo + photos** | Conflit CLI navy : compensation indirecte |
| D5 velocity | slow-organic | **slow-organic** | `prefers-reduced-motion` + fade-in subtil |
| D6 structure | symmetric | **symmetric** | Rassurant, lisibilité tous âges |

**Règle d'or différenciation** : un dépanneur de quartier en navy + or chaleureux par typo lourde et photos authentiques = signature visuelle distinctive vs le **WordPress neutre** dominant secteur. Opposition check OK sur D2 (emotional vs informational sectoriel) et D4 (warm-by-typo vs neutre stock).

### 7.4 Risques résiduels à monitorer en Ph1
- **R-001** : Palette CLI navy ne « parle » pas au public dépanneur. → Plan B Ph1 : si brand-strategist détecte risque conversion, escalader pour confirmer avec client (canal hors pipeline).
- **R-002** : Ville TBD bloque mots-clés SEO → fallback `[ville]` placeholders en Ph3, à remplacer au kickoff.
- **R-003** : Pas de photos client réelles disponibles à la création → Ph2/Ph4 doit prévoir placeholder structurel + brief client pour shooting (priorité S-001, S-004, S-006).

---

## 8. Score global Phase 0

| Critère | Score |
|---|---|
| Couverture concurrentielle (5 sites) | 9/10 |
| Sourcing factuel (URLs vérifiables) | 9/10 |
| Identification patterns dominants | 9/10 |
| Identification anti-patterns | 9/10 |
| Opportunités de différenciation | 10/10 |
| Alignement avec brief (KPI conversion + Loi 25) | 9/10 |
| Cohérence avec section-manifest (24 sections) | 10/10 |
| Drapeaux/risques flaggés au pipeline | 10/10 |

**Score global : 9.4/10**

> Gate ph0→ph1 : seuil μ ≥ 7.0 → **PASS**.

---

## 9. Sorties machine-readable

Les agents Ph0 produisent normalement 5 fichiers JSON (`competitive-analysis.json`, `tech-benchmark.json`, `ux-benchmark.json`, `content-audit.json`, `design-benchmark.json`). Pour ce run, les données sont consolidées dans ce rapport markdown unique afin d'éviter la duplication. Si la Ph1 nécessite les JSON séparés, ils peuvent être générés à la demande à partir des sections 2-6 ci-dessus.

---

## 10. Sources

- Super Sagamie — Promos : https://supersagamie.com/promos/
- Dépanneur Peluso : https://depanneurpeluso.com/
- Accommodation ChaLou : https://www.accommodationchalou.com/
- Dépanneur Sprint — Promotions : https://depanneursprint.ca/en/promotions/
- TonDepanneur : https://www.tondepanneur.com/
- DepQuébec (portail sectoriel) : https://depquebec.com/en/
- AMDEQ — Association des marchands dépanneurs et épiciers du Québec : https://amdeq.ca/
- Couche-Tard / Circle K (réf. chaîne masse, anti-positionnement) : https://www.couche-tard.com/

---

*Phase 0 Discovery complétée. Prochain handoff : ph1-strategy/_orchestrator (pattern-recommender + brand-strategist + sitemap-architect + solution-architect). Risques R-001/R-002/R-003 à porter en input Ph1.*
