# Autodev

> **An AI-powered bug analysis and fix workflow for VS Code.**  
> JIRA → Root Cause Analysis (with SharePoint docs) → Fix → Gerrit → Knowledge Graph

---

## What it does

Autodev is a VS Code Copilot agent mode workflow that automates the full cycle
from receiving a bug ticket to pushing a reviewed fix and recording institutional memory:

```
JIRA ticket
    │
    ▼
Fetch issue details (JIRA MCP)
    │
    ├──► Retrieve relevant SW design docs, API specs,
    │    component info from SharePoint (SharePoint MCP)
    │
    ├──► Query similar past bugs (Knowledge Graph MCP)
    │
    ▼
Root Cause Analysis (AI synthesis)
    │
    ▼
Post RCA as JIRA comment (JIRA MCP)
    │
    ▼
Fix Plan → USER APPROVAL GATE
    │
    ▼  (approved)
Apply code changes in workspace
    │
    ▼
Push to Gerrit for review (Gerrit MCP)
    │
    ▼
Store analysis + fix + Gerrit link in Knowledge Graph (KG MCP)
    │
    ▼
Post confirmation comment to JIRA
```

---

## Key Features

### 🔍 Automated Log Processing

Autodev automatically downloads and processes JIRA attachments:

- **Download** all attachments via JIRA MCP
- **Extract** compressed archives (zip, tar, gz, tgz, bz2)
- **Classify** logs by type (logcat, tombstones, ANR traces, system logs)
- **Organize** into categorized directories for efficient analysis

**Android IVI Log Categories:**

| Type | What It Contains |
|------|------------------|
| **logcat** | Android system logs, app logs, crash logs |
| **tombstones** | Native crash dumps (SIGSEGV, SIGABRT) |
| **anr** | ANR traces (main thread blocked) |
| **system** | Kernel logs, bugreport, dumpsys output |

The BugAnalyst agent automatically reads priority logs in order (ANR → tombstones → logcat → system) and includes relevant excerpts as evidence in the Root Cause Analysis.

See [scripts/README.md](scripts/README.md) for technical details.

---

## Project Structure

```
Autodev/
├── .github/
│   └── copilot-instructions.md     ← Agent workflow definition (this drives Copilot)
├── .vscode/
│   └── mcp.json                    ← VS Code MCP server configuration
├── scripts/
│   ├── process_jira_attachments.py ← Attachment processor (extract & organize logs)
│   └── README.md                   ← Processor documentation
├── workspace/                      ← Working directory for processed logs
│   └── <ISSUE_KEY>/
│       ├── attachments/            ← Raw JIRA attachments
│       ├── extracted/              ← Extracted archive contents
│       └── logs/                   ← Organized by type
│           ├── logcat/
│           ├── tombstones/
│           ├── anr/
│           └── system/
└── docs/
    ├── component-info-template.md  ← Template for component documentation
    └── kg-schema.ttl               ← RDF ontology for the knowledge graph

architecture.md (moved to root)     ← Detailed system architecture & data flow
```

Uses existing MCP servers from `pmt-mcp-servers-main`:
- `src/jira/jiramcpserver.py` — JIRA integration
- `src/sharepoint/sharepointonprem/sharepointonpremserver.py` — SharePoint integration

---

## Initial Setup (From GitHub)

> **📖 Detailed setup guide:** See [SETUP.md](SETUP.md) for comprehensive step-by-step instructions, troubleshooting, and configuration examples.
>
> **✅ Setup checklist:** See [../SETUP_CHECKLIST.md](../SETUP_CHECKLIST.md) for a quick verification checklist.

**Quick overview for first-time setup:**

### Step 1: Clone the Repository

```bash
# Clone the main workspace repository
git clone <your-github-repo-url> Autodev
cd Autodev

# Clone the MCP servers repository (if separate)
git clone <pmt-mcp-servers-repo-url> pmt-mcp-servers-main
```

**Expected structure after cloning:**
```
Autodev/
├── .github/
│   ├── agents/           # Autodev custom agents
│   └── copilot-instructions.md
├── .vscode/
│   └── mcp.json          # MCP server configuration template
├── Autodev/
└── pmt-mcp-servers-main/ # MCP servers (JIRA, SharePoint, Gerrit, KG)
```

### Step 2: Install Prerequisites

#### Python ≥ 3.13
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3.13 python3.13-venv

# macOS (Homebrew)
brew install python@3.13

# Verify
python3 --version
```

#### uv Package Manager
```bash
pip install uv

# Verify
uv --version
```

#### VS Code with GitHub Copilot
1. Download VS Code: https://code.visualstudio.com/
2. Install GitHub Copilot extension
3. Sign in with your GitHub account

#### Enable Custom Agents in VS Code

Add to VS Code user settings (`~/.config/Code/User/settings.json`):
```json
{
  "chat.agent.enabled": true
}
```

Or via VS Code UI:
1. Press `Ctrl+,` (Settings)
2. Search for "chat agent"
3. Enable "Chat: Agent Enabled"

### Step 3: Install MCP Server Dependencies

```bash
cd Autodev/pmt-mcp-servers-main

# Install JIRA MCP server
cd src/jira
uv sync
cd ../..

# Install SharePoint MCP server
cd src/sharepoint/sharepointonprem
uv sync
cd ../../..

# Install Gerrit MCP server
cd src/gerrit
uv sync
cd ../..

# (Optional) Install Knowledge Graph MCP server - planned feature
# cd src/knowledge_graph
# uv sync
# cd ../..
```

### Step 4: Install Autodev Python Dependencies

Autodev requires Python packages for document conversion (ComponentSetup wizard):

```bash
cd Autodev  # Navigate to Autodev root

# Quick install
./setup.sh

# Or manual install
pip3 install --user -r requirements.txt
```

**Installed packages:**
- `python-docx` — DOCX to Markdown conversion for ComponentSetup uploads

**Optional system packages (for PDF support):**
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

**Verify installation:**
```bash
python3 -c "import docx; print('✓ python-docx installed')"
```

### Step 5: Configure MCP Servers

Copy the MCP configuration template:

```bash
cd Autodev
cp .vscode/mcp.json.example .vscode/mcp.json  # If you have a template
```

Or create `.vscode/mcp.json` from scratch:

```json
{
  "servers": {
    "jira": {
      "type": "stdio",
      "command": "/home/<username>/.local/bin/uv",
      "args": ["run", "jiramcpserver.py"],
      "cwd": "/absolute/path/to/pmt-mcp-servers-main/src/jira",
      "env": {
        "TRACKER_URL": "${input:jira-url}",
        "JIRA_TOKEN": "${input:jira-token}"
      }
    },
    "sharepoint": {
      "type": "stdio",
      "command": "/home/<username>/.local/bin/uv",
      "args": ["run", "sharepointonpremserver.py"],
      "cwd": "/absolute/path/to/pmt-mcp-servers-main/src/sharepoint/sharepointonprem",
      "env": {
        "SHAREPOINT_URL": "https://sharepoint.yourcompany.com",
        "SHAREPOINT_USERNAME": "DOMAIN\\username",
        "SHAREPOINT_PASSWORD": "${input:sharepoint-password}"
      }
    },
    "gerrit": {
      "type": "stdio",
      "command": "/home/<username>/.local/bin/uv",
      "args": ["run", "gerritmcpserver.py"],
      "cwd": "/absolute/path/to/pmt-mcp-servers-main/src/gerrit",
      "env": {
        "GERRIT_URL": "https://gerrit.yourcompany.com",
        "GERRIT_USERNAME": "your-username",
        "GERRIT_HTTP_PASSWORD": "${input:gerrit-password}"
      }
    }
  },
  "inputs": [
    {
      "id": "jira-url",
      "type": "promptString",
      "description": "Enter your JIRA base URL",
      "default": "https://jira.yourcompany.com"
    },
    {
      "id": "jira-token",
      "type": "promptString",
      "description": "Enter your JIRA personal access token",
      "password": true
    },
    {
      "id": "sharepoint-password",
      "type": "promptString",
      "description": "Enter your SharePoint password",
      "password": true
    },
    {
      "id": "gerrit-password",
      "type": "promptString",
      "description": "Enter your Gerrit HTTP password",
      "password": true
    }
  ]
}
```

**Important:** Replace all placeholders:
- `<username>` → Your actual username
- `/absolute/path/to/` → Actual absolute paths
- `yourcompany.com` → Your organization's domain
- `DOMAIN\\username` → Your SharePoint domain/username

**Finding `uv` path:**
```bash
which uv
# Use this path in "command" field
```

### Step 6: Generate Access Tokens

#### JIRA Personal Access Token
1. Go to `https://jira.yourcompany.com/secure/ViewProfile.jspa`
2. Click "Personal Access Tokens"
3. Create token → Copy and store securely

#### Gerrit HTTP Password
1. Go to `https://gerrit.yourcompany.com/settings/#HTTPCredentials`
2. Generate/View HTTP Password → Copy

#### SharePoint
Uses your AD/LDAP password (prompted at runtime).

### Step 7: Test the Setup

```bash
cd Autodev/Autodev

# Test the attachment processor
python3 scripts/test_processor.py

# Expected output:
# ✓ Saved: logcat_main.txt
# ✓ Extracted zip: 4 files from logs.zip
# ✓ Classified as logcat: logcat.txt
# ...
```

### Step 7: Open in VS Code

```bash
# Open the workspace
code Autodev
```

VS Code will:
1. Detect `.vscode/mcp.json`
2. Start MCP servers automatically
3. Load custom agents from `.github/agents/`

### Step 8: Verify Agents are Loaded

1. Open Copilot Chat (`Ctrl+Alt+I`)
2. Look for the agent picker dropdown
3. You should see:
   - **Autodev** (orchestrator)
   - BugAnalyst (hidden - invoked by Autodev)
   - FixGenerator (hidden - invoked by Autodev)
   - KGUpdater (hidden - planned feature)

If agents don't appear:
```bash
# Reload VS Code
Ctrl+Shift+P → "Developer: Reload Window"

# Verify settings
cat ~/.config/Code/User/settings.json | grep agent
# Should show: "chat.agent.enabled": true
```

### Step 9: First Run

1. In Copilot Chat, select **Autodev** from the agent picker
2. Enter a JIRA issue key when prompted (e.g., `PROJ-1234`)
3. Follow the workflow:
   - BugAnalyst fetches ticket + attachments
   - Extracts and organizes logs
   - Retrieves SharePoint docs
   - Produces Root Cause Analysis
   - **Waits for your approval** ⛔
   - FixGenerator creates fix plan
   - **Waits for your approval** ⛔
   - Applies code changes
   - Pushes to Gerrit
   - Posts closure comment to JIRA

---

## Quick Start (After Initial Setup)

### Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python ≥ 3.13 | For MCP servers |
| [uv](https://github.com/astral-sh/uv) | Package runner (`pip install uv`) |
| VS Code ≥ 1.99 | With GitHub Copilot extension |
| Neo4j ≥ 5.x + Graphiti | For knowledge graph *(planned feature)* |
| git | With Gerrit remote configured |

### 1 — Configure `.vscode/mcp.json`

Edit [`.vscode/mcp.json`](.vscode/mcp.json) and replace all `<PLACEHOLDER>` values:

```json
"cwd": "/absolute/path/to/pmt-mcp-servers-main/src/gerrit"
"GERRIT_URL": "https://gerrit.yourcompany.com"
"JIRA": "https://jira.yourcompany.com"
// ... etc
```

All passwords are prompted securely at runtime via `${input:...}` — never stored.

### 2 — Install dependencies for new MCP servers

```bash
# Gerrit MCP server
cd pmt-mcp-servers-main/src/gerrit
uv sync

# Knowledge Graph MCP server
cd ../knowledge_graph
uv sync
```

### 3 — Create the Neo4j database (one-time) *(planned feature)*

```bash
# TODO: spin up Neo4j + Graphiti instance
# then update NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD in mcp.json
```

### 4 — Test attachment processor (optional)

```bash
cd Autodev

# Test with sample data
python3 scripts/test_processor.py

# View results
ls -la workspace/TEST-123/logs/

# Cleanup
rm -rf workspace/TEST-123/
```

### 5 — Open Autodev folder in VS Code

```bash
code /path/to/Autodev
```

VS Code will automatically detect `.vscode/mcp.json` and start the configured
MCP servers when you open Copilot Chat in **Agent Mode**.

### 6 — Run a debug session

In Copilot Chat (`Ctrl+Alt+I`), select **Agent Mode**, then type:

```
Analyse PROJ-123
```

Copilot will follow the workflow automatically:
1. Fetch JIRA issue and download attachments
2. Extract and organize logs (logcat, tombstones, ANR, system)
3. Retrieve SharePoint documentation
4. Perform root cause analysis using logs + docs
5. Update JIRA with findings
6. Produce a fix plan
7. **Ask for your approval** ← you respond yes/no
8. Apply the code fix
9. Push to Gerrit
10. Store everything in the knowledge graph

---

## MCP Servers

### New Servers (in this project)

| Server | Location | Purpose |
|--------|----------|---------|
| Gerrit MCP | `src/gerrit/` | Push code, query changes via Gerrit REST API |
| Bug KG MCP | `pmt-mcp-servers-main/src/knowledge_graph/` | Store/query bug history in Graphiti + Neo4j graph *(planned)* |

### Reused Servers (from `pmt-mcp-servers-main`)

| Server | Location | Purpose |
|--------|----------|---------|
| JIRA MCP | `../pmt-mcp-servers-main/src/jira/` | Fetch issues, post comments, transitions |
| SharePoint MCP | `../pmt-mcp-servers-main/src/sharepoint/sharepointonprem/` | Search & read SW documentation |

---

## Knowledge Graph

The knowledge graph builds **institutional memory** over time.
Every bug analysis is stored with:

- JIRA issue key + summary
- Root cause text
- Software component name
- Affected file paths
- Fix description
- Fix lifecycle status (`open` → `proposed` → `merged`)
- Gerrit change ID

When debugging future issues in the **same component**, the agent automatically
queries for similar past bugs — enabling faster diagnosis and reuse of proven fixes.

See [`docs/kg-schema.ttl`](docs/kg-schema.ttl) for the full RDF ontology.

---

## Configuration Reference

### Environment Variables

| Variable | Server | Description |
|----------|--------|-------------|
| `JIRA_TOKEN` | JIRA | Personal access token |
| `TRACKER_URL` | JIRA | JIRA base URL |
| `SHAREPOINT_URL` | SharePoint | SharePoint site URL |
| `SHAREPOINT_USERNAME` | SharePoint | Domain username (DOMAIN\user) |
| `SHAREPOINT_PASSWORD` | SharePoint | Domain password |
| `GERRIT_URL` | Gerrit | Gerrit base URL |
| `GERRIT_USERNAME` | Gerrit | Gerrit HTTP username |
| `GERRIT_HTTP_PASSWORD` | Gerrit | HTTP password from Gerrit Settings |
| `NEO4J_URI`      | KG | Neo4j bolt/http URI (e.g. `bolt://localhost:7687`) |
| `NEO4J_USERNAME` | KG | Neo4j username |
| `NEO4J_PASSWORD` | KG | Neo4j password |
| `NEO4J_DATABASE` | KG | Database name (default: `bug_knowledge_graph`) |

---

## Security

- No credentials are ever stored in files — all secrets use `${input:...}` prompts
- The agent will **not apply fixes or push to Gerrit without explicit user approval**
- JIRA, SharePoint, Gerrit, and Neo4j connections all use their native auth mechanisms
- The knowledge graph stores only text analysis data — no source code, no credentials

---

## Architecture

See [`architecture.md`](../architecture.md) for the full system diagram and data flow.
