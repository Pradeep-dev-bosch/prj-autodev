# Official MCP Server for Enterprise Architect

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Enterprise Architect, officially provided by Sparx Systems.

## Overview

The [Official MCP Server for Enterprise Architect](https://www.sparxsystems.jp/en/MCP/) enables AI assistants to interact with EA repositories using the officially supported mcp server from Sparx Systems. This server provides comprehensive access to EA models, allowing you to query, create, and manipulate model elements, packages, diagrams, and connectors directly from your AI-enabled development environment.<br>
**For the most up-to-date installers, changelog, prerequisites, and detailed usage notes, refer to the [official release page](https://www.sparxsystems.jp/en/MCP/) (information there supersedes this README).**

### Limitations

- Only a limited subset of Enterprise Architect object properties (elements, diagrams, packages, connectors) is exposed; many advanced or rarely used attributes are not yet returned.
- Enterprise Architect must be running with a project opened before starting the Official MCP Server; it does not launch EA automatically.
- If multiple EA instances are open, the server attaches to the first project loaded. Close additional instances to avoid ambiguity.
- Runs only in Windows environment; containerized or headless execution is not supported.
- Installer requires .NET Desktop Runtime 9.0.5+; if missing, the MSI may appear to complete without installing files.

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Operating System: Windows 10/11 (64-bit)
- Runtime: .NET Desktop Runtime 9.0.5 or later, .NET Framework 4.7.2 or later
- Enterprise Architect: Version tested with EA 17.1 build 1713 (64-bit)

### MCP Client Integration

Refer to the [Official Sparx Systems MCP page](https://www.sparxsystems.jp/en/MCP/ ) for the latest installer.

1. After installing the mcp server, the easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference.

2. Open Enterprise Architect application and open the desired resource or package.

3. After adding the `.vscode/mcp.json` configuration file, start the MCP server. It is now ready to use. See the [parent README](../../README.md) for startup instructions.

Note: Always re-check the official page for new releases.


### Troubleshooting

| Issue | Solution |
|-------|----------|
| Installer finishes without installing files | Ensure .NET Desktop Runtime 9.0.5 or later is installed |
| MCP server fails to start | Verify EA is running and the executable path in mcp.json is correct |
| Multiple EA instances warning | Close additional EA instances; MCP connects to the first opened project |
| Connection errors | Ensure EA application is open before starting the MCP server |
| Unexpected or missing data from tools | Generic query too broad or filter mismatch - Refine prompt with specific element type, package, or diagram name |
| Results inconsistent or incomplete | AI model limitations with complex queries - Switch to premium models (GPT-5, Claude Sonnet 4.5 etc.) for better reasoning |

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Official Sparx Systems MCP page](https://www.sparxsystems.jp/en/MCP/)

