import logging
import re
import time
import xml.etree.ElementTree as ET

import win32com.client


class EAController:
    """Enterprise Architect Controller.

    Provides a high-level wrapper around the Enterprise Architect COM automation
    interface, exposing convenience methods for common repository, package,
    diagram and element operations.
    """

    def __init__(self):
        """Initialize the EA Controller and connect to the repository."""
        self.repository = None
        self.ea = None
        self.connect()

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
        Allows: SELECT queries only (COM API is read-only)

        Matches at the start of statement or after semicolon to avoid
        false positives from string literals or WHERE clauses.
        """
        q = self._clean_sql(query)
        # Match destructive keywords at start of statement or after semicolon
        destructive_keywords = r"(delete|drop|truncate|alter)"
        return bool(re.search(rf"(^|;)\s*{destructive_keywords}\b", q))

    def connect(self):
        """Connect to an active Enterprise Architect application instance.

        Attempts to connect to an existing instance of Enterprise Architect. If no
        instance is found, a new instance is launched and connected.

        Returns:
            str: Connection status message.
        """
        logging.info("Connecting to App...")
        try:
            self.ea = win32com.client.GetActiveObject("EA.App")
            self.repository = self.ea.Repository
            logging.info("Connected to existing app.")
            return "Connected to EA Repository successfully."
        except Exception:
            logging.info("No existing instance found, launching new EA instance.")
            self.ea = win32com.client.Dispatch("EA.App")
            self.repository = self.ea.Repository
            logging.info("Started and connected to new EA app instance.")
            return "Connected to EA Repository successfully."

    def disconnect(self):
        """Disconnect from the repository and close the session.

        Ensures that the connection to the Enterprise Architect repository is
        properly closed and the application instance is terminated.

        Returns:
            str: Disconnection status message.
        """
        if self.repository:
            logging.info("Disconnecting from EA repository.")
            self.repository.Exit()
            self.repository = None
            logging.info("Disconnected from EA application.")
            return "Disconnected successfully."
        logging.info("Disconnect requested but no active repository present.")
        return "No active connection to disconnect."

    # --- Element Creation and Update Methods ---

    def create_element(
        self,
        name,
        typeStr,
        packageID,
        stereotype=None,
        notes=None,
        alias=None,
        status=None,
        isAbstract=False,
    ):
        """Creates a new element in a specified package with optional properties.

        Args:
            name (str): Name of the new element.
            typeStr (str): Type of the element (e.g., Class, Interface).
            packageID (int): ID of the parent package where the element will be created.
            stereotype (str, optional): Stereotype to apply to the element. Defaults to None.
            notes (str, optional): Notes or description for the element. Defaults to None.
            alias (str, optional): Alias for the element. Defaults to None.
            status (str, optional): Status of the element. Defaults to None.
            isAbstract (bool, optional): Whether the element is abstract. Defaults to False.

        Returns:
            dict: Success message with element details or error message.
        """
        logging.info(f"Creating element '{name}' of type '{typeStr}' in packageID={packageID}")
        try:
            package = self.repository.GetPackageByID(packageID)
            if not package:
                return {"error": f"Cannot find parent package with ID {packageID}."}
            new_element = package.Elements.AddNew(name, typeStr)
            if stereotype:
                new_element.StereotypeEx = stereotype
            if notes:
                new_element.Notes = notes
            if alias:
                new_element.Alias = alias
            if status:
                new_element.Status = status
            new_element.Abstract = "1" if isAbstract else "0"
            new_element.Update()
            package.Elements.Refresh()
            logging.info(f"Successfully created element '{name}' (ID={new_element.ElementID})")
            return {
                "Success": f"Element '{name}' created successfully.",
                "ElementID": new_element.ElementID,
                "ElementGUID": new_element.ElementGUID,
            }
        except Exception as e:
            return {"error": f"Failed to create element: {e}"}

    def update_element(
        self,
        elementID,
        name=None,
        typeStr=None,
        stereotype=None,
        notes=None,
        alias=None,
        status=None,
        isAbstract=None,
    ):
        """Updates properties of an existing element.

        Args:
            elementID (int): ID of the element to update.
            name (str, optional): New name for the element. Defaults to None.
            typeStr (str, optional): New type for the element. Defaults to None.
            stereotype (str, optional): New stereotype for the element. Defaults to None.
            notes (str, optional): New notes or description for the element. Defaults to None.
            alias (str, optional): New alias for the element. Defaults to None.
            status (str, optional): New status for the element. Defaults to None.
            isAbstract (bool, optional): Whether the element is abstract. Defaults to None.

        Returns:
            dict: Success message with updated properties or error message.
        """
        logging.info(f"Updating element with ID={elementID}")
        try:
            element = self.repository.GetElementByID(elementID)
            if not element:
                return {"error": f"Element with ID {elementID} not found."}
            updated_props = []
            if name is not None:
                element.Name = name
                updated_props.append("Name")
            if typeStr is not None:
                element.Type = typeStr
                updated_props.append("Type")
            if stereotype is not None:
                element.StereotypeEx = stereotype
                updated_props.append("Stereotype")
            if notes is not None:
                element.Notes = notes
                updated_props.append("Notes")
            if alias is not None:
                element.Alias = alias
                updated_props.append("Alias")
            if status is not None:
                element.Status = status
                updated_props.append("Status")
            if isAbstract is not None:
                element.Abstract = "1" if isAbstract else "0"
                updated_props.append("Abstract")
            if not updated_props:
                return {"info": "No properties were specified for update."}
            element.Update()
            logging.info(f"Successfully updated element ID={elementID}. Changed properties: {', '.join(updated_props)}")
            return {
                "Success": f"Element '{element.Name}' (ID={elementID}) updated successfully.",
                "UpdatedProperties": updated_props,
            }
        except Exception as e:
            return {"error": f"Failed to update element: {e}"}

    # --- Information Retrieval Methods ---

    def get_diagram_information(self, diagramID):
        """
        Get detailed information about a diagram.
        *** FIXED to correctly retrieve connector information. ***
        """
        logging.info(f"Fetching diagram information for diagramID={diagramID}")
        try:
            diagram = self.repository.GetDiagramByID(diagramID)
            if not diagram:
                return {"error": "Diagram not found"}

            # Correctly process diagram links
            links_info = []
            for diagram_link in diagram.DiagramLinks:
                connector = self.repository.GetConnectorByID(diagram_link.ConnectorID)
                if connector:  # Ensure the connector exists
                    links_info.append(
                        {
                            "ConnectorID": connector.ConnectorID,
                            "Type": connector.Type,
                            "SourceID": connector.ClientID,
                            "TargetID": connector.SupplierID,
                        }
                    )

            info = {
                "Name": diagram.Name,
                "GUID": diagram.DiagramGUID,
                "Elements": [
                    {
                        "ElementID": obj.ElementID,
                        "Name": self.repository.GetElementByID(obj.ElementID).Name,
                    }
                    for obj in diagram.DiagramObjects
                ],
                "Links": links_info,
            }
            return info
        except Exception as e:
            logging.error(f"Failed to retrieve diagram info (id={diagramID}): {e}")
            return {"error": f"Failed to retrieve diagram information: {e}"}

    def get_root_packages(self):
        """Get all root packages (Models) in the repository."""
        logging.info("Listing root packages.")
        try:
            root_packages = [
                {
                    "name": pkg.Name,
                    "description": pkg.Notes or "",
                    "packageID": pkg.PackageID,
                    "parentPackageID": pkg.ParentID or 0,
                    "path": f"/{pkg.Name}",
                }
                for pkg in self.repository.Models
            ]
            return {"Root packages": root_packages}
        except Exception as e:
            return {"error": f"Failed to retrieve root packages: {e}"}

    def get_package_information(self, packageID):
        """Get basic information about a specific package."""
        logging.info(f"Getting package information for packageID={packageID}")
        try:
            package = self.repository.GetPackageByID(packageID)
            if not package:
                return {"error": "Package not found"}
            return {"Name": package.Name, "PackageID": package.PackageID}
        except Exception as e:
            return {"error": f"Failed to retrieve package information: {e}"}

    def get_diagram_image(self, diagramID):
        """Saves a diagram's image to a file and returns the file path."""
        logging.info(f"Exporting diagram image for diagramID={diagramID}")
        try:
            diagram = self.repository.GetDiagramByID(diagramID)
            if not diagram:
                return {"error": "Diagram not found"}
            file_path = f"C:\\temp\\{diagram.Name.replace(' ', '_')}_{int(time.time())}.png"
            project_interface = self.repository.GetProjectInterface()
            project_interface.PutDiagramImageToFile(diagram.DiagramGUID, file_path, 1)  # 1 for PNG
            return {"DiagramID": diagram.DiagramID, "ImageSavedAt": file_path}
        except Exception as e:
            return {"error": f"Failed to save diagram image: {e}"}

    def get_opened_diagrams(self):
        """Get a list of all diagrams currently open in the EA user interface."""
        logging.info("Retrieving list of currently opened diagrams.")
        try:
            diagrams_count = self.repository.GetDiagramCount()
            diagrams = [
                {
                    "DiagramID": self.repository.GetDiagramByPos(i).DiagramID,
                    "Name": self.repository.GetDiagramByPos(i).Name,
                }
                for i in range(diagrams_count)
            ]
            return diagrams
        except Exception as e:
            return {"error": f"Failed to retrieve opened diagrams: {e}"}

    def get_element_information(self, elementID):
        """Get detailed information about an element."""
        logging.info(f"Fetching element information for elementID={elementID}")
        try:
            element = self.repository.GetElementByID(elementID)
            if not element:
                return {"error": "Element not found"}
            info = {
                "Name": element.Name,
                "ElementID": element.ElementID,
                "GUID": element.ElementGUID,
                "Type": element.Type,
                "Stereotype": element.StereotypeEx,
                "Abstract": element.Abstract,
                "Notes": element.Notes,
                "Attributes": [
                    {"Name": attr.Name, "Type": attr.Type, "ID": attr.AttributeID} for attr in element.Attributes
                ],
                "Methods": [
                    {
                        "Name": method.Name,
                        "ReturnType": method.ReturnType,
                        "ID": method.MethodID,
                    }
                    for method in element.Methods
                ],
            }
            return info
        except Exception as e:
            return {"error": f"Failed to retrieve element information: {e}"}

    def get_current_element(self):
        """Get detailed information for the currently selected element in the EA UI."""
        logging.info("Getting currently selected element from EA UI context.")
        try:
            context = self.repository.GetContextObject()
            if context and context.ObjectType == 10:  # otElement
                return self.get_element_information(context.ElementID)
            return {"error": "No element currently selected"}
        except Exception as e:
            return {"error": f"Failed to retrieve current element: {e}"}

    def find_packages_by_name(self, name, exactMatch=False):
        """
        Find packages by their name using a direct SQL query.
        *** FIXED to correctly identify and return the found package. ***
        """
        logging.info(f"Searching for packages by name='{name}' (exactMatch={exactMatch})")
        try:
            safe_name = name.replace("'", "''")
            query = f"SELECT o.Object_ID FROM t_object o WHERE o.Object_Type = 'Package' AND o.Name {'=' if exactMatch else 'LIKE'} '{'' if exactMatch else '%'}{safe_name}{'' if exactMatch else '%'}'"
            xml_results = self.repository.SQLQuery(query)
            root = ET.fromstring(xml_results)
            results = []
            for row in root.findall(".//Row/Object_ID"):
                element = self.repository.GetElementByID(int(row.text))
                if element:
                    # A package-element's PackageID is its PARENT. To get the actual package, use its GUID.
                    package = self.repository.GetPackageByGuid(element.ElementGUID)
                    if package:
                        results.append({"PackageID": package.PackageID, "Name": package.Name})
            logging.info(f"Found {len(results)} matching packages for name '{name}'.")
            return results
        except Exception as e:
            logging.error(f"Failed to find packages by name '{name}': {e}")
            return {"error": f"Failed to find packages by name: {e}"}

    def get_current_package(self):
        """Get information for the currently selected package in the EA UI."""
        logging.info("Getting currently selected package from EA UI context.")
        try:
            context = self.repository.GetContextObject()
            if context and context.ObjectType == 5:  # otPackage
                return self.get_package_information(context.PackageID)
            return {"error": "No package currently selected"}
        except Exception as e:
            return {"error": f"Failed to get the current package: {e}"}

    def create_package(self, name, parentPackageID):
        """Create a new package under a specified parent package."""
        logging.info(f"Creating package '{name}' under parentPackageID={parentPackageID}")
        try:
            parent_package = self.repository.GetPackageByID(parentPackageID)
            if not parent_package:
                return {"error": "Cannot find specified parent package."}
            new_package = parent_package.Packages.AddNew(name, "")
            new_package.Update()
            parent_package.Packages.Refresh()
            return {"Success": f"Package '{name}' created with ID {new_package.PackageID}."}
        except Exception as e:
            return {"error": f"Failed to create package: {e}"}

    def place_element_on_diagram(self, elementID, diagramID):
        """Place an element onto a diagram.

        Args:
            elementID (int): ID of the element to place.
            diagramID (int): ID of the diagram where the element will be placed.

        Returns:
            dict: Success message or error message.
        """
        logging.info(f"Placing elementID={elementID} onto diagramID={diagramID}")
        try:
            element = self.repository.GetElementByID(elementID)
            diagram = self.repository.GetDiagramByID(diagramID)
            if not element or not diagram:
                return {"error": "Element or Diagram not found"}
            diagramObj = diagram.DiagramObjects.AddNew("", "")
            diagramObj.ElementID = element.ElementID
            diagramObj.Update()
            diagram.DiagramObjects.Refresh()
            return {"Success": f"Element '{element.Name}' added to diagram '{diagram.Name}'"}
        except Exception as e:
            return {"error": f"Failed to place element on diagram: {e}"}

    def create_connector(self, sourceID, targetID, connectorType):
        """Create a connector between two elements.

        Args:
            sourceID (int): ID of the source element.
            targetID (int): ID of the target element.
            connectorType (str): Type of the connector (e.g., Association, Dependency).

        Returns:
            dict: Connector details or error message.
        """
        logging.info(f"Creating connector type='{connectorType}' from sourceID={sourceID} to targetID={targetID}")
        try:
            source_element = self.repository.GetElementByID(sourceID)
            target_element = self.repository.GetElementByID(targetID)
            if not source_element or not target_element:
                return {"error": "Source or Target element not found"}
            connector = source_element.Connectors.AddNew("", connectorType)
            connector.SupplierID = target_element.ElementID
            connector.Update()
            source_element.Connectors.Refresh()
            return {
                "ConnectorID": connector.ConnectorID,
                "ConnectorGUID": connector.ConnectorGUID,
            }
        except Exception as e:
            return {"error": f"Failed to create connector: {e}"}

    def find_in_diagrams(self, elementID):
        """Find diagrams containing a specific element.

        Args:
            elementID (int): ID of the element to find in diagrams.

        Returns:
            list: List of diagrams containing the element or error message.
        """
        logging.info(f"Finding diagrams containing elementID={elementID}")
        try:
            query = f"SELECT Diagram_ID FROM t_diagramobjects WHERE Object_ID = {elementID}"
            xml_results = self.repository.SQLQuery(query)
            root = ET.fromstring(xml_results)
            results = []
            for row in root.findall(".//Row/Diagram_ID"):
                diag_id = int(row.text)
                diagram = self.repository.GetDiagramByID(diag_id)
                if diagram:
                    results.append({"DiagramID": diag_id, "Name": diagram.Name})
            return results
        except Exception as e:
            return {"error": f"Failed to find diagrams for element: {e}"}

    def select_element_in_diagram(self, elementID, diagramID):
        """Select an element in a diagram.

        Args:
            elementID (int): ID of the element to select.
            diagramID (int): ID of the diagram containing the element.

        Returns:
            dict: Success message or error message.
        """
        logging.info(f"Selecting elementID={elementID} within diagramID={diagramID}")
        try:
            diagram = self.repository.GetDiagramByID(diagramID)
            element = self.repository.GetElementByID(elementID)
            if not diagram or not element:
                return {"error": "Diagram or Element not found"}
            self.repository.OpenDiagram(diagramID)
            diagram_object_to_select = next(
                (obj for obj in diagram.DiagramObjects if obj.ElementID == elementID),
                None,
            )
            if diagram_object_to_select:
                diagram.SelectedObjects.AddNew(f"{diagram_object_to_select.ElementID}", "")
                self.repository.ReloadDiagram(diagramID)
                return {"success": f"Element '{element.Name}' selected in Diagram '{diagram.Name}'"}
            return {"error": "Element not found in the specified diagram"}
        except Exception as e:
            return {"error": f"Failed to select element in diagram: {e}"}

    def get_current_diagram(self):
        """Get detailed information for the currently active diagram in the EA UI."""
        logging.info("Retrieving current active diagram.")
        try:
            diagram = self.repository.GetCurrentDiagram()
            if not diagram:
                return {"error": "No diagram is currently active"}
            return self.get_diagram_information(diagram.DiagramID)  # This now calls the fixed method
        except Exception as e:
            return {"error": f"Failed to get the current diagram: {e}"}

    def create_diagram(self, name, typeStr, packageID):
        """Create a new diagram in a package.

        Args:
            name (str): Name of the new diagram.
            typeStr (str): Type of the diagram (e.g., UML, Flowchart).
            packageID (int): ID of the package where the diagram will be created.

        Returns:
            dict: Diagram details or error message.
        """
        logging.info(f"Creating diagram '{name}' of type '{typeStr}' in packageID={packageID}")
        try:
            package = self.repository.GetPackageByID(packageID)
            if not package:
                return {"error": "Package not found"}
            new_diagram = package.Diagrams.AddNew(name, typeStr)
            new_diagram.Update()
            package.Diagrams.Refresh()
            return {
                "DiagramID": new_diagram.DiagramID,
                "Name": new_diagram.Name,
                "GUID": new_diagram.DiagramGUID,
            }
        except Exception as e:
            return {"error": f"Failed to create diagram: {e}"}

    def open_diagram(self, diagramID):
        """Open a diagram in the EA UI.

        Args:
            diagramID (int): ID of the diagram to open.

        Returns:
            dict: Success message or error message.
        """
        logging.info(f"Opening diagramID={diagramID}")
        try:
            diagram = self.repository.GetDiagramByID(diagramID)
            if not diagram:
                return {"error": "Diagram not found"}
            self.repository.OpenDiagram(diagramID)
            return {"success": f"Diagram '{diagram.Name}' opened"}
        except Exception as e:
            return {"error": f"Failed to open diagram: {e}"}

    def set_element_property(self, elementID, propertyName, value):
        """Set a property of an element.

        Args:
            elementID (int): ID of the element.
            propertyName (str): Name of the property to set.
            value: New value for the property.

        Returns:
            dict: Success message or error message.
        """
        logging.info(f"Setting property '{propertyName}' on elementID={elementID} to value={value}")
        try:
            element = self.repository.GetElementByID(elementID)
            if not element:
                return {"error": "Element not found"}
            if hasattr(element, propertyName):
                setattr(element, propertyName, value)
                element.Update()
                return {"success": f"Property '{propertyName}' set for element '{element.Name}'"}
            return {"error": f"Invalid property name: '{propertyName}'"}
        except Exception as e:
            return {"error": f"Failed to set element property: {e}"}

    def layout_diagram(self, diagramID):
        """Apply auto-layout to a diagram.

        Args:
            diagramID (int): ID of the diagram to layout.

        Returns:
            dict: Success message or error message.
        """
        logging.info(f"Applying auto-layout to diagramID={diagramID}")
        try:
            project_interface = self.repository.GetProjectInterface()
            diagram = self.repository.GetDiagramByID(diagramID)
            if not diagram:
                return {"error": "Diagram not found"}
            project_interface.LayoutDiagramEx(diagram.DiagramGUID, 0, 4, 20, 20, True)
            self.repository.ReloadDiagram(diagramID)
            return {"success": f"Diagram '{diagram.Name}' layout updated"}
        except Exception as e:
            return {"error": f"Failed to layout diagram: {e}"}

    def query_repository(self, sql_query: str) -> list:
        """
        Executes a read-only SQL query and returns the result as a list of dicts.

        Args:
            sql_query (str): The SQL query string to execute.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a row.
                        Returns an error dictionary on failure.
        """
        logging.info(f"Executing SQL query: {sql_query}")

        # Security check: prevent destructive SQL operations
        if self._contains_destructive_sql(sql_query):
            raise PermissionError(
                "Destructive SQL operations (DELETE, DROP, TRUNCATE, ALTER) are restricted for safety. "
                "Should be done by the user manually."
            )

        try:
            xml_results = self.repository.SQLQuery(sql_query)
            root = ET.fromstring(xml_results)

            # The data is inside the first <Dataset_0><Data> block
            data_node = root.find(".//Data")
            if data_node is None:
                logging.info("Query returned no data.")
                return []

            results = []
            rows = data_node.findall("Row")
            for row in rows:
                row_data = {child.tag: child.text for child in row}
                results.append(row_data)

            logging.info(f"Query returned {len(results)} rows.")
            return results
        except Exception as e:
            logging.error(f"Failed to execute or parse SQL query '{sql_query}': {e}")
            return [{"error": f"Failed to execute SQL query: {e}"}]
