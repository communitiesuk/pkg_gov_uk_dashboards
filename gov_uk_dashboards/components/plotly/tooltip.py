"""tooltip"""
from dash import html
import dash_bootstrap_components as dbc


def tooltip(tooltip_text: str, tooltip_id: str, color: str, font_size: int):
    """Creates a tooltip for providing further information

    Args:
        tooltip_text (str): The text to display when hovering
        tooltip_id (str): The element ID to contain the tooltip text
        color (str): The color of the tooltip text
        font_size (int): The size of the tooltip text

    Returns:
        html.Span: The dash HTML object for the tooltip.
    """

    return html.Span(
        [
            " ⓘ",
            dbc.Tooltip(
                tooltip_text,
                role="tooltip",
                target=tooltip_id,
                class_name="tooltip tooltiptext",
                style={"color": color, "font-size": font_size},
            ),
        ],
        id=tooltip_id,
        style={"cursor": "pointer"},
    )
