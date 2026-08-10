u# Autodev Setup Checklist

Use this checklist when setting up Autodev for the first time.

## ☑️ Component Registration *(Do this first for each IVI component)*

Run the **ComponentSetup** agent for every Android IVI component your team works on.
This gives BugAnalyst precise local context before it touches SharePoint or JIRA.

- [ ] Open Copilot Chat → select **ComponentSetup** agent
- [ ] Register each component in scope (e.g. DTV Service, MIS, Audio HAL, VHAL, Diagnosis)
- [ ] Verify files created: `core/docs/components/<component-slug>/component-info.md`
- [ ] Verify files created: `core/docs/components/<component-slug>/component-flow.md`

> **Tip:** One agent session = one component. Re-run for each additional component.
> To update an existing component, edit the files directly or re-run ComponentSetup.

## ☑️ Prerequisites

- [ ] Python 3.13+ installed (`python3 --version`)
- [ ] uv installed (`uv --version`)
- [ ] VS Code installed with GitHub Copilot extension
- [ ] Git installed (`git --version`)
- [ ] Access to JIRA, SharePoint, and Gerrit

## ☑️ Installation

- [ ] Cloned main repository
- [ ] Cloned `pmt-mcp-servers-main` repository
- [ ] Ran `uv sync` in `src/jira/`
- [ ] Ran `uv sync` in `src/sharepoint/sharepointonprem/`
- [ ] Ran `uv sync` in `src/gerrit/`

## ☑️ Configuration

- [ ] Copied `.vscode/mcp.json.example` to `.vscode/mcp.json`
- [ ] Updated `uv` command path (`which uv`)
- [ ] Updated absolute paths to MCP servers
- [ ] Set JIRA URL
- [ ] Set SharePoint URL and username
- [ ] Set Gerrit URL and username

## ☑️ Credentials

- [ ] Generated JIRA Personal Access Token
- [ ] Generated Gerrit HTTP Password
- [ ] Verified SharePoint password

## ☑️ VS Code Setup

- [ ] Enabled custom agents: `"chat.agent.enabled": true`
- [ ] Opened workspace in VS Code
- [ ] Verified MCP servers started (check status bar)
- [ ] Confirmed Autodev agent appears in agent picker

## ☑️ Testing

- [ ] Ran `python3 scripts/test_processor.py` successfully
- [ ] Verified test workspace created at `workspace/TEST-123/`
- [ ] Cleaned up test data (`rm -rf workspace/TEST-123/`)

## ☑️ First Run

- [ ] Selected Autodev agent in Copilot Chat
- [ ] Entered a test JIRA issue key
- [ ] MCP servers prompted for credentials
- [ ] JIRA issue fetched successfully
- [ ] Attachments downloaded and extracted
- [ ] SharePoint documents retrieved
- [ ] Root Cause Analysis generated
- [ ] Approved RCA (or tested rejection)
- [ ] Fix plan generated
- [ ] Approved fix (or tested rejection)
- [ ] Code changes applied
- [ ] Gerrit push completed

## 📚 Documentation

- [ ] Read [README.md](Autodev/README.md) - Overview
- [ ] Read [SETUP.md](Autodev/SETUP.md) - Detailed setup guide
- [ ] Read [QUICK_REFERENCE.md](Autodev/QUICK_REFERENCE.md) - Commands and patterns
- [ ] Bookmarked troubleshooting section in SETUP.md

## 🆘 Troubleshooting

If you encounter issues, check:

1. **VS Code Output panel** → Select "MCP" to see server logs
2. **Agent files** exist: `ls .github/agents/*.agent.md`
3. **Settings** enabled: `cat ~/.config/Code/User/settings.json | grep agent`
4. **MCP config** valid: Check `.vscode/mcp.json` for typos
5. **Paths** absolute: Use `pwd` to verify
6. **Credentials** valid: Test JIRA token with curl

See [SETUP.md#troubleshooting](Autodev/SETUP.md#troubleshooting) for detailed solutions.

---

## Ready to Go? 🚀

Once all checkboxes are ticked:

1. Open Copilot Chat (`Ctrl+Alt+I`)
2. Select **Autodev** from agent picker
3. Enter your first JIRA issue key
4. Let Autodev analyze, fix, and push!
