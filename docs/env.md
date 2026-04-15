# Variables d'environnement

Toutes les variables reconnues par NEXOS sont définies et consommées dans [`nexos/config.py`](../nexos/config.py). Ce fichier est la **source de vérité** pour la configuration.

Fichier d'exemple à la racine du monorepo : [`../../.env.example`](../../.env.example). Copier vers `.env` et adapter.

## Paths (tous optionnels — auto-détectés si la structure par défaut est respectée)

| Variable | Rôle | Défaut |
|---|---|---|
| `NEXOS_REPO_ROOT` | Racine du repo `nexos_v.3.0/` | Auto-détectée depuis `nexos/config.py` |
| `NEXOS_WORKSPACE_ROOT` | Racine du monorepo `NEXOS_PLATFORM/` | Parent de `NEXOS_REPO_ROOT` |
| `NEXOS_CLIENTS_DIR` | Dossier des projets clients | `$REPO/clients` |
| `NEXOS_SOIC_PATH` | Paquet SOIC (via symlink `soic → ../soic_v3`) | `$REPO/soic` |
| `NEXOS_TEMPLATES_DIR` | Templates sécurisés | `$REPO/templates` |
| `NEXOS_TOOLS_DIR` | Scripts outils (preflight, etc.) | `$REPO/tools` |
| `NEXOS_OUTPUT_DIR` | Outputs globaux (non par client) | `$REPO/output` |

## Sous-systèmes périphériques

| Variable | Rôle | Défaut |
|---|---|---|
| `AUDIT_TOOLKIT_PATH` | Chemin vers `audit_toolkit/` | `$WORKSPACE/audit_toolkit` |
| `OSIRIS_PATH` | Chemin vers `osiris/` | `$WORKSPACE/osiris` |

## Runtime

| Variable | Rôle | Défaut |
|---|---|---|
| `NEXOS_LOG_LEVEL` | Niveau de log (`DEBUG` / `INFO` / `WARNING` / `ERROR`) | `INFO` |

## API externes (optionnelles — laisser vide si non utilisées)

| Variable | Rôle |
|---|---|
| `MOZ_API_KEY` | Audit SEO (Domain Authority Moz) |
| `WHOIS_API_KEY` | Whois / domaine |
| `GSC_SERVICE_ACCOUNT_JSON` | Google Search Console (JSON service account) |

## Audit ponctuel

| Variable | Rôle |
|---|---|
| `TARGET_URL` | URL cible d'un audit rapide |
| `TARGET_SOURCE_PATH` | Chemin source d'un audit rapide (par défaut `$CLIENTS_DIR/<slug>/site`) |

## Gateway / SaaS

| Variable | Rôle | Défaut |
|---|---|---|
| `NEXOS_GATEWAY_PORT` | Port du gateway API (FastAPI) | `8000` |

## Notes

- **Précédence** : `.env` (chargé si `python-dotenv` est installé) → variables d'environnement shell → défauts du code.
- **`Settings` est immuable** : les variables sont lues **une seule fois** au démarrage (via `nexos/config.py::_build_settings()`). Changer une variable en runtime n'affecte pas un process déjà démarré.
- **Git-ignoré** : le fichier `.env` **ne doit jamais** être commité. `.env.example` est le seul fichier versionné.

## Voir aussi

- [`../CLAUDE.md`](../CLAUDE.md) — règles absolues
- [ADR 006 — Logging stdlib](./adr/006-logging-stdlib.md)
- [`docker.md`](./docker.md) — variables passées aux conteneurs
