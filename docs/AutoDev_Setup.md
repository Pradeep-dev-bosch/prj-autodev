## Prerequisites

* **Git**
* **Python 3.13 or above**
* **uv** — Python package and virtual environment manager
* **Node.js 22 or above**
* **npm**
* **dotenv-cli** — npm package
* **GitHub Copilot CLI**
* **GitHub Copilot subscription and authentication**
* **VS Code 1.99 or above** — required only when using the VS Code setup
* **JIRA Personal Access Token (PAT)**
* **SharePoint domain username and password**
* **Gerrit HTTP credentials**
* **poppler-utils** — required only for PDF extraction
* **python-docx 1.0.0 or above**

## Installing Prerequisites

### Git

**Windows**

```powershell
winget install --id Git.Git -e --source winget
```

**Linux (Ubuntu/Debian)**

```bash
sudo apt update && sudo apt install -y git
```

---

### uv

**Windows**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

### npm

**Windows**

```powershell
winget install OpenJS.NodeJS.LTS
```

**Linux (Ubuntu/Debian)**

```bash
sudo apt update && sudo apt install -y npm
```

> Ensure `node --version` is **22 or above** when using GitHub Copilot CLI.

---

### dotenv-cli

Requires npm to be installed.

**Windows**

```powershell
npm install -g dotenv-cli
```

**Linux**

```bash
npm install -g dotenv-cli
```

---

### Verify Installation

**Windows / Linux**

```bash
git --version
uv --version
node --version
npm --version
dotenv --version
```
## Setting Up the MCP Servers

1. Copy `.mcp.json.example` to `.mcp.json` in the **project root**:

   ```bash
   cp .mcp.json.example .mcp.json
   ```

2. Open `.mcp.json` and replace the placeholders with the **absolute paths** to:

   * The `.env` file
   * JIRA MCP server
   * Gerrit MCP server
   * Other configured MCP servers

3. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

4. Add your **JIRA credentials** to `.env`:

   * JIRA Tracker URL
   * Personal Access Token (PAT)

5. Add your **Gerrit credentials** to `.env`:

   * Gerrit URL
   * Username
   * Generated HTTP password

6. **SharePoint MCP is currently unavailable.**

> **Important:** The MCP configuration file must be named exactly `.mcp.json`. Do not rename it to `mcp.json`, as GitHub Copilot CLI will not detect it.
### Installing MCP Server Dependencies

Navigate to the `pmt-mcp-servers-main` directory:

**Windows (PowerShell)**

```powershell
cd pmt-mcp-servers-main
```

**Linux**

```bash
cd pmt-mcp-servers-main
```

Install the Python dependencies for each MCP server using `uv sync`. This creates a local `.venv` for each server.

### JIRA

```bash
cd src/jira
uv sync
```

### Gerrit

From `pmt-mcp-servers-main`:

```bash
cd src/gerrit
uv sync
```

### SharePoint

> **Note:** SharePoint MCP is currently unavailable.

```bash
cd src/sharepoint/sharepointonprem
uv sync
```

### Optional Root-Level Dependencies

From the project root, install the optional dependencies used by the ComponentSetup document-conversion wizard:

```bash
pip install -r requirements.txt
```

