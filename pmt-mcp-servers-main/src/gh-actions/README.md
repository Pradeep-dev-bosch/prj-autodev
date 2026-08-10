# GitHub Actions MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with GitHub's platform and GitHub Actions workflows.

## Overview

The GitHub Actions MCP Server enables AI assistants to interact with GitHub Actions workflows and team context. This server acts as a bridge between conversational AI and your GitHub infrastructure, allowing for natural language queries to be translated into GitHub API calls.

> **Note:** This server (`src/gh-actions`) and the GitHub server (`src/github`) use the same Docker image (`ghcr.io/github/github-mcp-server:0.31.0`) but with different `GITHUB_TOOLSETS`:
> - **`actions,context`** (this server): Covers GitHub Actions workflows and team context
> - **`default`** (src/github): Covers GitHub standard tools (repositories, issues, pull requests, etc.)

### Limitations

- Be aware that you are using your own token and workflow triggers are executed in your name.
- Token scope requirements vary by toolset: `workflow` scope is required for Actions tools; `read:org` is required for Context tools.
- For SAML-authenticated organizations, the token must be authorized via SSO before use.
- The accuracy of results may vary depending on the LLM model used. For optimal performance, it is **recommended to use premium models such as Claude Sonnet**.

## Getting Started

### Prerequisites

- Docker ([Docker for Linux installation guide](https://inside-docupedia.bosch.com/confluence/spaces/DEVCORNER/pages/1595519415/Docker+for+Linux) if not already installed via WSL setup)
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- GitHub account with appropriate repository access
- Personal Access Token (PAT) with required scopes (`repo`, `workflow`, `read:org`)
- GitHub Copilot Subscription

### MCP Client Integration

1. Integrate the MCP server with your VSCode GitHub Copilot by adding a configuration file `.vscode/mcp.json`. Use the provided [`mcp.json`](mcp.json) as a reference and replace all placeholders.
2. Start the Docker MCP server after adding `.vscode/mcp.json`. It is ready to use now.
3. See [`../README.md`](../README.md) for more on [Running MCP Servers](../README.md#running-mcp-servers-for-development).

### Configuration Details

Set the following environment variables (in `mcp.json`) for the MCP server:

| Variable | Description | Example |
|----------|-------------|---------|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | GitHub Personal Access Token (token should have the right access permissions based on selected toolsets) | `ghp_xxxxxxxxxxxxxxxxxxxx` |
| `GITHUB_TOOLSETS` | Comma-separated list of enabled toolsets | `context,actions` |
| `GITHUB_HOST` | GitHub host URL for GitHub.com or GitHub Enterprise Server | `https://github.com` or `https://github.boschdevcloud.com` |

> **Docker Image Version:** The current configuration uses `ghcr.io/github/github-mcp-server:0.31.0`. Available versions can be found on the [GitHub tags page](https://github.com/github/github-mcp-server/tags). Users may, at their own risk, use the latest version (`ghcr.io/github/github-mcp-server:latest`). However, the README and usage parameters must be verified against the specific version being used.

#### Available Toolsets

| Toolset | Description |
|---------|-------------|
| `actions` | GitHub Actions workflow tools (trigger, monitor, and manage workflows) |
| `context` | User and team context tools (authenticated user profile, teams, members) |

#### Authentication Setup

1. **Create a Personal Access Token:**
	- Go to GitHub Settings > Developer settings > Personal access tokens
	- Generate new token (classic) with required scopes:
		- `repo` - Full repository access (required for actions)
		- `workflow` - GitHub Actions workflow access (required for actions toolset)
		- `read:org` - Organization team access (required for context toolset)

2. **For SAML-authenticated tokens:**
	If your organization uses SAML authentication, authorize your token:
	- Go to Settings > Personal access tokens
	- Find your token and click "Configure SSO"
	- Select your organization and authorize

3. **Use the token** when configuring the MCP server (see MCP Client Integration section above).

### Usage Examples

Once connected to VSCode GitHub Copilot chat or an MCP-compatible client, you can interact with GitHub Actions and team context using natural language. Try these examples:

**GitHub Actions Workflows:**
- "List all workflows in the repository owner/repo"
- "Show me workflow runs for repository owner/repo"
- "Get logs for failed jobs in run 123456789"
- "Trigger workflow 'deploy.yml' on branch main in repository owner/repo"
- "Cancel workflow run 123456789 in repository owner/repo"
- "Download artifact from workflow run 123456789"

**Team Context:**
- "Get my GitHub user profile"
- "List teams for user username"
- "Get members of team team-slug in organization org-name"

### Features

The server provides the following MCP tool categories:

- **GitHub Actions** (`actions` toolset):
	- `actions_get` - Get details of workflows, workflow runs, jobs, and artifacts
	- `actions_list` - List workflows, workflow runs, workflow jobs, and artifacts
	- `actions_run_trigger` - Trigger, rerun, cancel workflow runs or delete logs
	- `get_job_logs` - Get workflow job logs, optionally filtered to failed steps only

- **Team Context** (`context` toolset):
	- `get_me` - Get the authenticated user's profile
	- `get_teams` - Get teams for a user (requires `read:org` scope)
	- `get_team_members` - Get members of a team in an organization (requires `read:org` scope)

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication failed | Ensure your Personal Access Token has the correct scopes (`repo`, `workflow`, `read:org`) and is not expired |
| SAML SSO token not authorized | Go to Settings > Personal access tokens > Configure SSO and authorize for your organization |
| MCP server connection issues | Ensure Docker is installed and running; verify `mcp.json` is valid JSON; restart your MCP client |
| Rate limiting errors | GitHub API allows 5000 requests/hour for authenticated users; wait for the rate limit to reset |
| Workflow trigger fails | Verify the workflow file exists on the target branch and the token has `workflow` scope |
| Missing team data | Ensure the token has `read:org` scope and is authorized for SAML SSO if applicable |

## Related Resources

- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [MCP Protocol Specification](https://spec.modelcontextprotocol.io/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
