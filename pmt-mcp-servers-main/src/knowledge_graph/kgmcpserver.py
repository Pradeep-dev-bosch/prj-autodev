"""
Bug Knowledge Graph MCP Server

Stores and retrieves bug analysis records in a Stardog RDF knowledge graph.
Each record captures: JIRA issue, root cause, affected component/files,
fix description, fix status, and Gerrit change linkage.

This builds an institutional memory so past fixes can inform future debugging.

Environment variables required:
  STARDOG_ENDPOINT  - Stardog server URL (e.g. http://localhost:5820)
  STARDOG_USERNAME  - Stardog username
  STARDOG_PASSWORD  - Stardog password
  STARDOG_DATABASE  - Target database name (default: bug_knowledge_graph)
  KG_NAMESPACE      - RDF namespace prefix (default: http://bugknowledge.org/)
"""

import os
import json
import logging
from datetime import datetime, timezone
from typing import Optional

import httpx
from fastmcp import FastMCP

STARDOG_ENDPOINT = os.getenv("STARDOG_ENDPOINT", "").rstrip("/")
STARDOG_USERNAME = os.getenv("STARDOG_USERNAME", "")
STARDOG_PASSWORD = os.getenv("STARDOG_PASSWORD", "")
STARDOG_DATABASE = os.getenv("STARDOG_DATABASE", "bug_knowledge_graph")
KG_NS = os.getenv("KG_NAMESPACE", "http://bugknowledge.org/")

mcp = FastMCP("bug-knowledge-graph")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _auth() -> tuple[str, str]:
    return (STARDOG_USERNAME, STARDOG_PASSWORD)


def _issue_uri(issue_key: str) -> str:
    return f"{KG_NS}bug/{issue_key.replace('-', '_')}"


def _esc(value: str) -> str:
    """Escape a string value for safe embedding in SPARQL literals."""
    return (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )


def _sparql_select(query: str) -> dict:
    url = f"{STARDOG_ENDPOINT}/{STARDOG_DATABASE}/query"
    try:
        resp = httpx.post(
            url,
            data={"query": query},
            headers={"Accept": "application/sparql-results+json"},
            auth=_auth(),
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as exc:
        logging.error("SPARQL SELECT error: %s", exc)
        return {"error": str(exc)}


def _sparql_update(update: str) -> dict:
    url = f"{STARDOG_ENDPOINT}/{STARDOG_DATABASE}/update"
    try:
        resp = httpx.post(
            url,
            data={"update": update},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=_auth(),
            timeout=30,
        )
        resp.raise_for_status()
        return {"status": "success", "http_status": resp.status_code}
    except Exception as exc:
        logging.error("SPARQL UPDATE error: %s", exc)
        return {"error": str(exc)}


def _bindings_to_records(bindings: list, field_map: dict) -> list[dict]:
    """Convert SPARQL result bindings to a list of dicts using field_map."""
    records = []
    for b in bindings:
        record: dict = {}
        for key, sparql_var in field_map.items():
            record[key] = b.get(sparql_var, {}).get("value", "")
        records.append(record)
    return records


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def store_bug_analysis(
    issue_key: str,
    summary: str,
    root_cause: str,
    component: str,
    affected_files: list[str],
    fix_description: str,
    fix_status: str = "proposed",
    gerrit_change_id: Optional[str] = None,
    notes: Optional[str] = None,
) -> dict:
    """Store (or overwrite) a bug analysis record in the knowledge graph.

    Call this after completing root cause analysis, and again after applying
    a fix to update the fix status and Gerrit change ID.

    Args:
        issue_key: JIRA issue key (e.g. 'PROJ-123')
        summary: Short issue summary / title
        root_cause: Detailed root cause analysis text
        component: Name of the software component affected (e.g. 'BrakingController')
        affected_files: List of repository-relative file paths involved
        fix_description: Description of the proposed or applied fix
        fix_status: Lifecycle status - one of: 'open', 'proposed', 'merged', 'abandoned'
        gerrit_change_id: Gerrit change numeric ID or Change-Id (optional)
        notes: Additional free-text notes

    Returns:
        dict with 'status' or 'error'
    """
    now = datetime.now(timezone.utc).isoformat()
    uri = _issue_uri(issue_key)
    ns = KG_NS

    files_triples = "\n  ".join(
        f'<{uri}> <{ns}hasAffectedFile> "{_esc(f)}" .'
        for f in affected_files
    )
    gerrit_triple = (
        f'<{uri}> <{ns}hasGerritChangeId> "{_esc(gerrit_change_id)}" .'
        if gerrit_change_id else ""
    )
    notes_triple = (
        f'<{uri}> <{ns}hasNotes> "{_esc(notes)}" .'
        if notes else ""
    )

    # Delete existing record and insert fresh data atomically
    update = f"""PREFIX kg: <{ns}>
DELETE {{ <{uri}> ?p ?o }} WHERE {{ <{uri}> ?p ?o }} ;
INSERT DATA {{
  <{uri}> a kg:BugRecord ;
    kg:hasIssueKey      "{_esc(issue_key)}" ;
    kg:hasSummary       "{_esc(summary)}" ;
    kg:hasRootCause     "{_esc(root_cause)}" ;
    kg:hasComponent     "{_esc(component)}" ;
    kg:hasFixDescription "{_esc(fix_description)}" ;
    kg:hasFixStatus     "{_esc(fix_status)}" ;
    kg:hasCreatedDate   "{now}" ;
    kg:hasUpdatedDate   "{now}" .
  {files_triples}
  {gerrit_triple}
  {notes_triple}
}}"""
    return _sparql_update(update)


@mcp.tool()
def update_fix_status(
    issue_key: str,
    fix_status: str,
    gerrit_change_id: Optional[str] = None,
    notes: Optional[str] = None,
) -> dict:
    """Update the fix lifecycle status of an existing bug record.

    Use this to mark a fix as 'merged' after Gerrit approval, or 'abandoned'
    if the approach was changed.

    Args:
        issue_key: JIRA issue key (e.g. 'PROJ-123')
        fix_status: New status: 'open', 'proposed', 'merged', 'abandoned'
        gerrit_change_id: Gerrit change ID to record (optional)
        notes: Additional notes to append (optional)

    Returns:
        dict with 'status' or 'error'
    """
    now = datetime.now(timezone.utc).isoformat()
    uri = _issue_uri(issue_key)
    ns = KG_NS

    # Build inlined DELETE / INSERT for mutable fields only
    gerrit_delete = f"OPTIONAL {{ <{uri}> <{ns}hasGerritChangeId> ?g }}"
    gerrit_insert = (
        f'<{uri}> <{ns}hasGerritChangeId> "{_esc(gerrit_change_id)}" .'
        if gerrit_change_id else ""
    )
    notes_insert = (
        f'<{uri}> <{ns}hasNotes> "{_esc(notes)}" .'
        if notes else ""
    )

    update = f"""PREFIX kg: <{ns}>
DELETE {{
  <{uri}> <{ns}hasFixStatus>    ?s .
  <{uri}> <{ns}hasUpdatedDate>  ?d .
  <{uri}> <{ns}hasGerritChangeId> ?g .
}}
WHERE {{
  OPTIONAL {{ <{uri}> <{ns}hasFixStatus>    ?s }}
  OPTIONAL {{ <{uri}> <{ns}hasUpdatedDate>  ?d }}
  {gerrit_delete}
}} ;
INSERT DATA {{
  <{uri}> <{ns}hasFixStatus>   "{_esc(fix_status)}" .
  <{uri}> <{ns}hasUpdatedDate> "{now}" .
  {gerrit_insert}
  {notes_insert}
}}"""
    return _sparql_update(update)


@mcp.tool()
def get_issue_knowledge(issue_key: str) -> dict:
    """Retrieve all stored knowledge about a specific JIRA issue from the graph.

    Args:
        issue_key: JIRA issue key (e.g. 'PROJ-123')

    Returns:
        Flat dict of all properties for the issue, or 'error'
    """
    ns = KG_NS
    query = f"""PREFIX kg: <{ns}>
SELECT ?prop ?val WHERE {{
  ?rec kg:hasIssueKey "{_esc(issue_key)}" ;
       ?prop ?val .
}}"""
    result = _sparql_select(query)
    if "error" in result:
        return result

    record: dict = {"issue_key": issue_key}
    for b in result.get("results", {}).get("bindings", []):
        raw_prop = b.get("prop", {}).get("value", "")
        val = b.get("val", {}).get("value", "")
        # Use short local name as key
        key = raw_prop.split("/")[-1] if "/" in raw_prop else raw_prop
        if key in record:
            existing = record[key]
            if isinstance(existing, list):
                existing.append(val)
            else:
                record[key] = [existing, val]
        else:
            record[key] = val
    return record


@mcp.tool()
def query_similar_issues(
    component: str,
    keywords: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """Find historically similar bugs in the same component.

    Use this during analysis to check whether the same root cause has been
    seen before, so previous fixes can inform the current one.

    Args:
        component: Software component name to scope the search
        keywords: Optional keywords to match in root cause or summary
        limit: Max number of results (default 10)

    Returns:
        dict with 'issues' list (most recently updated first) or 'error'
    """
    ns = KG_NS
    kw_filter = ""
    if keywords:
        kw_esc = _esc(keywords)
        kw_filter = (
            f'FILTER('
            f'CONTAINS(LCASE(?rootCause), LCASE("{kw_esc}")) || '
            f'CONTAINS(LCASE(?summary), LCASE("{kw_esc}")))'
        )

    query = f"""PREFIX kg: <{ns}>
SELECT ?issueKey ?summary ?rootCause ?fixDescription ?fixStatus ?updatedDate WHERE {{
  ?rec a kg:BugRecord ;
       kg:hasIssueKey       ?issueKey ;
       kg:hasSummary        ?summary ;
       kg:hasRootCause      ?rootCause ;
       kg:hasFixDescription ?fixDescription ;
       kg:hasFixStatus      ?fixStatus ;
       kg:hasComponent      "{_esc(component)}" .
  OPTIONAL {{ ?rec kg:hasUpdatedDate ?updatedDate }}
  {kw_filter}
}}
ORDER BY DESC(?updatedDate)
LIMIT {limit}"""

    result = _sparql_select(query)
    if "error" in result:
        return result

    field_map = {
        "issue_key": "issueKey",
        "summary": "summary",
        "root_cause": "rootCause",
        "fix_description": "fixDescription",
        "fix_status": "fixStatus",
        "updated_date": "updatedDate",
    }
    issues = _bindings_to_records(
        result.get("results", {}).get("bindings", []), field_map
    )
    return {"component": component, "issues": issues, "total": len(issues)}


@mcp.tool()
def get_component_history(component: str, limit: int = 20) -> dict:
    """Get the full bug and fix history for a software component.

    Useful for understanding recurring issues and overall component health.

    Args:
        component: Software component name
        limit: Maximum records to return (default 20)

    Returns:
        dict with 'component', 'records' list, 'total' or 'error'
    """
    ns = KG_NS
    query = f"""PREFIX kg: <{ns}>
SELECT ?issueKey ?summary ?fixStatus ?updatedDate ?gerritChange WHERE {{
  ?rec a kg:BugRecord ;
       kg:hasIssueKey  ?issueKey ;
       kg:hasSummary   ?summary ;
       kg:hasFixStatus ?fixStatus ;
       kg:hasComponent "{_esc(component)}" .
  OPTIONAL {{ ?rec kg:hasUpdatedDate    ?updatedDate }}
  OPTIONAL {{ ?rec kg:hasGerritChangeId ?gerritChange }}
}}
ORDER BY DESC(?updatedDate)
LIMIT {limit}"""

    result = _sparql_select(query)
    if "error" in result:
        return result

    field_map = {
        "issue_key": "issueKey",
        "summary": "summary",
        "fix_status": "fixStatus",
        "updated_date": "updatedDate",
        "gerrit_change": "gerritChange",
    }
    records = _bindings_to_records(
        result.get("results", {}).get("bindings", []), field_map
    )
    return {"component": component, "records": records, "total": len(records)}


@mcp.tool()
def get_all_open_issues(limit: int = 50) -> dict:
    """Get all bug records with fix_status 'open' or 'proposed' across all components.

    Args:
        limit: Maximum records to return (default 50)

    Returns:
        dict with 'issues' list or 'error'
    """
    ns = KG_NS
    query = f"""PREFIX kg: <{ns}>
SELECT ?issueKey ?summary ?component ?fixStatus ?updatedDate WHERE {{
  ?rec a kg:BugRecord ;
       kg:hasIssueKey  ?issueKey ;
       kg:hasSummary   ?summary ;
       kg:hasComponent ?component ;
       kg:hasFixStatus ?fixStatus .
  OPTIONAL {{ ?rec kg:hasUpdatedDate ?updatedDate }}
  FILTER(?fixStatus IN ("open", "proposed"))
}}
ORDER BY DESC(?updatedDate)
LIMIT {limit}"""

    result = _sparql_select(query)
    if "error" in result:
        return result

    field_map = {
        "issue_key": "issueKey",
        "summary": "summary",
        "component": "component",
        "fix_status": "fixStatus",
        "updated_date": "updatedDate",
    }
    issues = _bindings_to_records(
        result.get("results", {}).get("bindings", []), field_map
    )
    return {"issues": issues, "total": len(issues)}


@mcp.tool()
def sparql_query(query: str) -> dict:
    """Execute a raw SPARQL SELECT query against the bug knowledge graph.

    Use for advanced custom queries beyond the built-in tools.

    Args:
        query: Valid SPARQL SELECT query string

    Returns:
        dict with full SPARQL results or 'error'
    """
    return _sparql_select(query)


@mcp.tool()
def sparql_update(update: str) -> dict:
    """Execute a raw SPARQL UPDATE (INSERT DATA / DELETE DATA) against the graph.

    Use for advanced custom mutations beyond the built-in tools.

    Args:
        update: Valid SPARQL UPDATE string

    Returns:
        dict with 'status' or 'error'
    """
    return _sparql_update(update)


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
        port = int(os.getenv("HOST_PORT", "8002"))
        mcp.run(transport=transport, host=host, port=port)
