"""
Authentication module for Outlook MCP Server.

This module handles:
- Token cache management (get_token_cache, save_token_cache)
- MSAL app initialization (get_msal_app)
- OAuth callback server (OAuthCallbackHandler, start_callback_server)
- Token acquisition with PKCE (acquire_token_via_auth_code_flow, get_access_token)
- Helper function (make_graph_request)

Note: PKCE (RFC 7636) is handled automatically by MSAL's initiate_auth_code_flow().
"""

import os
import logging
import sys
from typing import Any, Optional, Dict
import msal
import requests
from pathlib import Path
import secrets
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading

# Environment variables for Microsoft Graph API
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
OAUTH_REDIRECT_PORT = os.getenv(
    "OAUTH_REDIRECT_PORT", "8080"
)  # Default to 8080 if not specified

if not CLIENT_ID or not TENANT_ID or not CLIENT_SECRET:
    raise ValueError(
        "Missing required environment variables: AZURE_CLIENT_ID, "
        "AZURE_TENANT_ID, AZURE_CLIENT_SECRET (required for Bosch CD 07900 compliance)"
    )

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
# Delegated permissions scopes
SCOPE = [
    "Mail.Read",
    "Mail.ReadWrite",
    "Mail.Send",
    "Calendars.ReadWrite",
    "Contacts.ReadWrite",
]
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Token cache file
TOKEN_CACHE_FILE = Path.home() / ".outlook_mcp_token_cache.json"

# Proxy configuration
HTTP_PROXY = os.getenv("HTTP_PROXY") or os.getenv("http_proxy")
HTTPS_PROXY = os.getenv("HTTPS_PROXY") or os.getenv("https_proxy")

# Configure proxies for requests
PROXIES = {}
if HTTP_PROXY:
    PROXIES["http"] = HTTP_PROXY
if HTTPS_PROXY:
    PROXIES["https"] = HTTPS_PROXY

# MSAL Confidential Client (lazy initialization) - required for Bosch CD 07900 compliance
_app = None
_token_cache = None

# Global variable to store authorization code from callback
_auth_code = None
_auth_state = None
_auth_error = None
_auth_flow = None  # Store the auth flow object (MSAL manages PKCE internally)


# Token Cache Management
def get_token_cache():
    """Load or create token cache."""
    global _token_cache
    if _token_cache is None:
        _token_cache = msal.SerializableTokenCache()
        if TOKEN_CACHE_FILE.exists():
            try:
                with open(TOKEN_CACHE_FILE, "r") as f:
                    _token_cache.deserialize(f.read())
                logging.info("Token cache loaded successfully")
            except Exception as e:
                logging.warning(f"Could not load token cache: {e}")
    return _token_cache


def save_token_cache():
    """Save token cache to file."""
    if _token_cache and _token_cache.has_state_changed:
        try:
            TOKEN_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(TOKEN_CACHE_FILE, "w") as f:
                f.write(_token_cache.serialize())
            logging.info("Token cache saved successfully")
        except Exception as e:
            logging.warning(f"Could not save token cache: {e}")


# MSAL App Initialization
def get_msal_app():
    """Get or create MSAL application instance with proxy support.

    Creates ConfidentialClientApplication for Bosch CD 07900 compliance.
    Uses Authorization Code Flow with PKCE (RFC 7636) for secure authentication.

    Returns:
        ConfidentialClientApplication: MSAL app instance

    Note:
        PUBLIC CLIENT APPLICATIONS ARE PROHIBITED by Bosch CD 07900.
        CLIENT_SECRET is mandatory - enforced at module initialization.
    """
    global _app
    if _app is None:
        # Create proxies dict for MSAL if needed
        proxies = PROXIES if PROXIES else None
        cache = get_token_cache()

        # Use ConfidentialClientApplication (required for Bosch CD 07900 compliance)
        # CLIENT_SECRET is verified at module load time
        _app = msal.ConfidentialClientApplication(
            CLIENT_ID,
            client_credential=CLIENT_SECRET,
            authority=AUTHORITY,
            token_cache=cache,
            proxies=proxies,
        )
        logging.info(
            "MSAL Confidential Client application initialized "
            "(Authorization Code Flow with PKCE) - Bosch CD 07900 compliant"
        )
    return _app


def acquire_token_via_browser(app: msal.PublicClientApplication) -> Optional[str]:
    """Acquire access token using interactive browser flow.

    DEPRECATED: This method uses PublicClientApplication which violates Bosch CD 07900.
    Kept for reference only - DO NOT USE.

    Args:
        app: MSAL application instance

    Returns:
        Access token if successful, None otherwise
    """
    raise Exception(
        "Browser authentication with PublicClientApplication is prohibited by Bosch CD 07900. "
        "Use Authorization Code Flow instead."
    )


def acquire_token_via_device_code(app: msal.PublicClientApplication) -> str:
    """Acquire access token using device code flow.

    DEPRECATED: This method uses PublicClientApplication which violates Bosch CD 07900.
    Kept for reference only - DO NOT USE.

    Args:
        app: MSAL application instance

    Returns:
        Access token

    Raises:
        Exception: Always - method is prohibited
    """
    raise Exception(
        "Device code flow is prohibited by Bosch CD 07900 (requires public client). "
        "Use Authorization Code Flow instead."
    )


# OAuth Callback Server
class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP request handler for OAuth2 authorization code callback."""

    def do_GET(self):
        """Handle GET request with authorization code."""
        global _auth_code, _auth_state, _auth_error

        # Parse query parameters
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        # Check for error
        if "error" in params:
            _auth_error = params["error"][0]
            error_desc = params.get("error_description", ["Unknown error"])[0]
            logging.error(f"OAuth error: {_auth_error} - {error_desc}")

            # Send error response
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"""
            <html><body>
            <h1>Authentication Failed</h1>
            <p>Error: {_auth_error}</p>
            <p>Description: {error_desc}</p>
            <p>You can close this window.</p>
            </body></html>
            """.encode()
            )
            return

        # Extract authorization code and state
        if "code" in params:
            _auth_code = params["code"][0]
            _auth_state = params.get("state", [None])[0]
            logging.info("Authorization code received successfully")

            # Send success response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"""
            <html><body>
            <h1>Authentication Successful!</h1>
            <p>You have successfully authenticated with Microsoft.</p>
            <p>You can close this window and return to the application.</p>
            <script>window.close();</script>
            </body></html>
            """
            )
        else:
            _auth_error = "no_code"
            logging.error("No authorization code in callback")

            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"""
            <html><body>
            <h1>Authentication Failed</h1>
            <p>No authorization code received.</p>
            <p>You can close this window.</p>
            </body></html>
            """
            )

    def log_message(self, format, *args):
        """Suppress default HTTP server logging."""
        pass


def start_callback_server(port: int = 8080, timeout: int = 120) -> Optional[int]:
    """Start HTTP server to listen for OAuth callback.

    Args:
        port: Port to listen on (default: 8080)
        timeout: Timeout in seconds (default: 120)

    Returns:
        Port number if successful, None if port unavailable
    """
    try:
        # Bind to 0.0.0.0 to accept connections from Docker host
        server = HTTPServer(("0.0.0.0", port), OAuthCallbackHandler)
        server.timeout = timeout

        def run_server():
            server.handle_request()  # Handle single request then stop

        # Start server in background thread
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()

        logging.info(f"OAuth callback server started on port {port}")
        return port
    except OSError as e:
        logging.warning(f"Port {port} unavailable: {e}")
        return None


# Token Acquisition
def acquire_token_via_auth_code_flow(app) -> str:
    """Acquire access token using Authorization Code Flow with PKCE.

    Bosch CD 07900 compliant implementation using ConfidentialClientApplication.
    PKCE is handled automatically by MSAL's initiate_auth_code_flow() for additional security (RFC 7636).
    Supports delegated permissions for personal mailboxes.
    Compatible with MFA, conditional access, and proxy requirements.

    Args:
        app: MSAL ConfidentialClientApplication instance

    Returns:
        Access token

    Raises:
        Exception: If authentication fails
    """
    global _auth_code, _auth_state, _auth_error, _auth_flow

    # Reset global variables
    _auth_code = None
    _auth_state = None
    _auth_error = None
    _auth_flow = None

    logging.info("Initiating Authorization Code Flow with PKCE")

    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)

    # Get the configured OAuth redirect port
    # CRITICAL: This port MUST match the redirect URI registered in Azure App Registration
    try:
        redirect_port = int(OAUTH_REDIRECT_PORT)
    except (ValueError, TypeError):
        redirect_port = 8080

    # Start callback server on the exact port (no fallbacks - must match Azure registration)
    server_port = start_callback_server(redirect_port, timeout=120)

    if not server_port:
        raise Exception(
            f"Could not start OAuth callback server on port {redirect_port}. "
            f"This port must match your Azure App Registration redirect URI (http://localhost:{redirect_port}). "
            f"Please ensure:\n"
            f"1. Port {redirect_port} is not in use\n"
            f"2. http://localhost:{redirect_port} is registered in your Azure App Registration\n"
            f"3. OAUTH_REDIRECT_PORT environment variable matches your Azure configuration"
        )

    redirect_uri = f"http://localhost:{server_port}"
    logging.info(f"Using redirect URI: {redirect_uri}")

    # Build authorization URL with PKCE (MSAL handles PKCE automatically)
    flow = app.initiate_auth_code_flow(
        scopes=SCOPE,
        redirect_uri=redirect_uri,
        state=state,
        prompt="select_account",  # Allow user to select account
    )

    if "error" in flow:
        raise Exception(
            f"Failed to initiate auth flow: {flow.get('error_description', flow.get('error'))}"
        )

    # Store the flow for later use in token exchange
    _auth_flow = flow

    auth_url = flow["auth_uri"]

    # Display authentication instructions
    sys.stderr.write("\n" + "=" * 60 + "\n")
    sys.stderr.write("AUTHENTICATION REQUIRED\n")
    sys.stderr.write("=" * 60 + "\n")
    sys.stderr.write("Please open this URL in your browser:\n\n")
    sys.stderr.write(auth_url + "\n\n")
    sys.stderr.write("=" * 60 + "\n\n")
    sys.stderr.flush()

    logging.info("Waiting for user to authenticate via browser")

    # Wait for callback (server handles single request then stops)
    logging.info("Waiting for authorization code (timeout: 120 seconds)...")
    import time

    timeout = 120
    start_time = time.time()

    while _auth_code is None and _auth_error is None:
        if time.time() - start_time > timeout:
            raise Exception(
                "Authentication timeout. User did not complete authentication within 120 seconds."
            )
        time.sleep(0.5)

    # Check for errors
    if _auth_error:
        raise Exception(f"Authentication failed: {_auth_error}")

    if not _auth_code:
        raise Exception("No authorization code received")

    # Validate state to prevent CSRF
    if _auth_state != state:
        raise Exception(
            f"State mismatch: expected {state}, got {_auth_state}. Possible CSRF attack."
        )

    logging.info("Authorization code received, exchanging for access token...")

    # Exchange authorization code for access token using the stored flow
    # MSAL automatically handles PKCE verification using the flow object
    result = app.acquire_token_by_auth_code_flow(
        auth_code_flow=_auth_flow,
        auth_response={"code": _auth_code, "state": _auth_state},
    )

    if "access_token" in result:
        save_token_cache()
        logging.info("Successfully authenticated via Authorization Code Flow with PKCE")
        return result["access_token"]
    else:
        error_msg = result.get(
            "error_description", result.get("error", "Unknown error")
        )
        logging.error(f"Failed to obtain access token: {error_msg}")
        raise Exception(f"Could not obtain access token: {error_msg}")


def get_access_token() -> str:
    """Acquire access token from Azure AD using Authorization Code Flow with PKCE.

    This implementation complies with Bosch CD 07900 security policy by:
    - Using ConfidentialClientApplication (not public client)
    - Using PKCE for enhanced security (handled automatically by MSAL)
    - Supporting MFA and conditional access policies
    - Working with Bosch enterprise proxy infrastructure

    Returns:
        Access token

    Raises:
        Exception: If authentication fails
    """
    app = get_msal_app()

    # Try to get token from cache first
    accounts = app.get_accounts()
    if accounts:
        logging.info("Using cached account")
        result = app.acquire_token_silent(SCOPE, account=accounts[0])
        if result and "access_token" in result:
            return result["access_token"]

    # No cached token, need to authenticate using Authorization Code Flow
    logging.info("No cached token found, initiating Authorization Code Flow with PKCE")
    return acquire_token_via_auth_code_flow(app)


# Graph API Helper
def make_graph_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Dict[str, Any]:
    """Make a request to Microsoft Graph API."""
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{GRAPH_API_ENDPOINT}{endpoint}"

    # Use proxies if configured
    request_kwargs: Dict[str, Any] = {"headers": headers}
    if PROXIES:
        request_kwargs["proxies"] = PROXIES

    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, **request_kwargs)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, params=params, **request_kwargs)
        elif method.upper() == "PATCH":
            response = requests.patch(url, json=data, params=params, **request_kwargs)
        elif method.upper() == "DELETE":
            response = requests.delete(url, **request_kwargs)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()

        # Handle empty responses (e.g., 204 No Content)
        if response.status_code == 204 or not response.content:
            return {"success": True, "status_code": response.status_code}

        return response.json()
    except requests.exceptions.HTTPError as e:
        logging.error(
            f"Graph API HTTP error: {e.response.status_code} {e.response.text}"
        )
        return {"error": e.response.text, "status_code": e.response.status_code}
    except Exception as e:
        logging.error(f"Graph API error: {str(e)}")
        return {"error": str(e)}
