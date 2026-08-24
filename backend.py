# backend.py
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from generator.report import ReportGenerator

app = FastAPI(
    title="Power BI Report Generator API",
    description="Transforms visual types, bindings, properties, and layouts into PBIR JSON format.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for browser access
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
def health_check():
    return {
        "status": "online",
        "message": "Power BI Generator API is running. Visit /docs for the API interface.",
    }


@app.post("/generate")
def generate_report_endpoint(payload: Dict[str, Any]):
    """Accepts raw visual/page JSON and returns the mapped Power BI layout."""
    try:
        return process_report_request(payload)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Report generation error: {str(e)}"
        )
