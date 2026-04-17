# Images — La Table de Marguerite

Les SVG placeholders sont **volontairement schématiques** — leur rôle est de permettre le build et de démontrer la composition éditoriale (P20) dès le scaffold.

## TODO client (avant production)

Remplacer par des photos réelles — photographiées chaque semaine au rythme du menu (P20 est un pattern **vivant**, pas une galerie figée).

### Exigences photo produit (plats + hero)

- **Format** : AVIF ou WebP (fallback JPG).
- **Cadrage** : vertical 4:5, composition éditoriale (lumière naturelle, assiette centrée, fond tonal).
- **Dimensions source** : 1200×1500 ; `next/image` gère les tailles responsives.
- **Poids** : < 100 Ko chacune (exigence brief P20).
- **Alt-text** : descriptif précis du plat + son assiette, en FR + EN (conservé dans `messages/{fr,en}.json::home.menu.items.<key>.alt`).
- **Pas de PDF en remplacement** — anti-pattern P20.

### Exigences photo chef

- Portrait **humain authentique** (pas stock).
- Lumière naturelle chaude, cuisine réelle en arrière-plan.
- Dimensions 1200×1500, AVIF/WebP, < 350 Ko.

## Liste à produire

| Clé | Emplacement | Sujet |
|---|---|---|
| `hero-still-life` | `hero-still-life.{avif,webp}` | Nature morte terroir (pain au levain + beurre fermier) |
| `chef-portrait` | `chef-portrait.{avif,webp}` | Portrait Marguerite Lefebvre |
| `tartare-bison` | `menu/tartare-bison.{avif,webp}` | Tartare de bison, câpres, noisette |
| `beets-chevre` | `menu/beets-chevre.{avif,webp}` | Betteraves rôties, chèvre frais, sirop de sapin |
| `tomme-saison` | `menu/tomme-saison.{avif,webp}` | Tomme de Kamouraska, miel de sarrasin, pain noir |
| `omble-chevalier` | `menu/omble-chevalier.{avif,webp}` | Omble chevalier, salicorne, beurre blanc au cidre |
| `agneau-charlevoix` | `menu/agneau-charlevoix.{avif,webp}` | Agneau de Charlevoix, topinambour, thym |
| `tarte-poireaux` | `menu/tarte-poireaux.{avif,webp}` | Tarte fine aux poireaux, fumet de truite, oeuf de caille |
| `sabayon-sureau` | `menu/sabayon-sureau.{avif,webp}` | Sabayon au sureau, framboises, biscotti sarrasin |
| `tarte-argousier` | `menu/tarte-argousier.{avif,webp}` | Tarte à l'argousier, meringue brûlée |
| `chocolat-sarrasin` | `menu/chocolat-sarrasin.{avif,webp}` | Chocolat 80%, miel de sarrasin, crème glacée lait de foin |

## Cadence

Le menu change chaque jeudi : prévoir **session photo hebdomadaire** (~2 h). Les anciennes photos peuvent être archivées dans un dossier `archive/YYYY-WW/` pour conserver la mémoire des saisons.
