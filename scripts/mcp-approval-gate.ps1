# mcp-approval-gate.ps1
# preToolUse hook — returns permissionDecision "ask" for protected MCP tools.
# Reads hook input JSON from stdin; supports both .tool_name and .toolName.
$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
# Protected tool names (exact match required)
# ---------------------------------------------------------------------------
$ProtectedTools = @(
    "jira-python-mcp-server-add_issue_comment"
    "jira-python-mcp-server-transition_issue"
    "gerrit-push_to_gerrit"
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
if ($ProtectedTools -contains $ToolName) {
    Write-Output '{"permissionDecision":"ask"}'
} else {
    Write-Output '{"permissionDecision":"allow"}'
}
