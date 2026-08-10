# SharePoint On-Premises MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides comprehensive SharePoint On-Premises integration for files, folders, and site management.

## Overview

The SharePoint On-Premises MCP Server provides complete integration with SharePoint On-Premises sites. It exposes 28 specialized tools for managing files, folders, search, permissions, and site operations directly inside MCP-enabled clients (e.g., VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the SharePoint REST API with NTLM authentication for secure access.

### Limitations

- Only supports NTLM authentication (Windows domain credentials)
- SharePoint Online is not supported (use the SharePoint Online MCP server instead)
- Some operations require full server relative paths starting with '/'
- List management features are not available in this version
- Direct folder move across directories is not supported by SharePoint REST API - use download + upload workflow
- Depending on the LLM models, accuracy might differ. Premium models like GPT-4+ or Claude Sonnet 4.5 are recommended for better performance and results with complex SharePoint operations

## Getting Started

### Prerequisites

- GitHub Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ) (for Windows users)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-docker-artifactory-repository))
- SharePoint On-Premises server access
- Valid Windows domain credentials (NTID and password) for NTLM authentication

### Authentication Setup

The SharePoint On-Premises MCP server uses NTLM authentication with Windows domain credentials:

1. **Prepare Domain Credentials**
   - Ensure you have valid Windows domain credentials
   - NTID format: `NTID` or `DOMAIN\NTID`
   - Password: Your Windows domain password

2. **Configure Credentials in mcp.json**
   - Set `SHAREPOINT_SITE_URL` to your SharePoint On-Premises site URL
   - Use `${input:sharepoint-onprem-user}` for username (prompted securely)
   - Use `${input:sharepoint-onprem-pass}` for password (prompted securely)

3. **Important Notes:**
   - ✅ Credentials are securely provided via input prompts when the MCP server is first configured
   - ✅ Credentials are not stored in configuration files
   - ✅ VS Code will prompt you for your username and password the first time you start the server
   - ✅ Ensure the user account has appropriate SharePoint site and folder permissions via Active Directory/domain groups

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

**Important for Docker Users:**
The Docker configuration includes a volume mount for SSL certificates:
```
-v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro
```
This mounts your system's CA certificates into the container, enabling secure SSL connections to SharePoint instances with corporate/custom SSL certificates. This is the industry-standard approach for Docker in corporate environments and allows SSL verification to remain enabled (secure by default).

Start the Docker version MCP server after adding `.vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `SHAREPOINT_SITE_URL` | SharePoint On-Premises site URL | ✅ Yes | `https://sharepoint.company.com/sites/yoursite` |
| `SHAREPOINT_USERNAME` | Windows domain NTID | ✅ Yes | `NTID` or `DOMAIN\NTID` |
| `SHAREPOINT_PASSWORD` | Windows domain password | ✅ Yes | Prompted securely via `${input:sharepoint-onprem-pass}` |
| `CERTIFICATE_PATH` | SSL certificate override: leave unset for Docker (auto-mounted), set path for custom certs, or "false" to disable SSL | No | Not needed for Docker, `/path/to/custom-ca.crt`, or `"false"` |
| `TRANSPORT` | MCP transport protocol | No | `stdio` (default), `http`, `sse` |
| `HOST` | Server host address (if not using stdio) | No | `127.0.0.1` (default) |
| `HOST_PORT` | Server port (if not using stdio) | No | `8000` (default) |

**Note:** When using the provided `mcp.json` configuration, set the environment variables as shown in the example configuration file.

#### SSL/TLS Certificate Configuration

SSL certificate validation is configured differently for Docker vs Python modes:

**Docker Mode (Recommended)**
- ✅ **Automatic**: System certificates are mounted via volume in `mcp.json`
- ✅ **No configuration needed**: The volume mount `-v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro` handles corporate/custom CAs
- ✅ **Most secure**: SSL verification enabled by default with your system's trusted certificates
- **Override only if needed**:
  - Set `CERTIFICATE_PATH="false"` to disable SSL verification (dev/test only)
  - Set `CERTIFICATE_PATH="/custom/path"` to use a different certificate file

**Python Mode (uv/Direct Python)**
- **Default**: Uses Python's certifi certificate bundle (standard trusted CAs)
- **Custom certificates**: Set `CERTIFICATE_PATH` to path of your corporate CA bundle file
  - Example: `"CERTIFICATE_PATH": "/etc/ssl/certs/ca-certificates.crt"`
  - Required if SharePoint uses self-signed or corporate CA not in certifi bundle
- **Disable SSL** (dev/test only): Set `CERTIFICATE_PATH="false"`
  - ⚠️ **Warning**: Vulnerable to man-in-the-middle attacks - never use in production

**Summary**:
- **Docker users**: No CERTIFICATE_PATH needed - volume mount handles everything
- **Python users**: Set CERTIFICATE_PATH only if using custom corporate certificates or need to disable SSL

#### Configuration Examples

**Example 1: Docker Mode - Standard Setup (Recommended)**
```json
{
  "SHAREPOINT_SITE_URL": "https://sharepoint.company.com/sites/myproject",
  "SHAREPOINT_USERNAME": "${input:sharepoint-onprem-user}",
  "SHAREPOINT_PASSWORD": "${input:sharepoint-onprem-pass}"
}
```
*No CERTIFICATE_PATH needed - volume mount in mcp.json handles certificates*

**Example 2: Python Mode - Custom Corporate Certificate**
```json
{
  "SHAREPOINT_SITE_URL": "https://sharepoint-internal.company.com/sites/myproject",
  "SHAREPOINT_USERNAME": "${input:sharepoint-onprem-user}",
  "SHAREPOINT_PASSWORD": "${input:sharepoint-onprem-pass}",
  "CERTIFICATE_PATH": "/etc/ssl/certs/ca-certificates.crt"
}
```
*Required for Python mode when SharePoint uses corporate/custom SSL certificates*

**Example 3: Disable SSL Verification (Dev/Test Only)**
```json
{
  "SHAREPOINT_SITE_URL": "https://localhost:8443/sites/devsite",
  "SHAREPOINT_USERNAME": "${input:sharepoint-onprem-user}",
  "SHAREPOINT_PASSWORD": "${input:sharepoint-onprem-pass}",
  "CERTIFICATE_PATH": "false"
}
```
⚠️ **Warning**: Only use `CERTIFICATE_PATH="false"` for local development/testing. Never in production!

### Usage Examples

Once connected to an MCP-compatible client, you can interact with SharePoint On-Premises using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Check if I can access the SharePoint site"
- "List all files in the Documents folder"
- "Search for files containing 'budget' in the name"
- "Download the file report.docx from Documents"
- "Upload myfile.pdf to the Documents/Reports folder"
- "Show me the SharePoint site information"
- "Get the most recent 5 files from the Documents folder"
- "What's the total size of the Archive folder?"
- "Create a new folder called 'Q1-2024' in Documents"
- "Move file.txt from Documents to Archive"
- "Get the SharePoint link for the Reports folder"
- "Show me what's in the recycle bin"
- "List all available SharePoint sites"

The AI assistant will translate these natural language requests into actual SharePoint REST API requests and execute them.

### Features

The server provides comprehensive SharePoint On-Premises integration capabilities with 28 specialized MCP tools covering:

- File and folder downloading/uploading (single and bulk operations)
- Advanced search and filtering capabilities
- File and folder metadata and permissions management
- Site and user information retrieval
- Recycle bin operations

The following MCP tools are available for comprehensive SharePoint On-Premises management:

The following MCP tools are available for comprehensive SharePoint On-Premises management:

- **File Operations**:
  - `download_sharepoint_file` - Download a file from SharePoint to local storage
  - `upload_sharepoint_file` - Upload a file to SharePoint from local storage
  - `read_file_content` - Read the content of a file from SharePoint as text
  - `get_file_properties` - Get detailed properties and metadata of a SharePoint file
  - `get_recent_files` - Get the most recently modified files in a SharePoint folder
  - `bulk_download_sharepoint` - Download multiple files and/or folders from SharePoint in bulk
  - `bulk_upload_sharepoint` - Upload multiple files to SharePoint in bulk

- **Folder Operations**:
  - `download_sharepoint_folder` - Download an entire SharePoint folder recursively with all files and subfolders
  - `upload_sharepoint_folder` - Recursively upload a local folder with all contents to SharePoint
  - `create_sharepoint_folder` - Create a new empty folder in SharePoint
  - `list_sharepoint_folder` - List all items (files and folders) in a SharePoint folder with filtering
  - `list_all_folders_recursive` - Recursively list all folders in SharePoint starting from a given folder
  - `get_folder_properties` - Get detailed properties and metadata of a SharePoint folder
  - `get_folder_size` - Calculate the total size of all files in a folder and subfolders
  - `download_and_zip_folder` - Download a SharePoint folder and create a ZIP archive locally

- **Item Operations** (Files & Folders):
  - `update_sharepoint_item` - Rename or move a file/folder in SharePoint
  - `delete_sharepoint_item` - Delete a file or folder from SharePoint
  - `copy_sharepoint_item` - Copy a file from one location to another in SharePoint
  - `get_sharepoint_link` - Get the direct SharePoint link for a file or folder
  - `get_item_permissions` - Get permissions and role assignments for a file or folder

- **Search Operations**:
  - `search_sharepoint` - Deep search for folders and/or files in SharePoint by name across the entire site

- **Site Operations**:
  - `check_sharepoint_access` - Check connectivity to SharePoint site using NTLM authentication
  - `get_site_info` - Get comprehensive information about the SharePoint site
  - `list_sharepoint_sites` - List all SharePoint sites accessible to the current user
  - `list_sharepoint_site_contents` - List all contents of the SharePoint site (libraries, folders, files, lists)
  - `get_current_user_info` - Get detailed information about the current authenticated user

- **Recycle Bin Operations**:
  - `list_recycle_bin_items` - List all items in the SharePoint recycle bin
  - `restore_recycle_bin_item` - Restore an item from the SharePoint recycle bin by ID
  - `empty_recycle_bin` - Permanently delete all items from the SharePoint recycle bin

### Troubleshooting

#### Authentication Issues
- **401 Unauthorized:** Invalid credentials - verify NTID and password are correct
- **NTLM Authentication Failures:**
  - Ensure NTID is in correct format: `NTID` or `DOMAIN\NTID`
  - Verify Windows domain credentials are valid and not expired
  - Check if NTLM authentication is enabled on the SharePoint server
  - Ensure account is not locked or disabled in Active Directory
- **403 Forbidden:** Insufficient permissions - ensure user has required SharePoint site permissions via Active Directory/domain groups
- **Credentials Stored Incorrectly:** Use `${input:sharepoint-onprem-user}` and `${input:sharepoint-onprem-pass}` in mcp.json for secure credential prompts

#### Connection Issues
- **Cannot Connect to SharePoint:** Verify `SHAREPOINT_SITE_URL` is correct and accessible from your network
- **Network Timeout:** Check proxy settings if running in corporate environment
- **SSL/TLS Certificate Errors:**
  - **Docker Mode:** Certificates are auto-mounted via volume in mcp.json
    - If SSL errors occur, verify `/etc/ssl/certs/ca-certificates.crt` exists on your host system
    - Corporate CA certificates should be in your system's CA bundle
    - For custom certs, update your system CA bundle or set `CERTIFICATE_PATH` to override
  - **Python Mode:** Set `CERTIFICATE_PATH` to your CA certificate bundle path
    - Example: `CERTIFICATE_PATH="/etc/ssl/certs/ca-certificates.crt"`
    - Required when SharePoint uses self-signed or corporate CA certificates
  - **Dev/Test Only:** Set `CERTIFICATE_PATH="false"` to disable SSL verification (⚠️ not secure)
  - Ensure the SharePoint server's SSL certificate is valid and not expired
- **Firewall Blocking:** Check network firewall rules and corporate proxy settings
- **Site Not Found (404):** Verify site URL is correct and accessible - use `check_sharepoint_access` to test connectivity

#### File and Folder Operations
- **File Not Found:** Check file path and access permissions - use `search_sharepoint` to locate files
- **Folder Not Found:** Verify folder path exists and you have access permissions - use `list_sharepoint_folder` to explore
- **Path Format Issues:**
  - Most operations require full server relative paths starting with `/` (e.g., `/sites/mysite/Documents/file.txt`)
  - Use forward slashes `/` not backslashes `\` in paths
  - Ensure paths are URL-encoded if they contain special characters or spaces
- **Upload Failed:** Check folder exists and you have write permissions
- **Download Failed:** Verify file exists and you have read permissions
- **Cannot Move Folder:** Direct folder move across directories is not supported by SharePoint REST API - use download + upload workflow instead

#### Permission Issues
- **Cannot Create Folder:** User needs contribute permissions or higher on the target library
- **Cannot Delete Item:** User needs delete permissions or higher, or must be the item owner
- **Cannot Update Item:** User needs edit permissions or higher on the item
- **Cannot Access Site Contents:** User may not have appropriate site permissions - contact site administrator
- **Recycle Bin Operations Failed:** User needs site collection administrator or full control permissions

#### Common Errors
- **Invalid URL Format:** Ensure `SHAREPOINT_SITE_URL` includes the protocol (https://) and correct hostname
- **Item Already Exists:** File or folder with same name already exists at destination - rename or delete existing item first
- **Path Too Long:** SharePoint has path length limitations - use shorter folder structures or file names
- **Special Characters in Names:** Some characters are not allowed in file/folder names (e.g., `\ / : * ? " < > | #`)
- **Operation Timeout:** Large files or slow networks may timeout - increase `timeout_seconds` parameter if available
- **REST API Limitations:** Some advanced operations require specific SharePoint versions or service packs

## Further Information

- [SharePoint REST API Documentation](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
- [SharePoint On-Premises REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/complete-basic-operations-using-sharepoint-rest-endpoints)
- [NTLM Authentication](https://learn.microsoft.com/en-us/windows/win32/secauthn/microsoft-ntlm)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
