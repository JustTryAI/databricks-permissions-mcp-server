"""
Entry point module for the Databricks Permissions MCP Server.
"""

from src.server.databricks_permissions_mcp_server import main

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
