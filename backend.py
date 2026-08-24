# backend.py
from typing import Any, Dict
from generator.report import ReportGenerator


def process_report_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Backend service entrypoint for executing transformations."""
    generator = ReportGenerator(payload)
    return generator.generate()