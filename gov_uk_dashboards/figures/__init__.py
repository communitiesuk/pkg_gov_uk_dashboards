"""Module containing standard Plotly figures for use in dashboards.

Contains:
- ChartData: A dataclass for containing standard information useful for
    plotting charts.
- line_chart: Create and return a plotly express line chart with
    standard formatting.
- enums: Module containing enums used in the construction of plotly figures.
    - DashPatterns: Sets out valid dash patterns used by plotly/plotly express.
- styles: Module containing classes & functions used for styling plotly figures.
    - LineStyle: Dataclass containing information on how to style a line on a line
        chart.
"""

from . import enums
from . import styles

# from .chart_data import ChartData
# from .line_chart import line_chart
