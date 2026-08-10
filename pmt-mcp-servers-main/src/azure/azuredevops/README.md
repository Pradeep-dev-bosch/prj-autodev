# Azure DevOps MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that exposes Azure DevOps data (Projects, Repos, Boards, Agent Pools) to MCP‑enabled clients (e.g. VS Code GitHub Copilot Chat).

Built with `FastMCP` and the Azure DevOps CLI extension (`azure-devops`). It wraps Azure CLI commands via a lightweight tool interface while keeping credentials in environment variables.

## Overview

This server provides read and limited update access to Azure DevOps resources by invoking `az` commands with a Personal Access Token (PAT). Tools are designed to translate natural language requests into Azure DevOps operations.

### Limitations

- Only JSON output from Azure CLI is supported
- Work item updates limited to basic fields (state, assigned_to, title)
- No pipeline creation/modification yet
- Bulk operations not implemented
- PAT must have sufficient scopes (e.g. Work Items (Read & Write), Code (Read), Project & Team)

## Getting Started

### Prerequisites

- GitHub Copilot subscription
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Docker (optional for containerized run)
- Azure CLI >= 2.0.69 (`az --version`)
- Azure DevOps CLI extension: `az extension add --name azure-devops`
- Valid Azure DevOps organization URL (e.g. `https://dev.azure.com/yourorg`)
- PAT with required scopes

### MCP Client Integration

Add a configuration file (example: `./vscode/mcp.json`) pointing to this server, supplying environment variables. Then start the MCP server (Python or Docker) and use it in VS Code Copilot Chat.

### Features (Tools)

- `azdo_projects` – List projects
- `azdo_repos(project)` – List repositories in a project
- `azdo_boards_work_items(project, top)` – Fetch latest work items
- `azdo_agent_pools` – List agent pools
- `azdo_boards_teams(project)` – List teams for a project
- `azdo_boards_iterations(project, team)` – List iterations
- `azdo_boards_backlog_levels(project, team)` – Show backlog levels
- `azdo_boards_update_work_item(work_item_id, state?, assigned_to?, title?)` – Update a work item

### Usage Examples

In Copilot Chat (after connection):
- "List Azure DevOps projects"
- "Show repos in project X"
- "Get 5 recent work items from project Y"
- "Update work item 12345 state to Active"
- "List teams in project Z"
- "Show iterations for team Alpha in project Beta"

### Configuration

Set environment variables before starting:

```bash
export AZDO_ORG_URL=https://dev.azure.com/yourorg
export AZDO_PAT=your_pat_value
```

PAT scopes should include:
- Work Items (Read & Write) for updates
- Code (Read) for repos
- Project and Team (Read)

### Security

- PAT pulled from `AZDO_PAT` only at runtime
- Do not commit PAT or org URL into source control
- Rotate PAT periodically

### Troubleshooting

| Issue | Action |
|-------|--------|
| "Missing required environment variables" | Ensure AZDO_ORG_URL and AZDO_PAT are exported |
| CLI errors / 401 | Verify PAT scopes and org URL |
| Empty tool output | Check project name spelling and access rights |
| 403 errors | PAT lacks required permissions |
| Slow responses | Reduce `top` parameter or network constraints |

### Common Errors

- `Azure CLI error: ...` – Run the failing `az` command manually for diagnostics
- `ValueError on JSON` – Ensure CLI extension installed and output format JSON

### Development

Install dependencies, set env vars, run:
```bash
python adomcpserver.py
```

## References

- Azure DevOps CLI: https://learn.microsoft.com/azure/devops/cli/
- PAT Scopes: https://learn.microsoft.com/azure/devops/organizations/accounts/use-personal-access-tokens
- Model Context Protocol: https://modelcontextprotocol.io/
- FastMCP: https://github.com/jlowin/fastmcp
