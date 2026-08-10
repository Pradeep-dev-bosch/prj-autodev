# Jenkins MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides comprehensive Jenkins CI/CD automation and management.

## Overview

The Jenkins MCP Server provides complete integration with Jenkins for managing jobs, builds, pipelines, nodes, and system operations. It exposes 36+ specialized tools for automating Jenkins workflows directly inside MCP-enabled clients (e.g., VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the Jenkins REST API with Basic authentication for secure access.

### Limitations

- Authentication (username and API token) is optional for anonymous Jenkins instances but required for write operations
- Some operations require specific Jenkins plugins (Blue Ocean, Replay, Workflow API)
- Credential listing requires credentials plugin and appropriate permissions
- Write operations (trigger builds, stop builds, etc.) typically require authentication even on instances with anonymous read access
- Depending on the LLM models, accuracy might differ. Premium models like GPT-4+ or Claude Sonnet 4.5 are recommended for better performance and results with complex Jenkins operations

## Getting Started

### Prerequisites

- GitHub Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ) (for Windows users)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-docker-artifactory-repository))
- Jenkins server with API access
- Jenkins username and API token - **Optional, only required for authenticated Jenkins instances**

### Jenkins API Token Setup

The Jenkins MCP server supports two authentication methods:

#### Method 1: Auth-Based (For Jenkins Instances with Login)

Use this method when your Jenkins instance requires authentication:

1. **Generate Jenkins API Token**
   - Log in to Jenkins
   - Go to User → Configure → API Token
   - Click "Add new Token"
   - Copy the generated token

2. **Configure Credentials in mcp.json**
   - Set `JENKINS_USERNAME` to your Jenkins username
   - Set `JENKINS_API_TOKEN` to the token you generated
   - The server will automatically handle base64 encoding

3. **Important Notes:**
   - ✅ Token should have minimal required permissions
   - ✅ Never commit tokens to version control
   - ✅ Use different tokens for different MCP servers/environments
   - ✅ Rotate tokens periodically following security best practices
   - ✅ No manual base64 encoding needed - the server handles this automatically

#### Method 2: No-Auth (For Jenkins Instances with Anonymous Access)

Use this method when your Jenkins instance allows anonymous/public access:

1. **Leave Credentials Empty**
   - In `mcp.json`, leave both `JENKINS_USERNAME` and `JENKINS_API_TOKEN` empty
   - Or don't set them in environment variables

2. **Verify Anonymous Access**
   - Ensure your Jenkins instance is configured to allow anonymous read access
   - Test by accessing the Jenkins URL without logging in

3. **Limitations:**
   - Some operations may be restricted (e.g., triggering builds, stopping builds)
   - Write operations typically require authentication even on "open" Jenkins instances

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

**Important for Docker Users:**
The Docker configuration includes a volume mount for SSL certificates:
```
-v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro
```
This mounts your system's CA certificates into the container, enabling secure SSL connections to Jenkins instances with corporate/custom SSL certificates. This is the industry-standard approach for Docker in corporate environments and allows SSL verification to remain enabled (secure by default).

Start the Docker version MCP server after adding `.vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `JENKINS_BASE_URL` | Jenkins server URL | ✅ Yes | `https://jenkins.example.com` |
| `JENKINS_USERNAME` | Jenkins username | ⚠️ Optional (for anonymous access) | `john.doe` or empty |
| `JENKINS_API_TOKEN` | Jenkins API token (not base64 encoded) | ⚠️ Optional (for anonymous access) | `11a1b2c3d4e5f6g7h8i9j0` or empty |
| `TRANSPORT` | MCP transport protocol | No | `stdio` (default), `http`, `sse` |
| `HOST` | Server host address (if not using stdio) | No | `127.0.0.1` (default) |
| `HOST_PORT` | Server port (if not using stdio) | No | `8000` (default) |

**Note:** When using the provided `mcp.json` configuration, set the environment variables as shown in the example configuration file.

#### Configuration Examples

**Example 1: Authenticated Access**
```json
{
  "JENKINS_BASE_URL": "https://rb-jmaas.de.bosch.com/YourProject",
  "JENKINS_USERNAME": "john.doe",
  "JENKINS_API_TOKEN": "11a1b2c3d4e5f6g7h8i9j0"
}
```
The server automatically creates the Basic authentication header by:
1. Combining username and token: `john.doe:11a1b2c3d4e5f6g7h8i9j0`
2. Base64 encoding the credentials
3. Setting the Authorization header: `Basic <base64_encoded_credentials>`

**Example 2: Anonymous Access**
```json
{
  "JENKINS_BASE_URL": "https://jenkins-public.example.com",
  "JENKINS_USERNAME": "",
  "JENKINS_API_TOKEN": ""
}
```
Leave both username and token empty for Jenkins instances that allow anonymous read access.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with Jenkins using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "List all Jenkins jobs"
- "Show me jobs in the cx-dash folder"
- "Get information about the test job"
- "Search for jobs containing 'pipeline' in the name"
- "What's the success rate of the test job?"
- "Trigger a build for the test job"
- "Get the latest build of test job"
- "Show me the build log for build #11"
- "Get the last successful build from test job"
- "Show me the build history of test job"
- "Get pipeline stages for build #10"
- "Replay build #11 of test job"
- "List all Jenkins plugins"
- "Show me all Jenkins nodes"
- "Get system information and queue stats"

The AI assistant will translate these natural language requests into actual Jenkins API requests and execute them.

### Features

The server provides comprehensive Jenkins integration capabilities with 36+ specialized MCP tools covering:

- Job querying, management, and configuration
- Build triggering, monitoring, and artifact management
- Pipeline stage analysis and replay functionality
- Node and system monitoring
- Plugin and credential listing

The following MCP tools are available for comprehensive Jenkins management:

- **Job Operations**:
  - `list_jobs` - List jobs recursively with filtering options
  - `get_job_info` - Get comprehensive job information
  - `get_job_description` - Retrieve job description text
  - `update_job_description` - Update job description via config.xml
  - `get_job_config` - Get complete job configuration XML
  - `get_job_metrics` - Calculate job metrics (success rate, avg duration)
  - `search_job` - Search jobs by name with detailed metrics

- **Build Operations**:
  - `get_build_info` - Get detailed build information
  - `get_build_log` - Retrieve console log output with line limiting
  - `get_build_history` - Get build history with optional date filtering
  - `get_last_build` - Get most recent build details
  - `get_last_successful_build` - Get last successful build
  - `get_last_failed_build` - Get last failed build
  - `trigger_build` - Trigger new builds with optional parameters
  - `search_builds` - Search builds with result filtering
  - `stop_build` - Stop/abort running builds
  - `get_build_changes` - Get SCM changesets for a build
  - `get_build_artifacts` - List build artifacts with download URLs
  - `download_artifact` - Download specific build artifacts (base64 encoded)

- **Pipeline Operations**:
  - `get_pipeline_stages` - Get detailed pipeline stage information (wfapi)
  - `get_pipeline_run_details` - Get Blue Ocean style pipeline details
  - `replay_pipeline` - Replay pipeline builds with optional script modification

- **System Operations**:
  - `ping` - Verify Jenkins server connectivity and get version info
  - `get_system_info` - Get Jenkins system info and queue statistics
  - `get_nodes` - List all Jenkins nodes/agents with status
  - `get_node_info` - Get detailed information about specific nodes
  - `get_plugins` - List all installed plugins with versions

- **Security Operations**:
  - `list_credentials` - List Jenkins credentials metadata (requires permissions)

### Troubleshooting

#### Authentication Issues
- **Anonymous Access Works, Auth Fails:** Verify username and token are correct
- **Invalid Credentials:** 401 Unauthorized - verify username and token are correct (no base64 encoding needed)
- **Insufficient Permissions:** 403 Forbidden - ensure user has required Jenkins permissions
- **Token Expired:** Generate new token and update configuration
- **Write Operations Fail on Anonymous:** Most Jenkins instances restrict write operations even with anonymous read access - use auth-based method for full functionality

#### Connection Issues
- **Cannot Connect:** Verify `JENKINS_BASE_URL` is correct and accessible
- **Network Timeout:** Check proxy settings if running in corporate environment
- **SSL/TLS Errors (Docker):** The Docker version mounts system CA certificates via volume mount. If you still see SSL errors:
  - Verify `/etc/ssl/certs/ca-certificates.crt` exists on your system
  - For custom certificates, you may need to add them to your system's CA bundle first
  - Python/stdio version uses system certificates directly and typically works without issues
- **Firewall Blocking:** Check network firewall rules and corporate proxy settings

#### Job Path Issues
- **404 Not Found:** Job path normalization failed - try different formats:
  - Simple: `job-name`
  - Nested: `folder/subfolder/job-name`
  - Full API: `job/folder/job/subfolder/job/job-name`
- **Path Contains Spaces:** Ensure spaces are properly handled in job names

#### Build Operations
- **Build Not Starting:** Check if job requires parameters - use `trigger_build` with parameters
- **Cannot Stop Build:** Build may have already completed or not be running
- **Missing Build Number:** Use `get_last_build` or `search_builds` to find build numbers

#### Pipeline Issues
- **Pipeline Stages Missing:** Requires Workflow API (wfapi) plugin to be installed
- **Blue Ocean Not Available:** Requires Blue Ocean plugin to be installed
- **Replay Failed:** Requires Replay plugin and build must be a pipeline

#### Common Errors
- **Rate Limiting:** Jenkins API throttling - reduce request frequency
- **Plugin Not Installed:** Some features require specific plugins (Blue Ocean, wfapi, Replay)
- **Credential Listing Failed:** Requires credentials plugin and appropriate permissions
- **Network Proxy Issues:** Set HTTP_PROXY and HTTPS_PROXY environment variables if needed

## Further Information

- [Jenkins REST API Documentation](https://www.jenkins.io/doc/book/using/remote-access-api/)
- [Jenkins Pipeline Documentation](https://www.jenkins.io/doc/book/pipeline/)
- [Jenkins Blue Ocean](https://www.jenkins.io/doc/book/blueocean/)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
