# Use a minimal base image
FROM docker-io-remote.rb-artifactory.bosch.com/python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install --upgrade pip && pip install uv

# Create and activate a virtual environment using uv
RUN uv venv .venv
ENV PATH="/app/.venv/bin:$PATH"

# Install Python dependencies using uv
COPY requirements.txt /app/
RUN uv pip install -r requirements.txt

# Copy MCP configuration to VS Code directory
RUN mkdir -p /app/.vscode
COPY mcp.json /app/.vscode/mcp.json
