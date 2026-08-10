import json
import logging
import os
import re
import base64
import html
from typing import List

import requests
from fastmcp import FastMCP

mcp = FastMCP("DocupediaMCPServer")

# Bosch internal Confluence instance details
BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
PAT_TOKEN = os.getenv("CONFLUENCE_PAT_TOKEN")

# Validate required environment variables
missing_vars = [
    name for name, value in {"CONFLUENCE_BASE_URL": BASE_URL, "CONFLUENCE_PAT_TOKEN": PAT_TOKEN}.items() if not value
]
if missing_vars:
    raise ValueError(f"Missing required environment variable(s): {', '.join(missing_vars)}")


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.
    Returns:
        tuple[str, str, int]: A tuple containing:
            - transport_type (str): Transport protocol type, defaults to "stdio"
            - host (str): Server host address, defaults to "127.0.0.1"
            - port (int): Server port number, defaults to 8000
    """
    transport = os.getenv("TRANSPORT") or "stdio"
    if transport in ["stdio", "<TRANSPORT>", None, "", "-", "null"]:
        logging.info("MCP init: transport=stdio")
        return ("stdio", "", 0)

    host = os.getenv("HOST") or "127.0.0.1"
    port_str = os.getenv("HOST_PORT") or "8000"

    if host == "<HOST>":
        host = "127.0.0.1"
    if port_str == "<HOST_PORT>":
        port_str = "8000"

    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"Invalid PORT env variable: '{port_str}' - must be a valid integer")

    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


@mcp.tool()
def find_page_id(space_key: str, page_title: str) -> str:
    """Find a Confluence page ID by space and title.

    Args:
        space_key: The Confluence space key (e.g., "MYSPACE")
        page_title: The exact page title to search for

    Returns:
        JSON string containing the page ID or error message.
    """
    logging.debug(f"Looking up page ID for '{page_title}' in {space_key}")

    if not space_key or not page_title:
        return json.dumps({"error": "Both space_key and page_title are required"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    params = {
        "spaceKey": space_key,
        "title": page_title,
        "type": "page",
        "expand": "space",
    }

    try:
        response = requests.get(f"{BASE_URL}/rest/api/content", headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if data["results"]:
            page_id = data["results"][0]["id"]
            return json.dumps({"page_id": page_id, "title": page_title, "space": space_key})
        else:
            return json.dumps({"error": f"Page '{page_title}' not found in space '{space_key}'"})

    except Exception as e:
        logging.error(f"Error finding page: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_page_content(space_key: str, page_title: str) -> str:
    """Retrieve the full content of a Confluence page.

    Args:
        space_key: The Confluence space key
        page_title: The page title to retrieve

    Returns:
        JSON string containing the page content or error message.
    """
    logging.debug(f"Fetching content for '{page_title}' in {space_key}")

    if not space_key or not page_title:
        return json.dumps({"error": "Both space_key and page_title are required"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    params = {
        "spaceKey": space_key,
        "title": page_title,
        "type": "page",
        "expand": "body.storage,space",
    }

    try:
        response = requests.get(f"{BASE_URL}/rest/api/content", headers=headers, params=params)
        response.raise_for_status()

        data = response.json()
        if data["results"]:
            page = data["results"][0]
            content = page["body"]["storage"]["value"]
            return json.dumps({"title": page_title, "space": space_key, "content": content})
        else:
            return json.dumps({"error": f"Page '{page_title}' not found in space '{space_key}'"})

    except Exception as e:
        logging.error(f"Error reading page content: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def search_confluence(query: str, space_key: str = None, limit: int = 25) -> str:
    """Search for pages in Confluence.

    Args:
        query: Text to search for in page content
        space_key: Optional space to limit search scope
        limit: Maximum number of results to return (1-100)

    Returns:
        JSON string containing search results or error message.
    """
    logging.debug(f"Searching for '{query}'" + (f" in {space_key}" if space_key else ""))

    if not query.strip():
        return json.dumps({"error": "Search query cannot be empty"})

    if limit < 1 or limit > 100:
        return json.dumps({"error": "limit must be between 1 and 100"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    # Build CQL query
    cql = f'text ~ "{query}"'
    if space_key:
        cql += f' and space = "{space_key}"'

    params = {
        "cql": cql,
        "expand": "space",
        "limit": limit,
    }

    try:
        response = requests.get(f"{BASE_URL}/rest/api/content/search", headers=headers, params=params)
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Search error: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def search_with_excerpts(query: str, space_key: str = None, max_results: int = 5) -> str:
    """Search for pages and return content excerpts.

    Args:
        query: Text to search for
        space_key: Optional space to limit search scope
        max_results: Maximum number of pages to return (1-10)

    Returns:
        JSON string containing search results with content excerpts.
    """
    logging.debug(f"Searching with excerpts: '{query}', max={max_results}")

    if not query.strip():
        return json.dumps({"error": "Search query cannot be empty"})

    if max_results < 1 or max_results > 10:
        return json.dumps({"error": "max_results must be between 1 and 10"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    # Search for pages
    cql = f'text ~ "{query}"'
    if space_key:
        cql += f' and space = "{space_key}"'

    search_params = {
        "cql": cql,
        "expand": "space",
        "limit": max_results,
    }

    try:
        search_response = requests.get(f"{BASE_URL}/rest/api/content/search", headers=headers, params=search_params)
        search_response.raise_for_status()
        search_data = search_response.json()

        if not search_data["results"]:
            return json.dumps({"query": query, "results": [], "count": 0})

        results = []

        # Get content for each page
        for page in search_data["results"]:
            content_params = {"expand": "body.storage"}

            try:
                content_response = requests.get(
                    f"{BASE_URL}/rest/api/content/{page['id']}", headers=headers, params=content_params
                )
                content_response.raise_for_status()
                content_data = content_response.json()

                # Clean up HTML content
                html_content = content_data["body"]["storage"]["value"]
                clean_text = re.sub(r"<[^>]+>", "", html_content)
                clean_text = re.sub(r"\s+", " ", clean_text).strip()

                # Create excerpt
                excerpt = clean_text[:400] + "..." if len(clean_text) > 400 else clean_text

                page_url = f"{BASE_URL}/pages/viewpage.action?pageId={page['id']}"
                results.append(
                    {"title": page["title"], "space": page["space"]["key"], "url": page_url, "excerpt": excerpt}
                )

            except Exception as e:
                logging.error(f"Error getting content for page {page['id']}: {e}")
                # Still include the page without excerpt
                page_url = f"{BASE_URL}/pages/viewpage.action?pageId={page['id']}"
                results.append(
                    {
                        "title": page["title"],
                        "space": page["space"]["key"],
                        "url": page_url,
                        "excerpt": "Content unavailable",
                    }
                )

        return json.dumps({"query": query, "results": results, "count": len(results)})

    except Exception as e:
        logging.error(f"Search with excerpts error: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def create_page(space_key: str, page_title: str, content: str, parent_page_id: str = None) -> str:
    """Create a new Confluence page.

    Args:
        space_key: The Confluence space key where the page will be created
        page_title: The title for the new page
        content: The HTML content for the page body
        parent_page_id: Optional parent page ID to create page as child

    Returns:
        JSON string containing the created page information or error message.
    """
    logging.debug(f"Creating page '{page_title}' in space {space_key}")

    if not space_key or not page_title or not content:
        return json.dumps({"error": "space_key, page_title, and content are all required"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    page_data = {
        "type": "page",
        "title": page_title,
        "space": {"key": space_key},
        "body": {"storage": {"value": content, "representation": "storage"}},
    }

    if parent_page_id:
        page_data["ancestors"] = [{"id": parent_page_id}]

    try:
        response = requests.post(f"{BASE_URL}/rest/api/content", headers=headers, json=page_data)
        response.raise_for_status()

        data = response.json()
        page_url = f"{BASE_URL}/pages/viewpage.action?pageId={data['id']}"

        return json.dumps(
            {"success": True, "page_id": data["id"], "title": data["title"], "space": space_key, "url": page_url}
        )

    except Exception as e:
        logging.error(f"Error creating page: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def generate_table_html(table_data_json: str, headers_json: str = None) -> str:
    """Generate Confluence table HTML from data.

    Args:
        table_data_json: JSON string representing table data as array of arrays (e.g., '[["row1col1","row1col2"],["row2col1","row2col2"]]')
        headers_json: Optional JSON string of header column names (e.g., '["Header1","Header2"]')

    Returns:
        JSON string containing the generated HTML table or error message.
    """
    logging.debug("Generating table HTML")

    try:
        # Parse JSON inputs
        table_data = json.loads(table_data_json)
        headers = json.loads(headers_json) if headers_json else None

        if not table_data or not all(isinstance(row, list) for row in table_data):
            return json.dumps({"error": "table_data_json must be a non-empty array of arrays"})

        # Generate table HTML
        table_html = _generate_table_html(table_data, headers)

        return json.dumps(
            {
                "success": True,
                "html": table_html,
                "rows": len(table_data),
                "columns": max(len(row) for row in table_data) if table_data else 0,
            }
        )

    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON format: {e}"})
    except Exception as e:
        logging.error(f"Error generating table HTML: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def update_page_content(page_id: str, content: str, insert_position: str = "append") -> str:
    """Update a Confluence page's content.

    Args:
        page_id: The Confluence page ID to update
        content: The HTML content to insert
        insert_position: Where to insert ("append", "prepend", or "replace")

    Returns:
        JSON string containing the operation result.
    """
    logging.debug(f"Updating page ID {page_id} with insert_position={insert_position}")

    if not all([page_id, content]):
        return json.dumps({"error": "page_id and content are both required"})

    if insert_position not in ["append", "prepend", "replace"]:
        return json.dumps({"error": "insert_position must be 'append', 'prepend', or 'replace'"})

    # Validate basic HTML structure
    if not content.strip():
        return json.dumps({"error": "content cannot be empty"})

    http_headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        # Get current page data
        response = requests.get(
            f"{BASE_URL}/rest/api/content/{page_id}", headers=http_headers, params={"expand": "body.storage,version"}
        )
        response.raise_for_status()
        page_data = response.json()

        current_content = page_data["body"]["storage"]["value"]
        page_title = page_data["title"]
        current_version = page_data["version"]["number"]

        # Determine new content based on insert position
        if insert_position == "prepend":
            new_content = content + current_content
        elif insert_position == "replace":
            new_content = content
        else:  # append
            new_content = current_content + content

        # Update the page
        update_data = {
            "version": {"number": current_version + 1},
            "type": "page",
            "title": page_title,
            "body": {"storage": {"value": new_content, "representation": "storage"}},
        }

        response = requests.put(f"{BASE_URL}/rest/api/content/{page_id}", headers=http_headers, json=update_data)
        response.raise_for_status()

        page_url = f"{BASE_URL}/pages/viewpage.action?pageId={page_id}"

        return json.dumps(
            {
                "success": True,
                "page_id": page_id,
                "title": page_title,
                "url": page_url,
                "insert_position": insert_position,
                "version": current_version + 1,
            }
        )

    except Exception as e:
        logging.error(f"Error updating page content: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_child_pages(page_id: str) -> str:
    """Get all child pages of a Confluence page.

    Args:
        page_id: The parent page ID

    Returns:
        JSON string containing list of child pages or error message.
    """
    logging.debug(f"Getting child pages for page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{BASE_URL}/rest/api/content/{page_id}/child/page", headers=headers, params={"expand": "space"}
        )
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error getting child pages: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_page_history(page_id: str) -> str:
    """Get version history of a Confluence page.

    Args:
        page_id: The page ID to get history for

    Returns:
        JSON string containing version history or error message.
    """
    logging.debug(f"Getting history for page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{BASE_URL}/rest/api/content/{page_id}/history",
            headers=headers,
            params={"expand": "lastUpdated.by,previousVersion.by"},
        )
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error getting page history: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def add_labels_to_page(page_id: str, labels_json: str) -> str:
    """Add labels/tags to a Confluence page.

    Args:
        page_id: The page ID to add labels to
        labels_json: JSON array of label names (e.g., '["important", "draft"]')

    Returns:
        JSON string containing operation result or error message.
    """
    logging.debug(f"Adding labels to page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        labels = json.loads(labels_json)
        if not isinstance(labels, list):
            return json.dumps({"error": "labels_json must be a JSON array"})

        label_objects = [{"prefix": "global", "name": label} for label in labels]

        response = requests.post(f"{BASE_URL}/rest/api/content/{page_id}/label", headers=headers, json=label_objects)
        response.raise_for_status()

        return json.dumps({"success": True, "page_id": page_id, "labels_added": labels})

    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON format: {e}"})
    except Exception as e:
        logging.error(f"Error adding labels: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_page_labels(page_id: str) -> str:
    """Get all labels/tags from a Confluence page.

    Args:
        page_id: The page ID to get labels from

    Returns:
        JSON string containing labels or error message.
    """
    logging.debug(f"Getting labels for page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(f"{BASE_URL}/rest/api/content/{page_id}/label", headers=headers)
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error getting labels: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def add_comment_to_page(page_id: str, comment_text: str) -> str:
    """Add a comment to a Confluence page.

    Args:
        page_id: The page ID to comment on
        comment_text: The comment text (plain text or HTML)

    Returns:
        JSON string containing the created comment info or error message.
    """
    logging.debug(f"Adding comment to page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    # Escape HTML special characters to prevent injection
    escaped_comment = html.escape(comment_text)

    comment_data = {
        "type": "comment",
        "container": {"id": page_id, "type": "page"},
        "body": {"storage": {"value": f"<p>{escaped_comment}</p>", "representation": "storage"}},
    }

    try:
        response = requests.post(f"{BASE_URL}/rest/api/content", headers=headers, json=comment_data)
        response.raise_for_status()
        data = response.json()

        return json.dumps({"success": True, "comment_id": data["id"], "page_id": page_id})

    except Exception as e:
        logging.error(f"Error adding comment: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_page_comments(page_id: str, limit: int = 10) -> str:
    """Get comments from a Confluence page.

    Args:
        page_id: The page ID to get comments from
        limit: Maximum number of comments to return (1-25)

    Returns:
        JSON string containing comments or error message.
    """
    logging.debug(f"Getting comments for page ID {page_id}")

    if limit < 1 or limit > 25:
        return json.dumps({"error": "limit must be between 1 and 25"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{BASE_URL}/rest/api/content/{page_id}/child/comment",
            headers=headers,
            params={"expand": "body.storage,version.by", "limit": limit},
        )
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error getting comments: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def list_spaces(limit: int = 25) -> str:
    """List available Confluence spaces.

    Args:
        limit: Maximum number of spaces to return (1-100)

    Returns:
        JSON string containing list of spaces or error message.
    """
    logging.debug(f"Listing spaces with limit={limit}")

    if limit < 1 or limit > 100:
        return json.dumps({"error": "limit must be between 1 and 100"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(f"{BASE_URL}/rest/api/space", headers=headers, params={"limit": limit})
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error listing spaces: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_space_info(space_key: str) -> str:
    """Get detailed information about a Confluence space.

    Args:
        space_key: The space key to get info for

    Returns:
        JSON string containing space details or error message.
    """
    logging.debug(f"Getting info for space {space_key}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{BASE_URL}/rest/api/space/{space_key}", headers=headers, params={"expand": "description.plain,homepage"}
        )
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error getting space info: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def delete_page(page_id: str) -> str:
    """Delete a Confluence page.

    Args:
        page_id: The page ID to delete

    Returns:
        JSON string containing operation result or error message.
    """
    logging.debug(f"Deleting page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.delete(f"{BASE_URL}/rest/api/content/{page_id}", headers=headers)
        response.raise_for_status()

        return json.dumps({"success": True, "page_id": page_id, "message": "Page deleted successfully"})

    except Exception as e:
        logging.error(f"Error deleting page: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def list_page_attachments(page_id: str) -> str:
    """List all attachments on a Confluence page.

    Args:
        page_id: The page ID to list attachments from

    Returns:
        JSON string containing list of attachments or error message.
    """
    logging.debug(f"Listing attachments for page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(f"{BASE_URL}/rest/api/content/{page_id}/child/attachment", headers=headers)
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error listing attachments: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def upload_attachment(
    page_id: str, file_base64: str, file_name: str, mime_type: str = "application/octet-stream"
) -> str:
    """Upload a file attachment to a Confluence page.

    Args:
        page_id: The Confluence page ID where the file will be attached
        file_base64: Base64 encoded file data
        file_name: Name for the file (e.g., "document.pdf")
        mime_type: MIME type of the file (default: "application/octet-stream")

    Returns:
        JSON string containing upload result.
    """
    logging.debug(f"Uploading attachment '{file_name}' to page ID {page_id}")

    if not all([page_id, file_base64, file_name]):
        return json.dumps({"error": "page_id, file_base64, and file_name are all required"})

    headers = {"Authorization": f"Bearer {PAT_TOKEN}", "X-Atlassian-Token": "no-check"}

    try:
        file_data = base64.b64decode(file_base64)

        files = {"file": (file_name, file_data, mime_type), "comment": (None, "Uploaded via MCP Server")}

        response = requests.post(
            f"{BASE_URL}/rest/api/content/{page_id}/child/attachment", headers=headers, files=files
        )
        response.raise_for_status()

        return json.dumps(response.json())

    except Exception as e:
        logging.error(f"Error uploading attachment: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def move_page(page_id: str, target_parent_id: str = None, target_space_key: str = None) -> str:
    """Move a page to a different parent or space.

    Args:
        page_id: The page ID to move
        target_parent_id: Optional new parent page ID
        target_space_key: Optional target space key (for moving to different space)

    Returns:
        JSON string containing operation result or error message.
    """
    logging.debug(f"Moving page ID {page_id}")

    if not target_parent_id and not target_space_key:
        return json.dumps({"error": "Either target_parent_id or target_space_key must be provided"})

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        # Get current page data
        response = requests.get(
            f"{BASE_URL}/rest/api/content/{page_id}", headers=headers, params={"expand": "body.storage,version,space"}
        )
        response.raise_for_status()
        page_data = response.json()

        update_data = {
            "version": {"number": page_data["version"]["number"] + 1},
            "type": "page",
            "title": page_data["title"],
            "body": page_data["body"],
        }

        if target_space_key:
            update_data["space"] = {"key": target_space_key}

        if target_parent_id:
            update_data["ancestors"] = [{"id": target_parent_id}]

        response = requests.put(f"{BASE_URL}/rest/api/content/{page_id}", headers=headers, json=update_data)
        response.raise_for_status()

        page_url = f"{BASE_URL}/pages/viewpage.action?pageId={page_id}"

        return json.dumps({"success": True, "page_id": page_id, "url": page_url, "message": "Page moved successfully"})

    except Exception as e:
        logging.error(f"Error moving page: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def generate_macro_html(macro_name: str, parameters_json: str = None, body: str = None) -> str:
    """Generate Confluence macro HTML.

    Args:
        macro_name: Name of the macro (e.g., "info", "code", "status")
        parameters_json: Optional JSON object of macro parameters (e.g., '{"title":"Note"}')
        body: Optional macro body content

    Returns:
        JSON string containing the generated macro HTML or error message.
    """
    logging.debug(f"Generating macro HTML for '{macro_name}'")

    try:
        params = json.loads(parameters_json) if parameters_json else {}

        # Build parameter attributes
        param_attrs = ""
        for key, value in params.items():
            param_attrs += f'<ac:parameter ac:name="{key}">{value}</ac:parameter>'

        # Build macro HTML
        if body:
            macro_html = f'<ac:structured-macro ac:name="{macro_name}">{param_attrs}<ac:rich-text-body>{body}</ac:rich-text-body></ac:structured-macro>'
        else:
            macro_html = f'<ac:structured-macro ac:name="{macro_name}">{param_attrs}</ac:structured-macro>'

        return json.dumps({"success": True, "macro_name": macro_name, "html": macro_html})

    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON format: {e}"})
    except Exception as e:
        logging.error(f"Error generating macro HTML: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def watch_page(page_id: str) -> str:
    """Watch a Confluence page for updates.

    Args:
        page_id: The page ID to watch

    Returns:
        JSON string containing operation result or error message.
    """
    logging.debug(f"Watching page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(f"{BASE_URL}/rest/api/user/watch/content/{page_id}", headers=headers)
        response.raise_for_status()

        return json.dumps({"success": True, "page_id": page_id, "message": "Now watching page"})

    except Exception as e:
        logging.error(f"Error watching page: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def unwatch_page(page_id: str) -> str:
    """Stop watching a Confluence page.

    Args:
        page_id: The page ID to unwatch

    Returns:
        JSON string containing operation result or error message.
    """
    logging.debug(f"Unwatching page ID {page_id}")

    headers = {
        "Authorization": f"Bearer {PAT_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.delete(f"{BASE_URL}/rest/api/user/watch/content/{page_id}", headers=headers)
        response.raise_for_status()

        return json.dumps({"success": True, "page_id": page_id, "message": "Stopped watching page"})

    except Exception as e:
        logging.error(f"Error unwatching page: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


def _generate_table_html(table_data: List[List[str]], headers: List[str] = None) -> str:
    """Generate Confluence storage format HTML for a table.

    Args:
        table_data: List of lists representing table rows
        headers: Optional list of header column names

    Returns:
        HTML string in Confluence storage format
    """
    html = "<table><colgroup>"

    # Determine number of columns
    max_cols = max(len(row) for row in table_data) if table_data else 0
    if headers:
        max_cols = max(max_cols, len(headers))

    # Add column definitions
    for _ in range(max_cols):
        html += '<col style="width: auto;" />'
    html += "</colgroup><tbody>"

    # Add header row if provided
    if headers:
        html += "<tr>"
        for header in headers:
            html += f"<th><p><strong>{header}</strong></p></th>"
        # Fill remaining columns if needed
        for _ in range(len(headers), max_cols):
            html += "<th><p></p></th>"
        html += "</tr>"

    # Add data rows
    for row in table_data:
        html += "<tr>"
        for cell in row:
            html += f"<td><p>{cell}</p></td>"
        # Fill remaining columns if needed
        for _ in range(len(row), max_cols):
            html += "<td><p></p></td>"
        html += "</tr>"

    html += "</tbody></table>"
    return html


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    # Start the MCP server (default: stdio)
    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
