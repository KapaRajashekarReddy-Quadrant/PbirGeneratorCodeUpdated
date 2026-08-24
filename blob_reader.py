import json
import os
from typing import Any, Dict, Union
from urllib.parse import unquote, urlparse
from azure.storage.blob import BlobServiceClient


def get_blob_service_client() -> BlobServiceClient:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    if not connection_string:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable is missing."
        )
    return BlobServiceClient.from_connection_string(connection_string)


def extract_container_and_blob(raw_path: str):
    """Accurately extracts container_name and blob_name regardless of path type."""
    clean_path = raw_path.strip()

    if clean_path.startswith("http://") or clean_path.startswith("https://"):
        parsed = urlparse(clean_path)
        path_without_params = unquote(parsed.path).lstrip("/")
        parts = path_without_params.split("/", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        elif len(parts) == 1:
            return parts[0], ""

    clean_path = clean_path.lstrip("/")
    env_container = os.getenv("AZURE_BLOB_CONTAINER_NAME", "").strip()

    if "/" in clean_path:
        parts = clean_path.split("/", 1)
        if env_container and parts[0] != env_container:
            return env_container, clean_path
        return parts[0], parts[1]

    container = env_container if env_container else "metadata"
    return container, clean_path


def unwrap_metadata(payload: Any) -> Dict[str, Any]:
    """Recursively checks and unwraps the metadata dictionary from any wrapper object."""
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            return {}

    if isinstance(payload, dict):
        if "metadata" in payload and isinstance(payload["metadata"], dict):
            return payload["metadata"]
        return payload

    return {}


def read_blob_json_by_path(path_or_data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Dynamically ingests JSON from Azure Blob, local file, or direct Dict."""
    if isinstance(path_or_data, dict):
        return unwrap_metadata(path_or_data)

    if not isinstance(path_or_data, str) or not path_or_data.strip():
        raise ValueError("Invalid input: must provide a non-empty path, URL, or dict.")

    clean_input = path_or_data.strip()

    # If it's a raw JSON string passed directly
    if clean_input.startswith("{") and clean_input.endswith("}"):
        return unwrap_metadata(clean_input)

    # If it's a local file path
    if os.path.exists(clean_input):
        with open(clean_input, "r", encoding="utf-8") as f:
            return unwrap_metadata(json.load(f))

    # Azure Blob Storage retrieval
    container_name, blob_name = extract_container_and_blob(clean_input)
    if not container_name or not blob_name:
        raise ValueError(
            f"Unable to parse container and blob from: '{clean_input}'."
        )

    client = get_blob_service_client()
    blob_client = client.get_blob_client(container=container_name, blob=blob_name)

    content = blob_client.download_blob().readall().decode("utf-8")
    return unwrap_metadata(content)
