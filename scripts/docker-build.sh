#!/usr/bin/env bash
# scripts/docker-build.sh — wrapper docker build qui déréférence les symlinks
# (soic → ../soic_v3) en piquant un tarball comme contexte.
#
# Usage:
#   ./scripts/docker-build.sh                    # tag par défaut: nexos:dev
#   ./scripts/docker-build.sh nexos:v4.2.0       # tag custom
#   TAG=nexos:dev ./scripts/docker-build.sh      # via env
#
# Phase J — chantier mise_a_niveau.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TAG="${1:-${TAG:-nexos:dev}}"

cd "$REPO_ROOT"

# Vérif rapide
if [[ ! -f Dockerfile ]]; then
  echo "Erreur: Dockerfile introuvable dans $REPO_ROOT" >&2
  exit 1
fi

echo "==> Build context (tar -czh, déréférence symlinks) → docker build -t $TAG"

# tar -h : suit les symlinks (essentiel pour soic → ../soic_v3)
# excludes : alignés avec .dockerignore (perf)
tar -czh \
  --exclude='./.git' \
  --exclude='./.venv' \
  --exclude='./venv' \
  --exclude='./node_modules' \
  --exclude='**/node_modules' \
  --exclude='./clients' \
  --exclude='./archive' \
  --exclude='./output' \
  --exclude='./__pycache__' \
  --exclude='**/__pycache__' \
  --exclude='*.egg-info' \
  --exclude='./.pytest_cache' \
  --exclude='./.mypy_cache' \
  --exclude='./.ruff_cache' \
  --exclude='./htmlcov' \
  --exclude='./.coverage' \
  -C "$REPO_ROOT" . \
  | docker build -t "$TAG" -

echo "==> Build OK: $TAG"
docker image inspect "$TAG" --format 'Taille: {{.Size}}' \
  | awk '{printf "Taille: %.1f MB\n", $2/1024/1024}'
