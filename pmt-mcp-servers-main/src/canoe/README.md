# CANoe MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides comprehensive integration with Vector CANoe application.

## Overview

The CANoe MCP Server provides remote integration with Vector CANoe application through a client-server architecture. It enables AI assistants to control CANoe measurements, execute test configurations, manage system variables, and orchestrate automotive test scenarios directly from MCP-enabled clients (e.g., VS Code Copilot Chat).

The server consists of two components:

1. **Remote CANoe Server** - FastAPI-based server running on Windows with CANoe installed
2. **MCP Client** - MCP interface that communicates with the remote server via HTTP

### Limitations

- Currently, only test execution related tools are available. Additional CANoe automation tools will be added in future releases
- Multiple concurrent CANoe instances not supported
- Depending on the LLM models, accuracy might differ. Premium models like GPT-5 or Claude Sonnet 4.5 are recommended for better performance with complex test automation tasks

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- **Test Bench Requirements:**
  - Vector CANoe application installed and licensed
  - Python installed
  - Network accessibility to the test bench

### Remote Server Setup

The remote CANoe server must be set up on the test bench machine where CANoe is installed:

#### 1. Copy Required Files to Test Bench

Before starting the server, ensure the necessary files are available on the test bench. You have two options:

**Option A: Clone the Repository**

```cmd
git clone https://github.com/bosch-rbadas/pmt-mcp-servers.git
cd pmt-mcp-servers\src\canoe
```

**Option B: Copy Files Manually**

Copy the following files to the test bench:

- `start_canoe_remoteserver.bat` - Startup script
- `remotecanoeserver.py` - Remote server implementation

#### 2. Start the Remote Server

Run the provided batch script on the Windows test bench:

```cmd
start_canoe_remoteserver.bat
```

The script will:

- Create a Python virtual environment (if not exists)
- Install required dependencies (FastAPI, uvicorn, pywin32, pydantic)
- Prompt for the port number (default: 8037)
- Start the remote server

#### 3. Configure Windows Firewall

To allow remote connections to the CANoe server, you must configure the Windows firewall to permit inbound connections on the chosen port.

**Run PowerShell as Administrator** and execute:

```powershell
New-NetFirewallRule -DisplayName "CANoe Remote Server Port" -Direction Inbound -Action Allow -Protocol TCP -LocalPort <PORT>
```

Replace `<PORT>` with your chosen port number.

**Example with custom port:**

```powershell
New-NetFirewallRule -DisplayName "CANoe Remote Server 9000" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 9000
```

#### 4. Verify Server Status

Once started, the remote server will be accessible at:

```
http://<testbench-hostname>:<port>/health
```

Example: `http://ABC-X-0000.abt.de.bosch.com:1234/health`

> **⚠️ Important Note: Before logging out of the Testbench after completing your work, ensure you close the remote server bat terminal window. This prevents the server from continuing to run in the background and ensures proper cleanup of resources. The server will not be available after you log out if the terminal is closed.**

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

**Configuration Steps:**

1. Copy the `mcp.json` template to your workspace's `.vscode/` folder
2. Replace `<TESTBENCH_ADDRESS>` with your test bench hostname or IP address (e.g., `ABC-X-0000.abt.de.bosch.com` , `10.210.111.1`)
3. Replace `<CANOE_REMOTE_PORT>` with the port number (e.g., `8037`)
4. Configure transport settings (default: `stdio`)

Example configuration:

```json
{
  "servers": {
    "canoe-python-mcp-server": {
      "cwd": "${workspaceFolder}/src/canoe",
      "command": "uv",
      "args": ["run", "canoemcpserver.py"],
      "env": {
        "TESTBENCH_ADDRESS": "ABC-X-0000.abt.de.bosch.com:1234",
        "TRANSPORT": "<TRANSPORT>",
        "HOST": "<HOST>",
        "HOST_PORT": "<HOST_PORT>"
      }
    }
  }
}
```

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with CANoe using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Launch CANoe and load configuration from C:\CANoe\MyProject.cfg"
- "Start measurement in CANoe"
- "Get the value of system variable MyNamespace::MyVariable"
- "Set system variable TestSignals::Speed to 100"
- "Execute test configuration named 'Functional Tests'"
- "Get all test environments in the loaded configuration"
- "Execute test modules named 'TestModule1, TestModule2' and get the report"
- "Add XCP configuration from C:\CANoe\ECU_Config.a2l"
- "Enable logging block named 'DataLogger1'"
- "Stop measurement and quit CANoe"

The AI assistant will translate these natural language requests into appropriate CANoe API calls and execute them on the remote test bench.

### Features

The server provides comprehensive CANoe automation capabilities with over 20 specialized MCP tools covering:

- Application lifecycle management (launch, quit, configuration loading)
- Measurement control (start, stop, status monitoring)
- System variable manipulation (get, set)
- Test automation (test configurations, environments, modules)
- XCP device management
- Logging and measurement setup control
- Test execution and result collection

The following MCP tools are available for comprehensive CANoe management:

- **Application Control**:

  - `health_check` - Check health status of the remote CANoe server
  - `launch_canoe` - Launch CANoe application with optional configuration
  - `quit_canoe` - Quit CANoe application with optional save
  - `load_configuration` - Load a CANoe configuration file
  - `start_measurement` - Start a CANoe measurement
  - `stop_measurement` - Stop the running measurement

- **Simulation Management**:

    - `get_simulation_setup_info` - Get details of simulation setup structure
    - `get_canoe_configuration_info` - Get configuration info

- **Measurement Management**:

  - `enable_disable_measurement_setup_block` - Enable or disable measurement setup blocks
  - `get_logging_block_list` - Get list of logging blocks in the measurement setup

- **System Variables**:

  - `get_sysvar_value` - Get the value of a CANoe system variable
  - `set_sysvar_value` - Set the value of a CANoe system variable

- **Test Configuration Management**:

  - `get_test_configurations_info` - Get information about all test configurations
  - `create_test_configuration` - Create a new test configuration
  - `execute_test_configuration` - Execute test configuration(s) with optional SW variant
  - `add_test_unit_to_test_config` - Add test unit(s) to a test configuration

- **Test Environment Management**:

  - `get_test_environments_info` - Get information about all test environments
  - `create_test_environment` - Create a new test environment
  - `add_test_environment` - Add an existing test environment file
  - `execute_test_environment` - Execute test environment(s)
  - `add_capl_test_module_to_test_environment` - Add CAPL test module to environment
  - `add_xml_test_module_to_test_environment` - Add XML test module to environment
  - `execute_test_modules` - Execute specific test module(s) by name

- **XCP Device Management**:
  - `add_xcp_configuration` - Add XCP configuration file to CANoe
  - `remove_all_xcp_devices` - Remove all XCP devices from configuration

### Configuration

The MCP client requires the following environment variables in `mcp.json`:

| Variable            | Description                     | Example                            |
| ------------------- | ------------------------------- | ---------------------------------- |
| `TESTBENCH_ADDRESS` | Test bench hostname and port    | `ABC-X-0000.abt.de.bosch.com:1234` |
| `TRANSPORT`         | MCP transport protocol          | `stdio` (default)                  |
| `HOST`              | MCP server host (for non-stdio) | `127.0.0.1` (default)              |
| `HOST_PORT`         | MCP server port (for non-stdio) | `8000` (default)                   |

### Troubleshooting

#### Remote Server Issues

> **⚠️ Important:** Always close the remote server bat terminal window before logging out of the Testbench when you're done with your work and no longer need the MCP server. This ensures proper resource cleanup and prevents orphaned processes.

| Issue                         | Solution                                                                          |
| ----------------------------- | --------------------------------------------------------------------------------- |
| Server fails to start         | Ensure Python is installed and available in PATH                                  |
| CANoe not found               | Verify CANoe is installed and properly licensed on the Windows machine            |
| Port already in use           | Choose a different port or stop the process using the current port                |
| Firewall blocking connections | Run the PowerShell command to allow inbound connections (see Remote Server Setup) |
| Virtual environment errors    | Delete `venv` folder and restart `start_canoe_remoteserver.bat`                   |
| MCP tool returns error        | Try closing the `start_remotecanoeserver.bat` window and start it again                      |

#### MCP Client Issues

| Issue                                               | Solution                                                                        |
| --------------------------------------------------- | ------------------------------------------------------------------------------- |
| "TESTBENCH_ADDRESS environment variable is not set" | Verify `TESTBENCH_ADDRESS` is configured in `mcp.json`                          |
| Connection timeout                                  | Check network connectivity to test bench and firewall rules                     |
| Remote server error                                 | Verify remote server is running and accessible at the specified address         |
| Remote address not found                            | Verify remote server address is correct try with IP address instead of hostname |

#### CANoe Operation Issues

| Issue                       | Solution                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------ |
| Configuration fails to load | Verify the configuration file path exists on the Windows machine                     |
| Measurement won't start     | Check if CANoe configuration is valid and hardware is connected                      |
| System variable not found   | Verify namespace and variable name are correct - check CANoe System Variables window |
| Test execution fails        | Ensure test configurations/environments exist in the loaded CANoe configuration      |
| XCP device errors           | Verify XCP configuration file path and format are correct                            |

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Vector CANoe About](https://www.vector.com/int/en/products/products-a-z/software/canoe/)
