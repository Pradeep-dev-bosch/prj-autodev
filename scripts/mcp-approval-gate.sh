#!/usr/bin/env bash
# mcp-approval-gate.sh
# preToolUse hook — returns permissionDecision "ask" for protected MCP tools.
# Reads hook input JSON from stdin; supports both .tool_name and .toolName.
set -euo pipefail

# ---------------------------------------------------------------------------
# Protected tool names (exact match required)
# ---------------------------------------------------------------------------
PROTECTED_TOOLS=(
  add_issue_comment add_issue_components update_issue_components set_issue_custom_field
  add_watcher add_web_link_to_issue add_worklog_entry assign_issue
  bulk_add_collaboration_links bulk_add_comments bulk_transition_issues
  clone_issue create_collaboration_link create_filter create_issue
  delete_filter delete_issue_comment link_epic_to_issue link_issues
  modify_issue_labels modify_issue_type remove_vote remove_watcher
  remove_web_link set_due_date set_issue_acceptance_criteria
  set_issue_description set_issue_reporter set_issue_summary
  transition_issue unlink_issues update_collaboration_link update_filter
  update_issue_comment update_time_tracking upload_attachment vote_for_issue
  push_to_gerrit
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
# Normalise prefixed names (e.g. jira-python-mcp-server-add_issue_comment) to the bare name
BARE_NAME="${TOOL_NAME##*[-/]}"

for protected in "${PROTECTED_TOOLS[@]}"; do
  if [[ "$BARE_NAME" == "$protected" ]]; then
    printf '{"permissionDecision":"ask"}\n'
    exit 0
  fi
done

# Not a protected tool — allow
printf '{"permissionDecision":"allow"}\n'
exit 0
