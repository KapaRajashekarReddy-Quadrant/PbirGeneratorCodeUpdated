# auth/token.py
import os

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID", "default_tenant_id")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID", "default_client_id")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET", "")
POWERBI_WORKSPACE_ID = os.getenv("POWERBI_WORKSPACE_ID", "")
POWERBI_DATASET_ID = os.getenv("POWERBI_DATASET_ID", "")


def get_auth_headers() -> dict:
    """Returns headers configured with environment-based access tokens."""
    token = os.getenv("POWERBI_ACCESS_TOKEN", "")
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    

