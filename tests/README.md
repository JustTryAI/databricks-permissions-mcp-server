# Databricks Permissions MCP Server Tests

This directory contains tests for the Databricks Permissions MCP server, focusing on permissions and credentials management functionality.

## Test Files

- `test_tools.py`: Tests for individual tools in the Databricks Permissions MCP server
- `test_direct.py`: Tests for direct usage of the server without going through the MCP protocol
- `test_mcp_client.py`: Tests for using the server through the MCP protocol
- `test_mcp_server.py`: Tests for the MCP server implementation

## Running Tests

To run the tests, use the following command from the project root directory:

```bash
# Run all tests
pytest tests/

# Run a specific test file
pytest tests/test_tools.py

# Run with verbose output
pytest -v tests/

# Run with coverage report
pytest --cov=src tests/ --cov-report=term-missing
```

## Test Coverage

The tests cover the following functionality:

### Permissions Management
- List service principals
- List Git credentials
- Get schema permissions
- Get cluster permissions
- Get permission levels
- Set permissions
- Update permissions

### MCP Protocol
- Server initialization
- Tool registration
- Tool execution
- Error handling

## Writing New Tests

When writing new tests, follow these guidelines:

1. Focus on permissions and credentials management functionality
2. Use descriptive test names that indicate what is being tested
3. Include assertions to verify the expected behavior
4. Add logging to help with debugging
5. Handle exceptions appropriately

Example test function:

```python
async def test_get_permissions():
    """Test the get_permissions tool."""
    logger.info("Testing get_permissions tool")
    server = DatabricksPermissionsMCPServer()
    
    result = await server.call_tool("get_permissions", {
        "object_type": "clusters",
        "object_id": "123456789"
    })
    
    # Check if result is valid
    assert isinstance(result, Dict), "Result should be a Dict"
    assert "access_control_list" in result, "Result should contain access_control_list"
    logger.info(f"Result: {json.dumps(result, indent=2)}") 