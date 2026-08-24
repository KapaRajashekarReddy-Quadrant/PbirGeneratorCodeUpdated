# blob_reader.py
import json
import os
from typing import Any, Dict

# Configurable storage paths via environment variables
BLOB_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
INPUT_STORAGE_CONTAINER = os.getenv("INPUT_STORAGE_CONTAINER", "powerbi-inputs")
OUTPUT_STORAGE_CONTAINER = os.getenv("OUTPUT_STORAGE_CONTAINER", "powerbi-outputs")
LOCAL_OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")


def read_json_payload(file_path: str) -> Dict[str, Any]:
    """Reads JSON payload from local filesystem (or blob if configured)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json_payload(file_path: str, data: Dict[str, Any]) -> None:
    """Writes output payload to target directory."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)