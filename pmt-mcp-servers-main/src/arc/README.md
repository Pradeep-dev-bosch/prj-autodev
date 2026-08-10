# ARC MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides comprehensive integration with ARC (Automatic Release Checker), an automated QG questionnaire evaluation system.

## Overview

The ARC MCP Server provides integration with ARC for automating quality gate questionnaire evaluation, ensuring compliance with DROP (Delivery Release of Product) guidelines. It exposes tools for executing release checks, analyzing reports, and managing the evaluation workflow directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via runtime prompting.

The server is built with the `FastMCP` framework and integrates with the ARC CLI tool.

### Limitations

- Requires ARC package (v3.5) installed from Bosch Artifactory
- Report analysis depends on ARC's HTML output format
- Network access required for external integrations (SharePoint, OneQ, Splunk, Jira, Docupedia)
- Depending on the LLM models, accuracy might differ

## Getting Started

### Prerequisites

- GitHub Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ) (for Windows users)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-docker-artifactory-repository))
- Python 3.13+ (for local development)
- Valid Bosch credentials for required services (SharePoint, Jira, OneQ, etc.)
- JFrog Artifactory access for ARC package installation

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `./vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding `./vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with ARC using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Validate my ARC environment configuration"
- "Run an ARC dry-run check for release 550_SW against 541_SW with RT04"
- "Execute ARC quality gate evaluation for the VW_RADAR project"
- "Analyze the latest ARC report and summarize quality gate findings"
- "Show me all failed quality checks from the report"

The AI assistant will translate these natural language requests into actual ARC operations and execute them.

### Features

The server provides the following MCP tools for comprehensive ARC workflows:

- **Environment & Validation**:
  - `arc_validate_environment` - Check environment configuration and credential setup

- **Execution & Reports**:
  - `arc_execute_command` - Execute ARC release checks with configurable parameters
  - `arc_analyze_report` - Parse and summarize HTML reports with quality gate findings


## Configuration

### Environment Variables

The server requires the following environment variables which will be prompted via `mcp.json` inputs:

**Artifactory Access** (Required for ARC package installation):
- `TECH_USERNAME` - Technical username for Artifactory
- `JFROG_TOKEN` - JFrog access token

**SharePoint Integration**:
- `SHAREPOINT_USERNAME` - SharePoint username
- `SHAREPOINT_PASSWORD` - SharePoint password

**Database Access**:
- `SQL_TECH_PASSWORD` - SQL database password

**OneQ Integration**:
- `ONEQ_API_KEY` - OneQ API key
- `ONEQ_SECRET` - OneQ API secret

**Monitoring & Logging**:
- `SPLUNK_USERNAME` - Splunk username
- `SPLUNK_PASSWORD` - Splunk password

**Collaboration Tools**:
- `JIRA_TOKEN` - Jira API token
- `DOCUPEDIA_TOKEN` - Docupedia API token

**Configuration**:
- `BU` - Business unit identifier

**Workspace & SSL** (Pre-configured in mcp.json):
- `ARC_WORKSPACE` - Path to ARC workspace directory
- `CERT_PATH` - SSL certificate configuration:
  - `""` (default) -> use system certificates
  - custom absolute path -> use custom CA bundle
  - `"false"|"disable"|"off"|"no"` -> disable SSL verification (dev/test only)


## Report Output

ARC generates quality gate reports in:

- **HTML Reports**: `html/report.html` with detailed evaluation findings
- **Documentation Tree**: `doctrees/report.doctree` for Sphinx documentation

Each report contains:

- Quality gate questionnaire evaluations
- Status indicators (Red/Yellow/Green)
- Detailed check results with remarks
- Links to relevant documentation

## Troubleshooting

### Common Issues

1. **Missing credentials**: Ensure all 12 environment variables are provided via mcp.json inputs
2. **Certificate errors**:
  - Use default `CERT_PATH=""` for system certificates (recommended)
  - If needed, set `CERT_PATH` to a custom CA bundle path
  - For local dev only, set `CERT_PATH="false"` to disable SSL verification
3. **ARC command failures**: Check proxy settings and network connectivity
4. **Report parsing errors**: Ensure ARC generated valid HTML output in expected format

## Further Information

- [Automatic Release Checker](https://inside-docupedia.bosch.com/confluence/spaces/CCD/pages/4386330146/%F0%9F%94%84Automatic+Release+Checker+ARC+%F0%9F%94%84)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)

