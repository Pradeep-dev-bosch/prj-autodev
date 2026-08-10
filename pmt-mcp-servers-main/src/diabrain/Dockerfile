FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Proxy settings are configurable via build args and should be set at runtime as needed.
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
# Optionally set proxy environment variables if build args are provided
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}

# Install uv with proxy if configured
RUN if [ -n "$HTTP_PROXY" ]; then \
        pip install --proxy "$HTTP_PROXY" uv; \
    else \
        pip install uv; \
    fi

WORKDIR /app
# Copy uv configuration
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with lock file
RUN HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    uv sync --frozen --no-cache

# Copy the server code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1


# Expose the server
ENTRYPOINT ["uv", "run", "diabrainmcpserver.py"]
