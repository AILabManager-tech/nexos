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

## Allocation des ports — sous-blocs nommés

NEXOS respecte la convention machine documentée dans `~/.claude/CLAUDE.md` user
(section *Allocation des ports*). Aucun port automatique : tout passe par
`nexos.port_allocator` ou son wrapper bash `tools/alloc-port.sh`.

### Zones interdites (jamais utiliser)

- **0-1023** : ports privilégiés OS (root requis)
- **32768-60999** : zone éphémère kernel (cf `/proc/sys/net/ipv4/ip_local_port_range`)

L'allocator refuse explicitement tout sous-bloc qui chevauche ces zones
(`ForbiddenZoneError`) — validation au load du module.

### Sous-blocs disponibles

```bash
bash tools/alloc-port.sh --list
```

Sortie attendue :

```
NEXOS_TESTS      20000-20099   tests éphémères (sites Next preview)
NEXOS_ENGINE     20100-20199   pipeline engine (preflight Next.js ← P3)
NEXOS_SCRAPING   20200-20299   scraping & automation
NEXOS_CYBERSEC   20300-20399   cybersec interne pipeline
NEXOS_BUFFER     20900-20999   ad-hoc NEXOS
GENESIS_*        21000-21199   réservé Genesis
GENCORE          22000-22999   RAG, qwen-gencore
SAAS             23000-23999   NEXOS_PLATFORM/saas/
CYBERSEC_LABS    24000-24999   juice-shop, DVWA, hexstrike
AUDIT_TOOLKIT    25000-25999   osiris standalone
GLOBAL_BUFFER    29000-29999   one-shot tous projets
```

### Usage Python (orchestrator)

```python
from nexos.port_allocator import allocate_port, NEXOS_ENGINE, SubblockSaturatedError

try:
    port = allocate_port(NEXOS_ENGINE)   # premier libre dans 20100-20199
except SubblockSaturatedError:
    # Aucun port libre. Pas de purge automatique.
    # → caller décide : skip preflight OU purge explicite + retry.
    ...
```

### Usage CLI

```bash
# Allocation simple — JSON parsable sur stdout
bash tools/alloc-port.sh NEXOS_ENGINE
# {"port": 20100, "subblock": "NEXOS_ENGINE"}

# Sous-bloc saturé → exit 3 + JSON erreur sur stderr
bash tools/alloc-port.sh NEXOS_ENGINE
# {"error": "saturated", "subblock": "NEXOS_ENGINE", ...}
```

### Incident — sous-bloc saturé

L'allocator NE purge JAMAIS automatiquement. Si `NEXOS_ENGINE` (ou tout autre
sous-bloc) est saturé, le pipeline preflight skip proprement et un message
explicite s'affiche :

```
✗ NEXOS_ENGINE saturé — ...
  Hint: bash tools/alloc-port.sh NEXOS_ENGINE --purge
```

Purge explicite (kill -TERM sur tous les listeners du sous-bloc) :

```bash
bash tools/alloc-port.sh NEXOS_ENGINE --purge
# {"port": 20100, "subblock": "NEXOS_ENGINE", "purged_pids": [4242, 4243]}
```

`--purge` envoie `SIGTERM` (pas `SIGKILL`) — laisse aux serveurs Next.js le
temps de cleanup proprement. Si un PID résiste, escalader manuellement avec
`kill -9 <pid>` après inspection (`ss -ltnp | grep :2010`).

### Diagnostic — qui écoute dans le sous-bloc ?

```bash
ss -Hltnp | awk '$4 ~ /:201[0-9]{2}$/'   # NEXOS_ENGINE 20100-20199
```

### Régression P3

- **Bug initial** (2026-05-15) : `_find_free_port()` dans `orchestrator/preflight.py`
  faisait `socket.bind(("", 0))` ce qui pioche dans la zone éphémère kernel
  (32768-60999, ex: port 55191 observé).
- **Fix** : `_find_free_port()` délègue à `allocate_port(NEXOS_ENGINE)`.
- **Test régression** : `tests/test_port_allocator.py::test_preflight_find_free_port_uses_nexos_engine`
  ancre que le port retourné est toujours dans 20100-20199.

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
