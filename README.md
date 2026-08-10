# Autodev

> **AI-Powered Bug Analysis & Fix Workflow for Android IVI Teams**  
> 🤖 Automated root cause analysis 🔍 → Fix generation 🔧 → Gerrit integration 🚀

[![VS Code Extension](https://img.shields.io/badge/VS%20Code-GitHub%20Copilot-blue?logo=visual-studio-code)](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
[![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📖 Overview

**Autodev** is an intelligent VS Code agent workflow built for **Android IVI (In-Vehicle Infotainment)** development teams working with AOSP/Android Automotive OS (AAOS). It automates the complete bug resolution lifecycle:

```
📋 JIRA Issue → 🔍 Root Cause Analysis → 🔧 Fix Generation → 🚀 Gerrit Push → 📊 Knowledge Storage
```

### The Problem

Android IVI teams face significant challenges:

- ⏱️ **Time-consuming manual analysis** across JIRA, SharePoint, and multiple documentation sources
- 📝 **Incomplete bug tickets** missing critical test setups, specs, or logs
- 🔄 **Knowledge silos** leading to repeated investigations of similar issues
- 🔀 **Manual context switching** between tools and repositories
- ⚠️ **Inconsistent fix quality** due to lack of structured workflows

### The Solution

Autodev provides:

- ✅ **Automated JIRA validation** with 24 quality criteria checks
- 🤖 **AI-assisted root cause analysis** with multi-source documentation retrieval
- 📝 **Structured RCA reports** covering all Android layers (App/Framework/HAL/Kernel)
- 🔐 **Mandatory approval gates** preventing premature or incorrect fixes
- 🚀 **Automated Gerrit integration** following AOSP contribution guidelines
- 📚 **Component registry system** for fast, workspace-first documentation access

---

## ✨ Key Features

### 🔍 Intelligent Root Cause Analysis

- **Multi-source synthesis**: Combines JIRA tickets, SharePoint documents (AIDL specs, SDD, HMI designs), local component docs, and workspace source code
- **Android layer-aware**: Analyzes issues across App, Framework, HAL, and Kernel layers
- **Log processing**: Automatically extracts and prioritizes logs (ANR → tombstones → logcat → system)
- **Structured reports**: Consistent RCA format with symptoms, contributing factors, root cause, and fix direction

### 🛡️ Quality Gates

- **Pre-flight validation**: InternalQualityCheckerAgent validates 24 ticket criteria before analysis begins
- **RCA approval gate**: User must review and approve root cause analysis before posting to JIRA
- **Fix approval gate**: User must review and approve code changes before applying and pushing
- **Fail-fast approach**: Invalid tickets blocked before expensive analysis work

### 🔄 Complete AOSP/AAOS Integration

- **JIRA**: Fetch issues, post comments, transition status, manage labels
- **SharePoint**: Retrieve AIDL API specs, Software Design Documents, HMI designs, Component Information Documents
- **Gerrit**: Push code changes following AOSP guidelines, track review status
- **Knowledge Graph** *(planned)*: Store historical bug patterns for similarity detection

### 📁 Workspace-First Component Registry

- **ComponentSetup wizard**: Interactive setup for registering IVI components (DTV, MIS, Audio HAL, VHAL, etc.)
- **Local documentation**: Pre-fetched SharePoint docs stored in `core/docs/components/`
- **Code analysis**: Auto-extracted interface signatures, logcat tags, dependencies
- **Layer diagrams**: ASCII architecture diagrams and interface maps
- **Fast access**: BugAnalyst reads local registry before querying SharePoint

---

## 🏗️ Architecture

### Agent Pipeline

```
User provides JIRA key (e.g., PROJ-123)
        ↓
┌─────────────────────────────────────────────────┐
│  Autodev Orchestrator                           │
│  • Validates input                              │
│  • Tracks pipeline state                        │
│  • Delegates to sub-agents                      │
└─────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────┐
│  Step 0: InternalQualityCheckerAgent            │
│  • Validates 24 JIRA criteria                   │
│  • Checks attachments, test setup, spec links   │
│  • Labels: IQC_Pass / IQC_Fail                  │
│  • ⛔ Stops pipeline if validation fails        │
└─────────────────────────────────────────────────┘
        ↓ (only if PASS)
┌─────────────────────────────────────────────────┐
│  Step 1: BugAnalyst                             │
│  • Fetches JIRA ticket                          │
│  • Checks local component registry              │
│  • Browses workspace source files               │
│  • Downloads & processes attachments            │
│  • Queries SharePoint (if needed)               │
│  • Produces structured RCA                      │
│  • ⛔ Approval gate: User approves RCA          │
│  • Posts RCA to JIRA after approval             │
└─────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────┐
│  Step 2: FixGenerator                           │
│  • Loads workspace paths from component-info.md │
│  • Reads source files (Java/Kotlin/C++/AIDL)    │
│  • Generates detailed fix plan                  │
│  • ⛔ Approval gate: User approves fix plan     │
│  • Applies code changes to workspace            │
│  • Pushes to Gerrit following AOSP guidelines   │
│  • Posts confirmation to JIRA                   │
└─────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────┐
│  Step 3: KGUpdater (Planned - Disabled)         │
│  • Stores analysis + fix in knowledge graph     │
│  • Updates status when Gerrit change merges     │
└─────────────────────────────────────────────────┘
```

### Available Agents

| Agent | User-Invokable | Purpose |
|-------|:--------------:|---------|
| **Autodev** | ✅ | Main orchestrator - entry point for bug resolution workflow |
| **ComponentSetup** | ✅ | Interactive wizard for registering IVI components |
| **BugAnalyst** | ❌ | Root cause analysis (invoked by Autodev) |
| **FixGenerator** | ❌ | Fix generation & Gerrit push (invoked by Autodev) |
| **InternalQualityCheckerAgent** | ❌ | JIRA validation (invoked by Autodev) |
| **KGUpdater** | ❌ | Knowledge graph persistence (planned - disabled) |

### MCP Servers

| Server | Purpose | Status |
|--------|---------|:------:|
| **jira-python-mcp-server** | JIRA API integration (fetch, comment, transition, labels) | ✅ Active |
| **sharepoint-mcp-server** | SharePoint document retrieval (AIDL, SDD, HMI, CID) | ✅ Active |
| **gerrit-mcp-server** | Gerrit code review integration (push, query changes) | ✅ Active |
| **bug-knowledge-graph** | Historical bug pattern storage (Neo4j + Graphiti) | 📅 Planned |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.13+** (`python3 --version`)
- **uv** package manager (`uv --version` - [install guide](https://github.com/astral-sh/uv))
- **VS Code** with [GitHub Copilot extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)
- **Git** (`git --version`)
- Access credentials for:
  - JIRA (Personal Access Token)
  - SharePoint (username + password)
  - Gerrit (HTTP password)

### Quick Installation

```bash
# 1. Clone the repository
git clone <autodev-repo-url>
cd Autodev

# 2. Run setup script
./setup.sh

# 3. Configure MCP servers
cp .vscode/mcp.json.example .vscode/mcp.json
# Edit .vscode/mcp.json with your paths and credentials

# 4. Open in VS Code
code .
```

### Detailed Setup

For comprehensive setup instructions, see:
- 📘 [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Step-by-step installation checklist
- 📗 [core/SETUP.md](core/SETUP.md) - Detailed configuration guide with troubleshooting

---

## 📚 Usage

### 1️⃣ Register Components (First Time)

Before analyzing bugs, register each IVI component with ComponentSetup:

```
1. Open Copilot Chat in VS Code
2. Select @ComponentSetup agent
3. Type: start
4. Follow the interactive wizard:
   - Enter component name (e.g., "DTV Service")
   - Provide workspace source paths
   - Choose registration method:
     • Option 1: Fetch from SharePoint (recommended)
     • Option 2: Upload local documents (PDF/DOCX/TXT/MD)
     • Option 3: Manual interview (no documents)
```

This creates:
```
core/docs/components/dtv-service/
├── component-info.md          # Architecture, interfaces, logcat tags
├── component-flow.md          # Layer diagram, interface map
└── source-documents/          # Fetched SharePoint docs
    ├── INDEX.md               # Document inventory
    ├── dtv-sdd-v2.3.md        # Software Design Document
    ├── dtv-aidl-api-v1.5.md   # AIDL API specification
    └── dtv-hmi-flow.md        # HMI design flow
```

### 2️⃣ Analyze a Bug

```
1. Open Copilot Chat
2. Select @Autodev agent
3. Enter JIRA issue key: PROJ-123
```

**The workflow will:**
1. ✅ Validate ticket quality (InternalQualityCheckerAgent)
2. 🔍 Perform root cause analysis (BugAnalyst)
   - ⛔ **STOP**: Review and approve RCA
3. 🔧 Generate fix plan (FixGenerator)
   - ⛔ **STOP**: Review and approve fix
4. 🚀 Apply changes and push to Gerrit
5. 📝 Update JIRA with RCA and Gerrit link

### 3️⃣ Log Processing (Automatic)

Autodev automatically processes JIRA attachments:

```
workspace/PROJ-123/
├── attachments/               # Raw downloads
│   └── bugreport-2026-04-28.zip
├── extracted/                 # Extracted archives
│   └── bugreport-2026-04-28/
└── logs/                      # Organized by type
    ├── anr/                   # ANR traces (highest priority)
    ├── tombstones/            # Native crash dumps
    ├── logcat/                # Android system logs
    └── system/                # Kernel logs, dumpsys output
```

BugAnalyst automatically reads priority logs: **ANR → tombstones → logcat → system**

---

## 📂 Project Structure

```
Autodev/
├── .github/
│   ├── copilot-instructions.md        # Main agent workflow instructions
│   └── agents/                        # Sub-agent definitions
│       ├── Autodev.agent.md           # Orchestrator agent
│       ├── BugAnalyst.agent.md        # Root cause analysis agent
│       ├── FixGenerator.agent.md      # Fix generation agent
│       ├── ComponentSetup.agent.md    # Component registration wizard
│       ├── InternalQualityCheckerAgent.agent.md
│       └── KGUpdater.agent.md         # (Planned) Knowledge graph agent
│
├── .vscode/
│   ├── mcp.json                       # MCP server configuration
│   └── mcp.json.example               # Template configuration
│
├── core/
│   ├── docs/
│   │   └── components/                # Component registry (workspace-first docs)
│   │       ├── README.md
│   │       └── <component-slug>/
│   │           ├── component-info.md  # Architecture, interfaces, tags
│   │           ├── component-flow.md  # Layer diagrams, interface maps
│   │           └── source-documents/  # Fetched SharePoint docs
│   │               └── INDEX.md
│   │
│   ├── scripts/
│   │   ├── process_jira_attachments.py  # Attachment extraction & organization
│   │   ├── extract_pdf_to_md.py         # PDF → Markdown converter
│   │   ├── extract_docx_to_md.py        # DOCX → Markdown converter
│   │   ├── convert_docx_enhanced.py     # Enhanced DOCX processor
│   │   ├── extract_image_to_md.py       # Image → Markdown (OCR)
│   │   ├── extract_text_to_md.py        # Plain text → Markdown
│   │   ├── test_processor.py            # Test suite
│   │   └── README.md                    # Script documentation
│   │
│   ├── workspace/                       # Working directory for bug analysis
│   │   └── <ISSUE-KEY>/
│   │       ├── attachments/
│   │       ├── extracted/
│   │       └── logs/
│   │
│   ├── README.md                        # Core subsystem overview
│   ├── SETUP.md                         # Detailed setup guide
│   └── QUICK_REFERENCE.md               # Command reference
│
├── pmt-mcp-servers-main/                # MCP server implementations
│   └── src/
│       ├── jira/                        # JIRA MCP server
│       ├── sharepoint/                  # SharePoint MCP server
│       ├── gerrit/                      # Gerrit MCP server
│       └── knowledge_graph/             # (Planned) KG MCP server
│
├── architecture.md                      # System architecture & data flow
├── PROJECT_SUBMISSION.md                # Project overview & business value
├── SETUP_CHECKLIST.md                   # Installation checklist
├── requirements.txt                     # Python dependencies
├── setup.sh                             # Automated setup script
└── README.md                            # This file
```

---

## 🎯 Business Value

### Time Savings

- **70-80% reduction** in context gathering time across JIRA, SharePoint, component docs
- **50-60% faster** root cause analysis through automated document retrieval
- **Immediate detection** of incomplete JIRA tickets before analysis begins

### Quality Improvement

- **Structured RCA reports** ensuring consistent analysis across Android layers
- **Mandatory approval gates** preventing incorrect or premature fixes
- **Specification-driven analysis** with automatic AIDL, SDD, and HMI doc retrieval

### Automation

- ✅ Automated JIRA ticket quality validation (24 criteria)
- ✅ Automated fix generation for Java, Kotlin, C++ (NDK), and AIDL
- ✅ Automated Gerrit push following AOSP contribution guidelines
- ✅ Automated log processing and prioritization

### Knowledge Management

- 📚 Component registry system with workspace-first documentation
- 🔍 (Planned) Historical bug pattern detection via knowledge graph
- 📝 Standardized documentation through ComponentSetup wizard

---

## 🛠️ Development

### Testing

```bash
# Test attachment processor
cd core/scripts
python3 test_processor.py

# Verify test workspace created
ls -la ../workspace/TEST-123/

# Clean up test data
rm -rf ../workspace/TEST-123/
```

### MCP Server Configuration

Edit `.vscode/mcp.json` to configure server connections:

```json
{
  "mcpServers": {
    "jira-python-mcp-server": {
      "command": "/path/to/uv",
      "args": ["--directory", "/path/to/pmt-mcp-servers-main/src/jira", "run", "jira-python-mcp-server"],
      "env": {
        "JIRA_URL": "https://your-jira.atlassian.net",
        "JIRA_TOKEN": "your-personal-access-token"
      }
    }
  }
}
```

See [core/SETUP.md](core/SETUP.md) for complete configuration guide.

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [README.md](README.md) | This file - project overview |
| [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) | Step-by-step installation checklist |
| [core/SETUP.md](core/SETUP.md) | Detailed setup with troubleshooting |
| [core/QUICK_REFERENCE.md](core/QUICK_REFERENCE.md) | Command reference & patterns |
| [architecture.md](architecture.md) | System architecture & data flow |
| [PROJECT_SUBMISSION.md](PROJECT_SUBMISSION.md) | Business value & objectives |
| [core/scripts/README.md](core/scripts/README.md) | Script documentation |
| [core/docs/DESIGN_RATIONALE_MARKDOWN_REGISTRY.md](core/docs/DESIGN_RATIONALE_MARKDOWN_REGISTRY.md) | Component registry design |

---

## 🔧 Troubleshooting

### MCP Servers Not Starting

1. Check VS Code Output panel → Select "MCP"
2. Verify `uv` path: `which uv`
3. Verify absolute paths in `.vscode/mcp.json`
4. Test server manually:
   ```bash
   cd pmt-mcp-servers-main/src/jira
   uv sync
   uv run jira-python-mcp-server
   ```

### Agents Not Visible

1. Enable custom agents in VS Code settings:
   ```json
   {
     "chat.agent.enabled": true
   }
   ```
2. Verify agent files exist: `ls .github/agents/*.agent.md`
3. Restart VS Code

### Component Not Found

If BugAnalyst reports "Component not registered":

1. Open Copilot Chat
2. Select `@ComponentSetup`
3. Type: `start`
4. Register the component following the wizard
5. Re-run Autodev for the JIRA issue

See [core/SETUP.md#troubleshooting](core/SETUP.md#troubleshooting) for more solutions.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Read the [architecture.md](architecture.md) to understand the system
2. Check existing [issues](../../issues) or create a new one
3. Follow the existing code style and agent patterns
4. Test your changes with real JIRA tickets
5. Update documentation as needed

---

## 📄 License

[MIT License](LICENSE) - See LICENSE file for details

---

## 🙏 Acknowledgments

Built with:
- [GitHub Copilot](https://github.com/features/copilot) (Claude Sonnet 4.5)
- [Model Context Protocol (MCP)](https://github.com/anthropics/mcp)
- Python MCP servers (jira-python-mcp, sharepoint-mcp, gerrit-mcp)

For Android IVI teams building on **AOSP** and **Android Automotive OS (AAOS)**.

---

## 📞 Support

- 📖 Documentation: See [core/SETUP.md](core/SETUP.md) and [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- 🐛 Issues: [GitHub Issues](../../issues)
- 💬 Discussions: [GitHub Discussions](../../discussions)

---

**Ready to get started?** → See [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) ✅
