# Conan MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides powerful integration with the Conan package manager.

## Overview

The Conan MCP Server lets you search packages, inspect profiles, install dependencies, analyze graphs, collect licenses, scan vulnerabilities, and run editable workflows—all from MCP-enabled clients (e.g. VS Code Copilot Chat).

Built with `FastMCP` and the Conan CLI.

### Limitations

- Requires Conan installed and accessible to the server
- Some operations depend on remotes availability and network/proxy settings
- Vulnerability scanning uses external audit service and may be rate-limited

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Conan [installed](https://docs.conan.io/2/installation.html) on the machine running the MCP server
- **For Dev Container usage**: Mount MCP server code in your `docker-compose.yaml`:
  ```yaml
  services:
    dev-env:
      volumes:
        - /path/to/repository/pmt-mcp-servers/src/conan/:/path/to/repository/pmt-mcp-servers/src/conan/
  ```

### MCP Client Integration

Add a configuration file like `./vscode/mcp.json`. Use this repository’s `mcp.json` in `src/conan/` as a reference and replace placeholders.

Start the Docker or Python `uv` server based on your environment.

See [`../README.md`](../README.md) for more on [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development).

### Usage Examples

Once connected to an MCP-compatible client, try prompts like:

- "List available versions of fmt in conancenter"
- "List all packages from artifactory-prod in conan-local repository"
- "Show me packages matching 'mycompany/*' from conan-remote repository"
- "Install dependencies in this project with profile tools/conan/profiles/mypackage/custom_profile"
- "Show me the dependency graph for this project"
- "Create a CMake executable project called 'myapp' with fmt and openssl"
- "Scan zlib/1.3.1 for vulnerabilities"

The assistant will translate requests into Conan CLI operations.

### Features

The server provides the following MCP tools for comprehensive Conan workflows:

- **Profiles & Environment**:
  - `get_conan_profile` - Show profile configuration
  - `list_conan_profiles` - List available profiles
  - `discover_package_profiles` - Discover package-specific profiles in `tools/conan/profiles/...`

- **Search & Cache**:
  - `list_conan_packages` - Search packages in remotes and/or cache with filters
  - `list_cached_packages` - List what resides in local cache
  - `list_packages_from_remote` - List packages from Artifactory or other remotes using Conan commands

- **Install & Graph**:
  - `install_conan_packages` - Install dependencies and produce full graph/lockfile
  - `get_dependency_graph` - Generate interactive HTML dependency graph with clickable link and summary
  - `analyze_install_sources` - Categorize packages by source (Cache/Download/Build/Skip)

- **Licenses & Security**:
  - `get_conan_licenses` - Collect licenses from dependency graph (host context)
  - `scan_conan_dependencies` - Audit dependencies or specific references for vulnerabilities

- **Editable Workflow**:
  - `add_editable_package`, `remove_editable_package`, `list_editable_packages`
  - `discover_cmake_presets` - Read available CMake presets

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `CONAN_MCP_CONAN_PATH` | Path to Conan executable used by the server | `/home/user/venv/bin/conan` |
| `ARTIFACTORY_CONNECTION` | (Optional) JSON object mapping Artifactory server names to base URLs for `list_packages_from_remote` | `{"artifactory-02": {"url": "https://artifactory-02.boschdevcloud.com/artifactory", "user": "ntid@bosch.com", "password": "api-token"}}` |

Note: If `CONAN_MCP_CONAN_PATH` is not set, the server uses `conan` from PATH or the active virtual environment.
Note: `ARTIFACTORY_CONNECTION` stores only base Artifactory URLs. The tool will ask for the repository name (e.g., "conan-local") and construct the full URL as `{base_url}/api/conan/{repository_name}`.

### Detailed Tool Guide

Refer to in-code docstrings and examples for each tool. Common ones:

- `list_conan_packages(name, version, remote, filter_settings, filter_options, ...)`
- `list_packages_from_remote(artifactory_name, repository_name, package_pattern, username, password, ...)`
- `install_conan_packages(path, work_dir, host_profile, options_host, settings_host, build_missing, ...)`
- `get_dependency_graph(work_dir, path | requires, host_profile, ...)`
- `get_conan_licenses(work_dir, path | requires, host_profile, ...)`
- `scan_conan_dependencies(work_dir, path | reference)`
- `add_editable_package(path, name, version, user, channel, output_folder)`

### Troubleshooting

- Conan not found: Set `CONAN_MCP_CONAN_PATH` or ensure Conan is on PATH
- Remote/network errors: Verify proxy settings; adjust `mcp.json` env vars
- Missing binaries: Use `--build=missing` or adjust profile settings/options
- License extraction empty: Ensure graph is computed for host context dependencies
- Audit rate limits: External audit service may limit daily requests

## Further Information

- [Conan Documentation](https://docs.conan.io/2)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
