"""convert_fig_to_image_and_download"""

import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc


def convert_fig_to_image_and_download(fig: go.Figure, name: str):
    """Converts a given Plotly figure to a PNG image and returns a Dash component
    for downloading the image.
    """
    fig.update_layout(margin={"t": 150, "b": 250, "l": 100, "r": 50})

    filename = f"{name}-chart.png"
    img_bytes = pio.to_image(fig, format="png", width=1600, height=800)
    return dcc.send_bytes(img_bytes, filename)
