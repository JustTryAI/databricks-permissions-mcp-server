"""
Tests for individual tools in the Databricks Permissions MCP server.

This module contains tests for each individual tool in the Databricks Permissions MCP server,
focusing on permissions and credentials management.
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any, List

from src.server.databricks_permissions_mcp_server import DatabricksPermissionsMCPServer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_list_service_principals():
    """Test the list_service_principals tool."""
    logger.info("Testing list_service_principals tool")
    server = DatabricksPermissionsMCPServer()
    
    result = await server.call_tool("list_service_principals", {})
    
    # Check if result is valid
    assert isinstance(result, List), "Result should be a List"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def test_list_git_credentials():
    """Test the list_git_credentials tool."""
    logger.info("Testing list_git_credentials tool")
    server = DatabricksPermissionsMCPServer()
    
    result = await server.call_tool("list_git_credentials", {})
    
    # Check if result is valid
    assert isinstance(result, List), "Result should be a List"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def test_get_schema_permissions():
    """Test the get_schema_permissions tool."""
    logger.info("Testing get_schema_permissions tool")
    server = DatabricksPermissionsMCPServer()
    
    result = await server.call_tool("get_schema_permissions", {"schema_id": "123456798"})
    
    # Check if result is valid
    assert isinstance(result, Dict), "Result should be a Dict"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def test_get_cluster_permissions():
    """Test the get_cluster_permissions tool."""
    logger.info("Testing get_cluster_permissions tool")
    server = DatabricksPermissionsMCPServer()
    
    result = await server.call_tool("get_cluster_permissions", {"cluster_id": "123456789"})
    
    # Check if result is valid
    assert isinstance(result, Dict), "Result should be a Dict"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def test_get_permission_levels():
    """Test the get_permission_levels tool."""
    logger.info("Testing get_permission_levels tool")
    server = DatabricksPermissionsMCPServer()
    
    result = await server.call_tool("get_permission_levels", {"object_type": "clusters"})
    
    # Check if result is valid
    assert isinstance(result, Dict), "Result should be a Dict"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def test_set_permissions():
    """Test the set_permissions tool."""
    logger.info("Testing set_permissions tool")
    server = DatabricksPermissionsMCPServer()
    
    access_control_list = [
        {
            "user_name": "test-user@example.com",
            "permission_level": "CAN_MANAGE"
        }
    ]
    
    result = await server.call_tool("set_permissions", {
        "object_type": "clusters",
        "object_id": "123456789",
        "access_control_list": access_control_list
    })
    
    # Check if result is valid
    assert isinstance(result, Dict), "Result should be a Dict"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def test_update_permissions():
    """Test the update_permissions tool."""
    logger.info("Testing update_permissions tool")
    server = DatabricksPermissionsMCPServer()
    
    access_control_list = [
        {
            "user_name": "test-user@example.com",
            "permission_level": "CAN_MANAGE"
        }
    ]
    
    result = await server.call_tool("update_permissions", {
        "object_type": "clusters",
        "object_id": "123456789",
        "access_control_list": access_control_list
    })
    
    # Check if result is valid
    assert isinstance(result, Dict), "Result should be a Dict"
    logger.info(f"Result: {json.dumps(result, indent=2)}")


async def run_tests():
    """Run all tests."""
    logger.info("Running tests for Databricks Permissions MCP server tools")
    
    tests = [
        test_list_service_principals(),
        test_list_git_credentials(),
        test_get_schema_permissions(),
        test_get_cluster_permissions(),
        test_get_permission_levels(),
        test_set_permissions(),
        test_update_permissions()
    ]
    
    await asyncio.gather(*tests)
    logger.info("All tests completed")


if __name__ == "__main__":
    asyncio.run(run_tests()) 