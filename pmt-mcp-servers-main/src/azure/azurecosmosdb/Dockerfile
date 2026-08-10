FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

WORKDIR /app

# Install uv via pip
RUN pip install --proxy http://rb-proxy-de.bosch.com:8080 uv

# Copy uv configuration
COPY pyproject.toml uv.lock ./

# Install dependencies with proxy settings
RUN HTTP_PROXY=http://rb-proxy-de.bosch.com:8080 \
    HTTPS_PROXY=http://rb-proxy-de.bosch.com:8080 \
    uv sync --frozen --no-cache

# Copy the rest of the application code
COPY azurecosmosdbmcpserver.py ./

# Expose port 8080
EXPOSE 8080
ENV MCP_BINDING="0.0.0.0"

# Default command (can be changed as needed)
CMD ["uv", "run", "azurecosmosdbmcpserver.py"]