# backend.py
from typing import Any, Dict
from auth.token import get_auth_headers
from blob_reader import read_blob_json_by_path
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from generator.report import ReportGenerator
from pydantic import BaseModel

app = FastAPI(
    title="Power BI PBIR API",
    description="Generates embed tokens and runtime visual PBIR configurations from blob metadata.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS
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
    workspaceId: str = ""
    reportId: str = ""
    datasetId: str = ""


# -------------------------------------------------------------
# 1. POST /embed-token
# -------------------------------------------------------------
@app.post("/embed-token", summary="Generate Embed Token")
def generate_embed_token(request: EmbedTokenRequest = None):
    """Generates Azure AD / Power BI Embed Token using MSAL credentials."""
    try:
        headers = get_auth_headers()
        return {
            "token": headers.get("Authorization", "").replace("Bearer ", ""),
            "status": "success",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embed token: {str(e)}",
        )


# -------------------------------------------------------------
# 2. POST /runtime-visuals (Reads from Blob & Returns JSON)
# -------------------------------------------------------------
@app.post("/runtime-visuals", summary="Generate Runtime Visuals")
def generate_runtime_visuals(request: RuntimeVisualsRequest):
    """Reads metadata JSON from the provided Blob Storage path,

    maps visual types, layout coordinates, filters, aggregations,
    and returns the compiled PBIR JSON schema.
    """
    try:
        # 1. Read input JSON directly from the Blob storage path
        raw_metadata = read_blob_json_by_path(request.metadataBlobPath)

        # 2. Run transformations (visuals mapping, aggregations, layout, filters)
        generator = ReportGenerator(raw_metadata)
        result = generator.generate()

        # 3. Return exact JSON format directly as HTTP response
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process runtime visuals from blob: {str(e)}",
        )
