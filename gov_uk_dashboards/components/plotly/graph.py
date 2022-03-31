"""Create a graph"""
from dash import dcc


def graph(element_id: str, figure: any, style: dict = None):
    """
    Create a responsive dash graph.
    Forces the default height of 450px that plotly uses for
    graphs if style is not specified.
    """
    if not style:
        style = {}

    if "height" not in style.keys():
        style["height"] = "450px"

    return dcc.Graph(
        id=element_id,
        responsive=True,
        figure=figure,
        style=style,
        config={"displayModeBar": False},
    )
