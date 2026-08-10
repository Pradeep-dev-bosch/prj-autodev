# Perforce QAC MCP Server

> **⚠️ DISCLAIMER**: This MCP server is currently in a pilot state and has been tested exclusively with OneDriving (OD) DevContainer environments. Use in other environments may require additional configuration and testing.

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server for automating Perforce Helix QAC/QACPP static analysis workflows (full, diff, single-file), exporting results, filtering by severity/rules, and generating threshold reports — usable directly or inside a project DevContainer with dual virtual environments.

## Overview

The Perforce QAC MCP Server provides comprehensive integration with Perforce Helix QAC static analysis tools. The server wraps the `sca_tools` CLI and exposes high-level MCP tools so an AI assistant can:

* Create and manage project variant configurations
* Run full analysis (create → analyze → export → filter)
* Run diff analysis (changed files only, baseline comparison)
* Run single-file analysis for quick feedback
* Export artifacts (CSV / HTML / XLSX) & filter results
* Generate threshold compliance reports
* Analyse the findings from generated reports and LLM can suggest fixes

The server is built with the `FastMCP` framework and the `sca_tools` CLI.

### Limitations

* Linux only (Debian/Ubuntu and similar); Windows untested (use WSL2)
* Requires Helix QAC installed & you have Helix license (validated with 2023.4 & 2024.4) in container `/opt/Perforce/Helix-QAC-<version>`
* Its better to create the project configuration files beforehand, as per the template given in [Project Configuration JSON Example](#project-configuration-json-example) sub section. There is an MCP tool for it and you can mention in chat to create it (eg: Create the project config with below info), before mentioning the MCP server to run a full/diff/single file analysis.
* MCP tools will skip project creation, if it sees a compile_commands.json existing. So, if you want to have project creation, mention in chat "Don't skip project creation".
* Private Bosch Artifactory access needed for internal Python packages
* Diff analysis assumes accessible git merge base & proper datastore baseline paths
* As this is tightly coupled with sca_tools implementation, one should know the path to the project datastore target json file, the path to Helix installation in the container, etc.
* The accuracy of results may vary depending on the LLM model used. The MCP server was tested against both basic models and premium models and both produce almost same results. When it comes to post processing chats, especially in fixing bugs reported during QAC analysis, premium models might give better results.

## Getting Started

### Prerequisites

* Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
* Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
* Python 3.10+
* Helix QAC 2023.4 and up installation
* `sca_tools` available (project toolchain)
* Access to Bosch Artifactory (od / sofa / poe repos)

### MCP Client Integration

Before deploying the qac-mcp-server, ensure the following prerequisites are met:

* **Bootstrap Script Deployment**  
   Copy `src/qac/qac_mcp_bootstrap.sh` to your project's `.devcontainer` directory and ensure the script is executable.

* **DevContainer Configuration**
   Update the `postCreateCommand` property in your `.devcontainer.json` file to execute the bootstrap script during container initialization. This ensures the pip package and qac-mcp CLI command are properly installed.

   ```json
   "postCreateCommand": "${containerWorkspaceFolder}/.devcontainer/qac_mcp_bootstrap.sh"
   ```

   > **Note:** If a `postCreateCommand` is already defined in your configuration, include our bootstrap script using the `&&` operator to ensure sequential execution:
   >
   > ```json
   > "postCreateCommand": "existing-command && ${containerWorkspaceFolder}/.devcontainer/qac_mcp_bootstrap.sh"
   > ```

* **Container Rebuild**  
   Rebuild the DevContainer to execute the `postCreateCommand`. Press `Ctrl+Shift+P`, then select "Dev Containers: Rebuild Container" from the command palette.

* **MCP Configuration**
   Create a configuration file at `.vscode/mcp.json` within your project workspace (not within the MCP repository). Refer to the provided [`mcp.json`](mcp.json) template and replace all placeholder values with your environment-specific settings.

* **Server Initialization**
   After configuring `.vscode/mcp.json`, start the MCP server through your IDE. The server will be ready for use once initialization is complete.

For further details check out the [`../README.md`](../README.md) to find out more about e.g. [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with QAC using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Create a QAC project configuration for my project"
- "Run a full QAC analysis for variant 'ABC' "
- "Run a diff analysis for branch 'abc' against target branch as 'xyz' with a min severity level of 7, for variant 'ABC' "
- "Run analysis on a single file: src/main.cpp"
- "Export the analysis results as CSV and HTML"
- "Generate a threshold compliance report"
- "Show me all background tasks"
- "Get the status of task abc123"

The AI assistant will translate these natural language requests into actual QAC analysis commands and execute them.

### Features

The server provides comprehensive QAC integration capabilities organized into these categories:

| Category | Tool | Purpose |
|----------|------|---------|
| **Project Management** | `create_qacpp_config` | Create project config |
| | `list_projects` | List configs |
| | `get_project_details` | Inspect config details |
| | `delete_project_config` | Remove config |
| | `create_qacpp_project` | Initialize QACPP project database |
| **Background Analysis** | `run_full_analysis_background` | End‑to‑end full scan (returns task_id) |
| | `run_diff_analysis_background` | Changed files only (returns task_id) |
| **Direct Analysis** | `run_qacpp_analysis` | Run analysis directly on configured project |
| | `run_single_file_analysis_workflow` | Analyze single file (blocking) |
| **Task Management** | `list_background_tasks` | List all background tasks |
| | `get_task_status` | Get status of background task |
| | `get_task_result` | Get results from completed task |
| **Results** | `export_qacpp_results` | Export artifacts |
| | `extract_results` | Filter by severity / rules |
| | `generate_threshold_report` | Threshold violations report |

#### Project Configuration JSON Example

```json
{
  "datastore_paths": "/path/to/tools/sca/qac.json",
  "datastore_target": "TARGET_NAME",
  "project_root": "/path/to/project/",
  "qac_bin_path": "/opt/Perforce/Helix-QAC-2023.4/common/bin"
}
```

#### Handling Timeouts and Long-Running Analyses

Static analysis with `sca_tools qac analyze` can run for tens of minutes to hours. MCP clients (like Copilot Chat) may drop the connection if there's no activity for a while. This server includes two complementary mechanisms to keep your workflows smooth:

**1. Background Execution (Recommended)**

Run QAC/QACPP analyses in the background so you can continue using your MCP client while processing completes.

* Start an analysis and get a task ID immediately
* Continue chatting and issuing other commands
* Check status anytime with `get_task_status(task_id)`
* Retrieve results when completed with `get_task_result(task_id)`

**Core Tools:**
- `run_full_analysis_background(project_name, ...)` – Start full analysis
- `run_diff_analysis_background(project_name, merge_base, ...)` – Start diff analysis
- `get_task_status(task_id)` – Check if running/completed/failed
- `get_task_result(task_id)` – Retrieve results of a completed task
- `list_background_tasks(status_filter)` – See all tasks

**Example:**

```python
# Start full analysis
resp = run_full_analysis_background(project_name="MyProject", min_severity_level=5)
task_id = resp["task_id"]

# Check progress
status = get_task_status(task_id=task_id)

# Get results when done
if status["status"] == "completed":
    results = get_task_result(task_id=task_id)
```

**2. Async Streaming Keepalive**

* The server streams subprocess stdout/stderr in real time and emits heartbeat logs if the tool is quiet for ~30s
* Effect: prevents MCP connection timeouts for foreground runs; you still wait in the same chat while it finishes
* Progress is tracked with status updates and logged to the console

**When to Use Background:**

All analysis workflows now use background execution exclusively:
- Full codebase analysis (tens of minutes to hours)
- Diff analysis for large changes
- Single file analysis (use `run_single_file_analysis_workflow` for quick blocking execution)

### Configuration

Set the following environment variables in your `mcp.json`:

| Variable | Description | Example |
|----------|-------------|---------|
| `ARTIFACTORY_URL` | Base Artifactory URL | `https://artifactory.boschdevcloud.com` |
| `ARTIFACTORY_USER` | Artifactory username | `<YOUR_NTID>@bosch.com` |
| `ARTIFACTORY_API_TOKEN` | ID token for artifactory | `****` |
| `BASELINE_URL` | Baseline artifact path or URL in artifactory | `od-artifacts-develop-local/latest/rpc_apl/ALPHA_2_QACPP/qac-baseline/develop/files.sup` |

**Note:** When using the provided `mcp.json` configuration, you'll be prompted for credentials and configuration at runtime.

### Troubleshooting

#### Connection Issues
- **"Venv Creation Fails"**: Delete the venv, temp folder and cache and try again (`rm -rf /path/to/repository/src/qac/.tmp /path/to/repository/src/qac/.uv_cache /path/to/repository/src/qac/.uv_python /path/to/repository/src/qac/.venv`). Ensure that you have access to bosch private repos to download packages by ensuring that proper PAT tokens are given in `~/.netrc`
- **"Package Version Errors"**: Verify dual venv wrapper script executed; recreate MCP venv if broken

#### Analysis Errors
- **"Analysis Fails"**: Ensure `compile_commands.json` present; correct datastore target; validate `qac_bin_path`; inspect console logs for `sca_tools` analyze output
- **"Export Fails"**: Check console logs; verify exported CSV/HTML/XLSX exist; confirm permissions & disk space
- **"Threshold Non‑Zero Exit"**: Indicates violation count above threshold — adjust rules or severity cutoff

#### Diff Analysis Issues
- **"Diff Issues"**: Fetch latest refs (`git fetch origin`); confirm merge base; handle renames manually if needed

#### Network Issues
- **"Proxy / Network"**: Revisit proxy env vars; ensure internal domains in `NO_PROXY`

#### Common Errors
- **Skip creation optimization**: If the project is already created, set `skip_create=true` when invoking the tools
- **"Tool not found"**: Ensure the tool is installed in the correct venv and shims are configured properly

## Further Information

* [Model Context Protocol](https://modelcontextprotocol.io/)
* [FastMCP Framework](https://github.com/jlowin/fastmcp)
* [uv Package Manager](https://github.com/astral-sh/uv)
* Helix QAC (internal docs)
* SCA Tools CLI (internal usage)
* Bosch Artifactory Access (internal)