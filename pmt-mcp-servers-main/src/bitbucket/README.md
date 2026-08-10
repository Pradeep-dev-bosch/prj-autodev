# Bitbucket MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Bitbucket Data Server environments.

## Overview

The Bitbucket MCP Server allows AI assistants to interact with Bitbucket repositories, projects, pull requests, branches, files, and more. It enables you to query, create, and manage Bitbucket resources directly from your AI-powered development tools.

### Limitations

- Direct creation or updating of files in Bitbucket repositories is not supported. To modify or create files, the repository is cloned locally and git operations are performed.
- The accuracy of results may vary depending on the LLM model used. For optimal performance and results, it is **recommended to use premium models such as GPT-5 or Claude Sonnet 4.5.**


## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../../README.md#access-to-pmt-artifactory-repository))
- Access to Bitbucket repository and a valid http API token.

### MCP Client Integration

1. Integrate the MCP server with your VSCode GitHub Copilot by adding a configuration file `.vscode/mcp.json`. Use the provided [`mcp.json`](mcp.json) as a reference and replace all placeholders.
2. Start the Docker or Python version MCP server after adding `.vscode/mcp.json`.
3. See [`../../README.md`](../../README.md) for more on [`Running MCP Servers using uv/python`](../../README.md#running-mcp-servers-for-development)

### Configuration

Set the following environment variables (in `mcp.json`) for the required MCP server `bitbucket-docker-mcp-server` or `bitbucket-python-mcp-server`:

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `BITBUCKET_URL` | Bitbucket server base URL | `https://sourcecode01.de.bosch.com` `https://sourcecode06.dev.bosch.com/projects/PRJ_NAME/repos/REPO_NAME/browse` `https://sourcecode06.dev.bosch.com/`|
| `BITBUCKET_TOKEN` | Bitbucket HTTP API token | `xxxxxxx` |
| `ALLOW_DELETION` | Enable destructive operations (delete branch/tag/pr) | `false` (default) or `true` |
| `TRANSPORT` | MCP transport protocol | `stdio` (default), `http`, `sse`|
| `HOST` | Server host address | `127.0.0.1` (default) |
| `HOST_PORT` | Server port | `8000` (default) |

**Note:** API tokens and sensitive credentials should be securely provided via input prompts, not stored in configuration files.

### Usage Examples

Once connected to VSCode GitHub Copilot chat or an MCP-compatible client, you can interact with Bitbucket using natural language. Try these examples:

- "Get summary of the repo https://sourcecode06.dev.bosch.com/projects/PRJ_NAME/repos/REPO_NAME/browse"
- "List all open pull requests in 'my-repo'"
- "Get list of feature branches which are older than 3 months"
- "Create a new branch 'feature/xyz' from 'main' in 'my-repo' in project 'MYPROJ', and make changes to <file_name> and commit."
- "Create pull request feature/xyz to main branch"
- "Review pull request <pull_request_link> and add review comments (mention 'comment from copilot' as note)"
- "Download the file 'README.md' from branch 'main'"
- "Delete the pull request #5 in 'my-repo' project 'MYPROJ'" (requires `ALLOW_DELETION=true`)

The AI assistant will translate these natural language requests into actual Bitbucket REST API requests and execute them against your Bitbucket server.

### Features

The server provides the following MCP tools for comprehensive Bitbucket management:

- **Project Management**:
	- `project_list` - List all projects
	- `repo_list` - List repositories in a project
	- `get_project` - Get project details
	- `get_project_permissions` - List users/groups with project permissions

- **Repository Management**:
	- `get_repo` - Get repository details
	- `get_repo_permissions` - List users/groups with repository permissions
	- `repo_grant_user_permissions` - Grant user permissions
	- `repo_grant_group_permissions` - Grant group permissions

- **Branching & Branch Content**:
	- `get_branches` - List branches
	- `create_branch` - Create a new branch
	- `get_branch_content` - List files in a branch
	- `get_branching_model` - Get branching model config

- **File & Commit Operations**:
	- `download_file_from_bitbucket` - Download a file
	- `get_file_content` - Get file content (raw/markup)
	- `get_commits` - List commits between two hashes
	- `get_commit_info` - Get commit details and changes
	- `get_diff` - Get file diff between commits

- **Pull Request Management**:
	- `get_pull_requests` - List pull requests
	- `get_pull_request_details` - Get PR details, activities, changes, commits
	- `open_pull_request` - Create a new pull request
	- `add_pull_request_comment` - Add comment to PR
	- `assign_pull_request_reviewer` - Assign reviewer to PR
	- `is_pull_request_can_be_merged` - Check if PR can be merged
	- `merge_pull_request` - Merge PR
	- `reopen_pull_request` - Reopen PR
	- `decline_pull_request` - Decline PR
	- `delete_pull_request` - Delete PR (requires `ALLOW_DELETION=true`)
    - `add_pull_request_inline_comment` - Add an inline comment to a specific line in a pull request
    - `set_pull_request_comment_state` - Resolve or reopen a pull request comment thread
    - `edit_pull_request_comment` - Edit an existing pull request comment
    - `set_pull_request_approval` - Approve or unapprove a pull request
    - `delete_pull_request_comment` - Delete a pull request comment (requires `ALLOW_DELETION=true`)

- **Tag Management**:
	- `get_tags` - List/get tags
	- `set_tag` - Create a tag
	- `delete_tag` - Delete a tag (requires `ALLOW_DELETION=true`)

- **Branch Permissions**:
	- `set_branches_permissions` - Set branch permissions
	- `get_branch_permission` - Get branch permission by ID

- **Webhooks**:
	- `get_repo_webhooks` - List repository webhooks

- **Reviewer Conditions**:
	- `get_project_conditions` - List project reviewer conditions
	- `get_repo_conditions` - List repo reviewer conditions

- **Deletion Operations** (requires `ALLOW_DELETION=true`):
	- `delete_branch` - Delete a branch
	- `delete_pull_request` - Delete a pull request
	- `delete_tag` - Delete a tag

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Authentication errors | Verify BITBUCKET_URL and http BITBUCKET_TOKEN are correct |
| The result is not good or the LLM produces nonsensical output | It is recommended to use premium models such as GPT-5 or Claude Sonnet 4.5 for better accuracy |
| Creation or updation of files fails or produces unexpected results | Always use premium models for file creation/updation operations. Note: LLM may run `git clone`, which can prompt for Bitbucket username and http_token—these should be entered when prompted. |
| Destructive operation fails | Ensure `ALLOW_DELETION=true` is set and you have required permissions |
| Unexpected or missing data | Refine your prompt or check Bitbucket API limitations |

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
- [PMT MCP Servers Artifactory](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local)
