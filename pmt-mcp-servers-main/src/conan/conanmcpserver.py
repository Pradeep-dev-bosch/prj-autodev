"""MCP server for Conan Package Manager.

This server provides comprehensive tools to interact with Conan, the C/C++ package manager,
supporting package management, dependency analysis, project creation, and build operations.

Features:
- Package search and discovery across Conan remotes
- Dependency graph analysis and visualization
- Project scaffolding with templates
- Build profile management
- Cache inspection and package information
- Error analysis and troubleshooting
- Editable package management for development workflows

Environment Variables:
=======================
- CONAN_MCP_CONAN_PATH: (Optional) Path to conan binary, defaults to 'conan'
- ARTIFACTORY_CONNECTION: (Optional) JSON object mapping Artifactory server names to their base URLs
  Example: {"artifactory-02": {"url": "https://artifactory-02.boschdevcloud.com/artifactory", "user": "ntid@bosch.com", "password": "api-token"},
            "artifactory-dev": {"url": "https://dev.artifactory.com/artifactory", "user": "user2", "password": "pass2"}}
  Note: Only the base Artifactory URL is stored. The Conan repository path will be requested from the user.
- TRANSPORT: (Optional) Transport type, defaults to 'stdio'
  * stdio: Standard input/output (default, for MCP clients like Claude Desktop)
  * sse: Server-Sent Events (HTTP streaming)
  * Other transports supported by FastMCP
- HOST: (Optional) Host for non-stdio transport, defaults to '127.0.0.1'
- HOST_PORT: (Optional) Port for non-stdio transport, defaults to '8000'
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path

from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("conan")

# Maximum number of dependencies to display in summary
MAX_DISPLAYED_DEPS = 10


def _get_conan_binary() -> str:
    """Get the Conan binary path from environment variable or default to 'conan'.

    Returns:
        Path to conan binary. Defaults to 'conan' if CONAN_MCP_CONAN_PATH is not set.
    """
    return os.environ.get("CONAN_MCP_CONAN_PATH", "conan")


async def run_command(
    cmd: list[str], timeout: float = 30.0, cwd: str | None = None
) -> str:
    """Execute a command and return the output.

    Args:
        cmd: List of command arguments (e.g., ["conan", "search", "boost"])
        timeout: Timeout in seconds
        cwd: Working directory where the command should be executed (optional)

    Returns:
        Command output as string

    Raises:
        RuntimeError: If command is not found or fails
    """
    proc = None
    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.DEVNULL,
            cwd=cwd,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)

        if proc.returncode == 0:
            logging.debug(f"Command succeeded: {' '.join(cmd[:3])}")
            return stdout.decode("utf-8", "replace")
        else:
            error_msg = stderr.decode("utf-8", "replace").strip()
            if not error_msg:
                error_msg = f"Conan command failed with return code {proc.returncode}"
            logging.error(f"Command failed: {' '.join(cmd[:3])} - {error_msg[:200]}")
            raise RuntimeError(f"Command error: {error_msg}")
    except asyncio.TimeoutError:
        if proc:
            proc.kill()
        logging.error(f"Command timeout after {timeout}s: {' '.join(cmd[:3])}")
        raise RuntimeError(f"Command timeout after {timeout}s")
    except asyncio.CancelledError:
        if proc:
            proc.kill()
        logging.warning(f"Command cancelled: {' '.join(cmd[:3])}")
        raise
    except FileNotFoundError:
        logging.error(f"Command not found: {cmd[0]}")
        raise RuntimeError("Command not found.")
    except Exception as e:
        logging.error(f"Error running command: {str(e)}", exc_info=True)
        raise RuntimeError(f"Error running command: {str(e)}")


def _analyze_conan_error(log_content: str) -> dict:
    """Analyze Conan log content and extract error information with solutions.

    Args:
        log_content: Content of the Conan log file or error output

    Returns:
        Dictionary containing error analysis and suggested solutions
    """
    errors_found = []
    error_patterns = {
        # Missing package errors
        "missing_package": {
            "patterns": [
                r"ERROR: Missing binary: (.+)",
                r"ERROR: Missing prebuilt package for '(.+)'",
                r"Can't find a '(.+)' package",
            ],
            "solution": (
                "The required binary package is not available in the cache or remotes. "
                "Solutions:\n"
                "1. Add '--build=missing' to build the package from source\n"
                "2. Check if the package exists for your settings (arch, os, compiler)\n"
                "3. Use 'list_conan_packages' to verify available binaries\n"
                "4. Adjust your profile settings to match available packages"
            ),
        },
        # Version conflicts
        "version_conflict": {
            "patterns": [
                r"ERROR: Version conflict: (.+)",
                r"Conflict between (.+) and (.+)",
                r"ERROR: Requirement (.+) conflicts with",
            ],
            "solution": (
                "There's a version conflict in your dependency tree. "
                "Solutions:\n"
                "1. Check dependency versions using 'get_dependency_graph'\n"
                "2. Use version ranges to allow flexibility: [>=1.0 <2.0]\n"
                "3. Override the conflicting version in your conanfile\n"
                "4. Check if a newer version of dependencies is available"
            ),
        },
        # Recipe not found
        "recipe_not_found": {
            "patterns": [
                r"ERROR: Recipe not found: '(.+)'",
                r"ERROR: Unable to find '(.+)' in remotes",
                r"Package '(.+)' not found in",
            ],
            "solution": (
                "The recipe/package was not found in any remote. "
                "Solutions:\n"
                "1. Check the package name and version are correct\n"
                "2. Verify the remote is configured: conan remote list\n"
                "3. Search for the package: 'list_conan_packages'\n"
                "4. Check if the package name has changed or been deprecated"
            ),
        },
        # Settings compatibility
        "settings_incompatible": {
            "patterns": [
                r"Invalid setting '(.+)'",
                r"ERROR: Invalid setting",
                r"'(.+)' is not a valid",
                r"does not support (.+)",
            ],
            "solution": (
                "Package settings are incompatible or invalid. "
                "Solutions:\n"
                "1. Check your profile settings using 'get_conan_profile'\n"
                "2. Verify the package supports your OS/arch/compiler\n"
                "3. Use 'list_conan_packages' with filter_settings to check available configs\n"
                "4. Update your profile to use supported settings"
            ),
        },
        # Options errors
        "invalid_option": {
            "patterns": [
                r"ERROR: option '(.+)' doesn't exist",
                r"Unknown option '(.+)'",
                r"Invalid option",
            ],
            "solution": (
                "An invalid option was specified. "
                "Solutions:\n"
                "1. Check available options in the package recipe\n"
                "2. Use 'get_dependency_graph' to see package options\n"
                "3. Remove or correct the invalid option in your conanfile or command line"
            ),
        },
        # Network/remote errors
        "network_error": {
            "patterns": [
                r"ERROR: Error downloading",
                r"Connection error",
                r"Timeout",
                r"Unable to connect",
                r"ConnectionError",
            ],
            "solution": (
                "Network or remote connection error. "
                "Solutions:\n"
                "1. Check your internet connection\n"
                "2. Verify remote URL is accessible\n"
                "3. Check if you need authentication for the remote\n"
                "4. Try using a different remote or mirror"
            ),
        },
        # Recipe/build errors
        "build_error": {
            "patterns": [
                r"ERROR: Package '(.+)' build failed",
                r"Build error",
                r"CMake Error",
                r"Compiler error",
            ],
            "solution": (
                "Package failed to build from source. "
                "Solutions:\n"
                "1. Check if you have the required compiler and build tools installed\n"
                "2. Verify your compiler version is supported\n"
                "3. Check build logs for specific compilation errors\n"
                "4. Try using a prebuilt binary instead (remove --build=missing)"
            ),
        },
        # Profile errors
        "profile_error": {
            "patterns": [
                r"ERROR: Profile '(.+)' not found",
                r"Profile does not exist",
                r"Error loading profile",
            ],
            "solution": (
                "Profile not found or invalid. "
                "Solutions:\n"
                "1. List available profiles using 'list_conan_profiles'\n"
                "2. Create the profile or use the default profile\n"
                "3. Check profile path and name spelling"
            ),
        },
        # Revision errors
        "revision_error": {
            "patterns": [
                r"ERROR: Recipe revision '(.+)' not found",
                r"Package revision .+ does not exist",
            ],
            "solution": (
                "Specific recipe or package revision not found. "
                "Solutions:\n"
                "1. Use 'list_conan_packages' to check available revisions\n"
                "2. Remove the revision specifier to use the latest\n"
                "3. Check if the revision has been removed or replaced"
            ),
        },
    }

    # Analyze log for each error pattern
    for error_type, error_info in error_patterns.items():
        for pattern in error_info["patterns"]:
            matches = re.findall(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            if matches:
                errors_found.append(
                    {
                        "type": error_type,
                        "matched_text": matches[0] if isinstance(matches[0], str) else " ".join(matches[0]),
                        "solution": error_info["solution"],
                    }
                )
                break  # Only report each error type once

    # Extract ERROR: lines for context
    error_lines = []
    for line in log_content.split("\n"):
        if "ERROR:" in line.upper() or "WARN:" in line.upper():
            error_lines.append(line.strip())

    if errors_found:
        logging.warning(f"Conan error analysis found {len(errors_found)} error(s)")
        for error in errors_found:
            logging.debug(f"Error type: {error['type']} - {error['matched_text']}")

    return {
        "errors_detected": len(errors_found) > 0,
        "error_count": len(errors_found),
        "errors": errors_found,
        "error_lines": error_lines[:20],  # Limit to first 20 error lines
    }


@mcp.tool(
    description="""Search for Conan packages across remotes with filtering by version, settings, and options.

    Args:
        name: Package name pattern (required). Wildcards: "fmt", "fmt*", "*fmt*", "*fmt"
        version: Version or range (default: "*"). Examples: "1.2.3", "[>=1.0 <2.0]", "[~1.2]", "[^1.0]"
        user: User name (default: None). Use "*" for all users.
        channel: Channel name (default: None). Use "*" for all channels.
        recipe_revision: Recipe revision (rrev). Use "*" for all, "latest" for latest.
        package_id: Package ID. Use "*" for all packages.
        filter_settings: Filter by settings. Examples: ["arch=armv8", "os=Windows", "build_type=Release"]
        filter_options: Filter by options. Examples: ["*:fPIC=True", "*:shared=False"]
            - ["*:header_only=True"] : header only
            - ["*:shared=False"] : shared library
            - ["*:with_boost=True"] : with boost option
        remote: Remote name (default: "*").
            - None: Search in local cache only
            - "conancenter": Search in ConanCenter remote
            - "*": Search in all remotes
            - Other remote names: Search in specific remote
        search_in_cache: Include local cache in search (default: False).
            - True: Search in both remotes and local cache
            - False: Search only in remotes (default)
            Note: This parameter should be set consistently across requests.
        include_all_package_revisions: Include all package revisions (default: False).
            - True: Include all package revisions.
            - False: Include only the latest package revision (default)

    Returns:
        Dictionary containing available packages and their metadata.

     Examples:
         - list_conan_packages(name="fmt", version="1.0.0")
         - list_conan_packages(name="*boost*", filter_settings=["arch=armv8", "os=Windows"])
         - list_conan_packages(name="zlib", filter_options=["*:shared=True"])
    """
)
async def list_conan_packages(
    name: str = Field(description="Package name pattern (supports wildcards)"),
    version: str = Field(
        default="*", description="Version or version range to search for."
    ),
    user: str = Field(
        default=None, description="User name. Use * to search all users."
    ),
    channel: str = Field(
        default=None, description="Channel name. Use * to search all channels."
    ),
    recipe_revision: str = Field(
        default=None,
        description='Recipe revision number also known as rrev. Use * to search all revisions. Use "latest" to search the latest revision.',
    ),
    package_id: str = Field(
        default=None, description="Package ID. Use * to search all packages."
    ),
    filter_settings: list[str] = Field(
        default=None,
        description="Filter settings like architecture, operating system, build type, compiler, compiler version, compiler runtime, compiler runtime version.",
    ),
    filter_options: list[str] = Field(
        default=None,
        description="Filter options like fPIC, header_only, shared, with_*, without_*, etc.",
    ),
    remote: str = Field(default="*", description="Name of the remote to search in."),
    search_in_cache: bool = Field(
        default=False, description="Include local cache in search"
    ),
    include_all_package_revisions: bool = Field(
        default=False, description="Include all package revisions"
    ),
) -> dict:
    if (filter_settings or filter_options) and not package_id:
        # No package ID provided, searching for all packages
        package_id = "*"

    pattern = f"{name}/{version if version else '*'}"
    pattern += (
        f"@{user if user else '*'}/{channel if channel else '*'}"
        if user or channel
        else ""
    )
    pattern += f"#{recipe_revision}" if recipe_revision else ""
    if package_id:
        pattern += f":{package_id}"
        pattern += "#*" if include_all_package_revisions else ""

    logging.info(f"Searching for Conan packages: {pattern}")

    cmd = [_get_conan_binary(), "list", pattern, "--format=json"]
    if remote:
        cmd.append(f"--remote={remote}")
    if filter_settings:
        for fs in filter_settings:
            cmd.append(f"-fs={fs}")
    if filter_options:
        for fo in filter_options:
            cmd.append(f"-fo={fo}")
    if search_in_cache:
        cmd.append("--cache")
    raw_output = await run_command(cmd)
    
    result = json.loads(raw_output)
    logging.info(f"Found {len(result.get('Local Cache', {}).get('Local Cache', {}))} cached items and {len([k for k in result.keys() if k != 'Local Cache'])} remote results")
    
    return result


@mcp.tool(
    description="""List Conan packages from an Artifactory remote repository using Conan commands.

    This tool helps you discover and list Conan packages from Artifactory servers. 
    It uses Conan's native 'conan list' command to search packages in remotes.

    **Smart Workflow:**
    1. If remote_name is provided and exists in Conan: Uses it directly
    2. If remote_name doesn't exist but ARTIFACTORY_CONNECTION is configured:
       - Interprets remote_name as repository_name
       - Asks user to choose Artifactory server (if not provided)
       - Constructs full URL: {base_url}/api/conan/{repository_name}
       - Adds remote to Conan as: {artifactory_name}-{repository_name}
    3. If no remote_name but artifactory_name provided:
       - Asks for repository_name if not provided
       - Constructs full URL and adds remote
    4. Authenticates with credentials and searches packages
    5. **Case-insensitive search**: If package_pattern is a simple name (no wildcards), 
       automatically converts to '*pattern*' for case-insensitive matching

    **Environment Variables (Optional):**
    - ARTIFACTORY_CONNECTION: JSON object with Artifactory server configurations (base URLs only)
      Example: {"artifactory-prod": {"url": "https://artifactory.example.com/artifactory", "user": "user1", "password": "pass1"}}
      Note: Only base URL is stored; repository path is requested from user

    **Use Cases:**
    - "List packages from lab000136-recompute-ci-local" (tool asks which Artifactory)
    - "Find Serialize package in lab000136-recompute-ci-local" (case-insensitive auto-search)
    - "Show serialize packages from lab000136-recompute-ci-local in artifactory-prod"
    - "List packages from conancenter" (uses existing Conan remote)

    Examples:
        - list_packages_from_remote(remote_name="lab000136-recompute-ci-local", package_pattern="serialize")
          → Tool: "Which Artifactory? artifactory-prod or artifactory-dev?"
          → Searches with pattern: "*serialize*" (case-insensitive)
        
        - list_packages_from_remote(remote_name="lab000136-recompute-ci-local", artifactory_name="artifactory-prod", package_pattern="Serialize")
          → Constructs: https://artifactory.example.com/artifactory/api/conan/lab000136-recompute-ci-local
          → Adds as: artifactory-prod-lab000136-recompute-ci-local
          → Searches with pattern: "*Serialize*" (matches serialize, Serialize, SERIALIZE)
        
        - list_packages_from_remote(artifactory_name="artifactory-prod", repository_name="conan-local")
          → Explicit Artifactory workflow
          → Searches all packages (pattern="*")
        
        - list_packages_from_remote(remote_name="conancenter", package_pattern="boost*")
          → Uses existing Conan remote directly
          → Searches packages starting with "boost"

    Args:
        remote_name: Conan remote name OR repository name. If exists in Conan, uses it directly. 
                    If not found, interprets as repository_name and asks for Artifactory.
        artifactory_name: Name of Artifactory server from ARTIFACTORY_CONNECTION env var (optional)
        repository_name: Conan repository name in Artifactory (e.g., "conan-local", "lab000136-recompute-ci-local")
        package_pattern: Filter packages by pattern (e.g., "mycompany/*", "boost*", "*fmt*")
        username: Override username from env var (optional)
        password: Override password from env var (optional)

    Returns:
        Dictionary containing:
        - "packages": List of package references found
        - "count": Total number of packages
        - "remote_name": Conan remote name used
        - "remote_url": Full Conan remote URL constructed
        - "remote_added": Whether remote was added to Conan
        - "prompt": User prompt for missing information (if applicable)
        - "error": Error message if operation failed
    """
)
async def list_packages_from_remote(
    artifactory_name: str = Field(
        default=None,
        description="Name of Artifactory server from ARTIFACTORY_CONNECTION environment variable. If not provided, user will be asked to choose."
    ),
    repository_name: str = Field(
        default=None,
        description="Conan repository name in Artifactory (e.g., 'conan-local', 'conan-remote', 'conan-stable'). Required for Artifactory URLs."
    ),
    remote_name: str = Field(
        default=None,
        description="Use an existing Conan remote name instead of constructing from Artifactory. Bypasses Artifactory workflow."
    ),
    package_pattern: str = Field(
        default="*",
        description="Package name pattern to search for. Examples: 'serialize', 'boost*', '*fmt*', 'mycompany/*'. Use '*' for all packages. NOTE: Conan search is case-sensitive by default. For case-insensitive search, use wildcards: '*serialize*' will match 'Serialize', 'SERIALIZE', 'serialize', etc."
    ),
    username: str = Field(
        default=None,
        description="Username for authentication. Overrides value from ARTIFACTORY_CONNECTION if provided."
    ),
    password: str = Field(
        default=None,
        description="Password or API key for authentication. Overrides value from ARTIFACTORY_CONNECTION if provided."
    ),
) -> dict:
    """List Conan packages from Artifactory or existing Conan remote."""
    
    result = {
        "packages": [],
        "count": 0,
        "remote_added": False
    }
    
    # Load Artifactory base URLs from environment (we'll need this for both options)
    artifactory_configs = {}
    artifactory_urls_json = os.environ.get("ARTIFACTORY_CONNECTION")
    
    if artifactory_urls_json:
        try:
            artifactory_configs = json.loads(artifactory_urls_json)
            logging.info(f"Loaded {len(artifactory_configs)} Artifactory servers from ARTIFACTORY_CONNECTION")
        except json.JSONDecodeError as e:
            logging.warning(f"Failed to parse ARTIFACTORY_CONNECTION: {e}")
    
    # Get list of existing Conan remotes first
    try:
        cmd = [_get_conan_binary(), "remote", "list", "--format=json"]
        raw_output = await run_command(cmd)
        conan_remotes = json.loads(raw_output)
        conan_remote_names = [r["name"] for r in conan_remotes.get("remotes", [])]
        logging.info(f"Found {len(conan_remote_names)} existing Conan remotes: {conan_remote_names}")
    except Exception as e:
        logging.error(f"Failed to list Conan remotes: {e}")
        conan_remotes = {"remotes": []}
        conan_remote_names = []
    
    # OPTION 1: User wants to use an existing Conan remote (bypass Artifactory workflow)
    if remote_name:
        if remote_name in conan_remote_names:
            # Remote exists - use it directly
            selected_remote_name = remote_name
            result["remote_name"] = selected_remote_name
            logging.info(f"Using existing Conan remote: {selected_remote_name}")
        else:
            # Remote doesn't exist - try to interpret it as a repository name
            logging.info(f"Remote '{remote_name}' not found in Conan. Checking if we can add it from Artifactory...")
            
            if not artifactory_configs:
                result["error"] = f"Remote '{remote_name}' not found in Conan remotes and no Artifactory servers configured"
                result["available_remotes"] = conan_remote_names
                result["help"] = "Either use an existing remote from the list or configure ARTIFACTORY_CONNECTION environment variable"
                return result
            
            # Treat remote_name as repository_name and ask user to choose Artifactory
            if not artifactory_name:
                result["interpreted_as_repository"] = remote_name
                result["available_artifactories"] = list(artifactory_configs.keys())
                result["prompt"] = f"The repository '{remote_name}' is not configured as a Conan remote. Which Artifactory server should I use to access it?"
                result["options"] = list(artifactory_configs.keys())
                result["help"] = f"Please specify artifactory_name to add '{remote_name}' repository. Available: {', '.join(artifactory_configs.keys())}"
                return result
            
            # We have both remote_name (as repo) and artifactory_name - construct URL
            if artifactory_name not in artifactory_configs:
                result["error"] = f"Artifactory '{artifactory_name}' not found in ARTIFACTORY_CONNECTION"
                result["available_artifactories"] = list(artifactory_configs.keys())
                return result
            
            # Use remote_name as repository_name
            repository_name = remote_name
            artifactory_config = artifactory_configs[artifactory_name]
            base_url = artifactory_config.get("url").rstrip("/")
            full_remote_url = f"{base_url}/api/conan/{repository_name}"
            
            # Use credentials from config if not provided
            if not username:
                username = artifactory_config.get("user")
            if not password:
                password = artifactory_config.get("password")
            
            # Generate unique remote name
            selected_remote_name = f"{artifactory_name}-{repository_name}"
            
            # Add the remote to Conan
            try:
                add_cmd = [_get_conan_binary(), "remote", "add", selected_remote_name, full_remote_url]
                await run_command(add_cmd)
                logging.info(f"Added Conan remote: {selected_remote_name} -> {full_remote_url}")
                result["remote_added"] = True
                result["remote_url"] = full_remote_url
                
                # Login if credentials provided
                if password:
                    login_cmd = [_get_conan_binary(), "remote", "login", selected_remote_name]
                    if username:
                        login_cmd.extend([username, "-p", password])
                    else:
                        login_cmd.extend(["-p", password])
                    await run_command(login_cmd)
                    logging.info(f"Logged in to remote: {selected_remote_name}")
                
            except Exception as e:
                result["error"] = f"Failed to add remote '{selected_remote_name}': {str(e)}"
                return result
            
            result["remote_name"] = selected_remote_name
            result["artifactory_name"] = artifactory_name
            result["repository_name"] = repository_name
            logging.info(f"Constructed remote '{selected_remote_name}' from Artifactory '{artifactory_name}' and repository '{repository_name}'")
    
    # OPTION 2: User wants to use Artifactory (construct URL from base + repository)
    else:
        # Check if we have Artifactory configurations
        if not artifactory_configs:
            # No Artifactory configs and no remote_name - show available remotes
            if conan_remote_names:
                result["available_remotes"] = conan_remote_names
                result["prompt"] = f"Which remote would you like to use? Available: {', '.join(conan_remote_names)}"
                result["help"] = "Please provide remote_name parameter or configure ARTIFACTORY_CONNECTION environment variable"
                return result
            else:
                result["error"] = "No Conan remotes configured and no Artifactory servers configured"
                result["help"] = "Please add a remote using 'conan remote add' or configure ARTIFACTORY_CONNECTION environment variable"
                return result
        
        # We have Artifactory configs - proceed with Artifactory workflow
        # Step 1: If artifactory_name not provided, ask user to choose
        if not artifactory_name:
            result["available_artifactories"] = list(artifactory_configs.keys())
            result["prompt"] = f"Which Artifactory server would you like to use? Available: {', '.join(artifactory_configs.keys())}"
            result["help"] = "Please provide artifactory_name parameter"
            if conan_remote_names:
                result["available_remotes"] = conan_remote_names
                result["alternative"] = f"Or use remote_name to select an existing Conan remote: {', '.join(conan_remote_names)}"
            return result
        
        # Step 2: Validate artifactory_name exists
        if artifactory_name not in artifactory_configs:
            result["error"] = f"Artifactory '{artifactory_name}' not found in ARTIFACTORY_CONNECTION"
            result["available_artifactories"] = list(artifactory_configs.keys())
            result["help"] = f"Available Artifactory servers: {', '.join(artifactory_configs.keys())}"
            return result
        
        # Step 3: If repository_name not provided, ask user
        if not repository_name:
            result["prompt"] = "Please provide the Conan repository name (e.g., 'conan-local', 'conan-remote', 'lab000136-recompute-ci-local')"
            result["help"] = "The repository name will be appended to the Artifactory base URL to form the complete Conan remote URL"
            result["example"] = f"For Artifactory base URL: {artifactory_configs[artifactory_name].get('url')}, you might use repository names like: 'conan-local', 'conan-remote', or 'lab000136-recompute-ci-local'"
            return result
        
        # Step 4: Construct the full Conan remote URL
        artifactory_config = artifactory_configs[artifactory_name]
        base_url = artifactory_config.get("url")
        
        # Remove trailing slash from base URL if present
        base_url = base_url.rstrip("/")
        
        # Construct full Conan remote URL: {base_url}/api/conan/{repository_name}
        full_remote_url = f"{base_url}/api/conan/{repository_name}"
        
        # Use credentials from config if not provided as parameters
        if not username:
            username = artifactory_config.get("user")
        if not password:
            password = artifactory_config.get("password")
        
        # Step 5: Generate a unique remote name for this Artifactory + repository combination
        selected_remote_name = f"{artifactory_name}-{repository_name}"
        
        # Step 6: Check if this remote already exists in Conan
        if selected_remote_name not in conan_remote_names:
            # Add the remote to Conan
            try:
                add_cmd = [_get_conan_binary(), "remote", "add", selected_remote_name, full_remote_url]
                await run_command(add_cmd)
                logging.info(f"Added Conan remote: {selected_remote_name} -> {full_remote_url}")
                result["remote_added"] = True
                result["remote_url"] = full_remote_url
                
                # Login if credentials provided
                if password:
                    login_cmd = [_get_conan_binary(), "remote", "login", selected_remote_name]
                    if username:
                        login_cmd.extend([username, "-p", password])
                    else:
                        login_cmd.extend(["-p", password])
                    await run_command(login_cmd)
                    logging.info(f"Logged in to remote: {selected_remote_name}")
                
            except Exception as e:
                result["error"] = f"Failed to add remote '{selected_remote_name}': {str(e)}"
                return result
        else:
            logging.info(f"Using existing Conan remote: {selected_remote_name}")
            result["remote_url"] = full_remote_url
        
        result["remote_name"] = selected_remote_name
        result["artifactory_name"] = artifactory_name
        result["repository_name"] = repository_name
    
    # Step 8: Search for packages in the selected remote
    # Make search case-insensitive by wrapping pattern in wildcards if it's a simple name
    search_pattern = package_pattern
    if package_pattern != "*" and not any(c in package_pattern for c in ['*', '/', '@']):
        # Simple package name without wildcards - make it case-insensitive
        search_pattern = f"*{package_pattern}*"
        logging.info(f"Converting '{package_pattern}' to case-insensitive pattern: '{search_pattern}'")
    
    logging.info(f"Searching for packages matching '{search_pattern}' in remote: {result['remote_name']}")
    
    try:
        # Use conan list command to search packages
        list_cmd = [_get_conan_binary(), "list", search_pattern, "-r", result["remote_name"], "--format=json"]
        
        raw_output = await run_command(list_cmd, timeout=60.0)
        list_result = json.loads(raw_output)
        
        # Extract package references from the result
        packages = []
        
        # The result format is: {<remote_name>: {<package_ref>: {...}}}
        if result["remote_name"] in list_result:
            remote_data = list_result[result["remote_name"]]
            for pkg_ref in remote_data.keys():
                if pkg_ref and pkg_ref != result["remote_name"]:
                    packages.append(pkg_ref)
        
        logging.info(f"Found {len(packages)} packages matching '{package_pattern}' in remote {result['remote_name']}")
        
        result.update({
            "packages": sorted(packages),
            "count": len(packages),
            "package_pattern": package_pattern,
            "search_pattern_used": search_pattern,
            "case_insensitive": search_pattern != package_pattern,
            "message": f"Successfully listed {len(packages)} packages from remote '{result['remote_name']}'"
        })
        
        return result
            
    except Exception as e:
        error_msg = f"Failed to list packages: {str(e)}"
        logging.error(f"Conan list error: {error_msg}")
        result["error"] = error_msg
        result["help"] = "Check that the remote is accessible and you have proper authentication. You may need to run 'conan remote login <remote>'"
        return result


@mcp.tool(
    description="""Get Conan profile configuration for default or specific profile.

    Retrieve host and build profile settings (compiler, arch, build_type, etc.).
    Use before platform-specific operations or package recommendations.

    Args:
        profile: Optional absolute path to profile file. If not provided, uses default profile.

    Returns:
        Dictionary with "host" and "build" profile configurations.
    """
)
async def get_conan_profile(
    profile: str = Field(
        default=None,
        description="Absolute path to profile file. If not provided, uses the default profile.",
    ),
) -> dict:
    logging.info(f"Retrieving Conan profile: {profile or 'default'}")
    cmd = [_get_conan_binary(), "profile", "show", "--format=json"]
    if profile:
        profile_path = Path(profile).expanduser().resolve()
        if not profile_path.exists():
            raise FileNotFoundError(f"Profile path does not exist: {profile_path}")
        cmd.append(f"--profile={str(profile_path)}")
    raw_output = await run_command(cmd)
    return json.loads(raw_output)


@mcp.tool(
    description="""List Conan profiles available.

    Use this tool to see which profiles are available to select or inspect.

    Returns:
        List of profile names.
    """
)
async def list_conan_profiles() -> list[str]:
    cmd = [_get_conan_binary(), "profile", "list", "--format=json"]
    raw_output = await run_command(cmd)
    return json.loads(raw_output)


@mcp.tool(
    description="""Discover Conan profiles for a package in tools/conan/profiles/<package_name>.

    **CRITICAL Workflow:**
    1. User mentions package or profile keyword (e.g., "install ref with premium", "ARM profile")
    2. Call this tool with package_name and optional keyword
    3. Present ALL discovered profiles to user for selection
    4. Wait for user selection
    5. Use selected profile path in install_conan_packages

    DO NOT guess profile paths - always discover first.

    Args:
        package_name: Package name (e.g., "ref", "mypackage")
        work_dir: Project root where tools/conan/profiles is located
        profile_dir: Custom profile directory relative to work_dir (default: "tools/conan/profiles")
        keyword: Optional filter (e.g., "premium", "vpx", "ARM", "M7", "GCC")

    Returns:
        Dictionary with discovered profiles for user selection.
        - "profiles_found": List of profiles - SHOW THESE TO USER
        - "options_for_user": Formatted options - USE THESE FOR PRESENTATION
        - "prompt_template": Ready-to-use prompt for asking user to choose
    """
)
async def discover_package_profiles(
    package_name: str = Field(description="Package name to find profiles for"),
    work_dir: str = Field(description="Working directory (project root)"),
    profile_dir: str = "tools/conan/profiles",
    keyword: str | None = None,
) -> dict:
    """Discover Conan profiles for a specific package."""

    logging.info(f"Discovering profiles for package '{package_name}' in '{work_dir}'")
    if keyword:
        logging.info(f"Filtering by keyword: '{keyword}'")

    base_dir = Path(work_dir).expanduser().resolve()
    profiles_base = base_dir / profile_dir
    package_profiles_dir = profiles_base / package_name

    result = {
        "package_name": package_name,
        "profiles_found": [],
        "profile_directory": str(package_profiles_dir),
        "count": 0,
        "recommendation": None,
    }

    # Check if the package-specific profile directory exists
    if not package_profiles_dir.exists():
        logging.warning(f"Profile directory not found: {package_profiles_dir}")
        result["error"] = f"Profile directory not found: {package_profiles_dir}"
        result["suggestion"] = f"Try checking if profiles exist in: {profiles_base}"

        # List available package directories
        if profiles_base.exists():
            available_packages = [d.name for d in profiles_base.iterdir() if d.is_dir()]
            result["available_packages"] = sorted(available_packages)
            logging.info(f"Found {len(available_packages)} package directories")

        return result

    # Discover all profiles in the directory
    all_profiles = []
    for item in package_profiles_dir.iterdir():
        if item.is_file() and not item.name.startswith('.'):
            # It's a profile file
            profile_path = f"{profile_dir}/{package_name}/{item.name}"
            all_profiles.append({
                "name": item.name,
                "path": profile_path,
                "full_path": str(item),
                "type": "file"
            })
        elif item.is_dir() and item.name not in ['__pycache__', '.']:
            # It's a subdirectory (e.g., "interface")
            for subitem in item.iterdir():
                if subitem.is_file() and not subitem.name.startswith('.'):
                    profile_path = f"{profile_dir}/{package_name}/{item.name}/{subitem.name}"
                    all_profiles.append({
                        "name": f"{item.name}/{subitem.name}",
                        "path": profile_path,
                        "full_path": str(subitem),
                        "type": "subdirectory"
                    })

    logging.info(f"Found {len(all_profiles)} total profiles for '{package_name}'")

    # Filter by keyword if provided
    if keyword:
        keyword_lower = keyword.lower()
        filtered_profiles = [
            p for p in all_profiles
            if keyword_lower in p["name"].lower()
        ]
        logging.info(f"Filtered to {len(filtered_profiles)} profiles matching keyword '{keyword}'")
    else:
        filtered_profiles = all_profiles

    result["profiles_found"] = filtered_profiles
    result["count"] = len(filtered_profiles)

    # Provide recommendation and user action prompt
    if result["count"] == 0:
        if keyword:
            result["recommendation"] = f"No profiles match keyword '{keyword}'. Available profiles: {len(all_profiles)}"
            result["all_profiles_count"] = len(all_profiles)
            result["user_action"] = "Try removing the keyword filter or use a different keyword to see all available profiles."
        else:
            result["recommendation"] = "No profiles found in this directory"
            result["user_action"] = "Check if the package name is correct or if profiles exist in a different location."
    elif result["count"] == 1:
        result["recommendation"] = f"Only one profile found: {filtered_profiles[0]['path']}"
        result["suggested_profile"] = filtered_profiles[0]["path"]
        result["user_action"] = f"You can proceed with this profile, or ask the user to confirm: '{filtered_profiles[0]['name']}'"
    else:
        result["recommendation"] = f"Found {result['count']} profiles. User must choose one from the list."
        result["user_action"] = "PRESENT THE FOLLOWING OPTIONS TO THE USER AND ASK THEM TO CHOOSE:"

        # Format profiles for easy selection
        result["options_for_user"] = [
            {
                "option_number": idx + 1,
                "profile_name": p["name"],
                "profile_path": p["path"],
                "description": f"Profile: {p['name']} (path: {p['path']})"
            }
            for idx, p in enumerate(filtered_profiles)
        ]

        result["prompt_template"] = (
            f"I found {result['count']} profiles for {package_name}. "
            "Please choose one:\n\n" +
            "\n".join([
                f"{opt['option_number']}. {opt['profile_name']}"
                for opt in result["options_for_user"]
            ]) +
            "\n\nWhich profile would you like to use?"
        )

        # Try to identify common profile types
        profile_types = {
            "arm": [p for p in filtered_profiles if "arm" in p["name"].lower()],
            "gcc": [p for p in filtered_profiles if "gcc" in p["name"].lower()],
            "linux": [p for p in filtered_profiles if "linux" in p["name"].lower()],
            "debug": [p for p in filtered_profiles if "debug" in p["name"].lower()],
            "release": [p for p in filtered_profiles if "release" in p["name"].lower()],
        }

        suggestions = []
        for ptype, profiles in profile_types.items():
            if profiles and len(profiles) < result["count"]:
                suggestions.append(f"For {ptype.upper()}: filter with keyword='{ptype}'")

        if suggestions:
            result["filter_suggestions"] = suggestions

    return result


@mcp.tool(
    description="""
    List which versions and binaries of a Conan package reside in the local cache.

    Use this tool when you need to:
    - Check what versions of a package are already downloaded/cached locally
    - Find which package binaries are available in cache for different configurations
    - Verify if a package is cached before attempting installation
    - See all cached recipe revisions and package revisions for a package

    This tool searches ONLY in the local Conan cache, not in remotes.

    Examples:
        - list_cached_packages(name="fmt") - List all cached versions of fmt
        - list_cached_packages(name="fmt", version="10.0.0") - List cached fmt/10.0.0 binaries
        - list_cached_packages(name="*boost*") - List all cached packages containing "boost"

    Args:
        name: Package name pattern (required). Supports wildcards:
            - "fmt" : exact name
            - "fmt*" : starts with "fmt"
            - "*fmt*" : contains "fmt"
        version: Version or version range (optional). Supports Conan2 syntax:
            - "10.0.0" : exact version
            - "*" : all versions (default)
        user: User name (optional). Use "*" for all users.
        channel: Channel name (optional). Use "*" for all channels.
        package_id: Package ID (optional). Use "*" to list all cached binaries.

    Returns:
        Dictionary containing cached packages with their versions, recipe revisions,
        and package binaries (if package_id is specified).
    """
)
async def list_cached_packages(
    name: str = Field(description="Package name pattern (supports wildcards)"),
    version: str = Field(
        default="*", description="Version or version range to search for."
    ),
    user: str = Field(
        default=None, description="User name. Use * to search all users."
    ),
    channel: str = Field(
        default=None, description="Channel name. Use * to search all channels."
    ),
    package_id: str = Field(
        default=None,
        description="Package ID. Use * to list all cached binaries for the package.",
    ),
) -> dict:
    pattern = f"{name}/{version if version else '*'}"
    pattern += (
        f"@{user if user else '*'}/{channel if channel else '*'}"
        if user or channel
        else ""
    )
    if package_id:
        pattern += f":{package_id}"

    cmd = [_get_conan_binary(), "list", pattern, "--cache", "--format=json"]
    raw_output = await run_command(cmd)
    return json.loads(raw_output)


@mcp.tool(
    description="""Install Conan package dependencies from a recipe file.

    ⚠️ **For custom profiles: Call discover_package_profiles FIRST, then use selected profile path.**

    **CORRECT workflow for customer projects:**
    1. Call discover_package_profiles(package_name="ref", keyword="premium")
    2. Show discovered profiles to user
    3. Wait for user selection
    4. Call THIS tool with the exact profile path user selected

    Installs dependencies, generates conan.lock and conaninfo.json in work_dir.

    Args:
        path: Path to recipe folder or file (conanfile.txt/py), relative to work_dir.
        work_dir: Working directory (base for all paths). Always required.
        remote: Optional remote name (searches all if not specified)
        search_in_cache: Resolve exclusively in cache, don't use remotes.
        build_profile: Profile for build context.
        host_profile: Profile for host context. Use discover_package_profiles first for custom profiles.
        settings_host: Substitute settings (e.g., ["arch=armv8", "os=Windows", "build_type=Release"])
        options_host: Substitute options (e.g., ["*:fPIC=True", "&:shared=False"])
        build_missing: Build missing binaries from source

    Returns:
        JSON with dependency graph. Generates conan.lock and conaninfo.json in work_dir.
        Binary/recipe status: Missing, Invalid, Build, Cache, Skip, Download, or null.
    """
)
async def install_conan_packages(
    path: str = Field(
        description="Path to the folder containing the recipe of the project or to a recipe file conanfile.txt/.py"
    ),
    work_dir: str = Field(
        description="Working directory where the command should be executed. This is the base directory from which all paths are resolved. Always required."
    ),
    remote: str = Field(
        default=None, description="Remote name. Omit to search in all remotes."
    ),
    search_in_cache: bool = Field(
        default=False,
        description="Do not use remote, resolve exclusively in the cache.",
    ),
    build_profile: str = Field(
        default=None,
        description="Profile to the build context.",
    ),
    host_profile: str = Field(
        default=None,
        description="Profile to the host context.",
    ),
    settings_host: list[str] = Field(
        default=None,
        description=(
            "Apply different settings like architecture, operating system, build type, compiler, "
        ),
    ),
    options_host: list[str] = Field(
        default=None,
        description=(
            "Apply options like fPIC, header_only, shared, with_*, without_*, etc. to the host context only. "
        ),
    ),
    build_missing: bool = Field(
        default=False,
        description="Build all the missing binary dependencies when they are not available in the cache or in the remotes for download.",
    ),
) -> dict:
    # Expand ~ in work_dir and ensure it exists
    base_work_dir = Path(work_dir).expanduser()
    base_work_dir.mkdir(parents=True, exist_ok=True)

    # Path is always relative to work_dir
    actual_path = str(base_work_dir / path)

    # Determine build variant folder from profile name
    # Extract variant name from profile path (e.g., "tools/conan/profiles/ref/CUSTOM_PROFILE" -> "CUSTOM_PROFILE")
    variant_name = "default"
    if host_profile:
        # Get the last component of the profile path as variant name
        profile_parts = Path(host_profile).parts
        if len(profile_parts) > 0:
            variant_name = profile_parts[-1]  # Use the profile filename as variant

    # Create build/<variant>/conan folder for output files
    conan_output_dir = base_work_dir / "build" / variant_name / "conan"
    conan_output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [_get_conan_binary(), "install", actual_path]

    if remote and not search_in_cache:
        cmd.append(f"--remote={remote}")

    if search_in_cache:
        cmd.append("--no-remote")

    if build_profile:
        cmd.append(f"-pr:b={build_profile}")

    if host_profile:
        cmd.append(f"-pr:h={host_profile}")

    if settings_host:
        for sh in settings_host:
            cmd.append(f"-s:h={sh}")
    if options_host:
        for oh in options_host:
            cmd.append(f"-o:h={oh}")

    timeout = 90.0

    if build_missing:
        cmd.append("--build=missing")
        timeout = 300.0

    # Add lockfile generation in build/<variant>/conan folder
    lockfile_path = conan_output_dir / "conan.lock"
    cmd.append(f"--lockfile-out={lockfile_path}")

    cmd.append("--format=json")

    logging.info(f"Installing Conan packages from '{actual_path}' to '{conan_output_dir}'")
    if host_profile:
        logging.info(f"Using host profile: {host_profile}")

    # Run command and save output to conaninfo.json in build/<variant>/conan folder
    conaninfo_path = conan_output_dir / "conaninfo.json"
    raw_output = await run_command(cmd, timeout=timeout, cwd=str(base_work_dir))

    # Write output to conaninfo.json
    with open(conaninfo_path, 'w') as f:
        f.write(raw_output)

    logging.info(f"Conan installation completed. Output saved to {conaninfo_path}")

    result = json.loads(raw_output)

    # Extract summary information instead of returning full graph
    nodes = result.get("graph", {}).get("nodes", {})
    package_count = len(nodes) - 1  # Exclude consumer node
    
    # Count packages by binary status
    cache_count = 0
    download_count = 0
    build_count = 0
    skip_count = 0
    
    for node_id, node_data in nodes.items():
        if node_data.get("recipe") == "Consumer":
            continue
        binary_status = node_data.get("binary")
        if binary_status == "Cache":
            cache_count += 1
        elif binary_status == "Download":
            download_count += 1
        elif binary_status == "Build":
            build_count += 1
        elif binary_status == "Skip":
            skip_count += 1
    
    # Return concise summary instead of full graph
    return {
        "success": True,
        "summary": {
            "total_packages": package_count,
            "from_cache": cache_count,
            "downloaded": download_count,
            "built_from_source": build_count,
            "skipped": skip_count,
        },
        "files_generated": {
            "lockfile": str(lockfile_path),
            "conaninfo": str(conaninfo_path),
            "output_directory": str(conan_output_dir),
        },
        "build_variant": variant_name,
        "note": f"Full dependency graph details saved to {conaninfo_path}"
    }


@mcp.tool(
    description="""Analyze Conan install to categorize packages by source: Cache, Download, Build, or Skip.

    Use to understand which dependencies are cached, which need downloading, or require building.
    Useful for optimizing CI/CD cache strategies and debugging dependency resolution.

    Args:
        path: Path to recipe folder or file (conanfile.txt/py), relative to work_dir.
        work_dir: Working directory (base for all paths). Always required.
        remote: Optional remote name (searches all if not specified)
        search_in_cache: Resolve exclusively in cache, don't use remotes.
        build_profile: Profile for build context.
        host_profile: Profile for host context.
        settings_host: Substitute settings from default host profile
        options_host: Substitute options from default host profile
        build_missing: Build missing binary dependencies from source

    Returns:
        Dictionary containing:
        - "from_cache": List of packages retrieved from local cache
        - "downloaded": List of packages downloaded from remotes
        - "built": List of packages built from source
        - "skipped": List of packages skipped
        - "summary": Summary statistics
    """
)
async def analyze_install_sources(
    path: str = Field(
        description="Path to the folder containing the recipe or to a recipe file conanfile.txt/.py"
    ),
    work_dir: str = Field(
        description="Working directory where the command should be executed. Always required."
    ),
    remote: str = Field(
        default=None, description="Remote name. Omit to search in all remotes."
    ),
    search_in_cache: bool = Field(
        default=False,
        description="Do not use remote, resolve exclusively in the cache.",
    ),
    build_profile: str = Field(
        default=None,
        description="Profile to the build context.",
    ),
    host_profile: str = Field(
        default=None,
        description="Profile to the host context.",
    ),
    settings_host: list[str] = Field(
        default=None,
        description="Apply different settings like architecture, OS, build type, compiler",
    ),
    options_host: list[str] = Field(
        default=None,
        description="Apply options like fPIC, shared, etc.",
    ),
    build_missing: bool = Field(
        default=False,
        description="Build all the missing binary dependencies.",
    ),
) -> dict:
    # Expand ~ in work_dir and ensure it exists
    base_work_dir = Path(work_dir).expanduser()
    base_work_dir.mkdir(parents=True, exist_ok=True)

    # Path is always relative to work_dir
    actual_path = str(base_work_dir / path)

    cmd = [_get_conan_binary(), "install", actual_path]

    if remote and not search_in_cache:
        cmd.append(f"--remote={remote}")

    if search_in_cache:
        cmd.append("--no-remote")

    if build_profile:
        cmd.append(f"-pr:b={build_profile}")

    if host_profile:
        cmd.append(f"-pr:h={host_profile}")

    if settings_host:
        for sh in settings_host:
            cmd.append(f"-s:h={sh}")
    if options_host:
        for oh in options_host:
            cmd.append(f"-o:h={oh}")

    timeout = 90.0

    if build_missing:
        cmd.append("--build=missing")
        timeout = 300.0

    cmd.append("--format=json")

    # Convert Path to string only when passing to run_command
    raw_output = await run_command(cmd, timeout=timeout, cwd=str(base_work_dir))
    result = json.loads(raw_output)

    # Analyze the graph to categorize packages by source
    from_cache = []
    downloaded = []
    built = []
    skipped = []

    nodes = result.get("graph", {}).get("nodes", {})
    for node_id, node_data in nodes.items():
        ref = node_data.get("ref")
        if ref == "Consumer" or not ref:  # Skip consumer node
            continue

        binary_status = node_data.get("binary")
        context = node_data.get("context")

        # Only analyze host context packages
        if context != "host":
            continue

        package_info = {
            "ref": ref,
            "binary_status": binary_status,
        }

        if binary_status == "Cache":
            from_cache.append(package_info)
        elif binary_status == "Download":
            downloaded.append(package_info)
        elif binary_status == "Build":
            built.append(package_info)
        elif binary_status == "Skip":
            skipped.append(package_info)

    return {
        "from_cache": from_cache,
        "downloaded": downloaded,
        "built": built,
        "skipped": skipped,
        "summary": {
            "total_from_cache": len(from_cache),
            "total_downloaded": len(downloaded),
            "total_built": len(built),
            "total_skipped": len(skipped),
        },
    }


@mcp.tool(
    description="""Create a new Conan project with specified dependencies using templates.

    Templates: cmake_lib (default), cmake_exe, meson_lib, meson_exe, header_lib, 
              msbuild_lib, msbuild_exe, bazel_lib, bazel_exe, autotools_lib, autotools_exe

    Note: Review generated code - update includes, source usage, and build system targets.

    Args:
        name: Project name
        work_dir: Working directory where project will be created. Always required.
        template: Template type (default: "cmake_lib")
        version: Project version (default: "0.1")
        requires: List of dependencies (e.g., ['fmt/12.0.0', 'openssl/3.6.0'])
        tool_requires: List of tool dependencies (e.g., ['cmake/4.1.2', 'ninja/1.13.1'])
        force: Overwrite existing files (default: False)

    Returns:
        Dictionary with result message and raw output from conan new command.
    """
)
async def create_conan_project(
    name: str = Field(description="Name of the project"),
    work_dir: str = Field(
        description="Working directory where the command should be executed. The project will be created directly in this directory. Always required."
    ),
    template: str = Field(
        default="cmake_lib",
        description="Template type for the project. If not specified, use cmake_lib for libraries or cmake_exe for executables"
    ),
    version: str = Field(default="0.1", description="Version of the project"),
    requires: list[str] = Field(
        default=None,
        description="List of dependencies with versions",
    ),
    tool_requires: list[str] = Field(
        default=None,
        description="List of tool dependencies with versions. Common examples: ['cmake/4.1.2'], ['ninja/1.13.1'], ['meson/1.9.1']",
    ),
    force: bool = Field(
        default=False, description="Overwrite existing files if they exist"
    ),
) -> dict:
    """Create a new Conan project with specified dependencies."""

    # Expand ~ in work_dir and ensure it exists
    base_work_dir = Path(work_dir).expanduser()
    base_work_dir.mkdir(parents=True, exist_ok=True)

    # Build the conan new command
    cmd = [_get_conan_binary(), "new", template]

    # Add template arguments
    cmd.append(f"--define=name={name}")
    cmd.append(f"--define=version={version}")

    # Add dependencies if provided
    if requires:
        for dep in requires:
            if dep.strip():  # Skip empty strings
                cmd.append(f"--define=requires={dep.strip()}")

    # Add tool dependencies if provided
    if tool_requires:
        for dep in tool_requires:
            if dep.strip():  # Skip empty strings
                cmd.append(f"--define=tool_requires={dep.strip()}")

    # Add force flag if requested
    if force:
        cmd.append("--force")

    logging.info(f"Creating Conan project '{name}' with template '{template}' in '{work_dir}'")
    if requires:
        logging.info(f"Dependencies: {', '.join(requires)}")

    output = await run_command(cmd, cwd=str(base_work_dir))

    logging.info(f"Project '{name}' created successfully")

    deps_note = (
        f" (WARNING: Review and update the generated code to use these dependencies: {', '.join(requires)} - check includes, source code usage, and build system targets)"
        if requires
        else ""
    )
    return {
        "result": f"Project '{name}' created successfully with template '{template}'{deps_note}\n\nOutput:\n{output}"
    }


def _build_graph_command(
    format_type: str,
    base_work_dir: Path,
    path: str | None,
    requires: list[str] | None,
    remote: str | None,
    build_profile: str | None,
    host_profile: str | None,
    settings_host: list[str] | None,
    options_host: list[str] | None,
) -> list[str]:
    """Build a conan graph info command with the specified parameters.
    
    Args:
        format_type: Output format (e.g., 'html', 'json')
        base_work_dir: Base working directory
        path: Optional path to conanfile (relative to base_work_dir)
        requires: Optional list of package references
        remote: Optional remote name
        build_profile: Optional build profile
        host_profile: Optional host profile
        settings_host: Optional list of host settings
        options_host: Optional list of host options
    
    Returns:
        List of command arguments
    """
    cmd = [_get_conan_binary(), "graph", "info", f"--format={format_type}"]
    
    # Add path or requires
    if path:
        # Path is always relative to work_dir
        actual_path = str(base_work_dir / path)
        cmd.append(actual_path)
    elif requires:
        # Add each reference as a --requires flag
        for ref in requires:
            cmd.append(f"--requires={ref}")
    
    if remote:
        cmd.append(f"--remote={remote}")
    
    if build_profile:
        cmd.append(f"-pr:b={build_profile}")
    
    if host_profile:
        cmd.append(f"-pr:h={host_profile}")
    
    if settings_host:
        for sh in settings_host:
            cmd.append(f"-s:h={sh}")
    
    if options_host:
        for oh in options_host:
            cmd.append(f"-o:h={oh}")
    
    return cmd


@mcp.tool(
    description="""Get dependency graph for a Conan project as interactive HTML visualization.

    Generates an interactive HTML dependency graph and returns a clickable link to view it in a browser.
    The HTML file includes all dependencies (direct and transitive), package metadata
    (versions, revisions, settings, options), and relationships.

    Args:
        work_dir: Working directory (base for all paths). Always required.
        path: Path to recipe folder or file (conanfile.txt/py), relative to work_dir. Optional if requires is provided.
        requires: List of package references (e.g., ["zlib/1.2.11", "fmt/10.0.0"]). Optional if path is provided.
        remote: Optional remote name (searches all if not specified)
        build_profile: Profile for build context.
        host_profile: Profile for host context.
        settings_host: Substitute settings from default host profile
        options_host: Substitute options from default host profile

    Returns:
        Dictionary with clickable HTML link and summary of dependencies.
    """
)
async def get_dependency_graph(
    work_dir: str = Field(
        description="Working directory where the command should be executed. Always required."
    ),
    path: str = Field(
        default=None,
        description="Path to the folder containing the recipe or to a recipe file. Optional if requires is provided."
    ),
    requires: list[str] = Field(
        default=None,
        description="List of package references to analyze. Optional if path is provided."
    ),
    remote: str = Field(
        default=None, description="Remote name. Omit to search in all remotes."
    ),
    build_profile: str = Field(
        default=None,
        description="Profile to the build context.",
    ),
    host_profile: str = Field(
        default=None,
        description="Profile to the host context.",
    ),
    settings_host: list[str] = Field(
        default=None,
        description="Apply different settings like architecture, OS, build type, compiler",
    ),
    options_host: list[str] = Field(
        default=None,
        description="Apply options like fPIC, shared, etc.",
    ),
) -> dict:
    """Generate HTML dependency graph for a Conan project."""

    # Validate that at least one of path or requires is provided
    if not path and not requires:
        raise ValueError("Either 'path' or 'requires' must be provided")

    # Expand ~ in work_dir and ensure it exists
    base_work_dir = Path(work_dir).expanduser()
    if not base_work_dir.is_dir():
        raise FileNotFoundError(f"Work directory does not exist: {base_work_dir}")

    # Create graphs directory for output
    graphs_dir = base_work_dir / "build" / "graphs"
    graphs_dir.mkdir(parents=True, exist_ok=True)

    # Build conan graph info command for HTML
    cmd_html = _build_graph_command(
        "html", base_work_dir, path, requires, remote,
        build_profile, host_profile, settings_host, options_host
    )

    # Execute command to get HTML
    logging.info(f"Generating HTML dependency graph in {graphs_dir}")
    raw_html = await run_command(cmd_html, timeout=90.0, cwd=str(base_work_dir))

    # Save HTML to file with timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_filename = f"dependency_graph_{timestamp}.html"
    html_file = graphs_dir / html_filename
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(raw_html)

    logging.info(f"HTML dependency graph saved to {html_file}")

    # Also get JSON for detailed summary
    cmd_json = _build_graph_command(
        "json", base_work_dir, path, requires, remote,
        build_profile, host_profile, settings_host, options_host
    )

    raw_json = await run_command(cmd_json, timeout=90.0, cwd=str(base_work_dir))
    graph_data = json.loads(raw_json)

    # Generate summary from JSON
    nodes = graph_data.get("graph", {}).get("nodes", {})
    host_deps = []
    build_deps = []

    for node_id, node_data in nodes.items():
        ref = node_data.get("ref")
        if ref == "Consumer" or not ref:  # Skip consumer node
            continue

        context = node_data.get("context")
        if context == "host":
            host_deps.append(ref)
        elif context == "build":
            build_deps.append(ref)

    # Return clickable link and summary
    return {
        "html_graph_link": f"file://{html_file}",
        "html_file_path": str(html_file),
        "summary": {
            "total_dependencies": len(host_deps) + len(build_deps),
            "host_dependencies_count": len(host_deps),
            "build_dependencies_count": len(build_deps),
            "host_dependencies": host_deps[:MAX_DISPLAYED_DEPS] if len(host_deps) > MAX_DISPLAYED_DEPS else host_deps,
            "build_dependencies": build_deps[:MAX_DISPLAYED_DEPS] if len(build_deps) > MAX_DISPLAYED_DEPS else build_deps,
            "note": f"Interactive dependency graph saved. Click the link above to open in browser.",
        },
    }


def _extract_licenses_from_graph(graph_data: dict) -> list[dict[str, str | list[str]]]:
    """Extract license information from conan graph info JSON output.

    Args:
        graph_data: Parsed JSON from conan graph info

    Returns:
        List of dictionaries, each containing "ref" (package reference) and "licenses" (list of license strings)
    """
    licenses_list = []

    nodes = graph_data.get("graph", {}).get("nodes", {})

    for node_id, node_data in nodes.items():
        # Only process nodes in the "host" context (skip build context nodes)
        context = node_data.get("context")
        if context != "host":
            continue

        recipe = node_data.get("recipe")
        # Skip the root conanfile node (not a dependency)
        if recipe == "Consumer":
            continue

        # Try multiple ways to get license information
        license_info = node_data.get("license")

        # Handle license as string, list, or None - always convert to list
        if isinstance(license_info, list):
            # Filter out None/empty values and convert to strings
            licenses = [str(l) for l in license_info if l]
        elif license_info:
            # Single license as string
            licenses = [str(license_info)]
        else:
            # No license specified
            licenses = []

        ref = node_data.get("ref")
        licenses_list.append({"ref": ref, "licenses": licenses})

    return licenses_list


@mcp.tool(
    description="""
    Collect license information for Conan package dependencies.

    This tool uses `conan graph info` to extract license information from the dependency
    graph for all packages.

    Only packages in the "host" context are analyzed (build context packages are excluded
    as they are build-time tools and not included in the final product).

    You can either provide a path to a conanfile OR a list of package references to check.
    At least one of these must be provided.
    
    Use this tool when you need to:
    - Search for licenses of the project
    - Extract license information
    - Check license information 

    Examples:
        - get_conan_licenses(work_dir="/home/user/project", path="conanfile.py")
        - get_conan_licenses(work_dir="~/my_project", path="conanfile.txt")
        - get_conan_licenses(work_dir="/tmp", requires=["zlib/1.2.11"])
        - get_conan_licenses(work_dir="/tmp", requires=["zlib/1.2.11", "fmt/10.0.0"])

    Args:
        work_dir: Working directory where the command should be executed.
                  This is the base directory from which all paths are resolved.
                  Always required.
        path: Path to a folder containing a recipe or to a recipe file (conanfile.txt or conanfile.py).
              This path is ALWAYS relative to work_dir. Optional if requires is provided.
        requires: List of package references to check licenses for (e.g., ["zlib/1.2.11", "fmt/10.0.0"]).
                  Each reference will be passed as a --requires flag to conan graph info.
                  Optional if path is provided. At least one of path or requires must be provided.
        remote: Optional remote name to search in (searches all remotes if not specified)
        build_profile: Profile to the build context.
        host_profile: Profile to the host context.

    Returns:
        List of dictionaries, each containing:
        - "ref": Package reference (string)
        - "licenses": List of license strings (always a list, empty if no license specified)
    """
)
async def get_conan_licenses(
    work_dir: str = Field(
        description="Working directory where the command should be executed. This is the base directory from which all paths are resolved. Always required."
    ),
    path: str = Field(
        default=None,
        description="Path to the folder containing the recipe of the project or to a recipe file conanfile.txt/.py. Optional if requires is provided."
    ),
    requires: list[str] = Field(
        default=None,
        description="List of package references to check licenses for (e.g., ['zlib/1.2.11', 'fmt/10.0.0']). Each reference will be passed as a --requires flag. Optional if path is provided."
    ),
    remote: str = Field(
        default=None, description="Remote name. Omit to search in all remotes."
    ),
    build_profile: str = Field(
        default=None,
        description="Profile to the build context.",
    ),
    host_profile: str = Field(
        default=None,
        description="Profile to the host context.",
    ),
) -> list[dict[str, str | list[str]]]:
    """Collect license information for Conan package dependencies."""

    # Validate that at least one of path or requires is provided
    if not path and not requires:
        raise ValueError("Either 'path' or 'requires' must be provided")

    # Expand ~ in work_dir and ensure it exists
    base_work_dir = Path(work_dir).expanduser()
    if not base_work_dir.is_dir():
        raise FileNotFoundError(f"Work directory does not exist: {base_work_dir}")


    # Build conan graph info command
    cmd = [_get_conan_binary(), "graph", "info", "--format=json"]

    # Add path or requires
    if path:
        # Path is always relative to work_dir
        actual_path = str(base_work_dir / path)
        cmd.append(actual_path)
    elif requires:
        # Add each reference as a --requires flag
        for ref in requires:
            cmd.append(f"--requires={ref}")

    if remote:
        cmd.append(f"--remote={remote}")

    if build_profile:
        cmd.append(f"-pr:b={build_profile}")

    if host_profile:
        cmd.append(f"-pr:h={host_profile}")

    # Execute command with longer timeout since graph info can take time
    raw_output = await run_command(cmd, timeout=90.0, cwd=str(base_work_dir))
    graph_data = json.loads(raw_output)

    # Extract licenses from graph
    licenses_list = _extract_licenses_from_graph(graph_data)

    return licenses_list

@mcp.tool(
    description="""
    ⚠️ WARNING: This tool makes an API call to audit.conan.io service. Only use when explicitly requested by the user.

    Requires provider authentication. If you don't have any yet you can get a token by signing up for free at https://audit.conan.io/register

    Audit a Conan project or a specific package for security vulnerabilities using the audit.conan.io service.
    When using path: Scans the conanfile and all its transitive dependencies for vulnerabilities.
    When using reference: Scans only the vulnerabilities of that specific package reference, but NOT its dependencies.

    There is a limit of 100 API calls per day. If the limit is reached, the tool will return an error.
    Use path to scan the complete graph of dependencies. Use reference to audit a specific package.
    Do not use both path and reference at the same time.

    Args:
        work_dir: Working directory where the command should be executed. Always required.
        path: This path is ALWAYS relative to work_dir. For example, if work_dir is "/home/user/project" and path is "conanfile.txt", it will resolve to "/home/user/project/conanfile.txt". When using path, all transitive dependencies will be scanned for vulnerabilities.

        reference: Conan reference to audit. For example, "fmt/12.0.0". Use it in case the user provides a specific reference to audit. Use it instead of path. When using reference, only the vulnerabilities of that specific package reference will be scanned, but NOT its dependencies.
    Returns:
        Dictionary containing the result of the audit scan.
    """
)
async def scan_conan_dependencies(
    work_dir: str = Field(
        description="Working directory where the command should be executed. Always required."
    ),
    path: str = Field(
        default=None,
        description="Path to the folder relative to working directory containing the recipe of the project or to a recipe file conanfile.txt/.py",
    ),
    reference: str = Field(
        default=None, description="Conan reference to audit. For example, 'fmt/12.0.0'."
    ),
) -> dict:
    if path and reference:
        raise RuntimeError("Do not use both path and reference at the same time.")
    if path:
        base_work_dir = Path(work_dir).expanduser()
        actual_path = str(base_work_dir / path)
        cmd = [_get_conan_binary(), "audit", "scan", actual_path, "--format=json"]
        raw_output = await run_command(cmd, cwd=str(base_work_dir))
        return json.loads(raw_output)
    elif reference:
        cmd = [_get_conan_binary(), "audit", "list", reference, "--format=json"]
        raw_output = await run_command(cmd)
        return json.loads(raw_output)

    raise RuntimeError("Either path or reference must be provided.")


@mcp.tool(
    description="""
    Add a Conan package as editable for local development.

    Editable packages allow developers to work on a package locally while other packages
    depend on it, without needing to export or create the package for every change.
    This is extremely useful during active development of libraries.

    When a package is added as editable:
    - The package is built and used directly from the specified local path
    - Changes to source code are immediately reflected in dependent packages
    - No need to constantly export or create packages during development
    - The <package_name>_ROOT variable points to local build folder, not Conan cache

    Examples:
        - add_editable_package(path="/home/user/mnt/repos/prj.rsp/conanfile.py", version="21.1.0", user="ra", channel="__")
        - add_editable_package(path="~/dev/fmt/conanfile.py", version="10.0.0", user="myuser", channel="dev")
        - add_editable_package(path="/path/to/conanfile.py")

    Args:
        path: Absolute path to the conanfile.py file.
              The package name will be read from this conanfile.
              Typically points to a conanfile.py in ~/mnt/repos/<package>/ in Dev Container.
        version: Package version (optional). If not specified, uses the version in the conanfile.
        user: User name (optional). If not specified, uses the user in the conanfile.
        channel: Channel name (optional). If not specified, uses the channel in the conanfile.
        output_folder: Output folder path for build files (optional). If not specified,
                      uses the layout declared in the conanfile.

    Returns:
        Dictionary with success message and the reference that was added as editable.
    """
)
async def add_editable_package(
    path: str = Field(
        description="Path to the conanfile.py file"
    ),
    version: str = Field(
        default=None,
        description="Package version. If not specified, uses the version in the conanfile.",
    ),
    user: str = Field(
        default=None,
        description="User name. If not specified, uses the user in the conanfile.",
    ),
    channel: str = Field(
        default=None,
        description="Channel name. If not specified, uses the channel in the conanfile.",
    ),
    output_folder: str = Field(
        default=None,
        description="Output folder path for build files. If not specified, uses the layout in conanfile.",
    ),
) -> dict:
    """Add a Conan package as editable for local development."""

    # Expand path
    package_path = Path(path).expanduser().resolve()
    if not package_path.exists():
        raise FileNotFoundError(f"Path does not exist: {package_path}")

    # Build command: conan editable add --version <ver> --user <user> --channel <ch> <path>
    cmd = [_get_conan_binary(), "editable", "add"]
    
    if version:
        cmd.extend(["--version", version])
    if user:
        cmd.extend(["--user", user])
    if channel:
        cmd.extend(["--channel", channel])
    if output_folder:
        output_path = Path(output_folder).expanduser().resolve()
        cmd.extend(["--output-folder", str(output_path)])
    
    cmd.append(str(package_path))

    raw_output = await run_command(cmd)

    return {
        "result": f"Successfully added package as editable from path: {package_path}",
        "path": str(package_path),
        "output": raw_output.strip(),
    }


@mcp.tool(
    description="""
    Remove a Conan package from editables.

    Use this tool to stop using the local editable version of a package and revert
    to using the normal package from cache or remotes.

    Examples:
        - remove_editable_package(path="/home/user/mnt/repos/gtest_rabbit/conanfile.py", name="gtest_rabbit", version="21.1.0", user="ra", channel="__")
        - remove_editable_package(path="~/dev/fmt/conanfile.py", name="fmt", version="10.0.0", user="myuser", channel="dev")

    Args:
        path: Absolute or relative path to the conanfile.py file (required)
        name: Package name (required)
        version: Package version (required)
        user: User name (optional)
        channel: Channel name (optional)

    Returns:
        Dictionary with success message and the reference that was removed.
    """
)
async def remove_editable_package(
    path: str = Field(description="Path to the conanfile.py file"),
    name: str = Field(description="Package name"),
    version: str = Field(description="Package version"),
    user: str = Field(default=None, description="User name (optional)"),
    channel: str = Field(default=None, description="Channel name (optional)"),
) -> dict:
    """Remove a Conan package from editables."""

    # Expand path
    package_path = Path(path).expanduser().resolve()
    if not package_path.exists():
        raise FileNotFoundError(f"Path does not exist: {package_path}")

    # Build reference
    ref = f"{name}/{version}"
    if user or channel:
        ref += f"@{user or '_'}/{channel or '_'}"

    # Command format: conan editable remove <path> -r <reference>
    cmd = [_get_conan_binary(), "editable", "remove", str(package_path), "-r", ref]
    raw_output = await run_command(cmd)

    return {
        "result": f"Successfully removed '{ref}' from editables",
        "reference": ref,
        "path": str(package_path),
        "output": raw_output.strip(),
    }


@mcp.tool(
    description="""
    List all Conan packages currently added as editables.

    Use this tool to see which packages are currently in editable mode and their
    local paths. This is useful for:
    - Checking which packages you're actively developing
    - Verifying editable paths are correct
    - Troubleshooting dependency resolution issues
    - Getting an overview of your local development environment

    Returns:
        Dictionary containing:
        - "editables": List of editable packages with their references and paths
        - "count": Total number of editable packages
    """
)
async def list_editable_packages() -> dict:
    """List all Conan packages currently added as editables."""

    cmd = [_get_conan_binary(), "editable", "list", "--format=json"]
    raw_output = await run_command(cmd)
    result = json.loads(raw_output)

    # Parse the editables - the JSON structure is flat with ref as key
    editables = []

    for ref, info in result.items():
        editables.append({
            "reference": ref,
            "path": info.get("path", ""),
            "output_folder": info.get("output_folder", ""),
        })

    return {
        "editables": editables,
        "count": len(editables),
    }


@mcp.tool(
    description="""
    Discover CMake presets available in the directory where conan install was executed.

    This helper tool discovers available CMake presets from CMakeUserPresets.json that is
    generated by conan install in the working directory. Use this to see which presets
    are available for building the project.

    Args:
        work_dir: Working directory where conan install was executed (where CMakeUserPresets.json is located)

    Returns:
        Dictionary with available presets for user to choose from
    """
)
async def discover_cmake_presets(
    work_dir: str = Field(description="Working directory where conan install was executed"),
) -> dict:
    """Discover CMake presets in the conan install directory."""

    install_dir = Path(work_dir).expanduser().resolve()
    
    # Look for CMakeUserPresets.json in the directory where conan install was executed
    user_presets_file = install_dir / "CMakeUserPresets.json"
    
    if not user_presets_file.exists():
        return {
            "status": "no_presets",
            "message": f"No CMakeUserPresets.json found in {install_dir}. Make sure to run 'conan install' first.",
            "presets": []
        }

    try:
        with open(user_presets_file, 'r') as f:
            presets_data = json.load(f)

        configure_presets = presets_data.get("configurePresets", [])
        build_presets = presets_data.get("buildPresets", [])

        return {
            "status": "found",
            "install_dir": str(install_dir),
            "file_used": "CMakeUserPresets.json",
            "configure_presets": [p.get("name") for p in configure_presets if isinstance(p, dict)],
            "build_presets": [p.get("name") for p in build_presets if isinstance(p, dict)],
            "preset_count": len(configure_presets)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "presets": []
        }


@mcp.tool(
    description="""
    Analyze Conan install errors from log files or command output.

    This tool reads and analyzes Conan install log files or error output to:
    - Identify common error patterns (missing packages, version conflicts, etc.)
    - Provide specific, actionable solutions for each error
    - Extract and summarize all error and warning messages
    - Help developers quickly understand what went wrong

    This is extremely useful when:
    - Conan install fails and you need to understand why
    - Debugging dependency resolution issues
    - Getting quick solutions without reading lengthy logs
    - Learning how to fix common Conan problems

    The tool recognizes these error types:
    - Missing binary packages
    - Version conflicts
    - Recipe not found
    - Settings incompatibility
    - Invalid options
    - Network/remote errors
    - Build errors
    - Profile errors
    - Revision errors

    Examples:
        - analyze_conan_install_error(log_file="/home/user/conan_install.log")
        - analyze_conan_install_error(work_dir="/home/user/project", log_file="conan.log")
        - analyze_conan_install_error(error_text="ERROR: Missing binary: zlib/1.2.11")

    Args:
        log_file: Path to the Conan log file (optional). Can be absolute or relative to work_dir.
                 Common locations:
                 - Terminal output redirected to file: conan install . > conan.log 2>&1
                 - Build folder logs
                 - CI/CD artifact logs
        work_dir: Working directory for resolving relative log_file paths (optional).
                 If log_file is relative, it will be resolved from this directory.
        error_text: Direct error text/output to analyze (optional).
                   Use this if you have the error message but not a log file.

    Note: Provide either log_file OR error_text, not both.

    Returns:
        Dictionary containing:
        - "errors_detected": Boolean indicating if errors were found
        - "error_count": Number of distinct error types detected
        - "errors": List of errors with type, matched text, and solutions
        - "error_lines": First 20 ERROR/WARN lines from the log
        - "summary": Human-readable summary and recommendations
    """
)
async def analyze_conan_install_error(
    log_file: str = Field(
        default=None,
        description="Path to Conan log file. Can be absolute or relative to work_dir.",
    ),
    work_dir: str = Field(
        default=None,
        description="Working directory for resolving relative log file paths.",
    ),
    error_text: str = Field(
        default=None,
        description="Direct error text to analyze instead of reading from a file.",
    ),
) -> dict:
    """Analyze Conan install errors and provide solutions."""

    # Validate input
    if not log_file and not error_text:
        raise ValueError("Either 'log_file' or 'error_text' must be provided")

    if log_file and error_text:
        raise ValueError("Provide either 'log_file' OR 'error_text', not both")

    log_content = ""

    # Read log file if provided
    if log_file:
        log_path = Path(log_file)

        # If work_dir provided and log_file is relative, resolve from work_dir
        if work_dir and not log_path.is_absolute():
            base_work_dir = Path(work_dir).expanduser()
            log_path = base_work_dir / log_file
        else:
            log_path = log_path.expanduser()

        # Check if file exists
        if not log_path.is_file():
            raise FileNotFoundError(f"Log file not found: {log_path}")

        # Read the log file
        try:
            with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                log_content = f.read()
        except Exception as e:
            raise RuntimeError(f"Error reading log file: {str(e)}")
    else:
        # Use provided error text
        log_content = error_text

    # Analyze the log content
    analysis = _analyze_conan_error(log_content)

    # Generate summary
    summary_parts = []

    if not analysis["errors_detected"]:
        summary_parts.append("No recognized Conan errors found in the log.")
        summary_parts.append("The command may have succeeded, or the error pattern is not recognized.")
        summary_parts.append("Check the error_lines section for any warnings or messages.")
    else:
        summary_parts.append(f"Found {analysis['error_count']} error type(s) in the log:")
        summary_parts.append("")

        for idx, error in enumerate(analysis["errors"], 1):
            summary_parts.append(f"{idx}. {error['type'].replace('_', ' ').title()}")
            summary_parts.append(f"   Issue: {error['matched_text']}")
            summary_parts.append("")

        summary_parts.append("See the 'errors' section for detailed solutions for each issue.")

    analysis["summary"] = "\n".join(summary_parts)

    # Add file info if applicable
    if log_file:
        analysis["log_file_analyzed"] = str(log_path) if log_file else None

    return analysis


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
        raise ValueError(f"Invalid HOST_PORT env variable: '{port_str}' - must be a valid integer")

    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)
    logging.info("Starting Conan MCP Server")
    
    # Get transport configuration
    transport, host, port = get_mcp_init_vars()
    
    # Start the MCP server with configured transport
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
