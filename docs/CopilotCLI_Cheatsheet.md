## Essential GitHub Copilot CLI Commands

Start Copilot CLI from your project directory:

```bash
copilot
```

### Most Used Commands

| Command    | Purpose                                              |
| ---------- | ---------------------------------------------------- |
| `/help`    | Display available commands and help                  |
| `/login`   | Sign in to GitHub                                    |
| `/logout`  | Sign out of GitHub                                   |
| `/agent`   | View and switch between available custom agents      |
| `/model`   | View or change the AI model                          |
| `/mcp`     | View and manage configured MCP servers               |
| `/tools`   | View tools available to the current session          |
| `/clear`   | Clear the current conversation                       |
| `/compact` | Compact conversation history to reduce context usage |
| `/context` | View information about the current context           |
| `/usage`   | View session usage information                       |
| `/exit`    | Exit Copilot CLI                                     |

### Starting with a Custom Agent

Start Copilot CLI:

```bash
copilot
```
Prefer using as we would need tools to be available in the session.
```bash 
copilot --allow-all
```


Then select an available agent:

```text
/agent
```

### Checking MCP Servers

View configured MCP servers and their status:

```text
/mcp
```

If an MCP server is correctly configured and running, its tools become available to Copilot.

View the available tools:

```text
/tools
```

### Allowing Tools

Copilot may ask for confirmation before executing tools or commands. To start Copilot with all tools allowed:

```bash
copilot --allow-all
```

> Use `--allow-all` only in a trusted project and environment, as it allows Copilot to execute tools without requesting confirmation.

### Exit Copilot

```text
/exit
```

You can also use:

```text
Ctrl+C
```

## Saving and Resuming Copilot CLI Sessions

GitHub Copilot CLI automatically saves your session history and context. Previous sessions can be resumed later.

### Resume the Most Recent Session

```bash
copilot --continue
```

Resumes the most recent session for the current project.

### Choose a Previous Session

```bash
copilot --resume
```

Opens a list of recent sessions and lets you select one to resume.

### Resume a Specific Session

```bash
copilot --resume <SESSION-ID>
```

Resumes a specific session using its session ID.

### Resume While Inside Copilot CLI

```text
/resume
```

Opens the recent session picker without exiting Copilot CLI.

### View Current Session ID

```text
/session
```

Displays information about the current session, including its session ID.

### Rename a Session

Give important sessions meaningful names so they are easier to find later:

```text
/rename Bug Resolution - JIRA 1234
```

### Managing Long Context

For long-running sessions, Copilot automatically manages the available context. You can also manually compact the conversation:

```text
/compact
```

This summarizes older conversation context while keeping the session active.


> **Note:** For more information on these refer [Official GitHub Copilot CLI Docs](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference#slash-commands-in-the-interactive-interface).