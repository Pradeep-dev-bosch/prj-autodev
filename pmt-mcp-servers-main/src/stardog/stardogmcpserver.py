import json
import logging
import os

from fastmcp import FastMCP

import stardog

mcp = FastMCP("StardogMCPServer")


@mcp.tool()
def stardog_sparql_query(query: str) -> str:
    """Execute a SPARQL query against the Stardog database.

    Args:
        query: SPARQL query to execute. Supports SELECT queries.
               Example: "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"

    Returns:
        JSON string containing the query results or error message.
    """
    logging.debug(f"Querying Stardog with SPARQL: {query}")

    conn_details: dict[str, str | None] = {
        "endpoint": os.getenv("STARDOG_ENDPOINT"),
        "username": os.getenv("STARDOG_USERNAME"),
        "password": os.getenv("STARDOG_PASSWORD"),
        "database": os.getenv("STARDOG_DATABASE"),
    }

    # Validate that all required environment variables are set
    missing_vars = [key for key, value in conn_details.items() if value is None]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variable(s): {', '.join('STARDOG_' + key.upper() for key in missing_vars)}"
        )

    try:
        with stardog.Connection(**conn_details) as conn:
            results = conn.select(query)

        if isinstance(results, bytes):
            return json.dumps(results.decode("utf-8"))
        else:
            return json.dumps(results)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return json.dumps({"Error": "An internal error occurred. Please check the server logs."})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    mcp.run()  # Uses STDIO transport by default
