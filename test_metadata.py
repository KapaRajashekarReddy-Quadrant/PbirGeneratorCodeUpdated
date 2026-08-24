# test_metadata.py
import json
import unittest
from backend import process_report_request


class TestReportGeneration(unittest.TestCase):

    def test_visual_mapping_and_schema(self):
        sample_input = {
            "visuals": [
                {
                    "visualType": "text table",
                    "title": "Test Table",
                    "bindings": {
                        "Category": {"table": "Dim", "column": "col1"},
                        "Y": [{"table": "Fact", "column": "val", "aggregation": "Sum"}],
                    },
                }
            ]
        }
        res = process_report_request(sample_input)
        self.assertIn("visuals", res)
        self.assertEqual(res["visuals"][0]["visualType"], "tableEx")
        self.assertIn("pages", res)
        self.assertIn("dashboards", res)


if __name__ == "__main__":
    unittest.main()