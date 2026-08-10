"""
Gerrit MCP Server
Provides tools to interact with Gerrit Code Review via its REST API.
Enables: listing/getting changes, posting reviews, pushing commits to Gerrit.

Environment variables required:
  GERRIT_URL           - Base URL of Gerrit instance (e.g. https://gerrit.example.com)
  GERRIT_USERNAME      - Gerrit HTTP username
  GERRIT_HTTP_PASSWORD - Gerrit HTTP password (generated in Account Settings)
"""

import os
import json
import base64
import logging
import subprocess
import urllib.parse
from typing import Optional
import ssl
import httpx
from fastmcp import FastMCP

GERRIT_URL = os.getenv("GERRIT_URL", "").rstrip("/")
GERRIT_USERNAME = os.getenv("GERRIT_USERNAME", "")
GERRIT_HTTP_PASSWORD = os.getenv("GERRIT_HTTP_PASSWORD", "")
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.load_default_certs()
mcp = FastMCP("gerrit")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _auth() -> tuple[str, str]:
    return (GERRIT_USERNAME, GERRIT_HTTP_PASSWORD)


def _api(path: str) -> str:
    """Return the full authenticated REST API URL."""
    return f"{GERRIT_URL}/a{path}"


def _parse(text: str) -> dict | list:
    """Strip Gerrit's anti-XSSI prefix )]}'\\n and parse JSON."""
    if text.startswith(")]}'\n"):
        text = text[5:]
    return json.loads(text)


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_gerrit_changes(
    query: str,
    n: int = 25,
    options: Optional[list[str]] = None,
) -> dict:
    """List Gerrit changes matching a query string.

    Args:
        query: Gerrit query (e.g. 'project:myrepo status:open owner:me')
        n: Max results to return (default 25)
        options: Extra detail fields (e.g. ['DETAILED_LABELS', 'CURRENT_REVISION'])

    Returns:
        dict with 'changes' list or 'error'
    """
    params: dict = {"q": query, "n": n}
    if options:
        params["o"] = options
    try:
        resp = httpx.get(_api("/changes/"), params=params, auth=_auth(), timeout=30,verify=SSL_CONTEXT,)
        resp.raise_for_status()
        return {"changes": _parse(resp.text)}
    except Exception as exc:
        logging.error("list_gerrit_changes: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_gerrit_change(
    change_id: str,
    options: Optional[list[str]] = None,
) -> dict:
    """Get full details of a Gerrit change.

    Args:
        change_id: Numeric ID, Change-Id, or project~branch~Change-Id format
        options: Detail options (e.g. ['DETAILED_LABELS', 'CURRENT_FILES', 'MESSAGES'])

    Returns:
        dict with change details or 'error'
    """
    params: dict = {}
    if options:
        params["o"] = options
    try:
        resp = httpx.get(
            _api(f"/changes/{change_id}/detail"),
            params=params,
            auth=_auth(),
            timeout=30,
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("get_gerrit_change: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def create_gerrit_change(
    project: str,
    branch: str,
    subject: str,
    topic: Optional[str] = None,
    base_commit: Optional[str] = None,
) -> dict:
    """Create a new empty Gerrit change (placeholder / WIP).

    Args:
        project: Gerrit project name (e.g. 'platform/system/core')
        branch: Target branch (e.g. 'main')
        subject: Commit message subject line
        topic: Optional topic label for grouping related changes
        base_commit: Optional parent commit SHA

    Returns:
        dict with created change info or 'error'
    """
    payload: dict = {"project": project, "branch": branch, "subject": subject}
    if topic:
        payload["topic"] = topic
    if base_commit:
        payload["base_commit"] = base_commit
    try:
        resp = httpx.post(
            _api("/changes/"),
            json=payload,
            auth=_auth(),
            timeout=30,
            headers={"Content-Type": "application/json"},
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("create_gerrit_change: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def set_gerrit_review(
    change_id: str,
    revision_id: str,
    message: str,
    code_review_vote: Optional[int] = None,
    verified_vote: Optional[int] = None,
) -> dict:
    """Post a review message and/or score labels on a Gerrit change.

    Args:
        change_id: Change identifier
        revision_id: Revision identifier, use 'current' for latest
        message: Human-readable review comment
        code_review_vote: Code-Review label vote (-2, -1, 0, +1, +2)
        verified_vote: Verified label vote (-1, 0, +1)

    Returns:
        dict with review result or 'error'
    """
    payload: dict = {"message": message}
    labels: dict = {}
    if code_review_vote is not None:
        labels["Code-Review"] = code_review_vote
    if verified_vote is not None:
        labels["Verified"] = verified_vote
    if labels:
        payload["labels"] = labels
    try:
        resp = httpx.post(
            _api(f"/changes/{change_id}/revisions/{revision_id}/review"),
            json=payload,
            auth=_auth(),
            timeout=30,
            headers={"Content-Type": "application/json"},
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("set_gerrit_review: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def abandon_gerrit_change(
    change_id: str,
    message: Optional[str] = None,
) -> dict:
    """Abandon an open Gerrit change.

    Args:
        change_id: Change identifier
        message: Optional reason for abandoning

    Returns:
        dict with updated change or 'error'
    """
    payload: dict = {}
    if message:
        payload["message"] = message
    try:
        resp = httpx.post(
            _api(f"/changes/{change_id}/abandon"),
            json=payload,
            auth=_auth(),
            timeout=30,
            headers={"Content-Type": "application/json"},
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("abandon_gerrit_change: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_gerrit_change_files(
    change_id: str,
    revision_id: str = "current",
) -> dict:
    """List all files changed in a Gerrit change revision.

    Args:
        change_id: Change identifier
        revision_id: Revision to inspect (default: 'current')

    Returns:
        dict mapping file paths to their change info, or 'error'
    """
    try:
        resp = httpx.get(
            _api(f"/changes/{change_id}/revisions/{revision_id}/files"),
            auth=_auth(),
            timeout=30,
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("get_gerrit_change_files: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_gerrit_file_content(
    change_id: str,
    revision_id: str,
    file_path: str,
) -> dict:
    """Get the decoded content of a file in a Gerrit change revision.

    Args:
        change_id: Change identifier
        revision_id: Revision identifier ('current' or SHA)
        file_path: Repository-relative path to the file

    Returns:
        dict with 'content' (decoded text) or 'error'
    """
    encoded_path = urllib.parse.quote(file_path, safe="")
    try:
        resp = httpx.get(
            _api(f"/changes/{change_id}/revisions/{revision_id}/files/{encoded_path}/content"),
            auth=_auth(),
            timeout=30,
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        decoded = base64.b64decode(resp.content).decode("utf-8", errors="replace")
        return {"content": decoded}
    except Exception as exc:
        logging.error("get_gerrit_file_content: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def push_to_gerrit(
    repo_path: str,
    branch: str = "main",
    remote: str = "origin",
    topic: Optional[str] = None,
    reviewers: Optional[list[str]] = None,
    dry_run: bool = False,
) -> dict:
    """Push local Git commits to Gerrit for code review.

    Executes: git push <remote> HEAD:refs/for/<branch>[%topic=...,r=...]

    Args:
        repo_path: Absolute path to the local git repository
        branch: Target branch in Gerrit (default: 'main')
        remote: Git remote name (default: 'origin')
        topic: Optional Gerrit topic to group related changes
        reviewers: List of reviewer username/email addresses
        dry_run: If True, add --dry-run flag (no actual push)

    Returns:
        dict with 'stdout', 'stderr', 'returncode', 'success' or 'error'
    """
    push_opts: list[str] = []
    if topic:
        push_opts.append(f"topic={topic}")
    if reviewers:
        for reviewer in reviewers:
            push_opts.append(f"r={reviewer}")

    refspec = f"HEAD:refs/for/{branch}"
    if push_opts:
        refspec += "%" + ",".join(push_opts)

    cmd = ["git", "push", remote, refspec]
    if dry_run:
        cmd.append("--dry-run")

    try:
        result = subprocess.run(
            cmd,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0,
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        return {"error": "git push timed out after 60 seconds"}
    except Exception as exc:
        logging.error("push_to_gerrit: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def list_gerrit_projects(
    prefix: Optional[str] = None,
    limit: int = 50,
) -> dict:
    """List Gerrit projects, optionally filtered by name prefix.

    Args:
        prefix: Optional project name prefix to filter results
        limit: Maximum number of projects to return

    Returns:
        dict mapping project names to project info, or 'error'
    """
    params: dict = {"n": limit}
    if prefix:
        params["p"] = prefix
    try:
        resp = httpx.get(_api("/projects/"), params=params, auth=_auth(), timeout=30,verify=SSL_CONTEXT,)
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("list_gerrit_projects: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_gerrit_project(project_name: str) -> dict:
    """Get details for a specific Gerrit project.

    Args:
        project_name: Full project name (slashes are URL-encoded automatically)

    Returns:
        dict with project info or 'error'
    """
    encoded = urllib.parse.quote(project_name, safe="")
    try:
        resp = httpx.get(_api(f"/projects/{encoded}/"), auth=_auth(), timeout=30,verify=SSL_CONTEXT,)
        resp.raise_for_status()
        return _parse(resp.text)  # type: ignore[return-value]
    except Exception as exc:
        logging.error("get_gerrit_project: %s", exc)
        return {"error": str(exc)}


@mcp.tool()
def get_gerrit_change_messages(change_id: str) -> dict:
    """Get all review messages / discussion thread for a Gerrit change.

    Args:
        change_id: Change identifier

    Returns:
        dict with 'messages' list or 'error'
    """
    try:
        resp = httpx.get(
            _api(f"/changes/{change_id}/messages"),
            auth=_auth(),
            timeout=30,
            verify=SSL_CONTEXT,
        )
        resp.raise_for_status()
        return {"messages": _parse(resp.text)}
    except Exception as exc:
        logging.error("get_gerrit_change_messages: %s", exc)
        return {"error": str(exc)}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    transport = os.getenv("TRANSPORT", "stdio")
    if transport == "stdio":
        mcp.run()
    else:
        host = os.getenv("HOST", "127.0.0.1")
        port = int(os.getenv("HOST_PORT", "8001"))
        mcp.run(transport=transport, host=host, port=port)
