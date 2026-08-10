#!/usr/bin/env python3
"""
RTC CCM MCP Server

This MCP server provides comprehensive tools for interacting with IBM RTC CCM
(Rational Team Concert) using the rtcclient Python library.

Features:
- Project Area and Team Area management
- Work item CRUD operations
- Template-based work item creation
- Parent/child relationship management
- Comments and subscribers management
- Saved query execution
- Advanced filtering and querying

Documentation: https://rtcclient.readthedocs.io/en/latest/

Environment Variables Required:
================================
- RTC_SERVER_URL (or ELM_SERVER_BASE_URL): Base URL of the RTC/CCM server
- RTC_USERNAME (or ELM_USERNAME): Username for authentication
- RTC_PASSWORD (or ELM_PASSWORD): Password for authentication
- ELM_CCM_APPSTRING: (Optional) CCM app string, defaults to 'ccm'
- RTC_VERIFY_SSL: (Optional) Set to 'false' to disable SSL verification
- TRANSPORT: (Optional) Transport type, defaults to 'stdio'
- HOST: (Optional) Host for non-stdio transport
- HOST_PORT: (Optional) Port for non-stdio transport
- SSE_PING_INTERVAL: (Optional) SSE ping interval in seconds, defaults to 600
"""

import os
import sys
import json
import logging
import base64
import xml.etree.ElementTree as ET
from typing import Dict, List, Any, Optional

from fastmcp import FastMCP
from sse_starlette.sse import EventSourceResponse

# Log environment status
rtc_url = os.getenv("RTC_SERVER_URL") or os.getenv("ELM_SERVER_BASE_URL")
rtc_user = os.getenv("RTC_USERNAME") or os.getenv("ELM_USERNAME")
if rtc_url and rtc_user:
    logging.info(f"Environment variables loaded - Server: {rtc_url}, User: {rtc_user}")
else:
    logging.warning("Environment variables not found - tools will require explicit credentials")

# Configure SSE ping interval
ping_interval = int(os.getenv("SSE_PING_INTERVAL", 600))
EventSourceResponse.DEFAULT_PING_INTERVAL = ping_interval
logging.info(f"SSE Ping configured: {ping_interval} seconds ({ping_interval / 60:.1f} minutes)")

# Initialize the MCP server
mcp = FastMCP("RTC CCM Server")

# Import rtcclient library
try:
    from rtcclient import RTCClient
    from rtcclient.project_area import ProjectArea
    from rtcclient.workitem import Workitem

    logging.info("Using standard rtcclient library")
except ImportError:
    logging.error("ERROR: rtcclient library not found")
    logging.error("Install with: pip install rtcclient")
    sys.exit(1)


# ============= Custom RTC Client Implementation =============


class BoschWorkitem(Workitem):
    """
    Extended Workitem class with enhanced link navigation capabilities
    for Bosch-specific RTC server configurations.
    """

    def __init__(self, url: str, rtc_obj: "BoschRTCClient", raw_data: Optional[Dict] = None):
        super().__init__(url, rtc_obj, raw_data=raw_data)
        self.parent_url: Optional[str] = None
        self.comments_url: Optional[str] = None
        self.project_id: Optional[str] = None

    def getChildren(self, returned_properties: Optional[str] = None) -> List["BoschWorkitem"]:
        """Get child work items using OSLC query"""
        base_url = self.url.split("?")[0] if "?" in self.url else self.url
        query_str = f'rtc_cm:parent="{base_url}"'

        return self.rtc_obj.queryWorkitems(
            query_str=query_str, projectarea_id=self.project_id, returned_properties=returned_properties
        )

    def getParent(self, returned_properties: Optional[str] = None) -> Optional["BoschWorkitem"]:
        """Get parent work item"""
        if not self.parent_url:
            return None
        return self.rtc_obj.getWorkitemByUrl(self.parent_url, returned_properties=returned_properties)

    def getComments(self) -> List[Any]:
        """Get work item comments"""
        if not self.comments_url:
            self.comments_url = f"{self.url}/rtc_cm:comments"
        return self.rtc_obj.getCommentsByUrl(self.comments_url)


class BoschRTCClient(RTCClient):
    """
    Extended RTCClient that uses Basic Authentication and custom OSLC endpoints
    to work with modern ELM servers that have authentication challenges.
    """

    def _get_headers(self) -> Dict[str, str]:
        """Override to use Basic Authentication instead of form-based auth"""
        logging.info(f"Initializing BoschRTCClient with Basic Auth for user: {self.username}")

        auth_str = f"{self.username}:{self.password}"
        auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        return {
            "Content-Type": "application/xml",
            "Accept": "application/xml",
            "Authorization": f"Basic {auth_b64}",
            "OSLC-Core-Version": "2.0",
        }

    def getProjectAreas(self, archived: bool = False, returned_properties: Optional[str] = None) -> List[ProjectArea]:
        """Get project areas using OSLC catalog endpoint"""
        logging.info("Fetching project areas via OSLC catalog")

        url = f"{self.url}/oslc/workitems/catalog"
        resp = self.get(url, headers=self.headers)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.warning(f"Failed to get project areas via OSLC catalog: {resp.status_code}")
            url = f"{self.url}/process/project-areas"
            resp = self.get(url, headers=self.headers)

        if resp.status_code != 200:
            logging.error(f"Failed to get project areas: {resp.status_code}")
            return []

        root = ET.fromstring(resp.content)
        projects = []

        ns_oslc = {"oslc": "http://open-services.net/ns/core#", "dc": "http://purl.org/dc/terms/"}
        for sp in root.findall(".//oslc:ServiceProvider", ns_oslc):
            title_elem = sp.find(".//dc:title", ns_oslc)
            about = sp.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")

            if title_elem is not None:
                identifier = ""
                if about and "/contexts/" in about:
                    parts = about.split("/contexts/")
                    if len(parts) > 1:
                        identifier = parts[1].split("/")[0]
                elif about:
                    identifier = about.split("/")[-1]

                raw_data = {
                    "dc:title": title_elem.text,
                    "dc:identifier": identifier,
                    "@rdf:resource": about,
                    "rtc_cm:archived": "true" if archived else "false",
                }

                try:
                    pa = ProjectArea(about, self, raw_data=raw_data)
                    if not hasattr(pa, "title") or not pa.title:
                        pa.title = title_elem.text
                    if not hasattr(pa, "identifier") or not pa.identifier:
                        pa.identifier = identifier
                    projects.append(pa)
                except Exception as e:
                    logging.warning(f"Failed to create ProjectArea object: {e}")

        logging.info(f"Found {len(projects)} project areas")
        return projects

    def getProjectArea(
        self, projectarea_name: str, archived: bool = False, returned_properties: Optional[str] = None
    ) -> Optional[ProjectArea]:
        """Get a specific project area by name"""
        projects = self.getProjectAreas(archived=archived, returned_properties=returned_properties)
        for proj in projects:
            if getattr(proj, "title", "") == projectarea_name:
                return proj
        return None

    def getWorkitems(
        self,
        projectarea_name: Optional[str] = None,
        projectarea_id: Optional[str] = None,
        returned_properties: Optional[str] = None,
        archived: bool = False,
    ) -> List[BoschWorkitem]:
        """Get work items using OSLC Atom feed endpoint"""
        if projectarea_name:
            pa = self.getProjectArea(projectarea_name, archived=archived)
            if pa:
                projectarea_id = pa.identifier
            else:
                raise Exception(f"Project '{projectarea_name}' not found")

        if not projectarea_id:
            return []

        feed_url = f"{self.url}/oslc/contexts/{projectarea_id}/workitems.xml"

        params = {"oslc.select": returned_properties if returned_properties else "*", "oslc.pageSize": "100"}

        logging.info(f"Fetching work items feed: {feed_url}")
        resp = self.get(feed_url, headers=self.headers, params=params)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.error(f"Failed to get work items feed: {resp.status_code}")
            return []

        return self._parse_workitems_response(resp.content, projectarea_id)

    def getSavedQueries(self, projectarea_name: str) -> List[Any]:
        """Get saved queries for a project area"""
        pa = self.getProjectArea(projectarea_name)
        if not pa:
            raise Exception(f"Project '{projectarea_name}' not found")

        url = f"{self.url}/oslc/queries"
        params = {"oslc.select": "*"}

        logging.info(f"Fetching saved queries from: {url}")
        resp = self.get(url, headers=self.headers, params=params)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.error(f"Failed to get saved queries: {resp.status_code}")
            return []

        root = ET.fromstring(resp.content)
        queries = []

        ns = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dcterms": "http://purl.org/dc/terms/",
            "rtc_cm": "http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/",
        }

        query_elements = (
            root.findall(".//rtc_cm:QueryDescriptor", ns)
            + root.findall(".//rtc_cm:SimpleQueryDescriptor", ns)
            + root.findall(".//rtc_cm:Query", ns)
        )

        for query_elem in query_elements:
            title = query_elem.find(".//dcterms:title", ns)
            identifier = query_elem.find(".//dcterms:identifier", ns)
            about = query_elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")

            if title is not None and about:
                q_obj = type("SavedQuery", (), {})()
                q_obj.title = title.text
                q_obj.url = about
                q_obj.identifier = identifier.text if identifier is not None else ""
                queries.append(q_obj)

        logging.info(f"Found {len(queries)} saved queries")
        return queries

    def runSavedQuery(self, saved_query_url: str, returned_properties: Optional[str] = None) -> List[BoschWorkitem]:
        """Execute a saved query and return results"""
        import re

        if "/resource/itemOid/" in saved_query_url:
            query_id = saved_query_url.split("/")[-1]
        elif "/oslc/queries/" in saved_query_url:
            query_id = saved_query_url.split("/")[-1]
        else:
            match = re.search(r"([a-zA-Z0-9_-]{22,23})", saved_query_url)
            query_id = match.group(1) if match else saved_query_url.split("/")[-1]

        results_url = f"{self.url}/oslc/queries/{query_id}/rtc_cm:results"
        params = {"oslc.select": returned_properties if returned_properties else "*", "oslc.pageSize": "100"}

        logging.info(f"Running saved query: {results_url}")
        resp = self.get(results_url, headers=self.headers, params=params)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.error(f"Failed to run saved query: {resp.status_code}")
            return []

        return self._parse_workitems_response(resp.content)

    def queryWorkitems(
        self,
        query_str: str,
        projectarea_name: Optional[str] = None,
        projectarea_id: Optional[str] = None,
        returned_properties: Optional[str] = None,
    ) -> List[BoschWorkitem]:
        """Query work items using OSLC query syntax"""
        if projectarea_name and not projectarea_id:
            pa = self.getProjectArea(projectarea_name)
            if pa:
                projectarea_id = pa.identifier
            else:
                raise Exception(f"Project '{projectarea_name}' not found")

        query_url = (
            f"{self.url}/oslc/contexts/{projectarea_id}/workitems" if projectarea_id else f"{self.url}/oslc/workitems"
        )

        params = {
            "oslc.where": query_str,
            "oslc.pageSize": "100",
            "oslc.select": returned_properties if returned_properties else "*",
        }

        logging.info(f"Querying work items: {query_url} with where={query_str}")
        resp = self.get(query_url, headers=self.headers, params=params)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.error(f"Failed to query work items: {resp.status_code}")
            return []

        return self._parse_workitems_response(resp.content, projectarea_id)

    def getWorkitemByUrl(self, workitem_url: str, returned_properties: Optional[str] = None) -> Optional[BoschWorkitem]:
        """Fetch a work item by its direct URL"""
        params = {"oslc.select": returned_properties if returned_properties else "*"}

        logging.info(f"Fetching work item by URL: {workitem_url}")
        resp = self.get(workitem_url, headers=self.headers, params=params)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.error(f"Failed to get work item by URL: {resp.status_code}")
            return None

        return self._parse_single_workitem_response(resp.content, workitem_url)

    def getCommentsByUrl(self, comments_url: str) -> List[Any]:
        """Fetch comments from a comments URL"""
        logging.info(f"Fetching comments from: {comments_url}")
        resp = self.get(comments_url, headers=self.headers)
        logging.info(f"Request URL: {resp.url}")

        if resp.status_code != 200:
            logging.error(f"Failed to get comments: {resp.status_code}")
            return []

        root = ET.fromstring(resp.content)
        comments = []

        ns = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rtc_cm": "http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/",
            "dc": "http://purl.org/dc/terms/",
        }

        for comment_elem in root.findall(".//rtc_cm:Comment", ns):
            c_obj = type("Comment", (), {})()
            c_obj.description = self._get_val(comment_elem, ".//dc:description", ns)
            c_obj.created = self._get_val(comment_elem, ".//dc:created", ns)
            c_obj.creator = self._get_res(comment_elem, ".//dc:creator", ns)
            comments.append(c_obj)

        logging.info(f"Found {len(comments)} comments")
        return comments

    def getWorkitem(
        self, workitem_id: str, projectarea_name: Optional[str] = None, returned_properties: Optional[str] = None
    ) -> Optional[BoschWorkitem]:
        """Get a work item by ID using direct OSLC resource URL"""
        resource_url = f"{self.url}/oslc/workitems/{workitem_id}"
        wi = self.getWorkitemByUrl(resource_url, returned_properties)

        if not wi:
            logging.warning(f"Failed to get work item via OSLC: {resource_url}")
            resource_url = f"{self.url}/resource/itemName/com.ibm.team.workitem.WorkItem/{workitem_id}"
            logging.info(f"Trying alternative URL: {resource_url}")
            wi = self.getWorkitemByUrl(resource_url, returned_properties)

        return wi

    def createWorkitem(
        self,
        item_type: str,
        title: str,
        description: Optional[str] = None,
        projectarea_id: Optional[str] = None,
        projectarea_name: Optional[str] = None,
        template: Optional[str] = None,
        copied_from: Optional[str] = None,
        keep: bool = False,
        **kwargs,
    ) -> BoschWorkitem:
        """Create a work item using OSLC without requiring item type metadata"""
        try:
            import xmltodict
        except ImportError:
            logging.error("xmltodict library required for createWorkitem")
            raise

        if not isinstance(projectarea_id, str) or not projectarea_id:
            projectarea = self.getProjectArea(projectarea_name)
            projectarea_id = projectarea.identifier

        itemtype_identifier = item_type.lower()

        wi_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<oslc_cm:ChangeRequest xmlns:oslc_cm="http://open-services.net/ns/cm#"
    xmlns:dc="http://purl.org/dc/terms/"
    xmlns:rtc_cm="http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/">
    <dc:title>{title}</dc:title>"""

        if description:
            wi_xml += f"""
    <dc:description>{description}</dc:description>"""

        for key, value in kwargs.items():
            if key in ["ownedBy", "owner"]:
                wi_xml += f'''
    <rtc_cm:ownedBy rdf:resource="{value}" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>'''
            elif key == "priority":
                wi_xml += f'''
    <oslc_cm:priority rdf:resource="{value}" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>'''
            elif key == "severity":
                wi_xml += f'''
    <oslc_cm:severity rdf:resource="{value}" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>'''

        wi_xml += """
</oslc_cm:ChangeRequest>"""

        logging.info(f"Creating work item of type '{item_type}' with title '{title}'")

        wi_url_post = f"{self.url}/oslc/contexts/{projectarea_id}/workitems/{itemtype_identifier}"
        logging.info(f"POST URL: {wi_url_post}")

        resp = self.post(
            wi_url_post, verify=self.verify, headers=self.headers, proxies=self.proxies, data=wi_xml.encode("utf-8")
        )

        logging.info(f"Create response status: {resp.status_code}")

        if resp.status_code not in [200, 201]:
            logging.error(f"Failed to create work item: {resp.status_code}")
            logging.error(f"Response: {resp.text}")
            raise Exception(f"Failed to create work item: {resp.status_code} - {resp.text[:500]}")

        raw_data = xmltodict.parse(resp.content)
        workitem_raw = raw_data.get("oslc_cm:ChangeRequest", raw_data)
        workitem_id = workitem_raw.get("dc:identifier")

        if not workitem_id:
            logging.error(f"No workitem ID in response: {raw_data}")
            raise Exception("Created work item but no ID returned")

        workitem_url = f"{self.url}/oslc/workitems/{workitem_id}"

        new_wi = BoschWorkitem(workitem_url, self, raw_data=workitem_raw)
        new_wi.identifier = workitem_id
        new_wi.project_id = projectarea_id

        logging.info(f"Successfully created work item #{workitem_id}")
        return new_wi

    def _get_val(self, elem, xpath: str, ns: Dict[str, str]) -> Optional[str]:
        """Extract text value from XML element"""
        e = elem.find(xpath, ns)
        return e.text if e is not None else None

    def _get_res(self, elem, xpath: str, ns: Dict[str, str]) -> Optional[str]:
        """Extract resource URL from XML element"""
        e = elem.find(xpath, ns)
        return e.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource") if e is not None else None

    def _parse_workitems_response(self, content: bytes, project_id: Optional[str] = None) -> List[BoschWorkitem]:
        """Parse XML response containing multiple work items"""
        root = ET.fromstring(content)
        workitems = []

        ns = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rtc_cm": "http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/",
            "oslc_cm": "http://open-services.net/ns/cm#",
            "dc": "http://purl.org/dc/terms/",
        }

        found_elements = root.findall(".//rtc_cm:WorkItem", ns) + root.findall(".//oslc_cm:ChangeRequest", ns)

        for wi_elem in found_elements:
            wi = self._create_workitem_from_element(wi_elem, ns, project_id=project_id)
            if wi:
                workitems.append(wi)

        return workitems

    def _parse_single_workitem_response(self, content: bytes, url: Optional[str] = None) -> Optional[BoschWorkitem]:
        """Parse XML response containing a single work item"""
        root = ET.fromstring(content)

        ns = {
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rtc_cm": "http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/",
            "oslc_cm": "http://open-services.net/ns/cm#",
            "dc": "http://purl.org/dc/terms/",
        }

        if root.tag.endswith("WorkItem") or root.tag.endswith("ChangeRequest"):
            wi_elem = root
        else:
            wi_elem = root.find(".//rtc_cm:WorkItem", ns) or root.find(".//oslc_cm:ChangeRequest", ns)

        return self._create_workitem_from_element(wi_elem, ns, url) if wi_elem is not None else None

    def _create_workitem_from_element(
        self, wi_elem, ns: Dict[str, str], url: Optional[str] = None, project_id: Optional[str] = None
    ) -> Optional[BoschWorkitem]:
        """Create BoschWorkitem instance from XML element"""
        about = wi_elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about") or url

        # Extract fields
        identifier = self._get_val(wi_elem, ".//dc:identifier", ns)
        title = self._get_val(wi_elem, ".//dc:title", ns)
        state = self._get_val(wi_elem, ".//rtc_cm:state", ns) or self._get_val(wi_elem, ".//oslc_cm:status", ns)
        desc = self._get_val(wi_elem, ".//dc:description", ns)
        creator = self._get_val(wi_elem, ".//dc:creator", ns) or self._get_res(wi_elem, ".//dc:creator", ns)
        created = self._get_val(wi_elem, ".//dc:created", ns)
        ownedBy = self._get_res(wi_elem, ".//rtc_cm:ownedBy", ns)
        wi_type = self._get_res(wi_elem, ".//rtc_cm:type", ns) or self._get_res(wi_elem, ".//dc:type", ns)
        priority = self._get_res(wi_elem, ".//oslc_cm:priority", ns)
        severity = self._get_res(wi_elem, ".//oslc_cm:severity", ns)
        filedAgainst = self._get_res(wi_elem, ".//rtc_cm:filedAgainst", ns)
        plannedFor = self._get_res(wi_elem, ".//rtc_cm:plannedFor", ns)
        parent = self._get_res(wi_elem, ".//rtc_cm:parent", ns)
        comments = self._get_res(wi_elem, ".//rtc_cm:comments", ns)

        raw_data = {
            "dc:identifier": identifier,
            "dc:title": title,
            "dc:description": desc,
            "rtc_cm:state": state,
            "dc:creator": creator,
            "dc:created": created,
            "rtc_cm:ownedBy": ownedBy,
            "dc:type": wi_type,
            "oslc_cm:priority": priority,
            "oslc_cm:severity": severity,
            "rtc_cm:filedAgainst": filedAgainst,
            "rtc_cm:plannedFor": plannedFor,
            "@rdf:about": about,
        }

        try:
            wi = BoschWorkitem(about, self, raw_data=raw_data)
            wi.parent_url = parent
            wi.comments_url = comments
            wi.project_id = project_id

            # Set attributes
            wi.identifier = identifier
            wi.title = title
            wi.state = state
            wi.description = desc
            wi.creator = creator
            wi.created = created
            if hasattr(wi, "ownedBy"):
                wi.ownedBy = ownedBy
            if hasattr(wi, "owner"):
                wi.owner = ownedBy
            wi.type = wi_type
            wi.priority = priority
            wi.severity = severity
            wi.filedAgainst = filedAgainst
            wi.plannedFor = plannedFor

            return wi
        except Exception as e:
            logging.error(f"Failed to instantiate BoschWorkitem: {e}")
            return None

    def updateWorkitem(
        self,
        workitem_id: str,
        updates: Dict[str, Any],
        projectarea_id: Optional[str] = None,
        projectarea_name: Optional[str] = None,
    ) -> BoschWorkitem:
        """
        Update a work item using OSLC PUT operation

        Args:
            workitem_id: Work item ID to update
            updates: Dictionary of field names and values to update
            projectarea_id: Optional project area ID
            projectarea_name: Optional project area name

        Returns:
            Updated BoschWorkitem instance
        """

        # Get current work item with all properties
        logging.info(f"Fetching current state of work item #{workitem_id}")
        current_wi = self.getWorkitem(workitem_id, projectarea_name=projectarea_name, returned_properties="*")

        if not current_wi:
            raise Exception(f"Work item #{workitem_id} not found")

        # Get ETag for optimistic locking
        workitem_url = f"{self.url}/oslc/workitems/{workitem_id}"
        resp = self.get(workitem_url, headers=self.headers, params={"oslc.select": "*"})

        if resp.status_code != 200:
            raise Exception(f"Failed to fetch work item for update: {resp.status_code}")

        etag = resp.headers.get("ETag")
        if not etag:
            logging.warning("No ETag found, proceeding without optimistic locking")

        # Build XML for update
        wi_xml = """<?xml version="1.0" encoding="UTF-8"?>
<oslc_cm:ChangeRequest xmlns:oslc_cm="http://open-services.net/ns/cm#"
    xmlns:dc="http://purl.org/dc/terms/"
    xmlns:rtc_cm="http://jazz.net/xmlns/prod/jazz/rtc/cm/1.0/"
    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">"""

        # Add identifier
        wi_xml += f"""
    <dc:identifier>{workitem_id}</dc:identifier>"""

        # Add updates
        for field, value in updates.items():
            if field in ["title", "dc:title"]:
                wi_xml += f"""
    <dc:title>{value}</dc:title>"""
            elif field in ["description", "dc:description"]:
                wi_xml += f"""
    <dc:description>{value}</dc:description>"""
            elif field in ["state", "rtc_cm:state"]:
                wi_xml += f"""
    <rtc_cm:state>{value}</rtc_cm:state>"""
            elif field in ["ownedBy", "rtc_cm:ownedBy", "owner"]:
                wi_xml += f'''
    <rtc_cm:ownedBy rdf:resource="{value}"/>'''
            elif field in ["priority", "oslc_cm:priority"]:
                wi_xml += f'''
    <oslc_cm:priority rdf:resource="{value}"/>'''
            elif field in ["severity", "oslc_cm:severity"]:
                wi_xml += f'''
    <oslc_cm:severity rdf:resource="{value}"/>'''
            elif field in ["filedAgainst", "rtc_cm:filedAgainst"]:
                wi_xml += f'''
    <rtc_cm:filedAgainst rdf:resource="{value}"/>'''
            elif field in ["plannedFor", "rtc_cm:plannedFor"]:
                wi_xml += f'''
    <rtc_cm:plannedFor rdf:resource="{value}"/>'''
            else:
                # Generic field update
                wi_xml += f"""
    <{field}>{value}</{field}>"""

        wi_xml += """
</oslc_cm:ChangeRequest>"""

        logging.info(f"Updating work item #{workitem_id}")
        logging.debug(f"Update XML: {wi_xml}")

        # Prepare headers with ETag if available
        update_headers = self.headers.copy()
        if etag:
            update_headers["If-Match"] = etag

        # Execute PUT request
        resp = self.put(
            workitem_url, verify=self.verify, headers=update_headers, proxies=self.proxies, data=wi_xml.encode("utf-8")
        )

        logging.info(f"Update response status: {resp.status_code}")

        if resp.status_code not in [200, 201, 204]:
            logging.error(f"Failed to update work item: {resp.status_code}")
            logging.error(f"Response: {resp.text}")
            raise Exception(f"Failed to update work item: {resp.status_code} - {resp.text[:500]}")

        # Fetch updated work item
        updated_wi = self.getWorkitem(workitem_id, projectarea_name=projectarea_name, returned_properties="*")

        if not updated_wi:
            logging.warning("Update may have succeeded but couldn't fetch updated work item")
            return current_wi

        logging.info(f"Successfully updated work item #{workitem_id}")
        return updated_wi


# ============= Connection Management =============

_connection_cache: Dict[str, BoschRTCClient] = {}


def get_rtc_client(
    server_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
) -> BoschRTCClient:
    """
    Get or create an RTC client connection with connection pooling

    Args:
        server_url: RTC server URL
        username: RTC username
        password: RTC password

    Returns:
        BoschRTCClient instance

    Raises:
        ValueError: If required connection parameters are missing
    """
    if not server_url:
        server_url = os.getenv("RTC_SERVER_URL", os.getenv("ELM_SERVER_BASE_URL"))
    if not username:
        username = os.getenv("RTC_USERNAME", os.getenv("ELM_USERNAME"))
    if not password:
        password = os.getenv("RTC_PASSWORD", os.getenv("ELM_PASSWORD"))

    if not all([server_url, username, password]):
        raise ValueError("Missing required connection parameters. Set RTC_SERVER_URL, RTC_USERNAME, RTC_PASSWORD")

    ccm_appstring = os.getenv("ELM_CCM_APPSTRING", "ccm")
    if not server_url.endswith(ccm_appstring) and not server_url.endswith("jazz"):
        server_url = f"{server_url.rstrip('/')}/{ccm_appstring}"

    cache_key = f"{server_url}:{username}"

    if cache_key not in _connection_cache:
        logging.info(f"Creating new RTC client connection to {server_url}")

        ends_with_jazz = server_url.rstrip("/").endswith("jazz")

        client = BoschRTCClient(
            url=server_url, username=username, password=password, ends_with_jazz=ends_with_jazz, verify=False
        )

        _connection_cache[cache_key] = client
        logging.info("RTC client connected successfully")

    return _connection_cache[cache_key]


# ============= Helper Functions =============


def _workitem_to_dict(wi: BoschWorkitem) -> Dict[str, Any]:
    """
    Convert a work item object to dictionary

    Args:
        wi: RTC Workitem object

    Returns:
        Dictionary containing work item data
    """

    def get_attr(obj, attr_name: str, default: Any = None) -> Any:
        return getattr(obj, attr_name, default)

    return {
        "id": get_attr(wi, "identifier"),
        "title": get_attr(wi, "title"),
        "state": get_attr(wi, "state"),
        "description": get_attr(wi, "description"),
        "creator": get_attr(wi, "creator"),
        "created": get_attr(wi, "created"),
        "owner": get_attr(wi, "ownedBy") or get_attr(wi, "owner"),
        "type": get_attr(wi, "type"),
        "priority": str(priority) if (priority := get_attr(wi, "priority")) else None,
        "severity": str(severity) if (severity := get_attr(wi, "severity")) else None,
        "filed_against": str(filed_against) if (filed_against := get_attr(wi, "filedAgainst")) else None,
        "planned_for": str(planned_for) if (planned_for := get_attr(wi, "plannedFor")) else None,
        "url": get_attr(wi, "url"),
    }


# ============= MCP Tool Definitions =============


@mcp.tool()
def list_projects(
    server_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
) -> str:
    """
    List all available RTC project areas

    Args:
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of projects
    """
    try:
        client = get_rtc_client(server_url, username, password)
        projects = client.getProjectAreas()

        project_list = [
            {"name": getattr(proj, "title", str(proj)), "url": getattr(proj, "url", "")} for proj in projects
        ]

        return json.dumps(project_list, indent=2)

    except Exception as e:
        logging.error(f"Error listing projects: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_project_by_name(
    project_name: str, server_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
) -> str:
    """
    Get a specific project area by name

    Args:
        project_name: Name of the project area
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing project information
    """
    try:
        client = get_rtc_client(server_url, username, password)
        project = client.getProjectArea(project_name)

        if not project:
            return json.dumps({"error": f"Project '{project_name}' not found"})

        result = {
            "name": getattr(project, "title", project_name),
            "url": getattr(project, "url", ""),
            "identifier": getattr(project, "identifier", ""),
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting project: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


# ============= Work Item Functions =============


@mcp.tool()
def get_workitem_by_id(
    workitem_id: str,
    project_name: Optional[str] = None,
    returned_properties: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Get a specific work item by ID

    Args:
        workitem_id: Work item ID/number
        project_name: Optional project area name
        returned_properties: Optional comma-separated properties to return
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing work item information
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Convert to int if possible
        try:
            wid = int(workitem_id)
        except ValueError:
            wid = workitem_id

        # Get work item
        wi = client.getWorkitem(wid, returned_properties=returned_properties)

        if not wi:
            return json.dumps({"error": f"Work item '{workitem_id}' not found"})

        # Extract work item data
        result = _workitem_to_dict(wi)

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting work item: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_workitems(
    project_name: str,
    returned_properties: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Get all work items in a project area

    Args:
        project_name: Name of the project area
        returned_properties: Optional comma-separated properties to return
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of work items
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # getWorkitems returns a list of Workitem objects
        workitems = client.getWorkitems(projectarea_name=project_name, returned_properties=returned_properties)

        result = [_workitem_to_dict(wi) for wi in workitems]

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting work items: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


# ============= Query Functions =============


@mcp.tool()
def query_workitems(
    query_str: str,
    project_name: str,
    returned_properties: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Query work items using RTC query syntax

    Query Syntax Examples:
        - dcterms:title="My Title" - Exact match
        - dcterms:type="task" and rtc_cm:state!="closed" - Type and state
        - rtc_cm:ownedBy="user@email.com" - Owner filter

    Args:
        query_str: RTC query string (see advanced_usage_web.txt for syntax)
        project_name: Name of the project area
        returned_properties: Optional comma-separated properties to return
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of matching work items
    """
    try:
        client = get_rtc_client(server_url, username, password)

        workitems = client.queryWorkitems(
            query_str=query_str, projectarea_name=project_name, returned_properties=returned_properties
        )

        result = [_workitem_to_dict(wi) for wi in workitems]

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error querying work items: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_saved_queries(
    project_name: str,
    creator: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Get all saved queries in a project area

    Args:
        project_name: Name of the project area
        creator: Optional creator email to filter queries
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of saved queries
    """
    try:
        client = get_rtc_client(server_url, username, password)

        if creator:
            # For now we don't support filtering by creator in the custom implementation
            # unless we filter the results
            queries = client.getSavedQueries(project_name)
            # Filter if needed (not implemented deeply)
        else:
            queries = client.getSavedQueries(project_name)

        result = []
        for query in queries:
            result.append(
                {
                    "name": getattr(query, "title", str(query)),
                    "url": getattr(query, "url", ""),
                    "identifier": getattr(query, "identifier", ""),
                }
            )

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting saved queries: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def run_saved_query(
    saved_query_url: str,
    returned_properties: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Run a saved query by URL

    Args:
        saved_query_url: URL of the saved query
        returned_properties: Optional comma-separated properties to return
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of work items
    """
    try:
        client = get_rtc_client(server_url, username, password)

        workitems = client.runSavedQuery(saved_query_url=saved_query_url, returned_properties=returned_properties)

        result = [_workitem_to_dict(wi) for wi in workitems]

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error running saved query: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


# ============= Advanced Work Item Functions =============


@mcp.tool()
def get_workitem_children(
    workitem_id: str,
    returned_properties: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Get all children of a work item

    Args:
        workitem_id: Work item ID/number
        returned_properties: Optional comma-separated properties to return
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of child work items
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Convert to int if possible
        try:
            wid = int(workitem_id)
        except ValueError:
            wid = workitem_id

        # Get work item
        wi = client.getWorkitem(wid)

        if not wi:
            return json.dumps({"error": f"Work item '{workitem_id}' not found"})

        # Get children
        children = wi.getChildren(returned_properties=returned_properties)

        if not children:
            return json.dumps([])

        # Handle both single workitem and list
        if not isinstance(children, list):
            children = [children]

        result = [_workitem_to_dict(child) for child in children]

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting work item children: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_workitem_parent(
    workitem_id: str,
    returned_properties: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Get the parent of a work item

    Args:
        workitem_id: Work item ID/number
        returned_properties: Optional comma-separated properties to return
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing parent work item
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Convert to int if possible
        try:
            wid = int(workitem_id)
        except ValueError:
            wid = workitem_id

        # Get work item
        wi = client.getWorkitem(wid)

        if not wi:
            return json.dumps({"error": f"Work item '{workitem_id}' not found"})

        # Get parent
        parent = wi.getParent(returned_properties=returned_properties)

        if not parent:
            return json.dumps({"message": "No parent work item found"})

        result = _workitem_to_dict(parent)

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting work item parent: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_workitem_comments(
    workitem_id: str, server_url: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None
) -> str:
    """
    Get all comments for a work item

    Args:
        workitem_id: Work item ID/number
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing list of comments
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Convert to int if possible
        try:
            wid = int(workitem_id)
        except ValueError:
            wid = workitem_id

        # Get work item
        wi = client.getWorkitem(wid)

        if not wi:
            return json.dumps({"error": f"Work item '{workitem_id}' not found"})

        # Get comments
        comments = wi.getComments()

        result = []
        for comment in comments:
            result.append(
                {
                    "created": getattr(comment, "created", ""),
                    "creator": getattr(comment, "creator", ""),
                    "description": getattr(comment, "description", ""),
                }
            )

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error getting work item comments: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


# ============= Work Item Creation Functions =============


@mcp.tool()
def create_workitem(
    project_name: str,
    workitem_type: str,
    title: str,
    description: Optional[str] = None,
    fields_json: Optional[str] = None,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Create a new work item in a project area

    Common work item types:
        - task
        - defect
        - story
        - epic
        - impediment

    Args:
        project_name: Name of the project area
        workitem_type: Type of work item (task, defect, story, etc.)
        title: Work item title
        description: Optional work item description
        fields_json: Optional JSON string with additional fields, e.g.:
                    {"rtc_cm:ownedBy": "user@email.com", "rtc_cm:priority": "High"}
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing success/failure message and created work item data
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Get project area ID
        project = client.getProjectArea(project_name)
        if not project:
            return json.dumps({"success": False, "error": f"Project '{project_name}' not found"})

        # Build kwargs for createWorkitem
        kwargs = {}

        # Add description if provided
        if description:
            kwargs["description"] = description

        # Parse and merge additional fields if provided
        if fields_json:
            try:
                additional_fields = json.loads(fields_json)
                kwargs.update(additional_fields)
            except json.JSONDecodeError as e:
                return json.dumps({"success": False, "error": f"Invalid JSON format in fields_json: {e}"})

        # Create work item using rtcclient
        wi = client.createWorkitem(item_type=workitem_type, title=title, projectarea_name=project_name, **kwargs)

        if not wi:
            return json.dumps({"success": False, "error": "Failed to create work item"})

        # Get the created work item ID
        workitem_id = getattr(wi, "identifier", "Unknown")

        result = {
            "success": True,
            "message": f"Successfully created {workitem_type} #{workitem_id} in project '{project_name}'",
            "workitem_id": workitem_id,
            "workitem": _workitem_to_dict(wi),
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        logging.error(f"Error creating work item: {e}", exc_info=True)
        return json.dumps({"error": str(e)})


# ============= Work Item Update Functions =============


@mcp.tool()
def update_workitem_field(
    workitem_id: str,
    field_name: str,
    field_value: str,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Update a single field in a work item

    Args:
        workitem_id: Work item ID/number
        field_name: Name of the field to update (e.g., 'title', 'description', 'state', 'ownedBy')
        field_value: New value for the field
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing success status and updated work item data

    Example:
        update_workitem_field("12345", "title", "New Title")
        update_workitem_field("12345", "state", "In Progress")
        update_workitem_field("12345", "description", "Updated description text")
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Create updates dictionary with single field
        updates = {field_name: field_value}

        # Update the work item
        updated_wi = client.updateWorkitem(workitem_id, updates)

        result = {
            "success": True,
            "message": f"Successfully updated field '{field_name}' in work item #{workitem_id}",
            "workitem": _workitem_to_dict(updated_wi),
        }

        return json.dumps(result)

    except Exception as e:
        logging.error(f"Failed to update work item field: {e}")
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def update_workitem_multiple_fields(
    workitem_id: str,
    fields_json: str,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Update multiple fields in a work item at once

    Args:
        workitem_id: Work item ID/number
        fields_json: JSON string of field names and values to update
                    Example: '{"title": "New Title", "description": "New Desc", "state": "In Progress"}'
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing success status and updated work item data

    Example:
        update_workitem_multiple_fields("12345", '{"title": "New Title", "state": "Resolved"}')
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Parse the fields JSON
        updates = json.loads(fields_json)

        if not isinstance(updates, dict):
            raise ValueError("fields_json must be a JSON object/dictionary")

        # Update the work item
        updated_wi = client.updateWorkitem(workitem_id, updates)

        result = {
            "success": True,
            "message": f"Successfully updated {len(updates)} field(s) in work item #{workitem_id}",
            "updated_fields": list(updates.keys()),
            "workitem": _workitem_to_dict(updated_wi),
        }

        return json.dumps(result)

    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in fields_json: {e}")
        return json.dumps({"success": False, "error": f"Invalid JSON format: {str(e)}"})
    except Exception as e:
        logging.error(f"Failed to update work item fields: {e}")
        return json.dumps({"success": False, "error": str(e)})


@mcp.tool()
def update_workitem_state(
    workitem_id: str,
    new_state: str,
    server_url: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
) -> str:
    """
    Update the state of a work item

    Args:
        workitem_id: Work item ID/number
        new_state: New state value (e.g., 'New', 'In Progress', 'Resolved', 'Closed')
        server_url: Optional RTC server URL
        username: Optional username
        password: Optional password

    Returns:
        JSON string containing success status and updated work item data

    Example:
        update_workitem_state("12345", "In Progress")
        update_workitem_state("12345", "Resolved")
    """
    try:
        client = get_rtc_client(server_url, username, password)

        # Create updates dictionary with state field
        updates = {"state": new_state}

        # Update the work item
        updated_wi = client.updateWorkitem(workitem_id, updates)

        result = {
            "success": True,
            "message": f"Successfully updated state of work item #{workitem_id} to '{new_state}'",
            "workitem": _workitem_to_dict(updated_wi),
        }

        return json.dumps(result)

    except Exception as e:
        logging.error(f"Failed to update work item state: {e}")
        return json.dumps({"success": False, "error": str(e)})


# ============= Utility Functions =============


def get_mcp_init_vars() -> tuple[str, str, int]:
    """
    Get MCP initialization variables from environment configuration

    Returns:
        Tuple of (transport, host, port)

    Raises:
        ValueError: If PORT is invalid
    """
    transport = os.getenv("TRANSPORT") or "stdio"
    if transport in ["stdio", "<TRANSPORT>", None, "", "-", "null"]:
        logging.info("MCP init: transport=stdio")
        return ("stdio", "", 0)

    host = os.getenv("HOST") or "127.0.0.1"
    port_str = os.getenv("HOST_PORT") or "8001"

    if host == "<HOST>":
        host = "127.0.0.1"
    if port_str == "<HOST_PORT>":
        port_str = "8001"

    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"Invalid PORT env variable: '{port_str}' - must be a valid integer")

    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


# ============= Main Entry Point =============

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", force=True)

    transport, host, port = get_mcp_init_vars()

    if transport == "stdio":
        logging.info("Starting CCM/RTC MCP Server with STDIO transport...")
        mcp.run(transport="stdio")
    else:
        logging.info(f"Starting CCM/RTC MCP Server with {transport.upper()} transport...")
        logging.info(f"Server will be available at: http://{host}:{port}/mcp")
        logging.info("Press Ctrl+C to stop the server")
        mcp.run(transport=transport, host=host, port=port)
