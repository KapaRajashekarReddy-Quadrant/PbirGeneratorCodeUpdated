import os
import msal
from typing import Optional


def get_powerbi_access_token() -> Optional[str]:
    """Dynamically acquires an OAuth2 token for Power BI API using Service Principal or Device Flow."""
    client_id = os.getenv("AZURE_CLIENT_ID", "").strip()
    client_secret = os.getenv("AZURE_CLIENT_SECRET", "").strip()
    tenant_id = os.getenv("AZURE_TENANT_ID", "").strip()

    # Avoid crashing on import if env variables are not present during startup
    if not client_id or not tenant_id:
        return None

    authority = f"https://login.microsoftonline.com/{tenant_id}"
    scope = ["https://analysis.windows.net/powerbi/api/.default"]

    if client_secret:
        # Confidential Client Flow (Service Principal)
        app = msal.ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret
        )
        result = app.acquire_token_for_client(scopes=scope)
    else:
        # Public Client Flow
        app = msal.PublicClientApplication(client_id, authority=authority)
        result = app.acquire_token_silent(scope, account=None)

    if result and "access_token" in result:
        return result["access_token"]
    
    return None
