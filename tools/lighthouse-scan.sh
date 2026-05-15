#!/bin/bash
# Scan Lighthouse complet — output JSON vers stdout.
#
# Pattern hardening (P4d) :
#   - set -uo pipefail
#   - Toujours JSON valide sur stdout, même en erreur (exit 0)
#   - stderr capturé et inclus dans JSON erreur
#   - Timeout via `timeout` cmd (lighthouse a son maxWaitForLoad mais peut hang
#     côté Chrome headless)
set -uo pipefail

URL="${1:?Usage: lighthouse-scan.sh <URL>}"

LH_TIMEOUT_S="${LH_TIMEOUT_S:-120}"

_emit_error() {
    URL_ENV="$URL" ERROR_MSG="$1" STDERR="${2:-}" python3 -c "
import json, os
print(json.dumps({
    'error': os.environ['ERROR_MSG'],
    'url': os.environ['URL_ENV'],
    'stderr': os.environ['STDERR'][:500],
    'categories': {},
}, ensure_ascii=False))
"
}

if ! command -v lighthouse &>/dev/null; then
    _emit_error "lighthouse not installed" "install via: npm i -g lighthouse"
    exit 0
fi

stderr_file=$(mktemp)
trap 'rm -f "$stderr_file"' EXIT

output=$(timeout "$LH_TIMEOUT_S" lighthouse "$URL" \
    --output json \
    --output-path stdout \
    --chrome-flags="--headless --no-sandbox --disable-gpu" \
    --max-wait-for-load=45000 \
    --quiet 2>"$stderr_file")
rc=$?
stderr_capture=$(cat "$stderr_file")

if [ "$rc" -eq 0 ] && [ -n "$output" ] && echo "$output" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1; then
    echo "$output"
    exit 0
fi

if [ "$rc" -eq 124 ]; then
    _emit_error "lighthouse timeout after ${LH_TIMEOUT_S}s" "$stderr_capture"
elif [ -n "$stderr_capture" ]; then
    _emit_error "lighthouse failed (exit $rc)" "$stderr_capture"
else
    _emit_error "lighthouse empty output (exit $rc)" ""
fi
exit 0
