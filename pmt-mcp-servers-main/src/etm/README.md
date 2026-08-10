# ETM MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with IBM Engineering Test Management (ETM).

## Overview

The ETM MCP Server provides comprehensive integration with IBM's Engineering Test Management system (RB-Tracker). It exposes a rich set of tools for managing test plans, test cases, test suites, execution results, and defect linking directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the ETM REST API.

### Limitations

- Some bulk operations on large datasets may not work as expected (pagination handling is yet to be done)
- Depending on the LLM models, accuracy might differ
- Complex test script steps with rich formatting may need special handling
- execution records creation requires pre-requisites to be met

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Access to IBM ETM [ALM-ETM Instance - Example](https://rb-alm-13-q.de.bosch.com/qm)
- Valid ETM credentials (username and password)
- ETM Project Area name [Example](CC-DA ESM Sandbox)

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Features

The server provides the following MCP tools for comprehensive ETM management:

- **Connection & Utilities**:
  - `test_project_connection` - Test connection to a specific project area
  - `list_project_areas` - List all available project areas
  - `search_resources` - Search ETM resources by category or type

- **Test Plan Management**:
  - `list_test_plans` - List all test plans in a project
  - `get_test_plan` - Get detailed information about a specific test plan
  - `create_test_plan` - Create a new test plan with dates and owner
  - `update_test_plan` - Update test plan details
  - `delete_test_plan` - Delete a test plan
  - `get_test_plan_statistics` - Get execution statistics for a test plan
  - `get_test_plan_tree` - Get complete test plan hierarchy (suites → cases → scripts)

- **Test Case Management**:
  - `list_test_cases` - List test cases with optional category filter
  - `get_test_case` - Get detailed information about a test case
  - `create_test_case` - Create a new test case
  - `update_test_case` - Update test case details
  - `delete_test_case` - Delete a test case
  - `get_test_case_links` - Get all links (requirements, defects) for a test case
  - `get_test_case_attachments` - Get attachments for a test case
  - `get_test_cases_by_use_case` - Find test cases by use case name

- **Test Suite Management**:
  - `list_test_suites` - List all test suites
  - `get_test_suite` - Get test suite details
  - `create_test_suite` - Create a new test suite
  - `update_test_suite` - Update test suite details
  - `delete_test_suite` - Delete a test suite
  - `add_test_cases_to_suite` - Add multiple test cases to a suite

- **Test Script Management**:
  - `list_test_scripts` - List test scripts
  - `get_test_script` - Get test script details
  - `create_test_script` - Create a new test script with steps

- **Execution Management**:
  - `list_execution_results` - List execution results with filtering
  - `get_execution_result` - Get detailed execution result information
  - `create_execution_record` - Create test execution record with result
  - `update_execution_result` - Update execution status and comments
  - `get_execution_results_by_test_plan` - Get all executions for a test plan
  - `get_execution_timeline` - Get execution results over time for trend analysis

- **Defect Linking**:
  - `get_execution_defects` - Get defects linked to an execution result
  - `link_defect_to_execution_result` - Link a JIRA defect to an execution
  - `get_failed_executions_without_defects` - Find failed tests without defect links

- **Linking Operations**:
  - `link_testcase_to_testplan` - Link a test case to a test plan
  - `link_test_suite_to_plan` - Link a test suite to a test plan

- **Advanced Analysis**:
  - `get_requirement_to_test_mapping` - Get requirements → test cases traceability
  - `find_orphaned_test_cases` - Find test cases not linked to requirements or plans

- **Additional Resources**:
  - `list_test_phases` - List test phases
  - `get_test_phase` - Get test phase details
  - `create_test_phase` - Create a new test phase
  - `list_build_records` - List build records
  - `get_build_record` - Get build information
  - `list_configurations` - List test configurations
  - `get_configuration` - Get configuration details
  - `list_attachments` - List attachments
  - `get_attachment` - Get attachment details
  - `list_templates` - List templates
  - `get_test_plan_template` - Get test plan template

- **Bulk Operations**:
  - `bulk_create_test_cases` - Create multiple test cases in batch
  - `bulk_execute_tests` - Execute multiple tests in batch

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `ETM_BASE_URL` | Base URL for ETM instance | `https://rb-alm-13-q.de.bosch.com/qm` |
| `ETM_USERNAME` | Username for ETM authentication | `soz1kor` |
| `ETM_PASSWORD` | Password for ETM authentication | `xxxxx` |
| `ETM_PROJECT_AREA` | Default project area to work with | `CC-DA ESM Sandbox` |

**Note:** When using the provided `mcp.json` configuration, you'll be prompted for credentials and configuration at runtime.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with ETM using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "List the test plans based on the latest release in my project"
- "Create a new test case titled 'Login validation'"
- "Show me all failed test executions for test plan 105520"
- "Link the test cases <testcaseID> to test plan <testplanID>"
- "Show me test plan 105520 with all its test suites and cases"
- "Add test cases 3435411, 3435412, 3435413 to test suite 7423"

The AI assistant will translate these natural language requests into actual API requests and execute them in ETM.

### Troubleshooting

#### Connection Issues
- **"Failed to connect to ETM"**: Verify `ETM_BASE_URL`, `ETM_USERNAME`, and `ETM_PASSWORD` are correct
- **Authentication failures**: Check if credentials are valid and not expired
- **Permission errors**: Ensure user has necessary project and execution permissions

#### Common Errors
- **"Resource not found"**: Verify resource ID format - use numeric webId for GET/UPDATE operations
- **"Project not found"**: Check project area name - use `list_project_areas` to see available projects
- **Network timeouts**: Check proxy settings if running in corporate environment
- **"Invalid URL"**: Ensure `ETM_BASE_URL` includes the protocol (https://) and correct hostname
- **"Permission denied"**: User may not have write permissions - check user roles in ETM

#### Resource ID Issues
- **"Cannot update/delete resource"**: Make sure you're using the numeric webId, not the slug__ identifier
- **"Resource created but cannot be retrieved"**: After creation, list resources to get the numeric webId
- **How to get webId**: Use list operations (e.g., `list_test_cases`) to see both slug__ and webId for resources

## Further Information

- [IBM Engineering Test Management Documentation](https://www.ibm.com/docs/en/engineering-test-management)
- [ETM REST API Guide](https://jazz.net/wiki/bin/view/Main/RqmApi)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
