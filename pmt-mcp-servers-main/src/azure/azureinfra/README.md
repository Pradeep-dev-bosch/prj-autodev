# Azure Cloud MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Microsoft Azure services through REST APIs and SDKs.

## Overview

The Azure Cloud MCP Server enables AI assistants to interact with Azure resources including storage accounts, virtual machines, databases, and other cloud services. This server acts as a bridge between conversational AI and your Azure infrastructure, allowing for natural language queries to be translated into Azure API calls.

## Features

- **Comprehensive Azure Service Access**: Interact with 30+ Azure services including Storage, VMs, Databases, Key Vault, and more
- **Multiple Authentication Methods**: Support for Service Principal, Azure CLI, and Managed Identity authentication
- **Secure Connection Management**: Environment-based configuration for Azure credentials
- **Error Handling**: Comprehensive error handling and logging for debugging
- **Flexible Deployment**: Support for Docker, NPM, and native deployments
- **Proxy Support**: Built-in support for corporate proxy environments

## Available Tools

### Core Azure Tools

- `subscription_list` - List all Azure subscriptions
- `group_list` - List resource groups in a subscription
- `storage` - Manage Azure Storage accounts and blobs
- `keyvault` - Access Azure Key Vault secrets and keys
- `sql` - Interact with Azure SQL databases
- `cosmos` - Query Azure Cosmos DB resources
- `appservice` - Manage Azure App Services
- `functionapp` - Work with Azure Functions

## Prerequisites

- Docker
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Azure subscription with appropriate permissions
- Service Principal with required role assignments (Reader role minimum)
- Required environment variables (see Configuration section)
- Azure CLI (optional, for authentication setup)

## Installation
### Installation

Choose one of the options below to install and run the Azure MCP Server.

#### Docker (recommended)
1. Pull the official image:
```bash
docker pull artifactory.boschdevcloud.com/pmt-mcp-servers-docker-local/azure-mcp-server:0.0.0
```
2. Run the container (replace the env-file path with your `.env`):
```bash
docker run -i --rm --env-file /path/to/.env artifactory.boschdevcloud.com/pmt-mcp-servers-docker-local/azure-mcp-server:0.0.0
```

#### Install Azure CLI (required for optional CLI auth workflows)
Execute the official installer for wsl Debian/Ubuntu:
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```
After installation, verify with:
```bash
az --version
```

#### Run from source
1. Clone the repository:
```bash
git clone https://github.com/your-org/azure-mcp.git
cd azure-mcp
```


Notes:
- Ensure your `.env` file contains the required Azure credentials (see Configuration).
- When running in corporate networks, configure Docker/CLI proxy settings if needed.
- Use a Service Principal or Managed Identity with appropriate roles for production deployments.
### Docker

1. **Ensure Docker is installed:**

   Docker is typically included in the WSL setup. If Docker is not found in your WSL environment, follow the [Docker for Linux installation guide](https://inside-docupedia.bosch.com/confluence/spaces/DEVCORNER/pages/1595519415/Docker+for+Linux).

2. **Configure environment variables** (see Configuration section)

3. **Move the mcp.json file into .vscode**

   ```bash
   # Create .vscode directory and move mcp.json into it
   mkdir -p .vscode
   mv mcp.json .vscode/
   ```

## Configuration
### .env example and setup

Create a `.env` file containing your Azure Service Principal credentials. Do NOT commit this file to version control.

Example contents:
```env
# Azure Service Principal credentials
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret

# Optional (recommended): subscription used by the server
AZURE_SUBSCRIPTION_ID=your-subscription-id
```

Create and secure the file:
```bash
# create .env interactively (replace placeholders)
cat > .env <<'EOF'
AZURE_TENANT_ID=your-tenant-id
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_SUBSCRIPTION_ID=your-subscription-id
EOF

# restrict permissions
chmod 600 .env
```

Verify the credentials (service-principal login):
```bash
az login --service-principal -u "$AZURE_CLIENT_ID" -p "$AZURE_CLIENT_SECRET" --tenant "$AZURE_TENANT_ID"
az account show
```

### Authentication Setup

1. **Create a Service Principal:**

   ```bash
   az ad sp create-for-rbac --name "your-mcp-server" --role Reader --scopes /subscriptions/YOUR_SUBSCRIPTION_ID
   ```

2. **Copy the credentials** to your `.env` file

3. **Verify authentication:**

   ```bash
   docker run -i --rm \
     --env-file azurecloud/.env \
     artifactory.boschdevcloud.com/pmt-mcp-servers-docker-local/azure-mcp-server:0.0.01 \
     az account show
   ```

## MCP Client Integration

### VS Code Agent

Use mcp.json to start the Azure MCP server when running in VS Code agent mode.

1. Start the server:
- If your VS Code agent extension supports mcp.json, it will read this file and launch the configured server. Consult your agent extension docs to start/attach to MCP servers.
- Otherwise start the server manually from the workspace root using the same command from mcp.json:
```bash
docker run -i --rm --env-file src/azurecloud/.env artifactory.boschdevcloud.com/pmt-mcp-servers-docker-local/azure-mcp-server:0.0.0
```

Or use VS Code agent integration with the updated `mcp.json`.

## Usage Examples

Once configured, you can interact with Azure resources through MCP-compatible AI assistants. Example prompts:

**Resource Management:**
- "List all virtual machines in my subscription"
- "Show me the storage accounts in resource group 'production'"
- "Get the status of Azure Function App 'my-function'"

**Monitoring & Insights:**
- "Show me Application Insights metrics for the last 24 hours"
- "Get resource health alerts for my subscription"
- "Display Azure Monitor logs for failed requests"

**Infrastructure:**
- "List all AKS clusters and their node status"
- "Show me Key Vault secrets (metadata only)"
- "Get Azure SQL database performance metrics"

### Common Issues

**"No subscriptions found" error:**
- Ensure your service principal has at least Reader role on the subscription
- Verify all environment variables are set correctly in your `.env` file

**Docker container fails to start:**
- Check Docker is running: `docker --version`
- Verify the image exists: `docker images | grep azure-sdk/azure-mcp`
- Ensure .env file path is correct and readable

**Authentication errors:**
- Test Azure CLI login: `az account list`
- Verify service principal: `az ad sp show --id YOUR_CLIENT_ID`
- Check tenant ID matches your Azure subscription

### Support

For additional support:
- [Azure MCP Documentation](https://github.com/microsoft/mcp)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [Azure SDK Documentation](https://docs.microsoft.com/en-us/azure/developer/)
