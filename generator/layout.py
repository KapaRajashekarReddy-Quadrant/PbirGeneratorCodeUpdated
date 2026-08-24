from typing import Any, Dict, List
from generator.visual import VisualGenerator


class LayoutGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata) if isinstance(metadata, dict) else {}
        self.dashboards = self.metadata.get("dashboards", [])
        self.visual_gen = VisualGenerator(self.metadata)

    def generate_runtime_structure(self) -> Dict[str, Any]:
        """Generates dynamic runtime structure matching any schema."""
        all_visuals = []
        pages = []
        dashboards_summary = []

        # If no explicit dashboard array is defined, treat worksheets as a single default canvas
        if not isinstance(self.dashboards, list) or not self.dashboards:
            worksheets = self.metadata.get("worksheets", {})
            sheet_keys = worksheets.keys() if isinstance(worksheets, dict) else [ws.get("name") for ws in worksheets if isinstance(ws, dict)]
            
            default_visuals = []
            cur_y = 10
            z_idx = 1
            for name in sheet_keys:
                layout = {"x": 10, "y": cur_y, "width": 400, "height": 250}
                vis = self.visual_gen.get_runtime_visual(name, layout, z_idx)
                default_visuals.append(vis)
                cur_y += 260
                z_idx += 1

            return {
                "visuals": default_visuals,
                "pages": [{"name": "Default Page", "size": {"width": 1000, "height": max(800, cur_y)}, "visuals": default_visuals}],
                "dashboards": [{"name": "Default Dashboard", "width": 1000, "height": max(800, cur_y)}]
            }

        # Dynamic parsing for defined dashboards
        for dash in self.dashboards:
            if not isinstance(dash, dict):
                continue

            dash_name = dash.get("dashboardName") or dash.get("name") or "Overview"
            canvas = dash.get("canvas", {})
            canvas_width = canvas.get("width") or dash.get("width") or 1000
            canvas_height = canvas.get("height") or dash.get("height") or 800

            page_visuals = []
            seen_positions = set()
            z_index = 1

            for v in dash.get("visuals", []):
                if not isinstance(v, dict):
                    continue

                name = v.get("name", "Visual")
                px = v.get("pixel_layout", {})

                if px and isinstance(px, dict):
                    x = px.get("pixel_x", 0)
                    y = px.get("pixel_y", 0)
                    width = px.get("pixel_width", 300)
                    height = px.get("pixel_height", 200)
                else:
                    # Scale down from 100,000 Tableau grid if coordinate values are raw
                    raw_x = v.get("x", 0)
                    raw_y = v.get("y", 0)
                    raw_w = v.get("width", 300)
                    raw_h = v.get("height", 200)

                    if raw_w > canvas_width or raw_h > canvas_height:
                        x = int((raw_x / 100000) * canvas_width)
                        y = int((raw_y / 100000) * canvas_height)
                        width = int((raw_w / 100000) * canvas_width)
                        height = int((raw_h / 100000) * canvas_height)
                    else:
                        x, y, width, height = raw_x, raw_y, raw_w, raw_h

                pos_key = (name, x, y, width, height)
                if pos_key in seen_positions:
                    continue
                seen_positions.add(pos_key)

                layout_dict = {"x": x, "y": y, "width": width, "height": height}
                runtime_vis = self.visual_gen.get_runtime_visual(name, layout_dict, z_index)
                
                page_visuals.append(runtime_vis)
                all_visuals.append(runtime_vis)
                z_index += 1

            pages.append({
                "name": dash_name,
                "size": {
                    "width": canvas_width,
                    "height": canvas_height
                },
                "visuals": page_visuals
            })

            dashboards_summary.append({
                "name": dash_name,
                "width": canvas_width,
                "height": canvas_height
            })

        return {
            "visuals": all_visuals,
            "pages": pages,
            "dashboards": dashboards_summary
        }
