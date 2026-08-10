# Database EA MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server that provides direct access to Enterprise Architect `.qea` / `.qeax` SQLite models.
## Overview

The Database EA MCP Server enables AI assistants to interact with Enterprise Architect repositories by directly accessing the SQLite database files. This server loads an Enterprise Architect SQLite-based repository file (`.qea` / `.qeax`) and exposes structured MCP tools for exploring and manipulating model content including packages, elements, connectors, and diagrams. It is designed for automation, analysis, and selective generation activities where the EA UI is not required (headless).

### Limitations

1. No synchronization with a simultaneously open EA GUI session (changes may not appear until reload in EA)
2. UI-specific interactions (opening diagrams visually, layout algorithms, EA prompts) are not available
3. Large models may require memory and time for broader scans; prefer targeted queries
4. Destructive SQL operations restricted: DELETE, DROP, TRUNCATE, and ALTER are blocked in `custom_query()` for safety. Use EA GUI for these operations.

## Getting Started

### Prerequisites

- Github Copilot Subscription ([GH-Copilot Access](https://docs.boschdevcloud.com/userguide/index.html?id=GHCopilot_getstarted))
- [WSL setup](https://inside-docupedia.bosch.com/confluence/x/37HoYQ)
- Access to [PMT MCP servers](https://artifactory.boschdevcloud.com/ui/repos/tree/General/pmt-mcp-servers-docker-local) ([Get access to Artifactory](../../README.md#access-to-pmt-artifactory-repository))
- Local Enterprise Architect `.qea` / `.qeax` repository file accessible to the server
- File permissions to read/write the EA file (write mode only if you intend to modify)

### MCP Client Integration

1. The easiest way to integrate the MCP server with your VSCode GitHub Copilot is by adding a configuration file `.vscode/mcp.json`. Use this [`mcp.json`](mcp.json) as a reference and replace all placeholders.

2. Start the Docker version MCP server after adding `.vscode/mcp.json`. It is ready to use now.

3. Check out the [`../../README.md`](../../README.md) to find out more about [`Running MCP Servers using uv/python`](../../README.md#running-mcp-servers-for-development)

### Configuration

Provide needed environment variables else default values are considered.

| Variable | Allowed Values | Default | Effect |
|----------|----------------|---------|--------|
| `TRANSPORT` | `stdio`, `http`, `streamable-http`, `sse` | `stdio` | Communication method. `stdio`  is **recommended for GitHub Copilot Chat integration**. |
| `HOST` | e.g. `127.0.0.1`, `0.0.0.0`, `localhost` | `127.0.0.1` (ignored for `stdio`) | Bind address for non-stdio transports. |
| `HOST_PORT` | Integer TCP port which is free (e.g. `8000`) | `8000` (ignored for `stdio`) | Listening port for non-stdio transports. |

Behavior: If `TRANSPORT` is empty / `-` / `null` it is coerced to `stdio` and host/port are ignored. Any other valid value starts a network server on `HOST:HOST_PORT`.

**Note:** When using WSL with Docker, your host home directory is automatically mounted to the container's home directory, making your local EA files available.

### Usage Examples

Once connected to VSCode GitHub Copilot chat or an MCP-compatible client, you can interact with your EA models using natural language.<br>Try these examples in your VSCode GitHub Copilot chat:  (Use premium models such as GPT-5, Claude Sonnet 4.5 etc. in to get best results)

#### Example 1: Basic Read Operations
```
Open this model /path/to/your/model.qeax.
Get count of diagrams in this model.
Get all types of objects present in this model and thier count
Get list of elements with names ending with _CPF.
Get count of ABB in this model.
```

#### Example 2: Creating Structure
```
Open this model /path/to/your/model.qeax with read_only=False.
Create a package named "NewComponents" under PackageName.
Create a Class element named "MyComponent" in the NewComponents package with stereotype "Component".
Save the changes.
```

#### Example 3: Working with Ports and Connectors
```
Open this model /path/to/your/model.qeax with read_only=False.
Get object with GUID {ABC123-...}.
Create a port named "InputPort" under element {ABC123-...} with classifier {DEF456-...}.
Create a connector from {ABC123-...} to {GHI789-...} of type Association.
Save the changes.
```

#### Example 4: Diagram Creation
```
Open this model /path/to/your/model.qeax with read_only=False.
Create a diagram named "Component Overview" in package Root/Views of type Component.
Add element {ABC123-...} to the diagram at position left=100, top=100.
Add diagram connector between {ABC123-...} and {DEF456-...} of type Dependency.
Save the changes.
```

#### Example 5: Advanced Query
```
Open this model /path/to/your/model.qeax.
Execute select query: SELECT Name, Stereotype FROM t_object WHERE Object_Type='Class' LIMIT 10.
Get all connectors where source is {ABC123-...}.
```

The AI assistant will translate these natural language requests into structured database operations and execute them against your EA SQLite model.

### Features

The server provides comprehensive MCP tools for EA model management. Write tools require opening the model with `open_model(..., read_only=False)`.

**Model Management**:
- `open_model` - Open an EA `.qea` / `.qeax` / `.sqlite` model **(must call first)**
- `alive_check` - Check if the current model connection is alive
- `commit` - Commit pending database changes (write mode)

**Search & Query**:
- `search_objects` - Fast filtered search (name/object_type/stereotype/package) with truncation detection
- `custom_query` - Execute raw SQL statements with safety limits (COUNT first recommended)
- `get_object_summary` - Lightweight list of objects (GUID, name, type, stereotype)

**Object Management**:
- `get_object` - Full enriched object details by GUID
- `get_objects` - Paginated enriched objects filtered by package and/or parent
- `create_object` - Create a model element (Class/Component/Part/Port/etc.)
- `update_object` - Update element name, notes, stereotype, and/or status

**Package Management**:
- `get_packages` - Paginated packages (hierarchy support via parent_id)
- `create_package` - Create a package (inserts into `t_package` and corresponding `t_object`)

**Connector Management**:
- `get_connectors` - Paginated connectors filtered by source GUID, target GUID, and/or type
- `create_connector` - Create a relationship between two objects
- `add_connector_to_diagram` - Show an existing connector on a diagram

**Attributes & Operations**:
- `get_attributes` - Paginated attributes for an object
- `create_attribute` - Create an attribute/property on an object
- `get_operations` - Paginated operations for an object
- `create_operation` - Create an operation/method on an object

**Tagged Values**:
- `get_tagged_values` - Paginated tagged values for an object
- `update_tagged_value` - Update an existing tagged value (write mode)
- `add_tagged_value` - Add a new tagged value (write mode)

**Diagram Management**:
- `get_diagrams` - Paginated diagrams (optionally filter by package)
- `create_diagram` - Create a diagram in a package
- `add_object_to_diagram` - Place an existing object on a diagram with coordinates

### Troubleshooting

| Symptom | Possible Cause | Suggested Action |
|---------|----------------|------------------|
| `RuntimeError: Model not opened` | Forgot to call `open_model` first | Call `open_model` with valid path |
| `PermissionError` on write tool | Model opened with `read_only=True` | Reopen with `read_only=False` |
| Empty result for GUID | GUID formatting mismatch | Use full EA GUID or let server normalize braces |
| Slow `get_objects` | Large package scope | Add filters (parent/package) or direct GUID queries |
| `ValueError` in connector creation | Source/target GUID invalid | Verify element existence via `get_object` |
| Connection issues | Database file locked or inaccessible | Ensure EA is not locking the file, check file permissions |
| Unexpected or missing data from `get_*` | Generic query too broad or filter mismatch | Refine prompt with specific object type, stereotype, or package path |
| Results inconsistent or incomplete | AI model limitations with complex queries | Switch to premium models (GPT-5, Claude Sonnet 4.5 etc.) for better reasoning |

## Related Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [BOSCH OneIDM](https://oneidm.bosch.com/oneidm/html/rbwebshop/#/start/home)
