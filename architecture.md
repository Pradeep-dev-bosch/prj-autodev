# Autodev — System Architecture

## Overview

Autodev is a VS Code Copilot agent workflow that automates the full
bug-analysis-to-fix-to-history cycle for **Android IVI (In-Vehicle Infotainment)**
software teams building on AOSP / Android Automotive OS (AAOS).

### Target system: Android IVI Head Unit

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Android IVI Head Unit (SoC)                      │
├───────────────┬─────────────────┬───────────────────┬───────────────────┤
│  APPLICATIONS │    FRAMEWORK    │        HAL        │  KERNEL / DRIVER  │
│               │                 │                   │                   │
│  Media Player │  CarService     │  VehicleHAL       │  CAN / LIN driver │
│  Navigation   │  MediaSession   │  AudioHAL         │  GPU driver       │
│  Phone / BT   │  BluetoothSvc   │  GraphicsHAL      │  Display driver   │
│  Climate Ctrl │  InputService   │  CameraHAL        │  TouchScreen drv  │
│  Settings     │  WindowManager  │  SensorHAL        │  Wi-Fi / BT drv   │
│  Launcher     │  TelecomService │  GnssHAL          │                   │
├───────────────┴─────────────────┴───────────────────┴───────────────────┤
│  Android Binder IPC  │  HIDL / AIDL  │  VehicleHAL properties           │
├─────────────────────────────────────────────────────────────────────────┤
│  Linux Kernel (GKI)  │  CAN SocketCAN  │  USB / Ethernet                │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ Vehicle bus (CAN / LIN / Ethernet)
                    ┌──────────▼───────────┐
                    │   Gateway ECU /      │
                    │   Body Control Mod.  │
                    └──────────────────────┘

```

### Autodev Agent System inside VS Code

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                              VS Code  —  Agent Mode                                      │
│                                                                                          │
│   Developer types JIRA key  ──►  Autodev (Orchestrator)                                 │
│                                          │                                               │
│                                          ▼                                               │
│                        ┌──────────────────────────────────────────┐                      │
│                        │  InternalQualityCheckerAgent             │                      │
│                        │  [user-invocable: false]                 │                      │
│                        │                                          │                      │
│                        │  • Validate 24 JIRA ticket criteria      │                      │
│                        │  • Check attachments, test setup table   │                      │
│                        │  • Verify spec links, description fields │                      │
│                        │  • Labels: IQC_Pass / IQC_Fail           │                      │
│                        │  • ⛔ STOP pipeline if validation fails   │                      │
│                        └──────────────────────────────────────────┘                      │
│                                          │                                               │
│                                          │ (only if IQC_Pass)                            │
│              ┌───────────────────────────┼───────────────────────┐                       │
│              │                           │                       │                       │
│              ▼                           ▼                       ▼                       │
│   ┌─────────────────────┐   ┌─────────────────────┐   ┌──────────────────────┐          │
│   │     BugAnalyst      │   │    FixGenerator      │   │      KGUpdater       │          │
│   │                     │   │                      │   │  [PLANNED / disabled]│          │
│   │ 1. Check local docs │   │ 1. Load workspace    │   │                      │          │
│   │    core/docs/       │   │    paths from        │   │ • store_bug_analysis │          │
│   │    components/      │   │    component-info.md │   │ • update_fix_status  │          │
│   │ 2. Browse workspace │   │ 2. Read source files │   │ • close JIRA ticket  │          │
│   │    source files     │   │    (AIDL/Java/C++)   │   │                      │          │
│   │    (AIDL/Java/C++)  │   │ 3. Write fix plan    │   └──────────────────────┘          │
│   │ 3. Query SharePoint │   │ 4. Apply fix  ⛔     │                                     │
│   │ 4. Query JIRA logs  │   │ 5. Push to Gerrit ⛔ │                                     │
│   │ 5. Write RCA  ⛔    │   │ 6. Update JIRA       │                                     │
│   │ 6. Post to JIRA     │   │                      │                                     │
│   └─────────────────────┘   └─────────────────────┘                                     │
│                                                                                          │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─  MCP Tool Layer  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─            │
│                                                                                          │
│  ┌──────────────┐  ┌──────────────────┐  ┌──────────────┐  ┌────────────────┐           │
│  │   JIRA MCP   │  │  SharePoint MCP  │  │  Gerrit MCP  │  │  KG MCP        │           │
│  │              │  │                  │  │              │  │  [PLANNED]     │           │
│  │ • fetch      │  │ • API specs      │  │ • push fix   │  │                │           │
│  │ • comment    │  │ • SDD / CID      │  │ • get change │  │ • store RCA    │           │
│  │ • transition │  │ • HMI docs       │  │   ID / URL   │  │ • query hist.  │           │
│  │ • labels     │  │                  │  │              │  │                │           │
│  └──────────────┘  └──────────────────┘  └──────────────┘  └────────────────┘           │
│                                                                                          │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─  Local Component Registry (workspace-first) ─ ─ ─ ─ ─ ─ ─           │
│                                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────────┐           │
│  │  core/docs/components/<slug>/                                            │           │
│  │                                                                          │           │
│  │  component-info.md  — layer types, workspace paths, AOSP paths,         │           │
│  │                        AIDL interfaces, logcat tags, error handling      │           │
│  │  component-flow.md  — ASCII layer diagram, interface map, adb commands  │           │
│  │                                                                          │           │
│  │  ► Populated by ComponentSetup (chat wizard — no terminal needed)       │           │
│  │  ► Read by BugAnalyst BEFORE SharePoint on every ticket analysis        │           │
│  │  ► Read by FixGenerator to locate and edit workspace source files       │           │
│  └──────────────────────────────────────────────────────────────────────────┘           │
└──────────────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

### Prerequisites: Component Registration (one-time setup)

Before analysing any JIRA tickets, run the **ComponentSetup** wizard for each IVI component:

```
1. USER: Open Copilot Chat → select ComponentSetup agent → type "start"
        │
        ▼
2. AGENT: 5-phase interview in chat (no terminal, no scripts):
          Phase 1: Component name, IVI domain, JIRA tag, owner, safety
          Phase 2: Layer flow (HMI → Service → HAL → Kernel) + per-layer details
                   • Workspace path (for direct file access in VS Code)
                   • AOSP/Gerrit repo path (for Gerrit pushes)
                   • Logcat tag, language, description
                   • Validates workspace paths using read tool
          Phase 3: Interface contracts (AIDL/HIDL/Binder/JNI) per boundary
          Phase 4: Gerrit URL, SharePoint folder, error handling, known issues
          Phase 5: Summary approval gate → writes files
        │
        ▼
3. FILES WRITTEN:
   • core/docs/components/<component-slug>/component-info.md
     (identity, architecture, interfaces, workspace paths, known issues)
   • core/docs/components/<component-slug>/component-flow.md
     (ASCII layer diagram + interface map + logcat tags)
        │
        ▼
   ✓ BugAnalyst and FixGenerator now have rich local context for this component.
```

### Main Workflow: Bug Analysis → Fix → Push

```
1. USER: "Analyse PROJ-123"
        │
        ▼
2. JIRA MCP:  jira_request(jql="key=PROJ-123")
        │     → summary, description, components, priority
        │
        ▼
   [Step 0] Quality Validation (InternalQualityCheckerAgent - Internal-only):
        │     • Validate 24 JIRA ticket criteria:
        │       - 3 attachment checks (exists, not empty, ForCustomer naming)
        │       - 8 basic fields (Summary, Defect Occurrence, Frequency, Severity, Carline, Variants, Region)
        │       - 4 Test Setup table checks (exists, all 17 required fields, no empty cells, no placeholders)
        │       - 6 description sections (Pre-condition, Action, Observation, Expected, Healing, Impact)
        │       - 4 spec references (Bosch Spec Link, Sheet Name, Cell No, Spec Screenshot)
        │     • Decision:
        │       - ALL PASS → Add IQC_Pass label, proceed to Step 2a
        │       - ANY FAIL → Add IQC_Fail label, post failed checks to JIRA, ⛔ STOP PIPELINE
        │     • user-invocable: false (only Autodev orchestrator can call)
        │
        ▼  (only if IQC_Pass)
   [Step 2a] Check local component docs:
        │     • Derive component slug from JIRA component field
        │     • Read core/docs/components/<slug>/component-info.md
        │     • Read core/docs/components/<slug>/component-flow.md
        │     → architecture, workspace paths, interfaces, logcat tags
        │
        ▼
   [Step 2b] Browse workspace source files:
        │     • Use workspace paths from component-info.md
        │     • Read .aidl, .java, .kt, .cpp files directly from VS Code workspace
        │     • Extract real interface contracts and service entry points
        │     → code evidence for RCA hypotheses
        │
        ▼
   [PLANNED] KG MCP: query_similar_issues()
        │     → disabled — knowledge graph not yet deployed
        │
        ▼
3. SharePoint: search_sharepoint(component/keywords)
              read_file_content(relevant docs)
        │     → API spec sections, SW design, component interfaces
        │     (supplements local docs if found; primary if local docs missing)
        │
        ▼
4. AGENT:     produce RCA(Root Cause Analysis)  ──►  RCA APPROVAL GATE ⛔ (user: yes / no / edit)
        │
        ▼  (approved)
5. JIRA MCP:  add_issue_comment(issue_key, root_cause_text)
        │     transition_issue → "In Analysis"
        │
        ▼
6. AGENT:     produce Component Fix Summary + Fix Plan
              • Uses workspace paths from component-info.md to navigate directly to source files
              • Reads target files before writing fixes
              ──►  FIX APPROVAL GATE ⛔ (user: yes / no / edit)
        │
        ▼  (approved)
7. AGENT:     apply code changes in workspace
        │     (using workspace paths — edits happen in open VS Code files)
        │
        ▼
8. Gerrit MCP: push_to_gerrit(repo_path, branch, topic=PROJ-123)
        │      → change URL, change ID
        │
        ▼
9. JIRA MCP:  add_issue_comment(gerrit change link + closure summary)

   [PLANNED] Step 10: KG MCP: store_bug_analysis() — disabled
   [PLANNED] Step 11: After merge — KG MCP: update_fix_status() — disabled
```

---

## Component Documentation System

Autodev uses a **workspace-first documentation model** — component architecture, source paths, and interface contracts are registered locally in the VS Code workspace before any JIRA analysis begins. This gives BugAnalyst and FixGenerator precise, verified context about the codebase they're working with.

### Structure

```
core/docs/components/                    ← Local component registry
├── dtv-service/
│   ├── component-info.md                ← Identity, architecture, workspace paths, interfaces
│   └── component-flow.md                ← ASCII layer diagram + logcat tags
├── media-input-service/
│   ├── component-info.md
│   └── component-flow.md
└── audio-hal/
    ├── component-info.md
    └── component-flow.md
```

### Key Data Stored

| Field | Purpose | Used By |
|-------|---------|---------|
| **Workspace paths** | Absolute or repo-relative path to source in open VS Code workspace | BugAnalyst (reads source), FixGenerator (edits source) |
| **AOSP/Gerrit repo path** | Path inside AOSP tree (for Gerrit pushes) | FixGenerator (Gerrit push), copilot-instructions |
| **Logcat tags** | Per-layer Android logcat tag | BugAnalyst (log filtering), attachment processor |
| **Interface contracts** | AIDL/HIDL/Binder/JNI interface names + descriptions per boundary | BugAnalyst (RCA), FixGenerator (backward compat check) |
| **Layer flow** | HMI → Service → HAL → Kernel | BugAnalyst (layer boundary identification) |
| **Error handling strategy** | How each layer handles RemoteException, HAL failures, ANR | BugAnalyst (failure mode analysis) |
| **Known issues** | Open bugs, constraints | BugAnalyst (avoids false positives) |

### How It Works

1. **Registration** — User runs `ComponentSetup` wizard in chat → answers 5 phases of questions → wizard validates workspace paths using VS Code's `read` tool → writes both markdown files.

2. **Lookup** — When BugAnalyst receives a JIRA issue:
   - Derives component slug from JIRA "Components" field (e.g. "DTV Service" → `dtv-service`)
   - Checks if `core/docs/components/dtv-service/component-info.md` exists
   - **If found** → reads it, extracts workspace paths table, browses real source files
   - **If not found** → falls back to SharePoint only (less context)

3. **Source browsing** — BugAnalyst reads up to 3 key files per layer:
   - AIDL interface definitions (`.aidl`) — reveals IPC contracts
   - Service/HAL entry point (`.java`, `.kt`, `.cpp`) — main implementation
   - Manager/client class — consumer side
   
   This provides **code evidence** cited directly in the RCA.

4. **Fix navigation** — FixGenerator uses workspace paths to:
   - Navigate directly to the affected layer's source directory
   - Read the exact files needing modification
   - Apply edits in place (VS Code workspace files are modified)
   - Push to Gerrit using the AOSP/Gerrit repo path

### Why Two Paths?

- **Workspace path** — where the code lives *right now* in the developer's machine (may be a non-standard checkout, vendor overlay, or work-in-progress branch).
- **AOSP/Gerrit path** — canonical AOSP tree location for Gerrit pushes and cross-repo references.

They're often the same (e.g. `packages/apps/DTVApp/`), but may differ if the workspace uses symlinks, vendor-specific folder structures, or out-of-tree builds.

---

## IVI-Specific Bug Categories

BugAnalyst is tuned to recognise the following Android IVI bug patterns:

| Category | Indicators | Android Layer |
|----------|------------|---------------|
| **ANR** | `Input dispatching timed out`, `/data/anr/anr_*.txt` | App / Framework |
| **App crash (Java)** | `FATAL EXCEPTION`, `java.lang.NullPointerException` | App |
| **Native crash** | `tombstone_*`, `signal 11 (SIGSEGV)` | NDK / HAL |
| **HAL failure** | `HIDL call failed`, `VehicleHal error` | HAL |
| **Binder failure** | `DeadObjectException`, `RemoteException` | Framework / HAL |
| **Audio glitch** | `AudioFlinger`, `underrun`, `overrun` | AudioHAL / Framework |
| **Display / GPU** | `SurfaceFlinger`, `GPU fault`, `jank` | GraphicsHAL / Framework |
| **Vehicle signal** | `CarPropertyManager error`, `VHAL timeout` | VehicleHAL / CarService |
| **Boot / init** | `init: Service ... died`, `Zygote restart` | Kernel / init |
| **Memory pressure** | `Low on memory`, `LMK killed`, `OOM` | Kernel / Framework |
| **Connectivity** | `Bluetooth stack error`, `Wi-Fi supplicant` | BT/Wi-Fi driver |

## Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **ComponentSetup** | **Chat wizard for registering IVI components** — collects layer flow, workspace paths, AIDL/HIDL interfaces, logcat tags; validates workspace paths; writes `core/docs/components/<slug>/` markdown files |
| **InternalQualityCheckerAgent** | **JIRA ticket quality validation (Step 0)** — validates 24 criteria (attachments, test setup table, description sections, spec links, basic fields); labels as IQC_Pass/IQC_Fail; **stops pipeline if validation fails**; `user-invocable: false` (internal-only, orchestrator access only); supports single-ticket mode (Autodev) and batch mode (standalone) |
| JIRA MCP | Issue retrieval, status updates, comment posting, label management |
| SharePoint MCP | SDD, AIDL API specs, HMI design docs, component info sheets |
| Gerrit MCP | AOSP / AAOS code review push, change tracking |
| Knowledge Graph MCP | *(planned feature — not yet deployed)* Persistent bug/fix history |
| Autodev Orchestrator | Pipeline coordination, 4-step status board, quality gate enforcement, exception handling |
| **BugAnalyst** | Root cause analysis using **local component docs (workspace-first)**, workspace source file browsing (AIDL/Java/Kotlin/C++), logcat, tombstones, VHAL traces, SharePoint docs |
| **FixGenerator** | Code fix (Java/Kotlin/C++ NDK), uses workspace paths for direct file navigation, approval gates, Gerrit push |
| KGUpdater | *(planned feature — not yet active)* KG persistence, JIRA closure |

## Security Notes

- All credentials are injected via environment variables and VS Code `${input:...}` prompts — never stored in files.
- Gerrit push requires a valid git remote with SSH key or HTTP credentials configured for the AOSP/AAOS repo.
- The knowledge graph stores no passwords; only bug analysis text and IDs. *(planned feature — not yet deployed)*
- SharePoint access uses NTLM/OAuth authentication (on-premise / M365).
- ADB access to production vehicle head units must follow the OEM security policy — never enable ADB on a production build.

---

## Architecture Principles

### Component Registry Pattern
- **ComponentSetup** (one-time): Fetches SharePoint docs → stores locally in `core/docs/components/<slug>/source-documents/`
- **BugAnalyst** (every run): Reads from local registry only, never calls SharePoint
- **Result**: No duplicate API calls, faster analysis (local filesystem vs network)

### Scripts vs Agents
- **Scripts** (`core/scripts/`): Business logic (extraction, classification) — standalone, testable, CLI-enabled
- **Agents** (`.github/agents/`): Orchestration only — call tools + scripts, no embedded logic
- **Result**: Single source of truth, unit-testable code, no duplication

### Tool Access Control
- **ComponentSetup**: Only agent with SharePoint tools in YAML `tools:` list
- **BugAnalyst**: JIRA + filesystem tools only (no SharePoint)
- **FixGenerator**: JIRA + filesystem + Gerrit tools (no SharePoint)
- **Result**: Clear boundaries, impossible to accidentally duplicate fetches
