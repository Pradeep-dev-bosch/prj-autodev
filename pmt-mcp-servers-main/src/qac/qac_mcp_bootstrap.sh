#!/usr/bin/env bash
set -e

MCP_HOME="$HOME/.mcp/qac"
BIN_TARGET="/usr/local/bin/qac-mcp"
BIN_NAME="qac-mcp"
PYTHON_BIN=$(command -v python3 || command -v python)

# Ensure parent directory exists
if [ ! -d "$MCP_HOME" ]; then
  echo "Creating $HOME/.mcp/qac directory"
  mkdir -p $MCP_HOME
fi

# Creating Virtual Environment for MCP
if [ ! -x "$MCP_HOME/bin/python" ]; then
  echo "Creating MCP venv at $MCP_HOME"
  "$PYTHON_BIN" -m venv "$MCP_HOME"
  "$MCP_HOME/bin/pip" install --upgrade pip
else
  echo "MCP venv already exists"
fi

# Install or upgrade MCP package
echo "Installing / upgrading qac-mcp-server package"
  "$MCP_HOME/bin/pip" install qac-mcp-server \
  --extra-index-url https://artifactory.boschdevcloud.com/artifactory/api/pypi/pmt-mcp-servers-pypi-local/simple \
  --upgrade

# Create CLI command for qac-mcp-server
if [ -w "/usr/local/bin" ]; then
  ln -sf "$MCP_HOME/bin/$BIN_NAME" "$BIN_TARGET"
else
  mkdir -p "$HOME/.local/bin"
  ln -sf "$MCP_HOME/bin/$BIN_NAME" "$HOME/.local/bin/$BIN_NAME"
fi

echo "qac-mcp-server is now available as '$BIN_NAME'"