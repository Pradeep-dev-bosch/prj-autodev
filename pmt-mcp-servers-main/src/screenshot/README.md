# MCP Screenshot Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides screenshot capture capabilities for Windows environments.

## Overview

The MCP Screenshot Server provides integration with Windows screenshot functionality. It exposes a tool for capturing screenshots directly inside MCP-enabled clients (e.g. VS Code Copilot Chat).

The server is built with the `FastMCP` framework and Python's `PIL/Pillow` library.

### Limitations

⚠️ **Platform Limitation**: This server uses `PIL.ImageGrab` which **only works on Windows OS**. It does not support WSL (Windows Subsystem for Linux) or Docker containers due to the lack of Windows GUI access in those environments.

- Screenshots of DRM-protected content may appear black
- Multi-monitor setups capture the primary display only
- Some applications may block screen capture due to privacy settings

## Getting Started

### Prerequisites

- **Windows OS** (required - does not work in WSL or Docker)
- Python 3.10+
- UV package manager
- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the MCP server after adding `.vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with the screenshot tool using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "Take a screenshot and save it to my desktop"
- "Capture the screen"
- "Take a screenshot and save it to C:/temp/screen.png"
- "Capture a screenshot to my Documents folder"

The AI assistant will translate these natural language requests into actual screenshot capture operations.

### Features

The server provides a single specialized MCP tool:

- **Screenshot Capture**:
  - `take_screenshot` - Capture full screen with optional custom save path

**Tool: `take_screenshot`**
- **Parameters:**
  - `save_path` (optional): Full path where to save the screenshot. If not provided, saves to a temp directory with timestamp.
- **Returns:** Path to the saved screenshot file

### Configuration

No environment variables are required. The server runs locally and uses Windows GUI access.

**Note:** Ensure your Windows privacy settings allow screen capture for Python applications.

### Troubleshooting

#### Connection Issues
- **"X get_image failed" or similar errors**: This typically means you're trying to run on WSL or in a Docker container
  - Solution: Run directly on Windows using Windows Python installation
- **"Module import errors"**: Ensure all dependencies are installed: `uv sync`
- **"Permission denied"**: Check Windows privacy settings for screen recording permissions

#### Common Errors
- **Screenshot is black or empty**:
  - Ensure no applications are blocking screen capture
  - Check Windows privacy settings for screen recording permissions
  - Some DRM-protected content may appear black in screenshots
- **"No module named 'PIL'"**: Run `uv sync` to install dependencies
- **File save errors**: Ensure the target directory exists and you have write permissions

## Platform Support

| Platform | Supported | Notes |
|----------|-----------|-------|
| Windows | ✅ Yes | Full support with PIL.ImageGrab |
| WSL | ❌ No | ImageGrab cannot access Windows GUI from WSL |
| Docker | ❌ No | No GUI access in containers |
| Linux | ❌ No | ImageGrab is Windows-only; use alternative tools like `scrot` |
| macOS | ✅ Partial | ImageGrab works but with limited functionality |

## Alternative Solutions for WSL/Linux

If you need screenshot capabilities on WSL or Linux, consider:
- **scrot**: `sudo apt install scrot && scrot ~/screenshot.png`
- **imagemagick**: `sudo apt install imagemagick && import -window root screenshot.png`
- **gnome-screenshot**: `gnome-screenshot -f ~/screenshot.png`

These can be wrapped in a separate MCP server for Linux environments.

## Further Information

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
