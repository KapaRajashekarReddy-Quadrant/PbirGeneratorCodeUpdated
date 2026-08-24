# main.py
import json
import os
from backend import process_report_request
from blob_reader import write_json_payload

OUTPUT_FILE_PATH = os.getenv(
    "OUTPUT_FILE_PATH", os.path.join("output", "runtime_visuals.json")
)

# Exact input specification provided
SAMPLE_INPUT = {
    "visuals": [
        {
            "visualType": "tableEx",
            "title": "Top 5 Machines by Downtime",
            "layout": {
                "x": 18,
                "y": 99,
                "width": 608,
                "height": 225,
                "z": 1,
            },
            "bindings": {
                "Category": {
                    "table": "Dim_Machine",
                    "column": "machine_name",
                },
                "Y": [
                    {
                        "table": "Fact_Production",
                        "column": "downtime_minutes",
                        "aggregation": "Sum",
                    }
                ],
            },
            "sortBy": {
                "target": {
                    "table": "Fact_Production",
                    "column": "downtime_minutes",
                    "aggregation": "Sum",
                },
                "direction": "Descending",
            },
            "filters": [
                {
                    "table": "Dim_Machine",
                    "column": "machine_type",
                    "operator": "In",
                    "values": ["CNC Lathe", "CNC Mill"],
                }
            ],
            "properties": [
                {
                    "objectName": "values",
                    "propertyName": "labelDisplayUnits",
                    "value": 1000,
                }
            ],
        },
        {
            "visualType": "lineChart",
            "title": "OEE Trend",
            "layout": {
                "x": 18,
                "y": 340,
                "width": 608,
                "height": 200,
                "z": 2,
            },
            "bindings": {
                "X": {
                    "table": "Fact_Production",
                    "column": "shift_date",
                },
                "Y": [{"table": "Fact_Production", "measure": "OEE"}],
            },
            "sortBy": {
                "target": {
                    "table": "Fact_Production",
                    "column": "shift_date",
                },
                "direction": "Ascending",
            },
        },
    ],
    "pages": [
        {
            "name": "Production Overview",
            "size": {"width": 646, "height": 560},
            "visuals": [
                {
                    "visualType": "tableEx",
                    "title": "Top 5 Machines by Downtime",
                    "layout": {
                        "x": 18,
                        "y": 99,
                        "width": 608,
                        "height": 225,
                        "z": 1,
                    },
                    "bindings": {
                        "Category": {
                            "table": "Dim_Machine",
                            "column": "machine_name",
                        },
                        "Y": [
                            {
                                "table": "Fact_Production",
                                "column": "downtime_minutes",
                                "aggregation": "Count",
                            }
                        ],
                    },
                    "sortBy": {
                        "target": {
                            "table": "Fact_Production",
                            "column": "downtime_minutes",
                            "aggregation": "Count",
                        },
                        "direction": "Descending",
                    },
                    "filters": [
                        {
                            "table": "Dim_Machine",
                            "column": "machine_type",
                            "operator": "In",
                            "values": ["CNC Lathe", "CNC Mill"],
                        }
                    ],
                    "properties": [
                        {
                            "objectName": "values",
                            "propertyName": "labelDisplayUnits",
                            "value": 1000,
                        }
                    ],
                },
                {
                    "visualType": "lineChart",
                    "title": "OEE Trend",
                    "layout": {
                        "x": 18,
                        "y": 340,
                        "width": 608,
                        "height": 200,
                        "z": 2,
                    },
                    "bindings": {
                        "X": {
                            "table": "Fact_Production",
                            "column": "shift_date",
                        },
                        "Y": [{"table": "Fact_Production", "measure": "OEE"}],
                    },
                    "sortBy": {
                        "target": {
                            "table": "Fact_Production",
                            "column": "shift_date",
                        },
                        "direction": "Ascending",
                    },
                },
            ],
        }
    ],
    "dashboards": [
        {"name": "Production Overview", "width": 644, "height": 560}
    ],
}

if __name__ == "__main__":
    result = process_report_request(SAMPLE_INPUT)
    write_json_payload(OUTPUT_FILE_PATH, result)
    print(json.dumps(result, indent=2))