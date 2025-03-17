#!/usr/bin/env python
"""
Databricks Permissions MCP Server - MCP Client Usage Example

This example demonstrates how to use the Databricks Permissions MCP server
through the MCP protocol. It shows how to connect to the server and call
its tools to manage permissions and credentials.
"""

import asyncio
import json
import logging
import os
import sys
import subprocess
from typing import Any, Dict, List, Optional

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
    print_section_header("Databricks Permissions MCP Server - MCP Client Usage Example")
    
    # Start the MCP server in a separate process
    server_process = subprocess.Popen(
        [sys.executable, "-m", "src.server.databricks_permissions_mcp_server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Wait a moment for the server to start
        await asyncio.sleep(2)
        
        # Initialize the MCP protocol
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {}
            }
        }
        server_process.stdin.write(json.dumps(init_message) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        print(f"Initialize response: {json.dumps(response, indent=2)}")
        
        # List available tools
        list_tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "listTools",
            "params": {}
        }
        server_process.stdin.write(json.dumps(list_tools_message) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        print(f"List tools response: {json.dumps(response, indent=2)}")
        
        # Call the list_service_principals tool
        print_section_header("List Service Principals")
        call_tool_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "callTool",
            "params": {
                "name": "list_service_principals",
                "input": {}
            }
        }
        server_process.stdin.write(json.dumps(call_tool_message) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        print(f"List service principals response: {json.dumps(response, indent=2)}")
        
        # Call the list_git_credentials tool
        print_section_header("List Git Credentials")
        call_tool_message = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "callTool",
            "params": {
                "name": "list_git_credentials",
                "input": {}
            }
        }
        server_process.stdin.write(json.dumps(call_tool_message) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        print(f"List git credentials response: {json.dumps(response, indent=2)}")
        
        # Call the get_schema_permissions tool
        print_section_header("Get Schema Permissions")
        call_tool_message = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "callTool",
            "params": {
                "name": "get_schema_permissions",
                "input": {"schema_id": "123456798"}
            }
        }
        server_process.stdin.write(json.dumps(call_tool_message) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        print(f"Get schema permissions response: {json.dumps(response, indent=2)}")
        
        # Call the get_cluster_permissions tool
        print_section_header("Get Cluster Permissions")
        call_tool_message = {
            "jsonrpc": "2.0",
            "id": 6,
            "method": "callTool",
            "params": {
                "name": "get_cluster_permissions",
                "input": {"cluster_id": "123456789"}
            }
        }
        server_process.stdin.write(json.dumps(call_tool_message) + "\n")
        server_process.stdin.flush()
        
        # Read the response
        response = json.loads(server_process.stdout.readline())
        print(f"Get cluster permissions response: {json.dumps(response, indent=2)}")
        
    finally:
        # Shutdown the server
        shutdown_message = {
            "jsonrpc": "2.0",
            "id": 7,
            "method": "shutdown",
            "params": {}
        }
        server_process.stdin.write(json.dumps(shutdown_message) + "\n")
        server_process.stdin.flush()
        
        # Wait for the server to shut down
        server_process.wait(timeout=5)

if __name__ == "__main__":
    asyncio.run(main()) 