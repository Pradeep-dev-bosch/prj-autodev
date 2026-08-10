# syntax=docker/dockerfile:1
FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Build arguments for proxy only.
# NOTE: Proxy settings are for build time only - NOT runtime.
# Artifactory credentials are supplied via BuildKit --secret (never baked into image layers):
#   docker build --secret id=tech_username,env=TECH_USERNAME \
#                --secret id=jfrog_token,env=JFROG_TOKEN ...
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

WORKDIR /app

# Install system dependencies for matplotlib and other packages that need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libfreetype6-dev \
    libpng-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv via pip with proxy (build time only)
RUN if [ -n "$HTTP_PROXY" ]; then \
        pip install --proxy "$HTTP_PROXY" uv; \
    else \
        pip install uv; \
    fi

# Copy project configuration files and lock file for reproducible builds
COPY pyproject.toml uv.lock README.md ./

# Configure UV with Artifactory authentication and install dependencies.
# Credentials are read from BuildKit secrets and passed as UV_INDEX_* env vars
# so they are never embedded in URLs or baked into image layers.
RUN --mount=type=secret,id=tech_username \
    --mount=type=secret,id=jfrog_token \
    TECH_USERNAME=$(cat /run/secrets/tech_username 2>/dev/null || echo "") && \
    JFROG_TOKEN=$(cat /run/secrets/jfrog_token 2>/dev/null || echo "") && \
    if [ -n "$TECH_USERNAME" ] && [ -n "$JFROG_TOKEN" ]; then \
        echo "Installing with ARC package from Artifactory..."; \
        if [ -n "$HTTP_PROXY" ]; then \
            UV_INDEX_PYSOFA_ARC_USERNAME="$TECH_USERNAME" UV_INDEX_PYSOFA_ARC_PASSWORD="$JFROG_TOKEN" \
            HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} uv sync --frozen --no-cache; \
        else \
            UV_INDEX_PYSOFA_ARC_USERNAME="$TECH_USERNAME" UV_INDEX_PYSOFA_ARC_PASSWORD="$JFROG_TOKEN" \
            uv sync --frozen --no-cache; \
        fi; \
    else \
        echo "WARNING: Credentials not provided via BuildKit secrets. Installation may fail for ARC package."; \
        if [ -n "$HTTP_PROXY" ]; then \
            HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} uv sync --frozen --no-cache || echo "Installation failed - ARC package may be unavailable"; \
        else \
            uv sync --frozen --no-cache || echo "Installation failed - ARC package may be unavailable"; \
        fi; \
    fi

# Copy the MCP server script
COPY arcmcpserver.py .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TRANSPORT=stdio
ENV CERT_PATH=
# Set system CA bundle defaults so Python requests / curl use the
# system trust store by default. At runtime, initialize_arc() overrides these when
# CERT_PATH is set to a custom path or to a disable keyword.
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

# CRITICAL: Do NOT set HTTP_PROXY/HTTPS_PROXY environment variables at runtime!
# Proxy settings will BLOCK Bosch internal service connections (SharePoint, Jira, OneQ, etc.)
# The container should connect directly to these services without proxy.

# Run the MCP server
CMD ["uv", "run", "arcmcpserver.py"]
