# WebEA MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Web Enterprise Architect environments using the Enterprise Architect OSLC API.

## Overview

The WebEA MCP Server allows AI assistants to seamlessly interact with Enterprise Architect repositories hosted on Pro Cloud. It offers full integration with WebEA environments, enabling you to query, create, and manage model elements, packages, and connectors directly from your AI-powered development tools. The server can be operated in a headless mode.

### Limitations

1. Through the WebEA API, the diagram object is not accessible. This means:
   - The content of the diagram cannot be retrieved
   - Diagrams cannot be created programmatically
   - However, diagrams can be retrieved as images, and elements can be created. Users must manually attach elements to diagrams
2. This server works only for WebEA server-based repositories/models and not for repositories stored in github.
3. Destructive SQL operations restricted: DELETE, DROP, TRUNCATE, and ALTER are blocked in `query_resources()` parameters for safety. Use EA GUI for these operations
4. Currently, only a single endpoint and model are supported at a time. To switch to a different model, you must restart the MCP server after updating the input.

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../../README.md#access-to-pmt-artifactory-repository))
- Access to Bosch WebEA server and model.

### MCP Client Integration

1. The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

2. Start the Docker version MCP server after adding `.vscode/mcp.json`.

3. Check out the [`../../README.md`](../../README.md) to find out more about [`Running MCP Servers using uv/python`](../../README.md#running-mcp-servers-for-development)

### Configuration

Set the following environment variables (in `mcp.json`) for required MCP server `webea-docker-mcp-server`:

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `WEBEA_USERNAME` | Username for WebEA authentication NT ID with region | `de\\qqq1fe` |
| `WEBEA_PASSWORD` | Password for WebEA authentication, VSCode will open a prompt for this password | `xxxxxxx` |
| `WEBEA_ENDPOINT` | WebEA server endpoint URL | `https://xc-ea.de.bosch.com/:804` |
| `WEBEA_MODEL` | Model/Repository name | `MY_MODEL` |

Configure the proxy environment variables `HTTP_PROXY`, `HTTPS_PROXY`, `http_proxy`, and `https_proxy` (example: `http://rb-proxy-de.bosch.com:8080`) in `mcp.json` if required for your Bosch environment.

**Note:** Passwords and tokens are securely taken as input from the user and are not stored in configuration files. To retry password input check out the [`../../README.md`](../../README.md) for instructions

### Usage Examples

Once connected to VSCode GitHub Copilot chat or an MCP-compatible client, you can interact with WebEA using natural language.<br>Try these examples in your VSCode GitHub Copilot chat:  (Use premium models such as GPT-5, Claude Sonnet 4.5 etc. to get best results)

- "What is the root package of the EA model"
- "How many diagrams are present in this model"
- "Explain ElementA to me"
- "Create a new requirement element called 'SystemComponent' inside the parent package Pkg_name"
- "Create a connector between ElementA and ElementB of type Association"
- "Create a package inside the Pkg1 and then create a top 5 requirement elements of a adas ECU inside this newly created package."
- "Retrieve the diagram image for diagram 'SystemOverview'"

The AI assistant will translate these natural language requests into actual OSLC API requests and execute them against your WebEA model.

### Features

The server provides the following MCP tools for comprehensive WebEA management:

- **Package Management**:
  - `get_root_package` - Retrieves the root package of the EA model
  - `get_target_package` - Provides information about the target package
  - `get_package_info` - Fetches detailed information about a package
  - `create_package` - Creates a new package under a parent package

- **Element Management**:
  - `get_element_info` - Fetches details about a specific element
  - `create_element` - Creates a new element in a package
  - `update_element` - Updates properties of an existing element

- **Connector Management**:
  - `create_connector` - Links elements with a connector
  - `update_connector` - Updates properties of an existing connector

- **Diagram & Visualization**:
  - `get_diagram_info` - Retrieves information about a specific diagram
  - `get_diagram_image` - Retrieves an image of a specific diagram

- **Query & Status**:
  - `query_resources` - Queries resources based on a where clause
  - `get_server_status` - Provides the current status of the server

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication errors | Verify WEBEA_USERNAME and WEBEA_PASSWORD are correct |
| Access denied | Verify if you have the access to the server and model you are trying to access |
| Connection timeout | Check WEBEA_ENDPOINT URL and ensure proxy settings are configured correctly |
| Results inconsistent or incomplete | AI model limitations with complex queries | Switch to premium models (GPT-5, Claude Sonnet 4.5 etc.) for better reasoning |
| Element creation in wrong location | Always mention exact location where the objects should be created (include parent package name or guid in propmts) |
| Docker image pull fails | Ensure Artifactory access and authentication token are properly configured |
| Unkown Error | Check `webea_mcp_server.log` for detailed error messages |
| Unexpected or missing data from tools | Generic query too broad or filter mismatch - Refine prompt with specific element type, package, or diagram name |
| Results inconsistent or incomplete | AI model limitations with complex queries - Switch to premium models (GPT-5, Claude Sonnet 4.5 etc.) for better reasoning |

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
- [OSLC Architecture Management](https://sparxsystems.fr/enterprise_architect_user_guide/17.0/the_model_repository/oslc_am_top.html)
