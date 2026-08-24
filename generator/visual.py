from typing import Dict, List, Any


class VisualGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata) if isinstance(metadata, dict) else {}
        self.worksheets = self.metadata.get("worksheets", [])

    def get_parsed_worksheets(self) -> Dict[str, Dict[str, Any]]:
        """Parses any worksheet schema dynamically."""
        parsed_sheets = {}

        if not isinstance(self.worksheets, list):
            return parsed_sheets

        for ws in self.worksheets:
            if not isinstance(ws, dict):
                continue

            sheet_name = ws.get("name", "Worksheet")
            visual_type = ws.get("visualType") or ws.get("type", "Custom")

            title_info = ws.get("title", {})
            if isinstance(title_info, dict):
                title = (
                    title_info.get("displayText")
                    or title_info.get("text")
                    or sheet_name
                )
            elif isinstance(title_info, str):
                title = title_info
            else:
                title = sheet_name

            dimensions = []
            measures = []

            for field in ws.get("fields", []):
                if not isinstance(field, dict):
                    continue

                field_data = {
                    "name": field.get("name") or field.get("column"),
                    "shelf": field.get("shelf", "Marks"),
                    "dataType": field.get("dataType", "string"),
                    "fieldType": field.get("fieldType"),
                    "table": field.get("table"),
                    "column": field.get("column"),
                    "formula": field.get("formula"),
                    "calculationId": field.get("calculationId")
                }

                role = field.get("role", "").lower()
                if role == "dimension":
                    dimensions.append(field_data)
                elif role == "measure":
                    measures.append(field_data)
                else:
                    # Fallback inference if role is missing
                    if field.get("dataType") in ["integer", "real", "float", "double"] and not field.get("name", "").endswith("_id"):
                        measures.append(field_data)
                    else:
                        dimensions.append(field_data)

            parsed_sheets[sheet_name] = {
                "name": sheet_name,
                "title": title,
                "visualType": visual_type,
                "dimensions": dimensions,
                "measures": measures,
                "encodings": ws.get("encodings", []),
                "filters": ws.get("filters", []),
                "columnsShelf": ws.get("columnsShelf", []),
                "rows": ws.get("rows", [])
            }

        return parsed_sheets
