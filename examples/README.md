# Databricks Permissions MCP Server Examples

This directory contains examples of how to use the Databricks Permissions MCP server to manage permissions and credentials in Databricks.

## Available Examples

- `direct_usage.py`: Demonstrates how to use the server directly without going through the MCP protocol
- `mcp_client_usage.py`: Demonstrates how to use the server through the MCP protocol

## Running the Examples

### Prerequisites

Before running the examples, make sure you have:

1. Set up your Databricks credentials in environment variables:
   ```bash
   # Windows
   set DATABRICKS_HOST=https://your-databricks-instance.azuredatabricks.net
   set DATABRICKS_TOKEN=your-personal-access-token
   
   # Linux/Mac
   export DATABRICKS_HOST=https://your-databricks-instance.azuredatabricks.net
   export DATABRICKS_TOKEN=your-personal-access-token
   ```

2. Installed the required dependencies:
   ```bash
   pip install -e ..
   ```

### Direct Usage Example

This example shows how to use the server directly without going through the MCP protocol:

```bash
python direct_usage.py
```

The example will:
1. List all service principals
2. List all Git credentials
3. Get permissions for a schema (using ID "123456798")
4. Get permissions for a cluster (using ID "123456789")
5. Get permission levels for clusters

### MCP Client Usage Example

This example shows how to use the server through the MCP protocol:

```bash
python mcp_client_usage.py
```

The example will:
1. Start the MCP server
2. Initialize the MCP protocol
3. List available tools
4. Call the list_service_principals tool
5. Call the list_git_credentials tool
6. Call the get_schema_permissions tool (using ID "123456798")
7. Call the get_cluster_permissions tool (using ID "123456789")
8. Shutdown the server

## Example Output

The examples will output the results of each operation in a formatted way. For example:

```
--------------------------------------------------------------------------------
List Service Principals
--------------------------------------------------------------------------------
[
  {
    "application_id": "00000000-0000-0000-0000-000000000000",
    "display_name": "Example Service Principal",
    "id": "1234567890"
  }
]

--------------------------------------------------------------------------------
List Git Credentials
--------------------------------------------------------------------------------
[
  {
    "credential_id": "1234567890",
    "git_provider": "github",
    "git_username": "example-user"
  }
]
```

## Using in Your Own Code

You can use these examples as a starting point for your own code. The key components are:

1. Creating an instance of the `DatabricksPermissionsMCPServer` class
2. Calling the appropriate tools with the required parameters
3. Processing the results 