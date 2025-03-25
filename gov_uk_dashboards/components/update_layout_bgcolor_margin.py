"""Function to update the background colour and margin for plots"""

import plotly.graph_objects as go
from gov_uk_dashboards import colours


def update_layout_bgcolor_margin(fig: go.Figure, colour: str):
    """update background colour and margin for plot"""
    fig.update_layout(
        plot_bgcolor=colour,
        paper_bgcolor=colour,
        yaxis_zerolinecolor=colour,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )
    fig.update_xaxes(
        gridcolor=colour,
        zerolinecolor=colour,
        ticks="outside",
        tickcolor=colours.GovUKColours.MID_GREY.value,
    )
    fig.update_yaxes(
        gridcolor=colours.GovUKColours.MID_GREY.value,
        zerolinecolor=colours.GovUKColours.MID_GREY.value,
    )
