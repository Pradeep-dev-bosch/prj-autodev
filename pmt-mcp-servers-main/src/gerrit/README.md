# Gerrit MCP Server

MCP server for interacting with [Gerrit Code Review](https://www.gerritcodereview.com/) via its REST API.

## Available Tools

| Tool | Description |
|------|-------------|
| `list_gerrit_changes` | Search changes using Gerrit query syntax |
| `get_gerrit_change` | Get full details of a specific change |
| `create_gerrit_change` | Create an empty new change |
| `set_gerrit_review` | Post review message and vote labels |
| `abandon_gerrit_change` | Abandon an open change |
| `get_gerrit_change_files` | List files modified in a change revision |
| `get_gerrit_file_content` | Read content of a file in a change |
| `push_to_gerrit` | `git push` local commits to `refs/for/<branch>` |
| `list_gerrit_projects` | List available Gerrit projects |
| `get_gerrit_project` | Get info about a specific project |
| `get_gerrit_change_messages` | Get review discussion thread |

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `GERRIT_URL` | Base URL (e.g. `https://gerrit.example.com`) |
| `GERRIT_USERNAME` | Gerrit HTTP username |
| `GERRIT_HTTP_PASSWORD` | HTTP password from **Account Settings → HTTP Credentials** |
| `TRANSPORT` | Transport type: `stdio` (default) or `sse` |
| `HOST` | Host when using SSE transport (default: `127.0.0.1`) |
| `HOST_PORT` | Port when using SSE transport (default: `8001`) |

### Running with uv (stdio)

```bash
cd pmt-mcp-servers-main/src/gerrit
uv run gerritmcpserver.py
```

### Running with Docker

```bash
docker build -t gerrit-mcp-server .
docker run -i --rm \
  -e GERRIT_URL=https://gerrit.example.com \
  -e GERRIT_USERNAME=myuser \
  -e GERRIT_HTTP_PASSWORD=mypassword \
  gerrit-mcp-server
```

## Notes

- Authentication uses HTTP Basic Auth with your Gerrit HTTP password (not your SSO password).
- Generate the HTTP password in Gerrit UI under **Settings → HTTP Credentials → Generate Password**.
- The `push_to_gerrit` tool requires `git` to be available in `PATH` and the repository configured with the Gerrit remote.
