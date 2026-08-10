# DNG MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with IBM Doors Next Generation (DNG) Requirements Management.

## Overview

The DNG MCP Server provides comprehensive integration with IBM's Doors Next Generation (DNG) system, formerly known as Dynamic Requirements Gateway. It exposes a rich set of tools for managing requirements, modules, views, collections, baselines, and artifacts directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the DNG Reportable REST API.

### Limitations

- Some bulk operations on large datasets may be paginated (default page size of 100 artifacts)
- Depending on the LLM models, accuracy might differ
- History operations can be resource-intensive for large datasets
- `update requirement` mcp tool doesn't support modifications of custom attributes yet

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to IBM Doors Next Generation instance (e.g., https://server:port/rm)
- Valid DNG credentials (username and password)
- DNG Project name or URI

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding `.vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Features

The server provides the following MCP tools for comprehensive DNG requirements management:

- **Schema & Metadata**:
  - `get_schema` - Get the generated schema for a service context

- **Project Management**:
  - `list_all_projects` - List all accessible projects with names and URIs
  - `get_project_info` - Get detailed information about a project
  - `get_project_modules` - Get all modules in a project
  - `get_project_collections` - Get all collections in a project
  - `get_project_snapshots` - Get all snapshots (baselines) in a project

- **Resource Retrieval**:
  - `get_resources_by_project` - Get all resources in a project (paginated)
  - `get_resources_by_ids` - Get base resource information by resource URIs

- **Consolidated Filtering**:
  - `get_resources_filtered` - Get resources with various filtering options (view, type, attributes, module)

- **Collection Operations**:
  - `get_collection_uri` - Get resource revisions in a collection

- **Text Format Operations**:
  - `get_text_with_embed_titles` - Get text format with embedded artifact titles
  - `get_text_with_expanded_embeds` - Get text with expanded embedded artifacts

- **Modification Tracking (ETL)**:
  - `get_modified_since` - Get resources modified since timestamp

- **History Operations**:
  - `get_artifact_history` - Get complete artifact history
  - `get_artifact_history_by_timerange` - Get history filtered by time range

- **User Activity Tracking**:
  - `get_user_activity` - Get artifacts created/modified/deleted by user

- **Advanced Search & Query**:
  - `search_resources_advanced` - Advanced search with multiple filter combinations
  - `oslc_query_requirements` - Execute OSLC queries with flexible filtering, selection, and sorting

- **Folder Management**:
  - `create_folder` - Create a new folder in DNG
  - `get_folders_by_project` - Get all folders in a project
  - `get_folder_contents` - Get artifacts contained in a folder
  - `move_artifact_to_folder` - Move an artifact to a different folder

- **Update Operations**:
  - `create_requirement` - Create a new requirement in a project
  - `update_requirement` - Update an existing requirement (title, description, folder, attributes)

- **Pagination**:
  - `get_next_page` - Fetch next page of paginated results (Note: Use next page URLs from response pagination links)

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `DNG_SERVER` | Base URL of the DNG server | `https://rb-alm-13-q.de.bosch.com/` |
| `DNG_USERNAME` | Username for authentication | `your-username` |
| `DNG_PASSWORD` | Password for authentication | `xxxxx` |
| `DNG_VERIFY_SSL` | Enable/disable SSL verification | `true` or `false` |
| `TRANSPORT` | Transport type (optional) | `stdio` (default), `http`, `streamable-http`, `sse` |
| `HOST` | Host for non-stdio transport (optional) | `127.0.0.1` (default), `0.0.0.0`, `localhost` |
| `HOST_PORT` | Port for non-stdio transport (optional) | `8000` |

**Note:** When using the provided `mcp.json` configuration, you'll be prompted for credentials and configuration at runtime.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with DNG using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "List all projects in DNG"
- "Get all requirements from project 'MyProject'"
- "Show me requirements of type 'Feature' in project URI https://server/rm/process/project-areas/_abc123"
- "Get requirements modified since 2024-01-01T00:00:00.000Z"
- "Show me the history of requirement with URI https://server/rm/resources/_xyz789"
- "Get all requirements in module with URI https://server/rm/modules/_mod456"
- "Search for users with name 'John'"
- "Show me what user 'jdoe' created yesterday"
- "Get requirements filtered by view 'Critical Features'"
- "List all baselines for project URI https://server/rm/process/project-areas/_abc123"
- "Create a new requirement titled 'User Authentication' in project URI https://server/rm/process/project-areas/_abc123"
- "Create a requirement 'Data Encryption' with description 'All data must be encrypted' in project URI https://server/rm/process/project-areas/_abc123"

The AI assistant will translate these natural language requests into actual API calls and execute them in DNG.

### Troubleshooting

#### Connection Issues
- **"Failed to connect to DNG"**: Verify `DNG_SERVER`, `DNG_USERNAME`, and `DNG_PASSWORD` are correct
- **SSL certificate errors**: Set `DNG_VERIFY_SSL=false` if using self-signed certificates (not recommended for production)
- **Authentication failures**: Check if credentials are valid and not expired
- **Permission errors**: Ensure user has necessary project access permissions

#### Common Errors
- **"Resource not found"**: Verify resource URI format - should be full URI (e.g., https://server/rm/resources/_abc123)
- **"Project not found"**: Use `list_all_projects` to see available projects and their URIs
- **Network timeouts**: Check proxy settings if running in corporate environment - may need to configure `HTTP_PROXY` and `HTTPS_PROXY`
- **"Invalid URL"**: Ensure `DNG_SERVER` includes protocol (https://) and correct hostname/port
- **"Permission denied"**: User may not have read permissions - check user roles in DNG
- **Pagination issues**: Large result sets are paginated - use `get_next_page` with the next page URL from response

#### Resource URI Issues
- **"Cannot find resource"**: Make sure you're using full resource URIs, not just IDs
- **"Invalid resource format"**: Resource URIs should follow pattern: `https://server/rm/resources/_resourceId`
- **Project URIs**: Project URIs follow pattern: `https://server/rm/process/project-areas/_projectId`
- **Module URIs**: Module URIs follow pattern: `https://server/rm/modules/_moduleId`

#### XML Parsing
- **"XML parsing error"**: Use `parse_artifacts_summary` or `extract_artifact_links` to extract data from XML responses
- **Empty results**: Some queries may return empty results if filters don't match any resources
- **Namespace issues**: The server handles all XML namespaces automatically

## Further Information

- [IBM Doors Next Generation Documentation](https://www.ibm.com/docs/en/engineering-lifecycle-management-suite/doors-next)
- [DNG Reportable REST API Guide](https://jazz.net/wiki/bin/view/Main/DNGReportableRestAPI)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
