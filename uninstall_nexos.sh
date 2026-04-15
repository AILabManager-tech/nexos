#!/usr/bin/env bash
# NEXOS — Désinstallation (phase L du chantier mise_a_niveau v4.2.0)
#
# Usage: bash uninstall_nexos.sh
#
# Ne supprime PAS le venv ni les fichiers utilisateur (briefs, clients).
# Retire uniquement le symlink CLI et les hooks pre-commit.

set -euo pipefail

NEXOS_ROOT="$(cd "$(dirname "$0")" && pwd)"
LINK_PATH="$HOME/.local/bin/nexos"

if [[ -e "$LINK_PATH" || -L "$LINK_PATH" ]]; then
  rm -f "$LINK_PATH"
  echo "✓ Symlink $LINK_PATH supprimé"
fi

# Hooks pre-commit (si installé)
if [[ -f "$NEXOS_ROOT/.git/hooks/pre-commit" ]]; then
  (cd "$NEXOS_ROOT" && pre-commit uninstall) || true
fi

cat <<EOF
✅ NEXOS CLI désinstallé.

Le venv $NEXOS_ROOT/.venv et les données (clients/, output/) sont PRÉSERVÉS.
Pour supprimer complètement: rm -rf $NEXOS_ROOT/.venv
EOF
