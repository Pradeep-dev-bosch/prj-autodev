"""MCP server for IBM DNG Requirements Management (RM).

This server provides comprehensive tools to interact with IBM DNG via REST API,
supporting requirements, modules, views, collections, and reportable REST API operations.

Environment Variables Required:
================================
- DNG_SERVER: Base URL of the DNG server (e.g., https://rb-alm-13-q.de.bosch.com/)
- DNG_USERNAME: Username for authentication
- DNG_PASSWORD: Password for authentication
- DNG_VERIFY_SSL: (Optional) Set to 'false' to disable SSL verification
- TRANSPORT: (Optional) Transport type, defaults to 'stdio'
- HOST: (Optional) Host for non-stdio transport
- HOST_PORT: (Optional) Port for non-stdio transport

Documentation Reference:
========================
https://jazz.net/wiki/bin/view/Main/DNGReportableRestAPI
"""

import json
import logging
import os
import xml.etree.ElementTree as ET
from typing import Any, Optional
from urllib.parse import urlencode

import requests
from fastmcp import FastMCP

# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

# Initialize MCP server
mcp = FastMCP("DNG-RM-Server")

# IBM DNG connection details
DNG_SERVER = os.getenv("DNG_SERVER", "").rstrip("/")
DNG_USERNAME = os.getenv("DNG_USERNAME", "")
DNG_PASSWORD = os.getenv("DNG_PASSWORD", "")
DNG_VERIFY_SSL = os.getenv("DNG_VERIFY_SSL", "true").lower() == "true"

# API endpoints
DNG_PUBLISH_PATH = "/rm/publish"
DNG_ROOT_SERVICES = "/rm/rootservices"
DNG_CATALOG = "/rm/oslc_rm/catalog"

# XML namespaces
DNG_NAMESPACES = {
    "ds": "http://jazz.net/xmlns/alm/rm/datasource/v0.1",
    "rrm": "http://www.ibm.com/xmlns/rrm/1.0/",
    "attribute": "http://jazz.net/xmlns/alm/rm/attribute/v0.1",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "oslc": "http://open-services.net/ns/core#",
    "oslc_rm": "http://open-services.net/ns/rm#",
    "dcterms": "http://purl.org/dc/terms/",
    "rm": "http://jazz.net/ns/rm#",
    "nav": "http://jazz.net/ns/rm/navigation#",
    "public_rm": "http://com.ibm.rdm/navigation#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "jp": "http://jazz.net/xmlns/prod/jazz/process/0.6/",
}

# Request timeouts (in seconds)
DEFAULT_TIMEOUT = 120
LONG_TIMEOUT = 180
SHORT_TIMEOUT = 30

# Validate environment variables
missing_vars = [
    name
    for name, value in {
        "DNG_SERVER": DNG_SERVER,
        "DNG_USERNAME": DNG_USERNAME,
        "DNG_PASSWORD": DNG_PASSWORD,
    }.items()
    if not value
]
if missing_vars:
    raise ValueError(f"Missing required environment variable(s): {', '.join(missing_vars)}")

# Configure SSL verification
if not DNG_VERIFY_SSL:
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    logging.warning("SSL certificate verification is disabled. This is not recommended for production.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _get_headers(accept_type: str = "application/rdf+xml") -> dict[str, str]:
    """Generate standard headers for DNG API requests.

    Args:
        accept_type: The Accept header value for the response format

    Returns:
        Dictionary of HTTP headers
    """
    return {
        "Accept": accept_type,
        "OSLC-Core-Version": "2.0",
        "X-Jazz-CSRF-Prevent": "true",  # Required for POST/PUT/DELETE operations
    }


def _build_url(artifact_format: str, params: Optional[dict[str, Any]] = None) -> str:
    """Build the DNG publish URL with query parameters.

    Args:
        artifact_format: The artifact format endpoint (e.g., 'resources', 'text')
        params: Optional query parameters dictionary

    Returns:
        Fully constructed URL with encoded parameters
    """
    base_url = f"{DNG_SERVER}{DNG_PUBLISH_PATH}/{artifact_format}"
    if params:
        # Filter out None values
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            base_url += "?" + urlencode(params, safe=",")
    return base_url


def _make_request(
    url: str,
    method: str = "GET",
    headers: Optional[dict[str, str]] = None,
    data: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> requests.Response:
    """Make an HTTP request to the DNG API.

    Args:
        url: The target URL
        method: HTTP method (GET, POST, PUT, DELETE)
        headers: Optional additional headers
        data: Optional request body data
        timeout: Request timeout in seconds

    Returns:
        Response object

    Raises:
        requests.exceptions.RequestException: On request failure
    """
    request_headers = _get_headers()
    if headers:
        request_headers.update(headers)

    try:
        response = requests.request(
            method,
            url,
            headers=request_headers,
            auth=(DNG_USERNAME, DNG_PASSWORD),
            data=data,
            verify=DNG_VERIFY_SSL,
            timeout=timeout,
        )
        logging.info(f"{method} {url} - Status: {response.status_code}")
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        if hasattr(e, "response") and e.response is not None:
            logging.error(f"Response: {e.response.status_code} - {e.response.text[:500]}")
        raise


def _handle_error(func_name: str, e: Exception) -> str:
    """Standardized error handling for tool functions.

    Args:
        func_name: Name of the function where error occurred
        e: The exception object

    Returns:
        JSON-formatted error message
    """
    error_msg = str(e)
    logging.error(f"Error in {func_name}: {error_msg}", exc_info=True)

    # common errors
    if isinstance(e, requests.exceptions.HTTPError):
        if hasattr(e, "response") and e.response is not None:
            status_code = e.response.status_code
            if status_code == 401:
                error_msg = "Authentication failed. Check DNG_USERNAME and DNG_PASSWORD."
            elif status_code == 403:
                error_msg = "Access forbidden. Insufficient permissions."
            elif status_code == 404:
                error_msg = "Resource not found. Check the URI."
            elif status_code == 412:
                error_msg = "Precondition failed. Resource was modified by another user."

    return json.dumps({"error": error_msg, "function": func_name})


def _extract_text_or_empty(element: Optional[ET.Element]) -> str:
    """Extract text from an XML element or return empty string if None.

    Args:
        element: XML element or None

    Returns:
        Extracted text content or empty string
    """
    if element is not None and element.text:
        return element.text.strip()
    return ""


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.

    Returns:
        Tuple of (transport, host, port)

    Raises:
        ValueError: If port is invalid
    """
    transport = os.getenv("TRANSPORT", "").strip()

    # Default to stdio for empty or placeholder values
    if transport in ["stdio", "<TRANSPORT>", "", "-", "null"]:
        logging.info("MCP init: transport=stdio")
        return ("stdio", "", 0)

    host = os.getenv("HOST", "127.0.0.1").strip()
    port_str = os.getenv("HOST_PORT", "8000").strip()

    # Handle placeholder values
    if host in ["<HOST>", ""]:
        host = "127.0.0.1"
    if port_str in ["<HOST_PORT>", ""]:
        port_str = "8000"

    try:
        port = int(port_str)
        if port < 1 or port > 65535:
            raise ValueError(f"Port must be between 1 and 65535, got {port}")
    except ValueError as e:
        raise ValueError(f"Invalid HOST_PORT environment variable: '{port_str}' - {str(e)}")

    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def _get_service_provider_url(project_uri: str) -> Optional[str]:
    """Get the service provider URL for a project.

    Args:
        project_uri: Project area URI

    Returns:
        Service provider URL with /services.xml path, or None if invalid
    """
    if not project_uri or "/process/project-areas/" not in project_uri:
        logging.error(f"Invalid project_uri format: {project_uri}")
        return None

    # Extract project UUID and build service provider URL
    project_uuid = project_uri.split("/process/project-areas/")[-1]
    return f"{DNG_SERVER}/rm/oslc_rm/{project_uuid}/services.xml"


def _discover_creation_factory(project_uri: str) -> Optional[tuple[str, list[str]]]:
    """Discover the requirement creation factory and resource shapes.

    Args:
        project_uri: The project URI

    Returns:
        Tuple of (creation_factory_url, list of resource_shape_urls) or None
    """
    try:
        service_provider_url = _get_service_provider_url(project_uri)
        if not service_provider_url:
            return None

        response = _make_request(service_provider_url, timeout=SHORT_TIMEOUT)
        root = ET.fromstring(response.text)

        # Find creation factory for requirements
        for factory in root.findall(".//oslc:CreationFactory", DNG_NAMESPACES):
            resource_types = factory.findall(".//oslc:resourceType", DNG_NAMESPACES)

            for rt in resource_types:
                rt_value = rt.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", "")
                if "Requirement" in rt_value and "Collection" not in rt_value:
                    # Found requirement creation factory
                    creation_elem = factory.find(".//oslc:creation", DNG_NAMESPACES)
                    if creation_elem is not None:
                        factory_url = creation_elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", "")

                        # Get resource shapes
                        shape_elems = factory.findall(".//oslc:resourceShape", DNG_NAMESPACES)
                        shapes = [
                            shape.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", "")
                            for shape in shape_elems
                        ]

                        logging.info(f"Found creation factory: {factory_url}")
                        return (factory_url, shapes)

        logging.error(f"No requirement creation factory found for project: {project_uri}")
        return None

    except ET.ParseError as e:
        logging.error(f"XML parsing error in creation factory discovery: {e}")
        return None
    except Exception as e:
        logging.error(f"Error discovering creation factory: {e}")
        return None


def _discover_query_capability(project_uri: str) -> Optional[str]:
    """Discover the OSLC query capability base URL for requirements in a project.

    Args:
        project_uri: The project URI

    Returns:
        Query base URL for requirements or None
    """
    try:
        service_provider_url = _get_service_provider_url(project_uri)
        if not service_provider_url:
            return None

        response = _make_request(service_provider_url, timeout=SHORT_TIMEOUT)
        root = ET.fromstring(response.text)

        # Find query capability specifically for Requirements
        for query_cap in root.findall(".//oslc:QueryCapability", DNG_NAMESPACES):
            # Check if this query capability is for Requirements
            resource_types = query_cap.findall(".//oslc:resourceType", DNG_NAMESPACES)

            is_requirement_query = False
            for rt in resource_types:
                rt_value = rt.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", "")
                # Look for Requirement resource type, but exclude RequirementCollection
                if "Requirement" in rt_value and "Collection" not in rt_value:
                    is_requirement_query = True
                    break

            if not is_requirement_query:
                continue

            # Found requirement query capability
            query_base_elem = query_cap.find(".//oslc:queryBase", DNG_NAMESPACES)
            if query_base_elem is not None:
                query_url = query_base_elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", "")
                logging.info(f"Found requirement query capability: {query_url}")
                return query_url

        logging.error(f"No requirement query capability found for project: {project_uri}")
        return None

    except ET.ParseError as e:
        logging.error(f"XML parsing error in query capability discovery: {e}")
        return None
    except Exception as e:
        logging.error(f"Error discovering query capability: {e}")
        return None


def _build_requirement_rdf(
    title: str,
    primary_text: Optional[str] = None,
    artifact_type: Optional[str] = None,
    folder_uri: Optional[str] = None,
    attributes: Optional[dict[str, Any]] = None,
) -> str:
    """Build RDF/XML for a requirement resource following OSLC RM specification.

    Args:
        title: Requirement title
        primary_text: Optional description/primary text
        artifact_type: Optional artifact type URI
        folder_uri: Optional parent folder URI
        attributes: Optional custom attributes dictionary

    Returns:
        RDF/XML string representation
    """
    # Escape XML special characters in text content
    from xml.sax.saxutils import escape

    rdf_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        "<rdf:RDF",
        '    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
        '    xmlns:dcterms="http://purl.org/dc/terms/"',
        '    xmlns:oslc="http://open-services.net/ns/core#"',
        '    xmlns:oslc_rm="http://open-services.net/ns/rm#"',
        '    xmlns:nav="http://jazz.net/ns/rm/navigation#">',
        '    <rdf:Description rdf:about="">',
        '        <rdf:type rdf:resource="http://open-services.net/ns/rm#Requirement"/>',
        f'        <dcterms:title rdf:parseType="Literal">{escape(title)}</dcterms:title>',
    ]

    if primary_text:
        rdf_parts.append(
            f'        <dcterms:description rdf:parseType="Literal">{escape(primary_text)}</dcterms:description>'
        )

    if artifact_type:
        rdf_parts.append(f'        <oslc:instanceShape rdf:resource="{escape(artifact_type)}"/>')

    if folder_uri:
        rdf_parts.append(f'        <nav:parent rdf:resource="{escape(folder_uri)}"/>')

    # Add custom attributes
    if attributes:
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, str):
                rdf_parts.append(f"        <{attr_name}>{escape(attr_value)}</{attr_name}>")
            elif isinstance(attr_value, dict) and "uri" in attr_value:
                rdf_parts.append(f'        <{attr_name} rdf:resource="{escape(attr_value["uri"])}"/>')

    rdf_parts.extend(["    </rdf:Description>", "</rdf:RDF>"])

    return "\n".join(rdf_parts)


# ============================================================================
# GENERIC RESOURCE OPERATIONS
# ============================================================================


def _generic_get_resources(
    artifact_format: str = "resources",
    params: Optional[dict[str, Any]] = None,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """Generic function to get resources with optional parameters.

    Args:
        artifact_format: The artifact format endpoint
        params: Optional query parameters
        timeout: Request timeout in seconds

    Returns:
        XML response text or JSON error
    """
    try:
        url = _build_url(artifact_format, params)
        response = _make_request(url, timeout=timeout)
        return response.text
    except Exception as e:
        return _handle_error(f"get_resources_{artifact_format}", e)


# ============================================================================
# TOOLS - SCHEMA & METADATA
# ============================================================================


@mcp.tool()
def get_schema(artifact_format: str = "resources") -> str:
    """Get the generated schema for a service context.

    Args:
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML schema definition for the specified service context
    """
    return _generic_get_resources(artifact_format, {"metadata": "schema"}, timeout=SHORT_TIMEOUT)


# ============================================================================
# TOOLS - RESOURCE RETRIEVAL
# ============================================================================


@mcp.tool()
def get_resources_by_project(project_uri: str, artifact_format: str = "resources") -> str:
    """Get base resource information for all accessible resources in a project.

    Args:
        project_uri: The project URI or project UUID
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML response with resource information (paginated, default 100 per page)
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required and must not be empty"})

    return _generic_get_resources(artifact_format, {"projectURI": project_uri})


@mcp.tool()
def get_resources_by_ids(resource_uri: str, artifact_format: str = "resources") -> str:
    """Get base resource information for specified resource IDs.

    Args:
        resource_uri: The resource URI or comma-separated list of URIs
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML response with resource information
    """
    if not resource_uri or not resource_uri.strip():
        return json.dumps({"error": "resource_uri is required and must not be empty"})

    return _generic_get_resources(artifact_format, {"resourceURI": resource_uri})


# ============================================================================
# TOOLS - CONSOLIDATED FILTERING
# ============================================================================


@mcp.tool()
def get_resources_filtered(
    artifact_format: str = "resources",
    project_uri: Optional[str] = None,
    view_uri: Optional[str] = None,
    view_name: Optional[str] = None,
    type_uri: Optional[str] = None,
    type_name: Optional[str] = None,
    attribute_uris: Optional[str] = None,
    module_uri: Optional[str] = None,
    resource_uri: Optional[str] = None,
) -> str:
    """Get resources with various filtering options (view, type, attributes, module).

    This consolidated tool supports multiple filtering strategies that can be combined:
    - Filter by saved view (URI or name)
    - Filter by artifact type (URI or name)
    - Filter specific attributes to include in response
    - Filter by module membership
    - Filter by specific resource URI

    Args:
        artifact_format: The artifact format type (default: 'resources')
        project_uri: The project URI (required for view_name or type_name)
        view_uri: URI of a saved view to filter by
        view_name: Name of a saved view (requires project_uri)
        type_uri: URI of an artifact type to filter by
        type_name: Name of an artifact type (requires project_uri)
        attribute_uris: Comma-separated list of attribute URIs to include in response
        module_uri: URI of a module to filter artifacts by
        resource_uri: Specific resource URI(s) to retrieve

    Returns:
        XML response with filtered resources
    """
    # Validate parameter combinations
    if view_name and not project_uri:
        return json.dumps({"error": "view_name requires project_uri"})

    if type_name and not project_uri:
        return json.dumps({"error": "type_name requires project_uri"})

    # Build parameters dictionary
    params = {}

    if project_uri:
        params["projectURI"] = project_uri

    # View filtering
    if view_uri:
        params["viewURI"] = view_uri
    elif view_name:
        params["viewName"] = view_name

    # Type filtering
    if type_uri:
        params["typeURI"] = type_uri
    elif type_name:
        params["typeName"] = type_name

    # Attribute filtering
    if attribute_uris:
        params["attributeURI"] = attribute_uris

    # Module filtering
    if module_uri:
        params["moduleURI"] = module_uri

    # Resource filtering
    if resource_uri:
        params["resourceURI"] = resource_uri

    # Ensure at least one filter is provided
    if not params:
        return json.dumps({"error": "At least one filter parameter must be provided"})

    return _generic_get_resources(artifact_format, params)


# ============================================================================
# TOOLS - COLLECTIONS
# ============================================================================


@mcp.tool()
def get_collection_uri(collection_uri: str, artifact_format: str = "resources") -> str:
    """Get resource revisions associated with a specific collection.

    Args:
        collection_uri: The URI of the collection
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML response with collection resource revisions
    """
    if not collection_uri:
        return json.dumps({"error": "collection_uri is required"})
    return _generic_get_resources(artifact_format, {"collectionURI": collection_uri})


# ============================================================================
# TOOLS - TEXT FORMAT & EMBEDDED ARTIFACTS
# ============================================================================


@mcp.tool()
def get_text_with_embed_titles(resource_uri: Optional[str] = None, show_embed_titles: bool = True) -> str:
    """Get text format with embedded artifact titles displayed.

    Args:
        resource_uri: Optional specific resource URI
        show_embed_titles: Whether to display titles of embedded artifacts (default: True)

    Returns:
        Text format response with embedded artifact titles
    """
    params = {}
    if resource_uri:
        params["resourceURI"] = resource_uri
    if show_embed_titles:
        params["showEmbedTitles"] = "true"
    return _generic_get_resources("text", params)


@mcp.tool()
def get_text_with_expanded_embeds(
    resource_uri: Optional[str] = None, maximise_embeds: bool = True, show_embed_titles: bool = False
) -> str:
    """Get text format with embedded artifacts fully expanded.

    Args:
        resource_uri: Optional specific resource URI
        maximise_embeds: Whether to expand embedded artifacts to full content (default: True)
        show_embed_titles: Whether to display titles of embedded artifacts (default: False)

    Returns:
        Text format response with expanded embedded artifacts
    """
    params = {}
    if resource_uri:
        params["resourceURI"] = resource_uri
    if maximise_embeds:
        params["maximiseEmbeds"] = "true"
    if show_embed_titles:
        params["showEmbedTitles"] = "true"
    return _generic_get_resources("text", params)


# ============================================================================
# TOOLS - LINK TYPES & MODIFICATION TRACKING (ETL)
# ============================================================================


@mcp.tool()
def get_modified_since(modified_since: str, artifact_format: str = "resources", links_only: bool = False) -> str:
    """Get resources modified since a specific timestamp.

    Args:
        modified_since: ISO 8601 timestamp (format: yyyy-MM-dd'T'HH:mm:ss.SSS'Z')
        artifact_format: The artifact format type (default: 'resources')
        links_only: If True, only return link changes (default: False)

    Returns:
        XML response with modified resources

    Note:
        Commonly used for ETL operations to track changes and synchronize data.
    """
    if not modified_since:
        return json.dumps({"error": "modified_since is required"})

    params = {"modifiedSince": modified_since}
    if links_only:
        params["linksonly"] = "true"

    return _generic_get_resources(artifact_format, params, timeout=180)


# ============================================================================
# TOOLS - HISTORY OPERATIONS
# ============================================================================


@mcp.tool()
def get_artifact_history(resource_uri: str, artifact_format: str = "resources") -> str:
    """Get complete artifact history information including all revisions.

    Args:
        resource_uri: The URI of the artifact
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML response with full revision history
    """
    if not resource_uri:
        return json.dumps({"error": "resource_uri is required"})
    return _generic_get_resources(artifact_format, {"resourceURI": resource_uri, "history": "true"}, timeout=180)


@mcp.tool()
def get_artifact_history_by_timerange(
    resource_uri: str, start_date: str, end_date: Optional[str] = None, artifact_format: str = "resources"
) -> str:
    """Get artifact history filtered by time range.

    Args:
        resource_uri: The URI of the artifact
        start_date: Start date in ISO 8601 format (yyyy-MM-dd'T'HH:mm:ss.SSS'Z')
        end_date: Optional end date in ISO 8601 format
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML response with revisions in time range (paginated, 25 per page)
    """
    if not resource_uri or not start_date:
        return json.dumps({"error": "resource_uri and start_date are required"})

    params = {"resourceURI": resource_uri, "history": "true", "startDate": start_date}
    if end_date:
        params["endDate"] = end_date

    return _generic_get_resources(artifact_format, params, timeout=180)


# ============================================================================
# TOOLS - USER ACTIVITY TRACKING
# ============================================================================


@mcp.tool()
def get_user_activity(action: str, start: str, end: str, user: str, configuration_context: str) -> str:
    """Get artifact information created, modified, or deleted by a user within a time range.

    Args:
        action: The type of action ('created', 'modified', or 'deleted')
        start: Start date in ISO 8601 format
        end: End date in ISO 8601 format
        user: Username or user URI
        configuration_context: The configuration context identifier

    Returns:
        XML response with user activity artifacts
    """
    if action not in ["created", "modified", "deleted"]:
        return json.dumps({"error": "action must be 'created', 'modified', or 'deleted'"})

    if not all([start, end, user, configuration_context]):
        return json.dumps({"error": "All parameters are required"})

    try:
        params = {"action": action, "start": start, "end": end, "user": user}
        headers = {"Configuration-Context": configuration_context}
        url = _build_url("activity", params)
        response = _make_request(url, headers=headers, timeout=180)
        return response.text
    except Exception as e:
        return _handle_error("get_user_activity", e)


# ============================================================================
# TOOLS - ADVANCED QUERIES
# ============================================================================


@mcp.tool()
def search_resources_advanced(
    artifact_format: str = "resources",
    project_uri: Optional[str] = None,
    type_uri: Optional[str] = None,
    type_name: Optional[str] = None,
    view_uri: Optional[str] = None,
    view_name: Optional[str] = None,
    module_uri: Optional[str] = None,
    collection_uri: Optional[str] = None,
    snapshot_id: Optional[str] = None,
    modified_since: Optional[str] = None,
) -> str:
    """Perform advanced resource search with multiple filter combinations.

    Args:
        artifact_format: The artifact format type (default: 'resources')
        project_uri: Optional project URI to scope the search
        type_uri: Optional artifact type URI filter
        type_name: Optional artifact type name filter (requires project_uri)
        view_uri: Optional view URI filter (requires project_uri)
        view_name: Optional view name filter (requires project_uri)
        module_uri: Optional module URI filter
        collection_uri: Optional collection URI filter
        snapshot_id: Optional snapshot/baseline ID filter
        modified_since: Optional timestamp filter (ISO 8601 format)

    Returns:
        XML response with filtered resources (filters combined with AND logic)
    """
    params = {}

    if project_uri:
        params["projectURI"] = project_uri

    if type_uri:
        params["typeURI"] = type_uri
    elif type_name:
        if not project_uri:
            return json.dumps({"error": "type_name requires project_uri"})
        params["typeName"] = type_name

    if view_uri:
        if not project_uri:
            return json.dumps({"error": "view_uri requires project_uri"})
        params["viewURI"] = view_uri
    elif view_name:
        if not project_uri:
            return json.dumps({"error": "view_name requires project_uri"})
        params["viewName"] = view_name

    if module_uri:
        params["moduleURI"] = module_uri
    if collection_uri:
        params["collectionURI"] = collection_uri
    if snapshot_id:
        params["snapshotId"] = snapshot_id
    if modified_since:
        params["modifiedSince"] = modified_since

    if not params:
        return json.dumps({"error": "At least one filter parameter is required"})

    return _generic_get_resources(artifact_format, params, timeout=180)


# ============================================================================
# TOOLS - OSLC QUERY
# ============================================================================


@mcp.tool()
def oslc_query_requirements(
    project_uri: str,
    oslc_where: Optional[str] = None,
    oslc_select: Optional[str] = None,
    oslc_prefix: Optional[str] = None,
    oslc_orderBy: Optional[str] = None,
) -> str:
    """Execute OSLC query to retrieve requirements with filters.

    This is the primary tool for querying requirements in DNG. It supports flexible OSLC query
    syntax to filter, select, and sort requirements based on various criteria.

    Note: This function specifically queries Requirements (not Folders or Collections).

    Args:
        project_uri: The project URI (Example: https://rb-alm-13-q.de.bosch.com/rm/process/project-areas/_dJAGoNA3EfCrlrBrAnaxQA)
        oslc_where: OSLC where clause for filtering (optional)
        oslc_select: Fields to select - use '*' for all or comma-separated list (optional)
        oslc_prefix: Namespace prefixes for query terms (optional but recommended)
        oslc_orderBy: Sort order specification (optional)

    Returns:
        XML response with query results

    Common Query Examples:
    =====================

    1. Query by identifier (numeric ID):
       oslc_where='dcterms:identifier=1431'
       oslc_prefix='dcterms=<http://purl.org/dc/terms/>'
       oslc_select='*'

    2. Query by title (exact match):
       oslc_where='dcterms:title="My Requirement"'
       oslc_prefix='dcterms=<http://purl.org/dc/terms/>'
       oslc_select='*'

    3. Query by title (contains):
       oslc_where='dcterms:title="*security*"'
       (wildcard search - check DNG version for support)

    4. Query by folder/parent:
       oslc_where='nav:parent=<https://server/rm/folders/_uuid>'
       oslc_prefix='nav=<http://com.ibm.rdm/navigation#>,dcterms=<http://purl.org/dc/terms/>'
       oslc_select='dcterms:title,dcterms:description'

    5. Query by artifact type:
       oslc_where='rm:ofType=<https://server/rm/types/_typeId>'
       oslc_prefix='rm=<http://www.ibm.com/xmlns/rdm/rdf/>'
       oslc_select='*'

    6. Query by modification date:
       oslc_where='dcterms:modified>="2024-01-01T00:00:00.000Z"^^xsd:dateTime'
       oslc_prefix='dcterms=<http://purl.org/dc/terms/>'
       oslc_select='dcterms:title,dcterms:modified'

    7. Query collection members:
       oslc_where='dcterms:identifier=123'
       oslc_prefix='oslc_rm=<http://open-services.net/ns/rm#>,dcterms=<http://purl.org/dc/terms/>'
       oslc_select='oslc_rm:uses{dcterms:title},oslc_rm:uses{dcterms:identifier}'

    8. Combined filters with AND:
       oslc_where='dcterms:identifier>100 and dcterms:modified>="2024-01-01T00:00:00.000Z"^^xsd:dateTime'

    9. Query with sorting:
       oslc_where='dcterms:identifier>0'
       oslc_orderBy='dcterms:modified'

    Common Namespace Prefixes:
    =========================
    dcterms=<http://purl.org/dc/terms/>
    oslc=<http://open-services.net/ns/core#>
    oslc_rm=<http://open-services.net/ns/rm#>
    rm=<http://www.ibm.com/xmlns/rdm/rdf/>
    nav=<http://com.ibm.rdm/navigation#>

    Common Properties:
    =================
    dcterms:identifier - Numeric artifact ID
    dcterms:title - Requirement title
    dcterms:description - Requirement description/primary text
    dcterms:created - Creation timestamp
    dcterms:modified - Last modification timestamp
    dcterms:creator - Creator URI
    oslc:instanceShape - Artifact type URI
    nav:parent - Parent folder URI
    rm:ofType - Type classification

    Notes:
    ======
    - If no oslc_where clause provided, returns all requirements in project (paginated)
    - Use oslc_select='*' to retrieve all properties
    - Combine multiple namespace prefixes with commas in oslc_prefix
    - Date comparisons require ^^xsd:dateTime suffix
    - URI values in where clauses must be enclosed in angle brackets <>
    - String values must be enclosed in double quotes ""
    """
    if not project_uri:
        return json.dumps({"error": "project_uri is required"})

    try:
        # Discover query capability
        query_base = _discover_query_capability(project_uri)
        if not query_base:
            return json.dumps(
                {
                    "error": "Could not discover query capability for project",
                    "project_uri": project_uri,
                }
            )

        # Build OSLC query parameters
        oslc_params = []
        if oslc_where:
            oslc_params.append(f"oslc.where={oslc_where}")
        if oslc_select:
            oslc_params.append(f"oslc.select={oslc_select}")
        if oslc_prefix:
            oslc_params.append(f"oslc.prefix={oslc_prefix}")
        if oslc_orderBy:
            oslc_params.append(f"oslc.orderBy={oslc_orderBy}")

        # Determine separator based on whether query_base already has parameters
        separator = "&" if "?" in query_base else "?"

        # Append OSLC parameters to query base
        if oslc_params:
            query_url = query_base + separator + "&".join(oslc_params)
        else:
            query_url = query_base

        logging.info(f"Executing OSLC query: {query_url}")

        response = _make_request(query_url, timeout=DEFAULT_TIMEOUT)
        return response.text

    except Exception as e:
        return _handle_error("oslc_query_requirements", e)


# ============================================================================
# TOOLS - FOLDER MANAGEMENT
# ============================================================================


@mcp.tool()
def create_folder(
    project_uri: str,
    title: str,
    parent_uri: Optional[str] = None,
    description: Optional[str] = None,
) -> str:
    """Create a new folder in DNG RM.

    Args:
        project_uri: The project area URI
        title: The title of the folder
        parent_uri: Optional URI of the parent folder
        description: Optional description for the folder

    Returns:
        JSON with creation status and created folder URI
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required and must not be empty"})

    if not title or not title.strip():
        return json.dumps({"error": "title is required and must not be empty"})

    try:
        from xml.sax.saxutils import escape

        # Build RDF/XML payload for the folder
        rdf_parts = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            "<rdf:RDF",
            '    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"',
            '    xmlns:dcterms="http://purl.org/dc/terms/"',
            '    xmlns:oslc="http://open-services.net/ns/core#"',
            '    xmlns:nav="http://jazz.net/ns/rm/navigation#">',
            '    <rdf:Description rdf:about="">',
            '        <rdf:type rdf:resource="http://jazz.net/ns/rm#Folder"/>',
            f'        <dcterms:title rdf:parseType="Literal">{escape(title)}</dcterms:title>',
        ]

        if description:
            rdf_parts.append(
                f'        <dcterms:description rdf:parseType="Literal">{escape(description)}</dcterms:description>'
            )

        if parent_uri:
            rdf_parts.append(f'        <nav:parent rdf:resource="{escape(parent_uri)}"/>')

        rdf_parts.extend(["    </rdf:Description>", "</rdf:RDF>"])

        rdf_payload = "\n".join(rdf_parts)

        # Prepare headers
        headers = {
            "Content-Type": "application/rdf+xml",
            "Accept": "application/rdf+xml",
            "OSLC-Core-Version": "2.0",
            "X-Jazz-CSRF-Prevent": "true",
        }

        # Make POST request
        response = requests.post(
            project_uri,
            data=rdf_payload,
            headers=headers,
            auth=(DNG_USERNAME, DNG_PASSWORD),
            verify=DNG_VERIFY_SSL,
            timeout=60,
        )

        logging.info(f"POST {project_uri} - Status: {response.status_code}")
        response.raise_for_status()

        # Extract created resource URI
        resource_uri = response.headers.get("Location") or response.headers.get("Content-Location", "")

        return json.dumps(
            {
                "success": True,
                "message": "Folder created successfully",
                "resource_uri": resource_uri,
                "status_code": response.status_code,
            },
            indent=2,
        )

    except Exception as e:
        return _handle_error("create_folder", e)


@mcp.tool()
def get_folders_by_project(project_uri: str) -> str:
    """Get all folders in a project.

    Args:
        project_uri: The project URI or project UUID

    Returns:
        XML response with folder information
    """
    if not project_uri.strip():
        return json.dumps({"error": "project_uri is required"})

    return _generic_get_resources("resources", {"projectURI": project_uri, "typeURI": "Folder"})


@mcp.tool()
def get_folder_contents(folder_uri: str, artifact_format: str = "resources") -> str:
    """Get the contents of a folder (artifacts contained in the folder).

    Args:
        folder_uri: The URI of the folder
        artifact_format: The artifact format type (default: 'resources')

    Returns:
        XML response with artifacts in the folder
    """
    if not folder_uri:
        return json.dumps({"error": "folder_uri is required"})

    return _generic_get_resources(artifact_format, {"folderURI": folder_uri})


@mcp.tool()
def move_artifact_to_folder(artifact_uri: str, target_folder_uri: str) -> str:
    """Move an artifact (requirement) to a different folder.

    Args:
        artifact_uri: The URI of the artifact to move
        target_folder_uri: The URI of the target folder

    Returns:
        JSON with move status
    """
    if not all([artifact_uri, target_folder_uri]):
        return json.dumps({"error": "artifact_uri and target_folder_uri are required"})

    try:
        # Prepare the RDF payload to update the parent folder
        rdf_payload = f"""
        <?xml version="1.0" encoding="UTF-8"?>
        <rdf:RDF
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:oslc="http://open-services.net/ns/core#"
            xmlns:oslc_rm="http://open-services.net/ns/rm#"
            xmlns:nav="http://jazz.net/ns/rm/navigation#">
          <rdf:Description rdf:about="{artifact_uri}">
            <nav:parent rdf:resource="{target_folder_uri}"/>
          </rdf:Description>
        </rdf:RDF>
        """

        # Prepare headers with CSRF prevention
        headers = {
            "Content-Type": "application/rdf+xml",
            "Accept": "application/rdf+xml",
            "OSLC-Core-Version": "2.0",
            "X-Jazz-CSRF-Prevent": "true",
        }

        # Make PUT request to update the artifact
        response = requests.put(
            artifact_uri,
            data=rdf_payload,
            headers=headers,
            auth=(DNG_USERNAME, DNG_PASSWORD),
            verify=DNG_VERIFY_SSL,
            timeout=60,
        )

        logging.info(f"PUT {artifact_uri} - Status: {response.status_code}")

        response.raise_for_status()

        return json.dumps(
            {
                "success": True,
                "message": "Artifact moved to folder successfully",
                "status_code": response.status_code,
            },
            indent=2,
        )

    except Exception as e:
        return _handle_error("move_artifact_to_folder", e)


# ============================================================================
# TOOLS - PROJECT INFORMATION
# ============================================================================


@mcp.tool()
def list_all_projects() -> str:
    """List all accessible projects with their names and URIs.

    Returns:
        JSON with project list and metadata
    """
    try:
        catalog_url = f"{DNG_SERVER}{DNG_CATALOG}"
        response = _make_request(catalog_url, timeout=LONG_TIMEOUT)
        root = ET.fromstring(response.text)

        projects_list = []
        for service_provider in root.findall(".//oslc:ServiceProvider", DNG_NAMESPACES):
            resource_uri = service_provider.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about", "")
            title = _extract_text_or_empty(service_provider.find(".//dcterms:title", DNG_NAMESPACES))

            # Get project area URI from details
            details_elem = service_provider.find(".//oslc:details", DNG_NAMESPACES)
            project_area_uri = ""
            if details_elem is not None:
                project_area_uri = details_elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", "")

            # Extract project UUID
            project_uuid = ""
            if "/oslc_rm/" in resource_uri:
                project_uuid = resource_uri.split("/oslc_rm/")[1].split("/")[0]
            elif project_area_uri and "/project-areas/" in project_area_uri:
                project_uuid = project_area_uri.split("/project-areas/")[-1]

            projects_list.append(
                {
                    "project_name": title or "Unknown",
                    "project_uuid": project_uuid,
                    "service_provider_uri": resource_uri,
                    "project_area_uri": project_area_uri,
                }
            )

        return json.dumps(
            {
                "total_projects": len(projects_list),
                "projects": projects_list,
            },
            indent=2,
        )

    except ET.ParseError as e:
        return json.dumps({"error": f"XML parsing error: {str(e)}"})
    except Exception as e:
        return _handle_error("list_all_projects", e)


@mcp.tool()
def get_project_info(project_uri: str) -> str:
    """Get detailed information about a project.

    Args:
        project_uri: The project URI or project UUID

    Returns:
        XML response with project details
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required"})

    return _generic_get_resources("resources", {"projectURI": project_uri, "typeURI": "Project"})


@mcp.tool()
def get_project_modules(project_uri: str) -> str:
    """Get all modules in a project.

    Args:
        project_uri: The project URI or project UUID

    Returns:
        XML response with module information
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required"})

    return _generic_get_resources("resources", {"projectURI": project_uri, "typeURI": "Module"})


@mcp.tool()
def get_project_collections(project_uri: str) -> str:
    """Get all collections in a project.

    Args:
        project_uri: The project URI or project UUID

    Returns:
        XML response with collection information
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required"})

    return _generic_get_resources("resources", {"projectURI": project_uri, "typeURI": "Collection"})


@mcp.tool()
def get_project_snapshots(project_uri: str) -> str:
    """Get all snapshots (baselines) in a project.

    Args:
        project_uri: The project URI or project UUID

    Returns:
        XML response with snapshot information
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required"})

    return _generic_get_resources("resources", {"projectURI": project_uri, "typeURI": "Snapshot"})


# ============================================================================
# TOOLS - UPDATE OPERATIONS
# ============================================================================


@mcp.tool()
def create_requirement(
    project_uri: str,
    title: str,
    primary_text: Optional[str] = None,
    artifact_type: Optional[str] = None,
    folder_uri: Optional[str] = None,
    attributes_json: Optional[str] = None,
) -> str:
    """Create a new requirement in DNG RM.

    Args:
        project_uri: The project area URI
        title: The title of the requirement
        primary_text: Optional description/primary text for the requirement
        artifact_type: Optional artifact type URI (resource shape)
        folder_uri: Optional parent folder URI to place the requirement
        attributes_json: Optional JSON string of custom attributes as key-value pairs

    Returns:
        JSON with creation status and created requirement URI

    Example attributes_json:
        '{"rm:priority": "High", "dcterms:subject": "Security"}'
        '{"custom:status": {"uri": "https://server/rm/types/_statusId"}}'

    Note:
        - The artifact_type should be a resource shape URI if you want to specify a type
        - Custom attributes must use proper namespace prefixes
        - System attributes (created, modified, creator, etc.) are set automatically
    """
    if not project_uri or not project_uri.strip():
        return json.dumps({"error": "project_uri is required and must not be empty"})

    if not title or not title.strip():
        return json.dumps({"error": "title is required and must not be empty"})

    try:
        # Discover creation factory
        factory_result = _discover_creation_factory(project_uri)
        if not factory_result:
            return json.dumps(
                {
                    "error": "Could not discover requirement creation factory for project",
                    "project_uri": project_uri,
                }
            )

        creation_factory_url, resource_shapes = factory_result
        logging.info(f"Using creation factory: {creation_factory_url}")

        # Parse custom attributes if provided
        attributes = None
        if attributes_json:
            try:
                attributes = json.loads(attributes_json)
            except json.JSONDecodeError as e:
                return json.dumps({"error": f"Invalid attributes_json: {str(e)}"})

        # Build RDF/XML payload
        rdf_payload = _build_requirement_rdf(
            title=title,
            primary_text=primary_text,
            artifact_type=artifact_type,
            folder_uri=folder_uri,
            attributes=attributes,
        )

        # Prepare headers
        headers = {
            "Content-Type": "application/rdf+xml",
            "Accept": "application/rdf+xml",
            "OSLC-Core-Version": "2.0",
            "X-Jazz-CSRF-Prevent": "true",
        }

        # Make POST request to creation factory
        response = requests.post(
            creation_factory_url,
            data=rdf_payload,
            headers=headers,
            auth=(DNG_USERNAME, DNG_PASSWORD),
            verify=DNG_VERIFY_SSL,
            timeout=60,
        )

        logging.info(f"POST {creation_factory_url} - Status: {response.status_code}")
        response.raise_for_status()

        # Extract created resource URI from Location header
        resource_uri = response.headers.get("Location") or response.headers.get("Content-Location", "")

        return json.dumps(
            {
                "success": True,
                "message": "Requirement created successfully",
                "resource_uri": resource_uri,
                "status_code": response.status_code,
            },
            indent=2,
        )

    except Exception as e:
        return _handle_error("create_requirement", e)


@mcp.tool()
def update_requirement(
    resource_uri: str,
    title: Optional[str] = None,
    primary_text: Optional[str] = None,
    folder_uri: Optional[str] = None,
    attributes_json: Optional[str] = None,
) -> str:
    """Update an existing requirement in DNG using OSLC protocol.

    Args:
        resource_uri: The URI of the requirement to update
        title: New title for the requirement
        primary_text: New primary text or description
        folder_uri: New folder URI to move the requirement
        attributes_json: JSON string of attributes to update as key-value pairs

    Returns:
        JSON with update status

    Note:
        This fetches the current requirement, modifies specified fields, and performs
        a PUT operation with proper ETag handling for optimistic locking.

        System attributes cannot be modified using this tool.
    """
    if not resource_uri or not resource_uri.strip():
        return json.dumps({"error": "resource_uri is required and must not be empty"})

    if not any([title, primary_text, folder_uri, attributes_json]):
        return json.dumps({"error": "At least one field to update must be provided"})

    try:
        # Fetch current requirement with ETag
        get_headers = _get_headers()

        get_response = requests.get(
            resource_uri,
            headers=get_headers,
            auth=(DNG_USERNAME, DNG_PASSWORD),
            verify=DNG_VERIFY_SSL,
            timeout=SHORT_TIMEOUT,
        )
        get_response.raise_for_status()

        etag = get_response.headers.get("ETag", "")
        if not etag:
            logging.warning("No ETag received. Update may fail due to missing optimistic locking.")

        # Parse current RDF
        current_rdf = get_response.text
        root = ET.fromstring(current_rdf)

        # Register namespaces for output
        for prefix, uri in DNG_NAMESPACES.items():
            ET.register_namespace(prefix, uri)

        # Find requirement description
        description = root.find(".//{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description")
        if description is None:
            return json.dumps({"error": "Could not parse requirement RDF structure"})

        # Update title
        if title:
            title_elem = description.find(".//{http://purl.org/dc/terms/}title")
            if title_elem is not None:
                title_elem.text = title
            else:
                logging.warning("Title element not found in requirement RDF")

        # Update description
        if primary_text:
            desc_elem = description.find(".//{http://purl.org/dc/terms/}description")
            if desc_elem is not None:
                desc_elem.text = primary_text
            else:
                # Add description if not exists
                new_desc = ET.SubElement(description, "{http://purl.org/dc/terms/}description")
                new_desc.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}parseType", "Literal")
                new_desc.text = primary_text

        # Update folder (move requirement)
        if folder_uri:
            parent_elem = description.find(".//{http://jazz.net/ns/rm/navigation#}parent")
            if parent_elem is not None:
                parent_elem.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", folder_uri)
            else:
                # Add parent if not exists
                new_parent = ET.SubElement(description, "{http://jazz.net/ns/rm/navigation#}parent")
                new_parent.set("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource", folder_uri)

        # Update custom attributes
        if attributes_json:
            try:
                attributes = json.loads(attributes_json)
                for attr_name, attr_value in attributes.items():
                    # Handle namespaced attributes
                    if ":" in attr_name:
                        prefix, local = attr_name.split(":", 1)
                        if prefix in DNG_NAMESPACES:
                            full_name = f"{{{DNG_NAMESPACES[prefix]}}}{local}"

                            attr_elem = description.find(f".//{full_name}")
                            if attr_elem is not None:
                                if isinstance(attr_value, str):
                                    attr_elem.text = attr_value
                                elif isinstance(attr_value, dict) and "uri" in attr_value:
                                    attr_elem.set(
                                        "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource",
                                        attr_value["uri"],
                                    )
                        else:
                            logging.warning(f"Unknown namespace prefix: {prefix}")
            except json.JSONDecodeError as e:
                return json.dumps({"error": f"Invalid attributes_json: {str(e)}"})

        # Convert back to XML string
        updated_rdf = ET.tostring(root, encoding="utf-8", method="xml").decode("utf-8")

        # Prepare headers with ETag
        headers = {
            "Content-Type": "application/rdf+xml",
            "Accept": "application/rdf+xml",
            "OSLC-Core-Version": "2.0",
            "X-Jazz-CSRF-Prevent": "true",
        }

        if etag:
            headers["If-Match"] = etag

        # Make PUT request
        response = requests.put(
            resource_uri,
            data=updated_rdf,
            headers=headers,
            auth=(DNG_USERNAME, DNG_PASSWORD),
            verify=DNG_VERIFY_SSL,
            timeout=60,
        )

        logging.info(f"PUT {resource_uri} - Status: {response.status_code}")

        if response.status_code == 412:
            return json.dumps(
                {
                    "error": "Precondition Failed - Resource was modified by another user",
                    "suggestion": "Fetch the latest version and retry",
                }
            )

        response.raise_for_status()

        return json.dumps(
            {
                "success": True,
                "message": "Requirement updated successfully",
                "resource_uri": resource_uri,
                "status_code": response.status_code,
            },
            indent=2,
        )

    except ET.ParseError as e:
        return json.dumps({"error": f"XML parsing error: {str(e)}"})
    except Exception as e:
        return _handle_error("update_requirement", e)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,
    )

    try:
        transport, host, port = get_mcp_init_vars()
        if transport == "stdio":
            mcp.run(transport="stdio")
        else:
            mcp.run(transport=transport, host=host, port=port)
    except Exception as e:
        logging.error(f"Failed to start MCP server: {e}", exc_info=True)
        raise
