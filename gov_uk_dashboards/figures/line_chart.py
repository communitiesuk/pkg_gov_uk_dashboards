# """Line chart function"""
# from typing import Optional
# import plotly.express as px
# from gov_uk_dashboards.axes import calc_axis_range
# from gov_uk_dashboards.colours import ONSAccessibleColours
# from .styles import LineStyle
# from .chart_data import ChartData


# def line_chart(
#     data: ChartData,
#     title: str,
#     markers: bool = False,
#     line_styles: Optional[dict[str, LineStyle]] = None,
#     **px_line_kwargs,
# ):
#     """
#     Create and return a plotly express line chart with standard formatting.

#     Dataframe should be sorted so x axis is in the correct order for plotting.

#     If no style information provided, lines will be plotted as solid lines
#     using the ONSAcessibleColours enum for their colours.

#     Args:
#         data (ChartData): Data for the chart.
#         title (str): Title to be shown above the chart.
#         markers (bool, optional): Whether markers should be plotted for each point.
#             Defaults to False.
#         line_styles (dict[str, LineStyle], optional): A dictionary with keys that match
#             the categories in the category column (if supplied), and values that are
#             LineStyle data objects to set out the style of the corresponding line.
#             Defaults to None.
#         **px_line_kwargs: Any other keyword arguments to pass to the plotly express
#             line graph function.

#     Returns:
#         plotly.Figure: The generated line chart figure object.
#     """
#     color_discrete_map = None
#     line_dash_map = None
#     labels = None
#     if line_styles:
#         color_discrete_map = {
#             category: line_style.color for category, line_style in line_styles.items()
#         }
#         line_dash_map = {
#             category: line_style.dash_pattern
#             for category, line_style in line_styles.items()
#         }
#         # If line dashes are set, plotly express automatically appends the name of the dash style
#         # to the label in the legend/hover data.
#         # As this is normally not desired, labels are set manually to override this.
#         labels = {category: category for category in line_styles}

#     linechart = px.line(
#         data.dataframe,
#         x=data.x_column,
#         y=data.y_column,
#         range_y=calc_axis_range(data.dataframe, data.y_column),
#         color_discrete_map=color_discrete_map,
#         line_dash_map=line_dash_map,
#         line_dash=data.category_column,
#         color=data.category_column,
#         labels=labels,
#         markers=markers,
#         color_discrete_sequence=[colour.value for colour in ONSAccessibleColours]
#         if not line_styles
#         else None,
#         **px_line_kwargs,
#     )

#     linechart.update_layout(
#         title=title,
#         paper_bgcolor="rgba(0,0,0,0)",
#         plot_bgcolor="rgba(0,0,0,0)",
#         xaxis_type="category",
#     )

#     return linechart
