"""card"""
from dash import html


def card(children):
    """A rectangle with a grey background.
    Mostly used to wrap individual visualisations, e.g. a gauge."""
    style = {"padding-top": "0px",  "padding-left": "0px"}
    return html.Div(children, className="mini-card", style=style)


def empty_card():
    """
    An empty card that is hidden to help keep alignment with rows and columns.
    """
    return html.Div(className="mini-card-empty")
