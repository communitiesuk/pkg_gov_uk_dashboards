"""Creates a Dash Graph component from a given Plotly figure"""

from typing import Any, Dict, Union
import plotly.graph_objects as Figure
from dash import dcc


def generate_dash_graph_from_figure(
    figure: Figure,
    graph_name: str,
    graph_style: Union[Dict[str, Any], None] = None,
    double_click_attribute: Union[str, bool] = False,
    class_name: str = "",
) -> dcc.Graph:
    """
    Creates a Dash Graph component from a given Plotly figure. This function allows for the
    customisation of the graph's appearance and behavior, and includes default pointer cursor,
    from "default-cursor-graph" class.
    Args:
    - figure: Plotly.graph_objects.Figure instance to be displayed within the Dash Graph component.
    - graph_name: A name for the id of the graph component.
    - graph_style: An optional dictionary specifying CSS styles to apply to the graph component.
    - double_click_attribute: Determines the action taken on double-clicking the graph.
                              Can be a boolean or a string specifying the mode.
    - className (str): A string containing one or more CSS class names to apply to the graph.
    Returns:
    - A dash.dcc.Graph component configured with the provided parameters and styles.
    """

    if not graph_style:
        graph_style = {}

    if "height" not in graph_style.keys():
        graph_style["height"] = "450px"

    figure.update_layout(dragmode=False)
    # pylint: disable=duplicate-code
    return dcc.Graph(
        id=f"{graph_name}-graph",
        responsive=True,
        figure=figure,
        style=graph_style,
        config={
            "displayModeBar": False,
            "doubleClick": double_click_attribute,
            "scrollZoom": False,
        },
        className="default-cursor-graph " + class_name,
    )
