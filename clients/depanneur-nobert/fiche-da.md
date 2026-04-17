# Fiche DA — Dépanneur Nobert

> **Direction artistique condensée** pour la Phase L (création via `nexos create`).
> Source : `brief-client.json` + `pattern-recommendation.json` (chantier-K).

---

## Personnalité (matrice 6D)

| Dim | Valeur | Rationale |
|---|---|---|
| D1 Densité | **3** (équilibrée) | Catalogue produits visible sans saturation, positionnement accessible |
| D2 Registre | **emotional** | Convivialité de quartier, anti-corporate par nature |
| D3 Typo | **heavy** | Lisibilité immédiate clientèle tous âges (20-80 ans) |
| D4 Palette | **warm** | Brun boiseries + or doré — rejet explicite du bleu corporate |
| D5 Vélocité | **slow-organic** | Commerce ancré, pas de gadget (opposé mechanical/fast) |
| D6 Structure | **symmetric** | Rassurante, classique, accessible à tous |

**Règle d'or** : PASS — 4 oppositions vs `electro-maitre-industriel` (D2, D4, D5, D6). Oppositions faibles vs clinique-aura et table-de-marguerite attendues (tous emotional+warm).

---

## Palette (imposée)

| Rôle | Code | Usage |
|---|---|---|
| `primary` | `#8B4513` | Brun boiseries — titres, liens, éléments principaux |
| `primary-hover` | `#A0522D` | Hover state |
| `accent` | `#FFD700` | Jaune doré — CTA, highlights, promotions |
| `background` | `#FFF8E7` | Fond crème — accueillant |
| `surface` | `#FFFFFF` | Cartes produits, sections contrastées |
| `text` | `#2A1810` | Texte principal — chocolat foncé |
| `text-muted` | `#6B4F3C` | Texte secondaire, métadonnées |
| `border` | `#D4C5A9` | Bordures subtiles, séparateurs |

Rationale : brun chaleureux + jaune doré + fond crème. Aucun bleu, aucun gris corporate.

---

## Typographie (propositions)

- **Display** : `Recoleta` OU `Fraunces` (serif chaleureux avec caractère — italique contextuel possible via Fraunces)
- **Body** : `Inter` OU `Karla` (sans humaniste, lisibilité écran)
- **Weights** : display 700, body 400/500, micro-copy 400
- **Import** : via `next/font` (préchargement + CLS-safe)

---

## Patterns recommandés (depuis `pattern-recommendation.json`)

### Primaires (7)

1. **P01 Sticky CTA persistant** — "Voir les promotions de la semaine" omniprésent
2. **P02 Social proof adjacente CTA** — témoignages voisinage (+2× leads measured)
3. **P09 3-word brand messaging** — "Ton dépanneur. Ton quartier." ou variant local
4. **P11 Page par localisation** — SEO `dépanneur + [ville]`
5. **P13 Anti-polish authenticity** — textures papier/boiseries, photos non retouchées
6. **P17 Scroll-triggered animations** — sobres, `prefers-reduced-motion` respecté
7. **P20 Menu galerie images** — catalogue visuel produits + promotions

### Secondaire (1)

8. **P19 StoryBrand messaging** — cadre narratif home/about (+420% trafic measured)

### Évités (explicites)

P04 Hero vidéo (coût solo), P07 portfolio (solo), P08 Story-first (redondant P19), P10 démo interactive (solo), P12 palette shift (palette imposée), P14 code-breaking (hors registre), P15 gamified (WCAG + solo), P18 micro-univers (overkill).

---

## Sites de référence à étudier

| Priorité | ID | Site | Patterns couverts |
|---|---|---|---|
| 1 | S01 | [Twin Boro](https://twinboro.com) (SEC-01) | P01 + P11 — multi-localisations |
| 2 | S14 | [La Semilla](https://lasemillanyc.com) (SEC-03) | P20 — menu galerie images |
| 2 | S13 | [Ma'ono](https://maono.com) (SEC-03) | P09 — palette cousine (jaune bold + warm) |
| 2 | S12 | [Gazzo](https://gazzo.dk) (SEC-03) | P13 — anti-polish authentique |
| 2 | S05 | [Bloor Jane](https://bloorjanephysio.com) (SEC-01) | P02 — social proof measured |

---

## Sections / pages requises

| Page | Sections |
|---|---|
| `/` (Accueil) | hero, promotions-semaine, catégories-produits, infos-pratiques, carte-google, cta-infolettre |
| `/promotions` | liste complète promotions hebdo |
| `/produits` | catalogue par catégories (galerie P20) |
| `/contact` | coordonnées + heures + formulaire + carte |
| `/politique-confidentialite` | **Loi 25** — RPP, finalités, rétention, droits |
| `/mentions-legales` | dénomination, NEQ, adresse, hébergeur |

---

## Loi 25 (rappel obligatoire)

- **RPP** : Nobert Tremblay (`nobert@depanneur-nobert.ca`)
- **Cookie consent** : opt-in (essentiels actifs par défaut, refus aussi visible qu'accepter)
- **Données collectées** : courriel (infolettre), téléphone (commandes), navigation (analytics)
- **Transferts hors QC** : oui (Google Analytics IP tronquée, Google Maps, Vercel US) — documentés en politique
- **Rétention** : infolettre 12 mois, téléphone 6 mois, analytics 30 jours
- **Incident** : process actif, email `nobert@depanneur-nobert.ca`

---

## Contraintes stack (imposées)

- **Framework** : Next.js 15+ (App Router)
- **CSS** : Tailwind
- **i18n** : `next-intl` (fr + en)
- **Déploiement** : Vercel
- **Images** : `next/image` obligatoire (CLS-safe + optimisation)
- **Fonts** : `next/font` (préchargement)

---

## Notes pour Phase L

- **Sector mapping SEC-03 avec confidence 0.5** — revue humaine recommandée avant de coder. Si l'approximation gêne (ex: P20 menu galerie = format gastronomie, peu adapté à des boîtes de céréales), dégrader vers layout grille simple.
- **Variable `[ville]`** à fixer au kickoff (adresse + téléphone + horaires manquants du brief — placeholders TBD).
- **NEQ** : à obtenir auprès du propriétaire avant publication mentions légales.
- **Logo** : non fourni (`logo_provided: false`) — Phase ph2 devra gérer création ou wordmark typographique.
