# SharePoint On-Prem MCP Server
# Implements MCP tools for SharePoint On-Premises using NTLM authentication

import os
import logging
from pathlib import Path
import requests
from requests_ntlm import HttpNtlmAuth
from fastmcp import FastMCP

# MCP server initialization
mcp = FastMCP("sharepointonprem")


# Auth / Client
sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL", "")
sp_username = os.getenv("SHAREPOINT_USERNAME", "")
sp_password = os.getenv("SHAREPOINT_PASSWORD", "")

if not sharepoint_site_url or not sp_username or not sp_password:
    raise ValueError(
        "Missing required environment variables: SHAREPOINT_SITE_URL, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD"
    )

SHAREPOINT_SITE = sharepoint_site_url
SHAREPOINT_USERNAME = sp_username
SHAREPOINT_PASSWORD = sp_password

# SSL Verification Configuration
# CERTIFICATE_PATH environment variable controls SSL verification:
#   - File path (e.g., /etc/ssl/certs/ca-certificates.crt) → Uses that certificate file
#   - "false" / "disable" / "off" / "no" → Disables SSL verification (dev/test only)
#   - Not set / Empty string → Checks if volume-mounted cert exists, otherwise uses certifi
CERTIFICATE_PATH = os.getenv("CERTIFICATE_PATH", "")

# Determine verify parameter for requests
if CERTIFICATE_PATH and CERTIFICATE_PATH.lower() in ["false", "disable", "off", "no"]:
    SSL_VERIFY_PARAM = False  # Disable SSL verification
elif CERTIFICATE_PATH:
    SSL_VERIFY_PARAM = CERTIFICATE_PATH  # Use specified certificate file
else:
    # Check if certificate is mounted via Docker volume
    if os.path.exists("/etc/ssl/certs/ca-certificates.crt"):
        SSL_VERIFY_PARAM = "/etc/ssl/certs/ca-certificates.crt"
    else:
        SSL_VERIFY_PARAM = True  # Use default certifi bundle


def _get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.
    Returns:
            tuple[str, str, int]: A tuple containing:
                    - transport_type (str): Transport protocol type, defaults to "stdio"
                    - host (str): Server host address, defaults to "127.0.0.1"
                    - port (int): Server port number, defaults to "8000"
    """
    transport = os.getenv("TRANSPORT") or "stdio"
    if transport in ["stdio", "<TRANSPORT>", None, "", "-", "null"]:
        logging.info("MCP init: transport=stdio")
        return ("stdio", "", 0)

    host = os.getenv("HOST") or "127.0.0.1"
    port_str = os.getenv("HOST_PORT") or "8000"
    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(
            f"Invalid PORT env variable: '{port_str}' - must be a valid integer"
        )
    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def _ntlm_auth():
    if not SHAREPOINT_USERNAME or not SHAREPOINT_PASSWORD:
        raise ValueError(
            "Missing NTLM credentials: SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD"
        )
    return HttpNtlmAuth(SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD)


def _get_headers():
    return {"Accept": "application/json;odata=verbose"}


@mcp.tool()
def check_sharepoint_access(timeout_seconds: int = 10) -> dict:
    """Check connectivity to SharePoint site using NTLM authentication."""
    try:
        response = requests.get(
            SHAREPOINT_SITE,
            auth=_ntlm_auth(),
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )
        if response.ok:
            return {
                "success": True,
                "status_code": response.status_code,
                "message": "Successfully accessed SharePoint site.",
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def download_sharepoint_file(
    file_url: str, save_as: str = "", timeout_seconds: int = 60
) -> dict:
    """
    Download a file from SharePoint using NTLM authentication.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - file_url MUST be a full URL starting with 'https://' (e.g., https://sharepoint.com/sites/xxx/Documents/file.pdf)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a filename (e.g., "camserv.log") and NOT the full URL:
    1. FIRST call search_sharepoint(search_query="filename", search_type="file") to find the file
    2. From the search results, get the 'server_relative_url' field (e.g., /sites/xxx/Documents/folder/file.pdf)
    3. Construct the full URL by combining the SharePoint site base URL with the server_relative_url
    4. THEN call this download_sharepoint_file tool with the full URL

    DO NOT call this tool with just a filename - it will fail!

    Args:
            file_url (str): Full URL to the file (must start with 'https://').
                    Example: https://sites.inside-share5.bosch.com/sites/190445/Documents/test_mcp/camserv.log
            save_as (str): Local filename to save as. If empty, extracts filename from the URL.
            timeout_seconds (int): Download timeout in seconds (default: 60).

    Returns:
            dict: Success status, file URL, and local path where file was saved.
    """
    try:
        # Extract filename from URL if save_as is not provided
        if not save_as:
            save_as = file_url.split("/")[-1]

        response = requests.get(
            file_url,
            auth=_ntlm_auth(),
            stream=True,
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )
        if response.status_code != 200:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
        local_path = Path(save_as)
        with local_path.open("wb") as local_file:
            local_file.write(response.content)
        return {"success": True, "file_url": file_url, "saved_as": str(local_path)}
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def download_sharepoint_folder(
    folder_path: str, local_base_path: str = ".", timeout_seconds: int = 60
) -> dict:
    """
    Download an entire SharePoint folder recursively with all files and subfolders.
    Preserves the folder structure locally.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - folder_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a folder name (e.g., "deep_tool") and NOT the full path:
    1. FIRST call search_sharepoint(search_query="foldername", search_type="folder") to find the folder
    2. From the search results, get the 'server_relative_url' field (e.g., /sites/xxx/Documents/test_mcp/deep_tool)
    3. THEN call this download_sharepoint_folder tool with that server_relative_url

    DO NOT call this tool with just a folder name - it will fail!

    Args:
            folder_path (str): Server-relative path to the folder (must start with '/').
                    Example: /sites/190445/Documents/test_mcp/deep_tool
            local_base_path (str): Local directory to save the folder (default: current directory).
            timeout_seconds (int): Download timeout in seconds per file (default: 60).

    Returns:
            dict: Success status, total files downloaded, folder structure, and any errors encountered.
    """

    def download_folder_recursive(
        sp_folder_path: str, local_folder_path: Path, stats: dict
    ):
        """Recursively download all files and subfolders"""
        try:
            # Create local folder if it doesn't exist
            local_folder_path.mkdir(parents=True, exist_ok=True)

            # Get all files in current folder
            api_url_files = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{sp_folder_path}')/Files"
            response_files = requests.get(
                api_url_files,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )

            if response_files.ok:
                files = response_files.json()["d"]["results"]
                for file in files:
                    try:
                        # Use the proper file download endpoint
                        server_relative_url = file["ServerRelativeUrl"]
                        file_url = (
                            f"{SHAREPOINT_SITE}/_api/web/"
                            f"GetFileByServerRelativeUrl('{server_relative_url}')/$value"
                        )
                        file_name = file["Name"]
                        local_file_path = local_folder_path / file_name

                        # Download file
                        response = requests.get(
                            file_url,
                            auth=_ntlm_auth(),
                            stream=True,
                            timeout=timeout_seconds,
                            verify=SSL_VERIFY_PARAM,
                        )

                        if response.status_code == 200:
                            with local_file_path.open("wb") as f:
                                f.write(response.content)
                            stats["files_downloaded"] += 1
                            file_size = (
                                int(file.get("Length", 0)) if file.get("Length") else 0
                            )
                            stats["total_bytes"] += file_size
                            stats["downloaded_files"].append(
                                {
                                    "name": file_name,
                                    "path": str(local_file_path),
                                    "size_bytes": file_size,
                                }
                            )
                        else:
                            stats["errors"].append(
                                f"Failed to download {file_name}: {response.reason}"
                            )
                    except Exception as e:
                        stats["errors"].append(
                            f"Error downloading {file.get('Name', 'unknown')}: {str(e)}"
                        )

            # Get all subfolders
            api_url_folders = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{sp_folder_path}')/Folders"
            response_folders = requests.get(
                api_url_folders,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )

            if response_folders.ok:
                folders = response_folders.json()["d"]["results"]
                for folder in folders:
                    # Skip system folders
                    if folder["Name"] not in ["Forms", "_catalogs", "_private"]:
                        subfolder_path = folder["ServerRelativeUrl"]
                        local_subfolder_path = local_folder_path / folder["Name"]
                        stats["folders_created"] += 1
                        # Recursively download subfolder
                        download_folder_recursive(
                            subfolder_path, local_subfolder_path, stats
                        )

        except Exception as e:
            stats["errors"].append(f"Error accessing folder {sp_folder_path}: {str(e)}")

    try:
        # Extract folder name from path
        folder_name = folder_path.split("/")[-1]

        # Initialize statistics
        stats = {
            "files_downloaded": 0,
            "folders_created": 0,
            "total_bytes": 0,
            "downloaded_files": [],
            "errors": [],
        }

        # Create base local path
        local_base = Path(local_base_path)
        local_folder = local_base / folder_name

        # Start recursive download
        download_folder_recursive(folder_path, local_folder, stats)

        # Convert bytes to human-readable
        def human_readable_size(size_bytes):
            for unit in ["B", "KB", "MB", "GB", "TB"]:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024.0

        return {
            "success": True,
            "folder_path": folder_path,
            "local_path": str(local_folder),
            "files_downloaded": stats["files_downloaded"],
            "folders_created": stats["folders_created"],
            "total_size_bytes": stats["total_bytes"],
            "total_size_readable": human_readable_size(stats["total_bytes"]),
            "downloaded_files": stats["downloaded_files"],
            "errors": stats["errors"],
            "has_errors": len(stats["errors"]) > 0,  # type: ignore[arg-type]
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def read_file_content(
    file_url: str, encoding: str = "utf-8", timeout_seconds: int = 60
) -> dict:
    """
    Read the content of a file from SharePoint as text.

    Args:
            file_url (str): Server-relative path to the file (e.g., /sites/xxx/Documents/folder/file.txt).
            encoding (str): Text encoding to use (default: "utf-8").
            timeout_seconds (int): Request timeout in seconds (default: 60).

    Returns:
            dict: Success status, file path, and file content as text.
    """
    try:
        # Use SharePoint REST API endpoint for file content
        api_url = f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{file_url}')/$value"
        response = requests.get(
            api_url,
            auth=_ntlm_auth(),
            stream=True,
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )
        if response.status_code != 200:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
        content = response.content.decode(encoding)
        return {"success": True, "file_url": file_url, "content": content}
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def search_sharepoint(search_query: str, search_type: str = "both") -> dict:
    """
    Deep search for folders and/or files in SharePoint by name across the entire site.
    Performs a recursive search through all folders and subfolders.

    Args:
            search_query (str): The name of the folder or file to search for (supports partial matches).
            search_type (str): "both", "file", or "folder". Default is "both" to search everything.

    Returns:
            dict: Search results with type indicators (file/folder) and server_relative_url for each match.
    """

    def search_files_recursive(folder_path: str, query: str, matches: list):
        """Recursively search for files in all folders"""
        try:
            # Search files in current folder
            api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Files"
            response = requests.get(
                api_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            if response.ok:
                files = response.json()["d"]["results"]
                for file in files:
                    # Case-insensitive partial match
                    if query.lower() in file["Name"].lower():
                        matches.append(
                            {
                                "type": "file",
                                "name": file["Name"],
                                "server_relative_url": file["ServerRelativeUrl"],
                                "folder_path": folder_path,
                                "size_bytes": file.get("Length"),
                                "time_last_modified": file.get("TimeLastModified"),
                            }
                        )

            # Get subfolders and search recursively
            api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Folders"
            response = requests.get(
                api_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            if response.ok:
                folders = response.json()["d"]["results"]
                for folder in folders:
                    # Skip system folders
                    if folder["Name"] not in ["Forms", "_catalogs", "_private"]:
                        search_files_recursive(
                            folder["ServerRelativeUrl"], query, matches
                        )
        except Exception as e:
            logging.warning(f"Error searching in folder {folder_path}: {str(e)}")

    def search_folders_recursive(folder_path: str, query: str, matches: list):
        """Recursively search for folders"""
        try:
            api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Folders"
            response = requests.get(
                api_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            if response.ok:
                folders = response.json()["d"]["results"]
                for folder in folders:
                    # Case-insensitive partial match
                    if query.lower() in folder["Name"].lower():
                        matches.append(
                            {
                                "type": "folder",
                                "name": folder["Name"],
                                "server_relative_url": folder["ServerRelativeUrl"],
                                "item_count": folder.get("ItemCount", 0),
                            }
                        )
                    # Skip system folders for recursion
                    if folder["Name"] not in ["Forms", "_catalogs", "_private"]:
                        search_folders_recursive(
                            folder["ServerRelativeUrl"], query, matches
                        )
        except Exception as e:
            logging.warning(f"Error searching folders in {folder_path}: {str(e)}")

    try:
        matches: list[dict] = []

        # Search based on type
        if search_type == "file":
            search_files_recursive("Documents", search_query, matches)
        elif search_type == "folder":
            search_folders_recursive("Documents", search_query, matches)
        else:  # "both" or any other value
            # Search both files and folders
            search_files_recursive("Documents", search_query, matches)
            search_folders_recursive("Documents", search_query, matches)

        if matches:
            # Separate results by type for clarity
            files = [m for m in matches if m.get("type") == "file"]
            folders = [m for m in matches if m.get("type") == "folder"]

            return {
                "success": True,
                "search_query": search_query,
                "search_type": search_type,
                "results_found": len(matches),
                "files_found": len(files),
                "folders_found": len(folders),
                "results": matches,
                "server_relative_url": matches[0][
                    "server_relative_url"
                ],  # For backward compatibility
            }
        else:
            return {"success": False, "message": "No results found."}
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def list_sharepoint_folder(folder_path: str = "Documents") -> dict:
    """
    List all items (files and folders) in a SharePoint folder.
    This is a smart tool that works with folder names, partial paths, or full paths.

    FLEXIBLE INPUT - THIS TOOL IS SMART:
    - Empty or "Documents": Lists root Documents library
    - Just folder name (e.g., "test_mcp"): Automatically searches SharePoint and lists that folder
    - Full server-relative path (e.g., "/sites/xxx/Documents/test_mcp"): Lists that specific folder

    Examples:
            list_sharepoint_folder() → Lists root Documents
            list_sharepoint_folder("test_mcp") → Searches for test_mcp folder and lists its contents
            list_sharepoint_folder("/sites/190445/Documents/test_mcp") → Lists specific folder

    Args:
            folder_path (str): Folder name or path to list. Defaults to "Documents" (root).
                    Can be: folder name, partial path, or full server-relative path

    Returns:
            dict: Contents of the folder (files and folders with details).
    """

    def list_folder_contents(path: str) -> dict:
        """Helper to list contents of a folder"""
        try:
            api_url_folders = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{path}')/Folders"
            api_url_files = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{path}')/Files"

            response_folders = requests.get(
                api_url_folders,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            response_folders.raise_for_status()
            folders = response_folders.json()["d"]["results"]

            response_files = requests.get(
                api_url_files,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            response_files.raise_for_status()
            files = response_files.json()["d"]["results"]

            folder_list = []
            for folder in folders:
                if folder["Name"] not in ["Forms", "_catalogs", "_private"]:
                    folder_list.append(
                        {
                            "name": folder["Name"],
                            "type": "folder",
                            "server_relative_url": folder["ServerRelativeUrl"],
                            "item_count": folder.get("ItemCount", 0),
                        }
                    )

            file_list = []
            for file in files:
                file_list.append(
                    {
                        "name": file["Name"],
                        "type": "file",
                        "server_relative_url": file["ServerRelativeUrl"],
                        "size_bytes": file.get("Length"),
                        "time_last_modified": file.get("TimeLastModified"),
                    }
                )

            return {
                "success": True,
                "folder_path": path,
                "folders": folder_list,
                "files": file_list,
                "total_folders": len(folder_list),
                "total_files": len(file_list),
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    try:
        # If it's a full server-relative path (starts with /), use it directly
        if folder_path.startswith("/"):
            return list_folder_contents(folder_path)

        # If it's "Documents" or empty, list root
        if folder_path in ["Documents", "", None]:
            return list_folder_contents("Documents")

        # Otherwise, it's a folder name - search for it recursively
        logging.info(f"Searching for folder: '{folder_path}'")

        def search_folder_recursive(current_path: str, target_name: str) -> str:
            """Recursively search for a folder by name"""
            try:
                api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{current_path}')/Folders"
                response = requests.get(
                    api_url,
                    auth=_ntlm_auth(),
                    headers=_get_headers(),
                    verify=SSL_VERIFY_PARAM,
                )
                if response.ok:
                    folders = response.json()["d"]["results"]
                    for folder in folders:
                        # Skip system folders
                        if folder["Name"] in ["Forms", "_catalogs", "_private"]:
                            continue
                        # Case-insensitive match
                        if folder["Name"].lower() == target_name.lower():
                            return folder["ServerRelativeUrl"]
                        # Recursively search subfolders
                        result = search_folder_recursive(
                            folder["ServerRelativeUrl"], target_name
                        )
                        if result:
                            return result
            except Exception as e:
                logging.warning(f"Error searching in {current_path}: {str(e)}")
            return ""

        # Search for the folder starting from Documents
        found_path = search_folder_recursive("Documents", folder_path)

        if found_path:
            logging.info(f"Found folder at: {found_path}")
            return list_folder_contents(found_path)
        else:
            return {
                "success": False,
                "message": (
                    f"Folder '{folder_path}' not found in SharePoint. "
                    "Try using search_sharepoint tool for partial matches."
                ),
            }

    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_file_properties(file_url: str) -> dict:
    """
    Get detailed properties and metadata of a file from SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - file_url MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder/file.pdf)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a filename (e.g., "cams.log") and NOT the full path:
    1. FIRST call search_sharepoint(search_query="filename", search_type="file") to find the file
    2. From the search results, get the 'server_relative_url' field (e.g., /sites/xxx/Documents/folder/file.pdf)
    3. THEN call this get_file_properties tool with that server_relative_url

    DO NOT call this tool with just a filename - it will fail!

    Args:
            file_url (str): Full server relative path to the file starting with '/'.
                    Example: /sites/190885/Documents/test_mcp/cams.log
    Returns:
            dict: File properties including name, size, created/modified dates, author, etc.
    """
    try:
        api_url = (
            f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{file_url}')"
            "?$expand=Author,ModifiedBy,ListItemAllFields"
        )
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()
        file_data = response.json()["d"]

        properties = {
            "success": True,
            "name": file_data.get("Name"),
            "server_relative_url": file_data.get("ServerRelativeUrl"),
            "size_bytes": file_data.get("Length"),
            "time_created": file_data.get("TimeCreated"),
            "time_last_modified": file_data.get("TimeLastModified"),
            "title": file_data.get("Title"),
            "file_type": file_data.get("Name", "").split(".")[-1]
            if "." in file_data.get("Name", "")
            else "",
        }

        if "Author" in file_data:
            properties["created_by"] = file_data["Author"].get("Title")
        if "ModifiedBy" in file_data:
            properties["modified_by"] = file_data["ModifiedBy"].get("Title")

        return properties
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_folder_properties(folder_url: str) -> dict:
    """
    Get detailed properties and metadata of a folder from SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - folder_url MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a folder name (e.g., "test_mcp") and NOT the full path:
    1. FIRST call search_sharepoint(search_query="foldername", search_type="folder") to find the folder
    2. From the search results, get the 'server_relative_url' field (e.g., /sites/xxx/Documents/test_mcp)
    3. THEN call this get_folder_properties tool with that server_relative_url

    DO NOT call this tool with just a folder name - it will fail!

    Args:
            folder_url (str): Full server relative path to the folder starting with '/'.
                    Example: /sites/19555/Documents/test_mcp/test2/test3
    Returns:
            dict: Folder properties including name, item count, created/modified dates, etc.
    """
    try:
        api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_url}')?$expand=ListItemAllFields"
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()
        folder_data = response.json()["d"]

        properties = {
            "success": True,
            "name": folder_data.get("Name"),
            "server_relative_url": folder_data.get("ServerRelativeUrl"),
            "item_count": folder_data.get("ItemCount"),
            "time_created": folder_data.get("TimeCreated"),
            "time_last_modified": folder_data.get("TimeLastModified"),
        }

        return properties
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def list_all_folders_recursive(start_folder: str = "Documents") -> dict:
    """
    Recursively list all folders in SharePoint starting from a given folder.

    Args:
            start_folder (str): Starting folder path (default: "Documents").
    Returns:
            dict: List of all folder paths found recursively.
    """

    def get_subfolders(folder_path: str, all_folders: list):
        try:
            api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Folders"
            response = requests.get(
                api_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            response.raise_for_status()
            folders = response.json()["d"]["results"]

            for folder in folders:
                folder_url = folder["ServerRelativeUrl"]
                all_folders.append(
                    {
                        "name": folder["Name"],
                        "path": folder_url,
                        "item_count": folder.get("ItemCount", 0),
                    }
                )
                # Recursively get subfolders
                get_subfolders(folder_url, all_folders)
        except Exception as e:
            logging.warning(f"Error accessing folder {folder_path}: {str(e)}")

    try:
        all_folders: list[dict] = []
        get_subfolders(start_folder, all_folders)
        return {
            "success": True,
            "total_folders": len(all_folders),
            "folders": all_folders,
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_recent_files(folder_path: str = "Documents", top: int = 10) -> dict:
    """
    Get the most recently modified files in a folder.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - folder_path MUST be a full server-relative path (e.g., /sites/xxx/Documents/folder)
      or a valid folder under Documents.

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a folder name (e.g., "test_mcp") and NOT the full path:
    1. FIRST call search_sharepoint(search_query="foldername", search_type="folder") to find the folder
    2. From the search results, get the 'server_relative_url' field (e.g., /sites/xxx/Documents/test_mcp)
    3. THEN call this get_recent_files tool with that server_relative_url

    DO NOT call this tool with just a folder name - it may not resolve the correct path!

    Args:
            folder_path (str): Folder path to search in (default: "Documents").
            top (int): Number of recent files to return (default: 10).
    Returns:
            dict: List of recently modified files.
    """
    try:
        api_url = (
            f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Files"
            f"?$orderby=TimeLastModified desc&$top={top}"
        )
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()
        files = response.json()["d"]["results"]

        file_list = []
        for file in files:
            file_list.append(
                {
                    "name": file["Name"],
                    "server_relative_url": file["ServerRelativeUrl"],
                    "size_bytes": file.get("Length"),
                    "time_last_modified": file.get("TimeLastModified"),
                    "time_created": file.get("TimeCreated"),
                }
            )

        return {"success": True, "folder": folder_path, "files": file_list}
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_folder_size(folder_path: str) -> dict:
    """
    Calculate the total size of all files in a folder (non-recursive).

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - folder_path MUST be a full server-relative path (e.g., /sites/xxx/Documents/folder).

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a folder name (e.g., "test") and NOT the full path:
    1. FIRST call search_sharepoint(search_query="foldername", search_type="folder") to find the folder
    2. From the search results, get the 'server_relative_url' field (e.g., /sites/xxx/Documents/test_mcp/test)
    3. THEN call this get_folder_size tool with that server_relative_url

    DO NOT call this tool with just a folder name - it may not resolve the correct path!

    Args:
            folder_path (str): Full server relative path to the folder.
    Returns:
            dict: Total size in bytes and human-readable format.
    """
    try:
        api_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{folder_path}')/Files"
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()
        files = response.json()["d"]["results"]

        # Safely convert file sizes to integers before summing
        total_size = 0
        for file in files:
            length = file.get("Length", 0)
            # Convert string to int if necessary
            if isinstance(length, str):
                total_size += int(length) if length.isdigit() else 0
            else:
                total_size += int(length) if length else 0

        file_count = len(files)

        # Convert to human-readable format
        def human_readable_size(size_bytes):
            for unit in ["B", "KB", "MB", "GB", "TB"]:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.2f} {unit}"
                size_bytes /= 1024.0

        return {
            "success": True,
            "folder_path": folder_path,
            "total_size_bytes": total_size,
            "total_size_readable": human_readable_size(total_size),
            "file_count": file_count,
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Write/Create Operation: Upload File ---
@mcp.tool()
def upload_sharepoint_file(
    local_file_path: str,
    target_folder_path: str,
    overwrite: bool = True,
    timeout_seconds: int = 60,
) -> dict:
    """
    Upload a file (any format, including .zip) to SharePoint using NTLM authentication.

    - target_folder_path: Server-relative path to the target SharePoint folder (must start with '/').
    - local_file_path: Path to the local file to upload (.zip, .txt, .docx, etc.).
    - overwrite: Whether to overwrite if file exists (default: True).
    - timeout_seconds: Upload timeout in seconds (default: 60).

    Returns:
            dict: Success status, uploaded file name, and SharePoint URL.
    """
    try:
        import os

        file_name = os.path.basename(local_file_path)

        # Get form digest token for POST operations
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {
                "success": False,
                "message": "Failed to get form digest token",
                "status_code": digest_response.status_code,
            }
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        overwrite_str = "true" if overwrite else "false"
        api_url = (
            f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{target_folder_path}')"
            f"/Files/add(url='{file_name}',overwrite={overwrite_str})"
        )
        with open(local_file_path, "rb") as f:
            file_content = f.read()
        headers = _get_headers()
        headers["Content-Type"] = "application/octet-stream"
        headers["X-RequestDigest"] = form_digest
        response = requests.post(
            api_url,
            auth=_ntlm_auth(),
            headers=headers,
            data=file_content,
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )
        if response.status_code in [200, 201]:
            result = response.json()["d"]
            return {
                "success": True,
                "file_name": result.get("Name", file_name),
                "server_relative_url": result.get("ServerRelativeUrl"),
                "message": "File uploaded successfully.",
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Upload Folder Operation: Recursively Upload Local Folder ---
@mcp.tool()
def upload_sharepoint_folder(
    local_folder_path: str,
    target_folder_path: str,
    overwrite: bool = True,
    timeout_seconds: int = 60,
) -> dict:
    """
    Recursively upload a local folder (including subfolders and files) to SharePoint.

    Args:
            local_folder_path (str): Path to the local folder to upload.
            target_folder_path (str): Server-relative path to the target SharePoint folder (must start with '/').
            overwrite (bool): Whether to overwrite files if they exist (default: True).
            timeout_seconds (int): Timeout for each upload (default: 60).

    Returns:
            dict: Success status, details of uploaded files/folders, errors if any.
    """
    results = []
    errors = []
    try:
        # Get the folder name from local path
        local_folder_name = os.path.basename(local_folder_path)

        # Create the root folder in SharePoint first
        root_sp_folder = f"{target_folder_path}/{local_folder_name}"
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.ok:
            form_digest = digest_response.json()["d"]["GetContextWebInformation"][
                "FormDigestValue"
            ]
            api_url = f"{SHAREPOINT_SITE}/_api/web/folders"
            headers = _get_headers()
            headers["Content-Type"] = "application/json;odata=verbose"
            headers["X-RequestDigest"] = form_digest
            data = {
                "__metadata": {"type": "SP.Folder"},
                "ServerRelativeUrl": root_sp_folder,
            }
            try:
                response = requests.post(
                    api_url,
                    auth=_ntlm_auth(),
                    headers=headers,
                    json=data,
                    timeout=timeout_seconds,
                    verify=SSL_VERIFY_PARAM,
                )
                if response.status_code not in [200, 201]:
                    errors.append(
                        f"Failed to create root folder {root_sp_folder}: {response.reason}"
                    )
            except Exception as e:
                errors.append(f"Error creating root folder {root_sp_folder}: {str(e)}")
        else:
            errors.append("Failed to get form digest token for root folder creation")

        for root, dirs, files in os.walk(local_folder_path):
            # Compute relative path in local folder
            rel_path = os.path.relpath(root, local_folder_path)
            # Compute corresponding SharePoint folder path
            if rel_path == ".":
                sp_folder_path = root_sp_folder
            else:
                sp_folder_path = f"{root_sp_folder}/{rel_path.replace(os.sep, '/')}"

            # Create subfolder in SharePoint (if not root)
            if rel_path != ".":
                # Get form digest token
                digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
                digest_response = requests.post(
                    digest_url,
                    auth=_ntlm_auth(),
                    headers=_get_headers(),
                    verify=SSL_VERIFY_PARAM,
                )
                if digest_response.ok:
                    form_digest = digest_response.json()["d"][
                        "GetContextWebInformation"
                    ]["FormDigestValue"]
                else:
                    errors.append("Failed to get form digest token for folder creation")
                    continue

                api_url = f"{SHAREPOINT_SITE}/_api/web/folders"
                headers = _get_headers()
                headers["Content-Type"] = "application/json;odata=verbose"
                headers["X-RequestDigest"] = form_digest
                data = {
                    "__metadata": {"type": "SP.Folder"},
                    "ServerRelativeUrl": sp_folder_path,
                }
                try:
                    response = requests.post(
                        api_url,
                        auth=_ntlm_auth(),
                        headers=headers,
                        json=data,
                        timeout=timeout_seconds,
                        verify=SSL_VERIFY_PARAM,
                    )
                    if response.status_code not in [200, 201]:
                        errors.append(
                            f"Failed to create folder {sp_folder_path}: {response.reason}"
                        )
                except Exception as e:
                    errors.append(f"Error creating folder {sp_folder_path}: {str(e)}")

            # Upload files in this folder
            for file_name in files:
                local_file = os.path.join(root, file_name)

                # Get form digest token
                digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
                digest_response = requests.post(
                    digest_url,
                    auth=_ntlm_auth(),
                    headers=_get_headers(),
                    verify=SSL_VERIFY_PARAM,
                )
                if not digest_response.ok:
                    errors.append(
                        f"Failed to get form digest token for file upload: {file_name}"
                    )
                    continue
                form_digest = digest_response.json()["d"]["GetContextWebInformation"][
                    "FormDigestValue"
                ]

                overwrite_str = "true" if overwrite else "false"
                api_url = (
                    f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{sp_folder_path}')"
                    f"/Files/add(url='{file_name}',overwrite={overwrite_str})"
                )
                try:
                    with open(local_file, "rb") as f:
                        file_content = f.read()
                    headers = _get_headers()
                    headers["Content-Type"] = "application/octet-stream"
                    headers["X-RequestDigest"] = form_digest
                    response = requests.post(
                        api_url,
                        auth=_ntlm_auth(),
                        headers=headers,
                        data=file_content,
                        timeout=timeout_seconds,
                        verify=SSL_VERIFY_PARAM,
                    )
                    if response.status_code in [200, 201]:
                        results.append({"file": file_name, "folder": sp_folder_path})
                    else:
                        errors.append(
                            f"Failed to upload {file_name} to {sp_folder_path}: {response.reason}"
                        )
                except Exception as e:
                    errors.append(
                        f"Error uploading {file_name} to {sp_folder_path}: {str(e)}"
                    )

        return {
            "success": len(errors) == 0,
            "uploaded": results,
            "errors": errors,
            "has_errors": len(errors) > 0,
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "uploaded": results,
            "errors": errors,
            "has_errors": True,
        }


# --- Update Operation: Rename/Move File or Folder ---
@mcp.tool()
def update_sharepoint_item(
    item_url: str, new_name: str, is_folder: bool = False, timeout_seconds: int = 60
) -> dict:
    """
    Rename or move a file/folder in SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - item_url MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder/file.txt)
    - new_name MUST be the new name (for rename) or new path (for move).

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a file/folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="name", search_type="file" or "folder") to find the item
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this update_sharepoint_item tool with that server_relative_url

    FOLDER MOVE WORKAROUND:
    Moving folders to different parent directories is NOT supported directly via REST API.
    When you need to move a folder to a different location:
    1. FIRST call download_sharepoint_folder(folder_path=item_url) to download the folder locally
    2. THEN call upload_sharepoint_folder(local_folder_path="folder_name", target_folder_path=new_parent_path)
    3. OPTIONALLY delete the original folder if needed
    This tool will return an error with instructions if you try to move a folder across directories.

    Args:
            item_url (str): Server-relative path to the file or folder.
            new_name (str): New name or new path for the item.
            is_folder (bool): True if item is a folder, False if file.
            timeout_seconds (int): Timeout in seconds (default: 60).

    Returns:
            dict: Success status and updated item info.
    """
    try:
        # Get form digest token for POST operations
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {
                "success": False,
                "message": "Failed to get form digest token",
                "status_code": digest_response.status_code,
            }
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        # For files, use MoveTo API
        if not is_folder:
            api_url = (
                f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{item_url}')"
                f"/MoveTo(newurl='{new_name}',flags=1)"
            )
            headers = _get_headers()
            headers["X-RequestDigest"] = form_digest
            response = requests.post(
                api_url,
                auth=_ntlm_auth(),
                headers=headers,
                timeout=timeout_seconds,
                verify=SSL_VERIFY_PARAM,
            )
            if response.status_code in [200, 201, 204]:
                return {
                    "success": True,
                    "item_url": item_url,
                    "new_name": new_name,
                    "message": "Item renamed/moved successfully.",
                }
            else:
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "message": response.reason,
                }
        else:
            # For folders, use ListItemAllFields to get the list item and update it
            # First, get the folder's list item
            get_item_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{item_url}')/ListItemAllFields"
            get_response = requests.get(
                get_item_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )

            if not get_response.ok:
                return {
                    "success": False,
                    "status_code": get_response.status_code,
                    "message": f"Failed to get folder item: {get_response.reason}",
                }

            item_data = get_response.json()["d"]
            item_id = item_data.get("Id")
            item_type = item_data.get("__metadata", {}).get("type")

            # Extract the new folder name from the new path
            new_folder_name = new_name.split("/")[-1]
            item_url.split("/")[-1]

            # Check if it's just a rename (same parent folder) or a move
            old_parent = "/".join(item_url.split("/")[:-1])
            new_parent = "/".join(new_name.split("/")[:-1])

            if old_parent == new_parent:
                # Simple rename - update the Name field via MERGE
                update_url = f"{SHAREPOINT_SITE}/_api/web/lists/getbytitle('Documents')/items({item_id})"
                headers = _get_headers()
                headers["Content-Type"] = "application/json;odata=verbose"
                headers["X-RequestDigest"] = form_digest
                headers["X-HTTP-Method"] = "MERGE"
                headers["IF-MATCH"] = "*"

                update_data = {
                    "__metadata": {"type": item_type},
                    "FileLeafRef": new_folder_name,
                }

                response = requests.post(
                    update_url,
                    auth=_ntlm_auth(),
                    headers=headers,
                    json=update_data,
                    timeout=timeout_seconds,
                    verify=SSL_VERIFY_PARAM,
                )

                if response.status_code in [200, 201, 204]:
                    return {
                        "success": True,
                        "item_url": item_url,
                        "new_name": new_name,
                        "message": "Folder renamed successfully.",
                    }
                else:
                    return {
                        "success": False,
                        "status_code": response.status_code,
                        "message": f"Failed to rename folder: {response.reason}",
                    }
            else:
                # Move operation - this is more complex and may require copying
                return {
                    "success": False,
                    "message": (
                        "Moving folders to different parent directories is not supported via REST API. "
                        "Please use copy/delete approach or SharePoint UI."
                    ),
                    "suggestion": (
                        "Consider using bulk_download_sharepoint to download the folder, "
                        "then upload_sharepoint_folder to upload it to the new location."
                    ),
                }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Create Folder Operation ---
@mcp.tool()
def create_sharepoint_folder(
    parent_folder_path: str, new_folder_name: str, timeout_seconds: int = 60
) -> dict:
    """
    Create a new empty folder in SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - parent_folder_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/test_mcp)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a parent folder name (e.g., "test_mcp") and NOT the full path:
    1. FIRST call search_sharepoint(search_query="test_mcp", search_type="folder") to find the parent folder
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this create_sharepoint_folder tool with that path

    DO NOT call this tool with just a folder name - it will fail!

    Args:
            parent_folder_path (str): Server-relative path to the parent folder (must start with '/').
                    Example: /sites/190445/Documents/test_mcp
            new_folder_name (str): Name of the new folder to create.
            timeout_seconds (int): Request timeout in seconds (default: 60).

    Returns:
            dict: Success status and created folder details.
    """
    try:
        # Construct full path for new folder
        new_folder_path = f"{parent_folder_path}/{new_folder_name}"

        # Get form digest token for POST operations
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {
                "success": False,
                "message": "Failed to get form digest token",
                "status_code": digest_response.status_code,
            }
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        # Create folder
        api_url = f"{SHAREPOINT_SITE}/_api/web/folders"
        headers = _get_headers()
        headers["Content-Type"] = "application/json;odata=verbose"
        headers["X-RequestDigest"] = form_digest
        data = {
            "__metadata": {"type": "SP.Folder"},
            "ServerRelativeUrl": new_folder_path,
        }

        response = requests.post(
            api_url,
            auth=_ntlm_auth(),
            headers=headers,
            json=data,
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )

        if response.status_code in [200, 201]:
            result = response.json()["d"]
            return {
                "success": True,
                "folder_name": result.get("Name"),
                "server_relative_url": result.get("ServerRelativeUrl"),
                "parent_folder": parent_folder_path,
                "message": "Folder created successfully.",
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Delete Operation ---
@mcp.tool()
def delete_sharepoint_item(
    item_url: str, is_folder: bool = False, timeout_seconds: int = 60
) -> dict:
    """
    Delete a file or folder from SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - item_url MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder/file.txt)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a file/folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="name", search_type="file" or "folder") to find the item
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this delete_sharepoint_item tool with that server_relative_url

    WARNING: This operation is permanent and cannot be undone!

    Args:
            item_url (str): Server-relative path to the file or folder to delete.
            is_folder (bool): True if item is a folder, False if file (default: False).
            timeout_seconds (int): Request timeout in seconds (default: 60).

    Returns:
            dict: Success status and confirmation message.
    """
    try:
        # Get form digest token for POST operations
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {
                "success": False,
                "message": "Failed to get form digest token",
                "status_code": digest_response.status_code,
            }
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        # Delete file or folder
        if is_folder:
            api_url = (
                f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{item_url}')"
            )
        else:
            api_url = (
                f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{item_url}')"
            )

        headers = _get_headers()
        headers["X-RequestDigest"] = form_digest
        headers["X-HTTP-Method"] = "DELETE"
        headers["IF-MATCH"] = "*"

        response = requests.post(
            api_url,
            auth=_ntlm_auth(),
            headers=headers,
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )

        if response.status_code in [200, 204]:
            return {
                "success": True,
                "item_url": item_url,
                "message": f"{'Folder' if is_folder else 'File'} deleted successfully.",
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Copy Item Operation ---
@mcp.tool()
def copy_sharepoint_item(
    source_item_path: str,
    target_parent_path: str,
    new_item_name: str = "",
    is_folder: bool = False,
    timeout_seconds: int = 60,
) -> dict:
    """
    Copy a file or folder from one location to another in SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - source_item_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder/file.txt)
    - target_parent_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/target_folder)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a file/folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="name", search_type="file" or "folder") to find the item
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this copy_sharepoint_item tool with that server_relative_url

    DO NOT call this tool with just a file/folder name - it will fail!

    For FILES: Uses SharePoint REST API CopyTo operation (direct copy)

    For FOLDERS: SharePoint REST API doesn't support direct folder copy.
    When you need to copy a folder:
    1. FIRST call download_sharepoint_folder(folder_path=source_item_path) to download the folder locally
    2. THEN call upload_sharepoint_folder(local_folder_path="folder_name", target_folder_path=target_parent_path)
    3. OPTIONALLY call delete_sharepoint_item if you need to remove the downloaded local folder
    This tool will return an error with instructions if you try to copy a folder.

    Args:
            source_item_path (str): Server-relative path to the source file or folder
                    (must start with '/'). Example: /sites/190445/Documents/test_mcp/file.txt
            target_parent_path (str): Server-relative path to the target parent folder
                    (must start with '/'). Example: /sites/190445/Documents/target_folder
            new_item_name (str): New name for the copied item. If empty, uses source item name.
            is_folder (bool): True if item is a folder, False if file (default: False).
            timeout_seconds (int): Request timeout in seconds (default: 60).

    Returns:
            dict: Success status and copy details for files, or error with workflow
                    instructions for folders.
    """
    try:
        source_name = source_item_path.split("/")[-1]
        target_name = new_item_name if new_item_name else source_name
        target_full_path = f"{target_parent_path}/{target_name}"

        if is_folder:
            # Folders cannot be copied directly - return error with instructions
            return {
                "success": False,
                "message": (
                    "Direct folder copy is not supported via REST API. "
                    "Use download_sharepoint_folder + upload_sharepoint_folder workflow."
                ),
                "workflow_instructions": {
                    "step1": (
                        f"Call download_sharepoint_folder(folder_path='{source_item_path}') "
                        "to download locally"
                    ),
                    "step2": (
                        f"Call upload_sharepoint_folder(local_folder_path='{source_name}', "
                        f"target_folder_path='{target_parent_path}') to upload to target"
                    ),
                    "step3_optional": (
                        "Optionally rename the uploaded folder using update_sharepoint_item if needed"
                    ),
                },
                "source_folder": source_item_path,
                "target_location": target_full_path,
                "item_type": "folder",
            }

        # For files, use CopyTo REST API
        # Get form digest token for POST operations
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {
                "success": False,
                "message": "Failed to get form digest token",
                "status_code": digest_response.status_code,
            }
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        # Use CopyTo operation
        api_url = (
            f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{source_item_path}')"
            f"/CopyTo(strNewUrl='{target_full_path}',boverwrite=true)"
        )
        headers = _get_headers()
        headers["X-RequestDigest"] = form_digest

        response = requests.post(
            api_url,
            auth=_ntlm_auth(),
            headers=headers,
            timeout=timeout_seconds,
            verify=SSL_VERIFY_PARAM,
        )

        if response.status_code in [200, 201, 204]:
            return {
                "success": True,
                "source_path": source_item_path,
                "target_path": target_full_path,
                "item_type": "file",
                "message": "File copied successfully.",
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Bulk Download Operation ---
@mcp.tool()
def bulk_download_sharepoint(
    items: list, local_base_path: str = ".", timeout_seconds: int = 60
) -> dict:
    """
    Download multiple files and/or folders from SharePoint in bulk.
    Preserves folder structure locally for folders.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - Each item in 'items' MUST be a dict with keys: 'type' ('file' or 'folder'),
      'server_relative_url' (starting with '/')

    IMPORTANT WORKFLOW FOR LLM:
    If you only have names and NOT the full paths:
    1. FIRST call search_sharepoint(search_query="name", search_type="file" or "folder") to find the items
    2. From the search results, get the 'server_relative_url' field for each item
    3. THEN call this bulk_download_sharepoint tool with those URLs

    ALTERNATIVE APPROACH:
    Instead of using this bulk tool, you can call download_sharepoint_file() for each file and
    download_sharepoint_folder() for each folder individually. This may be more reliable and provide
    better error handling per item.

    Args:
            items (list): List of dicts with 'type' and 'server_relative_url'.
            local_base_path (str): Local directory to save files/folders (default: current directory).
            timeout_seconds (int): Download timeout per item (default: 60).

    Returns:
            dict: Success status, details of downloaded items, errors if any.
    """
    results = []
    errors = []
    try:
        for item in items:
            item_type = item.get("type")
            url = item.get("server_relative_url")

            if item_type == "file":
                # Download file
                file_name = url.split("/")[-1]
                file_api_url = f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{url}')/$value"
                local_file_path = Path(local_base_path) / file_name
                try:
                    response = requests.get(
                        file_api_url,
                        auth=_ntlm_auth(),
                        stream=True,
                        timeout=timeout_seconds,
                        verify=SSL_VERIFY_PARAM,
                    )
                    if response.status_code == 200:
                        with local_file_path.open("wb") as f:
                            f.write(response.content)
                        results.append(
                            {
                                "type": "file",
                                "name": file_name,
                                "local_path": str(local_file_path),
                                "server_relative_url": url,
                            }
                        )
                    else:
                        errors.append(
                            f"Failed to download file {file_name}: "
                            f"{response.reason}"
                        )
                except Exception as e:
                    errors.append(f"Error downloading file {file_name}: {str(e)}")

            elif item_type == "folder":
                # Download folder recursively (inline implementation)
                try:
                    folder_name = url.split("/")[-1]
                    local_folder_path = Path(local_base_path) / folder_name

                    def download_folder_recursive(
                        sp_folder_path: str, local_folder_path: Path, stats: dict
                    ):
                        try:
                            local_folder_path.mkdir(parents=True, exist_ok=True)
                            api_url_files = (
                                f"{SHAREPOINT_SITE}/_api/web/"
                                f"GetFolderByServerRelativeUrl('{sp_folder_path}')/Files"
                            )
                            response_files = requests.get(
                                api_url_files,
                                auth=_ntlm_auth(),
                                headers=_get_headers(),
                                verify=SSL_VERIFY_PARAM,
                            )
                            if response_files.ok:
                                files = response_files.json()["d"]["results"]
                                for file in files:
                                    server_relative_url = file["ServerRelativeUrl"]
                                    file_api_url = (
                                        f"{SHAREPOINT_SITE}/_api/web/"
                                        f"GetFileByServerRelativeUrl('{server_relative_url}')/$value"
                                    )
                                    file_name = file["Name"]
                                    local_file_path = local_folder_path / file_name
                                    response = requests.get(
                                        file_api_url,
                                        auth=_ntlm_auth(),
                                        stream=True,
                                        timeout=timeout_seconds,
                                        verify=SSL_VERIFY_PARAM,
                                    )
                                    if response.status_code == 200:
                                        with local_file_path.open("wb") as f:
                                            f.write(response.content)
                                        stats["files_downloaded"] += 1
                                        stats["downloaded_files"].append(
                                            {
                                                "name": file_name,
                                                "path": str(local_file_path),
                                            }
                                        )
                                    else:
                                        stats["errors"].append(
                                            f"Failed to download {file_name}: {response.reason}"
                                        )
                            api_url_folders = (
                                f"{SHAREPOINT_SITE}/_api/web/"
                                f"GetFolderByServerRelativeUrl('{sp_folder_path}')/Folders"
                            )
                            response_folders = requests.get(
                                api_url_folders,
                                auth=_ntlm_auth(),
                                headers=_get_headers(),
                                verify=SSL_VERIFY_PARAM,
                            )
                            if response_folders.ok:
                                folders = response_folders.json()["d"]["results"]
                                for folder in folders:
                                    if folder["Name"] not in [
                                        "Forms",
                                        "_catalogs",
                                        "_private",
                                    ]:
                                        subfolder_path = folder["ServerRelativeUrl"]
                                        local_subfolder_path = (
                                            local_folder_path / folder["Name"]
                                        )
                                        stats["folders_created"] += 1
                                        download_folder_recursive(
                                            subfolder_path, local_subfolder_path, stats
                                        )
                        except Exception as e:
                            stats["errors"].append(
                                f"Error accessing folder {sp_folder_path}: {str(e)}"
                            )

                    stats = {
                        "files_downloaded": 0,
                        "folders_created": 0,
                        "downloaded_files": [],
                        "errors": [],
                    }
                    download_folder_recursive(url, local_folder_path, stats)
                    results.append(
                        {
                            "type": "folder",
                            "name": folder_name,
                            "local_path": str(local_folder_path),
                            "server_relative_url": url,
                            "stats": stats,
                        }
                    )
                    if stats["errors"]:
                        errors.extend(stats["errors"])  # type: ignore[arg-type]
                except Exception as e:
                    errors.append(f"Error downloading folder {url}: {str(e)}")

            else:
                errors.append(f"Unknown item type: {item_type} for {url}")

        return {
            "success": len(errors) == 0,
            "results": results,
            "errors": errors,
            "has_errors": len(errors) > 0,
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "results": results,
            "errors": errors,
            "has_errors": True,
        }


# --- Bulk Upload Operation ---
@mcp.tool()
def bulk_upload_sharepoint(
    items: list,
    target_folder_path: str,
    overwrite: bool = True,
    timeout_seconds: int = 60,
) -> dict:
    """
    Upload multiple files to SharePoint in bulk.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - target_folder_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder)
    - Each item in 'items' MUST be a dict with keys: 'local_file_path' (path to local file)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a target folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="foldername", search_type="folder") to find the folder
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this bulk_upload_sharepoint tool with that path

    Args:
            items (list): List of dicts with 'local_file_path' keys pointing to files to upload.
            target_folder_path (str): Server-relative path to the target SharePoint folder (must start with '/').
            overwrite (bool): Whether to overwrite files if they exist (default: True).
            timeout_seconds (int): Upload timeout per file (default: 60).

    Returns:
            dict: Success status, details of uploaded files, errors if any.
    """
    results = []
    errors = []
    try:
        # Get form digest token once for all uploads
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {
                "success": False,
                "message": "Failed to get form digest token",
                "status_code": digest_response.status_code,
            }
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        for item in items:
            local_file_path = item.get("local_file_path")
            if not local_file_path:
                errors.append(f"Missing 'local_file_path' in item: {item}")
                continue

            try:
                file_name = os.path.basename(local_file_path)
                overwrite_str = "true" if overwrite else "false"
                api_url = (
                    f"{SHAREPOINT_SITE}/_api/web/"
                    f"GetFolderByServerRelativeUrl('{target_folder_path}')"
                    f"/Files/add(url='{file_name}',overwrite={overwrite_str})"
                )

                with open(local_file_path, "rb") as f:
                    file_content = f.read()

                headers = _get_headers()
                headers["Content-Type"] = "application/octet-stream"
                headers["X-RequestDigest"] = form_digest

                response = requests.post(
                    api_url,
                    auth=_ntlm_auth(),
                    headers=headers,
                    data=file_content,
                    timeout=timeout_seconds,
                    verify=SSL_VERIFY_PARAM,
                )

                if response.status_code in [200, 201]:
                    result = response.json()["d"]
                    results.append(
                        {
                            "file_name": result.get("Name", file_name),
                            "server_relative_url": result.get("ServerRelativeUrl"),
                            "local_path": local_file_path,
                        }
                    )
                else:
                    errors.append(f"Failed to upload {file_name}: {response.reason}")
            except Exception as e:
                errors.append(f"Error uploading {local_file_path}: {str(e)}")

        return {
            "success": len(errors) == 0,
            "uploaded": results,
            "errors": errors,
            "has_errors": len(errors) > 0,
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "uploaded": results,
            "errors": errors,
            "has_errors": True,
        }


# --- Zip and Download Folder Operation ---
@mcp.tool()
def download_and_zip_folder(
    folder_path: str, zip_file_name: str = "", timeout_seconds: int = 60
) -> dict:
    """
    Download a SharePoint folder and create a ZIP archive locally.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - folder_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="foldername", search_type="folder") to find the folder
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this download_and_zip_folder tool with that path

    Args:
            folder_path (str): Server-relative path to the folder (must start with '/').
            zip_file_name (str): Name for the ZIP file. If empty, uses folder name.
            timeout_seconds (int): Download timeout per file (default: 60).

    Returns:
            dict: Success status, ZIP file path, and statistics.
    """
    import zipfile
    import shutil
    from pathlib import Path

    try:
        # Extract folder name
        folder_name = folder_path.split("/")[-1]
        zip_name = zip_file_name if zip_file_name else f"{folder_name}.zip"

        # Download the folder first
        temp_dir = Path(f"temp_{folder_name}")

        def download_folder_recursive(
            sp_folder_path: str, local_folder_path: Path, stats: dict
        ):
            try:
                local_folder_path.mkdir(parents=True, exist_ok=True)

                # Download files
                api_url_files = (
                    f"{SHAREPOINT_SITE}/_api/web/"
                    f"GetFolderByServerRelativeUrl('{sp_folder_path}')/Files"
                )
                response_files = requests.get(
                    api_url_files,
                    auth=_ntlm_auth(),
                    headers=_get_headers(),
                    verify=SSL_VERIFY_PARAM,
                )

                if response_files.ok:
                    files = response_files.json()["d"]["results"]
                    for file in files:
                        server_relative_url = file["ServerRelativeUrl"]
                        file_api_url = (
                            f"{SHAREPOINT_SITE}/_api/web/"
                            f"GetFileByServerRelativeUrl('{server_relative_url}')/$value"
                        )
                        file_name = file["Name"]
                        local_file_path = local_folder_path / file_name

                        response = requests.get(
                            file_api_url,
                            auth=_ntlm_auth(),
                            stream=True,
                            timeout=timeout_seconds,
                            verify=SSL_VERIFY_PARAM,
                        )

                        if response.status_code == 200:
                            with local_file_path.open("wb") as f:
                                f.write(response.content)
                            stats["files_downloaded"] += 1
                            stats["total_bytes"] += int(file.get("Length", 0))
                        else:
                            stats["errors"].append(f"Failed to download {file_name}")

                # Download subfolders
                api_url_folders = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{sp_folder_path}')/Folders"
                response_folders = requests.get(
                    api_url_folders,
                    auth=_ntlm_auth(),
                    headers=_get_headers(),
                    verify=SSL_VERIFY_PARAM,
                )

                if response_folders.ok:
                    folders = response_folders.json()["d"]["results"]
                    for folder in folders:
                        if folder["Name"] not in ["Forms", "_catalogs", "_private"]:
                            subfolder_path = folder["ServerRelativeUrl"]
                            local_subfolder_path = local_folder_path / folder["Name"]
                            download_folder_recursive(
                                subfolder_path, local_subfolder_path, stats
                            )

            except Exception as e:
                stats["errors"].append(
                    f"Error accessing folder {sp_folder_path}: {str(e)}"
                )

        stats = {"files_downloaded": 0, "total_bytes": 0, "errors": []}
        download_folder_recursive(folder_path, temp_dir, stats)

        # Create ZIP file
        zip_path = Path(zip_name)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in temp_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)

        # Clean up temporary directory
        shutil.rmtree(temp_dir)

        return {
            "success": True,
            "zip_file": str(zip_path),
            "folder_path": folder_path,
            "files_downloaded": stats["files_downloaded"],
            "total_size_bytes": stats["total_bytes"],
            "errors": stats["errors"],
            "has_errors": len(stats["errors"]) > 0,  # type: ignore[arg-type]
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Get SharePoint Site Information ---
@mcp.tool()
def get_site_info() -> dict:
    """
    Get information about the SharePoint site.

    Returns:
            dict: Site information including title, URL, description, and web template.
    """
    try:
        api_url = f"{SHAREPOINT_SITE}/_api/web"
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()

        site_data = response.json()["d"]

        return {
            "success": True,
            "site_title": site_data.get("Title"),
            "site_url": site_data.get("Url"),
            "description": site_data.get("Description"),
            "web_template": site_data.get("WebTemplate"),
            "created": site_data.get("Created"),
            "last_item_modified": site_data.get("LastItemModifiedDate"),
            "language": site_data.get("Language"),
            "server_relative_url": site_data.get("ServerRelativeUrl"),
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Recycle Bin Operations ---
@mcp.tool()
def list_recycle_bin_items() -> dict:
    """
    List all items in the SharePoint recycle bin.

    Returns:
            dict: List of items in the recycle bin with details.
    """
    try:
        api_url = f"{SHAREPOINT_SITE}/_api/web/RecycleBin"
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()

        items = response.json()["d"]["results"]

        recycle_items = []
        for item in items:
            recycle_items.append(
                {
                    "id": item.get("Id"),
                    "title": item.get("Title"),
                    "item_type": item.get("ItemType"),
                    "dir_name": item.get("DirName"),
                    "deleted_by": item.get("DeletedByName"),
                    "deleted_date": item.get("DeletedDate"),
                    "size": item.get("Size"),
                }
            )

        return {
            "success": True,
            "total_items": len(recycle_items),
            "items": recycle_items,
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def restore_recycle_bin_item(item_id: str) -> dict:
    """
    Restore an item from the SharePoint recycle bin.

    Args:
            item_id (str): The ID of the item to restore (get from list_recycle_bin_items).

    Returns:
            dict: Success status and confirmation message.
    """
    try:
        # Get form digest token
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {"success": False, "message": "Failed to get form digest token"}
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        # Restore item
        api_url = f"{SHAREPOINT_SITE}/_api/web/RecycleBin('{item_id}')/restore()"
        headers = _get_headers()
        headers["X-RequestDigest"] = form_digest

        response = requests.post(
            api_url, auth=_ntlm_auth(), headers=headers, verify=SSL_VERIFY_PARAM
        )

        if response.status_code in [200, 204]:
            return {
                "success": True,
                "item_id": item_id,
                "message": "Item restored successfully.",
            }
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def empty_recycle_bin() -> dict:
    """
    Permanently delete all items from the SharePoint recycle bin.

    WARNING: This operation is permanent and cannot be undone!

    Returns:
            dict: Success status and confirmation message.
    """
    try:
        # Get form digest token
        digest_url = f"{SHAREPOINT_SITE}/_api/contextinfo"
        digest_response = requests.post(
            digest_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        if digest_response.status_code != 200:
            return {"success": False, "message": "Failed to get form digest token"}
        form_digest = digest_response.json()["d"]["GetContextWebInformation"][
            "FormDigestValue"
        ]

        # Empty recycle bin
        api_url = f"{SHAREPOINT_SITE}/_api/web/RecycleBin/DeleteAll()"
        headers = _get_headers()
        headers["X-RequestDigest"] = form_digest

        response = requests.post(
            api_url, auth=_ntlm_auth(), headers=headers, verify=SSL_VERIFY_PARAM
        )

        if response.status_code in [200, 204]:
            return {"success": True, "message": "Recycle bin emptied successfully."}
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": response.reason,
            }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Get File/Folder Permissions ---
@mcp.tool()
def get_item_permissions(item_url: str, is_folder: bool = False) -> dict:
    """
    Get permissions for a file or folder in SharePoint.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - item_url MUST be a server-relative path starting with '/'
      (e.g., /sites/xxx/Documents/folder/file.txt)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a file/folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="name", search_type="file" or "folder") to find the item
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this get_item_permissions tool with that path

    Args:
            item_url (str): Server-relative path to the file or folder (must start with '/').
            is_folder (bool): True if item is a folder, False if file (default: False).

    Returns:
            dict: Permission information including role assignments and members.
    """
    try:
        if is_folder:
            api_url = (
                f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('{item_url}')"
                "/ListItemAllFields/RoleAssignments?$expand=Member,RoleDefinitionBindings"
            )
        else:
            api_url = (
                f"{SHAREPOINT_SITE}/_api/web/GetFileByServerRelativeUrl('{item_url}')"
                "/ListItemAllFields/RoleAssignments?$expand=Member,RoleDefinitionBindings"
            )

        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()

        assignments = response.json()["d"]["results"]

        permissions = []
        for assignment in assignments:
            member = assignment.get("Member", {})
            roles = assignment.get("RoleDefinitionBindings", {}).get("results", [])

            role_names = [role.get("Name") for role in roles]

            permissions.append(
                {
                    "principal_id": assignment.get("PrincipalId"),
                    "member_name": member.get("Title"),
                    "member_type": member.get("PrincipalType"),
                    "login_name": member.get("LoginName"),
                    "roles": role_names,
                }
            )

        return {
            "success": True,
            "item_url": item_url,
            "item_type": "folder" if is_folder else "file",
            "permissions": permissions,
            "total_assignments": len(permissions),
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Get SharePoint Link for File/Folder ---
@mcp.tool()
def get_sharepoint_link(item_path: str, is_folder: bool = False) -> dict:
    """
    Get the direct SharePoint link for a file or folder.

    CRITICAL REQUIREMENT - READ THIS CAREFULLY:
    - item_path MUST be a server-relative path starting with '/' (e.g., /sites/xxx/Documents/folder/file.txt)

    IMPORTANT WORKFLOW FOR LLM:
    If you only have a file/folder name and NOT the full path:
    1. FIRST call search_sharepoint(search_query="name", search_type="file" or "folder") to find the item
    2. From the search results, get the 'server_relative_url' field
    3. THEN call this get_sharepoint_link tool with that server_relative_url

    DO NOT call this tool with just a file/folder name - it will fail!

    Args:
            item_path (str): Server-relative path to the file or folder (must start with '/').
                    Example: /sites/190445/Documents/test_mcp/file1.txt
            is_folder (bool): True if item is a folder, False if file (default: False).

    Returns:
            dict: Success status, item path, and direct SharePoint link.
    """
    try:
        # Extract site ID from the SharePoint site URL
        # Example: https://sites.inside-share5.bosch.com/sites/190445 -> 190445
        site_parts = SHAREPOINT_SITE.split("/sites/")
        if len(site_parts) > 1:
            site_id = site_parts[1].strip("/")
            # Remove the site ID portion from the item path to get the relative path
            relative_path = item_path.replace(f"/sites/{site_id}", "")
        else:
            # If no /sites/ in URL, use the path as is
            relative_path = item_path

        # Construct the full SharePoint URL
        full_url = f"{SHAREPOINT_SITE}{relative_path}"

        return {
            "success": True,
            "item_path": item_path,
            "item_type": "folder" if is_folder else "file",
            "sharepoint_link": full_url,
            "message": f"Direct link to {'folder' if is_folder else 'file'} generated successfully.",
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Get Current User Information ---
@mcp.tool()
def get_current_user_info() -> dict:
    """
    Get detailed information about the current authenticated user.

    Returns:
            dict: User information including name, email, login name, and user ID.
    """
    try:
        api_url = f"{SHAREPOINT_SITE}/_api/web/currentuser"
        response = requests.get(
            api_url, auth=_ntlm_auth(), headers=_get_headers(), verify=SSL_VERIFY_PARAM
        )
        response.raise_for_status()

        user_data = response.json()["d"]

        return {
            "success": True,
            "user_id": user_data.get("Id"),
            "title": user_data.get("Title"),
            "login_name": user_data.get("LoginName"),
            "email": user_data.get("Email"),
            "is_site_admin": user_data.get("IsSiteAdmin"),
            "user_principal_name": user_data.get("UserPrincipalName"),
            "message": "Current user information retrieved successfully.",
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


# --- Site Discovery Tools ---
@mcp.tool()
def list_sharepoint_sites() -> dict:
    """
    List all SharePoint sites that the current user has access to.

    Returns:
            dict: List of accessible SharePoint sites with their details.
    """
    try:
        sites = []

        # First, get the current site information
        current_site_url = f"{SHAREPOINT_SITE}/_api/web"
        current_response = requests.get(
            current_site_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )

        if current_response.ok:
            current_site = current_response.json()["d"]
            sites.append(
                {
                    "title": current_site.get("Title"),
                    "url": current_site.get("Url"),
                    "server_relative_url": current_site.get("ServerRelativeUrl"),
                    "description": current_site.get("Description"),
                    "web_template": current_site.get("WebTemplate"),
                    "created": current_site.get("Created"),
                    "last_item_modified": current_site.get("LastItemModifiedDate"),
                    "language": current_site.get("Language"),
                    "is_current_site": True,
                }
            )

        # Try to get subsites (may fail due to permissions)
        try:
            subsites_url = f"{SHAREPOINT_SITE}/_api/web/webs"
            subsites_response = requests.get(
                subsites_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )

            if subsites_response.ok:
                webs = subsites_response.json()["d"]["results"]
                for web in webs:
                    sites.append(
                        {
                            "title": web.get("Title"),
                            "url": web.get("Url"),
                            "server_relative_url": web.get("ServerRelativeUrl"),
                            "description": web.get("Description"),
                            "web_template": web.get("WebTemplate"),
                            "created": web.get("Created"),
                            "last_item_modified": web.get("LastItemModifiedDate"),
                            "language": web.get("Language"),
                            "is_current_site": False,
                        }
                    )
        except Exception as subsite_error:
            logging.warning(f"Could not retrieve subsites: {str(subsite_error)}")

        return {
            "success": True,
            "total_sites": len(sites),
            "sites": sites,
            "message": (
                f"Found {len(sites)} accessible SharePoint site(s). "
                "Note: Subsites may require additional permissions."
            ),
            "note": (
                "If subsites are not listed, the current user may not have permission "
                "to view them, or they may not exist."
            ),
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


@mcp.tool()
def list_sharepoint_site_contents() -> dict:
    """
    List all contents (document libraries, folders, files, and lists) of the current SharePoint site.
    Provides a complete inventory of the site's contents.

    Returns:
            dict: Complete inventory of site contents including libraries, lists, folders, and files.
    """
    try:
        contents: dict[str, list] = {
            "document_libraries": [],
            "lists": [],
            "folders": [],
            "files": [],
        }

        # Get all lists (includes document libraries)
        lists_url = f"{SHAREPOINT_SITE}/_api/web/lists"
        lists_response = requests.get(
            lists_url,
            auth=_ntlm_auth(),
            headers=_get_headers(),
            verify=SSL_VERIFY_PARAM,
        )
        lists_response.raise_for_status()

        all_lists = lists_response.json()["d"]["results"]

        for list_item in all_lists:
            base_type = list_item.get("BaseType")
            list_info = {
                "title": list_item.get("Title"),
                "description": list_item.get("Description"),
                "item_count": list_item.get("ItemCount"),
                "created": list_item.get("Created"),
                "last_item_modified": list_item.get("LastItemModifiedDate"),
                "server_relative_url": list_item.get("RootFolder", {}).get(
                    "ServerRelativeUrl"
                )
                if isinstance(list_item.get("RootFolder"), dict)
                else None,
            }

            # BaseType: 0 = Generic List, 1 = Document Library
            if base_type == 1:
                contents["document_libraries"].append(list_info)
            elif base_type == 0:
                # Skip hidden/system lists
                if not list_item.get("Hidden", False):
                    contents["lists"].append(list_info)

        # Get all folders from the main Documents library
        try:
            folders_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('Documents')/Folders"
            folders_response = requests.get(
                folders_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            if folders_response.ok:
                folders = folders_response.json()["d"]["results"]
                for folder in folders:
                    if folder["Name"] not in ["Forms", "_catalogs", "_private"]:
                        contents["folders"].append(
                            {
                                "name": folder["Name"],
                                "server_relative_url": folder["ServerRelativeUrl"],
                                "item_count": folder.get("ItemCount", 0),
                                "time_created": folder.get("TimeCreated"),
                                "time_last_modified": folder.get("TimeLastModified"),
                            }
                        )
        except Exception as e:
            logging.warning(f"Could not retrieve folders: {str(e)}")

        # Get all files from the main Documents library
        try:
            files_url = f"{SHAREPOINT_SITE}/_api/web/GetFolderByServerRelativeUrl('Documents')/Files"
            files_response = requests.get(
                files_url,
                auth=_ntlm_auth(),
                headers=_get_headers(),
                verify=SSL_VERIFY_PARAM,
            )
            if files_response.ok:
                files = files_response.json()["d"]["results"]
                for file in files:
                    contents["files"].append(
                        {
                            "name": file["Name"],
                            "server_relative_url": file["ServerRelativeUrl"],
                            "size_bytes": file.get("Length"),
                            "time_created": file.get("TimeCreated"),
                            "time_last_modified": file.get("TimeLastModified"),
                        }
                    )
        except Exception as e:
            logging.warning(f"Could not retrieve files: {str(e)}")

        return {
            "success": True,
            "site_url": SHAREPOINT_SITE,
            "contents": contents,
            "summary": {
                "total_document_libraries": len(contents["document_libraries"]),
                "total_lists": len(contents["lists"]),
                "total_folders": len(contents["folders"]),
                "total_files": len(contents["files"]),
            },
            "message": "Site contents retrieved successfully.",
        }
    except Exception as e:
        return {"success": False, "message": str(e)}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    transport, host, port = _get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
