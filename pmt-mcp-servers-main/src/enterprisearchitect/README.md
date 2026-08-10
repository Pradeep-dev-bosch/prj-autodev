# Enterprise Architect MCP Server

A [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) server implementation for Enterprise Architect, offering multiple server options.

## Overview

The Enterprise Architect MCP Server enables AI assistants to interact with EA repositories through various interfaces. This document provides a basic overview of the available MCP server options. For detailed setup instructions and usage, refer to the respective README files in each server's folder.

## Available MCP Servers

| # | MCP Server              | Description                                                                 | Folder                                      | Details                                                                                      |
|---|-------------------------|-----------------------------------------------------------------------------|---------------------------------------------|----------------------------------------------------------------------------------------------|
| 1 | **COM EA MCP Server**      | Integration with EA desktop via COM interface.                              | [`comeamcpserver/`](comeamcpserver/)        | See [`comeamcpserver/README.md`](comeamcpserver/README.md)                                   |
| 2 | **Database EA MCP Server** | Direct read/write access to `.qea` / `.qeax` via SQLite            | [`dbeamcpserver/`](dbeamcpserver/)          | See [`dbeamcpserver/README.md`](dbeamcpserver/README.md)                                     | 
| 3 | **Official EA MCP Server** | Official server by Sparx Systems for EA integration.                        | [`officialeamcpserver/`](officialeamcpserver/) | See [Official MCP server page](https://www.sparxsystems.jp/en/MCP/), [`officialeamcpserver/README.md`](officialeamcpserver/README.md) |
| 4 | **WebEA MCP Server**    | Integrates with WebEA via EA OSLC API.                                      | [`webeamcpserver/`](webeamcpserver/)        | See [`webeamcpserver/README.md`](webeamcpserver/README.md)                                   |

## Choosing the Right MCP Server

| Server Type                | Best For                                  | Input Needed                | Headless Supported | EA App GUI Interaction Supported | Notes                                      |
|----------------------------|-------------------------------------------|-----------------------------|--------------------|--------------------|--------------------------------------------|
| **COM EA MCP Server**         | Desktop EA tasks (alternative to Official MCP Server) | Model should be opened in EA desktop application   | No | Yes | Recommended to use Official MCP Server if installation requirements are met; otherwise, COM MCP Server is a suitable alternative |
| **Database EA MCP Server** | Direct repository access, headless ops    | EA Model file (`.qea` / `.qeax`) path   | Yes                | No | Read-only by default, supports raw SQL     |
| **Official EA MCP Server**    | Desktop EA tasks | Model should be opened in EA desktop application | No                 | Yes | Provided by Sparx Systems                  |
| **WebEA MCP Server**       | WebEA stored EA models                 | WebEA server endpoint and model name          | Yes                | No | Uses OSLC API, suitable for web workflows  |


