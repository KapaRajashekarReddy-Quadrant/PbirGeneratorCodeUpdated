import json
import os
from typing import Any, Dict
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
    """Accurately extracts container_name and blob_name regardless of whether raw_path
    is a full URL (https://...), a URI with SAS tokens, or a relative path ('container/path/file.json').
    """
    clean_path = raw_path.strip()

    # Case 1: Full HTTPS URL (e.g., https://myaccount.blob.core.windows.net/mycontainer/folder/file.json?sv=...)
    if clean_path.startswith("http://") or clean_path.startswith("https://"):
        parsed = urlparse(clean_path)
        path_without_params = unquote(parsed.path).lstrip("/")
        parts = path_without_params.split("/", 1)
        if len(parts) == 2:
            return parts[0], parts[1]
        elif len(parts) == 1:
            return parts[0], ""

    # Case 2: Strip any accidental leading slashes or whitespace
    clean_path = clean_path.lstrip("/")

    # Check if a default container is configured in Environment variables
    env_container = os.getenv("AZURE_BLOB_CONTAINER_NAME", "").strip()

    if "/" in clean_path:
        parts = clean_path.split("/", 1)
        # If env container is set AND the path doesn't start with it, treat whole path as blob inside env container
        if env_container and parts[0] != env_container:
            return env_container, clean_path
        # Otherwise, the first token is the container and the remainder is the blob path
        return parts[0], parts[1]

    # Case 3: Just a file name was passed
    container = env_container if env_container else "metadata"
    return container, clean_path


def read_blob_json_by_path(full_or_relative_path: str) -> Dict[str, Any]:
    """Downloads and parses JSON from Azure Blob Storage cleanly,

    automatically unwrapping the root 'metadata' key if present.
    """
    container_name, blob_name = extract_container_and_blob(
        full_or_relative_path
    )

    if not container_name or not blob_name:
        raise ValueError(
            f"Invalid blob path supplied: '{full_or_relative_path}'. Container or blob name cannot be empty."
        )

    client = get_blob_service_client()
    blob_client = client.get_blob_client(
        container=container_name, blob=blob_name
    )

    download_stream = blob_client.download_blob()
    content = download_stream.readall().decode("utf-8")
    data = json.loads(content)

    # Automatically unwrap wrapper dictionary if stored under 'metadata'
    if isinstance(data, dict) and "metadata" in data and isinstance(data["metadata"], dict):
        return data["metadata"]
    return data
