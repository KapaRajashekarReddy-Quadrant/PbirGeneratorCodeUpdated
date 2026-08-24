# generator/report.py
import copy
from typing import Any, Dict, List
from generator.layout import LayoutEngine
from generator.visual import VisualBuilder


class ReportGenerator:
    """Builds the complete multi-page/dashboard Power BI output JSON schema."""

    def __init__(self, raw_data: Dict[str, Any]):
        self.raw_data = raw_data

    def generate(self) -> Dict[str, Any]:
        raw_visuals = self.raw_data.get("visuals", [])
        raw_pages = self.raw_data.get("pages", [])
        raw_dashboards = self.raw_data.get("dashboards", [])

        # 1. Parse all top-level visuals
        processed_visuals = [VisualBuilder.build(v) for v in raw_visuals]

        # 2. Extract page metadata
        page_meta = raw_pages[0] if raw_pages else {}
        page_name = page_meta.get("name", "Production Overview")
        page_size = page_meta.get("size", {"width": 646, "height": 560})

        # 3. Apply layout engine
        arranged_visuals = LayoutEngine.adjust_layout(
            processed_visuals,
            canvas_width=page_size.get("width", 646),
            canvas_height=page_size.get("height", 560),
        )

        # 4. Construct pages array
        pages = []
        if raw_pages:
            for p in raw_pages:
                p_visuals = [VisualBuilder.build(v) for v in p.get("visuals", [])]
                p_arranged = LayoutEngine.adjust_layout(
                    p_visuals,
                    canvas_width=p.get("size", {}).get("width", 646),
                    canvas_height=p.get("size", {}).get("height", 560),
                )
                pages.append({
                    "name": p.get("name", page_name),
                    "size": p.get("size", page_size),
                    "visuals": p_arranged,
                })
        else:
            pages.append({
                "name": page_name,
                "size": page_size,
                "visuals": copy.deepcopy(arranged_visuals),
            })

        # 5. Construct dashboards array
        dashboards = []
        if raw_dashboards:
            for d in raw_dashboards:
                dashboards.append({
                    "name": d.get("name", page_name),
                    "width": d.get("width", 644),
                    "height": d.get("height", page_size.get("height", 560)),
                })
        else:
            dashboards.append({
                "name": page_name,
                "width": 644,
                "height": page_size.get("height", 560),
            })

        return {
            "visuals": arranged_visuals,
            "pages": pages,
            "dashboards": dashboards,
        }