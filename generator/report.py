# from typing import Any, Dict, List
# from generator.layout import LayoutGenerator
# from generator.visual import VisualGenerator


# class ReportGenerator:
#     def __init__(self, metadata: Dict[str, Any]):
#         # Unwrap nested metadata if present
#         if isinstance(metadata, dict) and "metadata" in metadata:
#             self.metadata = metadata["metadata"]
#         else:
#             self.metadata = metadata or {}

#         self.layout_gen = LayoutGenerator(self.metadata)
#         self.visual_gen = VisualGenerator(self.metadata)

#     def generate_runtime_json(self) -> Dict[str, Any]:
#         """
#         Builds the exact Power BI runtime JSON structure:
#         {
#           "visuals": [...],
#           "pages": [...],
#           "dashboards": [...]
#         }
#         """
#         dashboards_meta = self.metadata.get("dashboards", [])
#         worksheets_meta = self.metadata.get("worksheets", {})

#         all_visuals = []
#         pages = []
#         dashboards_list = []

#         # If no dashboards are defined, auto-generate from worksheets
#         if not dashboards_meta:
#             sheet_names = (
#                 list(worksheets_meta.keys())
#                 if isinstance(worksheets_meta, dict)
#                 else [w.get("name") for w in worksheets_meta if isinstance(w, dict)]
#             )
            
#             page_visuals = []
#             y_offset = 50
#             for idx, s_name in enumerate(sheet_names, start=1):
#                 layout = {"x": 20, "y": y_offset, "width": 600, "height": 220, "z": idx}
#                 vis = self.visual_gen.build_visual(s_name, layout)
#                 page_visuals.append(vis)
#                 all_visuals.append(vis)
#                 y_offset += 240

#             page_obj = {
#                 "name": "Production Overview",
#                 "size": {"width": 646, "height": max(560, y_offset + 50)},
#                 "visuals": page_visuals
#             }
#             pages.append(page_obj)
#             dashboards_list.append({"name": "Production Overview", "width": 646, "height": max(560, y_offset + 50)})

#             return {
#                 "visuals": all_visuals,
#                 "pages": pages,
#                 "dashboards": dashboards_list
#             }

#         # Dynamically iterate over each dashboard
#         for dash in dashboards_meta:
#             if not isinstance(dash, dict):
#                 continue

#             dash_name = dash.get("dashboardName") or dash.get("name") or "Overview"
#             canvas = dash.get("canvas", {})
#             canvas_w = canvas.get("width") or dash.get("width") or 646
#             canvas_h = canvas.get("height") or dash.get("height") or 560

#             page_visuals = []
#             seen_positions = set()
#             z_counter = 1

#             for v in dash.get("visuals", []):
#                 if not isinstance(v, dict):
#                     continue

#                 name = v.get("name", "Visual")
#                 px = v.get("pixel_layout", {})

#                 # Dynamic coordinate handling
#                 if px and isinstance(px, dict):
#                     x = px.get("pixel_x", 0)
#                     y = px.get("pixel_y", 0)
#                     w = px.get("pixel_width", 300)
#                     h = px.get("pixel_height", 200)
#                 else:
#                     raw_x, raw_y = v.get("x", 0), v.get("y", 0)
#                     raw_w, raw_h = v.get("width", 300), v.get("height", 200)
#                     if raw_w > canvas_w or raw_h > canvas_h:
#                         x = int((raw_x / 100000) * canvas_w)
#                         y = int((raw_y / 100000) * canvas_h)
#                         w = int((raw_w / 100000) * canvas_w)
#                         h = int((raw_h / 100000) * canvas_h)
#                     else:
#                         x, y, w, h = raw_x, raw_y, raw_w, raw_h

#                 # Prevent duplicates
#                 key = (name, x, y, w, h)
#                 if key in seen_positions:
#                     continue
#                 seen_positions.add(key)

#                 layout_obj = {"x": x, "y": y, "width": w, "height": h, "z": z_counter}
#                 runtime_vis = self.visual_gen.build_visual(name, layout_obj)
                
#                 page_visuals.append(runtime_vis)
#                 all_visuals.append(runtime_vis)
#                 z_counter += 1

#             pages.append({
#                 "name": dash_name,
#                 "size": {"width": canvas_w, "height": canvas_h},
#                 "visuals": page_visuals
#             })

#             dashboards_list.append({
#                 "name": dash_name,
#                 "width": canvas_w,
#                 "height": canvas_h
#             })

#         return {
#             "visuals": all_visuals,
#             "pages": pages,
#             "dashboards": dashboards_list
#         }

from typing import Any, Dict, List
from generator.layout import LayoutGenerator
from generator.visual import VisualGenerator


class ReportGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        # Unwrap nested metadata if present
        if isinstance(metadata, dict) and "metadata" in metadata:
            self.metadata = metadata["metadata"]
        else:
            self.metadata = metadata or {}

        self.layout_gen = LayoutGenerator(self.metadata)
        self.visual_gen = VisualGenerator(self.metadata)

    def generate_runtime_json(self) -> Dict[str, Any]:
        """
        Builds the exact Power BI runtime JSON structure:
        {
          "visuals": [...],
          "pages": [...],
          "dashboards": [...]
        }
        """
        dashboards_meta = self.metadata.get("dashboards", [])
        worksheets_meta = self.metadata.get("worksheets", {})

        all_visuals = []
        pages = []
        dashboards_list = []

        # If no dashboards are defined, auto-generate from worksheets
        if not dashboards_meta:
            sheet_names = (
                list(worksheets_meta.keys())
                if isinstance(worksheets_meta, dict)
                else [w.get("name") for w in worksheets_meta if isinstance(w, dict)]
            )
            
            page_visuals = []
            y_offset = 50
            for idx, s_name in enumerate(sheet_names, start=1):
                layout = {"x": 20, "y": y_offset, "width": 600, "height": 220, "z": idx}
                vis = self.visual_gen.build_visual(s_name, layout)
                page_visuals.append(vis)
                all_visuals.append(vis)
                y_offset += 240

            page_obj = {
                "name": "Production Overview",
                "size": {"width": 646, "height": max(560, y_offset + 50)},
                "visuals": page_visuals
            }
            pages.append(page_obj)
            dashboards_list.append({"name": "Production Overview", "width": 646, "height": max(560, y_offset + 50)})

            return {
                "visuals": all_visuals,
                "pages": pages,
                "dashboards": dashboards_list
            }

        # Dynamically iterate over each dashboard
        for dash in dashboards_meta:
            if not isinstance(dash, dict):
                continue

            dash_name = dash.get("dashboardName") or dash.get("name") or "Overview"
            canvas = dash.get("canvas", {})
            canvas_w = canvas.get("width") or dash.get("width") or 646
            canvas_h = canvas.get("height") or dash.get("height") or 560

            page_visuals = []
            seen_positions = set()
            z_counter = 1

            for v in dash.get("visuals", []):
                if not isinstance(v, dict):
                    continue

                name = v.get("name", "Visual")
                px = v.get("pixel_layout", {})

                # Dynamic coordinate handling
                if px and isinstance(px, dict):
                    x = px.get("pixel_x", 0)
                    y = px.get("pixel_y", 0)
                    w = px.get("pixel_width", 300)
                    h = px.get("pixel_height", 200)
                else:
                    raw_x, raw_y = v.get("x", 0), v.get("y", 0)
                    raw_w, raw_h = v.get("width", 300), v.get("height", 200)
                    if raw_w > canvas_w or raw_h > canvas_h:
                        x = int((raw_x / 100000) * canvas_w)
                        y = int((raw_y / 100000) * canvas_h)
                        w = int((raw_w / 100000) * canvas_w)
                        h = int((raw_h / 100000) * canvas_h)
                    else:
                        x, y, w, h = raw_x, raw_y, raw_w, raw_h

                # Prevent true duplicates only - prefer a stable identifier
                # from the source (id/zoneId/visualId) when present, since
                # relying on name+x+y+w+h alone can wrongly collapse two
                # different visuals that both fell back to default coords
                # (0, 0, 300, 200) because no pixel_layout was provided.
                visual_key = v.get("id") or v.get("visualId") or v.get("zoneId")
                key = visual_key if visual_key else (name, x, y, w, h)
                if key in seen_positions:
                    continue
                seen_positions.add(key)

                layout_obj = {"x": x, "y": y, "width": w, "height": h, "z": z_counter}
                runtime_vis = self.visual_gen.build_visual(name, layout_obj, visual_meta=v)
                
                page_visuals.append(runtime_vis)
                all_visuals.append(runtime_vis)
                z_counter += 1

            pages.append({
                "name": dash_name,
                "size": {"width": canvas_w, "height": canvas_h},
                "visuals": page_visuals
            })

            dashboards_list.append({
                "name": dash_name,
                "width": canvas_w,
                "height": canvas_h
            })

        return {
            "visuals": all_visuals,
            "pages": pages,
            "dashboards": dashboards_list
        }
