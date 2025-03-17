"""
FastAPI application for Databricks Permissions API.

This is a stub module that provides compatibility with existing tests.
The actual implementation uses the MCP protocol directly.
"""

from fastapi import FastAPI

from src.api import service_principals, unity_catalog, permissions, shares, git_credentials
from src.core.config import settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: The configured FastAPI application
    """
    app = FastAPI(
        title="Databricks Permissions API",
        description="API for managing Databricks permissions, credentials, and Git credentials",
        version="1.0.0",
    )

    # Service Principal endpoints
    @app.post("/api/2.0/service-principals/create")
    async def create_service_principal(request_data: dict):
        return await service_principals.create_service_principal(
            request_data.get("display_name"),
            request_data.get("application_id"),
            request_data.get("allow_cluster_create", False)
        )

    @app.get("/api/2.0/service-principals/list")
    async def list_service_principals():
        return await service_principals.list_service_principals()

    @app.get("/api/2.0/service-principals/get/{sp_id}")
    async def get_service_principal(sp_id: str):
        return await service_principals.get_service_principal(sp_id)

    @app.post("/api/2.0/service-principals/update")
    async def update_service_principal(request_data: dict):
        return await service_principals.update_service_principal(
            request_data.get("id"),
            request_data.get("display_name"),
            request_data.get("allow_cluster_create")
        )

    @app.post("/api/2.0/service-principals/delete")
    async def delete_service_principal(request_data: dict):
        return await service_principals.delete_service_principal(request_data.get("id"))

    # Storage Credential endpoints
    @app.post("/api/2.0/unity-catalog/storage-credentials/create")
    async def create_storage_credential(request_data: dict):
        return await unity_catalog.create_storage_credential(
            request_data.get("name"),
            request_data.get("aws_iam_role"),
            request_data.get("azure_service_principal"),
            request_data.get("comment")
        )

    @app.get("/api/2.0/unity-catalog/storage-credentials/list")
    async def list_storage_credentials():
        return await unity_catalog.list_storage_credentials()

    # Permissions endpoints
    @app.get("/api/2.0/permissions/{object_type}/{object_id}")
    async def get_permissions(object_type: str, object_id: str):
        return await permissions.get_permissions(object_type, object_id)
    
    @app.put("/api/2.0/permissions/{object_type}/{object_id}")
    async def set_permissions(object_type: str, object_id: str, request_data: dict):
        return await permissions.set_permissions(object_type, object_id, request_data.get("access_control_list", []))
    
    @app.patch("/api/2.0/permissions/{object_type}/{object_id}")
    async def update_permissions(object_type: str, object_id: str, request_data: dict):
        return await permissions.update_permissions(object_type, object_id, request_data.get("access_control_list", []))
    
    @app.get("/api/2.0/permissions/{object_type}")
    async def get_permission_levels(object_type: str):
        return await permissions.get_permission_levels(object_type)
    
    # Specific object permissions endpoints
    @app.get("/api/2.0/permissions/clusters/{cluster_id}")
    async def get_cluster_permissions(cluster_id: str):
        return await permissions.get_cluster_permissions(cluster_id)
    
    @app.put("/api/2.0/permissions/clusters/{cluster_id}")
    async def set_cluster_permissions(cluster_id: str, request_data: dict):
        return await permissions.set_cluster_permissions(cluster_id, request_data.get("access_control_list", []))
    
    @app.get("/api/2.0/permissions/jobs/{job_id}")
    async def get_job_permissions(job_id: str):
        return await permissions.get_job_permissions(job_id)
    
    @app.put("/api/2.0/permissions/jobs/{job_id}")
    async def set_job_permissions(job_id: str, request_data: dict):
        return await permissions.set_job_permissions(job_id, request_data.get("access_control_list", []))
    
    @app.get("/api/2.0/permissions/sql/warehouses/{warehouse_id}")
    async def get_warehouse_permissions(warehouse_id: str):
        return await permissions.get_warehouse_permissions(warehouse_id)
    
    @app.put("/api/2.0/permissions/sql/warehouses/{warehouse_id}")
    async def set_warehouse_permissions(warehouse_id: str, request_data: dict):
        return await permissions.set_warehouse_permissions(warehouse_id, request_data.get("access_control_list", []))
    
    @app.get("/api/2.0/permissions/directories/{object_id}")
    async def get_workspace_object_permissions(object_id: str):
        return await permissions.get_workspace_object_permissions(object_id)
    
    @app.put("/api/2.0/permissions/directories/{object_id}")
    async def set_workspace_object_permissions(object_id: str, request_data: dict):
        return await permissions.set_workspace_object_permissions(object_id, request_data.get("access_control_list", []))

    # Shares endpoints
    @app.post("/api/2.1/unity-catalog/shares")
    async def create_share(request_data: dict):
        return await shares.create_share(
            request_data.get("name"),
            request_data.get("comment")
        )
    
    @app.get("/api/2.1/unity-catalog/shares/{name}")
    async def get_share(name: str):
        return await shares.get_share(name)
    
    @app.patch("/api/2.1/unity-catalog/shares/{name}")
    async def update_share(name: str, request_data: dict):
        return await shares.update_share(
            name,
            request_data.get("name"),
            request_data.get("comment")
        )
    
    @app.delete("/api/2.1/unity-catalog/shares/{name}")
    async def delete_share(name: str):
        return await shares.delete_share(name)
    
    @app.get("/api/2.1/unity-catalog/shares")
    async def list_shares():
        return await shares.list_shares()
    
    @app.get("/api/2.1/unity-catalog/shares/{name}/permissions")
    async def get_share_permissions(name: str):
        return await shares.get_share_permissions(name)
    
    @app.patch("/api/2.1/unity-catalog/shares/{name}/permissions")
    async def update_share_permissions(name: str, request_data: dict):
        return await shares.update_share_permissions(name, request_data.get("changes", []))
    
    @app.post("/api/2.1/unity-catalog/shares/{share_name}/objects")
    async def add_to_share(share_name: str, request_data: dict):
        return await shares.add_to_share(
            share_name,
            request_data.get("object_type"),
            request_data.get("object_key"),
            request_data.get("comment")
        )
    
    @app.delete("/api/2.1/unity-catalog/shares/{share_name}/objects")
    async def remove_from_share(share_name: str, request_data: dict):
        return await shares.remove_from_share(
            share_name,
            request_data.get("object_type"),
            request_data.get("object_key")
        )
    
    @app.get("/api/2.1/unity-catalog/shares/{share_name}/objects")
    async def list_share_objects(share_name: str):
        return await shares.list_share_objects(share_name)
    
    @app.put("/api/2.1/unity-catalog/shares/{share_name}/recipients/{recipient_name}")
    async def add_recipient_to_share(share_name: str, recipient_name: str, request_data: dict):
        return await shares.add_recipient_to_share(
            share_name,
            recipient_name,
            request_data.get("comment")
        )
    
    @app.delete("/api/2.1/unity-catalog/shares/{share_name}/recipients/{recipient_name}")
    async def remove_recipient_from_share(share_name: str, recipient_name: str):
        return await shares.remove_recipient_from_share(share_name, recipient_name)
    
    @app.get("/api/2.1/unity-catalog/shares/{share_name}/recipients")
    async def list_share_recipients(share_name: str):
        return await shares.list_share_recipients(share_name)

    # Git credentials endpoints
    @app.post("/api/2.0/git-credentials")
    async def create_git_credential(request_data: dict):
        return await git_credentials.create_git_credential(
            request_data.get("git_provider"),
            request_data.get("git_username"),
            request_data.get("personal_access_token"),
            request_data.get("comment")
        )
    
    @app.get("/api/2.0/git-credentials")
    async def list_git_credentials():
        return await git_credentials.list_git_credentials()
    
    @app.patch("/api/2.0/git-credentials")
    async def update_git_credential(request_data: dict):
        return await git_credentials.update_git_credential(
            request_data.get("credential_id"),
            request_data.get("git_provider"),
            request_data.get("git_username"),
            request_data.get("personal_access_token"),
            request_data.get("comment")
        )
    
    @app.delete("/api/2.0/git-credentials")
    async def delete_git_credential(request_data: dict):
        return await git_credentials.delete_git_credential(request_data.get("credential_id"))

    return app 