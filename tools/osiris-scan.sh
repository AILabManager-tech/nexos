#!/bin/bash
# Scan sobriété web via OSIRIS
URL="${1:?Usage: osiris-scan.sh <URL>}"

# Résolution du path OSIRIS, par ordre de priorité :
# 1. Variable d'env OSIRIS_PATH (override explicite)
# 2. Sibling dans le monorepo NEXOS_PLATFORM (../osiris depuis tools/)
# 3. Legacy $HOME/osiris-scanner
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIBLING_OSIRIS="$SCRIPT_DIR/../../osiris"

if [ -z "$OSIRIS_PATH" ]; then
    if [ -f "$SIBLING_OSIRIS/scanner.py" ]; then
        OSIRIS_PATH="$SIBLING_OSIRIS"
    else
        OSIRIS_PATH="$HOME/osiris-scanner"
    fi
fi

if [ -f "$OSIRIS_PATH/scanner.py" ]; then
    python3 "$OSIRIS_PATH/scanner.py" "$URL" --format json 2>/dev/null
else
    echo '{"error": "osiris-scanner not found", "path": "'"$OSIRIS_PATH"'"}'
fi
