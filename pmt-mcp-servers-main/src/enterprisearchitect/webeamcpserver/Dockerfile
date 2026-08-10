FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Set proxy environment variables for pip
ENV HTTPS_PROXY=http://host.docker.internal:3128
ENV HTTP_PROXY=http://host.docker.internal:3128
ENV http_proxy=http://host.docker.internal:3128
ENV https_proxy=http://host.docker.internal:3128
ENV NO_PROXY=host.docker.internal,localhost,127.0.0.1,.bosch.com

# Install uv via pip
RUN pip install --proxy http://rb-proxy-de.bosch.com:8080 uv

WORKDIR /app

# Create output directory
RUN mkdir -p mcpserver_output

# Copy uv configuration
COPY pyproject.toml uv.lock ./

# Install dependencies with proxy settings
RUN HTTP_PROXY=http://rb-proxy-de.bosch.com:8080 \
    HTTPS_PROXY=http://rb-proxy-de.bosch.com:8080 \
    uv sync --frozen --no-cache

# Copy source code
COPY webeaclient.py webeamcpserver.py ./

# Run the MCP server
CMD ["uv", "run", "webeamcpserver.py"]
