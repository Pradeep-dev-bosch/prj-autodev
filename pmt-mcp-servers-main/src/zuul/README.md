# Zuul CI MCP Server

A Bosch developed [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Zuul CI. This server is sourced from the [BOSCH internal repository](https://github.boschdevcloud.com/bios-genAI/zuul-mcp-server/tree/master) and referenced here for MCP client integration.

## Overview

The Zuul CI MCP Server provides comprehensive integration with Zuul CI instances. It exposes a rich set of tools for querying builds, jobs, and tenant information directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the Model Context Protocol and uses the Zuul REST API.

### Limitations

- Some advanced Zuul features may not be exposed yet
- Authentication token must have appropriate permissions for the tenant
- Job secrets are automatically redacted in responses

## Getting Started

### Prerequisites

- Github Copilot Subscription
- Access to a Zuul CI instance (e.g., `https://neo-zuul-dev.rbadas.bosch.tech`)
- Valid Zuul authentication token

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `ZUUL_API_URL` | Base URL for Zuul CI instance | `https://neo-zuul-dev.rbadas.bosch.tech` |
| `ZUUL_AUTH_TOKEN` | Authentication token for Zuul API access | `xxxxx` |

**Note:** When using the provided `mcp.json` configuration, you'll be prompted for credentials and configuration at runtime.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with Zuul CI using natural language. Try these examples in your VS Code GitHub Copilot chat:

- "Show me recent builds for project X"
- "Get information about build UUID abc-123"
- "What jobs are configured for the check pipeline in tenant main?"
- "Show me the job graph for this change"
- "Get details about the freeze-job configuration"

The AI assistant will translate these natural language requests into actual API requests and execute them against your Zuul CI instance.

## Features

The server provides the following MCP tools for comprehensive Zuul CI management:

- **Server Information**:
  - `info` - Get Zuul server information and status (no parameters required)
  
- **Tenant Management**:
  - `tenant_info` - Retrieve detailed tenant information (requires `tenant` parameter)
  
- **Build Management**:
  - `build_info` - Get detailed build information by UUID (optional `inventory_only` parameter returns just inventory)
  - `builds` - List builds matching filters (supports many filters: project, pipeline, change, branch, patchset, result, etc.)
  
- **Job Management**:
  - `freeze_job` - Get job definition as it would run in a pipeline (combines variants; secrets are redacted)
  - `job_graph` - Get job dependency graph for a change or ref in a pipeline (shows job dependencies and relationships)

> [!NOTE]
> More MCP tools are under development.

## Troubleshooting

### Connection Issues
- **"Failed to connect to Zuul API"**: Verify `ZUUL_API_URL` and `ZUUL_AUTH_TOKEN` are correct
- **Authentication failures**: Check if authentication token is valid and not expired
- **Permission errors**: Ensure token has necessary tenant and project permissions
- **Network timeouts**: Check network connectivity to Zuul instance

### Common Errors
- **"Tenant not found"**: Verify tenant name is correct - use `info` tool to see available tenants
- **"Build not found"**: Check build UUID is correct and accessible with your credentials
- **"Invalid parameters"**: Ensure all required parameters are provided for the tool
- **"ZUUL_AUTH_TOKEN environment variable is required"**: Ensure the token is set in environment or `.env` file
- **"Invalid URL"**: Ensure `ZUUL_API_URL` includes the protocol (https://) and correct hostname
- **"Permission denied"**: Token may not have access to requested tenant or project
- **Empty results**: Check filter parameters - overly restrictive filters may return no results

## Further Information

- [Author](https://github.com/buu1sh_bosch)
- [Zuul MCP server Source Repository](https://github.boschdevcloud.com/bios-genAI/zuul-mcp-server/tree/master)
- [Zuul CI Documentation](https://zuul-ci.org/docs/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
