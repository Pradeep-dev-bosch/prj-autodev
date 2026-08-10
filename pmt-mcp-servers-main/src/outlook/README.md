# Outlook MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides seamless integration with Microsoft Outlook via the Microsoft Graph API.

## Overview

The Outlook MCP Server provides comprehensive integration with Microsoft Outlook for email, calendar, and contact management. It exposes a rich set of tools for managing emails, events, and contacts directly inside MCP-enabled clients (e.g. VS Code Copilot Chat) while keeping credentials secure via environment variables.

The server is built with the `FastMCP` framework and uses the Microsoft Graph API with OAuth 2.0 Authorization Code Flow with PKCE (RFC 7636) for secure authentication.

### Limitations

- Requires Azure AD application registration with client secret (ConfidentialClientApplication)
- Only supports delegated permissions for personal mailboxes
- OAuth callback requires browser access for first-time authentication
- Message IDs required for most operations (use search_emails to find IDs from subjects)
- Depending on the LLM models, accuracy might differ. Premium models like GPT-5 or Claude Sonnet 4.5 are recommended for better performance and results with complex Outlook operations

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../README.md#access-to-pmt-artifactory-repository))
- Azure AD application registration with Microsoft Graph API permissions
- Valid Microsoft account for authentication

### Azure AD Application Setup

1. **Register an application in Azure AD**
   - Go to Azure Portal → Azure Active Directory → App registrations → New registration
   - Name: "Outlook MCP Server" (or your preferred name)
   - Supported account types: Choose based on your organization's requirements
   - Redirect URI: Skip this for now (will configure in step 5)

2. **Configure as Confidential Client (Required for Bosch CD 07900 compliance)**
   - Navigate to **Certificates & secrets**
   - Create a new **Client secret**
   - Copy the secret value immediately (it won't be shown again)
   - Note down: Client ID, Tenant ID, and Client Secret

3. **Configure API Permissions (Delegated permissions for Authorization Code Flow)**

   **Required Delegated Permissions:**

   **Mail Permissions:**
   - `Mail.Read` - Read user mail
   - `Mail.ReadWrite` - Read and write access to user mail
   - `Mail.Send` - Send mail as a user
   - `Mail.Read.Shared` - Read user and shared mail
   - `Mail.ReadBasic` - Read user basic mail
   - `Mail.ReadBasic.Shared` - Read user and shared basic mail
   - `Mail.ReadWrite.Shared` - Read and write user and shared mail

   **Calendar Permissions:**
   - `Calendars.Read` - Read user calendars
   - `Calendars.ReadWrite` - Have full access to user calendars
   - `Calendars.Read.Shared` - Read user and shared calendars
   - `Calendars.ReadBasic` - Read basic details of user calendars

   **Contact Permissions:**
   - `Contacts.Read` - Read user contacts
   - `Contacts.ReadWrite` - Have full access to user contacts
   - `Contacts.Read.Shared` - Read user and shared contacts
   - `Contacts.ReadWrite.Shared` - Read and write user and shared contacts

   **Authentication Permissions:**
   - `email` - View users' email address
   - `openid` - Sign users in
   - `profile` - View users' basic profile
   - `offline_access` - Maintain access to data you have given it access to

   **How to add permissions:**
   - Go to **API permissions** → Add a permission → Microsoft Graph → **Delegated permissions**
   - Search and select the permissions listed above
   - Click "Add permissions"

4. **Grant admin consent** (required for Bosch users)
   - At Bosch, admin consent is required for all Microsoft Graph API permissions
   - Follow the [Pre-Approval Service Desk Workflow](https://inside-docupedia.bosch.com/confluence/spaces/dirservices/pages/2083399013/3+Pre-Approval+Service+Desk+Workflow) to raise a ticket for admin consent
   - The ticket should include your Azure AD application details and the permissions listed above
   - Once approved, admin consent will be granted by the Directory Services team

5. **Configure Redirect URIs**
   - Go to **Authentication** → Add platform → Web
   - Add redirect URIs:
     - `http://localhost:8080` (or your configured `OAUTH_REDIRECT_PORT` value)
     - `https://localhost.local` (required for Bosch central security policies)
   - Both URIs are required: the first for OAuth callback, the second for Bosch IT security compliance

**Important Notes:**
- ✅ Uses **Delegated permissions** - operates on behalf of the signed-in user
- ✅ Supports **personal mailboxes** - user's own email, calendar, and contacts
- ✅ **Bosch CD 07900 compliant** - uses ConfidentialClientApplication, not public client
- ✅ **MFA compatible** - supports multi-factor authentication during sign-in
- ✅ **Conditional access ready** - respects Azure AD conditional access policies
- ❌ **Public client prohibited** - Device Code Flow and Interactive Browser Flow are NOT supported per Bosch policy

### MCP Client Integration

The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

Start the Docker version MCP server after adding `.vscode/mcp.json`. It is ready to use now.

Check out the [`../README.md`](../README.md) to find out more about [`Running MCP Servers using uv/python`](../README.md#running-mcp-servers-for-development)

### Usage Examples

Once connected to an MCP-compatible client, you can interact with Outlook using natural language. Try these examples in your VSCode GitHub Copilot chat:

- "List my last 20 emails from inbox"
- "Search for emails about project report"
- "Send an email to colleague@example.com with subject 'Project Update'"
- "Create a draft email to team@example.com"
- "Mark email with subject 'Meeting Notes' as read"
- "List my calendar events for next week"
- "Create a Teams meeting tomorrow at 2pm for 1 hour"
- "Accept the meeting invitation for tomorrow's standup"
- "List all my contacts"
- "Search for contacts named John"
- "Create a new contact for Jane Doe"

The AI assistant will translate these natural language requests into actual Microsoft Graph API requests and execute them in Outlook.

### Features

The server provides comprehensive Outlook integration capabilities with 30+ specialized MCP tools covering:

- Email querying, sending, and management
- Draft email creation and editing
- Calendar event creation and management
- Contact management and search
- Mail folder operations
- Teams meeting integration

The following MCP tools are available for comprehensive Outlook management:

- **Email Operations**:
  - `list_emails` - List emails from specific folders with optional filtering
  - `get_email` - Get detailed information about a specific email
  - `search_emails` - Search emails using search queries
  - `send_email` - Send email messages with attachments support
  - `reply_to_email` - Reply to emails (reply or reply-all)
  - `forward_email` - Forward emails to other recipients
  - `move_email` - Move emails between folders
  - `delete_email` - Delete emails (soft or permanent delete)
  - `mark_email_as_read` - Mark emails as read or unread

- **Draft Email Operations**:
  - `create_draft_email` - Create draft emails without sending
  - `update_draft_email` - Modify existing draft emails
  - `send_draft_email` - Send existing draft emails

- **Mail Folder Management**:
  - `list_mail_folders` - List all mail folders including subfolders
  - `create_mail_folder` - Create new mail folders

- **Calendar Operations**:
  - `list_calendar_events` - List calendar events within date ranges
  - `get_calendar_event` - Get detailed event information
  - `create_calendar_event` - Create new calendar events/meetings
  - `update_calendar_event` - Update existing calendar events
  - `delete_calendar_event` - Delete calendar events
  - `cancel_calendar_event` - Cancel events and notify attendees
  - `list_calendars` - List all user calendars

- **Contact Management**:
  - `list_contacts` - List all contacts with ordering options
  - `get_contact` - Get detailed contact information
  - `search_contacts` - Search contacts by name, email, or other fields
  - `list_contact_folders` - List contact folders/groups

### Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_CLIENT_ID` | Azure AD application (client) ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_TENANT_ID` | Azure AD tenant ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_CLIENT_SECRET` | Azure AD client secret (required for Bosch CD 07900 compliance) | `xxxxx~xxxxx` |
| `OAUTH_REDIRECT_PORT` | OAuth callback port (optional) | `8080` (default) |
| `HTTP_PROXY` | HTTP proxy URL (optional, for corporate environments) | `http://proxy.example.com:8080` |
| `HTTPS_PROXY` | HTTPS proxy URL (optional, for corporate environments) | `http://proxy.example.com:8080` |
| `TRANSPORT` | MCP transport protocol | `stdio` (default), `http`, `sse` |
| `HOST` | Server host address (if not using stdio) | `127.0.0.1` (default) |
| `HOST_PORT` | Server port (if not using stdio) | `8000` (default) |

**Authentication Flow:**
On first run, the server will display a URL in the terminal. Open this URL in your browser to sign in with your Microsoft account. After successful authentication, tokens are cached locally (`~/.outlook_mcp_token_cache.json`) for future use.

**Note:** When using the provided `mcp.json` configuration, set the environment variables as shown in the example configuration file.

### Troubleshooting

#### Authentication Issues
- **Missing CLIENT_SECRET:** Error "Missing required environment variables" - ensure `AZURE_CLIENT_SECRET` is set
- **Port Already in Use:** Change `OAUTH_REDIRECT_PORT` to a different port (must match Azure AD redirect URI)
- **Redirect URI Mismatch:** Ensure `http://localhost:[PORT]` is registered in Azure AD app registration
- **Token Cache Issues:** Delete `~/.outlook_mcp_token_cache.json` and re-authenticate
- **Browser Not Opening:** Manually copy the authentication URL from terminal output and open in browser
- **Proxy Issues:** Set `HTTP_PROXY` and `HTTPS_PROXY` environment variables for corporate networks

#### Permission Errors
- **"Insufficient privileges":** Ensure **delegated permissions** are granted (not application permissions)
- **Admin Consent:** Some organizations require admin consent - contact your IT administrator
- **Wrong Permission Type:** Verify you're using delegated permissions (Mail.Read, not Mail.Read.All)
- **User Not Authorized:** Ensure the signed-in user has access to the mailbox being accessed

#### Bosch-Specific Issues
- **Public Client Error:** If you see "Public clients are not allowed at Bosch" - ensure `CLIENT_SECRET` is provided
- **CD 07900 Compliance:** Server enforces ConfidentialClientApplication - PUBLIC CLIENT IS PROHIBITED
- **Conditional Access:** MFA and device compliance policies are fully supported
- **Central Security Policies:** Ensure Web platform with `https://localhost.local` is configured

#### Common Errors
- **"Message ID required":** Most email operations require message ID - use `search_emails` to find the message ID from subject
- **Rate Limiting:** Microsoft Graph API throttling - reduce request frequency or implement retry logic
- **Invalid DateTime Format:** Calendar operations require ISO 8601 format (e.g., "2026-01-16T14:00:00")
- **Network timeouts:** Check proxy settings if running in corporate environment

## Further Information

- [Microsoft Graph API Documentation](https://learn.microsoft.com/en-us/graph/overview)
- [Microsoft Graph API Mail Reference](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)
- [Microsoft Graph API Calendar Reference](https://learn.microsoft.com/en-us/graph/api/resources/calendar)
- [OAuth 2.0 Authorization Code Flow](https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow)
- [PKCE (RFC 7636)](https://tools.ietf.org/html/rfc7636)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Bosch CD 07900 Security Policy](https://inside-docupedia.bosch.com/confluence/x/hDlNjg)
