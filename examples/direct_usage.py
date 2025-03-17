#!/usr/bin/env python
"""
Databricks Permissions MCP Server - Direct Usage Example

This example demonstrates how to directly use the Databricks Permissions MCP server
without going through the MCP protocol. It shows how to instantiate the
server class and call its methods directly to manage permissions and credentials.
"""

import json
import logging
import os
import sys
from typing import Any, Dict, List, Optional

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.server.databricks_permissions_mcp_server import DatabricksPermissionsMCPServer

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def print_section_header(title: str) -> None:
    """Print a section header with the given title."""
    print(f"\n{'-' * 80}")
    print(f"{title}")
    print(f"{'-' * 80}")

async def main() -> None:
    """Run the example."""
    # Create an instance of the server
    server = DatabricksPermissionsMCPServer()
    
    # List Service Principals
    print_section_header("List Service Principals")
    result = await server.call_tool("list_service_principals", {})
    print(json.dumps(result, indent=2))
    
    # List Git Credentials
    print_section_header("List Git Credentials")
    result = await server.call_tool("list_git_credentials", {})
    print(json.dumps(result, indent=2))
    
    # Get Schema Permissions
    print_section_header("Get Schema Permissions")
    result = await server.call_tool("get_schema_permissions", {"schema_id": "123456798"})
    print(json.dumps(result, indent=2))
    
    # Get Cluster Permissions
    print_section_header("Get Cluster Permissions")
    result = await server.call_tool("get_cluster_permissions", {"cluster_id": "123456789"})
    print(json.dumps(result, indent=2))
    
    # Get Permission Levels for Clusters
    print_section_header("Get Permission Levels for Clusters")
    result = await server.call_tool("get_permission_levels", {"object_type": "clusters"})
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 