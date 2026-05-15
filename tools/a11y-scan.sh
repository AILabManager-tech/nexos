#!/bin/bash
# Scan accessibilité WCAG2AA via pa11y.
#
# Pattern hardening (P4d) :
#   - set -uo pipefail
#   - Toujours JSON valide sur stdout, même en erreur (exit 0)
#   - stderr capturé et inclus dans JSON erreur
#   - Timeout explicite (pa11y peut hang sur sites lourds)
#   - Distingue "pa11y absent" (warning) de "pa11y erreur" (vraie panne)
set -uo pipefail

URL="${1:?Usage: a11y-scan.sh <URL>}"

PA11Y_TIMEOUT_S="${PA11Y_TIMEOUT_S:-90}"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

_emit_empty() {
    URL_ENV="$URL" NOTE="$1" python3 -c "
import json, os
print(json.dumps({
    'issues': [],
    'note': os.environ['NOTE'],
    'url': os.environ['URL_ENV'],
}, ensure_ascii=False))
"
}

_emit_error() {
    URL_ENV="$URL" ERROR_MSG="$1" STDERR="${2:-}" python3 -c "
import json, os
print(json.dumps({
    'issues': [],
    'error': os.environ['ERROR_MSG'],
    'stderr': os.environ['STDERR'][:500],
    'url': os.environ['URL_ENV'],
}, ensure_ascii=False))
"
}

if ! command -v pa11y &>/dev/null; then
    _emit_empty "pa11y not installed (install: npm i -g pa11y)"
    exit 0
fi

stderr_file=$(mktemp)
trap 'rm -f "$stderr_file"' EXIT

output=$(timeout "$PA11Y_TIMEOUT_S" pa11y "$URL" \
    --reporter json \
    --standard WCAG2AA \
    --config "$SCRIPT_DIR/pa11y.config.json" \
    2>"$stderr_file")
rc=$?
stderr_capture=$(cat "$stderr_file")

# pa11y retourne 2 quand des issues sont trouvées — stdout reste valide.
# Considère le JSON valide tant que python3 sait le parser.
if [ -n "$output" ] && echo "$output" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1; then
    echo "$output"
    exit 0
fi

if [ "$rc" -eq 124 ]; then
    _emit_error "pa11y timeout after ${PA11Y_TIMEOUT_S}s" "$stderr_capture"
elif [ -n "$stderr_capture" ]; then
    _emit_error "pa11y failed (exit $rc)" "$stderr_capture"
else
    _emit_error "pa11y empty output (exit $rc)" ""
fi
exit 0
