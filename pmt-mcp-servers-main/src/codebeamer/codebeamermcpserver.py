import json
import os
import httpx
import logging
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP
import validators
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="/app/.env")

# Load configuration from config.json (optional)
config = {}
config_path = os.path.join(os.path.dirname(__file__), "config.json")
try:
    with open(config_path, "r") as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    # config.json is optional when using environment variables
    pass
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid JSON in config file: {e}")

# Access credentials from environment variables
CB_USER = os.getenv("CB_USER")
CB_PASS = os.getenv("CB_PASS")

# Validate environment variables
if not CB_USER or not CB_PASS:
    raise ValueError("Missing required environment variables: CB_USER, CB_PASS")

# Load CB_BASE_URL from env var or config.json
CB_BASE = os.getenv("CB_BASE_URL") or config.get("CB_BASE_URL")
if not CB_BASE:
    raise ValueError("CB_BASE_URL must be set in environment variables or config.json")

CB_BASE = CB_BASE.rstrip("/")

# Validate CB_BASE_URL
if not validators.url(CB_BASE):
    raise ValueError(f"Invalid URL format for CB_BASE_URL: {CB_BASE}")

logging.info(f"Initialized Codebeamer MCP server with base URL: {CB_BASE}")

mcp = FastMCP("CodebeamerMCPServer")
client = httpx.Client(timeout=45.0, verify=False)


def _header() -> Dict[str, str]:
    return {"Content-Type": "application/json", "Accept": "application/json"}


def _auth():
    return (CB_USER, CB_PASS)


# Helpers for API calls
def _get(path: str, params: Dict[str, Any] | None = None):
    try:
        url = f"{CB_BASE}/api/v3{path}"
        response = client.get(
            url,
            headers=_header(),
            auth=_auth(),
            params=params,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"HTTP {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise ValueError(f"Request failed: {str(e)}")


def _post(path: str, body: Dict[str, Any]):
    try:
        url = f"{CB_BASE}/api/v3{path}"
        response = client.post(url, headers=_header(), auth=_auth(), json=body)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        raise ValueError(f"HTTP {e.response.status_code}: {e.response.text}")
    except httpx.RequestError as e:
        raise ValueError(f"Request failed: {str(e)}")


# MCP Tools
@mcp.tool
def cb_projects(params: Optional[Dict[str, Any]] = None) -> Any:
    """
    GET /api/v3/projects. Forwards query params
    Example: cb_projects(params={"page": 1})
    """
    result = _get("/projects", params=params)
    return result


@mcp.tool
def cb_trackers(project_id: int) -> Dict[str, Any]:
    """List trackers in a project"""
    trackers = _get(f"/projects/{project_id}/trackers")
    return {"project_id": project_id, "count": len(trackers), "trackers": trackers}


@mcp.tool
def cb_tracker_items(
    tracker_id: int, page: int = 1, autopage: bool = False
) -> Dict[str, Any]:
    """
    List items in a tracker. If autopage=True, fetch all pages.
    Returns 'items' and 'nextPageToken' (when autopage=False).
    """
    all_items: List[Dict[str, Any]] = []
    current_page = page
    next_token: Optional[str] = None

    while True:
        params = {"page": current_page}
        data = _get(f"/trackers/{tracker_id}/items", params=params)

        page_items = data.get("itemRefs", [])
        all_items.extend(page_items)

        next_token = data.get("nextPageToken")
        if not autopage or not next_token:
            break
        current_page += 1

    res = {"tracker_id": tracker_id, "items": all_items}
    if not autopage:
        res["nextPageToken"] = next_token
        res["page"] = page
    else:
        res["pages_fetched"] = current_page - page + 1
    return res


@mcp.tool
def cb_item(item_id: int) -> Dict[str, Any]:
    """Get full item JSON by id"""
    result = _get(f"/items/{item_id}")
    return result


@mcp.tool
def cb_fetch_crs_srs_all(
    cbql: str, page: int = 1, workspace: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a CbQL query (POST /items/query). Returns raw result.
    Example: "project.name = 'test'
    AND tracker.name = 'System Requirement Specifications'"

    Args:
        cbql: The CbQL query string
        page: Page number for pagination (default: 1)
        workspace: Optional workspace parameter
    """
    query_body = {"queryString": cbql, "page": page}

    if workspace:
        query_body["workspace"] = workspace

    result = _post("/items/query", query_body)
    return result


def validate_credentials():
    """Validate credentials by making a test API call"""
    try:
        logging.info("Validating credentials with Codebeamer API")
        response = client.get(f"{CB_BASE}/api/v3/projects", auth=(CB_USER, CB_PASS))
        if response.status_code == 401:
            raise ValueError("Authentication failed: Invalid credentials")
        elif response.status_code != 200:
            raise ValueError(
                f"API validation failed with status {response.status_code}"
            )
        logging.info("Credentials validated successfully")
    except httpx.RequestError as e:
        raise ValueError(f"Failed to connect to Codebeamer API: {str(e)}")


# Validate credentials after loading them
validate_credentials()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Starting Codebeamer MCP server")
    mcp.run()
