# diabrainmcpserver.py
import logging
import os
import urllib3
from fastmcp import FastMCP
import requests

# Create an MCP server
mcp = FastMCP("DIA Brain")

# SSL configuration
SSL_VERIFY = os.getenv("SSL_VERIFY", "true").lower() != "false"
if not SSL_VERIFY:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Default brain configuration from environment
DEFAULT_BRAIN_ID = os.getenv("DEFAULT_BRAIN_ID", "")
ENABLED_BRAIN_IDS = os.getenv("ENABLED_BRAIN_IDS", "")  # Comma-separated list


def get_default_brain_id():
    """Get the default brain ID from configuration

    Returns:
        The configured DEFAULT_BRAIN_ID, or first from ENABLED_BRAIN_IDS if not set
    """
    # Prefer explicit DEFAULT_BRAIN_ID
    if DEFAULT_BRAIN_ID:
        return DEFAULT_BRAIN_ID.strip()

    # Fallback to first enabled brain
    if ENABLED_BRAIN_IDS:
        brain_ids = [bid.strip() for bid in ENABLED_BRAIN_IDS.split(",") if bid.strip()]
        if brain_ids:
            return brain_ids[0]

    return ""


def get_access_token():
    """Get OAuth2 access token for DIA Brain API

    Requires:
    - CLIENT_SECRET environment variable (expires every 180 days, requires rotation)
    - CLIENT_ID environment variable
    - TENANT_ID environment variable (Azure AD tenant ID)

    See: https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain
    """
    client_secret = os.getenv("CLIENT_SECRET")
    if not client_secret:
        raise ValueError(
            "CLIENT_SECRET environment variable is required. "
            "Please set it in your mcp.json configuration. "
            "See: https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain"
        )

    client_id = os.getenv("CLIENT_ID")
    if not client_id:
        raise ValueError(
            "CLIENT_ID environment variable is required. "
            "Please set it in your mcp.json configuration. "
            "See: https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain"
        )

    tenant_id = os.getenv("TENANT_ID")
    if not tenant_id:
        raise ValueError(
            "TENANT_ID environment variable is required. "
            "Please set it in your mcp.json configuration. "
            "See: https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain"
        )

    logging.info(f"Requesting access token for client_id: {client_id}")

    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "client_id": client_id,
        "scope": "api://dia-brain/.default",
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.post(url, data=payload, verify=SSL_VERIFY)

    if response.status_code == 200:
        token_info = response.json()
        logging.info("Successfully obtained access token")
        return token_info["access_token"]
    else:
        error_msg = (
            f"Authentication failed (HTTP {response.status_code}). "
            f"Response: {response.text}\n"
            f"Common causes:\n"
            f"  - Expired CLIENT_SECRET (expires every 180 days)\n"
            f"  - Invalid client_id: {client_id}\n"
            f"See: https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain"
        )
        raise Exception(error_msg)


def query_dia_brain(
    prompt, knowledge_base_id, sharepoint_site_ids, docupedia_space_ids
):
    """Query the DIA Brain API with specified knowledge bases

    Note: User-Agent header is required for Python API calls to avoid authentication errors.
    See: https://inside-docupedia.bosch.com/confluence/spaces/GSDI/pages/4064414322/REST+API+to+Brain
    """
    access_token = get_access_token()
    api_url = "https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/chat/retrieval-augmented"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "PostmanRuntime/7.37.3",  # Required for Python API calls
        "Content-Type": "application/json",
    }
    data = {
        "prompt": prompt,
        "knowledgeBaseId": knowledge_base_id,
        "sharepointSiteIds": sharepoint_site_ids,
        "docupediaSpaceIds": docupedia_space_ids,
        "useGptKnowledge": "true",
    }

    logging.info(f"Querying DIA Brain API with knowledge_base_id: {knowledge_base_id}")
    response = requests.post(
        api_url, headers=headers, json=data, timeout=60, verify=SSL_VERIFY
    )

    if response.status_code == 200:
        logging.info("Query successful")
        return response.json().get("result")
    elif response.status_code == 401:
        error_msg = (
            f"DIA Brain API Authorization Failed (HTTP 401).\n"
            f"Error: {response.text}\n\n"
            f"This 'MessageBlocked' error means:\n"
            f"  1. Your user account hasn't connected this application ID to Brain\n"
            f"  2. The application may not be whitelisted on Bosch API Manager\n\n"
            f"REQUIRED ACTION:\n"
            f"  → Go to: https://brain.prd.dia-apps.bosch.tech/brains\n"
            f"  → Click your user menu → 'API Integration'\n"
            f"  → Enter application ID: {os.getenv('CLIENT_ID')}\n"
            f"  → Submit to connect the app to YOUR user account\n\n"
            f"If still failing after connecting, the app may need whitelisting:\n"
            f"  → Submit request: https://forms.office.com/e/K3gHBLbcbh\n"
            f"  → Wait for confirmation (up to 5 working days)"
        )
        raise Exception(error_msg)
    else:
        error_msg = (
            f"DIA Brain API request failed (HTTP {response.status_code}).\n"
            f"Response: {response.text}\n"
            f"Ensure you have access to the knowledge base and your app is properly configured."
        )
        raise Exception(error_msg)


@mcp.tool()
def query_brain(
    prompt: str,
    brain_id: str = "",
    sharepoint_sites: str = "",
    docupedia_spaces: str = "",
):
    """
    Query any DIA Brain knowledge base

    Args:
        prompt: The question or query to ask
        brain_id: The knowledge base ID (optional if DEFAULT_BRAIN_ID is set in config)
        sharepoint_sites: Comma-separated SharePoint site IDs (e.g., "Autosar" or "Site1,Site2")
        docupedia_spaces: Comma-separated Docupedia space IDs (e.g., "RA6" or "Space1,Space2")

    Returns:
        The response from the DIA Brain API

    Examples:
        With default brain: query_brain(prompt="What is AUTOSAR?", sharepoint_sites="Autosar")
        Specific brain: query_brain(prompt="What is AUTOSAR?", brain_id="VoEGl_0KtuAJ", sharepoint_sites="Autosar")
    """
    # Use default brain if not specified
    if not brain_id:
        brain_id = get_default_brain_id()
        if not brain_id:
            raise ValueError(
                "No brain_id provided and no DEFAULT_BRAIN_ID configured. "
                "Either pass brain_id parameter or set DEFAULT_BRAIN_ID/ENABLED_BRAIN_IDS in mcp.json"
            )
        logging.info(f"Using default brain_id: {brain_id}")

    # Parse comma-separated lists
    sharepoint_ids = [s.strip() for s in sharepoint_sites.split(",") if s.strip()]
    docupedia_ids = [s.strip() for s in docupedia_spaces.split(",") if s.strip()]

    logging.info(
        f"Querying brain_id={brain_id}, sharepoint={sharepoint_ids}, docupedia={docupedia_ids}"
    )
    return query_dia_brain(prompt, brain_id, sharepoint_ids, docupedia_ids)


@mcp.tool()
def list_brains():
    """
    List all available DIA Brain knowledge bases the user has access to

    Returns:
        List of knowledge bases with their IDs, names, and descriptions
    """
    access_token = get_access_token()
    api_url = "https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/knowledge-bases/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "PostmanRuntime/7.37.3",
        "Content-Type": "application/json",
    }

    logging.info("Fetching list of available knowledge bases")
    response = requests.get(api_url, headers=headers, timeout=30, verify=SSL_VERIFY)

    if response.status_code == 200:
        logging.info("Successfully retrieved knowledge bases list")
        brains = response.json()

        # Add configuration info
        enabled_ids = (
            [bid.strip() for bid in ENABLED_BRAIN_IDS.split(",") if bid.strip()]
            if ENABLED_BRAIN_IDS
            else []
        )
        default_id = get_default_brain_id()

        result = {
            "brains": brains,
            "configuration": {
                "default_brain_id": default_id,
                "enabled_brain_ids": enabled_ids,
                "note": (
                    "Configure DEFAULT_BRAIN_ID or ENABLED_BRAIN_IDS "
                    "in mcp.json to avoid passing brain_id every time"
                ),
            },
        }
        return result
    else:
        error_msg = (
            f"Failed to list knowledge bases (HTTP {response.status_code}).\n"
            f"Response: {response.text}"
        )
        raise Exception(error_msg)


@mcp.tool()
def get_enabled_brains():
    """
    Get the list of brain IDs configured and fetch their details from API

    Returns:
        Dictionary with default brain, enabled brains with names and descriptions
    """
    enabled_ids = (
        [bid.strip() for bid in ENABLED_BRAIN_IDS.split(",") if bid.strip()]
        if ENABLED_BRAIN_IDS
        else []
    )
    default_id = get_default_brain_id()

    # Fetch all brains from API to show names
    try:
        access_token = get_access_token()
        api_url = "https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/knowledge-bases/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "PostmanRuntime/7.37.3",
            "Content-Type": "application/json",
        }
        response = requests.get(api_url, headers=headers, timeout=30, verify=SSL_VERIFY)

        if response.status_code == 200:
            all_brains = response.json()

            # Filter to show only enabled brains
            enabled_brains = [
                {
                    "id": brain["id"],
                    "title": brain.get("title", "N/A"),
                    "description": brain.get("description", "")[:100] + "..."
                    if brain.get("description", "")
                    else "No description",
                    "is_default": brain["id"] == default_id,
                }
                for brain in all_brains
                if brain["id"] in enabled_ids
            ]

            return {
                "default_brain_id": default_id,
                "enabled_brain_count": len(enabled_ids),
                "enabled_brains": enabled_brains,
                "note": (
                    "Restart server to change default brain. "
                    "Pass brain_id parameter to override for specific queries."
                ),
            }
    except Exception as e:
        logging.error(f"Could not fetch brain details: {str(e)}")

    # Fallback if API call fails
    return {
        "default_brain_id": default_id,
        "enabled_brain_ids": enabled_ids,
        "count": len(enabled_ids),
        "note": "Run list_brains() to see brain names and descriptions. Restart server to change default.",
    }


@mcp.tool()
def get_brain_details(brain_id: str):
    """
    Get detailed information about a specific knowledge base

    Args:
        brain_id: The knowledge base ID

    Returns:
        Detailed information including sources, permissions, and configuration
    """
    access_token = get_access_token()
    api_url = f"https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/knowledge-bases/{brain_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "PostmanRuntime/7.37.3",
        "Content-Type": "application/json",
    }

    logging.info(f"Fetching details for knowledge base: {brain_id}")
    response = requests.get(api_url, headers=headers, timeout=30, verify=SSL_VERIFY)

    if response.status_code == 200:
        logging.info(f"Successfully retrieved details for brain: {brain_id}")
        return response.json()
    else:
        error_msg = (
            f"Failed to get brain details (HTTP {response.status_code}).\n"
            f"Response: {response.text}"
        )
        raise Exception(error_msg)


@mcp.tool()
def list_sharepoint_sites(brain_id: str):
    """
    List all SharePoint sites connected to a knowledge base

    Args:
        brain_id: The knowledge base ID

    Returns:
        List of SharePoint sites with their metadata and processing state
    """
    access_token = get_access_token()
    api_url = f"https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/sharepoint-sites?knowledgeBaseId={brain_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "PostmanRuntime/7.37.3",
        "Content-Type": "application/json",
    }

    logging.info(f"Fetching SharePoint sites for knowledge base: {brain_id}")
    response = requests.get(api_url, headers=headers, timeout=30, verify=SSL_VERIFY)

    if response.status_code == 200:
        logging.info(f"Successfully retrieved SharePoint sites for brain: {brain_id}")
        return response.json()
    else:
        error_msg = (
            f"Failed to list SharePoint sites (HTTP {response.status_code}).\n"
            f"Response: {response.text}"
        )
        raise Exception(error_msg)


@mcp.tool()
def list_docupedia_spaces(brain_id: str):
    """
    List all Docupedia spaces connected to a knowledge base

    Args:
        brain_id: The knowledge base ID

    Returns:
        List of Docupedia spaces with their metadata and processing state
    """
    access_token = get_access_token()
    api_url = f"https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/docupedia-space?knowledgeBaseId={brain_id}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "PostmanRuntime/7.37.3",
        "Content-Type": "application/json",
    }

    logging.info(f"Fetching Docupedia spaces for knowledge base: {brain_id}")
    response = requests.get(api_url, headers=headers, timeout=30, verify=SSL_VERIFY)

    if response.status_code == 200:
        logging.info(f"Successfully retrieved Docupedia spaces for brain: {brain_id}")
        return response.json()
    else:
        error_msg = (
            f"Failed to list Docupedia spaces (HTTP {response.status_code}).\n"
            f"Response: {response.text}"
        )
        raise Exception(error_msg)


@mcp.tool()
def list_documents(brain_id: str, document_types: str = ""):
    """
    List documents associated with a knowledge base

    Args:
        brain_id: The knowledge base ID
        document_types: Comma-separated document types to filter (FILE, WEBPAGE, CONFLUENCE_PAGE, SERVICE_NOW_ARTICLE)

    Returns:
        List of documents with their metadata and processing state
    """
    access_token = get_access_token()
    api_url = f"https://ews-emea.api.bosch.com/it/application/dia-brain/v1/api/documents?knowledgeBaseId={brain_id}"

    # Parse comma-separated document types
    if document_types:
        doc_types = [dt.strip() for dt in document_types.split(",") if dt.strip()]
        if doc_types:
            doc_types_param = "&".join([f"documentTypes={dt}" for dt in doc_types])
            api_url += f"&{doc_types_param}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "PostmanRuntime/7.37.3",
        "Content-Type": "application/json",
    }

    logging.info(f"Fetching documents for knowledge base: {brain_id}")
    response = requests.get(api_url, headers=headers, timeout=30, verify=SSL_VERIFY)

    if response.status_code == 200:
        logging.info(f"Successfully retrieved documents for brain: {brain_id}")
        return response.json()
    else:
        error_msg = (
            f"Failed to list documents (HTTP {response.status_code}).\n"
            f"Response: {response.text}"
        )
        raise Exception(error_msg)


@mcp.tool()
def batch_query(
    prompts: list[str],
    brain_id: str = "",
    sharepoint_sites: str = "",
    docupedia_spaces: str = "",
):
    """
    Execute multiple queries in a single batch operation for efficiency

    Args:
        prompts: List of questions or queries to ask
        brain_id: The knowledge base ID (optional if DEFAULT_BRAIN_ID is set in config)
        sharepoint_sites: Comma-separated SharePoint site IDs
        docupedia_spaces: Comma-separated Docupedia space IDs

    Returns:
        List of responses corresponding to each prompt
    """
    # Use default brain if not specified
    if not brain_id:
        brain_id = get_default_brain_id()
        if not brain_id:
            raise ValueError(
                "No brain_id provided and no DEFAULT_BRAIN_ID configured. "
                "Either pass brain_id parameter or set DEFAULT_BRAIN_ID/ENABLED_BRAIN_IDS in mcp.json"
            )
        logging.info(f"Using default brain_id: {brain_id}")

    # Parse comma-separated lists
    sharepoint_ids = [s.strip() for s in sharepoint_sites.split(",") if s.strip()]
    docupedia_ids = [s.strip() for s in docupedia_spaces.split(",") if s.strip()]

    logging.info(f"Executing batch query with {len(prompts)} prompts")

    results = []
    for i, prompt in enumerate(prompts):
        try:
            logging.info(f"Executing query {i+1}/{len(prompts)}")
            result = query_dia_brain(prompt, brain_id, sharepoint_ids, docupedia_ids)
            results.append({"prompt": prompt, "result": result, "status": "success"})
        except Exception as e:
            logging.error(f"Query {i+1} failed: {str(e)}")
            results.append({"prompt": prompt, "error": str(e), "status": "failed"})

    return results


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Starting the DIA Brain MCP server...")
    mcp.run(transport="stdio")
