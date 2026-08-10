# Codebeamer MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Codebeamer.

## Overview

The Codebeamer MCP Server provides comprehensive integration with Codebeamer instances. It exposes a rich set of tools for managing projects, trackers, and items directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the Codebeamer REST API.

### Limitations

- Tracker creation and deletion are not supported
- Bulk item operations are not available yet
- Depending on the LLM models, accuracy might differ

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to Codebeamer instance (default: `https://rb-cb-01-t3.dev.bosch.com`)
- Valid Codebeamer username and password
- Codebeamer API Access for the project

### Codebeamer API Access

> **Important:** API access requires approval from the **Master of Data** for each project you need access to. This can cause delays if not handled proactively.

**To speed up the access process:**

1. **Option A:** Contact your project's Master of Data *before* submitting your request to get pre-approval
2. **Option B:** Ask your Master of Data to request API access on your behalf

See [Codebeamer Access Documentation](https://inside-docupedia.bosch.com/confluence/spaces/CCD/pages/5773563428/Codebeamer+Access) for details.

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with Codebeamer using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Get all projects from Codebeamer"
- "List all trackers in project X"
- "Fetch items from tracker Y with pagination"
- "Get detailed information about item with ID 12345"
- "Execute a CbQL query to find all requirements"

The AI assistant will translate these natural language requests into actual API requests and execute them in Codebeamer.

### Features

The server provides the following MCP tools for comprehensive Codebeamer management:

- **Project Management**:
  - `cb_projects` - Retrieve a list of projects

- **Tracker Management**:
  - `cb_trackers` - List trackers within a project
  - `cb_tracker_items` - Fetch items from a tracker with pagination support

- **Item Management**:
  - `cb_item` - Retrieve detailed information about a specific item

- **Query Support**:
  - `cb_query` - Execute CbQL (Codebeamer Query Language) queries to filter and retrieve items
  - `cb_fetch_crs_srs_all` - Execute CbQL query to retrieve filtered items

### Configuration

Set the following environment variables:

```bash
export CB_BASE_URL=https://rb-cb-01-t3.dev.bosch.com
export CB_USER=your_ntid
export CB_PASS=your_password
```

**Note:** Passwords are securely taken as input from the user and are not stored in configuration files. The MCP server will prompt for credentials when needed, ensuring sensitive information remains protected.

### Troubleshooting

#### Connection Issues
- **"Failed to connect to Codebeamer"**: Verify `CB_BASE_URL`, `CB_USER`, and `CB_PASS` are correct
- **Authentication failures**: Check if username and password are valid
- **Permission errors**: Ensure user has necessary project and tracker permissions

#### Common Errors
- **"Project not found"**: Verify project name or ID exists - use `cb_projects` to list available projects
- **"Tracker not found"**: Check tracker ID and project access - use `cb_trackers` to list available trackers
- **"Item not found"**: Verify item ID exists and you have access permissions
- **Network timeouts**: Check proxy settings if running in corporate environment
- **"Invalid URL"**: Ensure `CB_BASE_URL` includes the protocol (https://) and correct hostname

## Further Information

- [Codebeamer Documentation](https://codebeamer.com/cb/wiki/11375739)
- [Codebeamer REST API](https://codebeamer.com/cb/wiki/11375739)
- [CbQL Query Language](https://codebeamer.com/cb/wiki/11375739)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
