# DRIVE Companion MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server enabling seamless integration with [DRIVE Companion](https://inside-docupedia.bosch.com/confluence2/x/QmgIIg) retrieval-augmented generation (RAG) models and chat-based interactions.


## Overview

The [DRIVE Companion](https://inside-docupedia.bosch.com/confluence2/x/QmgIIg) MCP Server enables AI assistants and clients to interact with DRIVE Companion models via a unified MCP interface. It supports chat-based interactions and model listing.

### Limitations

- File and collection upload operations are not yet supported.
- The accuracy and quality of results depend on the underlying model and configuration.


## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../../README.md#access-to-pmt-artifactory-repository))
- Access to a DRIVE Companion chat interface and a valid API key.


### MCP Client Integration

1. Integrate the MCP server with your VSCode GitHub Copilot by adding a configuration file `.vscode/mcp.json`. Use the provided [`mcp.json`](mcp.json) as a reference and replace all placeholders.
2. Start the Docker or Python version MCP server after adding `.vscode/mcp.json`.
3. See [`../../README.md`](../../README.md) for more on [`Running MCP Servers using uv/python`](../../README.md#running-mcp-servers-for-development)


### Configuration

Set the following environment variables (in `mcp.json`) for the required MCP server `drivecompanion-docker-mcp-server` or `drivecompanion-python-mcp-server`:

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `DRIVECOMPANION_URL` | DRIVE Companion backend base URL | `https://d3f9sv9ory62r0.cloudfront.net/` |
| `DRIVECOMPANION_API_KEY` | DRIVE Companion HTTP API key | `xxxxxxx` |
| `TRANSPORT` | MCP transport protocol | `stdio` (default), `http`, `sse` |
| `HOST` | Server host address | `127.0.0.1` (default) |
| `HOST_PORT` | Server port | `8000` (default) |

**Note:** API tokens and sensitive credentials should be securely provided via input prompts, not stored in configuration files.


### Usage Examples

Once connected to VSCode GitHub Copilot chat or an MCP-compatible client, you can interact with DRIVE Companion using natural language. Try these examples:

- "List all available models in DRIVE Companion chatbot"
- "Ask XC DRIVE Companion: Provide a comprehensive list of the requested ADAS features and functions for Toyota project 19PFver3KAI together with the sources/links of the information."

The AI assistant will translate these natural language requests into actual DRIVE Companion API requests and execute them against your DRIVE Companion backend.


### Features

The server provides the following MCP tools for DRIVE Companion:
- `list_models` - List all available models in DRIVE Companion chat interface
- `query_model` - Chat with a given model name as input.


### Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing environment variables | Ensure all required variables are set in your environment or `mcp.json` |
| API errors | Check the DRIVE Companion backend URL and API key |
| Connection issues | Verify network connectivity and backend availability |
| Unexpected or missing data | Refine your prompt or check DRIVE Companion API limitations |
| Chat is slow or takes long | Prompt may be complex; try simplifying your prompt |


## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [DRIVE Companion Doc](https://inside-docupedia.bosch.com/confluence2/x/QmgIIg)
- [DRIVE Companion Chat](https://d3f9sv9ory62r0.cloudfront.net/)
