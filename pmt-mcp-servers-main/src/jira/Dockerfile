FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Proxy settings are configurable via build args and should be set at runtime as needed.
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
# Optionally set proxy environment variables if build args are provided
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}

# Remove explicit proxy settings since they are now in the JSON file
RUN pip install --proxy "$HTTP_PROXY" uv

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
ENTRYPOINT ["uv", "run", "jiramcpserver.py"]

# Add a comment to clarify the use of rb-proxy
# Ensure the rb-proxy settings are passed during the build process
# Example: docker build --build-arg HTTP_PROXY=http://rb-proxy-de.bosch.com:8080 --build-arg HTTPS_PROXY=http://rb-proxy-de.bosch.com:8080 --build-arg NO_PROXY=localhost,127.0.0.1 .
