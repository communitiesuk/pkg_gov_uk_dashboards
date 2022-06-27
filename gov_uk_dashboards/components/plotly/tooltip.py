"""tooltip"""
from dash import html
import dash_bootstrap_components as dbc


def tooltip(tooltip_text, tooltip_id):
    """Creates a tooltip for providing further information"""

    return html.Span(
        [
            " ⓘ",
            dbc.Tooltip(
                tooltip_text,
                target=tooltip_id,
                class_name="tooltip tooltiptext",
                style={"color": "white", "font-size": 12, "width": "10px"},
            ),
        ],
        id=tooltip_id,
        style={"cursor": "pointer"},
    )
