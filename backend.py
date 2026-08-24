# backend.py
import json
import os
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from generator.report import ReportGenerator

app = FastAPI(
    title="Power BI PBIR Generator API",
    description="API for processing visual mappings, filters, layouts, and PBIR generation.",
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


def process_report_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Backend service entrypoint for executing transformations."""
    generator = ReportGenerator(payload)
    return generator.generate()


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Power BI Generator API is running. Go to /docs to view Swagger documentation.",
    }


@app.post("/runtime-visuals")
@app.post("/generate")
def create_runtime_visuals(payload: Dict[str, Any]):
    """Accepts visual specifications and returns the transformed Power BI schema."""
    try:
        result = process_report_request(payload)

        # Save copy to output directory if needed
        output_dir = os.getenv("OUTPUT_DIR", "output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "runtime_visuals.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)

        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Generation failed: {str(e)}"
        )


@app.get("/runtime-visuals")
def get_cached_runtime_visuals():
    """Reads and returns the last generated runtime_visuals.json file."""
    output_path = os.path.join(
        os.getenv("OUTPUT_DIR", "output"), "runtime_visuals.json"
    )
    if not os.path.exists(output_path):
        raise HTTPException(
            status_code=404, detail="No runtime visuals found. Run POST first."
        )
    with open(output_path, "r", encoding="utf-8") as f:
        return json.load(f)
