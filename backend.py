# backend.py
import json
import os
from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from generator.report import ReportGenerator
from blob_reader import read_blob_json, write_blob_json

app = FastAPI(
    title="Power BI Report Generator API",
    description="Transforms visual types, bindings, properties, filters, and layouts into PBIR JSON format.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend and cross-origin clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BlobProcessRequest(BaseModel):
    container_name: str
    input_blob_path: str
    output_blob_path: Optional[str] = "output/runtime_visuals.json"


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint to verify App Service status."""
    return {
        "status": "online",
        "service": "Power BI Generator API",
        "swagger_docs": "/docs",
    }


@app.post("/runtime-visuals", tags=["Report Generation"])
@app.post("/generate", tags=["Report Generation"])
def generate_runtime_visuals(payload: Dict[str, Any]):
    """Accepts visual specifications and returns the exact Power BI JSON schema."""
    try:
        generator = ReportGenerator(payload)
        result = generator.generate()

        # Cache locally to output directory
        output_dir = os.getenv("OUTPUT_DIR", "output")
        os.makedirs(output_dir, exist_ok=True)
        local_output_path = os.path.join(output_dir, "runtime_visuals.json")
        with open(local_output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation error: {str(e)}",
        )


@app.get("/runtime-visuals", tags=["Report Generation"])
def get_latest_runtime_visuals():
    """Retrieves the last generated runtime_visuals.json."""
    output_dir = os.getenv("OUTPUT_DIR", "output")
    local_output_path = os.path.join(output_dir, "runtime_visuals.json")
    if not os.path.exists(local_output_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No runtime_visuals.json found. Execute a POST request first.",
        )
    with open(local_output_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.post("/process-blob", tags=["Blob Storage"])
def process_blob_report(request: BlobProcessRequest):
    """Downloads JSON from an Azure Blob, transforms it, and uploads the result back to Blob Storage."""
    try:
        raw_payload = read_blob_json(
            container_name=request.container_name,
            blob_path=request.input_blob_path,
        )

        generator = ReportGenerator(raw_payload)
        result = generator.generate()

        output_url = write_blob_json(
            container_name=request.container_name,
            blob_path=request.output_blob_path,
            data=result,
        )

        return {
            "status": "success",
            "message": "Report generated and saved to blob successfully.",
            "output_blob_url": output_url,
            "data": result,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Blob processing failed: {str(e)}",
        )
