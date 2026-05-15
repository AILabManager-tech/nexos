#!/bin/bash
# Scan SSL/TLS via testssl.sh (préféré) ou fallback openssl.
#
# Pattern hardening (P4d) :
#   - set -uo pipefail
#   - Toujours JSON valide sur stdout, même en erreur (exit 0)
#   - stderr capturé et inclus dans JSON erreur
#   - Timeout explicite sur testssl.sh et openssl
#   - JSON émis via python3 (échappement subject/issuer avec virgules + accents)
set -uo pipefail

URL="${1:?Usage: ssl-scan.sh <URL>}"

SSL_TIMEOUT_S="${SSL_TIMEOUT_S:-60}"

# Extrait le domaine de l'URL (ignore scheme + path + port)
DOMAIN=$(echo "$URL" | python3 -c "
import sys
from urllib.parse import urlparse
url = sys.stdin.read().strip()
if '://' not in url:
    url = 'https://' + url
parsed = urlparse(url)
print(parsed.hostname or '')
")

_emit_error() {
    DOMAIN_ENV="$DOMAIN" ERROR_MSG="$1" STDERR="${2:-}" python3 -c "
import json, os
print(json.dumps({
    'grade': 'error',
    'error': os.environ['ERROR_MSG'],
    'domain': os.environ['DOMAIN_ENV'],
    'stderr': os.environ['STDERR'][:500],
}, ensure_ascii=False))
"
}

if [ -z "$DOMAIN" ]; then
    _emit_error "cannot extract domain from URL" "url=$URL"
    exit 0
fi

stderr_file=$(mktemp)
trap 'rm -f "$stderr_file"' EXIT

# Préférence testssl.sh (analyse exhaustive)
TESTSSL_CMD=""
if command -v testssl.sh &>/dev/null; then
    TESTSSL_CMD="testssl.sh"
elif command -v testssl &>/dev/null; then
    TESTSSL_CMD="testssl"
fi

if [ -n "$TESTSSL_CMD" ]; then
    output=$(timeout "$SSL_TIMEOUT_S" "$TESTSSL_CMD" --jsonfile stdout --quiet "$DOMAIN" 2>"$stderr_file")
    rc=$?
    stderr_capture=$(cat "$stderr_file")
    if [ "$rc" -eq 0 ] && [ -n "$output" ] && echo "$output" | python3 -c "import json,sys; json.loads(sys.stdin.read())" >/dev/null 2>&1; then
        echo "$output"
        exit 0
    fi
    if [ "$rc" -eq 124 ]; then
        _emit_error "testssl timeout after ${SSL_TIMEOUT_S}s" "$stderr_capture"
    else
        _emit_error "testssl failed (exit $rc)" "$stderr_capture"
    fi
    exit 0
fi

# Fallback openssl : extraction certificat basique
cert_raw=$(echo | timeout 15 openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN" 2>"$stderr_file")
rc=$?
stderr_capture=$(cat "$stderr_file")

if [ "$rc" -ne 0 ] || [ -z "$cert_raw" ]; then
    if [ "$rc" -eq 124 ]; then
        _emit_error "openssl timeout after 15s" "$stderr_capture"
    else
        _emit_error "unable to connect to $DOMAIN:443 (openssl exit $rc)" "$stderr_capture"
    fi
    exit 0
fi

DOMAIN_ENV="$DOMAIN" CERT_RAW="$cert_raw" python3 - <<'PYEOF'
import json
import os
import re
import subprocess

domain = os.environ["DOMAIN_ENV"]
cert_raw = os.environ["CERT_RAW"]


def openssl_x509(arg: str) -> str:
    try:
        proc = subprocess.run(
            ["openssl", "x509", "-noout", arg],
            input=cert_raw,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return proc.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


dates = openssl_x509("-dates")
issuer = re.sub(r"^issuer=", "", openssl_x509("-issuer"))
subject = re.sub(r"^subject=", "", openssl_x509("-subject"))

not_before = ""
not_after = ""
for line in dates.splitlines():
    if line.startswith("notBefore="):
        not_before = line.split("=", 1)[1]
    elif line.startswith("notAfter="):
        not_after = line.split("=", 1)[1]

protocol_match = re.search(r"Protocol\s*:\s*(\S+)", cert_raw)
protocol = protocol_match.group(1) if protocol_match else "unknown"

print(
    json.dumps(
        {
            "grade": "unknown",
            "note": "testssl.sh non disponible, fallback openssl",
            "domain": domain,
            "protocol": protocol,
            "issuer": issuer,
            "subject": subject,
            "not_before": not_before,
            "not_after": not_after,
        },
        ensure_ascii=False,
    )
)
PYEOF
exit 0
