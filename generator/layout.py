# generator/layout.py
import os
from typing import Any, Dict, List

DEFAULT_PAGE_WIDTH = int(os.getenv("DEFAULT_PAGE_WIDTH", "646"))
DEFAULT_PAGE_HEIGHT = int(os.getenv("DEFAULT_PAGE_HEIGHT", "560"))
DEFAULT_MARGIN = int(os.getenv("DEFAULT_MARGIN", "18"))
DEFAULT_GAP = int(os.getenv("DEFAULT_GAP", "16"))


class LayoutEngine:

    @staticmethod
    def adjust_layout(
        visuals: List[Dict[str, Any]],
        canvas_width: int = DEFAULT_PAGE_WIDTH,
        canvas_height: int = DEFAULT_PAGE_HEIGHT,
        margin: int = DEFAULT_MARGIN,
        default_gap: int = DEFAULT_GAP,
    ) -> List[Dict[str, Any]]:
        running_y = 99
        content_width = canvas_width - (margin * 2)

        for index, visual in enumerate(visuals, start=1):
            layout = visual.get("layout", {})
            if "x" not in layout or "y" not in layout:
                layout["x"] = margin
                layout["y"] = running_y
                layout["width"] = content_width
                layout["height"] = 200
                running_y += 200 + default_gap

            layout["z"] = layout.get("z", index)
            visual["layout"] = layout

        return visuals
