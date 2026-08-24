# blob_reader.py
import json
import os
from typing import Any, Dict
from azure.storage.blob import BlobServiceClient


def get_blob_service_client() -> BlobServiceClient:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    if not connection_string:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING environment variable is missing."
        )
    return BlobServiceClient.from_connection_string(connection_string)


def read_blob_json_by_path(full_or_relative_path: str) -> Dict[str, Any]:
    """Downloads and parses JSON from Azure Blob Storage given a blob path or container/blob path."""
    container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME", "metadata")
    client = get_blob_service_client()

    # Handle if container name is included in path or defaults to env
    clean_path = full_or_relative_path.strip().lstrip("/")
    if "/" in clean_path and not os.getenv("AZURE_BLOB_CONTAINER_NAME"):
        parts = clean_path.split("/", 1)
        container_name = parts[0]
        blob_name = parts[1]
    else:
        blob_name = clean_path

    blob_client = client.get_blob_client(
        container=container_name, blob=blob_name
    )
    download_stream = blob_client.download_blob()
    content = download_stream.readall().decode("utf-8")
    return json.loads(content)
