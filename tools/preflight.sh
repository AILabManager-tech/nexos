#!/bin/bash
# NEXOS v3.0 — Preflight Tooling
# Usage: ./preflight.sh <URL> <CLIENT_DIR>
#
# Exécute les outils de mesure CLI AVANT les agents LLM.
# Résultats stockés dans <CLIENT_DIR>/tooling/

set -euo pipefail

URL="${1:?Usage: preflight.sh <URL> <CLIENT_DIR>}"
CLIENT_DIR="${2:?Usage: preflight.sh <URL> <CLIENT_DIR>}"
TOOLING_DIR="$CLIENT_DIR/tooling"
TOOLS_DIR="$(dirname "$0")"

mkdir -p "$TOOLING_DIR"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  NEXOS v3.0 — PREFLIGHT TOOLING"
echo "  URL: $URL"
echo "  Output: $TOOLING_DIR/"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. Lighthouse ──
echo -n "[1/6] Lighthouse... "
if command -v lighthouse &>/dev/null; then
    lighthouse "$URL" \
        --output json \
        --output-path "$TOOLING_DIR/lighthouse.json" \
        --chrome-flags="--headless --no-sandbox --disable-gpu" \
        --quiet 2>/dev/null && echo "✓" || echo "⚠ partial"
else
    echo "⚠ non installé (npm i -g lighthouse)"
fi

# ── 2. Headers HTTP ──
echo -n "[2/6] Headers HTTP... "
bash "$TOOLS_DIR/headers-scan.sh" "$URL" > "$TOOLING_DIR/headers.json" 2>/dev/null \
    && echo "✓" || echo "⚠ erreur"

# ── 3. npm audit ──
echo -n "[3/6] npm audit... "
SITE_DIR="$CLIENT_DIR/site"
if [ -f "$SITE_DIR/package.json" ]; then
    cd "$SITE_DIR"
    npm audit --json > "$TOOLING_DIR/npm-audit.json" 2>/dev/null || true
    echo "✓"
    cd - >/dev/null
else
    echo "⚠ pas de package.json"
    echo '{"metadata":{"vulnerabilities":{"high":0,"critical":0}}}' > "$TOOLING_DIR/npm-audit.json"
fi

# ── 4. pa11y (accessibilité) ──
# AVANT (bug attrapé audit dette 2026-05-15) :
# - écrivait dans pa11y.json alors que les agents Ph5 lisent a11y.json
#   → mismatch silencieux, Ph5 lisait l'ancien a11y.json sans le savoir
# - n'utilisait pas pa11y.config.json (--no-sandbox), donc Chrome crashait
#   sur certaines machines et le JSON était vide (avec stderr supprimé)
# Fix : passer par a11y-scan.sh qui a la bonne config + standard WCAG2AA.
echo -n "[4/6] pa11y... "
if command -v pa11y &>/dev/null; then
    bash "$TOOLS_DIR/a11y-scan.sh" "$URL" > "$TOOLING_DIR/a11y.json" 2>/dev/null \
        && echo "✓" || echo "⚠ partial"
else
    echo "⚠ non installé (npm i -g pa11y)"
    echo '[]' > "$TOOLING_DIR/a11y.json"
fi

# ── 5. testssl.sh ──
echo -n "[5/6] testssl.sh... "
if command -v testssl.sh &>/dev/null || command -v testssl &>/dev/null; then
    bash "$TOOLS_DIR/ssl-scan.sh" "$URL" > "$TOOLING_DIR/ssl.json" 2>/dev/null \
        && echo "✓" || echo "⚠ partial"
else
    echo "⚠ non installé (apt install testssl.sh)"
fi

# ── 6. OSIRIS ──
echo -n "[6/6] OSIRIS scanner... "
OSIRIS_PATH="$HOME/osiris-scanner"
if [ -d "$OSIRIS_PATH" ]; then
    python3 "$OSIRIS_PATH/scanner.py" "$URL" --format json > "$TOOLING_DIR/osiris.json" 2>/dev/null \
        && echo "✓" || echo "⚠ partial"
else
    echo "⚠ osiris-scanner non trouvé"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  TOOLING TERMINÉ"
echo "  Fichiers: $(ls -1 "$TOOLING_DIR" | wc -l) JSON générés"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
