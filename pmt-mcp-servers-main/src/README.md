## Access to PMT Artifactory Repository

Use [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home) to get the role 'IdM2BCD_pmt_mcp_servers' which gives you read access on the BDC Artifactory repository containing all [PMT MCP servers (docker)](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) and [PMT MCP servers (python)](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-pypi-local)
Use the "Set Me Up" button in the Artifactory repository to generate a Token and follow the instructions.

### Docker Installation

Docker is typically included in the WSL setup. If Docker is not found in your WSL environment, follow the [Docker for Linux installation guide](https://inside-docupedia.bosch.com/confluence/spaces/DEVCORNER/pages/1595519415/Docker+for+Linux).


### Docker Login for Artifactory

Once you have access, execute the following command to log in to Artifactory:

```bash
docker login artifactory.boschdevcloud.com
```

### Docker Platform Compatibility

To ensure the containers remain compatible with ARM-based systems (e.g., Apple Silicon Macs), we have added the required platform flag while running them. This handles the platform compatibility:

```json
"args": [
  "run",
  "-i",
  "--rm",
  "--platform",
  "linux/amd64",
  ...
]
```

This flag is included in all `mcp.json` docker configurations to ensure consistent behavior across different architectures.

## Running MCP Servers for Development

### Python with uv

For local development or if you prefer not to use Docker:

1. **Install uv**: Check out the documentation for [installing uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)

2. **Navigate to the MCP server directory**:
   ```bash
   cd src/<mcp-server>  # use the specific MCP server you want to run
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

4. **Configure MCP client (example)** - Add to your `.vscode/mcp.json`:
   ```json
   {
     "servers": {
       "docupedia-python-mcp-server": {
         "command": "uv",
         "args": [
           "--directory",
           "/path/to/repo/pmt-mcp-servers/src/docupedia",
           "run",
           "docupediamcpserver.py"
         ],
         "env": {
            "CONFLUENCE_BASE_URL": "${input:docupedia-url}",
            "CONFLUENCE_PAT_TOKEN": "${input:docupedia-key}",
            "HTTP_PROXY": "http://rb-proxy-de.bosch.com:8080",
            "HTTPS_PROXY": "http://rb-proxy-de.bosch.com:8080"
         }
       }
     }
   }
   ```

## Handling Secrets and Credentials

### Secure Secret Input with promptString

![Credentials Input](../img/credentials-prompt.png)

**How it works:**
- When you start the MCP server, VSCode will prompt you to enter the token
- The token is stored securely in your system's credential manager

In case you have to re-enter the password/token

![Re-enter Credentials Input](../img/re-enter-credentials.png)

### Alternate Approach: Centralized Token Management with Environment Variables

If you are working across multiple repositories and want to avoid entering tokens in `mcp.json` for every repository, you can use a centralized approach by storing your credentials in a `.token` file, sourcing it in your `.bashrc`, and replacing the `${input:...}` variable with `${env:...}` in your `mcp.json`. This way, the tokens are part of your shell environment and automatically available across all repositories.

#### 1. Create a `.token` file

Create a `.token` file (e.g., in your home directory) with all the tokens you need:

```bash
# ~/.token
export JIRA_TOKEN=your-jira-token
export BITBUCKET_TOKEN=your-bitbucket-token
export GITHUB_PERSONAL_ACCESS_TOKEN=your-github-token
export ARTIFACTORY_PAT_TOKEN=your-artifactory-token
# Add more tokens as needed
```

> ⚠️ **Security:** Never commit this file to version control. Add `.token` to your `.gitignore`.

#### 2. Source it in your `.bashrc`

Add the following to your `~/.bashrc` so the tokens are loaded automatically in every shell session:

```bash
# ~/.bashrc
if [ -f ~/.token ]; then
    source ~/.token
fi
```

#### 3. Replace `${input:...}` with `${env:...}` in `mcp.json`

In your `.vscode/mcp.json`, replace the `promptString`-based input references with environment variable references:

```json
// Before: prompts for token every session
"env": {
   "JIRA_TOKEN": "${input:jira-token}"
}

// After: reads token from environment variable
"env": {
   "JIRA_TOKEN": "${env:JIRA_TOKEN}"
}
```

You can also remove the corresponding entry from the `"inputs"` array since it is no longer needed for that variable.

#### 4. Using with Devcontainers

This approach also works with devcontainers. Ensure your `.bashrc` (or the `.token` file) is mounted and sourced inside the devcontainer so that the environment variables are available. You can verify by running `echo $JIRA_TOKEN` in the devcontainer terminal — if it prints the token value, `${env:JIRA_TOKEN}` in `mcp.json` will resolve correctly.

> **Note:** VS Code must be launched from a terminal where `.bashrc` has been sourced (e.g., via `code .`) for `${env:...}` to resolve. Launching VS Code from a desktop shortcut may not inherit the shell environment.

## Starting the MCP Server

After adding the required configuration to your `.vscode/mcp.json`:

1. Click the **Start** button in the MCP server status bar

![MCP Start Button](../img/mcp-server-start.png)

The MCP server will start and connect to your VSCode GitHub Copilot.

## Viewing MCP Server Logs

To validate whether the MCP server is running and debug any issues:

1. After starting the server, click **"Show Output"** in the MCP server panel

![MCP Server Output](../img/mcp-server-output.png)

**What to look for in logs:**
- Server initialization messages
- Tool registration confirmations
- Connection status
- Authentication errors
- Network/proxy issues
- Configuration problems

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Framework](https://github.com/jlowin/fastmcp)
- [uv Package Manager](https://docs.astral.sh/uv/)
- [Install Docker @ BOSCH](https://inside-docupedia.bosch.com/confluence/x/V5nDXQ)
