"""
API for managing Databricks Unity Catalog credentials.
"""

import logging
from typing import Any, Dict, List, Optional

from src.core.utils import DatabricksAPIError, make_api_request

# Configure logging
logger = logging.getLogger(__name__)

# Storage Credentials
async def create_storage_credential(
    name: str,
    aws_credentials: Optional[Dict[str, Any]] = None,
    azure_credentials: Optional[Dict[str, Any]] = None,
    gcp_credentials: Optional[Dict[str, Any]] = None,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new storage credential in the Unity Catalog.
    
    Args:
        name: Name of the storage credential
        aws_credentials: Optional AWS credentials configuration
        azure_credentials: Optional Azure credentials configuration
        gcp_credentials: Optional GCP credentials configuration
        comment: Optional comment for the storage credential
        
    Returns:
        Response containing the created storage credential info
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Creating new storage credential: {name}")
    
    data = {"name": name}
    
    if aws_credentials:
        data["aws_credentials"] = aws_credentials
    elif azure_credentials:
        data["azure_managed_identity"] = azure_credentials
    elif gcp_credentials:
        data["gcp_service_account"] = gcp_credentials
    
    if comment:
        data["comment"] = comment
    
    return make_api_request("POST", "/api/2.1/unity-catalog/storage-credentials", data=data)


async def get_storage_credential(name: str) -> Dict[str, Any]:
    """
    Get details of a storage credential in the Unity Catalog.
    
    Args:
        name: Name of the storage credential
        
    Returns:
        Response containing storage credential details
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Getting storage credential details: {name}")
    return make_api_request("GET", f"/api/2.1/unity-catalog/storage-credentials/{name}")


async def update_storage_credential(
    name: str,
    new_name: Optional[str] = None,
    aws_credentials: Optional[Dict[str, Any]] = None,
    azure_credentials: Optional[Dict[str, Any]] = None,
    gcp_credentials: Optional[Dict[str, Any]] = None,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a storage credential in the Unity Catalog.
    
    Args:
        name: Name of the storage credential to update
        new_name: Optional new name for the storage credential
        aws_credentials: Optional new AWS credentials configuration
        azure_credentials: Optional new Azure credentials configuration
        gcp_credentials: Optional new GCP credentials configuration
        comment: Optional new comment for the storage credential
        
    Returns:
        Response containing the updated storage credential info
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Updating storage credential: {name}")
    
    data = {}
    
    if new_name:
        data["name"] = new_name
        
    if aws_credentials:
        data["aws_credentials"] = aws_credentials
    elif azure_credentials:
        data["azure_managed_identity"] = azure_credentials
    elif gcp_credentials:
        data["gcp_service_account"] = gcp_credentials
    
    if comment:
        data["comment"] = comment
    
    return make_api_request("PATCH", f"/api/2.1/unity-catalog/storage-credentials/{name}", data=data)


async def delete_storage_credential(name: str) -> Dict[str, Any]:
    """
    Delete a storage credential from the Unity Catalog.
    
    Args:
        name: Name of the storage credential to delete
        
    Returns:
        Empty response on success
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Deleting storage credential: {name}")
    return make_api_request("DELETE", f"/api/2.1/unity-catalog/storage-credentials/{name}")


async def list_storage_credentials(max_results: Optional[int] = None) -> Dict[str, Any]:
    """
    List storage credentials in the Unity Catalog.
    
    Args:
        max_results: Optional maximum number of storage credentials to return
        
    Returns:
        Response containing a list of storage credentials
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info("Listing storage credentials")
    
    params = {}
    if max_results:
        params["max_results"] = max_results
    
    return make_api_request("GET", "/api/2.1/unity-catalog/storage-credentials", params=params)


# Credentials
async def create_credential(
    name: str,
    aws_credentials: Optional[Dict[str, Any]] = None,
    azure_credentials: Optional[Dict[str, Any]] = None,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a new credential in the Unity Catalog.
    
    Args:
        name: Name of the credential
        aws_credentials: Optional AWS credentials configuration
        azure_credentials: Optional Azure credentials configuration
        comment: Optional comment for the credential
        
    Returns:
        Response containing the created credential info
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Creating new credential: {name}")
    
    data = {"name": name}
    
    if aws_credentials:
        data["aws_credentials"] = aws_credentials
    elif azure_credentials:
        data["azure_service_principal"] = azure_credentials
    
    if comment:
        data["comment"] = comment
    
    return make_api_request("POST", "/api/2.1/unity-catalog/credentials", data=data)


async def list_credentials() -> Dict[str, Any]:
    """
    List all credentials in the Unity Catalog.
    
    Returns:
        Response containing a list of credentials
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info("Listing credentials")
    return make_api_request("GET", "/api/2.1/unity-catalog/credentials")


async def update_credential(
    name: str,
    new_name: Optional[str] = None,
    aws_credentials: Optional[Dict[str, Any]] = None,
    azure_credentials: Optional[Dict[str, Any]] = None,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a credential in the Unity Catalog.
    
    Args:
        name: Name of the credential to update
        new_name: Optional new name for the credential
        aws_credentials: Optional new AWS credentials configuration
        azure_credentials: Optional new Azure credentials configuration
        comment: Optional new comment for the credential
        
    Returns:
        Response containing the updated credential info
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Updating credential: {name}")
    
    data = {}
    
    if new_name:
        data["name"] = new_name
        
    if aws_credentials:
        data["aws_credentials"] = aws_credentials
    elif azure_credentials:
        data["azure_service_principal"] = azure_credentials
    
    if comment:
        data["comment"] = comment
    
    return make_api_request("PATCH", f"/api/2.1/unity-catalog/credentials/{name}", data=data)


async def delete_credential(name: str) -> Dict[str, Any]:
    """
    Delete a credential from the Unity Catalog.
    
    Args:
        name: Name of the credential to delete
        
    Returns:
        Empty response on success
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Deleting credential: {name}")
    return make_api_request("DELETE", f"/api/2.1/unity-catalog/credentials/{name}") 