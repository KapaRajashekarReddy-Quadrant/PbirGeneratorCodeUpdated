from typing import Dict, List, Any


class VisualGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata)
        self.worksheets = self.metadata.get("worksheets", [])

    def get_parsed_worksheets(self) -> Dict[str, Dict[str, Any]]:
        """Parses worksheets into visual definitions with shelves, roles, and encodings."""
        parsed_sheets = {}

        for ws in self.worksheets:
            sheet_name = ws.get("name")
            visual_type = ws.get("visualType", "Custom")

            title_info = ws.get("title", {})
            title = (
                title_info.get("displayText")
                or title_info.get("text")
                or sheet_name
            )

            dimensions = []
            measures = []

            for field in ws.get("fields", []):
                field_data = {
                    "name": field.get("name"),
                    "shelf": field.get("shelf"),
                    "dataType": field.get("dataType"),
                    "fieldType": field.get("fieldType"),
                    "table": field.get("table"),
                    "column": field.get("column"),
                    "formula": field.get("formula"),
                    "calculationId": field.get("calculationId")
                }
                if field.get("role") == "dimension":
                    dimensions.append(field_data)
                else:
                    measures.append(field_data)

            parsed_sheets[sheet_name] = {
                "name": sheet_name,
                "title": title,
                "visualType": visual_type,
                "dimensions": dimensions,
                "measures": measures,
                "encodings": ws.get("encodings", []),
                "filters": ws.get("filters", [])
            }

        return parsed_sheets
