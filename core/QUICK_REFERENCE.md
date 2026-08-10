# Autodev Quick Reference

## Quick Setup

```bash
# From Autodev root directory
./setup.sh  # Installs Python dependencies (python-docx)
```

**Dependencies:**
- `python-docx` — Document conversion for ComponentSetup
- Optional: `poppler-utils` — PDF support

---

## Directory Structure

```
Autodev/
├── setup.sh                             # Quick Python dependency installer
├── requirements.txt                     # Python dependencies
├── .github/
│   ├── agents/                          # Custom agent definitions
│   │   ├── Autodev.agent.md             # Orchestrator (user-facing)
│   │   ├── BugAnalyst.agent.md          # RCA + log analysis
│   │   ├── FixGenerator.agent.md        # Code fix + Gerrit push
│   │   ├── ComponentSetup.agent.md      # Component registration wizard
│   │   └── KGUpdater.agent.md           # KG persistence (planned)
│   └── copilot-instructions.md          # Workspace instructions
├── scripts/
│   ├── convert_docx_enhanced.py         # DOCX → Markdown (python-docx)
│   ├── extract_docx_to_md.py           # DOCX → Markdown (standard lib)
│   ├── extract_pdf_to_md.py            # PDF → Markdown
│   ├── process_jira_attachments.py     # Attachment processor
│   ├── test_processor.py               # Test script with sample data
│   └── README.md                       # Scripts documentation
├── workspace/                           # Auto-created per JIRA issue
│   └── <ISSUE_KEY>/
│       ├── attachments/                # Raw JIRA files
│       ├── extracted/                  # Unzipped archives
│       └── logs/                       # Organized logs
│           ├── logcat/                 # Android system logs
│           ├── tombstones/             # Native crashes
│           ├── anr/                    # ANR traces
│           └── system/                 # Kernel/bugreport
└── docs/
    ├── components/                      # Registered IVI components
    │   └── <component-slug>/
    │       ├── source-documents/        # Design docs (SWDD, SDD, CID)
    │       ├── component-info.md        # Full component metadata
    │       └── component-flow.md        # Architecture layer diagram
    ├── component-info-template.md       # Component doc template
    └── kg-schema.ttl                    # Knowledge graph ontology

architecture.md (root)                   # System design
```

## Common Commands

### Test Processor

```bash
# Test with sample data
python3 scripts/test_processor.py

# Cleanup test data
rm -rf workspace/TEST-123/
```

### Running Autodev

1. Open VS Code in the workspace root:
   ```bash
   code /path/to/Autodev
   ```

2. Open Copilot Chat (`Ctrl+Alt+I`)

3. Select **Autodev** agent from picker

4. Enter JIRA issue key when prompted (e.g., `PROJ-1234`)

5. Follow the workflow:
   - Review RCA → Approve/Reject
   - Review Fix Plan → Approve/Reject
   - Review Gerrit Push → Approve/Reject

### Manual Attachment Processing

```python
from Autodev.scripts.process_jira_attachments import JiraAttachmentProcessor

# Initialize processor
processor = JiraAttachmentProcessor("workspace", "PROJ-1234")

# Process attachments (from JIRA MCP)
summary = processor.process_attachments(attachment_files)

# Get priority logs
logs = processor.get_priority_logs()

# Cleanup
processor.cleanup()
```

## Log Analysis Priority

When analyzing Android IVI bugs, read logs in this order:

1. **ANR traces** (`logs/anr/`)
   - Main thread blocked
   - Input dispatch timeout
   - Binder timeout

2. **Tombstones** (`logs/tombstones/`)
   - Native crashes (SIGSEGV, SIGABRT)
   - Stack traces for C/C++ code
   - Signal information

3. **Logcat** (`logs/logcat/`)
   - Java/Kotlin exceptions
   - Binder errors
   - VHAL timeouts
   - Service crashes

4. **System logs** (`logs/system/`)
   - Kernel messages (dmesg)
   - Bugreport dumps
   - Dumpsys output
   - Init failures

## Key Log Patterns

### ANR Detection
```
ANR in <package> (<activity>)
PID: <pid>
Reason: Input dispatching timed out
```

### Native Crash
```
signal 11 (SIGSEGV), code 1 (SEGV_MAPERR)
Build fingerprint: Android/aosp_car/...
Cmdline: /system/bin/<service>
```

### Java Crash
```
FATAL EXCEPTION: main
Process: <package>, PID: <pid>
java.lang.NullPointerException
    at <class>.<method>(<file>:<line>)
```

### Binder Failure
```
E Binder  : DeadObjectException
E ServiceManager: Cannot find service: <service_name>
```

### VHAL Timeout
```
E VehicleHal: Property <property_id> get/set timeout
E CarService: VHAL connection lost
```

## MCP Servers

| Server | Purpose | Status |
|--------|---------|--------|
| JIRA | Fetch issues, post comments, transition tickets | ✅ Active |
| SharePoint | Search/read API specs, SDD, HMI docs | ✅ Active |
| Gerrit | Push code, query changes | ✅ Active |
| Bug-KG | Store/query historical bug analysis | 🔜 Planned |

## Agent Handoffs

```
User input (JIRA key)
        ↓
  Autodev (orchestrator)
        ↓
  BugAnalyst (fetch + analyze + RCA)
        ↓
  User approval ⛔
        ↓
  BugAnalyst → posts to JIRA
        ↓
  FixGenerator (plan + apply + push)
        ↓
  User approval ⛔
        ↓
  FixGenerator → pushes to Gerrit
        ↓
  KGUpdater (store in knowledge graph) [planned]
```

## Approval Gates

Autodev has **3 mandatory approval gates**:

1. **RCA Approval** (BugAnalyst)
   - Review root cause analysis before posting to JIRA
   - Options: `yes` / `no` / `edit`

2. **Fix Approval** (FixGenerator)
   - Review code changes before applying to workspace
   - Options: `yes` / `no` / `edit`

3. **Gerrit Push Approval** (FixGenerator)
   - Confirm before pushing to Gerrit for review
   - Options: `yes` / `no` / `edit`

## Troubleshooting

### MCP Server Not Starting

Check `.vscode/mcp.json`:
- Correct `cwd` paths (absolute paths required)
- Valid credentials (tokens/passwords prompted at runtime)
- `uv` installed and in PATH

### Attachment Processor Fails

```bash
# Test manually
python3 scripts/process_jira_attachments.py workspace TEST-123

# Check Python version
python3 --version  # Need ≥ 3.7

# Verify workspace permissions
ls -la workspace/
```

### Agent Not Visible in Picker

1. Check `.github/agents/*.agent.md` files exist
2. Verify YAML frontmatter syntax (no tabs, proper quotes)
3. Reload VS Code: `Ctrl+Shift+P` → `Developer: Reload Window`
4. Check `chat.agent.enabled: true` in VS Code settings

### Logs Not Classified Correctly

Edit `scripts/process_jira_attachments.py`:
- Update `LOG_PATTERNS` dictionary
- Add new filename patterns
- Adjust content detection regex

## Resources

- [Architecture Documentation](../architecture.md)
- [Scripts README](scripts/README.md)
- [Workspace Guide](workspace/README.md)
- [MCP Servers](../pmt-mcp-servers-main/)
