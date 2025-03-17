"""
API for managing Databricks Unity Catalog share permissions.

This module provides functions for managing share permissions in Databricks Unity Catalog.
"""

import logging
from typing import Any, Dict, List, Optional

from src.core.utils import DatabricksAPIError, make_api_request

# Configure logging
logger = logging.getLogger(__name__)

# Share permissions
SHARE_PERMISSIONS = ["SELECT", "USAGE"]

# Share permissions management
async def get_share_permissions(name: str) -> Dict[str, Any]:
    """
    Get permissions for a share.
    
    Args:
        name: Name of the share
        
    Returns:
        Response containing the share permissions
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Getting permissions for share: {name}")
    return make_api_request("GET", f"/api/2.1/unity-catalog/shares/{name}/permissions")

async def update_share_permissions(name: str, changes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update permissions for a share.
    
    Args:
        name: Name of the share
        changes: List of permission changes to apply
            Each change should have:
            - principal: The principal to change permissions for
            - add: List of permissions to add
            - remove: List of permissions to remove
        
    Returns:
        Response containing the updated share permissions
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Updating permissions for share: {name}")
    
    # Validate permissions
    for change in changes:
        if "add" in change:
            for perm in change["add"]:
                if perm not in SHARE_PERMISSIONS:
                    raise ValueError(f"Invalid permission: {perm}. Must be one of {SHARE_PERMISSIONS}")
        if "remove" in change:
            for perm in change["remove"]:
                if perm not in SHARE_PERMISSIONS:
                    raise ValueError(f"Invalid permission: {perm}. Must be one of {SHARE_PERMISSIONS}")
    
    data = {"changes": changes}
    return make_api_request("PATCH", f"/api/2.1/unity-catalog/shares/{name}/permissions", data=data) 