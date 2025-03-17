"""
Databricks Permissions MCP Server

This module implements a standalone MCP server that provides tools for interacting
with Databricks permissions, credentials, and Git credentials APIs. It follows the Model Context Protocol standard, 
communicating via stdio and directly connecting to Databricks when tools are invoked.
"""

import asyncio
import json
import logging
import sys
import os
from typing import Any, Dict, List, Optional, Union, cast

from mcp.server import FastMCP
from mcp.types import TextContent
from mcp.server.stdio import stdio_server

from src.api import service_principals, unity_catalog, permissions, shares, git_credentials
from src.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    filename="databricks_permissions_mcp.log",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DatabricksPermissionsMCPServer(FastMCP):
    """An MCP server for Databricks Permissions and Credentials APIs."""

    def __init__(self):
        """Initialize the Databricks Permissions MCP server."""
        super().__init__(name="databricks-permissions-mcp", 
                         version="1.0.0", 
                         instructions="Use this server to manage Databricks permissions and credentials")
        logger.info("Initializing Databricks Permissions MCP server")
        logger.info(f"Databricks host: {settings.DATABRICKS_HOST}")
        
        # Register tools
        self._register_tools()
    
    def _register_tools(self):
        """Register all Databricks Permissions MCP tools."""
        
        # Service Principal tools
        @self.tool(
            name="create_service_principal",
            description="Create a service principal with parameters: display_name (required), application_id (required), allow_cluster_create (optional)",
        )
        async def create_service_principal(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Creating service principal with params: {params}")
            try:
                display_name = params.get("display_name")
                application_id = params.get("application_id")
                allow_cluster_create = params.get("allow_cluster_create", False)
                result = await service_principals.create_service_principal(display_name, application_id, allow_cluster_create)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error creating service principal: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="list_service_principals",
            description="List service principals with parameters: page_size (optional), page_token (optional)",
        )
        async def list_service_principals(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing service principals with params: {params}")
            try:
                page_size = params.get("page_size")
                page_token = params.get("page_token")
                result = await service_principals.list_service_principals(page_size, page_token)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing service principals: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_service_principal",
            description="Get details of a service principal with parameter: id (required)",
        )
        async def get_service_principal(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting service principal with params: {params}")
            try:
                sp_id = params.get("id")
                result = await service_principals.get_service_principal(sp_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting service principal: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="update_service_principal",
            description="Update a service principal with parameters: id (required), display_name (optional), allow_cluster_create (optional)",
        )
        async def update_service_principal(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Updating service principal with params: {params}")
            try:
                sp_id = params.get("id")
                display_name = params.get("display_name")
                allow_cluster_create = params.get("allow_cluster_create")
                result = await service_principals.update_service_principal(sp_id, display_name, allow_cluster_create)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error updating service principal: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="delete_service_principal",
            description="Delete a service principal with parameter: id (required)",
        )
        async def delete_service_principal(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Deleting service principal with params: {params}")
            try:
                sp_id = params.get("id")
                result = await service_principals.delete_service_principal(sp_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error deleting service principal: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        # Storage Credentials operations
        @self.tool(
            name="create_storage_credential",
            description="Create a storage credential in Unity Catalog with parameters: name (required), aws_iam_role (optional), azure_service_principal (optional), comment (optional)",
        )
        async def create_storage_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Creating storage credential with params: {params}")
            try:
                name = params.get("name")
                aws_iam_role = params.get("aws_iam_role")
                azure_service_principal = params.get("azure_service_principal")
                comment = params.get("comment")
                result = await unity_catalog.create_storage_credential(name, aws_iam_role, azure_service_principal, comment)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error creating storage credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_storage_credential",
            description="Get details of a storage credential with parameter: name (required)",
        )
        async def get_storage_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting storage credential with params: {params}")
            try:
                name = params.get("name")
                result = await unity_catalog.get_storage_credential(name)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting storage credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="update_storage_credential",
            description="Update a storage credential with parameters: name (required), new_name (optional), aws_iam_role (optional), azure_service_principal (optional), comment (optional)",
        )
        async def update_storage_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Updating storage credential with params: {params}")
            try:
                name = params.get("name")
                new_name = params.get("new_name")
                aws_iam_role = params.get("aws_iam_role")
                azure_service_principal = params.get("azure_service_principal")
                comment = params.get("comment")
                result = await unity_catalog.update_storage_credential(name, new_name, aws_iam_role, azure_service_principal, comment)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error updating storage credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="delete_storage_credential",
            description="Delete a storage credential with parameter: name (required)",
        )
        async def delete_storage_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Deleting storage credential with params: {params}")
            try:
                name = params.get("name")
                result = await unity_catalog.delete_storage_credential(name)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error deleting storage credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="list_storage_credentials",
            description="List storage credentials in Unity Catalog",
        )
        async def list_storage_credentials(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing storage credentials with params: {params}")
            try:
                result = await unity_catalog.list_storage_credentials()
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing storage credentials: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        # Credential operations
        @self.tool(
            name="create_credential",
            description="Create a credential in Unity Catalog with parameters: name (required), credential_type (required), credential_info (required), comment (optional)",
        )
        async def create_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Creating credential with params: {params}")
            try:
                name = params.get("name")
                credential_type = params.get("credential_type")
                credential_info = params.get("credential_info")
                comment = params.get("comment")
                result = await unity_catalog.create_credential(name, credential_type, credential_info, comment)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error creating credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="list_credentials",
            description="List credentials in Unity Catalog with parameter: credential_type (optional)",
        )
        async def list_credentials(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Listing credentials with params: {params}")
            try:
                credential_type = params.get("credential_type")
                result = await unity_catalog.list_credentials(credential_type)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing credentials: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="update_credential",
            description="Update a credential with parameters: name (required), new_name (optional), credential_info (optional), comment (optional)",
        )
        async def update_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Updating credential with params: {params}")
            try:
                name = params.get("name")
                new_name = params.get("new_name")
                credential_info = params.get("credential_info")
                comment = params.get("comment")
                result = await unity_catalog.update_credential(name, new_name, credential_info, comment)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error updating credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="delete_credential",
            description="Delete a credential with parameter: name (required)",
        )
        async def delete_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Deleting credential with params: {params}")
            try:
                name = params.get("name")
                result = await unity_catalog.delete_credential(name)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error deleting credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        # Permission management tools
        @self.tool(
            name="get_permissions",
            description="Get permissions for a Databricks object with parameters: object_type (required, e.g., 'clusters', 'jobs'), object_id (required)",
        )
        async def get_object_permissions(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting permissions with params: {params}")
            try:
                object_type = params.get("object_type")
                object_id = params.get("object_id")
                
                if not object_type:
                    return [{"text": json.dumps({"error": "object_type is required"})}]
                if not object_id:
                    return [{"text": json.dumps({"error": "object_id is required"})}]
                
                result = await permissions.get_permissions(object_type, object_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="set_permissions",
            description="Set permissions for a Databricks object with parameters: object_type (required), object_id (required), access_control_list (required)",
        )
        async def set_object_permissions(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Setting permissions with params: {params}")
            try:
                object_type = params.get("object_type")
                object_id = params.get("object_id")
                access_control_list = params.get("access_control_list")
                
                if not object_type:
                    return [{"text": json.dumps({"error": "object_type is required"})}]
                if not object_id:
                    return [{"text": json.dumps({"error": "object_id is required"})}]
                if not access_control_list:
                    return [{"text": json.dumps({"error": "access_control_list is required"})}]
                
                result = await permissions.set_permissions(object_type, object_id, access_control_list)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error setting permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="update_permissions",
            description="Update permissions for a Databricks object with parameters: object_type (required), object_id (required), access_control_list (required)",
        )
        async def update_object_permissions(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Updating permissions with params: {params}")
            try:
                object_type = params.get("object_type")
                object_id = params.get("object_id")
                access_control_list = params.get("access_control_list")
                
                if not object_type:
                    return [{"text": json.dumps({"error": "object_type is required"})}]
                if not object_id:
                    return [{"text": json.dumps({"error": "object_id is required"})}]
                if not access_control_list:
                    return [{"text": json.dumps({"error": "access_control_list is required"})}]
                
                result = await permissions.update_permissions(object_type, object_id, access_control_list)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error updating permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_permission_levels",
            description="Get available permission levels for a Databricks object type with parameter: object_type (required)",
        )
        async def get_object_permission_levels(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting permission levels with params: {params}")
            try:
                object_type = params.get("object_type")
                
                if not object_type:
                    return [{"text": json.dumps({"error": "object_type is required"})}]
                
                result = await permissions.get_permission_levels(object_type)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting permission levels: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        # Specific object permission tools
        @self.tool(
            name="get_cluster_permissions",
            description="Get permissions for a cluster with parameter: cluster_id (required)",
        )
        async def get_cluster_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting cluster permissions with params: {params}")
            try:
                cluster_id = params.get("cluster_id")
                
                if not cluster_id:
                    return [{"text": json.dumps({"error": "cluster_id is required"})}]
                
                result = await permissions.get_cluster_permissions(cluster_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting cluster permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="set_cluster_permissions",
            description="Set permissions for a cluster with parameters: cluster_id (required), access_control_list (required)",
        )
        async def set_cluster_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Setting cluster permissions with params: {params}")
            try:
                cluster_id = params.get("cluster_id")
                access_control_list = params.get("access_control_list")
                
                if not cluster_id:
                    return [{"text": json.dumps({"error": "cluster_id is required"})}]
                if not access_control_list:
                    return [{"text": json.dumps({"error": "access_control_list is required"})}]
                
                result = await permissions.set_cluster_permissions(cluster_id, access_control_list)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error setting cluster permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_job_permissions",
            description="Get permissions for a job with parameter: job_id (required)",
        )
        async def get_job_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting job permissions with params: {params}")
            try:
                job_id = params.get("job_id")
                
                if not job_id:
                    return [{"text": json.dumps({"error": "job_id is required"})}]
                
                result = await permissions.get_job_permissions(job_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting job permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="set_job_permissions",
            description="Set permissions for a job with parameters: job_id (required), access_control_list (required)",
        )
        async def set_job_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Setting job permissions with params: {params}")
            try:
                job_id = params.get("job_id")
                access_control_list = params.get("access_control_list")
                
                if not job_id:
                    return [{"text": json.dumps({"error": "job_id is required"})}]
                if not access_control_list:
                    return [{"text": json.dumps({"error": "access_control_list is required"})}]
                
                result = await permissions.set_job_permissions(job_id, access_control_list)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error setting job permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_warehouse_permissions",
            description="Get permissions for a SQL warehouse with parameter: warehouse_id (required)",
        )
        async def get_warehouse_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting warehouse permissions with params: {params}")
            try:
                warehouse_id = params.get("warehouse_id")
                
                if not warehouse_id:
                    return [{"text": json.dumps({"error": "warehouse_id is required"})}]
                
                result = await permissions.get_warehouse_permissions(warehouse_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting warehouse permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="set_warehouse_permissions",
            description="Set permissions for a SQL warehouse with parameters: warehouse_id (required), access_control_list (required)",
        )
        async def set_warehouse_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Setting warehouse permissions with params: {params}")
            try:
                warehouse_id = params.get("warehouse_id")
                access_control_list = params.get("access_control_list")
                
                if not warehouse_id:
                    return [{"text": json.dumps({"error": "warehouse_id is required"})}]
                if not access_control_list:
                    return [{"text": json.dumps({"error": "access_control_list is required"})}]
                
                result = await permissions.set_warehouse_permissions(warehouse_id, access_control_list)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error setting warehouse permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="get_workspace_object_permissions",
            description="Get permissions for a workspace object (notebook, directory) with parameter: object_id (required)",
        )
        async def get_workspace_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting workspace object permissions with params: {params}")
            try:
                object_id = params.get("object_id")
                
                if not object_id:
                    return [{"text": json.dumps({"error": "object_id is required"})}]
                
                result = await permissions.get_workspace_object_permissions(object_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting workspace object permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="set_workspace_object_permissions",
            description="Set permissions for a workspace object with parameters: object_id (required), access_control_list (required)",
        )
        async def set_workspace_perms(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Setting workspace object permissions with params: {params}")
            try:
                object_id = params.get("object_id")
                access_control_list = params.get("access_control_list")
                
                if not object_id:
                    return [{"text": json.dumps({"error": "object_id is required"})}]
                if not access_control_list:
                    return [{"text": json.dumps({"error": "access_control_list is required"})}]
                
                result = await permissions.set_workspace_object_permissions(object_id, access_control_list)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error setting workspace object permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        # Share permissions management
        @self.tool(
            name="get_share_permissions",
            description="Get permissions for a share with parameter: name (required)",
        )
        async def get_share_permissions(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Getting share permissions with params: {params}")
            try:
                name = params.get("name")
                
                if not name:
                    return [{"text": json.dumps({"error": "name is required"})}]
                
                result = await shares.get_share_permissions(name)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error getting share permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="update_share_permissions",
            description="Update permissions for a share with parameters: name (required), changes (required)",
        )
        async def update_share_permissions(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Updating share permissions with params: {params}")
            try:
                name = params.get("name")
                changes = params.get("changes")
                
                if not name:
                    return [{"text": json.dumps({"error": "name is required"})}]
                if not changes:
                    return [{"text": json.dumps({"error": "changes is required"})}]
                
                result = await shares.update_share_permissions(name, changes)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error updating share permissions: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]

        # Git credentials management
        @self.tool(
            name="create_git_credential",
            description="Create a Git credential with parameters: git_provider (required), git_username (required), personal_access_token (required), comment (optional)",
        )
        async def create_git_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Creating Git credential with params: {params}")
            try:
                git_provider = params.get("git_provider")
                git_username = params.get("git_username")
                personal_access_token = params.get("personal_access_token")
                comment = params.get("comment")
                
                if not git_provider:
                    return [{"text": json.dumps({"error": "git_provider is required"})}]
                if not git_username:
                    return [{"text": json.dumps({"error": "git_username is required"})}]
                if not personal_access_token:
                    return [{"text": json.dumps({"error": "personal_access_token is required"})}]
                
                result = await git_credentials.create_git_credential(
                    git_provider=git_provider,
                    git_username=git_username,
                    personal_access_token=personal_access_token,
                    comment=comment
                )
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error creating Git credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="list_git_credentials",
            description="List all Git credentials",
        )
        async def list_git_credentials(params: Dict[str, Any]) -> List[TextContent]:
            logger.info("Listing Git credentials")
            try:
                result = await git_credentials.list_git_credentials()
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error listing Git credentials: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="update_git_credential",
            description="Update a Git credential with parameters: credential_id (required), git_provider (optional), git_username (optional), personal_access_token (optional), comment (optional)",
        )
        async def update_git_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Updating Git credential with params: {params}")
            try:
                credential_id = params.get("credential_id")
                git_provider = params.get("git_provider")
                git_username = params.get("git_username")
                personal_access_token = params.get("personal_access_token")
                comment = params.get("comment")
                
                if not credential_id:
                    return [{"text": json.dumps({"error": "credential_id is required"})}]
                
                result = await git_credentials.update_git_credential(
                    credential_id=credential_id,
                    git_provider=git_provider,
                    git_username=git_username,
                    personal_access_token=personal_access_token,
                    comment=comment
                )
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error updating Git credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]
        
        @self.tool(
            name="delete_git_credential",
            description="Delete a Git credential with parameter: credential_id (required)",
        )
        async def delete_git_credential(params: Dict[str, Any]) -> List[TextContent]:
            logger.info(f"Deleting Git credential with params: {params}")
            try:
                credential_id = params.get("credential_id")
                
                if not credential_id:
                    return [{"text": json.dumps({"error": "credential_id is required"})}]
                
                result = await git_credentials.delete_git_credential(credential_id)
                return [{"text": json.dumps(result)}]
            except Exception as e:
                logger.error(f"Error deleting Git credential: {str(e)}")
                return [{"text": json.dumps({"error": str(e)})}]


async def main():
    """Main entry point for the MCP server."""
    try:
        logger.info("Starting Databricks Permissions MCP server")
        server = DatabricksPermissionsMCPServer()
        
        # Use the built-in method for stdio servers
        # This is the recommended approach for MCP servers
        await server.run_stdio_async()
            
    except Exception as e:
        logger.error(f"Error in Databricks Permissions MCP server: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    # Turn off buffering in stdout
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(line_buffering=True)
    
    asyncio.run(main()) 