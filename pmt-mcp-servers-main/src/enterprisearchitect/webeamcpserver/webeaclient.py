"""
Enterprise Architect OSLC API Client  (webEA)
Provides a thin wrapper around EA's OSLC REST API, returning raw XML responses
for processing by MCP server and LLM.
reference: https://sparxsystems.com/enterprise_architect_user_guide/17.1/the_model_repository/oslc_am_top.html
"""

import base64
import os
import re
import uuid
import xml.etree.ElementTree as ET
from typing import Any, Dict, Optional, Tuple
from urllib.parse import quote, unquote

import requests
import urllib3
from requests.adapters import HTTPAdapter
from requests_ntlm import HttpNtlmAuth
from urllib3.util.retry import Retry

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class WebEAController:
    """
    Enterprise Architect API client that returns raw XML responses.
    Minimal parsing only for authentication and package verification.
    """

    # XML namespaces
    NAMESPACES = {
        "ss": "http://www.sparxsystems.com.au/oslc_am#",
        "dcterms": "http://purl.org/dc/terms/",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "oslc_am": "http://open-services.net/ns/am#",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "foaf": "http://xmlns.com/foaf/0.1/",
    }

    # GUID prefixes according to documentation
    GUID_PREFIXES = {
        "ModelRoot": "mr_",
        "Package": "pk_",
        "Element": "el_",
        "Diagram": "dg_",
        "Link": "lt_",
        "RunState": "rs_",
        "Attribute": "at_",
        "AttributeTaggedValue": "attv_",
        "Operation": "op_",
        "OperationTaggedValue": "optv_",
        "OperationParameter": "pr_",
        "LinkedDocument": "ld_",
        "DiagramImage": "di_",
        "Requirement": "rq_",
        "Constraint": "cn_",
        "Scenario": "sc_",
        "File": "fl_",
        "TaggedValue": "tv_",
        "Test": "ts_",
        "ResourceAllocation": "ra_",
        "Change": "ch_",
        "Defect": "df_",
        "Issue": "is_",
        "Task": "tk_",
        "Event": "ev_",
        "Decision": "dc_",
        "Document": "dm_",
        "Feature": "mf_",
        "Effort": "ef_",
        "Risk": "ri_",
        "Metric": "me_",
        "Discussion": "dr_",
    }

    # Connector types reference
    CONNECTOR_TYPES = {
        "UML": [
            "Association",
            "Aggregation",
            "Composition",
            "Generalization",
            "Dependency",
            "Realization",
            "Usage",
            "Abstraction",
            "Substitution",
        ],
        "Behavioral": [
            "Sequence",
            "Collaboration",
            "StateFlow",
            "ControlFlow",
            "ObjectFlow",
        ],
        "UseCase": ["UseCase", "Include", "Extend"],
        "Component": ["Assembly", "Delegate"],
        "Deployment": ["Deploy", "Manifest"],
        "BPMN": ["ControlFlow", "Association"],  # For BPMN2.0
        "Other": ["InformationFlow", "Nesting", "Interaction", "Collaboration"],
    }

    def __init__(
        self,
        server_url: str,
        model_name: str,
        username: str = "",
        password: str = "",
    ):
        """
        Initialize the EA API client

        Args:
            server_url: EA server URL
            model_name: EA model name
            username: Username for authentication
            password: Password for authentication
        """
        self.server_url = server_url.rstrip("/")
        self.model_name = model_name
        self.username = username
        self.password = password
        self.user_token = None
        self.session = self._create_session()
        self.base_url = f"{self.server_url}/{self.model_name}/oslc/am"

    def _create_session(
        self,
        retries: int = 3,
        backoff_factor: float = 0.3,
        status_forcelist: Tuple[int, ...] = (500, 502, 504),
    ) -> requests.Session:
        """Configure session with retry logic"""
        session = requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _clean_sql(self, query: str) -> str:
        """Clean SQL query by removing comments and normalizing whitespace."""
        # remove -- comments
        q = re.sub(r"--.*?(\n|$)", "", query)
        # remove /* */ comments
        q = re.sub(r"/\*.*?\*/", "", query, flags=re.DOTALL)
        # collapse spaces
        return " ".join(q.split()).lower()

    def _contains_destructive_sql(self, query: str) -> bool:
        """Check if SQL query contains destructive statements that can modify or delete data.

        Blocks: DELETE, DROP, TRUNCATE, ALTER (can drop columns/tables)
        Allows: INSERT, UPDATE (handled by separate validation)

        Matches at the start of statement or after semicolon to avoid
        false positives from string literals or WHERE clauses.
        """
        q = self._clean_sql(query)
        # Match destructive keywords at start of statement or after semicolon
        destructive_keywords = r"(delete|drop|truncate|alter)"
        return bool(re.search(rf"(^|;)\s*{destructive_keywords}\b", q))

    def authenticate(self) -> Dict[str, Any]:
        """
        Authenticate to webEA endpoint.
        Returns minimal info - user token and package GUID only.
        """
        login_url = f"{self.base_url}/login/"

        try:
            self.session.auth = HttpNtlmAuth(self.username, self.password, self.session)
            response = self.session.post(login_url, data="sso=ntlm;", verify=False)
            response.raise_for_status()

            # Extract user token
            self.user_token = self._extract_text(response.text, ".//ss:useridentifier")

            if not self.user_token:
                return {"success": False, "message": "Failed to extract user token"}

            return {
                "success": True,
                "message": "Authentication successful",
                "user_token": self.user_token,
            }

        except Exception as e:
            return {"success": False, "message": f"Authentication failed: {str(e)}"}

    def _extract_text(self, xml_content: str, xpath: str) -> Optional[str]:
        """
        Minimal XML parsing - extract single text value.
        Used only for authentication and verification.
        """
        try:
            root = ET.fromstring(xml_content)
            element = root.find(xpath, self.NAMESPACES)
            return element.text if element is not None and element.text else None
        except Exception:
            return None

    def _normalize_guid(self, resource_guid: str, expected_prefix: str = None) -> str:
        """
        Normalize GUID to ensure proper format with prefix and braces.

        Args:
            resource_guid: GUID in any format
            expected_prefix: Expected prefix (el_, dg_, pk_, etc.)

        Returns:
            Normalized GUID with correct prefix and braces
        """
        # Remove any existing prefix and braces
        clean_guid = resource_guid
        for prefix in self.GUID_PREFIXES.values():
            clean_guid = clean_guid.replace(prefix, "")
        clean_guid = clean_guid.replace("{", "").replace("}", "").strip()

        # Add prefix if provided
        if expected_prefix:
            return f"{expected_prefix}{{{clean_guid}}}"
        else:
            # Try to detect prefix from original guid
            for prefix in self.GUID_PREFIXES.values():
                if resource_guid.startswith(prefix):
                    return f"{prefix}{{{clean_guid}}}"
            # If no prefix found, return with braces only
            return f"{{{clean_guid}}}"

    def _build_url(self, path: str, guid: str = None) -> str:
        """
        Build API URL with optional GUID parameter.
        Uses manual URL construction to avoid encoding issues.
        """
        url = f"{self.base_url}/{path}"
        if guid:
            url += f"/{guid}"
        url += f"/?useridentifier={self.user_token}"
        return url

    def _make_request(self, url: str) -> Optional[str]:
        """
        Make HTTP request using PreparedRequest to avoid URL encoding.
        Returns raw XML response or None on failure.
        """
        try:
            req = requests.Request("GET", url)
            prepared = self.session.prepare_request(req)
            prepared.url = url  # Override to prevent encoding
            response = self.session.send(prepared, verify=False)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(e)
            return None

    def query_resources(self, where_clause: str = "", select_fields: str = "*") -> Optional[str]:
        """
        Query resources and return raw XML response.

        Args:
            where_clause: OSLC where clause for filtering
            select_fields: Fields to select (comma-separated or *)

        Returns:
            XML response as string or None on failure
        """
        if not self.user_token:
            return None

        # Check for destructive SQL operations in where clause
        if where_clause and self._contains_destructive_sql(where_clause):
            raise PermissionError(
                "Destructive SQL operations (DELETE, DROP, TRUNCATE, ALTER) are restricted for safety. "
                "Should be done by the user manually."
            )

        # Check for destructive SQL operations in select fields
        if select_fields and select_fields != "*" and self._contains_destructive_sql(select_fields):
            raise PermissionError(
                "Destructive SQL operations (DELETE, DROP, TRUNCATE, ALTER) are restricted for safety. "
                "Should be done by the user manually."
            )
        select_fields = quote(unquote(select_fields), safe=",")
        where_clause = quote(unquote(where_clause), safe="")
        url = f"{self.base_url}/qc/"
        params = {"useridentifier": self.user_token}

        if select_fields and select_fields != "*":
            params["oslc.select"] = select_fields

        if where_clause:
            params["oslc.where"] = where_clause

        try:
            response = self.session.get(url, params=params, verify=False)
            response.raise_for_status()
            return response.text
        except Exception:
            return None

    def get_root_package(self) -> Optional[str]:
        """
        Get the root (top-level) package of the current model.
        Returns raw XML response.
        """
        if not self.user_token:
            return None

        where_clause = 'dcterms:type="ModelRoot"'
        return self.query_resources(where_clause=where_clause)

    def get_package_info(self, package_guid: str) -> Dict[str, Optional[str]]:
        """
        Get comprehensive information about a package including its contents.

        Args:
            package_guid: Package GUID (mandatory)

        Returns:
            Dict containing raw XML for:
            - basic: Package basic properties
            - resources_in_package_xml: All resources in the package
        """
        if not package_guid:
            return {
                "success": False,
                "message": "Package GUID is required",
                "basic": None,
                "resources_in_package_xml": None,
            }

        # Normalize GUID if needed
        if not package_guid.startswith("pk_"):
            package_guid = self._normalize_guid(package_guid, "pk_")

        # Get basic package info
        basic_info = self.get_resource(package_guid)

        if not basic_info:
            return {
                "success": False,
                "message": f"Could not retrieve package information for GUID: {package_guid}",
                "basic": None,
                "resources_in_package_xml": None,
            }

        # Query for child elements using parent identifier
        resources_in_package = self.query_resources(where_clause=f'ss:parentresourceidentifier="{package_guid}"')
        return {
            "success": True,
            "message": f"Retrieved package information for {package_guid}",
            "basic": basic_info,
            "resources_in_package_xml": str(resources_in_package),
        }

    def get_resource(self, resource_guid: str) -> Optional[str]:
        """
        Get a resource by GUID and return raw XML.

        Args:
            resource_guid: Resource GUID (with prefix like el_, dg_, pk_)

        Returns:
            XML response as string or None on failure
        """
        if not self.user_token:
            return None

        normalized_guid = self._normalize_guid(resource_guid)
        url = self._build_url("resource", normalized_guid)
        return self._make_request(url)

    def get_diagram_info(self, diagram_guid: str) -> Optional[str]:
        """
        Get all possible information about a diagram.

        Args:
            diagram_guid: Diagram GUID

        Returns:
            Raw XML with diagram information
        """
        if not diagram_guid.startswith("dg_"):
            diagram_guid = self._normalize_guid(diagram_guid, "dg_")

        return self.get_resource(diagram_guid)

    def get_element_info(self, element_guid: str) -> Dict[str, Any]:
        """
        Get comprehensive information about an element.

        Args:
            element_guid: Element GUID (with or without 'el_' prefix)

        Returns:
            Dict containing basic info and element properties
        """
        if not element_guid.startswith("el_"):
            element_guid = self._normalize_guid(element_guid, "el_")

        # Get basic element info
        basic_info = self.get_resource(element_guid)

        if not basic_info:
            return {
                "success": False,
                "message": f"Could not retrieve element information for GUID: {element_guid}",
            }

        # Get all element properties as separate XML responses
        result = {
            "success": True,
            "message": f"Retrieved element information for {element_guid}",
            "basic": basic_info,
            "attributes": self.get_element_attributes(element_guid),
            "operations": self.get_element_operations(element_guid),
            "connectors": self.get_element_connectors(element_guid),
            "requirements": self.get_element_requirements(element_guid),
            "constraints": self.get_element_constraints(element_guid),
            "scenarios": self.get_element_scenarios(element_guid),
            "tagged_values": self.get_element_tagged_values(element_guid),
            "tests": self.get_element_tests(element_guid),
            "discussions": self.get_element_discussions(element_guid),
            "files": self.get_element_files(element_guid),
            "resource_allocations": self.get_element_resource_allocations(element_guid),
            "changes": self.get_element_changes(element_guid),
            "defects": self.get_element_defects(element_guid),
            "issues": self.get_element_issues(element_guid),
            "tasks": self.get_element_tasks(element_guid),
            "events": self.get_element_events(element_guid),
            "decisions": self.get_element_decisions(element_guid),
            "documents": self.get_element_documents(element_guid),
            "features": self.get_element_features(element_guid),
            "efforts": self.get_element_efforts(element_guid),
            "risks": self.get_element_risks(element_guid),
            "metrics": self.get_element_metrics(element_guid),
        }

        return result

    def get_feature(self, endpoint: str, resource_guid: str) -> Optional[str]:
        """
        Get a resource feature and return raw XML.

        Args:
            endpoint: API endpoint (e.g., 'attributes', 'operations', 'linkedresources')
            resource_guid: Resource GUID (with prefix)

        Returns:
            XML response as string or None on failure
        """
        if not self.user_token:
            return None

        normalized_guid = self._normalize_guid(resource_guid)
        url = self._build_url(endpoint, normalized_guid)
        return self._make_request(url)

    # Feature-specific methods
    def get_element_attributes(self, element_guid: str) -> Optional[str]:
        """Get element attributes - returns raw XML"""
        return self.get_feature("attributes", element_guid)

    def get_element_operations(self, element_guid: str) -> Optional[str]:
        """Get element operations - returns raw XML"""
        return self.get_feature("operations", element_guid)

    def get_element_connectors(self, element_guid: str) -> Optional[str]:
        """Get element connectors - returns raw XML"""
        return self.get_feature("linkedresources", element_guid)

    def get_element_requirements(self, element_guid: str) -> Optional[str]:
        """Get element requirements - returns raw XML"""
        return self.get_feature("requirements", element_guid)

    def get_element_constraints(self, element_guid: str) -> Optional[str]:
        """Get element constraints - returns raw XML"""
        return self.get_feature("constraints", element_guid)

    def get_element_scenarios(self, element_guid: str) -> Optional[str]:
        """Get element scenarios - returns raw XML"""
        return self.get_feature("scenarios", element_guid)

    def get_element_files(self, element_guid: str) -> Optional[str]:
        """Get element files - returns raw XML"""
        return self.get_feature("files", element_guid)

    def get_element_tagged_values(self, element_guid: str) -> Optional[str]:
        """Get element tagged values - returns raw XML"""
        return self.get_feature("taggedvalues", element_guid)

    def get_element_tests(self, element_guid: str) -> Optional[str]:
        """Get element tests - returns raw XML"""
        return self.get_feature("tests", element_guid)

    def get_element_discussions(self, element_guid: str) -> Optional[str]:
        """Get element discussions - returns raw XML"""
        return self.get_feature("discussions", element_guid)

    def get_element_resource_allocations(self, element_guid: str) -> Optional[str]:
        """Get element resource allocations - returns raw XML"""
        return self.get_feature("resourceallocations", element_guid)

    def get_element_changes(self, element_guid: str) -> Optional[str]:
        """Get element changes - returns raw XML"""
        return self.get_feature("changes", element_guid)

    def get_element_defects(self, element_guid: str) -> Optional[str]:
        """Get element defects - returns raw XML"""
        return self.get_feature("defects", element_guid)

    def get_element_issues(self, element_guid: str) -> Optional[str]:
        """Get element issues - returns raw XML"""
        return self.get_feature("issues", element_guid)

    def get_element_tasks(self, element_guid: str) -> Optional[str]:
        """Get element tasks - returns raw XML"""
        return self.get_feature("tasks", element_guid)

    def get_element_events(self, element_guid: str) -> Optional[str]:
        """Get element events - returns raw XML"""
        return self.get_feature("events", element_guid)

    def get_element_decisions(self, element_guid: str) -> Optional[str]:
        """Get element decisions - returns raw XML"""
        return self.get_feature("decisions", element_guid)

    def get_element_documents(self, element_guid: str) -> Optional[str]:
        """Get element documents - returns raw XML"""
        return self.get_feature("documents", element_guid)

    def get_element_features(self, element_guid: str) -> Optional[str]:
        """Get element features - returns raw XML"""
        return self.get_feature("mfeatures", element_guid)

    def get_element_efforts(self, element_guid: str) -> Optional[str]:
        """Get element efforts - returns raw XML"""
        return self.get_feature("efforts", element_guid)

    def get_element_risks(self, element_guid: str) -> Optional[str]:
        """Get element risks - returns raw XML"""
        return self.get_feature("risks", element_guid)

    def get_element_metrics(self, element_guid: str) -> Optional[str]:
        """Get element metrics - returns raw XML"""
        return self.get_feature("metrics", element_guid)

    def get_operation_parameters(self, operation_guid: str) -> Optional[str]:
        """Get operation parameters - returns raw XML"""
        return self.get_feature("parameters", operation_guid)

    def get_diagram_image(self, diagram_guid: str) -> Optional[str]:
        """
        Get diagram image by accessing the diagram's features endpoint.

        Args:
            diagram_guid: Diagram GUID (with or without 'dg_' prefix)

        Returns:
            decoded png format of base64
        """
        if not self.user_token:
            return None

        # Ensure proper GUID format
        if not diagram_guid.startswith("dg_"):
            diagram_guid = self._normalize_guid(diagram_guid, "dg_")

        # Access the features endpoint which contains the embedded image
        url = f"{self.base_url}/features/{diagram_guid}/?useridentifier={self.user_token}"

        try:
            req = requests.Request("GET", url)
            prepared = self.session.prepare_request(req)
            prepared.url = url  # Override to prevent encoding
            response = self.session.send(prepared, verify=False)
            response.raise_for_status()
            try:
                root = ET.fromstring(response.text)
                image_elem = root.find(".//ss:image", self.NAMESPACES)
                if image_elem is not None and image_elem.text:
                    # Decode Base64 to bytes
                    output_dir = os.path.join("webea_mcpserver_output", "downloaded_diagrams")
                    os.makedirs(output_dir, exist_ok=True)
                    img_name = os.path.join(output_dir, f"diagram_{diagram_guid.replace('{', '').replace('}', '')}.png")
                    with open(img_name, "wb") as img_file:
                        img_file.write(base64.b64decode(image_elem.text.strip()))
                    return f"Image saved successfully: {img_name}"

            except Exception as e:
                return f"Error extracting PNG: {str(e)}"
        except Exception:
            return None

    def get_diagram_discussions(self, diagram_guid: str) -> Optional[str]:
        """Get diagram discussions - returns raw XML"""
        return self.get_feature("discussions", diagram_guid)

    def logout(self) -> Dict[str, bool]:
        """
        Logout from the EA server.
        Returns simple success/failure dict.
        """
        if not self.user_token:
            return {"success": True}

        logout_url = f"{self.base_url}/logout/"
        params = {"useridentifier": self.user_token}

        try:
            response = self.session.get(logout_url, params=params, verify=False)
            response.raise_for_status()
            self.user_token = None
            self.is_package_verified = False
            return {"success": True}
        except Exception:
            return {"success": False}

    # Creations methods:
    def create_package(
        self,
        title: str,
        parent_package_guid: str,
        description: str = "",
    ) -> Dict[str, Any]:
        """Create a new package in EA."""
        if not self.user_token:
            return {"success": False, "message": "Not authenticated"}

        if not parent_package_guid:
            return {
                "success": False,
                "message": "Parent package GUID is required",
            }

        if not parent_package_guid.startswith("pk_"):
            parent_guid = self._normalize_guid(parent_package_guid, "pk_")
        else:
            parent_guid = parent_package_guid

        # Build creation XML payload
        xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:oslc_am="http://open-services.net/ns/am#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dcterms="http://purl.org/dc/terms/" 
            xmlns:foaf="http://xmlns.com/foaf/0.1/"
            xmlns:ss="http://www.sparxsystems.com.au/oslc_am#">
        <oslc_am:Resource>
            <dcterms:title>{self._escape_xml(title)}</dcterms:title>
            <dcterms:type>Package</dcterms:type>
            <ss:resourcetype>Package</ss:resourcetype>
            <ss:parentresourceidentifier>{parent_guid}</ss:parentresourceidentifier>
            <ss:useridentifier>{self.user_token}</ss:useridentifier>"""

        if description:
            xml_payload += f"""
            <dcterms:description>{self._escape_xml(description)}</dcterms:description>"""

        xml_payload += """
        </oslc_am:Resource>
    </rdf:RDF>"""

        # POST to creation factory - NO useridentifier in URL!
        url = f"{self.base_url}/cf/resource/"

        try:
            response = self.session.post(
                url,
                data=xml_payload.encode("utf-8"),
                headers={"Content-Type": "application/rdf+xml"},
                verify=False,
            )
            response.raise_for_status()

            created_guid = self._extract_text(response.text, ".//dcterms:identifier")

            return {
                "success": True,
                "message": f"Package created successfully: {title}",
                "guid": created_guid,
                "xml": response.text,
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create package: {str(e)}",
                "xml_sent": xml_payload,
            }

    def create_element(
        self,
        title: str,
        element_type: str,
        parent_package_guid: str,
        description: str = "",
        stereotype: str = None,
        **optional_props,
    ) -> Dict[str, Any]:
        """
        Create a new element in EA. This is the implementation for the MCP tool.
        """
        if not self.user_token:
            return {"success": False, "message": "Not authenticated"}

        if not parent_package_guid:
            return {
                "success": False,
                "message": "Parent package GUID is required",
            }
        parent_guid = self._normalize_guid(parent_package_guid, "pk_")

        xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:oslc_am="http://open-services.net/ns/am#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:foaf="http://xmlns.com/foaf/0.1/"
            xmlns:ss="http://www.sparxsystems.com.au/oslc_am#">
        <oslc_am:Resource>
            <dcterms:title>{self._escape_xml(title)}</dcterms:title>
            <dcterms:type>{self._escape_xml(element_type)}</dcterms:type>
            <ss:resourcetype>Element</ss:resourcetype>
            <ss:parentresourceidentifier>{parent_guid}</ss:parentresourceidentifier>
            <ss:useridentifier>{self.user_token}</ss:useridentifier>"""

        if description:
            xml_payload += f"""
            <dcterms:description>{self._escape_xml(description)}</dcterms:description>"""
        if "keywords" in optional_props and optional_props["keywords"]:
            xml_payload += f"""
            <dcterms:subject>{self._escape_xml(optional_props["keywords"])}</dcterms:subject>"""
        if "author" in optional_props and optional_props["author"]:
            xml_payload += f"""
            <dcterms:creator>
                <foaf:Person>
                    <foaf:name>{self._escape_xml(optional_props["author"])}</foaf:name>
                </foaf:Person>
            </dcterms:creator>"""

        property_mappings = {
            "alias": "ss:alias",
            "status": "ss:status",
            "complexity": "ss:complexity",
            "phase": "ss:phase",
            "version": "ss:version",
            "difficulty": "ss:difficulty",
            "priority": "ss:priority",
            "language": "ss:language",
        }
        for prop_name, xml_tag in property_mappings.items():
            if prop_name in optional_props and optional_props[prop_name] is not None:
                xml_payload += f"""
            <{xml_tag}>{self._escape_xml(str(optional_props[prop_name]))}</{xml_tag}>"""
        if stereotype:
            xml_payload += f"""
            <ss:stereotype>
                <ss:stereotypename>
                    <ss:name>{self._escape_xml(stereotype)}</ss:name>
                </ss:stereotypename>
            </ss:stereotype>"""

        xml_payload += """
        </oslc_am:Resource>
    </rdf:RDF>"""
        url = f"{self.base_url}/cf/resource/"
        try:
            response = self.session.post(
                url,
                data=xml_payload.encode("utf-8"),
                headers={"Content-Type": "application/rdf+xml"},
                verify=False,
            )
            response.raise_for_status()
            created_guid = self._extract_text(response.text, ".//dcterms:identifier")
            return {
                "success": True,
                "message": f"Element created successfully: {title}",
                "guid": created_guid,
                "xml": response.text,
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "message": f"Failed to create element: {e.response.status_code} - {e.response.text}",
                "xml_sent": xml_payload,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create element: {str(e)}",
                "xml_sent": xml_payload,
            }

    def update_element(self, element_guid: str, **properties) -> Dict[str, Any]:
        """Update properties of an existing element."""
        if not self.user_token:
            return {"success": False, "message": "Not authenticated"}

        element_guid = self._normalize_guid(element_guid, "el_")

        xml_payload = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:oslc_am="http://open-services.net/ns/am#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:foaf="http://xmlns.com/foaf/0.1/"
            xmlns:ss="http://www.sparxsystems.com.au/oslc_am#">
        <oslc_am:Resource>
            <dcterms:identifier>{element_guid}</dcterms:identifier>
            <ss:useridentifier>{self.user_token}</ss:useridentifier>"""

        if "title" in properties:
            xml_payload += f"""
            <dcterms:title>{self._escape_xml(properties["title"])}</dcterms:title>"""
        if "description" in properties:
            xml_payload += f"""
            <dcterms:description>{self._escape_xml(properties["description"])}</dcterms:description>"""
        if "keywords" in properties:
            xml_payload += f"""
            <dcterms:subject>{self._escape_xml(properties["keywords"])}</dcterms:subject>"""
        if "author" in properties:
            xml_payload += f"""
            <dcterms:creator>
                <foaf:Person>
                    <foaf:name>{self._escape_xml(properties["author"])}</foaf:name>
                </foaf:Person>
            </dcterms:creator>"""

        property_mappings = {
            "alias": "ss:alias",
            "status": "ss:status",
            "complexity": "ss:complexity",
            "phase": "ss:phase",
            "version": "ss:version",
            "difficulty": "ss:difficulty",
            "priority": "ss:priority",
            "language": "ss:language",
        }
        for prop_name, xml_tag in property_mappings.items():
            if prop_name in properties and properties[prop_name] is not None:
                xml_payload += f"""
            <{xml_tag}>{self._escape_xml(str(properties[prop_name]))}</{xml_tag}>"""

        xml_payload += """
        </oslc_am:Resource>
    </rdf:RDF>"""
        url = f"{self.base_url}/pu/resource/"
        try:
            response = self.session.post(
                url,
                data=xml_payload.encode("utf-8"),
                headers={"Content-Type": "application/rdf+xml"},
                verify=False,
            )
            response.raise_for_status()
            return {
                "success": True,
                "message": f"Element updated successfully: {element_guid}",
                "xml": response.text,
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "message": f"Failed to update element: {e.response.status_code} - {e.response.text}",
                "xml_sent": xml_payload,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update element: {str(e)}",
                "xml_sent": xml_payload,
            }

    def create_connector(
        self,
        source_element_guid: str,
        target_element_guid: str,
        connector_type: str,
        name: str = "",
        description: str = "",
        direction: str = "Source -> Destination",
        stereotype: str = None,
    ) -> Dict[str, Any]:
        """Create a connector (relationship) between two elements."""
        if not self.user_token:
            return {"success": False, "message": "Not authenticated"}

        source_guid_norm = self._normalize_guid(source_element_guid, "el_")
        target_guid_norm = self._normalize_guid(target_element_guid, "el_")

        conn_id = f"conn_{str(uuid.uuid4())[:8]}"
        target_url = f"{self.server_url}/{self.model_name}/oslc/am/resource/{target_guid_norm}/"

        xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:oslc_am="http://open-services.net/ns/am#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:ss="http://www.sparxsystems.com.au/oslc_am#">
        <oslc_am:Resource>
            <dcterms:identifier>{source_guid_norm}</dcterms:identifier>
            <ss:{connector_type} rdf:ID="{conn_id}" rdf:resource="{target_url}"/>
        </oslc_am:Resource>
        <rdf:Description rdf:about="#{conn_id}">
            <ss:useridentifier>{self.user_token}</ss:useridentifier>'''

        if name:
            xml_payload += f"""
            <dcterms:title>{self._escape_xml(name)}</dcterms:title>"""

        # -- CORRECTED FIX --
        # This property is mandatory for certain connector types like Composition and Realization.
        # It is now always included to ensure all connector types can be created successfully.
        if connector_type:
            xml_payload += f"""
            <dcterms:type>{self._escape_xml(connector_type)}</dcterms:type>"""
        # -------------------

        if description:
            xml_payload += f"""
            <dcterms:description>{self._escape_xml(description)}</dcterms:description>"""
        if direction:
            xml_payload += f"""
            <ss:direction>{self._escape_xml(direction)}</ss:direction>"""
        if stereotype:
            xml_payload += f"""
            <ss:stereotype>
                <ss:stereotypename>
                    <ss:name>{self._escape_xml(stereotype)}</ss:name>
                </ss:stereotypename>
            </ss:stereotype>"""

        xml_payload += """
        </rdf:Description>
    </rdf:RDF>"""

        url = f"{self.base_url}/cf/resourcelink/"
        try:
            response = self.session.post(
                url,
                data=xml_payload.encode("utf-8"),
                headers={"Content-Type": "application/rdf+xml"},
                verify=False,
            )
            response.raise_for_status()

            created_guid = self._extract_text(response.text, ".//dcterms:identifier")

            return {
                "success": True,
                "message": f'Connector "{name}" of type "{connector_type}" created successfully.',
                "guid": created_guid,
                "xml": response.text,
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "message": f"Failed to create connector: {e.response.status_code} - {e.response.text}",
                "xml_sent": xml_payload,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to create connector: {str(e)}",
                "xml_sent": xml_payload,
            }

    def update_connector(
        self,
        connector_guid: str,
        source_element_guid: str,
        target_element_guid: str,
        connector_type: str,
        name: str = None,
        description: str = None,
        direction: str = None,
    ) -> Dict[str, Any]:
        """Update properties of an existing connector."""
        if not self.user_token:
            return {"success": False, "message": "Not authenticated"}

        conn_guid_norm = self._normalize_guid(connector_guid, "lt_")
        source_guid_norm = self._normalize_guid(source_element_guid, "el_")
        target_guid_norm = self._normalize_guid(target_element_guid, "el_")
        conn_id = f"conn_{str(uuid.uuid4())[:8]}"
        target_url = f"{self.server_url}/{self.model_name}/oslc/am/resource/{target_guid_norm}/"

        xml_payload = f'''<?xml version="1.0" encoding="UTF-8"?>
    <rdf:RDF xmlns:oslc_am="http://open-services.net/ns/am#"
            xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dcterms="http://purl.org/dc/terms/"
            xmlns:ss="http://www.sparxsystems.com.au/oslc_am#">
        <oslc_am:Resource>
            <dcterms:identifier>{source_guid_norm}</dcterms:identifier>
            <ss:{connector_type} rdf:ID="{conn_id}" rdf:resource="{target_url}"/>
        </oslc_am:Resource>
        <rdf:Description rdf:about="#{conn_id}">
            <dcterms:identifier>{conn_guid_norm}</dcterms:identifier>
            <ss:useridentifier>{self.user_token}</ss:useridentifier>'''

        if name is not None:
            xml_payload += f"""
            <dcterms:title>{self._escape_xml(name)}</dcterms:title>"""
        if description is not None:
            xml_payload += f"""
            <dcterms:description>{self._escape_xml(description)}</dcterms:description>"""
        if direction is not None:
            xml_payload += f"""
            <ss:direction>{self._escape_xml(direction)}</ss:direction>"""

        xml_payload += """
        </rdf:Description>
    </rdf:RDF>"""
        url = f"{self.base_url}/pu/resourcelink/"
        try:
            response = self.session.post(
                url,
                data=xml_payload.encode("utf-8"),
                headers={"Content-Type": "application/rdf+xml"},
                verify=False,
            )
            response.raise_for_status()
            return {
                "success": True,
                "message": f"Connector {conn_guid_norm} updated successfully",
                "xml": response.text,
            }
        except requests.exceptions.HTTPError as e:
            return {
                "success": False,
                "message": f"Failed to update connector: {e.response.status_code} - {e.response.text}",
                "xml_sent": xml_payload,
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to update connector: {str(e)}",
                "xml_sent": xml_payload,
            }

    def _escape_xml(self, text: str) -> str:
        """Escape special XML characters."""
        if not text:
            return ""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&apos;")
        )
