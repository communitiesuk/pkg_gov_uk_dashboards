"""download_button"""
from typing import Optional
from dash import html


def download_button(button_text: str, button_id: Optional[str] = "download-button"):
    """
    Return a download button which is aligned to the right

    Args:
    button_text (str): The text to display on the button.
    button_id: (str, Optional) = id for dropdown, default to "download-button"
    """
    return html.Div(
        [
            html.Button(
                button_text,
                id=button_id,
                n_clicks=0,
                className="govuk-button govuk-button--secondary",
            ),
        ],
        className="govuk-button-group",
        style={"float": "right"},
    )
