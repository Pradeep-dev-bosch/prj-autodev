import logging
import os
from typing import Any, Optional, Dict, List
from fastmcp import FastMCP
from outlook_auth import make_graph_request

mcp = FastMCP("outlook-mcp-server")


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.
    Returns:
        tuple[str, str, int]: A tuple containing:
            - transport_type (str): Transport protocol type, defaults to "stdio"
            - host (str): Server host address, defaults to "127.0.0.1"
            - port (int): Server port number, defaults to "8000"
    """
    transport = os.getenv("TRANSPORT") or "stdio"
    if transport in ["stdio", "<TRANSPORT>", None, "", "-", "null"]:
        logging.info("MCP init: transport=stdio")
        return ("stdio", "", 0)

    host = os.getenv("HOST") or "127.0.0.1"
    port_str = os.getenv("HOST_PORT") or "8000"

    if host == "<HOST>":
        host = "127.0.0.1"
    if port_str == "<HOST_PORT>":
        port_str = "8000"

    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(
            f"Invalid PORT env variable: '{port_str}' - must be a valid integer"
        )
    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


# EMAIL OPERATIONS
@mcp.tool()
def list_emails(
    top: int = 10, folder: str = "inbox", filter_query: Optional[str] = None
) -> Dict[str, Any]:
    """List emails from a specific folder.

    Args:
        top: Number of emails to retrieve (default: 10, max: 999)
        folder: Folder name (inbox, sentitems, drafts, deleteditems) or folder ID
        filter_query: OData filter query (e.g., "from/emailAddress/address eq 'user@example.com'")

    Returns:
        Dictionary containing email list with subject, sender, received time, etc.
    """
    params = {"$top": min(top, 999), "$orderby": "receivedDateTime DESC"}
    if filter_query:
        params["$filter"] = filter_query

    return make_graph_request(
        "GET", f"/me/mailFolders/{folder}/messages", params=params
    )


@mcp.tool()
def get_email(message_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific email message.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this get_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the email message (NOT the subject line)

    Returns:
        Dictionary containing full email details including body, attachments, etc.
    """
    return make_graph_request("GET", f"/me/messages/{message_id}")


@mcp.tool()
def search_emails(query: str, top: int = 25) -> Dict[str, Any]:
    """Search emails using a search query.

    Args:
        query: Search query string (searches subject, body, sender, recipients)
        top: Number of results to return (default: 25)

    Returns:
        Dictionary containing matching emails
    """
    params = {"$search": f'"{query}"', "$top": top}
    return make_graph_request("GET", "/me/messages", params=params)


@mcp.tool()
def send_email(
    to_recipients: List[str],
    subject: str,
    body: str,
    body_type: str = "HTML",
    cc_recipients: Optional[List[str]] = None,
    bcc_recipients: Optional[List[str]] = None,
    importance: str = "normal",
) -> Dict[str, Any]:
    """Send an email message.

    Args:
        to_recipients: List of recipient email addresses
        subject: Email subject
        body: Email body content
        body_type: Content type - "HTML" or "Text" (default: HTML)
        cc_recipients: Optional list of CC recipient email addresses
        bcc_recipients: Optional list of BCC recipient email addresses
        importance: Message importance - "low", "normal", or "high" (default: normal)

    Returns:
        Dictionary with success status
    """

    def format_recipients(emails: List[str]) -> List[Dict]:
        return [{"emailAddress": {"address": email}} for email in emails]

    message_body: Dict[str, Any] = {
        "subject": subject,
        "body": {"contentType": body_type, "content": body},
        "toRecipients": format_recipients(to_recipients),
        "importance": importance,
    }

    if cc_recipients:
        message_body["ccRecipients"] = format_recipients(cc_recipients)
    if bcc_recipients:
        message_body["bccRecipients"] = format_recipients(bcc_recipients)

    message = {
        "message": message_body,
        "saveToSentItems": "true",
    }

    return make_graph_request("POST", "/me/sendMail", data=message)


@mcp.tool()
def reply_to_email(
    message_id: str, comment: str, reply_all: bool = False
) -> Dict[str, Any]:
    """Reply to an email message.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this reply_to_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the message to reply to (NOT the subject line)
        comment: Reply message content
        reply_all: If True, reply to all recipients; if False, reply only to sender

    Returns:
        Dictionary with success status
    """
    endpoint = f"/me/messages/{message_id}/{'replyAll' if reply_all else 'reply'}"
    data = {"comment": comment}
    return make_graph_request("POST", endpoint, data=data)


@mcp.tool()
def forward_email(
    message_id: str, to_recipients: List[str], comment: Optional[str] = None
) -> Dict[str, Any]:
    """Forward an email message.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this forward_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the message to forward (NOT the subject line)
        to_recipients: List of recipient email addresses
        comment: Optional comment to include with the forwarded message

    Returns:
        Dictionary with success status
    """
    data: Dict[str, Any] = {
        "toRecipients": [
            {"emailAddress": {"address": email}} for email in to_recipients
        ]
    }
    if comment:
        data["comment"] = comment

    return make_graph_request("POST", f"/me/messages/{message_id}/forward", data=data)


@mcp.tool()
def move_email(message_id: str, destination_folder: str) -> Dict[str, Any]:
    """Move an email to a different folder.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this move_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the message to move (NOT the subject line)
        destination_folder: Destination folder name (inbox, sentitems, drafts, deleteditems) or folder ID.
                          For subfolders, use the folder ID from list_mail_folders tool.

    Returns:
        Dictionary with the moved message details
    """
    data = {"destinationId": destination_folder}
    return make_graph_request("POST", f"/me/messages/{message_id}/move", data=data)


@mcp.tool()
def delete_email(message_id: str, permanent: bool = False) -> Dict[str, Any]:
    """Delete an email message.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this delete_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the message to delete (NOT the subject line)
        permanent: If True, permanently delete; if False, move to Deleted Items

    Returns:
        Dictionary with success status
    """
    if permanent:
        return make_graph_request("DELETE", f"/me/messages/{message_id}")
    else:
        # Move to deleted items
        data = {"destinationId": "deleteditems"}
        return make_graph_request("POST", f"/me/messages/{message_id}/move", data=data)


@mcp.tool()
def mark_email_as_read(message_id: str, is_read: bool = True) -> Dict[str, Any]:
    """Mark an email as read or unread.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this mark_email_as_read tool with the retrieved message ID.

    Args:
        message_id: The ID of the message (NOT the subject line)
        is_read: True to mark as read, False to mark as unread

    Returns:
        Dictionary with success status
    """
    data = {"isRead": is_read}
    return make_graph_request("PATCH", f"/me/messages/{message_id}", data=data)


@mcp.tool()
def list_mail_folders() -> Dict[str, Any]:
    """List all mail folders including subfolders.

    Returns:
        Dictionary containing all mail folders with their subfolders recursively populated
    """

    def fetch_child_folders(folder_id: str) -> List[Dict[str, Any]]:
        """Recursively fetch child folders for a given folder."""
        try:
            response = make_graph_request(
                "GET", f"/me/mailFolders/{folder_id}/childFolders"
            )
            child_folders = response.get("value", [])

            # Recursively fetch subfolders for each child
            for folder in child_folders:
                if folder.get("childFolderCount", 0) > 0:
                    folder["childFolders"] = fetch_child_folders(folder["id"])

            return child_folders
        except Exception as e:
            logging.error(f"Error fetching child folders for {folder_id}: {e}")
            return []

    # Get top-level folders
    response = make_graph_request("GET", "/me/mailFolders")
    folders = response.get("value", [])

    # Fetch subfolders for folders that have children
    for folder in folders:
        if folder.get("childFolderCount", 0) > 0:
            folder["childFolders"] = fetch_child_folders(folder["id"])

    response["value"] = folders
    return response


@mcp.tool()
def create_mail_folder(
    display_name: str, parent_folder_id: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new mail folder.

    Args:
        display_name: Name for the new folder
        parent_folder_id: Optional parent folder ID (if not provided, creates at root level)

    Returns:
        Dictionary with the created folder details
    """
    data = {"displayName": display_name}
    endpoint = (
        f"/me/mailFolders/{parent_folder_id}/childFolders"
        if parent_folder_id
        else "/me/mailFolders"
    )
    return make_graph_request("POST", endpoint, data=data)


# DRAFT EMAIL OPERATIONS
@mcp.tool()
def create_draft_email(
    to_recipients: List[str],
    subject: str,
    body: str,
    body_type: str = "HTML",
    cc_recipients: Optional[List[str]] = None,
    bcc_recipients: Optional[List[str]] = None,
    importance: str = "normal",
) -> Dict[str, Any]:
    """Create a draft email without sending.

    Args:
        to_recipients: List of recipient email addresses
        subject: Email subject
        body: Email body content
        body_type: Content type - "HTML" or "Text" (default: HTML)
        cc_recipients: Optional list of CC recipient email addresses
        bcc_recipients: Optional list of BCC recipient email addresses
        importance: Message importance - "low", "normal", or "high" (default: normal)

    Returns:
        Dictionary with draft message details including draft ID
    """

    def format_recipients(emails: List[str]) -> List[Dict]:
        return [{"emailAddress": {"address": email}} for email in emails]

    message_body: Dict[str, Any] = {
        "subject": subject,
        "body": {"contentType": body_type, "content": body},
        "toRecipients": format_recipients(to_recipients),
        "importance": importance,
    }

    if cc_recipients:
        message_body["ccRecipients"] = format_recipients(cc_recipients)
    if bcc_recipients:
        message_body["bccRecipients"] = format_recipients(bcc_recipients)

    return make_graph_request("POST", "/me/messages", data=message_body)


@mcp.tool()
def update_draft_email(
    message_id: str,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    body_type: str = "HTML",
    to_recipients: Optional[List[str]] = None,
    cc_recipients: Optional[List[str]] = None,
    bcc_recipients: Optional[List[str]] = None,
    importance: Optional[str] = None,
) -> Dict[str, Any]:
    """Modify an existing draft email.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this update_draft_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the draft message to update (NOT the subject line)
        subject: New email subject (optional)
        body: New email body content (optional)
        body_type: Content type - "HTML" or "Text" (default: HTML)
        to_recipients: New list of recipient email addresses (optional)
        cc_recipients: New list of CC recipient email addresses (optional)
        bcc_recipients: New list of BCC recipient email addresses (optional)
        importance: New message importance - "low", "normal", or "high" (optional)

    Returns:
        Dictionary with updated draft message details
    """

    def format_recipients(emails: List[str]) -> List[Dict]:
        return [{"emailAddress": {"address": email}} for email in emails]

    update_data: Dict[str, Any] = {}

    if subject is not None:
        update_data["subject"] = subject
    if body is not None:
        update_data["body"] = {"contentType": body_type, "content": body}
    if to_recipients is not None:
        update_data["toRecipients"] = format_recipients(to_recipients)
    if cc_recipients is not None:
        update_data["ccRecipients"] = format_recipients(cc_recipients)
    if bcc_recipients is not None:
        update_data["bccRecipients"] = format_recipients(bcc_recipients)
    if importance is not None:
        update_data["importance"] = importance

    return make_graph_request("PATCH", f"/me/messages/{message_id}", data=update_data)


# CONTACTS OPERATIONS
@mcp.tool()
def list_contacts(top: int = 50, order_by: str = "displayName") -> Dict[str, Any]:
    """List all contacts.

    Args:
        top: Number of contacts to retrieve (default: 50, max: 999)
        order_by: Field to order by (default: displayName)

    Returns:
        Dictionary containing contacts with name, email, phone numbers, etc.
    """
    params = {"$top": min(top, 999), "$orderby": order_by}
    return make_graph_request("GET", "/me/contacts", params=params)


@mcp.tool()
def get_contact(contact_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific contact.

    Args:
        contact_id: The ID of the contact

    Returns:
        Dictionary containing full contact details
    """
    return make_graph_request("GET", f"/me/contacts/{contact_id}")


@mcp.tool()
def search_contacts(query: str, top: int = 25) -> Dict[str, Any]:
    """Search contacts by name, email, or other fields.

    Args:
        query: Search query string (searches display name, email, etc.)
        top: Number of results to return (default: 25)

    Returns:
        Dictionary containing matching contacts
    """
    params = {"$search": f'"{query}"', "$top": top}
    return make_graph_request("GET", "/me/contacts", params=params)


@mcp.tool()
def list_contact_folders() -> Dict[str, Any]:
    """List all contact folders/groups.

    Returns:
        Dictionary containing all contact folders
    """
    return make_graph_request("GET", "/me/contactFolders")


# CALENDAR OPERATIONS
@mcp.tool()
def list_calendar_events(
    start_datetime: Optional[str] = None,
    end_datetime: Optional[str] = None,
    top: int = 50,
    calendar_id: str = "calendar",
) -> Dict[str, Any]:
    """List calendar events within a date range.

    Args:
        start_datetime: Start date/time in ISO 8601 format (e.g., "2026-01-16T00:00:00")
                       If not provided, defaults to current date
        end_datetime: End date/time in ISO 8601 format (e.g., "2026-01-16T23:59:59")
                     If not provided, defaults to 7 days from start
        top: Number of events to retrieve (default: 50, max: 999)
        calendar_id: Calendar ID or "calendar" for default calendar

    Returns:
        Dictionary containing calendar events with subject, start, end, attendees, location, etc.
    """
    from datetime import datetime, timedelta

    if start_datetime is None:
        start_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_datetime = start_dt.isoformat()

    if end_datetime is None:
        start_dt = datetime.fromisoformat(
            start_datetime.replace("Z", "+00:00")
            if "Z" in start_datetime
            else start_datetime
        )
        end_dt = start_dt + timedelta(days=7)
        end_datetime = end_dt.isoformat()

    params = {
        "$top": min(top, 999),
        "$orderby": "start/dateTime",
        "startDateTime": start_datetime,
        "endDateTime": end_datetime,
    }

    return make_graph_request(
        "GET", f"/me/calendars/{calendar_id}/calendarView", params=params
    )


@mcp.tool()
def get_calendar_event(event_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific calendar event.

    Args:
        event_id: The ID of the calendar event

    Returns:
        Dictionary containing full event details including attendees, location, body, etc.
    """
    return make_graph_request("GET", f"/me/events/{event_id}")


@mcp.tool()
def create_calendar_event(
    subject: str,
    start_datetime: str,
    end_datetime: str,
    attendees: Optional[List[str]] = None,
    location: Optional[str] = None,
    body: Optional[str] = None,
    body_type: str = "HTML",
    is_online_meeting: bool = False,
    online_meeting_provider: str = "teamsForBusiness",
    is_reminder_on: bool = True,
    reminder_minutes_before_start: int = 15,
    calendar_id: str = "calendar",
) -> Dict[str, Any]:
    """Create a new calendar event/meeting.

    Args:
        subject: Event subject/title
        start_datetime: Start date/time in ISO 8601 format (e.g., "2026-01-16T14:00:00")
        end_datetime: End date/time in ISO 8601 format (e.g., "2026-01-16T15:00:00")
        attendees: Optional list of attendee email addresses
        location: Optional location/room name
        body: Optional event description/body
        body_type: Content type - "HTML" or "Text" (default: HTML)
        is_online_meeting: If True, creates Teams meeting link (default: False)
        online_meeting_provider: "teamsForBusiness" or "skypeForBusiness" (default: teamsForBusiness)
        is_reminder_on: Enable reminder (default: True)
        reminder_minutes_before_start: Minutes before event to remind (default: 15)
        calendar_id: Calendar ID or "calendar" for default calendar

    Returns:
        Dictionary with created event details including Teams link if requested
    """
    event_data: Dict[str, Any] = {
        "subject": subject,
        "start": {"dateTime": start_datetime, "timeZone": "UTC"},
        "end": {"dateTime": end_datetime, "timeZone": "UTC"},
        "isReminderOn": is_reminder_on,
        "reminderMinutesBeforeStart": reminder_minutes_before_start,
    }

    if attendees:
        event_data["attendees"] = [
            {"emailAddress": {"address": email}, "type": "required"}
            for email in attendees
        ]

    if location:
        event_data["location"] = {"displayName": location}

    if body:
        event_data["body"] = {"contentType": body_type, "content": body}

    if is_online_meeting:
        event_data["isOnlineMeeting"] = True
        event_data["onlineMeetingProvider"] = online_meeting_provider

    return make_graph_request(
        "POST", f"/me/calendars/{calendar_id}/events", data=event_data
    )


@mcp.tool()
def update_calendar_event(
    event_id: str,
    subject: Optional[str] = None,
    start_datetime: Optional[str] = None,
    end_datetime: Optional[str] = None,
    attendees: Optional[List[str]] = None,
    location: Optional[str] = None,
    body: Optional[str] = None,
    body_type: str = "HTML",
    is_reminder_on: Optional[bool] = None,
    reminder_minutes_before_start: Optional[int] = None,
) -> Dict[str, Any]:
    """Update an existing calendar event.

    Args:
        event_id: The ID of the event to update
        subject: New event subject/title (optional)
        start_datetime: New start date/time in ISO 8601 format (optional)
        end_datetime: New end date/time in ISO 8601 format (optional)
        attendees: New list of attendee email addresses (optional)
        location: New location/room name (optional)
        body: New event description/body (optional)
        body_type: Content type - "HTML" or "Text" (default: HTML)
        is_reminder_on: Enable/disable reminder (optional)
        reminder_minutes_before_start: Minutes before event to remind (optional)

    Returns:
        Dictionary with updated event details
    """
    update_data: Dict[str, Any] = {}

    if subject is not None:
        update_data["subject"] = subject

    if start_datetime is not None:
        update_data["start"] = {"dateTime": start_datetime, "timeZone": "UTC"}

    if end_datetime is not None:
        update_data["end"] = {"dateTime": end_datetime, "timeZone": "UTC"}

    if attendees is not None:
        update_data["attendees"] = [
            {"emailAddress": {"address": email}, "type": "required"}
            for email in attendees
        ]

    if location is not None:
        update_data["location"] = {"displayName": location}

    if body is not None:
        update_data["body"] = {"contentType": body_type, "content": body}

    if is_reminder_on is not None:
        update_data["isReminderOn"] = is_reminder_on

    if reminder_minutes_before_start is not None:
        update_data["reminderMinutesBeforeStart"] = reminder_minutes_before_start

    return make_graph_request("PATCH", f"/me/events/{event_id}", data=update_data)


@mcp.tool()
def delete_calendar_event(event_id: str) -> Dict[str, Any]:
    """Delete a calendar event.

    Args:
        event_id: The ID of the event to delete

    Returns:
        Dictionary with success status
    """
    return make_graph_request("DELETE", f"/me/events/{event_id}")


@mcp.tool()
def cancel_calendar_event(
    event_id: str, comment: Optional[str] = None
) -> Dict[str, Any]:
    """Cancel a calendar event and send cancellation notice to all attendees.

    Args:
        event_id: The ID of the event to cancel
        comment: Optional cancellation message to send to attendees

    Returns:
        Dictionary with success status
    """
    data: Dict[str, Any] = {}
    if comment:
        data["comment"] = comment

    return make_graph_request("POST", f"/me/events/{event_id}/cancel", data=data)


@mcp.tool()
def list_calendars() -> Dict[str, Any]:
    """List all calendars for the user.

    Returns:
        Dictionary containing all calendars with their names and IDs
    """
    return make_graph_request("GET", "/me/calendars")


@mcp.tool()
def send_draft_email(message_id: str) -> Dict[str, Any]:
    """Send an existing draft email.

    IMPORTANT: If the user provides only an email subject (not a message ID),
    you MUST first call the search_emails tool to find the message ID,
    then call this send_draft_email tool with the retrieved message ID.

    Args:
        message_id: The ID of the draft message to send (NOT the subject line)

    Returns:
        Dictionary with success status
    """
    return make_graph_request("POST", f"/me/messages/{message_id}/send")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
