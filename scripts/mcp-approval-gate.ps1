# mcp-approval-gate.ps1
# preToolUse hook — returns permissionDecision "ask" for protected MCP tools.
# Reads hook input JSON from stdin; supports both .tool_name and .toolName.
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Protected tool names (exact match required)
# ---------------------------------------------------------------------------
$ProtectedTools = @(
    "add_issue_comment", "add_issue_components", "update_issue_components", "set_issue_custom_field",
    "add_watcher", "add_web_link_to_issue", "add_worklog_entry", "assign_issue",
    "bulk_add_collaboration_links", "bulk_add_comments", "bulk_transition_issues",
    "clone_issue", "create_collaboration_link", "create_filter", "create_issue",
    "delete_filter", "delete_issue_comment", "link_epic_to_issue", "link_issues",
    "modify_issue_labels", "modify_issue_type", "remove_vote", "remove_watcher",
    "remove_web_link", "set_due_date", "set_issue_acceptance_criteria",
    "set_issue_description", "set_issue_reporter", "set_issue_summary",
    "transition_issue", "unlink_issues", "update_collaboration_link", "update_filter",
    "update_issue_comment", "update_time_tracking", "upload_attachment", "vote_for_issue",
    "push_to_gerrit"
)

# ---------------------------------------------------------------------------
# Read full stdin payload
# ---------------------------------------------------------------------------
$Input = $input | Out-String

if ([string]::IsNullOrWhiteSpace($Input)) {
    Write-Output '{"permissionDecision":"allow"}'
    exit 0
}

try {
    $Payload = $Input | ConvertFrom-Json
} catch {
    Write-Output '{"permissionDecision":"allow"}'
    exit 0
}

# Resolve tool name — prefer .tool_name, fall back to .toolName
$ToolName = if ($Payload.tool_name) { $Payload.tool_name } elseif ($Payload.toolName) { $Payload.toolName } else { $null }

if (-not $ToolName) {
    Write-Output '{"permissionDecision":"allow"}'
    exit 0
}

# ---------------------------------------------------------------------------
# Check against protected list
# ---------------------------------------------------------------------------
# Normalise: "jira-python-mcp-server-add_issue_comment" / ".../add_issue_comment" -> bare name
$BareName = $ToolName -replace '^.*[-/]', ''

if ($ProtectedTools -contains $BareName) {
    Write-Output '{"permissionDecision":"ask"}'
} else {
    Write-Output '{"permissionDecision":"allow"}'
}
