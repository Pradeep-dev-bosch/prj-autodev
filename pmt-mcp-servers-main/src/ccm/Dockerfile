FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Set proxy environment variables for pip
ENV HTTPS_PROXY=http://rb-proxy-de.bosch.com:8080
ENV HTTP_PROXY=http://rb-proxy-de.bosch.com:8080
ENV http_proxy=http://rb-proxy-de.bosch.com:8080
ENV https_proxy=http://rb-proxy-de.bosch.com:8080
ENV NO_PROXY=localhost,127.0.0.1,.bosch.com

WORKDIR /app

# Install uv via pip
RUN pip install --proxy http://rb-proxy-de.bosch.com:8080 uv

# Copy uv configuration
COPY pyproject.toml uv.lock ./

# Install dependencies with proxy settings
RUN HTTP_PROXY=http://rb-proxy-de.bosch.com:8080 \
    HTTPS_PROXY=http://rb-proxy-de.bosch.com:8080 \
    uv sync --frozen --no-cache

# Copy the server code
COPY ccmmcpserver.py .

# Set environment variables
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1

# Start CCM MCP server
CMD ["uv", "run", "ccmmcpserver.py"]
