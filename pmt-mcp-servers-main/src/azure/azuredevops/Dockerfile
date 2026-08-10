FROM mcr.microsoft.com/azure-cli:2.61.0

WORKDIR /app

# Install uv (fast Python package manager)
RUN pip install --upgrade pip && pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install Python dependencies using uv
RUN uv sync --frozen --no-dev

# Copy azure devops server code
COPY . .

# Install Azure DevOps CLI extension
RUN az extension add --name azure-devops

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["uv", "run", "azuredevopsmcpserver.py"]
