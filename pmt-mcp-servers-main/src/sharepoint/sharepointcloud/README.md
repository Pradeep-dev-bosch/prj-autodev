# SharePoint MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Microsoft SharePoint Online.

## Overview

The SharePoint MCP Server provides comprehensive integration with SharePoint Online sites. It exposes a rich set of tools for managing files, folders, lists, and site operations directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the SharePoint REST API through the `office365-rest-python-client` library.

### Limitations

- Only supports username/password authentication (UserCredential method)
- SharePoint on-premises is not supported
- Some operations require full server relative paths
- Accuracy may vary depending on the LLM model used. For best performance and results, it is recommended to use advanced models such as GPT-4.1, GPT-5, or Claude Sonnet 4.5.

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../../README.md#access-to-pmt-artifactory-repository))
- Access to a SharePoint Online site
- Valid SharePoint username and password

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file './vscode/mcp.json'. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding './vscode/mcp.json'. It is ready to use now.

Check out the [`../../README.md`](../../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Configuration

**Security Note:** Credentials are securely provided via input prompts when the MCP server is first configured - they are not stored in configuration files. VS Code will prompt you for your username and password the first time you start the server, ensuring sensitive information remains protected.

#### Proxy Configuration

**IMPORTANT for Corporate Networks:**

The SharePoint MCP server is designed to work correctly in corporate environments with proxy requirements. The provided `mcp.json` configuration explicitly disables proxy at runtime by setting:
- `HTTP_PROXY=""`, `HTTPS_PROXY=""`, `http_proxy=""`, `https_proxy=""`
- `NO_PROXY="*"`, `no_proxy="*"`

**Why proxy is disabled:** SharePoint Online (*.sharepoint.com) authentication will FAIL if routed through a corporate proxy. The proxy blocks the OAuth/authentication flow required for SharePoint Online access.

**Note:** The Docker image from Artifactory is pre-built with all required Python packages already installed, so you don't need proxy settings to download dependencies at runtime. Simply use the configuration from `mcp.json` as-is.

If you experience authentication errors like `'NoneType' object has no attribute 'text'`, verify that proxy settings are disabled in your runtime configuration.

### Usage Examples

Once connected to an MCP-compatible client, you can interact with SharePoint using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "List all files in the Shared Documents folder"
- "Search for files containing 'budget'"
- "Download the latest version of report.docx"
- "Upload myfile.pdf to the Documents folder"
- "Show me all SharePoint lists in the site"
- "Get the items from the Tasks list"

The AI assistant will translate these natural language requests into actual API requests and execute them in SharePoint.

### Features

The server provides the following MCP tools for comprehensive SharePoint management:

- **File Management**:
  - `upload_sharepoint_file` - Upload a file to SharePoint
  - `download_sharepoint_file` - Download a file from SharePoint
  - `delete_sharepoint_file` - Delete a file from SharePoint
  - `move_sharepoint_file` - Move a file from one folder to another
  - `copy_sharepoint_file` - Copy a file to another folder
  - `rename_sharepoint_file` - Rename a file in SharePoint
  - `get_sharepoint_file_metadata` - Get metadata for a SharePoint file
  - `get_file_versions` - Get version history of a SharePoint file
  - `restore_file_version` - Restore a previous version of a SharePoint file
  - `bulk_upload_files` - Upload multiple files to a SharePoint folder
  - `bulk_download_files` - Download multiple files from SharePoint to a local directory
  - `read_file_content` - Read the content of a file from SharePoint as text
  - `zip_and_download_folder` - Zip the contents of a SharePoint folder and download the zip file
  - `get_recent_files` - Get the most recently modified files in a SharePoint folder
  - `get_file_by_id` - Retrieve a file using its unique SharePoint ID

- **Folder Management**:
  - `create_sharepoint_folder` - Create a folder in SharePoint
  - `delete_sharepoint_folder` - Delete a folder from SharePoint
  - `rename_folder` - Rename a folder in SharePoint
  - `move_folder` - Move a folder to another location in SharePoint
  - `copy_folder` - Copy a folder to another location in SharePoint, including the folder itself
  - `list_items_in_sharepoint_folder` - List all items (files and folders) in a SharePoint folder
  - `get_folder_permissions` - Get permissions for a specific folder in SharePoint

- **Search Operations**:
  - `search_sharepoint` - Search across entire SharePoint site for files and/or folders

- **Site Management**:
  - `list_sharepoint_sites` - List accessible SharePoint sites
  - `get_sharepoint_site_info` - Get detailed information about a SharePoint site
  - `list_sharepoint_site_contents` - List all contents (files, folders, and lists) of a SharePoint site

- **List Management**:
  - `create_sharepoint_list` - Create a new SharePoint list
  - `fetch_sharepoint_lists` - Fetch all available SharePoint lists
  - `fetch_sharepoint_list_content` - Fetch the content (items) of a specific SharePoint list
  - `get_sharepoint_list_link` - Retrieve the URL of a specific SharePoint list by its name
  - `get_list_schema` - Get complete schema structure of a SharePoint list including all fields/columns
  - `add_list_item` - Add a new item to a SharePoint list
  - `update_list_item` - Update an existing item in a SharePoint list
  - `delete_list_item` - Delete an item from a SharePoint list
  - `add_list_column` - Add a new field/column to a SharePoint list
  - `update_list_column` - Update properties of an existing field/column in a SharePoint list
  - `delete_list_column` - Delete a field/column from a SharePoint list
  - `export_list_to_csv` - Export the contents of a SharePoint list to a CSV file

- **Recycle Bin Operations**:
  - `get_recycle_bin_items` - Get items in the SharePoint recycle bin
  - `restore_recycle_bin_item` - Restore an item from the SharePoint recycle bin to its original location
  - `restore_all_recycle_bin_items` - Restore all items from the SharePoint recycle bin to their original locations
  - `delete_recycle_bin_item` - Permanently delete an item from the SharePoint recycle bin
  - `empty_recycle_bin` - Empty the SharePoint recycle bin (permanently delete all items)

- **User & Permissions**:
  - `get_current_user_info` - Get detailed information about the current authenticated user


### Troubleshooting

#### Connection Issues
- **"Failed to connect to SharePoint"**: Verify `SHAREPOINT_SITE_URL`, `SHAREPOINT_USERNAME`, and `SHAREPOINT_PASSWORD` are correct
- **Authentication failures**: Check if username and password are valid. **CRITICAL**: Ensure proxy settings are disabled at runtime (see Proxy Configuration section)
- **Permission errors**: Ensure user has necessary site and folder permissions
- **`'NoneType' object has no attribute 'text'`**: This error indicates authentication failure, typically caused by proxy blocking SharePoint Online authentication. Remove all proxy environment variables from your runtime configuration

#### Common Errors
- **"Site not found"**: Verify site URL is correct and accessible - use `list_sharepoint_sites` to list available sites
- **"File not found"**: Check file path and access permissions - use `search_sharepoint` to find files
- **"Folder not found"**: Verify folder path exists and you have access permissions
- **"Full paths required"**: Most operations require full server relative paths starting with `/` (e.g., `/sites/mysite/Shared Documents/file.txt`)
- **"Invalid URL"**: Ensure `SHAREPOINT_SITE_URL` includes the protocol (https://) and correct hostname

## Further Information

- [SharePoint REST API Documentation](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/get-to-know-the-sharepoint-rest-service)
- [office365-rest-python-client](https://github.com/vgrem/Office365-REST-Python-Client)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
