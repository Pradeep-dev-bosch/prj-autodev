# Splunk MCP Server

A production-ready Model Context Protocol (MCP) server that provides secure access to Splunk search, analytics, and resource management capabilities.

## Overview

The Splunk MCP Server enables MCP-enabled clients (like VS Code Copilot Chat, Claude Desktop, or other AI assistants) to interact with Splunk Enterprise instances. It provides a comprehensive set of tools for executing searches, retrieving events, managing indexes, and accessing saved searches/dashboards with built-in security guardrails.

## Features

- **7 Powerful MCP Tools**:
  - `validate_spl` - Validate SPL queries with risk assessment
  - `search_oneshot` - Execute one-shot searches with immediate results
  - `search_export` - Stream large result sets efficiently
  - `get_indexes` - List and inspect Splunk indexes
  - `get_saved_searches` - Access saved searches and dashboards
  - `run_saved_search` - Execute saved searches by name
  - `get_config` - Retrieve current server configuration

- **Security Guardrails**:
  - SPL query risk scoring (0-100 scale)
  - Configurable risk tolerance thresholds
  - Event count limits to prevent resource exhaustion
  - SSL/TLS verification controls
  - Output sanitization options

- **Flexible Output Formats**:
  - JSON (structured data)
  - Markdown (human-readable tables)
  - CSV (spreadsheet import)
  - Summary (executive overview)

- **Enterprise-Ready**:
  - Interactive credential management
  - Proxy support (HTTP/HTTPS)
  - Comprehensive logging with session tracking
  - Docker containerization
  - Python 3.11+ compatibility

## Project Structure

```
.
├── Dockerfile              # Docker build configuration
├── docker-compose.yml      # Docker compose setup
├── mcp.json               # MCP client configuration
├── pyproject.toml         # Python project metadata
├── uv.lock                # Locked dependencies
├── .python-version        # Python version specification
├── README.md              # This file
├── RELEASES.md            # Release notes
├── server.py              # Entry point wrapper
├── splunkmcpserver.py     # Main server implementation
├── splunk_client.py       # Splunk REST API client
├── guardrails.py          # Security validation logic
├── spl_risk_rules.py      # SPL query risk rules
├── helpers.py             # Utility functions
└── logs/                  # Session logs directory
```

## Prerequisites

- **Python**: 3.11 or higher
- **Splunk Access**: Enterprise instance with API access (port 8089)
- **Credentials**: Username/password or API token
- **Optional**: Docker for containerized deployment
- **Optional**: UV package manager (recommended)

## Installation

See the [main MCP servers installation guide](../README.md#running-mcp-servers-for-development) for general setup instructions including UV installation and Docker configuration.

For Splunk-specific setup:
```bash
cd src/splunk
uv sync
```

## Configuration

### MCP Client Setup

The `mcp.json` file provides two deployment options:

#### Option 1: Python (UV)
```json
{
  "servers": {
    "splunk-python-mcp-server": {
      "command": "uv",
      "cwd": "/path/to/splunk",
      "args": ["run", "--python", "3.11", "mcp-splunk"],
      "env": {
        "SPLUNK_HOST": "${input:splunk-host}",
        "SPLUNK_PORT": "${input:splunk-port}",
        "SPLUNK_USERNAME": "${input:splunk-username}",
        "SPLUNK_PASSWORD": "${input:splunk-password}",
        "SPLUNK_VERIFY_SSL": "false",
        "TRANSPORT": "stdio"
      }
    }
  }
}
```

#### Option 2: Docker
```json
{
  "servers": {
    "splunk-docker-mcp-server": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-splunk:latest"],
      "env": {
        "SPLUNK_HOST": "${input:splunk-host}",
        "SPLUNK_PORT": "${input:splunk-port}",
        "SPLUNK_USERNAME": "${input:splunk-username}",
        "SPLUNK_PASSWORD": "${input:splunk-password}"
      }
    }
  }
}
```

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SPLUNK_HOST` | Splunk hostname/IP (no protocol) | `127.0.0.1` | Yes |
| `SPLUNK_PORT` | Management API port | `8089` | Yes |
| `SPLUNK_USERNAME` | Authentication username | `admin` | Yes* |
| `SPLUNK_PASSWORD` | Authentication password | - | Yes* |
| `SPLUNK_TOKEN` | API token (alternative auth) | - | Yes* |
| `SPLUNK_VERIFY_SSL` | Enable SSL verification | `true` | No |
| `TRANSPORT` | MCP transport mode | `stdio` | No |
| `SPL_MAX_EVENTS_COUNT` | Max events per query | `100000` | No |
| `SPL_RISK_TOLERANCE` | Risk score threshold | `75` | No |
| `SPL_SANITIZE_OUTPUT` | Sanitize output | `false` | No |
| `HTTP_PROXY` | HTTP proxy URL | - | No |
| `HTTPS_PROXY` | HTTPS proxy URL | - | No |

*Either username/password or token required

## Usage

### Running the Server

#### With UV:
```bash
cd /path/to/splunk
uv run mcp-splunk
```

#### With Docker:
```bash
docker run --rm \
  -e SPLUNK_HOST=127.0.0.1 \
  -e SPLUNK_PORT=8089 \
  -e SPLUNK_USERNAME=admin \
  -e SPLUNK_PASSWORD=yourpassword \
  mcp-splunk:latest
```

#### With Docker Compose:
```bash
docker-compose up
```

### Example MCP Tool Usage

Once connected to an MCP client:

**List indexes:**
```
Get me the list of Splunk indexes
```

**Execute search:**
```
Search for errors in the last hour in the _internal index
```

**Validate query:**
```
Check if this SPL query is safe: index=* | stats count
```

**Get configuration:**
```
Show me the current Splunk MCP server configuration
```

## Docker Build

Build for production:
```bash
docker build -t mcp-splunk:0.1.0 .
```

Build with proxy (Bosch example):
```bash
docker build \
  --build-arg HTTP_PROXY=http://rb-proxy-de.bosch.com:8080 \
  --build-arg HTTPS_PROXY=http://rb-proxy-de.bosch.com:8080 \
  -t mcp-splunk:0.1.0 .
```

Tag and push to registry:
```bash
docker tag mcp-splunk:0.1.0 your-registry/mcp-splunk:0.1.0
docker push your-registry/mcp-splunk:0.1.0
```

## Troubleshooting

### Connection Issues
- **Error**: `Name or service not known`
  - **Fix**: Ensure `SPLUNK_HOST` contains only hostname/IP (no `https://`)

- **Error**: `Connection refused`
  - **Fix**: Verify Splunk is running and port 8089 is accessible

### Authentication Failures
- **Error**: `401 Unauthorized`
  - **Fix**: Verify credentials are correct and user has API access

- **Error**: `403 Forbidden`
  - **Fix**: Check user has necessary Splunk role permissions

### SSL/TLS Issues
- **Error**: `SSL certificate verify failed`
  - **Fix**: Set `SPLUNK_VERIFY_SSL=false` for self-signed certificates
  - **Production**: Mount CA certificates in Docker: `-v /etc/ssl/certs/ca-certificates.crt:/etc/ssl/certs/ca-certificates.crt:ro`

### Query Blocked
- **Error**: `Query would be BLOCKED - risk score too high`
  - **Fix**: Add time constraints or specific indexes to reduce risk score
  - **Alternative**: Adjust `SPL_RISK_TOLERANCE` environment variable

### Python Version
- **Error**: `Python 3.14 not supported`
  - **Fix**: Use `--python 3.11` flag or set `.python-version` to `3.11`

## Security Considerations

1. **Credentials**: Never hardcode credentials in configuration files
2. **SSL**: SSL verification enabled by default (`SPLUNK_VERIFY_SSL=true`)
3. **Risk Tolerance**: Set appropriate `SPL_RISK_TOLERANCE` for your environment
4. **Event Limits**: Configure `SPL_MAX_EVENTS_COUNT` to prevent resource exhaustion
5. **Network**: Use firewall rules to restrict Splunk API access
6. **Logging**: Review session logs in `logs/` directory regularly

## Development

```bash
cd src/splunk
uv sync
uv run mcp-splunk
```

For testing and contributing guidelines, see the [main repository README](../README.md).

For issues or questions:
- Create an issue in the project tracker
- Contact the maintainer team
- Review RELEASES.md for known issues

## Version

Current version: **0.1.0** (2026-02-04)

See [RELEASES.md](RELEASES.md) for full release history.
