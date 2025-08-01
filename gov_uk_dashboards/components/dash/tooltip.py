"""tooltip"""

from dash import html
import dash_bootstrap_components as dbc


def tooltip(
    tooltip_text: str, tooltip_id: str, color: str = "white", font_size: str = "16px"
):
    """Creates a tooltip for providing further information

    Args:
        tooltip_text (str): The text to display when hovering
        tooltip_id (str): The element ID to contain the tooltip text
        color (str): The color of the tooltip text
        font_size (str): The size of the tooltip text

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
                style={"color": color, "fontSize": font_size},
            ),
        ],
        id=tooltip_id,
        role="tooltip",
        **{"aria-label": tooltip_text},
        style={"cursor": "pointer"},
    )
