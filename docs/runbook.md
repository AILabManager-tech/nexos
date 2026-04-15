# Runbook — NEXOS en production

Procédures opérationnelles pour la maintenance, les incidents et le déploiement.

## Check de santé quotidien

```bash
nexos doctor
```

**Attendu** : tous les outils critiques ✓, templates valides, SOIC accessible, ≥ 1 client listé.

Si un outil critique manque, voir **Incident — outils manquants** ci-dessous.

## Lancer un pipeline

```bash
# Création complète
nexos create --client-dir clients/<slug>

# Modification ciblée d'une section
nexos modify --client-dir clients/<slug> --section S-NNN

# Audit d'un site existant
nexos audit --client-dir clients/<slug> --url https://example.com
```

### Logs verbeux

```bash
NEXOS_LOG_LEVEL=DEBUG nexos create --client-dir clients/<slug> 2> /tmp/nexos.log
tail -f /tmp/nexos.log
```

Niveaux : `DEBUG | INFO | WARNING | ERROR`. Défaut : `INFO`.

---

## Incident — gate SOIC échoue en boucle

1. **Vérifier le symlink `soic/`**
   ```bash
   ls -la nexos_v.3.0/soic
   # Doit pointer vers ../soic_v3
   ```
   Si cassé → voir **Incident — `import soic` échoue**.
2. **Forcer un auto-fix manuel**
   ```bash
   nexos fix clients/<slug>
   nexos fix clients/<slug> --dry-run   # aperçu sans appliquer
   ```
3. **Identifier la dimension défaillante**
   ```bash
   cat clients/<slug>/soic-gates.json | jq '.'
   ```
   Chercher la dimension D1–D8 dont le score est le plus bas.
4. **Cas D8 — Loi 25** : vérifier que `components/CookieConsent.tsx`, `app/politique-confidentialite/page.tsx` et `app/mentions-legales/page.tsx` existent et ne contiennent **pas** de placeholders `[À COMPLÉTER]`.
5. **Cas D4 — Sécurité** :
   ```bash
   cd clients/<slug>/site/
   npm audit --omit=dev
   cat vercel.json | jq '.headers'
   ```
   Les headers `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`, `HSTS` doivent être présents.

## Incident — `nexos doctor` remonte des outils manquants

| Outil manquant | Correction |
|---|---|
| `codex` | Installer Codex CLI (doc provider) |
| `lighthouse` | `npm install -g lighthouse` |
| `pa11y` | `npm install -g pa11y` |
| Python < 3.10 | Mettre à jour Python **ou** utiliser un venv 3.10+ |
| `uv` | `pip install uv` ou `curl -LsSf https://astral.sh/uv/install.sh | sh` |

## Incident — `import soic` échoue

Voir la **phase A** du chantier `mise_a_niveau` :

```bash
cd nexos_v.3.0/
ls -la soic
# Si broken/absent :
ln -sfn ../soic_v3 soic
python3 -c "import soic; print(soic.__file__)"
```

## Incident — pipeline s'interrompt sans trace claire

```bash
# 1. Relire le changelog du client
cat clients/<slug>/nexos-changelog.json | jq '.events[-20:]'

# 2. Chercher la dernière phase qui a démarré sans se terminer
cat clients/<slug>/nexos-changelog.json \
  | jq '.events[] | select(.type | test("PHASE_"))'

# 3. Relancer cette phase uniquement via le mode approprié
```

---

## Déploiement d'un client (production)

> ⚠️ **Ne pas automatiser ici — décision humaine à chaque fois.**

```bash
# 1. Pré-flight
nexos audit --url https://staging.<client>.com --client-dir clients/<slug>

# 2. Vérifier le gate ph5→deploy
jq '.gates["ph5_to_deploy"].mu' clients/<slug>/soic-gates.json
# → doit être ≥ 8.5
```

Si μ ≥ 8.5 :

```bash
# 3. Déployer manuellement
cd clients/<slug>/site/
vercel --prod --yes    # NE PAS mettre dans un CI qui se déclenche sur main
```

## Rollback d'un commit NEXOS

```bash
git log --oneline -10
git revert <sha>
git push origin feature/revert-<sha>
# Ouvrir PR → review → merge
```

> ⛔ **Jamais** de `git reset --hard` ou de `git push --force` sur `main`.

## Rollback d'un déploiement Vercel

```bash
# Lister les déploiements d'un projet client
vercel ls <project-name>

# Promouvoir un déploiement précédent en prod
vercel promote <deployment-url> --scope=<team>
```

---

## Contacts / traçabilité

- **RPP Loi 25** d'un client : `clients/<slug>/brief-client.json` → `loi25.rpp.{nom,titre,courriel}`.
- **Incident de confidentialité** : délai légal **72 h** pour notifier (Loi 25, art. 3.5). Courriel de notification configuré dans le brief.
- **Audit trail pipeline** : `clients/<slug>/nexos-changelog.json` (append-only, 19 `EventType`).

## Voir aussi

- [`adding-agents.md`](./adding-agents.md) — contribuer un agent
- [`docker.md`](./docker.md) — build + compose
- [`env.md`](./env.md) — variables d'environnement
- [`deployment.md`](./deployment.md) — déploiement prod (détails)
- [`troubleshooting.md`](./troubleshooting.md) — dépannage général
- [`adr/`](./adr/) — décisions d'architecture
