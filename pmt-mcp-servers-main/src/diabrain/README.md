# DIA Brain MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Bosch DIA Brain API.

## Overview

The DIA Brain MCP Server provides integration with the Bosch DIA Brain knowledge retrieval system. It exposes tools for querying knowledge bases including SharePoint sites and Docupedia spaces directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the DIA Brain retrieval-augmented API.

For complete DIA Brain documentation, see: [DIA BRAIN - User Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/3693697491/DIA+BRAIN+-+User+Documentation)

### Limitations

- Authentication requires valid Azure AD credentials and client secrets (expires every 180 days)
- API access is restricted to Bosch internal networks or requires proxy configuration
- Query timeouts are set to 60 seconds
- User account must be connected to the application in DIA Brain's API Integration settings
- Depending on the LLM models, accuracy might differ. Premium models like GPT-5 or Claude Sonnet 4.5 are recommended for better performance and results

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-docker-artifactory-repository))
- Valid Azure AD client credentials for DIA Brain API (CLIENT_SECRET expires every 180 days)
- Access to Bosch internal network or proxy configuration
- User account connected to the application in DIA Brain API Integration (see Configuration section)

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with DIA Brain using natural language. Try these examples in your VSCode GitHub Copilot chat:

**With Default Brain** (no brain_id needed):
- "What is MCP Inspector?"
- "Find information about AUTOSAR specifications"
- "Search for tool development best practices"
- "What is RA6?"

**With Specific Brain ID** (override default):
- "Query brain ID VoEGl_0KtuAJ about AUTOSAR specifications from SharePoint site Autosar"
- "Search brain ID 3jm3g_KljdIG for tool development best practices"
- "Query brain ID VoEGl_0KtuAJ for information about RA6 from Docupedia space RA6"

**Configuration Management**:
- "Show my enabled brains" - See which brains are configured
- "List all available brains" - View all brains you have access to

The AI assistant will translate these natural language requests into actual API requests and execute them against the DIA Brain API.

### Features

The server provides the following MCP tools for interacting with DIA Brain:

#### Knowledge Base Query Tools
- **`query_brain`** - Query any DIA Brain knowledge base
  - **Optional** `brain_id` parameter (uses default if not specified)
  - Configure specific SharePoint site IDs (comma-separated)
  - Configure specific Docupedia space IDs (comma-separated)
  - GPT knowledge augmentation is automatically enabled

- **`batch_query`** - Execute multiple queries efficiently in one operation
  - Pass list of prompts
  - **Optional** `brain_id` parameter (uses default if not specified)
  - Supports SharePoint and Docupedia filtering
  - Returns results for all prompts with success/failure status

#### Knowledge Base Discovery Tools
- **`list_brains`** - List all DIA Brain knowledge bases you have access to
  - Shows brain IDs, titles, descriptions
  - Includes current configuration (default brain, enabled brains)

- **`get_enabled_brains`** - View your configured brain settings
  - Shows default brain ID with name
  - Lists all enabled brains with names and descriptions
  - Indicates which brain is currently set as default

- **`get_brain_details`** - Get detailed information about a specific brain
  - Shows configuration, permissions, and settings
  - View LLM model, search mode, security levels

#### Knowledge Source Tools
- **`list_sharepoint_sites`** - List SharePoint sites connected to a brain
  - Shows site names, URLs, processing states

- **`list_docupedia_spaces`** - List Docupedia spaces connected to a brain
  - Shows space names, keys, processing states
  - View connected pages and their states

- **`list_documents`** - List documents in a knowledge base
  - Optional filtering by document types (FILE, WEBPAGE, CONFLUENCE_PAGE, SERVICE_NOW_ARTICLE)
  - Shows document names, sources, processing states

**Example Usage**:
```python
# Use default brain (configured in mcp.json)
query_brain(prompt="What is AUTOSAR?")

# Override with specific brain
query_brain(prompt="What is AUTOSAR?", brain_id="VoEGl_0KtuAJ", sharepoint_sites="Autosar")

# Query with Docupedia sources
query_brain(prompt="What is RA6?", docupedia_spaces="RA6")

# Batch queries
batch_query(prompts=["What is MCP?", "What is AUTOSAR?", "What is RA6?"])

# View configuration
get_enabled_brains()  # Shows your default and enabled brains

# List all accessible brains
list_brains()

# Get details of specific brain
get_brain_details(brain_id="3jm3g_KljdIG")
```

### Configuration

All environment variables are configured in your [mcp.json](mcp.json) file. The required variables are:

**Authentication** (Required):
- `CLIENT_SECRET` - Your Azure AD client secret (expires every 180 days, requires rotation)
- `CLIENT_ID` - Your application ID from Azure AD
- `TENANT_ID` - Azure AD tenant ID (default: `0ae51e19-07c8-4e4b-bb6d-648ee58410f4`)

**Brain Configuration** (Optional but Recommended):
- `ENABLED_BRAIN_IDS` - Comma-separated list of brain IDs you have access to (e.g., `3jm3g_KljdIG,VoEGl_0KtuAJ`)
- `DEFAULT_BRAIN_ID` - The brain ID to use by default when not specified in queries
  - If not set, the first brain from `ENABLED_BRAIN_IDS` will be used
  - Allows querying without repeatedly specifying `brain_id` parameter

**Network Configuration**:
- `HTTP_PROXY`, `HTTPS_PROXY` - Proxy settings as needed
- `NO_PROXY` - Proxy exclusions for local and Bosch domains
- `SSL_VERIFY` - Set to `false` for local proxy, `true` for production

**Brain Configuration Benefits**:
- Query without specifying `brain_id`: `query_brain(prompt="What is MCP?")`
- Quickly switch brains by restarting server and selecting different default
- View configured brains with `get_enabled_brains()`
- Override default when needed: `query_brain(prompt="...", brain_id="OTHER_BRAIN_ID")`

**Important Configuration Steps**:

1. **Create Azure App and Get Client Credentials**:
   - Follow the complete guide: [DIA Brain REST API Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain)
   - Create an Azure App Registration in Bosch tenant
   - Generate CLIENT_SECRET (expires every 180 days and requires rotation)
   - Note your CLIENT_ID from the app registration

2. **Add/Create Brain (Knowledge Base)** (Optional - if creating your own brain):
   - Follow the guide: [Add Brain Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414244/Add+Brain)
   - Create and configure your custom knowledge base
   - Note your brain_id for use in queries

3. **Connect Application to Your User Account**:
   - Go to: https://brain.prd.dia-apps.bosch.tech/brains
   - Click your user menu → 'API Integration'
   - Enter application ID: `YOUR_APPLICATION_ID` (or your custom CLIENT_ID)
   - Submit to connect the app to YOUR user account
   - This step is **required** to avoid 401 MessageBlocked errors

4. **Request Application Whitelisting** (if still failing after step 3):
   - Submit request: https://forms.office.com/e/K3gHBLbcbh
   - Wait for confirmation (up to 5 working days)

For development or testing with Python/uv, you can also set environment variables directly in your shell (see Development section).

### Connection Details

The server connects to:
- **Authentication Endpoint**: `https://login.microsoftonline.com/0ae51e19-07c8-4e4b-bb6d-648ee58410f4/oauth2/v2.0/token`
- **API Endpoint**: `https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/chat/retrieval-augmented`
- **Proxy Configuration**:
  - Docker: `host.docker.internal:3129` (local proxy)
  - Direct: `rb-proxy-de.bosch.com:8080` (Bosch corporate proxy)
  - NO_PROXY: `localhost,127.0.0.1,*.bosch.com,*.bosch.tech`
- **Scope**: `api://dia-brain/.default`


## Troubleshooting

### Authentication Issues

- **"CLIENT_SECRET environment variable is required"**:
  - Verify CLIENT_SECRET is set in your mcp.json or environment
  - Check that the secret is not expired (expires every 180 days)
  - Follow [DIA Brain REST API Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain) to create Azure app and generate new credentials

- **401 MessageBlocked Error**:
  - Your user account hasn't connected this application to Brain
  - Go to: https://brain.prd.dia-apps.bosch.tech/brains
  - Click user menu → 'API Integration' → Enter application ID → Submit
  - If still failing, request app whitelisting: https://forms.office.com/e/K3gHBLbcbh

- **Authentication Failed (HTTP 401/400)**:
  - Verify CLIENT_SECRET is correct and not expired
  - Check CLIENT_ID matches the application ID (default: `YOUR_DEFAULT_CLIENT_ID`)
  - Ensure you have network access to login.microsoftonline.com

### Connection Issues

- **"Failed to connect to DIA Brain API"**:
  - Verify you're on the Bosch network or connected via VPN
  - Check proxy configuration matches your network requirements (HTTP_PROXY, HTTPS_PROXY)
  - Ensure firewall rules allow access to ews-emea.api.bosch.com

- **SSL/TLS Errors**:
  - Verify SSL_VERIFY is set correctly (default: true)
  - Check your network's SSL/TLS configuration
  - Contact IT support if corporate proxy is interfering

### Query Issues

- **Query Timeouts**:
  - Queries have a 60-second timeout limit
  - Complex queries may take longer - consider breaking them into smaller queries
  - Check your network latency to the API endpoint

- **Empty or No Results**:
  - Verify the brain_id is correct for your knowledge base
  - Check that SharePoint site IDs or Docupedia space IDs are valid
  - Ensure you have access permissions to the specified knowledge bases

- **Permission Errors**:
  - Verify you have access to the knowledge base
  - Check that your app is properly configured and whitelisted
  - Confirm your user account has the necessary permissions

## Further Information

- [DIA BRAIN - User Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/3693697491/DIA+BRAIN+-+User+Documentation) - Main documentation hub
- [DIA Brain REST API Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain)
- [Add Brain Documentation](https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414244/Add+Brain) - Guide for creating custom knowledge bases
- [DIA Brain Portal](https://brain.prd.dia-apps.bosch.tech/brains)
- [API Integration Setup](https://brain.prd.dia-apps.bosch.tech/brains) (User Menu → API Integration)
- [Application Whitelisting Request Form](https://forms.office.com/e/K3gHBLbcbh)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
