 copilot --resume=1cc5ed59-904d-488c-8988-7fee657ec9bd
# Project User Guide

## 1. Overview

**Autodev** is a GitHub Copilot agent workflow for Android IVI (In-Vehicle Infotainment) teams building on AOSP / Android Automotive OS (AAOS). It automates the bug-resolution lifecycle: a developer supplies a JIRA issue key, and a pipeline of custom Copilot agents validates the ticket, performs root-cause analysis using local component documentation and workspace source code, proposes and (after human approval) applies a code fix, and pushes it to Gerrit for review.

High-level flow (evidence: `README.md`, `architecture.md`, `.github/copilot-instructions.md`):

```
JIRA issue key
   → InternalQualityCheckerAgent (validates ticket completeness)
   → BugAnalyst (root cause analysis, reads local docs + workspace source)
   → FixGenerator (fix plan → approval gate → code changes → Gerrit push)
   → KGUpdater (knowledge-graph persistence — planned feature, currently disabled)
```

Two mandatory human approval gates exist in the pipeline: approving the Root Cause Analysis before it is posted to JIRA, and approving the fix plan before code is changed and pushed to Gerrit (`.github/copilot-instructions.md`, Step 3a and Step 6).

A companion agent, **ComponentSetup**, is used once per software component to pre-fetch design documents (from SharePoint) and analyze workspace source code, writing the results into `core/docs/components/<slug>/` so that BugAnalyst/FixGenerator never need to query SharePoint directly (`.github/agents/ComponentSetup.agent.md`).

This guide was produced by directly inspecting the repository contents at `C:\Users\EIB4KOR\Documents\prj_autodev-main`. Where the workspace did not conclusively establish something, this guide says so explicitly rather than guessing.

---

## 2. Architecture

### 2.1 Components

| Component | Type | Evidence |
|---|---|---|
| **Autodev** | Orchestrator custom agent — entry point, delegates via handoffs | `.github/agents/Autodev.agent.md` |
| **InternalQualityCheckerAgent** | Custom agent, not user-invocable, validates ticket completeness, labels `IQC_Pass`/`IQC_Fail` | `.github/agents/InternalQualityCheckerAgent.agent.md` |
| **BugAnalyst** | Custom agent, not user-invocable, produces Root Cause Analysis (no code changes) | `.github/agents/BugAnalyst.agent.md` |
| **FixGenerator** | Custom agent, not user-invocable, produces fix plan, applies code, pushes to Gerrit | `.github/agents/FixGenerator.agent.md` |
| **KGUpdater** | Custom agent — **planned feature, disabled** (no knowledge-graph MCP server deployed) | `.github/agents/KGUpdater.agent.md` |
| **ComponentSetup** | Custom agent, user-invocable, one-time-per-component registration wizard | `.github/agents/ComponentSetup.agent.md` |
| **Documentation Agent** (this guide's author) | Custom agent, user-invocable, produces workspace-verified documentation | `.github/agents/Documentation.agent.md` |
| **jira-python-mcp-server** | MCP server — JIRA REST integration | `.mcp.json`, `pmt-mcp-servers-main/src/jira/` |
| **sharepoint** MCP server | MCP server — SharePoint On-Premises integration (NTLM) | `.mcp.json`, `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/` |
| **gerrit** MCP server | MCP server — Gerrit Code Review REST integration | `.mcp.json`, `pmt-mcp-servers-main/src/gerrit/` |
| **bug-knowledge-graph** MCP server | Referenced in instructions as *planned feature*, **not present in this workspace** (no `pmt-mcp-servers-main/src/knowledge_graph` server files were found configured in `.mcp.json`/`.vscode/mcp.json`) | `.github/copilot-instructions.md` |

### 2.2 How components interact

1. The user invokes the **Autodev** agent with a JIRA issue key.
2. Autodev calls the **jira-python-mcp-server** to fetch the issue, then hands off to **InternalQualityCheckerAgent**, which also uses the JIRA MCP server to validate ticket fields and apply labels.
3. If validation passes, Autodev hands off to **BugAnalyst**, which reads JIRA (via MCP), local component docs under `core/docs/components/<slug>/` (created ahead of time by ComponentSetup), and workspace source files, then produces a Root Cause Analysis.
4. After explicit user approval, BugAnalyst posts the RCA to JIRA and hands off to **FixGenerator**, which drafts a fix plan, and — after a second explicit user approval — edits workspace files and pushes the change to Gerrit via the **gerrit** MCP server's `push_to_gerrit` tool.
5. A final JIRA comment is added confirming the fix; the **KGUpdater** step is explicitly skipped because the knowledge-graph feature is disabled (`.github/copilot-instructions.md`, Step 9).
6. Independently, **ComponentSetup** is run once per IVI component to fetch SharePoint documents and analyze source code, populating `core/docs/components/<slug>/component-info.md` and `component-flow.md`, which BugAnalyst/FixGenerator later read (`.github/agents/ComponentSetup.agent.md`).

### 2.3 Existing component registry data found in this workspace

`core/docs/components/` currently contains a `README.md` and one registered component directory: `dtv` (`core/docs/components/dtv`). No other components are registered.

---

## 3. Prerequisites

| Prerequisite | Required Version | Why it's required | Evidence |
|---|---|---|---|
| **Git** | Not specified by the project. | Clone/manage the repository; `push_to_gerrit` shells out to `git push` (`pmt-mcp-servers-main/src/gerrit/README.md`). | `core/SETUP.md`, `pmt-mcp-servers-main/src/gerrit/README.md` |
| **Python** | `>=3.13` for all three MCP servers (`requires-python` in each `pyproject.toml`). | Runs the JIRA, SharePoint, and Gerrit MCP servers. | `pmt-mcp-servers-main/src/jira/pyproject.toml`, `.../gerrit/pyproject.toml`, `.../sharepoint/sharepointonprem/pyproject.toml` |
| **uv** (Python package/venv manager) | Not specified by the project (only "latest" mentioned in `core/SETUP.md`, unverified). | The root `.mcp.json` launches each MCP server with `uv run --directory <path> <script>.py`. | `.mcp.json` |
| **dotenv-cli (npm package)** | Not specified. Confirmed present on this machine at `C:\Users\EIB4KOR\AppData\Roaming\npm\dotenv.cmd`. | The root `.mcp.json` wraps every MCP server command in `dotenv -e <path-to-.env> -- uv run ...` to load credentials from `.env` before starting the server. | `.mcp.json` |
| **GitHub Copilot CLI** | Version not specified by the project workspace. | This project's agents (`.github/agents/*.agent.md`) and MCP configuration are designed to be used from GitHub Copilot (chat/CLI); `README.md`/`core/SETUP.md` describe usage via the Copilot agent picker. | `.github/agents/`, `README.md` |
| **GitHub Copilot subscription/authentication** | Not determinable from the current workspace (no auth config files found). | Required to use Copilot Chat/CLI at all; referenced generally in `pmt-mcp-servers-main/src/jira/README.md` ("GitHub Copilot Subscription"). | `pmt-mcp-servers-main/src/jira/README.md` |
| **VS Code** ≥ 1.99 (per `core/SETUP.md`, unverified against any lock/version file) | Not verified elsewhere in the workspace. | `core/SETUP.md` describes enabling custom agents and MCP servers through VS Code settings (`.vscode/mcp.json`, `.vscode/settings.json`). Note: if you are using GitHub Copilot CLI instead of VS Code, VS Code itself is not required — see Section 5. | `core/SETUP.md`, `.vscode/mcp.json`, `.vscode/settings.json` |
| **Access credentials** for JIRA (personal access token), SharePoint (domain username/password), Gerrit (HTTP password) | N/A | Required by the three MCP servers to authenticate against each backend. | `.env.example`, `pmt-mcp-servers-main/src/*/README.md` |
| **poppler-utils** (system package) | Not specified. | Listed in `requirements.txt` as an optional dependency needed only if PDF-extraction via `pdfplumber` is enabled (currently commented out). | `requirements.txt` |
| **python-docx** (Python package, `>=1.0.0`) | `>=1.0.0` | Used by `setup.sh`/`requirements.txt` for DOCX→Markdown conversion in the ComponentSetup wizard. | `requirements.txt`, `setup.sh` |

**Discrepancy noted:** `README.md` and `core/SETUP.md` list "Python 3.13+" and "uv" as top-level prerequisites for the whole project, but the only place a Python version is actually pinned is inside each MCP server's `pyproject.toml` (`requires-python = ">=3.13"`). There is no root-level `pyproject.toml`/`requirements.txt` version pin for the main Autodev scripts themselves.

---

## 4. Repository Setup

1. **Obtain the repository.** This workspace (`prj_autodev-main`) already contains the MCP server implementations vendored under `pmt-mcp-servers-main/` — it is not a separate clone as `README.md`/`core/SETUP.md` suggest ("Clone MCP servers (if separate repository)"). No `.git` directory was found at the workspace root, so the exact remote origin/clone URL is **not determinable from the current workspace**.
2. **Enter the project directory:**
   ```powershell
   cd C:\Users\EIB4KOR\Documents\prj_autodev-main
   ```
3. **Install the MCP servers' Python dependencies** using `uv sync` inside each server directory (creates a local `.venv`), as documented in `core/SETUP.md`:
   ```powershell
   cd pmt-mcp-servers-main\src\jira; uv sync
   cd ..\sharepoint\sharepointonprem; uv sync
   cd ..\..\gerrit; uv sync
   ```
   Evidence: `.venv` directories already exist under each of these three server folders in this workspace, and each has its own `pyproject.toml`/`uv.lock`.
4. **Install the optional root-level Python dependencies** (used by the ComponentSetup document-conversion wizard), via `requirements.txt`:
   ```powershell
   pip install --user -r requirements.txt
   ```
   Note: `setup.sh` (evidence: `setup.sh`) automates this step but is a **Bash script** — on Windows it must be run under WSL/Git Bash, or the `pip install --user -r requirements.txt` command run directly in PowerShell.

---

## 5. GitHub Copilot CLI Setup

The workspace does not contain any installer, script, or documentation for installing GitHub Copilot CLI itself — external GitHub documentation must be consulted for installation and `gh`/Copilot CLI authentication (`gh auth login` or equivalent). This is **not determinable from the current workspace**.

What the workspace *does* define for the CLI:

- A root-level **`.mcp.json`** (evidence: `.mcp.json`) configuring three MCP servers (`jira-python-mcp-server`, `sharepoint`, `gerrit`) for use by an MCP-compatible client such as GitHub Copilot CLI. Each server entry uses `"type": "stdio"` (or `"local"`) and runs:
  ```
  dotenv -e C:\Users\EIB4KOR\Documents\prj_autodev-main\.env -- uv run --directory <server-dir> <script>.py
  ```
- Custom agents under **`.github/agents/*.agent.md`** (`Autodev`, `BugAnalyst`, `ComponentSetup`, `Documentation`, `FixGenerator`, `InternalQualityCheckerAgent`, `KGUpdater`) that a Copilot CLI/Copilot Chat client can discover and invoke by name.
- A hooks configuration at **`.github/hooks/approval-policy.json`** wiring a `preToolUse` hook (`scripts/mcp-approval-gate.ps1` / `.sh`) that forces a human-approval prompt before the tools `jira-python-mcp-server-add_issue_comment`, `jira-python-mcp-server-transition_issue`, and `gerrit-push_to_gerrit` are executed — this is enforced regardless of what the agent instructions say.

Only run commands that can be verified. To use this project with GitHub Copilot CLI:
1. Install and authenticate the GitHub Copilot CLI per GitHub's official documentation (external — not covered by this workspace).
2. Start the CLI with the current directory set to `C:\Users\EIB4KOR\Documents\prj_autodev-main` so it discovers `.mcp.json` and `.github/agents/`.
3. Ensure `.env` exists at the workspace root (see Section 6) before starting the CLI, since `.mcp.json` invokes `dotenv -e <absolute-path-to-.env>` to inject credentials — if this path or file is wrong/missing, MCP servers will start with empty credentials.

**Note on VS Code vs CLI configuration:** There is a **separate** configuration at `.vscode/mcp.json` intended for VS Code's GitHub Copilot Chat extension (not the CLI). It uses a different schema (`"servers"` instead of `"mcpServers"`), a direct path to the `uv.exe` binary, and VS Code's `${input:...}` credential-prompt mechanism rather than `.env`/`dotenv`. Do not confuse the two — the CLI reads `.mcp.json` at the workspace root, while VS Code reads `.vscode/mcp.json`.

---

## 6. Environment Configuration

Credentials are stored in a workspace-root `.env` file (git-ignored per `.gitignore`: `*.env`), loaded by `.mcp.json` via `dotenv -e <path>`. A template is provided at `.env.example`.

| Variable | Used By | Required/Optional | Purpose | Evidence |
|---|---|---|---|---|
| `TRACKER_URL` | jira-python-mcp-server | Required | Base JIRA instance URL | `.env.example`; read as `os.getenv("TRACKER_URL")` in `pmt-mcp-servers-main/src/jira/jiramcpserver.py:10` |
| `JIRA_TOKEN` | jira-python-mcp-server | Required | JIRA personal access token | `.env.example`; `jiramcpserver.py:12` |
| `SHAREPOINT_URL` | `.env`/`.env.example` only | — | Present in `.env.example`, but **not read by the SharePoint server code** (see discrepancy below) | `.env.example` |
| `SHAREPOINT_SITE_URL` | sharepoint MCP server | Required (per code) | SharePoint On-Premises site URL | `sharepointonpremserver.py:16` (`os.getenv("SHAREPOINT_SITE_URL", "")`) |
| `SHAREPOINT_USERNAME` | sharepoint MCP server | Required | Windows domain NTID (`DOMAIN\username`) | `.env.example`; `sharepointonpremserver.py:17` |
| `SHAREPOINT_PASSWORD` | sharepoint MCP server | Required | Windows domain password | `.env.example`; `sharepointonpremserver.py:18` |
| `CERTIFICATE_PATH` | sharepoint MCP server | Optional | Override CA bundle for SSL, or `"false"` to disable SSL verification (dev/test only) | `sharepointonpremserver.py:34` |
| `GERRIT_URL` | gerrit MCP server | Required | Base Gerrit URL | `.env.example`; `gerritmcpserver.py:23` |
| `GERRIT_USERNAME` | gerrit MCP server | Required | Gerrit HTTP username | `.env.example`; `gerritmcpserver.py:24` |
| `GERRIT_HTTP_PASSWORD` | gerrit MCP server | Required | Gerrit HTTP password (generated in Gerrit Settings → HTTP Credentials, **not** the SSO password) | `.env.example`; `gerritmcpserver.py:25` |
| `TRANSPORT` | all three MCP servers | Optional | MCP transport (`stdio` default, or `http`/`sse`) | `jiramcpserver.py:41`, `sharepointonpremserver.py:57`, `gerritmcpserver.py:433` |
| `HOST` | all three MCP servers | Optional | Host address if not using stdio transport (default `127.0.0.1`) | same files |
| `HOST_PORT` | all three MCP servers | Optional | Port if not using stdio transport (defaults: jira/sharepoint `8000`, gerrit `8001`) | same files |

**⚠️ Discrepancy — flagged, not silently resolved:** `.env.example`, `.env`, and the CLI's `.mcp.json` all define **`SHAREPOINT_URL`**, but the SharePoint server implementation (`pmt-mcp-servers-main/src/sharepoint/sharepointonprem/sharepointonpremserver.py:16`) reads **`SHAREPOINT_SITE_URL`** instead — `SHAREPOINT_URL` is never read by the code. As configured, the SharePoint MCP server will start with an empty site URL unless `SHAREPOINT_SITE_URL` is also set. The VS Code config `.vscode/mcp.json` does not define either variable for the `sharepoint` server's `env` block, so it inherits none of these values automatically either — VS Code instead relies on its own `${input:...}` prompts, which per `.vscode/mcp.json` are only wired for `SHAREPOINT_URL`/`SHAREPOINT_PASSWORD`, compounding the same mismatch.

Safe example for a new `.env` (never commit real values):
```
TRACKER_URL=<your-jira-base-url>
JIRA_TOKEN=<your-jira-personal-access-token>

SHAREPOINT_SITE_URL=<your-sharepoint-site-url>
SHAREPOINT_USERNAME=<domain>\<your-username>
SHAREPOINT_PASSWORD=<your-sharepoint-password>

GERRIT_URL=<your-gerrit-url>
GERRIT_USERNAME=<your-gerrit-username>
GERRIT_HTTP_PASSWORD=<your-gerrit-http-password>
```

---

## 7. MCP Server Configuration

### 7.1 jira-python-mcp-server

- **Purpose:** JIRA REST API integration — fetch issues, comment, transition status, manage labels, links, worklogs, etc. (67 tools per `pmt-mcp-servers-main/src/jira/README.md`).
- **Implementation:** `pmt-mcp-servers-main/src/jira/jiramcpserver.py`; package name `jira`, `requires-python = ">=3.13"` (`pmt-mcp-servers-main/src/jira/pyproject.toml`).
- **Startup command (CLI, `.mcp.json`):**
  ```
  dotenv -e <workspace>\.env -- uv run --directory <workspace>\pmt-mcp-servers-main\src\jira jiramcpserver.py
  ```
- **Startup command (VS Code, `.vscode/mcp.json`):** direct `uv.exe run jiramcpserver.py` with `cwd` set to the jira server directory and `env` populated via VS Code `${input:jira-url}` / `${input:jira-token}` prompts.
- **Required env vars:** `TRACKER_URL`, `JIRA_TOKEN` (Section 6).
- **External system:** a JIRA instance reachable at `TRACKER_URL`.
- **Auth:** Bearer personal access token (`JIRA_TOKEN`).
- **Verification:** with dependencies installed, run manually:
  ```powershell
  cd pmt-mcp-servers-main\src\jira
  uv run jiramcpserver.py
  ```
  A working server should start without raising a Python exception and remain running, waiting for stdio MCP requests (no output is expected on a bare stdio run — this is expected behavior, not an error).

### 7.2 sharepoint (SharePoint On-Premises)

- **Purpose:** SharePoint On-Premises file/folder management via NTLM auth (28 tools per `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/README.md`). Used exclusively by the **ComponentSetup** agent per `.github/copilot-instructions.md`.
- **Implementation:** `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/sharepointonpremserver.py`; package `sharepoint-onprem`, `requires-python = ">=3.13"`.
- **Startup command (CLI, `.mcp.json`):**
  ```
  dotenv -e <workspace>\.env -- uv run --directory <workspace>\pmt-mcp-servers-main\src\sharepoint\sharepointonprem sharepointonpremserver.py
  ```
- **Required env vars:** `SHAREPOINT_SITE_URL`, `SHAREPOINT_USERNAME`, `SHAREPOINT_PASSWORD` (see Section 6 discrepancy re: `SHAREPOINT_URL` vs `SHAREPOINT_SITE_URL`). Optional: `CERTIFICATE_PATH`.
- **External system:** SharePoint On-Premises server (NTLM), not SharePoint Online.
- **Auth:** NTLM using Windows domain credentials (`DOMAIN\username` + password).
- **Verification:** manually run `uv run sharepointonpremserver.py` from `pmt-mcp-servers-main/src/sharepoint/sharepointonprem`; once connected through a client, the `check_sharepoint_access` tool can confirm connectivity.

### 7.3 gerrit

- **Purpose:** Gerrit Code Review REST API integration — list/get changes, post reviews, and push local commits (`push_to_gerrit`) (`pmt-mcp-servers-main/src/gerrit/README.md`).
- **Implementation:** `pmt-mcp-servers-main/src/gerrit/gerritmcpserver.py`; package `gerritmcpserver`, `requires-python = ">=3.13"`.
- **Startup command (CLI, `.mcp.json`):**
  ```
  dotenv -e <workspace>\.env -- uv run --directory <workspace>\pmt-mcp-servers-main\src\gerrit gerritmcpserver.py
  ```
- **Required env vars:** `GERRIT_URL`, `GERRIT_USERNAME`, `GERRIT_HTTP_PASSWORD`.
- **External system:** a Gerrit Code Review server.
- **Auth:** HTTP Basic Auth using a Gerrit-generated HTTP password (Settings → HTTP Credentials), **not** the SSO/login password (`pmt-mcp-servers-main/src/gerrit/README.md`).
- **Additional requirement:** `push_to_gerrit` requires `git` on `PATH` and the local repository already configured with the Gerrit remote (`pmt-mcp-servers-main/src/gerrit/README.md`).
- **Verification:** `uv run gerritmcpserver.py` from `pmt-mcp-servers-main/src/gerrit` should start without error; the `list_gerrit_projects`/`list_gerrit_changes` tools can confirm connectivity once wired into a client.

### 7.4 bug-knowledge-graph (planned, not present)

`.github/copilot-instructions.md` and several agent files reference a fourth MCP server, `bug-knowledge-graph` (Neo4j + Graphiti backend), for storing/querying historical bug analyses. No corresponding server implementation, `.mcp.json` entry, or `.vscode/mcp.json` entry exists in this workspace. All KG-related steps in the pipeline are explicitly marked "planned feature — disabled" and are skipped (`.github/copilot-instructions.md`, Step 9; `.github/agents/KGUpdater.agent.md`).

### 7.5 Approval-gate hook

`.github/hooks/approval-policy.json` registers a `preToolUse` hook running `scripts/mcp-approval-gate.ps1` (Windows) / `scripts/mcp-approval-gate.sh`. It inspects the tool name from stdin JSON and returns `{"permissionDecision":"ask"}` for exactly these tool names, forcing an interactive approval prompt: `jira-python-mcp-server-add_issue_comment`, `jira-python-mcp-server-transition_issue`, `gerrit-push_to_gerrit`. All other tool calls return `{"permissionDecision":"allow"}`. This is enforced independent of, and in addition to, the approval-gate language written into the agent instructions.

---

## 8. Running the Project

1. **Create/verify `.env`** at the workspace root (Section 6). Where run: `C:\Users\EIB4KOR\Documents\prj_autodev-main\.env`. What it does: supplies JIRA/SharePoint/Gerrit credentials that `.mcp.json` injects via `dotenv -e`. Success looks like: the file exists with all keys from `.env.example` populated with real values (never commit it — it is covered by `.gitignore`'s `*.env` rule).
2. **Sync each MCP server's dependencies** (Section 4, step 3):
   ```powershell
   cd pmt-mcp-servers-main\src\jira; uv sync
   cd ..\..\sharepoint\sharepointonprem; uv sync
   cd ..\..\gerrit; uv sync
   ```
   Where run: each server subdirectory. What it does: resolves and installs each server's pinned dependencies into a local `.venv` per its `uv.lock`. Success: a `.venv` directory is created/updated with no errors.
3. **Start GitHub Copilot CLI** with the working directory set to the workspace root so `.mcp.json` and `.github/agents/` are discovered. Exact CLI installation/launch command is **not determinable from the current workspace** — consult GitHub's official Copilot CLI documentation.
4. **Confirm the three MCP servers initialize.** How to verify this is client-specific; this workspace does not contain a CLI-specific verification script. For VS Code, `core/SETUP.md` describes checking the VS Code status bar / Output panel ("MCP") — this applies to the VS Code integration path, not necessarily the CLI.
5. **Invoke the `ComponentSetup` agent once per IVI software component** before analyzing any bugs for that component, per `README.md`/`SETUP_CHECKLIST.md`. This populates `core/docs/components/<slug>/`.
6. **Invoke the `Autodev` agent with a JIRA issue key** (e.g., `PROJ-1234`) to run the bug-analysis-to-fix pipeline described in Section 1 and Section 9.

---

## 9. Using the Copilot Agent

### 9.1 How agents are discovered

Agents are defined as Markdown files with YAML frontmatter under `.github/agents/*.agent.md`. Each file declares a `name`, `description`, `tools` list, optional `handoffs` to other agents, and (for several agents) a `human-in-the-loop` block describing mandatory approval gates. This matches the custom-agent format referenced by `pmt-mcp-servers-main/README.md` ("Custom agents are a way to create distinct identities and with specific tools for a specific task or domain... Invoke with @ or select the custom agent").

### 9.2 User-invocable vs internal agents

| Agent | `user-invocable` | Notes |
|---|---|---|
| `Autodev` | not set to false → user-invocable | Entry point; `argument-hint: Enter the JIRA issue key (e.g., PROJ-1234)` |
| `ComponentSetup` | not set to false → user-invocable | `argument-hint: "Type 'start' to begin component registration"` |
| `Documentation` (`documentation-agent`) | `user-invocable: true`, `disable-model-invocation: true` | Only invocable directly by name, never auto-selected |
| `BugAnalyst` | `user-invocable: false` | Only reachable via Autodev's handoff |
| `FixGenerator` | `user-invocable: false` | Only reachable via BugAnalyst's handoff |
| `InternalQualityCheckerAgent` | `user-invocable: false` | Only reachable via Autodev's handoff |
| `KGUpdater` | not explicitly user-invocable; feature marked disabled throughout instructions | Not part of the active pipeline |

Evidence: frontmatter of each `.github/agents/*.agent.md` file.

### 9.3 Typical workflow

**Register a component (one time per component):**
1. Invoke the `ComponentSetup` agent (e.g., by name/mention, per your Copilot client's convention) and type `start`.
2. Provide the component name and workspace source path(s).
3. Choose a registration method: SharePoint fetch, local document upload, or manual interview (`.github/agents/ComponentSetup.agent.md`).
4. Approve the file-creation step when prompted (`human-in-the-loop` block requires explicit consent before writing files).
5. Verify `core/docs/components/<slug>/component-info.md` and `component-flow.md` were created.

**Analyze and fix a bug:**
1. Invoke the `Autodev` agent and supply a JIRA issue key.
2. Autodev delegates to `InternalQualityCheckerAgent`, which validates the ticket and applies an `IQC_Pass`/`IQC_Fail` label (asking approval before posting labels/comments).
3. If passed, `BugAnalyst` reads the JIRA ticket, the local `core/docs/components/<slug>/` registry, and workspace source files, then presents a Root Cause Analysis and **stops**, asking: "Do you approve posting this to JIRA and proceeding? Reply yes/no/edit." (`.github/copilot-instructions.md`, Step 3a).
4. Upon approval, the RCA is posted to JIRA and `FixGenerator` is handed off the analysis; it drafts a fix plan and **stops** again, asking: "Do you approve applying these changes and pushing to Gerrit? Reply yes/no/edit." (Step 6).
5. Upon approval, `FixGenerator` edits the relevant files and calls `push_to_gerrit`, then reports the Gerrit change URL.
6. The `bug-knowledge-graph` step is skipped; instead a final JIRA comment notes that KG recording will be available in a future release (Step 9).

Tools available to each agent are restricted per its frontmatter `tools:` list (Section 9.2 evidence links); for example, `BugAnalyst` has no SharePoint tools (by design — it must read only the local registry), while `FixGenerator` has `gerrit/push_to_gerrit`, `gerrit/list_gerrit_changes`, `gerrit/get_gerrit_change` but no SharePoint tools either.

---

## 10. Verification

| Check | How to verify | Evidence |
|---|---|---|
| MCP servers can start | Run each server manually: `cd pmt-mcp-servers-main\src\jira; uv run jiramcpserver.py` (repeat for `sharepoint\sharepointonprem` and `gerrit`). No exception should be raised; the process stays running on stdio. | `.mcp.json`, each server's `pyproject.toml` |
| `.env` is being loaded | Confirm the `dotenv` CLI is installed (`where.exe dotenv` → resolved on this machine to `C:\Users\EIB4KOR\AppData\Roaming\npm\dotenv.cmd`) and that `.env` exists at the exact absolute path referenced in `.mcp.json` (`C:\Users\EIB4KOR\Documents\prj_autodev-main\.env`). | `.mcp.json` |
| JIRA auth works | Use the `jira_request` tool (or `get_all_projects`) once the JIRA MCP server is connected in a client; a 401 indicates `JIRA_TOKEN`/`TRACKER_URL` are wrong. | `pmt-mcp-servers-main/src/jira/README.md` |
| SharePoint auth works | Use `check_sharepoint_access`; confirm `SHAREPOINT_SITE_URL` (not `SHAREPOINT_URL`) is set — see Section 6 discrepancy. | `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/README.md` |
| Gerrit auth works | Use `list_gerrit_projects`; a 403/401 indicates `GERRIT_HTTP_PASSWORD` is wrong or expired. | `pmt-mcp-servers-main/src/gerrit/README.md` |
| Agents are discovered | Confirm all seven `.agent.md` files are present: `ls .github/agents/*.agent.md` should list `Autodev`, `BugAnalyst`, `ComponentSetup`, `Documentation`, `FixGenerator`, `InternalQualityCheckerAgent`, `KGUpdater`. | `.github/agents/` |
| Component registry available | `ls core/docs/components/` should show at least `README.md` and, in this workspace, `dtv/`. | `core/docs/components/` |
| External services reachable | Not determinable from the current workspace — no network/proxy test scripts exist here; standard `ping`/`curl` against your JIRA/SharePoint/Gerrit hostnames can be used if your network allows it. | — |

---

## 11. Troubleshooting

- **MCP server fails to start / "Failed to start MCP server":** Verify the `uv` binary is on `PATH` (`where.exe uv`) and that the absolute paths in `.mcp.json` / `.vscode/mcp.json` match this machine's actual clone location. Test each server manually as in Section 10. (`core/SETUP.md`, `.mcp.json`)
- **SharePoint server has no site URL configured:** This is the `SHAREPOINT_URL` vs `SHAREPOINT_SITE_URL` mismatch documented in Section 6 — set `SHAREPOINT_SITE_URL` in `.env`. (`sharepointonpremserver.py:16`)
- **JIRA 401 Unauthorized:** `JIRA_TOKEN` is invalid or expired; regenerate a personal access token and update `.env`. (`pmt-mcp-servers-main/src/jira/README.md`, "Authentication Issues")
- **JIRA "Failed to connect to Jira":** `TRACKER_URL` is malformed — must include the `https://` scheme and should not have a trailing slash. (`core/SETUP.md`)
- **Gerrit push fails with HTTP 403:** `GERRIT_HTTP_PASSWORD` must be the Gerrit-generated HTTP password from Settings → HTTP Credentials, not your SSO password; also confirm the local git repo's remote points at the Gerrit URL and that `git` is on `PATH`. (`pmt-mcp-servers-main/src/gerrit/README.md`)
- **SharePoint SSL/certificate errors:** Set `CERTIFICATE_PATH` to a corporate CA bundle path, or `"false"` to disable verification for local dev/test only (not for production). (`sharepointonpremserver.py:34`, `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/README.md`)
- **`python3`/`pip3` not found while running `setup.sh`:** `setup.sh` is a Bash script that explicitly checks for `python3`/`pip3` on `PATH` and exits with an error if missing; on Windows this script must be run in WSL/Git Bash, or its `pip install --user -r requirements.txt` step run manually in PowerShell with `pip`. (`setup.sh`)
- **Agent not appearing in the agent picker:** Confirm `.github/agents/*.agent.md` files exist and check your Copilot client's setting for enabling custom/chat agents (for VS Code, `core/SETUP.md` references `"chat.agent.enabled": true`). Whether an equivalent setting exists for the CLI is **not determinable from the current workspace**.
- **Approval prompt appears unexpectedly (or doesn't):** This is governed by `.github/hooks/approval-policy.json` plus `scripts/mcp-approval-gate.ps1`/`.sh`, which force an "ask" decision only for `jira-python-mcp-server-add_issue_comment`, `jira-python-mcp-server-transition_issue`, and `gerrit-push_to_gerrit`. All other tool calls are auto-allowed by this hook (the agent-level human-in-the-loop instructions are a separate, additional layer).
- **Incorrect working directory:** Because `.mcp.json` and `core/SETUP.md`'s `uv sync` commands use paths relative to specific subdirectories (`pmt-mcp-servers-main/src/jira`, etc.), always run `uv sync`/`uv run` from inside that exact server directory, not the repository root.

---

## 12. Windows vs Linux

This workspace runs on **Windows** (evidence: `environment_context`, absolute paths in `.mcp.json` and `.vscode/mcp.json` use `C:\Users\...` and backslashes; `uv.exe` resolved under `AppData\Local\Microsoft\WinGet\...`). Platform-specific points found in the workspace:

| Aspect | Windows | Linux/macOS |
|---|---|---|
| `.mcp.json` command paths | Backslash paths, e.g. `C:\Users\EIB4KOR\Documents\prj_autodev-main\...` | `core/SETUP.md` and `.vscode/mcp.json.example` use forward-slash paths, e.g. `/home/YOUR_USERNAME/.local/bin/uv` |
| `setup.sh` | Not directly runnable in PowerShell — it is a Bash script (`#!/bin/bash`, uses `${BASH_SOURCE[0]}`) and requires WSL/Git Bash | Runs natively (`./setup.sh`) |
| `chat.agent.enabled` settings file location (VS Code, per `core/SETUP.md`) | `%APPDATA%\Code\User\settings.json` region not explicitly given for Windows in the workspace — `core/SETUP.md` only shows Linux/macOS paths | `~/.config/Code/User/settings.json` (Linux) / `~/Library/Application Support/Code/User/settings.json` (macOS) |
| `.venv` layout | `Scripts\` subfolder (e.g. `pmt-mcp-servers-main\src\jira\.venv\Scripts\`) confirmed present in this workspace | `bin/` subfolder (not present here) |
| poppler-utils install command in `requirements.txt`/`setup.sh` | Not applicable directly — `sudo apt-get install poppler-utils` is Debian/Ubuntu-specific | Applies on Debian/Ubuntu; an equivalent Windows package/install method is **not determinable from the current workspace** |

No workspace file documents a Windows-specific `.mcp.json`/`.vscode/mcp.json.example` template except the one already present with this machine's real paths (`.vscode/mcp.json`) — the generic template (`.vscode/mcp.json.example`) is Linux-oriented.

---

## 13. Complete First-Time Setup Checklist

- [ ] Install Git, Python (`>=3.13` for MCP servers), and `uv` (versions otherwise not specified by the project).
- [ ] Install and authenticate GitHub Copilot CLI per GitHub's official docs (not covered by this workspace).
- [ ] Install the `dotenv` CLI (npm package) if not already present — required by `.mcp.json`.
- [ ] Clone/open the repository at a known absolute path.
- [ ] Run `uv sync` inside `pmt-mcp-servers-main/src/jira`, `pmt-mcp-servers-main/src/sharepoint/sharepointonprem`, and `pmt-mcp-servers-main/src/gerrit`.
- [ ] Optionally run `pip install --user -r requirements.txt` (or `setup.sh` under WSL/Git Bash) for the ComponentSetup document-conversion dependencies.
- [ ] Create `.env` at the workspace root from `.env.example`, populating `TRACKER_URL`, `JIRA_TOKEN`, `SHAREPOINT_SITE_URL` (not `SHAREPOINT_URL` — see Section 6), `SHAREPOINT_USERNAME`, `SHAREPOINT_PASSWORD`, `GERRIT_URL`, `GERRIT_USERNAME`, `GERRIT_HTTP_PASSWORD`.
- [ ] Generate a JIRA personal access token and a Gerrit HTTP password; confirm SharePoint domain credentials.
- [ ] Verify absolute paths inside `.mcp.json` (CLI) match your machine, or `.vscode/mcp.json` if using VS Code instead.
- [ ] Start GitHub Copilot CLI from the workspace root directory.
- [ ] Manually smoke-test each MCP server (`uv run <script>.py` in each server directory) to confirm no startup errors.
- [ ] Confirm `.github/agents/*.agent.md` are discovered by your Copilot client.
- [ ] Run `ComponentSetup` for each IVI component your team works on (skip if already present under `core/docs/components/`, e.g. `dtv` in this workspace).
- [ ] Run `Autodev` with a real JIRA issue key and walk through both approval gates (RCA approval, fix-plan approval) to confirm end-to-end operation.

---

## 14. Workspace Evidence

| File | Information Obtained |
|---|---|
| `README.md` | Project overview, features, agent pipeline description, usage instructions |
| `SETUP_CHECKLIST.md` | Setup checklist claims (cross-checked against actual config) |
| `core/SETUP.md` | Detailed setup/troubleshooting narrative (cross-checked against actual config) |
| `architecture.md` | System architecture diagrams (Android IVI layers, agent pipeline) |
| `.github/copilot-instructions.md` | Canonical orchestrator workflow, approval gates, tool quick-reference |
| `.github/agents/Autodev.agent.md` | Orchestrator agent frontmatter, tools, handoffs |
| `.github/agents/BugAnalyst.agent.md` | RCA agent frontmatter, tools, human-in-the-loop gates |
| `.github/agents/FixGenerator.agent.md` | Fix-generation agent frontmatter, tools, human-in-the-loop gates |
| `.github/agents/ComponentSetup.agent.md` | Component registration wizard frontmatter and notes |
| `.github/agents/InternalQualityCheckerAgent.agent.md` | Ticket validation agent frontmatter, tools |
| `.github/agents/KGUpdater.agent.md` | Disabled/planned knowledge-graph agent |
| `.github/agents/Documentation.agent.md` | This documentation agent's own instructions |
| `.github/hooks/approval-policy.json` | `preToolUse` hook registration |
| `scripts/mcp-approval-gate.ps1` | Logic forcing approval prompts for specific MCP tool calls |
| `.mcp.json` | Root MCP server configuration used by GitHub Copilot CLI (`dotenv` + `uv run`) |
| `.vscode/mcp.json` | VS Code-specific MCP server configuration (direct `uv.exe`, `${input:...}` prompts) |
| `.vscode/mcp.json.example` | Linux-oriented template for `.vscode/mcp.json` |
| `.vscode/settings.json` | `chat.mcp.serverSampling` allowed-models configuration |
| `.env.example` | Environment variable names/template (`TRACKER_URL`, `JIRA_TOKEN`, `SHAREPOINT_URL`, `SHAREPOINT_USERNAME`, `SHAREPOINT_PASSWORD`, `GERRIT_URL`, `GERRIT_USERNAME`, `GERRIT_HTTP_PASSWORD`) |
| `.env` (keys only; values never read into this guide) | Confirms actual `.env` present at workspace root uses the same key names as `.env.example` |
| `.gitignore` | Confirms `.env`, `.vscode/mcp.json`, `custome_agents.code-workspace`, and `core/workspace/` are excluded from version control |
| `requirements.txt` | Root-level optional Python dependencies (`python-docx`, optional `pdfplumber`) |
| `setup.sh` | Bash installer for `requirements.txt` dependencies |
| `pmt-mcp-servers-main/src/jira/jiramcpserver.py` | JIRA MCP server env var reads (`TRACKER_URL`, `JIRA_TOKEN`, `TRANSPORT`, `HOST`, `HOST_PORT`) |
| `pmt-mcp-servers-main/src/jira/pyproject.toml` | JIRA server Python version/dependency pins |
| `pmt-mcp-servers-main/src/jira/README.md` | JIRA server configuration table, tool list, troubleshooting |
| `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/sharepointonpremserver.py` | SharePoint server env var reads (`SHAREPOINT_SITE_URL`, `SHAREPOINT_USERNAME`, `SHAREPOINT_PASSWORD`, `CERTIFICATE_PATH`, `TRANSPORT`, `HOST`, `HOST_PORT`) — revealed the `SHAREPOINT_URL` mismatch |
| `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/pyproject.toml` | SharePoint server Python version/dependency pins |
| `pmt-mcp-servers-main/src/sharepoint/sharepointonprem/README.md` | SharePoint server configuration table, tool list, troubleshooting |
| `pmt-mcp-servers-main/src/gerrit/gerritmcpserver.py` | Gerrit server env var reads (`GERRIT_URL`, `GERRIT_USERNAME`, `GERRIT_HTTP_PASSWORD`, `TRANSPORT`, `HOST`, `HOST_PORT`) |
| `pmt-mcp-servers-main/src/gerrit/pyproject.toml` | Gerrit server Python version/dependency pins |
| `pmt-mcp-servers-main/src/gerrit/README.md` | Gerrit server configuration table, tool list, `push_to_gerrit` requirements |
| `pmt-mcp-servers-main/README.md` | Confirms custom-agent invocation convention (`@agent` / picker) and broader PMT@XC MCP server catalog |
| `core/docs/components/` (directory listing) | Confirms only one component (`dtv`) is currently registered |
| `core/scripts/` (directory listing) | Confirms attachment-processing scripts live under `core/scripts/`, not the top-level `scripts/` referenced by `README.md`/`core/SETUP.md` |
| `custome_agents.code-workspace.template` | Multi-root workspace template referencing an external AOSP project folder |

**Discrepancy summary (for quick reference):**
1. `SHAREPOINT_URL` (in `.env`/`.env.example`/`.mcp.json`) vs `SHAREPOINT_SITE_URL` (actually read by `sharepointonpremserver.py`).
2. `README.md`/`core/SETUP.md` describe `scripts/test_processor.py` and `scripts/README.md` at the project root, but these files actually live under `core/scripts/`; the top-level `scripts/` directory in this workspace only contains the approval-gate hook scripts.
3. `README.md`/`core/SETUP.md` describe cloning `Autodev` and `pmt-mcp-servers-main` as two separate repositories side by side; in this workspace, `pmt-mcp-servers-main` is already vendored inside `prj_autodev-main` as a subdirectory, and no `.git` directory was found to confirm remote origins.
4. `README.md`/`core/SETUP.md` reference an "Autodev" project folder name and nested `Autodev/Autodev` paths in some examples; the actual workspace root directory name is `prj_autodev-main`.
