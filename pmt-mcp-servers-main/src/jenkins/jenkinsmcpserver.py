import json
import logging
import os
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
import xml.etree.ElementTree as ET

import requests
from fastmcp import FastMCP

mcp = FastMCP("JenkinsMCPServer")

SERVICE_BASE_URL = os.getenv("JENKINS_BASE_URL")
JENKINS_USERNAME = (
    os.getenv("JENKINS_USERNAME") or None
)  # Optional for anonymous access
JENKINS_API_TOKEN = (
    os.getenv("JENKINS_API_TOKEN") or None
)  # Optional for anonymous access
SSL_VERIFY = os.getenv("SSL_VERIFY", "true").lower() not in [
    "false",
    "0",
    "no",
]  # SSL verification enabled by default

if not SERVICE_BASE_URL:
    raise ValueError("JENKINS_BASE_URL environment variable is required")

# Authentication modes:
# 1. AUTH-BASED: Set JENKINS_USERNAME and JENKINS_API_TOKEN for instances requiring authentication
#    The server will automatically create the base64-encoded Basic auth header
# 2. NO-AUTH (Anonymous): Leave both USERNAME and TOKEN empty for instances with anonymous access

# Create base64-encoded auth token if credentials are provided
SERVICE_AUTH_TOKEN_ENCODED = None
if JENKINS_USERNAME and JENKINS_API_TOKEN:
    credentials = f"{JENKINS_USERNAME}:{JENKINS_API_TOKEN}"
    SERVICE_AUTH_TOKEN_ENCODED = base64.b64encode(credentials.encode()).decode()
    logging.info(f"Authentication mode: AUTH-BASED (username: {JENKINS_USERNAME})")
else:
    logging.info("Authentication mode: NO-AUTH (Anonymous)")


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.

    Returns:
        tuple[str, str, int]: A tuple containing:
            - transport_type (str): Transport protocol type, defaults to "stdio"
            - host (str): Server host address, defaults to "127.0.0.1"
            - port (int): Server port number, defaults to "8000"
    """
    transport = os.getenv("TRANSPORT") or "stdio"
    if transport in ["stdio", None, "", "-", "null", "<TRANSPORT>"]:
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
            f"Invalid HOST_PORT env variable: '{port_str}' - must be a valid integer"
        )

    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def _auth_headers() -> dict:
    """Generate authentication headers for Jenkins API requests.

    Returns:
        dict: Authorization header if credentials are configured, empty dict for anonymous access.

    Authentication Methods:
        - AUTH-BASED: Returns Basic auth header when JENKINS_USERNAME and JENKINS_API_TOKEN are set
          The base64 encoding is handled automatically by the server
        - NO-AUTH: Returns empty headers for anonymous Jenkins instances
    """
    if SERVICE_AUTH_TOKEN_ENCODED:
        return {"Authorization": f"Basic {SERVICE_AUTH_TOKEN_ENCODED}"}
    return {}


def _normalize_job_path(job_name: str) -> str:
    """Convert job path to Jenkins API format with /job/ prefixes.

    Examples:
        'test' -> 'job/test'
        'cx-dash/Tests/test' -> 'job/cx-dash/job/Tests/job/test'
        'job/cx-dash/job/Tests/job/test' -> 'job/cx-dash/job/Tests/job/test'
    """
    if not job_name:
        return ""

    # If already in correct format, return as-is
    if job_name.startswith("job/") and "/job/" in job_name:
        return job_name

    # Split by '/' and add 'job/' prefix to each part
    parts = [p.strip() for p in job_name.split("/") if p.strip() and p.strip() != "job"]
    if not parts:
        return ""

    return "/".join(f"job/{part}" for part in parts)


def _request(method: str, url: str, **kwargs) -> requests.Response:
    headers = _auth_headers()
    headers.update(kwargs.pop("headers", {}))
    kwargs["headers"] = headers
    kwargs.setdefault("timeout", 30)
    kwargs.setdefault("verify", SSL_VERIFY)  # Use SSL_VERIFY setting
    resp = requests.request(method, url, **kwargs)
    resp.raise_for_status()
    return resp


def _get_crumb() -> Optional[dict]:
    """Fetch Jenkins CSRF crumb details when required."""
    try:
        url = f"{SERVICE_BASE_URL}/crumbIssuer/api/json"
        resp = _request("GET", url)
        data = resp.json()
        crumb = data.get("crumb")
        field = data.get("crumbRequestField") or "Jenkins-Crumb"
        if crumb:
            return {"field": field, "crumb": crumb}
    except requests.RequestException:
        pass
    return None


@mcp.tool()
def ping() -> str:
    """Ping Jenkins server to verify connectivity.

    Returns:
        JSON string with status and server information.
    """
    url = f"{SERVICE_BASE_URL}/api/json"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(
            {
                "status": "ok",
                "jenkins_version": data.get("version"),
                "url": SERVICE_BASE_URL,
            }
        )
    except requests.RequestException as e:
        logging.error(f"Ping failed: {e}")
        return json.dumps({"error": str(e), "url": SERVICE_BASE_URL})


@mcp.tool()
def list_jobs(
    recursive: bool = True,
    name_contains: Optional[str] = None,
    folder: Optional[str] = None,
    limit: int = 200,
) -> str:
    """List all Jenkins jobs with their status. By default, recursively lists all jobs including those in subfolders.

    Args:
        recursive: If True, recursively list jobs in all subfolders (default: True). If False, list only top-level jobs.
        name_contains: Optional case-insensitive substring to filter job names
        folder: Optional folder path to start from (e.g., "cx-dash" or "job/cx-dash")
        limit: Maximum number of results to return (default: 200)

    Returns:
        JSON string with list of jobs including name, url, color (status), and full path.
    """
    if not recursive:
        # Non-recursive: list only jobs at the specified level
        if folder:
            # Normalize folder path
            folder_path = folder.strip("/")
            if not folder_path.startswith("job/"):
                folder_path = f"job/{folder_path}"
            url = (
                f"{SERVICE_BASE_URL}/{folder_path}/api/json?"
                "tree=jobs[name,url,color,lastBuild[number,url,result,timestamp]]"
            )
        else:
            url = (
                f"{SERVICE_BASE_URL}/api/json?"
                "tree=jobs[name,url,color,lastBuild[number,url,result,timestamp]]"
            )
        try:
            resp = _request("GET", url)
            data = resp.json()
            jobs = data.get("jobs", [])
            if name_contains:
                needle = name_contains.lower()
                jobs = [
                    j for j in jobs if (j.get("name") or "").lower().find(needle) != -1
                ]
            return json.dumps(
                {"jobs": jobs[:limit], "count": len(jobs[:limit]), "recursive": False}
            )
        except requests.RequestException as e:
            logging.error(f"Failed to list jobs: {e}")
            return json.dumps({"error": str(e)})
    else:
        # Recursive: use the helper function
        start_path = ""
        if folder:
            folder = folder.strip("/")
            if not folder.startswith("job/"):
                start_path = f"job/{folder}"
            else:
                start_path = folder

        all_jobs = _list_jobs_under(start_path)
        if name_contains:
            needle = name_contains.lower()
            all_jobs = [
                j for j in all_jobs if (j.get("name") or "").lower().find(needle) != -1
            ]
        return json.dumps(
            {
                "count": min(len(all_jobs), limit),
                "jobs": all_jobs[:limit],
                "recursive": True,
            }
        )


@mcp.tool()
def get_job_info(job_name: str) -> str:
    """Get detailed information about a specific Jenkins job.

    Args:
        job_name: Name of the Jenkins job

    Returns:
        JSON string with job details including builds, parameters, and configuration.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/api/json"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(data)
    except requests.RequestException as e:
        logging.error(f"Failed to get job info for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_job_description(job_name: str) -> str:
    """Get job description text."""
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/api/json?tree=description"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps({"job": job_name, "description": data.get("description")})
    except requests.RequestException as e:
        logging.error(f"Failed to get job description for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def update_job_description(job_name: str, description: str) -> str:
    """Update job description by modifying config.xml.

    Attempts POST to config.xml; retries with crumb header if required.
    """
    normalized_path = _normalize_job_path(job_name)
    get_url = f"{SERVICE_BASE_URL}/{normalized_path}/config.xml"
    try:
        cfg_resp = _request("GET", get_url, headers={"Accept": "application/xml"})
        root = ET.fromstring(cfg_resp.text)
        desc_el = root.find("description")
        if desc_el is None:
            desc_el = ET.SubElement(root, "description")
        desc_el.text = description
        updated_xml = ET.tostring(root, encoding="utf-8")

        try:
            post_resp = _request(
                "POST",
                get_url,
                data=updated_xml,
                headers={"Content-Type": "application/xml"},
            )
            return json.dumps(
                {"job": job_name, "status": "updated", "code": post_resp.status_code}
            )
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 403:
                crumb = _get_crumb()
                if crumb:
                    headers = {
                        "Content-Type": "application/xml",
                        crumb["field"]: crumb["crumb"],
                    }
                    post_resp = _request(
                        "POST", get_url, data=updated_xml, headers=headers
                    )
                    return json.dumps(
                        {
                            "job": job_name,
                            "status": "updated",
                            "code": post_resp.status_code,
                        }
                    )
            raise
    except requests.RequestException as e:
        logging.error(f"Failed to update job description for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_build_info(job_name: str, build_number: int) -> str:
    """Get detailed information about a specific build.

    Args:
        job_name: Name of the Jenkins job
        build_number: Build number to query

    Returns:
        JSON string with build details including status, duration, timestamp, and parameters.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/api/json"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(data)
    except requests.RequestException as e:
        logging.error(f"Failed to get build info for {job_name} #{build_number}: {e}")
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def get_build_log(job_name: str, build_number: int, max_lines: int = 100) -> str:
    """Get console log output from a specific build.

    Args:
        job_name: Name of the Jenkins job
        build_number: Build number to query
        max_lines: Maximum number of lines to return (default: 100)

    Returns:
        JSON string with console log text.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/consoleText"
    try:
        resp = _request("GET", url)
        log_text = resp.text
        lines = log_text.split("\n")
        if len(lines) > max_lines:
            lines = lines[-max_lines:]
            truncated = True
        else:
            truncated = False

        return json.dumps(
            {
                "log": "\n".join(lines),
                "truncated": truncated,
                "total_lines": len(log_text.split("\n")),
                "returned_lines": len(lines),
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to get build log for {job_name} #{build_number}: {e}")
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def get_last_build(job_name: str) -> str:
    """Get information about the last build of a job.

    Args:
        job_name: Name of the Jenkins job

    Returns:
        JSON string with last build details.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/lastBuild/api/json"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(data)
    except requests.RequestException as e:
        logging.error(f"Failed to get last build for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_system_info() -> str:
    """Get Jenkins system information and queue stats."""
    try:
        root_resp = _request("GET", f"{SERVICE_BASE_URL}/api/json")
        root = root_resp.json()
        queue_resp = _request("GET", f"{SERVICE_BASE_URL}/queue/api/json")
        queue = queue_resp.json()
        return json.dumps(
            {
                "core": {
                    "nodeName": root.get("nodeName"),
                    "numExecutors": root.get("numExecutors"),
                    "mode": root.get("mode"),
                    "quietingDown": root.get("quietingDown"),
                    "jenkins_version": root.get("version"),
                },
                "queue": {"length": len(queue.get("items", []))},
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to get system info: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_plugins() -> str:
    """List installed plugins with versions."""
    url = f"{SERVICE_BASE_URL}/pluginManager/api/json?tree=plugins[shortName,longName,version,enabled,active]"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps({"plugins": data.get("plugins", [])})
    except requests.RequestException as e:
        logging.error(f"Failed to get plugins: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def trigger_build(job_name: str, parameters: Optional[str] = None) -> str:
    """Trigger a new build for a Jenkins job.

    Args:
        job_name: Name of the Jenkins job
        parameters: Optional JSON string of build parameters (e.g., '{"param1": "value1", "param2": "value2"}')

    Returns:
        JSON string with trigger status and queue URL.
    """
    normalized_path = _normalize_job_path(job_name)
    if parameters:
        try:
            params = json.loads(parameters)
            url = f"{SERVICE_BASE_URL}/{normalized_path}/buildWithParameters"
        except json.JSONDecodeError as e:
            return json.dumps({"error": f"Invalid JSON parameters: {e}"})
    else:
        params = {}
        url = f"{SERVICE_BASE_URL}/{normalized_path}/build"

    try:
        resp = _request("POST", url, params=params)
        queue_url = resp.headers.get("Location", "")
        return json.dumps(
            {
                "status": "triggered",
                "job": job_name,
                "queue_url": queue_url,
                "code": resp.status_code,
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to trigger build for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_build_history(
    job_name: str,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    fetch_limit: int = 500,
) -> str:
    """Get build history with optional date range filtering.

    Args:
        job_name: Jenkins job path
        from_time: Optional ISO8601 or epoch ms string to include builds after this time
        to_time: Optional ISO8601 or epoch ms string to include builds before this time
        fetch_limit: Maximum number of builds to fetch from Jenkins API
    """
    normalized_path = _normalize_job_path(job_name)
    url = (
        f"{SERVICE_BASE_URL}/{normalized_path}/api/json?"
        f"tree=builds[number,result,timestamp,duration,url]{{0,{fetch_limit}}}"
    )
    try:
        resp = _request("GET", url)
        data = resp.json()
        builds = data.get("builds", [])

        def parse_to_ms(value: Optional[str]) -> Optional[int]:
            if not value:
                return None
            try:
                return int(value)
            except ValueError:
                try:
                    dt = datetime_from_any(value)
                    return int(dt.timestamp() * 1000)
                except Exception:
                    return None

        def datetime_from_any(s: str):
            # Try ISO formats
            from datetime import datetime

            for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    continue
            return datetime.fromisoformat(s)

        from_ms = parse_to_ms(from_time)
        to_ms = parse_to_ms(to_time)

        if from_ms is not None:
            builds = [b for b in builds if (b.get("timestamp") or 0) >= from_ms]
        if to_ms is not None:
            builds = [b for b in builds if (b.get("timestamp") or 0) <= to_ms]

        return json.dumps(
            {
                "job": job_name,
                "count": len(builds),
                "builds": builds,
                "from": from_ms,
                "to": to_ms,
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to get build history for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_last_successful_build(job_name: str) -> str:
    """Get last successful build details."""
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/lastSuccessfulBuild/api/json"
    try:
        resp = _request("GET", url)
        return json.dumps(resp.json())
    except requests.RequestException as e:
        logging.error(f"Failed to get last successful build for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_last_failed_build(job_name: str) -> str:
    """Get last failed build details."""
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/lastFailedBuild/api/json"
    try:
        resp = _request("GET", url)
        return json.dumps(resp.json())
    except requests.RequestException as e:
        logging.error(f"Failed to get last failed build for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def download_artifact(
    job_name: str,
    build_number: int,
    file_name: Optional[str] = None,
    relative_path: Optional[str] = None,
    as_base64: bool = True,
    max_bytes: Optional[int] = None,
) -> str:
    """Download an artifact from a build.

    Provide either file_name or relative_path. Returns base64 content by default.
    """
    normalized_path = _normalize_job_path(job_name)
    try:
        if not relative_path:
            art_resp = _request(
                "GET",
                f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/api/json?tree=artifacts[fileName,relativePath]",
            )
            arts = art_resp.json().get("artifacts", [])
            match = None
            if file_name:
                for a in arts:
                    if a.get("fileName") == file_name:
                        match = a
                        break
            else:
                if arts:
                    match = arts[0]
            if not match:
                return json.dumps(
                    {
                        "error": "Artifact not found",
                        "job": job_name,
                        "build": build_number,
                        "file_name": file_name,
                    }
                )
            relative_path = match.get("relativePath")

        url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/artifact/{relative_path}"
        resp = _request("GET", url)
        content = resp.content
        if max_bytes is not None and len(content) > max_bytes:
            content = content[:max_bytes]
            truncated = True
        else:
            truncated = False
        payload = base64.b64encode(content).decode("ascii") if as_base64 else None
        return json.dumps(
            {
                "job": job_name,
                "build": build_number,
                "relativePath": relative_path,
                "size": len(content),
                "truncated": truncated,
                "contentBase64": payload,
                "downloadUrl": url,
            }
        )
    except requests.RequestException as e:
        logging.error(
            f"Failed to download artifact for {job_name} #{build_number}: {e}"
        )
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def replay_pipeline(
    job_name: str, build_number: int, script: Optional[str] = None
) -> str:
    """Replay a pipeline build. Requires Replay plugin.

    If script is provided, attempts to use it for replay; otherwise replays as-is.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/replay"
    data = {}
    if script is not None:
        data["script"] = script
    data["Submit"] = "Replay"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        resp = _request("POST", url, data=data, headers=headers)
        return json.dumps(
            {
                "job": job_name,
                "build": build_number,
                "status": "requested",
                "code": resp.status_code,
            }
        )
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            crumb = _get_crumb()
            if crumb:
                headers[crumb["field"]] = crumb["crumb"]
                resp = _request("POST", url, data=data, headers=headers)
                return json.dumps(
                    {
                        "job": job_name,
                        "build": build_number,
                        "status": "requested",
                        "code": resp.status_code,
                    }
                )
        if e.response is not None and e.response.status_code == 404:
            return json.dumps(
                {
                    "error": "Replay endpoint not available. Ensure Replay plugin is installed.",
                    "job": job_name,
                    "build": build_number,
                }
            )
        logging.error(f"Failed to replay pipeline for {job_name} #{build_number}: {e}")
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


def _job_path_to_blue(job_path: str) -> str:
    parts = [p for p in job_path.split("/") if p and p != "job"]
    return "/".join(
        [
            "blue",
            "rest",
            "organizations",
            "jenkins",
            "pipelines",
            "/pipelines/".join(parts),
        ]
    )


@mcp.tool()
def get_pipeline_run_details(job_name: str, build_number: int) -> str:
    """Get Blue Ocean style pipeline run details, fallback to wfapi."""
    normalized_path = _normalize_job_path(job_name)
    try:
        blue_path = _job_path_to_blue(job_name)
        url = f"{SERVICE_BASE_URL}/{blue_path}/runs/{build_number}/"
        resp = _request("GET", url)
        return json.dumps(resp.json())
    except requests.RequestException:
        # Fallback to wfapi
        try:
            wf_url = (
                f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/wfapi/describe"
            )
            wf_resp = _request("GET", wf_url)
            data = wf_resp.json()
            return json.dumps({"source": "wfapi", **data})
        except requests.RequestException as e2:
            logging.error(
                f"Failed to get pipeline run details for {job_name} #{build_number}: {e2}"
            )
            return json.dumps(
                {"error": str(e2), "job": job_name, "build": build_number}
            )


@mcp.tool()
def search_builds(
    job_name: str, result_filter: Optional[str] = None, limit: int = 10
) -> str:
    """Search recent builds of a job with optional result filtering.

    Args:
        job_name: Name of the Jenkins job
        result_filter: Optional filter by result (SUCCESS, FAILURE, UNSTABLE, ABORTED)
        limit: Maximum number of builds to return (default: 10)

    Returns:
        JSON string with list of matching builds.
    """
    normalized_path = _normalize_job_path(job_name)
    url = (
        f"{SERVICE_BASE_URL}/{normalized_path}/api/json?"
        f"tree=builds[number,result,timestamp,duration,url]{{0,{limit}}}"
    )
    try:
        resp = _request("GET", url)
        data = resp.json()
        builds = data.get("builds", [])

        if result_filter:
            builds = [b for b in builds if b.get("result") == result_filter.upper()]

        return json.dumps(
            {"builds": builds, "count": len(builds), "filter": result_filter}
        )
    except requests.RequestException as e:
        logging.error(f"Failed to search builds for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def stop_build(job_name: str, build_number: int) -> str:
    """Stop/abort a running build.

    Args:
        job_name: Name/path of the Jenkins job (use nested path like "folder/job/sub/job/name" if needed)
        build_number: Build number to stop

    Returns:
        JSON with operation status and HTTP code.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/stop"
    try:
        resp = _request("POST", url)
        return json.dumps(
            {
                "status": "requested",
                "job": job_name,
                "build": build_number,
                "code": resp.status_code,
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to stop build for {job_name} #{build_number}: {e}")
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def get_build_changes(job_name: str, build_number: int) -> str:
    """Get SCM changesets associated with a specific build.

    Returns changeSets array when available.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/api/json?tree=changeSets[*[*]]"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(
            {
                "job": job_name,
                "build": build_number,
                "changeSets": data.get("changeSets", []),
            }
        )
    except requests.RequestException as e:
        logging.error(
            f"Failed to get build changes for {job_name} #{build_number}: {e}"
        )
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def get_build_artifacts(
    job_name: str, build_number: int, include_urls: bool = True
) -> str:
    """List artifacts produced by a build, optionally adding absolute download URLs.

    Args:
        job_name: Jenkins job path
        build_number: Build number
        include_urls: Whether to include absolute artifact URLs
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/api/json?tree=artifacts[fileName,relativePath]"
    try:
        resp = _request("GET", url)
        data = resp.json()
        artifacts = data.get("artifacts", [])
        if include_urls:
            base = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/artifact/"
            for a in artifacts:
                rel = a.get("relativePath", "")
                a["url"] = base + rel
        return json.dumps(
            {"job": job_name, "build": build_number, "artifacts": artifacts}
        )
    except requests.RequestException as e:
        logging.error(f"Failed to get artifacts for {job_name} #{build_number}: {e}")
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def get_pipeline_stages(job_name: str, build_number: int) -> str:
    """Get detailed pipeline stage information for a specific build.

    Requires Workflow API (wfapi) plugin.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/{build_number}/wfapi/describe"
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(data)
    except requests.RequestException as e:
        logging.error(
            f"Failed to get pipeline stages for {job_name} #{build_number}: {e}"
        )
        return json.dumps({"error": str(e), "job": job_name, "build": build_number})


@mcp.tool()
def get_nodes() -> str:
    """List Jenkins nodes/agents and their status."""
    url = f"{SERVICE_BASE_URL}/computer/api/json"
    try:
        resp = _request("GET", url)
        return json.dumps(resp.json())
    except requests.RequestException as e:
        logging.error(f"Failed to get nodes: {e}")
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_node_info(node_name: str) -> str:
    """Get details about a specific node.

    Note: Built-in node can be addressed as "(built-in)" or may be named "master" on older setups.
    """
    url = f"{SERVICE_BASE_URL}/computer/{node_name}/api/json"
    try:
        resp = _request("GET", url)
        return json.dumps(resp.json())
    except requests.RequestException as e:
        logging.error(f"Failed to get node info for {node_name}: {e}")
        return json.dumps({"error": str(e), "node": node_name})


def _list_jobs_under(path: str = "", max_workers: int = 10) -> list:
    """Recursively list jobs starting from optional folder path using parallel requests.

    Returns a flat list of job dictionaries with minimal fields.
    """
    if path:
        url = f"{SERVICE_BASE_URL}/{path}/api/json?tree=jobs[_class,name,url,color]"
    else:
        url = f"{SERVICE_BASE_URL}/api/json?tree=jobs[_class,name,url,color]"

    try:
        resp = _request("GET", url)
        data = resp.json()
        results = []
        folders_to_scan = []

        for j in data.get("jobs", []):
            job_class = j.get("_class", "")
            job_name = j.get("name", "")
            full_path = f"{path}/job/{job_name}" if path else f"job/{job_name}"

            results.append(
                {
                    "_class": job_class,
                    "name": job_name,
                    "url": j.get("url"),
                    "color": j.get("color"),
                    "fullPath": full_path,
                }
            )

            # Collect folders to scan in parallel
            if "Folder" in job_class:
                folders_to_scan.append(full_path)

        # Process all folders in parallel
        if folders_to_scan:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_path = {
                    executor.submit(
                        _list_jobs_under, folder_path, max_workers
                    ): folder_path
                    for folder_path in folders_to_scan
                }
                for future in as_completed(future_to_path):
                    try:
                        sub_results = future.result()
                        results.extend(sub_results)
                    except Exception as e:
                        folder = future_to_path[future]
                        logging.error(f"Error scanning folder {folder}: {e}")

        return results
    except requests.RequestException as e:
        logging.error(f"Failed to list jobs under {path}: {e}")
        return []


@mcp.tool()
def get_job_config(job_name: str) -> str:
    """Get job configuration XML for a given job.

    Returns the raw XML as string in the 'configXml' field.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/config.xml"
    try:
        resp = _request("GET", url, headers={"Accept": "application/xml"})
        return json.dumps({"job": job_name, "configXml": resp.text})
    except requests.RequestException as e:
        logging.error(f"Failed to get job config for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def get_job_metrics(job_name: str, limit: int = 20) -> str:
    """Compute simple metrics for a job across recent builds.

    Metrics: total builds scanned, success rate, average duration (ms), last build number/result.
    """
    normalized_path = _normalize_job_path(job_name)
    url = f"{SERVICE_BASE_URL}/{normalized_path}/api/json?tree=builds[number,result,duration,timestamp]{{0,{limit}}}"
    try:
        resp = _request("GET", url)
        data = resp.json()
        builds = data.get("builds", [])
        n = len(builds)
        if n == 0:
            return json.dumps(
                {
                    "job": job_name,
                    "count": 0,
                    "successRate": None,
                    "avgDuration": None,
                    "last": None,
                }
            )
        successes = sum(1 for b in builds if b.get("result") == "SUCCESS")
        durations = [b.get("duration") or 0 for b in builds]
        avg = sum(durations) / max(n, 1)
        last = max(builds, key=lambda b: b.get("number", 0))
        return json.dumps(
            {
                "job": job_name,
                "count": n,
                "successRate": successes / n,
                "avgDuration": avg,
                "last": last,
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to compute job metrics for {job_name}: {e}")
        return json.dumps({"error": str(e), "job": job_name})


@mcp.tool()
def list_credentials(store: str = "system", domain: str = "_") -> str:
    """Best-effort listing of Jenkins credentials metadata (requires appropriate permissions).

    Notes:
    - Standard Jenkins doesn't expose expiry dates for credentials by default.
    - This returns whatever metadata is available via the Credentials plugin API.
    - System store/domain path: /credentials/store/{store}/domain/{domain}/api/json
    """
    url = (
        f"{SERVICE_BASE_URL}/credentials/store/{store}/domain/{domain}/api/json?"
        "tree=credentials[id,name,displayName,typeName,description]"
    )
    try:
        resp = _request("GET", url)
        data = resp.json()
        return json.dumps(
            {
                "store": store,
                "domain": domain,
                "credentials": data.get("credentials", []),
            }
        )
    except requests.RequestException as e:
        logging.error(f"Failed to list credentials: {e}")
        return json.dumps({"error": str(e), "store": store, "domain": domain})


@mcp.tool()
def search_job(job_name: str, exact_match: bool = False) -> str:
    """Search for jobs across the entire Jenkins instance by name and return detailed information.

    Args:
        job_name: Job name to search for (case-insensitive partial match unless exact_match=True)
        exact_match: If True, only return exact name matches. If False, return partial matches (default: False)

    Returns:
        JSON string with list of matching jobs including full path, URL, status, build count,
        last build info, and success rate.
    """
    # Get all jobs from the instance
    all_jobs = _list_jobs_under("")

    # Filter by name
    needle = job_name.lower()
    if exact_match:
        matching_jobs = [j for j in all_jobs if j.get("name", "").lower() == needle]
    else:
        matching_jobs = [j for j in all_jobs if needle in j.get("name", "").lower()]

    if not matching_jobs:
        return json.dumps({"query": job_name, "matches": 0, "jobs": []})

    # Fetch detailed info for each match in parallel
    detailed_jobs = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_job = {
            executor.submit(_get_job_details, job["fullPath"]): job
            for job in matching_jobs
        }

        for future in as_completed(future_to_job):
            job_info = future_to_job[future]
            try:
                details = future.result()
                if details:
                    detailed_jobs.append(
                        {
                            "name": job_info["name"],
                            "fullPath": job_info["fullPath"],
                            "url": job_info["url"],
                            "status": job_info.get("color"),
                            **details,
                        }
                    )
            except Exception as e:
                logging.error(f"Error fetching details for {job_info['name']}: {e}")
                detailed_jobs.append(
                    {
                        "name": job_info["name"],
                        "fullPath": job_info["fullPath"],
                        "url": job_info["url"],
                        "status": job_info.get("color"),
                        "error": str(e),
                    }
                )

    return json.dumps(
        {"query": job_name, "matches": len(detailed_jobs), "jobs": detailed_jobs}
    )


def _get_job_details(job_path: str) -> dict:
    """Fetch detailed information for a specific job path.

    Returns dict with build count, last build info, and metrics.
    Note: job_path should already be in normalized format from _list_jobs_under.
    """
    # job_path from _list_jobs_under is already in 'job/folder/job/name' format
    url = (
        f"{SERVICE_BASE_URL}/{job_path}/api/json?"
        "tree=builds[number,result,timestamp,duration],lastBuild[number,result,timestamp],color"
    )
    try:
        resp = _request("GET", url)
        data = resp.json()

        builds = data.get("builds", [])
        build_count = len(builds)

        # Calculate metrics
        last_build = data.get("lastBuild")
        if builds:
            successes = sum(1 for b in builds if b.get("result") == "SUCCESS")
            success_rate = successes / build_count if build_count > 0 else 0

            durations = [b.get("duration", 0) for b in builds if b.get("duration")]
            avg_duration = sum(durations) / len(durations) if durations else 0
        else:
            success_rate = None
            avg_duration = None

        return {
            "buildCount": build_count,
            "lastBuild": last_build,
            "successRate": success_rate,
            "avgDuration": avg_duration,
        }
    except requests.RequestException as e:
        logging.error(f"Failed to get details for {job_path}: {e}")
        return {}


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
