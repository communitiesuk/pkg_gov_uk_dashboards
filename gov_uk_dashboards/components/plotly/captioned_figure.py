"""captioned_figure function"""

from typing import Any, Optional, Union
import plotly
import dash


def captioned_figure(
    figure: plotly.graph_objects.Figure,
    captions: Union[
        dash.development.base_component.Component,
        list[dash.development.base_component.Component],
    ],
    figure_name: str,
    *,
    graph_style: Optional[dict[str, Any]] = None,
    desktop_only: bool = False,
    double_click_attribute: Union[str, bool] = True,
):
    # pylint: disable=too-many-arguments
    """
    Return figure with attached caption that can be read by a screen reader.

    The caption will not be displayed to users viewing the website through a
    browser but is available for a screen reader to describe.

    The supplied graph and caption are wrapped in an HTML <figure> element.

    Args:
        figure (plotly.graph_objects.Figure): The plotly figure to display and caption.
        captions (Component, list[Component]): The captions to apply to the
            figure to be read by a screen reader.
        figure_name (str): Identifier for the figure. Should be lower case,
            with words separated by dashes, e.g. jitter-figure
        graph_style (Optional[dict], optional): Any custom style to apply to the graph.
            Defaults to None.
        desktop_only (bool, optional): Whether the figure should be replaced with
            the caption when viewed on mobile. Defaults to False.
        double_click_attribute (Union[str, bool]): Set the doubleClick attribute, which controls
            the response when a user double clicks on the plot. Defaults to True.

    Returns:
        dash.html.Figure: Figure html element containing the graph and its caption.
    """
    if not graph_style:
        graph_style = {}

    if "height" not in graph_style.keys():
        graph_style["height"] = "450px"

    return dash.html.Figure(
        [
            dash.html.Div(
                children=dash.dcc.Graph(
                    id=f"{figure_name}-graph",
                    responsive=True,
                    figure=figure,
                    style=graph_style,
                    config={
                        "displayModeBar": False,
                        "doubleClick": double_click_attribute,
                    },
                ),
                className="jitter-desktop-only" if desktop_only else "",
                **{"role": "img", "aria-labelledby": f"{figure_name}-caption"},
                id=f"{figure_name}-figure",
            ),
            dash.html.Figcaption(
                children=captions,
                id=f"{figure_name}-caption",
                className=(
                    "govuk-visually-hidden-desktop-only"
                    if desktop_only
                    else "govuk-visually-hidden"
                ),
            ),
        ]
    )
