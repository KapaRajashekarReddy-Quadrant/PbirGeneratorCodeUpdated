from typing import Any, Dict


class LayoutGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata or {}

    def get_canvas_size(self, dash: Dict[str, Any]) -> Dict[str, int]:
        canvas = dash.get("canvas", {})
        return {
            "width": canvas.get("width") or dash.get("width") or 646,
            "height": canvas.get("height") or dash.get("height") or 560
        }
