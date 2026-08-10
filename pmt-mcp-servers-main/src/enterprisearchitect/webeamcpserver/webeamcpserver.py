"""
Enterprise Architect MCP Server (webEA)
Exposes EA OSLC API functionality through Model Context Protocol
Returns raw XML responses for LLM processing
"""

import logging
import os
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP
from webeaclient import WebEAController

# Initialize FastMCP server
mcp = FastMCP("webea-mcp-server")

# Global client instance
client: Optional[WebEAController] = None


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
        raise ValueError(f"Invalid PORT env variable: '{port_str}' - must be a valid integer")
    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def get_server_parameters() -> tuple:
    """
    Read server configuration from environment variables only.

    Returns:
        tuple: (server_url, model_name, username, password)
    Raises:
        EnvironmentError: If any required variable is missing.
    """

    username = os.getenv("WEBEA_USERNAME")
    password = os.getenv("WEBEA_PASSWORD")
    server_url = os.getenv("WEBEA_ENDPOINT")
    model_name = os.getenv("WEBEA_MODEL")

    missing = []
    if not username:
        missing.append("WEBEA_USERNAME")
    if not password:
        missing.append("WEBEA_PASSWORD")
    if not server_url:
        missing.append("WEBEA_ENDPOINT")
    if not model_name:
        missing.append("WEBEA_MODEL")

    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

    return (server_url, model_name, username, password)


def initialize_client():
    """
    Initialize the EA client with server parameters.
    """
    global client

    try:
        logging.info("Starting initialize client...")
        server_url, model_name, username, password = get_server_parameters()

        client = WebEAController(
            server_url=server_url,
            model_name=model_name,
            username=username,
            password=password,
        )
        logging.info("Authenticating to webEA server...")
        auth_result = client.authenticate()
        if auth_result["success"]:
            logging.info(f"Authentication successful for user '{username}' on model '{model_name}'.")
            return True
        else:
            logging.error(f"Authentication failed for user '{username}': {auth_result.get('message', 'Unknown error')}")
            logging.error("Please verify your credentials and server access.")
        return False

    except Exception as e:
        logging.error(f"in initialize client: {e}")
        return False


@mcp.tool()
def get_root_package() -> Any:
    """
    Get the root (top-level) package of the current EA model.

    Returns:
        Raw XML response containing root package information including:
        - Package title, identifier (GUID), type
        - Creation and modification dates
        - Description and other properties

        Returns an error msg if fails.
    """
    if not client:
        return "Error: Not authenticated. Client not initialized."
    result = client.get_root_package()
    return result if result else "Error: Failed to retrieve root package"


@mcp.tool()
def get_package_info(package_guid: str) -> Any:
    """
    Get comprehensive information about a package including its contents.

    Args:
        package_guid: Package GUID (required, can be provided with or without 'pk_' prefix)

    Returns:
        Raw XML responses containing:
        - Package basic properties (title, type, GUID, dates, etc.)
        - All elements in the package
        - All diagrams in the package
        - All sub-packages

        The response is a dict object with keys: 'basic', 'elements', 'diagrams', 'subpackages'
        Each value contains raw XML. Returns error if fails.
    """
    if not client:
        return "Error: Not authenticated. Client not initialized."

    result = client.get_package_info(package_guid)

    if not result["success"]:
        return f"Error: {result['message']}"

    return result


@mcp.tool()
def get_diagram_info(diagram_guid: str) -> Any:
    """
    Get comprehensive information about a diagram.

    Args:
        diagram_guid: Diagram GUID (with or without 'dg_' prefix and curly braces)

    Returns:
        Raw XML response containing:
        - Diagram basic properties (title, type, GUID, creation/modification dates)
        - Parent package identifier
        - All associated discussions
        Returns error message if diagram not found.
    """
    if not client:
        return "Error: Not authenticated. Client not initialized."

    return client.get_diagram_info(diagram_guid)


@mcp.tool()
def get_element_info(element_guid: str) -> Any:
    """
    Get information about an element including all properties.

    Args:
        element_guid: Element GUID (with or without 'el_' prefix and curly braces)

    Returns:
        Raw XML response containing all element information

        Returns error message if element not found.
    """
    if not client:
        return "Error: Not authenticated. Client not initialized."
    return client.get_element_info(element_guid)


@mcp.tool()
def query_resources(where_clause: str, select_fields: str = "*") -> Any:
    """
    Query Enterprise Architect resources using OSLC API query syntax.
    Note: Destructive SQL operations are blocked for safety.

    Args:
        where_clause: OSLC API compliant filter string to select resources.
            Examples:
                - 'dcterms:title="MyClass"'
                - 'dcterms:type="Class"%20and%20ss:resourcetype="Element"'
                - 'ss:parentresourceidentifier="pk_{GUID}"'
        select_fields: Comma-separated list of fields to return, or "*" for all fields.
            Examples: "dcterms:title,dcterms:identifier,dcterms:type"

    Returns:
        Raw XML response containing resources that match the query criteria.
        Returns an error message if the query is invalid or fails.

    Supported query properties include:
        - dcterms:title, dcterms:type, dcterms:identifier
        - dcterms:created, dcterms:modified
        - dcterms:creator{foaf:name}
        - ss:resourcetype, ss:parentresourceidentifier
        - ss:status, ss:complexity, ss:phase, ss:version
        - ss:stereotype{ss:name} or ss:stereotype{ss:fqname}
    """
    if not client:
        return "Error: Not authenticated. Client not initialized."

    if not where_clause or not where_clause.strip():
        return "Error: where_clause is required"

    result = client.query_resources(where_clause, select_fields)

    if not result:
        return "Error: Query failed or returned no results"

    return result


@mcp.tool()
def get_diagram_image(diagram_guid: str) -> Any:
    """
    Download the diagram as png image format and save inside webea_mcpserver_output\\downloaded_diagrams folder.

    Args:
        diagram_guid: Diagram GUID (with or without 'dg_' prefix)

    Returns:
        returns success message or error message if fails.
    """
    if not client:
        return "Error: Not authenticated. Client not initialized."

    return client.get_diagram_image(diagram_guid)


@mcp.tool()
def get_server_status() -> Dict[str, Any]:
    """
    Get current server connection status and configuration.

    Returns:
        Dict containing:
        - authenticated: bool - Whether client is authenticated
        - server_url: str - EA server URL
        - model_name: str - Connected model name
    """
    if not client:
        return {"authenticated": False, "message": "Client not initialized"}

    return {
        "authenticated": client.user_token is not None,
        "server_url": client.server_url,
        "model_name": client.model_name,
    }


# Creation tools
@mcp.tool()
def create_package(
    title: str,
    parent_package_guid: str,
    description: str = "",
) -> Any:
    """
    Create a new package in Enterprise Architect.

    Args:
        title: Package name/title (required)
        parent_package_guid: Parent package GUID (required). Package will be created inside this parent package.
        description: Package description (optional)

    Returns:
        Dict containing:
        - success: bool - Whether creation succeeded
        - message: str - Success/error message
        - guid: str - Created package GUID (if successful)
        - xml: str - Full XML response from server
    """
    if not client:
        return {
            "success": False,
            "message": "Not authenticated. Client not initialized.",
        }

    return client.create_package(
        title=title,
        description=description,
        parent_package_guid=parent_package_guid,
    )


@mcp.tool()
def create_element(
    title: str,
    element_type: str,
    parent_package_guid: str,
    description: str = "",
    stereotype: str = None,
    alias: str = None,
    status: str = None,
    complexity: str = None,
    phase: str = None,
    version: str = None,
    difficulty: str = None,
    priority: str = None,
    language: str = None,
    keywords: str = None,
    author: str = None,
) -> Any:
    """
    Create a new element in Enterprise Architect.

    Args:
        title: Name of the element (required).
        element_type: The base type of the element (required). See list below.
        parent_package_guid: GUID of the parent package (required). Element will be created inside this package.
        description: Notes or description for the element (optional).
        stereotype: Stereotype to apply to the element (e.g., "control", "BPMN2.0::Activity").
        alias: An alternative name for the element.
        status: The current status of the element (e.g., "Proposed", "Implemented").
        complexity: The complexity of the element (e.g., "Easy", "Medium", "Hard").
        phase: The development phase (e.g., "1.0", "In Development").
        version: The version number (e.g., "1.1").
        difficulty: The difficulty level (e.g., "Low", "High").
        priority: The priority level (e.g., "Medium").
        language: The programming language associated with the element (for classes).
        keywords: Comma-separated keywords or tags for the element.
        author: The name of the element's author.

    Supported element_type values:
        - UML Structural: "Class", "Interface", "Component", "Node", "DataType", "Artifact", "Package"
        - UML Behavioral: "UseCase", "Actor", "Activity", "State", "StateMachine", "Interaction"
        - UML Other: "Object", "Requirement", "Boundary", "Entity"

    Note:
        To create stereotyped elements, use the base 'element_type' and add the 'stereotype'.
        - For a 'Control' element: use element_type="Class" and stereotype="control".
        - For a 'BPMN Activity': use element_type="Activity" and stereotype="BPMN2.0::Activity".
        - For a 'SysML Block': use element_type="Class" and stereotype="SysML1.4::Block".

    Returns:
        A dictionary with creation status: {success: bool, message: str, guid: str, xml: str}.
    """
    if not client:
        return {
            "success": False,
            "message": "Not authenticated. Client not initialized.",
        }

    # Build optional properties dict from non-None arguments
    optional_props = {
        k: v
        for k, v in locals().items()
        if k
        in [
            "alias",
            "status",
            "complexity",
            "phase",
            "version",
            "difficulty",
            "priority",
            "language",
            "keywords",
            "author",
        ]
        and v is not None
    }

    return client.create_element(
        title=title,
        element_type=element_type,
        parent_package_guid=parent_package_guid,
        description=description,
        stereotype=stereotype,
        **optional_props,
    )


@mcp.tool()
def update_element(
    element_guid: str,
    title: str = None,
    description: str = None,
    alias: str = None,
    status: str = None,
    complexity: str = None,
    phase: str = None,
    version: str = None,
    difficulty: str = None,
    priority: str = None,
    language: str = None,
    keywords: str = None,
    author: str = None,
) -> Any:
    """
    Update properties of an existing element in Enterprise Architect.

    Args:
        element_guid: GUID of the element to update (required, with or without 'el_' prefix).
        title: New element name/title.
        description: New element notes/description.
        alias: New element alias.
        status: New element status.
        complexity: New element complexity (e.g., "Easy", "Medium").
        phase: New development phase.
        version: New version number.
        difficulty: New difficulty level.
        priority: New priority level.
        language: New programming language.
        keywords: New keywords (comma-separated).
        author: New author name.

    Returns:
        A dictionary with update status: {success: bool, message: str, xml: str}.

    Note:
        Only provided properties are updated. The element's stereotype cannot be changed via this tool.
    """
    if not client:
        return {
            "success": False,
            "message": "Not authenticated. Client not initialized.",
        }

    # Build properties dict from non-None arguments
    properties = {k: v for k, v in locals().items() if k not in ["element_guid"] and v is not None}

    if not properties:
        return {"success": False, "message": "No properties specified for update"}

    return client.update_element(element_guid, **properties)


@mcp.tool()
def create_connector(
    source_element_guid: str,
    target_element_guid: str,
    connector_type: str,
    name: str = "",
    description: str = "",
    direction: str = "Source -> Destination",
    stereotype: str = None,
) -> Any:
    """
    Create a connector (relationship) between two elements in EA.

    Args:
        source_element_guid: GUID of the source element (with/without 'el_' prefix).
        target_element_guid: GUID of the target element (with/without 'el_' prefix).
        connector_type: The type of the connector (e.g., "Association"). See list below.
        name: An optional name for the connector.
        description: An optional description or notes for the connector.
        direction: The connector's direction. Use plain text strings. Valid values are
                   "Source -> Destination", "Destination -> Source", "Bi-Directional", "Unspecified".
        stereotype: An optional stereotype to apply to the connector (e.g., "realize").

    Supported `connector_type` values include:
    - UML General: "Association", "Aggregation", "Composition", "Generalization", "Dependency", "Usage", "Realization"
    - UML Behavioral: "Sequence", "ControlFlow", "StateFlow", "ObjectFlow"
    - Use Case: "Include", "Extend"
    - Other: "InformationFlow", "Nesting"

    Returns:
        A dictionary with creation status: {success: bool, message: str, guid: str, xml: str}.

    Note: connector_types Realization, Include, Extend, Composition will fail due to requirement of
    additional parameters which is unspecified in api documentation.
    """
    if not client:
        return {
            "success": False,
            "message": "Not authenticated. Client not initialized.",
        }

    return client.create_connector(
        source_element_guid=source_element_guid,
        target_element_guid=target_element_guid,
        connector_type=connector_type,
        name=name,
        description=description,
        direction=direction,
        stereotype=stereotype,
    )


@mcp.tool()
def update_connector(
    connector_guid: str,
    source_element_guid: str,
    target_element_guid: str,
    connector_type: str,
    name: str = None,
    description: str = None,
    direction: str = None,
) -> Any:
    """
    Update an existing connector's properties in Enterprise Architect.

    Args:
        connector_guid: GUID of the connector to update (required, with/without 'lt_' prefix).
        source_element_guid: GUID of the source element (required for the update operation).
        target_element_guid: GUID of the target element (required for the update operation).
        connector_type: The type of the connector (required for the update operation, e.g., "Association").
        name: The new name for the connector (optional).
        description: The new description for the connector (optional).
        direction: The new direction (optional, e.g., "Source -> Destination").

    Returns:
        A dictionary with update status: {success: bool, message: str, xml: str}.

    NOTE: The EA OSLC API requires the source GUID, target GUID, and connector type
    to be specified even for an update. Only the properties `name`, `description`,
    and `direction` will actually be changed. The stereotype cannot be changed.
    """
    if not client:
        return {
            "success": False,
            "message": "Not authenticated. Client not initialized.",
        }

    return client.update_connector(
        connector_guid=connector_guid,
        source_element_guid=source_element_guid,
        target_element_guid=target_element_guid,
        connector_type=connector_type,
        name=name,
        description=description,
        direction=direction,
    )


if __name__ == "__main__":
    os.makedirs("webea_mcpserver_output", exist_ok=True)
    log_file_path = os.path.join("webea_mcpserver_output", "webEA_mcp_server.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file_path, mode="w", encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )

    initialize_result = initialize_client()
    if initialize_result:
        transport, host, port = _get_mcp_init_vars()
        if transport == "stdio":
            mcp.run(transport="stdio")
        else:
            mcp.run(transport=transport, host=host, port=port)
    else:
        logging.error("Failed to initialize client. Please verify input parameters.")
