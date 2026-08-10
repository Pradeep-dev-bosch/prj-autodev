"""MCP server for ARC (Automatic Release Checker).

This server provides integration with ARC, an automated QG questionnaire evaluation system,
ensuring compliance with DROP (Delivery Release of Product) guidelines.

Features:
- ARC release check execution with interactive parameters
- HTML report analysis and quality gate summarization
- Full environment variable configuration via mcp.json

Environment Variables (set in mcp.json):
========================================
Required:
- ARC_WORKSPACE: Root workspace path for reports
  Example: /home/user/pmt-mcp-servers

Prompted at Runtime (via ${input:VAR}):
- TECH_USERNAME: Technical username for Artifactory
- JFROG_TOKEN: JFrog authentication token
- SHAREPOINT_USERNAME: SharePoint username
- SHAREPOINT_PASSWORD: SharePoint password
- SQL_TECH_PASSWORD: SQL technical password
- ONEQ_API_KEY: OneQ API key
- ONEQ_SECRET: OneQ secret
- SPLUNK_USERNAME: Splunk username
- SPLUNK_PASSWORD: Splunk password
- JIRA_TOKEN: Jira token
- DOCUPEDIA_TOKEN: Docupedia token
- BU: Business unit code
- CERT_PATH: SSL certificate configuration (optional)
    - Empty/unset: Use system certificates (secure default)
    - false/disable/off/no: Disable SSL verification (dev/test only)
    - Absolute path: Use custom CA bundle

Optional:
- TRANSPORT: Transport type, defaults to 'stdio'
- HOST: Host for non-stdio transport, defaults to '127.0.0.1'
- HOST_PORT: Port for non-stdio transport, defaults to '8000'

Requirements:
- Python 3.13+
- FastMCP framework
- BeautifulSoup4 for HTML parsing
- ARC CLI tool (v3.5)
"""

import asyncio
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

from fastmcp import FastMCP
from pydantic import Field
from bs4 import BeautifulSoup

mcp = FastMCP("ARC")

# Global configuration
ARC_WORKSPACE = None


def initialize_arc():
    """Initialize ARC configuration and validate required environment variables.
    
    Raises:
        ValueError: If ARC_WORKSPACE is not set
    """
    global ARC_WORKSPACE
    
    ARC_WORKSPACE = os.getenv("ARC_WORKSPACE")
    
    if not ARC_WORKSPACE:
        raise ValueError("Missing required environment variable: ARC_WORKSPACE")
    
    # Auto-create workspace directory if it doesn't exist
    workspace_path = Path(ARC_WORKSPACE)
    if not workspace_path.exists():
        logging.info(f"Creating ARC workspace directory: {workspace_path}")
        workspace_path.mkdir(parents=True, exist_ok=True)

    # Apply certificate configuration to the Python requests environment so that
    # FastMCP internals and any future direct HTTP calls respect the same cert
    # setting used by the ARC CLI subprocess (mirrors Jenkins SSL_VERIFY behaviour).
    cert_path = get_cert_path()
    if cert_path.lower() in ["false", "disable", "off", "no"]:
        # Disable SSL verification — remove CA bundle env vars to avoid confusion
        os.environ.pop("REQUESTS_CA_BUNDLE", None)
        os.environ.pop("CURL_CA_BUNDLE", None)
        logging.warning("SSL verification disabled via CERT_PATH (dev/test only)")
    elif cert_path:
        # Custom CA bundle — propagate to requests / curl layer
        os.environ["REQUESTS_CA_BUNDLE"] = cert_path
        os.environ["CURL_CA_BUNDLE"] = cert_path
        logging.info(f"SSL: Using custom CA bundle from CERT_PATH: {cert_path}")
    else:
        # Empty CERT_PATH → keep REQUESTS_CA_BUNDLE set by Dockerfile (system certs)
        logging.info("SSL: Using system CA bundle (REQUESTS_CA_BUNDLE from environment)")

    logging.info(f"ARC initialized with workspace: {ARC_WORKSPACE}")


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.
    
    Returns:
        Tuple of (transport, host, port)
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
        raise ValueError(f"Invalid HOST_PORT env variable: '{port_str}' - must be a valid integer")
    
    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def get_arc_workspace() -> Path:
    """Get ARC workspace path from global configuration.
    
    Returns:
        Path object for the workspace
        
    Raises:
        RuntimeError: If ARC_WORKSPACE is not initialized
    """
    if not ARC_WORKSPACE:
        raise RuntimeError("ARC not initialized. Call initialize_arc() first.")
    
    workspace = Path(ARC_WORKSPACE)
    # Auto-create workspace directory if it doesn't exist
    if not workspace.exists():
        logging.info(f"Creating workspace directory: {workspace}")
        workspace.mkdir(parents=True, exist_ok=True)
    
    return workspace


def get_cert_path() -> str:
    """Get certificate configuration from environment.

    Returns:
        CERT_PATH value as-is (empty string if unset)

    Notes:
        - Empty/unset -> system certificate store
        - false/disable/off/no -> disable SSL verification (dev/test only)
        - Any other value -> custom certificate path
    """
    return (os.getenv("CERT_PATH") or "").strip()


def get_ssl_verify():
    """Derive a requests-compatible SSL verify value from CERT_PATH.

    Mirrors the SSL_VERIFY pattern used in jenkinsmcpserver.py but supports
    the richer ARC CERT_PATH semantics (disable keyword, custom path, or empty).

    Returns:
        False  — SSL verification is disabled (CERT_PATH is a disable keyword)
        str    — path to custom CA bundle (CERT_PATH is an absolute path)
        True   — use default/system certificate store (CERT_PATH is empty)
    """
    cert_path = get_cert_path()
    if cert_path.lower() in ["false", "disable", "off", "no"]:
        return False
    if cert_path:
        return cert_path
    return True


async def run_arc_command(
    cmd: list[str], 
    timeout: float = 300.0,
    cwd: Optional[str] = None,
    env_vars: Optional[dict[str, str]] = None,
    stream_output: bool = True
) -> tuple[str, str, int]:
    """Execute an ARC command and return output with optional real-time streaming.
    
    Args:
        cmd: List of command arguments (e.g., ["arc", "--release-name", "550_SW"])
        timeout: Timeout in seconds (default 300s for release checks)
        cwd: Working directory (defaults to ARC_WORKSPACE)
        env_vars: Additional environment variables to pass
        stream_output: If True, logs output in real-time (default True)
        
    Returns:
        Tuple of (stdout, stderr, return_code)
        
    Raises:
        RuntimeError: If command fails or times out
    """
    if cwd is None:
        cwd = os.environ.get("ARC_WORKSPACE", str(get_arc_workspace()))
    
    # Build environment with ARC variables
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    proc = None
    try:
        logging.info(f"Running command: {' '.join(cmd)}")
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL,
            cwd=cwd,
            env=env,
        )
        
        stdout_lines = []
        stderr_lines = []
        
        async def read_stream(stream, is_stderr=False):
            """Read stream line by line and log progress."""
            lines = stderr_lines if is_stderr else stdout_lines
            while True:
                line = await stream.readline()
                if not line:
                    break
                decoded = line.decode("utf-8", "replace").rstrip()
                lines.append(decoded)
                
                if stream_output:
                    # Log important progress indicators
                    lower = decoded.lower()
                    if any(keyword in lower for keyword in [
                        'fetching', 'search job', 'created', 'processing', 
                        'building', 'generating', 'complete', 'error', 'warning'
                    ]):
                        log_func = logging.warning if is_stderr or 'error' in lower else logging.info
                        log_func(f"ARC: {decoded}")
        
        try:
            # Read both streams concurrently
            await asyncio.wait_for(
                asyncio.gather(
                    read_stream(proc.stdout, False),
                    read_stream(proc.stderr, True),
                    proc.wait()
                ),
                timeout=timeout
            )
            
            return (
                "\n".join(stdout_lines),
                "\n".join(stderr_lines),
                proc.returncode
            )
        except asyncio.TimeoutError:
            if proc:
                proc.kill()
                await proc.wait()
            logging.error(f"Command timeout after {timeout}s")
            raise RuntimeError(f"ARC command timeout after {timeout}s")
            
    except Exception as e:
        if proc:
            try:
                proc.kill()
            except:
                pass
        logging.error(f"Error running ARC command: {e}")
        raise


def parse_html_report(html_path: Path) -> dict[str, Any]:
    """Parse ARC HTML report and extract quality gate information.
    
    Args:
        html_path: Path to the HTML report file
        
    Returns:
        Dictionary containing parsed report data
    """
    if not html_path.exists():
        raise FileNotFoundError(f"Report not found at {html_path}")
    
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        raise RuntimeError(f"Could not read HTML report: {e}")
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    report_data = {
        "title": "",
        "generation_date": "",
        "dry_run": False,
        "evaluations": [],
        "summary": {
            "total_checks": 0,
            "red_count": 0,
            "yellow_count": 0,
            "green_count": 0,
            "no_rating_count": 0,
        }
    }
    
    # Extract title and metadata
    title_elem = soup.find("h1")
    if title_elem:
        report_data["title"] = title_elem.get_text(strip=True)
    
    # Find generation date
    meta_paragraph = soup.find("p")
    if meta_paragraph:
        meta_text = meta_paragraph.get_text()
        if "generated on" in meta_text:
            report_data["generation_date"] = meta_text
    
    # Check for dry run
    if "Dry Run Report" in html_content:
        report_data["dry_run"] = True
    
    # Extract all h2 headers (question IDs)
    h2_elements = soup.find_all("h2")
    for h2 in h2_elements:
        h2_text = h2.get_text(strip=True)
        
        # Skip if this is not a question (e.g., "Evaluation")
        if not h2_text or not h2_text[0].isalpha() or h2_text.lower() == "evaluation":
            continue
        
        question_id = h2_text.split()[0]
        
        # Determine status from image or color
        status = "unknown"
        img = h2.find("img")
        if img:
            img_src = img.get("src", "")
            if "red.png" in img_src:
                status = "red"
                report_data["summary"]["red_count"] += 1
            elif "yellow.png" in img_src:
                status = "yellow"
                report_data["summary"]["yellow_count"] += 1
            elif "green.png" in img_src:
                status = "green"
                report_data["summary"]["green_count"] += 1
            elif "no_rating.png" in img_src:
                status = "no_rating"
                report_data["summary"]["no_rating_count"] += 1
        
        # Find full question text (remove question ID and image)
        question_text = h2_text
        for img_tag in h2.find_all("img"):
            img_tag.extract()
        question_full = h2.get_text(strip=True)
        
        # Find description (p tag after h2)
        description = ""
        p_elem = h2.find_next("p")
        if p_elem and not p_elem.find("strong"):
            description = p_elem.get_text(strip=True)
        
        # Extract rating if present
        rating_text = ""
        for p in h2.find_next_siblings("p"):
            p_text = p.get_text()
            if "Rating" in p_text:
                rating_text = p_text
                break
        
        # Find table with details
        table = h2.find_next("table")
        details = []
        if table:
            rows = table.find_all("tr")[1:]  # Skip header
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 5:
                    # Extract status color from span if present
                    status_cell = cells[1]
                    status_span = status_cell.find("span")
                    cell_status = status_span.get_text(strip=True) if status_span else cells[1].get_text(strip=True)
                    
                    detail = {
                        "sub_topic": cells[0].get_text(strip=True),
                        "status": cell_status,
                        "check": cells[2].get_text(strip=True),
                        "expected": cells[3].get_text(strip=True),
                        "remarks": cells[4].get_text(strip=True),
                    }
                    details.append(detail)
        
        evaluation = {
            "question_id": question_id,
            "question_text": question_full,
            "status": status,
            "rating": rating_text,
            "description": description,
            "details": details,
        }
        report_data["evaluations"].append(evaluation)
        report_data["summary"]["total_checks"] += 1
    
    return report_data


def format_report_summary(report_data: dict[str, Any]) -> str:
    """Format parsed report data into a readable summary with actionable insights.
    
    Args:
        report_data: Parsed report data dictionary
        
    Returns:
        Formatted summary string with key insights and recommendations
    """
    summary = []
    summary.append(f"# 🎯 ARC Quality Gate Report Analysis\n")
    summary.append(f"**Project**: {report_data['title']}")
    summary.append(f"**Generated**: {report_data['generation_date']}")
    summary.append(f"**Report Type**: {'🔍 Dry Run (Preview)' if report_data['dry_run'] else '✅ Official Release'}\n")
    
    s = report_data["summary"]
    
    # Calculate release readiness score
    total_rated = s['red_count'] + s['yellow_count'] + s['green_count']
    if total_rated > 0:
        readiness_score = ((s['green_count'] * 100 + s['yellow_count'] * 50) / total_rated)
        readiness_emoji = "🟢" if readiness_score >= 80 else "🟡" if readiness_score >= 50 else "🔴"
    else:
        readiness_score = 0
        readiness_emoji = "⚪"
    
    summary.append(f"## 📊 Release Readiness Score: {readiness_emoji} {readiness_score:.1f}%\n")
    
    summary.append(f"## 📈 Quality Gate Summary")
    summary.append(f"```")
    summary.append(f"Total Questions Evaluated: {s['total_checks']}")
    summary.append(f"├─ 🔴 Red (Critical Issues):     {s['red_count']:>3} ({s['red_count']/s['total_checks']*100 if s['total_checks'] > 0 else 0:.1f}%)")
    summary.append(f"├─ 🟡 Yellow (Warnings):         {s['yellow_count']:>3} ({s['yellow_count']/s['total_checks']*100 if s['total_checks'] > 0 else 0:.1f}%)")
    summary.append(f"├─ 🟢 Green (Passed):            {s['green_count']:>3} ({s['green_count']/s['total_checks']*100 if s['total_checks'] > 0 else 0:.1f}%)")
    summary.append(f"└─ ⚪ No Rating:                 {s['no_rating_count']:>3}")
    summary.append(f"```\n")
    
    # Critical Issues (Red) - Most Important
    red_evals = [e for e in report_data["evaluations"] if e["status"] == "red"]
    if red_evals:
        summary.append(f"## 🔴 CRITICAL ISSUES - ACTION REQUIRED ({len(red_evals)} items)\n")
        
        # Extract key metrics and blockers
        blockers = []
        metrics = []
        
        for eval in red_evals:
            summary.append(f"### {eval['question_id']}: {eval.get('description', 'No description')[:80]}...")
            
            if eval['details']:
                action_items = []
                for detail in eval['details']:
                    status_text = detail.get('status', '')
                    remarks = detail.get('remarks', '')
                    
                    # Extract percentage/numeric metrics from remarks
                    percentage_match = re.search(r'(\d+)%', remarks)
                    if percentage_match:
                        pct = int(percentage_match.group(1))
                        if pct < 100:
                            metrics.append({
                                'question': eval['question_id'],
                                'topic': detail['sub_topic'],
                                'value': pct,
                                'remark': remarks
                            })
                    
                    # Check for errors or missing data
                    if 'error' in remarks.lower() or 'not available' in remarks.lower():
                        blockers.append({
                            'question': eval['question_id'],
                            'topic': detail['sub_topic'],
                            'issue': remarks
                        })
                    
                    if 'action required' in status_text.lower():
                        action_items.append(f"  - **{detail['sub_topic']}**: {remarks[:150]}")
                
                if action_items:
                    for item in action_items[:3]:  # Show top 3 action items
                        summary.append(item)
                    if len(action_items) > 3:
                        summary.append(f"  - *...and {len(action_items) - 3} more action items*")
            summary.append("")
        
        # Show critical metrics that need attention
        if metrics:
            summary.append(f"\n### 📉 Key Metrics Requiring Attention\n")
            for m in sorted(metrics, key=lambda x: x['value'])[:5]:  # Top 5 worst metrics
                summary.append(f"- **{m['question']} - {m['topic']}**: {m['value']}% (Target: 100%)")
                summary.append(f"  ↳ {m['remark'][:100]}")
        
        # Show blockers (missing data/errors)
        if blockers:
            summary.append(f"\n### ⚠️ Data Availability Issues ({len(blockers)} items)\n")
            for b in blockers[:5]:  # Top 5 blockers
                summary.append(f"- **{b['question']} - {b['topic']}**")
                summary.append(f"  ↳ {b['issue'][:120]}")
    
    # Warnings (Yellow)
    yellow_evals = [e for e in report_data["evaluations"] if e["status"] == "yellow"]
    if yellow_evals:
        summary.append(f"\n## 🟡 WARNINGS - REVIEW RECOMMENDED ({len(yellow_evals)} items)\n")
        for eval in yellow_evals[:3]:  # Show top 3
            summary.append(f"### {eval['question_id']}: {eval.get('description', 'No description')[:80]}...")
            if eval['details']:
                for detail in eval['details'][:2]:
                    summary.append(f"- **{detail['sub_topic']}**: {detail.get('remarks', 'No remarks')[:100]}")
        if len(yellow_evals) > 3:
            summary.append(f"\n*...and {len(yellow_evals) - 3} more warnings*")
    
    # Success Items (Green)
    green_evals = [e for e in report_data["evaluations"] if e["status"] == "green"]
    if green_evals:
        summary.append(f"\n## 🟢 PASSED CHECKS ({len(green_evals)} items)\n")
        green_questions = [e['question_id'] for e in green_evals]
        summary.append(f"Questions passed: {', '.join(green_questions)}")
    
    # No Rating items
    no_rating = [e for e in report_data["evaluations"] if e["status"] == "no_rating"]
    if no_rating:
        summary.append(f"\n## ⚪ NOT RATED ({len(no_rating)} items)\n")
        for eval in no_rating[:2]:
            summary.append(f"- **{eval['question_id']}**: {eval.get('description', 'No description')[:80]}...")
    
    # Final recommendations
    summary.append(f"\n## 💡 RECOMMENDATIONS\n")
    if s['red_count'] > 0:
        summary.append(f"1. **CRITICAL**: Address all {s['red_count']} red-flagged quality gates before release")
        if blockers:
            summary.append(f"2. **DATA**: Resolve {len(blockers)} data availability issues to complete evaluation")
        if metrics:
            summary.append(f"3. **METRICS**: Improve coverage metrics - {len([m for m in metrics if m['value'] < 95])} items below 95%")
    
    if s['yellow_count'] > 0:
        summary.append(f"4. **REVIEW**: Examine {s['yellow_count']} warning items for potential risks")
    
    if readiness_score >= 80:
        summary.append(f"\n✅ **Overall**: Project shows good readiness ({readiness_score:.1f}%). Focus on resolving critical items.")
    elif readiness_score >= 50:
        summary.append(f"\n⚠️ **Overall**: Project needs improvement ({readiness_score:.1f}%). Multiple quality gates require attention.")
    else:
        summary.append(f"\n🔴 **Overall**: Project is not ready for release ({readiness_score:.1f}%). Significant work required.")
    
    return "\n".join(summary)


@mcp.tool()
async def arc_validate_environment() -> str:
    """Validate ARC environment configuration.
    
    Checks that the workspace is accessible and lists configured credentials.
    Use this to verify environment setup before running ARC commands.
    
    Returns:
        Status message with environment validation details
    """
    try:
        workspace = get_arc_workspace()
        cert_path = get_cert_path()
        
        status = []
        status.append(f"✓ ARC Workspace: {workspace}")
        status.append(f"  - Exists: {'Yes' if workspace.exists() else 'No (will be created)'}")
        
        if not cert_path:
            status.append("✓ SSL: Using system certificates (CERT_PATH is empty/unset)")
        elif cert_path.lower() in ["false", "disable", "off", "no"]:
            status.append("⚠ SSL: Verification disabled via CERT_PATH (dev/test only)")
        else:
            status.append(f"✓ SSL: Using custom certificate path: {cert_path}")
            status.append(f"  - Exists: {'Yes' if Path(cert_path).exists() else 'No'}")
        
        # Check for configured credentials (don't show values)
        creds = []
        for var in ["TECH_USERNAME", "JFROG_TOKEN", "SHAREPOINT_USERNAME", "SHAREPOINT_PASSWORD",
                    "SQL_TECH_PASSWORD", "ONEQ_API_KEY", "ONEQ_SECRET", "SPLUNK_USERNAME",
                    "SPLUNK_PASSWORD", "JIRA_TOKEN", "DOCUPEDIA_TOKEN", "BU"]:
            if os.getenv(var):
                creds.append(var)
        
        status.append(f"\n✓ Configured credentials: {len(creds)}/12")
        if len(creds) < 12:
            missing = set(["TECH_USERNAME", "JFROG_TOKEN", "SHAREPOINT_USERNAME", "SHAREPOINT_PASSWORD",
                          "SQL_TECH_PASSWORD", "ONEQ_API_KEY", "ONEQ_SECRET", "SPLUNK_USERNAME",
                          "SPLUNK_PASSWORD", "JIRA_TOKEN", "DOCUPEDIA_TOKEN", "BU"]) - set(creds)
            status.append(f"⚠ Missing: {', '.join(sorted(missing))}")
        
        return "\n".join(status)
    except Exception as e:
        logging.error(f"Failed to validate environment: {e}")
        raise RuntimeError(f"Environment validation failed: {e}")


@mcp.tool()
async def arc_execute_command(
    project_name: str = Field(description="Project configuration name (e.g., VW_RADAR for VW_RADAR.yaml)"),
    release_name: str = Field(description="Current release name (e.g., 550_SW)"),
    prev_release_name: str = Field(description="Previous release name (e.g., 541_SW)"),
    splunk_bbm_metric_url: str = Field(description="Splunk BBM metrics dashboard URL (required)"),
    rt_level: str = Field(default="RT04", description="RT Level (e.g., RT04, RT05)"),
    release_type: str = Field(default="Product Release", description="Type of release (QG/Product release)"),
    dry_run: bool = Field(default=True, description="Enable dry-run mode (True/False)"),
    create_new_assessment: bool = Field(default=False, description="Create new assessment (True/False)"),
    docuplan_version: Optional[str] = Field(default=None, description="Version of document plan to use"),
) -> str:
    """Execute ARC release check command.
    
    WORKFLOW:
    1. Call arc_validate_environment first to check configuration
    2. Run this command to execute ARC release check
    3. Use arc_analyze_report to review generated reports
    
    Runs the ARC tool with specified parameters to evaluate quality gates
    and generate compliance reports in {ARC_WORKSPACE}/html/ and {ARC_WORKSPACE}/doctrees/.
    
    Args:
        project_name: Project configuration name (e.g., VW_RADAR)
        release_name: Current release name
        prev_release_name: Previous release name
        splunk_bbm_metric_url: Splunk BBM metrics dashboard URL (required)
        rt_level: RT level (default RT04)
        release_type: Type of release (default "Product Release")
        dry_run: Whether to run in dry-run mode (default True)
        create_new_assessment: Whether to create new assessment (default False)
        docuplan_version: Optional docuplan version
        
    Returns:
        ARC command output and status
    """
    try:
        # Verify and create workspace if needed
        workspace = get_arc_workspace()
        if not workspace.exists():
            logging.info(f"Creating workspace directory: {workspace}")
            workspace.mkdir(parents=True, exist_ok=True)
        logging.info(f"Running ARC in workspace: {workspace}")
    except Exception as e:
        raise RuntimeError(f"Environment not properly configured: {e}")
    
    # Build ARC command
    cmd = [
        "arc",
        "--release-name", release_name,
        "--prev-release-name", prev_release_name,
        "--rt", rt_level,
        "--release-type", release_type,
        "--dry-run", "Yes" if dry_run else "No",
        "--create-new-assessment", "Yes" if create_new_assessment else "No",
        
    ]
    
    if docuplan_version:
        cmd.extend(["--docuplan-version", docuplan_version])
    
    cmd.extend(["--splunk-bbm-metric-url", splunk_bbm_metric_url])
    
    # Prepare ARC required environment variables
    # CERT_PATH="" (our "use system certs" signal) is not accepted by the ARC CLI —
    # it requires a non-empty path. Resolve to the actual system CA bundle.
    cert_path = get_cert_path()
    if not cert_path:
        for candidate in [
            "/etc/ssl/certs/ca-certificates.crt",  # Debian/Ubuntu
            "/etc/pki/tls/certs/ca-bundle.crt",     # RHEL/CentOS
            "/etc/ssl/cert.pem",                     # macOS/Alpine
        ]:
            if Path(candidate).exists():
                cert_path = candidate
                logging.info(f"SSL: Resolved system cert bundle → {cert_path}")
                break

    arc_env = {
        "PROJECT_NAME": project_name,
        "CERT_PATH": cert_path,
        "PYTHON_EXEC": os.getenv("PYTHON_EXEC", sys.executable),
    }
    
    logging.info(f"🚀 Starting ARC execution for {project_name}")
    logging.info(f"📋 Release: {release_name} (previous: {prev_release_name})")
    logging.info(f"🔧 RT Level: {rt_level}, Mode: {'Dry-run' if dry_run else 'Live'}")
    logging.info(f"Executing ARC command: {' '.join(cmd)}")
    logging.info(f"PROJECT_NAME={project_name}, CERT_PATH={arc_env['CERT_PATH']}")
    logging.info("⏳ ARC execution in progress... (this may take 2-5 minutes)")
    
    try:
        stdout, stderr, returncode = await run_arc_command(cmd, env_vars=arc_env, stream_output=True)
        
        if returncode == 0:
            # Summarize output instead of including full command output
            result = f"✓ ARC command executed successfully\n\n"
            result += f"**Release**: {release_name} (previous: {prev_release_name})\n"
            result += f"**RT Level**: {rt_level}\n"
            result += f"**Mode**: {'Dry-run' if dry_run else 'Live'}\n"
            result += f"**Create New Assessment**: {'Yes' if create_new_assessment else 'No'}\n"
            result += f"**Reports Location**: {workspace}/html/\n\n"
            
            # Extract key information from output (last few lines typically contain summary)
            output_lines = stdout.strip().split('\n')
            if len(output_lines) > 10:
                # Show first 2 and last 5 lines as summary
                summary_lines = output_lines[:2] + ['...'] + output_lines[-5:]
                result += f"**Execution Summary** (truncated):\n" + '\n'.join(summary_lines)
            else:
                result += f"**Execution Summary**:\n{stdout}"
            
            if stderr:
                # Only show warnings if they exist, but keep them brief
                stderr_lines = stderr.strip().split('\n')
                if len(stderr_lines) <= 5:
                    result += f"\n\n**Warnings**:\n{stderr}"
                else:
                    result += f"\n\n**Warnings** ({len(stderr_lines)} lines): Check logs for details"
            
            result += f"\n\n💡 Use arc_analyze_report() to get detailed quality gate findings from the generated report."
            return result
        else:
            # For errors, show last 20 lines to keep it reasonable
            error_output = stderr if stderr else stdout
            error_lines = error_output.strip().split('\n')
            if len(error_lines) > 20:
                error_summary = '\n'.join(error_lines[-20:])
                return f"✗ ARC command failed with return code {returncode}\n\n**Error** (last 20 lines):\n{error_summary}"
            else:
                return f"✗ ARC command failed with return code {returncode}\n\n**Error**:\n{error_output}"
    except Exception as e:
        logging.error(f"Failed to execute ARC command: {e}")
        raise RuntimeError(f"ARC execution failed: {e}")


@mcp.tool()
async def arc_analyze_report(
    report_path: Optional[str] = Field(
        default=None,
        description="Path to HTML report (default: html/report.html in ARC_WORKSPACE)"
    )
) -> str:
    """Analyze ARC HTML report and provide actionable quality gate insights.
    
    WORKFLOW:
    1. Call arc_execute_command to run ARC and generate reports
    2. Call this tool to get comprehensive analysis with actionable recommendations
    
    This tool parses the HTML quality gate report and provides:
    - 🎯 Release readiness score (0-100%)
    - 📊 Quality gate summary with status breakdown
    - 🔴 Critical issues requiring immediate action
    - 📉 Key metrics below target (e.g., verification coverage %)
    - ⚠️ Data availability problems and blockers
    - 💡 Prioritized recommendations for release readiness
    
    The analysis extracts specific metrics like:
    - Requirements verification percentages
    - Defect closure rates
    - Safety requirements coverage
    - Resource utilization (RAM/ROM/CPU)
    - MISRA compliance warnings
    
    Args:
        report_path: Path to HTML report file. If not specified, uses
                    {ARC_WORKSPACE}/html/report.html

    Returns:
        Formatted report summary with quality gate analysis
    """
    try:
        if not report_path:
            workspace = Path(os.environ.get("ARC_WORKSPACE", get_arc_workspace()))
            report_path = workspace / "html" / "report.html"
        else:
            report_path = Path(report_path)
        
        # Parse the report
        report_data = parse_html_report(report_path)
        
        # Format and return summary
        summary = format_report_summary(report_data)
        return summary
    except FileNotFoundError as e:
        raise RuntimeError(f"Report file not found: {e}")
    except Exception as e:
        logging.error(f"Failed to analyze report: {e}")
        raise RuntimeError(f"Report analysis failed: {e}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    logging.info("ARC MCP Server starting up")
    initialize_arc()
    transport, host, port = get_mcp_init_vars()
    
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
