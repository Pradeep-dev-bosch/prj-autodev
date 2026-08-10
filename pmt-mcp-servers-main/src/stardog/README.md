# Stardog MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Stardog knowledge graphs through SPARQL queries.

## Overview

The Stardog MCP Server enables AI assistants to interact with Stardog by executing SPARQL queries. This server acts as a bridge between conversational AI and your semantic data, allowing for natural language queries to be translated into SPARQL and executed against your Stardog databases.

### Limitations

- Only supports SPARQL SELECT queries

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to a Stardog database

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the MCP server after adding './vscode/mcp.json'. It is ready to use now.

For further details check out the [`../README.md`](../README.md) to find out more about e.g. [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

- Replace the placeholder values (e.g., `<STARDOG_USERNAME>`) with your actual Stardog information
- The proxy settings are configured for Bosch corporate environment - remove or modify these if not needed

| Variable | Description | Example |
|----------|-------------|---------|
| `STARDOG_USERNAME` | Username for Stardog authentication | `admin` |
| `STARDOG_PASSWORD` | Password for Stardog authentication, VSCode will open a prompt for this password | `admin` |
| `STARDOG_ENDPOINT` | Stardog server endpoint URL | `http://localhost:5820` |
| `STARDOG_DATABASE` | Target database name | `myknowledgegraph` |

### Usage Examples

The AI assistant will translate these following requests into appropriate SPARQL queries and execute them against your Stardog database. Try them out in your VSCode GitHub Copilot chat:

- "Use the available stardog-docker-mcp-server tool to run an easy example Stardog SPARQL query e.g. "SELECT ?s ?p ?o\nWHERE {\n  ?s ?p ?o\n}\nLIMIT 10""

Check out our [BoschTube channel](https://bosch.mediaspace.de.kaltura.com/channel/Leverage%2BAI%2B%2540%2BBOSCH%2Bempowered%2Bby%2BPMT%2540XC/389167) for an example use.

### Features

- `stardog_sparql_query`: Execute SELECT SPARQL queries against your Stardog database.

### Troubleshooting

To check access to Stardog run the following command (with all placeholders replaced):

```bash
curl -i --request POST --url <STARDOG_ENDPOINT>/<STARDOG_DATABASE>/query  --header 'authorization: Basic <base64(STARDOG_USERNAME:STARDOG_PASSWORD)>' --header 'content-type: application/sparql-query' --data 'SELECT * WHERE { ?s ?p ?o . }'
```

## Further Information

- [Stardog Documentation](https://docs.stardog.com/)
- [SPARQL 1.1 Specification](https://www.w3.org/TR/sparql11-query/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
