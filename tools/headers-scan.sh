#!/bin/bash
# Fetch HTTP headers via curl et output JSON.
#
# Pattern hardening (P4d) :
#   - set -uo pipefail
#   - Toujours JSON valide sur stdout, même en erreur (exit 0)
#   - stderr capturé et inclus dans JSON erreur
#   - JSON émis via python3 (échappement guillemets, accents, sauts de ligne)
#   - Dédup headers : pour chaque clé, garde la DERNIÈRE valeur (sémantique
#     HTTP après redirects)
set -uo pipefail

URL="${1:?Usage: headers-scan.sh <URL>}"

HEADERS_TIMEOUT_S="${HEADERS_TIMEOUT_S:-30}"

_emit_error() {
    URL_ENV="$URL" ERROR_MSG="$1" STDERR="${2:-}" python3 -c "
import json, os
print(json.dumps({
    'error': os.environ['ERROR_MSG'],
    'url': os.environ['URL_ENV'],
    'stderr': os.environ['STDERR'][:500],
}, ensure_ascii=False))
"
}

stderr_file=$(mktemp)
trap 'rm -f "$stderr_file"' EXIT

raw_headers=$(curl -sI -L --max-time "$HEADERS_TIMEOUT_S" --max-redirs 5 "$URL" 2>"$stderr_file" | tr -d '\r')
rc=$?
stderr_capture=$(cat "$stderr_file")

if [ "$rc" -ne 0 ] || [ -z "$raw_headers" ]; then
    if [ "$rc" -eq 28 ]; then
        _emit_error "curl timeout after ${HEADERS_TIMEOUT_S}s" "$stderr_capture"
    else
        _emit_error "unable to fetch headers (curl exit $rc)" "$stderr_capture"
    fi
    exit 0
fi

# Émission JSON via python3 — gère échappement, dédup, et garantit validité.
URL_ENV="$URL" RAW_HEADERS="$raw_headers" python3 -c "
import json, os, sys

raw = os.environ['RAW_HEADERS']
url = os.environ['URL_ENV']

last_value: dict[str, str] = {}
order: list[str] = []
for line in raw.splitlines():
    line = line.strip()
    if not line or line.startswith('HTTP/'):
        continue
    if ':' not in line:
        continue
    key, _, value = line.partition(':')
    key_lower = key.strip().lower()
    if not key_lower:
        continue
    if key_lower not in last_value:
        order.append(key_lower)
    last_value[key_lower] = value.strip()

result: dict = {'url': url}
for key in order:
    result[key] = last_value[key]
print(json.dumps(result, ensure_ascii=False))
"
exit 0
