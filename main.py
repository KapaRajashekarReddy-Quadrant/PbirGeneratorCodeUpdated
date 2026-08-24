import os
from typing import Any, Dict, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend import process_metadata_dynamic
from auth.token import get_powerbi_access_token

app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    description="Tableau to Power BI Runtime Visuals & Embed Token Generator"
)

# Enable CORS for frontend consumption
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RuntimeVisualsRequest(BaseModel):
    metadataBlobPath: str


class EmbedTokenRequest(BaseModel):
    workspace_id: Optional[str] = None
    report_id: Optional[str] = None
    dataset_id: Optional[str] = None


@app.get("/")
@app.get("/health")
def health_check():
    """Liveness probe for Azure App Service container startup."""
    return {"status": "HEALTHY", "service": "Runtime Visuals API"}


@app.post("/embed-token", summary="Generate Embed Token")
def generate_embed_token(request: Optional[EmbedTokenRequest] = None):
    """
    Acquires an Azure MSAL access token for embedding Power BI artifacts.
    """
    try:
        token = get_powerbi_access_token()
        if not token:
            raise HTTPException(
                status_code=400,
                detail="Failed to generate embed token. Verify Azure Service Principal credentials in App Settings."
            )
        return {
            "token": token,
            "token_type": "Bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/runtime-visuals", summary="Generate Runtime Visuals")
def generate_runtime_visuals(request: RuntimeVisualsRequest):
    """
    Accepts the metadataBlobPath JSON parameter, fetches the metadata,
    and returns parsed Power BI runtime visuals and layouts.
    """
    if not request.metadataBlobPath or not request.metadataBlobPath.strip():
        raise HTTPException(
            status_code=400,
            detail="Field 'metadataBlobPath' cannot be empty."
        )

    try:
        result = process_metadata_dynamic(request.metadataBlobPath)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating runtime visuals: {str(e)}"
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", os.environ.get("WEBSITES_PORT", 8000)))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
