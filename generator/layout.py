from typing import Dict, List, Any


class LayoutGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata) if isinstance(metadata, dict) else {}
        self.dashboards = self.metadata.get("dashboards", [])

    def get_dashboard_layouts(self) -> List[Dict[str, Any]]:
        """Dynamically parses canvas properties and visual layout positioning."""
        dashboard_configs = []

        if not isinstance(self.dashboards, list):
            return dashboard_configs

        for dash in self.dashboards:
            if not isinstance(dash, dict):
                continue

            canvas = dash.get("canvas", {})
            canvas_width = canvas.get("width", 1000)
            canvas_height = canvas.get("height", 800)

            visuals = []
            seen_positions = set()

            for v in dash.get("visuals", []):
                if not isinstance(v, dict):
                    continue

                name = v.get("name", "Visual")
                px = v.get("pixel_layout", {})

                # Coordinate extraction with fallbacks
                if px and isinstance(px, dict):
                    x = px.get("pixel_x", 0)
                    y = px.get("pixel_y", 0)
                    width = px.get("pixel_width", 300)
                    height = px.get("pixel_height", 200)
                else:
                    # Scale down from Tableau 100,000 grid if pixel_layout is missing
                    raw_x = v.get("x", 0)
                    raw_y = v.get("y", 0)
                    raw_w = v.get("width", 20000)
                    raw_h = v.get("height", 20000)

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

                visuals.append({
                    "name": name,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                })

            dashboard_configs.append({
                "dashboardName": dash.get("dashboardName") or dash.get("name", "Main Dashboard"),
                "canvas": {
                    "width": canvas_width,
                    "height": canvas_height
                },
                "coordinateSystem": dash.get("coordinateSystem", "pixel"),
                "visuals": visuals
            })

        return dashboard_configs
