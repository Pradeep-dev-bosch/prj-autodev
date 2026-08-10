FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Proxy settings configured via build args
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
# Optionally set proxy environment variables if build args are provided
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}

# Install uv via pip
RUN pip install --proxy "$HTTP_PROXY" uv

WORKDIR /app

# Copy uv configuration
COPY pyproject.toml uv.lock ./

# Install dependencies using uv with lock file
RUN uv sync --frozen --no-dev

# Copy the MCP server code
COPY artifactorymcpserver.py .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["uv", "run", "artifactorymcpserver.py"]
