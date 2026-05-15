#!/bin/bash
# Scan sobriété/sécurité web via OSIRIS — P7 fix API désynchronisée.
#
# CHANGEMENTS API (2026-05-15) :
# - Ancienne CLI : `scanner.py <URL> --format json` (positional URL + flag --format)
# - Nouvelle CLI : `scanner.py --url <URL> --output report --mode fast`
#   Le scanner écrit `reports/<domain>_<date>.json` (relatif au CWD du process)
#   au lieu d'émettre sur stdout. On capture ce fichier puis on émet sur stdout.
#
# Pattern hardening conservé (P4d) :
# - set -uo pipefail
# - Toujours exit 0 + JSON valide même en erreur
# - stderr capturé pour diagnostic
# - Timeout + retry + budget
# - Erreurs encodées via python3 pour échappement correct
#
# Vars d'env configurables :
# - OSIRIS_PATH        : override explicite du path scanner
# - OSIRIS_TIMEOUT_S   : timeout par tentative (default 60s)
# - OSIRIS_MAX_RETRIES : nombre max de tentatives (default 3)
# - OSIRIS_BUDGET_S    : budget total cumulé (default 300s = 5 min)
# - OSIRIS_MODE        : fast (default, HTML only) ou deep (Playwright)
set -uo pipefail
URL="${1:?Usage: osiris-scan.sh <URL>}"

OSIRIS_TIMEOUT_S="${OSIRIS_TIMEOUT_S:-60}"
OSIRIS_MAX_RETRIES="${OSIRIS_MAX_RETRIES:-3}"
OSIRIS_BUDGET_S="${OSIRIS_BUDGET_S:-300}"
OSIRIS_MODE="${OSIRIS_MODE:-fast}"

# Résolution du path OSIRIS, par ordre de priorité :
# 1. Variable d'env OSIRIS_PATH (override explicite)
# 2. Sibling dans le monorepo NEXOS_PLATFORM (../osiris depuis nexos_v.3.0/tools/)
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

# Extrait le domaine depuis l'URL (le scanner nomme reports/<domain>_<date>.json)
DOMAIN=$(echo "$URL" | python3 -c "
import sys
from urllib.parse import urlparse
url = sys.stdin.read().strip()
if '://' not in url:
    url = 'https://' + url
parsed = urlparse(url)
print(parsed.hostname or '')
")

if [ -z "$DOMAIN" ]; then
    echo "{\"error\": \"cannot extract domain from URL\", \"url\": \"$URL\"}"
    exit 0
fi

# Dossier de travail temporaire — le scanner écrit `reports/` relatif à son CWD
WORK_DIR=$(mktemp -d)
trap 'rm -rf "$WORK_DIR"' EXIT

start=$(date +%s)
attempt=1
last_error="never attempted"

while [ "$attempt" -le "$OSIRIS_MAX_RETRIES" ]; do
    elapsed=$(($(date +%s) - start))
    if [ "$elapsed" -ge "$OSIRIS_BUDGET_S" ]; then
        echo "{\"error\": \"osiris budget exceeded\", \"elapsed_s\": $elapsed, \"budget_s\": $OSIRIS_BUDGET_S, \"attempts\": $((attempt - 1))}"
        exit 0
    fi

    # Nettoie reports/ avant chaque tentative pour repartir propre
    rm -rf "$WORK_DIR/reports"

    # Run scanner depuis le WORK_DIR pour que reports/ soit écrit là
    # stderr/stdout du scanner = bruit Rich/logs, capturé en tampon pour diagnostic
    stderr_file=$(mktemp)
    (cd "$WORK_DIR" && timeout "$OSIRIS_TIMEOUT_S" python3 "$OSIRIS_PATH/scanner.py" \
        --url "$URL" \
        --output report \
        --mode "$OSIRIS_MODE" \
        >"$stderr_file" 2>&1)
    rc=$?
    output=$(cat "$stderr_file")
    rm -f "$stderr_file"

    # Cherche le rapport JSON généré (pattern: reports/<domain>_<YYYY-MM-DD>.json)
    report_json=$(find "$WORK_DIR/reports" -maxdepth 1 -name "${DOMAIN}_*.json" 2>/dev/null | head -1)

    if [ "$rc" -eq 0 ] && [ -n "$report_json" ] && [ -f "$report_json" ]; then
        # Valide le JSON puis l'émet sur stdout
        if _validate_json "$(cat "$report_json")"; then
            cat "$report_json"
            exit 0
        else
            last_error="report JSON invalide (attempt $attempt): $report_json"
        fi
    elif [ "$rc" -eq 124 ]; then
        last_error="timeout after ${OSIRIS_TIMEOUT_S}s (attempt $attempt)"
    elif [ -n "$output" ]; then
        last_error="exit $rc: $(echo "$output" | head -c 200)"
    else
        last_error="exit $rc with empty output (no report file generated)"
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

# JSON émis via python3 pour garantir l'échappement correct des caractères de
# contrôle (newlines, guillemets) présents dans $last_error (traceback Python
# multi-ligne capturé par head -c 200).
OSIRIS_MAX_RETRIES="$OSIRIS_MAX_RETRIES" LAST_ERROR="$last_error" python3 -c "
import json, os
print(json.dumps({
    'error': f\"osiris scan failed after {os.environ['OSIRIS_MAX_RETRIES']} attempts\",
    'last_error': os.environ['LAST_ERROR'],
}, ensure_ascii=False))
"
exit 0
