import re
from typing import Any, Dict, List, Optional


class VisualGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata or {}
        self.worksheets = self.metadata.get("worksheets", {})
        self.tables_meta = self.metadata.get("tables", {})
        self.measures_meta = self.metadata.get("measures", [])
        
        # Build quick lookup for calculation definitions
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
            # Prioritize clean display text over raw text
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

        # Clean dynamic Tableau markup like '<Sheet Name>'
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

    def _map_visual_type(self, raw_type: str) -> str:
        """Maps any visual type to Power BI visual string."""
        if not raw_type:
            return "tableEx"
        t = str(raw_type).lower()
        if "line" in t:
            return "lineChart"
        elif "pie" in t:
            return "pieChart"
        elif "card" in t or "kpi" in t:
            return "card"
        elif "table" in t or "text" in t:
            return "tableEx"
        return "tableEx"

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

    def build_visual(self, sheet_name: str, layout: Dict[str, Any]) -> Dict[str, Any]:
        """Constructs a runtime visual object with pure string title."""
        ws = {}
        if isinstance(self.worksheets, dict):
            ws = self.worksheets.get(sheet_name, {})
        elif isinstance(self.worksheets, list):
            for item in self.worksheets:
                if isinstance(item, dict) and item.get("name") == sheet_name:
                    ws = item
                    break

        v_type = self._map_visual_type(ws.get("visualType", ""))
        
        # Pure string extraction for title
        title_str = self._extract_title_text(ws.get("title"), sheet_name)

        dims, meas = self._extract_fields(ws)

        # 1. Bindings
        bindings: Dict[str, Any] = {}
        
        # Category or X Binding
        if dims:
            d = dims[0]
            d_name = d.get("column") or d.get("name") or "Category"
            d_table = d.get("table") or self._infer_table_for_column(d_name)
            
            if v_type == "lineChart":
                bindings["X"] = {"table": d_table, "column": d_name}
            else:
                bindings["Category"] = {"table": d_table, "column": d_name}

        # Y (Measures) Binding
        y_list = []
        for m in meas:
            m_name = m.get("name") or m.get("column") or "Value"
            m_table = m.get("table") or self._infer_table_for_column(m_name)
            
            is_calc = (
                m.get("fieldType") == "calculatedField"
                or bool(m.get("formula"))
                or bool(m.get("calculationId"))
                or m_name in self.calc_lookup
            )

            if is_calc:
                y_list.append({
                    "table": m_table,
                    "measure": m_name
                })
            else:
                y_list.append({
                    "table": m_table,
                    "column": m.get("column") or m_name,
                    "aggregation": m.get("derivation") or "Sum"
                })

        if y_list:
            bindings["Y"] = y_list

        # 2. SortBy
        sort_by: Dict[str, Any] = {}
        if "Y" in bindings and bindings["Y"]:
            sort_by = {
                "target": bindings["Y"][0],
                "direction": "Descending"
            }
        elif "Category" in bindings:
            sort_by = {
                "target": bindings["Category"],
                "direction": "Ascending"
            }
        elif "X" in bindings:
            sort_by = {
                "target": bindings["X"],
                "direction": "Ascending"
            }

        # 3. Filters
        filters = []
        for flt in ws.get("filters", []):
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
