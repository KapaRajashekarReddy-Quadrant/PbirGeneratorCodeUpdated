# # # # generator/utils.py
# # # from typing import Optional

# # # VISUAL_TYPE_MAPPINGS = {
# # #     "Bar Chart": "clusteredBarChart",
# # #     "horizontal bar": "clusteredBarChart",
# # #     "stacked bar": "barChart",
# # #     "100% stacked bar": "hundredPercentStackedBarChart",
# # #     "standard column": "clusteredColumnChart",
# # #     "vertical column": "clusteredColumnChart",
# # #     "stacked column": "columnChart",
# # #     "100% stacked column": "hundredPercentStackedColumnChart",
# # #     "pie chart": "pieChart",
# # #     "donut chart": "donutChart",
# # #     "semi-circle chart": "gauge",
# # #     "half donut chart": "gauge",
# # #     "nested donut chart": "donutChart",
# # #     "treemap": "treemap",
# # #     "sunburst chart": "treemap",
# # #     "marimekko chart": "hundredPercentStackedColumnChart",
# # #     "mosaic chart": "hundredPercentStackedColumnChart",
# # #     "waffle chart": "clusteredColumnChart",
# # #     "dot matrix chart": "clusteredColumnChart",
# # #     "pictogram chart": "clusteredColumnChart",
# # #     "isotype chart": "clusteredColumnChart",
# # #     "unit chart": "clusteredColumnChart",
# # #     "radial bar chart": "donutChart",
# # #     "concentric rings chart": "donutChart",
# # #     "polar area chart": "clusteredColumnChart",
# # #     "coxcomb chart": "clusteredColumnChart",
# # #     "rose chart": "clusteredColumnChart",
# # #     "wind rose chart": "clusteredColumnChart",
# # #     "lollipop chart": "lineClusteredColumnComboChart",
# # #     "dumbbell chart": "clusteredBarChart",
# # #     "dna chart": "clusteredBarChart",
# # #     "tornado chart": "clusteredBarChart",
# # #     "population pyramid": "clusteredBarChart",
# # #     "diverging stacked bar": "hundredPercentStackedBarChart",
# # #     "likert scale chart": "hundredPercentStackedBarChart",
# # #     "bar-in-bar chart": "clusteredBarChart",
# # #     "bullet graph": "gauge",
# # #     "floating bar chart": "clusteredBarChart",
# # #     "range bar chart": "clusteredBarChart",
# # #     "gantt chart": "clusteredBarChart",
# # #     "waterfall chart": "waterfallChart",
# # #     "stepped waterfall chart": "waterfallChart",
# # #     "bridge chart": "waterfallChart",
# # #     "funnel chart": "funnel",
# # #     "pipeline funnel": "funnel",
# # #     "pyramid chart": "funnel",
# # #     "continuous line": "lineChart",
# # #     "discrete line": "lineChart",
# # #     "multi-line chart": "lineChart",
# # #     "dual axis line": "lineChart",
# # #     "dual axis combo chart": "lineClusteredColumnComboChart",
# # #     "line and clustered column": "lineClusteredColumnComboChart",
# # #     "line and stacked column": "lineStackedColumnComboChart",
# # #     "step line": "lineChart",
# # #     "jump line": "lineChart",
# # #     "sparkline standalone": "lineChart",
# # #     "sparklines in table": "pivotTable",
# # #     "area chart": "areaChart",
# # #     "stacked area": "stackedAreaChart",
# # #     "100% stacked area": "stackedAreaChart",
# # #     "streamgraph": "stackedAreaChart",
# # #     "horizon chart": "areaChart",
# # #     "slope chart": "lineChart",
# # #     "bump chart": "lineChart",
# # #     "ranking over time": "lineChart",
# # #     "cycle plot": "lineChart",
# # #     "seasonal trend chart": "lineChart",
# # #     "ribbon chart": "ribbonChart",
# # #     "connected scatter plot": "lineChart",
# # #     "parallel coordinates plot": "lineChart",
# # #     "sankey diagram": "ribbonChart",
# # #     "chord diagram": "ribbonChart",
# # #     "alluvial diagram": "ribbonChart",
# # #     "network relationship graph": "scatterChart",
# # #     "tree diagram": "Decomposition Tree",
# # #     "org chart": "Decomposition Tree",
# # #     "decision flow diagram": "Decomposition Tree",
# # #     "scatter plot": "scatterChart",
# # #     "bubble chart": "scatterChart",
# # #     "packed bubbles": "scatterChart",
# # #     "circle view": "scatterChart",
# # #     "strip plot": "scatterChart",
# # #     "jitter plot": "scatterChart",
# # #     "dot plot": "scatterChart",
# # #     "histogram": "clusteredColumnChart",
# # #     "binned frequency distribution": "clusteredColumnChart",
# # #     "box and whisker plot": "scatterChart",
# # #     "violin plot": "scatterChart",
# # #     "ridgeline plot": "areaChart",
# # #     "joyplot": "areaChart",
# # #     "density contour plot": "scatterChart",
# # #     "ternary plot": "scatterChart",
# # #     "quadrant plot": "scatterChart",
# # #     "2x2 matrix plot": "scatterChart",
# # #     "pareto chart": "lineClusteredColumnComboChart",
# # #     "80-20 chart": "lineClusteredColumnComboChart",
# # #     "radar chart": "lineChart",
# # #     "spider chart": "lineChart",
# # #     "web chart": "lineChart",
# # #     "candlestick chart": "waterfallChart",
# # #     "ohlc chart": "waterfallChart",
# # #     "kagi chart": "waterfallChart",
# # #     "renko chart": "clusteredColumnChart",
# # #     "point and figure chart": "pivotTable",
# # #     "symbol map": "map",
# # #     "bubble map": "map",
# # #     "proportional symbol map": "map",
# # #     "dot density map": "map",
# # #     "choropleth map": "filledMap",
# # #     "filled map": "filledMap",
# # #     "shape map": "shapeMap",
# # #     "custom topojson map": "shapeMap",
# # #     "azure maps visual": None,
# # #     "spatial polygon map": "filledMap",
# # #     "isochrone map": None,
# # #     "travel-time map": None,
# # #     "flow map": "ribbonChart",
# # #     "origin-destination map": "ribbonChart",
# # #     "heat map layer": "filledMap",
# # #     "density map": "filledMap",
# # #     "hexbin map": "filledMap",
# # #     "cartogram map": "filledMap",
# # #     "tile grid map": "pivotTable",
# # #     "text table": "tableEx",
# # #     "crosstab": "pivotTable",
# # #     "matrix": "pivotTable",
# # #     "highlight table": "pivotTable",
# # #     "matrix with micro-charts": "pivotTable",
# # #     "heat map table": "pivotTable",
# # #     "calendar heatmap": "pivotTable",
# # #     "single value KPI card": "card",
# # #     "multi-row KPI card": "multiRowCard",
# # #     "new card visual": "card",
# # #     "multi-metric card": "card",
# # #     "kpi indicator with trend line": "kpi",
# # #     "linear gauge": "gauge",
# # #     "radial gauge": "gauge",
# # #     "speedometer": "gauge",
# # #     "donut progress gauge": "donutChart",
# # #     "kpi band chart": "kpi",
# # #     "filter control": "slicer",
# # #     "dropdown parameter": "slicer",
# # #     "range slider": "slicer",
# # #     "tile selector": "slicer",
# # #     "hierarchy slicer": "slicer",
# # #     "decomposition tree": "Decomposition Tree",
# # #     "key influencers": "keyDriversVisual",
# # #     "key drivers": "keyDriversVisual",
# # #     "anomaly detection": "lineChart",
# # #     "smart narrative": None,
# # #     "automated summary": None,
# # #     "q&a natural language box": "qnaVisual",
# # #     "word cloud": "treemap",
# # # }


# # # def map_visual_type(raw_type: Optional[str]) -> str:
# # #     """Normalizes input visual types using the dictionary mapping."""
# # #     if not raw_type:
# # #         return "tableEx"
# # #     lookup = str(raw_type).strip().lower()
# # #     return VISUAL_TYPE_MAPPINGS.get(lookup) or raw_type


# # # generator/utils.py
# # from typing import Optional

# # VISUAL_TYPE_MAPPINGS = {
# #     # Bars & Columns
# #     "bar chart": "clusteredBarChart",
# #     "bar": "clusteredBarChart",
# #     "horizontal bar": "clusteredBarChart",
# #     "stacked bar": "barChart",
# #     "100% stacked bar": "hundredPercentStackedBarChart",
# #     "standard column": "clusteredColumnChart",
# #     "column": "clusteredColumnChart",
# #     "column chart": "clusteredColumnChart",
# #     "vertical column": "clusteredColumnChart",
# #     "stacked column": "columnChart",
# #     "100% stacked column": "hundredPercentStackedColumnChart",
# #     "bar-in-bar chart": "clusteredBarChart",
# #     "floating bar chart": "clusteredBarChart",
# #     "range bar chart": "clusteredBarChart",
# #     "gantt chart": "clusteredBarChart",
# #     "dumbbell chart": "clusteredBarChart",
# #     "dna chart": "clusteredBarChart",
# #     "tornado chart": "clusteredBarChart",
# #     "population pyramid": "clusteredBarChart",
# #     "diverging stacked bar": "hundredPercentStackedBarChart",
# #     "likert scale chart": "hundredPercentStackedBarChart",

# #     # Pies & Circles
# #     "pie": "pieChart",
# #     "pie chart": "pieChart",
# #     "donut chart": "donutChart",
# #     "donut": "donutChart",
# #     "nested donut chart": "donutChart",
# #     "donut progress gauge": "donutChart",
# #     "radial bar chart": "donutChart",
# #     "concentric rings chart": "donutChart",
# #     "semi-circle chart": "gauge",
# #     "half donut chart": "gauge",

# #     # Lines & Areas
# #     "line": "lineChart",
# #     "line chart": "lineChart",
# #     "continuous line": "lineChart",
# #     "discrete line": "lineChart",
# #     "multi-line chart": "lineChart",
# #     "dual axis line": "lineChart",
# #     "step line": "lineChart",
# #     "jump line": "lineChart",
# #     "sparkline standalone": "lineChart",
# #     "slope chart": "lineChart",
# #     "bump chart": "lineChart",
# #     "ranking over time": "lineChart",
# #     "cycle plot": "lineChart",
# #     "seasonal trend chart": "lineChart",
# #     "connected scatter plot": "lineChart",
# #     "parallel coordinates plot": "lineChart",
# #     "radar chart": "lineChart",
# #     "spider chart": "lineChart",
# #     "web chart": "lineChart",
# #     "anomaly detection": "lineChart",
# #     "area chart": "areaChart",
# #     "area": "areaChart",
# #     "stacked area": "stackedAreaChart",
# #     "100% stacked area": "stackedAreaChart",
# #     "streamgraph": "stackedAreaChart",
# #     "horizon chart": "areaChart",
# #     "ridgeline plot": "areaChart",
# #     "joyplot": "areaChart",

# #     # Combos & Special
# #     "dual axis combo chart": "lineClusteredColumnComboChart",
# #     "line and clustered column": "lineClusteredColumnComboChart",
# #     "line and stacked column": "lineStackedColumnComboChart",
# #     "lollipop chart": "lineClusteredColumnComboChart",
# #     "pareto chart": "lineClusteredColumnComboChart",
# #     "80-20 chart": "lineClusteredColumnComboChart",
# #     "treemap": "treemap",
# #     "sunburst chart": "treemap",
# #     "word cloud": "treemap",
# #     "waterfall chart": "waterfallChart",
# #     "waterfall": "waterfallChart",
# #     "stepped waterfall chart": "waterfallChart",
# #     "bridge chart": "waterfallChart",
# #     "candlestick chart": "waterfallChart",
# #     "ohlc chart": "waterfallChart",
# #     "kagi chart": "waterfallChart",
# #     "funnel chart": "funnel",
# #     "funnel": "funnel",
# #     "pipeline funnel": "funnel",
# #     "pyramid chart": "funnel",
# #     "ribbon chart": "ribbonChart",
# #     "sankey diagram": "ribbonChart",
# #     "chord diagram": "ribbonChart",
# #     "alluvial diagram": "ribbonChart",
# #     "flow map": "ribbonChart",
# #     "origin-destination map": "ribbonChart",

# #     # Scatter & Distributions
# #     "scatter plot": "scatterChart",
# #     "scatter": "scatterChart",
# #     "bubble chart": "scatterChart",
# #     "packed bubbles": "scatterChart",
# #     "circle view": "scatterChart",
# #     "strip plot": "scatterChart",
# #     "jitter plot": "scatterChart",
# #     "dot plot": "scatterChart",
# #     "box and whisker plot": "scatterChart",
# #     "violin plot": "scatterChart",
# #     "density contour plot": "scatterChart",
# #     "ternary plot": "scatterChart",
# #     "quadrant plot": "scatterChart",
# #     "2x2 matrix plot": "scatterChart",
# #     "network relationship graph": "scatterChart",
# #     "histogram": "clusteredColumnChart",
# #     "binned frequency distribution": "clusteredColumnChart",
# #     "renko chart": "clusteredColumnChart",
# #     "waffle chart": "clusteredColumnChart",
# #     "dot matrix chart": "clusteredColumnChart",
# #     "pictogram chart": "clusteredColumnChart",
# #     "isotype chart": "clusteredColumnChart",
# #     "unit chart": "clusteredColumnChart",
# #     "polar area chart": "clusteredColumnChart",
# #     "coxcomb chart": "clusteredColumnChart",
# #     "rose chart": "clusteredColumnChart",
# #     "wind rose chart": "clusteredColumnChart",

# #     # Maps
# #     "symbol map": "map",
# #     "bubble map": "map",
# #     "proportional symbol map": "map",
# #     "dot density map": "map",
# #     "choropleth map": "filledMap",
# #     "filled map": "filledMap",
# #     "spatial polygon map": "filledMap",
# #     "heat map layer": "filledMap",
# #     "density map": "filledMap",
# #     "hexbin map": "filledMap",
# #     "cartogram map": "filledMap",
# #     "shape map": "shapeMap",
# #     "custom topojson map": "shapeMap",

# #     # Tables & Matrix
# #     "text table": "tableEx",
# #     "table": "tableEx",
# #     "tableex": "tableEx",
# #     "crosstab": "pivotTable",
# #     "matrix": "pivotTable",
# #     "pivottable": "pivotTable",
# #     "highlight table": "pivotTable",
# #     "matrix with micro-charts": "pivotTable",
# #     "heat map table": "pivotTable",
# #     "calendar heatmap": "pivotTable",
# #     "sparklines in table": "pivotTable",
# #     "point and figure chart": "pivotTable",
# #     "tile grid map": "pivotTable",

# #     # Cards & Gauges
# #     "card": "card",
# #     "single value kpi card": "card",
# #     "new card visual": "card",
# #     "multi-metric card": "card",
# #     "multi-row kpi card": "multiRowCard",
# #     "multirowcard": "multiRowCard",
# #     "kpi indicator with trend line": "kpi",
# #     "kpi band chart": "kpi",
# #     "kpi": "kpi",
# #     "gauge": "gauge",
# #     "linear gauge": "gauge",
# #     "radial gauge": "gauge",
# #     "speedometer": "gauge",
# #     "bullet graph": "gauge",

# #     # Advanced / AI
# #     "filter control": "slicer",
# #     "dropdown parameter": "slicer",
# #     "range slider": "slicer",
# #     "tile selector": "slicer",
# #     "hierarchy slicer": "slicer",
# #     "slicer": "slicer",
# #     "tree diagram": "Decomposition Tree",
# #     "org chart": "Decomposition Tree",
# #     "decision flow diagram": "Decomposition Tree",
# #     "decomposition tree": "Decomposition Tree",
# #     "key influencers": "keyDriversVisual",
# #     "key drivers": "keyDriversVisual",
# #     "q&a natural language box": "qnaVisual",
# # }


# # def map_visual_type(raw_type: Optional[str]) -> str:
# #     """
# #     Normalizes input visual types using a single centralized lookup.
# #     Matches once and immediately returns. If no match is found, defaults to 'tableEx'.
# #     """
# #     if not raw_type:
# #         return "tableEx"

# #     cleaned = str(raw_type).strip().lower()

# #     # 1. Exact match from dictionary
# #     if cleaned in VISUAL_TYPE_MAPPINGS:
# #         matched = VISUAL_TYPE_MAPPINGS[cleaned]
# #         return matched if matched else "tableEx"

# #     # 2. Single-pass keyword heuristics (skip further checks on first match)
# #     if "pie" in cleaned:
# #         return "pieChart"
# #     if "donut" in cleaned:
# #         return "donutChart"
# #     if "bar" in cleaned:
# #         return "clusteredBarChart"
# #     if "column" in cleaned:
# #         return "clusteredColumnChart"
# #     if "line" in cleaned:
# #         return "lineChart"
# #     if "card" in cleaned or "kpi" in cleaned:
# #         return "card"
# #     if "scatter" in cleaned:
# #         return "scatterChart"
# #     if "area" in cleaned:
# #         return "areaChart"
# #     if "tree" in cleaned:
# #         return "treemap"
# #     if "map" in cleaned:
# #         return "map"

# #     # 3. Default fallback if not mapped
# #     return "tableEx"

# from typing import Optional
 
# VISUAL_TYPE_MAPPINGS = {
#     # Bars & Columns
#     "bar chart": "clusteredBarChart",
#     "bar": "clusteredBarChart",
#     "horizontal bar": "clusteredBarChart",
#     "stacked bar": "barChart",
#     "100% stacked bar": "hundredPercentStackedBarChart",
#     "standard column": "clusteredColumnChart",
#     "column": "clusteredColumnChart",
#     "column chart": "clusteredColumnChart",
#     "vertical column": "clusteredColumnChart",
#     "stacked column": "columnChart",
#     "100% stacked column": "hundredPercentStackedColumnChart",
#     "bar-in-bar chart": "clusteredBarChart",
#     "floating bar chart": "clusteredBarChart",
#     "range bar chart": "clusteredBarChart",
#     "gantt chart": "clusteredBarChart",
#     "dumbbell chart": "clusteredBarChart",
#     "dna chart": "clusteredBarChart",
#     "tornado chart": "clusteredBarChart",
#     "population pyramid": "clusteredBarChart",
#     "diverging stacked bar": "hundredPercentStackedBarChart",
#     "likert scale chart": "hundredPercentStackedBarChart",
 
#     # Pies & Circles
#     "pie": "pieChart",
#     "pie chart": "pieChart",
#     "donut chart": "donutChart",
#     "donut": "donutChart",
#     "nested donut chart": "donutChart",
#     "donut progress gauge": "donutChart",
#     "radial bar chart": "donutChart",
#     "concentric rings chart": "donutChart",
#     "semi-circle chart": "gauge",
#     "half donut chart": "gauge",
 
#     # Lines & Areas
#     "line": "lineChart",
#     "line chart": "lineChart",
#     "continuous line": "lineChart",
#     "discrete line": "lineChart",
#     "multi-line chart": "lineChart",
#     "dual axis line": "lineChart",
#     "step line": "lineChart",
#     "jump line": "lineChart",
#     "sparkline standalone": "lineChart",
#     "slope chart": "lineChart",
#     "bump chart": "lineChart",
#     "ranking over time": "lineChart",
#     "cycle plot": "lineChart",
#     "seasonal trend chart": "lineChart",
#     "connected scatter plot": "lineChart",
#     "parallel coordinates plot": "lineChart",
#     "radar chart": "lineChart",
#     "spider chart": "lineChart",
#     "web chart": "lineChart",
#     "anomaly detection": "lineChart",
#     "area chart": "areaChart",
#     "area": "areaChart",
#     "stacked area": "stackedAreaChart",
#     "100% stacked area": "stackedAreaChart",
#     "streamgraph": "stackedAreaChart",
#     "horizon chart": "areaChart",
#     "ridgeline plot": "areaChart",
#     "joyplot": "areaChart",
 
#     # Combos & Special
#     "dual axis combo chart": "lineClusteredColumnComboChart",
#     "line and clustered column": "lineClusteredColumnComboChart",
#     "line and stacked column": "lineStackedColumnComboChart",
#     "lollipop chart": "lineClusteredColumnComboChart",
#     "pareto chart": "lineClusteredColumnComboChart",
#     "80-20 chart": "lineClusteredColumnComboChart",
#     "treemap": "treemap",
#     "sunburst chart": "treemap",
#     "word cloud": "treemap",
#     "waterfall chart": "waterfallChart",
#     "waterfall": "waterfallChart",
#     "stepped waterfall chart": "waterfallChart",
#     "bridge chart": "waterfallChart",
#     "candlestick chart": "waterfallChart",
#     "ohlc chart": "waterfallChart",
#     "kagi chart": "waterfallChart",
#     "funnel chart": "funnel",
#     "funnel": "funnel",
#     "pipeline funnel": "funnel",
#     "pyramid chart": "funnel",
#     "ribbon chart": "ribbonChart",
#     "sankey diagram": "ribbonChart",
#     "chord diagram": "ribbonChart",
#     "alluvial diagram": "ribbonChart",
#     "flow map": "ribbonChart",
#     "origin-destination map": "ribbonChart",
 
#     # Scatter & Distributions
#     "scatter plot": "scatterChart",
#     "scatter": "scatterChart",
#     "bubble chart": "scatterChart",
#     "packed bubbles": "scatterChart",
#     "circle view": "scatterChart",
#     "strip plot": "scatterChart",
#     "jitter plot": "scatterChart",
#     "dot plot": "scatterChart",
#     "box and whisker plot": "scatterChart",
#     "violin plot": "scatterChart",
#     "density contour plot": "scatterChart",
#     "ternary plot": "scatterChart",
#     "quadrant plot": "scatterChart",
#     "2x2 matrix plot": "scatterChart",
#     "network relationship graph": "scatterChart",
#     "histogram": "clusteredColumnChart",
#     "binned frequency distribution": "clusteredColumnChart",
#     "renko chart": "clusteredColumnChart",
#     "waffle chart": "clusteredColumnChart",
#     "dot matrix chart": "clusteredColumnChart",
#     "pictogram chart": "clusteredColumnChart",
#     "isotype chart": "clusteredColumnChart",
#     "unit chart": "clusteredColumnChart",
#     "polar area chart": "clusteredColumnChart",
#     "coxcomb chart": "clusteredColumnChart",
#     "rose chart": "clusteredColumnChart",
#     "wind rose chart": "clusteredColumnChart",
 
#     # Maps
#     "symbol map": "map",
#     "bubble map": "map",
#     "proportional symbol map": "map",
#     "dot density map": "map",
#     "choropleth map": "filledMap",
#     "filled map": "filledMap",
#     "spatial polygon map": "filledMap",
#     "heat map layer": "filledMap",
#     "density map": "filledMap",
#     "hexbin map": "filledMap",
#     "cartogram map": "filledMap",
#     "shape map": "shapeMap",
#     "custom topojson map": "shapeMap",
 
#     # Tables & Matrix
#     "text table": "tableEx",
#     "table": "tableEx",
#     "tableex": "tableEx",
#     "crosstab": "pivotTable",
#     "matrix": "pivotTable",
#     "pivottable": "pivotTable",
#     "highlight table": "pivotTable",
#     "matrix with micro-charts": "pivotTable",
#     "heat map table": "pivotTable",
#     "calendar heatmap": "pivotTable",
#     "sparklines in table": "pivotTable",
#     "point and figure chart": "pivotTable",
#     "tile grid map": "pivotTable",
 
#     # Cards & Gauges
#     "card": "card",
#     "single value kpi card": "card",
#     "new card visual": "card",
#     "multi-metric card": "card",
#     "multi-row kpi card": "multiRowCard",
#     "multirowcard": "multiRowCard",
#     "kpi indicator with trend line": "kpi",
#     "kpi band chart": "kpi",
#     "kpi": "kpi",
#     "gauge": "gauge",
#     "linear gauge": "gauge",
#     "radial gauge": "gauge",
#     "speedometer": "gauge",
#     "bullet graph": "gauge",
 
#     # Advanced / AI
#     "filter control": "slicer",
#     "dropdown parameter": "slicer",
#     "range slider": "slicer",
#     "tile selector": "slicer",
#     "hierarchy slicer": "slicer",
#     "slicer": "slicer",
#     "tree diagram": "Decomposition Tree",
#     "org chart": "Decomposition Tree",
#     "decision flow diagram": "Decomposition Tree",
#     "decomposition tree": "Decomposition Tree",
#     "key influencers": "keyDriversVisual",
#     "key drivers": "keyDriversVisual",
#     "q&a natural language box": "qnaVisual",
# }
 
 
# # Ordered fallback keyword rules, most specific first. The very first rule
# # whose keyword appears in the cleaned string wins and the search stops
# # immediately (single match -> break), so one Tableau visual can never be
# # expanded into more than one Power BI visual type.
# _KEYWORD_FALLBACKS = [
#     ("donut", "donutChart"),
#     ("pie", "pieChart"),
#     ("waterfall", "waterfallChart"),
#     ("funnel", "funnel"),
#     ("gauge", "gauge"),
#     ("ribbon", "ribbonChart"),
#     ("sankey", "ribbonChart"),
#     ("treemap", "treemap"),
#     ("tree", "treemap"),
#     ("decomposition", "Decomposition Tree"),
#     ("scatter", "scatterChart"),
#     ("bubble", "scatterChart"),
#     ("stacked bar", "hundredPercentStackedBarChart"),
#     ("bar", "clusteredBarChart"),
#     ("stacked column", "columnChart"),
#     ("column", "clusteredColumnChart"),
#     ("area", "areaChart"),
#     ("line", "lineChart"),
#     ("card", "card"),
#     ("kpi", "kpi"),
#     ("matrix", "pivotTable"),
#     ("pivot", "pivotTable"),
#     ("crosstab", "pivotTable"),
#     ("slicer", "slicer"),
#     ("filter", "slicer"),
#     ("map", "map"),
#     ("table", "tableEx"),
# ]
 
 
# def map_visual_type(raw_type: Optional[str]) -> str:
#     """
#     Normalizes any incoming (Tableau) visual type string into exactly ONE
#     Power BI visual type string.
 
#     Resolution order (stops at the very first match, guaranteeing a single
#     visual is ever produced for a given raw type):
#       1. Exact match against VISUAL_TYPE_MAPPINGS.
#       2. First matching keyword from an ordered fallback list.
#       3. 'tableEx' if nothing matches at all.
#     """
#     if not raw_type:
#         return "tableEx"
 
#     cleaned = str(raw_type).strip().lower()
#     if not cleaned:
#         return "tableEx"
 
#     # 1. Exact match from dictionary - resolved once, no further lookups.
#     if cleaned in VISUAL_TYPE_MAPPINGS:
#         matched = VISUAL_TYPE_MAPPINGS[cleaned]
#         return matched if matched else "tableEx"
 
#     # 2. Ordered keyword scan - break out of the loop on the first hit so a
#     #    string like "stacked bar chart" can't also satisfy a later, more
#     #    generic rule and produce ambiguous/duplicate mappings.
#     for keyword, mapped in _KEYWORD_FALLBACKS:
#         if keyword in cleaned:
#             return mapped
 
#     # 3. Nothing matched anywhere in the list -> safe default.
#     return "tableEx"
 import re
from typing import Optional

VISUAL_TYPE_MAPPINGS = {
    # -------------------------------------------------------------
    # Tableau Unspaced / Metadata Raw Tokens & Typo Handlers
    # -------------------------------------------------------------
    "hundredpercentbarchat": "hundredPercentStackedBarChart",
    "hundredpercentbarchart": "hundredPercentStackedBarChart",
    "100barchat": "hundredPercentStackedBarChart",
    "100barchart": "hundredPercentStackedBarChart",
    "hundredpercentstackedbarchat": "hundredPercentStackedBarChart",
    "hundredpercentstackedbarchart": "hundredPercentStackedBarChart",
    "hundredpercentcolumnchat": "hundredPercentStackedColumnChart",
    "hundredpercentcolumnchart": "hundredPercentStackedColumnChart",
    "100columnchat": "hundredPercentStackedColumnChart",
    "100columnchart": "hundredPercentStackedColumnChart",
    "hundredpercentstackedcolumnchat": "hundredPercentStackedColumnChart",
    "hundredpercentstackedcolumnchart": "hundredPercentStackedColumnChart",
    "stackedbarchat": "barChart",
    "stackedbarchart": "barChart",
    "stackedcolumnchat": "columnChart",
    "stackedcolumnchart": "columnChart",

    # Tableau Raw Mark Types
    "text": "tableEx",
    "square": "treemap",
    "circle": "scatterChart",
    "shape": "scatterChart",
    "ganttbar": "clusteredBarChart",
    "polygon": "filledMap",
    "multipolygon": "filledMap",
    "density": "filledMap",

    # Bars & Columns
    "bar chart": "clusteredBarChart",
    "bar": "clusteredBarChart",
    "horizontal bar": "clusteredBarChart",
    "stacked bar": "barChart",
    "stacked bar chart": "barChart",
    "100% stacked bar": "hundredPercentStackedBarChart",
    "100% stacked bar chart": "hundredPercentStackedBarChart",
    "diverging stacked bar": "hundredPercentStackedBarChart",
    "likert scale chart": "hundredPercentStackedBarChart",
    "column": "clusteredColumnChart",
    "column chart": "clusteredColumnChart",
    "standard column": "clusteredColumnChart",
    "vertical column": "clusteredColumnChart",
    "stacked column": "columnChart",
    "stacked column chart": "columnChart",
    "100% stacked column": "hundredPercentStackedColumnChart",
    "100% stacked column chart": "hundredPercentStackedColumnChart",
    "marimekko chart": "hundredPercentStackedColumnChart",
    "mosaic chart": "hundredPercentStackedColumnChart",
    "histogram": "clusteredColumnChart",
    "gantt chart": "clusteredBarChart",

    # Pies & Circles
    "pie": "pieChart",
    "pie chart": "pieChart",
    "donut": "donutChart",
    "donut chart": "donutChart",
    "radial bar chart": "donutChart",
    "semi-circle chart": "gauge",
    "half donut chart": "gauge",

    # Lines & Areas
    "line": "lineChart",
    "line chart": "lineChart",
    "multi-line chart": "lineChart",
    "dual axis line": "lineChart",
    "sparkline standalone": "lineChart",
    "area": "areaChart",
    "area chart": "areaChart",
    "stacked area": "stackedAreaChart",
    "100% stacked area": "stackedAreaChart",

    # Combos
    "combo chart": "lineClusteredColumnComboChart",
    "dual axis combo chart": "lineClusteredColumnComboChart",
    "line and clustered column": "lineClusteredColumnComboChart",
    "line and stacked column": "lineStackedColumnComboChart",
    "pareto chart": "lineClusteredColumnComboChart",

    # Trees, Hierarchies & Flows
    "treemap": "treemap",
    "sunburst chart": "treemap",
    "waterfall": "waterfallChart",
    "waterfall chart": "waterfallChart",
    "funnel": "funnel",
    "funnel chart": "funnel",
    "ribbon chart": "ribbonChart",
    "sankey diagram": "ribbonChart",

    # Scatter
    "scatter": "scatterChart",
    "scatter plot": "scatterChart",
    "bubble chart": "scatterChart",
    "box and whisker plot": "scatterChart",

    # Maps
    "symbol map": "map",
    "bubble map": "map",
    "choropleth map": "filledMap",
    "filled map": "filledMap",
    "shape map": "shapeMap",

    # Tables & Matrices
    "text table": "tableEx",
    "table": "tableEx",
    "crosstab": "pivotTable",
    "matrix": "pivotTable",
    "pivot table": "pivotTable",

    # Cards & Gauges
    "card": "card",
    "multi-row kpi card": "multiRowCard",
    "kpi": "kpi",
    "gauge": "gauge",
    "bullet graph": "gauge",

    # Advanced
    "slicer": "slicer",
    "filter control": "slicer",
    "decomposition tree": "decompositionTree",
    "key influencers": "keyDriversVisual",
    "q&a natural language box": "qnaVisual",
}

_NORMALIZED_FALLBACKS = [
    ("hundredpercentbar", "hundredPercentStackedBarChart"),
    ("100percentbar", "hundredPercentStackedBarChart"),
    ("100bar", "hundredPercentStackedBarChart"),
    ("hundredpercentcolumn", "hundredPercentStackedColumnChart"),
    ("100percentcolumn", "hundredPercentStackedColumnChart"),
    ("100column", "hundredPercentStackedColumnChart"),
    ("hundredpercentarea", "stackedAreaChart"),
    ("100percentarea", "stackedAreaChart"),
    ("stackedbar", "barChart"),
    ("stackedcolumn", "columnChart"),
    ("stackedarea", "stackedAreaChart"),
    ("combo", "lineClusteredColumnComboChart"),
    ("dualaxis", "lineClusteredColumnComboChart"),
    ("donut", "donutChart"),
    ("pie", "pieChart"),
    ("waterfall", "waterfallChart"),
    ("funnel", "funnel"),
    ("gauge", "gauge"),
    ("bullet", "gauge"),
    ("ribbon", "ribbonChart"),
    ("sankey", "ribbonChart"),
    ("decomposition", "decompositionTree"),
    ("influencer", "keyDriversVisual"),
    ("treemap", "treemap"),
    ("scatter", "scatterChart"),
    ("bubble", "scatterChart"),
    ("bar", "clusteredBarChart"),
    ("column", "clusteredColumnChart"),
    ("area", "areaChart"),
    ("line", "lineChart"),
    ("multirow", "multiRowCard"),
    ("card", "card"),
    ("kpi", "kpi"),
    ("matrix", "pivotTable"),
    ("pivot", "pivotTable"),
    ("crosstab", "pivotTable"),
    ("slicer", "slicer"),
    ("filter", "slicer"),
    ("shapemap", "shapeMap"),
    ("filledmap", "filledMap"),
    ("map", "map"),
    ("table", "tableEx"),
]


def map_visual_type(raw_type: Optional[str]) -> str:
    """Normalizes raw Tableau metadata visual types to Power BI visualType."""
    if not raw_type:
        return "tableEx"

    cleaned = str(raw_type).strip().lower()
    if not cleaned:
        return "tableEx"

    # 1. Direct dictionary match (with original spaces/punctuation)
    if cleaned in VISUAL_TYPE_MAPPINGS:
        return VISUAL_TYPE_MAPPINGS[cleaned]

    # 2. Normalized alphanumeric representation (removes spaces, hyphens, %)
    # E.g., "100% stacked bar chart" -> "100stackedbarchart"
    compact = re.sub(r"[^a-z0-9]", "", cleaned)
    if compact in VISUAL_TYPE_MAPPINGS:
        return VISUAL_TYPE_MAPPINGS[compact]

    # Handle common typo "chat" -> "chart"
    compact_fixed = compact.replace("barchat", "barchart").replace("columnchat", "columnchart")
    if compact_fixed in VISUAL_TYPE_MAPPINGS:
        return VISUAL_TYPE_MAPPINGS[compact_fixed]

    # 3. Normalized fallback keyword scan
    for keyword, mapped in _NORMALIZED_FALLBACKS:
        if keyword in compact or keyword in compact_fixed:
            return mapped

    return "tableEx"
