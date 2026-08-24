from typing import Dict, List, Any


class DatasetGenerator:
    def __init__(self, metadata: Dict[str, Any]):
        self.metadata = metadata.get("metadata", metadata) if isinstance(metadata, dict) else {}
        self.tables = self.metadata.get("tables", {})
        self.relationships = self.metadata.get("relationships", [])
        self.calculations = self.metadata.get("calculations", [])

    def get_table_schema(self) -> Dict[str, List[Dict[str, Any]]]:
        """Dynamically builds schemas for all tables found in the JSON."""
        schema = {}
        if isinstance(self.tables, dict):
            for table_name, columns in self.tables.items():
                if isinstance(columns, list):
                    schema[table_name] = [
                        {
                            "name": col.get("name", ""),
                            "dataType": col.get("dataType", "string")
                        }
                        for col in columns if isinstance(col, dict)
                    ]
        elif isinstance(self.tables, list):
            # Fallback if tables are formatted as a list of objects
            for tbl in self.tables:
                if isinstance(tbl, dict):
                    t_name = tbl.get("name", "UnknownTable")
                    schema[t_name] = tbl.get("columns", [])
        return schema

    def get_relationships(self) -> List[Dict[str, Any]]:
        """Extracts dynamic relationships and foreign keys."""
        relationships = []
        for rel in self.relationships:
            if isinstance(rel, dict):
                relationships.append({
                    "fromTable": rel.get("fromTable") or rel.get("from_table"),
                    "fromColumn": rel.get("fromColumn") or rel.get("from_column"),
                    "toTable": rel.get("toTable") or rel.get("to_table"),
                    "toColumn": rel.get("toColumn") or rel.get("to_column"),
                    "relationshipType": rel.get("relationshipType") or rel.get("relationship_type", "Many-to-One")
                })
        return relationships

    def get_measures(self) -> List[Dict[str, Any]]:
        """Extracts calculations and measures regardless of key casing."""
        measures = []
        for calc in self.calculations:
            if isinstance(calc, dict):
                measures.append({
                    "calculationId": calc.get("calculationId") or calc.get("id"),
                    "name": calc.get("name", "Unnamed_Measure"),
                    "formula": calc.get("formula", ""),
                    "dataType": calc.get("dataType", "real"),
                    "role": calc.get("role", "measure"),
                    "defaultFormat": calc.get("defaultFormat") or calc.get("format")
                })
        return measures
