"""MCP server for IBM Engineering Test Management (ETM).

This server provides comprehensive tools to interact with IBM ETM via REST API,
supporting test plans, test cases, test suites, execution results, and advanced
traceability operations.

IMPORTANT - Resource ID Format Requirements:
============================================
ETM uses TWO different ID formats for resources:

1. CREATE operations return: slug__ format (e.g., 'slug__9h4owMtxEfCBCr45cRCLXQ')
2. GET/UPDATE operations require: Numeric webId format (e.g., '3435411', '7423', '105520')

When you create a resource, the response includes a slug__ identifier. To use that resource
in GET or UPDATE operations, you must:
- Use list operations to find the numeric webId, OR
- Extract the webId from the creation response headers/XML

Example workflow:
1. create_test_case() returns: {"testcase_id": "slug__9h4owMtxEfCBCr45cRCLXQ", ...}
2. list_test_cases() shows: {"identifier": "slug__...", "webId": "3435411", ...}
3. update_test_case(test_case_id="3435411", ...) - use numeric webId!

All GET, UPDATE, and DELETE operations require the numeric webId format.

Environment Variables Required:
================================
- ETM_BASE_URL: Base URL of the ETM server
- ETM_USERNAME: Username for authentication
- ETM_PASSWORD: Password for authentication
- ETM_PROJECT_AREA: Default project area name
- ETM_VERIFY_SSL: (Optional) Set to 'false' to disable SSL verification
- TRANSPORT: (Optional) Transport type, defaults to 'stdio'
- HOST: (Optional) Host for non-stdio transport
- HOST_PORT: (Optional) Port for non-stdio transport
"""

import json
import logging
import os
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Any, Optional
from urllib.parse import quote
from xml.sax.saxutils import escape

import requests
from fastmcp import FastMCP

# Initialize MCP server
mcp = FastMCP("ETMMCP Server")

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# IBM ETM connection details
ETM_BASE_URL = os.getenv("ETM_BASE_URL", "").rstrip("/")
ETM_USERNAME = os.getenv("ETM_USERNAME")
ETM_PASSWORD = os.getenv("ETM_PASSWORD")
ETM_PROJECT_AREA = os.getenv("ETM_PROJECT_AREA")
ETM_VERIFY_SSL = os.getenv("ETM_VERIFY_SSL", "true").lower() == "true"

# Constants
ETM_NAMESPACE = "http://jazz.net/xmlns/alm/qm/v0.1/"
ETM_SERVICE_PATH = "/service/com.ibm.rqm.integration.service.IIntegrationService/resources"

# Validate environment variables
missing_vars = [
    name
    for name, value in {
        "ETM_BASE_URL": ETM_BASE_URL,
        "ETM_USERNAME": ETM_USERNAME,
        "ETM_PASSWORD": ETM_PASSWORD,
        "ETM_PROJECT_AREA": ETM_PROJECT_AREA,
    }.items()
    if not value
]
if missing_vars:
    raise ValueError(f"Missing required environment variable(s): {', '.join(missing_vars)}")

# Configure SSL verification
if not ETM_VERIFY_SSL:
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # SSL Certificate warnings disabled
    logging.warning("SSL certificate verification is disabled.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_headers(accept_type: str = "application/json") -> dict[str, str]:
    """Generate standard headers for ETM API requests.

    Args:
        accept_type: The Accept header value (default: application/json)

    Returns:
        Dictionary of HTTP headers
    """
    return {"Accept": accept_type, "OSLC-Core-Version": "2.0"}


def _build_resource_url(project: str, resource_type: str, resource_id: Optional[str] = None) -> str:
    """Build the ETM resource URL.

    Args:
        project: Project area name
        resource_type: Type of resource (testcase, testplan, etc.)
        resource_id: Optional resource ID

    Returns:
        Formatted resource URL path
    """
    encoded_project = quote(project, safe="")
    base = f"{ETM_SERVICE_PATH}/{encoded_project}/{resource_type}"
    if resource_id:
        if resource_id.startswith("urn:com.ibm.rqm:"):
            return f"{base}/{resource_id}"
        # ETM expects just the numeric ID in the URN format
        return f"{base}/urn:com.ibm.rqm:{resource_type}:{resource_id}"
    return base


def _build_resource_href(project: str, resource_type: str, resource_id: str) -> str:
    """Build a complete resource href URL for ETM references.

    Args:
        project: Project area name
        resource_type: Type of resource
        resource_id: Resource ID

    Returns:
        Complete href URL
    """
    encoded_project = quote(project, safe="")
    if resource_id.startswith("urn:"):
        url = f"{ETM_SERVICE_PATH}/{encoded_project}/{resource_type}/{resource_id}"
    else:
        url = f"{ETM_SERVICE_PATH}/{encoded_project}/{resource_type}/urn:com.ibm.rqm:{resource_type}:{resource_id}"
    return f"{ETM_BASE_URL}{url}"


def _make_request(
    endpoint: str,
    method: str = "GET",
    params: Optional[dict[str, Any]] = None,
    accept_type: str = "application/json",
    timeout: int = 30,
    data: Optional[bytes | str] = None,
    content_type: Optional[str] = None,
) -> requests.Response:
    """Make an HTTP request to the ETM API.

    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, PUT, DELETE)
        params: Query parameters
        accept_type: Accept header value
        timeout: Request timeout in seconds
        data: Request body data
        content_type: Content-Type header value

    Returns:
        Response object
    """
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"
    url = f"{ETM_BASE_URL}{endpoint}"

    headers = _get_headers(accept_type)
    if data:
        headers["Content-Type"] = content_type or "application/rdf+xml"
    if method in ["POST", "PUT"]:
        headers["X-Jazz-CSRF-Prevent"] = "true"

    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            params=params,
            data=data,
            auth=(ETM_USERNAME, ETM_PASSWORD),
            verify=ETM_VERIFY_SSL,
            timeout=timeout,
        )
        logging.info(f"{method} {response.url} - Status: {response.status_code}")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"ETM API request failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            logging.error(f"Response: {e.response.status_code} - {e.response.text[:500]}")
        raise


def _extract_resource_id(response: requests.Response, resource_type: str) -> Optional[str]:
    """Extract resource ID from API response.

    Attempts to extract the resource ID from the response body (XML) or headers.

    Args:
        response: The HTTP response object
        resource_type: Type of resource being extracted

    Returns:
        Extracted resource ID or None if not found
    """
    try:
        root = ET.fromstring(response.text)
        ns = {
            "dcterms": "http://purl.org/dc/terms/",
            "rqm": "http://schema.ibm.com/rqm/2007#executionresult",
            "ns2": ETM_NAMESPACE,
        }

        # Try dcterms:identifier, rqm:resultId, then webId
        for xpath in [".//dcterms:identifier", ".//rqm:resultId", ".//ns2:webId"]:
            elem = root.find(xpath, ns)
            if elem is not None and elem.text:
                logging.info(f"Extracted {resource_type} ID from XML: {elem.text}")
                return elem.text
    except ET.ParseError as e:
        logging.debug(f"Could not parse XML response for {resource_type}: {e}")

    # Fallback to checking response headers
    for header in ["Location", "location", "Content-Location", "content-location"]:
        location = response.headers.get(header)
        if location:
            resource_id = location.split(":")[-1] if ":" in location else location.split("/")[-1]
            logging.info(f"Extracted {resource_type} ID from header {header}: {resource_id}")
            return resource_id

    logging.warning(f"Could not extract {resource_type} ID")
    return None


def _create_xml_resource(resource_type: str, title: str, description: str, **extra_fields: Any) -> str:
    """Generate XML payload for creating ETM resources.

    Args:
        resource_type: Type of resource to create
        title: Resource title
        description: Resource description
        **extra_fields: Additional fields to include in the XML

    Returns:
        XML string representation of the resource
    """
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ns2:{resource_type} xmlns:ns2="{ETM_NAMESPACE}" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{escape(title)}</dc:title>
    <dc:description>{escape(description)}</dc:description>"""

    for field, value in extra_fields.items():
        if value:
            if field.startswith("href_"):
                ref_type = field[5:]  # Remove "href_" prefix
                xml += f'\n    <ns2:{ref_type} href="{value}"/>'
            else:
                xml += f"\n    <ns2:{field}>{escape(str(value))}</ns2:{field}>"

    xml += f"\n</ns2:{resource_type}>"
    return xml


def _update_xml_resource(xml_text: str, **updates: Any) -> bytes:
    """Update XML resource with new field values.

    Args:
        xml_text: Original XML text
        **updates: Fields to update with their new values

    Returns:
        Updated XML as bytes
    """
    root = ET.fromstring(xml_text)
    ns = {"ns2": ETM_NAMESPACE, "dc": "http://purl.org/dc/elements/1.1/"}

    for field, value in updates.items():
        if not value:
            continue

        if field in ["title", "description"]:
            elem = root.find(f"dc:{field}", ns)
            if elem is not None:
                elem.text = escape(value)
            else:
                elem = ET.SubElement(root, f"{{http://purl.org/dc/elements/1.1/}}{field}")
                elem.text = escape(value)
        else:
            elem = root.find(f"ns2:{field}", ns)
            if elem is not None:
                elem.text = str(value)
            else:
                elem = ET.SubElement(root, f"{{{ETM_NAMESPACE}}}{field}")
                elem.text = str(value)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def _handle_error(func_name: str, e: Exception) -> str:
    """Standardized error handling for tool functions.

    Args:
        func_name: Name of the function where error occurred
        e: The exception that was raised

    Returns:
        JSON string with error information
    """
    error_msg = str(e)
    logging.error(f"Error in {func_name}: {error_msg}", exc_info=True)
    return json.dumps({"error": error_msg, "function": func_name})


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


# ============================================================================
# TOOLS - CONNECTION & UTILITIES
# ============================================================================


@mcp.tool()
def test_project_connection(project_area: str) -> str:
    """Test connection to a specific project area.

    Args:
        project_area: Name of the project area to test

    Returns:
        JSON string with connection status
    """
    try:
        if not project_area.strip():
            return json.dumps({"error": "project_area is required"})

        endpoint = _build_resource_url(project_area, "testplan")
        _make_request(endpoint, params={"abbreviate": "false"})

        return json.dumps(
            {
                "success": True,
                "project_area": project_area,
                "message": f"✓ Successfully connected to project '{project_area}'",
            }
        )
    except Exception as e:
        return _handle_error("test_project_connection", e)


@mcp.tool()
def list_project_areas() -> str:
    """List all available project areas.

    Returns:
        XML string containing all project areas
    """
    try:
        response = _make_request("/process/project-areas", accept_type="application/xml")
        return response.text
    except Exception as e:
        return _handle_error("list_project_areas", e)


@mcp.tool()
def search_resources(
    resource_type: str, category: Optional[str] = None, project_area: Optional[str] = None, limit: int = 50
) -> str:
    """Search ETM resources by category or list all resources of a type."""
    valid_types = [
        "testcase",
        "testplan",
        "testsuite",
        "executionworkitem",
        "executionresult",
        "testscript",
        "configuration",
        "buildrecord",
    ]

    if resource_type not in valid_types:
        return json.dumps({"error": f"resource_type must be one of: {', '.join(valid_types)}"})
    if not (1 <= limit <= 200):
        return json.dumps({"error": "limit must be between 1 and 200"})

    try:
        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, resource_type)
        params: dict[str, str] = {"abbreviate": "false"}

        if category:
            params["fields"] = f"{resource_type}[category/term='{category}']"

        response = _make_request(endpoint, params=params, timeout=120)
        return response.text
    except Exception as e:
        return _handle_error("search_resources", e)


# ============================================================================
# TOOLS - GENERIC CRUD OPERATIONS
# ============================================================================


def _generic_list(resource_type: str, project_area: Optional[str] = None, limit: int = 50) -> str:
    """Generic list function for any ETM resource

    Note: Uses ETM_PROJECT_AREA environment variable by default.
    List operations return resources with both slug__ identifiers and numeric webIds.
    """
    try:
        if not (1 <= limit <= 200):
            return json.dumps({"error": "limit must be between 1 and 200"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, resource_type)
        response = _make_request(endpoint, params={"abbreviate": "false"})
        return response.text
    except Exception as e:
        return _handle_error(f"list_{resource_type}", e)


def _generic_get(resource_type: str, resource_id: str, project_area: Optional[str] = None) -> str:
    """Generic get function for any ETM resource

    IMPORTANT: resource_id must be the numeric webId (e.g., '3435411'), NOT the slug__ identifier.
    The ETM API requires numeric IDs for GET operations, even though create operations return slug__ format.

    Note: Uses ETM_PROJECT_AREA environment variable by default.
    """
    try:
        if not resource_id.strip():
            return json.dumps({"error": f"{resource_type}_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, resource_type, resource_id)
        response = _make_request(endpoint)
        return response.text
    except Exception as e:
        return _handle_error(f"get_{resource_type}", e)


def _generic_create(
    resource_type: str, title: str, description: str, project_area: Optional[str] = None, **extra_fields
) -> str:
    """Generic create function for ETM resources

    Returns: JSON with resource_id in slug__ format (e.g., 'slug__9h4owMtxEfCBCr45cRCLXQ').
    Note: To use this resource in GET/UPDATE operations, you must use the numeric webId instead,
    which can be obtained by listing resources or from the webId field in the response.
    """
    try:
        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, resource_type)

        xml_payload = _create_xml_resource(resource_type, title, description, **extra_fields)
        logging.info(f"Creating {resource_type}: '{title}'")

        response = _make_request(
            endpoint,
            method="POST",
            data=xml_payload.encode("utf-8"),
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        resource_id = _extract_resource_id(response, resource_type)
        location = response.headers.get("Location", "")

        return json.dumps(
            {
                "success": True,
                f"{resource_type}_id": resource_id,
                "location": location,
                "message": f"{resource_type.title()} '{title}' created successfully",
            }
        )
    except Exception as e:
        return _handle_error(f"create_{resource_type}", e)


def _generic_update(resource_type: str, resource_id: str, project_area: Optional[str] = None, **updates) -> str:
    """Generic update function for ETM resources

    IMPORTANT: resource_id must be the numeric webId (e.g., '3435411'), NOT the slug__ identifier.
    The ETM API requires numeric IDs for UPDATE operations, even though create operations return slug__ format.

    Note: Uses ETM_PROJECT_AREA environment variable by default.
    """
    try:
        if not resource_id:
            return json.dumps({"error": f"{resource_type}_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, resource_type, resource_id)

        response = _make_request(endpoint, accept_type="application/xml")
        updated_xml = _update_xml_resource(response.text, **updates)

        logging.info(f"Updating {resource_type} {resource_id}")

        _make_request(
            endpoint,
            method="PUT",
            data=updated_xml,
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        return json.dumps(
            {
                "success": True,
                f"{resource_type}_id": resource_id,
                "message": f"{resource_type.title()} updated successfully",
            }
        )
    except Exception as e:
        return _handle_error(f"update_{resource_type}", e)


def _generic_delete(resource_type: str, resource_id: str, project_area: Optional[str] = None) -> str:
    """Generic delete function for ETM resources"""
    try:
        if not resource_id:
            return json.dumps({"error": f"{resource_type}_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, resource_type, resource_id)
        _make_request(endpoint, method="DELETE", timeout=60)

        return json.dumps(
            {
                "success": True,
                f"{resource_type}_id": resource_id,
                "message": f"{resource_type.title()} deleted successfully",
            }
        )
    except Exception as e:
        return _handle_error(f"delete_{resource_type}", e)


# ============================================================================
# TOOLS - TEST PLANS
# ============================================================================


@mcp.tool()
def list_test_plans(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List test plans."""
    return _generic_list("testplan", project_area, limit)


@mcp.tool()
def get_test_plan(test_plan_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test plan.

    Args:
        test_plan_id: Numeric webId (e.g., '105520'), NOT slug__ identifier
        project_area: Optional project area override
    """
    return _generic_get("testplan", test_plan_id, project_area)


@mcp.tool()
def create_test_plan(
    title: str,
    description: str,
    project_area: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    owner: Optional[str] = None,
) -> str:
    """Create a new test plan."""
    return _generic_create(
        "testplan", title, description, project_area, startdate=start_date, enddate=end_date, owner=owner
    )


@mcp.tool()
def update_test_plan(
    test_plan_id: str,
    project_area: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    owner: Optional[str] = None,
) -> str:
    """Update an existing test plan.

    Args:
        test_plan_id: Numeric webId (e.g., '105520'), NOT slug__ identifier
        project_area: Optional project area override
        title: New title (optional)
        description: New description (optional)
        start_date: New start date (optional)
        end_date: New end date (optional)
        owner: New owner (optional)
    """
    updates = {
        k: v
        for k, v in {
            "title": title,
            "description": description,
            "startdate": start_date,
            "enddate": end_date,
            "owner": owner,
        }.items()
        if v is not None
    }
    return _generic_update("testplan", test_plan_id, project_area, **updates)


@mcp.tool()
def delete_test_plan(test_plan_id: str, project_area: Optional[str] = None) -> str:
    """Delete a test plan. Use with caution."""
    return _generic_delete("testplan", test_plan_id, project_area)


@mcp.tool()
def get_test_plan_statistics(test_plan_id: str, project_area: Optional[str] = None) -> str:
    """Get statistics for a test plan (pass rate, execution count, etc.)."""
    try:
        if not test_plan_id:
            return json.dumps({"error": "test_plan_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "executionresult")
        response = _make_request(endpoint, params={"abbreviate": "false"}, accept_type="application/xml", timeout=180)

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "ns2": ETM_NAMESPACE}

        stats = {"total": 0, "passed": 0, "failed": 0, "blocked": 0, "incomplete": 0}

        for entry in root.findall(".//atom:entry", ns):
            exec_result = entry.find(".//ns2:executionresult", ns)
            if exec_result is None:
                continue

            # Check if belongs to test plan
            tp_elem = exec_result.find(".//ns2:testplan", ns)
            if tp_elem is not None and test_plan_id not in tp_elem.get("href", ""):
                continue

            stats["total"] += 1
            state_elem = exec_result.find(".//ns2:state", ns)
            if state_elem is not None:
                state = state_elem.text.lower()
                if "passed" in state:
                    stats["passed"] += 1
                elif "failed" in state:
                    stats["failed"] += 1
                elif "blocked" in state:
                    stats["blocked"] += 1
                else:
                    stats["incomplete"] += 1

        stats["pass_rate"] = round((stats["passed"] / stats["total"]) * 100, 2) if stats["total"] > 0 else 0

        return json.dumps({"success": True, "test_plan_id": test_plan_id, "statistics": stats}, indent=2)
    except Exception as e:
        return _handle_error("get_test_plan_statistics", e)


# ============================================================================
# TOOLS - TEST CASES
# ============================================================================


@mcp.tool()
def list_test_cases(project_area: Optional[str] = None, limit: int = 50, category: Optional[str] = None) -> str:
    """List test cases with optional category filter."""
    try:
        if not (1 <= limit <= 200):
            return json.dumps({"error": "limit must be between 1 and 200"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testcase")
        params = {"abbreviate": "false"}

        if category:
            params["fields"] = f"testcase[category/term='{category}']"

        response = _make_request(endpoint, params=params, timeout=120)
        return response.text
    except Exception as e:
        return _handle_error("list_test_cases", e)


@mcp.tool()
def get_test_case(test_case_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test case.

    Args:
        test_case_id: Numeric webId (e.g., '3435411'), NOT slug__ identifier
        project_area: Optional project area override
    """
    return _generic_get("testcase", test_case_id, project_area)


@mcp.tool()
def create_test_case(
    title: str, description: str, project_area: Optional[str] = None, test_script_id: Optional[str] = None
) -> str:
    """Create a new test case."""
    extra = {}
    if test_script_id:
        project = project_area or ETM_PROJECT_AREA
        extra["href_testscript"] = _build_resource_href(project, "testscript", test_script_id)
    return _generic_create("testcase", title, description, project_area, **extra)


@mcp.tool()
def update_test_case(
    test_case_id: str,
    project_area: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Update an existing test case.

    Args:
        test_case_id: Numeric webId (e.g., '3435411'), NOT slug__ identifier
        project_area: Optional project area override
        title: New title (optional)
        description: New description (optional)
    """
    updates = {k: v for k, v in {"title": title, "description": description}.items() if v is not None}
    return _generic_update("testcase", test_case_id, project_area, **updates)


@mcp.tool()
def delete_test_case(test_case_id: str, project_area: Optional[str] = None) -> str:
    """Delete a test case. Use with caution."""
    return _generic_delete("testcase", test_case_id, project_area)


# ============================================================================
# TOOLS - TEST SUITES
# ============================================================================


@mcp.tool()
def list_test_suites(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List test suites."""
    return _generic_list("testsuite", project_area, limit)


@mcp.tool()
def get_test_suite(test_suite_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test suite.

    Args:
        test_suite_id: Numeric webId (e.g., '7423'), NOT slug__ identifier
        project_area: Optional project area override
    """
    return _generic_get("testsuite", test_suite_id, project_area)


@mcp.tool()
def create_test_suite(title: str, description: str, project_area: Optional[str] = None) -> str:
    """Create a new test suite."""
    return _generic_create("testsuite", title, description, project_area)


@mcp.tool()
def update_test_suite(
    test_suite_id: str,
    project_area: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Update an existing test suite.

    Args:
        test_suite_id: Numeric webId (e.g., '7423'), NOT slug__ identifier
        project_area: Optional project area override
        title: New title (optional)
        description: New description (optional)
    """
    updates = {k: v for k, v in {"title": title, "description": description}.items() if v is not None}
    return _generic_update("testsuite", test_suite_id, project_area, **updates)


@mcp.tool()
def delete_test_suite(test_suite_id: str, project_area: Optional[str] = None) -> str:
    """Delete a test suite. Use with caution."""
    return _generic_delete("testsuite", test_suite_id, project_area)


# ============================================================================
# TOOLS - TEST PHASES
# ============================================================================


@mcp.tool()
def list_test_phases(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List test phases."""
    return _generic_list("testphase", project_area, limit)


@mcp.tool()
def get_test_phase(test_phase_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test phase."""
    return _generic_get("testphase", test_phase_id, project_area)


@mcp.tool()
def create_test_phase(title: str, description: str = "", project_area: Optional[str] = None) -> str:
    """Create a new test phase."""
    return _generic_create("testphase", title, description, project_area)


# ============================================================================
# TOOLS - ATTACHMENTS
# ============================================================================


@mcp.tool()
def list_attachments(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List attachments."""
    return _generic_list("attachment", project_area, limit)


@mcp.tool()
def get_attachment(attachment_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific attachment."""
    return _generic_get("attachment", attachment_id, project_area)


@mcp.tool()
def get_test_case_attachments(test_case_id: str, project_area: Optional[str] = None) -> str:
    """Get attachments for a specific test case."""
    try:
        if not test_case_id:
            return json.dumps({"error": "test_case_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testcase", test_case_id)

        response = _make_request(endpoint, params={"fields": "testcase/attachment"}, accept_type="application/xml")
        return response.text
    except Exception as e:
        return _handle_error("get_test_case_attachments", e)


# ============================================================================
# TOOLS - TEMPLATES
# ============================================================================


@mcp.tool()
def list_templates(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List templates (test plan, test case, test suite)."""
    return _generic_list("template", project_area, limit)


@mcp.tool()
def get_test_plan_template(template_name: str, project_area: Optional[str] = None) -> str:
    """Get a specific test plan template."""
    try:
        project = project_area or ETM_PROJECT_AREA
        endpoint = f"{_build_resource_url(project, 'template')}/testplan/{template_name}"
        response = _make_request(endpoint)
        return response.text
    except Exception as e:
        return _handle_error("get_test_plan_template", e)


# ============================================================================
# TOOLS - EXECUTION RESULTS
# ============================================================================


@mcp.tool()
def list_execution_results(
    project_area: Optional[str] = None, limit: int = 50, test_plan_id: Optional[str] = None, state: Optional[str] = None
) -> str:
    """List execution results with optional filtering."""
    try:
        if not (1 <= limit <= 200):
            return json.dumps({"error": "limit must be between 1 and 200"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "executionresult")
        params = {"abbreviate": "false"}

        # Add server-side filters
        if test_plan_id or state:
            conditions = []
            if test_plan_id:
                conditions.append(f"testplan[@href='{_build_resource_href(project, 'testplan', test_plan_id)}']")
            if state:
                conditions.append(f"state='{state}'")
            params["fields"] = f"executionresult[{' and '.join(conditions)}]"

        response = _make_request(endpoint, params=params, timeout=180)
        return response.text
    except Exception as e:
        return _handle_error("list_execution_results", e)


@mcp.tool()
def get_execution_result(result_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific execution result."""
    return _generic_get("executionresult", result_id, project_area)


@mcp.tool()
def create_execution_record(
    test_case_id: str,
    result: str,
    project_area: Optional[str] = None,
    test_plan_id: Optional[str] = None,
    executed_by: Optional[str] = None,
    comments: Optional[str] = None,
) -> str:
    """Create a test execution record (TCER + Execution Result).

    This is a two-step process:
    1. Create a Test Case Execution Record (TCER)
    2. Create an Execution Result linked to the TCER

    Args:
        test_case_id: Numeric webId of the test case
        result: Result status (passed, failed, incomplete, blocked)
        project_area: Optional project area override
        test_plan_id: Optional test plan to associate with
        executed_by: Optional executor name
        comments: Optional comments about the execution

    Returns:
        JSON string with execution record details
    """
    try:
        project = project_area or ETM_PROJECT_AREA

        logging.info(f"Step 1: Creating TCER for test case {test_case_id}")

        # Map result to ETM state
        state_map = {
            "passed": "com.ibm.rqm.execution.common.state.passed",
            "failed": "com.ibm.rqm.execution.common.state.failed",
            "incomplete": "com.ibm.rqm.execution.common.state.incomplete",
            "blocked": "com.ibm.rqm.execution.common.state.blocked",
        }
        state = state_map.get(result.lower(), "com.ibm.rqm.execution.common.state.incomplete")

        # Step 1: Create TCER
        tcer_extra: dict[str, str] = {"href_testcase": _build_resource_href(project, "testcase", test_case_id)}
        if test_plan_id:
            tcer_extra["href_testplan"] = _build_resource_href(project, "testplan", test_plan_id)

        tcer_endpoint = _build_resource_url(project, "executionworkitem")
        tcer_xml = _create_xml_resource("executionworkitem", "Execution Record", "", **tcer_extra)

        tcer_response = _make_request(
            tcer_endpoint,
            method="POST",
            data=tcer_xml.encode("utf-8"),
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        tcer_id = _extract_resource_id(tcer_response, "executionworkitem")
        if not tcer_id:
            return json.dumps({"error": "Failed to extract TCER ID"})

        logging.info(f"TCER created: {tcer_id}")

        # Small delay to ensure TCER is available
        time.sleep(1)

        logging.info(f"Step 2: Creating execution result for TCER {tcer_id}")

        # Step 2: Create Execution Result
        tcer_href = _build_resource_href(project, "executionworkitem", tcer_id)

        result_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<ns2:executionresult xmlns:ns2="{ETM_NAMESPACE}" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Execution Result</dc:title>
    <dc:description>{escape(comments or "")}</dc:description>
    <ns2:state>{state}</ns2:state>
    <ns2:testcase href="{_build_resource_href(project, "testcase", test_case_id)}"/>
    <ns2:executionworkitem href="{tcer_href}"/>"""

        if test_plan_id:
            result_xml += f'\n    <ns2:testplan href="{_build_resource_href(project, "testplan", test_plan_id)}"/>'

        if executed_by:
            result_xml += f"\n    <ns2:executedby>{escape(executed_by)}</ns2:executedby>"

        result_xml += "\n</ns2:executionresult>"

        result_endpoint = _build_resource_url(project, "executionresult")
        result_response = _make_request(
            result_endpoint,
            method="POST",
            data=result_xml.encode("utf-8"),
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        result_id = _extract_resource_id(result_response, "executionresult") or "unknown"
        logging.info(f"Execution result created: {result_id}")

        return json.dumps(
            {
                "success": True,
                "execution_result_id": result_id,
                "execution_record_id": tcer_id,
                "result": result,
                "message": f"Execution record created with result: {result}",
            }
        )
    except Exception as e:
        return _handle_error("create_execution_record", e)


@mcp.tool()
def update_execution_result(
    execution_result_id: str,
    project_area: Optional[str] = None,
    state: Optional[str] = None,
    comments: Optional[str] = None,
) -> str:
    """Update an existing execution result.

    Args:
        execution_result_id: Numeric webId of the execution result
        project_area: Optional project area override
        state: New state (passed, failed, incomplete, blocked)
        comments: New comments

    Returns:
        JSON string with update status
    """
    updates: dict[str, str] = {}
    if state:
        state_map = {
            "passed": "com.ibm.rqm.execution.common.state.passed",
            "failed": "com.ibm.rqm.execution.common.state.failed",
            "incomplete": "com.ibm.rqm.execution.common.state.incomplete",
            "blocked": "com.ibm.rqm.execution.common.state.blocked",
        }
        updates["state"] = state_map.get(state.lower(), state)
    if comments:
        updates["description"] = comments
    return _generic_update("executionresult", execution_result_id, project_area, **updates)


# ============================================================================
# TOOLS - ADVANCED ANALYSIS
# ============================================================================


@mcp.tool()
def get_test_case_links(test_case_id: str, project_area: Optional[str] = None) -> str:
    """Get all links (requirements, defects) for a test case."""
    try:
        if not test_case_id:
            return json.dumps({"error": "test_case_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testcase", test_case_id)
        response = _make_request(endpoint, accept_type="application/xml")
        root = ET.fromstring(response.text)

        ns = {"ns2": ETM_NAMESPACE, "dc": "http://purl.org/dc/elements/1.1/"}

        links = {
            "requirements": [
                {"href": elem.get("href", ""), "type": "validates"}
                for elem in root.findall(".//ns2:validates", ns)
                if elem.get("href")
            ],
            "work_items": [
                {"href": elem.get("href", ""), "type": "related_work_item"}
                for elem in root.findall(".//ns2:relatedworkitem", ns)
                if elem.get("href")
            ],
            "test_plans": [
                {"href": elem.get("href", ""), "type": "test_plan"}
                for elem in root.findall(".//ns2:testplan", ns)
                if elem.get("href")
            ],
        }

        total_links = sum(len(link_list) for link_list in links.values())

        return json.dumps(
            {"success": True, "test_case_id": test_case_id, "total_links": total_links, "links": links}, indent=2
        )
    except Exception as e:
        return _handle_error("get_test_case_links", e)


@mcp.tool()
def add_test_cases_to_suite(
    test_suite_id: str,
    test_case_ids: list[str],
    project_area: Optional[str] = None,
) -> str:
    """Add test cases to an existing test suite."""
    try:
        if not test_suite_id or not test_case_ids:
            return json.dumps({"error": "test_suite_id and test_case_ids are required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testsuite", test_suite_id)

        response = _make_request(endpoint, accept_type="application/xml")
        root = ET.fromstring(response.text)

        # Add new test case references
        for tc_id in test_case_ids:
            tc_href = _build_resource_href(project, "testcase", tc_id)
            suite_elem = ET.SubElement(root, f"{{{ETM_NAMESPACE}}}suiteelements")
            tc_elem = ET.SubElement(suite_elem, f"{{{ETM_NAMESPACE}}}testcase")
            tc_elem.set("href", tc_href)

        updated_xml = ET.tostring(root, encoding="unicode")
        logging.debug(f"Adding test cases to suite with XML:\n{updated_xml}")
        _make_request(
            endpoint,
            method="PUT",
            data=updated_xml,
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        return json.dumps(
            {
                "success": True,
                "test_suite_id": test_suite_id,
                "test_cases_added": len(test_case_ids),
                "message": "Test cases added to suite successfully",
            }
        )
    except Exception as e:
        logging.error(f"Error in add_test_cases_to_suite: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def link_testcase_to_testplan(
    test_plan_id: str,
    test_case_id: str,
    project_area: Optional[str] = None,
) -> str:
    """Link a test case to a test plan."""
    try:
        project = project_area or ETM_PROJECT_AREA

        # Get the test plan
        plan_endpoint = _build_resource_url(project, "testplan", test_plan_id)
        plan_response = _make_request(plan_endpoint, accept_type="application/xml")

        root = ET.fromstring(plan_response.text)

        # Build proper href using _build_resource_href
        testcase_href = _build_resource_href(project, "testcase", test_case_id)

        # Create new testcase element
        testcase_elem = ET.Element(f"{{{ETM_NAMESPACE}}}testcase")
        testcase_elem.set("href", testcase_href)
        root.append(testcase_elem)

        # Convert back to XML string
        updated_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)

        logging.info(f"Linking test case to plan with XML:\n{updated_xml.decode('utf-8')}")

        # PUT the updated test plan
        _make_request(
            plan_endpoint,
            method="PUT",
            data=updated_xml,
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        return json.dumps({"success": True, "message": f"Test case {test_case_id} linked to test plan {test_plan_id}"})
    except Exception as e:
        logging.error(f"Error in link_testcase_to_testplan: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def link_test_suite_to_plan(
    test_suite_id: str,
    test_plan_id: str,
    project_area: Optional[str] = None,
) -> str:
    """Link a test suite to a test plan."""
    try:
        if not test_suite_id or not test_plan_id:
            return json.dumps({"error": "test_suite_id and test_plan_id are required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testplan", test_plan_id)

        response = _make_request(endpoint, accept_type="application/xml")
        root = ET.fromstring(response.text)

        # Use _build_resource_href for proper URL
        suite_href = _build_resource_href(project, "testsuite", test_suite_id)
        suite_elem = ET.SubElement(root, f"{{{ETM_NAMESPACE}}}testsuite")
        suite_elem.set("href", suite_href)

        updated_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        logging.info(f"Linking test suite to plan with XML:\n{updated_xml.decode('utf-8')}")

        _make_request(
            endpoint,
            method="PUT",
            data=updated_xml,
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        return json.dumps(
            {
                "success": True,
                "test_suite_id": test_suite_id,
                "test_plan_id": test_plan_id,
                "message": "Test suite linked to plan successfully",
            }
        )
    except Exception as e:
        logging.error(f"Error in link_test_suite_to_plan: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_test_cases_by_use_case(
    use_case_name: str,
    project_area: Optional[str] = None,
) -> str:
    """Get test cases associated with a specific use case.

    Supports test manager workflow: "Show me all test cases for use case X"

    This searches for test cases by:
    1. Category matching the use case name
    2. Title containing the use case name
    3. Description containing the use case name

    Args:
        use_case_name: Use case name or identifier
    """
    try:
        if not use_case_name:
            return json.dumps({"error": "use_case_name is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testcase")

        # Fetch all test cases
        params = {"abbreviate": "false"}
        response = _make_request(endpoint, params=params, timeout=120)

        # Parse and filter
        root = ET.fromstring(response.text)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "ns2": ETM_NAMESPACE,
            "dc": "http://purl.org/dc/elements/1.1/",
        }

        matching_cases = []

        for entry in root.findall(".//atom:entry", ns):
            testcase = entry.find(".//ns2:testcase", ns)
            if testcase is None:
                continue

            # Check category
            category_match = False
            for cat_elem in testcase.findall(".//ns2:category", ns):
                term = cat_elem.get("term", "")
                if use_case_name.lower() in term.lower():
                    category_match = True
                    break

            # Check title
            title_elem = testcase.find(".//dc:title", ns)
            title_match = False
            if title_elem is not None and title_elem.text:
                if use_case_name.lower() in title_elem.text.lower():
                    title_match = True

            # Check description
            desc_elem = testcase.find(".//dc:description", ns)
            desc_match = False
            if desc_elem is not None and desc_elem.text:
                if use_case_name.lower() in desc_elem.text.lower():
                    desc_match = True

            # If any match, include
            if category_match or title_match or desc_match:
                tc_id = testcase.get("{http://purl.org/dc/terms/}identifier", "unknown")
                title = title_elem.text if title_elem is not None else "unknown"

                matching_cases.append(
                    {
                        "test_case_id": tc_id,
                        "title": title,
                        "match_type": "category" if category_match else ("title" if title_match else "description"),
                    }
                )

        return json.dumps(
            {
                "success": True,
                "use_case": use_case_name,
                "count": len(matching_cases),
                "test_cases": matching_cases,
            },
            indent=2,
        )

    except Exception as e:
        logging.error(f"Error in get_test_cases_by_use_case: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_failed_executions_without_defects(
    project_area: Optional[str] = None,
    test_plan_id: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> str:
    """Get failed test executions that don't have defects linked.

    Critical for defect linking workflow - finds failures that need
    manual review or automated defect linking.

    Args:
        test_plan_id: Optional - filter by test plan
        start_date: Optional - YYYY-MM-DD format
        end_date: Optional - YYYY-MM-DD format
    """
    try:
        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "executionresult")

        # Fetch all execution results
        params = {"abbreviate": "false"}
        response = _make_request(endpoint, params=params, accept_type="application/xml", timeout=180)

        # Parse and filter
        root = ET.fromstring(response.text)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "ns2": ETM_NAMESPACE,
        }

        failed_without_defects = []

        for entry in root.findall(".//atom:entry", ns):
            exec_result = entry.find(".//ns2:executionresult", ns)
            if exec_result is None:
                continue

            # Check if failed
            state_elem = exec_result.find(".//ns2:state", ns)
            if state_elem is None or state_elem.text != "com.ibm.rqm.execution.common.state.failed":
                continue

            # Filter by test plan if specified
            if test_plan_id:
                tp_elem = exec_result.find(".//ns2:testplan", ns)
                if tp_elem is not None:
                    href = tp_elem.get("href", "")
                    if test_plan_id not in href:
                        continue
                else:
                    continue

            # Filter by date range
            if start_date or end_date:
                updated_elem = exec_result.find(".//ns2:updated", ns)
                if updated_elem is not None:
                    updated_str = updated_elem.text.split("T")[0]
                    if start_date and updated_str < start_date:
                        continue
                    if end_date and updated_str > end_date:
                        continue

            # Check if defects are linked
            defects = exec_result.findall(".//ns2:relatedworkitem", ns)
            if len(defects) > 0:
                continue  # Has defects, skip

            # Extract key info
            exec_id = exec_result.get("{http://purl.org/dc/terms/}identifier", "unknown")

            tc_elem = exec_result.find(".//ns2:testcase", ns)
            test_case = tc_elem.get("href", "").split(":")[-1] if tc_elem is not None else "unknown"

            updated_elem = exec_result.find(".//ns2:updated", ns)
            updated = updated_elem.text if updated_elem is not None else "unknown"

            failed_without_defects.append(
                {
                    "execution_id": exec_id,
                    "test_case_id": test_case,
                    "updated": updated,
                }
            )

        return json.dumps(
            {
                "success": True,
                "count": len(failed_without_defects),
                "failed_without_defects": failed_without_defects,
            },
            indent=2,
        )

    except Exception as e:
        logging.error(f"Error in get_failed_executions_without_defects: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_execution_defects(
    execution_result_id: str,
    project_area: Optional[str] = None,
) -> str:
    """Get defects linked to a specific execution result.

    Returns list of defect URLs (e.g., JIRA tickets) associated with
    this execution.

    Args:
        execution_result_id: Execution result ID
    """
    try:
        if not execution_result_id:
            return json.dumps({"error": "execution_result_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "executionresult", execution_result_id)

        response = _make_request(endpoint, accept_type="application/xml")
        root = ET.fromstring(response.text)

        ns = {"ns2": ETM_NAMESPACE}

        # Find all related work items (defects)
        defects = []
        for workitem in root.findall(".//ns2:relatedworkitem", ns):
            href = workitem.get("href", "")
            if href:
                defects.append(href)

        return json.dumps(
            {
                "success": True,
                "execution_result_id": execution_result_id,
                "defect_count": len(defects),
                "defects": defects,
            },
            indent=2,
        )

    except Exception as e:
        logging.error(f"Error in get_execution_defects: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def link_defect_to_execution_result(
    execution_result_id: str,
    defect_url: str,
    project_area: Optional[str] = None,
) -> str:
    """Link a defect (JIRA ticket) to a test execution result.

    This creates the ETM-side link to track which defects are associated
    with failed test executions.

    Args:
        execution_result_id: Execution result ID
        defect_url: Full URL to defect (e.g., JIRA ticket URL)
    """
    try:
        if not execution_result_id or not defect_url:
            return json.dumps({"error": "execution_result_id and defect_url are required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "executionresult", execution_result_id)

        # Get current execution result
        response = _make_request(endpoint, accept_type="application/xml")
        root = ET.fromstring(response.text)

        # Add defect reference
        defect_elem = ET.SubElement(root, f"{{{ETM_NAMESPACE}}}relatedworkitem")
        defect_elem.set("href", defect_url)

        updated_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        logging.info(f"Linking defect to execution result:\n{updated_xml.decode('utf-8')}")

        _make_request(
            endpoint,
            method="PUT",
            data=updated_xml,
            accept_type="application/xml",
            content_type="application/xml",
            timeout=60,
        )

        return json.dumps(
            {
                "success": True,
                "execution_result_id": execution_result_id,
                "defect_url": defect_url,
                "message": "Defect linked to execution result successfully",
            }
        )
    except Exception as e:
        logging.error(f"Error in link_defect_to_execution_result: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_test_plan_tree(test_plan_id: str, project_area: Optional[str] = None) -> str:
    """Get complete test plan hierarchy (suites → cases → scripts)."""
    try:
        if not test_plan_id:
            return json.dumps({"error": "test_plan_id is required"})

        project = project_area or ETM_PROJECT_AREA

        # Get test plan details
        plan_response = _make_request(
            _build_resource_url(project, "testplan", test_plan_id), accept_type="application/xml"
        )
        plan_root = ET.fromstring(plan_response.text)

        ns = {"ns2": ETM_NAMESPACE, "dc": "http://purl.org/dc/elements/1.1/"}

        title_elem = plan_root.find(".//dc:title", ns)
        plan_title = title_elem.text if title_elem is not None else "Unknown"

        tree = {"test_plan": {"id": test_plan_id, "title": plan_title, "test_suites": [], "direct_test_cases": []}}

        # Process test suites
        for testsuite_elem in plan_root.findall(".//ns2:testsuite", ns):
            suite_href = testsuite_elem.get("href", "")
            if not suite_href:
                continue

            suite_id = suite_href.split(":")[-1] if ":" in suite_href else suite_href.split("/")[-1]
            suite_response = _make_request(
                _build_resource_url(project, "testsuite", suite_id), accept_type="application/xml"
            )
            suite_root = ET.fromstring(suite_response.text)

            suite_title_elem = suite_root.find(".//dc:title", ns)
            suite_data = {
                "id": suite_id,
                "title": suite_title_elem.text if suite_title_elem is not None else "Unknown",
                "test_cases": [],
            }

            # Process test cases in suite
            for testcase_elem in suite_root.findall(".//ns2:testcase", ns):
                case_href = testcase_elem.get("href", "")
                if not case_href:
                    continue

                case_id = case_href.split(":")[-1] if ":" in case_href else case_href.split("/")[-1]
                case_response = _make_request(
                    _build_resource_url(project, "testcase", case_id), accept_type="application/xml"
                )
                case_root = ET.fromstring(case_response.text)

                case_title_elem = case_root.find(".//dc:title", ns)
                case_data = {
                    "id": case_id,
                    "title": case_title_elem.text if case_title_elem is not None else "Unknown",
                    "test_scripts": [
                        {"id": script_elem.get("href", "").split(":")[-1]}
                        for script_elem in case_root.findall(".//ns2:testscript", ns)
                        if script_elem.get("href")
                    ],
                }

                suite_data["test_cases"].append(case_data)

            tree["test_plan"]["test_suites"].append(suite_data)

        # Calculate statistics
        total_suites = len(tree["test_plan"]["test_suites"])
        total_cases = sum(len(suite["test_cases"]) for suite in tree["test_plan"]["test_suites"])
        total_scripts = sum(
            len(case["test_scripts"]) for suite in tree["test_plan"]["test_suites"] for case in suite["test_cases"]
        )

        tree["statistics"] = {"total_suites": total_suites, "total_cases": total_cases, "total_scripts": total_scripts}

        return json.dumps(tree, indent=2)
    except Exception as e:
        return _handle_error("get_test_plan_tree", e)


@mcp.tool()
def get_execution_timeline(test_plan_id: str, days_back: int = 30, project_area: Optional[str] = None) -> str:
    """Get execution results over time for trend analysis."""
    try:
        if not test_plan_id:
            return json.dumps({"error": "test_plan_id is required"})
        if not (1 <= days_back <= 365):
            return json.dumps({"error": "days_back must be between 1 and 365"})

        project = project_area or ETM_PROJECT_AREA

        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        start_date_str = start_date.strftime("%Y-%m-%d")

        # Get execution results
        endpoint = _build_resource_url(project, "executionresult")
        response = _make_request(endpoint, params={"abbreviate": "false"}, accept_type="application/xml", timeout=180)

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "ns2": ETM_NAMESPACE}

        daily_stats = {}

        for entry in root.findall(".//atom:entry", ns):
            exec_result = entry.find(".//ns2:executionresult", ns)
            if exec_result is None:
                continue

            # Filter by test plan
            tp_elem = exec_result.find(".//ns2:testplan", ns)
            if tp_elem is None or test_plan_id not in tp_elem.get("href", ""):
                continue

            # Get execution date
            updated_elem = exec_result.find(".//ns2:updated", ns)
            if updated_elem is None or not updated_elem.text:
                continue

            exec_date = updated_elem.text.split("T")[0]
            if exec_date < start_date_str:
                continue

            # Initialize stats for date
            if exec_date not in daily_stats:
                daily_stats[exec_date] = {"total": 0, "passed": 0, "failed": 0, "blocked": 0, "incomplete": 0}

            daily_stats[exec_date]["total"] += 1

            # Categorize by state
            state_elem = exec_result.find(".//ns2:state", ns)
            if state_elem is not None:
                state = state_elem.text.lower()
                if "passed" in state:
                    daily_stats[exec_date]["passed"] += 1
                elif "failed" in state:
                    daily_stats[exec_date]["failed"] += 1
                elif "blocked" in state:
                    daily_stats[exec_date]["blocked"] += 1
                else:
                    daily_stats[exec_date]["incomplete"] += 1

        # Build timeline with missing days filled
        timeline = []
        current_date = start_date
        total_executions = total_passed = 0

        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")

            if date_str in daily_stats:
                day_data = daily_stats[date_str]
                pass_rate = (day_data["passed"] / day_data["total"] * 100) if day_data["total"] > 0 else 0
            else:
                day_data = {"total": 0, "passed": 0, "failed": 0, "blocked": 0, "incomplete": 0}
                pass_rate = 0

            timeline.append(
                {
                    "date": date_str,
                    "executions": day_data["total"],
                    "passed": day_data["passed"],
                    "failed": day_data["failed"],
                    "blocked": day_data["blocked"],
                    "incomplete": day_data["incomplete"],
                    "pass_rate": round(pass_rate, 2),
                }
            )

            total_executions += day_data["total"]
            total_passed += day_data["passed"]
            current_date += timedelta(days=1)

        overall_pass_rate = (total_passed / total_executions * 100) if total_executions > 0 else 0

        return json.dumps(
            {
                "success": True,
                "test_plan_id": test_plan_id,
                "period": f"{days_back} days",
                "summary": {"total_executions": total_executions, "overall_pass_rate": round(overall_pass_rate, 2)},
                "timeline": timeline,
            },
            indent=2,
        )
    except Exception as e:
        return _handle_error("get_execution_timeline", e)


@mcp.tool()
def get_requirement_to_test_mapping(project_area: Optional[str] = None) -> str:
    """Get complete requirements → test cases traceability matrix."""
    try:
        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "testcase")
        response = _make_request(endpoint, params={"abbreviate": "false"}, accept_type="application/xml", timeout=180)

        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "ns2": ETM_NAMESPACE, "dc": "http://purl.org/dc/elements/1.1/"}

        requirement_mapping = {}
        orphaned_test_cases = []

        for entry in root.findall(".//atom:entry", ns):
            testcase = entry.find(".//ns2:testcase", ns)
            if testcase is None:
                continue

            # Get test case info
            tc_id_elem = testcase.find(".//dcterms:identifier", {"dcterms": "http://purl.org/dc/terms/"})
            tc_id = tc_id_elem.text if tc_id_elem is not None else "unknown"

            title_elem = testcase.find(".//dc:title", ns)
            tc_title = title_elem.text if title_elem is not None else "Unknown"

            test_case_data = {"id": tc_id, "title": tc_title}

            # Find requirement links
            requirement_links = [
                elem.get("href", "") for elem in testcase.findall(".//ns2:validates", ns) if elem.get("href")
            ]

            if requirement_links:
                for req_href in requirement_links:
                    req_id = req_href.split("/")[-1] if "/" in req_href else req_href
                    if req_id not in requirement_mapping:
                        requirement_mapping[req_id] = {"requirement_id": req_id, "test_cases": [], "coverage_count": 0}

                    requirement_mapping[req_id]["test_cases"].append(test_case_data)
                    requirement_mapping[req_id]["coverage_count"] += 1
            else:
                orphaned_test_cases.append(test_case_data)

        requirements = sorted(requirement_mapping.values(), key=lambda x: x["coverage_count"], reverse=True)

        coverage_analysis = {
            "total_requirements": len(requirements),
            "orphaned_test_cases": len(orphaned_test_cases),
            "over_tested_requirements": len([req for req in requirements if req["coverage_count"] > 3]),
        }

        return json.dumps(
            {
                "success": True,
                "project_area": project,
                "coverage_analysis": coverage_analysis,
                "requirements": requirements[:20],
                "orphaned_test_cases": orphaned_test_cases[:10],
            },
            indent=2,
        )
    except Exception as e:
        return _handle_error("get_requirement_to_test_mapping", e)


@mcp.tool()
def find_orphaned_test_cases(project_area: Optional[str] = None) -> str:
    """Find test cases not linked to any requirements or test plans."""
    try:
        project = project_area or ETM_PROJECT_AREA

        # Get all resources in parallel-like fashion
        testcase_response = _make_request(
            _build_resource_url(project, "testcase"),
            params={"abbreviate": "false"},
            accept_type="application/xml",
            timeout=180,
        )
        testplan_response = _make_request(
            _build_resource_url(project, "testplan"),
            params={"abbreviate": "false"},
            accept_type="application/xml",
            timeout=180,
        )

        ns = {"atom": "http://www.w3.org/2005/Atom", "ns2": ETM_NAMESPACE, "dc": "http://purl.org/dc/elements/1.1/"}

        # Parse test cases
        testcase_root = ET.fromstring(testcase_response.text)
        all_test_cases = {}

        for entry in testcase_root.findall(".//atom:entry", ns):
            testcase = entry.find(".//ns2:testcase", ns)
            if testcase is None:
                continue

            tc_id_elem = testcase.find(".//dcterms:identifier", {"dcterms": "http://purl.org/dc/terms/"})
            tc_id = tc_id_elem.text if tc_id_elem is not None else None
            if not tc_id:
                continue

            title_elem = testcase.find(".//dc:title", ns)
            has_requirements = len(testcase.findall(".//ns2:validates", ns)) > 0

            all_test_cases[tc_id] = {
                "id": tc_id,
                "title": title_elem.text if title_elem is not None else "Unknown",
                "has_requirements": has_requirements,
                "in_test_plans": [],
            }

        # Check test plan references
        testplan_root = ET.fromstring(testplan_response.text)
        for entry in testplan_root.findall(".//atom:entry", ns):
            testplan = entry.find(".//ns2:testplan", ns)
            if testplan is None:
                continue

            for testcase_ref in testplan.findall(".//ns2:testcase", ns):
                href = testcase_ref.get("href", "")
                if href:
                    referenced_tc_id = href.split(":")[-1] if ":" in href else href.split("/")[-1]
                    if referenced_tc_id in all_test_cases:
                        all_test_cases[referenced_tc_id]["in_test_plans"].append({"href": href})

        # Categorize orphans
        orphaned_categories = {"no_requirements": [], "no_test_plans": [], "completely_isolated": []}

        for tc_data in all_test_cases.values():
            if not tc_data["has_requirements"]:
                orphaned_categories["no_requirements"].append(tc_data)
            if not tc_data["in_test_plans"]:
                orphaned_categories["no_test_plans"].append(tc_data)
            if not tc_data["has_requirements"] and not tc_data["in_test_plans"]:
                orphaned_categories["completely_isolated"].append(tc_data)

        statistics = {
            "total_test_cases": len(all_test_cases),
            "no_requirements_count": len(orphaned_categories["no_requirements"]),
            "no_test_plans_count": len(orphaned_categories["no_test_plans"]),
            "completely_isolated_count": len(orphaned_categories["completely_isolated"]),
            "orphan_percentage": round((len(orphaned_categories["completely_isolated"]) / len(all_test_cases) * 100), 2)
            if all_test_cases
            else 0,
        }

        return json.dumps(
            {
                "success": True,
                "project_area": project,
                "statistics": statistics,
                "orphaned_categories": {
                    "completely_isolated": orphaned_categories["completely_isolated"][:10],  # Most critical
                    "no_requirements": orphaned_categories["no_requirements"][:15],
                    "no_test_plans": orphaned_categories["no_test_plans"][:15],
                },
                "recommendations": {
                    "high_priority": "Review completely isolated test cases - they may be obsolete",
                    "medium_priority": "Add requirement traceability to test cases without links",
                    "low_priority": "Organize test cases into appropriate test plans",
                },
            },
            indent=2,
        )
    except Exception as e:
        return _handle_error("find_orphaned_test_cases", e)


# ============================================================================
# HELPER FUNCTIONS FOR ADVANCED TOOLS
# ============================================================================


@mcp.tool()
def get_execution_results_by_test_plan(test_plan_id: str, project_area: Optional[str] = None) -> str:
    """Get all execution results for a specific test plan."""
    try:
        if not test_plan_id:
            return json.dumps({"error": "test_plan_id is required"})

        project = project_area or ETM_PROJECT_AREA
        endpoint = _build_resource_url(project, "executionresult")

        params = {"abbreviate": "false"}
        response = _make_request(endpoint, params=params, accept_type="application/xml", timeout=180)

        # Filter by test plan on client side
        root = ET.fromstring(response.text)
        ns = {"atom": "http://www.w3.org/2005/Atom", "ns2": ETM_NAMESPACE}

        # Remove entries that don't match the test plan
        entries = root.findall(".//atom:entry", ns)
        matched_entries = []

        for entry in entries:
            exec_result = entry.find(".//ns2:executionresult", ns)
            if exec_result is None:
                continue

            # Check if belongs to test plan
            tp_elem = exec_result.find(".//ns2:testplan", ns)
            if tp_elem is not None:
                href = tp_elem.get("href", "")
                if test_plan_id in href:
                    matched_entries.append(entry)

        # Remove all entries and add only matched ones
        for entry in entries:
            root.remove(entry)
        for entry in matched_entries:
            root.append(entry)

        # Update count
        total_results = root.find(".//atom:totalResults", ns)
        if total_results is not None:
            total_results.text = str(len(matched_entries))

        filtered_xml = ET.tostring(root, encoding="unicode")
        return filtered_xml

    except Exception as e:
        return _handle_error("get_execution_results_by_test_plan", e)


# ============================================================================
# BULK OPERATIONS (Optional - for advanced users)
# ============================================================================


@mcp.tool()
def bulk_create_test_cases(test_cases_data: list, project_area: Optional[str] = None) -> str:
    """Create multiple test cases in batch."""
    try:
        if not test_cases_data or not isinstance(test_cases_data, list):
            return json.dumps({"error": "test_cases_data must be a non-empty list"})

        project = project_area or ETM_PROJECT_AREA
        results = {"success": [], "failed": []}

        for i, tc_data in enumerate(test_cases_data):
            try:
                if not isinstance(tc_data, dict) or "title" not in tc_data:
                    results["failed"].append({"index": i, "error": "Missing title"})
                    continue

                title = tc_data["title"]
                description = tc_data.get("description", "")

                result = create_test_case(title, description, project)
                result_data = json.loads(result)

                if result_data.get("success"):
                    results["success"].append(
                        {"index": i, "title": title, "test_case_id": result_data.get("test_case_id")}
                    )
                else:
                    results["failed"].append(
                        {"index": i, "title": title, "error": result_data.get("error", "Unknown error")}
                    )

            except Exception as e:
                results["failed"].append({"index": i, "error": str(e)})

        return json.dumps(
            {
                "success": True,
                "total_requested": len(test_cases_data),
                "created": len(results["success"]),
                "failed": len(results["failed"]),
                "results": results,
            },
            indent=2,
        )

    except Exception as e:
        return _handle_error("bulk_create_test_cases", e)


@mcp.tool()
def bulk_execute_tests(execution_requests: list, project_area: Optional[str] = None) -> str:
    """Execute multiple tests in batch."""
    try:
        if not execution_requests or not isinstance(execution_requests, list):
            return json.dumps({"error": "execution_requests must be a non-empty list"})

        project = project_area or ETM_PROJECT_AREA
        results = {"success": [], "failed": []}

        for i, exec_data in enumerate(execution_requests):
            try:
                if not isinstance(exec_data, dict) or "test_case_id" not in exec_data or "result" not in exec_data:
                    results["failed"].append({"index": i, "error": "Missing test_case_id or result"})
                    continue

                test_case_id = exec_data["test_case_id"]
                result = exec_data["result"]
                test_plan_id = exec_data.get("test_plan_id")
                executed_by = exec_data.get("executed_by")
                comments = exec_data.get("comments")

                exec_result = create_execution_record(
                    test_case_id, result, project, test_plan_id, executed_by, comments
                )
                exec_result_data = json.loads(exec_result)

                if exec_result_data.get("success"):
                    results["success"].append(
                        {
                            "index": i,
                            "test_case_id": test_case_id,
                            "result": result,
                            "execution_result_id": exec_result_data.get("execution_result_id"),
                        }
                    )
                else:
                    results["failed"].append(
                        {
                            "index": i,
                            "test_case_id": test_case_id,
                            "error": exec_result_data.get("error", "Unknown error"),
                        }
                    )

            except Exception as e:
                results["failed"].append({"index": i, "error": str(e)})

        return json.dumps(
            {
                "success": True,
                "total_requested": len(execution_requests),
                "executed": len(results["success"]),
                "failed": len(results["failed"]),
                "results": results,
            },
            indent=2,
        )

    except Exception as e:
        return _handle_error("bulk_execute_tests", e)


# ============================================================================
# SIMPLIFIED RESOURCE OPERATIONS (using generic functions)
# ============================================================================


# Test Scripts
@mcp.tool()
def list_test_scripts(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List test scripts."""
    return _generic_list("testscript", project_area, limit)


@mcp.tool()
def get_test_script(test_script_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test script."""
    return _generic_get("testscript", test_script_id, project_area)


@mcp.tool()
def create_test_script(
    title: str, description: str, project_area: Optional[str] = None, steps: Optional[str] = None
) -> str:
    """Create a new test script."""
    extra = {}
    if steps:
        extra["steps"] = f"<div xmlns='http://www.w3.org/1999/xhtml'>{escape(steps)}</div>"
    return _generic_create("testscript", title, description, project_area, **extra)


# Build Records
@mcp.tool()
def list_build_records(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List build records."""
    return _generic_list("buildrecord", project_area, limit)


@mcp.tool()
def get_build_record(build_id: str, project_area: Optional[str] = None) -> str:
    """Get build record information."""
    return _generic_get("buildrecord", build_id, project_area)


# Configurations
@mcp.tool()
def list_configurations(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List test configurations."""
    return _generic_list("configuration", project_area, limit)


@mcp.tool()
def get_configuration(config_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test configuration."""
    return _generic_get("configuration", config_id, project_area)


# Test Execution Records (TCER)
@mcp.tool()
def list_test_execution_records(project_area: Optional[str] = None, limit: int = 50) -> str:
    """List test execution records (TCER)."""
    return _generic_list("executionworkitem", project_area, limit)


@mcp.tool()
def get_test_execution_record(test_record_id: str, project_area: Optional[str] = None) -> str:
    """Get detailed information about a specific test execution record (TCER)."""
    return _generic_get("executionworkitem", test_record_id, project_area)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)

    # Start the MCP server (default: stdio)
    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
