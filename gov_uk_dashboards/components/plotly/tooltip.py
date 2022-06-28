"""tooltip"""
from dash import html
import dash_bootstrap_components as dbc


def tooltip(tooltip_text: str, tooltip_id: str):
    """Creates a tooltip for providing further information

    Args:
        tooltip_text (str): The text to display when hovering
        tooltip_id (str): The element ID to contain the tooltip text

    Returns:
        html.Span: The dash HTML object for the tooltip.
    """

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
