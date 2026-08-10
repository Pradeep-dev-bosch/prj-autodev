#!/bin/bash
# Setup script for Autodev workspace directory structure
# This creates the base directory structure (optional - directories are auto-created by the processor)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_DIR="$SCRIPT_DIR/workspace"

echo "Setting up Autodev workspace structure..."

# Create base template directory structure (for reference)
mkdir -p "$WORKSPACE_DIR"/_template/{attachments,extracted,logs/{logcat,tombstones,anr,system}}

# Create README files
cat > "$WORKSPACE_DIR"/_template/README.md << 'EOF'
# Template Directory Structure

This is a reference template showing the structure created for each JIRA issue.

Actual issue directories are created automatically at:
- `workspace/<ISSUE_KEY>/`

Example: `workspace/PROJ-1234/`
EOF

cat > "$WORKSPACE_DIR"/_template/attachments/README.md << 'EOF'
# Attachments

Raw files downloaded from JIRA are stored here.
EOF

cat > "$WORKSPACE_DIR"/_template/extracted/README.md << 'EOF'
# Extracted

Contents of zip/tar archives extracted from JIRA attachments.
EOF

cat > "$WORKSPACE_DIR"/_template/logs/README.md << 'EOF'
# Logs

Organized log files by category:
- **logcat/** - Android system logs, app logs
- **tombstones/** - Native crash dumps (C/C++)
- **anr/** - ANR traces (main thread blocked)
- **system/** - Kernel logs, bugreports, dumpsys output
EOF

# Make scripts executable
chmod +x "$SCRIPT_DIR"/scripts/*.py 2>/dev/null

echo "✓ Workspace structure created at: $WORKSPACE_DIR"
echo "✓ Template directory: $WORKSPACE_DIR/_template/"
echo ""
echo "Note: Actual issue directories (workspace/<ISSUE_KEY>/) are created"
echo "automatically by process_jira_attachments.py when analyzing tickets."
echo ""
echo "To test the processor:"
echo "  python3 scripts/process_jira_attachments.py workspace TEST-123"
