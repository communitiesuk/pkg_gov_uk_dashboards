"""captioned_figure function"""
from typing import Any, Optional, Union
import plotly
import dash
from gov_uk_dashboards.components.plotly.graph import graph


def captioned_figure(
    figure: plotly.graph_objects.Figure,
    captions: Union[
        dash.development.base_component.Component,
        list[dash.development.base_component.Component],
    ],
    figure_name: str,
    style: Optional[dict[str, Any]] = None,
):
    """
    Return figure with attached caption that can be read by a screen reader.

    The caption will not be displayed to users viewing the website through a
    browser but is available for the a screen reader to describe.

    The supplied graph and caption are wrapped in an HTML <figure> element.

    Args:
        figure (plotly.graph_objects.Figure): The plotly figure to display and caption.
        captions (Component, list[Component]): The captions to apply to the
            figure to be read by a screen reader.
        figure_name (str): Identifier for the figure. Should be lower case,
            with words separated by dashes.
        style (Optional[dict], optional): Any custom style to apply to the graph.
            Defaults to None.

    Returns:
        dash.html.Figure: Figure html element containing the graph and its caption.
    """
    return dash.html.Figure(
        [
            dash.html.Div(
                children=graph(
                    element_id=f"{figure_name}-figure",
                    figure=figure,
                    style=style,
                ),
                **{"role": "img", "aria-labelledby": f"{figure_name}-caption"},
                id=f"{figure_name}-graph",
            ),
            dash.html.Figcaption(
                children=captions,
                id=f"{figure_name}-caption",
                className="govuk-visually-hidden",
            ),
        ]
    )
