"""card"""

from dash import html


def card(children, amend_style=None):
    """A rectangle with a grey background.
    Mostly used to wrap individual visualisations, e.g. a gauge."""
    return html.Div(children, className="mini-card", style=amend_style)


def empty_card():
    """
    An empty card that is hidden to help keep alignment with rows and columns.
    """
    return html.Div(className="mini-card-empty")
