import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, Optional, Union
from backend import process_metadata_dynamic

app = FastAPI(title="PowerBI PBIR Generator API")


class MetadataRequest(BaseModel):
    blob_url: Optional[str] = None
    blob_path: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None


@app.get("/")
@app.get("/health")
def health_check():
    """Health check endpoint to prevent 503 on Azure App Service container startup."""
    return {"status": "HEALTHY", "service": "PBIR Generator"}


@app.post("/process")
def process_endpoint(request: Union[MetadataRequest, Dict[str, Any]]):
    """
    Accepts any dynamic input:
    - {"blob_url": "https://..."}
    - {"blob_path": "container/file.json"}
    - Direct JSON metadata payload
    """
    try:
        # Normalize input
        input_data = None
        if isinstance(request, MetadataRequest):
            input_data = request.blob_url or request.blob_path or request.payload
        elif isinstance(request, dict):
            input_data = request.get("blob_url") or request.get("blob_path") or request.get("payload") or request

        if not input_data:
            raise HTTPException(
                status_code=400,
                detail="Request body must provide 'blob_url', 'blob_path', or a valid JSON payload."
            )

        result = process_metadata_dynamic(input_data)
        return {
            "status": "SUCCESS",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Azure App Service sets the port in the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
