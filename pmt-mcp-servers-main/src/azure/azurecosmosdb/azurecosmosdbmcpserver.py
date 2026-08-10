"""Azure Cosmos DB MCP Server

A Model Context Protocol (MCP) server implementation for Azure Cosmos DB,
providing tools for querying and exploring Cosmos DB containers.

This server enables LLMs to interact with Cosmos DB through standardized
MCP tools, supporting operations like querying, schema inspection, and
data exploration.
"""

import argparse
import os
from typing import Optional, Tuple, cast, Any
import logging
import json

from azure.cosmos import cosmos_client
from azure.cosmos.database import DatabaseProxy
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.server import Transport

mcp = FastMCP("cosmos.vsm.db")
cosmos_db: Optional[DatabaseProxy] = None
logger = logging.getLogger("CosmosVsmMcpServer")
logging.getLogger("azure.core").setLevel(logging.ERROR)
logging.getLogger("azure").setLevel(logging.ERROR)


# Helper function to filter out internal Azure Cosmos DB fields
def filter_keys(obj: Any) -> Any:
    """Remove internal Cosmos DB fields (starting with _ or cnt_) from objects.

    Args:
        obj: The object to filter (dict, list, or primitive type)

    Returns:
        Filtered object with internal fields removed
    """
    if isinstance(obj, dict):
        return {k: filter_keys(v) for k, v in obj.items() if not (k.startswith("_") or k.startswith("cnt_"))}
    elif isinstance(obj, list):
        return [filter_keys(i) for i in obj]
    else:
        return obj


def init_mcp_server() -> Tuple[Transport, str, str]:
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, help="CosmosDB host")
    parser.add_argument("--masterkey", type=str, help="CosmosDB master key")
    parser.add_argument("--database_id", type=str, help="CosmosDB database id")
    parser.add_argument(
        "--transport",
        type=str,
        help="Transport protocol (stdio, http, sse, streamable-http)",
    )
    parser.add_argument("--port", type=int, help="Port for server (if applicable)")
    parser.add_argument("--mcp_binding", type=str, help="Binding address for MCP server")
    args = parser.parse_args()

    host_name = args.host or os.environ.get("COSMOS_HOST")
    db_key = args.masterkey or os.environ.get("COSMOS_KEY")
    database_id = args.database_id or os.environ.get("COSMOS_DATABASE")
    transport_protocol = args.transport or os.environ.get("TRANSPORT") or "stdio"
    if transport_protocol in ["<TRANSPORT>", None, "", "-", "null"]:
        transport_protocol = "stdio"
    env_port = os.environ.get("PORT")
    try:
        env_port_int = int(env_port) if env_port else None
    except ValueError:
        env_port_int = None
    mcp_port = args.port or env_port_int or 8080
    mcp_binding = args.mcp_binding or os.environ.get("MCP_BINDING", "127.0.0.1")

    if not host_name:
        raise ValueError("CosmosDB host must be provided (via CLI, env, or .env)")
    if not db_key:
        raise ValueError("CosmosDB master key must be provided (via CLI, env, or .env)")
    if not database_id:
        raise ValueError("CosmosDB database id must be provided (via CLI, env, or .env)")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logger.info(f"Connecting to CosmosDB host: {host_name}")
    logger.info(f"Using database: {database_id}")
    client = cosmos_client.CosmosClient(str(host_name), {"masterKey": str(db_key)})
    global cosmos_db
    cosmos_db = cast(DatabaseProxy, client.get_database_client(str(database_id)))
    cosmos_db.list_containers(1)
    logger.info(f"Connected to CosmosDB database: {cosmos_db.id}")
    logger.info(f"Using transport protocol: {transport_protocol}, port: {mcp_port}")
    return transport_protocol, mcp_port, mcp_binding


@mcp.tool
def query_container(container_id: str, query: str, max_item_count: int = 100) -> str:
    """
    Execute a SQL query on a specified container in the Cosmos DB database.

    This tool allows you to run SQL queries using Cosmos DB SQL API syntax.
    Common query patterns:
    - SELECT * FROM c WHERE c.property = 'value'
    - SELECT c.id, c.name FROM c
    - SELECT * FROM c ORDER BY c.timestamp DESC
    - SELECT COUNT(1) as count FROM c

    Args:
        container_id: Name of the container to query
        query: SQL query string (Cosmos DB SQL API syntax)
        max_item_count: Maximum number of items to return (default: 100, max: 1000)

    Returns:
        JSON-formatted string with query results or error message
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."

        # Validate max_item_count
        if max_item_count < 1 or max_item_count > 1000:
            return "max_item_count must be between 1 and 1000"

        container = cosmos_db.get_container_client(container_id)
        items = list(
            container.query_items(query=query, enable_cross_partition_query=True, max_item_count=max_item_count)
        )

        if not items:
            return f"No items found matching the query in container '{container_id}'"

        filtered_items = [filter_keys(item) for item in items]
        return json.dumps(filtered_items, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error querying container '{container_id}': {str(e)}"


@mcp.tool
def read_item(container_id: str, item_id: str, partition_key: str) -> str:
    """
    Read a specific item from a container by its ID and partition key.

    This is more efficient than querying when you know the exact item ID and partition key.

    Args:
        container_id: Name of the container
        item_id: The ID of the item to read
        partition_key: The partition key value for the item

    Returns:
        JSON-formatted string with the item data or error message
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."

        container = cosmos_db.get_container_client(container_id)
        item = container.read_item(item=item_id, partition_key=partition_key)

        filtered_item = filter_keys(item)
        return json.dumps(filtered_item, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error reading item '{item_id}' from container '{container_id}': {str(e)}"


@mcp.tool
def create_item(container_id: str, item_data: str) -> str:
    """
    Create a new item in the specified container.

    The item must include an 'id' field and the partition key field as defined by the container.
    This operation will fail if an item with the same ID and partition key already exists.

    Args:
        container_id: Name of the container
        item_data: JSON string representing the item to create (must include 'id' field)

    Returns:
        Success message with created item ID or error message
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."

        # Parse the JSON string
        item = json.loads(item_data)

        if "id" not in item:
            return "Error: Item must include an 'id' field"

        container = cosmos_db.get_container_client(container_id)
        created_item = container.create_item(body=item)

        return f"Successfully created item with ID: {created_item['id']}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for item_data"
    except Exception as e:
        return f"Error creating item in container '{container_id}': {str(e)}"


@mcp.tool
def upsert_item(container_id: str, item_data: str) -> str:
    """
    Create or update an item in the specified container.

    If an item with the same ID and partition key exists, it will be replaced.
    If it doesn't exist, a new item will be created.

    Args:
        container_id: Name of the container
        item_data: JSON string representing the item (must include 'id' field)

    Returns:
        Success message with upserted item ID or error message
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."

        # Parse the JSON string
        item = json.loads(item_data)

        if "id" not in item:
            return "Error: Item must include an 'id' field"

        container = cosmos_db.get_container_client(container_id)
        upserted_item = container.upsert_item(body=item)

        return f"Successfully upserted item with ID: {upserted_item['id']}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for item_data"
    except Exception as e:
        return f"Error upserting item in container '{container_id}': {str(e)}"


@mcp.tool
def delete_item(container_id: str, item_id: str, partition_key: str) -> str:
    """
    Delete a specific item from a container by its ID and partition key.

    This operation is permanent and cannot be undone.

    Args:
        container_id: Name of the container
        item_id: The ID of the item to delete
        partition_key: The partition key value for the item

    Returns:
        Success message or error message
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."

        container = cosmos_db.get_container_client(container_id)
        container.delete_item(item=item_id, partition_key=partition_key)

        return f"Successfully deleted item with ID: {item_id}"
    except Exception as e:
        return f"Error deleting item '{item_id}' from container '{container_id}': {str(e)}"


@mcp.tool
def list_containers() -> str:
    """
    List all container from the current database with their names.
    Useful for discovering available data tables.
    Returns:
        List of container names or error message
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."
        containers = list(cosmos_db.list_containers())
        if not containers:
            return "No containers found in database"
        container_names = [c['id'] for c in containers]
        return "Available containers:\n" + "\n".join(f"- {name}" for name in container_names)
    except Exception as e:
        return f"Error listing containers: {str(e)}"
    

@mcp.tool
def list_value_scopes() -> str:
    """
    List the names or IDs of all value scopes in the 'value_scope' container.

    Returns:
        A formatted string with each value scope name (or ID) on a new line, or an error message if the operation fails or no scopes are found.
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."
        container = cosmos_db.get_container_client("value_scope")
        items = list(container.read_all_items())
        if not items:
            return "No value scopes found in the 'value_scope' container."
        filtered_items = [filter_keys(item) for item in items]
        return json.dumps(filtered_items, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error listing value scopes: {str(e)}"

@mcp.tool
def list_value_scopes_names() -> str:
    """
    List the element_id and scope of all value scopes in the 'value_scope' container.

    Returns:
        A JSON-formatted string with each value scope's element_id and scope, or an error message if the operation fails or no scopes are found.
    """
    import json
    try:
        if cosmos_db is None:
            return "Database connection not initialized."
        container = cosmos_db.get_container_client("value_scope")
        items = list(container.read_all_items())
        if not items:
            return "No value scopes found in the 'value_scope' container."
        result = []
        for item in items:
            entry = {}
            if 'element_id' in item:
                entry['element_id'] = item['element_id']
            if 'scope' in item:
                entry['scope'] = item['scope']
            result.append(entry)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error listing value scopes: {str(e)}"
    

@mcp.tool
def list_implementation_bindings() -> str:
    """
    Retrieve a list of implementation binding names (also referred to as ABBs, Architecture Building Blocks, Building Blocks, building blocks) from the 'implementation_binding' container in the database.

    In the application domain, an implementation binding is synonymous with ABB (Architecture Building Block). This API provides a simple list of all ABB names without any additional metadata.

    AI agents and LLMs can use this API to:
    - Enumerate all ABB (implementation binding) names
    - Get a quick overview of available implementation bindings
    - Use the names for subsequent detailed queries

    Returns:
        A JSON-formatted string containing a list of implementation binding names, or an error message if the operation fails or no bindings are found.
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."
        container = cosmos_db.get_container_client("implementation_binding")
        items = list(container.read_all_items())
        if not items:
            return "No implementation bindings found in the 'implementation_binding' container."
        names = [item.get("name", item.get("id", "unnamed")) for item in items]
        return json.dumps(names, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error listing implementation bindings: {str(e)}"

@mcp.tool
def list_impl_binding_vs(value_scope_id: str) -> str:
    """
    Retrieve all implementation bindings (ABBs) from the 'implementation_binding' container that are referenced by the 'implemented_by' field of a given value scope.

    Args:
        value_scope_id: The element_id or unique identifier of the value scope to filter implementation bindings by.

    Returns:
        A JSON-formatted string containing all implementation bindings within the specified value scope, or an error message if none are found or on failure.
    """
    import json

    # Helper function to recursively filter out keys starting with '_' or 'cnt_'
    def filter_keys(obj):
        if isinstance(obj, dict):
            return {k: filter_keys(v) for k, v in obj.items() if not (k.startswith('_') or k.startswith('cnt_'))}
        elif isinstance(obj, list):
            return [filter_keys(i) for i in obj]
        else:
            return obj

    try:
        # Ensure the database connection is initialized
        if cosmos_db is None:
            return "Database connection not initialized."

        # Get the containers for value_scope and implementation_binding
        vs_container = cosmos_db.get_container_client("value_scope")
        ib_container = cosmos_db.get_container_client("implementation_binding")

        # Retrieve the value_scope document with the given element_id
        vs_query = "SELECT * FROM c WHERE c.element_id = @vs_id"
        vs_items = list(vs_container.query_items(
            query=vs_query,
            parameters=[{"name": "@vs_id", "value": value_scope_id}],
            enable_cross_partition_query=True
        ))
        if not vs_items:
            return f"No value scope found with element_id '{value_scope_id}'."
        value_scope = vs_items[0]

        # Get the list of implementation bindings referenced by this value scope
        implemented_by = value_scope.get("implemented_by")
        if not implemented_by:
            return f"No implementation bindings referenced by value scope '{value_scope_id}'."

        # Extract the element_ids from the implemented_by list
        ib_ids = [ib.get("element_id") for ib in implemented_by if ib.get("element_id")]
        if not ib_ids:
            return f"No valid implementation binding element_ids found in value scope '{value_scope_id}'."

        # Fetch each implementation_binding document by its element_id
        ib_docs = []
        for ib_id in ib_ids:
            # Query for the implementation_binding with the given element_id
            ib_query = "SELECT * FROM c WHERE c.element_id = @ib_id"
            ib_items = list(ib_container.query_items(
                query=ib_query,
                parameters=[{"name": "@ib_id", "value": ib_id}],
                enable_cross_partition_query=True
            ))
            ib_docs.extend(ib_items)

        if not ib_docs:
            return f"No implementation binding documents found for referenced element_ids in value scope '{value_scope_id}'."

        # Return only the element_id and name for each implementation_binding
        result = []
        for item in ib_docs:
            entry = {}
            if 'element_id' in item:
                entry['element_id'] = item['element_id']
            if 'name' in item:
                entry['name'] = item['name']
            result.append(entry)
        return json.dumps(result, indent=2, ensure_ascii=False)
    except Exception as e:
        # Return a helpful error message if anything goes wrong
        return f"Error listing implementation bindings for value scope '{value_scope_id}': {str(e)}"

        
@mcp.tool
def list_products() -> str:
    """
    Retrieve all products (also referred to as ADAS products) from the 'product' container in the database.

    This API provides a comprehensive list of all products, including all attributes and nested data structures for each product. It is useful for discovering product metadata, ownership, deployment views, architectural relationships, and KPI data.

    AI agents and LLMs can use this API to:
    - Enumerate all products and their metadata
    - Analyze product ownership, architecture, and deployment relationships
    - Extract links to product properties, KPIs, and configuration details
    - Integrate or synchronize product data with other systems
    - Support queries for reporting, compliance, and product lifecycle management

    Returns:
        A JSON-formatted string containing all products and their attributes, or an error message if the operation fails or no products are found.
    """
    try:
        if cosmos_db is None:
            return "Database connection not initialized."
        container = cosmos_db.get_container_client("product")
        items = list(container.read_all_items())
        if not items:
            return "No products found in the 'product' container."
        filtered_items = [filter_keys(item) for item in items]
        return json.dumps(filtered_items, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error listing products: {str(e)}"


if __name__ == "__main__":
    transport, mcp_port, mcp_binding = init_mcp_server()
    if transport in ["http", "streamable-http", "sse"] and mcp_port is not None:
        mcp.run(transport, host=mcp_binding, port=mcp_port)
    else:
        mcp.run(transport)
