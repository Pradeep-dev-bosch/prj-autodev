"""
MCP Server for CANoe - Local/Remote Client
This server acts as an MCP interface that communicates with a remote CANoe server via HTTP.
"""

import logging
import os
from typing import Any, Dict, Optional

import requests
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("canoe-mcp-server")

# Get remote server URL from environment or use default
REMOTE_SERVER_URL: Optional[str] = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.
    Returns:
        tuple[str, str, int]: A tuple containing:
            - transport_type (str): Transport protocol type, defaults to "stdio"
            - host (str): Server host address, defaults to "127.0.0.1"
            - port (int): Server port number, defaults to "8000"
    """
    global REMOTE_SERVER_URL

    REMOTE_SERVER_URL = os.getenv("TESTBENCH_ADDRESS") or None

    if REMOTE_SERVER_URL is None:
        logging.error("TESTBENCH_ADDRESS environment variable is not set.")
        raise ValueError("TESTBENCH_ADDRESS environment variable is not set.")

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


def _call_remote(
    endpoint: str, method: str = "GET", params: Optional[Dict] = None, json_data: Optional[Dict] = None
) -> Any:
    """Helper to call remote CANoe server API."""
    try:
        url = f"http://{REMOTE_SERVER_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url, params=params)
        elif method == "POST":
            response = requests.post(url, json=json_data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Extract detail message from the response body (FastAPI returns {"detail": "..."})
        try:
            error_detail = e.response.json().get("detail", str(e))
        except Exception:
            error_detail = str(e)
        return {"error": f"Remote server error: {error_detail}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Remote server error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """
    Check health status of the remote CANoe server.

    Returns:
        dict: Health status including CANoe initialization state and version.
    """
    return _call_remote("/health", method="GET")


@mcp.tool()
async def launch_canoe(config_path: str = "") -> Dict[str, Any]:
    """
    Launch CANoe application on remote server.

    Args:
        config_path (str, optional): Path to CANoe config file on remote server. Default is empty.

    Returns:
        dict: Launch status with CANoe version information.
    """
    params = {}
    if config_path:
        params["config_path"] = config_path

    return _call_remote("/launch_canoe", method="GET", params=params)


@mcp.tool()
async def load_configuration(config_path: str) -> Dict[str, Any]:
    """
    Load a CANoe configuration file on remote server.

    Args:
        config_path (str): Path to the CANoe config file on remote server.

    Returns:
        dict: Configuration load status.
    """
    return _call_remote("/load_configuration", method="POST", json_data={"config_path": config_path})


@mcp.tool()
async def start_measurement() -> Dict[str, Any]:
    """
    Start measurement in CANoe on remote server.

    Returns:
        dict: Measurement start status.
    """
    return _call_remote("/start_measurement", method="GET")


@mcp.tool()
async def stop_measurement() -> Dict[str, Any]:
    """
    Stop measurement in CANoe on remote server.

    Returns:
        dict: Measurement stop status.
    """
    return _call_remote("/stop_measurement", method="GET")


@mcp.tool()
async def add_xcp_configuration(xcp_configuration_file_path: str) -> Dict[str, Any]:
    """
    Add XCP configuration file to CANoe on remote server.

    Args:
        xcp_configuration_file_path (str): Path to XCP config file on remote server.

    Returns:
        dict: XCP configuration load status.
    """
    return _call_remote(
        "/add_xcp_configuration", method="POST", json_data={"xcp_configuration_file_path": xcp_configuration_file_path}
    )


@mcp.tool()
async def remove_all_xcp_devices() -> Dict[str, Any]:
    """
    Remove all XCP devices from CANoe configuration on remote server.

    Returns:
        dict: XCP devices removal status.
    """
    return _call_remote("/remove_all_xcp_devices", method="GET")


@mcp.tool()
async def get_sysvar_value(namespace: str, name: str) -> Dict[str, Any]:
    """
    Get the value of a CANoe system variable from remote server.

    Args:
        namespace (str): Namespace of the system variable.
        name (str): Name of the system variable.

    Returns:
        dict: System variable value.
    """
    return _call_remote("/get_sysvar_value", method="GET", params={"namespace": namespace, "name": name})


@mcp.tool()
async def set_sysvar_value(namespace: str, name: str, value: Any) -> Dict[str, Any]:
    """
    Set the value of a CANoe system variable on remote server.

    Args:
        namespace (str): Namespace of the system variable.
        name (str): Name of the system variable.
        value (int | float | str): Value to set.

    Returns:
        dict: System variable set status.
    """
    return _call_remote(
        "/set_sysvar_value", method="POST", json_data={"namespace": namespace, "name": name, "value": value}
    )


@mcp.tool()
async def get_test_configurations_info() -> Dict[str, Any]:
    """
    Get information about all test configurations in CANoe on remote server.

    Returns:
        dict: Test configurations information.
    """
    return _call_remote("/get_test_configurations_info", method="GET")


@mcp.tool()
async def create_test_configuration(test_config_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new test configuration in CANoe on remote server.

    Args:
        test_config_name (str, optional): Name for the new test configuration.

    Returns:
        dict: Test configuration creation status.
    """
    json_data = {}
    if test_config_name:
        json_data["test_config_name"] = test_config_name

    return _call_remote("/create_test_configuration", method="POST", json_data=json_data)


@mcp.tool()
async def execute_test_configuration(test_suite: str, sw_variant: Optional[str] = None) -> Dict[str, Any]:
    """
    Execute test configuration(s) in CANoe on remote server.

    Args:
        test_suite (str): Comma-separated test configuration names.
        sw_variant (str, optional): Software variant profile to apply.

    Returns:
        dict: Test execution results.
    """
    json_data = {"test_suite": test_suite}
    if sw_variant:
        json_data["sw_variant"] = sw_variant

    return _call_remote("/execute_test_configuration", method="POST", json_data=json_data)


@mcp.tool()
async def add_test_unit_to_test_config(
    test_unit_path: str, test_config_item_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Add test unit(s) to a test configuration in CANoe on remote server.

    Args:
        test_unit_path (str): Path to test unit file or folder on remote server.
        test_config_item_id (int, optional): Test configuration ID (1-based index).

    Returns:
        dict: Test unit add status.
    """
    json_data = {"test_unit_path": test_unit_path}
    if test_config_item_id is not None:
        json_data["test_config_item_id"] = test_config_item_id

    return _call_remote("/add_test_unit_to_test_config", method="POST", json_data=json_data)


@mcp.tool()
async def get_test_environments_info() -> Dict[str, Any]:
    """
    Get information about all test environments in CANoe on remote server.

    Returns:
        dict: Test environments information.
    """
    return _call_remote("/get_test_environments_info", method="GET")


@mcp.tool()
async def add_test_environment(test_environment_file_path: str) -> Dict[str, Any]:
    """
    Add a test environment to CANoe configuration on remote server.

    Args:
        test_environment_file_path (str): Path to test environment file on remote server.

    Returns:
        dict: Test environment add status.
    """
    return _call_remote(
        "/add_test_environment", method="POST", json_data={"test_environment_file_path": test_environment_file_path}
    )


@mcp.tool()
async def create_test_environment(test_environment_name: str) -> Dict[str, Any]:
    """
    Create a test environment in CANoe on remote server.

    Args:
        test_environment_name (str): Name of the test environment to create.

    Returns:
        dict: Test environment creation status.
    """
    return _call_remote(
        "/create_test_environment", method="POST", json_data={"test_environment_name": test_environment_name}
    )


@mcp.tool()
async def add_xml_test_module_to_test_environment(
    test_module_path: str, test_environment_name: str, test_module_components_list: list
) -> Dict[str, Any]:
    """
    Add XML test module to a test environment in CANoe on remote server.

    Args:
        test_module_path (str): Path to XML test module file on remote server.
        test_environment_name (str): Name of the test environment.
        test_module_components_list (list): List of test module components to add.

    Returns:
        dict: Test module add status.
    """
    return _call_remote(
        "/add_xml_test_module_to_test_environment",
        method="POST",
        json_data={
            "test_module_path": test_module_path,
            "test_environment_name": test_environment_name,
            "test_module_components_list": test_module_components_list,
        },
    )


@mcp.tool()
async def add_capl_test_module_to_test_environment(test_module_path: str, test_environment_name: str) -> Dict[str, Any]:
    """
    Add CAPL test module to a test environment in CANoe on remote server.

    Args:
        test_module_path (str): Path to CAPL test module file on remote server.
        test_environment_name (str): Name of the test environment.

    Returns:
        dict: Test module add status.
    """
    return _call_remote(
        "/add_capl_test_module_to_test_environment",
        method="POST",
        json_data={"test_module_path": test_module_path, "test_environment_name": test_environment_name},
    )


@mcp.tool()
async def execute_test_environment(test_environments: str) -> Dict[str, Any]:
    """
    Execute test environment(s) in CANoe on remote server.

    Args:
        test_environments (str): Comma-separated test environment names.

    Returns:
        dict: Test execution results.
    """
    return _call_remote("/execute_test_environment", method="POST", json_data={"test_environments": test_environments})


@mcp.tool()
async def execute_test_modules(test_module_names: str) -> Dict[str, Any]:
    """
    Execute test module(s) in CANoe on remote server.

    Args:
        test_module_names (str): Comma-separated test module names.

    Returns:
        dict: Test execution results.
    """
    return _call_remote("/execute_test_modules", method="POST", json_data={"test_module_names": test_module_names})


@mcp.tool()
async def enable_disable_measurement_setup_block(block_name: str, active: bool) -> Dict[str, Any]:
    """
    Enable or disable a measurement setup block in CANoe on remote server.

    Args:
        block_name (str): Name of the measurement setup block.
        active (bool): True to enable, False to disable.

    Returns:
        dict: Block status update result.
    """
    return _call_remote(
        "/enable_disable_measurement_setup_block", method="POST", json_data={"block_name": block_name, "active": active}
    )


@mcp.tool()
async def get_logging_block_list() -> Dict[str, Any]:
    """
    Get list of logging blocks in CANoe measurement setup on remote server.

    Returns:
        dict: List of logging blocks.
    """
    return _call_remote("/get_logging_block_list", method="GET")


@mcp.tool()
async def quit_canoe(save_cfg: bool = False) -> Dict[str, Any]:
    """
    Quit CANoe application on remote server.

    Args:
        save_cfg (bool, optional): Save configuration changes before quitting. Default is False.

    Returns:
        dict: Quit status message and any force-killed processes.
    """
    return _call_remote("/quit_canoe", method="GET", params={"save_cfg": save_cfg})


@mcp.tool()
async def get_simulation_setup_info() -> Dict[str, Any]:
    """
    Get information about the simulation setup in CANoe on remote server.

    Returns:
        dict: Simulation setup information including buses, nodes, and their configurations.
    """
    return _call_remote("/get_simulation_setup_info", method="GET")


@mcp.tool()
async def get_canoe_configuration_info() -> Dict[str, Any]:
    """
    Get CANoe configuration project path that is loaded.

    Returns:
        dict: Configuration info including Name and Path.
    """
    return _call_remote("/get_canoe_configuration_info", method="GET")


if __name__ == "__main__":
    # Initialize and run the MCP server
    logging.info(f"Starting CANoe MCP Remote Client - connecting to {REMOTE_SERVER_URL}")

    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
