# blob_reader.py
import json
import os
from typing import Any, Dict
from azure.storage.blob import BlobServiceClient


def get_blob_service_client() -> BlobServiceClient:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
    if not connection_string:
        raise ValueError(
            "AZURE_STORAGE_CONNECTION_STRING is not configured in environment variables."
        )
    return BlobServiceClient.from_connection_string(connection_string)


def read_blob_json(container_name: str, blob_path: str) -> Dict[str, Any]:
    """Downloads and parses a JSON blob from Azure Blob Storage."""
    client = get_blob_service_client()
    blob_client = client.get_blob_client(
        container=container_name, blob=blob_path
    )
    stream = blob_client.download_blob()
    content = stream.readall().decode("utf-8")
    return json.loads(content)


def write_blob_json(
    container_name: str, blob_path: str, data: Dict[str, Any]
) -> str:
    """Uploads a generated JSON payload to Azure Blob Storage."""
    client = get_blob_service_client()
    blob_client = client.get_blob_client(
        container=container_name, blob=blob_path
    )
    json_bytes = json.dumps(data, indent=2).encode("utf-8")
    blob_client.upload_blob(json_bytes, overwrite=True)
    return blob_client.url
