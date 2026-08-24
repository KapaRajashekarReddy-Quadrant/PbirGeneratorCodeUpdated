from typing import Dict, List, Any


class LayoutGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata)
        self.dashboards = self.metadata.get("dashboards", [])

    def get_dashboard_layouts(self) -> List[Dict[str, Any]]:
        """Extracts canvas configuration and de-duplicated visual layouts using pixel_layout."""
        dashboard_configs = []

        for dash in self.dashboards:
            canvas = dash.get("canvas", {})
            visuals = []
            seen_positions = set()

            for v in dash.get("visuals", []):
                name = v.get("name")
                px = v.get("pixel_layout", {})

                # Extract pixel coordinates
                x = px.get("pixel_x", 0)
                y = px.get("pixel_y", 0)
                width = px.get("pixel_width", 300)
                height = px.get("pixel_height", 200)

                # Skip duplicate visual placements
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
                "dashboardName": dash.get("dashboardName", "Main Dashboard"),
                "canvas": {
                    "width": canvas.get("width", 1000),
                    "height": canvas.get("height", 800)
                },
                "coordinateSystem": dash.get("coordinateSystem", "tableau_0_100000"),
                "visuals": visuals
            })

        return dashboard_configs
