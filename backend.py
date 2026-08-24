import os
from typing import Any, Dict, Union
from blob_reader import read_blob_json_by_path
from generator.dataset import DatasetGenerator
from generator.layout import LayoutGenerator
from generator.visual import VisualGenerator


def process_metadata_dynamic(file_input: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Accepts any dynamic blob URL, relative path, or JSON dict and returns 
    structured PowerBI metadata components.
    """
    metadata = read_blob_json_by_path(file_input)

    dataset_gen = DatasetGenerator(metadata)
    layout_gen = LayoutGenerator(metadata)
    visual_gen = VisualGenerator(metadata)

    return {
        "tables": dataset_gen.get_table_schema(),
        "relationships": dataset_gen.get_relationships(),
        "measures": dataset_gen.get_measures(),
        "dashboards": layout_gen.get_dashboard_layouts(),
        "worksheets": visual_gen.get_parsed_worksheets()
    }


def handler(request_payload: Union[str, Dict[str, Any]]):
    """
    General entrypoint for backend APIs or Azure Functions.
    Can be invoked dynamically: handler(dynamic_blob_url)
    """
    try:
        result = process_metadata_dynamic(request_payload)
        return {
            "status": "SUCCESS",
            "data": result
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }


