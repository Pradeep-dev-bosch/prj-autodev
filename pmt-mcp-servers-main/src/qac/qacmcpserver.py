#!/usr/bin/env python3
"""
QAC MCP Server - Simple wrapper for sca_tools commands

This server exposes QAC operations through MCP for use with VS Code/Roo Code.
It basically wraps sca_tools commands and provides project config management.
"""

import asyncio
import json
import logging
import os
import shutil
import sys
import threading
import uuid
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from artifactorylib import artifactory
from fastmcp import FastMCP
from rb_gitlib import gitlib


# Directories for configs and reports
SCRIPT_DIR = Path(__file__).resolve().parent
print(f"QAC MCP Server script location: {SCRIPT_DIR}")

LOG_DIR = SCRIPT_DIR / "logs"
CONFIG_DIR = SCRIPT_DIR / "configs"
REPORTS_DIR = SCRIPT_DIR / "reports"
print(f"Creating directories: {LOG_DIR}, {CONFIG_DIR}, {REPORTS_DIR}")

LOG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

log_file = LOG_DIR / "qac_mcp.log"

# Setup basic logging
# Rotating File Handler - max 1MB per file, keep 5 backup files
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=1024 * 1024,  # 1 MB
    backupCount=5,
    encoding="utf-8",
)

file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler.setFormatter(file_formatter)

# Console handler
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(console_formatter)

# Initialize MCP server
mcp = FastMCP("Perforce-QAC-MCP")

# Background task management
_background_tasks = {}
_task_lock = threading.Lock()


class BackgroundTask:
    """Represents a background analysis task"""

    def __init__(self, task_id: str, task_type: str, project_name: str):
        self.task_id = task_id
        self.task_type = task_type
        self.project_name = project_name
        self.status = "running"
        self.progress = "Started"
        self.result = None
        self.error = None
        self.started_at = datetime.now()
        self.completed_at = None
        self.thread = None

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dict for MCP response"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "project_name": self.project_name,
            "status": self.status,
            "progress": self.progress,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration_seconds": (
                (self.completed_at - self.started_at).total_seconds()
                if self.completed_at
                else (datetime.now() - self.started_at).total_seconds()
            ),
            "has_result": self.result is not None,
            "has_error": self.error is not None,
        }


def _register_task(task: BackgroundTask) -> str:
    """Register a background task"""
    with _task_lock:
        _background_tasks[task.task_id] = task
    logging.info(f"Registered background task: {task.task_id} ({task.task_type})")
    return task.task_id


def _update_task_progress(task_id: str, progress: str) -> None:
    """Update task progress message"""
    with _task_lock:
        if task_id in _background_tasks:
            _background_tasks[task_id].progress = progress
            logging.info(f"Task {task_id}: {progress}")


def _complete_task(task_id: str, result: dict[str, Any]) -> None:
    """Mark task as completed with result"""
    with _task_lock:
        if task_id in _background_tasks:
            task = _background_tasks[task_id]
            task.status = "completed"
            task.result = result
            task.completed_at = datetime.now()
            duration = (task.completed_at - task.started_at).total_seconds()
            logging.info(f"Task {task_id} completed in {duration:.1f}s")


def _fail_task(task_id: str, error: str) -> None:
    """Mark task as failed with error"""
    with _task_lock:
        if task_id in _background_tasks:
            task = _background_tasks[task_id]
            task.status = "failed"
            task.error = error
            task.completed_at = datetime.now()
            logging.error(f"Task {task_id} failed: {error}")


def _get_task(task_id: str) -> BackgroundTask | None:
    """Get task by ID"""
    with _task_lock:
        return _background_tasks.get(task_id)


def get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.

    Returns:
        tuple[str, str, int]: A tuple containing:
            - transport_type (str): Transport protocol type, defaults to "stdio"
            - host (str): Server host address, defaults to "127.0.0.1"
            - port (int): Server port number, defaults to 8000
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
        raise ValueError(f"Invalid PORT env variable: '{port_str}' - must be a valid integer")

    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def download_baselines_for_diff_analysis(
    baseline_path: str | Path, baseline_url: str, local_baseline_path: str | None = None
) -> None:
    """Function to download baselines, to be used for diff analysis"""
    logging.info("IN download_baselines_for_diff_analysis")
    artifactory_url = os.getenv("ARTIFACTORY_URL", None)

    if baseline_path.exists():
        logging.info(f"Deleting locally existing baseline directory at {baseline_path}...")
        shutil.rmtree(baseline_path, ignore_errors=True)
    logging.info(f"Creating baseline directory at {baseline_path}...")
    baseline_path.mkdir(parents=True, exist_ok=True)

    sup_path = baseline_path / "files.sup"
    if sup_path.exists():
        logging.info(f"Deleting locally existing QA baseline file at {sup_path}...")
        sup_path.unlink(missing_ok=True)

    if artifactory_url is not None:
        logging.info("Downloading QA baseline from artifactory...")
        art = artifactory.Transfer(
            url=artifactory_url, user=os.getenv("ARTIFACTORY_USER"), api_token=os.getenv("ARTIFACTORY_API_TOKEN")
        )
        art.download(baseline_url, to=baseline_path)
    else:
        local_baseline_file = Path(local_baseline_path) / "files.sup"
        logging.info(f"Copying baseline file {local_baseline_file} to {baseline_path}")
        shutil.copy(str(local_baseline_file), str(baseline_path))


def get_qac_project_path(json_path: str, datastore_target: str) -> str:
    """Return the value of QAC_PROJECT_PATH for the given datastore_target in json_path.

    Raises FileNotFoundError if the json file does not exist.
    Raises KeyError if the datastore_target or the QAC_PROJECT_PATH key is missing.
    """
    logging.info("Running get_qac_project_path")
    logging.info(f"json_path: {json_path}")
    logging.info(f"datastore_target: {datastore_target}")
    p = Path(json_path)
    if not p.exists():
        logging.warning(f"Raising file not found error for JSON file: {json_path}")
        raise FileNotFoundError(f"JSON file not found: {json_path}")

    with p.open("r", encoding="utf-8") as fh:
        logging.info("Load json file")
        data = json.load(fh)
    logging.info("JSON load completed")

    if datastore_target not in data:
        logging.warning(f"Raising key error for datastore_target '{datastore_target}' not found in JSON")
        raise KeyError(f"datastore_target '{datastore_target}' not found in JSON")
    else:
        logging.info(f"Found datastore_target '{datastore_target}' in JSON")

    entry: Any = data[datastore_target]
    if isinstance(entry, dict) and "QAC_PROJECT_PATH" in entry:
        return entry["QAC_PROJECT_PATH"]
    else:
        logging.info(f"QAC_PROJECT_PATH not found for '{datastore_target}', raising KeyError")

    logging.warning(f"Raising key error for QAC_PROJECT_PATH not found for '{datastore_target}' in {json_path}")
    raise KeyError(f"'QAC_PROJECT_PATH' not found for '{datastore_target}' in {json_path}")


def should_skip_project_creation(config: dict[str, Any]) -> dict[str, Any]:
    """
    Check whether project creation can be skipped.

    Rules:
      - If build/ does not exist -> cannot skip (return skip=False)
      - If build/ exists and contains any compile_commands.json (any subdir) ->
        skip creation (return skip=True)

    Returns a dict:
      - skip: bool
      - reason: short explanation
      - compile_commands_path: str (when found)
    """
    project_root = Path(config.get("project_root", "."))
    qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))
    build_dir = project_root / qac_project_path

    if not build_dir.exists():
        logging.debug(f"Build directory not found: {build_dir}")
        return {"skip": False, "reason": f"Build directory not found for {build_dir}"}

    # Look for compile_commands.json anywhere under build/
    matches = list(build_dir.rglob("compile_commands.json"))
    if matches:
        found = matches[0].resolve()
        logging.info(f"Found compile_commands.json, skipping project creation: {found}")
        return {"skip": True, "reason": "compile_commands.json found in build", "compile_commands_path": str(found)}

    logging.debug(f"No compile_commands.json found under: {build_dir}")
    return {"skip": False, "reason": f"No compile_commands.json under {build_dir}"}


def run_command(cmd: list[str], cwd: str | Path | None = None, timeout: int | None = None) -> dict[str, Any]:
    """Run a shell command and return the result (synchronous wrapper for threaded contexts)

    Args:
        cmd: Command and arguments as list
        cwd: Working directory
        timeout: Timeout in seconds (default: 7200 = 2 hours, None = no timeout)
    """
    # Use subprocess.run for synchronous execution (safe in threads)
    import subprocess

    # Default timeout: 2 hours (enough for large analysis runs)
    if timeout is None:
        timeout = 7200

    logging.info(f"Running: {' '.join(cmd)}")
    logging.info(f"Timeout: {timeout}s ({timeout / 3600:.1f} hours)")
    start = datetime.now()

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        duration = (datetime.now() - start).total_seconds()

        return {
            "success": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration,
        }
    except subprocess.TimeoutExpired as e:
        duration = (datetime.now() - start).total_seconds()
        logging.error(f"Command timed out after {duration}s: {' '.join(cmd)}")
        return {
            "success": False,
            "returncode": -1,
            "stdout": e.stdout or "",
            "stderr": e.stderr or "",
            "duration": duration,
            "error": "Command timed out",
        }
    except Exception as e:
        duration = (datetime.now() - start).total_seconds()
        logging.exception(f"Command failed: {' '.join(cmd)}")
        return {
            "success": False,
            "returncode": -1,
            "stdout": "",
            "stderr": str(e),
            "duration": duration,
            "error": str(e),
        }


async def run_command_async(cmd: list[str], cwd: str | Path | None = None) -> dict[str, Any]:
    """Run a shell command asynchronously with real-time output streaming"""
    logging.info(f"Running: {' '.join(cmd)}")

    start = datetime.now()
    stdout_lines = []
    stderr_lines = []

    try:
        # Create subprocess with pipes for streaming
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL,
        )

        async def read_stream(stream, is_stderr=False):
            """Read and log stream line by line in real-time"""
            lines = []
            while True:
                try:
                    line = await asyncio.wait_for(stream.readline(), timeout=30.0)
                    if not line:
                        break

                    decoded = line.decode("utf-8", errors="replace").rstrip()
                    lines.append(decoded)

                    # Log in real-time to keep connection alive
                    if decoded.strip():
                        if is_stderr:
                            logging.warning(f"  {decoded}")
                        else:
                            logging.info(f"  {decoded}")

                except asyncio.TimeoutError:
                    # No output for 30 seconds, log a heartbeat
                    logging.info("  ... (process still running)")
                    continue
                except Exception as e:
                    logging.error(f"Error reading stream: {e}")
                    break

            return lines

        # Read stdout and stderr concurrently
        stdout_task = asyncio.create_task(read_stream(process.stdout, is_stderr=False))
        stderr_task = asyncio.create_task(read_stream(process.stderr, is_stderr=True))

        # Wait for both streams to complete
        stdout_lines, stderr_lines = await asyncio.gather(stdout_task, stderr_task)

        # Wait for process to complete (should already be done)
        returncode = await process.wait()

        duration = (datetime.now() - start).total_seconds()

        success = returncode == 0
        if success:
            logging.info(f"Command completed successfully in {duration:.1f}s")
        else:
            logging.error(f"Command failed with code {returncode} after {duration:.1f}s")

        return {
            "success": success,
            "stdout": "\n".join(stdout_lines),
            "stderr": "\n".join(stderr_lines),
            "return_code": returncode,
            "duration": duration,
        }

    except asyncio.CancelledError:
        logging.error("Command was cancelled")
        if "process" in locals():
            process.kill()
            await process.wait()
        return {"success": False, "error": "Command was cancelled"}
    except Exception as e:
        logging.error(f"Command failed: {e}")
        return {"success": False, "error": str(e)}


def find_and_copy_export_files(project_name: str, project_root: str | Path, qac_project_path: str) -> list[str]:
    """
    Find sca_tools/export folder under build directory and copy CSV/XLSX files.

    Steps:
    1. Search for 'sca_tools/export' folder under build directory
    2. Find all .csv and .xlsx files in that folder
    3. Copy them to reports/{project_name}/ directory

    Args:
        project_name: Name of the project (used for destination folder)
        project_root: Root directory of the project
        qac_project_path: Path to build folder of the respective variant

    Returns:
        List of copied file paths, or empty list if nothing found
    """
    logging.info(f"Looking for exported CSV and XLSX files in {project_root}/{qac_project_path}")

    # Start searching from build directory
    build_dir = Path(project_root) / qac_project_path

    if not build_dir.exists():
        logging.warning(f"Build directory doesn't exist: {build_dir}")
        return []

    # Find sca_tools/export folder
    export_dir = None
    for export_path in build_dir.rglob("export"):
        if export_path.is_dir() and export_path.parent.name == "sca_tools":
            export_dir = export_path
            logging.info(f"The export directory is: {export_dir}")
            break

    if not export_dir:
        logging.warning("Could not find sca_tools/export folder")
        return []

    # Create destination directory: reports/{project_name}/
    dest_dir = REPORTS_DIR / project_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Destination directory: {dest_dir}")

    # Remove existing CSV/XLSX/HTML files in destination (if any) before copying
    removed = 0
    for pattern in ("*.csv", "*.xlsx", "*.html"):
        for existing in dest_dir.glob(pattern):
            try:
                existing.unlink()
            except Exception as e:
                logging.error(f"Failed to remove existing file {existing}: {e}")
            else:
                removed += 1
                logging.debug(f"Removed existing file: {existing}")
    if removed:
        logging.info(f"Removed {removed} existing export file(s) from {dest_dir}")
    else:
        logging.debug("No existing export files to remove")

    # Find and copy CSV, XLSX and HTML files
    copied_files = []

    logging.info(f"export dir is: {export_dir}")
    for pattern in ("*.csv", "*.xlsx", "*.html"):
        for src in export_dir.glob(pattern):
            dest_file = dest_dir / src.name
            try:
                logging.info(f"Copying {src} to {dest_file}")
                shutil.copy2(src, dest_file)
            except Exception as e:
                logging.error(f"Failed to copy {src}: {e}")
            else:
                copied_files.append(str(dest_file))
                logging.info(f"Copied: {src.name}")

    if copied_files:
        logging.info(f"Copied {len(copied_files)} file(s) to {dest_dir}")
    else:
        logging.warning("No CSV or XLSX files found in export directory")

    return copied_files


def load_project(project_name: str) -> dict[str, Any] | None:
    """Load project config from file"""
    config_file = CONFIG_DIR / f"project_{project_name}.json"
    if not config_file.exists():
        return None

    with open(config_file) as f:
        return json.load(f)


def save_project(project_config: dict[str, Any]) -> None:
    """Save project config to file"""
    name = project_config["name"]
    config_file = CONFIG_DIR / f"project_{name}.json"

    with open(config_file, "w") as f:
        json.dump(project_config, f, indent=2)

    logging.info(f"Saved config: {config_file}")


def list_all_projects() -> list[dict[str, Any]]:
    """Get list of all configured projects"""
    projects = []
    for config_file in CONFIG_DIR.glob("project_*.json"):
        try:
            with open(config_file) as f:
                config = json.load(f)
                projects.append(
                    {
                        "name": config["name"],
                        "description": config.get("description", ""),
                        "helix_version": config.get("helix_version", "unknown"),
                        "project_root": config["project_root"],
                    }
                )
        except Exception as e:
            logging.error(f"Error loading {config_file}: {e}")

    return projects


def find_git_diff(
    project_root: str | Path, find_includes_input_file: str | Path, merge_base: str, source_branch: str
) -> None:
    """
    A function to find the git diff between source branch and merge_base (target branch)
    The diff is written to a file specified by find_includes_input_file.
    Important:
    The source branch should be checked out in the repo, else the tool will throw Error.
    The diff is calculated between HEAD of the checked out branch and merge_base.
    We use the rb_gitlib PySOFA project for this operation.
    """
    file_list = []
    repo = gitlib.repo(project_root, override_auth=False)
    if repo.current_branch == str(source_branch):
        logging.info(f"Provided source branch is the current branch {source_branch}, so continuing with diff operation")
    else:
        logging.error(f"Current checked out branch doesn't match to {source_branch}, so exiting the operation")
        sys.exit(1)
    diff = repo.remote_diff(source="HEAD", target=merge_base)
    # pr_diff = repo.diff(target=merge_base, source="HEAD")

    for file in diff.as_dict():
        if any(file.endswith(extension) for extension in ("h", "hpp", "c", "cpp", "inl")):
            file_list.append(file)

    logging.info(f"file_list: {file_list}")
    with open(find_includes_input_file, "w+") as out:
        for item in file_list:
            out.write(f"{item}\n")


def _do_create_project(
    config: dict[str, Any],
    type_of_analysis: str = "full",
    baseline_path: str | Path | None = None,
) -> dict[str, Any]:
    cmd = [
        "sca_tools",
        "qac",
        "create",
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--project_root",
        config["project_root"],
        "--qac_bin_path",
        config["qac_bin_path"],
    ]
    logging.info(f"cmd is {cmd}")

    if type_of_analysis == "diff":
        cmd.extend(["--helper_set_baseline", str(baseline_path)])
        baseline_url = os.getenv("BASELINE_URL")
        local_baseline_path = os.getenv("LOCAL_BASELINE_PATH", None)
        logging.info("Calling download_baselines_for_diff_analysis")
        download_baselines_for_diff_analysis(baseline_path, baseline_url, local_baseline_path)

    logging.info(f"cmd is {cmd}")

    result = run_command(cmd, cwd=config["project_root"], timeout=10800)
    logging.info(f"result is {result}")

    result["project_name"] = config["name"]
    return result


def _do_analyze_project(
    config: dict[str, Any],
    type_of_analysis: str = "full",
    find_includes_input_file: str | Path | None = None,
    analyze_file: str | None = None,
) -> dict[str, Any]:
    """Internal function to actually run the analyze command"""
    cmd = [
        "sca_tools",
        "qac",
        "analyze",
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--project_root",
        config["project_root"],
        "--qac_bin_path",
        config["qac_bin_path"],
    ]

    if type_of_analysis == "diff":
        cmd.extend(["--analyze_list", find_includes_input_file])

    if type_of_analysis == "create_baseline":
        cmd.extend(["--helper_create_baseline", "yes"])

    if analyze_file:
        cmd.extend(["--analyze_file", analyze_file])
        logging.info(f"Analyzing single file: {analyze_file}")

    result = run_command(cmd, cwd=config["project_root"], timeout=14400)

    result["project_name"] = config["name"]
    return result


def _do_export_results(
    config: dict[str, Any],
    with_analysis: bool = True,
    with_summary: bool = True,
    with_metrics: bool = True,
    *,
    type_of_analysis: str | None = None,
) -> dict[str, Any]:
    """Internal function to actually run the export command.

    Note: `type_of_analysis` is keyword-only to avoid accidental positional
    usage. Only diff workflows should pass `type_of_analysis="diff"`.
    """
    cmd = [
        "sca_tools",
        "qac",
        "export_analysis",
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--project_root",
        config["project_root"],
        "--qac_bin_path",
        config["qac_bin_path"],
    ]

    if with_analysis:
        cmd.append("--with_analysis")
    if with_summary:
        cmd.append("--with_summary")
    if with_metrics:
        cmd.append("--with_metrics")
    if type_of_analysis == "diff":
        cmd.append("--reuse_analyze_list")

    # Export is usually fast but can take time for large projects - use 1 hour timeout
    result = run_command(cmd, cwd=config["project_root"], timeout=3600)

    result["project_name"] = config["name"]

    return result


def _do_find_includes(
    config: dict[str, Any],
    merge_base: str,
    source_branch: str,
    compile_commands: str | None = None,
    include_submodules: bool = False,
) -> dict[str, Any]:
    """
    Find changed files using git diff with merge base.

    Args:
        config: Project configuration
        merge_base: Git branch to compare against (e.g., "origin/main")
        compile_commands: Path to compile_commands.json
        include_submodules: Whether to include git submodules

    Returns:
        Path to file containing list of changed files
    """
    # Create output file in temp directory
    output_file = Path("configs") / f"{config['name']}_changed_files.txt"
    if not output_file.is_file():
        logging.info(f"Find Includes file {output_file} doesn't exist, so creating it")
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.touch()
    else:
        logging.info(f"Find Includes file {output_file} already exists, so deleting it")
        output_file.unlink()
        logging.info(f"Creating new Find Includes file {output_file}")
        output_file.touch()

    logging.info(f"Find includes process started for merge_base {merge_base}")
    find_git_diff(config["project_root"], output_file, str(merge_base), source_branch)

    cmd = [
        "sca_tools",
        "find_includes",
        "--project_root",
        config["project_root"],
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--merge_base",
        merge_base,
        "--output_file",
        str(output_file),
    ]

    # Add compile_commands if provided
    if compile_commands:
        cmd.extend(["--compile_commands", compile_commands])

    # Add git_submodules flag if requested
    if include_submodules:
        cmd.append("--git_submodules")

    result = run_command(cmd, cwd=config["project_root"])

    if result["success"] and output_file.exists():
        # Count how many files were found
        with open(output_file) as f:
            file_count = len([line for line in f if line.strip()])

        logging.info(f"Found {file_count} changed file(s)")
        result["changed_files"] = str(output_file)
        result["file_count"] = file_count
    else:
        logging.error("Failed to find changed files")

    return result


def _do_filter_qaview(
    config: dict[str, Any],
    qaview_csv: str,
    min_severity_level: int,
    output_html: str | None = None,
) -> dict[str, Any]:
    """
    Filter QAView analysis results by severity level.

    Args:
        config: Project configuration
        qaview_csv: Path to qacli-view-analysis.csv
        min_severity_level: Minimum severity level to report (2-9)
        output_html: Optional path to output HTML report

    Returns:
        Result dictionary
    """
    # Build severity threshold arguments
    # If user wants level 5 and above, we set thresholds for 6,7,8,9 to 0
    # and don't include lower levels
    cmd = [
        "sca_tools",
        "qac",
        "filter_qaview",
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--project_root",
        config["project_root"],
        "--qaview_csv",
        qaview_csv,
    ]

    # Add severity thresholds from min_severity_level to 9
    # Level 9 is highest severity, Level 2 is lowest we care about
    for level in range(9, min_severity_level - 1, -1):
        cmd.extend([f"--severity_level_fail_threshold_for_level_{level}", "0"])

    qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))
    logging.info(f"qac_project_path: {qac_project_path}")
    # Add output HTML if specified
    if not output_html:
        # Auto-generate output path
        project_root = Path(config["project_root"])
        export_dir = project_root / qac_project_path / "sca_tools" / "export"
        export_dir.mkdir(parents=True, exist_ok=True)
        output_html = str(export_dir / "open_warnings.html")

    cmd.extend(["--threshold_warnings_report", output_html])
    cmd.extend(["--qac_bin_path", config["qac_bin_path"]])

    result = run_command(cmd, cwd=config["project_root"])

    if result["success"]:
        result["output_html"] = output_html
        logging.info(f"Filter QAView report generated: {output_html}")

    return result


def _do_report_filter(
    config: dict[str, Any],
    input_csv: str,
    rules_json: str,
    report_dir: str | None = None,
    export_formats: list[str] | None = None,
) -> dict[str, Any]:
    """
    Generate filtered report using rules configuration.

    Args:
        config: Project configuration
        input_csv: Path to analysis CSV
        rules_json: Path to rules.json configuration
        report_dir: Directory for output reports
        export_formats: List of export formats (csv, html, json)

    Returns:
        Result dictionary
    """
    # Default report directory
    if not report_dir:
        report_dir = str(REPORTS_DIR / config["name"])

    # Create report directory
    Path(report_dir).mkdir(parents=True, exist_ok=True)

    # Default export formats
    if not export_formats:
        export_formats = ["csv", "html"]

    cmd = [
        "sca_tools",
        "report",
        "filter",
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--project_root",
        config["project_root"],
        "--input_file",
        input_csv,
        "--report_dir",
        report_dir,
        "--report_configuration",
        rules_json,
        "--export_formats",
        " ".join(export_formats),
    ]

    result = run_command(cmd, cwd=config["project_root"])

    if result["success"]:
        result["report_dir"] = report_dir
        result["export_formats"] = export_formats
        logging.info(f"Filtered reports generated in: {report_dir}")

    return result


@mcp.tool()
def extract_results(
    project_name: str,
    min_severity_level: int = 2,
    rules_json: str | None = None,
    use_filter_qaview: bool | None = None,
    input_csv: str | None = None,
    output_html: str | None = None,
    report_dir: str | None = None,
    export_formats: list[str] | None = None,
) -> dict[str, Any]:
    """
    Extract and filter QACPP analysis results.

    This tool provides two methods for result extraction:
    1. Filter QAView: Filter by severity level (simpler, no rules needed)
    2. Report Filter: Filter using rules.json (more flexible)

    The tool automatically chooses the best method:
    - If rules_json is provided: uses Report Filter
    - If rules_json is missing: uses Filter QAView (default)
    - You can force Filter QAView with use_filter_qaview=True

    Args:
        project_name: Name of the project
        min_severity_level: Minimum severity level to report (2-9, default 2)
                          Level 9 = highest severity, Level 2 = lowest
                          Example: level 5 means report warnings level 5 and above
        rules_json: Optional path to rules.json for Report Filter method
        use_filter_qaview: Force use of Filter QAView method (default: auto)
        input_csv: Optional path to qacli-view-analysis.csv (auto-detected if not provided)
        output_html: Optional output HTML path (for Filter QAView)
        report_dir: Optional report directory (for Report Filter)
        export_formats: Optional list of formats for Report Filter (e.g., ["csv", "html"])

    Examples:
        # Simple: Report all warnings level 5 and above
        extract_results(
            project_name="DemoProject",
            min_severity_level=5
        )

        # With rules.json (uses Report Filter)
        extract_results(
            project_name="DemoProject",
            rules_json="tools/sca/qac/rules.json"
        )

        # Force Filter QAView with custom output
        extract_results(
            project_name="DemoProject",
            min_severity_level=4,
            use_filter_qaview=True,
            output_html="reports/my_warnings.html"
        )

        # Report Filter with multiple formats
        extract_results(
            project_name="DemoProject",
            rules_json="tools/sca/qac/rules.json",
            export_formats=["csv", "html", "json"]
        )
    """
    logging.info(f"Extracting results for: {project_name}")
    logging.info(f"Minimum severity level: {min_severity_level}")

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Validate severity level
    if not 2 <= min_severity_level <= 9:
        return {"success": False, "error": f"Invalid severity level: {min_severity_level}. Must be between 2 and 9."}

    # Auto-detect input CSV if not provided
    if not input_csv:
        project_root = Path(config["project_root"])
        qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))
        build_dir = project_root / qac_project_path

        # Look for qacli-view-analysis.csv
        csv_files = list(build_dir.rglob("qacli-view-analysis.csv"))

        if not csv_files:
            return {
                "success": False,
                "error": "Could not find qacli-view-analysis.csv. Run export first or provide input_csv.",
            }

        input_csv = str(csv_files[0])
        logging.info(f"Auto-detected input CSV: {input_csv}")

    # Check if input CSV exists
    if not Path(input_csv).exists():
        return {"success": False, "error": f"Input CSV not found: {input_csv}"}

    # Decide which method to use
    method = None

    if use_filter_qaview is True:
        # User explicitly wants Filter QAView
        method = "filter_qaview"
        logging.info("Using Filter QAView method (user specified)")

    elif rules_json:
        # Check if rules.json exists
        rules_path = Path(rules_json)
        if rules_path.exists():
            method = "report_filter"
            logging.info("Using Report Filter method (rules.json provided)")
        else:
            logging.warning(f"rules.json not found at {rules_json}, falling back to Filter QAView")
            method = "filter_qaview"

    else:
        method = "filter_qaview"
        logging.info("Using Filter QAView method (default)")

    # Execute the appropriate method
    if method == "filter_qaview":
        result = _do_filter_qaview(config, input_csv, min_severity_level, output_html)

        return {
            "success": result["success"],
            "project_name": project_name,
            "method": "filter_qaview",
            "min_severity_level": min_severity_level,
            "input_csv": input_csv,
            "output_html": result.get("output_html"),
            "result": result,
        }

    else:  # report_filter
        logging.info("Running report filter...")
        filter_result = _do_report_filter(config, input_csv, rules_json, report_dir, export_formats)

        return {
            "success": filter_result["success"],
            "project_name": project_name,
            "method": "report_filter",
            "rules_json": rules_json,
            "input_csv": input_csv,
            "report_dir": filter_result.get("report_dir"),
            "export_formats": filter_result.get("export_formats"),
            "filter_result": filter_result,
        }


@mcp.tool()
def generate_threshold_report(
    project_name: str,
    rules_json: str,
    qac_project_path: str,
    input_csv: str | None = None,
    output_file: str | None = None,
) -> dict[str, Any]:
    """
    Generate threshold report from analysis results.

    This runs 'sca_tools report threshold' to check if violations exceed thresholds.
    Useful after diff analysis to validate changed files.

    Args:
        project_name: Name of the project
        rules_json: Path to threshold rules JSON file
        input_csv: Optional path to analysis CSV (auto-detected if not provided)
        output_file: Optional output file path

    Example:
        generate_threshold_report(
            project_name="DemoProject",
            rules_json="tools/sca/qac/rules.json",
            input_csv="build/qac_MyTarget/sca_tools/export/qacli-view-analysis.csv"
        )
    """
    logging.info(f"Generating threshold report for: {project_name}")

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Check if rules.json exists
    if not Path(rules_json).exists():
        return {"success": False, "error": f"rules.json not found: {rules_json}"}

    # Auto-detect input CSV if not provided
    if not input_csv:
        project_root = Path(config["project_root"])
        build_dir = project_root / qac_project_path

        # Look for qacli-view-analysis.csv
        csv_files = list(build_dir.rglob("qacli-view-analysis.csv"))

        if not csv_files:
            return {"success": False, "error": "Could not find analysis CSV file. Please provide input_csv parameter."}

        input_csv = str(csv_files[0])
        logging.info(f"Auto-detected input CSV: {input_csv}")

    # Generate output file if not provided
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = str(REPORTS_DIR / project_name / f"threshold_report_{timestamp}.txt")

    result = _do_report_threshold(config, input_csv, rules_json, output_file)

    return {
        "success": result["success"],
        "project_name": project_name,
        "input_csv": input_csv,
        "rules_json": rules_json,
        "output_file": output_file if result["success"] else None,
        "result": result,
    }


@mcp.tool()
def list_background_tasks(status_filter: str | None = None) -> dict[str, Any]:
    """
    List all background tasks.

    Args:
        status_filter: Optional filter by status: "running", "completed", "failed"

    Returns:
        List of all background tasks with their status

    Example:
        # List all tasks
        list_background_tasks()

        # List only running tasks
        list_background_tasks(status_filter="running")
    """
    with _task_lock:
        tasks = list(_background_tasks.values())

    # Apply filter if requested
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]

    # Convert to dict
    task_list = [t.to_dict() for t in tasks]

    return {"success": True, "count": len(task_list), "tasks": task_list}


@mcp.tool()
def get_task_status(task_id: str) -> dict[str, Any]:
    """
    Get detailed status of a specific background task.

    Args:
        task_id: The task ID returned when starting the analysis

    Returns:
        Detailed task information including status, progress, and results

    Example:
        get_task_status(task_id="abc-123-def")
    """
    task = _get_task(task_id)

    if not task:
        return {"success": False, "error": f"Task not found: {task_id}"}

    response = {"success": True, **task.to_dict()}

    # Include error if task failed
    if task.error:
        response["error"] = task.error

    return response


@mcp.tool()
def get_task_result(task_id: str) -> dict[str, Any]:
    """
    Retrieve the full result of a completed background task.

    Args:
        task_id: The task ID returned when starting the analysis

    Returns:
        The complete analysis result if task is completed

    Example:
        get_task_result(task_id="abc-123-def")
    """
    task = _get_task(task_id)

    if not task:
        return {"success": False, "error": f"Task not found: {task_id}"}

    if task.status == "running":
        return {
            "success": False,
            "error": "Task is still running. Check status with get_task_status().",
            "task_status": task.to_dict(),
        }

    if task.status == "failed":
        return {"success": False, "error": task.error or "Task failed", "task_status": task.to_dict()}

    # Task completed successfully
    return {"success": True, "task_id": task_id, "result": task.result}


@mcp.tool()
def create_qacpp_config(
    project_name: str,
    datastore_paths: list[str],
    datastore_target: str,
    project_root: str,
    qac_bin_path: str,
    helix_version: str = "2023.4",
    description: str = "",
) -> dict[str, Any]:
    """
    Creates a new QACPP configuration file to be used for static code analysis.

    Args:
        project_name: Name for this project config
        datastore_paths: List of paths to datastore JSON files
        datastore_target: Target name (e.g., "WholeWorld")
        project_root: Absolute path to project root directory
        qac_bin_path: Path to QAC bin directory
        helix_version: Helix QAC version (default "2023.4")
        description: Optional description
    """
    logging.info(f"Creating config for project: {project_name}")

    # Build config dict
    config = {
        "name": project_name,
        "datastore_paths": datastore_paths,
        "datastore_target": datastore_target,
        "project_root": project_root,
        "qac_bin_path": qac_bin_path,
        "helix_version": helix_version,
        "description": description,
        "created_at": datetime.now().isoformat(),
    }

    # Basic validation
    if not Path(project_root).exists():
        logging.warning(f"Project root doesn't exist: {project_root}")

    if not Path(qac_bin_path).exists():
        logging.warning(f"QAC bin path doesn't exist: {qac_bin_path}")

    # Save config
    save_project(config)

    return {
        "success": True,
        "message": f"Created config for {project_name}",
        "config_file": str(CONFIG_DIR / f"project_{project_name}.json"),
    }


@mcp.tool()
def list_projects() -> dict[str, Any]:
    """List all configured QACPP projects"""
    logging.info("Listing all projects")
    projects = list_all_projects()

    return {"success": True, "count": len(projects), "projects": projects}


@mcp.tool()
def get_project_details(project_name: str) -> dict[str, Any]:
    """Get full details for a project"""
    logging.info(f"Getting details for: {project_name}")

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    return {"success": True, "project": config}


@mcp.tool()
def create_qacpp_project(project_name: str) -> dict[str, Any]:
    """
    Create a QACPP project using sca_tools.

    This runs 'sca_tools qac create' to initialize the project database.
    This is the first step and must be done before analysis.
    """
    logging.info(f"Creating QACPP project: {project_name}")

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    result = _do_create_project(config, "full", None)
    return result


@mcp.tool()
def run_qacpp_analysis(project_name: str) -> dict[str, Any]:
    """
    Run 'sca_tools qac analyze' for a project.

    This performs the actual static analysis.
    """
    logging.info(f"Running analysis for: {project_name}")

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Run the actual analysis
    logging.info("Running analysis step")
    analyze_result = _do_analyze_project(config)
    return analyze_result


@mcp.tool()
def run_single_file_analysis_workflow(
    project_name: str,
    file_path: str,
    min_severity_level: int = 3,
    rules_json: str | None = None,
    use_filter_qaview: bool | None = None,
    skip_create: bool = False,
) -> dict[str, Any]:
    """
    Run complete QACPP single file analysis workflow.

    This executes the entire workflow for a single file:
    1. Create project (if not already created)
    2. Analyze single file
    3. Export results
    4. Extract/filter results by severity

    Use this for analyzing a specific file in the codebase.

    Args:
        project_name: Name of the configured project
        file_path: Path to the file to analyze (absolute or relative to project_root)
        min_severity_level: Minimum severity level to report (2-9, default 3)
        rules_json: Optional rules.json for filtering
        use_filter_qaview: Force Filter QAView method
        skip_create: Skip project creation step (default: False)

    Example:
        run_single_file_analysis_workflow(
            project_name="MyProject",
            file_path="src/main.cpp",
            min_severity_level=5,
            rules_json="tools/sca/qac/rules.json"
        )
    """
    logging.info("=" * 70)
    logging.info(f"SINGLE FILE ANALYSIS WORKFLOW for: {project_name}")
    logging.info(f"File: {file_path}")
    logging.info("=" * 70)

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))
    # Resolve file path
    file_to_analyze = Path(file_path)
    if not file_to_analyze.is_absolute():
        file_to_analyze = Path(config["project_root"]) / file_path

    if not file_to_analyze.exists():
        return {"success": False, "error": f"File not found: {file_path}", "resolved_path": str(file_to_analyze)}

    logging.info(f"Resolved file path: {file_to_analyze}")

    workflow_start = datetime.now()
    results = {
        "project_name": project_name,
        "workflow_type": "single_file_analysis",
        "file_path": file_path,
        "resolved_path": str(file_to_analyze),
        "steps": [],
    }

    # Check if we need to create
    state = should_skip_project_creation(config)
    logging.info(f"Project creation check: {state}")
    should_skip = state["skip"]
    logging.info(f"should_skip value: {should_skip}")
    logging.info(f"skip_create parameter: {skip_create}")

    # Step 1: Create project (if needed)
    if skip_create:
        logging.info("Skipping create - skip_create=True (user override)")
        results["steps"].append({"step": "create", "success": True, "skipped": True})
    else:
        logging.info("=" * 70)
        logging.info("Step 1/4: Creating QACPP project")
        logging.info("=" * 70)

        create_result = _do_create_project(config)
        results["steps"].append(
            {"step": "create", "success": create_result["success"], "duration": create_result.get("duration", 0)}
        )

        if not create_result["success"]:
            results["success"] = False
            results["failed_at"] = "create"
            results["error"] = create_result.get("error", "Project creation failed")
            return results

    # Step 2: Analyze single file
    logging.info("=" * 70)
    logging.info("Step 2/4: Running single file analysis")
    logging.info("=" * 70)

    analyze_result = _do_analyze_project(config, analyze_file=str(file_to_analyze))
    results["steps"].append(
        {"step": "analyze", "success": analyze_result["success"], "duration": analyze_result.get("duration", 0)}
    )

    if not analyze_result["success"]:
        results["success"] = False
        results["failed_at"] = "analyze"
        results["error"] = analyze_result.get("error", "Analysis failed")
        return results

    # Step 3: Export results
    logging.info("=" * 70)
    logging.info("Step 3/4: Exporting results")
    logging.info("=" * 70)

    export_result = _do_export_results(config, True, True, True)
    # Attempt to locate and copy CSV/XLSX export artifacts into reports/{project}
    copied_files = find_and_copy_export_files(config["name"], config["project_root"], qac_project_path)
    export_result["copied_files"] = copied_files
    if copied_files:
        logging.info(f"Copied {len(copied_files)} file(s) to reports/{config['name']}")
    else:
        logging.warning("No CSV/XLSX files found to copy")

    results["steps"].append(
        {
            "step": "export",
            "success": export_result["success"],
            "duration": export_result.get("duration", 0),
            "output_file": export_result.get("output_file"),
            "copied_files": export_result.get("copied_files", []),
        }
    )

    if not export_result["success"]:
        results["success"] = False
        results["failed_at"] = "export"
        results["error"] = export_result.get("error", "Export failed")
        return results

    # Step 4: Extract/filter results
    logging.info("=" * 70)
    logging.info("Step 4/4: Extracting and filtering results")
    logging.info("=" * 70)

    # Find the analysis CSV
    project_root = Path(config["project_root"])
    build_dir = project_root / qac_project_path
    csv_files = list(build_dir.rglob("qacli-view-analysis.csv"))

    if not csv_files:
        logging.warning("Could not find analysis CSV file for filtering")
        results["success"] = False
        results["failed_at"] = "extract"
        results["error"] = "Analysis CSV not found"
        return results
    else:
        input_csv = str(csv_files[0])
        logging.info(f"Using analysis CSV: {input_csv}")

        # Decide which extraction method to use
        if rules_json and Path(rules_json).exists():
            logging.info("Using Report Filter method with rules.json")
            filter_result = _do_report_filter(
                config,
                input_csv,
                rules_json,
                None,  # report_dir (auto)
                None,  # export_formats (auto)
            )

            results["steps"].append(
                {
                    "step": "extract",
                    "method": "report_filter",
                    "success": filter_result["success"],
                    "report_dir": filter_result.get("report_dir"),
                    "export_formats": filter_result.get("export_formats"),
                }
            )
        else:
            logging.info("Using Filter QAView method")
            filter_result = _do_filter_qaview(config, input_csv, min_severity_level, None)

            results["steps"].append(
                {
                    "step": "extract",
                    "method": "filter_qaview",
                    "success": filter_result["success"],
                    "min_severity_level": min_severity_level,
                    "output_html": filter_result.get("output_html"),
                }
            )

        if not filter_result["success"]:
            results["success"] = False
            results["failed_at"] = "extract"
            results["error"] = filter_result.get("error", "Result extraction failed")
            return results

    # Success!
    workflow_duration = (datetime.now() - workflow_start).total_seconds()
    results["success"] = True
    results["duration"] = workflow_duration

    logging.info("=" * 70)
    logging.info(f"SINGLE FILE ANALYSIS WORKFLOW COMPLETED in {workflow_duration:.1f}s")
    logging.info("=" * 70)

    return results


def _run_full_analysis_workflow_impl(
    project_name: str,
    baseline_path: str | None = None,
    min_severity_level: int = 3,
    rules_json: str | None = None,
    use_filter_qaview: bool | None = None,
    skip_create: bool = False,
) -> dict[str, Any]:
    """Internal implementation of full analysis workflow (callable from threads)"""
    logging.info("=" * 70)
    logging.info(f"FULL ANALYSIS WORKFLOW for: {project_name}")
    logging.info("=" * 70)

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Get qac_project_path early - needed for export file copying
    qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))

    workflow_start = datetime.now()
    results = {"project_name": project_name, "workflow_type": "full_analysis", "steps": []}

    # Check if we need to create
    state = should_skip_project_creation(config)
    logging.info(f"Project creation check: {state}")
    should_skip = state["skip"]
    logging.info(f"should_skip value: {should_skip}")
    logging.info(f"skip_create parameter: {skip_create}")

    # Step 1: Create project (if needed)
    if skip_create:
        logging.info("Skipping create - skip_create=True (user override)")
        results["steps"].append({"step": "create", "success": True, "skipped": True})
    else:
        logging.info("=" * 70)
        logging.info("Step 1/4: Creating QACPP project")
        logging.info("=" * 70)

        create_result = _do_create_project(config)
        results["steps"].append(
            {"step": "create", "success": create_result["success"], "duration": create_result.get("duration", 0)}
        )

        if not create_result["success"]:
            results["success"] = False
            results["failed_at"] = "create"
            results["error"] = create_result.get("error", "Create failed")
            return results

    # Step 2: Analyze all files
    logging.info("=" * 70)
    logging.info("Step 2/4: Running full analysis")
    logging.info("=" * 70)

    analyze_result = _do_analyze_project(config, type_of_analysis="create_baseline")
    results["steps"].append(
        {"step": "analyze", "success": analyze_result["success"], "duration": analyze_result.get("duration", 0)}
    )

    if not analyze_result["success"]:
        results["success"] = False
        results["failed_at"] = "analyze"
        results["error"] = analyze_result.get("error", "Analysis failed")
        return results

    # Step 3: Export results
    logging.info("=" * 70)
    logging.info("Step 3/4: Exporting results")
    logging.info("=" * 70)

    export_result = _do_export_results(config, True, True, True)
    # Attempt to locate and copy CSV/XLSX export artifacts into reports/{project}
    copied_files = find_and_copy_export_files(config["name"], config["project_root"], qac_project_path)
    export_result["copied_files"] = copied_files
    if copied_files:
        logging.info(f"Successfully copied {len(copied_files)} export file(s)")
    else:
        logging.warning("No export files found to copy")
    results["steps"].append(
        {
            "step": "export",
            "success": export_result["success"],
            "duration": export_result.get("duration", 0),
            "output_file": export_result.get("output_file"),
            "copied_files": export_result.get("copied_files", []),
        }
    )

    if not export_result["success"]:
        results["success"] = False
        results["failed_at"] = "export"
        results["error"] = export_result.get("error", "Export failed")
        return results

    # Step 4: Extract/filter results
    logging.info("=" * 70)
    logging.info("Step 4/4: Extracting and filtering results")
    logging.info("=" * 70)

    # Find the analysis CSV
    project_root = Path(config["project_root"])
    build_dir = project_root / qac_project_path
    csv_files = list(build_dir.rglob("qacli-view-analysis.csv"))

    if not csv_files:
        logging.warning("Could not find analysis CSV, skipping filter step")
        results["steps"].append({"step": "filter", "success": False, "error": "CSV not found"})
    else:
        input_csv = str(csv_files[0])

        # Decide method
        use_report_filter = False
        if rules_json and Path(rules_json).exists():
            use_report_filter = True
            method = "report_filter"
        elif not use_filter_qaview:
            use_report_filter = False
            method = "filter_qaview"
        else:
            method = "filter_qaview"

        logging.info(f"Using {method} method")

        if use_report_filter:
            filter_result = _do_report_filter(config, input_csv, rules_json)

            results["steps"].append(
                {
                    "step": "filter",
                    "method": "report_filter",
                    "success": filter_result["success"],
                    "duration": filter_result.get("duration", 0),
                    "report_dir": filter_result.get("report_dir"),
                }
            )
        else:
            # Filter QAView
            filter_result = _do_filter_qaview(config, input_csv, min_severity_level)

            results["steps"].append(
                {
                    "step": "filter",
                    "method": "filter_qaview",
                    "success": filter_result["success"],
                    "duration": filter_result.get("duration", 0),
                    "output_html": filter_result.get("output_html"),
                    "min_severity_level": min_severity_level,
                }
            )

    # Calculate total time
    workflow_end = datetime.now()
    total_duration = (workflow_end - workflow_start).total_seconds()

    results["success"] = True
    results["total_duration_seconds"] = total_duration

    logging.info("=" * 70)
    logging.info(f"✓ FULL ANALYSIS COMPLETED in {total_duration:.1f}s")
    logging.info("=" * 70)

    return results


def _run_diff_analysis_workflow_impl(
    project_name: str,
    merge_base: str,
    compile_commands: str | None = None,
    include_submodules: bool = False,
    min_severity_level: int = 3,
    rules_json: str | None = None,
    use_filter_qaview: bool | None = None,
    source_branch: str | None = None,
    skip_create: bool = False,
) -> dict[str, Any]:
    """Internal implementation of diff analysis workflow (callable from threads)"""
    logging.info("=" * 70)
    logging.info(f"DIFF ANALYSIS WORKFLOW for: {project_name}")
    logging.info(f"Comparing against: {merge_base}")
    logging.info("=" * 70)

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    workflow_start = datetime.now()
    results = {"project_name": project_name, "workflow_type": "diff_analysis", "merge_base": merge_base, "steps": []}
    qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))

    # Step 1: Find changed files
    logging.info("=" * 70)
    logging.info("Step 1/5: Finding changed files")
    logging.info("=" * 70)

    find_result = _do_find_includes(config, merge_base, source_branch, compile_commands, include_submodules)
    results["steps"].append(
        {
            "step": "find_includes",
            "success": find_result["success"],
            "duration": find_result.get("duration", 0),
            "file_count": find_result.get("file_count", 0),
        }
    )

    if not find_result["success"]:
        results["success"] = False
        results["failed_at"] = "find_includes"
        results["error"] = "Failed to find changed files"
        return results

    changed_files_path = find_result.get("changed_files")
    file_count = find_result.get("file_count", 0)

    if file_count == 0:
        logging.info("No changed files found - nothing to analyze")
        results["success"] = True
        results["message"] = "No changed files"
        results["file_count"] = 0
        return results

    logging.info(f"Found {file_count} changed file(s)")
    results["file_count"] = file_count
    results["changed_files"] = changed_files_path

    # Check if we need to create
    state = should_skip_project_creation(config)
    logging.info(f"Project creation check: {state}")
    should_skip = state["skip"]
    logging.info(f"should_skip value: {should_skip}")
    logging.info(f"skip_create parameter: {skip_create}")

    # Step 2: Create project (if needed)
    if skip_create:
        logging.info("Skipping create - skip_create=True (user override)")
        results["steps"].append({"step": "create", "success": True, "skipped": True})
    else:
        logging.info("=" * 70)
        logging.info("Step 2/5: Creating QACPP project")
        logging.info("=" * 70)

        logging.info(f"Determined QAC project path: {qac_project_path}")
        baseline_path = Path(config["project_root"]) / Path(qac_project_path) / "local_baseline"

        # Ensure project_root is defined and use it to compute baseline path
        project_root = config["project_root"]
        logging.info(f"Determined project root: {project_root}")

        # Compute baseline path inside the project's configs directory
        logging.info(f"Using baseline path: {baseline_path}")

        create_result = _do_create_project(config, "diff", baseline_path=baseline_path)
        results["steps"].append(
            {"step": "create", "success": create_result["success"], "duration": create_result.get("duration", 0)}
        )

        if not create_result["success"]:
            results["success"] = False
            results["failed_at"] = "create"
            results["error"] = "Project creation failed"
            return results

    # Step 3: Analyze only changed files
    logging.info("=" * 70)
    logging.info(f"Step 3/5: Analyzing {file_count} changed file(s)")
    logging.info("=" * 70)

    analyze_result = _do_analyze_project(
        config, type_of_analysis="diff", find_includes_input_file=changed_files_path, analyze_file=None
    )
    results["steps"].append(
        {"step": "analyze", "success": analyze_result["success"], "duration": analyze_result.get("duration", 0)}
    )

    if not analyze_result["success"]:
        results["success"] = False
        results["failed_at"] = "analyze"
        results["error"] = "Analysis failed"
        return results

    # Step 4: Export results
    logging.info("=" * 70)
    logging.info("Step 4/5: Exporting results")
    logging.info("=" * 70)

    export_result = _do_export_results(config, True, True, True, type_of_analysis="diff")
    # Attempt to locate and copy CSV/XLSX export artifacts into reports/{project}
    copied_files = find_and_copy_export_files(config["name"], config["project_root"], qac_project_path)
    export_result["copied_files"] = copied_files
    if copied_files:
        logging.info(f"Successfully copied {len(copied_files)} export file(s)")
    else:
        logging.warning("No export files found to copy")

    results["steps"].append(
        {
            "step": "export",
            "success": export_result["success"],
            "duration": export_result.get("duration", 0),
            "output_file": export_result.get("output_file"),
            "copied_files": export_result.get("copied_files", []),
        }
    )

    if not export_result["success"]:
        results["success"] = False
        results["failed_at"] = "export"
        results["error"] = "Export failed"
        return results

    # Step 5: Extract/filter results
    logging.info("=" * 70)
    logging.info("Step 5/5: Extracting and filtering results")
    logging.info("=" * 70)

    # Find the analysis CSV
    project_root = Path(config["project_root"])
    build_dir = project_root / qac_project_path
    csv_files = list(build_dir.rglob("qacli-view-analysis.csv"))

    if not csv_files:
        logging.warning("Could not find analysis CSV, skipping filter step")
        results["steps"].append({"step": "filter", "success": False, "error": "CSV not found"})
    else:
        input_csv = str(csv_files[0])

        # Decide method
        use_report_filter = False
        if rules_json and Path(rules_json).exists():
            use_report_filter = True
            method = "report_filter"
        elif not use_filter_qaview:
            use_report_filter = False
            method = "filter_qaview"
        else:
            method = "filter_qaview"

        logging.info(f"Using {method} method")

        if use_report_filter:
            # Report filter with threshold
            filter_result = _do_report_filter(config, input_csv, rules_json)

            results["steps"].append(
                {
                    "step": "filter",
                    "method": "report_filter",
                    "success": filter_result["success"],
                    "duration": filter_result.get("duration", 0),
                    "report_dir": filter_result.get("report_dir"),
                }
            )
        else:
            # Filter QAView
            filter_result = _do_filter_qaview(config, input_csv, min_severity_level)

            results["steps"].append(
                {
                    "step": "filter",
                    "method": "filter_qaview",
                    "success": filter_result["success"],
                    "duration": filter_result.get("duration", 0),
                    "output_html": filter_result.get("output_html"),
                    "min_severity_level": min_severity_level,
                }
            )

    # Calculate total time
    workflow_end = datetime.now()
    total_duration = (workflow_end - workflow_start).total_seconds()

    results["success"] = True
    results["total_duration_seconds"] = total_duration

    logging.info("=" * 70)
    logging.info(f"✓ DIFF ANALYSIS COMPLETED in {total_duration:.1f}s")
    logging.info(f"Analyzed {file_count} changed file(s)")
    logging.info("=" * 70)

    return results


@mcp.tool()
def export_qacpp_results(
    project_name: str,
    output_filename: str | None = None,
    with_analysis: bool = True,
    with_summary: bool = True,
    with_metrics: bool = True,
) -> dict[str, Any]:
    """
    Export QACPP analysis results.

    Args:
        project_name: Name of the project
        output_filename: Optional filename (auto-generated if not provided)
        with_analysis: Include detailed analysis
        with_summary: Include summary
        with_metrics: Include metrics
    """
    logging.info(f"Exporting results for: {project_name}")

    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Generate output filename if not provided
    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{project_name}_export_analysis_{timestamp}.json"

    cmd = [
        "sca_tools",
        "qac",
        "export_analysis",
        "--datastore_path",
        *config["datastore_paths"],
        "--datastore_target",
        config["datastore_target"],
        "--project_root",
        config["project_root"],
        "--qac_bin_path",
        config["qac_bin_path"],
    ]

    # Add export flags
    if with_analysis:
        cmd.append("--with_analysis")
    if with_summary:
        cmd.append("--with_summary")
    if with_metrics:
        cmd.append("--with_metrics")

        # Run the actual export
    logging.info("Running export step")
    export_result = _do_export_results(config, with_analysis, with_summary, with_metrics)

    qac_project_path = str(get_qac_project_path(*config["datastore_paths"], config["datastore_target"]))
    copied_files = find_and_copy_export_files(config["name"], config["project_root"], qac_project_path)
    export_result["copied_files"] = copied_files

    if copied_files:
        logging.info(f"Successfully copied {len(copied_files)} export file(s)")
    else:
        logging.warning("No export files found to copy")

    return export_result


@mcp.tool()
def delete_project_config(project_name: str) -> dict[str, Any]:
    """Delete a project configuration"""
    logging.info(f"Deleting config for: {project_name}")

    config_file = CONFIG_DIR / f"project_{project_name}.json"

    if not config_file.exists():
        return {"success": False, "error": f"Project '{project_name}' not found"}

    config_file.unlink()
    return {"success": True, "message": f"Deleted {project_name}"}


# ============================================================================
# BACKGROUND WORKFLOW TOOLS
# ============================================================================


def _run_full_analysis_in_background(task_id: str, project_name: str, **kwargs) -> None:
    """Background worker function for full analysis"""
    try:
        _update_task_progress(task_id, "Starting full analysis workflow")
        result = _run_full_analysis_workflow_impl(project_name, **kwargs)
        _complete_task(task_id, result)
    except Exception as e:
        logging.exception(f"Background task {task_id} failed with exception")
        _fail_task(task_id, str(e))


@mcp.tool()
def run_full_analysis_background(
    project_name: str,
    baseline_path: str | None = None,
    min_severity_level: int = 3,
    rules_json: str | None = None,
    use_filter_qaview: bool | None = None,
    skip_create: bool = False,
) -> dict[str, Any]:
    """
    Start a full QACPP analysis in the background and return immediately.

    This tool starts the analysis as a background task and returns a task_id.
    You can continue using the chat while the analysis runs.

    Use get_task_status(task_id) to check progress.
    Use get_task_result(task_id) to retrieve results when complete.

    Args:
        project_name: Name of the configured project
        baseline_path: Optional baseline for comparison
        min_severity_level: Minimum severity level to report (2-9, default 3)
        rules_json: Optional rules.json for filtering
        use_filter_qaview: Force Filter QAView method
        skip_create: Skip project creation step (default: False)

    Returns:
        task_id that can be used to check status and retrieve results

    Example:
        # Start analysis in background
        result = run_full_analysis_background(
            project_name="MyProject",
            min_severity_level=5
        )
        task_id = result["task_id"]

        # Continue with other work...

        # Check status later
        status = get_task_status(task_id=task_id)

        # Get results when done
        if status["status"] == "completed":
            results = get_task_result(task_id=task_id)
    """
    # Validate project exists
    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Create task
    task_id = str(uuid.uuid4())
    task = BackgroundTask(task_id, "full_analysis", project_name)
    _register_task(task)

    # Start background thread
    kwargs = {
        "baseline_path": baseline_path,
        "min_severity_level": min_severity_level,
        "rules_json": rules_json,
        "use_filter_qaview": use_filter_qaview,
        "skip_create": skip_create,
    }

    thread = threading.Thread(
        target=_run_full_analysis_in_background, args=(task_id, project_name), kwargs=kwargs, daemon=True
    )
    task.thread = thread
    thread.start()

    logging.info(f"Started full analysis in background: {task_id}")

    return {
        "success": True,
        "task_id": task_id,
        "message": f"Analysis started in background. Use get_task_status('{task_id}') to check progress.",
        "project_name": project_name,
    }


def _run_diff_analysis_in_background(task_id: str, project_name: str, **kwargs) -> None:
    """Background worker function for diff analysis"""
    try:
        _update_task_progress(task_id, "Starting diff analysis workflow")
        result = _run_diff_analysis_workflow_impl(project_name, **kwargs)
        _complete_task(task_id, result)
    except Exception as e:
        logging.exception(f"Background task {task_id} failed with exception")
        _fail_task(task_id, str(e))


@mcp.tool()
def run_diff_analysis_background(
    project_name: str,
    merge_base: str,
    compile_commands: str | None = None,
    include_submodules: bool = False,
    min_severity_level: int = 3,
    rules_json: str | None = None,
    use_filter_qaview: bool | None = None,
    source_branch: str | None = None,
    skip_create: bool = False,
) -> dict[str, Any]:
    """
    Start a diff QACPP analysis in the background and return immediately.

    This tool starts the diff analysis as a background task and returns a task_id.
    You can continue using the chat while the analysis runs.

    Use get_task_status(task_id) to check progress.
    Use get_task_result(task_id) to retrieve results when complete.

    Args:
        project_name: Name of the configured project
        merge_base: Git branch to compare against (e.g., "origin/main")
        compile_commands: Optional path to compile_commands.json
        include_submodules: Include git submodules in diff
        min_severity_level: Minimum severity level to report (2-9)
        rules_json: Optional rules.json for filtering
        use_filter_qaview: Force Filter QAView method
        source_branch: Source branch name
        skip_create: Skip project creation step (default: False)

    Returns:
        task_id that can be used to check status and retrieve results

    Example:
        # Start diff analysis in background
        result = run_diff_analysis_background(
            project_name="MyProject",
            merge_base="origin/main",
            source_branch="feature/my-changes"
        )
        task_id = result["task_id"]

        # Continue with other work...

        # Check status later
        status = get_task_status(task_id=task_id)
    """
    # Validate project exists
    config = load_project(project_name)
    if not config:
        return {"success": False, "error": f"Project '{project_name}' not found"}

    # Create task
    task_id = str(uuid.uuid4())
    task = BackgroundTask(task_id, "diff_analysis", project_name)
    _register_task(task)

    # Start background thread
    kwargs = {
        "merge_base": merge_base,
        "compile_commands": compile_commands,
        "include_submodules": include_submodules,
        "min_severity_level": min_severity_level,
        "rules_json": rules_json,
        "use_filter_qaview": use_filter_qaview,
        "source_branch": source_branch,
        "skip_create": skip_create,
    }

    thread = threading.Thread(
        target=_run_diff_analysis_in_background, args=(task_id, project_name), kwargs=kwargs, daemon=True
    )
    task.thread = thread
    thread.start()

    logging.info(f"Started diff analysis in background: {task_id}")

    return {
        "success": True,
        "task_id": task_id,
        "message": f"Diff analysis started in background. Use get_task_status('{task_id}') to check progress.",
        "project_name": project_name,
        "merge_base": merge_base,
    }


def main() -> None:
    """Main entry point for the QAC MCP server"""
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler], force=True)

    logging.info("### Starting Perforce QAC MCP Server ###")
    logging.info(f"Log file: {log_file}")
    logging.info(f"Config dir: {CONFIG_DIR}")
    logging.info(f"Reports dir: {REPORTS_DIR}")

    # Load existing projects
    projects = list_all_projects()
    logging.info(f"Loaded {len(projects)} project(s)")
    for p in projects:
        logging.info(f"  - {p['name']}")

    # Start the MCP server
    transport, host, port = get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)


if __name__ == "__main__":
    main()
