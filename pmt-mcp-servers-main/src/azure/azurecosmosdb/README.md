# Azure Cosmos DB MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Azure Cosmos DB through SQL API queries.

## Overview

The Azure Cosmos DB MCP Server enables AI assistants to interact with Cosmos DB by executing SQL queries and performing CRUD operations. This server acts as a bridge between conversational AI and your NoSQL data, allowing for natural language queries to be translated into Cosmos DB SQL API operations and executed against your databases.

This MCP server uses the **Azure Cosmos DB SQL API** (Core/NoSQL API) to provide read and write access to Cosmos DB containers.

### Limitations

- Only supports Azure Cosmos DB SQL API (Core/NoSQL API)
- Maximum query result limit: 1000 items per query

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to an Azure Cosmos DB account with SQL API

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the MCP server after adding './vscode/mcp.json'. It is ready to use now.

For further details check out the [`../README.md`](../README.md) to find out more about e.g. [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

Replace the placeholder values (e.g., `<COSMOS_KEY>`) with your actual Azure Cosmos DB information.

| Variable | Description | Example |
|----------|-------------|---------|
| `COSMOS_HOST` | Azure Cosmos DB account endpoint URL | `https://your-account.documents.azure.com:443/` |
| `COSMOS_KEY` | Master key or read-write key for authentication, VSCode will open a prompt for this key | `your_secret_key` |
| `COSMOS_DATABASE` | Target database name | `vsm-backend` |
| `TRANSPORT` | Transport protocol | `stdio` (default), `http`, `sse`, `streamable-http` |
| `PORT` | Port for server (only for http/sse/streamable-http) | `8080` |
| `MCP_BINDING` | Binding address for MCP server | `127.0.0.1` |

### Usage Examples

The AI assistant will translate these following requests into appropriate Cosmos DB operations and execute them against your database. Try them out in your VSCode GitHub Copilot chat:

#### General Operations
- "Use the Azure Cosmos DB MCP server to list all containers in the database"
- "Query the 'product' container for all items where status is 'active'"
- "Read item with ID 'abc123' from the 'users' container with partition key 'user-group-1'"
- "Show me all items in the 'value_scope' container"

#### SQL Query Examples
- "Count all items in the 'implementation_binding' container"
- "Get the top 10 products by name from the 'product' container"

#### VSM-Specific Operations
- "List all value scopes in the system"
- "Show me all implementation bindings (ABBs) with their metadata"
- "Retrieve all ADAS products from the database"

#### Write Operations
- "Create a new item in the 'users' container with id 'user123'"
- "Update the item with id 'product456' in the 'product' container"
- "Delete item 'old-record' from the 'archive' container"

Check out our [BoschTube channel](https://bosch.mediaspace.de.kaltura.com/channel/Leverage%2BAI%2B%2540%2BBOSCH%2Bempowered%2Bby%2BPMT%2B%40XC/389167) for example use.

### Features

#### General-Purpose Tools
- `list_containers`: List all containers in the database
- `query_container`: Execute SQL queries on any container with Cosmos DB SQL API syntax
- `read_item`: Retrieve specific items by ID and partition key
- `create_item`: Create new items in containers
- `upsert_item`: Create or update items
- `delete_item`: Delete items by ID and partition key

#### VSM Domain-Specific Tools
- `list_value_scopes`: Retrieve all value scopes from the 'value_scope' container with complete details
- `list_value_scopes_names`: Retrieve only the element_id and scope of all value scopes for quick reference
- `list_implementation_bindings`: Retrieve a list of implementation binding names (also referred to as ABBs, Architecture Building Blocks, Building Blocks, building blocks) from the 'implementation_binding' container in the database
- `list_impl_binding_vs`: Retrieve all implementation bindings (ABBs) referenced by a specific value scope's 'implemented_by' field
- `list_products`: Retrieve all ADAS products from the 'product' container

### Troubleshooting

#### Connection Issues

If you encounter connection errors:
1. Verify the `COSMOS_HOST` URL is correct (must include `https://` and `:443/`)
2. Check that `COSMOS_KEY` is valid
3. Ensure the database name exists
4. Verify network connectivity to Azure

## Further Information

### Azure Cosmos DB SQL API Documentation

- [Python SDK Overview](https://learn.microsoft.com/en-us/python/api/overview/azure/cosmos-readme)
- [SQL API Documentation](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/)
- [SQL Query Reference](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/query/)
- [Python SDK Samples](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/cosmos/azure-cosmos/samples)
- [Best Practices](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/best-practice-dotnet)

### Additional Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Azure Cosmos DB Documentation](https://learn.microsoft.com/en-us/azure/cosmos-db/)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
