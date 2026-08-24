import io
import os
from typing import Any, Dict, Optional, Union
import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

from backend import process_metadata_dynamic
from auth.token import get_powerbi_access_token

app = FastAPI(
    title="PowerBI PBIR Generator API",
    version="1.0.0",
    description="Dynamic converter from metadata JSON and Excel mappings to PowerBI PBIR artifacts"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MetadataRequest(BaseModel):
    blob_url: Optional[str] = None
    blob_path: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


@app.get("/")
@app.get("/health")
def health_check():
    """
    Liveness and readiness probe for Azure App Service container startup.
    Responding 200 here clears the 503 Service Unavailable state.
    """
    return {
        "status": "HEALTHY",
        "service": "PBIR Generator API",
        "port": int(os.environ.get("PORT", os.environ.get("WEBSITES_PORT", 8000)))
    }


@app.post("/auth/token")
def fetch_token():
    """Generates an MSAL Power BI bearer token."""
    try:
        token = get_powerbi_access_token()
        if not token:
            raise HTTPException(
                status_code=400,
                detail="Could not acquire token. Please verify AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_TENANT_ID environment variables."
            )
        return {"access_token": token, "token_type": "Bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")


@app.post("/process")
def process_endpoint(request: Union[MetadataRequest, Dict[str, Any]]):
    """
    Dynamically parses metadata from an Azure Blob URL, relative path, or direct JSON dictionary.
    """
    try:
        input_data = None
        if isinstance(request, MetadataRequest):
            input_data = request.blob_url or request.blob_path or request.payload
        elif isinstance(request, dict):
            input_data = (
                request.get("blob_url")
                or request.get("blob_path")
                or request.get("payload")
                or request
            )

        if not input_data:
            raise HTTPException(
                status_code=400,
                detail="Request body must provide 'blob_url', 'blob_path', or a valid JSON payload."
            )

        result = process_metadata_dynamic(input_data)
        return {"status": "SUCCESS", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-mapping")
async def upload_excel_mapping(
    file: UploadFile = File(...),
    blob_url: Optional[str] = Form(None)
):
    """
    Processes an uploaded Excel (.xlsx/.xls) mapping file alongside dynamic metadata.
    """
    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        mapping_records = df.to_dict(orient="records")

        response_data = {
            "mapping_rows_count": len(mapping_records),
            "mappings": mapping_records
        }

        if blob_url:
            metadata_result = process_metadata_dynamic(blob_url)
            response_data["metadata"] = metadata_result

        return {"status": "SUCCESS", "data": response_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse Excel file: {str(e)}")


if __name__ == "__main__":
    # Azure injects PORT or WEBSITES_PORT into the environment
    port = int(os.environ.get("PORT", os.environ.get("WEBSITES_PORT", 8000)))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
