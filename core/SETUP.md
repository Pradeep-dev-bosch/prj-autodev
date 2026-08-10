# Autodev Setup Guide

Complete step-by-step guide for setting up Autodev on a new machine.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Clone Repositories](#clone-repositories)
3. [Install Dependencies](#install-dependencies)
4. [Configure MCP Servers](#configure-mcp-servers)
5. [Generate Access Tokens](#generate-access-tokens)
6. [Test Installation](#test-installation)
7. [First Run](#first-run)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

| Component | Version | Purpose |
|-----------|---------|---------|
| **OS** | Linux (Ubuntu 20.04+) or macOS 12+ | Development environment |
| **Python** | ≥ 3.13 | MCP servers runtime |
| **uv** | Latest | Python package manager |
| **VS Code** | ≥ 1.99 | IDE with Copilot |
| **GitHub Copilot** | Latest | AI assistant |
| **Git** | ≥ 2.30 | Version control |
| **Gerrit** | Access credentials | Code review |
| **JIRA** | Access credentials | Issue tracking |
| **SharePoint** | Access credentials | Documentation |

**Optional (planned features):**
- Neo4j ≥ 5.x for knowledge graph
- Graphiti for graph embeddings

---

## Clone Repositories

### Main Workspace

```bash
# Clone to your preferred location
cd ~/projects
git clone <your-github-repo-url> Autodev
cd Autodev
```

### MCP Servers Repository

```bash
# Clone MCP servers (if separate repository)
git clone <pmt-mcp-servers-repo-url> pmt-mcp-servers-main
```

**Verify structure:**
```bash
tree -L 2
# Expected:
# .
# ├── .github/
# │   ├── agents/
# │   └── copilot-instructions.md
# ├── .vscode/
# │   └── mcp.json
# ├── Autodev/
# └── pmt-mcp-servers-main/
```

---

## Install Dependencies

### 1. Python 3.13

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install -y python3.13 python3.13-venv python3.13-dev
python3.13 --version
```

#### macOS (Homebrew)
```bash
brew install python@3.13
python3.13 --version
```

#### Alternative: pyenv
```bash
curl https://pyenv.run | bash
pyenv install 3.13.0
pyenv global 3.13.0
```

### 2. uv Package Manager

```bash
# Install
pip install uv

# Or via curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
which uv  # Note this path - you'll need it for mcp.json
```

### 3. VS Code

#### Download and Install
```bash
# Ubuntu/Debian
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# macOS
brew install --cask visual-studio-code
```

#### Install GitHub Copilot Extension
```bash
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
```

#### Enable Custom Agents

**Method 1: Settings UI**
1. Press `Ctrl+,` (or `Cmd+,` on macOS)
2. Search for "chat agent"
3. Enable "Chat: Agent Enabled"

**Method 2: settings.json**
```bash
# Linux
echo '{"chat.agent.enabled": true}' >> ~/.config/Code/User/settings.json

# macOS
echo '{"chat.agent.enabled": true}' >> ~/Library/Application\ Support/Code/User/settings.json
```

### 4. Install MCP Servers

```bash
cd Autodev/pmt-mcp-servers-main

# JIRA MCP
cd src/jira
uv sync  # Creates .venv and installs dependencies
cd ../..

# SharePoint MCP
cd src/sharepoint/sharepointonprem
uv sync
cd ../../..

# Gerrit MCP
cd src/gerrit
uv sync
cd ../..

# Verify installations
ls -la src/jira/.venv
ls -la src/sharepoint/sharepointonprem/.venv
ls -la src/gerrit/.venv
```

---

## Configure MCP Servers

### 1. Create mcp.json

```bash
cd Autodev
code .vscode/mcp.json
```

### 2. Configuration Template

Replace **ALL** placeholders with your actual values:

```json
{
  "servers": {
    "jira": {
      "type": "stdio",
      "command": "/home/YOUR_USERNAME/.local/bin/uv",
      "args": ["run", "jiramcpserver.py"],
      "cwd": "/absolute/path/to/Autodev/pmt-mcp-servers-main/src/jira",
      "env": {
        "TRACKER_URL": "${input:jira-url}",
        "JIRA_TOKEN": "${input:jira-token}"
      }
    },
    "sharepoint": {
      "type": "stdio",
      "command": "/home/YOUR_USERNAME/.local/bin/uv",
      "args": ["run", "sharepointonpremserver.py"],
      "cwd": "/absolute/path/to/Autodev/pmt-mcp-servers-main/src/sharepoint/sharepointonprem",
      "env": {
        "SHAREPOINT_URL": "https://sharepoint.yourcompany.com",
        "SHAREPOINT_USERNAME": "DOMAIN\\your-username",
        "SHAREPOINT_PASSWORD": "${input:sharepoint-password}"
      }
    },
    "gerrit": {
      "type": "stdio",
      "command": "/home/YOUR_USERNAME/.local/bin/uv",
      "args": ["run", "gerritmcpserver.py"],
      "cwd": "/absolute/path/to/Autodev/pmt-mcp-servers-main/src/gerrit",
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

### 3. Find Values

#### uv Path
```bash
which uv
# Example output: /home/username/.local/bin/uv
# Use this in "command" field
```

#### Absolute Paths
```bash
pwd
# Example: /home/username/projects/Autodev
# Use this to build "cwd" paths
```

#### SharePoint Username Format
- **Windows AD:** `DOMAIN\username`
- **Email-based:** `username@yourcompany.com`
- **Check with your IT team if unsure**

---

## Generate Access Tokens

### JIRA Personal Access Token

1. Log in to JIRA: `https://jira.yourcompany.com`
2. Go to **Profile** → **Personal Access Tokens**
3. Click **Create token**
4. Name: `Autodev MCP`
5. Expiry: **1 year**
6. Copy the token immediately (shown only once)
7. Store securely:
   ```bash
   # Save to password manager or encrypted file
   echo "JIRA_TOKEN=your-token-here" >> ~/.credentials/debugpilot.env
   chmod 600 ~/.credentials/debugpilot.env
   ```

### Gerrit HTTP Password

1. Log in to Gerrit: `https://gerrit.yourcompany.com`
2. Go to **Settings** → **HTTP Credentials**
3. Click **Generate New Password**
4. Copy the password
5. Store securely (same as JIRA token)

### SharePoint

Uses your standard AD/LDAP password (prompted at runtime via VS Code).

---

## Test Installation

### 1. Test Python Scripts

```bash
cd Autodev/Autodev

# Test attachment processor with sample data
python3 scripts/test_processor.py
```

**Expected output:**
```
======================================================================
Autodev Attachment Processor - Test Mode
======================================================================

Workspace: /path/to/workspace
Issue Key: TEST-123

Creating sample attachments...
  - 3 attachments prepared

Processing attachments...
----------------------------------------------------------------------
✓ Saved: logcat_main.txt
✓ Saved: logs.zip
✓ Saved: screenshot.png
✓ Extracted zip: 4 files from logs.zip
✓ Classified as logcat: logcat.txt
✓ Classified as tombstones: tombstone_01
✓ Classified as anr: traces.txt
✓ Classified as system: dmesg.log
----------------------------------------------------------------------

Processing Summary:
  Attachments saved: 3
  Files extracted:   7

Logs organized:
  logcat       : 2 file(s)
  tombstones   : 1 file(s)
  anr          : 1 file(s)
  system       : 1 file(s)
```

### 2. Verify Workspace Structure

```bash
ls -la workspace/TEST-123/logs/
# Should show: logcat/ tombstones/ anr/ system/

# Cleanup
rm -rf workspace/TEST-123/
```

### 3. Open VS Code

```bash
code Autodev
```

Wait for MCP servers to initialize (check VS Code status bar).

### 4. Check Custom Agents

1. Open Copilot Chat (`Ctrl+Alt+I`)
2. Click the agent picker (top of chat)
3. Verify **Autodev** appears in the list

**If not visible:**
```bash
# Check settings
cat ~/.config/Code/User/settings.json | grep agent

# Reload VS Code
Ctrl+Shift+P → "Developer: Reload Window"
```

---

## First Run

### 1. Select Autodev Agent

In Copilot Chat:
1. Click agent picker
2. Select **Autodev**
3. You'll be prompted: "Enter the JIRA issue key (e.g., PROJ-1234)"

### 2. Enter JIRA Issue

Type a real JIRA issue key from your project:
```
PROJ-1234
```

### 3. Provide Credentials

VS Code will prompt for:
- JIRA URL (uses default from mcp.json)
- JIRA token
- SharePoint password
- Gerrit password

**Credentials are NOT stored** — prompted every VS Code session.

### 4. Follow the Workflow

Autodev will:

1. **Fetch JIRA ticket**
   - Downloads issue details
   - Retrieves all attachments

2. **Process attachments**
   - Extracts zip/tar files
   - Organizes logs (logcat, tombstones, ANR, system)
   - Reports summary

3. **Query SharePoint**
   - Searches for component docs (API specs, SDD, HMI)
   - Retrieves top 2-3 relevant documents

4. **Root Cause Analysis**
   - Analyzes logs + docs
   - Produces structured RCA report
   - **⛔ APPROVAL GATE:** Shows RCA, asks for approval
   - Options: `yes` / `no` / `edit`

5. **Post RCA to JIRA** (after approval)
   - Adds RCA as comment
   - Transitions ticket to "In Analysis"

6. **Generate Fix Plan**
   - Produces detailed fix with code changes
   - Shows component impact summary
   - **⛔ APPROVAL GATE:** Shows fix plan, asks for approval
   - Options: `yes` / `no` / `edit`

7. **Apply Fix** (after approval)
   - Modifies workspace files
   - Reports changes made

8. **Push to Gerrit**
   - **⛔ APPROVAL GATE:** Shows push summary, asks for approval
   - Options: `yes` / `no` / `edit`
   - Pushes change for review
   - Reports Gerrit change URL

9. **Close JIRA**
   - Posts closure comment with Gerrit link
   - Transitions ticket to "In Review"

---

## Troubleshooting

### Agents Not Visible

**Symptom:** Autodev doesn't appear in agent picker

**Solutions:**
```bash
# 1. Check chat.agent.enabled setting
cat ~/.config/Code/User/settings.json | grep agent
# Should show: "chat.agent.enabled": true

# 2. Verify agent files exist
ls -la .github/agents/*.agent.md
# Should show: Autodev.agent.md, BugAnalyst.agent.md, etc.

# 3. Check YAML frontmatter
head -15 .github/agents/Autodev.agent.md
# Should start with: ---
# name: Autodev
# ...

# 4. Reload VS Code
# Ctrl+Shift+P → "Developer: Reload Window"
```

### MCP Server Fails to Start

**Symptom:** Error in VS Code output: "Failed to start MCP server"

**Solutions:**
```bash
# 1. Check uv path
which uv
# Update "command" in mcp.json if different

# 2. Check absolute paths in mcp.json
pwd  # Note current directory
# Update "cwd" fields with absolute paths

# 3. Verify uv can run the server manually
cd pmt-mcp-servers-main/src/jira
uv run jiramcpserver.py
# Should not error

# 4. Check VS Code Output panel
# View → Output → Select "MCP" from dropdown
# Look for specific error messages
```

### JIRA Authentication Fails

**Symptom:** "401 Unauthorized" or "Invalid token"

**Solutions:**
```bash
# 1. Verify token is correct
curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://jira.yourcompany.com/rest/api/2/myself
# Should return your user details

# 2. Check token hasn't expired
# Regenerate if needed (see "Generate Access Tokens" section)

# 3. Verify TRACKER_URL is correct
# Should NOT have trailing slash
# Correct: https://jira.yourcompany.com
# Wrong:   https://jira.yourcompany.com/
```

### SharePoint Connection Issues

**Symptom:** "Cannot connect to SharePoint" or "401 Unauthorized"

**Solutions:**
```bash
# 1. Verify SharePoint URL
# Should be the site collection root
# Example: https://sharepoint.company.com/sites/engineering

# 2. Check username format
# Try both: DOMAIN\username and username@company.com

# 3. Test credentials manually
# Use SharePoint web interface to verify password

# 4. Check network access
ping sharepoint.yourcompany.com
```

### Gerrit Push Fails

**Symptom:** "Error pushing to Gerrit" or "HTTP 403"

**Solutions:**
```bash
# 1. Verify HTTP password
# Gerrit Settings → HTTP Credentials → Generate New Password

# 2. Check Gerrit URL format
# Should include protocol and port if non-standard
# Example: https://gerrit.company.com:8080

# 3. Verify git remote
cd your-aosp-repo
git remote -v
# Should show gerrit URL

# 4. Test manual push
git push origin HEAD:refs/for/main
```

### Attachment Processor Fails

**Symptom:** "Failed to extract archive" or "Classification error"

**Solutions:**
```bash
# 1. Check Python version
python3 --version
# Should be ≥ 3.7

# 2. Test manually
cd Autodev
python3 scripts/test_processor.py
# Should complete without errors

# 3. Check file permissions
ls -la workspace/
chmod 755 workspace/

# 4. Verify zip/tar tools available
which unzip
which tar
```

### Performance Issues

**Symptom:** MCP servers slow to respond

**Solutions:**
```bash
# 1. Check network latency to JIRA/SharePoint/Gerrit
ping jira.yourcompany.com
traceroute sharepoint.yourcompany.com

# 2. Monitor MCP server logs
# VS Code → Output → MCP

# 3. Restart MCP servers
# Ctrl+Shift+P → "Developer: Reload Window"

# 4. Check system resources
htop  # CPU/memory usage
```

---

## Additional Resources

- [Autodev README](README.md) - Overview and quick start
- [Processor Documentation](scripts/README.md) - Attachment processor details
- [Quick Reference](QUICK_REFERENCE.md) - Commands and log patterns
- [Architecture](../architecture.md) - System design

---

## Getting Help

1. **Check logs:** VS Code Output panel → Select "MCP"
2. **Run diagnostics:** `python3 scripts/test_processor.py`
3. **Verify config:** Review `.vscode/mcp.json` for typos
4. **Contact team:** Provide error messages and logs
