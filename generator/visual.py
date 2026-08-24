import re
from typing import Any, Dict, List, Optional, Set, Tuple


class VisualGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata) if isinstance(metadata, dict) else {}
        self.worksheets = self.metadata.get("worksheets", {})
        self.tables_meta = self.metadata.get("tables", {})
        self.measures_meta = self.metadata.get("measures", [])
        if isinstance(self.measures_meta, list):
            self.calc_lookup = {c.get("calculationId") or c.get("name"): c for c in self.measures_meta if isinstance(c, dict)}
        else:
            self.calc_lookup = {}

    def _find_table_for_column(self, col_name: str) -> str:
        """Dynamically identifies which table owns a column name."""
        if not col_name:
            return "Table"
        
        # Strip potential bracket/Tableau encodings
        clean_name = re.sub(r"[\[\]]", "", col_name).strip()

        if isinstance(self.tables_meta, dict):
            for tbl_name, cols in self.tables_meta.items():
                if isinstance(cols, list):
                    for c in cols:
                        if isinstance(c, dict) and c.get("name") == clean_name:
                            return tbl_name

        # Fallback to the first Fact or Dimension table available
        if isinstance(self.tables_meta, dict) and self.tables_meta:
            return next(iter(self.tables_meta.keys()))
        return "Fact_Table"

    def _map_visual_type(self, tableau_type: str) -> str:
        """Dynamically normalizes visual types into Power BI visual names."""
        if not tableau_type:
            return "barChart"
        t = str(tableau_type).lower()
        if any(k in t for k in ["text", "table", "grid"]):
            return "tableEx"
        elif any(k in t for k in ["line", "trend", "area"]):
            return "lineChart"
        elif any(k in t for k in ["pie", "donut"]):
            return "pieChart"
        elif any(k in t for k in ["card", "kpi", "metric"]):
            return "card"
        elif any(k in t for k in ["scatter", "bubble"]):
            return "scatterChart"
        return "barChart"

    def _extract_fields_dynamically(self, ws: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Dynamically partitions fields into dimensions and measures regardless of schema variance."""
        dimensions = ws.get("dimensions", [])
        measures = ws.get("measures", [])

        if not dimensions and not measures:
            # Parse from raw 'fields' or 'columns' shelf if present
            raw_fields = ws.get("fields", []) or ws.get("columns", [])
            for f in raw_fields:
                if not isinstance(f, dict):
                    continue
                role = str(f.get("role", "")).lower()
                dtype = str(f.get("dataType", "")).lower()

                if role == "dimension":
                    dimensions.append(f)
                elif role == "measure":
                    measures.append(f)
                else:
                    if dtype in ["real", "integer", "float", "double", "decimal", "numeric"]:
                        measures.append(f)
                    else:
                        dimensions.append(f)

        return dimensions, measures

    def _build_measure_target(self, m: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically generates measure reference bindings."""
        m_name = m.get("name") or m.get("column") or "Value"
        table_name = m.get("table") or self._find_table_for_column(m_name)
        
        is_calc = (
            m.get("fieldType") == "calculatedField" 
            or bool(m.get("formula")) 
            or bool(m.get("calculationId"))
            or m_name in self.calc_lookup
        )

        if is_calc:
            return {
                "table": table_name,
                "measure": m_name
            }
        else:
            return {
                "table": table_name,
                "column": m.get("column") or m_name,
                "aggregation": m.get("derivation") or "Sum"
            }

    def _build_dimension_target(self, d: Dict[str, Any]) -> Dict[str, Any]:
        """Dynamically generates dimension reference bindings."""
        d_name = d.get("name") or d.get("column") or "Category"
        table_name = d.get("table") or self._find_table_for_column(d_name)
        return {
            "table": table_name,
            "column": d.get("column") or d_name
        }

    def get_runtime_visual(self, sheet_name: str, layout_dict: Dict[str, Any], z_index: int = 1) -> Dict[str, Any]:
        """Generates dynamic runtime visual bindings, sorting, and properties."""
        ws = {}
        if isinstance(self.worksheets, dict):
            ws = self.worksheets.get(sheet_name, {})
        elif isinstance(self.worksheets, list):
            for item in self.worksheets:
                if isinstance(item, dict) and item.get("name") == sheet_name:
                    ws = item
                    break

        visual_type = self._map_visual_type(ws.get("visualType", "barChart"))
        title = ws.get("title") or sheet_name

        dimensions, measures = self._extract_fields_dynamically(ws)

        bindings: Dict[str, Any] = {}

        # 1. Dynamic Bindings Construction
        if visual_type == "lineChart":
            if dimensions:
                bindings["X"] = self._build_dimension_target(dimensions[0])
            if measures:
                bindings["Y"] = [self._build_measure_target(m) for m in measures]
        elif visual_type == "card":
            if measures:
                bindings["Y"] = [self._build_measure_target(m) for m in measures]
            elif dimensions:
                bindings["Y"] = [self._build_dimension_target(dimensions[0])]
        else:  # barChart, tableEx, pieChart, and other custom charts
            if dimensions:
                bindings["Category"] = self._build_dimension_target(dimensions[0])
            if measures:
                bindings["Y"] = [self._build_measure_target(m) for m in measures]

        # 2. Dynamic SortBy Construction
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

        # 3. Dynamic Filter Construction
        parsed_filters = []
        for flt in ws.get("filters", []):
            if isinstance(flt, dict):
                col = flt.get("name") or flt.get("column") or "Filter_Column"
                tbl = flt.get("table") or self._find_table_for_column(col)
                parsed_filters.append({
                    "table": tbl,
                    "column": col,
                    "operator": flt.get("operator", "In"),
                    "values": flt.get("values", [])
                })

        return {
            "visualType": visual_type,
            "title": title,
            "layout": {
                "x": layout_dict.get("x", 0),
                "y": layout_dict.get("y", 0),
                "width": layout_dict.get("width", 300),
                "height": layout_dict.get("height", 200),
                "z": z_index
            },
            "bindings": bindings,
            "sortBy": sort_by,
            "filters": parsed_filters,
            "properties": [
                {
                    "objectName": "values",
                    "propertyName": "labelDisplayUnits",
                    "value": 1000
                }
            ]
        }
