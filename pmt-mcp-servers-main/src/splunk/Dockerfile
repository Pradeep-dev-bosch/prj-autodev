FROM docker-io-remote.rb-artifactory.bosch.com/python:3.11-slim

# Accept proxy configuration as build arguments
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY=localhost,127.0.0.1,.bosch.com

# Set proxy environment variables if provided
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}

WORKDIR /app

# Install uv via pip with proxy if available
RUN if [ -n "$HTTP_PROXY" ]; then pip install --proxy $HTTP_PROXY uv; else pip install uv; fi

# Copy uv configuration
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy the server code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    TRANSPORT=stdio

# Start Splunk MCP server
CMD ["uv", "run", "mcp-splunk"]
