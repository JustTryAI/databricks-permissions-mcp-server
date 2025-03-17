"""
API for managing Databricks permissions.

This module provides functions for managing permissions on various Databricks resources
including clusters, jobs, notebooks, SQL warehouses, and more.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from src.core.utils import DatabricksAPIError, make_api_request

# Configure logging
logger = logging.getLogger(__name__)

# Permission levels
PERMISSION_LEVELS = {
    "CAN_VIEW": "Can view the object",
    "CAN_MANAGE": "Can manage the object, including granting permissions to others",
    "CAN_EDIT": "Can edit the object",
    "CAN_RUN": "Can run the object (e.g., jobs, notebooks)",
    "CAN_USE": "Can use the object (e.g., clusters)",
    "CAN_RESTART": "Can restart the object (e.g., clusters)",
    "CAN_ATTACH_TO": "Can attach to the object (e.g., clusters)",
    "IS_OWNER": "Is the owner of the object",
}

# Object types
OBJECT_TYPES = [
    "clusters", "jobs", "notebooks", "directories", "registered-models", 
    "experiments", "sql/warehouses", "sql/dashboards", "sql/queries", 
    "sql/alerts", "repos", "serving-endpoints", "pipelines", "instance-pools",
    "cluster-policies", "tokens"
]

async def get_permissions(object_type: str, object_id: str) -> Dict[str, Any]:
    """
    Get permissions for a Databricks object.
    
    Args:
        object_type: Type of object (e.g., "clusters", "jobs", "notebooks")
        object_id: ID of the object
        
    Returns:
        Response containing the permissions information
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Getting permissions for {object_type}/{object_id}")
    
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Invalid object type: {object_type}. Must be one of {OBJECT_TYPES}")
    
    endpoint = f"/api/2.0/permissions/{object_type}/{object_id}"
    return make_api_request("GET", endpoint)

async def set_permissions(
    object_type: str, 
    object_id: str, 
    access_control_list: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Set permissions for a Databricks object.
    
    Args:
        object_type: Type of object (e.g., "clusters", "jobs", "notebooks")
        object_id: ID of the object
        access_control_list: List of access control items to set
            Each item should have:
            - user_name, group_name, or service_principal_name
            - permission_level (one of the keys in PERMISSION_LEVELS)
        
    Returns:
        Response containing the updated permissions information
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Setting permissions for {object_type}/{object_id}")
    
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Invalid object type: {object_type}. Must be one of {OBJECT_TYPES}")
    
    # Validate permission levels
    for acl in access_control_list:
        if "permission_level" in acl and acl["permission_level"] not in PERMISSION_LEVELS:
            raise ValueError(f"Invalid permission level: {acl['permission_level']}. Must be one of {list(PERMISSION_LEVELS.keys())}")
    
    data = {"access_control_list": access_control_list}
    endpoint = f"/api/2.0/permissions/{object_type}/{object_id}"
    return make_api_request("PUT", endpoint, data=data)

async def update_permissions(
    object_type: str, 
    object_id: str, 
    access_control_list: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Update permissions for a Databricks object.
    
    Args:
        object_type: Type of object (e.g., "clusters", "jobs", "notebooks")
        object_id: ID of the object
        access_control_list: List of access control items to update
            Each item should have:
            - user_name, group_name, or service_principal_name
            - permission_level (one of the keys in PERMISSION_LEVELS)
        
    Returns:
        Response containing the updated permissions information
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Updating permissions for {object_type}/{object_id}")
    
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Invalid object type: {object_type}. Must be one of {OBJECT_TYPES}")
    
    # Validate permission levels
    for acl in access_control_list:
        if "permission_level" in acl and acl["permission_level"] not in PERMISSION_LEVELS:
            raise ValueError(f"Invalid permission level: {acl['permission_level']}. Must be one of {list(PERMISSION_LEVELS.keys())}")
    
    data = {"access_control_list": access_control_list}
    endpoint = f"/api/2.0/permissions/{object_type}/{object_id}"
    return make_api_request("PATCH", endpoint, data=data)

async def get_permission_levels(object_type: str) -> Dict[str, Any]:
    """
    Get permission levels available for a Databricks object type.
    
    Args:
        object_type: Type of object (e.g., "clusters", "jobs", "notebooks")
        
    Returns:
        Response containing the available permission levels
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Getting permission levels for {object_type}")
    
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Invalid object type: {object_type}. Must be one of {OBJECT_TYPES}")
    
    endpoint = f"/api/2.0/permissions/{object_type}"
    return make_api_request("GET", endpoint)

# Specific object type permission functions

async def get_cluster_permissions(cluster_id: str) -> Dict[str, Any]:
    """Get permissions for a cluster."""
    return await get_permissions("clusters", cluster_id)

async def set_cluster_permissions(cluster_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a cluster."""
    return await set_permissions("clusters", cluster_id, access_control_list)

async def update_cluster_permissions(cluster_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a cluster."""
    return await update_permissions("clusters", cluster_id, access_control_list)

async def get_job_permissions(job_id: str) -> Dict[str, Any]:
    """Get permissions for a job."""
    return await get_permissions("jobs", job_id)

async def set_job_permissions(job_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a job."""
    return await set_permissions("jobs", job_id, access_control_list)

async def update_job_permissions(job_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a job."""
    return await update_permissions("jobs", job_id, access_control_list)

async def get_notebook_permissions(notebook_id: str) -> Dict[str, Any]:
    """Get permissions for a notebook."""
    return await get_permissions("notebooks", notebook_id)

async def set_notebook_permissions(notebook_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a notebook."""
    return await set_permissions("notebooks", notebook_id, access_control_list)

async def update_notebook_permissions(notebook_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a notebook."""
    return await update_permissions("notebooks", notebook_id, access_control_list)

async def get_warehouse_permissions(warehouse_id: str) -> Dict[str, Any]:
    """Get permissions for a SQL warehouse."""
    return await get_permissions("sql/warehouses", warehouse_id)

async def set_warehouse_permissions(warehouse_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a SQL warehouse."""
    return await set_permissions("sql/warehouses", warehouse_id, access_control_list)

async def update_warehouse_permissions(warehouse_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a SQL warehouse."""
    return await update_permissions("sql/warehouses", warehouse_id, access_control_list)

async def get_dashboard_permissions(dashboard_id: str) -> Dict[str, Any]:
    """Get permissions for a SQL dashboard."""
    return await get_permissions("sql/dashboards", dashboard_id)

async def set_dashboard_permissions(dashboard_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a SQL dashboard."""
    return await set_permissions("sql/dashboards", dashboard_id, access_control_list)

async def update_dashboard_permissions(dashboard_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a SQL dashboard."""
    return await update_permissions("sql/dashboards", dashboard_id, access_control_list)

async def get_query_permissions(query_id: str) -> Dict[str, Any]:
    """Get permissions for a SQL query."""
    return await get_permissions("sql/queries", query_id)

async def set_query_permissions(query_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a SQL query."""
    return await set_permissions("sql/queries", query_id, access_control_list)

async def update_query_permissions(query_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a SQL query."""
    return await update_permissions("sql/queries", query_id, access_control_list)

async def get_alert_permissions(alert_id: str) -> Dict[str, Any]:
    """Get permissions for a SQL alert."""
    return await get_permissions("sql/alerts", alert_id)

async def set_alert_permissions(alert_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a SQL alert."""
    return await set_permissions("sql/alerts", alert_id, access_control_list)

async def update_alert_permissions(alert_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a SQL alert."""
    return await update_permissions("sql/alerts", alert_id, access_control_list)

async def get_repo_permissions(repo_id: str) -> Dict[str, Any]:
    """Get permissions for a repo."""
    return await get_permissions("repos", repo_id)

async def set_repo_permissions(repo_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a repo."""
    return await set_permissions("repos", repo_id, access_control_list)

async def update_repo_permissions(repo_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a repo."""
    return await update_permissions("repos", repo_id, access_control_list)

async def get_serving_endpoint_permissions(endpoint_id: str) -> Dict[str, Any]:
    """Get permissions for a serving endpoint."""
    return await get_permissions("serving-endpoints", endpoint_id)

async def set_serving_endpoint_permissions(endpoint_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a serving endpoint."""
    return await set_permissions("serving-endpoints", endpoint_id, access_control_list)

async def update_serving_endpoint_permissions(endpoint_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a serving endpoint."""
    return await update_permissions("serving-endpoints", endpoint_id, access_control_list)

async def get_pipeline_permissions(pipeline_id: str) -> Dict[str, Any]:
    """Get permissions for a pipeline."""
    return await get_permissions("pipelines", pipeline_id)

async def set_pipeline_permissions(pipeline_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a pipeline."""
    return await set_permissions("pipelines", pipeline_id, access_control_list)

async def update_pipeline_permissions(pipeline_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a pipeline."""
    return await update_permissions("pipelines", pipeline_id, access_control_list)

async def get_instance_pool_permissions(pool_id: str) -> Dict[str, Any]:
    """Get permissions for an instance pool."""
    return await get_permissions("instance-pools", pool_id)

async def set_instance_pool_permissions(pool_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for an instance pool."""
    return await set_permissions("instance-pools", pool_id, access_control_list)

async def update_instance_pool_permissions(pool_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for an instance pool."""
    return await update_permissions("instance-pools", pool_id, access_control_list)

async def get_cluster_policy_permissions(policy_id: str) -> Dict[str, Any]:
    """Get permissions for a cluster policy."""
    return await get_permissions("cluster-policies", policy_id)

async def set_cluster_policy_permissions(policy_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a cluster policy."""
    return await set_permissions("cluster-policies", policy_id, access_control_list)

async def update_cluster_policy_permissions(policy_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a cluster policy."""
    return await update_permissions("cluster-policies", policy_id, access_control_list)

async def get_token_permissions(token_id: str) -> Dict[str, Any]:
    """Get permissions for a token."""
    return await get_permissions("tokens", token_id)

async def set_token_permissions(token_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a token."""
    return await set_permissions("tokens", token_id, access_control_list)

async def update_token_permissions(token_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a token."""
    return await update_permissions("tokens", token_id, access_control_list)

# Workspace object permissions (directories, notebooks, files)
async def get_workspace_object_permissions(object_id: str) -> Dict[str, Any]:
    """Get permissions for a workspace object."""
    return make_api_request("GET", f"/api/2.0/permissions/directories/{object_id}")

async def set_workspace_object_permissions(object_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Set permissions for a workspace object."""
    data = {"access_control_list": access_control_list}
    return make_api_request("PUT", f"/api/2.0/permissions/directories/{object_id}", data=data)

async def update_workspace_object_permissions(object_id: str, access_control_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Update permissions for a workspace object."""
    data = {"access_control_list": access_control_list}
    return make_api_request("PATCH", f"/api/2.0/permissions/directories/{object_id}", data=data) 