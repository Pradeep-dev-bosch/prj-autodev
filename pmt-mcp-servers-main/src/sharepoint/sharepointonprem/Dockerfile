FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Proxy settings for build time only (downloading packages)
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# Install system CA certificates and dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN if [ -n "$HTTP_PROXY" ]; then \
        pip install --proxy "$HTTP_PROXY" uv; \
    else \
        pip install uv; \
    fi

WORKDIR /app
# Copy configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with lock file and create virtual environment
RUN if [ -n "$HTTP_PROXY" ]; then \
        HTTP_PROXY=${HTTP_PROXY} HTTPS_PROXY=${HTTPS_PROXY} uv sync --frozen; \
    else \
        uv sync --frozen; \
    fi

# Copy the server code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# SSL Configuration:
# Docker: Certificates mounted via volume in mcp.json (-v /etc/ssl/certs/ca-certificates.crt:...)
# Python: Set CERTIFICATE_PATH env variable if using custom certificates
#
# CERTIFICATE_PATH override options:
#   - Not set / Empty → Auto-detects mounted cert, falls back to certifi bundle
#   - "false" / "disable" / "off" / "no" → Disables SSL verification (dev/test only)
#   - File path → Uses specified certificate file (e.g., /path/to/custom-ca.pem)
#
# NOTE: NTLM authentication works with or without proxy configuration.

# Expose the server
ENTRYPOINT ["uv", "run", "sharepointonpremserver.py"]
