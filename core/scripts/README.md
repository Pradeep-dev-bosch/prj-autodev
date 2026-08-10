# Autodev Scripts

This directory contains automation scripts for the Autodev workflow.

---

## Document Conversion Scripts

### convert_docx_enhanced.py

**Purpose:** Convert Word (.docx) files to Markdown format for ComponentSetup wizard.

**Features:**
- Extracts text, headings, paragraphs, lists, and tables
- Preserves document structure and basic formatting
- Generates clean Markdown for easy parsing by BugAnalyst

**Dependencies:**
- `python-docx` (install: `pip3 install --user python-docx`)
- Or run: `./setup.sh` from Autodev root

**Usage:**

```bash
python3 convert_docx_enhanced.py input.docx output.md

# Example:
python3 convert_docx_enhanced.py SWCDD_DTV.docx SWCDD_DTV.md
```

**Used by:** ComponentSetup agent (automatic during upload method)

---

### extract_docx_to_md.py

**Purpose:** Fallback DOCX converter using Python standard library only (no dependencies).

**Features:**
- Zero external dependencies — uses built-in `zipfile` and `xml.etree`
- Extracts text by parsing internal DOCX XML structure
- Suitable for simple documents

**Usage:**

```bash
python3 extract_docx_to_md.py input.docx output.md
```

**When to use:** If `python-docx` is not available or cannot be installed.

---

### extract_pdf_to_md.py

**Purpose:** Extract text from PDF files and save as Markdown.

**Dependencies:**
- `pdftotext` (poppler-utils): `sudo apt-get install poppler-utils`

**Usage:**

```bash
python3 extract_pdf_to_md.py input.pdf output.md
```

---

## JIRA Attachment Processing

## process_jira_attachments.py

**Purpose:** Automatically download, extract, and organize JIRA attachments (logs, crash dumps, etc.) for root cause analysis.

### Features

- Downloads JIRA attachments via MCP `get_issue_attachments`
- Extracts compressed archives (`.zip`, `.tar`, `.gz`, `.tgz`, `.bz2`)
- Classifies log files by type using filename patterns and content analysis
- Organizes logs into categorized directories for efficient analysis

### Log Categories

| Category | File Patterns | Purpose |
|----------|--------------|---------|
| `logcat` | `*logcat*.txt`, `*main.log`, `*system.log`, `*crash.log` | Android system logs, app logs |
| `tombstones` | `*tombstone*`, `*crash_dump*`, `*native_crash*` | Native crash dumps (C/C++) |
| `anr` | `*anr*.txt`, `*traces*.txt`, `*ANR*` | ANR traces (main thread blocked) |
| `system` | `*dmesg*`, `*kernel*.log`, `*bugreport*.txt`, `*dumpsys*.txt` | Kernel logs, system dumps |

### Directory Structure

After processing JIRA issue `PROJ-1234`:

```
Autodev/workspace/PROJ-1234/
├── attachments/          # Raw files from JIRA
│   ├── logs.zip
│   └── screenshot.png
├── extracted/            # Extracted from archives
│   └── logs/
│       ├── logcat.txt
│       ├── tombstone_01
│       └── traces.txt
└── logs/                 # Organized by type
    ├── logcat/
    │   └── logcat.txt
    ├── tombstones/
    │   └── tombstone_01
    ├── anr/
    │   └── traces.txt
    └── system/
```

### Usage

#### From BugAnalyst Agent (Automated)

The BugAnalyst agent automatically invokes this processor when JIRA attachments are detected:

```python
from Autodev.scripts.process_jira_attachments import JiraAttachmentProcessor

processor = JiraAttachmentProcessor(
    workspace_root="/home/qsd1kor/Autodev/core/workspace",
    issue_key="PROJ-1234"
)

# attachment_files is list of (filename, bytes_content) from JIRA MCP
summary = processor.process_attachments(attachment_files)

# Get priority logs for RCA
priority_logs = processor.get_priority_logs()
```

#### Standalone CLI (Testing)

```bash
python3 process_jira_attachments.py <workspace_root> <issue_key>

# Example:
python3 process_jira_attachments.py \
    /home/qsd1kor/Autodev/core/workspace \
    PROJ-1234
```

### API Reference

#### `JiraAttachmentProcessor(workspace_root, issue_key)`

Main class for processing JIRA attachments.

**Methods:**

- `save_attachment(filename, content)` — Save raw binary attachment
- `extract_archive(filepath)` — Extract zip/tar archive
- `classify_log(filepath)` — Detect log type by pattern matching
- `organize_logs(files)` — Organize files into categorized directories
- `process_attachments(attachment_files)` — Main pipeline (save → extract → organize)
- `get_priority_logs()` — Return dict of priority logs (logcat, tombstones, ANR)
- `cleanup()` — Delete all workspace files for this issue

**Returns (process_attachments):**

```python
{
    'issue_key': 'PROJ-1234',
    'attachments_saved': 3,
    'files_extracted': 15,
    'logs': {
        'logcat': 2,
        'tombstones': 1,
        'anr': 1
    },
    'paths': {
        'attachments': '/path/to/workspace/PROJ-1234/attachments',
        'extracted': '/path/to/workspace/PROJ-1234/extracted',
        'logs': '/path/to/workspace/PROJ-1234/logs'
    },
    'organized_files': {
        'logcat': [Path('logs/logcat/logcat.txt'), ...],
        'tombstones': [Path('logs/tombstones/tombstone_01')],
        'anr': [Path('logs/anr/traces.txt')],
        'system': [],
        'other': []
    }
}
```

### Integration with BugAnalyst

The attachment processor is integrated into the BugAnalyst workflow at **Step 1a**:

1. BugAnalyst fetches the JIRA ticket
2. If attachments exist, calls `get_issue_attachments`
3. Passes attachment data to the processor
4. Processor extracts and organizes logs
5. BugAnalyst reads priority logs (ANR → tombstones → logcat → system)
6. Log excerpts are included as evidence in the Root Cause Analysis

### Cleanup

To remove processed files after analysis is complete:

```python
processor.cleanup()
```

This deletes the entire `workspace/<ISSUE_KEY>/` directory.

### Requirements

- Python 3.7+
- Standard library only (no external dependencies)
- Tested with zip, tar, tar.gz, tar.bz2 archives

### Error Handling

- Archive extraction failures are logged but do not block processing
- Unrecognized file types are placed in `logs/other/`
- Files > 100MB are not content-analyzed (filename pattern only)
