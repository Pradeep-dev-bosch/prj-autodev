# Bug Knowledge Graph MCP Server

An MCP server that provides a **persistent institutional memory** for bug analysis.
It stores root cause analyses, fix descriptions, affected components, and Gerrit change links
in a Stardog RDF knowledge graph using SPARQL.

## Why a Knowledge Graph?

- Every fix creates a record with rich semantic relationships (component → issue → fix → change)
- Future debugging of the same component retrieves all historic precedents
- Enables cross-component root-cause pattern detection via SPARQL queries
- Fully queryable by any SPARQL-capable tool

## Knowledge Graph Schema

```
kg:BugRecord
  ├── kg:hasIssueKey        (JIRA key, e.g. "PROJ-123")
  ├── kg:hasSummary         (short description)
  ├── kg:hasRootCause       (detailed root cause analysis)
  ├── kg:hasComponent       (software component name)
  ├── kg:hasAffectedFile    (0..N file paths)
  ├── kg:hasFixDescription  (what was changed and why)
  ├── kg:hasFixStatus       (open | proposed | merged | abandoned)
  ├── kg:hasGerritChangeId  (Gerrit change ID or Change-Id)
  ├── kg:hasNotes           (free-text notes)
  ├── kg:hasCreatedDate     (ISO 8601 timestamp)
  └── kg:hasUpdatedDate     (ISO 8601 timestamp)
```

## Available Tools

| Tool | Description |
|------|-------------|
| `store_bug_analysis` | Store or overwrite a complete bug analysis record |
| `update_fix_status` | Update only the fix status / Gerrit ID of an existing record |
| `get_issue_knowledge` | Retrieve all stored knowledge about one JIRA issue |
| `query_similar_issues` | Find similar past bugs in the same component |
| `get_component_history` | All bug/fix history for a component |
| `get_all_open_issues` | All issues with status 'open' or 'proposed' |
| `sparql_query` | Run arbitrary SPARQL SELECT queries |
| `sparql_update` | Run arbitrary SPARQL UPDATE statements |

## Setup

### Pre-requisite: Stardog Database

```bash
# Create the database in Stardog (one-time)
stardog-admin db create -n bug_knowledge_graph
```

### Configuration

| Variable | Description |
|----------|-------------|
| `STARDOG_ENDPOINT` | URL of Stardog server (e.g. `http://localhost:5820`) |
| `STARDOG_USERNAME` | Stardog username (default: `admin`) |
| `STARDOG_PASSWORD` | Stardog password |
| `STARDOG_DATABASE` | Database name (default: `bug_knowledge_graph`) |
| `KG_NAMESPACE` | RDF namespace (default: `http://bugknowledge.org/`) |

### Running with uv (stdio)

```bash
cd pmt-mcp-servers-main/src/knowledge_graph
uv run kgmcpserver.py
```

### Running with Docker

```bash
docker build -t bug-kg-mcp-server .
docker run -i --rm \
  -e STARDOG_ENDPOINT=http://localhost:5820 \
  -e STARDOG_USERNAME=admin \
  -e STARDOG_PASSWORD=secret \
  bug-kg-mcp-server
```
