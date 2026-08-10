import json
import logging
import os
import hashlib
from typing import Dict, Optional
from urllib.parse import quote
from pathlib import Path

import requests
from fastmcp import FastMCP

# Basic setup
mcp = FastMCP("JfrogArtifactoryMCPServer")

# Config - set these in your environment
ARTIFACTORY_URL = os.getenv("ARTIFACTORY_BASE_URL")
ACCESS_TOKEN = os.getenv("ARTIFACTORY_PAT_TOKEN")

# Validate environment variables
if not ARTIFACTORY_URL:
    raise ValueError("ARTIFACTORY_BASE_URL environment variable is required")
if not ACCESS_TOKEN:
    raise ValueError("ARTIFACTORY_PAT_TOKEN environment variable is required")


def _get_auth_headers() -> Dict[str, str]:
    """Build auth headers for requests.

    Returns:
        Dictionary containing authorization headers.
    """
    return {"Authorization": f"Bearer {ACCESS_TOKEN}"}


def _make_request(method: str, url: str, **kwargs) -> requests.Response:
    """Make authenticated requests to Artifactory.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE, etc.).
        url: Request URL.
        **kwargs: Additional arguments passed to requests.request().

    Returns:
        Response object from the request.
    """
    headers = _get_auth_headers()
    if "headers" in kwargs:
        headers.update(kwargs["headers"])
    kwargs["headers"] = headers

    kwargs.setdefault("timeout", 30)

    try:
        resp = requests.request(method, url, **kwargs)
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        logging.error(f"Request to {url} failed: {e}")
        raise


@mcp.tool()
def aql_search(aql_query: str) -> str:
    """Search packages using Artifactory Query Language (AQL).

    PRIMARY TOOL for searching packages by name, metadata, or complex criteria.

    AQL (Artifactory Query Language) is the most powerful and efficient way to find packages.

    WHEN TO USE AQL SEARCH:
    - Package name searches - Finding packages when you know part of the name
    - Date-based searches - Recent uploads, packages from specific timeframes
    - Metadata filtering - Packages with specific properties or tags
    - Performance critical - Faster than pattern searches on large repos

    PACKAGE SEARCH WORKFLOW EXAMPLE:

    1. Search by path (broader search):
       items.find({"path":{"$match":"*ems_base_service*"}})
       → Returns: Multiple versions across repositories
       → Found in: ra6-conan-develop-local, ra6-conan-temp-local, etc.
       → Versions: 1.1.3, 1.1.8, 1.2.3, 1.3.1

    2. Filter by specific repository or version:
       items.find({"repo":"ra6-conan-release-local","path":{"$match":"*ems_base_service*"}})
       items.find({"path":{"$match":"*ems_base_service/1.3.1*"}})

    PACKAGE FINDING EXAMPLES:

    Find packages by name:
    items.find({"name":"*mypackage*"})
    items.find({"path":{"$match":"*boost*"},"name":"conanfile.py"})
    items.find({"repo":"docker-local","path":{"$match":"*myapp*"},"name":"manifest.json"})

    Filter by repository:
    items.find({"repo":"conan-local","path":{"$match":"*mylib*"}})

    Recent packages:
    items.find({"name":"*mylib*","created":{"$gt":"2024-01-01"}})
    items.find({"repo":"conan-local","name":"conanfile.py","modified":{"$last":"1week"}})

    Specific versions:
    items.find({"path":{"$match":"*myapp/v1.2*"},"name":"manifest.json"})

    Args:
        aql_query: AQL query string using items.find() syntax.

    Returns:
        Dictionary containing search results with paths, checksums, and metadata.
    """
    logging.debug(f"Executing AQL search: {aql_query}")

    if not aql_query.strip():
        logging.error("AQL query cannot be empty")
        return json.dumps({"error": "AQL query cannot be empty"})

    aql_query = aql_query.strip()
    if not aql_query.startswith("items.find("):
        aql_query = f"items.find({aql_query})"

    url = f"{ARTIFACTORY_URL}/api/search/aql"
    headers = {"Content-Type": "text/plain"}

    try:
        resp = _make_request("POST", url, data=aql_query, headers=headers)
        return json.dumps(resp.json())
    except Exception as e:
        logging.error(f"AQL search failed: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def pattern_search(pattern: str, repos: Optional[str] = None) -> str:
    """Search by exact path patterns - use when you know the EXACT repository structure.

    WHEN TO USE PATTERN SEARCH (instead of AQL):
    - Browsing repository structure - When you want to explore folder hierarchies
    - Exact path matching - When you know the precise path format
    - Directory listing - Getting all files in a specific location
    - Path-based exploration - Understanding how packages are organized

    USE AQL SEARCH INSTEAD when:
    - You're searching by package NAME (use AQL with name/path matching)
    - You want to filter by metadata or dates
    - You're doing performance-critical searches
    - You need complex search criteria

    PATTERN SEARCH EXAMPLES:

    Repository structure exploration:
    docker-local/*/*/manifest.json    → Browse all Docker images
    conan-local/*/*/conanfile.py      → Browse all Conan packages

    Exact path targeting:
    docker-local/myapp/*/manifest.json → All versions of specific image

    Args:
        pattern: Path pattern with * and ** wildcards.
        repos: Limit to specific repos like "docker-local,conan-local".

    Returns:
        Dictionary containing matching artifacts with full repository paths.
    """
    logging.debug(f"Executing pattern_search: {pattern}, repos: {repos}")

    if not pattern.strip():
        logging.error("Pattern cannot be empty")
        return json.dumps({"error": "Pattern cannot be empty"})

    url = f"{ARTIFACTORY_URL}/api/search/pattern"
    pattern = pattern.strip()

    # Convert "repo/path" to "repo:path" format if needed
    if ":" not in pattern and "/" in pattern:
        parts = pattern.split("/", 1)
        if len(parts) == 2:
            pattern = f"{parts[0]}:{parts[1]}"

    params = {"pattern": pattern}
    if repos:
        params["repos"] = repos.strip()

    try:
        resp = _make_request("GET", url, params=params)
        return json.dumps(resp.json())
    except Exception as e:
        logging.error(f"Pattern search failed: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def artifact_search(name: str, repos: Optional[str] = None) -> str:
    """Search for artifacts by exact file names.

    WHEN TO USE ARTIFACT SEARCH:
    - Specific file types - Finding all files of a certain type
    - Exact file names - When you know the precise filename
    - File inventory - Getting all instances of specific files

    FOR PACKAGE NAME SEARCHES, USE AQL SEARCH INSTEAD:
    - PREFERRED: aql_search('items.find({"path":{"$match":"*packagename*"}})')
    - AVOID: artifact_search("*packagename*")

    BEST FOR:

    Find specific file types:
    name="manifest.json"     → All Docker manifests
    name="conanfile.py"      → All Conan package files
    name="config.json"       → Configuration files
    name="Dockerfile"        → Docker build files

    Args:
        name: File name or pattern. Use * for wildcards.
        repos: Specific repos to search (e.g. "docker-local,conan-local").
               Leave empty to search all accessible repos.

    Returns:
        Dictionary containing list of matching artifacts with download URLs
        and repo locations.
    """
    logging.debug(f"Searching artifacts by name: {name}, repos: {repos}")

    if not name.strip():
        logging.error("Artifact name cannot be empty")
        return json.dumps({"error": "Artifact name cannot be empty"})

    url = f"{ARTIFACTORY_URL}/api/search/artifact"
    params = {"name": name.strip()}
    if repos:
        params["repos"] = repos.strip()

    try:
        resp = _make_request("GET", url, params=params)
        return json.dumps(resp.json())
    except Exception as e:
        logging.error(f"Artifact search failed: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_repositories() -> str:
    """List all repositories to see what's available.

    PACKAGE FINDING WORKFLOW: Always start here to understand your repository landscape.

    Typical repositories you'll see:
    - docker-local, docker-remote → Docker images and containers
    - conan-local, conan-remote → Conan C++ packages
    - generic-local → Custom/misc packages

    USE THIS FIRST when looking for a package to understand:
    1. Which repo types are available
    2. Naming conventions (local vs remote vs virtual)
    3. Where your package type would likely be stored

    Then use aql_search like: items.find({"repo":"reponame","name":"*yourpackage*"})

    Returns:
        Dictionary with repository list and summary.
    """
    logging.debug("Fetching repository list")

    url = f"{ARTIFACTORY_URL}/api/repositories"

    try:
        resp = _make_request("GET", url)
        repos = resp.json()

        # Add useful summary
        repo_types = {}
        for repo in repos:
            repo_type = repo.get("type", "unknown")
            repo_types[repo_type] = repo_types.get(repo_type, 0) + 1

        return json.dumps({"repositories": repos, "total_count": len(repos), "types_summary": repo_types})
    except Exception as e:
        logging.error(f"Failed to get repositories: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_repository_info(repo_key: str) -> str:
    """Get details about a specific repository, including its type and layout.

    This is especially useful for understanding how packages are organized in Docker or Conan repositories.

    Examples:

    - **Docker repository**:
        Use this to confirm the repository is set up for Docker images and to see the layout used for image storage.
        Example:
            get_repository_info("docker-local")
        Typical output fields:
            packageType: "Docker"
            repoLayoutRef: "simple-default"
            description: "Local Docker registry"

    - **Conan repository**:
        Use this to check if the repository supports Conan C++ packages and to understand the user/channel structure.
        Example:
            get_repository_info("conan-local")
        Typical output fields:
            packageType: "Conan"
            repoLayoutRef: "conan-default"
            description: "Local Conan repository"

    This information helps you determine:
    - Which repository to use for uploading or searching for Docker/Conan packages
    - How to construct paths for browsing or uploading artifacts
    - What naming conventions and layouts are enforced

    Args:
        repo_key: Repository name like "docker-local" or "conan-local".

    Returns:
        Dictionary containing repository configuration and settings.
    """
    logging.debug(f"Getting repository info for: {repo_key}")

    if not repo_key.strip():
        logging.error("Repository key cannot be empty")
        return json.dumps({"error": "Repository key cannot be empty"})

    repo_key = repo_key.strip()
    url = f"{ARTIFACTORY_URL}/api/repositories/{repo_key}"

    try:
        resp = _make_request("GET", url)
        return json.dumps(resp.json())
    except Exception as e:
        logging.error(f"Failed to get repository info: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_folder_info(repo_key: str, folder_path: str = "") -> str:
    """Browse repository folders to explore package structure.

    Args:
        repo_key: Repository name.
        folder_path: Path within repo (start empty, then drill down).
                    Examples: "myapp", "boost/1.70.0".

    Returns:
        Dictionary containing folder contents with subdirectories and files.
    """
    logging.debug(f"Getting folder info for: {repo_key}/{folder_path}")

    if not repo_key.strip():
        logging.error("Repository key cannot be empty")
        return json.dumps({"error": "Repository key cannot be empty"})

    repo_key = repo_key.strip()
    folder_path = folder_path.strip()

    path = f"{repo_key}/{folder_path}" if folder_path else repo_key
    url = f"{ARTIFACTORY_URL}/api/storage/{path}"

    try:
        resp = _make_request("GET", url)
        return json.dumps(resp.json())
    except Exception as e:
        logging.error(f"Failed to get folder info: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_file_info(repo_key: str, file_path: str) -> str:
    """Get metadata for a specific file in a package.

    Shows file size, checksums, upload date, and any custom properties.
    Good for verifying package integrity or checking when something
    was last updated.

    Args:
        repo_key: Repository name.
        file_path: Full path to file.
                  Examples: "myapp/latest/manifest.json"
                           "boost/1.70.0/_/_/conanfile.py".

    Returns:
        Dictionary containing file metadata including checksums and timestamps.
    """
    logging.debug(f"Getting file info for: {repo_key}/{file_path}")

    if not repo_key.strip() or not file_path.strip():
        logging.error("Repository key and file path are required")
        return json.dumps({"error": "Repository key and file path are required"})

    repo_key = repo_key.strip()
    file_path = file_path.strip()

    url = f"{ARTIFACTORY_URL}/api/storage/{repo_key}/{file_path}"

    try:
        resp = _make_request("GET", url)
        return json.dumps(resp.json())
    except Exception as e:
        logging.error(f"Failed to get file info: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def download_file(repo_key: str, file_path: str, local_path: str) -> str:
    """Download a file from Artifactory and save it to a user-specified local path.

    Args:
        repo_key: Repository name.
        file_path: Path to file in the package.
        local_path: Path where file will be saved. Container path when running in Docker, file system path when running directly.

    Returns:
        Dictionary with download URL, file size, content type, and local file path.
    """
    logging.debug(f"Downloading file: {repo_key}/{file_path} to {local_path}")

    if not all([repo_key.strip(), file_path.strip(), local_path.strip()]):
        logging.error("All parameters are required")
        return json.dumps({"error": "All parameters are required"})

    repo_key = repo_key.strip()
    file_path = file_path.strip()
    local_path = local_path.strip()

    download_url = f"{ARTIFACTORY_URL}/{repo_key}/{file_path}"

    try:
        # Get file info
        resp = _make_request("HEAD", download_url)
        file_size = resp.headers.get("Content-Length", "unknown")
        content_type = resp.headers.get("Content-Type", "unknown")

        # Download to file
        resp = _make_request("GET", download_url, stream=True)
        Path(local_path).parent.mkdir(parents=True, exist_ok=True)

        with open(local_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return json.dumps(
            {
                "source_url": download_url,
                "size": file_size,
                "content_type": content_type,
                "downloaded_to": local_path,
                "status": "success",
            }
        )
    except Exception as e:
        logging.error(f"Failed to download file: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def get_retention_policy(repo_key: str) -> str:
    """Get retention policy information for a repository.

    Simple check for repository-level retention settings that are commonly configured.

    Args:
        repo_key: Repository name to check.

    Returns:
        Dictionary with basic retention info from repository configuration.
    """
    logging.debug(f"Getting retention policy for: {repo_key}")

    if not repo_key.strip():
        logging.error("Repository key cannot be empty")
        return json.dumps({"error": "Repository key cannot be empty"})
    try:
        repo_config = json.loads(get_repository_info(repo_key.strip()))

        # Check if there was an error in getting repo info
        if "error" in repo_config:
            return json.dumps(repo_config)

        # Extract the retention fields from repo config
        retention_info = {}
        retention_fields = ["maxUniqueTags", "maxUniqueSnapshots", "retentionPeriodDays"]

        for field in retention_fields:
            if field in repo_config:
                retention_info[field] = repo_config[field]

        return json.dumps(
            {
                "repository": repo_key,
                "package_type": repo_config.get("packageType", "Generic"),
                "repository_class": repo_config.get("rclass", "unknown"),
                "retention_settings": retention_info if retention_info else "No explicit retention settings",
                "description": repo_config.get("description", ""),
            }
        )
    except Exception as e:
        logging.error(f"Failed to get retention policy: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def upload_file(repo_key: str, target_path: str, local_file: str, properties: Optional[Dict[str, str]] = None) -> str:
    """
    Upload files to repositories.

    Mainly used for uploading Conan packages or Docker layers.
    The properties parameter lets you set custom metadata.
    
    Automatically includes retention policy information so you know
    how long your uploaded files will be kept.

    SECURITY NOTE: This function calculates MD5 and SHA-1 checksums as required
    by Artifactory's API for integrity verification only. These are NOT used for
    security purposes. SHA-256 is also calculated for better integrity verification.
    
    Args:
        repo_key: Target repository.
        target_path: Where to put the file in the repo.
        local_file: File path to upload. Container path when running in Docker, file system path when running directly.
        properties: Custom properties to attach to the file.

    Returns:
        Dictionary containing upload status, result info, and retention policy.
    """
    logging.debug(f"Uploading file: {local_file} to {repo_key}/{target_path}")

    if not all([repo_key.strip(), target_path.strip(), local_file.strip()]):
        logging.error("All parameters are required")
        return json.dumps({"error": "All parameters are required"})

    repo_key = repo_key.strip()
    target_path = target_path.strip()
    local_file = local_file.strip()

    if not Path(local_file).exists():
        logging.error(f"Local file not found: {local_file}")
        return json.dumps({"error": f"Local file not found: {local_file}"})

    # Calculate checksums for integrity verification
    sha1_hash = hashlib.sha1()
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    try:
        with open(local_file, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha1_hash.update(chunk)
                md5_hash.update(chunk)
                sha256_hash.update(chunk)
    except Exception as e:
        logging.error(f"Failed to calculate checksums: {e}")
        return json.dumps({"error": f"Failed to calculate checksums: {e}"})

    sha1_checksum = sha1_hash.hexdigest()
    md5_checksum = md5_hash.hexdigest()
    sha256_checksum = sha256_hash.hexdigest()

    upload_url = f"{ARTIFACTORY_URL}/{repo_key}/{target_path}"

    # Add properties as URL params if provided
    if properties:
        params = "&".join([f"{k}={quote(str(v))}" for k, v in properties.items()])
        upload_url += f"?{params}"

    headers = _get_auth_headers()
    # Add checksum headers (MD5/SHA-1 required by Artifactory API)
    headers.update(
        {"X-Checksum-Sha1": sha1_checksum, "X-Checksum-Md5": md5_checksum, "X-Checksum-Sha256": sha256_checksum}
    )

    try:
        with open(local_file, "rb") as f:
            resp = requests.put(upload_url, data=f, headers=headers, timeout=300)
            resp.raise_for_status()

        result = {
            "uploaded_to": f"{repo_key}/{target_path}",
            "source_file": local_file,
            "status": "success",
            "size_bytes": Path(local_file).stat().st_size,
            "checksums": {
                "sha256": sha256_checksum,  # Primary checksum for verification
                "sha1": sha1_checksum,  # Required by Artifactory API
                "md5": md5_checksum,  # Required by Artifactory API
            },
            "security_note": "MD5/SHA-1 used for API compatibility only. SHA-256 recommended for verification.",
        }

        if resp.content:
            try:
                result["response"] = resp.json()
            except json.JSONDecodeError:
                result["response"] = resp.text

        # Add retention policy information
        try:
            retention_info_str = get_retention_policy(repo_key)
            retention_info = json.loads(retention_info_str)
            if "error" not in retention_info:
                result["retention_policy"] = retention_info

                # Add a simple summary for quick reference
                retention_settings = retention_info.get("retention_settings")
                if retention_settings != "No explicit retention settings":
                    result["retention_summary"] = f"Repository has retention policies: {retention_settings}"
                else:
                    result["retention_summary"] = "No explicit retention policies - files may be kept indefinitely"
            else:
                result["retention_warning"] = f"Could not check retention policy: {retention_info['error']}"

        except Exception as e:
            result["retention_warning"] = f"Could not check retention policy: {str(e)}"

        return json.dumps(result)
    except Exception as e:
        logging.error(f"Failed to upload file: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def delete_item(repo_key: str, item_path: str) -> str:
    """Delete files or entire package directories.

    Be careful with this - it's permanent. Good for cleaning up
    old package versions or test uploads.

    Args:
        repo_key: Repository name.
        item_path: Path to file or directory to delete.

    Returns:
        Dictionary containing deletion confirmation.
    """
    logging.debug(f"Deleting item: {repo_key}/{item_path}")

    if not all([repo_key.strip(), item_path.strip()]):
        logging.error("Repository key and item path are required")
        return json.dumps({"error": "Repository key and item path are required"})

    repo_key = repo_key.strip()
    item_path = item_path.strip()

    delete_url = f"{ARTIFACTORY_URL}/{repo_key}/{item_path}"

    try:
        _make_request("DELETE", delete_url)
        return json.dumps({"deleted": f"{repo_key}/{item_path}", "status": "success"})
    except Exception as e:
        logging.error(f"Failed to delete item: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def copy_item(source_repo: str, source_path: str, target_repo: str, target_path: str) -> str:
    """Copy packages between repositories.

    Useful for promoting packages from staging to production repos
    or backing up important packages.

    Args:
        source_repo: Source repository.
        source_path: Source package path.
        target_repo: Destination repository.
        target_path: Destination path.

    Returns:
        Dictionary containing copy operation result.
    """
    logging.debug(f"Copying item: {source_repo}/{source_path} to {target_repo}/{target_path}")

    params = [source_repo, source_path, target_repo, target_path]
    if not all(p.strip() for p in params):
        logging.error("All parameters are required")
        return json.dumps({"error": "All parameters are required"})

    source_repo, source_path, target_repo, target_path = [p.strip() for p in params]

    url = f"{ARTIFACTORY_URL}/api/copy/{source_repo}/{source_path}"
    params = {"to": f"/{target_repo}/{target_path}"}

    try:
        _make_request("POST", url, params=params)
        return json.dumps(
            {
                "copied_from": f"{source_repo}/{source_path}",
                "copied_to": f"{target_repo}/{target_path}",
                "status": "success",
            }
        )
    except Exception as e:
        logging.error(f"Failed to copy item: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


@mcp.tool()
def move_item(source_repo: str, source_path: str, target_repo: str, target_path: str) -> str:
    """Move packages between repositories.

    Like copy but removes the original. Use when reorganizing packages
    or moving them between different repo types.

    Args:
        source_repo: Source repository.
        source_path: Source package path.
        target_repo: Destination repository.
        target_path: Destination path.

    Returns:
        Dictionary containing move operation result.
    """
    logging.debug(f"Moving item: {source_repo}/{source_path} to {target_repo}/{target_path}")

    params = [source_repo, source_path, target_repo, target_path]
    if not all(p.strip() for p in params):
        logging.error("All parameters are required")
        return json.dumps({"error": "All parameters are required"})

    source_repo, source_path, target_repo, target_path = [p.strip() for p in params]

    url = f"{ARTIFACTORY_URL}/api/move/{source_repo}/{source_path}"
    params = {"to": f"/{target_repo}/{target_path}"}

    try:
        _make_request("POST", url, params=params)
        return json.dumps(
            {
                "moved_from": f"{source_repo}/{source_path}",
                "moved_to": f"{target_repo}/{target_path}",
                "status": "success",
            }
        )
    except Exception as e:
        logging.error(f"Failed to move item: {e}")
        return json.dumps({"error": "An internal error occurred. Please check the server logs."})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    mcp.run()
