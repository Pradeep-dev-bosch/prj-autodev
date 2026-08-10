"""Enterprise Architect (.qea/.qeax) SQLite model reader.

Provides minimal high-level helpers for querying EA schema data plus a few write
primitives used by the MCP server. Opens databases read-only by default; callers
must reopen with read_only=False for mutations.
"""

import re
import sqlite3
import uuid
from pathlib import Path
from sqlite3 import Error
from typing import Optional


def _dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


class EaModelReader:
    def __init__(self, db_file, *, read_only: bool = True) -> None:
        """Initialize reader and validate EA SQLite database.

        Args:
            db_file: Path to EA .qea/.qeax SQLite file.
            read_only: When True uses URI mode=ro for a non-mutating connection.

        Raises:
            FileNotFoundError: If the database file does not exist.
            ValueError: If file is not a SQLite database or lacks required tables.
            RuntimeError: If connection cannot be opened.
        """
        if not Path(db_file).exists():
            raise FileNotFoundError(f"Model file not existing: {db_file}")
        with open(db_file, "rb") as f:
            if not f.read(15).startswith(b"SQLite format 3"):
                raise ValueError("Model file is not a valid SQLite database")
        self.create_connection(db_file, read_only=read_only)
        tables = self._query("SELECT name FROM sqlite_master where type like 'table'")
        if not tables:
            raise ValueError("Not all expected tables from EA schema found")
        names = {t["name"] for t in tables}
        required = {"t_package", "t_object", "t_xref"}
        if not required.issubset(names):
            raise ValueError("Not all expected tables from EA schema found")

    def create_connection(self, db_file, *, read_only=True) -> None:
        """Create underlying SQLite connection.

        Args:
            db_file: Path to EA model database.
            read_only: If True uses immutable read-only URI (mode=ro).

        Raises:
            RuntimeError: On failure to open database.
        """
        try:
            if read_only:
                self.conn = sqlite3.connect(f"file:{db_file}?mode=ro", uri=True, check_same_thread=False)
            else:
                self.conn = sqlite3.connect(str(db_file), check_same_thread=False)
            self.conn.row_factory = _dict_factory
            self.cur = self.conn.cursor()
        except Error as e:
            raise RuntimeError(f"Could not open database: {e}") from e

    def alive_check(self) -> bool:
        """Return True if the connection responds to a trivial query."""
        try:
            self._query("SELECT 1")
            return True
        except Exception:  # noqa: BLE001
            return False

    def _query(self, query: str, params: Optional[tuple] = None) -> list[dict]:
        """Execute a SQL query and return all rows.

        Internal helper; prefer public wrappers. Does not commit.

        Args:
            query: Raw SQL string.
            params: Optional tuple of bound parameters.

        Returns:
            List of row dicts.
        """
        res = self.cur.execute(query, params or ())
        return res.fetchall()

    def _insert(self, query: str) -> int:
        """Execute INSERT (or other write) returning last row id.

        Args:
            query: SQL write statement.

        Returns:
            The integer lastrowid produced by the cursor.
        """
        self.cur.execute(query)
        return self.cur.lastrowid

    # ========================================================================
    # READ OPERATIONS - PACKAGES
    # ========================================================================

    def get_packages(self, package_id: int | None = None, parent_id: int | None = None) -> list[dict]:
        """Return package metadata rows with optional filtering.

        ⚠️ SCHEMA: t_package has ONLY 5 columns: Package_ID, Name, Parent_ID, ea_guid, Version
        NO CreatedDate, ModifiedDate, Stereotype!

        Args:
            package_id: Filter by specific Package_ID (optional)
            parent_id: Filter by Parent_ID (optional)

        Returns:
            List of package dicts
        """
        # Query ONLY columns that actually exist in schema
        query = "SELECT Package_ID, Name, Parent_ID, ea_guid, Version FROM t_package"
        clauses = []
        params = []

        if package_id is not None:
            clauses.append("Package_ID=?")
            params.append(package_id)
        if parent_id is not None:
            clauses.append("Parent_ID=?")
            params.append(parent_id)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        return self._query(query, tuple(params))

    # ========================================================================
    # READ OPERATIONS - OBJECTS
    # ========================================================================

    def get_object(self, ea_guid: str) -> dict | None:
        """Return enriched object structure.

        Adds both ea_ID (historical) and Object_ID (alias) for downstream write helpers
        expecting raw schema keys. Also exposes numeric Classifier field for classifier
        resolution when no classifier_guid is present.

        Args:
            ea_guid: Braced GUID of EA object.

        Returns:
            Dict of enriched object fields or None if not found.
        """
        res = self._query(
            """SELECT o.Name,
                      o.Object_Type as 'Type',
                      o.Alias,
                      o.Author,
                      o.Version,
                      o.Note,
                      o.CreatedDate,
                      o.ModifiedDate,
                      o.Status,
                      o.Abstract,
                      o.ea_guid,
                      o.Object_ID as ea_ID,
                      o.Object_ID as Object_ID,
                      o.Package_ID,
                      o.ParentID,
                      o.Classifier as Classifier_ID,
                      o.Classifier_guid,
                      o.PDATA1,
                      o.PDATA3,
                      o.Stereotype as stereotype_legacy,
                      (SELECT x.Description FROM t_xref x WHERE x.Name = 'Stereotypes' AND x.Client = o.ea_guid) as stereotype_desc,
                      EXISTS (SELECT 1 FROM t_diagramobjects d WHERE d.object_id = o.object_id) as has_dia_link
               FROM t_object o WHERE o.ea_guid = ?""",
            (ea_guid,),
        )
        if not res:
            return None
        row = res[0]
        row["has_dia_link"] = bool(row["has_dia_link"])
        desc = row.pop("stereotype_desc")
        legacy = row.pop("stereotype_legacy")
        if desc:
            stereos = re.findall(r"@STEREO;Name=([^;]+);(?:GUID|FQName)=[^;]+;@ENDSTEREO", desc)
            row["Stereotypes"] = set(stereos) if stereos else set()
        else:
            row["Stereotypes"] = {legacy} if legacy else set()
        return row

    def get_objects(self, package_id: int | None = None, parent_id: int | None = None) -> list[dict]:
        """Return enriched objects filtered by package_id and/or parent_id.

        Args:
            package_id: Package_ID constraint (optional).
            parent_id: ParentID constraint (optional).

        Returns:
            List of object dicts.
        """
        base = "SELECT ea_guid FROM t_object"
        clauses = []
        params = []
        if package_id is not None:
            clauses.append("Package_id=?")
            params.append(package_id)
        if parent_id is not None:
            clauses.append("parentID=?")
            params.append(max(parent_id, 0))
        if clauses:
            base += " WHERE " + " AND ".join(clauses)
        guids = self._query(base, tuple(params))
        return [o for o in (self.get_object(g["ea_guid"]) for g in guids) if o]

    # ========================================================================
    # READ OPERATIONS - CONNECTORS
    # ========================================================================

    def get_connectors(
        self, source_guid: str | None = None, target_guid: str | None = None, connector_type: str | None = None
    ) -> list[dict]:
        """Retrieve connectors with optional filtering.

        Args:
            source_guid: Source object GUID (optional) to filter Start_Object_ID.
            target_guid: Target object GUID (optional) to filter End_Object_ID.
            connector_type: Connector_Type to filter (optional).

        Returns:
            List of connector row dicts.
        """
        base = """SELECT Name, Connector_Type, Direction, Subtype, SeqNo, 
                         Connector_ID as ea_ID, ea_guid, Start_Object_ID, End_Object_ID, 
                         Stereotype, DiagramID 
                  FROM t_connector"""

        clauses = []
        params = []

        if source_guid:
            clauses.append("Start_Object_ID IN (SELECT Object_ID FROM t_object WHERE ea_guid=?)")
            params.append(source_guid)
        if target_guid:
            clauses.append("End_Object_ID IN (SELECT Object_ID FROM t_object WHERE ea_guid=?)")
            params.append(target_guid)
        if connector_type:
            clauses.append("Connector_Type=?")
            params.append(connector_type)

        if clauses:
            base += " WHERE " + " AND ".join(clauses)

        return self._query(base, tuple(params))

    # ========================================================================
    # READ OPERATIONS - ATTRIBUTES
    # ========================================================================

    def get_attributes(self, object_guid: str) -> list[dict]:
        """Return attributes for an object.

        Args:
            object_guid: GUID of parent object

        Returns:
            List of attribute dicts
        """
        # Get Object_ID first
        obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
        obj_result = self._query(obj_query, (object_guid,))
        if not obj_result:
            return []

        object_id = obj_result[0]["Object_ID"]

        # ⚠️ Note: 'Default' column is quoted in schema, must use "Default" to avoid syntax errors
        query = """SELECT ID, Name, Type, Scope, Stereotype, "Default", LowerBound, UpperBound, 
                          Notes, ea_guid, Object_ID
                   FROM t_attribute 
                   WHERE Object_ID=?
                   ORDER BY Pos"""
        return self._query(query, (object_id,))

    # ========================================================================
    # READ OPERATIONS - OPERATIONS
    # ========================================================================

    def get_operations(self, object_guid: str) -> list[dict]:
        """Return operations/methods for an object.

        Args:
            object_guid: GUID of parent object

        Returns:
            List of operation dicts
        """
        # Get Object_ID first
        obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
        obj_result = self._query(obj_query, (object_guid,))
        if not obj_result:
            return []

        object_id = obj_result[0]["Object_ID"]

        query = """SELECT OperationID, Name, Type, Scope, Stereotype, ReturnArray, 
                          Notes, ea_guid, Object_ID, Abstract, Concurrency
                   FROM t_operation 
                   WHERE Object_ID=?
                   ORDER BY Pos"""
        return self._query(query, (object_id,))

    # ========================================================================
    # READ OPERATIONS - TAGGED VALUES
    # ========================================================================

    def get_tagged_value(self, component: dict, tag_name: str) -> str | None:
        """Return tagged value string for given component and tag name.

        Args:
            component: Enriched object dict.
            tag_name: Tagged value property name.

        Returns:
            String value or None if missing.
        """
        oid = component.get("Object_ID") or component.get("ea_ID")
        res = self._query("SELECT Value FROM t_objectproperties WHERE Object_ID=? AND Property LIKE ?", (oid, tag_name))
        return res[0]["Value"] if res else None

    def get_tagged_values(self, object_guid: str) -> list[dict]:
        """Return all tagged values for an object.

        Args:
            object_guid: GUID of object

        Returns:
            List of tagged value dicts with Property, Value, Notes, ea_guid
        """
        # Get Object_ID first
        obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
        obj_result = self._query(obj_query, (object_guid,))
        if not obj_result:
            return []

        object_id = obj_result[0]["Object_ID"]

        query = """SELECT PropertyID, Property, Value, Notes, ea_guid, Object_ID
                   FROM t_objectproperties 
                   WHERE Object_ID=?"""
        return self._query(query, (object_id,))

    # ========================================================================
    # READ OPERATIONS - DIAGRAMS
    # ========================================================================

    def get_diagrams(self, package_id: int | None = None) -> list[dict]:
        """Return diagrams with optional package filter.

        ⚠️ SCHEMA: Column is ea_guid, NOT DiagramGUID!

        Args:
            package_id: Filter by Package_ID (optional)

        Returns:
            List of diagram dicts
        """
        # Use ea_guid (actual column name from schema diagram)
        query = """SELECT Diagram_ID, Name, Diagram_Type, Package_ID, ParentID, 
                          ea_guid, Version, Author, ShowDetails, Notes, 
                          Stereotype, CreatedDate, ModifiedDate
                   FROM t_diagram"""

        if package_id is not None:
            query += " WHERE Package_ID=?"
            return self._query(query, (package_id,))

        return self._query(query)

    # ========================================================================
    # READ OPERATIONS - CLASSIFIER & RELATIONSHIPS
    # ========================================================================

    def get_classifier(self, component: dict) -> dict | None:
        """Resolve classifier across multiple EA storage patterns.

        Ports/Parts may use PDATA1, general elements may use classifier_guid or numeric Classifier field.

        Args:
            component: Enriched object dict whose classifier is requested.

        Returns:
            Enriched classifier object dict or None.
        """
        # Ports / Parts typed by PDATA1 (GUID stored there)
        if component["Type"] in ["Part", "Port"]:
            res = self._query("SELECT PDATA1 FROM t_object WHERE ea_guid=?", (component["ea_guid"],))
            if res and res[0]["PDATA1"]:
                return self.get_object(res[0]["PDATA1"])
        # Classifier GUID path
        if component.get("Classifier_guid"):
            return self.get_object(component["Classifier_guid"])
        # Numeric classifier ID path
        res2 = self._query("SELECT Classifier FROM t_object WHERE ea_guid=?", (component["ea_guid"],))
        if res2:
            cid = res2[0]["Classifier"]
            if cid and cid > 0:
                guid_row = self._query("SELECT ea_guid FROM t_object WHERE Object_ID=?", (cid,))
                if guid_row:
                    return self.get_object(guid_row[0]["ea_guid"])
        return None

    def get_parent_object(self, element: dict) -> dict | None:
        """Return parent element or owning package if parentID=0.

        Args:
            element: Enriched object dict.

        Returns:
            Parent object dict or package dict, or None.
        """
        res = self._query("SELECT ParentID FROM t_object WHERE ea_guid=?", (element["ea_guid"],))
        if res:
            parent_id = res[0]["ParentID"]
            if parent_id == 0:
                return self.get_owning_package(element)
            res2 = self._query("SELECT ea_guid FROM t_object WHERE Object_ID=?", (parent_id,))
            if res2:
                return self.get_object(res2[0]["ea_guid"])
        return None

    def get_owning_package(self, element: dict) -> dict | None:
        """Return package object (enriched) that owns the element.

        Args:
            element: Enriched object dict.

        Returns:
            Package object dict or None.
        """
        res = self._query("SELECT Package_ID FROM t_object WHERE ea_guid=?", (element["ea_guid"],))
        if res:
            res2 = self._query("SELECT ea_guid FROM t_package WHERE Package_ID=?", (res[0]["Package_ID"],))
            if res2:
                return self.get_object(res2[0]["ea_guid"])
        return None

    def get_children(self, parent: dict) -> list[dict]:
        """Return logical children (excluding Boundary wrappers which are traversed).

        Args:
            parent: Enriched parent object dict.

        Returns:
            List of child object dicts.
        """
        objects = self.get_objects(parent["Package_ID"], parent["ea_ID"])
        ret = []
        for o in objects:
            if o["Type"] == "Boundary":
                ret.extend(self.get_children(o))
            else:
                ret.append(o)
        return ret

    def get_connector_source(self, connector: dict) -> dict | None:
        """Return enriched source object for a connector row dict.

        Args:
            connector: Connector row dict containing Start_Object_ID.

        Returns:
            Enriched source object dict or None.
        """
        res = self._query("SELECT ea_guid FROM t_object WHERE Object_ID=?", (connector["Start_Object_ID"],))
        return self.get_object(res[0]["ea_guid"]) if res else None

    def get_classified_elements(self, classifier: dict) -> list[dict]:
        """Return elements typed by given classifier.

        Covers three patterns:
        - PDATA1 references classifier GUID (ports/parts)
        - classifier_guid column references GUID
        - numeric Classifier column references object id

        Args:
            classifier: Enriched classifier object dict.

        Returns:
            List of enriched object dicts typed by classifier.
        """
        guids = set()
        # PDATA1 GUID references
        for r in self._query("SELECT ea_guid FROM t_object WHERE PDATA1=?", (classifier["ea_guid"],)):
            guids.add(r["ea_guid"])
        # classifier_guid column
        for r in self._query("SELECT ea_guid FROM t_object WHERE classifier_guid=?", (classifier["ea_guid"],)):
            guids.add(r["ea_guid"])
        # numeric classifier id
        for r in self._query(
            "SELECT ea_guid FROM t_object WHERE Classifier=?", (classifier.get("ea_ID") or classifier.get("Object_ID"),)
        ):
            guids.add(r["ea_guid"])
        return [self.get_object(g) for g in guids]

    def is_conjugated(self, port: dict) -> bool:
        """Return True if a Port element is marked conjugated via custom properties.

        Args:
            port: Enriched port object dict.

        Returns:
            Boolean indicating conjugation.
        """
        if port["Type"] == "Port":
            res = self._query(
                "SELECT Description FROM t_xref WHERE Client LIKE ? AND Name LIKE 'CustomProperties' AND Type LIKE 'element property'",
                (port["ea_guid"],),
            )
            for row in res:
                m = re.search(
                    r"@NAME=isConjugated@ENDNAME;@TYPE=Boolean@ENDTYPE;@VALU=(-?\d+)@ENDVALU;", row["Description"]
                )
                if m and m.group(1) != "0":
                    return True
        return False

    # ========================================================================
    # READ OPERATIONS - PACKAGE PATH HELPERS
    # ========================================================================

    def get_or_create_package_path(self, package_path: str, root_package_id: int = 0) -> dict:
        """Return deepest package in path, creating intermediate ones if missing.

        Args:
            package_path: Slash or backslash separated path (e.g. "Root/Sub").
            root_package_id: Starting parent Package_ID (default 0 for model root).

        Returns:
            Dict row of final package.
        """
        parts = package_path.replace("\\", "/").split("/")
        cur_parent = root_package_id
        found = None
        for i, part in enumerate(parts):
            res = self._query("SELECT * FROM t_package WHERE Parent_ID=? AND Name LIKE ?", (cur_parent, part))
            if not res:
                found = self._add_package(part, cur_parent)
            else:
                found = res[0]
            cur_parent = found["Package_ID"]
        return found

    def get_package_for_path(self, package_path: str, root_package_id: int = 0) -> dict | None:
        """Resolve existing package path without creating.

        Args:
            package_path: Hierarchical path string.
            root_package_id: Starting parent Package_ID (default 0).

        Returns:
            Package dict or None if any segment missing.
        """
        parts = package_path.replace("\\", "/").split("/")
        cur_parent = root_package_id
        found = None
        for part in parts:
            res = self._query("SELECT * FROM t_package WHERE Parent_ID=? AND Name LIKE ?", (cur_parent, part))
            if not res:
                return None
            found = res[0]
            cur_parent = found["Package_ID"]
        return found

    def get_element(self, package: dict, name: str) -> dict | None:
        """Return raw object row for element name within package.

        Args:
            package: Package dict containing Package_ID.
            name: Element name to locate.

        Returns:
            Raw t_object row dict or None.
        """
        res = self._query("SELECT * FROM t_object WHERE Package_ID=? AND Name=?", (package["Package_ID"], name))
        return res[0] if res else None

    def get_element_for_path(self, element_path: str) -> dict | None:
        """Return enriched element for a full path (packages + element name).

        Args:
            element_path: e.g. "Root/Subsystem/Element".

        Returns:
            Enriched object dict or None.
        """
        parts = element_path.replace("\\", "/").split("/")
        package_path = "/".join(parts[:-1])
        name = parts[-1]
        pck = self.get_package_for_path(package_path)
        if not pck:
            return None
        elem = self.get_element(pck, name)
        return self.get_object(elem["ea_guid"]) if elem else None

    def get_elements_in_package(self, package: dict) -> list[dict]:
        """Return enriched objects contained directly within a package.

        Args:
            package: Package dict.

        Returns:
            List of object dicts.
        """
        return self.get_objects(package["Package_ID"])

    # ========================================================================
    # WRITE OPERATIONS - TAGGED VALUES (Additional Methods for Server)
    # ========================================================================

    def update_tagged_value(self, object_guid: str, tag_name: str, new_value: str) -> dict:
        """Update an existing tagged value or create if it doesn't exist.

        Args:
            object_guid: Object GUID
            tag_name: Name of the tagged value property
            new_value: New value to set

        Returns:
            dict with operation result
        """
        # Get Object_ID first
        obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
        obj_result = self._query(obj_query, (object_guid,))
        if not obj_result:
            raise ValueError(f"Object not found: {object_guid}")

        object_id = obj_result[0]["Object_ID"]

        # Check if tagged value exists
        res = self._query(
            "SELECT PropertyID FROM t_objectproperties WHERE Object_ID=? AND Property=?", (object_id, tag_name)
        )

        if res:
            # Update existing
            self.cur.execute(
                "UPDATE t_objectproperties SET Value=? WHERE PropertyID=?", (new_value, res[0]["PropertyID"])
            )
            return {
                "status": "updated",
                "PropertyID": res[0]["PropertyID"],
                "Property": tag_name,
                "Value": new_value,
                "Object_ID": object_id,
            }
        else:
            # Create new
            return self.add_tagged_value(object_guid, tag_name, new_value)

    def add_tagged_value(self, object_guid: str, tag_name: str, tag_value: str) -> dict:
        """Add a new tagged value to an object.

        Args:
            object_guid: Object GUID
            tag_name: Name of the tagged value property
            tag_value: Value to set

        Returns:
            dict with operation result
        """
        # Get Object_ID first
        obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
        obj_result = self._query(obj_query, (object_guid,))
        if not obj_result:
            raise ValueError(f"Object not found: {object_guid}")

        object_id = obj_result[0]["Object_ID"]

        # Generate GUID for the tagged value
        tv_guid = f"{{{str(uuid.uuid4()).upper()}}}"

        # Insert new tagged value
        self.cur.execute(
            "INSERT INTO t_objectproperties (Object_ID, Property, Value, ea_guid) VALUES (?, ?, ?, ?)",
            (object_id, tag_name, tag_value, tv_guid),
        )
        property_id = self.cur.lastrowid

        return {
            "status": "created",
            "PropertyID": property_id,
            "ea_guid": tv_guid,
            "Property": tag_name,
            "Value": tag_value,
            "Object_ID": object_id,
        }

    # ========================================================================
    # COMPATIBILITY METHODS (Maintain backward compatibility)
    # ========================================================================

    def set_tagged_value(self, component: dict, tag_name: str, tag_value: str) -> None:
        """Create or update a tagged value on an element (legacy method).

        Args:
            component: Enriched object dict.
            tag_name: Property name.
            tag_value: Value to set.

        Raises:
            ValueError: If component lacks object id fields.
        """
        element_guid = component.get("ea_guid")
        if not element_guid:
            raise ValueError("Component lacks ea_guid for tagging")

        self.update_tagged_value(element_guid, tag_name, tag_value)

    # ========================================================================
    # WRITE OPERATIONS - PACKAGES
    # ========================================================================

    def _add_package(self, package_name: str, parent_package_id: int) -> dict:
        """Insert a package record (and mirrored t_object entry).

        Args:
            package_name: Name for new package.
            parent_package_id: Parent_ID of owning package (0 for root).

        Returns:
            Enriched object row representing the package t_object entry.
        """
        # Generate EA-style GUID with braces and uppercase
        package_guid = f"{{{str(uuid.uuid4()).upper()}}}"

        # Insert into t_package - ONLY columns from schema diagram
        self.cur.execute(
            "INSERT INTO t_package (Parent_ID, ea_guid, Name, Version) VALUES (?, ?, ?, '1.0')",
            (parent_package_id, package_guid, package_name),
        )
        package_id = self.cur.lastrowid

        # Insert corresponding t_object entry
        self.cur.execute(
            "INSERT INTO t_object (Object_Type, Name, Stereotype, Package_ID, Classifier, ea_guid, ParentID) VALUES ('Package', ?, NULL, ?, 0, ?, 0)",
            (package_name, package_id, package_guid),
        )

        return self._query("SELECT * FROM t_object WHERE Package_ID=? AND Object_Type='Package'", (package_id,))[0]

    # ========================================================================
    # WRITE OPERATIONS - ELEMENTS
    # ========================================================================

    def _set_stereo_type(self, element_guid: str, stereotype: str) -> None:
        """Persist stereotype cross-reference row for an element.

        Args:
            element_guid: GUID of element being stereotyped.
            stereotype: Fully qualified stereotype string (may include namespace ::).
        """
        name_part = stereotype.split("::")[-1]
        xref_guid = str(uuid.uuid4())
        self.cur.execute(
            "INSERT INTO t_xref (XrefID, Name, Type, Visibility, Description, Client, Supplier) VALUES (?, 'Stereotypes', 'element property', 'Public', ?, ?, '<none>')",
            (
                xref_guid,
                f"@STEREO;Name={name_part};FQName={stereotype};@ENDSTEREO;",
                element_guid,
            ),
        )

    def _add_element(
        self,
        element_type: str,
        element_name: str,
        parent_package_id: int,
        *,
        parent_id: int = 0,
        classfier_id: int = 0,
        classifier_guid: str | None = None,
        stereotype: str | None = None,
        note: str | None = None,
    ) -> dict:
        """Insert a new element into t_object (optionally with stereotype and classifier).

        Args:
            element_type: EA Object_Type (e.g. 'Class').
            element_name: Name of element.
            parent_package_id: Owning Package_ID.
            parent_id: Parent object ID (0 if none).
            classfier_id: Numeric classifier Object_ID (legacy path).
            classifier_guid: GUID of classifier element.
            stereotype: Fully qualified stereotype string.
            note: Optional note text.

        Returns:
            Raw t_object row dict for created element.
        """
        element_guid = f"{{{str(uuid.uuid4()).upper()}}}"

        # Normalize classifier GUID if provided
        if classifier_guid and not classifier_guid.startswith("{"):
            classifier_guid = f"{{{classifier_guid.strip('{}').upper()}}}"

        # Use parameterized query for safety
        self.cur.execute(
            """INSERT INTO t_object (Object_Type, ea_guid, Name, Stereotype, Package_ID, ParentID, Classifier, Classifier_guid, Note)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                element_type,
                element_guid,
                element_name,
                stereotype.split("::")[-1] if stereotype else None,
                parent_package_id,
                parent_id,
                classfier_id,
                classifier_guid,
                note,
            ),
        )
        element_id = self.cur.lastrowid

        if stereotype:
            self._set_stereo_type(element_guid, stereotype)

        return self._query("SELECT * FROM t_object WHERE Object_ID=?", (element_id,))[0]

    # ========================================================================
    # WRITE OPERATIONS - CONNECTORS
    # ========================================================================

    def _add_connection(
        self,
        source: dict,
        target: dict,
        connection_type: str,
        *,
        subtype: str | None = None,
        stereotype: str | None = None,
    ) -> dict:
        """Create connector row linking source and target objects.

        Args:
            source: Source object dict (must include Object_ID or ea_ID).
            target: Target object dict.
            connection_type: EA Connector_Type string.
            subtype: Optional SubType value.
            stereotype: Optional stereotype string.

        Returns:
            Connector row dict.
        """
        element_guid = f"{{{str(uuid.uuid4()).upper()}}}"

        # Allow enriched objects (ea_ID) fallback
        def _oid(o):
            return o.get("Object_ID") or o.get("ea_ID")

        s_id = _oid(source)
        t_id = _oid(target)
        if s_id is None or t_id is None:
            raise ValueError("Source or target object missing Object_ID/ea_ID")

        self.cur.execute(
            """INSERT INTO t_connector (Direction, Connector_Type, SubType, LineColor, SourceAccess, DestAccess, 
                                        SourceIsNavigable, DestIsNavigable, Start_Object_ID, End_Object_ID, 
                                        RouteStyle, ea_guid, Stereotype)
               VALUES ('Source -> Destination', ?, ?, -1, 'Public', 'Public', 0, 1, ?, ?, 3, ?, ?)""",
            (connection_type, subtype, s_id, t_id, element_guid, stereotype),
        )
        new_id = self.cur.lastrowid

        return self._query(
            "SELECT Connector_ID, ea_guid, Connector_Type, Start_Object_ID, End_Object_ID, Direction, SubType, Stereotype FROM t_connector WHERE Connector_ID=?",
            (new_id,),
        )[0]

    # ========================================================================
    # PUBLIC WRITE WRAPPERS
    # ========================================================================

    def create_package(self, name: str, parent_package_id: int) -> dict:
        """Public wrapper to create a package via _add_package.

        Args:
            name: New package name.
            parent_package_id: Parent_ID of owning package.

        Returns:
            Enriched object row for package.
        """
        return self._add_package(name, parent_package_id)

    def create_element(
        self,
        name: str,
        type_str: str,
        package_id: int,
        *,
        parent_id: int = 0,
        classifier_guid: str | None = None,
        classifier_id: int = 0,
        stereotype: str | None = None,
        note: str | None = None,
    ) -> dict:
        """Create an element with optional classifier/stereotype/note.

        Args:
            name: Element name.
            type_str: EA Object_Type.
            package_id: Owning Package_ID.
            parent_id: Parent object ID.
            classifier_guid: GUID of classifier.
            classifier_id: Numeric classifier Object_ID (legacy path).
            stereotype: Stereotype string.
            note: Optional note text.

        Returns:
            Raw created element row dict.
        """
        return self._add_element(
            type_str,
            name,
            package_id,
            parent_id=parent_id,
            classfier_id=classifier_id,
            classifier_guid=classifier_guid,
            stereotype=stereotype,
            note=note,
        )

    def create_connector(
        self,
        source_obj: dict,
        target_obj: dict,
        connector_type: str,
        *,
        subtype: str | None = None,
        stereotype: str | None = None,
    ) -> dict:
        """Create connector between two objects.

        Args:
            source_obj: Source object dict.
            target_obj: Target object dict.
            connector_type: EA connector type string.
            subtype: Optional subtype string.
            stereotype: Optional stereotype string.

        Returns:
            Connector row dict.
        """
        return self._add_connection(source_obj, target_obj, connector_type, subtype=subtype, stereotype=stereotype)

    # ========================================================================
    # WRITE OPERATIONS - DIAGRAMS
    # ========================================================================

    def create_diagram(self, name: str, package_id: int, diagram_type: str = "Component") -> dict:
        """Create a new diagram row with minimal fields.

        Args:
            name: Diagram name.
            package_id: Owning package Package_ID.
            diagram_type: EA Diagram_Type string (default 'Component').

        Returns:
            Diagram row dict.
        """
        dia_guid = f"{{{str(uuid.uuid4()).upper()}}}"

        # Use ea_guid column name, not DiagramGUID
        self.cur.execute(
            """INSERT INTO t_diagram (Name, Package_ID, ParentID, Diagram_Type, Version, ea_guid, 
                                      Author, ShowDetails, CreatedDate, ModifiedDate)
               VALUES (?, ?, 0, ?, '1.0', ?, '', 0, datetime('now'), datetime('now'))""",
            (name, package_id, diagram_type, dia_guid),
        )
        dia_id = self.cur.lastrowid

        return self._query(
            "SELECT Diagram_ID, Name, Diagram_Type, Package_ID, ea_guid FROM t_diagram WHERE Diagram_ID=?", (dia_id,)
        )[0]

    def add_diagram_object(
        self, diagram_id: int, obj: dict, left: int, top: int, width: int = 120, height: int = 60
    ) -> dict:
        """Place an object on a diagram with rectangle geometry.

        Args:
            diagram_id: Target Diagram_ID.
            obj: Enriched object dict.
            left: Left X coordinate.
            top: Top Y coordinate.
            width: Width of shape (default 120).
            height: Height of shape (default 60).

        Returns:
            Dict describing placement result.
        """
        oid = obj.get("Object_ID") or obj.get("ea_ID")
        if oid is None:
            raise ValueError("Object missing Object_ID/ea_ID for diagram placement")

        right = left + width
        bottom = top + height

        self.cur.execute(
            "INSERT INTO t_diagramobjects (Object_ID, Diagram_ID, RectTop, RectLeft, RectRight, RectBottom, Sequence, ObjectStyle) VALUES (?, ?, ?, ?, ?, ?, 0, '')",
            (oid, diagram_id, top, left, right, bottom),
        )

        return {"placed": True, "object_id": oid, "diagram_id": diagram_id, "coords": (left, top, right, bottom)}

    def add_diagram_connector(self, diagram_id: int, connector_row: dict) -> dict:
        """Display an existing connector on a diagram (diagram link).

        Args:
            diagram_id: Target Diagram_ID
            connector_row: Connector dict containing Connector_ID

        Returns:
            Dict describing link result
        """
        cid = connector_row.get("Connector_ID") or connector_row.get("ea_ID")
        if cid is None:
            raise ValueError("Connector row missing Connector_ID")

        # Minimal geometry stub
        self.cur.execute(
            "INSERT INTO t_diagramlinks (ConnectorID, DiagramID, Geometry, Style, Hidden, Path) VALUES (?, ?, '', '', 0, '')",
            (cid, diagram_id),
        )

        return {"linked": True, "connector_id": cid, "diagram_id": diagram_id}

    # ========================================================================
    # TRANSACTION MANAGEMENT
    # ========================================================================

    def commit(self) -> None:
        """Commit pending write operations to disk."""
        if self.conn:
            self.conn.commit()

    def __del__(self) -> None:
        """Best-effort connection close on garbage collection."""
        try:
            if hasattr(self, "conn") and self.conn:
                self.conn.close()
        except Exception:
            pass
