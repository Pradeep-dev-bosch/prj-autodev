# COM EA MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides integration with Enterprise Architect desktop applications using the COM interface.

## Overview

The COM EA MCP Server enables AI assistants to interact with Enterprise Architect through the COM automation interface. This server provides comprehensive access to EA models, allowing you to query, create, and manipulate model elements, packages, diagrams, and connectors directly from your AI-enabled development environment.

### Limitations

1. The Enterprise Architect application must be opened manually before using the COM MCP Server.
2. If multiple Enterprise Architect instances are running, close all via Task Manager before reopening a project.
3. The COM interface cannot be containerized; use the Python MCP server. A standalone executable is planned for the future but not available yet.
4. MCP server must be started from windows environment.
5. Destructive SQL operations restricted: DELETE, DROP, TRUNCATE, and ALTER are blocked in query_repository() for safety. Use EA GUI for these operations.

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Operating System: Windows 10/11 (64-bit)
- Enterprise Architect: Application installed and licensed

### MCP Client Integration

1. The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference.

2. Check out the [`../../README.md`](../../README.md) to find out about [`Running MCP Servers using uv/python`](../../README.md#running-mcp-servers-for-development)

### Configuration

1. Open Enterprise Architect application and open the desired resource or package.

2. In `.vscode/mcp.json` start the server and its ready to use.

### Usage Examples

Once connected to VSCode GitHub Copilot chat or an MCP-compatible client, you can interact with your EA models using natural language.<br>Try these examples in your VSCode GitHub Copilot chat:  (Use premium models such as GPT-5, Claude Sonnet 4.5 etc. in to get best results)

- "What is the root packages in the current EA model"
- "Get information about the currently selected element"
- "Explain me current open diagram"
- "Create a new class called 'MyComponent' in the current package"
- "Find all diagrams that contain element 'SystemBoundary'"
- "Create a dependency connector between ElementA and ElementB"
- "Create a package and create requirement diagram in it with req1 and req2.. requirement elements"

The AI assistant will translate these natural language requests into appropriate COM API calls and execute them against your opened Enterprise Architect model.

### Features

The server provides the following MCP tools for comprehensive Enterprise Architect management:

- **Element Management**:
  - `create_element` - Creates a new element in the repository
  - `update_element` - Updates the properties of an existing element
  - `get_element_information` - Retrieves detailed information about an element
  - `get_current_element` - Retrieves detailed information for the currently selected element
  - `set_element_property` - Sets a specific property for an element

- **Package Management**:
  - `get_root_packages` - Fetches the root packages in the repository
  - `get_package_information` - Retrieves basic information about a specific package
  - `find_packages_by_name` - Finds packages by their name
  - `get_current_package` - Retrieves information for the currently selected package
  - `create_package` - Creates a new package under a specified parent package

- **Diagram Management**:
  - `get_diagram_information` - Retrieves detailed information about a diagram
  - `get_diagram_image` - Saves a diagram's image to a file and returns the file path
  - `get_opened_diagrams` - Lists all diagrams currently open in the EA user interface
  - `get_current_diagram` - Retrieves detailed information for the currently active diagram
  - `create_diagram` - Creates a new diagram of a specific type within a package
  - `open_diagram` - Opens a specified diagram in the EA user interface
  - `layout_diagram` - Applies an automatic layout to a specified diagram

- **Connector Management**:
  - `create_connector` - Creates a connector of a specific type to link two elements
  - `place_element_on_diagram` - Places an existing element onto a specific diagram
  - `select_element_in_diagram` - Highlights a specific element within a specific diagram
  - `find_in_diagrams` - Finds all diagrams in which the specified element is used

- **Query & Analysis**:
  - `query_resources` - Executes a read-only SQL query directly against the EA repository database

### Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP server fails to start | Ensure Enterprise Architect is running and a project/model is open |
| Multiple EA instances error | Close all EA instances via Task Manager and restart with only one instance |
| Connection errors | Check `ea_com_mcp_server.log` file for detailed error messages |
| COM interface not found | Verify EA is properly installed and licensed |
| Unexpected or missing data from tools | Generic query too broad or filter mismatch - Refine prompt with specific element type, package, or diagram name |
| Results inconsistent or incomplete | AI model limitations with complex queries - Switch to premium models (GPT-5, Claude Sonnet 4.5 etc.) for better reasoning |

Important: Open Enterprise Architect first with the desired project/package, then start the COM EA MCP server via `.vscode/mcp.json` to ensure the COM automation can connect.

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
