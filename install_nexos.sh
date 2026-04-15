#!/usr/bin/env bash
# NEXOS — Installation CLI (phase L du chantier mise_a_niveau v4.2.0)
#
# Usage:
#   bash install_nexos.sh              # installation standard (venv + core + api + wizard)
#   bash install_nexos.sh --dev        # + extras dev (ruff, mypy, pytest)
#   bash install_nexos.sh --no-venv    # saute la création du venv (utilise python courant)
#   bash install_nexos.sh --no-precommit  # saute l'install des hooks pre-commit
#   bash install_nexos.sh --help       # affiche cette aide

set -euo pipefail

# -----------------------------------------------------
# Defaults + parsing args
# -----------------------------------------------------
USE_VENV=1
INSTALL_DEV=0
INSTALL_PRECOMMIT=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --no-venv) USE_VENV=0; shift ;;
    --dev) INSTALL_DEV=1; shift ;;
    --no-precommit) INSTALL_PRECOMMIT=0; shift ;;
    --help|-h)
      grep "^#" "$0" | head -20
      exit 0
      ;;
    *) echo "Unknown flag: $1"; exit 2 ;;
  esac
done

# -----------------------------------------------------
# Helpers
# -----------------------------------------------------
C_OK='\033[0;32m'
C_WARN='\033[0;33m'
C_ERR='\033[0;31m'
C_RESET='\033[0m'

log()   { echo -e "${C_OK}[install]${C_RESET} $1"; }
warn()  { echo -e "${C_WARN}[warn]${C_RESET} $1"; }
err()   { echo -e "${C_ERR}[error]${C_RESET} $1" >&2; }
die()   { err "$1"; exit 1; }

# -----------------------------------------------------
# Preflight : check prérequis
# -----------------------------------------------------
log "Preflight checks..."

# Python 3.10+
if ! command -v python3 >/dev/null 2>&1; then
  die "python3 non trouvé. Installe Python 3.10+."
fi
PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if [[ "$PY_MAJOR" -lt 3 ]] || { [[ "$PY_MAJOR" -eq 3 ]] && [[ "$PY_MINOR" -lt 10 ]]; }; then
  die "Python $PY_VERSION détecté, NEXOS requiert ≥3.10."
fi
log "Python $PY_VERSION ✓"

# Node 20+ (warning seulement, pas bloquant pour les modes qui n'exécutent pas le build)
if command -v node >/dev/null 2>&1; then
  NODE_VERSION=$(node --version | sed 's/v//')
  NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)
  if [[ "$NODE_MAJOR" -lt 20 ]]; then
    warn "Node $NODE_VERSION détecté, NEXOS recommande ≥20 pour les builds Next.js."
  else
    log "Node $NODE_VERSION ✓"
  fi
else
  warn "Node non trouvé. NEXOS fonctionne sans Node pour les modes doctor/audit, mais npm/build sont requis pour create/modify."
fi

# Git
if ! command -v git >/dev/null 2>&1; then
  warn "Git non trouvé. Optionnel mais recommandé."
fi

# -----------------------------------------------------
# Paths
# -----------------------------------------------------
NEXOS_ROOT="$(cd "$(dirname "$0")" && pwd)"
CLI_PATH="$NEXOS_ROOT/nexos_cli.py"
LINK_PATH="$HOME/.local/bin/nexos"
VENV_PATH="$NEXOS_ROOT/.venv"

if [[ ! -f "$CLI_PATH" ]]; then
  die "nexos_cli.py introuvable dans $NEXOS_ROOT."
fi

# -----------------------------------------------------
# Venv (optionnel)
# -----------------------------------------------------
if [[ $USE_VENV -eq 1 ]]; then
  if [[ -d "$VENV_PATH" ]]; then
    log "Venv existant détecté à $VENV_PATH (réutilisation)"
  else
    log "Création du venv à $VENV_PATH"
    python3 -m venv "$VENV_PATH"
  fi
  # shellcheck disable=SC1091
  source "$VENV_PATH/bin/activate"
  log "Venv activé"
  PIP_CMD="pip"
else
  log "Mode --no-venv : utilisation du python3 courant"
  PIP_CMD="python3 -m pip --user"
fi

# -----------------------------------------------------
# Install NEXOS en éditable
# -----------------------------------------------------
log "Upgrade pip + setuptools..."
$PIP_CMD install --upgrade pip setuptools wheel

EXTRAS="api,wizard"
if [[ $INSTALL_DEV -eq 1 ]]; then
  EXTRAS="$EXTRAS,dev"
fi

log "Installing NEXOS en éditable (extras: $EXTRAS)..."
$PIP_CMD install -e "$NEXOS_ROOT[$EXTRAS]"

# -----------------------------------------------------
# Symlink CLI global
# -----------------------------------------------------
chmod +x "$CLI_PATH"
mkdir -p "$HOME/.local/bin"
if [[ -e "$LINK_PATH" || -L "$LINK_PATH" ]]; then
  rm -f "$LINK_PATH"
fi
ln -sf "$CLI_PATH" "$LINK_PATH"
log "Symlink $LINK_PATH → $CLI_PATH"

# Ajouter ~/.local/bin au PATH si manquant
EXPORT_LINE='export PATH="$HOME/.local/bin:$PATH"'
for rcfile in "$HOME/.bashrc" "$HOME/.zshrc"; do
  if [[ -f "$rcfile" ]] && ! grep -qF '.local/bin' "$rcfile"; then
    echo "$EXPORT_LINE" >> "$rcfile"
    log "PATH ajouté à $rcfile"
  fi
done
export PATH="$HOME/.local/bin:$PATH"

# -----------------------------------------------------
# Pre-commit hooks (optionnel)
# -----------------------------------------------------
if [[ $INSTALL_PRECOMMIT -eq 1 ]] && [[ $INSTALL_DEV -eq 1 ]]; then
  if [[ -f "$NEXOS_ROOT/.pre-commit-config.yaml" ]]; then
    log "Installation des hooks pre-commit..."
    (cd "$NEXOS_ROOT" && pre-commit install) || warn "pre-commit install a échoué (non bloquant)"
  else
    warn ".pre-commit-config.yaml absent. Skipping hooks."
  fi
elif [[ $INSTALL_PRECOMMIT -eq 1 ]]; then
  warn "pre-commit skippé (--dev requis pour l'installer)"
fi

# -----------------------------------------------------
# Smoke test final
# -----------------------------------------------------
if ! python3 -c "import nexos" 2>/dev/null; then
  die "Import 'nexos' échoue après install. Diagnostic requis."
fi

NEXOS_VERSION=$(python3 -c 'import tomllib,sys; d=tomllib.load(open(sys.argv[1],"rb")); print(d["project"]["version"])' "$NEXOS_ROOT/pyproject.toml" 2>/dev/null || echo "?")
log "✅ NEXOS v${NEXOS_VERSION} installé"

cat <<EOF

Quick start:
  nexos --help
  nexos doctor
  nexos create --client-dir clients/mon-client

Si 'nexos' n'est pas trouvé: ouvre un nouveau terminal (ou rechargement rc).

Désinstallation: bash $NEXOS_ROOT/uninstall_nexos.sh
EOF
