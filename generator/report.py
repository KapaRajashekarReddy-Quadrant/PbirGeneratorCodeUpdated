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
import json
from typing import Any, Dict, List
from generator.layout import LayoutGenerator
from generator.visual import VisualGenerator

# Zone/role hints that mark a dashboard entry as a companion widget (legend,
# filter, title bar, etc.) rather than an actual chart. These should never
# become their own duplicate visual - they ride along with their parent
# chart instead. Matched dynamically against whatever hint field the source
# export provides (zoneType/role/class/kind), so this isn't tied to any one
# report's naming.
_COMPANION_ZONE_HINTS = {
    "legend", "color-legend", "colorlegend", "size-legend", "sizelegend",
    "filter", "quickfilter", "quick-filter", "title", "text-legend",
}


class ReportGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        # Unwrap nested metadata if present
        if isinstance(metadata, dict) and "metadata" in metadata:
            self.metadata = metadata["metadata"]
        else:
            self.metadata = metadata or {}

        self.layout_gen = LayoutGenerator(self.metadata)
        self.visual_gen = VisualGenerator(self.metadata)

    @staticmethod
    def _is_companion_zone(v: Dict[str, Any]) -> bool:
        """Dynamically detects legend/filter/title companion zones using
        whichever hint field the source export happens to provide."""
        hint = str(
            v.get("zoneType") or v.get("zone_type") or v.get("role")
            or v.get("class") or v.get("kind") or ""
        ).strip().lower()
        return hint in _COMPANION_ZONE_HINTS

    @staticmethod
    def _content_signature(title: str, bindings: Dict[str, Any]) -> str:
        """Fingerprint of *what a visual actually shows* (title + bindings),
        independent of its size/position on the canvas. Two zones that
        resolve to this same signature are rendering the same underlying
        chart data - almost always a legend/companion duplicate, not two
        genuinely different visuals."""
        norm_title = VisualGenerator._normalize_name(title)
        try:
            norm_bindings = json.dumps(bindings, sort_keys=True, default=str)
        except Exception:
            norm_bindings = str(bindings)
        return f"{norm_title}::{norm_bindings}"

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

            page_visuals: List[Dict[str, Any]] = []
            seen_positions = set()
            # signature -> index into page_visuals/all_visuals, so a later
            # duplicate can replace an earlier smaller one if it turns out
            # to be the bigger/"real" chart.
            seen_signatures: Dict[str, int] = {}
            z_counter = 1

            for v in dash.get("visuals", []):
                if not isinstance(v, dict):
                    continue

                # Skip legend/filter/title companion zones outright - they
                # describe an existing chart rather than being one.
                if self._is_companion_zone(v):
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

                # Guard 1: exact same zone re-listed in the source (same
                # stable id, or identical name+coords).
                visual_key = v.get("id") or v.get("visualId") or v.get("zoneId")
                key = visual_key if visual_key else (name, x, y, w, h)
                if key in seen_positions:
                    continue
                seen_positions.add(key)

                layout_obj = {"x": x, "y": y, "width": w, "height": h, "z": z_counter}
                runtime_vis = self.visual_gen.build_visual(name, layout_obj, visual_meta=v)

                # Guard 2: content-based dedup. Two zones with the same
                # title + bindings are showing the same chart twice (the
                # classic "full chart" + "mini legend/thumbnail duplicate"
                # pattern) even though their ids/coords differ. Keep only
                # the larger one.
                sig = self._content_signature(runtime_vis.get("title", ""), runtime_vis.get("bindings", {}))
                if sig and sig in seen_signatures:
                    prev_idx = seen_signatures[sig]
                    prev_vis = page_visuals[prev_idx]
                    prev_area = prev_vis["layout"]["width"] * prev_vis["layout"]["height"]
                    new_area = w * h
                    if new_area > prev_area:
                        # Replace the smaller duplicate with this bigger one.
                        runtime_vis["layout"]["z"] = prev_vis["layout"]["z"]
                        page_visuals[prev_idx] = runtime_vis
                        all_idx = all_visuals.index(prev_vis)
                        all_visuals[all_idx] = runtime_vis
                    # Either way, don't append a second visual for this signature.
                    continue

                page_visuals.append(runtime_vis)
                all_visuals.append(runtime_vis)
                if sig:
                    seen_signatures[sig] = len(page_visuals) - 1
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
