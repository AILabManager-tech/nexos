# Docker — NEXOS

## Build

```bash
cd nexos_v.3.0/
docker build -t nexos:dev .
```

Taille typique : ~650-750 MB (Python 3.11 slim + Node 20 + lighthouse/pa11y).

## Runs typiques

### Diagnostic système
```bash
docker run --rm nexos:dev nexos doctor
```

### Audit d'un site avec volume monté
```bash
docker run --rm -v $PWD/clients:/app/clients \
  nexos:dev nexos audit https://example.com --client-dir /app/clients/test
```

### Gateway API (expose port 8000)
```bash
docker run --rm -p 8000:8000 \
  -v $PWD/clients:/app/clients \
  nexos:dev uvicorn nexos_gateway:app --host 0.0.0.0
```

### Mode dev (bind le code + deps dev)
Voir section **Docker Compose** ci-dessous.

## Docker Compose

### Services

- **`nexos`** : CLI one-shot (interactive ou commande unique)
- **`gateway`** : API FastAPI sur port 8000
- **`soic-eval`** : sanity check du module SOIC (profile `soic`)

### Profiles

- `default` : nexos + gateway
- `cli` : nexos uniquement
- `api` : gateway uniquement
- `dev` : bind-mount du code + hot reload
- `soic` : inclut soic-eval

### Commandes usuelles

```bash
# Démarrer gateway en prod
docker compose -f docker-compose.yml up gateway -d

# Dev avec hot reload (override auto)
docker compose --profile dev up

# CLI one-shot
docker compose run --rm nexos nexos doctor

# Tout arrêter
docker compose down
```

### Variables d'environnement

- `NEXOS_VERSION` : tag de l'image (dev, v4.2.0, latest)
- `NEXOS_LOG_LEVEL` : INFO / DEBUG / WARNING / ERROR
- `NEXOS_GATEWAY_PORT` : port hôte pour le gateway (8000 par défaut)

### Volumes

- `./clients` → `/app/clients` : dossier clients (briefs + sites)
- `./output` → `/app/output` : outputs du pipeline

### Healthcheck

Le service `gateway` expose `GET /health` (ajouté en phase K dans `nexos_gateway.py`).
Le compose l'utilise pour un healthcheck toutes les 30 s.

## Variables d'environnement

| Var | Description | Défaut |
|-----|-------------|--------|
| `NEXOS_LOG_LEVEL` | INFO / DEBUG / WARNING / ERROR | INFO |
| `NEXOS_CLIENTS_DIR` | Path interne des clients | /app/clients |
| `NEXOS_OUTPUT_DIR` | Path interne des outputs | /app/output |
| `MOZ_API_KEY` | Clé Moz (optionnel) | — |

## User non-root

L'image tourne en tant qu'utilisateur `nexos` (uid 1000) pour la sécurité.
Les volumes montés doivent être lisibles/écrivables par cet UID.

## Multi-stage

- **Stage 1 (builder)** : Python + Node + build-essential + deps dev → image gonflée mais installable.
- **Stage 2 (runtime)** : copie le venv + node_modules depuis le builder, pas de build-essential → image finale plus légère.

## Limites connues

- Lighthouse/pa11y utilisent Chromium en headless — les runs dans Docker peuvent nécessiter `--cap-add=SYS_ADMIN` ou `--security-opt seccomp=unconfined` selon l'hôte.
- Les clients/ ne sont pas dans l'image : volume obligatoire pour les pipelines create/modify.
