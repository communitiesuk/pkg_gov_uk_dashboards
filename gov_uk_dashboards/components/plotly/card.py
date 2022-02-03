"""card"""
from dash import html


def card(children):
    """A rectangle with a grey background.
    Mostly used to wrap individual visualisations, e.g. a gauge."""
    return html.Li(children, className="mini-card")
