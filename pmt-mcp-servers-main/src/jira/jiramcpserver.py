from atlassian import Jira
from typing import Any, Optional, Dict
import os
import re
from fastmcp import FastMCP
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


TRACKER_URL = os.getenv("TRACKER_URL")
# Get secret Jira token from environment (never store in repo)
JIRA_TOKEN = os.getenv("JIRA_TOKEN")

# Initialize Jira client with secret token
jira = Jira(url=TRACKER_URL, token=JIRA_TOKEN)

# Validate TRACKER_URL and JIRA_TOKEN by attempting to connect to Jira
try:
    test_jira = Jira(url=TRACKER_URL, token=JIRA_TOKEN)
    test_jira.get("/rest/api/2/myself")  # Test endpoint to verify login
    logging.info(
        "Successfully connected to Jira with the provided TRACKER_URL and JIRA_TOKEN."
    )
except Exception as e:
    logging.error(f"Failed to connect to Jira: {e}")
    raise ValueError(
        "Failed to connect to Jira. Please verify TRACKER_URL and JIRA_TOKEN."
    )

mcp = FastMCP("jira")


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
            f"Invalid HOST_PORT env variable: '{port_str}' - must be a valid integer"
        )
    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


@mcp.tool()
def jira_request(
    jql_request: str, start_at: int = 0, max_results: int = 50
) -> dict[str, Any]:
    """A tool to query Jira issues using JQL with pagination support.

    Args:
        jql_request: JQL query string to search for issues
        start_at: Starting index for pagination (default: 0)
        max_results: Maximum number of results to return (default: 50, max: 100)

    Returns:
        Dictionary containing:
        - issues: List of matching issues
        - startAt: Starting index of returned results
        - maxResults: Maximum results requested
        - total: Total number of matching issues
        - isLast: Boolean indicating if this is the last page
        - returned: Actual number of issues returned in the current page
    """
    # Jira Cloud typically has a max limit of 100
    if max_results > 100:
        max_results = 100

    # Call jira.jql with pagination parameters
    response = jira.jql(jql_request, start=start_at, limit=max_results)

    # Extract pagination metadata
    total = response.get("total", 0)
    returned_start = response.get("startAt", start_at)
    returned_max = response.get("maxResults", max_results)
    issues = response.get("issues", [])

    # Calculate if this is the last page, explicitly handling the no-results case
    is_last = total == 0 or (returned_start + len(issues)) >= total

    return {
        "issues": issues,
        "startAt": returned_start,
        "maxResults": returned_max,
        "total": total,
        "isLast": is_last,
        "returned": len(issues),
    }


@mcp.tool()
def get_all_projects() -> dict:
    """Retrieve all projects from the Jira tracker using the API endpoint method.

    Returns:
        A dictionary containing the list of projects.
    """
    try:
        return {"projects": jira.get("/rest/api/2/project")}
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve projects: {e}")


@mcp.tool()
def get_project(key: str) -> dict:
    """Retrieve details of a specific project.

    Args:
        key: Key of the project.

    Returns:
        Project details.
    """
    try:
        project = jira.get_project(key)
        return {"project": project}
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve project details: {e}")


@mcp.tool()
def get_project_components(key: str) -> dict:
    """Retrieve components of a specific project.

    Args:
        key: Key of the project.

    Returns:
        List of components.
    """
    try:
        components = jira.get_project_components(key)
        return {"components": components}
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve project components: {e}")


@mcp.tool()
def get_project_versions(key: str) -> dict:
    """Retrieve versions of a specific project.

    Args:
        key: Key of the project.

    Returns:
        List of versions.
    """
    try:
        versions = jira.get_project_versions(key)
        return {"versions": versions}
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve project versions: {e}")


@mcp.tool()
def get_project_roles(project_key: str) -> dict:
    """Retrieve roles of a specific project.

    Args:
        project_key: Key of the project.

    Returns:
        List of roles.
    """
    try:
        roles = jira.get_project_roles(project_key)
        return {"roles": roles}
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve project roles: {e}")


@mcp.tool()
def transition_issue(
    issue_key: str, transition: str | None = None, include_new_status: bool = True
) -> dict:
    """List or perform a workflow transition.

    Args:
        issue_key: Jira issue key (e.g. ABC-123).
        transition: Transition id or name (case-insensitive). If omitted -> list
            only.
        include_new_status: When True, executes an additional GET
            to return the updated status name.

    Returns:
        If listing: { issue, operation, available_transitions }
        If executing: { issue, operation, executed_id,
        executed_name, execution_response, new_status?, added_comment? }
    """
    api_path = f"/rest/api/2/issue/{issue_key}/transitions"
    transitions_raw: list[dict[str, Any]] = []
    try:
        data = jira.get(api_path)
        if isinstance(data, dict):
            transitions_raw = data.get("transitions", []) or []
    except Exception as e:  # surface concise error; no custom HTTP fallback
        raise RuntimeError(f"Unable to retrieve transitions via Jira client: {e}")

    available = {
        t.get("id"): t.get("name") for t in transitions_raw if isinstance(t, dict)
    }
    name_index = {
        (t.get("name") or "").lower(): t.get("id")
        for t in transitions_raw
        if isinstance(t, dict)
    }

    if transition is None:
        return {
            "issue": issue_key,
            "operation": "list_transitions",
            "available_transitions": available,
        }

    target_id = (
        transition if transition in available else name_index.get(transition.lower())
    )
    if not target_id:
        raise ValueError(f"Transition '{transition}' not found. Choices: {available}")

    payload = {"transition": {"id": target_id}}
    try:
        exec_resp = jira.post(api_path, data=payload)
    except Exception as e:
        raise RuntimeError(f"Transition execution failed (POST {api_path}): {e}")

    normalized = exec_resp if exec_resp not in (None, "") else {"status": "no_content"}

    new_status = None
    if include_new_status:
        try:
            issue_after = jira.issue(issue_key)
            if isinstance(issue_after, dict):
                new_status = issue_after.get("fields", {}).get("status", {}).get("name")
        except Exception:
            # Non-fatal; leave new_status as None
            pass

    result: dict[str, Any] = {
        "issue": issue_key,
        "operation": "transition",
        "executed_id": target_id,
        "executed_name": available.get(target_id),
        "execution_response": normalized,
    }
    if new_status is not None:
        result["new_status"] = new_status
    return result


@mcp.tool()
def create_issue(
    project_key: str,
    summary: str,
    issue_type: str = "User Story",
    epic_name: str | None = None,
    components: Optional[list[str]] = None,
) -> dict:
    """Create a new Jira issue (minimal interface).

    Only required inputs kept for simplicity.

    Args:
        project_key: Jira project key (e.g. PJAGENAI)
        summary: Issue summary/title
        issue_type: Issue type name (default 'User Story')
        epic_name: Epic Name (required if issue_type is 'Epic')
        components: Optional list of component names to add to the issue.
                    The components field must be enabled for the project/issue type.
                    If disabled, an error will be raised.

    Returns:
        { issue_key, issue_link, raw_issue }
    """
    fields: dict[str, Any] = {
        "project": {"key": project_key},
        "summary": summary,
        "issuetype": {"name": issue_type},
    }

    if issue_type == "Epic" and epic_name:
        fields["customfield_10102"] = epic_name  # Updated Epic Name field ID

    # Optionally set Components field (only if enabled for this project/issue type)
    if components:
        try:
            from urllib.parse import quote

            meta_path = (
                "/rest/api/2/issue/createmeta"
                f"?projectKeys={quote(project_key)}"
                f"&issuetypeNames={quote(issue_type)}"
                "&expand=projects.issuetypes.fields"
            )
            createmeta = jira.get(meta_path)
        except Exception as e:
            raise RuntimeError(
                f"Failed to retrieve create metadata for project {project_key}: {e}"
            )

        fields_meta: dict[str, Any] = {}
        if isinstance(createmeta, dict):
            projects = createmeta.get("projects", []) or []
            if projects:
                issuetypes = projects[0].get("issuetypes", []) or []
                if issuetypes:
                    fields_meta = issuetypes[0].get("fields", {}) or {}

        components_meta = (
            fields_meta.get("components") if isinstance(fields_meta, dict) else None
        )
        if not components_meta:
            raise RuntimeError(
                "Component field is disabled or not available for this project/issue "
                "type; cannot add components."
            )

        allowed_values = components_meta.get("allowedValues") or []
        allowed_by_name: dict[str, dict[str, Any]] = {}
        if isinstance(allowed_values, list):
            for comp in allowed_values:
                if isinstance(comp, dict) and comp.get("name"):
                    allowed_by_name[str(comp["name"])] = comp

        unknown_components = [
            name for name in components if name not in allowed_by_name
        ]
        if unknown_components:
            available_names = sorted(allowed_by_name.keys())
            raise ValueError(
                "Unknown component(s) requested: "
                + ", ".join(unknown_components)
                + (
                    ". Available components: " + ", ".join(available_names)
                    if available_names
                    else ""
                )
            )

        component_payload: list[dict[str, Any]] = []
        for name in components:
            meta = allowed_by_name.get(name)
            if not isinstance(meta, dict):
                continue
            comp_id = meta.get("id")
            if comp_id is not None:
                component_payload.append({"id": comp_id})
            else:
                component_payload.append({"name": name})

        if component_payload:
            fields["components"] = component_payload

    issue = jira.create_issue(fields=fields)
    key = issue.get("key") or issue.get("issueKey")
    link = f"{TRACKER_URL}/browse/{key}"
    return {"issue_key": key, "issue_link": link, "raw_issue": issue}


@mcp.tool()
def clone_issue(issue_key: str, summary_prefix: str = "[CLONE] ") -> dict:
    """Improved tool to clone an issue with a prefixed summary."""
    try:
        # Fetch the source issue
        src = jira.issue(issue_key)
        if not isinstance(src, dict):
            raise TypeError(
                "Expected source issue to be a dictionary, got {type(src).__name__}"
            )

        # Extract necessary fields
        fields = src.get("fields", {})
        project_key = fields.get("project", {}).get("key")
        issue_type = fields.get("issuetype", {}).get("name")
        summary = fields.get("summary", "")

        if not project_key:
            raise ValueError("Source issue is missing the project key")
        if not issue_type:
            raise ValueError("Source issue is missing the issue type")
        if not summary:
            raise ValueError("Source issue is missing the summary")

        # Prepare new issue fields
        new_fields = {
            "project": {"key": project_key},
            "summary": f"{summary_prefix}{summary}",
            "issuetype": {"name": issue_type},
        }

        # Create the cloned issue
        created = jira.create_issue(fields=new_fields)
        new_key = created.get("key") or created.get("issueKey")

        if not new_key:
            raise RuntimeError("Failed to retrieve the key of the cloned issue")

        return {
            "source": issue_key,
            "clone": new_key,
            "link": f"{TRACKER_URL}/browse/{new_key}",
        }

    except Exception as e:
        raise RuntimeError(f"Failed to clone issue {issue_key}: {e}")


@mcp.tool()
def get_issue_subtasks(issue_key: str) -> dict:
    """List subtasks (minimal info).

    Returns: { issue, count, subtasks: [ { key, summary } ] }
    """
    try:
        data = jira.issue(issue_key)
    except Exception as e:
        raise RuntimeError(f"Cannot load issue {issue_key}: {e}")
    subs = []
    if isinstance(data, dict):
        for s in data.get("fields", {}).get("subtasks", []) or []:
            if not isinstance(s, dict):
                continue
            key = s.get("key")
            summary = None
            if isinstance(s.get("fields"), dict):
                summary = s["fields"].get("summary")
            subs.append({"key": key, "summary": summary})
    return {"issue": issue_key, "count": len(subs), "subtasks": subs}


@mcp.tool()
def modify_issue_type(issue_key: str, new_issue_type: str | None = None) -> dict:
    """Modify the issue type of a Jira issue.

    Args:
        issue_key: Jira issue key (e.g., ABC-123).
        new_issue_type: The new issue type name. If not provided, the available
            issue types will be listed.

    Returns:
        A dictionary with the operation details.
    """
    try:
        # Fetch issue data and project key
        issue_data = jira.issue(issue_key)
        project_key = issue_data["fields"]["project"]["key"]

        # Fetch available issue types
        project_meta = jira.get(f"/rest/api/2/project/{project_key}/statuses")
        available_issue_types = [t["name"] for t in project_meta if "name" in t]

        if not new_issue_type:
            return {
                "issue": issue_key,
                "operation": "list_issue_types",
                "available_issue_types": available_issue_types,
            }

        if new_issue_type not in available_issue_types:
            raise ValueError(
                f"Invalid issue type '{new_issue_type}'. Available: "
                f"{', '.join(available_issue_types)}"
            )

        # Update issue type
        jira.update_issue_field(issue_key, {"issuetype": {"name": new_issue_type}})
        return {
            "issue": issue_key,
            "operation": "modify_issue_type",
            "new_issue_type": new_issue_type,
            "updated": True,
        }
    except Exception as e:
        raise RuntimeError(f"Error modifying issue type: {e}")


@mcp.tool()
def get_issue_link(link_id: str) -> str:
    """A tool to construct a direct link to an existing Jira issue by key.

    Example:
        get_issue_link("ABC-123") -> https://.../browse/ABC-123
    """
    return f"{TRACKER_URL}/browse/{link_id}"


@mcp.tool()
def add_issue_comment(issue_key: str, comment: str) -> dict:
    """Add a new comment to an issue.

    Returns the raw response from Jira (typically the created comment object)."""
    resp = jira.issue_add_comment(issue_key, comment)
    return {"issue": issue_key, "comment": resp}


@mcp.tool()
def update_issue_comment(issue_key: str, comment_id: str, comment: str) -> dict:
    """Update an existing comment's body (simplified implementation).

    Always performs a direct REST PUT to:
        /rest/api/2/issue/{issueKey}/comment/{commentId}

    Returns a concise response indicating success and the updated comment payload.
    """
    api_path = f"/rest/api/2/issue/{issue_key}/comment/{comment_id}"
    try:
        resp = jira.put(api_path, data={"body": comment})
    except Exception as e:
        raise RuntimeError(f"Failed to update comment {comment_id} on {issue_key}: {e}")
    return {
        "issue": issue_key,
        "comment_id": comment_id,
        "updated": True,
        "comment": resp,
    }


@mcp.tool()
def delete_issue_comment(issue_key: str, comment_id: str) -> dict:
    """Delete a specific comment by id (simplified implementation).

    Performs a direct REST DELETE to:
        /rest/api/2/issue/{issueKey}/comment/{commentId}
    Returns a concise success payload.
    """
    api_path = f"/rest/api/2/issue/{issue_key}/comment/{comment_id}"
    try:
        jira.delete(api_path)
    except Exception as e:
        raise RuntimeError(f"Failed to delete comment {comment_id} on {issue_key}: {e}")
    return {
        "issue": issue_key,
        "comment_id": comment_id,
        "deleted": True,
    }


@mcp.tool()
def get_issue_comments(issue_key: str) -> dict:
    """Retrieve all comments for an issue."""
    comments = jira.issue_get_comments(issue_key)
    return {"issue": issue_key, "comments": comments}


@mcp.tool()
def get_issue_pinned_comments(
    issue_key: str,
    pin_property_key: str = "sd-pinned",
    fallback_to_all: bool = True,
) -> dict:
    """Return pinned comments using the dedicated Jira endpoint if available.

    Uses /rest/api/2/issue/{key}/pinned-comments (as referenced in the REST browser).
    If that endpoint is missing/unsupported and fallback_to_all is True, returns
    all comments with a note. The pin_property_key parameter is retained for
    backward compatibility (ignored for the direct endpoint, only used if we
    fall back to property-based detection attempt).
    """
    endpoint = f"/rest/api/2/issue/{issue_key}/pinned-comments"
    try:
        resp = jira.get(endpoint)
        # Possible response shapes: {"comments": [...]}, or direct list
        if isinstance(resp, dict):
            pinned = resp.get("comments") or resp.get("pinnedComments") or []
        elif isinstance(resp, list):
            pinned = resp
        else:
            pinned = []
        return {
            "issue": issue_key,
            "pinned_count": len(pinned),
            "pinned_comments": pinned,
            "source": "endpoint",
        }
    except Exception as e:
        # Fallback: attempt property-based heuristic (older logic) only if allowed
        if not fallback_to_all:
            raise RuntimeError(f"Pinned comments endpoint failed: {e}")
        note = f"Pinned endpoint unavailable ({e}); returning all comments instead."
        try:
            all_comments = jira.issue_get_comments(issue_key)
        except Exception:
            all_comments = []
        return {
            "issue": issue_key,
            "pinned_count": 0,
            "pinned_comments": [],
            "all_comments": all_comments,
            "source": "fallback_all",
            "note": note,
        }


@mcp.tool()
def set_issue_description(issue_key: str, description: str) -> dict:
    """Replace the issue description with the provided text."""
    resp = jira.update_issue_field(issue_key, {"description": description})
    return {"issue": issue_key, "set_description": True, "response": resp}


@mcp.tool()
def set_issue_summary(issue_key: str, summary: str) -> dict:
    """Update the summary (title) of an existing issue.

    Args:
        issue_key: Jira issue key (e.g. ABC-123)
        summary: New summary/title (non-empty)

    Returns:
        { issue, operation, summary, response }
    """
    if not summary or not summary.strip():
        raise ValueError("Summary must be a non-empty string")
    try:
        resp = jira.update_issue_field(issue_key, {"summary": summary})
    except Exception as e:
        raise RuntimeError(f"Failed to set summary on {issue_key}: {e}")
    return {
        "issue": issue_key,
        "operation": "set_issue_summary",
        "summary": summary,
        "response": resp,
    }


@mcp.tool()
def get_issue_description(issue_key: str) -> dict:
    """Fetch the current issue description."""
    issue_data = jira.issue(issue_key)
    description_value = None
    if isinstance(issue_data, dict):
        description_value = issue_data.get("fields", {}).get(
            "description"
        ) or issue_data.get("description")
    return {"issue": issue_key, "description": description_value}


@mcp.tool()
def assign_issue(issue_key: str, assignee: str | None = None) -> dict:
    """Assign or reassign an issue to a user.

    If assignee omitted, resolves the current user via /myself.
    Returns a simple success payload.
    """
    target = assignee
    if target is None:
        try:
            me = jira.get("/rest/api/2/myself")
            if isinstance(me, dict):
                target = me.get("name") or me.get("username")
        except Exception:
            target = None
    if not target:
        raise ValueError("Could not resolve assignee (provide username explicitly).")
    try:
        resp = jira.put(
            f"/rest/api/2/issue/{issue_key}/assignee", data={"name": target}
        )
    except Exception as e:
        raise RuntimeError(f"Assignment failed: {e}")
    return {
        "issue": issue_key,
        "operation": "assign_issue",
        "assignee": target,
        "assigned_success": True,
        "raw_response": resp,
    }


@mcp.tool()
def modify_issue_labels(
    issue_key: str,
    add: list[str] | None = None,
    remove: list[str] | None = None,
    set_labels: list[str] | None = None,
) -> dict:
    """Modify an issue's labels with a single flexible tool.

        Usage patterns:
            - Provide set_labels to fully replace existing labels (add/remove ignored).
            - Provide add to append labels (idempotent; duplicates removed).
            - Provide remove to remove labels if present.
            - Provide both add and remove to perform both operations atomically
                (add first, then remove).

    Args:
        issue_key: Jira issue key.
        add: Labels to add (optional).
        remove: Labels to remove (optional).
        set_labels: If provided, replaces label list entirely (takes precedence).

    Returns:
        { issue, before_labels, after_labels, added_effective,
        removed_effective, operation }
    """
    if set_labels is None and not (add or remove):
        raise ValueError("Provide set_labels or at least one of add/remove.")

    issue_data = jira.issue(issue_key)
    before: list[str] = []
    try:
        before = (
            issue_data.get("fields", {}).get("labels", [])
            if isinstance(issue_data, dict)
            else []
        )
    except Exception:
        before = []

    if set_labels is not None:
        final_labels = list(
            dict.fromkeys(set_labels)
        )  # de-dupe preserve order in provided list
        jira.update_issue_field(issue_key, {"labels": final_labels})
        return {
            "issue": issue_key,
            "operation": "replace",
            "before_labels": before,
            "after_labels": final_labels,
            "added_effective": [label for label in final_labels if label not in before],
            "removed_effective": [
                label for label in before if label not in final_labels
            ],
        }

    # Start from current state
    working = before[:]

    added_effective: list[str] = []
    if add:
        for label in add:
            if label not in working:
                working.append(label)
                added_effective.append(label)

    removed_effective: list[str] = []
    if remove:
        to_remove = set(remove)
        new_working = []
        for lbl in working:
            if lbl in to_remove:
                removed_effective.append(lbl)
            else:
                new_working.append(lbl)
        working = new_working

    jira.update_issue_field(issue_key, {"labels": working})
    return {
        "issue": issue_key,
        "operation": "add_remove",
        "before_labels": before,
        "after_labels": working,
        "added_effective": added_effective,
        "removed_effective": removed_effective,
    }


@mcp.tool()
def add_issue_components(issue_key: str, components: list[str]) -> dict:
    """Add one or more components to an existing Jira issue.

    This tool first verifies that the Components field is enabled and editable for the
    given issue. If the field is disabled or not present on the edit screen, it will
    return a clear error explaining that components cannot be added.

    Components are specified by name and will be merged with any existing
    components on the issue (no duplicates).

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        components: List of component names to add (e.g., ['Backend', 'API'])

    Returns:
        Dictionary containing:
        - issue: The issue key
        - operation: 'add_issue_components'
        - project_key: The project key
        - before_components: List of component names before update
        - requested_components: List of requested component names
        - added_effective: List of components actually added (excludes duplicates)
        - after_components: List of component names after update
        - response: Raw Jira API response
    """
    if not components:
        raise ValueError("Provide at least one component name to add.")

    # Check whether Components field is editable for this issue
    try:
        editmeta = jira.get(f"/rest/api/2/issue/{issue_key}/editmeta")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve edit metadata for {issue_key}: {e}")

    fields_meta = editmeta.get("fields", {}) if isinstance(editmeta, dict) else {}
    components_meta = (
        fields_meta.get("components") if isinstance(fields_meta, dict) else None
    )
    if not components_meta:
        raise RuntimeError(
            "Component field is disabled or not editable for this issue; "
            "cannot add components."
        )

    # Load issue to get project key and current components
    try:
        issue_data = jira.issue(issue_key)
    except Exception as e:
        raise RuntimeError(f"Cannot load issue {issue_key}: {e}")

    if not isinstance(issue_data, dict):
        raise RuntimeError(f"Unexpected issue payload for {issue_key}; cannot update.")

    fields_data = issue_data.get("fields", {}) or {}
    project_key = (
        fields_data.get("project", {}).get("key")
        if isinstance(fields_data.get("project"), dict)
        else None
    )
    if not project_key:
        raise RuntimeError(
            f"Could not determine project key for issue {issue_key}; cannot resolve components."
        )

    # Retrieve allowed components for this project
    try:
        project_components = jira.get_project_components(project_key)
    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve components for project {project_key}: {e}"
        )

    allowed_by_name: dict[str, dict[str, Any]] = {}
    if isinstance(project_components, list):
        for comp in project_components:
            if isinstance(comp, dict) and comp.get("name"):
                allowed_by_name[str(comp["name"])] = comp

    if not allowed_by_name:
        raise RuntimeError(
            f"Component field appears enabled but no components are defined for project {project_key}; "
            "cannot add components."
        )

    # Validate requested component names
    unknown_components = [name for name in components if name not in allowed_by_name]
    if unknown_components:
        available_names = sorted(allowed_by_name.keys())
        raise ValueError(
            "Unknown component(s) requested: "
            + ", ".join(unknown_components)
            + (
                ". Available components: " + ", ".join(available_names)
                if available_names
                else ""
            )
        )

    # Compute existing and final component name sets (merge, no duplicates)
    current_components_raw = fields_data.get("components", []) or []
    before_names: list[str] = []
    if isinstance(current_components_raw, list):
        for comp in current_components_raw:
            if isinstance(comp, dict) and comp.get("name"):
                before_names.append(str(comp["name"]))

    added_effective: list[str] = []
    final_names: list[str] = before_names[:]
    for name in components:
        if name not in final_names:
            final_names.append(name)
            added_effective.append(name)

    # Build payload using component IDs when available
    final_components_payload: list[dict[str, Any]] = []
    for name in final_names:
        meta = allowed_by_name.get(name)
        if not isinstance(meta, dict):
            continue
        comp_id = meta.get("id")
        if comp_id is not None:
            final_components_payload.append({"id": comp_id})
        else:
            final_components_payload.append({"name": name})

    try:
        resp = jira.update_issue_field(
            issue_key, {"components": final_components_payload}
        )
    except Exception as e:
        raise RuntimeError(f"Failed to update components on {issue_key}: {e}")

    return {
        "issue": issue_key,
        "operation": "add_issue_components",
        "project_key": project_key,
        "before_components": before_names,
        "requested_components": components,
        "added_effective": added_effective,
        "after_components": final_names,
        "response": resp,
    }


@mcp.tool()
def issue_priority(
    issue_key: str | None = None,
    new_priority: str | None = None,
) -> dict:
    """Unified priority tool.

    Usage patterns:
        - List all priorities: issue_priority()
        - Get current issue priority (plus list):
            issue_priority(issue_key="ABC-123")
        - Set issue priority:
            issue_priority(issue_key="ABC-123", new_priority="High")

    Returns a dict containing:
        operation: list|get|set
        priorities: list of available priorities (id, name, description,
            iconUrl, statusColor)
        issue: (when provided)
        current_priority: (when issue_key provided)
        updated: bool (only for set operation)
        set_priority: the name applied (only for set operation)
        error: in case of recoverable issue fetch failure
    """
    # Fetch priorities first (shared for all modes)
    try:
        raw = jira.get("/rest/api/2/priority")
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve priorities: {e}")

    priorities: list[dict[str, Any]] = []
    name_index: dict[str, dict[str, Any]] = {}
    if isinstance(raw, list):
        for p in raw:
            if isinstance(p, dict):
                entry = {
                    "id": p.get("id"),
                    "name": p.get("name"),
                    "statusColor": p.get("statusColor"),
                    "description": p.get("description"),
                    "iconUrl": p.get("iconUrl"),
                }
                priorities.append(entry)
                if entry["name"]:
                    name_index[entry["name"].lower()] = entry
    else:
        return {"operation": "list", "priorities": [{"raw": raw}]}

    # Mode: list only
    if issue_key is None:
        return {"operation": "list", "priorities": priorities}

    # Try to get current priority of issue
    current_priority: str | None = None
    issue_error: str | None = None
    issue_data: dict[str, Any] | None = None
    try:
        issue_data = jira.issue(issue_key)
        if isinstance(issue_data, dict):
            current_priority = (
                issue_data.get("fields", {}).get("priority", {}).get("name")
            )
    except Exception as e:  # non-fatal for list mode
        issue_error = f"Failed to fetch issue {issue_key}: {e}"  # surfaced in response

    # If no new priority requested -> get mode
    if new_priority is None:
        resp: dict[str, Any] = {
            "operation": "get",
            "issue": issue_key,
            "current_priority": current_priority,
            "priorities": priorities,
        }
        if issue_error:
            resp["error"] = issue_error
        return resp

    # Set mode
    target_name_lower = new_priority.lower()
    if target_name_lower not in name_index:
        raise ValueError(
            f"Priority '{new_priority}' not found. Available: "
            + ", ".join(sorted(p["name"] for p in priorities if p.get("name")))
        )
    try:
        jira.update_issue_field(
            issue_key, {"priority": {"name": name_index[target_name_lower]["name"]}}
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to set priority '{new_priority}' on {issue_key}: {e}"
        )

    return {
        "operation": "set",
        "issue": issue_key,
        "set_priority": name_index[target_name_lower]["name"],
        "updated": True,
        "priorities": priorities,
        "previous_priority": current_priority,
    }


@mcp.tool()
def set_issue_reporter(issue_key: str, reporter: str) -> dict:
    """Change the reporter of an issue.

    NOTE: On Jira Cloud, this may require using accountId instead of
    username; provide the correct identifier accordingly.
    """
    if not reporter:
        raise ValueError("Reporter identifier required")
    # Try both conventional shapes (username/name) and accountId fallback
    # logic left to caller
    payload_options = [
        {"reporter": {"name": reporter}},  # Server/DC style
        {
            "reporter": {"accountId": reporter}
        },  # Cloud style if caller supplied accountId
    ]
    last_error = None
    for fields in payload_options:
        try:
            resp = jira.update_issue_field(issue_key, fields)
            return {
                "issue": issue_key,
                "operation": "set_issue_reporter",
                "reporter": reporter,
                "response": resp,
            }
        except Exception as e:  # try next shape
            last_error = e
            continue
    raise RuntimeError(f"Failed to set reporter using supported shapes: {last_error}")


@mcp.tool()
def issue_editable_fields(issue_key: str) -> dict:
    """Retrieve the editmeta for an issue and list editable fields.

    Useful to diagnose why a field (e.g. reporter) cannot be changed.
    If a field does not appear in the returned 'fields' structure, it
    generally means it is not on the edit screen or you lack permission
    to modify it.
    """
    api_path = f"/rest/api/2/issue/{issue_key}/editmeta"
    try:
        meta = jira.get(api_path)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch editmeta for {issue_key}: {e}")
    fields = meta.get("fields", {}) if isinstance(meta, dict) else {}
    editable_field_keys = sorted(list(fields.keys()))
    return {
        "issue": issue_key,
        "operation": "editmeta",
        "editable_field_count": len(editable_field_keys),
        "editable_fields": editable_field_keys,
        "raw": meta,
    }


@mcp.tool()
def search_users(query: str, max_results: int = 20) -> dict:
    """Search Jira users by a query (username / display name fragment).

    Tries both legacy 'username' param (Server/DC) and 'query' param (some
    deployments) and returns a normalized list of matches with key identity
    attributes.
    """
    if not query:
        raise ValueError("Provide a non-empty query string")
    candidates: list[dict[str, Any]] = []
    errors: list[str] = []
    # Attempt legacy username search
    for param in ("username", "query"):
        try:
            resp = jira.get(
                f"/rest/api/2/user/search?{param}={query}&maxResults={max_results}"
            )
            if isinstance(resp, list):
                for u in resp:
                    if not isinstance(u, dict):
                        continue
                    entry = {
                        "name": u.get("name") or u.get("username"),
                        "key": u.get("key"),
                        "displayName": u.get("displayName"),
                        "accountId": u.get("accountId"),
                        "active": u.get("active"),
                    }
                    if entry not in candidates:
                        candidates.append(entry)
        except Exception as e:
            errors.append(f"{param} search error: {e}")
    return {
        "operation": "search_users",
        "query": query,
        "match_count": len(candidates),
        "matches": candidates,
        "errors": errors or None,
    }


@mcp.tool()
def set_due_date(issue_key: str, due_date: str) -> dict:
    """Set (or replace) the issue due date.

    due_date must be in ISO format YYYY-MM-DD.
    """
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due_date):
        raise ValueError("due_date must be YYYY-MM-DD")
    try:
        jira.update_issue_field(issue_key, {"duedate": due_date})
    except Exception as e:
        raise RuntimeError(f"Failed to set due date: {e}")
    return {"issue": issue_key, "operation": "set_due_date", "due_date": due_date}


@mcp.tool()
def add_worklog_entry(
    issue_key: str,
    time_spent: str,
    comment: str | None = None,
    started: str | None = None,
) -> dict:
    """Add a worklog entry to an issue.

    Args:
        time_spent: e.g. '1h', '30m', '2h 15m'
        comment: optional comment
        started: ISO datetime (YYYY-MM-DDTHH:MM:SS.mmm+0000). If omitted Jira sets now.
    """
    payload: dict[str, Any] = {"timeSpent": time_spent}
    if comment:
        payload["comment"] = comment
    if started:
        payload["started"] = started
    api_path = f"/rest/api/2/issue/{issue_key}/worklog"
    try:
        resp = jira.post(api_path, data=payload)
    except Exception as e:
        raise RuntimeError(f"Failed to add worklog: {e}")
    return {
        "issue": issue_key,
        "operation": "add_worklog_entry",
        "time_spent": time_spent,
        "response": resp,
    }


@mcp.tool()
def update_time_tracking(
    issue_key: str,
    original_estimate: Optional[str] = None,
    remaining_estimate: Optional[str] = None,
) -> dict:
    """Update time tracking fields for a Jira issue.

    Args:
        issue_key: Jira issue key (e.g., ABC-123).
        original_estimate: Original estimated time (e.g., '3d', '5h').
        remaining_estimate: Remaining estimated time (e.g., '2d', '4h').

    Returns:
        A dictionary with the updated time tracking details.

    Notes:
        If only one of `original_estimate` or `remaining_estimate` is provided,
        Jira may automatically sync the other field to match the provided value.
        It is recommended to provide both fields simultaneously to avoid this behavior.
    """
    if not original_estimate and not remaining_estimate:
        raise ValueError(
            "At least one of `original_estimate` or `remaining_estimate` must "
            "be provided."
        )

    if original_estimate and not remaining_estimate:
        raise ValueError(
            "You provided only `original_estimate`. Please provide "
            "`remaining_estimate` as well to avoid unintended changes."
        )

    if remaining_estimate and not original_estimate:
        raise ValueError(
            "You provided only `remaining_estimate`. Please provide "
            "`original_estimate` as well to avoid unintended changes."
        )

    fields: Dict[str, Dict[str, str]] = {}

    if original_estimate or remaining_estimate:
        fields["timetracking"] = {}

    if original_estimate:
        fields["timetracking"]["originalEstimate"] = original_estimate

    if remaining_estimate:
        fields["timetracking"]["remainingEstimate"] = remaining_estimate

    try:
        response = jira.issue_update(issue_key, fields=fields)
    except Exception as e:
        raise RuntimeError(f"Failed to update time tracking for {issue_key}: {e}")

    return {
        "issue": issue_key,
        "updated_fields": fields,
        "response": response,
    }


@mcp.tool()
def get_issue_votes(issue_key: str) -> dict:
    """Retrieve the votes for a Jira issue."""
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/votes"
        response = jira.get(api_path)
        return {
            "issue": issue_key,
            "votes": response.get("votes"),
            "voters": response.get("voters", []),
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve votes for issue {issue_key}: {e}")


@mcp.tool()
def get_issue_watchers(issue_key: str) -> dict:
    """Retrieve the watchers for a Jira issue."""
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/watchers"
        response = jira.get(api_path)
        return {
            "issue": issue_key,
            "watchCount": response.get("watchCount"),
            "isWatching": response.get("isWatching"),
            "watchers": response.get("watchers", []),
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve watchers for issue {issue_key}: {e}")


@mcp.tool()
def vote_for_issue(issue_key: str) -> dict:
    """Vote for a Jira issue."""
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/votes"
        response = jira.post(api_path)
        return {
            "issue": issue_key,
            "operation": "vote",
            "response": response,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to vote for issue {issue_key}: {e}")


@mcp.tool()
def add_watcher(issue_key: str, watcher: str) -> dict:
    """Add a watcher to a Jira issue."""
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/watchers"
        response = jira.post(api_path, data=watcher)
        return {
            "issue": issue_key,
            "operation": "add_watcher",
            "watcher": watcher,
            "response": response,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to add watcher {watcher} to issue {issue_key}: {e}")


@mcp.tool()
def remove_watcher(issue_key: str, watcher: str) -> dict:
    """Remove a watcher from a Jira issue."""
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/watchers?username={watcher}"
        jira.delete(api_path)
        return {
            "issue": issue_key,
            "operation": "remove_watcher",
            "watcher": watcher,
            "status": "success",
        }
    except Exception as e:
        raise RuntimeError(
            f"Failed to remove watcher {watcher} from issue {issue_key}: {e}"
        )


@mcp.tool()
def remove_vote(issue_key: str) -> dict:
    """Remove the current user's vote from a Jira issue."""
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/votes"
        jira.delete(api_path)
        return {
            "issue": issue_key,
            "operation": "remove_vote",
            "status": "success",
        }
    except Exception as e:
        raise RuntimeError(f"Failed to remove vote from issue {issue_key}: {e}")


@mcp.tool()
def link_epic_to_issue(
    epic_key: str,
    issue_key: str,
    epic_field_id: str | None = None,
    mode: str = "link",
) -> dict:
    """Link an issue to an Epic with fallback logic.

    Link Strategy (same as earlier implementation):
      1. If `epic_field_id` provided, attempt direct field update.
      2. Otherwise (or on failure) use Agile epic issue POST endpoint.

    Args:
        epic_key: Epic key (required for linking).
        issue_key: Issue key to link.
        epic_field_id: Optional Epic Link field id (e.g. customfield_10014).

    Returns:
        Dict summarising operation outcome.
    """
    # Linking flow (original implementation)
    result: dict = {
        "operation": "link",
        "epic_key": epic_key,
        "issue_key": issue_key,
        "epic_field_id": epic_field_id,
        "linked": False,
        "method_used": None,
        "steps": [],
    }

    # Step 1: optional direct field update
    if epic_field_id:
        try:
            resp = jira.update_issue_field(issue_key, {epic_field_id: epic_key})
            result.update(
                {
                    "linked": True,
                    "method_used": "field_update",
                    "response": resp,
                    "steps": result["steps"] + ["field_update_success"],
                }
            )
            return result
        except Exception as e:  # fall through to Agile POST
            result["steps"].append(f"field_update_failed: {e}")

    # Step 2: Agile POST fallback
    try:
        base = jira.resource_url("epic", api_root="rest/agile", api_version="1.0")
        url = f"{base}/{epic_key}/issue/" f"{issue_key}"
        resp = jira.post(url, data={"issues": [issue_key]})
        result.update(
            {
                "linked": True,
                "method_used": "agile_post",
                "response": resp,
                "steps": result["steps"] + ["agile_post_success"],
            }
        )
        return result
    except Exception as e:
        result.update(
            {
                "linked": False,
                "method_used": result["method_used"] or "agile_post",
                "error": str(e),
                "steps": result["steps"] + [f"agile_post_failed: {e}"],
            }
        )
        return result


@mcp.tool()
def link_issues(
    inward_issue: str,
    outward_issue: str,
    link_type: str = "Relates",
    comment: str | None = None,
) -> dict:
    """Create a link between two Jira issues.

    Minimal wrapper that reuses the Jira module's native create_issue_link
    function (or issue_link alias) without re‑implementing logic.

    Args:
        inward_issue: Inward issue key (e.g. ABC-1)
        outward_issue: Outward issue key (e.g. ABC-2)
        link_type: Link type name (Relates, Blocks, Cloners, etc.)
        comment: Optional comment body

    Returns:
        { operation, inward_issue, outward_issue, link_type,
        comment_added, raw_response }
    """
    if not inward_issue or not outward_issue:
        raise ValueError("Both inward_issue and outward_issue are required")

    # The atlassian-python-api Jira client (jira.py) does not expose a direct
    # create_issue_link convenience method (confirmed via grep). We therefore
    # reuse the existing generic REST helper jira.post against /issueLink.
    payload: Dict[str, Any] = {
        "type": {"name": link_type},
        "inwardIssue": {"key": inward_issue},
        "outwardIssue": {"key": outward_issue},
    }
    if comment:
        payload["comment"] = {"body": comment}

    try:
        raw = jira.post("/rest/api/2/issueLink", data=payload)
    except Exception as e:
        raise RuntimeError(
            f"Failed to link issues {inward_issue} -> {outward_issue}: {e}"
        )

    return {
        "operation": "link_issues",
        "inward_issue": inward_issue,
        "outward_issue": outward_issue,
        "link_type": link_type,
        "comment_added": bool(comment),
        "request_payload": payload,
        "raw_response": raw,
    }


@mcp.tool()
def unlink_issues(
    inward_issue: str, outward_issue: str, link_type: str = "Relates"
) -> dict:
    """Remove a link between two Jira issues.

    Args:
        inward_issue: Inward issue key (e.g. ABC-1).
        outward_issue: Outward issue key (e.g. ABC-2).
        link_type: Link type name (Relates, Blocks, Cloners, etc.).

    Returns:
        { operation, inward_issue, outward_issue, link_type, raw_response }.
    """
    if not inward_issue or not outward_issue:
        raise ValueError("Both inward_issue and outward_issue are required")

    # Fetch all issue links for the inward issue
    try:
        issue_data = jira.issue(inward_issue)
        issue_links = issue_data.get("fields", {}).get("issuelinks", [])
    except Exception as e:
        raise RuntimeError(f"Failed to fetch issue links for {inward_issue}: {e}")

    # Find the link to remove
    link_id_to_remove = None
    for link in issue_links:
        if (
            link.get("type", {}).get("name") == link_type
            and link.get("outwardIssue", {}).get("key") == outward_issue
        ):
            link_id_to_remove = link.get("id")
            break

    if not link_id_to_remove:
        raise ValueError(
            f"No link of type '{link_type}' found between {inward_issue} and "
            f"{outward_issue}"
        )

    # Remove the link
    try:
        api_path = f"/rest/api/2/issueLink/{link_id_to_remove}"
        response = jira.delete(api_path)
    except Exception as e:
        raise RuntimeError(
            f"Failed to unlink issues {inward_issue} -> {outward_issue}: {e}"
        )

    return {
        "operation": "unlink_issues",
        "inward_issue": inward_issue,
        "outward_issue": outward_issue,
        "link_type": link_type,
        "raw_response": response,
    }


@mcp.tool()
def get_issue_attachments(issue_key: str) -> dict:
    """Get all attachments for a Jira issue.

    Args:
        issue_key: Jira issue key (e.g. ABC-123)

    Returns:
        Dictionary containing issue key and list of attachments with their details
    """
    try:
        issue_data = jira.issue(issue_key)
        attachments = issue_data.get("fields", {}).get("attachment", [])

        attachment_list = []
        for attachment in attachments:
            attachment_info = {
                "id": attachment.get("id"),
                "filename": attachment.get("filename"),
                "author": attachment.get("author", {}).get("displayName"),
                "created": attachment.get("created"),
                "size": attachment.get("size"),
                "mimeType": attachment.get("mimeType"),
                "content": attachment.get("content"),  # Download URL
                "thumbnail": attachment.get("thumbnail"),
            }
            attachment_list.append(attachment_info)

        return {
            "issue": issue_key,
            "attachment_count": len(attachment_list),
            "attachments": attachment_list,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get attachments for issue {issue_key}: {e}")


@mcp.tool()
def upload_attachment(
    issue_key: str, file_path: str, filename: Optional[str] = None
) -> dict:
    """Upload a file attachment to a Jira issue.

    Args:
        issue_key: Jira issue key (e.g. ABC-123)
        file_path: Local path to the file to upload
        filename: Optional custom filename (defaults to basename of file_path)

    Returns:
        Dictionary containing the uploaded file information
    """
    import os

    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    if not filename:
        filename = os.path.basename(file_path)

    try:
        # Use the atlassian library's attachment upload method
        api_path = f"/rest/api/2/issue/{issue_key}/attachments"

        with open(file_path, "rb") as file:
            files = {"file": (filename, file)}
            headers = {"X-Atlassian-Token": "no-check"}

            # Use the jira client's post method with files
            response = jira.post(api_path, files=files, headers=headers)

        return {
            "issue": issue_key,
            "operation": "upload_attachment",
            "filename": filename,
            "file_path": file_path,
            "uploaded": True,
            "response": response,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to upload attachment to issue {issue_key}: {e}")


@mcp.tool()
def download_attachment(attachment_id: str, save_path: Optional[str] = None) -> dict:
    """Download an attachment from Jira.

    Args:
        attachment_id: ID of the attachment to download
        save_path: Local path where to save the file (optional)

    Returns:
        Dictionary containing download result and file information
    """
    try:
        # First get attachment metadata
        api_path = f"/rest/api/2/attachment/{attachment_id}"
        attachment_meta = jira.get(api_path)

        filename = attachment_meta.get("filename", f"attachment_{attachment_id}")
        content_url = attachment_meta.get("content")

        if not content_url:
            raise RuntimeError("No content URL found for attachment")

        # Download the actual file content
        import os

        # Use the same session/auth as jira client
        response = jira._session.get(content_url)
        response.raise_for_status()

        # Determine save path
        if not save_path:
            save_path = os.path.join(os.getcwd(), filename)
        elif os.path.isdir(save_path):
            save_path = os.path.join(save_path, filename)

        # Save file
        with open(save_path, "wb") as f:
            f.write(response.content)

        return {
            "attachment_id": attachment_id,
            "operation": "download_attachment",
            "filename": filename,
            "save_path": save_path,
            "size": len(response.content),
            "downloaded": True,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to download attachment {attachment_id}: {e}")


@mcp.tool()
def get_attachment_metadata(attachment_id: str) -> dict:
    """Get metadata for a specific attachment.

    Args:
        attachment_id: ID of the attachment

    Returns:
        Dictionary containing attachment metadata
    """
    try:
        api_path = f"/rest/api/2/attachment/{attachment_id}"
        attachment_meta = jira.get(api_path)

        return {
            "attachment_id": attachment_id,
            "operation": "get_attachment_metadata",
            "metadata": {
                "id": attachment_meta.get("id"),
                "filename": attachment_meta.get("filename"),
                "author": attachment_meta.get("author", {}).get("displayName"),
                "created": attachment_meta.get("created"),
                "size": attachment_meta.get("size"),
                "mimeType": attachment_meta.get("mimeType"),
                "content": attachment_meta.get("content"),
                "thumbnail": attachment_meta.get("thumbnail"),
            },
        }
    except Exception as e:
        raise RuntimeError(
            f"Failed to get metadata for attachment {attachment_id}: {e}"
        )


@mcp.tool()
def get_user_filters() -> dict:
    """Get current user's saved filters.

    Returns:
        Dictionary containing user's saved filters
    """
    try:
        api_path = "/rest/api/2/filter/favourite"
        filters = jira.get(api_path)

        # Normalize the response
        normalized_filters = []
        for filter_item in filters:
            if isinstance(filter_item, dict):
                normalized = {
                    "id": filter_item.get("id"),
                    "name": filter_item.get("name"),
                    "description": filter_item.get("description"),
                    "jql": filter_item.get("jql"),
                    "owner": filter_item.get("owner", {}).get("displayName"),
                    "viewUrl": filter_item.get("viewUrl"),
                    "favourite": filter_item.get("favourite", False),
                    "sharePermissions": filter_item.get("sharePermissions", []),
                }
                normalized_filters.append(normalized)

        return {
            "operation": "get_user_filters",
            "filter_count": len(normalized_filters),
            "filters": normalized_filters,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve user filters: {e}")


@mcp.tool()
def create_filter(name: str, jql: str, description: Optional[str] = None) -> dict:
    """Create a new filter.

    Args:
        name: Name of the filter
        jql: JQL query for the filter
        description: Optional description

    Returns:
        Dictionary containing the created filter details
    """
    try:
        payload = {"name": name, "jql": jql, "favourite": True}

        if description:
            payload["description"] = description

        api_path = "/rest/api/2/filter"
        response = jira.post(api_path, data=payload)

        return {
            "operation": "create_filter",
            "filter": {
                "id": response.get("id"),
                "name": response.get("name"),
                "description": response.get("description"),
                "jql": response.get("jql"),
                "owner": response.get("owner", {}).get("displayName"),
                "viewUrl": response.get("viewUrl"),
            },
            "created": True,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to create filter: {e}")


@mcp.tool()
def get_filter_by_id(filter_id: str) -> dict:
    """Get details of a specific filter by ID.

    Args:
        filter_id: ID of the filter

    Returns:
        Dictionary containing filter details
    """
    try:
        api_path = f"/rest/api/2/filter/{filter_id}"
        filter_data = jira.get(api_path)

        return {
            "operation": "get_filter_by_id",
            "filter": {
                "id": filter_data.get("id"),
                "name": filter_data.get("name"),
                "description": filter_data.get("description"),
                "jql": filter_data.get("jql"),
                "owner": filter_data.get("owner", {}).get("displayName"),
                "viewUrl": filter_data.get("viewUrl"),
                "searchUrl": filter_data.get("searchUrl"),
                "favourite": filter_data.get("favourite", False),
                "sharePermissions": filter_data.get("sharePermissions", []),
            },
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve filter {filter_id}: {e}")


@mcp.tool()
def delete_filter(filter_id: str) -> dict:
    """Delete a filter by ID.

    Args:
        filter_id: ID of the filter to delete

    Returns:
        Dictionary containing deletion status
    """
    try:
        api_path = f"/rest/api/2/filter/{filter_id}"
        jira.delete(api_path)

        return {
            "operation": "delete_filter",
            "filter_id": filter_id,
            "deleted": True,
            "status": "success",
        }
    except Exception as e:
        raise RuntimeError(f"Failed to delete filter {filter_id}: {e}")


@mcp.tool()
def update_filter(
    filter_id: str,
    name: Optional[str] = None,
    jql: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """Update an existing filter.

    Args:
        filter_id: ID of the filter to update
        name: New name for the filter (optional)
        jql: New JQL query for the filter (optional)
        description: New description for the filter (optional)

    Returns:
        Dictionary containing the updated filter details
    """
    try:
        # First get the current filter to preserve any values not being updated
        api_path = f"/rest/api/2/filter/{filter_id}"
        current_filter = jira.get(api_path)

        # Prepare update payload with existing values for fields not specified
        payload = {
            "name": name if name is not None else current_filter.get("name"),
            "jql": jql if jql is not None else current_filter.get("jql"),
            "description": description
            if description is not None
            else current_filter.get("description"),
            "favourite": current_filter.get("favourite", True),
        }

        # Update the filter
        response = jira.put(api_path, data=payload)

        return {
            "operation": "update_filter",
            "filter": {
                "id": response.get("id"),
                "name": response.get("name"),
                "description": response.get("description"),
                "jql": response.get("jql"),
                "owner": response.get("owner", {}).get("displayName"),
                "viewUrl": response.get("viewUrl"),
            },
            "updated": True,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to update filter {filter_id}: {e}")


@mcp.tool()
def get_dashboards() -> dict:
    """Get user dashboards.

    Returns:
        Dictionary containing user's dashboards
    """
    try:
        api_path = "/rest/api/2/dashboard"
        dashboards_data = jira.get(api_path)

        # Extract the dashboards list
        dashboards_list = dashboards_data.get("dashboards", [])

        # Normalize the dashboards
        normalized_dashboards = []
        for dashboard in dashboards_list:
            if isinstance(dashboard, dict):
                normalized = {
                    "id": dashboard.get("id"),
                    "name": dashboard.get("name"),
                    "description": dashboard.get("description"),
                    "owner": dashboard.get("owner", {}).get("displayName"),
                    "viewUrl": dashboard.get("view"),
                    "isPrivate": dashboard.get("isPrivate", False),
                    "isFavourite": dashboard.get("favourite", False),
                    "popularity": dashboard.get("popularity"),
                }
                normalized_dashboards.append(normalized)

        return {
            "operation": "get_dashboards",
            "dashboard_count": len(normalized_dashboards),
            "total_count": dashboards_data.get("total", 0),
            "dashboards": normalized_dashboards,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve dashboards: {e}")


@mcp.tool()
def get_dashboard_by_id(dashboard_id: str) -> dict:
    """Get details of a specific dashboard by ID.

    Args:
        dashboard_id: ID of the dashboard

    Returns:
        Dictionary containing dashboard details
    """
    try:
        api_path = f"/rest/api/2/dashboard/{dashboard_id}"
        dashboard_data = jira.get(api_path)

        # Extract gadgets
        gadgets = []
        for gadget in dashboard_data.get("gadgets", []):
            if isinstance(gadget, dict):
                gadget_info = {
                    "id": gadget.get("id"),
                    "title": gadget.get("title"),
                    "type": gadget.get("gadgetType", {}).get("moduleKey"),
                    "position": {
                        "column": gadget.get("position", {}).get("column"),
                        "row": gadget.get("position", {}).get("row"),
                    },
                }
                gadgets.append(gadget_info)

        return {
            "operation": "get_dashboard_by_id",
            "dashboard": {
                "id": dashboard_data.get("id"),
                "name": dashboard_data.get("name"),
                "description": dashboard_data.get("description"),
                "owner": dashboard_data.get("owner", {}).get("displayName"),
                "viewUrl": dashboard_data.get("view"),
                "editUrl": dashboard_data.get("editUrl"),
                "isPrivate": dashboard_data.get("isPrivate", False),
                "popularity": dashboard_data.get("popularity"),
                "gadgets": gadgets,
            },
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve dashboard {dashboard_id}: {e}")


@mcp.tool()
def get_issue_history(issue_key: str, expand: bool = False) -> dict:
    """Get the complete history of an issue including all changes.

    Args:
        issue_key: Jira issue key (e.g., ABC-123)
        expand: Whether to expand all fields (defaults to False)

    Returns:
        Dictionary containing issue history details
    """
    try:
        # Use the REST API to fetch issue with changelog
        expand_params = "changelog"
        if expand:
            expand_params += ",renderedFields,names,schema"

        api_path = f"/rest/api/2/issue/{issue_key}?expand={expand_params}"
        issue_data = jira.get(api_path)

        # Extract changelog histories
        histories = []
        if "changelog" in issue_data and "histories" in issue_data["changelog"]:
            for history in issue_data["changelog"]["histories"]:
                history_entry = {
                    "id": history.get("id"),
                    "created": history.get("created"),
                    "author": {
                        "name": history.get("author", {}).get("displayName"),
                        "key": history.get("author", {}).get("key"),
                        "email": history.get("author", {}).get("emailAddress"),
                    },
                    "items": [],
                }

                # Process each changed item
                for item in history.get("items", []):
                    item_entry = {
                        "field": item.get("field"),
                        "fieldtype": item.get("fieldtype"),
                        "from": item.get("fromString"),
                        "to": item.get("toString"),
                    }
                    history_entry["items"].append(item_entry)

                histories.append(history_entry)

        return {
            "operation": "get_issue_history",
            "issue_key": issue_key,
            "issue_summary": issue_data.get("fields", {}).get("summary"),
            "history_count": len(histories),
            "histories": histories,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve history for issue {issue_key}: {e}")


@mcp.tool()
def get_issue_changelog(issue_key: str, field_filter: Optional[str] = None) -> dict:
    """Get a formatted changelog of an issue with optional field filtering.

    Args:
        issue_key: Jira issue key (e.g., ABC-123)
        field_filter: Optional field name to filter changes by
        (e.g., 'status', 'assignee')

    Returns:
        Dictionary containing formatted changelog details
    """
    try:
        # Use the REST API to fetch issue with changelog
        api_path = f"/rest/api/2/issue/{issue_key}?expand=changelog"
        issue_data = jira.get(api_path)

        # Extract issue details
        issue_summary = issue_data.get("fields", {}).get("summary", "")
        issue_type = issue_data.get("fields", {}).get("issuetype", {}).get("name", "")
        issue_status = issue_data.get("fields", {}).get("status", {}).get("name", "")

        # Process changelog entries
        changelog_entries = []
        if "changelog" in issue_data and "histories" in issue_data["changelog"]:
            for history in issue_data["changelog"]["histories"]:
                timestamp = history.get("created")
                author = history.get("author", {}).get("displayName", "Unknown")

                for item in history.get("items", []):
                    field = item.get("field")

                    # Apply field filter if specified
                    if field_filter and field.lower() != field_filter.lower():
                        continue

                    from_value = item.get("fromString", "")
                    to_value = item.get("toString", "")

                    entry = {
                        "timestamp": timestamp,
                        "author": author,
                        "field": field,
                        "from": from_value,
                        "to": to_value,
                        "formatted": (
                            f"{field}: {from_value or '(empty)'} "
                            f"\u2192 {to_value or '(empty)'}"
                        ),
                    }
                    changelog_entries.append(entry)

        # Sort entries by timestamp (newest first)
        changelog_entries.sort(key=lambda x: x["timestamp"], reverse=True)

        return {
            "operation": "get_issue_changelog",
            "issue_key": issue_key,
            "issue_summary": issue_summary,
            "issue_type": issue_type,
            "issue_status": issue_status,
            "changelog_count": len(changelog_entries),
            "field_filter": field_filter,
            "changelog": changelog_entries,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve changelog for issue {issue_key}: {e}")


@mcp.tool()
def get_board_sprints(board_id: int) -> dict:
    """Get all sprints for a specific board.

    Args:
        board_id: Jira board ID (e.g., 92176)

    Returns:
        Dictionary containing list of sprints with their details
    """
    try:
        api_path = f"/rest/agile/1.0/board/{board_id}/sprint"
        response = jira.get(api_path)

        sprints = []
        if isinstance(response, dict):
            sprint_list = response.get("values", [])
            for sprint in sprint_list:
                sprint_info = {
                    "id": sprint.get("id"),
                    "name": sprint.get("name"),
                    "state": sprint.get("state"),
                    "startDate": sprint.get("startDate"),
                    "endDate": sprint.get("endDate"),
                    "completeDate": sprint.get("completeDate"),
                    "originBoardId": sprint.get("originBoardId"),
                }
                sprints.append(sprint_info)

        return {
            "operation": "get_board_sprints",
            "board_id": board_id,
            "sprint_count": len(sprints),
            "sprints": sprints,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve sprints for board {board_id}: {e}")


@mcp.tool()
def get_sprint_issues(
    project_key: str,
    sprint_name: str,
    board_id: Optional[int] = None,
    group_by_assignee: bool = True,
) -> dict:
    """Get issues for a specific sprint, optionally grouped by assignee.

    Perfect for daily standup preparation. Queries issues by project and sprint name,
    and can group results by assignee for easy team review.

    Args:
        project_key: Jira project key (e.g., 'RAGVIICAR')
        sprint_name: Sprint name (e.g., 'S2511.4_EXP')
        board_id: Optional board ID for additional context
        group_by_assignee: If True, groups issues by assignee (default: True)

    Returns:
        Dictionary with issues, optionally grouped by assignee, including:
        - issue_key, summary, status, assignee, priority, issue_type
        - issue_link for easy access
    """
    try:
        # Build JQL query
        jql = f'project = "{project_key}" AND sprint = "{sprint_name}"'

        # Execute JQL query
        response = jira.jql(jql)

        issues_list = []
        if isinstance(response, dict):
            raw_issues = response.get("issues", [])

            for issue in raw_issues:
                fields = issue.get("fields", {})
                assignee_info = fields.get("assignee", {})

                issue_info = {
                    "issue_key": issue.get("key"),
                    "summary": fields.get("summary"),
                    "status": fields.get("status", {}).get("name"),
                    "assignee": assignee_info.get("displayName")
                    if assignee_info
                    else "Unassigned",
                    "assignee_email": assignee_info.get("emailAddress")
                    if assignee_info
                    else None,
                    "priority": fields.get("priority", {}).get("name"),
                    "issue_type": fields.get("issuetype", {}).get("name"),
                    "issue_link": f"{TRACKER_URL}/browse/{issue.get('key')}",
                }
                issues_list.append(issue_info)

        result: Dict[str, Any] = {
            "operation": "get_sprint_issues",
            "project_key": project_key,
            "sprint_name": sprint_name,
            "board_id": board_id,
            "total_issues": len(issues_list),
        }

        if group_by_assignee:
            # Group issues by assignee
            grouped: Dict[str, list[dict[str, Any]]] = {}
            for issue in issues_list:
                assignee = issue["assignee"]
                if assignee not in grouped:
                    grouped[assignee] = []
                grouped[assignee].append(issue)

            result["grouped_by_assignee"] = grouped
            result["assignee_count"] = len(grouped)
        else:
            result["issues"] = issues_list

        return result

    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve sprint issues for {project_key}/{sprint_name}: {e}"
        )


@mcp.tool()
def bulk_add_comments(issue_comments: dict[str, str]) -> dict:
    """Add comments to multiple issues at once.

    Perfect for updating standup notes across multiple issues after daily standup.

    Args:
        issue_comments: Dictionary mapping issue keys to comment text.
                       Example: {"ABC-123": "Completed testing", "ABC-124": "In progress"}

    Returns:
        Dictionary with:
        - total: Total number of issues processed
        - successful: List of successfully commented issues
        - failed: List of failed comment additions with error messages
        - summary: Success/failure counts
    """
    if not issue_comments:
        raise ValueError("issue_comments dictionary cannot be empty")

    successful = []
    failed = []

    for issue_key, comment_text in issue_comments.items():
        if not comment_text or not comment_text.strip():
            failed.append(
                {
                    "issue": issue_key,
                    "error": "Comment text cannot be empty",
                    "status": "invalid_input",
                }
            )
            continue

        try:
            # Add comment to issue
            resp = jira.issue_add_comment(issue_key, comment_text)

            successful.append(
                {
                    "issue": issue_key,
                    "comment_length": len(comment_text),
                    "comment_id": resp.get("id") if isinstance(resp, dict) else None,
                    "created": resp.get("created") if isinstance(resp, dict) else None,
                }
            )

        except Exception as e:
            failed.append(
                {
                    "issue": issue_key,
                    "error": str(e),
                    "status": "comment_failed",
                }
            )

    return {
        "operation": "bulk_add_comments",
        "total": len(issue_comments),
        "successful_count": len(successful),
        "failed_count": len(failed),
        "successful": successful,
        "failed": failed,
        "summary": {
            "success_rate": (
                f"{len(successful)}/{len(issue_comments)}"
                f" ({len(successful) * 100 // len(issue_comments)}%)"
                if issue_comments
                else "0/0"
            ),
        },
    }


@mcp.tool()
def add_web_link_to_issue(
    issue_key: str,
    url: str,
    title: str,
    relationship: str | None = None,
) -> dict:
    """Add a collaborative web link (e.g., Doors requirement URL) to a Jira issue.

    This function creates a remote link from a Jira issue to an external resource,
    commonly used to link Stories to Doors requirements for traceability.

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        url: The URL to link (e.g., Doors requirement URL)
        title: Display title for the link (e.g., 'Doors Requirement: REQ-001')
        relationship: Optional relationship description (e.g., 'implemented by')

    Returns:
        Dictionary containing the created link details
    """
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/remotelink"

        payload: Dict[str, Any] = {
            "object": {
                "url": url,
                "title": title,
            }
        }

        if relationship:
            payload["relationship"] = relationship

        response = jira.post(api_path, data=payload)

        return {
            "operation": "add_web_link_to_issue",
            "issue": issue_key,
            "url": url,
            "title": title,
            "relationship": relationship,
            "link_id": response.get("id") if isinstance(response, dict) else None,
            "created": True,
            "response": response,
        }

    except Exception as e:
        raise RuntimeError(f"Failed to add web link to issue {issue_key}: {e}")


@mcp.tool()
def get_issue_web_links(issue_key: str) -> dict:
    """Get all web links (remote links) from a Jira issue.

    This includes collaborative links such as Doors requirements, wiki pages,
    and other external resources linked to the issue.

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')

    Returns:
        Dictionary containing all web links for the issue
    """
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/remotelink"
        response = jira.get(api_path)

        web_links = []
        if isinstance(response, list):
            for link in response:
                if isinstance(link, dict):
                    link_object = link.get("object", {})
                    web_links.append(
                        {
                            "id": link.get("id"),
                            "url": link_object.get("url", ""),
                            "title": link_object.get("title", ""),
                            "relationship": link.get("relationship"),
                            "icon_url": link_object.get("icon", {}).get("url16x16"),
                            "status": link_object.get("status", {}),
                        }
                    )

        return {
            "operation": "get_issue_web_links",
            "issue": issue_key,
            "web_link_count": len(web_links),
            "web_links": web_links,
        }

    except Exception as e:
        raise RuntimeError(f"Failed to get web links for issue {issue_key}: {e}")


@mcp.tool()
def remove_web_link(
    issue_key: str,
    link_id: str,
) -> dict:
    """Remove a web link (remote link) from a Jira issue.

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        link_id: ID of the remote link to remove

    Returns:
        Dictionary containing deletion status
    """
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/remotelink/{link_id}"
        jira.delete(api_path)

        return {
            "operation": "remove_web_link",
            "issue": issue_key,
            "link_id": link_id,
            "deleted": True,
            "status": "success",
        }

    except Exception as e:
        raise RuntimeError(
            f"Failed to remove web link {link_id} from issue {issue_key}: {e}"
        )


@mcp.tool()
def create_collaboration_link(
    issue_key: str,
    url: str,
    title: str,
    link_type: str = "TRACKS_REQUIREMENT",
    icon_url: str | None = None,
) -> dict:
    """Create a collaboration link to a Doors requirement or external resource.

    This creates the recommended "Collaboration Link" type shown in Jira's UI,
    supporting specific relationship types for requirements traceability.

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        url: URL of the Doors requirement or external resource
        title: Display title for the link (e.g., 'REQ-SYS-001: User Authentication')
        link_type: Type of collaboration link. Options:
                   - 'TRACKS_REQUIREMENT' (default): This issue tracks a requirement
                   - 'IMPLEMENTS_REQUIREMENT': This issue implements a requirement
                   - 'RELATES_TO': General relationship
        icon_url: Optional custom icon URL for the link

    Returns:
        Dictionary containing the created collaboration link details

    Example:
        create_collaboration_link(
            issue_key="PROJ-123",
            url="https://doors.company.com/req/REQ-SYS-001",
            title="REQ-SYS-001: User Authentication",
            link_type="IMPLEMENTS_REQUIREMENT"
        )
    """
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/remotelink"

        # Build the payload for collaboration link
        payload: Dict[str, Any] = {
            "globalId": f"applinks={url}",  # Unique identifier
            "application": {
                "type": "com.atlassian.jira.plugin.system.issuetabpanels:web-links",
                "name": "Collaboration Link",
            },
            "relationship": link_type,  # This sets the link type
            "object": {
                "url": url,
                "title": title,
            },
        }

        # Add custom icon if provided
        if icon_url:
            payload["object"]["icon"] = {"url16x16": icon_url, "title": "Requirement"}
        else:
            # Default Doors/Requirements icon
            payload["object"]["icon"] = {
                "url16x16": "https://docs.atlassian.com/aui/latest/docs/images/icons/icon-requirement-16.png",
                "title": "Requirement",
            }

        response = jira.post(api_path, data=payload)

        return {
            "operation": "create_collaboration_link",
            "issue": issue_key,
            "url": url,
            "title": title,
            "link_type": link_type,
            "link_id": response.get("id") if isinstance(response, dict) else None,
            "created": True,
            "issue_link": f"{TRACKER_URL}/browse/{issue_key}",
            "response": response,
        }

    except Exception as e:
        raise RuntimeError(
            f"Failed to create collaboration link for issue {issue_key}: {e}"
        )


@mcp.tool()
def get_doors_requirements(
    issue_key: str,
    link_type: str | None = None,
    url_pattern: str | None = None,
) -> dict:
    """Get all Doors requirement links attached to a Jira issue as collaboration links.

    This retrieves collaborative links filtered by link type and/or URL pattern,
    specifically designed for Doors requirements traceability.

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        link_type: Filter by specific link type. Options:
                   - 'TRACKS_REQUIREMENT'
                   - 'IMPLEMENTS_REQUIREMENT'
                   - 'RELATES_TO'
                   - 'VERIFIES'
                   - 'DERIVES_FROM'
                   - None (default): Returns all types
        url_pattern: Filter by URL pattern (e.g., 'doors', 'requirements.company.com')
                     Case-insensitive substring match

    Returns:
        Dictionary containing:
        - issue: The issue key
        - total_links: Total number of Doors requirements found
        - doors_requirements: List of requirement links with details
        - grouped_by_type: Requirements grouped by link type

    Example:
        # Get all requirements that this issue implements
        get_doors_requirements("PROJ-123", link_type="IMPLEMENTS_REQUIREMENT")

        # Get all Doors links regardless of type
        get_doors_requirements("PROJ-123", url_pattern="doors")
    """
    try:
        api_path = f"/rest/api/2/issue/{issue_key}/remotelink"
        response = jira.get(api_path)

        doors_requirements = []
        grouped_by_type: Dict[str, list] = {}

        if isinstance(response, list):
            for link in response:
                if isinstance(link, dict):
                    link_object = link.get("object", {})
                    url = link_object.get("url", "")
                    title = link_object.get("title", "")
                    relationship = link.get("relationship", "")

                    # Apply filters
                    # Filter by link type if specified
                    if link_type and relationship != link_type:
                        continue

                    # Filter by URL pattern if specified
                    if url_pattern and url_pattern.lower() not in url.lower():
                        continue

                    # Check if it looks like a Doors/Requirements link
                    is_doors = any(
                        pattern in url.lower() or pattern in title.lower()
                        for pattern in [
                            "doors",
                            "requirement",
                            "req-",
                            "rm.",
                            "reqif",
                            "/rm/",
                            "alm",
                            "dwa/rm",
                        ]
                    )

                    if (
                        is_doors or url_pattern
                    ):  # Include if matches pattern even if not typical Doors URL
                        req_info = {
                            "id": link.get("id"),
                            "url": url,
                            "title": title,
                            "link_type": relationship,
                            "icon_url": link_object.get("icon", {}).get("url16x16"),
                            "status": link_object.get("status", {}),
                        }

                        doors_requirements.append(req_info)

                        # Group by type
                        if relationship not in grouped_by_type:
                            grouped_by_type[relationship] = []
                        grouped_by_type[relationship].append(req_info)

        # Get issue details
        issue_data = jira.issue(issue_key)
        issue_summary = (
            issue_data.get("fields", {}).get("summary", "")
            if isinstance(issue_data, dict)
            else ""
        )

        return {
            "operation": "get_doors_requirements",
            "issue": issue_key,
            "issue_summary": issue_summary,
            "issue_link": f"{TRACKER_URL}/browse/{issue_key}",
            "total_links": len(doors_requirements),
            "filter_applied": {
                "link_type": link_type,
                "url_pattern": url_pattern,
            },
            "doors_requirements": doors_requirements,
            "grouped_by_type": grouped_by_type,
            "link_type_counts": {
                link_type: len(links) for link_type, links in grouped_by_type.items()
            },
        }

    except Exception as e:
        raise RuntimeError(
            f"Failed to get Doors requirements for issue {issue_key}: {e}"
        )


@mcp.tool()
def bulk_add_collaboration_links(
    links: list[dict[str, str]],
) -> dict:
    """Add collaboration links to multiple issues at once.

    Perfect for bulk linking Doors requirements to multiple Jira issues.

    Args:
        links: List of dictionaries, each containing:
               - issue_key: Jira issue key (required)
               - url: Doors requirement URL (required)
               - title: Display title (required)
               - link_type: Type of link (optional, defaults to 'TRACKS_REQUIREMENT')

    Example:
        bulk_add_collaboration_links([
            {
                "issue_key": "PROJ-123",
                "url": "https://doors.company.com/req/REQ-001",
                "title": "REQ-001: Authentication",
                "link_type": "IMPLEMENTS_REQUIREMENT"
            },
            {
                "issue_key": "PROJ-124",
                "url": "https://doors.company.com/req/REQ-002",
                "title": "REQ-002: Authorization",
                "link_type": "IMPLEMENTS_REQUIREMENT"
            }
        ])

    Returns:
        Dictionary with:
        - total: Total number of links to create
        - successful: List of successfully created links
        - failed: List of failed link creations with errors
        - summary: Success/failure statistics
    """
    if not links:
        raise ValueError("links list cannot be empty")

    successful = []
    failed = []

    for link_info in links:
        # Validate required fields
        issue_key = link_info.get("issue_key")
        url = link_info.get("url")
        title = link_info.get("title")

        if not issue_key or not url or not title:
            failed.append(
                {
                    "link_info": link_info,
                    "error": "Missing required fields: issue_key, url, and title are required",
                    "status": "invalid_input",
                }
            )
            continue

        link_type = link_info.get("link_type", "TRACKS_REQUIREMENT")
        icon_url = link_info.get("icon_url")

        try:
            api_path = f"/rest/api/2/issue/{issue_key}/remotelink"

            payload: Dict[str, Any] = {
                "globalId": f"applinks={url}",
                "application": {
                    "type": "com.atlassian.jira.plugin.system.issuetabpanels:web-links",
                    "name": "Collaboration Link",
                },
                "relationship": link_type,
                "object": {
                    "url": url,
                    "title": title,
                },
            }

            if icon_url:
                payload["object"]["icon"] = {
                    "url16x16": icon_url,
                    "title": "Requirement",
                }
            else:
                payload["object"]["icon"] = {
                    "url16x16": "https://docs.atlassian.com/aui/latest/docs/images/icons/icon-requirement-16.png",
                    "title": "Requirement",
                }

            response = jira.post(api_path, data=payload)

            successful.append(
                {
                    "issue": issue_key,
                    "url": url,
                    "title": title,
                    "link_type": link_type,
                    "link_id": response.get("id")
                    if isinstance(response, dict)
                    else None,
                }
            )

        except Exception as e:
            failed.append(
                {
                    "issue": issue_key,
                    "url": url,
                    "title": title,
                    "error": str(e),
                    "status": "creation_failed",
                }
            )

    return {
        "operation": "bulk_add_collaboration_links",
        "total": len(links),
        "successful_count": len(successful),
        "failed_count": len(failed),
        "successful": successful,
        "failed": failed,
        "summary": {
            "success_rate": (
                f"{len(successful)}/{len(links)}"
                f" ({len(successful) * 100 // len(links)}%)"
                if links
                else "0/0"
            ),
        },
    }


@mcp.tool()
def update_collaboration_link(
    issue_key: str,
    link_id: str,
    url: str | None = None,
    title: str | None = None,
    link_type: str | None = None,
) -> dict:
    """Update an existing collaboration link.

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        link_id: ID of the remote link to update
        url: New URL (optional)
        title: New title (optional)
        link_type: New link type (optional). Options:
                   - 'TRACKS_REQUIREMENT'
                   - 'IMPLEMENTS_REQUIREMENT'
                   - 'RELATES_TO'

    Returns:
        Dictionary containing update status
    """
    try:
        # First, get the existing link
        get_api_path = f"/rest/api/2/issue/{issue_key}/remotelink/{link_id}"
        existing_link = jira.get(get_api_path)

        if not isinstance(existing_link, dict):
            raise ValueError(f"Link {link_id} not found")

        # Build updated payload
        existing_object = existing_link.get("object", {})

        payload: Dict[str, Any] = {
            "globalId": existing_link.get(
                "globalId", f"applinks={url or existing_object.get('url')}"
            ),
            "application": existing_link.get(
                "application",
                {
                    "type": "com.atlassian.jira.plugin.system.issuetabpanels:web-links",
                    "name": "Collaboration Link",
                },
            ),
            "relationship": link_type
            or existing_link.get("relationship", "TRACKS_REQUIREMENT"),
            "object": {
                "url": url or existing_object.get("url"),
                "title": title or existing_object.get("title"),
                "icon": existing_object.get(
                    "icon",
                    {
                        "url16x16": "https://docs.atlassian.com/aui/latest/docs/images/icons/icon-requirement-16.png",
                        "title": "Requirement",
                    },
                ),
            },
        }

        # Update using PUT
        update_api_path = f"/rest/api/2/issue/{issue_key}/remotelink/{link_id}"
        response = jira.put(update_api_path, data=payload)

        return {
            "operation": "update_collaboration_link",
            "issue": issue_key,
            "link_id": link_id,
            "updated_fields": {
                "url": url,
                "title": title,
                "link_type": link_type,
            },
            "updated": True,
            "response": response,
        }

    except Exception as e:
        raise RuntimeError(
            f"Failed to update collaboration link {link_id} for issue {issue_key}: {e}"
        )


@mcp.tool()
def get_collaboration_link_types(project_key: str, sample_size: int = 50) -> dict:
    """Get actual collaboration link types used in your Jira tracker.

    Scans issues in the specified project to discover what collaboration/remote link
    types are actually being used for linking to external requirements (e.g., Doors).
    Also fetches internal issue link types available in Jira.

    Args:
        project_key: Jira project key (e.g., 'ADDAPMT')
        sample_size: Number of recent issues to scan for collaboration links (default: 50, max: 200)

    Returns:
        Dictionary containing:
        - issue_link_types: Internal link types for linking Jira issues together
        - collaboration_link_types_in_use: Actual collaboration link types found in the tracker
        - sample_info: Information about how many issues were scanned
    """
    try:
        # 1. Fetch internal issue link types from Jira
        link_types_response = jira.get("/rest/api/2/issueLinkType")

        issue_link_types = []
        if isinstance(link_types_response, dict):
            raw_types = link_types_response.get("issueLinkTypes", [])
            for link_type in raw_types:
                if isinstance(link_type, dict):
                    issue_link_types.append(
                        {
                            "id": link_type.get("id"),
                            "name": link_type.get("name"),
                            "inward": link_type.get("inward"),
                            "outward": link_type.get("outward"),
                            "description": f"Inward: {link_type.get('inward')} | Outward: {link_type.get('outward')}",
                        }
                    )

        # 2. Scan project issues to find actual collaboration link types in use
        sample_size = min(max(sample_size, 10), 200)  # Clamp between 10 and 200

        jql = f'project = "{project_key}" ORDER BY created DESC'
        response = jira.jql(jql, limit=sample_size)

        collaboration_link_stats: Dict[str, Dict[str, Any]] = {}
        issues_scanned = 0
        issues_with_collab_links = 0
        total_collab_links = 0

        if isinstance(response, dict):
            raw_issues = response.get("issues", [])

            for issue in raw_issues:
                if not isinstance(issue, dict):
                    continue

                issue_key = issue.get("key")
                issues_scanned += 1

                try:
                    # Fetch remote/collaboration links for this issue
                    api_path = f"/rest/api/2/issue/{issue_key}/remotelink"
                    remote_links = jira.get(api_path)

                    if isinstance(remote_links, list) and remote_links:
                        issues_with_collab_links += 1

                        for link in remote_links:
                            if isinstance(link, dict):
                                relationship = link.get("relationship", "")
                                if relationship:
                                    total_collab_links += 1

                                    if relationship not in collaboration_link_stats:
                                        collaboration_link_stats[relationship] = {
                                            "link_type": relationship,
                                            "usage_count": 0,
                                            "example_issues": [],
                                            "example_urls": [],
                                        }

                                    collaboration_link_stats[relationship][
                                        "usage_count"
                                    ] += 1

                                    # Collect examples (max 3 per type)
                                    if (
                                        len(
                                            collaboration_link_stats[relationship][
                                                "example_issues"
                                            ]
                                        )
                                        < 3
                                    ):
                                        collaboration_link_stats[relationship][
                                            "example_issues"
                                        ].append(issue_key)

                                    link_url = link.get("object", {}).get("url", "")
                                    if (
                                        link_url
                                        and len(
                                            collaboration_link_stats[relationship][
                                                "example_urls"
                                            ]
                                        )
                                        < 2
                                    ):
                                        collaboration_link_stats[relationship][
                                            "example_urls"
                                        ].append(link_url)

                except Exception:
                    continue  # Skip issues that error out

        # Sort collaboration link types by usage
        collaboration_link_types_in_use = sorted(
            collaboration_link_stats.values(),
            key=lambda x: x["usage_count"],
            reverse=True,
        )

        return {
            "operation": "get_collaboration_link_types",
            "project": project_key,
            "issue_link_types": {
                "description": "Internal link types for linking Jira issues to each other",
                "count": len(issue_link_types),
                "types": issue_link_types,
            },
            "collaboration_link_types_in_use": {
                "description": (
                    "Collaboration/remote link types actually used in this project"
                ),
                "count": len(collaboration_link_types_in_use),
                "types": collaboration_link_types_in_use,
                "note": (
                    "These are the actual link types found by scanning issues. "
                    "You can use any of these or create new ones."
                ),
            },
            "sample_info": {
                "issues_scanned": issues_scanned,
                "issues_with_collaboration_links": issues_with_collab_links,
                "total_collaboration_links_found": total_collab_links,
                "unique_link_types_found": len(collaboration_link_stats),
            },
            "usage_guide": {
                "internal_links": (
                    "Use issue_link_types for linking between Jira issues "
                    "(e.g., PROJ-1 blocks PROJ-2)"
                ),
                "collaboration_links": (
                    "Use any of the collaboration_link_types_in_use found above, "
                    "or create a new custom type"
                ),
            },
        }

    except Exception as e:
        return {
            "operation": "get_collaboration_link_types",
            "error": str(e),
            "message": "Failed to fetch link types from Jira instance",
        }


@mcp.tool()
def generate_requirements_traceability_matrix(
    project_key: str,
    issue_type: str | None = None,
    link_type: str | None = None,
    format: str = "summary",
) -> dict:
    """Generate a requirements traceability matrix showing relationships between
    Jira issues and Doors requirements.

    This tool creates a comprehensive view of how issues map to requirements,
    useful for compliance, auditing, and project management.

    Args:
        project_key: Jira project key (e.g., 'PJAGENAI')
        issue_type: Filter by issue type (e.g., 'Story', 'Task'). Optional.
        link_type: Filter by collaboration link type (case-insensitive, e.g., 'implements requirement'). Optional.
        format: Output format:
                - 'summary': High-level statistics (default)
                - 'detailed': Full matrix with all issues and requirements
                - 'gaps': Only show issues without requirements

    Returns:
        Dictionary containing traceability matrix with:
        - statistics: Coverage metrics
        - matrix: Issue-to-requirement mappings
        - gaps: Issues missing requirement links (if format='gaps' or 'detailed')
        - recommendations: Suggestions for improving traceability
    """
    try:
        # Build JQL
        jql = f'project = "{project_key}"'
        if issue_type:
            jql += f' AND issuetype = "{issue_type}"'

        response = jira.jql(jql)

        matrix = []
        issues_with_reqs = 0
        issues_without_reqs = 0
        total_req_links = 0
        link_type_distribution: Dict[str, int] = {}

        if isinstance(response, dict):
            raw_issues = response.get("issues", [])

            for issue in raw_issues:
                if not isinstance(issue, dict):
                    continue

                issue_key = issue.get("key")
                fields = issue.get("fields", {})

                # Get Doors requirements for this issue
                try:
                    api_path = f"/rest/api/2/issue/{issue_key}/remotelink"
                    remote_links = jira.get(api_path)

                    doors_reqs = []
                    if isinstance(remote_links, list):
                        for link in remote_links:
                            if isinstance(link, dict):
                                link_object = link.get("object", {})
                                url = link_object.get("url", "")
                                title = link_object.get("title", "")
                                relationship = link.get("relationship", "")

                                # Check if it's a Doors link
                                is_doors = any(
                                    pattern in url.lower() or pattern in title.lower()
                                    for pattern in [
                                        "doors",
                                        "requirement",
                                        "req-",
                                        "rm.",
                                        "/rm/",
                                        "alm",
                                        "dwa/rm",
                                    ]
                                )

                                # Apply link type filter if specified
                                if link_type and relationship != link_type:
                                    continue

                                if is_doors:
                                    doors_reqs.append(
                                        {
                                            "url": url,
                                            "title": title,
                                            "link_type": relationship,
                                        }
                                    )

                                    # Track link type distribution
                                    link_type_distribution[relationship] = (
                                        link_type_distribution.get(relationship, 0) + 1
                                    )

                    if doors_reqs:
                        issues_with_reqs += 1
                        total_req_links += len(doors_reqs)
                    else:
                        issues_without_reqs += 1

                    matrix_entry = {
                        "issue_key": issue_key,
                        "summary": fields.get("summary", ""),
                        "issue_type": fields.get("issuetype", {}).get("name", ""),
                        "status": fields.get("status", {}).get("name", ""),
                        "assignee": fields.get("assignee", {}).get("displayName")
                        if fields.get("assignee")
                        else "Unassigned",
                        "requirements_count": len(doors_reqs),
                        "requirements": doors_reqs,
                        "issue_link": f"{TRACKER_URL}/browse/{issue_key}",
                    }

                    # Add to matrix based on format
                    if format == "gaps" and len(doors_reqs) == 0:
                        matrix.append(matrix_entry)
                    elif format in ["summary", "detailed"]:
                        matrix.append(matrix_entry)

                except Exception:
                    # Skip this issue if we can't get links
                    continue

        total_issues = issues_with_reqs + issues_without_reqs
        coverage_pct = (
            (issues_with_reqs * 100 // total_issues) if total_issues > 0 else 0
        )

        result: Dict[str, Any] = {
            "operation": "generate_requirements_traceability_matrix",
            "project": project_key,
            "filters": {
                "issue_type": issue_type,
                "link_type": link_type,
            },
            "statistics": {
                "total_issues": total_issues,
                "issues_with_requirements": issues_with_reqs,
                "issues_without_requirements": issues_without_reqs,
                "total_requirement_links": total_req_links,
                "coverage_percentage": coverage_pct,
                "avg_requirements_per_issue": (total_req_links / issues_with_reqs)
                if issues_with_reqs > 0
                else 0,
                "link_type_distribution": link_type_distribution,
            },
            "format": format,
        }

        # Add matrix data based on format
        if format == "summary":
            result["summary"] = {
                "top_linked_issues": sorted(
                    [entry for entry in matrix if entry["requirements_count"] > 0],
                    key=lambda x: x["requirements_count"],
                    reverse=True,
                )[:10],
                "gaps_count": issues_without_reqs,
            }
        elif format == "detailed":
            result["matrix"] = matrix
            gaps: list[dict[str, Any]] = [
                entry for entry in matrix if entry["requirements_count"] == 0
            ]
            result["gaps"] = gaps
        elif format == "gaps":
            result["gaps"] = matrix

        # Add recommendations
        recommendations = []
        if coverage_pct < 50:
            recommendations.append(
                "Coverage is below 50%. Consider adding requirement links to unlinked issues."
            )
        if issues_without_reqs > 0:
            recommendations.append(
                f"{issues_without_reqs} issues have no requirement links. Use bulk_add_collaboration_links to add them."
            )
        # Normalize link type keys to lowercase for case-insensitive comparison
        normalized_link_types = {lt.lower() for lt in link_type_distribution.keys()}
        if (
            "tracks requirement" not in normalized_link_types
            and "implements requirement" not in normalized_link_types
        ):
            recommendations.append(
                "Consider using 'tracks requirement' or 'implements requirement' link types for clearer traceability."
            )

        result["recommendations"] = recommendations

        return result

    except Exception as e:
        raise RuntimeError(
            f"Failed to generate requirements traceability matrix for {project_key}: {e}"
        )


@mcp.tool()
def list_issues_with_doors_requirements(
    project_key: str,
    issue_type: str | None = None,
    link_type: str | None = None,
    status: str | None = None,
    max_issues: int = 100,
) -> dict:
    """List all Jira issues that have Doors requirement links.

    This tool scans issues in a project and identifies which ones have
    Doors requirement links attached as remote/collaboration links.

    OPTIMIZED for performance: Handles 2000-4000 issues in under 30 seconds
    using parallel processing with up to 100 concurrent workers.

    Args:
        project_key: Jira project key (e.g., 'ADDAPMT')
        issue_type: Filter by issue type (e.g., 'Story', 'Task'). Optional.
        link_type: Filter by collaboration link type (case-insensitive, e.g., 'implements requirement'). Optional.
        status: Filter by issue status (e.g., 'Open', 'In Progress'). Optional.
        max_issues: Maximum number of issues to scan (default: 100, max: 10000)

    Returns:
        Dictionary containing:
        - issues_with_doors: List of issues that have Doors requirement links
        - statistics: Summary statistics about the scan
        - filters_applied: What filters were used
        - performance_metrics: Execution time and throughput
    """
    import time

    start_time = time.time()

    try:
        max_issues = min(max(max_issues, 10), 10000)  # Increased max to 10000

        # Build JQL query
        jql = f'project = "{project_key}"'
        if issue_type:
            jql += f' AND issuetype = "{issue_type}"'
        if status:
            jql += f' AND status = "{status}"'
        jql += " ORDER BY created DESC"

        response = jira.jql(jql, limit=max_issues)

        issues_with_doors = []
        total_doors_links = 0
        link_type_distribution: Dict[str, int] = {}
        issues_scanned = 0
        failed_fetches = 0

        if isinstance(response, dict):
            raw_issues = response.get("issues", [])

            # Thread-safe collections for aggregating results
            from threading import Lock

            results_lock = Lock()

            # Helper function to process a single issue - OPTIMIZED
            def process_issue(issue):
                nonlocal issues_scanned, failed_fetches

                if not isinstance(issue, dict):
                    return None

                issue_key = issue.get("key")
                fields = issue.get("fields", {})

                try:
                    # Get remote links for this issue
                    api_path = f"/rest/api/2/issue/{issue_key}/remotelink"
                    remote_links = jira.get(api_path)

                    doors_reqs = []
                    if isinstance(remote_links, list):
                        for link in remote_links:
                            if isinstance(link, dict):
                                link_object = link.get("object", {})
                                url = link_object.get("url", "")
                                title = link_object.get("title", "")
                                relationship = link.get("relationship", "")

                                # Check if it's a Doors link - OPTIMIZED: early exit
                                is_doors = any(
                                    pattern in url.lower() or pattern in title.lower()
                                    for pattern in [
                                        "doors",
                                        "requirement",
                                        "req-",
                                        "rm.",
                                        "reqif",
                                        "/rm/",
                                        "alm",
                                        "dwa/rm",
                                    ]
                                )

                                # Apply link type filter if specified (case-insensitive comparison)
                                if (
                                    link_type
                                    and relationship.lower() != link_type.lower()
                                ):
                                    continue

                                if is_doors:
                                    doors_reqs.append(
                                        {
                                            "id": link.get("id"),
                                            "url": url,
                                            "title": title,
                                            "link_type": relationship,
                                        }
                                    )

                    # If issue has Doors requirements, return the issue data
                    if doors_reqs:
                        return {
                            "issue_key": issue_key,
                            "summary": fields.get("summary", ""),
                            "status": fields.get("status", {}).get("name", ""),
                            "issue_type": fields.get("issuetype", {}).get("name", ""),
                            "assignee": fields.get("assignee", {}).get("displayName")
                            if fields.get("assignee")
                            else "Unassigned",
                            "doors_requirements_count": len(doors_reqs),
                            "doors_requirements": doors_reqs,
                            "issue_link": f"{TRACKER_URL}/browse/{issue_key}",
                            "link_type_dist": {
                                req["link_type"]: 1 for req in doors_reqs
                            },
                        }

                except Exception:
                    with results_lock:
                        failed_fetches += 1
                    return None

                return None

            # OPTIMIZED: Dynamically scale parallel workers with issue count
            # Use between 10 and 100 workers; larger workloads get more workers for better throughput
            max_workers = min(100, max(10, len(raw_issues) // 10))

            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all tasks at once for maximum parallelism
                future_to_issue = {
                    executor.submit(process_issue, issue): issue for issue in raw_issues
                }

                # Collect results as they complete
                for future in as_completed(future_to_issue):
                    with results_lock:
                        issues_scanned += 1

                    result = future.result()

                    if result:
                        with results_lock:
                            issues_with_doors.append(result)
                            total_doors_links += result["doors_requirements_count"]

                            # Aggregate link type distribution
                            for link_type_key in result.get("link_type_dist", {}):
                                link_type_distribution[link_type_key] = (
                                    link_type_distribution.get(link_type_key, 0) + 1
                                )

        end_time = time.time()
        execution_time = end_time - start_time
        throughput = issues_scanned / execution_time if execution_time > 0 else 0

        return {
            "operation": "list_issues_with_doors_requirements",
            "project": project_key,
            "filters_applied": {
                "issue_type": issue_type,
                "link_type": link_type,
                "status": status,
                "max_issues": max_issues,
            },
            "statistics": {
                "issues_scanned": issues_scanned,
                "issues_with_doors_requirements": len(issues_with_doors),
                "total_doors_requirement_links": total_doors_links,
                "link_type_distribution": link_type_distribution,
                "coverage_percentage": (len(issues_with_doors) * 100 // issues_scanned)
                if issues_scanned > 0
                else 0,
                "failed_fetches": failed_fetches,
            },
            "performance_metrics": {
                "execution_time_seconds": round(execution_time, 2),
                "throughput_issues_per_second": round(throughput, 2),
                "parallel_workers_used": max_workers,
                "avg_time_per_issue_ms": round(
                    (execution_time * 1000) / issues_scanned, 2
                )
                if issues_scanned > 0
                else 0,
            },
            "issues_with_doors": issues_with_doors,
        }

    except Exception as e:
        raise RuntimeError(
            f"Failed to list issues with Doors requirements for {project_key}: {e}"
        )


@mcp.tool()
def bulk_transition_issues(
    issue_keys: list[str], transition: str, comment: str | None = None
) -> dict:
    """Perform a workflow transition on multiple issues at once.

    Args:
        issue_keys: List of Jira issue keys (e.g. ["ABC-123", "ABC-124", "ABC-125"]).
        transition: Transition id or name (case-insensitive) to apply to all issues.
        comment: Optional comment to add when transitioning (applied to all issues).

    Returns:
        Dictionary with:
        - total: Total number of issues processed
        - successful: List of successfully transitioned issues with their new status
        - failed: List of failed transitions with error messages
        - summary: Success/failure counts
    """
    if not issue_keys:
        raise ValueError("issue_keys list cannot be empty")

    if not transition:
        raise ValueError("transition parameter is required")

    successful = []
    failed = []

    for issue_key in issue_keys:
        try:
            # Get available transitions for this issue
            api_path = f"/rest/api/2/issue/{issue_key}/transitions"
            transitions_raw: list[dict[str, Any]] = []

            try:
                data = jira.get(api_path)
                if isinstance(data, dict):
                    transitions_raw = data.get("transitions", []) or []
            except Exception as e:
                failed.append(
                    {
                        "issue": issue_key,
                        "error": f"Unable to retrieve transitions: {e}",
                        "status": "failed_to_get_transitions",
                    }
                )
                continue

            # Build transition mapping
            available = {
                t.get("id"): t.get("name")
                for t in transitions_raw
                if isinstance(t, dict)
            }
            name_index = {
                (t.get("name") or "").lower(): t.get("id")
                for t in transitions_raw
                if isinstance(t, dict)
            }

            # Find the target transition ID
            target_id = (
                transition
                if transition in available
                else name_index.get(transition.lower())
            )

            if not target_id:
                failed_entry: dict[str, Any] = {
                    "issue": issue_key,
                    "error": f"Transition '{transition}' not found",
                    "available_transitions": {
                        str(k): str(v) for k, v in available.items()
                    },
                    "status": "transition_not_found",
                }
                failed.append(failed_entry)
                continue

            # Prepare the payload
            payload: dict[str, Any] = {"transition": {"id": target_id}}

            # Add comment if provided
            if comment:
                payload["update"] = {"comment": [{"add": {"body": comment}}]}

            # Execute the transition
            try:
                jira.post(api_path, data=payload)
            except Exception as e:
                failed.append(
                    {
                        "issue": issue_key,
                        "error": f"Transition execution failed: {e}",
                        "status": "execution_failed",
                    }
                )
                continue

            # Get the new status
            new_status = None
            try:
                issue_after = jira.issue(issue_key)
                if isinstance(issue_after, dict):
                    new_status = (
                        issue_after.get("fields", {}).get("status", {}).get("name")
                    )
            except Exception:
                # Non-fatal; leave new_status as None
                pass

            successful.append(
                {
                    "issue": issue_key,
                    "transition_id": target_id,
                    "transition_name": available.get(target_id),
                    "new_status": new_status,
                    "comment_added": comment is not None,
                }
            )

        except Exception as e:
            failed.append(
                {
                    "issue": issue_key,
                    "error": f"Unexpected error: {e}",
                    "status": "unexpected_error",
                }
            )

    return {
        "operation": "bulk_transition",
        "total": len(issue_keys),
        "successful_count": len(successful),
        "failed_count": len(failed),
        "successful": successful,
        "failed": failed,
        "summary": {
            "success_rate": (
                f"{len(successful)}/{len(issue_keys)}"
                f" ({len(successful) * 100 // len(issue_keys)}%)"
                if issue_keys
                else "0/0"
            ),
            "transition_requested": transition,
            "comment_added": comment is not None,
        },
    }


@mcp.tool()
def analyze_custom_fields_for_requirements(
    project_key: str,
    issue_type: str = "Story",
    sample_size: int = 20,
) -> dict:
    """Analyze custom fields to find where DOORS requirements are stored.

    This tool examines issues in a project to discover how requirements are actually
    linked - whether in descriptions, custom fields, or other locations.

    Args:
        project_key: Jira project key (e.g., 'RAGVIICAR')
        issue_type: Issue type to analyze (default: 'Story')
        sample_size: Number of issues to analyze (default: 20, max: 50)

    Returns:
        Dictionary with analysis of where requirements are stored
    """
    try:
        sample_size = min(max(sample_size, 5), 50)

        jql = f'project = "{project_key}" AND issuetype = "{issue_type}" ORDER BY created DESC'
        response = jira.jql(jql, limit=sample_size)

        if not isinstance(response, dict) or "issues" not in response:
            raise ValueError("Unexpected response from JQL query")

        issues = response.get("issues", [])

        # Analysis tracking
        custom_field_usage = {}
        issues_with_req_in_desc = []
        issues_with_req_in_custom: list[dict[str, Any]] = []
        requirement_patterns = [
            "doors",
            "DOORS",
            "requirement",
            "Requirement",
            "REQ-",
            "req-",
            "rm.",
            "reqif",
            "http://",
        ]

        custom_fields_with_req_content: Dict[str, list[dict[str, Any]]] = {}

        for issue in issues:
            key = issue.get("key")
            fields = issue.get("fields", {})

            # Check description
            description = fields.get("description", "")
            if description and isinstance(description, str):
                if any(pattern in description for pattern in requirement_patterns):
                    issues_with_req_in_desc.append(
                        {
                            "issue_key": key,
                            "summary": fields.get("summary", ""),
                            "description_snippet": description[:300],
                        }
                    )

            # Analyze custom fields
            for field_key, field_value in fields.items():
                if field_key.startswith("customfield_") and field_value is not None:
                    # Track usage
                    if field_key not in custom_field_usage:
                        custom_field_usage[field_key] = {
                            "count": 0,
                            "sample_values": [],
                        }
                    count_val = custom_field_usage[field_key]["count"]
                    custom_field_usage[field_key]["count"] = (
                        int(count_val) + 1 if isinstance(count_val, (int, float)) else 1
                    )

                    # Check for requirement patterns
                    str_value = str(field_value)
                    if any(pattern in str_value for pattern in requirement_patterns):
                        if field_key not in custom_fields_with_req_content:
                            custom_fields_with_req_content[field_key] = []

                        custom_fields_with_req_content[field_key].append(
                            {"issue_key": key, "value_snippet": str_value[:200]}
                        )

                        if key not in [
                            i["issue_key"] for i in issues_with_req_in_custom
                        ]:
                            issues_with_req_in_custom.append(
                                {
                                    "issue_key": key,
                                    "summary": fields.get("summary", ""),
                                    "custom_field": field_key,
                                }
                            )

                    # Store sample values for frequently used fields
                    samples = custom_field_usage[field_key]["sample_values"]
                    if isinstance(samples, list) and len(samples) < 2:
                        sample = str_value[:100] if len(str_value) > 100 else str_value
                        if sample not in samples:
                            samples.append(sample)

        # Sort custom fields by usage frequency
        frequently_used_fields = sorted(
            [
                (k, v["count"], v["sample_values"])
                for k, v in custom_field_usage.items()
            ],
            key=lambda x: int(x[1]) if isinstance(x[1], (int, float)) else 0,
            reverse=True,
        )[:20]

        return {
            "operation": "analyze_custom_fields_for_requirements",
            "project_key": project_key,
            "issue_type": issue_type,
            "issues_analyzed": len(issues),
            "total_issues_in_project": response.get("total", 0),
            "findings": {
                "issues_with_requirements_in_description": {
                    "count": len(issues_with_req_in_desc),
                    "percentage": f"{len(issues_with_req_in_desc) * 100 / len(issues):.1f}%"
                    if issues
                    else "0%",
                    "examples": issues_with_req_in_desc[:5],
                },
                "issues_with_requirements_in_custom_fields": {
                    "count": len(issues_with_req_in_custom),
                    "percentage": f"{len(issues_with_req_in_custom) * 100 / len(issues):.1f}%"
                    if issues
                    else "0%",
                    "examples": issues_with_req_in_custom[:5],
                },
                "custom_fields_with_requirement_content": custom_fields_with_req_content,
                "total_unique_custom_fields": len(custom_field_usage),
                "frequently_used_custom_fields": [
                    {
                        "field_id": field_id,
                        "usage_count": count,
                        "usage_percentage": (
                            f"{(int(count) if isinstance(count, (int, float)) else 0) * 100 / len(issues):.1f}%"
                            if issues
                            else "0%"
                        ),
                        "sample_values": samples,
                    }
                    for field_id, count, samples in frequently_used_fields
                ],
            },
            "recommendation": (
                "Requirements found in descriptions"
                if issues_with_req_in_desc
                else "Requirements found in custom fields"
                if issues_with_req_in_custom
                else "No clear DOORS requirement patterns found in sampled issues"
            ),
        }

    except Exception as e:
        raise RuntimeError(f"Failed to analyze custom fields: {e}")


@mcp.tool()
def set_issue_acceptance_criteria(
    issue_key: str,
    acceptance_criteria: str,
    custom_field_id: str,
    append: bool = False,
) -> dict:
    """Set or update acceptance criteria for a Jira issue.

    IMPORTANT: To find the acceptance criteria field ID:
    1. Call: issue_editable_fields(issue_key="YOUR-ISSUE")
    2. Look for field with "acceptance" and "criteria" in name
    3. Use that field ID here (e.g., customfield_16428)

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        acceptance_criteria: The acceptance criteria text to set
        custom_field_id: Acceptance criteria field ID (e.g., 'customfield_16428')
        append: If True, appends to existing; if False, replaces (default: False)

    Returns:
        { issue, operation, custom_field_id, appended, response }
    """
    if not acceptance_criteria.strip():
        raise ValueError("Acceptance criteria must be non-empty")

    try:
        issue_data = jira.issue(issue_key)
        current_value = issue_data.get("fields", {}).get(custom_field_id, "") or ""

        new_value = (
            f"{current_value}\n\n{acceptance_criteria}" if append and current_value 
            else acceptance_criteria
        )

        resp = jira.update_issue_field(issue_key, {custom_field_id: new_value})

        return {
            "issue": issue_key,
            "operation": "set_acceptance_criteria",
            "custom_field_id": custom_field_id,
            "appended": append and bool(current_value),
            "response": resp,
        }
    except Exception as e:
        raise RuntimeError(f"Failed to set acceptance criteria on {issue_key}: {e}")


@mcp.tool()
def get_issue_acceptance_criteria(
    issue_key: str,
    custom_field_id: str,
) -> dict:
    """Get acceptance criteria for a Jira issue.

    IMPORTANT: To find the acceptance criteria field ID:
    1. Call: issue_editable_fields(issue_key="YOUR-ISSUE")
    2. Look for field with "acceptance" and "criteria" in name
    3. Use that field ID here (e.g., customfield_16428)

    Args:
        issue_key: Jira issue key (e.g., 'ABC-123')
        custom_field_id: Acceptance criteria field ID (e.g., 'customfield_16428')

    Returns:
        { issue, acceptance_criteria, custom_field_id, found }
    """
    try:
        issue_data = jira.issue(issue_key)
        fields = issue_data.get("fields", {})
        ac_value = fields.get(custom_field_id)

        return {
            "issue": issue_key,
            "acceptance_criteria": ac_value,
            "custom_field_id": custom_field_id,
            "found": bool(ac_value and str(ac_value).strip()),
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get acceptance criteria for {issue_key}: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    transport, host, port = _get_mcp_init_vars()
    if transport == "stdio":
        mcp.run()
    else:
        mcp.run(transport=transport, transport_options={"host": host, "port": port})
