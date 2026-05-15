#!/bin/bash
# Scan vulnérabilités npm (npm audit --json).
#
# Pattern hardening (P4d) — aligné sur osiris-scan.sh :
#   - set -uo pipefail
#   - Toujours JSON valide sur stdout, même en erreur (exit 0)
#   - stderr capturé et inclus dans JSON erreur (diagnostic)
#   - Timeout explicite via `timeout` (npm audit peut hang sur network)
#   - Erreurs encodées via python3 pour échappement correct
#
# A-010 fix conservé : npm audit --json peut retourner exit!=0 ET stdout JSON
# valide (cas vulns détectées). Capture stdout, valide, fallback si invalide.
set -uo pipefail

PROJECT_DIR="${1:?Usage: deps-scan.sh <PROJECT_DIR>}"

DEPS_TIMEOUT_S="${DEPS_TIMEOUT_S:-60}"

_emit_error() {
    local error_msg="$1"
    local stderr_capture="${2:-}"
    ERROR_MSG="$error_msg" STDERR="$stderr_capture" python3 -c "
import json, os
print(json.dumps({
    'error': os.environ['ERROR_MSG'],
    'stderr': os.environ['STDERR'][:500],
    'metadata': {'vulnerabilities': {'info': 0, 'low': 0, 'moderate': 0,
                                      'high': 0, 'critical': 0, 'total': 0}},
}, ensure_ascii=False))
"
}

if [ ! -f "$PROJECT_DIR/package.json" ]; then
    _emit_error "no package.json found" "looked in: $PROJECT_DIR"
    exit 0
fi

cd "$PROJECT_DIR" || { _emit_error "cannot cd to $PROJECT_DIR"; exit 0; }

stderr_file=$(mktemp)
trap 'rm -f "$stderr_file"' EXIT

output=$(timeout "$DEPS_TIMEOUT_S" npm audit --json 2>"$stderr_file")
rc=$?
stderr_capture=$(cat "$stderr_file")

# npm audit retourne exit!=0 quand des vulns sont détectées — stdout reste valide.
# On considère le JSON valide même si rc!=0, tant que python3 sait le parser.
if [ -n "$output" ] && echo "$output" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1; then
    echo "$output"
    exit 0
fi

if [ "$rc" -eq 124 ]; then
    _emit_error "npm audit timeout after ${DEPS_TIMEOUT_S}s" "$stderr_capture"
elif [ -n "$stderr_capture" ]; then
    _emit_error "npm audit failed (exit $rc)" "$stderr_capture"
else
    _emit_error "npm audit empty output (exit $rc)" ""
fi
exit 0
