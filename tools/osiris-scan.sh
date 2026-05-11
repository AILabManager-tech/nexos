#!/bin/bash
# Scan sobriété web via OSIRIS (Item 4 chantier 4 : timeout + retry + budget).
#
# Vars d'env configurables :
# - OSIRIS_PATH        : override explicite du path scanner
# - OSIRIS_TIMEOUT_S   : timeout par tentative (default 60s)
# - OSIRIS_MAX_RETRIES : nombre max de tentatives (default 3)
# - OSIRIS_BUDGET_S    : budget total cumulé (default 300s = 5 min)
#
# Toujours retourne un JSON valide sur stdout (exit 0). Encode les erreurs
# dans le JSON `{"error": "...", "metadata": {...}}` pour que les consommateurs
# ne crashent pas (Item 4 vs A-010 même principe : JSON valide même en erreur).
set -uo pipefail
URL="${1:?Usage: osiris-scan.sh <URL>}"

OSIRIS_TIMEOUT_S="${OSIRIS_TIMEOUT_S:-60}"
OSIRIS_MAX_RETRIES="${OSIRIS_MAX_RETRIES:-3}"
OSIRIS_BUDGET_S="${OSIRIS_BUDGET_S:-300}"

# Résolution du path OSIRIS, par ordre de priorité :
# 1. Variable d'env OSIRIS_PATH (override explicite)
# 2. Sibling dans le monorepo NEXOS_PLATFORM (../osiris depuis tools/)
# 3. Legacy $HOME/osiris-scanner
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SIBLING_OSIRIS="$SCRIPT_DIR/../../osiris"

if [ -z "${OSIRIS_PATH:-}" ]; then
    if [ -f "$SIBLING_OSIRIS/scanner.py" ]; then
        OSIRIS_PATH="$SIBLING_OSIRIS"
    else
        OSIRIS_PATH="$HOME/osiris-scanner"
    fi
fi

if [ ! -f "$OSIRIS_PATH/scanner.py" ]; then
    echo "{\"error\": \"osiris-scanner not found\", \"path\": \"$OSIRIS_PATH\"}"
    exit 0
fi

_validate_json() {
    echo "$1" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1
}

start=$(date +%s)
attempt=1
last_error="never attempted"

while [ "$attempt" -le "$OSIRIS_MAX_RETRIES" ]; do
    elapsed=$(($(date +%s) - start))
    if [ "$elapsed" -ge "$OSIRIS_BUDGET_S" ]; then
        echo "{\"error\": \"osiris budget exceeded\", \"elapsed_s\": $elapsed, \"budget_s\": $OSIRIS_BUDGET_S, \"attempts\": $((attempt - 1))}"
        exit 0
    fi

    # `timeout` retourne 124 sur kill, on capture aussi stderr pour diagnostic
    output=$(timeout "$OSIRIS_TIMEOUT_S" python3 "$OSIRIS_PATH/scanner.py" "$URL" --format json 2>&1)
    rc=$?

    if [ "$rc" -eq 0 ] && [ -n "$output" ] && _validate_json "$output"; then
        echo "$output"
        exit 0
    fi

    if [ "$rc" -eq 124 ]; then
        last_error="timeout after ${OSIRIS_TIMEOUT_S}s (attempt $attempt)"
    elif [ -n "$output" ]; then
        last_error="exit $rc: $(echo "$output" | head -c 200)"
    else
        last_error="exit $rc with empty output"
    fi

    # Backoff exponential : 5s, 15s, 45s — uniquement si il reste des tentatives
    if [ "$attempt" -lt "$OSIRIS_MAX_RETRIES" ]; then
        sleep_s=$((5 * (3 ** (attempt - 1))))
        # Cap le sleep pour ne pas exploser le budget
        remaining=$((OSIRIS_BUDGET_S - elapsed))
        if [ "$sleep_s" -gt "$remaining" ]; then
            sleep_s=$((remaining / 2))
        fi
        sleep "$sleep_s"
    fi

    attempt=$((attempt + 1))
done

echo "{\"error\": \"osiris scan failed after $OSIRIS_MAX_RETRIES attempts\", \"last_error\": \"$last_error\"}"
exit 0
