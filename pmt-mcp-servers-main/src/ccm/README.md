# CCM MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with IBM Rational Team Concert (RTC) Change and Configuration Management (CCM).

## Overview

The CCM MCP Server provides comprehensive integration with IBM's Rational Team Concert CCM system. It exposes a rich set of tools for managing work items, project areas, team areas, queries, and relationships directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the `rtcclient` Python library with custom enhancements for better compatibility.

### Limitations

- The standard rtcclient Python library is not working as expected for certain operations, so custom implementations have been added
- Depending on the LLM models, accuracy might differ
- Complex work item relationships may need multiple queries
- Update/Write operations require proper permissions in RTC

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to IBM RTC/CCM instance
- Valid RTC credentials (username and password)
- RTC Project Area name

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Features

The server provides the following MCP tools for comprehensive RTC CCM management:

- **Project Area Management**:
  - `list_projects` - List all available project areas
  - `get_project_by_name` - Get detailed information about a specific project area

- **Work Item Retrieval**:
  - `get_workitem_by_id` - Get a work item by ID
  - `get_workitems` - Get all work items in a project area
  - `get_workitem_children` - Get all child work items of a specific work item
  - `get_workitem_parent` - Get the parent work item
  - `get_workitem_comments` - Get all comments for a work item

- **Query & Search**:
  - `query_workitems` - Query work items using OSLC query syntax
  - `get_saved_queries` - Get all saved queries in a project area
  - `run_saved_query` - Execute a saved query by URL

- **Work Item Creation**:
  - `create_workitem` - Create a new work item (task, defect, story, etc.) with optional fields

- **Work Item Updates** (Limited Support):
  - `update_workitem_field` - Update a single field in a work item
  - `update_workitem_multiple_fields` - Update multiple fields at once
  - `update_workitem_state` - Update the state of a work item
  
  *Note: Work item update functionality has limited support due to rtcclient library constraints. These tools may require additional wrapper implementation.*

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `RTC_SERVER_URL` or `ELM_SERVER_BASE_URL` | Base URL for RTC/CCM server | `https://rtc-server.example.com/ccm` |
| `RTC_USERNAME` or `ELM_USERNAME` | Username for RTC authentication | `user@example.com` |
| `RTC_PASSWORD` or `ELM_PASSWORD` | Password for RTC authentication | `xxxxx` |
| `ELM_CCM_APPSTRING` | CCM application string (optional) | `ccm` (default) |
| `RTC_VERIFY_SSL` | Enable/disable SSL verification | `false` (for development) |
| `TRANSPORT` | Transport type | `stdio` (default) or `sse` |
| `HOST` | Host for non-stdio transport | `127.0.0.1` |
| `HOST_PORT` | Port for non-stdio transport | `8001` |

**Note:** When using the provided `mcp.json` configuration, you'll be prompted for credentials and configuration at runtime.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with RTC CCM using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "List all project areas in RTC"
- "Get information about project 'My Project'"
- "Show me work item 12345"
- "Get all work items in project 'My Project'"
- "Create a new defect titled 'Login page error' in project 'My Project'"
- "Query all high-priority tasks: dcterms:type='task' and oslc_cm:priority='High'"
- "Get all children of work item 100"
- "Get the parent of work item 200"
- "Get all comments for work item 300"
- "List all saved queries in project 'My Project'"
- "Run saved query with URL 'https://server/oslc/queries/xyz'"

The AI assistant will translate these natural language requests into actual API requests and execute them in RTC.

### OSLC Query Syntax

The server supports OSLC query syntax for advanced filtering:

```
# Exact match
dcterms:title="Bug in login"

# Type and state filtering
dcterms:type="task" and rtc_cm:state="new"

# Owner filtering
rtc_cm:ownedBy="user@example.com"

# Multiple conditions
dcterms:type="defect" and rtc_cm:state!="closed" and oslc_cm:priority="High"
```

**Common Field Names:**

| Display Name | OSLC Property | Example Value |
|--------------|---------------|---------------|
| Title | `dcterms:title` | "Fix login bug" |
| Description | `dcterms:description` | "Detailed description" |
| Type | `dcterms:type` | "task", "defect", "story" |
| State | `rtc_cm:state` | "new", "in-progress", "closed" |
| Owner | `rtc_cm:ownedBy` | "user@example.com" |
| Priority | `oslc_cm:priority` | "High", "Medium", "Low" |
| Severity | `oslc_cm:severity` | "Critical", "Major", "Minor" |
| Filed Against | `rtc_cm:filedAgainst` | Category/Component |
| Planned For | `rtc_cm:plannedFor` | Sprint/Iteration |

### Troubleshooting

#### Connection Issues
- **"Failed to get project areas"**: Verify `RTC_SERVER_URL` includes the `/ccm` endpoint
- **Authentication failures**: Check if credentials are valid and not expired. The server uses Basic Authentication.
- **401 Unauthorized**: Verify Basic Auth is enabled on the CCM server
- **403 Forbidden**: Verify if there is required permissions for the resources/work item on the CCM server
- **SSL certificate errors**: Set `RTC_VERIFY_SSL=false` for development or configure proper certificates

#### Common Errors
- **"Project 'XXX' not found"**: Check project name - use `list_projects` to see available projects
- **"Work item 'XXX' not found"**: Verify work item ID is correct and you have access permissions
- **Network timeouts**: Check proxy settings if running in corporate environment
- **"Invalid query syntax"**: Ensure OSLC query uses proper namespaces (e.g., `dcterms:`, `rtc_cm:`)
- **"Missing required connection parameters"**: Set all required environment variables

#### Query Syntax Issues
- **Wrong**: `type=defect` → **Correct**: `dcterms:type='defect'`
- **Wrong**: `priority=High AND state=open` → **Correct**: `oslc_cm:priority='High' and rtc_cm:state='open'`
- Use single quotes for values in queries
- Use lowercase `and`, `or` operators

#### Permission Errors
- User may not have write permissions - check user roles in RTC
- Some operations require specific project area permissions
- Verify access to project areas and work items

## Further Information

- [rtcclient Documentation](https://rtcclient.readthedocs.io/en/latest/)
- [OSLC Core Specification](https://open-services.net/specifications/oslc-core/)
- [OSLC Query Syntax](https://open-services.net/specifications/oslc-query/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
