# generator/visual.py
from typing import Any, Dict, List, Optional
from generator.utils import map_visual_type


class VisualBuilder:

    @classmethod
    def parse_field(cls, field_data: Dict[str, Any]) -> Dict[str, Any]:
        result = {"table": field_data.get("table", "")}
        if "measure" in field_data:
            result["measure"] = field_data["measure"]
        elif "column" in field_data:
            result["column"] = field_data["column"]

        if "aggregation" in field_data:
            result["aggregation"] = field_data["aggregation"]
        return result

    @classmethod
    def parse_bindings(cls, raw_bindings: Dict[str, Any]) -> Dict[str, Any]:
        parsed = {}
        for role_name, binding_value in raw_bindings.items():
            if isinstance(binding_value, list):
                parsed[role_name] = [
                    cls.parse_field(item) for item in binding_value
                ]
            elif isinstance(binding_value, dict):
                parsed[role_name] = cls.parse_field(binding_value)
        return parsed

    @classmethod
    def parse_sort_by(
        cls, raw_sort: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not raw_sort or "target" not in raw_sort:
            return None
        return {
            "target": cls.parse_field(raw_sort["target"]),
            "direction": raw_sort.get("direction", "Ascending"),
        }

    @classmethod
    def parse_filters(
        cls, raw_filters: Optional[List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        if not raw_filters:
            return []
        parsed = []
        for f in raw_filters:
            parsed.append(
                {
                    "table": f.get("table", ""),
                    "column": f.get("column", ""),
                    "operator": f.get("operator", "In"),
                    "values": f.get("values", []),
                }
            )
        return parsed

    @classmethod
    def parse_properties(
        cls, raw_props: Optional[List[Dict[str, Any]]]
    ) -> List[Dict[str, Any]]:
        if not raw_props:
            return []
        return [
            {
                "objectName": p.get("objectName", "values"),
                "propertyName": p.get("propertyName", ""),
                "value": p.get("value"),
            }
            for p in raw_props
        ]

    @classmethod
    def build(cls, raw_visual: Dict[str, Any]) -> Dict[str, Any]:
        mapped_type = map_visual_type(raw_visual.get("visualType"))
        layout = raw_visual.get("layout", {})

        visual_node = {
            "visualType": mapped_type,
            "title": raw_visual.get("title", ""),
            "layout": {
                "x": layout.get("x", 18),
                "y": layout.get("y", 18),
                "width": layout.get("width", 608),
                "height": layout.get("height", 200),
                "z": layout.get("z", 1),
            },
            "bindings": cls.parse_bindings(raw_visual.get("bindings", {})),
        }

        if "sortBy" in raw_visual and raw_visual["sortBy"]:
            visual_node["sortBy"] = cls.parse_sort_by(raw_visual["sortBy"])

        if "filters" in raw_visual and raw_visual["filters"]:
            visual_node["filters"] = cls.parse_filters(raw_visual["filters"])

        if "properties" in raw_visual and raw_visual["properties"]:
            visual_node["properties"] = cls.parse_properties(
                raw_visual["properties"]
            )

        return visual_node
