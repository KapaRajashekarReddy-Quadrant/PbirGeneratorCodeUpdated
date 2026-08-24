from typing import Any, Dict, Union
from blob_reader import read_blob_json_by_path
from generator.layout import LayoutGenerator


def process_metadata_dynamic(file_input: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Ingests any dynamic blob URL, relative path, or JSON dict and returns
    the runtime visual configuration: {"visuals": [...], "pages": [...], "dashboards": [...]}
    """
    metadata = read_blob_json_by_path(file_input)
    layout_gen = LayoutGenerator(metadata)
    return layout_gen.generate_runtime_structure()
