# JFrog Artifactory MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with JFrog Artifactory.

## Overview

The JFrog Artifactory MCP Server provides comprehensive integration with JFrog Artifactory instances. It exposes a rich set of tools for searching, retrieving, and managing artifacts and repositories directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via prompting the user in realtime and storing it in environment variables.

The server is built with the `FastMCP` framework and uses the JFrog Artifactory REST API.

### Limitations

- Repository creation and deletion are not supported
- Build integration and CI/CD pipeline features are not available
- Depending on the LLM models, accuracy might differ

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to JFrog Artifactory
- Valid JFrog Artifactory URL and personal access token

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with JFrog Artifactory using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Find the package with name 'ems_base_service' in the artifactory"
- "List all available repositories in Artifactory"
- "Download the latest version of package <package-name> from <repo-name>"
- "Upload the file my-artifact.json to the <repo-name>"
- "Copy the file <artifact-name> from <source-repo-path> to <target-repo-path>"

The AI assistant will translate these natural language requests into actual API requests and execute them in JFrog Artifactory.

### Features

The server provides the following MCP tools for comprehensive JFrog Artifactory management:

- **Search & Discovery**:
  - `aql_search` - Search packages using Artifactory Query Language (PRIMARY TOOL for package searches)
  - `pattern_search` - Search by exact path patterns for repository structure exploration
  - `artifact_search` - Search for artifacts by exact file names

- **Repository Management**:
  - `get_repositories` - List all accessible repositories with type summaries
  - `get_repository_info` - Get detailed configuration of a specific repository
  - `get_retention_policy` - Check retention policy settings for repositories

- **Browsing & Navigation**:
  - `get_folder_info` - Browse repository folders to explore package structure
  - `get_file_info` - Get metadata for specific files (checksums, timestamps, properties)

- **File Operations**:
  - `download_file` - Download files from Artifactory to local path
  - `upload_file` - Upload files to repositories with checksum verification and retention info
  - `delete_item` - Delete files or entire package directories
  - `copy_item` - Copy packages between repositories (for promotion/backup)
  - `move_item` - Move packages between repositories

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `ARTIFACTORY_BASE_URL` | Base URL for Artifactory | `https://artifactory-02.boschdevcloud.com/artifactory` |
| `ARTIFACTORY_PAT_TOKEN` | Token for Artifactory authentication, VSCode will open a prompt for the token | `xxxxx` |

**Note:** When using the provided `mcp.json` configuration, you don't need to manually set these environment variables. The base URL and token will be prompted securely at runtime.

### Troubleshooting

#### Connection Issues
- **"Failed to connect to JFrog Artifactory"**: Verify `ARTIFACTORY_BASE_URL` and `ARTIFACTORY_PAT_TOKEN` are correct
- **Authentication failures**: Check if PAT token is valid and not expired
- **Permission errors**: Ensure token has necessary repository permissions

#### Common Errors
- **"ARTIFACTORY_PAT_TOKEN environment variable is required"**: Set the environment variable with your PAT token
- **Network timeouts**: Check proxy settings if running in corporate environment
- **"Invalid URL"**: Ensure `ARTIFACTORY_BASE_URL` includes the protocol (https://) and correct hostname
- **"Local file not found"**: When uploading, verify the local file path exists and is accessible

## Further Information

- [JFrog Artifactory Documentation](https://jfrog.com/help/r/jfrog-artifactory-documentation)
- [Artifactory REST API](https://jfrog.com/help/r/jfrog-rest-apis/artifactory-rest-apis)
- [Artifactory Query Language (AQL)](https://jfrog.com/help/r/jfrog-artifactory-documentation/artifactory-query-language)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
