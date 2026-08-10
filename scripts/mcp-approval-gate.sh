#!/usr/bin/env bash
# mcp-approval-gate.sh
# preToolUse hook — returns permissionDecision "ask" for protected MCP tools.
# Reads hook input JSON from stdin; supports both .tool_name and .toolName.
set -euo pipefail

# ---------------------------------------------------------------------------
# Protected tool names (exact match required)
# ---------------------------------------------------------------------------
PROTECTED_TOOLS=(
  "add_issue_comment"
  "transition_issue"
  "push_to_gerrit"
)

# ---------------------------------------------------------------------------
# Read full stdin payload
# ---------------------------------------------------------------------------
INPUT="$(cat)"

# Resolve tool name — prefer .tool_name, fall back to .toolName
TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // .toolName // empty')"

if [[ -z "$TOOL_NAME" ]]; then
  # Cannot determine tool name; allow through and let the caller handle it
  printf '{"permissionDecision":"allow"}\n'
  exit 0
fi

# ---------------------------------------------------------------------------
# Check against protected list
# ---------------------------------------------------------------------------
for protected in "${PROTECTED_TOOLS[@]}"; do
  if [[ "$TOOL_NAME" == "$protected" ]]; then
    printf '{"permissionDecision":"ask"}\n'
    exit 0
  fi
done

# Not a protected tool — allow
printf '{"permissionDecision":"allow"}\n'
exit 0
