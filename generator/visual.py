# # # import re
# # # from typing import Any, Dict, List, Optional


# # # class VisualGenerator:
# # #     def __init__(self, metadata: Dict[str, Any]):
# # #         self.metadata = metadata or {}
# # #         self.worksheets = self.metadata.get("worksheets", {})
# # #         self.tables_meta = self.metadata.get("tables", {})
# # #         self.measures_meta = self.metadata.get("measures", [])
        
# # #         # Build quick lookup for calculation definitions
# # #         self.calc_lookup = {}
# # #         if isinstance(self.measures_meta, list):
# # #             for c in self.measures_meta:
# # #                 if isinstance(c, dict):
# # #                     calc_id = c.get("calculationId")
# # #                     calc_name = c.get("name")
# # #                     if calc_id:
# # #                         self.calc_lookup[calc_id] = c
# # #                     if calc_name:
# # #                         self.calc_lookup[calc_name] = c

# # #     def _extract_title_text(self, title_obj: Any, default_name: str) -> str:
# # #         """
# # #         Dynamically extracts a pure string title from title dict, string, or fallback.
# # #         Ensures title is never returned as a JSON object.
# # #         """
# # #         if isinstance(title_obj, dict):
# # #             # Prioritize clean display text over raw text
# # #             title = (
# # #                 title_obj.get("displayText")
# # #                 or title_obj.get("text")
# # #                 or title_obj.get("source")
# # #                 or default_name
# # #             )
# # #         elif isinstance(title_obj, str):
# # #             title = title_obj
# # #         else:
# # #             title = default_name

# # #         # Clean dynamic Tableau markup like '<Sheet Name>'
# # #         title_str = str(title).strip()
# # #         if title_str.lower() in ["<sheet name>", "sheet name", ""]:
# # #             return str(default_name).strip()
# # #         return title_str

# # #     def _infer_table_for_column(self, col_name: str) -> str:
# # #         """Dynamically finds which table contains the column."""
# # #         if not col_name:
# # #             if isinstance(self.tables_meta, dict) and self.tables_meta:
# # #                 return next(iter(self.tables_meta.keys()))
# # #             return "Table"

# # #         clean = re.sub(r"[\[\]]", "", str(col_name)).strip()
# # #         if isinstance(self.tables_meta, dict):
# # #             for tbl, cols in self.tables_meta.items():
# # #                 if isinstance(cols, list):
# # #                     for c in cols:
# # #                         if isinstance(c, dict) and c.get("name") == clean:
# # #                             return tbl

# # #         if isinstance(self.tables_meta, dict) and self.tables_meta:
# # #             return next(iter(self.tables_meta.keys()))
# # #         return "Table"

# # #     def _map_visual_type(self, raw_type: str) -> str:
# # #         """Maps any visual type to Power BI visual string."""
# # #         if not raw_type:
# # #             return "tableEx"
# # #         t = str(raw_type).lower()
# # #         if "line" in t:
# # #             return "lineChart"
# # #         elif "pie" in t:
# # #             return "pieChart"
# # #         elif "card" in t or "kpi" in t:
# # #             return "card"
# # #         elif "table" in t or "text" in t:
# # #             return "tableEx"
# # #         return "tableEx"

# # #     def _extract_fields(self, ws: Dict[str, Any]):
# # #         """Dynamically extracts dimensions and measures."""
# # #         dims = list(ws.get("dimensions", []))
# # #         meas = list(ws.get("measures", []))

# # #         # Fallback to fields array if dimensions/measures are not pre-partitioned
# # #         if not dims and not meas:
# # #             fields = ws.get("fields", []) or ws.get("columns", [])
# # #             for f in fields:
# # #                 if not isinstance(f, dict):
# # #                     continue
# # #                 role = str(f.get("role", "")).lower()
# # #                 dtype = str(f.get("dataType", "")).lower()
# # #                 if role == "dimension" or "name" in dtype:
# # #                     dims.append(f)
# # #                 else:
# # #                     meas.append(f)
# # #         return dims, meas

# # #     def build_visual(self, sheet_name: str, layout: Dict[str, Any]) -> Dict[str, Any]:
# # #         """Constructs a runtime visual object with pure string title."""
# # #         ws = {}
# # #         if isinstance(self.worksheets, dict):
# # #             ws = self.worksheets.get(sheet_name, {})
# # #         elif isinstance(self.worksheets, list):
# # #             for item in self.worksheets:
# # #                 if isinstance(item, dict) and item.get("name") == sheet_name:
# # #                     ws = item
# # #                     break

# # #         v_type = self._map_visual_type(ws.get("visualType", ""))
        
# # #         # Pure string extraction for title
# # #         title_str = self._extract_title_text(ws.get("title"), sheet_name)

# # #         dims, meas = self._extract_fields(ws)

# # #         # 1. Bindings
# # #         bindings: Dict[str, Any] = {}
        
# # #         # Category or X Binding
# # #         if dims:
# # #             d = dims[0]
# # #             d_name = d.get("column") or d.get("name") or "Category"
# # #             d_table = d.get("table") or self._infer_table_for_column(d_name)
            
# # #             if v_type == "lineChart":
# # #                 bindings["X"] = {"table": d_table, "column": d_name}
# # #             else:
# # #                 bindings["Category"] = {"table": d_table, "column": d_name}

# # #         # Y (Measures) Binding
# # #         y_list = []
# # #         for m in meas:
# # #             m_name = m.get("name") or m.get("column") or "Value"
# # #             m_table = m.get("table") or self._infer_table_for_column(m_name)
            
# # #             is_calc = (
# # #                 m.get("fieldType") == "calculatedField"
# # #                 or bool(m.get("formula"))
# # #                 or bool(m.get("calculationId"))
# # #                 or m_name in self.calc_lookup
# # #             )

# # #             if is_calc:
# # #                 y_list.append({
# # #                     "table": m_table,
# # #                     "measure": m_name
# # #                 })
# # #             else:
# # #                 y_list.append({
# # #                     "table": m_table,
# # #                     "column": m.get("column") or m_name,
# # #                     "aggregation": m.get("derivation") or "Sum"
# # #                 })

# # #         if y_list:
# # #             bindings["Y"] = y_list

# # #         # 2. SortBy
# # #         sort_by: Dict[str, Any] = {}
# # #         if "Y" in bindings and bindings["Y"]:
# # #             sort_by = {
# # #                 "target": bindings["Y"][0],
# # #                 "direction": "Descending"
# # #             }
# # #         elif "Category" in bindings:
# # #             sort_by = {
# # #                 "target": bindings["Category"],
# # #                 "direction": "Ascending"
# # #             }
# # #         elif "X" in bindings:
# # #             sort_by = {
# # #                 "target": bindings["X"],
# # #                 "direction": "Ascending"
# # #             }

# # #         # 3. Filters
# # #         filters = []
# # #         for flt in ws.get("filters", []):
# # #             if isinstance(flt, dict):
# # #                 col = flt.get("column") or flt.get("name") or "FilterColumn"
# # #                 tbl = flt.get("table") or self._infer_table_for_column(col)
# # #                 filters.append({
# # #                     "table": tbl,
# # #                     "column": col,
# # #                     "operator": flt.get("operator", "In"),
# # #                     "values": flt.get("values", [])
# # #                 })

# # #         return {
# # #             "visualType": v_type,
# # #             "title": title_str,
# # #             "layout": {
# # #                 "x": layout.get("x", 18),
# # #                 "y": layout.get("y", 99),
# # #                 "width": layout.get("width", 608),
# # #                 "height": layout.get("height", 225),
# # #                 "z": layout.get("z", 1)
# # #             },
# # #             "bindings": bindings,
# # #             "sortBy": sort_by,
# # #             "filters": filters,
# # #             "properties": [
# # #                 {
# # #                     "objectName": "values",
# # #                     "propertyName": "labelDisplayUnits",
# # #                     "value": 1000
# # #                 }
# # #             ]
# # #         }

# # # generator/visual.py
# # import re
# # from typing import Any, Dict, List, Optional
# # from generator.utils import map_visual_type


# # class VisualGenerator:
# #     def __init__(self, metadata: Dict[str, Any]):
# #         self.metadata = metadata or {}
# #         self.worksheets = self.metadata.get("worksheets", {})
# #         self.tables_meta = self.metadata.get("tables", {})
# #         self.measures_meta = self.metadata.get("measures", [])

# #         # Quick lookup for calculation definitions
# #         self.calc_lookup = {}
# #         if isinstance(self.measures_meta, list):
# #             for c in self.measures_meta:
# #                 if isinstance(c, dict):
# #                     calc_id = c.get("calculationId")
# #                     calc_name = c.get("name")
# #                     if calc_id:
# #                         self.calc_lookup[calc_id] = c
# #                     if calc_name:
# #                         self.calc_lookup[calc_name] = c

# #     def _extract_title_text(self, title_obj: Any, default_name: str) -> str:
# #         """
# #         Dynamically extracts a pure string title from title dict, string, or fallback.
# #         Ensures title is never returned as a JSON object.
# #         """
# #         if isinstance(title_obj, dict):
# #             title = (
# #                 title_obj.get("displayText")
# #                 or title_obj.get("text")
# #                 or title_obj.get("source")
# #                 or default_name
# #             )
# #         elif isinstance(title_obj, str):
# #             title = title_obj
# #         else:
# #             title = default_name

# #         title_str = str(title).strip()
# #         if title_str.lower() in ["<sheet name>", "sheet name", ""]:
# #             return str(default_name).strip()
# #         return title_str

# #     def _infer_table_for_column(self, col_name: str) -> str:
# #         """Dynamically finds which table contains the column."""
# #         if not col_name:
# #             if isinstance(self.tables_meta, dict) and self.tables_meta:
# #                 return next(iter(self.tables_meta.keys()))
# #             return "Table"

# #         clean = re.sub(r"[\[\]]", "", str(col_name)).strip()
# #         if isinstance(self.tables_meta, dict):
# #             for tbl, cols in self.tables_meta.items():
# #                 if isinstance(cols, list):
# #                     for c in cols:
# #                         if isinstance(c, dict) and c.get("name") == clean:
# #                             return tbl

# #         if isinstance(self.tables_meta, dict) and self.tables_meta:
# #             return next(iter(self.tables_meta.keys()))
# #         return "Table"

# #     def _extract_fields(self, ws: Dict[str, Any]):
# #         """Dynamically extracts dimensions and measures."""
# #         dims = list(ws.get("dimensions", []))
# #         meas = list(ws.get("measures", []))

# #         # Fallback to fields array if dimensions/measures are not pre-partitioned
# #         if not dims and not meas:
# #             fields = ws.get("fields", []) or ws.get("columns", [])
# #             for f in fields:
# #                 if not isinstance(f, dict):
# #                     continue
# #                 role = str(f.get("role", "")).lower()
# #                 dtype = str(f.get("dataType", "")).lower()
# #                 if role == "dimension" or "name" in dtype:
# #                     dims.append(f)
# #                 else:
# #                     meas.append(f)
# #         return dims, meas

# #     def build_visual(self, sheet_name: str, layout: Dict[str, Any]) -> Dict[str, Any]:
# #         """Constructs a single runtime visual object with standard visual types."""
# #         ws = {}
# #         if isinstance(self.worksheets, dict):
# #             ws = self.worksheets.get(sheet_name, {})
# #         elif isinstance(self.worksheets, list):
# #             for item in self.worksheets:
# #                 if isinstance(item, dict) and item.get("name") == sheet_name:
# #                     ws = item
# #                     break

# #         # Unified single-pass mapping
# #         raw_visual_type = ws.get("visualType") or ws.get("mark") or ws.get("type") or ""
# #         v_type = map_visual_type(raw_visual_type)

# #         title_str = self._extract_title_text(ws.get("title"), sheet_name)
# #         dims, meas = self._extract_fields(ws)

# #         # 1. Bindings
# #         bindings: Dict[str, Any] = {}

# #         if dims:
# #             d = dims[0]
# #             d_name = d.get("column") or d.get("name") or "Category"
# #             d_table = d.get("table") or self._infer_table_for_column(d_name)

# #             if v_type == "lineChart":
# #                 bindings["X"] = {"table": d_table, "column": d_name}
# #             else:
# #                 bindings["Category"] = {"table": d_table, "column": d_name}

# #         # Y (Measures) Binding
# #         y_list = []
# #         for m in meas:
# #             m_name = m.get("name") or m.get("column") or "Value"
# #             m_table = m.get("table") or self._infer_table_for_column(m_name)

# #             is_calc = (
# #                 m.get("fieldType") == "calculatedField"
# #                 or bool(m.get("formula"))
# #                 or bool(m.get("calculationId"))
# #                 or m_name in self.calc_lookup
# #             )

# #             if is_calc:
# #                 y_list.append({
# #                     "table": m_table,
# #                     "measure": m_name
# #                 })
# #             else:
# #                 y_list.append({
# #                     "table": m_table,
# #                     "column": m.get("column") or m_name,
# #                     "aggregation": m.get("derivation") or "Sum"
# #                 })

# #         if y_list:
# #             bindings["Y"] = y_list

# #         # 2. SortBy
# #         sort_by: Dict[str, Any] = {}
# #         if "Y" in bindings and bindings["Y"]:
# #             sort_by = {
# #                 "target": bindings["Y"][0],
# #                 "direction": "Descending"
# #             }
# #         elif "Category" in bindings:
# #             sort_by = {
# #                 "target": bindings["Category"],
# #                 "direction": "Ascending"
# #             }
# #         elif "X" in bindings:
# #             sort_by = {
# #                 "target": bindings["X"],
# #                 "direction": "Ascending"
# #             }

# #         # 3. Filters
# #         filters = []
# #         for flt in ws.get("filters", []):
# #             if isinstance(flt, dict):
# #                 col = flt.get("column") or flt.get("name") or "FilterColumn"
# #                 tbl = flt.get("table") or self._infer_table_for_column(col)
# #                 filters.append({
# #                     "table": tbl,
# #                     "column": col,
# #                     "operator": flt.get("operator", "In"),
# #                     "values": flt.get("values", [])
# #                 })

# #         return {
# #             "visualType": v_type,
# #             "title": title_str,
# #             "layout": {
# #                 "x": layout.get("x", 18),
# #                 "y": layout.get("y", 99),
# #                 "width": layout.get("width", 608),
# #                 "height": layout.get("height", 225),
# #                 "z": layout.get("z", 1)
# #             },
# #             "bindings": bindings,
# #             "sortBy": sort_by,
# #             "filters": filters,
# #             "properties": [
# #                 {
# #                     "objectName": "values",
# #                     "propertyName": "labelDisplayUnits",
# #                     "value": 1000
# #                 }
# #             ]
# #         }


import re
from typing import Any, Dict, List, Optional
from generator.utils import map_visual_type
 
 
class VisualGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata or {}
        self.worksheets = self.metadata.get("worksheets", {})
        self.tables_meta = self.metadata.get("tables", {})
        self.measures_meta = self.metadata.get("measures", [])
 
        # Quick lookup for calculation definitions
        self.calc_lookup = {}
        if isinstance(self.measures_meta, list):
            for c in self.measures_meta:
                if isinstance(c, dict):
                    calc_id = c.get("calculationId")
                    calc_name = c.get("name")
                    if calc_id:
                        self.calc_lookup[calc_id] = c
                    if calc_name:
                        self.calc_lookup[calc_name] = c
 
    def _extract_title_text(self, title_obj: Any, default_name: str) -> str:
        """
        Dynamically extracts a pure string title from title dict, string, or fallback.
        Ensures title is never returned as a JSON object.
        """
        if isinstance(title_obj, dict):
            title = (
                title_obj.get("displayText")
                or title_obj.get("text")
                or title_obj.get("source")
                or default_name
            )
        elif isinstance(title_obj, str):
            title = title_obj
        else:
            title = default_name
 
        title_str = str(title).strip()
        if title_str.lower() in ["<sheet name>", "sheet name", ""]:
            return str(default_name).strip()
        return title_str
 
    def _infer_table_for_column(self, col_name: str) -> str:
        """Dynamically finds which table contains the column."""
        if not col_name:
            if isinstance(self.tables_meta, dict) and self.tables_meta:
                return next(iter(self.tables_meta.keys()))
            return "Table"
 
        clean = re.sub(r"[\[\]]", "", str(col_name)).strip()
        if isinstance(self.tables_meta, dict):
            for tbl, cols in self.tables_meta.items():
                if isinstance(cols, list):
                    for c in cols:
                        if isinstance(c, dict) and c.get("name") == clean:
                            return tbl
 
        if isinstance(self.tables_meta, dict) and self.tables_meta:
            return next(iter(self.tables_meta.keys()))
        return "Table"
 
    @staticmethod
    def _normalize_name(name: Any) -> str:
        """Normalizes a sheet/visual name for fuzzy matching: lowercase,
        strip whitespace, and drop trailing Tableau duplicate suffixes like
        ' (2)' or '_1' that dashboards commonly add to repeated zones."""
        if not name:
            return ""
        s = str(name).strip().lower()
        s = re.sub(r"\s*\(\d+\)\s*$", "", s)   # trailing " (2)"
        s = re.sub(r"[_\-\s]+\d+$", "", s)      # trailing "_1", "-2", " 3"
        s = re.sub(r"[^a-z0-9]+", "", s)        # strip remaining punctuation/spaces
        return s
 
    def _find_worksheet(self, sheet_name: str) -> Dict[str, Any]:
        """Dynamically resolves a worksheet for any report, tolerant of
        naming mismatches between a dashboard's visual/zone name and the
        worksheet key it actually refers to (case, spacing, numeric
        dedupe suffixes, etc.). Falls back gracefully to {} only if truly
        nothing can be matched."""
        if not sheet_name:
            return {}
 
        # Build (or reuse) a list of (name, worksheet_dict) pairs regardless
        # of whether worksheets is a dict keyed by name or a list of dicts.
        items = []
        if isinstance(self.worksheets, dict):
            items = list(self.worksheets.items())
        elif isinstance(self.worksheets, list):
            for item in self.worksheets:
                if isinstance(item, dict):
                    items.append((item.get("name") or item.get("id") or "", item))
 
        if not items:
            return {}
 
        # 1. Exact match
        for name, ws in items:
            if name == sheet_name:
                return ws
 
        # 2. Case-insensitive / whitespace-tolerant match
        target_lower = str(sheet_name).strip().lower()
        for name, ws in items:
            if str(name).strip().lower() == target_lower:
                return ws
 
        # 3. Fully normalized match (handles "Sheet 1 (2)" -> "sheet1")
        target_norm = self._normalize_name(sheet_name)
        if target_norm:
            for name, ws in items:
                if self._normalize_name(name) == target_norm:
                    return ws
 
        # 4. Substring match as a last resort (one name contains the other)
        for name, ws in items:
            name_lower = str(name).strip().lower()
            if name_lower and (name_lower in target_lower or target_lower in name_lower):
                return ws
 
        return {}
 
    def _extract_fields(self, ws: Dict[str, Any]):
        """Dynamically extracts dimensions and measures."""
        dims = list(ws.get("dimensions", []))
        meas = list(ws.get("measures", []))
 
        # Fallback to fields array if dimensions/measures are not pre-partitioned
        if not dims and not meas:
            fields = ws.get("fields", []) or ws.get("columns", [])
            for f in fields:
                if not isinstance(f, dict):
                    continue
                role = str(f.get("role", "")).lower()
                dtype = str(f.get("dataType", "")).lower()
                if role == "dimension" or "name" in dtype:
                    dims.append(f)
                else:
                    meas.append(f)
        return dims, meas
 
    @staticmethod
    def _classify_role(field: Dict[str, Any]) -> str:
        """Reads an explicit role/shelf tag off a field, when the source
        metadata provides one (legend/color, tooltip, detail, size, etc.).
        Different report exports use different key names for this, so all
        the common ones are checked dynamically."""
        raw = (
            field.get("visualRole")
            or field.get("fieldRole")
            or field.get("shelf")
            or field.get("encoding")
            or field.get("markRole")
            or ""
        )
        return str(raw).strip().lower()
 
    @staticmethod
    def _is_calc_field(field: Dict[str, Any], calc_lookup: Dict[str, Any], name: str) -> bool:
        return bool(
            field.get("fieldType") == "calculatedField"
            or field.get("formula")
            or field.get("calculationId")
            or name in calc_lookup
        )
 
    def _field_binding(self, f: Dict[str, Any]) -> Dict[str, Any]:
        name = f.get("column") or f.get("name") or "Field"
        table = f.get("table") or self._infer_table_for_column(name)
        return {"table": table, "column": name}
 
    def _measure_binding(self, m: Dict[str, Any]) -> Dict[str, Any]:
        m_name = m.get("name") or m.get("column") or "Value"
        m_table = m.get("table") or self._infer_table_for_column(m_name)
        if self._is_calc_field(m, self.calc_lookup, m_name):
            return {"table": m_table, "measure": m_name}
        return {
            "table": m_table,
            "column": m.get("column") or m_name,
            "aggregation": m.get("derivation") or "Sum",
        }
 
    def _build_bindings(self, dims: List[Dict[str, Any]], meas: List[Dict[str, Any]], v_type: str) -> Dict[str, Any]:
        """Dynamically builds bindings so that no field/role is ever dropped.
 
        Every dimension and measure is placed into its binding role - if the
        source metadata explicitly tags a field's role (legend/color,
        tooltip, detail, size), that's honored directly. Fields without an
        explicit tag fall back to a positional rule: the first dimension is
        the primary axis (Category/X, or Rows for matrix visuals), and any
        *additional* dimensions become Legend/Columns instead of being
        silently discarded - which is what previously happened whenever a
        visual carried more than one dimension role.
        """
        bindings: Dict[str, Any] = {}
 
        role_buckets = {"legend": [], "color": [], "tooltip": [], "detail": [], "details": [], "size": []}
        leftover_dims = []
        for d in dims:
            role = self._classify_role(d)
            if role in role_buckets:
                role_buckets[role].append(d)
            else:
                leftover_dims.append(d)
 
        if v_type == "pivotTable" and len(leftover_dims) >= 2:
            # Matrix-style visual: split remaining dims into Rows + Columns
            # instead of collapsing everything into a single Category field.
            bindings["Rows"] = [self._field_binding(d) for d in leftover_dims[:-1]]
            bindings["Columns"] = [self._field_binding(leftover_dims[-1])]
        elif leftover_dims:
            primary_key = "X" if v_type == "lineChart" else "Category"
            bindings[primary_key] = self._field_binding(leftover_dims[0])
            # Any dimension beyond the first is a second role (commonly the
            # Legend/series breakdown) - never dropped.
            extra_dims = leftover_dims[1:]
            legend_fields = role_buckets["legend"] + role_buckets["color"] + extra_dims
            if legend_fields:
                bindings["Legend"] = [self._field_binding(f) for f in legend_fields]
        else:
            legend_fields = role_buckets["legend"] + role_buckets["color"]
            if legend_fields:
                bindings["Legend"] = [self._field_binding(f) for f in legend_fields]
 
        detail_fields = role_buckets["detail"] + role_buckets["details"]
        if detail_fields:
            bindings["Details"] = [self._field_binding(f) for f in detail_fields]
        if role_buckets["tooltip"]:
            bindings.setdefault("Tooltip", []).extend(self._field_binding(f) for f in role_buckets["tooltip"])
        if role_buckets["size"]:
            bindings.setdefault("Size", []).extend(self._field_binding(f) for f in role_buckets["size"])
 
        # Measures: same principle - route explicitly-tagged size/tooltip
        # measures to their own role, everything else becomes Y (values).
        y_list, size_list, tooltip_list = [], [], []
        for m in meas:
            role = self._classify_role(m)
            entry = self._measure_binding(m)
            if role == "size":
                size_list.append(entry)
            elif role == "tooltip":
                tooltip_list.append(entry)
            else:
                y_list.append(entry)
 
        if y_list:
            bindings["Y"] = y_list
        if size_list:
            bindings.setdefault("Size", []).extend(size_list)
        if tooltip_list:
            bindings.setdefault("Tooltip", []).extend(tooltip_list)
 
        return bindings
 
    def build_visual(
        self,
        sheet_name: str,
        layout: Dict[str, Any],
        visual_meta: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Constructs a single runtime visual object with standard visual types.
 
        visual_meta is the raw visual/zone entry as it appears directly under
        a dashboard's "visuals" list (when present). Reports vary in how much
        detail lives on the dashboard entry vs. the worksheets map, so both
        sources are merged dynamically: values already present on visual_meta
        win, and anything missing is filled in from the resolved worksheet.
        This is what keeps bindings populated for every report instead of
        only the ones whose visual name happens to exactly match a worksheet key.
        """
        visual_meta = visual_meta if isinstance(visual_meta, dict) else {}
 
        ws = self._find_worksheet(sheet_name)
 
        # If the dashboard visual itself already carries pre-built bindings
        # (as some report exports do), honor them directly rather than
        # rebuilding from dimensions/measures.
        prebuilt_bindings = visual_meta.get("bindings") if isinstance(visual_meta.get("bindings"), dict) else None
 
        # Unified single-pass mapping: prefer whatever type info is on the
        # dashboard visual entry, then fall back to the worksheet.
        raw_visual_type = (
            visual_meta.get("visualType")
            or visual_meta.get("mark")
            or visual_meta.get("type")
            or ws.get("visualType")
            or ws.get("mark")
            or ws.get("type")
            or ""
        )
        v_type = map_visual_type(raw_visual_type)
 
        title_str = self._extract_title_text(
            visual_meta.get("title") or ws.get("title"), sheet_name
        )
 
        # Merge dims/measures: dashboard-level fields (if any) take priority,
        # then fall back to the resolved worksheet's fields.
        dims, meas = self._extract_fields(visual_meta)
        if not dims and not meas:
            dims, meas = self._extract_fields(ws)
 
        # 1. Bindings - use whatever the source already provides if present,
        # otherwise build dynamically from ALL dims/measures (every role
        # gets placed, none are dropped even when a visual has 2+ roles).
        bindings: Dict[str, Any] = dict(prebuilt_bindings) if prebuilt_bindings else {}
 
        if not bindings:
            bindings = self._build_bindings(dims, meas, v_type)
 
        # 2. SortBy - dynamic fallback across every role that could anchor a sort.
        sort_by: Dict[str, Any] = {}
        for role in ("Y", "X", "Category", "Rows", "Columns", "Legend"):
            target = bindings.get(role)
            if not target:
                continue
            target_field = target[0] if isinstance(target, list) else target
            sort_by = {
                "target": target_field,
                "direction": "Descending" if role in ("Y",) else "Ascending",
            }
            break
 
        # 3. Filters - merge whichever source actually has them (dashboard
        # visual entry takes priority, worksheet is the dynamic fallback).
        filters = []
        raw_filters = visual_meta.get("filters") or ws.get("filters", [])
        for flt in raw_filters:
            if isinstance(flt, dict):
                col = flt.get("column") or flt.get("name") or "FilterColumn"
                tbl = flt.get("table") or self._infer_table_for_column(col)
                filters.append({
                    "table": tbl,
                    "column": col,
                    "operator": flt.get("operator", "In"),
                    "values": flt.get("values", [])
                })
 
        return {
            "visualType": v_type,
            "title": title_str,
            "layout": {
                "x": layout.get("x", 18),
                "y": layout.get("y", 99),
                "width": layout.get("width", 608),
                "height": layout.get("height", 225),
                "z": layout.get("z", 1)
            },
            "bindings": bindings,
            "sortBy": sort_by,
            "filters": filters,
            "properties": [
                {
                    "objectName": "values",
                    "propertyName": "labelDisplayUnits",
                    "value": 1000
                }
            ]
        }
 
