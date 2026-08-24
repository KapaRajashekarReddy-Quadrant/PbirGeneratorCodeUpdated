from typing import Any, Dict, Union
from blob_reader import read_blob_json_by_path
from generator.report import ReportGenerator


def process_metadata_dynamic(file_input: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ingests dynamic metadata from Azure Blob path, URL, or dict
    and returns the exact runtime visuals, pages, and dashboards schema.
    """
    metadata = read_blob_json_by_path(file_input)
    report_gen = ReportGenerator(metadata)
    return report_gen.generate_runtime_json()
