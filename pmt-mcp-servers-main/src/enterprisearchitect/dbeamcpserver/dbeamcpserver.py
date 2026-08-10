"""
Enterprise Architect MCP Server (DB-EA)
Exposes EA SQLite model read/query capabilities as MCP tools with pagination & safety features.
Includes creation tools for packages, objects, diagrams, connectors, attributes, and operations.
Environment: Absolute path to EA .qea/.qeax database file
"""

import logging
import os
import re
import uuid
from pathlib import Path
from typing import Optional

from dbeamodelreader import EaModelReader
from fastmcp import FastMCP

# ============================================================================
# INITIALIZATION
# ============================================================================

mcp = FastMCP("db-ea-mcp-server")
logging.info("EA DB MCP server initializing...")

_READER: Optional[EaModelReader] = None
_MODEL_PATH: Optional[str] = None
_READ_ONLY: bool = True


# ============================================================================
# UTILITY HELPERS
# ============================================================================


def _get_mcp_init_vars() -> tuple[str, str, int]:
    """Get MCP initialization variables from environment configuration.
    Returns:
        tuple[str, str, int]: A tuple containing:
            - transport_type (str): Transport protocol type, defaults to "stdio"
            - host (str): Server host address, defaults to "127.0.0.1"
            - port (int): Server port number, defaults to "8000"
    """
    transport = os.getenv("TRANSPORT") or "stdio"
    if transport in ["stdio", "<TRANSPORT>", None, "", "-", "null"]:
        logging.info("MCP init: transport=stdio")
        return ("stdio", "", 0)

    host = os.getenv("HOST") or "127.0.0.1"
    port_str = os.getenv("HOST_PORT") or "8000"
    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"Invalid PORT env variable: '{port_str}' - must be a valid integer")
    logging.info(f"MCP init: transport={transport}, host={host}, port={port}")
    return (transport, host, port)


def _ensure_reader() -> EaModelReader:
    """Ensure reader is initialized, raise error if not."""
    if _READER is None:
        logging.error("Reader access attempted before model open.")
        raise RuntimeError("Model not opened. Call open_model first.")
    return _READER


def _normalize_guid(g: str) -> str:
    """Normalize GUID to {UPPERCASE} format."""
    g = g.strip()
    if not g:
        return g
    if g.startswith("{") and g.endswith("}"):
        return g.upper()
    # Uppercase and brace
    core = g.strip("{} ").upper()
    return f"{{{core}}}"


def _guard_write():
    """Guard against write operations in read-only mode."""
    if _READ_ONLY:
        logging.error("Write operation attempted in read-only mode.")
        raise PermissionError("Model opened in read-only mode; reopen with read_only=False for write operations.")


def _clean_sql(query: str) -> str:
    """Clean SQL query by removing comments and normalizing whitespace."""
    # remove -- comments
    q = re.sub(r"--.*?(\n|$)", "", query)
    # remove /* */ comments
    q = re.sub(r"/\*.*?\*/", "", query, flags=re.DOTALL)
    # collapse spaces
    return " ".join(q.split()).lower()


def _contains_destructive_sql(query: str) -> bool:
    """Check if SQL query contains destructive statements that can modify or delete data.

    Blocks: DELETE, DROP, TRUNCATE, ALTER (can drop columns/tables)
    Allows: INSERT, UPDATE (handled by read-only mode check separately)

    Matches at the start of statement or after semicolon to avoid
    false positives from string literals or WHERE clauses.
    """
    q = _clean_sql(query)
    # Match destructive keywords at start of statement or after semicolon
    destructive_keywords = r"(delete|drop|truncate|alter)"
    return bool(re.search(rf"(^|;)\s*{destructive_keywords}\b", q))


# ============================================================================
# RESOURCES
# ============================================================================


@mcp.resource("dbea://usage-guide")
def get_usage_guide() -> str:
    """Return best practices for querying EA models efficiently."""
    return """
# EA Model Query Best Practices

## ⚠️ ALWAYS Follow This Pattern for Large Queries:

### 1. CHECK SIZE FIRST
- Use COUNT(*) queries before fetching data

### 2. USE PAGINATION
- Default limits are small (100 rows for get_objects)
- Use limit/offset parameters for iteration
- Process in chunks, don't fetch everything at once
- Check 'has_more' field to know if more pages exist

### 3. BE SPECIFIC
- Use search_objects() with filters instead of get_objects()
- Filter by package_id, object_type, stereotype
- Use name patterns (SQL LIKE syntax) to narrow results
- Combine multiple filters for precision

### 4. SAFE CUSTOM QUERIES
- Always use COUNT(*) first to check result size
- Add LIMIT clauses to prevent huge result sets
- Max auto-limit is 5000 rows, but prefer 500 or less
- Use WHERE clauses to filter data at the database level

## ❌ BAD PRACTICES (Will Cause Hangs):

```python
# DON'T: Fetch all objects without checking size
all_objects = get_objects()  # Could return 10,000+ rows!

# DON'T: Run SELECT * without LIMIT on large tables
custom_query("SELECT * FROM t_object")  # Disaster!
```

## ✅ GOOD PRACTICES (Efficient & Safe):

```python
# Example 1: Check size first, then paginate
summary = count(*)

if summary['total_objects'] > 100:
    page1 = get_objects(limit=100, offset=0)
    if page1['has_more']:
        page2 = get_objects(limit=100, offset=page1['next_offset'])

# Example 2: Use search with filters
controllers = search_objects(
    name_pattern='%Controller%',
    object_type='Class',
    limit=50
)

# Example 3: Safe custom queries
count_result = custom_query("SELECT COUNT(*) as total FROM t_object WHERE Object_Type='Class'")
total = count_result['data'][0]['total']

if total < 500:
    classes = custom_query("SELECT * FROM t_object WHERE Object_Type='Class' LIMIT 500")
```

## 📊 QUERY SIZE GUIDELINES

| Result Count | Action |
|--------------|--------|
| < 100 | Safe to fetch directly |
| 100-500 | Use pagination or filters |
| 500-1000 | Must paginate, check has_more |
| > 1000 | Use search_objects with strong filters |
| > 5000 | Break into multiple filtered queries |

## 🎯 TOOL SELECTION GUIDE

| Goal | Use This Tool |
|------|---------------|
| Browse model structure | get_object_summary() |
| Find specific items | search_objects() |
| Get all in package (small) | get_objects(package_id=X, limit=100) |
| Get all in package (large) | Loop with pagination |
| Complex queries | custom_query() with COUNT first |
| Single item details | get_object(ea_guid) |

## 🛡️ SAFETY FEATURES

- ✅ Auto-LIMIT applied to queries without LIMIT clause (max 5000)
- ✅ Warning when result approaches limit (>90% of max_rows)
- ✅ Pagination metadata (has_more, total_count) included
- ✅ Hard caps on limit parameters (1000 for get_objects)
- ✅ Truncation warnings in response data

#EA Terminologies and their meaning:
    ## ABB: Architecture Building Block (Class with 'block' stereotype).
    ## SBBI: Solution Building Block Instance (Part with a link to ABB in PDATA1).
    ## Product: Class with 'block' stereotype having SBBIs and a CompositeStructure (Internal Block Diagram) as children.
    ## Value Scopes: Class with 'value_scope' stereotype (Also can have a value scope diagram in same package with value scope elements in it).
    ## Interface Block: Class (with InterfaceBlock stereotype). 

"""


@mcp.resource("dbea://schema-reference")
def get_schema_reference() -> str:
    """Return EA database schema reference for understanding table structures and relationships."""
    return """
# Enterprise Architect Database Schema Reference

## Overview
This reference describes the essential tables in the EA SQLite database (.qea/.qeax files).
Use this to understand table structures when writing custom queries.

## 📋 Core Tables

### t_object (Model Elements/Objects)
**Description**: Central table storing all model elements (Classes, Components, Parts, Ports, Packages, etc.)

**Core Columns:**
| Column | Type | Description |
|--------|------|-------------|
| **Object_ID** | Long | Primary Key - Unique object identifier |
| **ea_guid** | Text(255) | GUID in {UPPERCASE} format |
| **Name** | Text(255) | Element name |
| **Object_Type** | Text(255) | Type: 'Class', 'Component', 'Part', 'Port', 'Package', etc. |
| **Stereotype** | Text(255) | Stereotype (e.g., 'block', 'InterfaceBlock') |
| **Package_ID** | Long | FK to t_package - Owning package |
| **ParentID** | Long | FK to Object_ID - Parent element (0 if root) |
| **Classifier** | Integer | Numeric classifier ID for typed elements |
| **Classifier_guid** | Text(255) | GUID of classifier |
| **Alias** | Text(255) | Element alias |
| **Note** | Memo | Element notes/description |
| **Author** | Text(255) | Author name |
| **Status** | Text(255) | Status: 'Proposed', 'Approved', 'Validated', etc. |
| **Version** | Text(255) | Version string |
| **CreatedDate** | DateTime | Creation timestamp |
| **ModifiedDate** | DateTime | Last modification timestamp |
| **Abstract** | Text(255) | Is abstract (boolean as text) |
| **PDATA1** | Text(255) | Classifier GUID for Parts/Ports (provenance) |
| **PDATA2** | Text(255) | Additional extended data |
| **PDATA3** | Text(255) | Additional extended data |
| **PDATA4** | Text(255) | Additional extended data |
| **PDATA5** | Text(255) | Additional extended data |
| **Diagram_ID** | Long | Associated diagram (if object is package) |

**Additional Columns:**
NType, Complexity, Effort, Style, Backcolor, BorderStyle, BorderWidth, Fontcolor, Bordercolor, Tagged,
Concurrency, Visibility, Persistence, Cardinality, GenType, GenFile, Header1, Header2, Phase, Scope,
GenOption, GenLinks, RunState, TPos, IsRoot, IsLeaf, IsSpec, IsActive, StateFlags, PackageFlags,
Multiplicity, StyleEx, ActionFlags, EventFlags.

**Common Object_Type Values**:
- `Class` - Classes, ABBs (Architecture Building Blocks)
- `Component` - Components
- `Part` - Parts, SBBIs (Solution Building Block Instances)
- `Port` - Ports
- `Package` - Packages
- `Interface` - Interfaces, Interfaces Blocks
- `Activity` - Activities
- `Sequence` - Sequence elements
- `Boundary` - Boundary wrappers

**Indexes**: Object_ID (PK), ea_guid, Package_ID, ParentID

---

### t_package (Packages)
**Description**: Package hierarchy structure

**Core Columns:**
| Column | Type | Description |
|--------|------|-------------|
| **Package_ID** | Long | Primary Key |
| **Name** | Text(255) | Package name |
| **Parent_ID** | Long | FK to Package_ID (0 for root) |
| **ea_guid** | Text(255) | Package GUID |
| **Version** | Text(255) | Version (default "1.0") |
| **CreatedDate** | DateTime | Creation timestamp |
| **ModifiedDate** | DateTime | Last modification timestamp |
| **Notes** | Memo | Package notes/description |

**Additional Columns:**
XMLPath, IsControlled, LastLoadDate, LastSaveDate, Protected, PkgOwner, UMLVersion, UseDTD, LogXML,
CodePath, Namespace, TPos, PackageFlags, BatchSave, BatchLoad.

**Note**: Package stereotypes are stored in the corresponding t_object entry, not in t_package.

**Relationships**:
- Parent_ID → Package_ID (self-referencing for hierarchy)
- t_object.Package_ID → Package_ID

---

### t_connector (Connectors/Relationships)
**Description**: Relationships between elements (associations, generalizations, dependencies, etc.)

**Core Columns:**
| Column | Type | Description |
|--------|------|-------------|
| **Connector_ID** | Long | Primary Key |
| **ea_guid** | Text(255) | Connector GUID |
| **Name** | Text(255) | Connector label/name |
| **Connector_Type** | Text(255) | Type: 'Association', 'Generalization', 'Dependency', etc. |
| **SubType** | Text(255) | Sub-type |
| **Stereotype** | Text(255) | Stereotype (e.g., 'ItemFlow', 'Connector') |
| **Direction** | Text(255) | 'Source -> Destination', 'Bi-Directional', 'Unspecified' |
| **Start_Object_ID** | Long | FK to t_object.Object_ID (source) |
| **End_Object_ID** | Long | FK to t_object.Object_ID (target) |
| **SourceAccess** | Text(255) | Source visibility |
| **DestAccess** | Text(255) | Target visibility |
| **SourceIsNavigable** | Integer | Source navigability |
| **DestIsNavigable** | Integer | Target navigability |
| **DiagramID** | Long | Associated diagram |
| **RouteStyle** | Long | Routing style |
| **SeqNo** | Long | Sequence number |
| **NOTES** | Memo | Connector notes |
| **PDATA1-5** | Text(255) | Extended property data |

**Additional Columns:**
SourceCard, SourceElement, DestCard, DestElement, SourceRole, SourceRoleType, SourceRoleNote,
SourceContainment, SourceIsAggregate, SourceIsOrdered, SourceQualifier, DestRole, DestRoleType,
DestRoleNote, DestContainment, DestIsAggregate, DestIsOrdered, DestQualifier, Top_Start_Label,
Top_Mid_Label, Top_End_Label, Btm_Start_Label, Btm_Mid_Label, Btm_End_Label, Start_Edge, End_Edge,
PtStartX, PtStartY, PtEndX, PtEndY, HeadStyle, LineStyle, IsBold, LineColor, VirtualInheritance,
LinkAccess, SourceConstraint, DestConstraint, IsRoot, IsLeaf, IsSpec, SourceChangeable, DestChangeable,
SourceTS, DestTS, StateFlags, ActionFlags, IsSignal, IsStimulus, DispatchAction, Target2, StyleEx,
SourceStereotype, DestStereotype, SourceStyle, DestStyle, EventFlags.

**Common Connector_Type Values**:
- `Association` - Associations
- `Generalization` - Inheritance
- `Dependency` - Dependencies
- `Aggregation` - Aggregation
- `Composition` - Composition
- `Realisation` - Interface realization
- `InformationFlow` - Information flows
- `Connector` - SysML connectors

**Relationships**:
- Start_Object_ID → t_object.Object_ID
- End_Object_ID → t_object.Object_ID

---

### t_attribute (Attributes/Properties)
**Description**: Attributes of objects (properties, value properties, part properties)

**Core Columns:**
| Column | Type | Description |
|--------|------|-------------|
| **ID** | Long | Primary Key |
| **ea_guid** | Text(255) | Attribute GUID |
| **Object_ID** | Long | FK to t_object.Object_ID |
| **Name** | Text(255) | Attribute name |
| **Type** | Text(255) | Data type (e.g., 'int', 'String', 'Real') |
| **Scope** | Text(255) | Visibility: 'Public', 'Private', 'Protected', 'Package' |
| **Stereotype** | Text(255) | Stereotype (e.g., 'ValueProperty', 'PartProperty') |
| **'Default'** | Text(255) | Default value (note: column name is quoted!) |
| **LowerBound** | Text(255) | Multiplicity lower bound |
| **UpperBound** | Text(255) | Multiplicity upper bound |
| **Notes** | Memo | Attribute notes |
| **Pos** | Long | Position/ordering |

**Additional Columns:**
Containment, IsStatic, IsCollection, IsOrdered, AllowDuplicates, Container, Derived, GenOption,
Length, Precision, Scale, Const, Style, Classifier, StyleEx.

**⚠️ Important**: The column name for default values is quoted as `'Default'` in the schema.
When querying, use: `SELECT "Default" AS DefaultValue FROM t_attribute` to avoid SQL syntax errors.

**Relationships**:
- Object_ID → t_object.Object_ID

---

### t_operation (Operations/Methods)
**Description**: Operations/methods of objects

**Core Columns:**
| Column | Type | Description |
|--------|------|-------------|
| **OperationID** | Long | Primary Key |
| **ea_guid** | Text(255) | Operation GUID |
| **Object_ID** | Long | FK to t_object.Object_ID |
| **Name** | Text(255) | Operation name |
| **Type** | Text(255) | Return type (e.g., 'void', 'int', 'Real') |
| **Scope** | Text(255) | Visibility: 'Public', 'Private', 'Protected', 'Package' |
| **Stereotype** | Text(255) | Stereotype |
| **ReturnArray** | Text(255) | Is return type array |
| **Notes** | Memo | Operation notes |
| **Abstract** | Text(255) | Is abstract |
| **Concurrency** | Text(255) | Concurrency type |
| **Pos** | Long | Position/ordering |

**Additional Columns:**
IsStatic, Behaviour, Synchronized, Const, Style, Pure, Throws, Classifier, Code, IsRoot, IsLeaf,
IsQuery, StateFlags, StyleEx, GenOption.

**Relationships**:
- Object_ID → t_object.Object_ID

---

### t_objectproperties (Tagged Values)
**Description**: Tagged values (custom properties) on elements

| Column | Type | Description |
|--------|------|-------------|
| **PropertyID** | Long | Primary Key |
| **ea_guid** | Text(255) | Property GUID |
| **Object_ID** | Long | FK to t_object.Object_ID |
| **Property** | Text(255) | Property name (tag name) |
| **Value** | Text(255) | Property value |
| **Notes** | Memo | Property notes |

**Common Properties for SBBIs**:
- `Solution` - Solution name
- `Configuration` - Configuration name
- `Variant` - Variant specification

**Relationships**:
- Object_ID → t_object.Object_ID

---

### t_connectortag (Connector Tagged Values)
**Description**: Tagged values on connectors

| Column | Type | Description |
|--------|------|-------------|
| **PropertyID** | Long | Primary Key |
| **ElementID** | Long | FK to t_connector.Connector_ID |
| **Property** | Text(255) | Property name |
| **VALUE** | Text(255) | Property value |
| **NOTES** | Memo | Notes |
| **ea_guid** | Text(255) | Property GUID |

**Relationships**:
- ElementID → t_connector.Connector_ID

---

### t_operationtag (Operation Tagged Values)
**Description**: Tagged values on operations

| Column | Type | Description |
|--------|------|-------------|
| **PropertyID** | Long | Primary Key |
| **ElementID** | Long | FK to t_operation.OperationID |
| **Property** | Text(255) | Property name |
| **VALUE** | Text(255) | Property value |
| **NOTES** | Memo | Notes |
| **ea_guid** | Text(255) | Property GUID |

**Relationships**:
- ElementID → t_operation.OperationID

---

## 📊 Diagram Representation Tables

### t_diagram (Diagrams)
**Description**: Diagram definitions

**Core Columns:**
| Column | Type | Description |
|--------|------|-------------|
| **Diagram_ID** | Long | Primary Key |
| **ea_guid** | Text(255) | Diagram GUID (use this column, not 'DiagramGUID') |
| **Package_ID** | Long | FK to t_package.Package_ID |
| **ParentID** | Long | Parent diagram (0 if root) |
| **Name** | Text(255) | Diagram name |
| **Diagram_Type** | Text(255) | Type: 'SysML', 'Component', 'Sequence', etc. |
| **Stereotype** | Text(255) | Diagram stereotype |
| **Version** | Text(255) | Version (default "1.0") |
| **Author** | Text(255) | Author |
| **ShowDetails** | Long | Show details flag (0/1) |
| **Notes** | Memo | Diagram notes |
| **CreatedDate** | DateTime | Creation timestamp |
| **ModifiedDate** | DateTime | Last modification timestamp |

**Additional Columns:**
AttPub, AttPri, AttPro, Orientation, cx, cy, Scale, HTMLPath, ShowForeign, ShowBorder,
ShowPackageContents, PDATA, Locked, TPos, Swimlanes, StyleEx.

**Common Diagram Stereotypes**:
- `block definition diagram` (BDD)
- `internal block diagram` (IBD)
- `parametric diagram`
- `requirement diagram`

**Relationships**:
- Package_ID → t_package.Package_ID

---

### t_diagramobjects (Objects on Diagrams)
**Description**: Visual representation of objects on diagrams

| Column | Type | Description |
|--------|------|-------------|
| **Instance_ID** | Long | Primary Key |
| **Diagram_ID** | Long | FK to t_diagram.Diagram_ID |
| **Object_ID** | Long | FK to t_object.Object_ID |
| **RectTop** | Long | Top Y coordinate |
| **RectLeft** | Long | Left X coordinate |
| **RectRight** | Long | Right X coordinate |
| **RectBottom** | Long | Bottom Y coordinate |
| **Sequence** | Long | Z-order sequence |
| **ObjectStyle** | Text(255) | Style properties |

**Note**: (Diagram_ID = Diagram_ID) relationship identifies which diagram contains which objects.

**Relationships**:
- Diagram_ID → t_diagram.Diagram_ID
- Object_ID → t_object.Object_ID

---

### t_diagramlinks (Connectors on Diagrams)
**Description**: Visual representation of connectors on diagrams

| Column | Type | Description |
|--------|------|-------------|
| **Instance_ID** | Long | Primary Key |
| **DiagramID** | Long | FK to t_diagram.Diagram_ID |
| **ConnectorID** | Long | FK to t_connector.Connector_ID |
| **Geometry** | Memo | Path geometry |
| **Style** | Text(255) | Style properties |
| **Hidden** | YesNo | Is hidden |
| **Path** | Text(255) | Routing path |

**Relationships**:
- DiagramID → t_diagram.Diagram_ID
- ConnectorID → t_connector.Connector_ID

---

##EA Terminologies and their meaning:
    ### ABB: Architecture Building Block (Class with 'block' stereotype).
    ### SBBI: Solution Building Block Instance (Part with a link to ABB in PDATA1).
    ### Product: Class with 'block' stereotype having SBBIs and a CompositeStructure (Internal Block Diagram) as children.
    ### Value Scopes: Class with 'value_scope' stereotype (Also can have a value scope diagram in same package with value scope elements in it).
    ### Interface Block: Class (with InterfaceBlock stereotype). 

## 🔍 Query Examples

### Find all ABBs (Architecture Building Blocks)
```sql
SELECT ea_guid, Name, Stereotype 
FROM t_object 
WHERE Object_Type = 'Class' 
  AND Stereotype LIKE '%block%'
LIMIT 100;
```

### Find all SBBIs (Solution Building Block Instances)
```sql
SELECT o.ea_guid, o.Name, p.Value as Solution
FROM t_object o
JOIN t_objectproperties p ON o.Object_ID = p.Object_ID
WHERE o.Object_Type = 'Part' LIMIT 100;
```

### Find all SBBIs with Solution tagged value
```sql
SELECT o.ea_guid, o.Name, p.Value as Solution
FROM t_object o
JOIN t_objectproperties p ON o.Object_ID = p.Object_ID
WHERE o.Object_Type = 'Part'
  AND p.Property = 'Solution'
LIMIT 100;
```

### Get package hierarchy
```sql
SELECT p1.Name as Parent, p2.Name as Child
FROM t_package p1
JOIN t_package p2 ON p1.Package_ID = p2.Parent_ID
WHERE p1.Parent_ID = 0
ORDER BY p1.Name, p2.Name;
```

### Find all objects in a package
```sql
SELECT ea_guid, Name, Object_Type, Stereotype
FROM t_object
WHERE Package_ID = ?
LIMIT 100;
```

### Get all connectors between specific types
```sql
SELECT c.Name, c.Connector_Type, 
       src.Name as Source, tgt.Name as Target
FROM t_connector c
JOIN t_object src ON c.Start_Object_ID = src.Object_ID
JOIN t_object tgt ON c.End_Object_ID = tgt.Object_ID
WHERE c.Connector_Type = 'Association'
LIMIT 100;
```

### Find objects by tagged value
```sql
SELECT o.ea_guid, o.Name, p.Property, p.Value
FROM t_object o
JOIN t_objectproperties p ON o.Object_ID = p.Object_ID
WHERE p.Property = 'Solution'
  AND p.Value LIKE '%Powertrain%'
LIMIT 100;
```

### Get all diagrams in a package
```sql
SELECT Diagram_ID, ea_guid, Name, Diagram_Type, Stereotype
FROM t_diagram
WHERE Package_ID = ?
LIMIT 100;
```

### Find objects on a specific diagram
```sql
SELECT o.ea_guid, o.Name, o.Object_Type,
       d.RectLeft, d.RectTop, d.RectRight, d.RectBottom
FROM t_diagramobjects d
JOIN t_object o ON d.Object_ID = o.Object_ID
WHERE d.Diagram_ID = ?;
```
---

## 🔗 Important Relationships

### Element Containment
- Package contains Objects: t_package.Package_ID ← t_object.Package_ID
- Object contains Objects: t_object.Object_ID ← t_object.ParentID (nested elements)
- Package hierarchy: t_package.Package_ID ← t_package.Parent_ID

### Element Classification
- Object typed by Classifier: t_object.Classifier_guid → t_object.ea_guid
- Part/Port typed via PDATA1: t_object.PDATA1 contains classifier GUID

### Element Details
- Object has Attributes: t_object.Object_ID ← t_attribute.Object_ID
- Object has Operations: t_object.Object_ID ← t_operation.Object_ID
- Object has Tagged Values: t_object.Object_ID ← t_objectproperties.Object_ID

### Connectors
- Connector links Objects:
  - t_connector.Start_Object_ID → t_object.Object_ID
  - t_connector.End_Object_ID → t_object.Object_ID
- Connector has Tagged Values: t_connector.Connector_ID ← t_connectortag.ElementID

### Diagrams
- Diagram in Package: t_diagram.Package_ID → t_package.Package_ID
- Object appears on Diagram: t_diagramobjects links Diagram_ID and Object_ID
- Connector appears on Diagram: t_diagramlinks links DiagramID and ConnectorID

---

## 💡 Best Practices for Queries
- Always use LIMIT: Add LIMIT clause to prevent massive result sets
- Filter by Package: Use Package_ID to scope queries to specific areas
- Use ea_guid for joins: More reliable than numeric IDs across models
- Check Object_Type: Always filter by Object_Type for targeted results
- Index-friendly: Queries on Object_ID, Package_ID, ea_guid are fast
- Tagged Values: Use JOIN to t_objectproperties for custom metadata
- Count first: Use COUNT(*) before fetching large result sets

---

## ⚠️ Important Notes
- GUID Format: Always {UPPERCASE} with braces, e.g., {A1B2C3D4-E5F6-...}
- ParentID = 0: Indicates root-level element (no parent)
- Parent_ID = 0: Indicates root-level package
- Classifier storage: Check Classifier_guid, Classifier (numeric), or PDATA1 (for Parts/Ports)
- Stereotypes: Can be stored in Stereotype column or t_xref table (for multiple stereotypes)
- Memo fields: Note, Notes, Geometry - can contain large text, handle carefully
- Default column: In t_attribute, the column is quoted as `'Default'` - use `"Default"` in queries

---

## 📚 Related Tables (Not Covered)
- t_xref: Cross-references for stereotypes, custom properties
- t_operationparams: Operation parameters
- t_attributetag: Attribute tagged values
- t_diagram_types: Diagram type definitions
- t_glossary: Glossary terms
- t_requirements: Requirements
- t_trxtypes: Transaction types

For complete schema, query sqlite_master table:
```sql
SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name;
```
"""


# ============================================================================
# MODEL LIFECYCLE
# ============================================================================


@mcp.tool()
def open_model(path: str, read_only: bool = True) -> dict:
    """Open an EA SQLite (.qea/.qeax) model. Replaces any previously opened model.

    Path / environment guidance:
    1. Direct Windows execution (python on Windows / PowerShell):
       - Pass a normal Windows absolute path, e.g. `C:\\Models\\myrepo\\architecture.qeax`.
    2. WSL session (Ubuntu on /mnt/c/...):
       - Either pass the WSL path (`/mnt/c/Models/myrepo/architecture.qeax`) OR a Windows path.
       - If you pass a Windows path (e.g. `C:\\Models\\...`) and it does not exist natively in the Linux FS,
         this function will attempt to auto-map it to `/mnt/<drive>/...` (e.g. `C:` -> `/mnt/c/`).
    3. Docker container running on Windows started from WSL:
       - The mounted workspace is "--volume", "./dbea_workspace:/app/dbea_workspace"
       - So make sure the input file is copied to this mounted workspace
         and then provide container path /app/dbea_workspace/<filename> passed as input
    4. Relative paths: If you place the database in the working directory (e.g. mounted workspace) you can pass
       a relative filename (e.g. `architecture.qeax`). Ensure the working directory matches the mounted location.

    Recommended remediation steps when path fails:
       - If running in WSL: rewrite `C:\\X\\Y.qeax` -> `/mnt/c/X/Y.qeax` and retry.
       - If running in Docker: ensure the input file is present in mounted folder;
         copy/upload the file into the mounted directory.
       - If still failing: list directory contents to confirm presence.

    Args:
        path: Absolute or relative path to .qea/.qeax/.sqlite file (Windows, WSL, or container path).
        read_only: Open in read-only mode (recommended unless modifying).

    Returns:
        dict: {"path": resolved_path, "read_only": bool, "alive": bool}
    """
    global _READER, _MODEL_PATH, _READ_ONLY
    original_path = path

    def _candidate_paths(p: str) -> list[str]:
        """Generate alternate path candidates across Windows/WSL conventions."""
        candidates: list[str] = []
        # Windows style to WSL
        if re.match(r"^[A-Za-z]:\\", p):
            drive = p[0].lower()
            wsl_variant = "/mnt/" + drive + "/" + p[3:].replace("\\", "/")
            candidates.append(wsl_variant)
        # WSL style to Windows
        m = re.match(r"^/mnt/([a-zA-Z])/", p)
        if m:
            drive = m.group(1).upper()
            remainder = p[len(f"/mnt/{m.group(1)}/") :]
            win_variant = f"{drive}:\\" + remainder.replace("/", "\\")
            candidates.append(win_variant)
        return candidates

    # Resolve path if not found: try generated candidates.
    if not os.path.exists(path):
        for cand in _candidate_paths(path):
            if os.path.exists(cand):
                logging.info(f"Resolved alternate path '{path}' -> '{cand}'")
                path = cand
                break
        else:
            # Additional hint when unreachable and looks like OS mismatch.
            if os.name == "nt" and path.startswith("/mnt/"):
                logging.warning(
                    "WSL-style path '%s' not accessible on native Windows. Consider converting to drive letter form.",
                    path,
                )
            elif os.name != "nt" and re.match(r"^[A-Za-z]:\\", path):
                logging.warning(
                    "Windows-style path '%s' not accessible on this POSIX environment. Consider /mnt/<drive>/ mapping or bind mount.",
                    path,
                )

    model_path = Path(path)
    logging.info(f"Opening model path='{model_path}' (original='{original_path}') read_only={read_only}")
    _READER = EaModelReader(model_path, read_only=read_only)
    _MODEL_PATH = str(model_path)
    _READ_ONLY = read_only
    result = {"path": _MODEL_PATH, "read_only": _READ_ONLY, "alive": _READER.alive_check()}
    logging.info(f"Model opened: {result}")
    return result


@mcp.tool()
def alive_check() -> bool:
    """Check if current reader connection is alive."""
    alive = _ensure_reader().alive_check()
    logging.info(f"Alive check: {alive}")
    return alive


# ============================================================================
# READ OPERATIONS - SAFETY & DISCOVERY
# ============================================================================


@mcp.tool()
def search_objects(
    name_pattern: str | None = None,
    object_type: str | None = None,
    stereotype: str | None = None,
    package_id: int | None = None,
    limit: int = 100,
) -> dict:
    """Search for objects with filters - MORE EFFICIENT than fetching all then filtering.

    ⚠️ USE THIS instead of get_objects() when looking for specific items!

    Filtering at the database level is much faster than fetching everything and filtering in Python.
    Combine multiple filters for precision. Supports SQL LIKE patterns for name and stereotype.

    Args:
        name_pattern: SQL LIKE pattern (e.g., '%Controller%', 'System%')
        object_type: Exact Object_Type match (e.g., 'Class', 'Component', 'Package', 'Port', 'Part')
        stereotype: SQL LIKE pattern for stereotype (e.g., '%block%', 'InterfaceBlock')
        package_id: Filter by Package_ID
        limit: Maximum results (default 100, max 1000)

    Returns:
        dict with:
            - results: List of matching objects (lightweight)
            - count: Number of results returned
            - truncated: True if more results exist beyond limit
            - filters_applied: Summary of filters used

    Examples:
        # Find all ABBs (Architecture Building Blocks)
        abbs = search_objects(object_type='Class', stereotype='%block%', limit=200)

        # Find all Controllers
        controllers = search_objects(name_pattern='%Controller%', object_type='Class')

        # Find Interface Blocks in specific package
        ifaces = search_objects(stereotype='InterfaceBlock', package_id=10, limit=50)

        # Find all Parts (potential SBBIs)
        parts = search_objects(object_type='Part', limit=500)
    """
    limit = min(limit, 1000)  # Hard cap

    query = "SELECT ea_guid, Name, Object_Type, Stereotype, Package_ID FROM t_object WHERE 1=1"
    params = []

    if name_pattern:
        query += " AND Name LIKE ?"
        params.append(name_pattern)
    if object_type:
        query += " AND Object_Type = ?"
        params.append(object_type)
    if stereotype:
        query += " AND Stereotype LIKE ?"
        params.append(stereotype)
    if package_id:
        query += " AND Package_ID = ?"
        params.append(package_id)

    # Fetch one extra to detect truncation
    query += f" LIMIT {limit + 1}"

    r = _ensure_reader()
    results = r._query(query, tuple(params))

    truncated = len(results) > limit
    if truncated:
        results = results[:limit]

    logging.info(
        f"search_objects(name={name_pattern}, type={object_type}, stereo={stereotype}, pkg={package_id}) "
        f"-> {len(results)} results, truncated={truncated}"
    )

    return {
        "results": results,
        "count": len(results),
        "truncated": truncated,
        "filters_applied": {
            "name_pattern": name_pattern,
            "object_type": object_type,
            "stereotype": stereotype,
            "package_id": package_id,
        },
        "note": "Use get_object(ea_guid) from results to fetch full enriched details",
    }


@mcp.tool()
def custom_query(sql: str, max_rows: int = 500) -> dict:
    """Execute custom SQL with automatic result limiting and safety warnings.

    ⚠️ IMPORTANT: For large result sets:
    1. Use COUNT(*) queries first to check size
    2. Add LIMIT clauses to your SELECT queries
    3. Use pagination for results > 500 rows
    4. Filter with WHERE clauses at database level
    5. DELETE operations are blocked for safety

    Args:
        sql: SQL statement(s) - separate multiple with semicolons
        max_rows: Maximum rows to return (default 500, max 5000)

    Returns:
        dict with:
            - data: Query results (for SELECT)
            - count: Number of rows returned
            - truncated: True if auto-limited
            - warning: Message if result set is large

    Examples:
        # Good: Count first
        result = custom_query("SELECT COUNT(*) as total FROM t_object WHERE Object_Type='Class'")

        # Good: Use LIMIT
        result = custom_query("SELECT * FROM t_object WHERE Object_Type='Class' LIMIT 100")
    """
    max_rows = min(max_rows, 5000)  # Absolute hard cap
    r = _ensure_reader()

    # Check for destructive SQL operations (DELETE, DROP, TRUNCATE, ALTER)
    if _contains_destructive_sql(sql):
        logging.warning("Destructive SQL operation blocked in custom_query")
        raise PermissionError(
            "Destructive SQL operations (DELETE, DROP, TRUNCATE, ALTER) are restricted for safety. Should be done by the user manually."
        )
    statements = [s.strip() for s in sql.strip().split(";") if s.strip()]
    if not statements:
        return {"data": [], "count": 0, "truncated": False}

    last_result: list[dict] | None = None
    auto_limited = False

    for stmt in statements:
        stmt_lower = stmt.lower().strip()

        # Detect read-only statements (SELECT, WITH, EXPLAIN, PRAGMA queries)
        is_select = (
            stmt_lower.startswith("select")
            or stmt_lower.startswith("with")  # CTE (Common Table Expressions)
            or stmt_lower.startswith("explain")
            or stmt_lower.startswith("pragma")  # SQLite PRAGMA queries (read-only ones)
        )

        if is_select:
            # Check if LIMIT already present (only for SELECT and WITH statements)
            if stmt_lower.startswith(("select", "with")) and "limit" not in stmt_lower:
                # Auto-append LIMIT
                stmt = f"{stmt} LIMIT {max_rows}"
                auto_limited = True
                logging.warning(f"Auto-limited query to {max_rows} rows")

            last_result = r._query(stmt)

            # Warning if hitting limit
            if len(last_result) >= max_rows * 0.9:  # 90% of limit
                logging.warning(f"Query returned {len(last_result)} rows near limit {max_rows}")
                return {
                    "data": last_result,
                    "count": len(last_result),
                    "warning": f"⚠️ Result set may be truncated at {max_rows} rows. Use COUNT(*) to check total, then add LIMIT/OFFSET for pagination.",
                    "truncated": True,
                    "auto_limited": auto_limited,
                }
        else:
            # Write operation detected
            if _READ_ONLY:
                raise PermissionError(f"Non-SELECT statement attempted while in read-only mode: {stmt[:50]}...")
            r.cur.execute(stmt)

    if last_result is not None:
        return {"data": last_result, "count": len(last_result), "truncated": False, "auto_limited": auto_limited}

    return {"rows_affected": r.cur.rowcount, "statements_executed": len(statements)}


# ============================================================================
# READ OPERATIONS - SPECIFIC QUERIES
# ============================================================================
@mcp.tool()
def get_object_summary(package_id: int | None = None) -> dict:
    """Get lightweight summary of objects (IDs and names only) for browsing.

    Useful for exploring model before fetching full details.
    """
    query = "SELECT ea_guid, Name, Object_Type, Stereotype FROM t_object"
    if package_id is not None:
        query += f" WHERE Package_ID={package_id}"
    query += " LIMIT 1000"  # Hard limit for summaries

    r = _ensure_reader()
    results = r._query(query)

    return {
        "objects": results,
        "count": len(results),
        "note": "Use get_object(ea_guid) to fetch full details for specific items",
    }


@mcp.tool()
def get_object(ea_guid: str) -> Optional[dict]:
    """Return enriched EA object by GUID.

    Fetches complete object details including stereotypes, classifiers, tagged values, etc.
    For browsing/searching, use get_object_summary() or search_objects() first.

    Args:
        ea_guid: Element GUID (with or without braces)

    Returns:
        Full enriched object dict or None if not found
    """
    logging.info(f"get_object guid='{ea_guid}'")
    obj = _ensure_reader().get_object(_normalize_guid(ea_guid))
    if obj is None:
        logging.info(f"Object not found guid='{ea_guid}'")
    return obj


@mcp.tool()
def get_objects(package_id: int | None = None, parent_id: int | None = None, limit: int = 100, offset: int = 0) -> dict:
    """Return objects filtered by package_id and/or parent_id WITH PAGINATION.

    ⚠️ RECOMMENDED WORKFLOW:
    1. Call count_objects(package_id, parent_id) FIRST to check total size
    2. If total > 100, use limit/offset to paginate through results
    3. Check 'has_more' field to know if additional pages exist
    4. For searching specific items, use search_objects() instead

    Args:
        package_id: Filter by Package_ID (optional)
        parent_id: Filter by ParentID (optional)
        limit: Maximum rows to return (default 100, max 1000)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with:
            - data: List of enriched object dicts (current page)
            - total_count: Total objects matching filters
            - returned_count: Number in current page
            - limit: Limit used
            - offset: Offset used
            - has_more: True if more pages available
            - next_offset: Suggested offset for next page (if has_more)

    Example:
        # Step 1: Check size
        count = count_objects(package_id=5)
        print(f"Total objects: {count['total_objects']}")

        # Step 2: Fetch first page
        page1 = get_objects(package_id=5, limit=100, offset=0)

        # Step 3: Fetch next page if more data exists
        if page1['has_more']:
            page2 = get_objects(package_id=5, limit=100, offset=page1['next_offset'])
    """
    limit = min(limit, 1000)  # Hard cap
    logging.info(f"get_objects package_id={package_id} parent_id={parent_id} limit={limit} offset={offset}")

    # Get total count first
    count_query = "SELECT COUNT(*) as total FROM t_object"
    clauses = []
    params = []
    if package_id is not None:
        clauses.append("Package_id=?")
        params.append(package_id)
    if parent_id is not None:
        clauses.append("parentID=?")
        params.append(max(parent_id, 0))
    if clauses:
        count_query += " WHERE " + " AND ".join(clauses)

    r = _ensure_reader()
    total = r._query(count_query, tuple(params))[0]["total"]

    # Get paginated data using existing reader method
    objs = r.get_objects(package_id, parent_id)
    paginated = objs[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_objects returned {len(paginated)}/{total} objects")
    return result


@mcp.tool()
def get_packages(
    package_id: int | None = None, parent_id: int | None = None, limit: int = 100, offset: int = 0
) -> dict:
    """Return packages with pagination support.

    Args:
        package_id: Filter by specific Package_ID (optional)
        parent_id: Filter by Parent_ID (optional)
        limit: Maximum rows to return (default 100, max 1000)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with paginated package data and metadata
    """
    limit = min(limit, 1000)
    logging.info(f"get_packages package_id={package_id} parent_id={parent_id} limit={limit} offset={offset}")

    # Get total count
    count_query = "SELECT COUNT(*) as total FROM t_package"
    clauses = []
    params = []
    if package_id is not None:
        clauses.append("Package_ID=?")
        params.append(package_id)
    if parent_id is not None:
        clauses.append("Parent_ID=?")
        params.append(max(parent_id, 0))
    if clauses:
        count_query += " WHERE " + " AND ".join(clauses)

    r = _ensure_reader()
    total = r._query(count_query, tuple(params))[0]["total"]

    # Get paginated data
    pkgs = r.get_packages(package_id, parent_id)
    paginated = pkgs[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_packages returned {len(paginated)}/{total} packages")
    return result


@mcp.tool()
def get_connectors(
    source_guid: str | None = None,
    target_guid: str | None = None,
    connector_type: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict:
    """Return connectors with pagination and filtering.

    Args:
        source_guid: Filter by source object GUID (optional)
        target_guid: Filter by target object GUID (optional)
        connector_type: Filter by connector type (optional)
        limit: Maximum rows to return (default 100, max 1000)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with paginated connector data and metadata
    """
    limit = min(limit, 1000)

    src = _normalize_guid(source_guid) if source_guid else None
    tgt = _normalize_guid(target_guid) if target_guid else None

    logging.info(f"get_connectors source={src} target={tgt} type={connector_type} limit={limit} offset={offset}")

    # Build count query
    count_query = "SELECT COUNT(*) as total FROM t_connector"
    clauses = []
    params = []
    if src:
        clauses.append("Start_Object_ID IN (SELECT Object_ID FROM t_object WHERE ea_guid=?)")
        params.append(src)
    if tgt:
        clauses.append("End_Object_ID IN (SELECT Object_ID FROM t_object WHERE ea_guid=?)")
        params.append(tgt)
    if connector_type:
        clauses.append("Connector_Type=?")
        params.append(connector_type)
    if clauses:
        count_query += " WHERE " + " AND ".join(clauses)

    r = _ensure_reader()
    total = r._query(count_query, tuple(params))[0]["total"]

    # Get paginated data
    conns = r.get_connectors(src, tgt, connector_type)
    paginated = conns[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_connectors returned {len(paginated)}/{total} connectors")
    return result


@mcp.tool()
def get_attributes(object_guid: str, limit: int = 100, offset: int = 0) -> dict:
    """Return attributes for an object with pagination.

    Args:
        object_guid: Object GUID to get attributes for
        limit: Maximum rows to return (default 100, max 500)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with paginated attribute data and metadata
    """
    limit = min(limit, 500)
    guid = _normalize_guid(object_guid)
    logging.info(f"get_attributes object_guid={guid} limit={limit} offset={offset}")

    # Get all attributes (typically not huge for single object)
    attrs = _ensure_reader().get_attributes(guid)
    total = len(attrs)
    paginated = attrs[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_attributes returned {len(paginated)}/{total} attributes")
    return result


@mcp.tool()
def get_operations(object_guid: str, limit: int = 100, offset: int = 0) -> dict:
    """Return operations for an object with pagination.

    Args:
        object_guid: Object GUID to get operations for
        limit: Maximum rows to return (default 100, max 500)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with paginated operation data and metadata
    """
    limit = min(limit, 500)
    guid = _normalize_guid(object_guid)
    logging.info(f"get_operations object_guid={guid} limit={limit} offset={offset}")

    # Get all operations
    ops = _ensure_reader().get_operations(guid)
    total = len(ops)
    paginated = ops[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_operations returned {len(paginated)}/{total} operations")
    return result


@mcp.tool()
def get_tagged_values(object_guid: str, limit: int = 200, offset: int = 0) -> dict:
    """Return tagged values for an object with pagination.

    Args:
        object_guid: Object GUID to get tagged values for
        limit: Maximum rows to return (default 200, max 500)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with paginated tagged value data and metadata
    """
    limit = min(limit, 500)
    guid = _normalize_guid(object_guid)
    logging.info(f"get_tagged_values object_guid={guid} limit={limit} offset={offset}")

    # Get all tagged values
    tvs = _ensure_reader().get_tagged_values(guid)
    total = len(tvs)
    paginated = tvs[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_tagged_values returned {len(paginated)}/{total} tagged values")
    return result


@mcp.tool()
def get_diagrams(package_id: int | None = None, limit: int = 100, offset: int = 0) -> dict:
    """Return diagrams with pagination.

    Args:
        package_id: Filter by Package_ID (optional)
        limit: Maximum rows to return (default 100, max 500)
        offset: Number of rows to skip for pagination (default 0)

    Returns:
        dict with paginated diagram data and metadata
    """
    limit = min(limit, 500)
    logging.info(f"get_diagrams package_id={package_id} limit={limit} offset={offset}")

    # Get all diagrams
    diagrams = _ensure_reader().get_diagrams(package_id)
    total = len(diagrams)
    paginated = diagrams[offset : offset + limit]

    has_more = (offset + limit) < total

    result = {
        "data": paginated,
        "total_count": total,
        "returned_count": len(paginated),
        "limit": limit,
        "offset": offset,
        "has_more": has_more,
        "next_offset": offset + limit if has_more else None,
    }
    logging.info(f"get_diagrams returned {len(paginated)}/{total} diagrams")
    return result


# ============================================================================
# WRITE OPERATIONS - TAGGED VALUES
# ============================================================================


@mcp.tool()
def update_tagged_value(object_guid: str, tag_name: str, new_value: str) -> dict:
    """Update a tagged value. Model must be opened with read_only=False.

    Args:
        object_guid: Object GUID
        tag_name: Name of the tagged value
        new_value: New value to set

    Returns:
        dict with operation result

    Example:
        result = update_tagged_value(
            object_guid=abb_guid,
            tag_name='Solution',
            new_value='PowertrainSolution'
        )
    """
    _guard_write()
    guid = _normalize_guid(object_guid)
    logging.info(f"update_tagged_value object_guid={guid} tag={tag_name} value={new_value}")
    result = _ensure_reader().update_tagged_value(guid, tag_name, new_value)
    logging.info(f"Tagged value updated: {result}")
    return result


@mcp.tool()
def add_tagged_value(object_guid: str, tag_name: str, tag_value: str) -> dict:
    """Add a new tagged value. Model must be opened with read_only=False.

    Args:
        object_guid: Object GUID
        tag_name: Name of the tagged value
        tag_value: Value to set

    Returns:
        dict with operation result

    Example:
        result = add_tagged_value(
            object_guid=sbbi_guid,
            tag_name='Configuration',
            tag_value='Default'
        )
    """
    _guard_write()
    guid = _normalize_guid(object_guid)
    logging.info(f"add_tagged_value object_guid={guid} tag={tag_name} value={tag_value}")
    result = _ensure_reader().add_tagged_value(guid, tag_name, tag_value)
    logging.info(f"Tagged value added: {result}")
    return result


# ============================================================================
# CREATION OPERATIONS - PACKAGES
# ============================================================================


@mcp.tool()
def create_package(name: str, parent_id: int = 0, notes: str = "") -> dict:
    """Create a new package in the EA model. Model must be opened with read_only=False.

    Args:
        name: Package name
        parent_id: Parent Package_ID (0 for root level)
        notes: Package notes/description (stored in corresponding t_object entry)

    Returns:
        dict with created package details including Package_ID and ea_guid
    """
    _guard_write()
    logging.info(f"create_package name='{name}' parent_id={parent_id}")

    r = _ensure_reader()

    # Generate GUID
    ea_guid = f"{{{str(uuid.uuid4()).upper()}}}"

    # Insert package - ONLY columns that exist in schema
    query = """
        INSERT INTO t_package (Name, Parent_ID, ea_guid, Version)
        VALUES (?, ?, ?, '1.0')
    """
    r.cur.execute(query, (name, parent_id, ea_guid))
    package_id = r.cur.lastrowid

    # Also create corresponding t_object entry (packages exist in both tables)
    obj_query = """
        INSERT INTO t_object (
            Object_Type, Name, Package_ID, ParentID, ea_guid, 
            Note, Classifier
        )
        VALUES ('Package', ?, ?, 0, ?, ?, 0)
    """
    r.cur.execute(obj_query, (name, package_id, ea_guid, notes if notes else ""))

    result = {
        "Package_ID": package_id,
        "ea_guid": ea_guid,
        "Name": name,
        "Parent_ID": parent_id,
        "status": "created",
        "note": "Package created in both t_package and t_object tables",
    }
    logging.info(f"Package created: {result}")
    return result


# ============================================================================
# CREATION OPERATIONS - OBJECTS/ELEMENTS
# ============================================================================


@mcp.tool()
def create_object(
    name: str,
    object_type: str,
    package_id: int,
    stereotype: str = "",
    notes: str = "",
    parent_id: int = 0,
    classifier_guid: str | None = None,
) -> dict:
    """Create a new object/element in the EA model. Model must be opened with read_only=False.

    Args:
        name: Object name
        object_type: Object type (e.g., 'Class', 'Component', 'Part', 'Port', 'Package', 'Interface')
        package_id: Package_ID where object will be created
        stereotype: Stereotype (e.g., 'block', 'InterfaceBlock', 'ACP_Function')
        notes: Object notes/description
        parent_id: Parent Object_ID for nested elements (0 for root)
        classifier_guid: GUID of classifier for typed elements (e.g., for Parts/Ports)

    Returns:
        dict with created object details including Object_ID and ea_guid

    Examples:
        # Create an ABB (Architecture Building Block)
        abb = create_object(
            name="DataController",
            object_type="Class",
            package_id=10,
            stereotype="block",
            notes="Manages data processing"
        )

        # Create an SBBI (Solution Building Block Instance) as a Part
        sbbi = create_object(
            name="controller1",
            object_type="Part",
            package_id=10,
            parent_id=system_obj_id,
            classifier_guid=abb['ea_guid']
        )

        # Create an Interface Block
        iface = create_object(
            name="IDataService",
            object_type="Class",
            package_id=10,
            stereotype="InterfaceBlock"
        )

        # Create a Port
        port = create_object(
            name="dataPort",
            object_type="Port",
            package_id=10,
            parent_id=abb_obj_id,
            classifier_guid=interface_guid
        )
    """
    _guard_write()
    logging.info(f"create_object name='{name}' type='{object_type}' package_id={package_id} stereotype='{stereotype}'")

    r = _ensure_reader()

    # Generate GUID
    ea_guid = f"{{{str(uuid.uuid4()).upper()}}}"

    # Normalize classifier GUID if provided
    classifier_id = None
    if classifier_guid:
        norm_guid = _normalize_guid(classifier_guid)
        # Get Object_ID of classifier
        classifier_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
        classifier_result = r._query(classifier_query, (norm_guid,))
        if classifier_result:
            classifier_id = classifier_result[0]["Object_ID"]

    # Insert object
    query = """
        INSERT INTO t_object (
            Object_Type, Name, Package_ID, Stereotype, Note, ParentID, 
            ea_guid, Classifier, CreatedDate, ModifiedDate, Status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'), 'Proposed')
    """
    r.cur.execute(query, (object_type, name, package_id, stereotype, notes, parent_id, ea_guid, classifier_id))
    object_id = r.cur.lastrowid

    result = {
        "Object_ID": object_id,
        "ea_guid": ea_guid,
        "Name": name,
        "Object_Type": object_type,
        "Package_ID": package_id,
        "Stereotype": stereotype,
        "ParentID": parent_id,
        "Classifier": classifier_id,
        "status": "created",
    }
    logging.info(f"Object created: {result}")
    return result


@mcp.tool()
def update_object(
    object_guid: str,
    name: str | None = None,
    notes: str | None = None,
    stereotype: str | None = None,
    status: str | None = None,
) -> dict:
    """Update object properties. Model must be opened with read_only=False.

    Args:
        object_guid: GUID of object to update
        name: New name (optional)
        notes: New notes (optional)
        stereotype: New stereotype (optional)
        status: New status (optional, e.g., 'Proposed', 'Approved', 'Validated')

    Returns:
        dict with update status

    Example:
        result = update_object(
            object_guid=abb['ea_guid'],
            status='Approved',
            notes='Updated architecture description'
        )
    """
    _guard_write()
    guid = _normalize_guid(object_guid)
    logging.info(f"update_object object_guid={guid}")

    r = _ensure_reader()

    # Build dynamic update query
    updates = []
    params = []

    if name is not None:
        updates.append("Name=?")
        params.append(name)
    if notes is not None:
        updates.append("Note=?")
        params.append(notes)
    if stereotype is not None:
        updates.append("Stereotype=?")
        params.append(stereotype)
    if status is not None:
        updates.append("Status=?")
        params.append(status)

    if not updates:
        return {"status": "no_changes", "message": "No fields provided to update"}

    updates.append("ModifiedDate=datetime('now')")
    params.append(guid)

    query = f"UPDATE t_object SET {', '.join(updates)} WHERE ea_guid=?"
    r.cur.execute(query, tuple(params))
    rows_affected = r.cur.rowcount

    result = {
        "status": "updated" if rows_affected > 0 else "not_found",
        "rows_affected": rows_affected,
        "ea_guid": guid,
    }
    logging.info(f"Object updated: {result}")
    return result


# ============================================================================
# CREATION OPERATIONS - CONNECTORS
# ============================================================================


@mcp.tool()
def create_connector(
    source_guid: str,
    target_guid: str,
    connector_type: str,
    name: str = "",
    stereotype: str = "",
    direction: str = "Unspecified",
) -> dict:
    """Create a connector/relationship between two objects. Model must be opened with read_only=False.

    Args:
        source_guid: Source object GUID
        target_guid: Target object GUID
        connector_type: Type of connector (e.g., 'Association', 'Generalization', 'Dependency',
                       'Aggregation', 'Composition', 'Realisation', 'InformationFlow', 'Connector')
        name: Connector name/label (optional)
        stereotype: Stereotype (e.g., 'ItemFlow', 'Abstraction')
        direction: Direction ('Source -> Destination', 'Destination -> Source', 'Bi-Directional', 'Unspecified')

    Returns:
        dict with created connector details including Connector_ID and ea_guid

    Examples:
        # Create association between ABBs
        conn = create_connector(
            source_guid=abb1_guid,
            target_guid=abb2_guid,
            connector_type="Association",
            name="uses"
        )

        # Create generalization (inheritance)
        gen = create_connector(
            source_guid=child_guid,
            target_guid=parent_guid,
            connector_type="Generalization"
        )

        # Create interface realization
        real = create_connector(
            source_guid=class_guid,
            target_guid=interface_guid,
            connector_type="Realisation"
        )

        # Create SysML connector between ports
        sys_conn = create_connector(
            source_guid=port1_guid,
            target_guid=port2_guid,
            connector_type="Connector",
            stereotype="Connector"
        )
    """
    _guard_write()
    src = _normalize_guid(source_guid)
    tgt = _normalize_guid(target_guid)
    logging.info(f"create_connector type='{connector_type}' source={src} target={tgt}")

    r = _ensure_reader()

    # Get Object_IDs
    src_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
    src_result = r._query(src_query, (src,))
    if not src_result:
        raise ValueError(f"Source object not found: {src}")
    source_id = src_result[0]["Object_ID"]

    tgt_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
    tgt_result = r._query(tgt_query, (tgt,))
    if not tgt_result:
        raise ValueError(f"Target object not found: {tgt}")
    target_id = tgt_result[0]["Object_ID"]

    # Generate GUID
    ea_guid = f"{{{str(uuid.uuid4()).upper()}}}"

    # Insert connector
    query = """
        INSERT INTO t_connector (
            Connector_Type, Name, Start_Object_ID, End_Object_ID, 
            Stereotype, Direction, ea_guid
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    r.cur.execute(query, (connector_type, name, source_id, target_id, stereotype, direction, ea_guid))
    connector_id = r.cur.lastrowid

    result = {
        "Connector_ID": connector_id,
        "ea_guid": ea_guid,
        "Connector_Type": connector_type,
        "Name": name,
        "Source_Object_ID": source_id,
        "Target_Object_ID": target_id,
        "Stereotype": stereotype,
        "Direction": direction,
        "status": "created",
    }
    logging.info(f"Connector created: {result}")
    return result


# ============================================================================
# CREATION OPERATIONS - DIAGRAMS
# ============================================================================


@mcp.tool()
def create_diagram(name: str, diagram_type: str, package_id: int, notes: str = "", stereotype: str = "") -> dict:
    """Create a new diagram in the EA model. Model must be opened with read_only=False.

    Args:
        name: Diagram name
        diagram_type: Diagram type (e.g., 'Logical', 'Component', 'Deployment', 'Sequence',
                     'Use Case', 'Activity', 'Statechart', 'Custom', 'Analysis', 'SysML')
        package_id: Package_ID where diagram will be created
        notes: Diagram notes/description
        stereotype: Diagram stereotype (e.g., 'block definition diagram', 'internal block diagram')

    Returns:
        dict with created diagram details including Diagram_ID and ea_guid

    Examples:
        # Create a BDD (Block Definition Diagram)
        bdd = create_diagram(
            name="System Architecture BDD",
            diagram_type="SysML",
            package_id=10,
            stereotype="block definition diagram"
        )

        # Create an IBD (Internal Block Diagram)
        ibd = create_diagram(
            name="System Internal Structure",
            diagram_type="SysML",
            package_id=10,
            stereotype="internal block diagram"
        )

        # Create a Component Diagram
        comp_diag = create_diagram(
            name="Component Architecture",
            diagram_type="Component",
            package_id=10
        )
    """
    _guard_write()
    logging.info(f"create_diagram name='{name}' type='{diagram_type}' package_id={package_id}")

    r = _ensure_reader()

    # Generate GUID - column name is ea_guid, NOT DiagramGUID
    diagram_guid = f"{{{str(uuid.uuid4()).upper()}}}"

    # Insert diagram - use correct column names from schema
    query = """
        INSERT INTO t_diagram (
            Name, Diagram_Type, Package_ID, ParentID, Notes, Stereotype, 
            ea_guid, Version, Author, ShowDetails, CreatedDate, ModifiedDate
        )
        VALUES (?, ?, ?, 0, ?, ?, ?, '1.0', '', 0, datetime('now'), datetime('now'))
    """
    r.cur.execute(query, (name, diagram_type, package_id, notes, stereotype, diagram_guid))
    diagram_id = r.cur.lastrowid

    result = {
        "Diagram_ID": diagram_id,
        "ea_guid": diagram_guid,  # Return as ea_guid (actual column name)
        "DiagramGUID": diagram_guid,  # Also return as DiagramGUID for compatibility
        "Name": name,
        "Diagram_Type": diagram_type,
        "Package_ID": package_id,
        "Stereotype": stereotype,
        "status": "created",
    }
    logging.info(f"Diagram created: {result}")
    return result


@mcp.tool()
def add_object_to_diagram(
    diagram_id: int,
    object_guid: str,
    rect_left: int = 100,
    rect_top: int = 100,
    rect_right: int = 200,
    rect_bottom: int = 150,
) -> dict:
    """Add an object to a diagram. Model must be opened with read_only=False.

    Args:
        diagram_id: Diagram_ID where object will be added
        object_guid: GUID of object to add
        rect_left: Left position (pixels)
        rect_top: Top position (pixels)
        rect_right: Right position (pixels)
        rect_bottom: Bottom position (pixels)

    Returns:
        dict with diagram object details including Instance_ID

    Example:
        # Add ABB to BDD diagram
        diag_obj = add_object_to_diagram(
            diagram_id=bdd['Diagram_ID'],
            object_guid=abb['ea_guid'],
            rect_left=100,
            rect_top=100,
            rect_right=250,
            rect_bottom=180
        )

        # Add multiple objects to a diagram
        objects = [abb1, abb2, abb3]
        y_pos = 50
        for obj in objects:
            add_object_to_diagram(
                diagram_id=bdd['Diagram_ID'],
                object_guid=obj['ea_guid'],
                rect_left=50,
                rect_top=y_pos,
                rect_right=200,
                rect_bottom=y_pos + 80
            )
            y_pos += 100  # Stack vertically
    """
    _guard_write()
    guid = _normalize_guid(object_guid)
    logging.info(f"add_object_to_diagram diagram_id={diagram_id} object_guid={guid}")

    r = _ensure_reader()

    # Get Object_ID
    obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
    obj_result = r._query(obj_query, (guid,))
    if not obj_result:
        raise ValueError(f"Object not found: {guid}")
    object_id = obj_result[0]["Object_ID"]

    # Insert diagram object
    query = """
        INSERT INTO t_diagramobjects (
            Diagram_ID, Object_ID, RectLeft, RectTop, RectRight, RectBottom
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """
    r.cur.execute(query, (diagram_id, object_id, rect_left, rect_top, rect_right, rect_bottom))
    instance_id = r.cur.lastrowid

    result = {
        "Instance_ID": instance_id,
        "Diagram_ID": diagram_id,
        "Object_ID": object_id,
        "position": {"left": rect_left, "top": rect_top, "right": rect_right, "bottom": rect_bottom},
        "status": "added",
    }
    logging.info(f"Object added to diagram: {result}")
    return result


@mcp.tool()
def add_connector_to_diagram(diagram_id: int, connector_id: int) -> dict:
    """Add a connector to a diagram. Model must be opened with read_only=False.

    Args:
        diagram_id: Diagram_ID where connector will be added
        connector_id: Connector_ID to add

    Returns:
        dict with diagram link details

    Example:
        # First create or get connector
        conn = create_connector(source_guid=obj1_guid, target_guid=obj2_guid, connector_type="Association")

        # Then add to diagram
        diag_link = add_connector_to_diagram(
            diagram_id=bdd['Diagram_ID'],
            connector_id=conn['Connector_ID']
        )
    """
    _guard_write()
    logging.info(f"add_connector_to_diagram diagram_id={diagram_id} connector_id={connector_id}")

    r = _ensure_reader()

    # Insert diagram link
    query = """
        INSERT INTO t_diagramlinks (
            DiagramID, ConnectorID
        )
        VALUES (?, ?)
    """
    r.cur.execute(query, (diagram_id, connector_id))
    instance_id = r.cur.lastrowid

    result = {"Instance_ID": instance_id, "DiagramID": diagram_id, "ConnectorID": connector_id, "status": "added"}
    logging.info(f"Connector added to diagram: {result}")
    return result


# ============================================================================
# CREATION OPERATIONS - ATTRIBUTES & OPERATIONS
# ============================================================================


@mcp.tool()
def create_attribute(
    object_guid: str,
    name: str,
    attribute_type: str = "",
    default_value: str = "",
    notes: str = "",
    stereotype: str = "",
    scope: str = "Private",
) -> dict:
    """Create an attribute for an object. Model must be opened with read_only=False.

    Args:
        object_guid: GUID of parent object
        name: Attribute name
        attribute_type: Data type (e.g., 'int', 'String', 'boolean', 'Real')
        default_value: Default value
        notes: Attribute notes
        stereotype: Stereotype (e.g., 'ValueProperty', 'PartProperty')
        scope: Visibility ('Public', 'Private', 'Protected', 'Package')

    Returns:
        dict with created attribute details including ID and ea_guid

    Examples:
        # Create a value property
        attr = create_attribute(
            object_guid=abb['ea_guid'],
            name="speed",
            attribute_type="Real",
            stereotype="ValueProperty",
            scope="Public"
        )

        # Create a part property
        part_prop = create_attribute(
            object_guid=system['ea_guid'],
            name="controller",
            attribute_type="DataController",
            stereotype="PartProperty",
            scope="Private"
        )

        # Create simple attribute with default value
        simple_attr = create_attribute(
            object_guid=class_guid,
            name="count",
            attribute_type="int",
            default_value="0",
            scope="Private"
        )
    """
    _guard_write()
    guid = _normalize_guid(object_guid)
    logging.info(f"create_attribute object_guid={guid} name='{name}' type='{attribute_type}'")

    r = _ensure_reader()

    # Get Object_ID
    obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
    obj_result = r._query(obj_query, (guid,))
    if not obj_result:
        raise ValueError(f"Object not found: {guid}")
    object_id = obj_result[0]["Object_ID"]

    # Generate GUID
    ea_guid = f"{{{str(uuid.uuid4()).upper()}}}"

    # Insert attribute
    query = """
        INSERT INTO t_attribute (
            Object_ID, Name, Type, Default, Notes, Stereotype, Scope, ea_guid
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    r.cur.execute(query, (object_id, name, attribute_type, default_value, notes, stereotype, scope, ea_guid))
    attr_id = r.cur.lastrowid

    result = {
        "ID": attr_id,
        "ea_guid": ea_guid,
        "Object_ID": object_id,
        "Name": name,
        "Type": attribute_type,
        "Default": default_value,
        "Stereotype": stereotype,
        "Scope": scope,
        "status": "created",
    }
    logging.info(f"Attribute created: {result}")
    return result


@mcp.tool()
def create_operation(
    object_guid: str, name: str, return_type: str = "void", notes: str = "", stereotype: str = "", scope: str = "Public"
) -> dict:
    """Create an operation/method for an object. Model must be opened with read_only=False.

    Args:
        object_guid: GUID of parent object
        name: Operation name
        return_type: Return type (e.g., 'void', 'int', 'String', 'Real', 'boolean')
        notes: Operation notes
        stereotype: Stereotype
        scope: Visibility ('Public', 'Private', 'Protected', 'Package')

    Returns:
        dict with created operation details including OperationID and ea_guid

    Examples:
        # Create a public method
        op = create_operation(
            object_guid=abb['ea_guid'],
            name="calculateSpeed",
            return_type="Real",
            scope="Public"
        )

        # Create a void method
        void_op = create_operation(
            object_guid=abb['ea_guid'],
            name="initialize",
            return_type="void",
            notes="Initializes the controller",
            scope="Public"
        )

        # Create a private helper method
        helper = create_operation(
            object_guid=class_guid,
            name="processData",
            return_type="boolean",
            scope="Private"
        )
    """
    _guard_write()
    guid = _normalize_guid(object_guid)
    logging.info(f"create_operation object_guid={guid} name='{name}' return_type='{return_type}'")

    r = _ensure_reader()

    # Get Object_ID
    obj_query = "SELECT Object_ID FROM t_object WHERE ea_guid=?"
    obj_result = r._query(obj_query, (guid,))
    if not obj_result:
        raise ValueError(f"Object not found: {guid}")
    object_id = obj_result[0]["Object_ID"]

    # Generate GUID
    ea_guid = f"{{{str(uuid.uuid4()).upper()}}}"

    # Insert operation
    query = """
        INSERT INTO t_operation (
            Object_ID, Name, Type, Notes, Stereotype, Scope, ea_guid
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    r.cur.execute(query, (object_id, name, return_type, notes, stereotype, scope, ea_guid))
    op_id = r.cur.lastrowid

    result = {
        "OperationID": op_id,
        "ea_guid": ea_guid,
        "Object_ID": object_id,
        "Name": name,
        "Type": return_type,
        "Stereotype": stereotype,
        "Scope": scope,
        "status": "created",
    }
    logging.info(f"Operation created: {result}")
    return result


# ============================================================================
# TRANSACTION MANAGEMENT
# ============================================================================


@mcp.tool()
def commit() -> dict:
    """Commit pending changes to database. Model must be opened with read_only=False.

    Returns:
        dict with commit status

    Example:
        # After making changes
        create_package(name="New Package", parent_id=0)
        create_object(name="New ABB", object_type="Class", package_id=10)

        # Commit all changes
        result = commit()
        print(f"Changes committed to: {result['path']}")
    """
    _guard_write()
    logging.info("Committing changes...")
    _ensure_reader().commit()
    result = {"status": "committed", "path": _MODEL_PATH}
    logging.info(f"Changes committed: {result}")
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    transport, host, port = _get_mcp_init_vars()
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        mcp.run(transport=transport, host=host, port=port)
