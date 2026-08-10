"""
DRIVE COMPANION MCP Server
"""

import json
import logging
import os
from typing import Optional
from urllib.parse import urljoin

import httpx
import requests
import urllib3
from fastmcp import FastMCP

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global configuration
drivecompanion_url: Optional[str] = None
drivecompanion_api_key: Optional[str] = None

mcp = FastMCP("drivecompanion-mcp-server")


def initialize_drivecompanion():
    """
    Initializes the global drivecompanion client configuration.

    Raises:
        ValueError: If any required environment variable is missing.
    """
    global drivecompanion_url, drivecompanion_api_key

    # drivecompanion configuration from environment variables
    drivecompanion_url = os.getenv("DRIVECOMPANION_URL")
    drivecompanion_api_key = os.getenv("DRIVECOMPANION_API_KEY")

    # Validate required environment variables
    missing_vars = [
        name
        for name, value in {
            "DRIVECOMPANION_URL": drivecompanion_url,
            "DRIVECOMPANION_API_KEY": drivecompanion_api_key,
        }.items()
        if not value
    ]
    if missing_vars:
        raise ValueError(f"Missing required environment variable(s): {', '.join(missing_vars)}")

    # Ensure URL ends with /
    if not drivecompanion_url.endswith("/"):
        drivecompanion_url = drivecompanion_url + "/"

    logging.info(f"drivecompanion client initialized with URL: {drivecompanion_url}")


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration."""
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
    """Recursively convert non-serializable objects to JSON-safe types."""
    if data is None:
        return None

    if isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, dict):
        return {key: safe_serialize(value) for key, value in data.items()}

    if isinstance(data, (list, tuple)):
        return [safe_serialize(item) for item in data]

    if isinstance(data, set):
        return [safe_serialize(item) for item in data]

    if hasattr(data, "__iter__") and not isinstance(data, (str, bytes, bytearray)):
        try:
            return [safe_serialize(item) for item in data]
        except TypeError:
            return str(data)

    try:
        json.dumps(data)
        return data
    except (TypeError, ValueError):
        return str(data)


@mcp.tool()
async def query_model(
    model: str,
    prompt: str,
) -> str:
    """
    Chat with DRIVE COMPANION chat interface - supports plain chat with streaming

    Args:
        model: Model identifier (e.g., "XC DRIVE Companion", "DRIVE Companion")
               Get available models via the list_models tool 
        prompt: message string to ask DRIVE companion chatbot models
                Example: "Get the latest info on product X"

    Returns:
        str: JSON with response or error

    Examples:
        >>> await query_model("XC DRIVE Companion", 'Hi')
    """
    try:
        
        # files are not supported yet
        file_ids: str = ""
        collection_ids: str = ""

        messages_list = [{"role": "user", "content": str(prompt)}]

        # Build payload with streaming enabled
        payload = {"model": model, "messages": messages_list, "stream": True}

        # Add file_ids if provided
        if file_ids:
            try:
                file_ids_list = json.loads(file_ids)
                if isinstance(file_ids_list, list):
                    payload["files"] = [{"type": "file", "id": fid} for fid in file_ids_list]
            except json.JSONDecodeError:
                return json.dumps({"error": "Invalid JSON for file_ids"})

        # Add collection_ids if provided
        if collection_ids:
            try:
                collection_ids_list = json.loads(collection_ids)
                if isinstance(collection_ids_list, list):
                    payload["metadata"] = {"knowledge_ids": collection_ids_list}
            except json.JSONDecodeError:
                return json.dumps({"error": "Invalid JSON for collection_ids"})

        # Make async request
        api_endpoint = urljoin(drivecompanion_url, "api/chat/completions")
        headers = {
            "Authorization": f"Bearer {drivecompanion_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient(verify=False, timeout=300.0) as client:
            async with client.stream(
                "POST",
                api_endpoint,
                headers=headers,
                json=payload
            ) as response:
                
                if response.status_code == 200:
                    # Handle streaming response
                    full_content = ""

                    async for line in response.aiter_lines():
                        if line:
                            line_text = line.strip()

                            # Skip empty lines
                            if not line_text:
                                continue

                            # Remove "data: " prefix if present
                            if line_text.startswith("data: "):
                                line_text = line_text[6:]

                            # Check for end of stream
                            if line_text.strip() == "[DONE]":
                                break

                            try:
                                # Parse the JSON chunk
                                chunk = json.loads(line_text)

                                # Extract content from the chunk
                                if "choices" in chunk and len(chunk["choices"]) > 0:
                                    delta = chunk["choices"][0].get("delta", {})
                                    if "content" in delta:
                                        content = delta["content"]
                                        full_content += content
                            except json.JSONDecodeError:
                                # Skip lines that aren't valid JSON
                                continue

                    # Return the accumulated content
                    return json.dumps({
                        "success": True, 
                        "content": full_content, 
                        "characters": len(full_content)
                    })
                else:
                    error_detail = await response.aread()
                    try:
                        error_json = response.json()
                        if "detail" in error_json:
                            error_detail = error_json["detail"]
                    except Exception as e:
                        logging.error(f"Error parsing error response JSON: {e}", exc_info=True)

                    return json.dumps({
                        "error": f"API request failed ({response.status_code}): {error_detail}"
                    })

    except httpx.TimeoutException:
        return json.dumps({"error": "Request timed out"})
    except httpx.ConnectError as e:
        return json.dumps({"error": f"Connection failed: {str(e)}"})
    except Exception as e:
        logging.error(f"Error in chat: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def list_models() -> str:
    """
    List all available models in DRIVE COMPANION.

    Returns:
        str: JSON with list of models

    Example:
        >>> list_models()
        {"success": True, "models": [{"id": "sage_xc_agent", ...}, ...]}
    """
    try:
        api_endpoint = urljoin(drivecompanion_url, "api/models")
        headers = {
            "Authorization": f"Bearer {drivecompanion_api_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(
            api_endpoint,
            headers=headers,
            timeout=30,
            verify=False, # Disable SSL verification (need to find betterway for docker version of mcp server)
        )

        if response.status_code == 200:
            response_data = response.json()
            return json.dumps({"success": True, "models": safe_serialize(response_data.get("data", []))})
        else:
            return json.dumps({"error": f"Failed to list models ({response.status_code}): {response.text}"})

    except Exception as e:
        logging.error(f"Error listing models: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    initialize_drivecompanion()
    transport, host, port = get_mcp_init_vars()

    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
