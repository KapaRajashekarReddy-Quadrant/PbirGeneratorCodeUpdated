from typing import Dict, List, Any


class DatasetGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        # Safeguard if raw payload was passed without unwrapping
        self.metadata = metadata.get("metadata", metadata)
        self.tables = self.metadata.get("tables", {})
        self.relationships = self.metadata.get("relationships", [])
        self.calculations = self.metadata.get("calculations", [])

    def get_table_schema(self) -> Dict[str, List[Dict[str, str]]]:
        """Extracts tables and their columns."""
        schema = {}
        for table_name, columns in self.tables.items():
            schema[table_name] = [
                {
                    "name": col.get("name"),
                    "dataType": col.get("dataType")
                }
                for col in columns
            ]
        return schema

    def get_relationships(self) -> List[Dict[str, str]]:
        """Maps relationships between Fact and Dimension tables."""
        relationships = []
        for rel in self.relationships:
            relationships.append({
                "fromTable": rel.get("fromTable"),
                "fromColumn": rel.get("fromColumn"),
                "toTable": rel.get("toTable"),
                "toColumn": rel.get("toColumn"),
                "relationshipType": rel.get("relationshipType", "Many-to-One")
            })
        return relationships

    def get_measures(self) -> List[Dict[str, Any]]:
        """Extracts calculation measures and formulas."""
        measures = []
        for calc in self.calculations:
            measures.append({
                "calculationId": calc.get("calculationId"),
                "name": calc.get("name"),
                "formula": calc.get("formula"),
                "dataType": calc.get("dataType"),
                "role": calc.get("role", "measure"),
                "defaultFormat": calc.get("defaultFormat")
            })
        return measures
