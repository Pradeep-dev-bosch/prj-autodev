import os
import subprocess
import json
import logging
from typing import Any, Dict, Optional, List, cast
from fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  # fallback for local dev

AZDO_ORG_RAW = os.getenv("AZDO_ORG_URL")
AZDO_PAT_RAW = os.getenv("AZDO_PAT")

if AZDO_ORG_RAW is None or AZDO_PAT_RAW is None:
    raise ValueError("Missing required environment variables: AZDO_ORG_URL, AZDO_PAT")

AZDO_ORG: str = cast(str, AZDO_ORG_RAW)
AZDO_PAT: str = cast(str, AZDO_PAT_RAW)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info(f"Initialized Azure DevOps MCP server for org: {AZDO_ORG}")

mcp = FastMCP("AzureDevOpsMCPServer")


def _az_cli(args: List[str], env: Optional[Dict[str, str]] = None) -> Any:
    """Run az cli with azure-devops extension and return parsed JSON output."""
    base_env = os.environ.copy()
    base_env["AZURE_DEVOPS_EXT_PAT"] = AZDO_PAT
    if env:
        base_env.update(env)
    cmd = ["az"] + args + ["--org", AZDO_ORG, "--output", "json"]
    logging.info(f"Executing command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, env=base_env, capture_output=True, check=True, text=True
        )
        if not result.stdout or result.stdout.strip() == "":
            logging.info("Empty response from Azure CLI")
            return None
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Azure CLI error: {e.stderr}")
        raise RuntimeError(f"Azure CLI error: {e.stderr}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse JSON response: {e}. Output: {result.stdout}")
        return None


@mcp.tool
def azdo_projects() -> Any:
    """List all Azure DevOps projects."""
    return _az_cli(["devops", "project", "list"])


@mcp.tool
def azdo_repos(project: str) -> Any:
    """List all repos in a project."""
    return _az_cli(["repos", "list", "--project", project])


@mcp.tool
def azdo_boards_work_items(project: str, top: int = 10) -> Any:
    """Query latest work items in a project (top N)."""
    wiql_parts = [
        "Select [System.Id], [System.Title], [System.State], [System.WorkItemType]",
        "From WorkItems",
        f"Where [System.TeamProject] = '{project}'",
        "Order By [System.ChangedDate] Desc",
    ]
    wiql = " ".join(wiql_parts)
    base_env = os.environ.copy()
    base_env["AZURE_DEVOPS_EXT_PAT"] = AZDO_PAT
    cmd = [
        "az",
        "boards",
        "query",
        "--wiql",
        wiql,
        "--org",
        AZDO_ORG,
        "--output",
        "json",
    ]
    logging.info(f"Executing command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, env=base_env, capture_output=True, check=True, text=True
        )
        query_result = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"Azure CLI error: {e.stderr}")
        raise RuntimeError(f"Azure CLI error: {e.stderr}")
    if isinstance(query_result, dict):
        work_items = query_result.get("workItems", [])
    elif isinstance(query_result, list):
        work_items = query_result
    else:
        logging.warning(f"Unexpected WIQL query result type: {type(query_result)}")
        work_items = []
    details: List[Any] = []
    for w in work_items[:top]:
        if isinstance(w, dict):
            wid = w.get("id")
            if wid is not None:
                detail = _az_cli(["boards", "work-item", "show", "--id", str(wid)])
                details.append(detail)
        else:
            logging.warning(f"Skipping unexpected work item structure: {w}")
    return details


@mcp.tool
def azdo_agent_pools() -> Any:
    """List agent pools."""
    return _az_cli(["pipelines", "agent", "pool", "list"])


@mcp.tool
def azdo_boards_teams(project: str) -> Any:
    """List teams in a project."""
    return _az_cli(["teams", "list", "--project", project])


@mcp.tool
def azdo_boards_iterations(project: str, team: str) -> Any:
    """List iterations for a team."""
    return _az_cli(
        ["boards", "iteration", "list", "--project", project, "--team", team]
    )


@mcp.tool
def azdo_boards_backlog_levels(project: str, team: str) -> Any:
    """List backlog levels for a team."""
    return _az_cli(["boards", "backlog", "list", "--project", project, "--team", team])


@mcp.tool
def azdo_boards_work_items_by_user(
    assigned_to: str, project: str, top: int = 10
) -> Any:
    """Query work items assigned to a specific user in a project (top N).
    
    Args:
        assigned_to: Email or display name of the user (e.g., 'user@company.com')
        project: Project name to search in
        top: Maximum number of work items to return (default: 10)
    """
    wiql_parts = [
        "Select [System.Id], [System.Title], [System.State], [System.WorkItemType]",
        "From WorkItems",
        f"Where [System.TeamProject] = '{project}'",
        f"AND [System.AssignedTo] = '{assigned_to}'",
        "Order By [System.ChangedDate] Desc",
    ]
    
    wiql = " ".join(wiql_parts)
    
    query_result = _az_cli(["boards", "query", "--wiql", wiql])
    
    if not query_result:
        return {
            "message": f"No work items found for user '{assigned_to}' in project '{project}'",
            "workItems": []
        }
    
    if isinstance(query_result, dict):
        work_items = query_result.get("workItems", [])
    elif isinstance(query_result, list):
        work_items = query_result
    else:
        logging.warning(f"Unexpected WIQL query result type: {type(query_result)}")
        work_items = []
    
    if not work_items:
        return {
            "message": f"No work items found for user '{assigned_to}' in project '{project}'",
            "workItems": []
        }
    
    details: List[Any] = []
    for w in work_items[:top]:
        if isinstance(w, dict):
            wid = w.get("id")
            if wid is not None:
                detail = _az_cli(["boards", "work-item", "show", "--id", str(wid)])
                details.append(detail)
        else:
            logging.warning(f"Skipping unexpected work item structure: {w}")
    
    return details


@mcp.tool
def azdo_boards_work_items_by_user_all_projects(
    assigned_to: str, top: int = 10
) -> Any:
    """Query work items assigned to a specific user across all projects (top N).
    
    Args:
        assigned_to: Email or display name of the user (e.g., 'user@company.com')
        top: Maximum number of work items to return (default: 10)
    """
    wiql_parts = [
        "Select [System.Id], [System.Title], [System.State], [System.WorkItemType]",
        "From WorkItems",
        f"Where [System.AssignedTo] = '{assigned_to}'",
        "Order By [System.ChangedDate] Desc",
    ]
    
    wiql = " ".join(wiql_parts)
    
    query_result = _az_cli(["boards", "query", "--wiql", wiql])
    
    if not query_result:
        return {
            "message": f"No work items found for user '{assigned_to}' across all projects",
            "workItems": []
        }
    
    if isinstance(query_result, dict):
        work_items = query_result.get("workItems", [])
    elif isinstance(query_result, list):
        work_items = query_result
    else:
        logging.warning(f"Unexpected WIQL query result type: {type(query_result)}")
        work_items = []
    
    if not work_items:
        return {
            "message": f"No work items found for user '{assigned_to}' across all projects",
            "workItems": []
        }
    
    details: List[Any] = []
    for w in work_items[:top]:
        if isinstance(w, dict):
            wid = w.get("id")
            if wid is not None:
                detail = _az_cli(["boards", "work-item", "show", "--id", str(wid)])
                details.append(detail)
        else:
            logging.warning(f"Skipping unexpected work item structure: {w}")
    
    return details
    


@mcp.tool
def azdo_boards_update_work_item(
    work_item_id: int,
    state: Optional[str] = None,
    assigned_to: Optional[str] = None,
    title: Optional[str] = None,
) -> Any:
    """Update a work item's state, assignee, or title."""
    args = ["boards", "work-item", "update", "--id", str(work_item_id)]

    if state:
        args.extend(["--state", state])
    if assigned_to:
        args.extend(["--assigned-to", assigned_to])
    if title:
        args.extend(["--title", title])

    return _az_cli(args)


def validate_az_cli():
    """Validate Azure CLI and extension availability."""
    try:
        subprocess.run(["az", "--version"], check=True, capture_output=True)
        subprocess.run(
            ["az", "extension", "show", "--name", "azure-devops"],
            check=True,
            capture_output=True,
        )
        logging.info("Azure CLI and azure-devops extension are available.")
    except subprocess.CalledProcessError:
        raise RuntimeError(
            "Azure CLI or azure-devops extension is not installed in the container."
        )


validate_az_cli()

if __name__ == "__main__":
    logging.info("Starting Azure DevOps MCP server")
    mcp.run()
