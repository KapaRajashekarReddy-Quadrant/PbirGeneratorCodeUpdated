# generator/dataset.py
from typing import Any, Dict, List


class DatasetManager:
    """Handles dataset schema extraction, field validation, and metadata normalization."""

    @staticmethod
    def extract_tables_and_columns(visuals: List[Dict[str, Any]]) -> Dict[str, set]:
        schema = {}
        for visual in visuals:
            bindings = visual.get("bindings", {})
            for role, role_def in bindings.items():
                items = role_def if isinstance(role_def, list) else [role_def]
                for item in items:
                    tbl = item.get("table")
                    col = item.get("column") or item.get("measure")
                    if tbl and col:
                        if tbl not in schema:
                            schema[tbl] = set()
                        schema[tbl].add(col)
        return {k: list(v) for k, v in schema.items()}