# Migration vers business — 2026-05-17

Ce dossier est désormais l'**atelier de fabrication** du client Dépanneur Nobert.
Le code source du site (`site/`) a été déplacé vers le dossier business officiel :

    /home/gear-code/01_business/clients/03_Depanneur_Nobert/04_livrables/site-web/

Ce qui reste ici (artefacts pipeline NEXOS, immuables) :
- `brief-client.json` (source pour re-fabrication potentielle)
- `ph0..ph5-*.md` (rapports phases)
- `soic-gates.json`, `soic-runs.jsonl` (verdicts SOIC)
- `nexos-changelog.json` (audit trail événementiel)
- `tooling/` (lighthouse, pa11y, npm-audit, ssl, osiris)
- `section-manifest.json`, `pattern-recommendation.json`, etc.

**Conséquence pour `nexos doctor`** : le rapport indiquera `site=MISSING` pour ce
client. C'est normal et attendu — le client est sorti du cycle de fabrication
NEXOS et vit maintenant son cycle business.

Pour re-fabriquer (si besoin) :
    cp /home/gear-code/01_business/clients/03_Depanneur_Nobert/04_livrables/site-web .
    # ou re-run nexos create avec le brief
