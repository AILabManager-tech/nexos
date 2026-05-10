# NEXOS — Dockerfile multi-stage
# Phase J du chantier mise_a_niveau (v4.2.0).
#
# Build:   docker build -t nexos:dev .
# Run:     docker run --rm -it nexos:dev nexos doctor
# Gateway: docker run --rm -p 8000:8000 nexos:dev uvicorn nexos_gateway:app --host 0.0.0.0

# =========================================================
# Stage 1 — builder : installe les deps Python + Node
# =========================================================
FROM python:3.11-slim AS builder

# Variables de build
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Deps système nécessaires au build + Node via nodesource
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      gnupg \
      git \
      build-essential \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copier pyproject.toml + lockfile pour installer deps (cache efficace)
COPY pyproject.toml ./
# Lockfile selon outil choisi en phase C
COPY uv.lock* poetry.lock* requirements.lock* ./

# Créer venv isolé
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Installer pip tools + deps
RUN pip install --upgrade pip setuptools wheel

# Copier le reste du code
COPY . .
RUN rm -f soic
COPY --from=soic_src / /app/soic

# Installer NEXOS en editable avec tous les extras sauf dev
# (dev contient mypy/ruff/pytest : pas utiles en runtime)
RUN pip install -e ".[api,wizard]"

# =========================================================
# Stage 2 — runtime : image minimale
# =========================================================
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:/usr/local/bin:/usr/bin:/bin" \
    NEXOS_LOG_LEVEL=INFO

# Deps runtime minimales (passwd fournit useradd, absent du slim)
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      ca-certificates \
      git \
      passwd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Node 20 via nodesource (runtime) + tooling Lighthouse/pa11y
# Installé directement ici (et non copié depuis le builder) pour préserver les
# symlinks /usr/bin/* créés par npm — un COPY déréférencerait le lien vers le
# script JS et casserait le résoudre des modules Node relatifs.
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && npm install -g lighthouse pa11y --omit=optional \
    && npm cache clean --force \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer un user non-root (useradd vit dans /usr/sbin, hors du PATH explicite)
RUN /usr/sbin/useradd -m -u 1000 -s /bin/bash nexos

# Copier venv et code depuis le builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder --chown=nexos:nexos /app /app

WORKDIR /app
USER nexos

# Exposer le port du gateway (si utilisé)
EXPOSE 8000

# Entry point : par défaut affiche l'aide
# Override via CLI: docker run nexos:dev nexos doctor
ENTRYPOINT []
CMD ["nexos", "--help"]

# Labels OCI
LABEL org.opencontainers.image.title="NEXOS"
LABEL org.opencontainers.image.description="NEXOS pipeline web autonome avec quality gates SOIC"
LABEL org.opencontainers.image.version="4.2.0-dev"
LABEL org.opencontainers.image.source="https://github.com/YOUR_ORG/nexos"
LABEL org.opencontainers.image.licenses="Proprietary"
