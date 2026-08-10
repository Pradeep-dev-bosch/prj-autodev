# Autodev - Project Submission Documentation

## Problem Statement & System Architecture

### Agent / Workflow Objective
**What problem are we trying to solve?**

Android IVI (In-Vehicle Infotainment) teams face several critical challenges in bug resolution:
- **Time-consuming manual root cause analysis** requiring investigation across multiple documentation sources (JIRA, SharePoint AIDL specs, SDD, HMI design docs)
- **Incomplete JIRA tickets** lacking critical test setup details, specifications, or evidence, causing analysis delays
- **Knowledge silos** where bug analysis insights are lost after resolution, leading to repeated investigations of similar issues
- **Manual context switching** between JIRA, SharePoint documentation, local component docs, and code repositories
- **Inconsistent fix quality** due to lack of structured analysis and approval workflows

**Solution:** Autodev is an AI-assisted bug resolution pipeline that automates JIRA ticket validation, root cause analysis with multi-source documentation retrieval, fix generation, and Gerrit integration following AOSP contribution guidelines.

---

### Business Value
**What improvement do we expect?**

**Time Savings:**
- **70-80% reduction** in time spent gathering context from JIRA, SharePoint, and component documentation
- **50-60% faster** root cause analysis through automated document retrieval and structured RCA templates
- **Immediate detection** of incomplete JIRA tickets (24 validation criteria) before analysis begins

**Quality Improvement:**
- **Structured RCA reports** ensuring consistent analysis across all Android layers (App, Framework, HAL, Kernel)
- **Mandatory approval gates** at RCA and fix stages preventing premature or incorrect fixes
- **Specification-driven analysis** with automatic retrieval of AIDL API specs, SDD, and HMI design documents

**Automation:**
- **Automated quality validation** of JIRA tickets (attachments, test setup, spec links, evidence)
- **Automated fix generation** with exact code changes in Java, Kotlin, C++ (NDK), or AIDL
- **Automated Gerrit push** following AOSP contribution guidelines

**Consistency:**
- **Knowledge graph persistence** (planned) storing historical bug patterns for similar issue detection
- **Component registration** via ComponentSetup wizard ensuring standardized documentation
- **Fail-fast quality gates** stopping invalid tickets before expensive analysis work

---

### System Block Diagram

**Pattern:** **Agentic Workflow** (Multi-agent orchestration with handoffs)

```
User provides JIRA key
        ↓
┌─────────────────────────────────────────────────────────┐
│  Autodev Orchestrator (Main Agent)                      │
│  • Validates input                                       │
│  • Tracks pipeline state                                │
│  • Delegates to sub-agents via handoffs                 │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  Step 0: InternalQualityCheckerAgent (Internal-only)    │
│  • Validates 24 JIRA ticket criteria                    │
│  • Checks attachments, test setup, spec links           │
│  • Labels: IQC_Pass / IQC_Fail                          │
│  • ⛔ STOP if validation fails                           │
└─────────────────────────────────────────────────────────┘
        ↓ (only if PASS)
┌─────────────────────────────────────────────────────────┐
│  Step 1: BugAnalyst                                      │
│  • Fetches JIRA ticket                                   │
│  • Retrieves SharePoint docs (AIDL, SDD, HMI, CID)      │
│  • Checks local component docs (core/docs/components/)  │
│  • Produces structured RCA report                        │
│  • ⛔ Approval gate: User must approve RCA               │
│  • Posts RCA to JIRA after approval                      │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: FixGenerator                                    │
│  • Generates fix plan (Java/Kotlin/C++/AIDL)            │
│  • ⛔ Approval gate: User must approve fix plan          │
│  • Applies code changes to workspace                     │
│  • Pushes to Gerrit following AOSP guidelines           │
│  • Posts closure comment to JIRA                         │
└─────────────────────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: KGUpdater (Planned Feature - Disabled)         │
│  • Stores analysis + fix in knowledge graph (Neo4j)      │
│  • Updates status when Gerrit change merges              │
└─────────────────────────────────────────────────────────┘
```

**Supporting Agent:**
- **ComponentSetup** - Interactive wizard for registering IVI components (DTV, MIS, Audio, etc.) with layer flow diagrams

---

**LLM Infra:** GitHub Copilot (Claude Sonnet 4.5)

**Tools/MCP Servers:**
- **JIRA** (jira-python-mcp-server) - Fetch tickets, add comments, transition status, manage labels
- **SharePoint** (sharepoint-mcp-server) - Search and retrieve AIDL specs, SDD, HMI docs, component info sheets
- **Gerrit** (gerrit-mcp-server) - Push code fixes for review, query existing AOSP/AAOS changes
- **Bug Knowledge Graph** (bug-knowledge-graph) - Planned: Store/query historical IVI bug analysis (Graphiti + Neo4j)

**Autonomy Level:** **Augment** (AI-assisted with mandatory human approval gates)
- Autonomous validation (Step 0)
- Human approval required at RCA stage (Step 1)
- Human approval required before code changes (Step 2)

**Workflow Trigger:** **Manual** (User provides JIRA issue key to Autodev orchestrator)

**Model Needed:** **Stronger Model (Claude Sonnet 4.5)**
- Complex reasoning required for root cause analysis across Android layers
- Multi-document synthesis from SharePoint, JIRA, local component docs
- Code generation in multiple languages (Java, Kotlin, C++, AIDL)

**Target Users:**
- **Developers** - Primary users for bug analysis and fix generation
- **Testers** - Can validate JIRA ticket quality before escalation
- **Managers** - Track pipeline progress via status boards

**Human Review Points:**
1. **After Step 0** - User notified if quality validation fails (ticket must be corrected)
2. **⛔ After RCA generation (Step 1)** - User must explicitly approve RCA before posting to JIRA
3. **⛔ After fix plan generation (Step 2)** - User must explicitly approve before code changes and Gerrit push
4. **Post-merge** - User confirms Gerrit merge for KG status update

**Others:**
- **Memory** - Session memory for in-progress analysis; Repository memory for component documentation
- **RAG** - SharePoint document retrieval based on component name and keywords from JIRA ticket
- **Local Knowledge Base** - Component docs stored in `core/docs/components/<slug>/` via ComponentSetup wizard

---

## Workflow Design Details

### Required Context / Data Sources

**System must reliably access:**

1. **JIRA Tickets (via jira-python-mcp-server)**
   - Issue summary, description, status, priority
   - Components, labels, fix version
   - Attachments (ForCustomer evidences, logs, screenshots)
   - Comments, reporter, assignee
   - Custom fields: Defect Occurrence, Frequency, Severity, Carline, Variants, Region

2. **SharePoint Documentation (via sharepoint-mcp-server)**
   - AIDL API specifications
   - Software Design Documents (SDD)
   - Component Interface Documents (CID)
   - HMI design specifications
   - Vehicle signal mapping documents (VHAL/CAN)
   - Architecture reference documents

3. **Local Component Documentation (workspace files)**
   - Component info files: `core/docs/components/<slug>/component-info.md`
   - Layer flow diagrams: `core/docs/components/<slug>/component-flow.md`
   - Registered via ComponentSetup agent

4. **Workspace Source Code (read-only for analysis)**
   - AIDL interface definitions
   - Java/Kotlin service implementations
   - C++ HAL implementations
   - Build configuration files

5. **Gerrit Repository (via gerrit-mcp-server)**
   - Existing AOSP/AAOS changes for reference
   - Code review history
   - Merge status tracking

6. **Bug Knowledge Graph (planned - currently disabled)**
   - Historical bug analysis records
   - Similar issue patterns
   - Component bug history

---

### Evaluation
**How will we measure success?**

**Quantitative Metrics:**
- **Time-to-RCA Reduction:** Measure average time from JIRA key input to approved RCA (target: 70-80% reduction)
- **Ticket Quality Improvement:** % of tickets passing IQC validation on first submission (target: >80% pass rate after 3 months)
- **Fix Accuracy Rate:** % of generated fixes merged without modification (target: >60%)
- **Context Retrieval Accuracy:** % of relevant SharePoint docs successfully retrieved (target: >90%)
- **Pipeline Completion Rate:** % of started analyses that reach Gerrit push (target: >70%)

**Qualitative Metrics:**
- **RCA Completeness:** Peer review of generated RCAs for Android layer coverage, spec citations, precision
- **User Satisfaction:** Developer feedback on RCA quality and fix relevance (survey after 1 month)
- **Knowledge Capture:** % of bugs with structured RCA in JIRA vs. ad-hoc comments (target: 100% for Autodev-processed issues)

**Operational Metrics:**
- **False Positive Rate (IQC):** % of tickets marked IQC_Fail that were actually complete (target: <5%)
- **Approval Gate Rejection Rate:** % of RCAs/fixes rejected by users (indicates AI quality)
- **Gerrit Push Success Rate:** % of pushes accepted by Gerrit without errors (target: >95%)

---

### Task Breakdown
**What are the major steps in the workflow?**

**Step 0: Pre-flight Check (Autodev Orchestrator)**
- Receive JIRA issue key from user
- Call `jira_request` to verify ticket exists
- Extract project, component, summary, status, priority
- Display 4-step pipeline status board

**Step 1: Quality Validation (InternalQualityCheckerAgent - Internal-only)**

**Agent Properties:**
- `user-invocable: false` — Cannot be called directly by users
- `model: Claude Sonnet 4.5` — Uses stronger model for validation
- Only invokable by Autodev orchestrator via handoff

**Automated 24-criteria validation:**

**Attachments (3 checks):**
  - ✓ Attachment file exists
  - ✓ Attachment file not empty
  - ✓ Any attachment file name starts with 'ForCustomer'

**Basic Fields (8 checks):**
  - ✓ Ticket Summary is readable and understandable
  - ✓ Defect Occurrence field updated
  - ✓ Frequency of Issue field updated
  - ✓ Severity updated
  - ✓ Carline field updated
  - ✓ Variants field updated
  - ✓ Region field updated

**Test Setup Details Table (4 checks):**
  - ✓ Table exists in description (Jira table format using | for cells with 2 columns)
  - ✓ First column cells contain ALL 17 required fields:
    - Test Name, HW Sample, Device Part Number, Display USED
    - Amplifier Connected, Test Type, Internal Version (SoC)
    - Version (Aurix), External Version, AASP Version
    - Carline, Region, MY, Variant, PD, CD
    - Devices Used (Mobile/iPod/USB), Connected External Components
  - ✓ Second column cells are NOT empty (no blank or whitespace-only cells)
  - ✓ Second column cells contain actual values (NOT placeholders like `<PLACEHOLDER>`, `<VALUE>`, `<PART NUMBER>`, `<INTERNAL VERSION>`, `<CARLINE>`, `<REGION>`)

**Description Sections (6 checks - must have content under each heading):**
  - ✓ Pre-condition: list of pre-condition text available
  - ✓ Action: list of Action text available
  - ✓ Observation: list of Observation text available
  - ✓ Expected: list of Expected text available
  - ✓ Healing: list of Healing text available
  - ✓ Impact to Customer: list of Impact text available

**Specification References (4 checks):**
  - ✓ Bosch Spec Link: any link available
  - ✓ Sheet Name: any text available
  - ✓ Cell No: any text available
  - ✓ Spec Screenshot: any image or text available

**Decision Rule:**
  - **IF all validations are TRUE:**
    - Remove `IQC_Open` label (if present)
    - Remove `forInternalQualityCheck` label (if present, batch mode only)
    - Add `IQC_Pass` label
    - Return: **"VALIDATION PASSED"** to orchestrator
    - Proceed to Step 2 (BugAnalyst)
  
  - **ELSE (any validation fails):**
    - Remove `IQC_Open` and `IQC_Reviewed` labels (if present)
    - Add `IQC_Fail` label
    - Post comment to JIRA: "IQC Failed" + "@" + ticket reporter + all failed checks (bullet list)
    - Return: **"VALIDATION FAILED"** to orchestrator with list of failed checks
    - **STOP pipeline** — user must correct ticket and re-run Autodev

**Operational Modes:**
  - **Mode 1 (Single Ticket):** Called by Autodev orchestrator for one specific JIRA key
  - **Mode 2 (Batch):** Standalone execution validating up to 50 tickets with brand/relevance filters, produces summary table

**Step 2: Root Cause Analysis (BugAnalyst)**
- Fetch full JIRA ticket details (description, attachments, comments)
- Derive component slug from JIRA Components field
- **Check local component docs:**
  - Read `core/docs/components/<slug>/component-info.md`
  - Read `core/docs/components/<slug>/component-flow.md`
  - Browse workspace source paths listed in component-info
- **Retrieve SharePoint documentation:**
  - Search SharePoint using component name + JIRA keywords
  - Download top 2-3 relevant docs (AIDL specs, SDD, HMI design)
- ~~**Query knowledge graph**~~ (planned feature - disabled)
- **Generate structured RCA:**
  - Symptom, Contributing Factors, Root Cause
  - Affected Component(s), Android layer identification
  - Proposed Fix Direction
  - Cite specific SharePoint doc sections
- **⛔ Approval Gate:** Present RCA to user, wait for explicit "yes" to proceed
- Post approved RCA to JIRA as comment
- Transition JIRA status (e.g., Open → In Analysis)

**Step 3: Fix Generation (FixGenerator)**
- **Generate detailed fix plan:**
  - Files to modify with specific line ranges
  - Exact code changes (diffs or full replacement blocks)
  - Test impact assessment
  - Risk assessment
- **⛔ Approval Gate:** Present fix plan to user, wait for explicit "yes" to proceed
- Apply code changes to workspace files
- Verify syntax and logical consistency
- **Push to Gerrit:**
  - Call `push_to_gerrit` with repo path, branch, topic (JIRA key), reviewers
  - Report Gerrit change URL
- Post closure comment to JIRA with Gerrit link

**Step 4: Knowledge Graph Update (KGUpdater - Planned, Disabled)**
- ~~Call `store_bug_analysis` with issue key, summary, root cause, component, affected files, fix description, Gerrit change ID~~
- ~~Update fix status when user reports Gerrit merge~~
- **Current behavior:** Skip KG storage, add JIRA comment noting KG feature is planned

**Supporting Workflow: Component Registration (ComponentSetup)**
- 5-phase chat interview:
  1. Component name & IVI domain
  2. Layer flow (HMI → Service → HAL → Kernel)
  3. Per-layer details (class names, AIDL, logcat tags)
  4. Interface contracts between layers
  5. Confirmation & file generation
- Writes `core/docs/components/<slug>/component-info.md` and `component-flow.md`

---

## Reliability and Guardrails

### Worst Case Failure
**If the system fails, what is the worst thing that could happen?**

**Catastrophic Failure Scenarios (Prevented by Guardrails):**

1. **❌ Incorrect Fix Pushed to Production Code**
   - **Impact:** Broken build, regression bugs, customer-facing failures
   - **Mitigation:** 
     - ⛔ **Mandatory approval gate** before any code changes
     - **Gerrit code review** required before merge
     - User explicitly confirms fix plan before application
     - No automatic merge - all changes go through standard Gerrit review flow

2. **❌ Sensitive Data Leaked to JIRA Comments**
   - **Impact:** Credentials, tokens, internal URLs exposed publicly
   - **Mitigation:**
     - RCA approval gate lets user review before posting
     - No credentials stored in code or templates
     - User confirms all JIRA posts before submission

3. **❌ Valid JIRA Tickets Blocked by False IQC Failures**
   - **Impact:** Development delays, frustrated users
   - **Mitigation:**
     - Clear, actionable IQC failure messages listing specific missing fields
     - Users can override by manually completing ticket and re-running
     - IQC criteria based on documented requirements, not subjective judgment

4. **❌ Incorrect Root Cause Analysis Misleading Debugging**
   - **Impact:** Wasted time fixing wrong component, delayed resolution
   - **Mitigation:**
     - ⛔ **Mandatory user approval** before RCA is posted to JIRA
     - User reviews RCA for accuracy before approval
     - Citations to SharePoint docs allow verification

**Realistic Failure Modes (Graceful Degradation):**

- **SharePoint retrieval fails:** BugAnalyst notes missing docs, proceeds with available context (JIRA + local component docs)
- **JIRA API timeout:** Error displayed to user, retry suggested
- **Gerrit push fails:** Error message shown, fix preserved in workspace for manual push
- **Invalid code generated:** Syntax validation detects errors pre-push, user rejects fix plan

---

### Guardrails
**Are there actions that must always require confirmation or should never happen automatically?**

**⛔ Mandatory Confirmation (Never Automatic):**

1. **Posting RCA to JIRA**
   - BugAnalyst must get explicit "yes" from user before `add_issue_comment`
   - User reviews full RCA text before posting
   - Once posted, RCA becomes part of official ticket record

2. **Applying Code Changes**
   - FixGenerator must get explicit "yes" before modifying workspace files
   - User reviews exact file paths and code diffs
   - No code changes without approval

3. **Pushing to Gerrit**
   - Included in fix plan approval (Step 2 approval gate)
   - User confirms before `push_to_gerrit` tool is called
   - Gerrit change URL reported after successful push

4. **JIRA Ticket Transitions**
   - Automated transitions (Open → In Analysis) happen only after RCA approval
   - Critical transitions (e.g., resolving) require manual user action

**🚫 Actions Never Performed Automatically:**

- **Merging Gerrit changes** - Always requires manual code review approval
- **Deleting JIRA tickets or comments** - Read-only for most operations
- **Modifying production code paths** - All changes go through Gerrit review
- **Accessing credentials or secrets** - MCP servers use environment variable auth, never hardcoded
- **Bypassing approval gates** - No auto-approve logic exists in any agent

**🔒 Internal-Only Actions (User Cannot Trigger):**

- **InternalQualityCheckerAgent invocation** - Marked `user-invocable: false`, only Autodev orchestrator can call
- Prevents users from skipping quality validation or manipulating IQC results

---

### Failure Detection
**If the system produces bad output, how will users detect it quickly?**

**Immediate Detection Mechanisms:**

1. **RCA Approval Gate (Step 1)**
   - User sees **full RCA text** before it's posted to JIRA
   - Can immediately identify incorrect Android layer, wrong component, missing citations
   - Can reject with "no" or request revisions with "edit"
   - **Detection time:** <1 minute

2. **Fix Plan Approval Gate (Step 2)**
   - User sees **exact code changes** with file paths and line numbers
   - Can verify changes match RCA analysis
   - Can detect incorrect logic, wrong files, syntax errors
   - **Detection time:** <2 minutes

3. **Syntax Validation (Step 2)**
   - FixGenerator runs syntax checks before presenting fix plan
   - Java/Kotlin/C++ compilation errors caught pre-push
   - **Detection time:** Immediate (before user approval)

4. **Gerrit Code Review**
   - All pushed changes visible in Gerrit UI
   - Team members review before merge
   - CI/CD tests run on Gerrit patchsets
   - **Detection time:** Minutes to hours (standard review cycle)

**Post-Execution Detection:**

5. **JIRA Comment Review**
   - Posted RCAs visible in JIRA ticket comments
   - Team members can flag incorrect analysis in replies
   - Reporter can verify against actual observed behavior
   - **Detection time:** Hours to days

6. **Build Failures**
   - If fix breaks compilation, CI rejects Gerrit change
   - Developer notified immediately
   - **Detection time:** Minutes (CI build time)

7. **Regression Testing**
   - Automated tests catch functional regressions
   - QA validates fix against original symptom
   - **Detection time:** Days (test cycle)

**User Feedback Channels:**

- **Approval rejection** - User clicks "no" at either gate → workflow stops
- **JIRA comments** - User or team flags incorrect RCA/fix in ticket
- **Gerrit comments** - Reviewers request changes or reject patchset
- **Session memory** - User can document issues for future improvement

**Quality Indicators:**

- **SharePoint doc retrieval count** - If 0 docs retrieved, RCA may lack spec citations
- **Component doc availability** - Warning if local component docs missing
- **Citation presence** - RCA without SharePoint citations flagged in approval view
- **Risk assessment** - Fix plan includes explicit risk section for user review

**Rollback/Recovery:**

- **RCA rejection:** User declines approval → nothing posted to JIRA, no state change
- **Fix rejection:** User declines fix approval → no code changes, workspace pristine
- **Bad Gerrit push:** User can abandon Gerrit change via Gerrit UI
- **Wrong JIRA comment:** Cannot auto-delete, but user can post correction comment

---

## Repository

**GitHub:** https://github.com/qsd1kor_bosch/prj_autodev

**Technology Stack:**
- GitHub Copilot Chat + Custom Agents (.agent.md files)
- MCP (Model Context Protocol) servers
- Python-based MCP integrations
- JIRA, SharePoint, Gerrit APIs
- Neo4j (planned for knowledge graph)

**Key Files:**
- `.github/agents/Autodev.agent.md` - Main orchestrator
- `.github/agents/InternalQualityCheckerAgent.agent.md` - JIRA validation (internal-only)
- `.github/agents/BugAnalyst.agent.md` - Root cause analysis
- `.github/agents/FixGenerator.agent.md` - Fix generation & Gerrit push
- `.github/agents/ComponentSetup.agent.md` - Component registration wizard
- `.github/agents/KGUpdater.agent.md` - Knowledge graph persistence (planned)
- `.github/copilot-instructions.md` - Global instructions for all agents
