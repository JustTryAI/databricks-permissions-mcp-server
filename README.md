# Databricks Permissions MCP Server

A Model Completion Protocol (MCP) server that provides access to Databricks permissions, credentials, and Git credentials via the MCP protocol. This allows LLM-powered tools like Claude to interact with Databricks permissions management systems.

## Features

- **MCP Protocol Support**: Implements the MCP protocol to allow LLMs to manage Databricks permissions
- **Databricks API Integration**: Provides secure access to Databricks permissions REST APIs
- **Permission Management**: Comprehensive tools for managing permissions on various Databricks resources
- **Git Credentials Management**: Tools for creating, listing, updating, and deleting Git credentials
- **Async Support**: Built with asyncio for efficient operation

## Available Tools

The Databricks Permissions MCP Server exposes the following tools:

### Permissions Management
- **get_permissions**: Get permissions for a Databricks object
- **set_permissions**: Set permissions for a Databricks object
- **update_permissions**: Update permissions for a Databricks object
- **get_permission_levels**: Get available permission levels for a Databricks object type

### Resource-Specific Permissions
- **get_cluster_permissions**: Get permissions for a cluster
- **set_cluster_permissions**: Set permissions for a cluster
- **update_cluster_permissions**: Update permissions for a cluster
- **get_job_permissions**: Get permissions for a job
- **set_job_permissions**: Set permissions for a job
- **get_warehouse_permissions**: Get permissions for a SQL warehouse
- **get_workspace_object_permissions**: Get permissions for a workspace object (notebooks, directories)

### Service Principals
- **list_service_principals**: List all service principals in the workspace
- **get_service_principal**: Get details of a specific service principal
- **create_service_principal**: Create a new service principal
- **update_service_principal**: Update an existing service principal
- **delete_service_principal**: Delete a service principal

### Unity Catalog Permissions
- **get_catalog_permissions**: Get permissions for a Unity Catalog catalog
- **get_schema_permissions**: Get permissions for a Unity Catalog schema
- **get_table_permissions**: Get permissions for a Unity Catalog table

### Git Credentials Management
- **list_git_credentials**: List all Git credentials
- **create_git_credential**: Create a new Git credential
- **update_git_credential**: Update an existing Git credential
- **delete_git_credential**: Delete a Git credential

## Installation

### Prerequisites

- Python 3.10 or higher
- MCP-compatible client (e.g., Claude Desktop)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/databricks-permissions-mcp-server.git
   cd databricks-permissions-mcp-server
   ```

2. Set up the project:
   ```bash
   # Create and activate virtual environment
   python -m venv .venv
   
   # On Windows
   .\.venv\Scripts\activate
   
   # On Linux/Mac
   source .venv/bin/activate
   
   # Install dependencies in development mode
   pip install -e .
   ```

3. Set up environment variables:
   ```bash
   # Windows
   set DATABRICKS_HOST=https://your-databricks-instance.azuredatabricks.net
   set DATABRICKS_TOKEN=your-personal-access-token
   
   # Linux/Mac
   export DATABRICKS_HOST=https://your-databricks-instance.azuredatabricks.net
   export DATABRICKS_TOKEN=your-personal-access-token
   ```

   You can also create an `.env` file based on the `.env.example` template.

## Running the MCP Server

To start the MCP server, run:

```bash
# Windows
.\start_mcp_server.ps1

# Linux/Mac
./start_mcp_server.sh
```

## Using with Claude Desktop

1. In Claude Desktop, click the "+" button to add a new tool
2. Select "Custom command"
3. Enter a name like "Databricks Permissions"
4. For the command, enter: `python -m src.server.databricks_permissions_mcp_server`
5. Click "Save"
6. You can now ask Claude to perform tasks like:
   - "List all Git credentials in Databricks"
   - "Show permissions for cluster X"
   - "Update permissions for job Y to give user Z 'CAN_MANAGE' access"

## Project Structure

```
databricks-permissions-mcp-server/
├── src/                             # Source code
│   ├── api/                         # Databricks API clients
│   │   ├── permissions.py           # Permissions API client
│   │   ├── service_principals.py    # Service principals API client
│   │   ├── unity_catalog.py         # Unity Catalog API client
│   │   ├── shares.py                # Delta Sharing API client
│   │   └── git_credentials.py       # Git credentials API client
│   ├── core/                        # Core functionality
│   ├── server/                      # Server implementation
│   │   ├── databricks_permissions_mcp_server.py # Main MCP server
│   │   └── app.py                   # FastAPI app for tests
│   └── cli/                         # Command-line interface
├── tests/                           # Test directory
├── scripts/                         # Helper scripts
└── pyproject.toml                   # Project configuration
```

## Development

### Code Standards

- Python code follows PEP 8 style guide with a maximum line length of 100 characters
- All classes, methods, and functions should have Google-style docstrings
- Type hints are required for all code except tests

## Testing

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest --cov=src tests/ --cov-report=term-missing
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 