# Jira MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Jira.

## Overview

The Jira MCP Server provides comprehensive integration with Jira instances. It exposes a rich set of tools for querying, creating, and managing Jira issues directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and the `atlassian-python-api` client library.

### Limitations

- Some advanced Jira features may not be available
- Bulk operations on multiple issues are limited
- Depending on the LLM models, accuracy might differ. Premium models like GPT-5 or Claude Sonnet 4.5 are recommended for better performance and results with complex Jira operations

## Getting Started

### Prerequisites

- GitHub Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ) (for Windows users)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-docker-artifactory-repository))
- Access to Jira instance (default: Track & Release)
- Valid Jira personal access token

### Jira Personal Access Token Setup

1. **Generate Jira Personal Access Token**
   - Log in to your Jira instance
   - Go to Account Settings → Security → Create and manage API tokens
   - Click "Create API token"
   - Give it a descriptive label (e.g., "MCP Server Access")
   - Copy the generated token immediately (it won't be shown again)

2. **Important Notes:**
   - ✅ Token should have minimal required permissions for your use case
   - ✅ Never commit tokens to version control
   - ✅ Use different tokens for different MCP servers/environments
   - ✅ Rotate tokens periodically following security best practices
   - ✅ Tokens are securely taken as input and not stored in configuration files

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding `.vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `TRACKER_URL` | Jira instance URL | ✅ Yes | `https://jira.example.com` |
| `JIRA_TOKEN` | Personal access token | ✅ Yes | `ATBBt3...xYzABC` |
| `TRANSPORT` | MCP transport protocol | No | `stdio` (default), `http`, `sse` |
| `HOST` | Server host address (if not using stdio) | No | `127.0.0.1` (default) |
| `HOST_PORT` | Server port (if not using stdio) | No | `8000` (default) |

**Note:** When using the provided `mcp.json` configuration, set the environment variables as shown in the example configuration file.

#### Configuration Examples

**Example 1: Standard Configuration**
```json
{
  "TRACKER_URL": "https://tracker.example.com",
  "JIRA_TOKEN": "ATBBt3...xYzABC"
}
```

**Example 2: Custom Instance with Transport Options**
```json
{
  "TRACKER_URL": "https://jira.bosch.com/YourProject",
  "JIRA_TOKEN": "ATBBt3...xYzABC",
  "TRANSPORT": "stdio"
}
```

### Usage Examples

Once connected to an MCP-compatible client, you can interact with Jira using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Get all projects from Jira"
- "Create a new issue in project X"
- "List all issues assigned to me"
- "Add a comment to issue PROJ-123"
- "Execute a JQL query to find all open bugs"
- "Get the change history for issue PROJ-456"
- "Show me the first 100 issues from project X" (pagination)
- "Get the next 50 issues" (pagination with natural language)
- "Fetch issues 101-150 from the project" (custom pagination)

The AI assistant will translate these natural language requests into actual API requests and execute them in Jira.

**Pagination Support**: The `jira_request` tool supports pagination for large result sets:
- Fetch up to 100 items per request
- Navigate through results using natural language commands
- Automatically handles pagination metadata (total count, position tracking)

### Features

The server provides comprehensive Jira integration capabilities with 67 specialized MCP tools covering:

- Project information retrieval and management
- Issue creation, cloning, and management
- Comments, labels, priorities, and properties handling
- Workflow transitions and status management
- Time tracking and worklog management
- Issue relationships and epic linking
- Web links management
- Collaboration links and Doors requirements traceability
- Voting and watching functionality
- Attachments handling
- Filters and dashboards management
- Change history tracking
- Sprint and agile board management
- Bulk operations for efficient batch processing

The following MCP tools are available for comprehensive Jira management:

- **Query & Search**:
  - `jira_request` - Execute JQL queries with pagination support (start_at, max_results)
  - `search_users` - Find users by name or username fragment

- **Project Management**:
  - `get_all_projects` - List all accessible projects
  - `get_project` - Get details of a specific project
  - `get_project_components` - List components for a project
  - `get_project_versions` - List versions for a project
  - `get_project_roles` - List roles for a project

- **Issue Management**:
  - `create_issue` - Create new issues with minimal required fields
  - `clone_issue` - Clone an existing issue with optional prefix
  - `get_issue_subtasks` - List subtasks for an issue
  - `modify_issue_type` - Change issue type or list available types
  - `assign_issue` - Assign issues to users
  - `set_issue_summary` - Update issue titles
  - `set_issue_description` / `get_issue_description` - Manage descriptions
  - `add_issue_components` - Add components to existing issues
  - `set_issue_acceptance_criteria` - Set or update acceptance criteria for issues
  - `get_issue_acceptance_criteria` - Retrieve acceptance criteria from issues

- **Comments**:
  - `add_issue_comment` - Add new comments
  - `update_issue_comment` - Update existing comment text
  - `delete_issue_comment` - Remove comments
  - `get_issue_comments` - List all comments
  - `get_issue_pinned_comments` - Retrieve pinned comments
  - `bulk_add_comments` - Add comments to multiple issues at once

- **Labels & Properties**:
  - `modify_issue_labels` - Add, remove, or replace labels
  - `issue_priority` - List priorities, get/set issue priority
  - `set_issue_reporter` - Change issue reporter
  - `set_due_date` - Set issue due dates
  - `issue_editable_fields` - Check which fields can be edited

- **Workflow & Status Management**:
  - `transition_issue` - List available transitions or move issues between states

- **Time Tracking & Work Logging**:
  - `add_worklog_entry` - Log time spent on issues
  - `update_time_tracking` - Set original/remaining estimates

- **Issue Relationships**:
  - `link_issues` / `unlink_issues` - Create/remove links between issues
  - `link_epic_to_issue` - Link issues to epics

- **Web Links**:
  - `add_web_link_to_issue` - Add web links to issues
  - `get_issue_web_links` - Retrieve all web links from an issue
  - `remove_web_link` - Remove web links from issues

- **Collaboration Links & Requirements Traceability**:
  - `create_collaboration_link` - Link issues to Doors requirements or external resources
  - `get_doors_requirements` - Get all Doors requirement links for an issue
  - `bulk_add_collaboration_links` - Add collaboration links to multiple issues at once
  - `update_collaboration_link` - Update existing collaboration links
  - `get_collaboration_link_types` - Discover collaboration link types in use
  - `generate_requirements_traceability_matrix` - Create traceability matrices with coverage analysis
  - `list_issues_with_doors_requirements` - List all issues with Doors requirement links
  - `analyze_custom_fields_for_requirements` - Analyze where requirements are stored

- **Bulk Operations**:
  - `bulk_transition_issues` - Transition multiple issues at once with optional comments

- **Voting & Watching**:
  - `vote_for_issue` / `remove_vote` - Vote on issues
  - `add_watcher` / `remove_watcher` - Manage watchers
  - `get_issue_votes` / `get_issue_watchers` - View votes and watchers

- **Attachments**:
  - `get_issue_attachments` - List all attachments for an issue
  - `upload_attachment` - Add new attachments to issues
  - `download_attachment` - Download attachment content
  - `get_attachment_metadata` - View attachment information

- **Filters & Dashboards**:
  - `get_user_filters` - List saved filters
  - `create_filter` - Create new filters
  - `get_filter_by_id` - Get filter details
  - `update_filter` - Modify existing filters
  - `delete_filter` - Remove filters
  - `get_dashboards` - List all dashboards
  - `get_dashboard_by_id` - Get dashboard details

- **History & Tracking**:
  - `get_issue_history` - Get complete issue history
  - `get_issue_changelog` - View issue change log

- **Sprint & Agile Management**:
  - `get_board_sprints` - Get all sprints for a specific board
  - `get_sprint_issues` - Get issues for a specific sprint with optional grouping by assignee

- **Utilities**:
  - `get_issue_link` - Generate direct URLs to issues

### Troubleshooting

#### Authentication Issues
- **Invalid Credentials:** Verify `JIRA_TOKEN` is correct and not expired
- **Token Expired:** Generate new token and update configuration
- **Insufficient Permissions:** Ensure token has required Jira project permissions
- **Permission Denied:** 403 Forbidden - verify user has access to requested projects/issues

#### Connection Issues
- **Cannot Connect:** Verify `TRACKER_URL` is correct and accessible
- **"Failed to connect to Jira"**: Check `TRACKER_URL` format includes https:// protocol
- **Network Timeout:** Check proxy settings if running in corporate environment
- **Firewall Blocking:** Check network firewall rules and corporate proxy settings

#### Issue Operations
- **"Field not editable"**: Use `issue_editable_fields()` to check which fields can be modified
- **"Transition not found"**: Use `transition_issue()` without transition parameter to list available workflow transitions
- **"Issue not found"**: Verify issue key exists and you have view permissions
- **"Project not found"**: Verify project key - use `get_all_projects` to list accessible projects

#### Query Issues
- **"Invalid JQL"**: Validate JQL syntax in Jira's web interface first
- **Empty Results:** Check if filters/permissions are limiting visibility
- **Pagination Issues:** Use `start_at` and `max_results` parameters correctly

#### User Management
- **"User not found"**: Use `search_users()` to find correct username or accountId
- **Cannot Assign Issue:** Verify user has permission to be assigned issues in that project
- **Watcher/Voter Errors:** Ensure user exists and has appropriate permissions

#### Common Errors
- **Rate Limiting:** Jira API throttling - reduce request frequency
- **Attachment Upload Failed:** Check file size limits and permissions
- **Link Creation Failed:** Verify both issues exist and link type is valid
- **Bulk Operation Partial Failure:** Check individual error messages in response
- **Custom Field Not Found:** Use `issue_editable_fields()` to discover available fields
- **Network Proxy Issues:** Set HTTP_PROXY and HTTPS_PROXY environment variables if needed

## Further Information

- [Jira REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [JQL (Jira Query Language)](https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Atlassian Python API](https://github.com/atlassian-api/atlassian-python-api)
