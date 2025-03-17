"""
Databricks Git Credentials API

This module provides functions for managing Git credentials in Databricks.
"""

import logging
from typing import Any, Dict, List, Optional

from src.core.utils import DatabricksAPIError, make_api_request

# Configure logging
logger = logging.getLogger(__name__)

# Git provider constants
GIT_PROVIDERS = [
    "github", 
    "gitlab", 
    "bitbucket", 
    "azureDevOpsServices", 
    "azureDevOpsServicesAAD", 
    "awsCodeCommit"
]

async def create_git_credential(
    git_provider: str,
    git_username: str,
    personal_access_token: str,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a Git credential.
    
    Args:
        git_provider: The Git provider (github, gitlab, bitbucket, azureDevOpsServices, etc.)
        git_username: The username for the Git provider
        personal_access_token: The personal access token for the Git provider
        comment: Optional comment for the Git credential
        
    Returns:
        Response containing the created Git credential info
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Creating Git credential for provider: {git_provider}")
    
    if git_provider not in GIT_PROVIDERS:
        raise ValueError(f"Invalid Git provider: {git_provider}. Must be one of {GIT_PROVIDERS}")
    
    data = {
        "git_provider": git_provider,
        "git_username": git_username,
        "personal_access_token": personal_access_token
    }
    
    if comment:
        data["comment"] = comment
    
    return await make_api_request("POST", "/api/2.0/git-credentials", data=data)

async def list_git_credentials() -> Dict[str, Any]:
    """
    List all Git credentials.
    
    Returns:
        Response containing a list of Git credentials
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info("Listing Git credentials")
    return await make_api_request("GET", "/api/2.0/git-credentials")

async def update_git_credential(
    credential_id: str,
    git_provider: Optional[str] = None,
    git_username: Optional[str] = None,
    personal_access_token: Optional[str] = None,
    comment: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update a Git credential.
    
    Args:
        credential_id: The ID of the Git credential to update
        git_provider: Optional new Git provider
        git_username: Optional new username for the Git provider
        personal_access_token: Optional new personal access token for the Git provider
        comment: Optional new comment for the Git credential
        
    Returns:
        Response containing the updated Git credential info
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Updating Git credential: {credential_id}")
    
    data = {"credential_id": credential_id}
    
    if git_provider:
        if git_provider not in GIT_PROVIDERS:
            raise ValueError(f"Invalid Git provider: {git_provider}. Must be one of {GIT_PROVIDERS}")
        data["git_provider"] = git_provider
    
    if git_username:
        data["git_username"] = git_username
    
    if personal_access_token:
        data["personal_access_token"] = personal_access_token
    
    if comment:
        data["comment"] = comment
    
    return await make_api_request("PATCH", "/api/2.0/git-credentials", data=data)

async def delete_git_credential(credential_id: str) -> Dict[str, Any]:
    """
    Delete a Git credential.
    
    Args:
        credential_id: The ID of the Git credential to delete
        
    Returns:
        Empty response if successful
        
    Raises:
        DatabricksAPIError: If the API request fails
    """
    logger.info(f"Deleting Git credential: {credential_id}")
    
    data = {"credential_id": credential_id}
    return await make_api_request("DELETE", "/api/2.0/git-credentials", data=data) 