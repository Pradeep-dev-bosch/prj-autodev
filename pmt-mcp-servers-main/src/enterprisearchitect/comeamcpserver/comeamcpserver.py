import logging
import os

from comeaclient import EAController
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server and controller
mcp = FastMCP("com-ea-mcp-server")
logging.info("EA COM MCP server, initializing...")
EA_REPO = EAController()


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


@mcp.tool()
def create_element(
    name: str,
    typeStr: str,
    packageID: int,
    stereotype: str = None,
    notes: str = None,
    alias: str = None,
    status: str = None,
    isAbstract: bool = False,
) -> dict:
    """Creates a new element in the repository."""
    return EA_REPO.create_element(name, typeStr, packageID, stereotype, notes, alias, status, isAbstract)


@mcp.tool()
def update_element(
    elementID: int,
    name: str = None,
    typeStr: str = None,
    stereotype: str = None,
    notes: str = None,
    alias: str = None,
    status: str = None,
    isAbstract: bool = None,
) -> dict:
    """Updates the properties of an existing element. Only provided properties will be changed."""
    return EA_REPO.update_element(elementID, name, typeStr, stereotype, notes, alias, status, isAbstract)


@mcp.tool()
def get_diagram_information(diagramID: int) -> dict:
    """Get detailed information about a diagram, including its elements and links."""
    return EA_REPO.get_diagram_information(diagramID)


@mcp.tool()
def get_root_packages() -> list:
    """Get all root packages (Models) in the repository."""
    return EA_REPO.get_root_packages()


@mcp.tool()
def get_package_information(packageID: int) -> dict:
    """Get basic information about a specific package."""
    return EA_REPO.get_package_information(packageID)


@mcp.tool()
def get_diagram_image(diagramID: int) -> dict:
    """Saves a diagram's image to a file and returns the file path."""
    return EA_REPO.get_diagram_image(diagramID)


@mcp.tool()
def get_opened_diagrams() -> list:
    """Get a list of all diagrams that are currently open in the EA user interface."""
    return EA_REPO.get_opened_diagrams()


@mcp.tool()
def get_element_information(elementID: int) -> dict:
    """Get detailed information about an element, including its attributes and methods."""
    return EA_REPO.get_element_information(elementID)


@mcp.tool()
def get_current_element() -> dict:
    """Get detailed information for the currently selected element in the EA user interface."""
    return EA_REPO.get_current_element()


@mcp.tool()
def find_packages_by_name(name: str, exactMatch: bool = False) -> list:
    """Find packages by their name. Supports exact or partial matching."""
    return EA_REPO.find_packages_by_name(name, exactMatch)


@mcp.tool()
def get_current_package() -> dict:
    """Get information for the currently selected package in the EA user interface."""
    return EA_REPO.get_current_package()


@mcp.tool()
def create_package(name: str, parentPackageID: int) -> dict:
    """Create a new package under a specified parent package."""
    return EA_REPO.create_package(name, parentPackageID)


@mcp.tool()
def place_element_on_diagram(elementID: int, diagramID: int) -> dict:
    """Place an existing element onto a specific diagram."""
    return EA_REPO.place_element_on_diagram(elementID, diagramID)


@mcp.tool()
def create_connector(sourceID: int, targetID: int, connectorType: str) -> dict:
    """Create a connector of a specific type to link two elements."""
    return EA_REPO.create_connector(sourceID, targetID, connectorType)


@mcp.tool()
def find_in_diagrams(elementID: int) -> list:
    """Find all diagrams in which the specified element is used."""
    return EA_REPO.find_in_diagrams(elementID)


@mcp.tool()
def select_element_in_diagram(elementID: int, diagramID: int) -> dict:
    """Highlights a specific element within a specific diagram in the EA user interface."""
    return EA_REPO.select_element_in_diagram(elementID, diagramID)


@mcp.tool()
def get_current_diagram() -> dict:
    """Get detailed information for the currently active (opened) diagram in the EA user interface."""
    return EA_REPO.get_current_diagram()


@mcp.tool()
def create_diagram(name: str, typeStr: str, packageID: int) -> dict:
    """Create a new diagram of a specific type within a package."""
    return EA_REPO.create_diagram(name, typeStr, packageID)


@mcp.tool()
def open_diagram(diagramID: int) -> dict:
    """Opens a specified diagram in the EA user interface."""
    return EA_REPO.open_diagram(diagramID)


@mcp.tool()
def set_element_property(elementID: int, propertyName: str, value: str) -> dict:
    """Set a specific property for an element (e.g., 'Notes', 'Stereotype', 'Abstract')."""
    return EA_REPO.set_element_property(elementID, propertyName, value)


@mcp.tool()
def layout_diagram(diagramID: int) -> dict:
    """Applies an automatic layout to a specified diagram."""
    return EA_REPO.layout_diagram(diagramID)


@mcp.tool()
def query_resources(sql_query: str) -> list:
    """
    Executes a read-only SQL query directly against the Enterprise Architect repository database.
    Results are returned as a list of dictionaries, where each dictionary is a row.

    **How to Query the EA Database:**

    The database contains many tables, but the most important ones for modeling artifacts are:

    1.  **t_object**: The master table for almost everything. Contains elements, packages, diagrams, etc.
        -   `Object_ID` (int): The unique ID of the object.
        -   `Object_Type` (str): The type of the object (e.g., 'Class', 'Actor', 'Package', 'Diagram').
        -   `Name` (str): The name of the object.
        -   `Package_ID` (int): The ID of the package that contains this object.
        -   `Stereotype` (str): The stereotype of the object.

    2.  **t_connector**: Contains all connectors (relationships) between elements.
        -   `Connector_ID` (int): The unique ID of the connector.
        -   `Connector_Type` (str): The type of relationship (e.g., 'Association', 'Aggregation', 'Realisation').
        -   `Start_Object_ID` (int): The ID of the source/client element. Links to `t_object.Object_ID`.
        -   `End_Object_ID` (int): The ID of the target/supplier element. Links to `t_object.Object_ID`.
        -   `Stereotype` (str): The stereotype of the connector.

    3.  **t_attribute**: Contains attributes of elements.
        -   `ID` (int): The unique ID of the attribute.
        -   `Object_ID` (int): The ID of the element that owns this attribute. Links to `t_object.Object_ID`.
        -   `Name` (str): The name of the attribute.
        -   `Type` (str): The data type of the attribute.

    4.  **t_operation**: Contains methods/operations of elements.
        -   `OperationID` (int): The unique ID of the operation.
        -   `Object_ID` (int): The ID of the element that owns this operation. Links to `t_object.Object_ID`.
        -   `Name` (str): The name of the operation.
        -   `ReturnType` (str): The return type of the operation.

    5.  **t_objectproperties**: Contains Tagged Values for elements.
        -   `PropertyID` (int): Unique ID of the tagged value.
        -   `Object_ID` (int): The ID of the element that owns this tag. Links to `t_object.Object_ID`.
        -   `Property` (str): The name of the tagged value.
        -   `Value` (str): The value of the tag.

    **--- EXAMPLES ---**

    *   **Example 1: Find all 'Class' elements in the model.**
        `"SELECT Name, Object_ID, Stereotype FROM t_object WHERE Object_Type = 'Class'"`

    *   **Example 2: Find all elements inside a specific package (e.g., package with ID 45).**
        `"SELECT Name, Object_Type, Object_ID FROM t_object WHERE Package_ID = 45"`

    *   **Example 3: Find all 'Class' elements that realize a 'Requirement'.**
        `"SELECT req.Name AS Requirement, cls.Name AS Realizing_Class FROM t_connector c JOIN t_object req ON c.Start_Object_ID = req.Object_ID JOIN t_object cls ON c.End_Object_ID = cls.Object_ID WHERE c.Connector_Type = 'Realisation' AND req.Object_Type = 'Requirement' AND cls.Object_Type = 'Class'"`

    Note: Destructive SQL operations are blocked for safety.

    Args:
        sql_query (str): The read-only SQL query to execute.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row from the query result.
    """
    return EA_REPO.query_repository(sql_query)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("ea_com_mcp_server.log", mode="w", encoding="utf-8"),
            logging.StreamHandler(),
        ],
        force=True,
    )
    transport, host, port = _get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
