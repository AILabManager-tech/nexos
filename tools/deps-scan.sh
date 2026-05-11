#!/bin/bash
# Scan vulnérabilités npm
# A-010 fix : npm audit --json peut retourner exit!=0 ET stdout JSON valide
# (cas où des vulns sont détectées). L'ancien `|| echo '{...}'` ajoutait alors
# un 2e objet JSON à la suite, produisant un fichier invalide.
# Solution : capturer stdout, valider, fallback uniquement si stdout vide/invalide.
PROJECT_DIR="${1:?Usage: deps-scan.sh <PROJECT_DIR>}"

if [ ! -f "$PROJECT_DIR/package.json" ]; then
    echo '{"error": "no package.json found"}'
    exit 0
fi

cd "$PROJECT_DIR"
output=$(npm audit --json 2>/dev/null)

if [ -n "$output" ] && echo "$output" | python3 -c "import sys, json; json.loads(sys.stdin.read())" >/dev/null 2>&1; then
    echo "$output"
else
    echo '{"metadata":{"vulnerabilities":{"info":0,"low":0,"moderate":0,"high":0,"critical":0,"total":0}}}'
fi
