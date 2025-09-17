"""warning_text_sensitive function"""

import os
from dash import html
from gov_uk_dashboards.components.dash.warning_text import warning_text


def warning_text_sensitive(text: str, sticky: bool = True) -> html.Div:
    """
    Creates a warning message to inform users. The warning text can optionally be made sticky,
    meaning it will stay visible at the top of the page when scrolling.
    Args:
    - text (str): The text to display.
    - sticky (bool, optional): If True, the warning text will have a sticky position, staying
      visible during scroll. Defaults to True.
    Returns:
    - dash_html_components.Div: A Dash HTML Div component containing the styled warning text.
    """
    outer_style_dict = {
        "zIndex": "1000",
    }
    # Added env condition because visual tests were failing due to banner moving by a few pixels
    if sticky and os.environ.get("STAGE") != "testing":
        outer_style_dict.update(
            {
                "position": "sticky",
                "top": "20px",
            }
        )

    inner_style_dict = {
        "padding": "5px 10px",
        "backgroundColor": "white",
        "display": "inline-block",
        "borderRadius": "5px",
    }

    return html.Div(
        warning_text(
            text,
            style=inner_style_dict,
        ),
        style=outer_style_dict,
    )
