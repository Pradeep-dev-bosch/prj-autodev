FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Proxy settings for build time only (downloading packages)
# WARNING: Do NOT pass proxy settings at runtime for Outlook/Microsoft Graph
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

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

# CRITICAL: Do NOT pass HTTP_PROXY/HTTPS_PROXY environment variables at runtime!
# Proxy settings will BLOCK Microsoft Graph/Outlook authentication (*.microsoft.com, *.office365.com).
# The container should connect directly to Microsoft Graph without proxy.
# Only use proxy for on-premises scenarios if explicitly required by your network.

# Expose the server
ENTRYPOINT ["uv", "run", "outlookmcpserver.py"]
