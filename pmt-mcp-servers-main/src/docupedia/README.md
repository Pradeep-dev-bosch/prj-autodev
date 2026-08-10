# Docupedia MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Bosch Confluence (Docupedia).

## Overview

The Docupedia MCP Server provides comprehensive integration with Bosch's internal Confluence instance. It exposes a rich set of tools for searching, finding, and reading content from Docupedia directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the Confluence REST API.

### Limitations

- Uploading images to the docupedia page is not possible yet at the moment
- We can only work with one of the docupedia instances at once (not both docupedia 1 and 2 at the same time)
- Depending on the LLM models, accuracy might differ

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to Bosch Confluence [Docupedia-1](https://inside-docupedia.bosch.com/confluence), [Docupedia-2](https://inside-docupedia.bosch.com/confluence2)
- Valid Confluence PAT token

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with Docupedia using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Find the latest SW release information for RA7"
- "Create a docupedia page named <page_name> in the space <space_name>"
- "Add this label <label_name> to the <page_name>"
- "Add a comment <comment> to the page <page_name>"

The AI assistant will translate these natural language requests into actual API requests and execute them in the docupedia.

### Features

The server provides the following MCP tools for comprehensive Docupedia management:

- **Page Management**:
  - `find_page_id` - Find a Confluence page ID by space and title
  - `get_page_content` - Retrieve the full content of a Confluence page
  - `create_page` - Create a new Confluence page with optional parent
  - `update_page_content` - Update page content (append, prepend, or replace)
  - `delete_page` - Delete a Confluence page
  - `move_page` - Move a page to a different parent or space
  - `get_child_pages` - Get all child pages of a page
  - `get_page_history` - Get version history of a page

- **Search & Discovery**:
  - `search_confluence` - Search for pages in Confluence with optional space filtering
  - `search_with_excerpts` - Search for pages and return content excerpts with summaries

- **Collaboration & Metadata**:
  - `add_comment_to_page` - Add a comment to a page
  - `get_page_comments` - Get comments from a page
  - `add_labels_to_page` - Add labels/tags to a page
  - `get_page_labels` - Get all labels from a page
  - `watch_page` - Watch a page for updates
  - `unwatch_page` - Stop watching a page

- **Space Management**:
  - `list_spaces` - List available Confluence spaces
  - `get_space_info` - Get detailed information about a space

- **Attachments**:
  - `list_page_attachments` - List all attachments on a page
  - `upload_attachment` - Upload a file attachment to a page

- **Content Generation**:
  - `generate_table_html` - Generate Confluence table HTML from data
  - `generate_macro_html` - Generate Confluence macro HTML (info, code, status, etc.)

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `CONFLUENCE_BASE_URL` | Base URL for docupedia, VSCode will prompt to select the choice | `https://inside-docupedia.bosch.com/confluence` |
| `CONFLUENCE_PAT_TOKEN` | Token for docupedia authentication, VSCode will open a prompt for the token | `xxxxx` |
| `TRANSPORT` | Transport protocol type (optional) | `stdio` (default), `sse`, `streamable-http` |
| `HOST` | Server host address when using non-stdio transport (optional) | `127.0.0.1` (default) |
| `HOST_PORT` | Server port when using non-stdio transport (optional) | `8000` (default) |

**Note:** When using the provided `mcp.json` configuration, you don't need to manually set these environment variables. The base URL and token will be prompted securely at runtime. The transport defaults to `stdio` which is suitable for most MCP client integrations.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with your Docupedia using natural language:

**Example interactions:**

- "Find the latest SW release information for RA7"
- "Create a docupedia page named <page_name> in the space <space_name>"
- "Add this label <label_name> to the <page_name>"
- "Add a comment <comment> to the page <page_name>"

The AI assistant will translate these natural language requests into actual API requests and execute them in the docupedia.

### Troubleshooting

#### Connection Issues
- **"Failed to connect to Confluence"**: Verify `CONFLUENCE_BASE_URL` and `CONFLUENCE_PAT_TOKEN` are correct
- **Authentication failures**: Check if PAT token is valid and not expired
- **Permission errors**: Ensure token has necessary space and page permissions
- **Proxy issues**: If behind corporate proxy, ensure proxy settings in `mcp.json` are correct

#### Common Errors
- **"Page not found"**: Verify page title and space key are correct - use `search_confluence` to find pages
- **"Space not found"**: Check space key exists - use `list_spaces` to see available spaces
- **"CONFLUENCE_PAT_TOKEN environment variable is required"**: Ensure the token is provided when prompted during server startup
- **Network timeouts**: Check proxy settings if running in corporate environment - may need to adjust proxy in `mcp.json`
- **"Invalid URL"**: Ensure `CONFLUENCE_BASE_URL` includes the protocol (https://) and correct hostname
- **"Permission denied"**: Token may not have write permissions - check token scope in Confluence settings
- **"Page title already exists"**: When creating pages, ensure title is unique in the space or use different title
- **Attachment upload failures**: Verify file size is within Confluence limits and file format is allowed

## Further Information

- [Confluence Documentation](https://confluence.atlassian.com/conf92/get-started-1477575467.html)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
