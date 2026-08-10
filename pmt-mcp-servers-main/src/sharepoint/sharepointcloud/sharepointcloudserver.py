"""
SharePoint MCP Server

This module implements MCP tools for interacting with SharePoint Online.

API/Library:
- office365-rest-python-client (Office 365 REST API Python client)
- Uses SharePoint REST API endpoints

Authentication:
- Method: UserCredential (username/password)
"""

from __future__ import annotations

import os
import logging
from typing import Optional, List, Dict, Any
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.client_context import ClientContext
from pathlib import Path
from fastmcp import FastMCP
from urllib.parse import quote, urlparse


# Initialize MCP Server
mcp = FastMCP("sharepoint")

# Auth / Client
sharepoint_site_url = os.getenv("SHAREPOINT_SITE_URL", "")
sp_username = os.getenv("SHAREPOINT_USERNAME", "")
sp_password = os.getenv("SHAREPOINT_PASSWORD", "")

if not sharepoint_site_url or not sp_username or not sp_password:
    raise ValueError(
        "Missing required environment variables: SHAREPOINT_SITE_URL, SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD"
    )


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


# HELPER FUNCTION
def _encode_url(url: str) -> str:
    """Helper to encode SharePoint URLs."""
    return "/".join([quote(part) if part else part for part in url.split("/")])


# Authentication and SharePoint Client Setup #
def _authenticate_cloud_sp() -> ClientContext:
    """
    Authenticates with SharePoint using provided credentials.

    Raises:
        ValueError: If authentication fails due to invalid credentials or site URL.
        OSError: If an OS error occurs during authentication.
        ClientRequestException: If a SharePoint client request error occurs.
    """
    # Validate environment variables before authentication
    if not sharepoint_site_url or not sp_username or not sp_password:
        logging.error(
            "Missing required credentials: SHAREPOINT_SITE_URL, "
            "SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD. Please check configuration."
        )
        raise ValueError(
            "Missing required credentials: SHAREPOINT_SITE_URL, "
            "SHAREPOINT_USERNAME, SHAREPOINT_PASSWORD. Please check configuration."
        )
    try:
        logging.info(
            "Attempting to authenticate with SharePoint at %s", sharepoint_site_url
        )
        ctx = ClientContext(sharepoint_site_url).with_credentials(
            UserCredential(sp_username, sp_password)
        )
        logging.info("Successfully authenticated with SharePoint")
        return ctx
    except ClientRequestException as exc:
        logging.warning("SharePoint authentication failed: %s", exc)
        raise ValueError(
            "SharePoint authentication failed. Check credentials and site URL."
        )
    except ValueError as exc:
        logging.error("Invalid value during SharePoint authentication: %s", exc)
        raise ValueError("Invalid value during SharePoint authentication.")
    except OSError as exc:
        logging.warning("OS error occurred during SharePoint authentication: %s", exc)
        raise OSError("OS error occurred during SharePoint authentication.")


@mcp.tool()
def download_sharepoint_file(file_url: str, save_as: str = "downloaded_file") -> dict:
    """Download a file from SharePoint using username/password authentication.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
            file_url: Server relative URL of the file (e.g., '/sites/mysite/Shared Documents/file.txt')
            save_as: Local filename to save as
    Returns:
            Dict with success status and message
    """
    local_path = Path(save_as)
    try:
        ctx = _authenticate_cloud_sp()
        # Dynamically extract the domain from sharepoint_site_url
        parsed_url = urlparse(sharepoint_site_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        url = file_url.replace(base_url, "")
        with local_path.open("wb") as local_file:
            file = ctx.web.get_file_by_server_relative_url(url)
            file.download(local_file).execute_query()
        logging.info("Downloaded file: %s", local_path.name)
        logging.info("File downloaded successfully: %s", local_path)
        return {
            "file_url": file_url,
            "saved_as": str(local_path),
            "success": True,
            "message": "Downloaded successfully",
        }
    except (OSError, ValueError, ClientRequestException) as error_msg:
        logging.error("Failed to download file: %s", error_msg, exc_info=True)
        return {"success": False, "message": f"Download failed: {error_msg}"}
    except Exception as exc:
        logging.error(
            "Unexpected error in download_sharepoint_file: %s", exc, exc_info=True
        )
        return {"success": False, "message": f"Unexpected error: {exc}"}


@mcp.tool()
def upload_sharepoint_file(local_path: str, target_folder_url: str) -> dict:
    """Upload a file to SharePoint using username/password authentication.

    IMPORTANT: target_folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
            local_path: Local file path to upload
            target_folder_url: Server relative URL of the target folder
    Returns:
            Dict with success status and message
    """
    try:
        ctx = _authenticate_cloud_sp()
        if not ctx:
            return {"success": False, "message": "SharePoint authentication failed."}
        filename = os.path.basename(local_path)
        with open(local_path, "rb") as content_file:
            target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)
            target_folder.upload_file(filename, content_file).execute_query()
        logging.info("Uploaded file: %s to %s", filename, target_folder_url)
        return {
            "local_path": local_path,
            "target_folder_url": target_folder_url,
            "success": True,
            "message": "Uploaded successfully",
        }
    except (OSError, ValueError, ClientRequestException) as error_msg:
        logging.error("Failed to upload file: %s", error_msg)
        return {"success": False, "message": f"Upload failed: {error_msg}"}
    except Exception as exc:
        logging.error("Unexpected error in upload_sharepoint_file: %s", exc)
        return {"success": False, "message": f"Unexpected error: {exc}"}


@mcp.tool()
def get_sharepoint_file_metadata(file_url: str) -> dict:
    """Get metadata for a SharePoint file using username/password authentication.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
            file_url: Server relative URL of the file (e.g., '/sites/mysite/Shared Documents/file.txt')
    Returns:
            Dict with file metadata
    """
    try:
        ctx = _authenticate_cloud_sp()
        if not ctx:
            return {"success": False, "message": "SharePoint authentication failed."}
        file = ctx.web.get_file_by_server_relative_url(file_url)
        ctx.load(file)
        ctx.execute_query()
        return {"file_url": file_url, "metadata": file.properties, "success": True}
    except (OSError, ValueError, ClientRequestException) as error_msg:
        logging.error("Failed to get file metadata: %s", error_msg)
        return {"success": False, "message": f"Get metadata failed: {error_msg}"}
    except Exception as exc:
        logging.error("Unexpected error in get_sharepoint_file_metadata: %s", exc)
        return {"success": False, "message": f"Unexpected error: {exc}"}


@mcp.tool()
def delete_sharepoint_file(file_url: str) -> dict:
    """Delete a file from SharePoint using username/password authentication.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        file_url: Server relative URL of the file to delete (e.g., '/sites/mysite/Shared Documents/file.txt')
    Returns:
        Dict with success status and message
    """
    try:
        ctx = _authenticate_cloud_sp()
        if not ctx:
            return {"success": False, "message": "SharePoint authentication failed."}
        file = ctx.web.get_file_by_server_relative_url(file_url)
        file.delete_object().execute_query()
        logging.info("Deleted file: %s", file_url)
        return {
            "file_url": file_url,
            "success": True,
            "message": "File deleted successfully",
        }
    except (OSError, ValueError, ClientRequestException) as error_msg:
        logging.error("Failed to delete file: %s", error_msg)
        return {"success": False, "message": f"Delete file failed: {error_msg}"}
    except Exception as exc:
        logging.error("Unexpected error in delete_sharepoint_file: %s", exc)
        return {"success": False, "message": f"Unexpected error: {exc}"}


@mcp.tool()
def list_files_in_sharepoint_folder_v2(folder_url: str) -> dict:
    """Alternative implementation using expand query option.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.
    """
    try:
        logging.info("Attempting to list files in folder: %s", folder_url)
        ctx = _authenticate_cloud_sp()

        # URL encode the folder path
        folder_parts = folder_url.split("/")
        encoded_parts = [quote(part) if part else part for part in folder_parts]
        encoded_folder_url = "/".join(encoded_parts)

        # Get folder with expanded files
        folder = ctx.web.get_folder_by_server_relative_url(encoded_folder_url)
        folder.expand(["Files"]).get().execute_query()

        files = []
        for file in folder.files:
            files.append(
                {
                    "name": file.properties.get("Name"),
                    "url": file.properties.get("ServerRelativeUrl"),
                    "length": file.properties.get("Length"),
                    "time_created": str(file.properties.get("TimeCreated")),
                    "time_last_modified": str(file.properties.get("TimeLastModified")),
                }
            )

        logging.info("Found %d files", len(files))

        return {
            "folder_url": folder_url,
            "files": files,
            "file_count": len(files),
            "success": True,
        }
    except Exception as e:
        logging.error("Error: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def list_items_in_sharepoint_folder(folder_url: str) -> dict:
    """List all items (files and folders) in a SharePoint folder.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        folder_url: Server relative URL of the folder to list items from
    Returns:
        Dict with success status and message
    """
    try:
        from urllib.parse import quote

        logging.info("Attempting to list items in folder: %s", folder_url)
        ctx = _authenticate_cloud_sp()

        # URL encode the folder path
        folder_parts = folder_url.split("/")
        encoded_parts = [quote(part) if part else part for part in folder_parts]
        encoded_folder_url = "/".join(encoded_parts)

        # Get folder with expanded files and folders
        folder = ctx.web.get_folder_by_server_relative_url(encoded_folder_url)
        folder.expand(["Files", "Folders"]).get().execute_query()

        files = []
        for file in folder.files:
            files.append(
                {
                    "type": "file",
                    "name": file.properties.get("Name"),
                    "url": file.properties.get("ServerRelativeUrl"),
                    "length": file.properties.get("Length"),
                    "time_created": str(file.properties.get("TimeCreated")),
                    "time_last_modified": str(file.properties.get("TimeLastModified")),
                }
            )

        folders = []
        for subfolder in folder.folders:
            folders.append(
                {
                    "type": "folder",
                    "name": subfolder.properties.get("Name"),
                    "url": subfolder.properties.get("ServerRelativeUrl"),
                    "item_count": subfolder.properties.get("ItemCount"),
                    "time_created": str(subfolder.properties.get("TimeCreated")),
                    "time_last_modified": str(
                        subfolder.properties.get("TimeLastModified")
                    ),
                }
            )

        logging.info("Found %d files and %d folders", len(files), len(folders))

        return {
            "folder_url": folder_url,
            "files": files,
            "folders": folders,
            "file_count": len(files),
            "folder_count": len(folders),
            "success": True,
        }
    except Exception as e:
        logging.error("Error: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def move_sharepoint_file(source_file_url: str, target_folder_url: str) -> dict:
    """Move a file from one folder to another within SharePoint.

    IMPORTANT: source_file_url and target_folder_url must be full server
    relative paths starting with '/'. If you only have filenames or folder
    names, call search_sharepoint(search_query="name", search_type="both")
    first to get the full paths, then use the 'server_relative_url' from
    the search results.

    Args:
        source_file_url: Server relative URL of the source file
            (e.g., '/sites/mysite/Shared Documents/file.txt')
        target_folder_url: Server relative URL of the target folder
            (e.g., '/sites/mysite/Shared Documents/TargetFolder')
    Returns:
        Dict with success status and message.
    """
    try:
        import io

        ctx = _authenticate_cloud_sp()

        # Get the source file
        source_file = ctx.web.get_file_by_server_relative_url(source_file_url)
        ctx.load(source_file)
        ctx.execute_query()

        file_name = source_file.properties.get("Name")
        if not file_name:
            raise ValueError("File name could not be retrieved.")

        # Download file content to memory
        file_content = io.BytesIO()
        source_file.download(file_content).execute_query()
        file_content.seek(0)

        # Get target folder
        target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)

        # Upload to target folder
        target_folder.upload_file(file_name, file_content.getvalue()).execute_query()

        # Delete the source file
        source_file.delete_object().execute_query()

        # Construct target URL
        if target_folder_url.endswith("/"):
            target_folder_url = target_folder_url[:-1]
        target_url = f"{target_folder_url}/{file_name}"

        logging.info("Moved file from %s to %s", source_file_url, target_url)
        return {
            "success": True,
            "message": "File moved successfully",
            "source_url": source_file_url,
            "target_url": target_url,
        }
    except Exception as e:
        logging.error("Failed to move file: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def copy_sharepoint_file(source_file_url: str, target_folder_url: str) -> dict:
    """Copy a file to another folder in SharePoint.

    IMPORTANT: source_file_url and target_folder_url must be full server relative paths starting with '/'.
    If you only have filenames or folder names, call search_sharepoint(search_query="name", search_type="both") first
    to get the full paths, then use the 'server_relative_url' from the search results.

    Args:
        source_file_url: Server relative URL of the source file
            (e.g., '/sites/mysite/Shared Documents/file.txt')
        target_folder_url: Server relative URL of the target folder
            (e.g., '/sites/mysite/Shared Documents/TargetFolder')
    Returns:
        Dict with success status and message.
    """
    try:
        import io

        ctx = _authenticate_cloud_sp()

        # Get the source file
        source_file = ctx.web.get_file_by_server_relative_url(source_file_url)
        ctx.load(source_file)
        ctx.execute_query()

        file_name = source_file.properties.get("Name")
        if not file_name:
            raise ValueError("File name could not be retrieved.")

        # Download file content to memory
        file_content = io.BytesIO()
        source_file.download(file_content).execute_query()
        file_content.seek(0)

        # Get target folder
        target_folder = ctx.web.get_folder_by_server_relative_url(target_folder_url)

        # Upload to target folder
        target_folder.upload_file(file_name, file_content.getvalue()).execute_query()

        # Construct target URL
        if target_folder_url.endswith("/"):
            target_folder_url = target_folder_url[:-1]
        target_url = f"{target_folder_url}/{file_name}"

        logging.info("Copied file from %s to %s", source_file_url, target_url)
        return {
            "success": True,
            "message": "File copied successfully",
            "source_url": source_file_url,
            "target_url": target_url,
        }
    except Exception as e:
        logging.error("Failed to copy file: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def rename_sharepoint_file(file_url: str, new_name: str) -> dict:
    """Rename a file in SharePoint.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        file_url: Server relative URL of the file to rename (e.g., '/sites/mysite/Shared Documents/file.txt')
        new_name: New name for the file (with extension).
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the file
        file = ctx.web.get_file_by_server_relative_url(file_url)

        # Load the list item
        list_item = file.listItemAllFields
        ctx.load(list_item)
        ctx.execute_query()

        # Update the FileLeafRef property (the actual file name)
        list_item.set_property("FileLeafRef", new_name)
        list_item.update()
        ctx.execute_query()

        # Calculate new URL
        parent_url = "/".join(file_url.split("/")[:-1])
        new_url = f"{parent_url}/{new_name}"

        logging.info("Successfully renamed file to %s", new_name)
        return {
            "success": True,
            "message": f"File renamed to {new_name}",
            "old_url": file_url,
            "new_url": new_url,
        }
    except Exception as e:
        logging.error("Failed to rename file: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def bulk_upload_files(folder_url: str, local_files: list[str]) -> dict:
    """Upload multiple files to a SharePoint folder.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        uploaded_files = []
        failed_files = []

        for file_path in local_files:
            try:
                file_name = Path(file_path).name
                with open(file_path, "rb") as file_content:
                    target_url = f"{folder_url}/{file_name}"
                    ctx.web.get_folder_by_server_relative_url(folder_url).upload_file(
                        file_name, file_content.read()
                    ).execute_query()
                    logging.info("Uploaded file: %s", target_url)
                    uploaded_files.append({"file": file_path, "target_url": target_url})
            except Exception as e:
                logging.error("Failed to upload %s: %s", file_path, e)
                failed_files.append({"file": file_path, "error": str(e)})

        return {
            "success": True,
            "uploaded_count": len(uploaded_files),
            "failed_count": len(failed_files),
            "uploaded_files": uploaded_files,
            "failed_files": failed_files,
        }
    except Exception as e:
        logging.error("Bulk upload failed: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def bulk_download_files(file_urls: list[str], local_folder: str) -> dict:
    """Download multiple files from SharePoint to a local directory.

    IMPORTANT: file_urls must be full server relative paths starting with '/'.
    If you only have filenames, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full paths, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        os.makedirs(local_folder, exist_ok=True)
        downloaded_files = []
        failed_files = []

        for file_url in file_urls:
            try:
                file_name = Path(file_url).name
                local_path = Path(local_folder) / file_name
                with open(local_path, "wb") as local_file:
                    (
                        ctx.web.get_file_by_server_relative_url(file_url)
                        .download(local_file)
                        .execute_query()
                    )
                    logging.info("Downloaded file: %s", local_path)
                    downloaded_files.append(
                        {"file_url": file_url, "local_path": str(local_path)}
                    )
            except Exception as e:
                logging.error("Failed to download %s: %s", file_url, e)
                failed_files.append({"file_url": file_url, "error": str(e)})

        return {
            "success": True,
            "downloaded_count": len(downloaded_files),
            "failed_count": len(failed_files),
            "downloaded_files": downloaded_files,
            "failed_files": failed_files,
            "local_folder": local_folder,
        }
    except Exception as e:
        logging.error("Bulk download failed: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def zip_and_download_folder(folder_url: str, zip_name: str) -> None:
    """Zip the contents of a SharePoint folder and download the zip file.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.
    """
    import zipfile

    ctx = _authenticate_cloud_sp()
    import io

    def add_folder_to_zip(sp_folder, zipf, base_path):
        sp_folder.expand(["Files", "Folders"]).get().execute_query()
        # Add files in current folder
        for file in sp_folder.files:
            file_name = file.properties.get("Name")
            file_stream = io.BytesIO()
            file.download(file_stream).execute_query()
            file_stream.seek(0)
            zip_path = f"{base_path}/{file_name}" if base_path else file_name
            zipf.writestr(zip_path, file_stream.read())
        # Recursively add subfolders
        if not sp_folder.files and not sp_folder.folders:
            # Add empty folder entry
            folder_entry = f"{base_path}/" if base_path else ""
            zinfo = zipfile.ZipInfo(folder_entry)
            zipf.writestr(zinfo, b"")
        for subfolder in sp_folder.folders:
            subfolder_name = subfolder.properties.get("Name")
            subfolder_path = (
                f"{base_path}/{subfolder_name}" if base_path else subfolder_name
            )
            add_folder_to_zip(subfolder, zipf, subfolder_path)

    with zipfile.ZipFile(zip_name, "w") as zipf:
        root_folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        add_folder_to_zip(root_folder, zipf, "")
    logging.info("Zipped and downloaded folder (recursive): %s", zip_name)


@mcp.tool()
def get_file_by_id(file_id: str) -> dict:
    """Retrieve a file using its unique SharePoint ID."""
    ctx = _authenticate_cloud_sp()
    file = ctx.web.get_file_by_id(file_id).get().execute_query()
    logging.info("Retrieved file by ID: %s", file.serverRelativeUrl)
    return {
        "name": file.name,
        "url": file.serverRelativeUrl,
        "size": file.length,
        "created": file.time_created,
        "modified": file.time_last_modified,
    }


@mcp.tool()
def get_file_versions(file_url: str) -> dict:
    """Get version history of a SharePoint file.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        file_url: Server relative URL of the file (e.g., '/sites/mysite/Shared Documents/file.txt')
    Returns:
        Dict with success status and list of file versions.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the file
        file = ctx.web.get_file_by_server_relative_url(file_url)
        ctx.load(file)
        ctx.execute_query()

        # Get versions
        versions = file.versions
        ctx.load(versions)
        ctx.execute_query()

        version_list = []
        for version in versions:
            version_list.append(
                {
                    "version_id": version.properties.get("ID"),
                    "version_label": version.properties.get("VersionLabel"),
                    "created": str(version.properties.get("Created")),
                    "created_by": version.properties.get("CreatedBy", {}).get(
                        "Title", "Unknown"
                    ),
                    "size": version.properties.get("Size"),
                    "url": version.properties.get("Url"),
                    "is_current": version.properties.get("IsCurrentVersion", False),
                }
            )

        logging.info("Retrieved %d versions for file: %s", len(version_list), file_url)
        return {
            "success": True,
            "file_url": file_url,
            "version_count": len(version_list),
            "versions": version_list,
        }
    except Exception as e:
        logging.error("Failed to get file versions: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def restore_file_version(file_url: str, version_label: str) -> dict:
    """Restore a previous version of a SharePoint file.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        file_url: Server relative URL of the file (e.g., '/sites/mysite/Shared Documents/file.txt')
        version_label: Version label to restore (e.g., "1.0", "2.0").
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the file
        file = ctx.web.get_file_by_server_relative_url(file_url)
        ctx.load(file)
        ctx.execute_query()

        # Get versions
        versions = file.versions
        ctx.load(versions)
        ctx.execute_query()

        # Find the specific version
        target_version = None
        for version in versions:
            if version.properties.get("VersionLabel") == version_label:
                target_version = version
                break

        if not target_version:
            return {
                "success": False,
                "message": f"Version '{version_label}' not found for file '{file_url}'",
            }

        # Restore the version
        target_version.restore().execute_query()

        logging.info("Restored file '%s' to version %s", file_url, version_label)
        return {
            "success": True,
            "message": f"File restored to version {version_label}",
            "file_url": file_url,
            "restored_version": version_label,
        }
    except Exception as e:
        logging.error("Failed to restore file version: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def read_file_content(file_url: str, encoding: str = "utf-8") -> dict:
    """Read the content of a file from SharePoint as text.

    IMPORTANT: file_url must be a full server relative path starting with '/'.
    If you only have a filename, call search_sharepoint(search_query="filename", search_type="file") first
    to get the full path, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        import io

        file = ctx.web.get_file_by_server_relative_url(file_url)
        file_stream = io.BytesIO()
        file.download(file_stream).execute_query()
        file_stream.seek(0)
        content = file_stream.read().decode(encoding)
        return {"success": True, "file_url": file_url, "content": content}
    except Exception as e:
        logging.error("Failed to read file content: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_recent_files(folder_url: str, count: int = 10) -> dict:
    """Get the most recently modified files in a SharePoint folder.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        folder.expand(["Files"]).get().execute_query()
        files = sorted(
            folder.files,
            key=lambda f: f.properties.get("TimeLastModified", ""),
            reverse=True,
        )
        recent_files = [
            {
                "name": f.properties.get("Name"),
                "url": f.properties.get("ServerRelativeUrl"),
                "modified": str(f.properties.get("TimeLastModified")),
            }
            for f in files[:count]
        ]
        return {"success": True, "folder_url": folder_url, "recent_files": recent_files}
    except Exception as e:
        logging.error("Failed to get recent files: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def create_sharepoint_folder(folder_url: str) -> dict:
    """Create a folder in SharePoint using username/password authentication.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        folder_url: Server relative URL of the folder to create
    Returns:
        Dict with success status and message
    """
    try:
        ctx = _authenticate_cloud_sp()
        if not ctx:
            return {"success": False, "message": "SharePoint authentication failed."}
        parent_folder_url, new_folder_name = os.path.split(folder_url)
        parent_folder = ctx.web.get_folder_by_server_relative_url(parent_folder_url)
        parent_folder.add(new_folder_name).execute_query()
        logging.info("Created folder: %s", folder_url)
        return {
            "folder_url": folder_url,
            "success": True,
            "message": "Folder created successfully",
        }
    except (OSError, ValueError, ClientRequestException) as error_msg:
        logging.error("Failed to create folder: %s", error_msg)
        return {"success": False, "message": f"Create folder failed: {error_msg}"}
    except Exception as exc:
        logging.error("Unexpected error in create_sharepoint_folder: %s", exc)
        return {"success": False, "message": f"Unexpected error: {exc}"}


@mcp.tool()
def delete_sharepoint_folder(folder_url: str) -> dict:
    """Delete a folder from SharePoint.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        folder_url: Server relative URL of the folder to delete (e.g., '/sites/mysite/Shared Documents/FolderName')
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the folder
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        ctx.load(folder)
        ctx.execute_query()

        # Delete the folder
        folder.delete_object().execute_query()

        logging.info("Successfully deleted folder: %s", folder_url)
        return {
            "success": True,
            "message": "Folder deleted successfully",
            "folder_url": folder_url,
        }
    except Exception as e:
        logging.error("Failed to delete folder: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def rename_folder(folder_url: str, new_name: str) -> dict:
    """Rename a folder in SharePoint.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        list_item = folder.list_item_all_fields
        ctx.load(list_item)
        ctx.execute_query()
        list_item.set_property("FileLeafRef", new_name)
        list_item.update()
        ctx.execute_query()
        parent_url = "/".join(folder_url.split("/")[:-1])
        new_url = f"{parent_url}/{new_name}"
        logging.info("Renamed folder %s to %s", folder_url, new_url)
        return {"success": True, "old_url": folder_url, "new_url": new_url}
    except Exception as e:
        logging.error("Failed to rename folder: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def move_folder(source_folder_url: str, target_folder_url: str) -> dict:
    """Move a folder to another location in SharePoint.

    IMPORTANT: source_folder_url and target_folder_url must be full server relative paths starting with '/'.
    If you only have folder names, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full paths, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        folder = ctx.web.get_folder_by_server_relative_url(source_folder_url)
        folder.move_to(target_folder_url).execute_query()
        logging.info("Moved folder from %s to %s", source_folder_url, target_folder_url)
        return {
            "success": True,
            "source_url": source_folder_url,
            "target_url": target_folder_url,
        }
    except Exception as e:
        logging.error("Failed to move folder: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def copy_folder(source_folder_url: str, target_folder_url: str) -> dict:
    """Copy a folder to another location in SharePoint, including the folder itself.

    IMPORTANT: source_folder_url and target_folder_url must be full server relative paths starting with '/'.
    If you only have folder names, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full paths, then use the 'server_relative_url' from the search results.
    """
    try:
        ctx = _authenticate_cloud_sp()
        import io

        source_folder = ctx.web.get_folder_by_server_relative_url(source_folder_url)
        target_parent_folder = ctx.web.get_folder_by_server_relative_url(
            target_folder_url
        )

        # Create the folder itself in the target location
        source_folder_name = source_folder_url.rstrip("/").split("/")[-1]
        new_folder = target_parent_folder.add(source_folder_name).execute_query()

        # Recursively copy files and subfolders
        def recursive_copy(src_folder, tgt_folder):
            src_folder.expand(["Files", "Folders"]).get().execute_query()
            for file in src_folder.files:
                file_stream = io.BytesIO()
                file.download(file_stream).execute_query()
                file_stream.seek(0)
                tgt_folder.upload_file(
                    file.properties["Name"], file_stream.read()
                ).execute_query()
            for subfolder in src_folder.folders:
                new_subfolder = tgt_folder.add(
                    subfolder.properties["Name"]
                ).execute_query()
                recursive_copy(subfolder, new_subfolder)

        recursive_copy(source_folder, new_folder)
        logging.info(
            "Copied folder from %s to %s", source_folder_url, target_folder_url
        )
        return {
            "success": True,
            "source_url": source_folder_url,
            "target_url": target_folder_url,
        }
    except Exception as e:
        logging.error("Failed to copy folder: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def search_sharepoint(
    search_query: str, search_type: str = "both", max_results: int = 100
) -> dict:
    """Search across entire SharePoint site for files and/or folders.
    Args:
        search_query: The name or partial name to search for.
        search_type: Type of items to search - 'file', 'folder', or 'both' (default: 'both').
        max_results: Maximum number of results to return (default: 100).
    Returns:
        Dict with search results including file/folder names, types, URLs, and full SharePoint links.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Normalize search query and type
        search_query_lower = search_query.lower()
        search_type = search_type.lower()

        if search_type not in ["file", "folder", "both"]:
            return {
                "success": False,
                "message": "search_type must be 'file', 'folder', or 'both'",
            }

        results: List[Dict[str, Any]] = []

        def search_in_folder(folder_url: str, depth: int = 0):
            """Recursively search in folder and subfolders."""
            if len(results) >= max_results or depth > 10:  # Prevent infinite recursion
                return

            try:
                folder = ctx.web.get_folder_by_server_relative_url(folder_url)
                folder.expand(["Files", "Folders"]).get().execute_query()

                # Search files if needed
                if search_type in ["file", "both"]:
                    for file in folder.files:
                        if len(results) >= max_results:
                            break

                        file_name = file.properties.get("Name", "")
                        if search_query_lower in file_name.lower():
                            server_relative_url = file.properties.get(
                                "ServerRelativeUrl", ""
                            )
                            # Construct full SharePoint URL with proper encoding
                            from urllib.parse import urlparse, quote

                            parsed_site_url = urlparse(sharepoint_site_url)
                            base_url = (
                                f"{parsed_site_url.scheme}://{parsed_site_url.netloc}"
                            )
                            # Encode the URL path while preserving the forward slashes
                            encoded_path = quote(server_relative_url, safe="/")
                            full_url = f"{base_url}{encoded_path}"

                            results.append(
                                {
                                    "type": "file",
                                    "name": file_name,
                                    "server_relative_url": server_relative_url,
                                    "full_url": full_url,
                                    "size": file.properties.get("Length", 0),
                                    "modified": str(
                                        file.properties.get("TimeLastModified", "")
                                    ),
                                    "created": str(
                                        file.properties.get("TimeCreated", "")
                                    ),
                                    "folder_path": folder_url,
                                }
                            )

                # Search folders if needed
                if search_type in ["folder", "both"]:
                    for subfolder in folder.folders:
                        folder_name = subfolder.properties.get("Name", "")

                        # Skip system folders
                        if folder_name.startswith("_") or folder_name in [
                            "Forms",
                            "Item",
                        ]:
                            continue

                        server_relative_url = subfolder.properties.get(
                            "ServerRelativeUrl", ""
                        )

                        # Check if folder name matches search query
                        if search_query_lower in folder_name.lower():
                            if len(results) < max_results:
                                # Construct full SharePoint URL with proper encoding
                                from urllib.parse import urlparse, quote

                                parsed_site_url = urlparse(sharepoint_site_url)
                                base_url = f"{parsed_site_url.scheme}://{parsed_site_url.netloc}"
                                # Encode the URL path while preserving the forward slashes
                                encoded_path = quote(server_relative_url, safe="/")
                                full_url = f"{base_url}{encoded_path}"

                                results.append(
                                    {
                                        "type": "folder",
                                        "name": folder_name,
                                        "server_relative_url": server_relative_url,
                                        "full_url": full_url,
                                        "item_count": subfolder.properties.get(
                                            "ItemCount", 0
                                        ),
                                        "modified": str(
                                            subfolder.properties.get(
                                                "TimeLastModified", ""
                                            )
                                        ),
                                        "created": str(
                                            subfolder.properties.get("TimeCreated", "")
                                        ),
                                        "parent_folder": folder_url,
                                    }
                                )

                        # Recursively search in subfolder
                        if len(results) < max_results:
                            search_in_folder(server_relative_url, depth + 1)

            except Exception as e:
                logging.debug("Error searching folder %s: %s", folder_url, e)

        # Start search from root document libraries
        try:
            web = ctx.web
            lists = (
                web.lists.filter("BaseTemplate eq 101").get().execute_query()
            )  # 101 = Document Library

            for doc_lib in lists:
                if len(results) >= max_results:
                    break

                lib_title = doc_lib.properties.get("Title", "")
                # Skip hidden or system libraries
                if doc_lib.properties.get("Hidden", False):
                    continue

                root_folder = doc_lib.root_folder
                ctx.load(root_folder)
                ctx.execute_query()

                root_url = root_folder.properties.get("ServerRelativeUrl", "")
                logging.info(
                    "Searching in document library: %s (%s)", lib_title, root_url
                )
                search_in_folder(root_url)

        except Exception as e:
            logging.error("Error getting document libraries: %s", e)
            # Fallback: search in common locations
            common_paths = ["Shared Documents", "Documents"]

            for path in common_paths:
                if len(results) >= max_results:
                    break
                try:
                    search_in_folder(path)
                except Exception as path_error:
                    logging.debug("Could not search path %s: %s", path, path_error)

        # Sort results by relevance (exact matches first, then by modification date)
        def sort_key(item):
            exact_match = item["name"].lower() == search_query_lower
            return (not exact_match, item.get("modified", ""))

        results.sort(key=sort_key, reverse=False)

        logging.info(
            "Search completed. Found %d results for '%s'", len(results), search_query
        )

        return {
            "success": True,
            "search_query": search_query,
            "search_type": search_type,
            "results": results,
            "count": len(results),
            "message": f"Found {len(results)} result(s) matching '{search_query}'",
        }

    except Exception as e:
        logging.error("Search error: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def list_sharepoint_sites() -> dict:
    """List accessible SharePoint sites.

    IMPORTANT: If you only have a partial site name, call
    search_sharepoint(search_query="sitename", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the
    search results.

    Returns:
        Dict with success status and site details.
    """
    try:
        from urllib.parse import urlparse

        tenant_url = (
            f"{urlparse(sharepoint_site_url).scheme}://"
            f"{urlparse(sharepoint_site_url).netloc}"
        )
        ctx = ClientContext(tenant_url).with_credentials(
            UserCredential(sp_username, sp_password)
        )

        from office365.sharepoint.tenant.administration.tenant import Tenant

        site_properties = Tenant(ctx).get_site_properties_from_sharepoint_by_filters(
            "", 0, False
        )
        ctx.execute_query()

        sites = [
            {
                "title": s.properties.get("Title", ""),
                "url": s.properties.get("Url", ""),
                "owner": s.properties.get("Owner", ""),
            }
            for s in site_properties
        ]

        return {"sites": sites, "count": len(sites), "success": True}
    except Exception as e:
        logging.error("List sites error: %s", e)
        return {
            "sites": [{"url": sharepoint_site_url}],
            "count": 1,
            "success": True,
            "note": str(e),
        }


@mcp.tool()
def get_sharepoint_site_info(site_url: Optional[str] = None) -> dict:
    """Get detailed information about a SharePoint site.

    IMPORTANT: site_url must be a full server relative path starting with '/'.
    If you only have a site name, call search_sharepoint(search_query="sitename", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        site_url: Server relative URL of the site (optional).
    Returns:
        Dict with success status and site details.
    """
    try:
        target_url = site_url or sharepoint_site_url
        ctx = ClientContext(target_url).with_credentials(
            UserCredential(sp_username, sp_password)
        )

        web = ctx.web
        ctx.load(web)
        ctx.execute_query()

        lists = web.lists
        ctx.load(lists)
        ctx.execute_query()

        return {
            "title": web.properties.get("Title", ""),
            "url": web.properties.get("Url", ""),
            "created": str(web.properties.get("Created", "")),
            "lists": [
                {
                    "title": lst.properties.get("Title", ""),
                    "items": lst.properties.get("ItemCount", 0),
                }
                for lst in lists
                if not lst.properties.get("Hidden", True)
            ],
            "success": True,
        }
    except Exception as e:
        logging.error("Get site info error: %s", e)
        return {"success": False, "message": str(e)}


@mcp.tool()
def list_sharepoint_site_contents() -> dict:
    """List all contents (files, folders, and lists) of a SharePoint site.

    IMPORTANT: If you only have a partial site name, call
    search_sharepoint(search_query="sitename", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the
    search results.

    Returns:
        Dict with success status and site contents.
    """
    try:
        ctx = _authenticate_cloud_sp()
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()

        # Fetch lists
        lists = web.lists.get().execute_query()
        list_details = [
            {"title": sp_list.properties["Title"], "id": sp_list.properties["Id"]}
            for sp_list in lists
        ]

        # Fetch site folders and files
        folders = web.folders.get().execute_query()
        folder_details = [
            {
                "name": folder.properties["Name"],
                "url": folder.properties["ServerRelativeUrl"],
            }
            for folder in folders
        ]

        return {
            "success": True,
            "site_title": web.properties.get("Title"),
            "lists": list_details,
            "folders": folder_details,
        }
    except Exception as e:
        logging.error("Failed to list SharePoint site contents: %s", e)
        return {"success": False, "message": str(e)}


@mcp.tool()
def create_sharepoint_list(list_name: str, description: str = "") -> dict:
    """Create a new SharePoint list.
    Args:
        list_name: Name of the list to create.
        description: Description of the list (optional).
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()
        list_creation_info = {
            "Title": list_name,
            "Description": description,
            "BaseTemplate": 100,  # Custom list template
            "__metadata": {"type": "SP.List"},
        }
        sp_list = ctx.web.lists.add(list_creation_info).execute_query()
        logging.info("Created SharePoint list: %s", list_name)
        return {
            "success": True,
            "message": f"List '{list_name}' created successfully.",
            "list_id": sp_list.id,
        }
    except Exception as e:
        logging.error("Failed to create SharePoint list: %s", e)
        return {"success": False, "message": str(e)}


@mcp.tool()
def fetch_sharepoint_lists() -> dict:
    """Fetch all available SharePoint lists.

    IMPORTANT: If you only have a partial list name, call
    search_sharepoint(search_query="listname", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the
    search results.

    Returns:
        Dict with success status and list details.
    """
    try:
        ctx = _authenticate_cloud_sp()
        lists = ctx.web.lists.get().execute_query()
        list_details = [
            {"title": sp_list.properties["Title"], "id": sp_list.properties["Id"]}
            for sp_list in lists
        ]
        logging.info("Fetched SharePoint lists: %d lists found", len(list_details))
        return {"success": True, "lists": list_details}
    except Exception as e:
        logging.error("Failed to fetch SharePoint lists: %s", e)
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_sharepoint_list_link(list_name: str) -> dict:
    """Retrieve the URL of a specific SharePoint list by its name.
    Args:
        list_name: Name of the SharePoint list.
    Returns:
        Dict with success status and the list URL.
    """
    try:
        ctx = _authenticate_cloud_sp()
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}
        list_url = f"{sharepoint_site_url}/Lists/{list_name}"
        logging.info("Retrieved URL for SharePoint list: %s", list_name)
        return {"success": True, "list_url": list_url}
    except Exception as e:
        logging.error("Failed to retrieve SharePoint list URL: %s", e)
        return {"success": False, "message": str(e)}


@mcp.tool()
def fetch_sharepoint_list_content(list_name: str) -> dict:
    """Fetch the content (items) of a specific SharePoint list.

    IMPORTANT: list_name must be the exact name of the list. If you only
    have a partial name, call
    search_sharepoint(search_query="listname", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the
    search results.

    Args:
        list_name: Name of the SharePoint list.
    Returns:
        Dict with success status and list content.
    """
    try:
        ctx = _authenticate_cloud_sp()
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}
        sp_list = lists[0]
        items = sp_list.items.get().execute_query()

        # Convert items to serializable format
        content = []
        for item in items:
            item_dict: Dict[str, Any] = {}
            for key, value in item.properties.items():
                # Convert non-serializable types to strings
                if value is None:
                    item_dict[key] = None
                elif isinstance(value, (str, int, float, bool)):
                    item_dict[key] = value
                elif isinstance(value, dict):
                    # Convert nested dicts to string to avoid type issues
                    item_dict[key] = str(value)
                else:
                    # Convert other types to strings
                    item_dict[key] = str(value)
            content.append(item_dict)

        logging.info(
            "Fetched content for SharePoint list '%s': %d items",
            list_name,
            len(content),
        )
        return {
            "success": True,
            "list_name": list_name,
            "item_count": len(content),
            "content": content,
        }
    except Exception as e:
        logging.error("Failed to fetch SharePoint list content: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def add_list_item(list_name: str, item_data: dict) -> dict:
    """Add a new item to a SharePoint list.
    Args:
        list_name: Name of the SharePoint list.
        item_data: Dictionary containing field names and values for the new item.
    Returns:
        Dict with success status and created item details.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Add new item using the correct method
        item_creation_info = {"Title": item_data.get("Title", "")}
        new_item = sp_list.add_item(item_creation_info).execute_query()

        logging.info(
            "Added item to list '%s': ID %s", list_name, new_item.properties.get("Id")
        )
        return {
            "success": True,
            "message": f"Item added successfully to list '{list_name}'",
            "item_id": new_item.properties.get("Id"),
            "item_data": item_data,
        }
    except Exception as e:
        logging.error("Failed to add list item: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def update_list_item(list_name: str, item_id: int, item_data: dict) -> dict:
    """Update an existing item in a SharePoint list.
    Args:
        list_name: Name of the SharePoint list.
        item_id: ID of the item to update.
        item_data: Dictionary containing field names and new values.
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Get the item by ID
        item = sp_list.items.get_by_id(item_id)
        ctx.load(item)
        ctx.execute_query()

        # Update the item
        for key, value in item_data.items():
            item.set_property(key, value)
        item.update()
        ctx.execute_query()

        logging.info("Updated item ID %s in list '%s'", item_id, list_name)
        return {
            "success": True,
            "message": f"Item ID {item_id} updated successfully in list '{list_name}'",
            "item_id": item_id,
            "updated_fields": item_data,
        }
    except Exception as e:
        logging.error("Failed to update list item: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def delete_list_item(list_name: str, item_id: int) -> dict:
    """Delete an item from a SharePoint list.
    Args:
        list_name: Name of the SharePoint list.
        item_id: ID of the item to delete.
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Get and delete the item
        item = sp_list.items.get_by_id(item_id)
        item.delete_object().execute_query()

        logging.info("Deleted item ID %s from list '%s'", item_id, list_name)
        return {
            "success": True,
            "message": f"Item ID {item_id} deleted successfully from list '{list_name}'",
            "item_id": item_id,
        }
    except Exception as e:
        logging.error("Failed to delete list item: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def export_list_to_csv(list_name: str, csv_path: str) -> dict:
    """Export the contents of a SharePoint list to a CSV file."""
    import csv

    try:
        ctx = _authenticate_cloud_sp()
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}
        sp_list = lists[0]
        items = sp_list.items.get().execute_query()
        if not items:
            return {
                "success": True,
                "message": "No items to export.",
                "csv_path": csv_path,
            }
        fieldnames = list(items[0].properties.keys())
        with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in items:
                writer.writerow(item.properties)
        logging.info("Exported list '%s' to CSV: %s", list_name, csv_path)
        return {"success": True, "csv_path": csv_path, "item_count": len(items)}
    except Exception as e:
        logging.error("Failed to export list to CSV: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_list_schema(list_name: str) -> dict:
    """Get complete schema structure of a SharePoint list including all fields/columns.

    Args:
        list_name: Name of the SharePoint list.
    Returns:
        Dict with success status and complete list schema including fields, content types, and settings.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Load fields
        fields = sp_list.fields
        ctx.load(fields)
        ctx.execute_query()

        # Extract field details
        field_list = []
        for field in fields:
            field_info = {
                "internal_name": field.properties.get("InternalName"),
                "title": field.properties.get("Title"),
                "type": field.properties.get("TypeAsString"),
                "required": field.properties.get("Required", False),
                "hidden": field.properties.get("Hidden", False),
                "read_only": field.properties.get("ReadOnlyField", False),
                "id": field.properties.get("Id"),
                "description": field.properties.get("Description", ""),
                "default_value": field.properties.get("DefaultValue", ""),
            }
            field_list.append(field_info)

        # Get list properties
        list_info = {
            "title": sp_list.properties.get("Title"),
            "description": sp_list.properties.get("Description"),
            "item_count": sp_list.properties.get("ItemCount"),
            "base_template": sp_list.properties.get("BaseTemplate"),
            "created": str(sp_list.properties.get("Created")),
            "last_modified": str(sp_list.properties.get("LastItemModifiedDate")),
            "enable_versioning": sp_list.properties.get("EnableVersioning", False),
            "enable_attachments": sp_list.properties.get("EnableAttachments", False),
        }

        logging.info(
            "Retrieved schema for list '%s': %d fields", list_name, len(field_list)
        )
        return {
            "success": True,
            "list_name": list_name,
            "list_info": list_info,
            "fields": field_list,
            "field_count": len(field_list),
        }
    except Exception as e:
        logging.error("Failed to get list schema: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def add_list_column(
    list_name: str,
    field_name: str,
    field_type: str,
    required: bool = False,
    description: str = "",
) -> dict:
    """Add a new field/column to a SharePoint list.

    Args:
        list_name: Name of the SharePoint list.
        field_name: Display name for the new field.
        field_type: Type of field. Common types: 'Text', 'Note', 'Number', 'DateTime',
                   'Boolean', 'Choice', 'Lookup', 'User', 'URL', 'Currency'
        required: Whether the field is required (default: False).
        description: Description of the field (optional).
    Returns:
        Dict with success status and field details.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Create field XML based on type
        field_xml = (
            f'<Field Type="{field_type}" DisplayName="{field_name}" '
            f'Required="{str(required).upper()}" Description="{description}" />'
        )

        # Add the field using the correct method
        new_field = sp_list.fields.create_field_as_xml(field_xml)
        ctx.execute_query()

        logging.info("Added field '%s' to list '%s'", field_name, list_name)
        return {
            "success": True,
            "message": f"Field '{field_name}' added successfully to list '{list_name}'",
            "field_id": new_field.properties.get("Id"),
            "field_name": field_name,
            "field_type": field_type,
            "internal_name": new_field.properties.get("InternalName"),
        }
    except Exception as e:
        logging.error("Failed to add list column: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def update_list_column(list_name: str, field_internal_name: str, updates: dict) -> dict:
    """Update properties of an existing field/column in a SharePoint list.

    Args:
        list_name: Name of the SharePoint list.
        field_internal_name: Internal name of the field to update.
        updates: Dictionary of properties to update. Common properties:
                - Title: Display name
                - Required: True/False
                - Description: Field description
                - Hidden: True/False
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Get the field
        field = sp_list.fields.get_by_internal_name_or_title(field_internal_name)
        ctx.load(field)
        ctx.execute_query()

        # Update field properties
        for key, value in updates.items():
            field.set_property(key, value)

        field.update()
        ctx.execute_query()

        logging.info("Updated field '%s' in list '%s'", field_internal_name, list_name)
        return {
            "success": True,
            "message": f"Field '{field_internal_name}' updated successfully in list '{list_name}'",
            "field_internal_name": field_internal_name,
            "updates_applied": updates,
        }
    except Exception as e:
        logging.error("Failed to update list column: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def delete_list_column(list_name: str, field_internal_name: str) -> dict:
    """Delete a field/column from a SharePoint list.

    Args:
        list_name: Name of the SharePoint list.
        field_internal_name: Internal name of the field to delete.
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the list
        lists = ctx.web.lists.filter(f"Title eq '{list_name}'").get().execute_query()
        if not lists:
            return {"success": False, "message": f"List '{list_name}' not found."}

        sp_list = lists[0]

        # Get the field
        field = sp_list.fields.get_by_internal_name_or_title(field_internal_name)
        ctx.load(field)
        ctx.execute_query()

        # Check if field can be deleted (some system fields cannot be deleted)
        if field.properties.get("ReadOnlyField", False) or field.properties.get(
            "Sealed", False
        ):
            return {
                "success": False,
                "message": f"Field '{field_internal_name}' is a system field and cannot be deleted.",
            }

        # Delete the field
        field.delete_object()
        ctx.execute_query()

        logging.info(
            "Deleted field '%s' from list '%s'", field_internal_name, list_name
        )
        return {
            "success": True,
            "message": f"Field '{field_internal_name}' deleted successfully from list '{list_name}'",
            "field_internal_name": field_internal_name,
        }
    except Exception as e:
        logging.error("Failed to delete list column: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_recycle_bin_items(include_secondary: bool = False) -> dict:
    """Get items in the SharePoint recycle bin.
    Args:
        include_secondary: If True, includes second-stage recycle bin items (default: False).
    Returns:
        Dict with success status and list of recycled items.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get recycle bin items
        recycle_items = ctx.web.recycle_bin
        ctx.load(recycle_items)
        ctx.execute_query()

        items_list = []
        for item in recycle_items:
            # Filter based on recycle bin stage
            item_stage = item.properties.get("ItemState", 1)
            # Stage 1 = First-stage recycle bin, Stage 2 = Second-stage (site collection)
            if not include_secondary and item_stage == 2:
                continue

            items_list.append(
                {
                    "id": item.properties.get("Id"),
                    "title": item.properties.get("Title"),
                    "original_location": item.properties.get("DirName"),
                    "deleted_by": item.properties.get("DeletedByName"),
                    "deleted_date": str(item.properties.get("DeletedDate")),
                    "size": item.properties.get("Size"),
                    "item_type": "File"
                    if item.properties.get("ItemType") == 1
                    else "Folder",
                    "stage": "First-stage" if item_stage == 1 else "Second-stage",
                }
            )

        logging.info("Retrieved %d recycle bin items", len(items_list))
        return {
            "success": True,
            "item_count": len(items_list),
            "items": items_list,
            "include_secondary": include_secondary,
        }
    except Exception as e:
        logging.error("Failed to get recycle bin items: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def restore_recycle_bin_item(item_id: str) -> dict:
    """Restore an item from the SharePoint recycle bin to its original location.
    Args:
        item_id: ID of the recycle bin item to restore.
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the recycle bin item
        recycle_items = ctx.web.recycle_bin
        ctx.load(recycle_items)
        ctx.execute_query()

        # Find the item by ID
        target_item = None
        for item in recycle_items:
            if str(item.properties.get("Id")) == str(item_id):
                target_item = item
                break

        if not target_item:
            return {
                "success": False,
                "message": f"Recycle bin item with ID '{item_id}' not found",
            }

        # Restore the item
        target_item.restore().execute_query()

        logging.info("Restored recycle bin item: %s", item_id)
        return {
            "success": True,
            "message": "Item restored successfully",
            "item_id": item_id,
            "original_location": target_item.properties.get("DirName"),
        }
    except Exception as e:
        logging.error("Failed to restore recycle bin item: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def delete_recycle_bin_item(item_id: str) -> dict:
    """Permanently delete an item from the SharePoint recycle bin.
    Args:
        item_id: ID of the recycle bin item to permanently delete.
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get the recycle bin item
        recycle_items = ctx.web.recycle_bin
        ctx.load(recycle_items)
        ctx.execute_query()

        # Find the item by ID
        target_item = None
        for item in recycle_items:
            if str(item.properties.get("Id")) == str(item_id):
                target_item = item
                break

        if not target_item:
            return {
                "success": False,
                "message": f"Recycle bin item with ID '{item_id}' not found",
            }

        # Permanently delete the item
        target_item.delete_object().execute_query()

        logging.info("Permanently deleted recycle bin item: %s", item_id)
        return {
            "success": True,
            "message": "Item permanently deleted from recycle bin",
            "item_id": item_id,
        }
    except Exception as e:
        logging.error("Failed to delete recycle bin item: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def empty_recycle_bin(include_secondary: bool = False) -> dict:
    """Empty the SharePoint recycle bin (permanently delete all items).
    Args:
        include_secondary: If True, also empties second-stage recycle bin (default: False).
    Returns:
        Dict with success status and message.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get all recycle bin items
        recycle_items = ctx.web.recycle_bin
        ctx.load(recycle_items)
        ctx.execute_query()

        deleted_count = 0
        for item in recycle_items:
            item_stage = item.properties.get("ItemState", 1)

            # Skip second-stage items if not requested
            if not include_secondary and item_stage == 2:
                continue

            try:
                item.delete_object().execute_query()
                deleted_count += 1
            except Exception as item_error:
                logging.warning(
                    "Failed to delete item %s: %s",
                    item.properties.get("Id"),
                    item_error,
                )

        logging.info("Emptied recycle bin: %d items deleted", deleted_count)
        return {
            "success": True,
            "message": "Recycle bin emptied successfully",
            "items_deleted": deleted_count,
            "include_secondary": include_secondary,
        }
    except Exception as e:
        logging.error("Failed to empty recycle bin: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def restore_all_recycle_bin_items(include_secondary: bool = False) -> dict:
    """Restore all items from the SharePoint recycle bin to their original locations.
    Args:
        include_secondary: If True, also restores second-stage recycle bin items (default: False).
    Returns:
        Dict with success status and count of restored items.
    """
    try:
        ctx = _authenticate_cloud_sp()

        # Get all recycle bin items
        recycle_items = ctx.web.recycle_bin
        ctx.load(recycle_items)
        ctx.execute_query()

        restored_count = 0
        failed_count = 0

        for item in recycle_items:
            item_stage = item.properties.get("ItemState", 1)

            # Skip second-stage items if not requested
            if not include_secondary and item_stage == 2:
                continue

            try:
                item.restore().execute_query()
                restored_count += 1
            except Exception as item_error:
                logging.warning(
                    "Failed to restore item %s: %s",
                    item.properties.get("Id"),
                    item_error,
                )
                failed_count += 1

        logging.info("Restored %d items from recycle bin", restored_count)
        return {
            "success": True,
            "message": "Recycle bin restore completed",
            "items_restored": restored_count,
            "items_failed": failed_count,
            "include_secondary": include_secondary,
        }
    except Exception as e:
        logging.error("Failed to restore recycle bin items: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_current_user_info() -> dict:
    """Get detailed information about the current authenticated user.
    Returns:
        Dict with success status and user details.
    """
    try:
        ctx = _authenticate_cloud_sp()
        current_user = ctx.web.current_user
        ctx.load(current_user)
        ctx.execute_query()

        user_info = {
            "id": current_user.properties.get("Id"),
            "login_name": current_user.properties.get("LoginName"),
            "title": current_user.properties.get("Title"),
            "email": current_user.properties.get("Email"),
            "is_site_admin": current_user.properties.get("IsSiteAdmin", False),
        }

        logging.info("Retrieved current user info: %s", user_info.get("login_name"))
        return {"success": True, "user": user_info}
    except Exception as e:
        logging.error("Failed to get current user info: %s", e, exc_info=True)
        return {"success": False, "message": str(e)}


@mcp.tool()
def get_folder_permissions(folder_url: str) -> dict:
    """Get permissions for a specific folder in SharePoint.

    IMPORTANT: folder_url must be a full server relative path starting with '/'.
    If you only have a folder name, call search_sharepoint(search_query="foldername", search_type="folder") first
    to get the full path, then use the 'server_relative_url' from the search results.

    Args:
        folder_url: Server relative URL of the folder (e.g., '/sites/mysite/Shared Documents/FolderName')
    Returns:
        Dict with success status and permission details.
    """
    try:
        ctx = _authenticate_cloud_sp()
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)

        # Get the folder's list item
        list_item = folder.list_item_all_fields
        ctx.load(list_item)
        ctx.execute_query()

        # Get role assignments with proper expansion
        role_assignments = list_item.role_assignments
        for role_assignment in role_assignments:
            ctx.load(role_assignment)
            ctx.load(role_assignment.member)
            ctx.load(role_assignment.role_definition_bindings)
        ctx.execute_query()

        permissions = []
        for role_assignment in role_assignments:
            member = role_assignment.member
            roles = [role.name for role in role_assignment.role_definition_bindings]

            permissions.append(
                {
                    "principal_id": member.properties.get("Id"),
                    "principal_title": member.properties.get("Title"),
                    "principal_type": member.properties.get("PrincipalType"),
                    "login_name": member.properties.get("LoginName", ""),
                    "roles": roles,
                }
            )

        logging.info("Retrieved permissions for folder: %s", folder_url)
        return {"success": True, "folder_url": folder_url, "permissions": permissions}
    except Exception as e:
        logging.error("Failed to get folder permissions: %s", e, exc_info=True)
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
