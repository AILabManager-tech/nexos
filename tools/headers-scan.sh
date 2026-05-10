#!/bin/bash
# Fetch HTTP headers et output en JSON
# Dedoublonne les cles : pour chaque cle, garde la DERNIERE valeur observee
# (semantique HTTP : la reponse finale apres redirects prime sur les hops intermediaires)
URL="${1:?Usage: headers-scan.sh <URL>}"

# Recupere les headers avec timeout et suivi des redirections
HEADERS=$(curl -sI -L --max-time 30 --max-redirs 5 "$URL" 2>/dev/null | tr -d '\r')

if [ -z "$HEADERS" ]; then
    echo '{"error": "unable to fetch headers", "url": "'"$URL"'"}'
    exit 1
fi

# Dedup : pour chaque cle, ne conserver que la derniere valeur observee.
# On preserve l'ordre d'apparition de la premiere occurrence (KEY_ORDER) afin
# que l'output JSON reste stable et lisible.
declare -A LAST_VALUE
declare -a KEY_ORDER
while IFS=': ' read -r key value; do
    [ -z "$key" ] && continue
    # Skip les lignes de statut HTTP
    echo "$key" | grep -q "^HTTP" && continue
    key_lower=$(echo "$key" | tr '[:upper:]' '[:lower:]')
    if [ -z "${LAST_VALUE[$key_lower]+x}" ]; then
        KEY_ORDER+=("$key_lower")
    fi
    # Escape les guillemets dans la valeur
    LAST_VALUE[$key_lower]=$(echo "$value" | sed 's/"/\\"/g')
done <<< "$HEADERS"

# Emet le JSON dedoublonne
echo "{"
echo '  "url": "'"$URL"'",'

first=true
for key in "${KEY_ORDER[@]}"; do
    if [ "$first" = true ]; then
        first=false
    else
        echo ","
    fi
    printf '  "%s": "%s"' "$key" "${LAST_VALUE[$key]}"
done
echo ""
echo "}"
