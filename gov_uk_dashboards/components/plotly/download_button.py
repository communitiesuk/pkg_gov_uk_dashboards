"""download_button"""
from dash import html


def download_button(button_text: str):
    """
    Return a download button which is aligned to the right

    Args:
    button_text (str): The text to display on the button.
    """
    return html.Div(
        [
            html.Button(
                button_text,
                id="download-button",
                n_clicks=0,
                className="govuk-button govuk-button--secondary",
            ),
        ],
        className="govuk-button-group",
        style={"float": "right"},
    )
