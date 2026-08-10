# Azure DevOps MCP Server Release Notes

This file describes the changes introduced with each version of Azure DevOps MCP Server.

## 0.1.0
- Enhanced error handling and JSON parsing for Azure CLI responses
- Add some calls to filter for user
- Added new tools: `azdo_boards_work_items_by_user()` and `azdo_boards_work_items_by_user_all_projects()`

## 0.0.1
- Initial implementation of Azure DevOps MCP Server using `azuredevopsmcpserver.py`.
- Features:
	- Environment variable support for `AZDO_ORG_URL` and `AZDO_PAT`.
	- Azure CLI integration for project, repo, work item, agent pool, team, iteration, and backlog management.
	- Work item querying and update capabilities.
	- Logging and error handling for CLI operations.
	- Validation of Azure CLI and extension availability at startup.

## 0.0.0
- Initial beta release
