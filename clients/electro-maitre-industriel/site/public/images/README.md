# Images — Électro-Maître Industriel

Les SVG placeholders de `projects/*.svg` sont **volontairement schématiques** — leur rôle est de démontrer l'effet grayscale→couleur (P06) dès le scaffold.

## TODO client (avant production)

Remplacer par des photos réelles de chantiers. Exigences :

- **Format** : AVIF ou WebP (fallback JPG).
- **Dimensions** : 1600×1200 source ; `next/image` gère les tailles responsives.
- **Poids** : < 250 Ko chacune.
- **Contenu** : photos industrielles **originales** (pas de stock footage — voir brief `free_text` et règles NEXOS §Sécurité).
- **Alt-text** : descriptif précis du lieu et du chantier, en FR + EN, conservé dans `messages/{fr,en}.json::home.projects.items.<key>.alt`.
- **Cohérence P06** : toute photo doit rester lisible en niveaux de gris (composition + contraste suffisants pour ne pas tuer le message sans couleur).

## Liste à produire

| Clé (i18n) | Sujet |
|---|---|
| `manufacturing` | Tableau 600 V rénové, usine d'embouteillage (Anjou) |
| `food-plant` | Chaîne de convoyeurs automatisée (Laval) |
| `datacenter` | Salle de distribution redondante Tier III (Ville-Saint-Laurent) |
| `warehouse` | Entrepôt logistique avec éclairage LED (Pointe-aux-Trembles) |
| `switchgear` | Remplacement de barre omnibus 12 kV (Est de Montréal) |
| `automation` | Armoire Siemens S7-1500 avec IHM tactiles (Longueuil) |
