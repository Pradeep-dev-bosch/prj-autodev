"""
Bitbucket MCP Server
"""

import base64
import hashlib
import json
import logging
import os
from typing import Optional
from urllib.parse import urlparse

from atlassian import Bitbucket
from fastmcp import FastMCP

# Global client instance
bitbucket: Optional[Bitbucket] = None
ALLOW_DELETION: bool = False

mcp = FastMCP("bitbucket-mcp-server")


def initialize_bitbucket():
    """
    Initializes the global Bitbucket client.

    Raises:
        ValueError: If any required environment variable is missing.

    """

    global bitbucket, ALLOW_DELETION

    # Bitbucket configuration from environment variables
    BITBUCKET_URL = os.getenv("BITBUCKET_URL")
    BITBUCKET_TOKEN = os.getenv("BITBUCKET_TOKEN")
    ALLOW_DELETION = os.getenv("ALLOW_DELETION", "false").lower() == "true"

    # Validate required environment variables
    missing_vars = [
        name
        for name, value in {
            "BITBUCKET_URL": BITBUCKET_URL,
            "BITBUCKET_TOKEN": BITBUCKET_TOKEN,
        }.items()
        if not value
    ]
    if missing_vars:
        raise ValueError(f"Missing required environment variable(s): {', '.join(missing_vars)}")

    # keep domain only in URL
    BITBUCKET_URL = get_base_url(BITBUCKET_URL)

    # Initialize Bitbucket client with session
    bitbucket = Bitbucket(url=BITBUCKET_URL, token=BITBUCKET_TOKEN)
    logging.info("Bitbucket Server client initialized")


def get_base_url(url: str) -> str:
    """
    Extract base URL (scheme + domain) from a full URL.

    Args:
        url: Full URL (e.g., "https://sourcecode01.de.bosch.com/projects/ABCD/repos/xyz/browse")

    Returns:
        str: Base URL (e.g., "https://sourcecode01.de.bosch.com")
    """
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def get_mcp_init_vars() -> tuple[str, str, int]:
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


def safe_serialize(data):
    """
    Recursively convert generators and other non-serializable objects to JSON-safe types.

    Args:
        data: Any Python object that needs to be made JSON-serializable.

    Returns:
        A JSON-serializable version of the input data.
    """
    # Handle None
    if data is None:
        return None

    # Handle basic JSON-serializable types
    if isinstance(data, (str, int, float, bool)):
        return data

    # Handle dictionaries recursively
    if isinstance(data, dict):
        return {key: safe_serialize(value) for key, value in data.items()}

    # Handle lists and tuples
    if isinstance(data, (list, tuple)):
        return [safe_serialize(item) for item in data]

    # Handle sets
    if isinstance(data, set):
        return [safe_serialize(item) for item in data]

    # Handle generators and other iterables (but not strings or bytes)
    if hasattr(data, "__iter__") and not isinstance(data, (str, bytes, bytearray)):
        try:
            # Convert to list and recursively serialize each item
            return [safe_serialize(item) for item in data]
        except TypeError:
            # If iteration fails, convert to string representation
            return str(data)

    # For any other type, try to convert to string
    try:
        # Try to serialize directly first
        json.dumps(data)
        return data
    except (TypeError, ValueError):
        # If that fails, convert to string
        return str(data)


@mcp.tool()
def project_list() -> str:
    """
    Get a list of all projects in Bitbucket.

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "projects": [list of project objects]}
            - On error: {"error": "error message"}
    """
    try:
        projects = bitbucket.project_list()
        return json.dumps({"success": True, "projects": safe_serialize(projects)})
    except Exception as e:
        logging.error(f"Error listing projects: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def repo_list(project_key: str, limit: int = 25) -> str:
    """
    Get a list of repositories in a specific project.

    Args:
        project_key: The unique key identifying the project (e.g., "MYPROJ")
        limit: Maximum number of repositories to return (default: 25)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repositories": [...]}
            - On error: {"error": "error message"}
    """
    try:
        repos = bitbucket.repo_list(project_key, limit=limit)
        return json.dumps({"success": True, "project_key": project_key, "repositories": safe_serialize(repos)})
    except Exception as e:
        logging.error(f"Error listing repositories: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_project(project_key: str) -> str:
    """
    Get detailed information about a specific project.

    Args:
        project_key: The unique key identifying the project (e.g., "MYPROJ")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": {project details}}
            - On error: {"error": "error message"}
    """
    try:
        project = bitbucket.project(project_key)
        return json.dumps({"success": True, "project": safe_serialize(project)})
    except Exception as e:
        logging.error(f"Error getting project: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_project_permissions(
    project_key: str,
    entity_type: str = "users",
    filter_admin_only: bool = False,
    filter_str: str = None,
    limit: int = 99999,
) -> str:
    """
    Get users or groups who have permissions in a project.

    Args:
        project_key: The unique key identifying the project
        entity_type: Type of entity to retrieve - "users" or "groups" (default: "users")
        filter_admin_only: If True, returns only administrators (default: False)
        filter_str: Optional filter string to search for specific users/groups
        limit: Maximum number of results to return (default: 99999)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "entity_type": "...",
                          "admin_only": bool, "results": [...]}
            - On error: {"error": "error message"} or validation error for invalid entity_type

    Example:
        >>> get_project_permissions("MYPROJ", entity_type="users", filter_admin_only=True)
    """
    try:
        if entity_type == "users":
            if filter_admin_only:
                result = bitbucket.project_users_with_administrator_permissions(project_key)
            else:
                result = bitbucket.project_users(project_key, limit=limit, filter_str=filter_str)
        elif entity_type == "groups":
            if filter_admin_only:
                result = bitbucket.project_groups_with_administrator_permissions(project_key)
            else:
                result = bitbucket.project_groups(project_key, limit=limit, filter_str=filter_str)
        else:
            return json.dumps({"error": "entity_type must be 'users' or 'groups'"})

        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "entity_type": entity_type,
                "admin_only": filter_admin_only,
                "results": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error getting project permissions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_repo(project_key: str, repository_slug: str) -> str:
    """
    Get detailed information about a repository.

    Args:
        project_key: The unique key identifying the project
        repository_slug: The repository slug/identifier (e.g., "my-repo")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "repository": {repository details}}
            - On error: {"error": "error message"}
    """
    try:
        repo = bitbucket.get_repo(project_key, repository_slug)
        return json.dumps({"success": True, "repository": safe_serialize(repo)})
    except Exception as e:
        logging.error(f"Error getting repository: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_repo_permissions(
    project_key: str, repo_key: str, entity_type: str = "users", filter_str: str = None, limit: int = 99999
) -> str:
    """
    Get users or groups who have permissions in a repository.

    This consolidated function retrieves permission information for either users or groups
    at the repository level. Useful for auditing access or managing permissions.

    Args:
        project_key: The unique key identifying the project
        repo_key: The repository key/slug
        entity_type: Type of entity to retrieve - "users" or "groups" (default: "users")
        filter_str: Optional filter string to search for specific users/groups
        limit: Maximum number of results to return (default: 99999)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repo_key": "...",
                          "entity_type": "...", "results": [...]}
            - On error: {"error": "error message"} or validation error for invalid entity_type

    Example:
        >>> get_repo_permissions("MYPROJ", "my-repo", entity_type="users")
    """
    try:
        if entity_type == "users":
            result = bitbucket.repo_users(project_key, repo_key, limit=limit, filter_str=filter_str)
        elif entity_type == "groups":
            result = bitbucket.repo_groups(project_key, repo_key, limit=limit, filter_str=filter_str)
        else:
            return json.dumps({"error": "entity_type must be 'users' or 'groups'"})

        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repo_key": repo_key,
                "entity_type": entity_type,
                "results": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error getting repository permissions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def repo_grant_user_permissions(project_key: str, repo_key: str, username: str, permission: str) -> str:
    """
    Grant repository permission to a specific user.

    Assigns a permission level to an individual user for the specified repository.
    Common repository permissions include REPO_READ, REPO_WRITE, and REPO_ADMIN.

    Args:
        project_key: The unique key identifying the project
        repo_key: The repository key/slug
        username: Username of the user to grant permission to
        permission: Permission level (e.g., "REPO_READ", "REPO_WRITE", "REPO_ADMIN")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repo_key": "...",
                          "username": "...", "permission": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> repo_grant_user_permissions("MYPROJ", "my-repo", "john.doe", "REPO_WRITE")
    """
    try:
        result = bitbucket.repo_grant_user_permissions(project_key, repo_key, username, permission)
        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repo_key": repo_key,
                "username": username,
                "permission": permission,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error granting repository user permissions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def repo_grant_group_permissions(project_key: str, repo_key: str, groupname: str, permission: str) -> str:
    """
    Grant repository permission to a specific group.

    Assigns a permission level to a group for the specified repository.
    All users in the group will receive this permission level.

    Args:
        project_key: The unique key identifying the project
        repo_key: The repository key/slug
        groupname: Name of the group to grant permission to
        permission: Permission level (e.g., "REPO_READ", "REPO_WRITE", "REPO_ADMIN")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repo_key": "...",
                          "groupname": "...", "permission": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> repo_grant_group_permissions("MYPROJ", "my-repo", "developers", "REPO_WRITE")
    """
    try:
        result = bitbucket.repo_grant_group_permissions(project_key, repo_key, groupname, permission)
        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repo_key": repo_key,
                "groupname": groupname,
                "permission": permission,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error granting repository group permissions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_branching_model(project_key: str, repo_key: str) -> str:
    """
    Get the branching model configuration for a repository.

    Retrieves the Git Flow or custom branching model configuration that defines
    branch types, prefixes, and naming conventions for the repository.

    Args:
        project_key: The unique key identifying the project
        repo_key: The repository key/slug

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "branching_model": {model configuration}}
            - On error: {"error": "error message"}

    Example:
        >>> get_branching_model("MYPROJ", "my-repo")
    """
    try:
        model = bitbucket.get_branching_model(project_key, repo_key)
        return json.dumps({"success": True, "branching_model": safe_serialize(model)})
    except Exception as e:
        logging.error(f"Error getting branching model: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_users(user_filter: str = "username", limit: int = 25, start: int = 0) -> str:
    """
    Get users from Bitbucket Server.

    Retrieves a list of users with optional filtering. Supports pagination for
    large result sets. Useful for user discovery and management operations.

    Args:
        user_filter: Filter string to search for users (default: "username").
                    Can match against username, display name, or email.
        limit: Maximum number of users to return per page (default: 25)
        start: Start index for pagination (default: 0)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "users": [list of user objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_users(user_filter="john", limit=10)
    """
    try:
        users = bitbucket.get_users(user_filter=user_filter, limit=limit, start=start)
        return json.dumps({"success": True, "users": safe_serialize(users)})
    except Exception as e:
        logging.error(f"Error getting users: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_branches(project: str, repository: str, filter_str: str = "", limit: int = 99999, details: bool = True) -> str:
    """
    Get branches from a repository.

    Retrieves all branches in the repository with optional filtering.
    Can include detailed information about each branch such as latest commit.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        filter_str: Optional filter string to match branch names (default: '')
        limit: Maximum number of branches to return (default: 99999)
        details: Include detailed branch information including latest commit (default: True)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "branches": [list of branch objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_branches("MYPROJ", "my-repo", filter_str="feature/", limit=50)
    """
    try:
        branches = bitbucket.get_branches(project, repository, filter=filter_str, limit=limit, details=details)
        return json.dumps({"success": True, "branches": safe_serialize(branches)})
    except Exception as e:
        logging.error(f"Error getting branches: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def create_branch(project_key: str, repository: str, name: str, start_point: str, message: str = "") -> str:
    """
    Create a new branch in a repository.

    Creates a new branch starting from a specified commit hash or existing branch.
    The new branch will point to the same commit as the start_point.

    Args:
        project_key: The unique key identifying the project
        repository: The repository slug/identifier
        name: Name for the new branch (e.g., "feature/new-feature")
        start_point: Commit hash or branch name to branch from (e.g., "main" or "abc123def")
        message: Optional commit message (default: "")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "branch": {created branch details}}
            - On error: {"error": "error message"}

    Example:
        >>> create_branch("MYPROJ", "my-repo", "feature/awesome", "main")
    """
    try:
        branch = bitbucket.create_branch(project_key, repository, name, start_point, message)
        return json.dumps({"success": True, "branch": safe_serialize(branch)})
    except Exception as e:
        logging.error(f"Error creating branch: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_branch_content(
    project: str,
    repository: str,
    branch: str,
    include_names: bool = False,
    path_prefix: str = None,
    page_size: int = 1000,
) -> str:
    """
    List files in a branch and return the count (optionally the file names).

    Retrieves all files in a specific branch, with optional filtering by path prefix.
    Can return just the count or include full file listings. Useful for analyzing
    repository contents and structure.

    Args:
        project: Bitbucket project key (e.g., "MYPROJ")
        repository: Repository slug (e.g., "my-repo")
        branch: Branch name (e.g., "main" or "feature/my-branch").
               Can also pass a full ref (e.g., "refs/heads/main") or commit hash.
               If not starting with "refs/", treated as "refs/heads/<branch>".
        include_names: If True, include the list of file paths in response (default: False)
        path_prefix: Optional path prefix to restrict results to subdirectory (e.g., "src/")
        page_size: Page size for Bitbucket paging API (default: 1000)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "ref": "refs/heads/...", "count": int, "files": [...]}
                          (files array only present when include_names=True)
            - On error: {"error": "error message"}

    Example:
        >>> get_branch_content("MYPROJ", "my-repo", "main", include_names=True)
    """
    try:
        if not project or not repository or not branch:
            return json.dumps({"error": "project, repository, and branch are required"})

        ref = branch if branch.startswith("refs/") else f"refs/heads/{branch}"
        api_path = f"/rest/api/1.0/projects/{project}/repos/{repository}/files"
        start = 0
        files = []

        while True:
            params = {"at": ref, "limit": page_size, "start": start}
            if path_prefix:
                params["path"] = path_prefix

            page = bitbucket.get(api_path, params=params)
            if not page:
                break

            if isinstance(page, dict):
                values = page.get("values", [])
                files.extend(values)
                if page.get("isLastPage", True):
                    break
                start = page.get("nextPageStart", None)
                if start is None:
                    break
            elif isinstance(page, list):
                files.extend(page)
                break
            else:
                return json.dumps({"error": f"Unexpected response type: {type(page).__name__}"})

        result = {
            "success": True,
            "project": project,
            "repository": repository,
            "ref": ref,
            "count": len(files),
        }
        if include_names:
            result["files"] = files

        return json.dumps(result)
    except Exception as e:
        logging.error(f"Error listing branch content: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def download_file_from_bitbucket(
    project: str,
    repository: str,
    path: str,
    at: str = None,
    output_filename: str = None,
    overwrite: bool = False,
    markup: bool = False,
) -> str:
    """
    Download a single file from Bitbucket Server to the current working directory.

    Args:
        project: Bitbucket project key (e.g., "MYPROJ")
        repository: Repository slug (e.g., "my-repo")
        path: Relative path to the file within repository (e.g., "README.md" or "src/app.py").
              Must not be empty.
        at: Optional commit hash, tag, or branch. If not provided, uses default branch HEAD.
        output_filename: Optional filename for local save. Defaults to basename of 'path'.
        overwrite: If False (default) and file exists, returns error instead of overwriting.
        markup: If True, Bitbucket renders supported markup (e.g., Markdown) before download (default: False)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "path": "...", "at": "...", "saved_to": "absolute/path",
                          "size_bytes": int, "sha256": "hex"}
            - On error: {"error": "error message", "hint": "..."}

    Example:
        >>> download_file_from_bitbucket("MYPROJ", "my-repo", "README.md", at="main")
    """
    try:
        if not path or not path.strip():
            return json.dumps({"error": "The parameter 'path' is required and cannot be empty."})

        markup_param = "true" if markup else None
        content = bitbucket.get_content_of_file(project, repository, path, at=at, markup=markup_param)

        if isinstance(content, str):
            content_bytes = content.encode("utf-8")
        elif isinstance(content, bytes):
            content_bytes = content
        else:
            return json.dumps({"error": f"Unexpected content type: {type(content).__name__}"})

        filename = output_filename or os.path.basename(path)
        if not filename:
            return json.dumps({"error": "Could not determine output filename; provide 'output_filename'."})

        dest_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(dest_path) and not overwrite:
            return json.dumps(
                {
                    "error": f"File already exists: {dest_path}",
                    "hint": "Set overwrite=True or provide a different output_filename.",
                }
            )

        with open(dest_path, "wb") as f:
            f.write(content_bytes)

        sha256 = hashlib.sha256(content_bytes).hexdigest()
        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "path": path,
                "at": at,
                "saved_to": os.path.abspath(dest_path),
                "size_bytes": len(content_bytes),
                "sha256": sha256,
            }
        )
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_create_or_update_file_instructions(project: str, repository: str, branch: str) -> str:
    """
    Get instructions for creating or updating files in a Bitbucket repository.

    Args:
        project: The unique key identifying the project (e.g., "MYPROJ")
        repository: The repository slug/identifier (e.g., "my-repo")
        branch: The branch name to work on (e.g. "feature/my-feature")

    Returns:
        str: JSON string containing instructions
    """
    try:
        instructions = f"""
        File Operations Instructions for {project}/{repository} on branch '{branch}'

        IMPORTANT NOTES:

        • Bitbucket API restricts direct file operations - must use Git clone/commit/push workflow
        • Clone repository if not already available locally
        • Checkout target branch '{branch}' (create if new branch)
        • Make your file changes (create/update/delete files as needed)
        • Stage changes with git add
        • **COMMIT MESSAGE RULES**: Project/repository may have pre-commit hooks with strict commit message format requirements
        - Check for conventional commits, Jira ticket references, or other patterns
        - Commit will fail if message doesn't follow required format
        - get previous commit message in the branch to understand the rules
        • Push changes to {branch}
        """

        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "branch": branch,
                "instructions": instructions.strip(),
            }
        )

    except Exception as e:
        logging.error(f"Error generating file operation instructions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_pull_requests(
    project: str, repository: str, state: str = "OPEN", order: str = "newest", limit: int = 100, start: int = 0
) -> str:
    """
    Get pull requests from a repository.

    Retrieves pull requests with filtering by state and ordering options.
    Supports pagination for large result sets.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        state: PR state filter - "OPEN", "MERGED", "DECLINED", or "ALL" (default: "OPEN")
        order: Sort order - "newest" or "oldest" (default: "newest")
        limit: Maximum number of PRs to return (default: 100)
        start: Start index for pagination (default: 0)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "pull_requests": [list of PR objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_pull_requests("MYPROJ", "my-repo", state="MERGED", limit=50)
    """
    try:
        prs = bitbucket.get_pull_requests(project, repository, state=state, order=order, limit=limit, start=start)
        return json.dumps({"success": True, "pull_requests": safe_serialize(prs)})
    except Exception as e:
        logging.error(f"Error getting pull requests: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_pull_request_details(project: str, repository: str, pull_request_id: int, detail_type: str = "info") -> str:
    """
    Get pull request details - basic info, activities, changes, commits, or all.

    Retrieves detailed information about a pull request. By default returns basic
    information including author, reviewers, approval status, title, description, etc.
    Can optionally include activities (comments, approvals, updates), file changes,
    and commit history.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        detail_type: Type of details to retrieve (default: "info"):
                    - "info": Basic PR information (author, reviewers, status, etc.)
                    - "activities": Include activities (comments, approvals, status changes)
                    - "changes": Include file changes/diffs
                    - "commits": Include commit list
                    - "all": Include everything (info + activities + changes + commits)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "detail_type": "...",
                          "info": {...}, "activities": [...], "changes": {...}, "commits": [...]}
                          (sections included based on detail_type)
            - On error: {"error": "error message"} or validation error for invalid detail_type

    Example:
        >>> # Get basic info only (default)
        >>> get_pull_request_details("MYPROJ", "my-repo", 42)

        >>> # Get info with activities
        >>> get_pull_request_details("MYPROJ", "my-repo", 42, detail_type="activities")

        >>> # Get everything
        >>> get_pull_request_details("MYPROJ", "my-repo", 42, detail_type="all")
    """
    try:
        # Validate detail_type
        valid_types = ["info", "activities", "changes", "commits", "all"]
        if detail_type not in valid_types:
            return json.dumps({"error": f"detail_type must be one of: {', '.join(valid_types)}"})

        result = {
            "success": True,
            "project": project,
            "repository": repository,
            "pull_request_id": pull_request_id,
            "detail_type": detail_type,
        }

        # Always get basic PR info for "info", "activities", "changes", "commits", or "all"
        if detail_type in ["info", "activities", "changes", "commits", "all"]:
            # Get basic PR information
            pr_endpoint = f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}"
            pr_info = bitbucket.get(pr_endpoint)

            if not pr_info:
                return json.dumps({"error": f"Pull request {pull_request_id} not found"})

            # Extract and format key information
            basic_info = {
                "id": pr_info.get("id"),
                "version": pr_info.get("version"),
                "title": pr_info.get("title"),
                "description": pr_info.get("description"),
                "state": pr_info.get("state"),  # OPEN, MERGED, DECLINED
                "open": pr_info.get("open"),
                "closed": pr_info.get("closed"),
                "createdDate": pr_info.get("createdDate"),
                "updatedDate": pr_info.get("updatedDate"),
                "fromRef": {
                    "id": pr_info.get("fromRef", {}).get("id"),
                    "displayId": pr_info.get("fromRef", {}).get("displayId"),
                    "repository": pr_info.get("fromRef", {}).get("repository", {}).get("name"),
                },
                "toRef": {
                    "id": pr_info.get("toRef", {}).get("id"),
                    "displayId": pr_info.get("toRef", {}).get("displayId"),
                    "repository": pr_info.get("toRef", {}).get("repository", {}).get("name"),
                },
                "locked": pr_info.get("locked"),
                "author": {
                    "user": {
                        "name": pr_info.get("author", {}).get("user", {}).get("name"),
                        "displayName": pr_info.get("author", {}).get("user", {}).get("displayName"),
                        "emailAddress": pr_info.get("author", {}).get("user", {}).get("emailAddress"),
                    },
                    "role": pr_info.get("author", {}).get("role"),
                    "approved": pr_info.get("author", {}).get("approved"),
                },
                "reviewers": [],
                "participants": [],
                "links": pr_info.get("links"),
            }

            # Process reviewers with approval status
            for reviewer in pr_info.get("reviewers", []):
                basic_info["reviewers"].append(
                    {
                        "user": {
                            "name": reviewer.get("user", {}).get("name"),
                            "displayName": reviewer.get("user", {}).get("displayName"),
                            "emailAddress": reviewer.get("user", {}).get("emailAddress"),
                        },
                        "role": reviewer.get("role"),  # REVIEWER
                        "approved": reviewer.get("approved"),  # True/False
                        "status": reviewer.get("status"),  # APPROVED, UNAPPROVED, NEEDS_WORK
                    }
                )

            # Process other participants
            for participant in pr_info.get("participants", []):
                basic_info["participants"].append(
                    {
                        "user": {
                            "name": participant.get("user", {}).get("name"),
                            "displayName": participant.get("user", {}).get("displayName"),
                            "emailAddress": participant.get("user", {}).get("emailAddress"),
                        },
                        "role": participant.get("role"),
                        "approved": participant.get("approved"),
                        "status": participant.get("status"),
                    }
                )

            # Add approval summary
            approved_reviewers = [r for r in basic_info["reviewers"] if r.get("approved")]
            unapproved_reviewers = [r for r in basic_info["reviewers"] if not r.get("approved")]

            basic_info["approval_summary"] = {
                "total_reviewers": len(basic_info["reviewers"]),
                "approved_count": len(approved_reviewers),
                "unapproved_count": len(unapproved_reviewers),
                "approved_by": [r["user"]["name"] for r in approved_reviewers],
                "pending_approval_from": [r["user"]["name"] for r in unapproved_reviewers],
            }

            result["info"] = safe_serialize(basic_info)

        # Include activities if requested
        if detail_type in ["activities", "all"]:
            activities = bitbucket.get_pull_requests_activities(project, repository, pull_request_id)
            result["activities"] = safe_serialize(activities)

        # Include changes if requested
        if detail_type in ["changes", "all"]:
            changes = bitbucket.get_pull_requests_changes(project, repository, pull_request_id)
            result["changes"] = safe_serialize(changes)

        # Include commits if requested
        if detail_type in ["commits", "all"]:
            commits = bitbucket.get_pull_requests_commits(project, repository, pull_request_id)
            result["commits"] = safe_serialize(commits)

        return json.dumps(result)

    except Exception as e:
        logging.error(f"Error getting pull request details: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def add_pull_request_comment(
    project: str, repository: str, pull_request_id: int, text: str, parent_id: int = None
) -> str:
    """
    Add comment to pull request or reply to an existing comment.

    Creates a new comment on a pull request. Can be a top-level comment or a reply
    to an existing comment thread by specifying parent_id.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        text: The comment text/content
        parent_id: Optional parent comment ID for threaded replies (default: None)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "result": {created comment details}}
            - On error: {"error": "error message"}

    Example:
        >>> add_pull_request_comment("MYPROJ", "my-repo", 42, "Looks good!")
    """
    try:
        result = bitbucket.add_pull_request_comment(project, repository, pull_request_id, text, parent_id=parent_id)
        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error adding pull request comment: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def add_pull_request_inline_comment(
    project: str,
    repository: str,
    pull_request_id: int,
    text: str,
    file_path: str,
    line_number: int,
    line_type: str = "ADDED",
    parent_id: int = None,
) -> str:
    """
    Add an inline comment on a specific line of a changed file in a pull request.

    Creates a comment anchored to a specific line in the diff view, allowing you to
    comment directly on code changes. This appears as an inline comment in the pull
    request's diff view.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        text: The comment text/content
        file_path: Path to the file in the diff (e.g., "src/main.py", "pc_info.bat")
        line_number: Line number in the diff to comment on
        line_type: Type of line - "ADDED", "REMOVED", or "CONTEXT" (default: "ADDED")
        parent_id: Optional parent comment ID for threaded replies (default: None)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "file_path": "...", "line_number": int,
                          "line_type": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> # Comment on an added line
        >>> add_pull_request_inline_comment("MYPROJ", "my-repo", 42,
        ...     "This variable name could be more descriptive",
        ...     "src/app.py", 25, "ADDED")

        >>> # Comment on a removed line
        >>> add_pull_request_inline_comment("MYPROJ", "my-repo", 42,
        ...     "Why was this removed?", "config.json", 10, "REMOVED")
    """
    try:
        # Construct the endpoint for adding comments
        endpoint = f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/comments"

        # Build the anchor object for inline comments
        anchor = {
            "line": line_number,
            "lineType": line_type.upper(),  # ADDED, REMOVED, or CONTEXT
            "fileType": "TO" if line_type.upper() == "ADDED" else "FROM",
            "path": file_path,
        }

        # Build the comment payload
        payload = {
            "text": text,
            "anchor": anchor,
        }

        # Add parent_id if this is a reply
        if parent_id is not None:
            payload["parent"] = {"id": parent_id}

        # Create the inline comment
        result = bitbucket.post(endpoint, data=payload)

        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "file_path": file_path,
                "line_number": line_number,
                "line_type": line_type,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error adding inline comment to pull request: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def set_pull_request_comment_state(
    project: str, repository: str, pull_request_id: int, comment_id: int, resolve: bool = True
) -> str:
    """
    Resolve or reopen a pull request comment thread.

    Marks a comment thread as resolved or reopens it. For comment threads (parent + replies),
    this resolves the entire thread. Resolved threads indicate that feedback has been addressed.
    The comment version is automatically fetched, so you only need to provide the comment ID.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        comment_id: The numeric ID of the comment to update (use parent comment ID for threads)
        resolve: If True, resolve the thread; if False, reopen it (default: True)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "comment_id": int, "resolved": bool,
                          "message": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> # Resolve a comment thread
        >>> set_pull_request_comment_state("MYPROJ", "my-repo", 42, 123, resolve=True)

        >>> # Reopen a comment thread
        >>> set_pull_request_comment_state("MYPROJ", "my-repo", 42, 123, resolve=False)
    """
    try:
        # Construct the endpoint for updating comment state
        endpoint = (
            f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/comments/{comment_id}"
        )

        # First get the current comment to get version and preserve the text
        current_comment = bitbucket.get(endpoint)

        if not current_comment:
            return json.dumps({"error": f"Comment {comment_id} not found"})

        # Get current version from the comment
        comment_version = current_comment.get("version")
        if comment_version is None:
            return json.dumps({"error": "Could not retrieve comment version"})

        # Determine the target state and severity
        if resolve:
            target_state = "RESOLVED"
            target_severity = "NORMAL"  # NORMAL severity when resolved
            thread_resolved = "true"
        else:
            target_state = "OPEN"
            target_severity = "BLOCKER"  # BLOCKER severity when reopening (makes it unresolved)
            thread_resolved = "false"

        # Update the comment state AND severity to properly resolve the thread
        payload = {
            "id": comment_id,
            "threadResolved": thread_resolved,
            "version": comment_version,
            "text": current_comment.get("text", ""),
            "state": target_state,
            "severity": target_severity,
        }

        result = bitbucket.put(endpoint, data=payload)

        message = "Comment thread resolved" if resolve else "Comment thread reopened"

        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "comment_id": comment_id,
                "resolved": resolve,
                "message": message,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error updating pull request comment state: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def edit_pull_request_comment(
    project: str,
    repository: str,
    pull_request_id: int,
    comment_id: int,
    comment_version: int,
    text: str,
) -> str:
    """
    Edit an existing pull request comment.

    Updates the text of an existing comment on a pull request. The comment version
    must match to prevent concurrent modifications. Only the comment author or
    administrators can edit comments.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        comment_id: The numeric ID of the comment to edit
        comment_version: The current version of the comment (for optimistic locking)
        text: The new text content for the comment

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "comment_id": int, "message": "...",
                          "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> edit_pull_request_comment("MYPROJ", "my-repo", 42, 123, 1, "Updated comment text")
    """
    try:
        # Construct the endpoint for updating comment
        endpoint = (
            f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/comments/{comment_id}"
        )

        # Update the comment text
        payload = {
            "version": comment_version,
            "text": text,
        }

        result = bitbucket.put(endpoint, data=payload)

        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "comment_id": comment_id,
                "message": "Comment updated",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error editing pull request comment: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def set_pull_request_approval(project: str, repository: str, pull_request_id: int, approve: bool = True) -> str:
    """
    Approve or unapprove a pull request (CONSOLIDATED).

    Adds or removes the current user's approval for a pull request. Approval indicates
    that the reviewer has reviewed the changes and approves them for merging. Multiple
    approvals may be required depending on repository settings and reviewer conditions.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        approve: If True, approve the PR; if False, remove approval (default: True)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "approved": bool, "message": "...",
                          "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> set_pull_request_approval("MYPROJ", "my-repo", 42, approve=True)
        >>> set_pull_request_approval("MYPROJ", "my-repo", 42, approve=False)
    """
    try:
        # Construct the endpoint for approving/unapproving PR
        endpoint = f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/approve"

        # Send POST to approve, DELETE to unapprove
        if approve:
            result = bitbucket.post(endpoint)
            message = "Pull request approved"
        else:
            result = bitbucket.delete(endpoint)
            message = "Pull request approval removed"

        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "approved": approve,
                "message": message,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error setting pull request approval: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def open_pull_request(
    source_project: str,
    source_repo: str,
    dest_project: str,
    dest_repo: str,
    source_branch: str,
    dest_branch: str,
    title: str,
    description: str,
    reviewers_json: str = None,
) -> str:
    """
    Create a new pull request between two branches.

    Opens a pull request to merge changes from a source branch into a destination branch.
    Can be within the same repository or across repositories. Optional reviewers can be
    assigned at creation time.

    Args:
        source_project: Source project key
        source_repo: Source repository slug
        dest_project: Destination project key (can be same as source)
        dest_repo: Destination repository slug (can be same as source)
        source_branch: Source branch name to merge from
        dest_branch: Destination branch name to merge into
        title: Pull request title
        description: Pull request description/body
        reviewers_json: Optional JSON array of reviewer usernames
                       (e.g., '["user1", "user2"]', default: None)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "pull_request": {created PR details}}
            - On error: {"error": "error message"} or {"error": "Invalid JSON format: ..."}

    Example:
        >>> open_pull_request("MYPROJ", "my-repo", "MYPROJ", "my-repo",
        ...                   "feature/new", "main", "Add new feature",
        ...                   "This PR adds...", '["john.doe"]')
    """
    try:
        reviewers = json.loads(reviewers_json) if reviewers_json else None
        pr = bitbucket.open_pull_request(
            source_project,
            source_repo,
            dest_project,
            dest_repo,
            source_branch,
            dest_branch,
            title,
            description,
            reviewers,
        )
        return json.dumps({"success": True, "pull_request": safe_serialize(pr)})
    except json.JSONDecodeError as e:
        return json.dumps({"error": f"Invalid JSON format: {e}"})
    except Exception as e:
        logging.error(f"Error creating pull request: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def is_pull_request_can_be_merged(project_key: str, repository: str, pr_id: int) -> str:
    """
    Check if a pull request can be merged.

    Evaluates merge conditions including conflicts, required approvals, build status,
    and other merge restrictions to determine if the PR is mergeable.

    Args:
        project_key: The unique key identifying the project
        repository: The repository slug/identifier
        pr_id: The numeric ID of the pull request

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "can_merge": bool/object, "pr_id": int}
            - On error: {"error": "error message"}

    Example:
        >>> is_pull_request_can_be_merged("MYPROJ", "my-repo", 42)
    """
    try:
        result = bitbucket.is_pull_request_can_be_merged(project_key, repository, pr_id)
        return json.dumps({"success": True, "can_merge": safe_serialize(result), "pr_id": pr_id})
    except Exception as e:
        logging.error(f"Error checking merge status: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def merge_pull_request(project_key: str, repository: str, pr_id: int, pr_version: int) -> str:
    """
    Merge a pull request.

    Merges an approved pull request into the destination branch. The PR must pass
    all merge conditions and the version must match to prevent concurrent modifications.

    Args:
        project_key: The unique key identifying the project
        repository: The repository slug/identifier
        pr_id: The numeric ID of the pull request
        pr_version: The current version of the pull request (for optimistic locking)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repository": "...",
                          "pr_id": int, "message": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> merge_pull_request("MYPROJ", "my-repo", 42, 5)
    """
    try:
        result = bitbucket.merge_pull_request(project_key, repository, pr_id, pr_version)
        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repository": repository,
                "pr_id": pr_id,
                "message": "Pull request merged",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error merging pull request: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def reopen_pull_request(project_key: str, repository: str, pr_id: int, pr_version: int) -> str:
    """
    Reopen a declined or merged pull request.

    Reopens a previously declined or merged pull request, allowing further review
    and modifications. The version must match the current PR version.

    Args:
        project_key: The unique key identifying the project
        repository: The repository slug/identifier
        pr_id: The numeric ID of the pull request
        pr_version: The current version of the pull request (for optimistic locking)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repository": "...",
                          "pr_id": int, "message": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> reopen_pull_request("MYPROJ", "my-repo", 42, 5)
    """
    try:
        result = bitbucket.reopen_pull_request(project_key, repository, pr_id, pr_version)
        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repository": repository,
                "pr_id": pr_id,
                "message": "Pull request reopened",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error reopening pull request: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def assign_pull_request_reviewer(project_key: str, repository: str, pr_id: int, username: str) -> str:
    """
    Assign a user as a reviewer for a pull request.

    Adds a user to the reviewers list for a pull request. The user will be notified
    and can approve or request changes to the PR.

    Args:
        project_key: The unique key identifying the project
        repository: The repository slug/identifier
        pr_id: The numeric ID of the pull request
        username: Username of the user to assign as reviewer

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repository": "...",
                          "pr_id": int, "username": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> assign_pull_request_reviewer("MYPROJ", "my-repo", 42, "jane.smith")
    """
    try:
        result = bitbucket.assign_pull_request_participant_role(project_key, repository, pr_id, "REVIEWER", username)
        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repository": repository,
                "pr_id": pr_id,
                "username": username,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error assigning reviewer: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_tags(project: str, repository: str, tag_name: str = None, filter_str: str = "", limit: int = 9999) -> str:
    """
    Get tags from a repository, optionally retrieve a specific tag (CONSOLIDATED).

    Retrieves all tags or a specific tag from a repository. Tags mark specific
    points in repository history, typically used for releases or milestones.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        tag_name: Optional specific tag name to retrieve (default: None)
        filter_str: Optional filter string to match tag names (ignored if tag_name provided)
        limit: Maximum number of tags to return (ignored if tag_name provided, default: 9999)

    Returns:
        str: JSON string containing:
            - On success (single tag): {"success": True, "tag": {tag object}}
            - On success (multiple tags): {"success": True, "tags": [list of tag objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_tags("MYPROJ", "my-repo", tag_name="v1.0.0")

        >>> get_tags("MYPROJ", "my-repo", filter_str="v1.", limit=10)
    """
    try:
        if tag_name:
            # Get specific tag
            tag = bitbucket.get_project_tags(project, repository, tag_name)
            return json.dumps({"success": True, "tag": safe_serialize(tag)})
        else:
            # Get all tags with filter
            tags = bitbucket.get_tags(project, repository, filter=filter_str, limit=limit)
            return json.dumps({"success": True, "tags": safe_serialize(tags)})
    except Exception as e:
        logging.error(f"Error getting tags: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def set_tag(project: str, repository: str, tag_name: str, commit_revision: str, description: str = None) -> str:
    """
    Create a tag on a specific commit.

    Creates a lightweight or annotated tag pointing to a specific commit in the
    repository history. Tags are typically used to mark release points.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        tag_name: Name for the tag (e.g., "v1.0.0", "release-2023-01")
        commit_revision: Commit hash to tag (full or abbreviated)
        description: Optional tag annotation/description (default: None)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "tag_name": "...", "commit_revision": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> set_tag("MYPROJ", "my-repo", "v1.0.0", "abc123def456", "Release version 1.0.0")
    """
    try:
        result = bitbucket.set_tag(project, repository, tag_name, commit_revision, description=description)
        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "tag_name": tag_name,
                "commit_revision": commit_revision,
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error setting tag: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_commits(project: str, repository: str, hash_oldest: str, hash_newest: str, limit: int = 99999) -> str:
    """
    Get commit list between two commit hashes.

    Retrieves all commits in the range from hash_oldest to hash_newest (inclusive).
    Useful for viewing history between releases or understanding changes in a range.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        hash_oldest: Oldest commit hash in the range (inclusive)
        hash_newest: Newest commit hash in the range (inclusive)
        limit: Maximum number of commits to return (default: 99999)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "commits": [list of commit objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_commits("MYPROJ", "my-repo", "abc123", "def456", limit=100)
    """
    try:
        commits = bitbucket.get_commits(project, repository, hash_oldest, hash_newest, limit=limit)
        return json.dumps({"success": True, "commits": safe_serialize(commits)})
    except Exception as e:
        logging.error(f"Error getting commits: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_commit_info(
    project: str,
    repository: str,
    commit_id: str,
    include_changes: bool = True,
    fetch_all_changes: bool = False,
    limit: int = 100,
    start: int = 0,
    max_changes: int = 5000,
    summary_only: bool = False,
) -> str:
    """
    Get detailed information for a specific commit with optional paginated changes.

    Retrieves comprehensive commit metadata including author, timestamp, message,
    and optionally the list of changed files. Supports pagination for commits with
    many file changes.

    Args:
        project: Bitbucket project key (e.g., "MYPROJ")
        repository: Repository slug (e.g., "my-repo")
        commit_id: Full or abbreviated commit hash to retrieve
        include_changes: If True, include changed files for the commit (default: True)
        fetch_all_changes: If True, automatically page through all changes up to max_changes (default: False)
        limit: Page size for changes pagination (default: 100)
        start: Start index for changes pagination (default: 0)
        max_changes: Upper bound on number of changes when fetch_all_changes=True (default: 5000)
        summary_only: If True, include only summary of changes (counts) without full file list (default: False)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "commit_id": "...", "commit": {...}, "change_summary": {...},
                          "changes": [...], "changes_paging": {...}, "truncated": bool}
            - On error: {"error": "error message"}

    Example:
        >>> get_commit_info("MYPROJ", "my-repo", "abc123def", include_changes=True, summary_only=True)
    """
    try:
        if not project or not repository or not commit_id or not commit_id.strip():
            return json.dumps({"error": "project, repository, and commit_id are required"})

        # Commit metadata
        commit_endpoint = f"/rest/api/1.0/projects/{project}/repos/{repository}/commits/{commit_id}"
        commit = bitbucket.get(commit_endpoint)
        if not commit:
            return json.dumps({"error": f"No commit found for id: {commit_id}"})
        if isinstance(commit, dict) and commit.get("errors"):
            return json.dumps({"error": safe_serialize(commit.get("errors"))})

        result = {
            "success": True,
            "project": project,
            "repository": repository,
            "commit_id": commit_id,
            "commit": safe_serialize(commit),
        }

        # Optionally fetch changes
        if include_changes:
            changes_endpoint = f"/rest/api/1.0/projects/{project}/repos/{repository}/commits/{commit_id}/changes"

            def summarize(ch_list):
                """Summarize changes by type."""
                counts = {}
                for ch in ch_list or []:
                    t = ch.get("type")
                    counts[t] = counts.get(t, 0) + 1
                return {"total": len(ch_list or []), "by_type": counts}

            truncated = False
            changes = []
            paging_info = {"fetched": 0, "isLastPage": True, "nextStart": None, "limit": limit, "start": start}

            if fetch_all_changes:
                s = start
                while True:
                    page = bitbucket.get(changes_endpoint, params={"limit": limit, "start": s})
                    if not page or not isinstance(page, dict):
                        break
                    values = page.get("values", []) or []
                    changes.extend(values)
                    paging_info["fetched"] = len(changes)
                    is_last = page.get("isLastPage", True)
                    next_start = page.get("nextPageStart", None)
                    # Stop if reached max_changes or last page
                    if len(changes) >= max_changes:
                        truncated = True
                        paging_info["isLastPage"] = False
                        paging_info["nextStart"] = next_start
                        break
                    if is_last or next_start is None:
                        paging_info["isLastPage"] = True
                        paging_info["nextStart"] = None
                        break
                    s = next_start

                result["change_summary"] = summarize(changes)
                if not summary_only:
                    result["changes"] = safe_serialize(changes)
                result["truncated"] = truncated
                result["changes_paging"] = paging_info

            else:
                page = bitbucket.get(changes_endpoint, params={"limit": limit, "start": start})
                if not page or not isinstance(page, dict):
                    # Still return commit info; no changes page
                    result["change_summary"] = {"total": 0, "by_type": {}}
                    result["changes_paging"] = paging_info
                else:
                    values = page.get("values", []) or []
                    result["change_summary"] = summarize(values)
                    if not summary_only:
                        result["changes"] = safe_serialize(values)
                    result["changes_paging"] = {
                        "fetched": len(values),
                        "isLastPage": page.get("isLastPage", True),
                        "nextStart": page.get("nextPageStart", None),
                        "limit": page.get("limit", limit),
                        "start": page.get("start", start),
                    }

        return json.dumps(result)
    except Exception as e:
        logging.error(f"Error getting commit info: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_diff(project: str, repository: str, path: str, hash_oldest: str, hash_newest: str) -> str:
    """
    Get diff for a file between two commits.

    Retrieves the line-by-line differences for a specific file between two commit hashes.
    Useful for code review and understanding changes over time.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        path: Relative path to the file within repository (e.g., "src/main.py")
        hash_oldest: Older commit hash in the comparison
        hash_newest: Newer commit hash in the comparison

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "diff": {diff object with changes}}
            - On error: {"error": "error message"}

    Example:
        >>> get_diff("MYPROJ", "my-repo", "src/app.py", "abc123", "def456")
    """
    try:
        diff = bitbucket.get_diff(project, repository, path, hash_oldest, hash_newest)
        return json.dumps({"success": True, "diff": safe_serialize(diff)})
    except Exception as e:
        logging.error(f"Error getting diff: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_file_content(
    project: str,
    repository: str,
    path: str,
    at: str = None,
    markup: bool = False,
    decode: bool = True,
    encoding: str = "utf-8",
) -> str:
    """
    Retrieve raw content of a file from Bitbucket Server.

    Fetches file content from a specific commit, branch, or tag. Can return either
    decoded text or base64-encoded binary content. Supports markup rendering for
    documentation files.

    Args:
        project: Bitbucket project key (e.g., "MYPROJ")
        repository: Repository slug (e.g., "my-repo")
        path: Relative file path within the repo (required; cannot be empty), e.g., "README.md"
        at: Optional commit hash, tag, or branch name. Defaults to default branch HEAD if not provided
        markup: If True, Bitbucket will render supported markup (e.g., Markdown) and return rendered content (default: False)
        decode: If True (default), attempts to decode raw bytes using the given encoding.
               If decoding fails or the file appears binary, returns base64 instead
        encoding: Text encoding used when decode=True (default: "utf-8")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...", "path": "...",
                          "at": "...", "markup": bool, "encoding": "...", "decoded": bool,
                          "text": "..." OR "content_base64": "..."}
            - On error: {"error": "error message", "hint": "..."}

    Example:
        >>> get_file_content("MYPROJ", "my-repo", "README.md", at="main", decode=True)
    """
    try:
        if not path or not path.strip():
            return json.dumps(
                {
                    "error": "The parameter 'path' is required and cannot be empty.",
                    "hint": "Provide a relative file path, e.g., 'README.md' or 'src/app.py'.",
                }
            )

        # Bitbucket expects markup as 'true' or omitted; map boolean accordingly
        markup_param = "true" if markup else None

        content = bitbucket.get_content_of_file(project, repository, path, at=at, markup=markup_param)

        # Normalize output: text if decodable, otherwise base64
        decoded = False
        result = {
            "success": True,
            "project": project,
            "repository": repository,
            "path": path,
            "at": at,
            "markup": markup,
            "encoding": encoding,
            "decoded": decoded,
        }

        if isinstance(content, bytes):
            if decode:
                try:
                    text = content.decode(encoding)
                    result["text"] = text
                    result["decoded"] = True
                except UnicodeDecodeError:
                    result["content_base64"] = base64.b64encode(content).decode("ascii")
            else:
                result["content_base64"] = base64.b64encode(content).decode("ascii")
        elif isinstance(content, str):
            # Some server responses may already be str (e.g., rendered markup)
            result["text"] = content
            result["decoded"] = True
        else:
            # Fallback: attempt to convert to bytes, then base64
            try:
                b = bytes(content)
                result["content_base64"] = base64.b64encode(b).decode("ascii")
            except Exception:
                result["error"] = f"Unexpected content type: {type(content).__name__}"
                return json.dumps(result)

        return json.dumps(result)
    except Exception as e:
        logging.error(f"Error getting file content: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def set_branches_permissions(
    project_key: str,
    multiple_permissions: bool = False,
    matcher_type: str = None,
    matcher_value: str = None,
    permission_type: str = None,
    repository_slug: str = None,
    except_users: str = None,
    except_groups: str = None,
    except_access_keys: str = None,
) -> str:
    """
    Set branch permissions for a project or repository.

    Configures branch-level access controls to protect important branches from
    unwanted changes. Can restrict who can push, delete, or rewrite history on
    specific branches or branch patterns.

    Args:
        project_key: The unique key identifying the project
        multiple_permissions: Whether to set multiple permissions in one call (default: False)
        matcher_type: Branch matcher type - "BRANCH" (exact), "PATTERN" (glob),
                     "MODEL_BRANCH" (from branching model)
        matcher_value: Branch matcher value (branch name, pattern, or model category)
        permission_type: Permission type - "read-only", "no-deletes", "pull-request-only", etc.
        repository_slug: Optional repository slug (for repo-level permissions, otherwise project-level)
        except_users: Optional comma-separated list of usernames exempt from restriction
        except_groups: Optional comma-separated list of groups exempt from restriction
        except_access_keys: Optional comma-separated list of access keys exempt from restriction

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> set_branches_permissions("MYPROJ", matcher_type="BRANCH", matcher_value="main",
        ...                          permission_type="read-only", except_users="admin,release-bot")
    """
    try:
        result = bitbucket.set_branches_permissions(
            project_key,
            multiple_permissions=multiple_permissions,
            matcher_type=matcher_type,
            matcher_value=matcher_value,
            permission_type=permission_type,
            repository_slug=repository_slug,
            except_users=except_users,
            except_groups=except_groups,
            except_access_keys=except_access_keys,
        )
        return json.dumps({"success": True, "project_key": project_key, "result": safe_serialize(result)})
    except Exception as e:
        logging.error(f"Error setting branch permissions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_branch_permission(project_key: str, permission_id: int, repository_slug: str = None) -> str:
    """
    Get a branch permission by ID.

    Retrieves detailed information about a specific branch permission restriction
    including matcher configuration and exceptions.

    Args:
        project_key: The unique key identifying the project
        permission_id: The numeric ID of the permission to retrieve
        repository_slug: Optional repository slug (for repo-level permissions)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "permission": {permission details}}
            - On error: {"error": "error message"}

    Example:
        >>> get_branch_permission("MYPROJ", 123)
    """
    try:
        permission = bitbucket.get_branch_permission(project_key, permission_id, repository_slug=repository_slug)
        return json.dumps({"success": True, "permission": safe_serialize(permission)})
    except Exception as e:
        logging.error(f"Error getting branch permission: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_repo_webhooks(project_key: str, repo_slug: str) -> str:
    """
    Get all webhooks for a repository.

    Retrieves all configured webhooks that trigger on repository events.
    Webhooks enable integration with external services by sending HTTP callbacks
    when events occur.

    Args:
        project_key: The unique key identifying the project
        repo_slug: The repository slug/identifier

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repo_slug": "...",
                          "webhooks": [list of webhook objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_repo_webhooks("MYPROJ", "my-repo")
    """
    try:
        webhooks = bitbucket.get_repo_webhooks(project_key, repo_slug)
        return json.dumps(
            {"success": True, "project_key": project_key, "repo_slug": repo_slug, "webhooks": safe_serialize(webhooks)}
        )
    except Exception as e:
        logging.error(f"Error getting repo webhooks: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_project_conditions(project_key: str, id_condition: int = None) -> str:
    """
    Get project reviewer conditions - all or specific condition (CONSOLIDATED).

    Retrieves reviewer conditions configured at the project level. Reviewer conditions
    define requirements for pull request approvals based on file paths, branch patterns,
    or other criteria.

    Args:
        project_key: The unique key identifying the project
        id_condition: Optional condition ID to get specific condition (default: None for all)

    Returns:
        str: JSON string containing:
            - On success (single): {"success": True, "condition": {condition details}}
            - On success (multiple): {"success": True, "project_key": "...",
                                     "conditions": [list of condition objects]}
            - On error: {"error": "error message"}

    Example:
        >>> get_project_conditions("MYPROJ")
        >>> get_project_conditions("MYPROJ", id_condition=42)
    """
    try:
        if id_condition is not None:
            condition = bitbucket.get_project_condition(project_key, id_condition)
            return json.dumps({"success": True, "condition": safe_serialize(condition)})
        else:
            conditions = bitbucket.get_project_conditions(project_key)
            return json.dumps({"success": True, "project_key": project_key, "conditions": safe_serialize(conditions)})
    except Exception as e:
        logging.error(f"Error getting project conditions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_repo_conditions(project_key: str, repo_key: str, id_condition: int = None, filter_type: str = "all") -> str:
    """
    Get repository reviewer conditions - all, project-type, repo-type, or specific (CONSOLIDATED).

    Retrieves reviewer conditions for a repository. Can filter to show only project-level
    conditions, repository-specific conditions, or all conditions affecting the repository.

    Args:
        project_key: The unique key identifying the project
        repo_key: The repository key/slug
        id_condition: Optional condition ID to get specific condition (default: None)
        filter_type: Filter by scope - "all", "project" (inherited), "repository" (repo-specific)
                    (default: "all")

    Returns:
        str: JSON string containing:
            - On success (single): {"success": True, "condition": {condition details}}
            - On success (multiple): {"success": True, "project_key": "...", "repo_key": "...",
                                     "filter_type": "...", "conditions": [list of conditions]}
            - On error: {"error": "error message"}

    Example:
        >>> get_repo_conditions("MYPROJ", "my-repo", filter_type="repository")
    """
    try:
        if id_condition is not None:
            condition = bitbucket.get_repo_condition(project_key, repo_key, id_condition)
            return json.dumps({"success": True, "condition": safe_serialize(condition)})

        if filter_type == "project":
            conditions = bitbucket.get_repo_project_conditions(project_key, repo_key)
        elif filter_type == "repository":
            conditions = bitbucket.get_repo_repo_conditions(project_key, repo_key)
        else:
            conditions = bitbucket.get_repo_conditions(project_key, repo_key)

        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repo_key": repo_key,
                "filter_type": filter_type,
                "conditions": safe_serialize(conditions),
            }
        )
    except Exception as e:
        logging.error(f"Error getting repo conditions: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def decline_pull_request(project_key: str, repository: str, pr_id: int, pr_version: int) -> str:
    """
    Decline a pull request.

    Marks a pull request as declined, preventing it from being merged. The PR can
    be reopened later if needed. The version must match to prevent concurrent modifications.

    Args:
        project_key: The unique key identifying the project
        repository: The repository slug/identifier
        pr_id: The numeric ID of the pull request to decline
        pr_version: The current version of the pull request (for optimistic locking)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project_key": "...", "repository": "...",
                          "pr_id": int, "message": "...", "result": {...}}
            - On error: {"error": "error message"}

    Example:
        >>> decline_pull_request("MYPROJ", "my-repo", 42, 5)
    """
    try:
        result = bitbucket.decline_pull_request(project_key, repository, pr_id, pr_version)
        return json.dumps(
            {
                "success": True,
                "project_key": project_key,
                "repository": repository,
                "pr_id": pr_id,
                "message": "Pull request declined",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error declining pull request: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def delete_branch(project: str, repository: str, name: str, end_point: str = None) -> str:
    """
    Delete a branch from a repository.

    Permanently removes a branch from the repository. This operation requires
    the ALLOW_DELETION environment variable to be set to "true". Cannot delete
    the default branch or branches with open pull requests.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        name: Branch name to delete (e.g., "feature/old-feature")
        end_point: Optional specific commit hash endpoint for the branch

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "branch_name": "...", "message": "...", "result": {...}}
            - On error: {"error": "Deletion operations disabled..."} if ALLOW_DELETION is false
            - On error: {"error": "error message"} for other failures

    Example:
        >>> delete_branch("MYPROJ", "my-repo", "feature/obsolete")
    """
    if not ALLOW_DELETION:
        return json.dumps({"error": "Deletion operations disabled (set ALLOW_DELETION=true to enable)."})
    try:
        result = bitbucket.delete_branch(project, repository, name, end_point=end_point)
        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "branch_name": name,
                "message": "Branch deleted",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error deleting branch: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def delete_pull_request(project: str, repository: str, pull_request_id: int, pull_request_version: int) -> str:
    """
    Delete a pull request.

    Permanently removes a pull request from the repository. This operation requires
    the ALLOW_DELETION environment variable to be set to "true". The version must
    match to prevent concurrent modification issues.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request to delete
        pull_request_version: The current version of the pull request (for optimistic locking)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "message": "...", "result": {...}}
            - On error: {"error": "Deletion operations disabled..."} if ALLOW_DELETION is false
            - On error: {"error": "error message"} for other failures

    Example:
        >>> delete_pull_request("MYPROJ", "my-repo", 99, 3)
    """
    if not ALLOW_DELETION:
        return json.dumps({"error": "Deletion operations disabled (set ALLOW_DELETION=true to enable)."})
    try:
        result = bitbucket.delete_pull_request(project, repository, pull_request_id, pull_request_version)
        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "message": "Pull request deleted",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error deleting pull request: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def delete_pull_request_comment(
    project: str, repository: str, pull_request_id: int, comment_id: int, comment_version: int
) -> str:
    """
    Delete a pull request comment.

    Permanently removes a comment from a pull request. Only the comment
    author or administrators can delete comments. The version must match to prevent
    concurrent modifications.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        pull_request_id: The numeric ID of the pull request
        comment_id: The numeric ID of the comment to delete
        comment_version: The current version of the comment (for optimistic locking)

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "pull_request_id": int, "comment_id": int, "message": "...",
                          "result": {...}}
            - On error: {"error": "Deletion operations disabled..."} if ALLOW_DELETION is false
            - On error: {"error": "error message"} for other failures

    Example:
        >>> delete_pull_request_comment("MYPROJ", "my-repo", 42, 123, 2)
    """
    if not ALLOW_DELETION:
        return json.dumps({"error": "Deletion operations disabled (set ALLOW_DELETION=true to enable)."})
    try:
        # Construct the endpoint for deleting comment
        endpoint = (
            f"/rest/api/1.0/projects/{project}/repos/{repository}/pull-requests/{pull_request_id}/comments/{comment_id}"
        )

        # Delete the comment with version for optimistic locking
        result = bitbucket.delete(endpoint, params={"version": comment_version})

        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "pull_request_id": pull_request_id,
                "comment_id": comment_id,
                "message": "Comment deleted",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error deleting pull request comment: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def delete_tag(project: str, repository: str, tag_name: str) -> str:
    """
    Delete a tag from a repository.

    Permanently removes a tag from the repository. This operation requires
    the ALLOW_DELETION environment variable to be set to "true". Use with
    caution as tags are typically used to mark important points in history.

    Args:
        project: The unique key identifying the project
        repository: The repository slug/identifier
        tag_name: Name of the tag to delete (e.g., "v1.0.0-beta")

    Returns:
        str: JSON string containing:
            - On success: {"success": True, "project": "...", "repository": "...",
                          "tag_name": "...", "message": "...", "result": {...}}
            - On error: {"error": "Deletion operations disabled..."} if ALLOW_DELETION is false
            - On error: {"error": "error message"} for other failures

    Example:
        >>> delete_tag("MYPROJ", "my-repo", "v0.1.0-alpha")
    """
    if not ALLOW_DELETION:
        return json.dumps({"error": "Deletion operations disabled (set ALLOW_DELETION=true to enable)."})
    try:
        result = bitbucket.delete_tag(project, repository, tag_name)
        return json.dumps(
            {
                "success": True,
                "project": project,
                "repository": repository,
                "tag_name": tag_name,
                "message": "Tag deleted",
                "result": safe_serialize(result),
            }
        )
    except Exception as e:
        logging.error(f"Error deleting tag: {e}")
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    initialize_bitbucket()
    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
