"""green_button"""

from dash import html


def green_button(button_text: str, button_id: str):
    """
    Return a green button which is aligned to the right

    Args:
    button_text (str): The text to display on the button.
    button_id: (str) = id for button
    """

    return html.Div(
        [
            html.Button(
                button_text,
                id=button_id,
                n_clicks=0,
                className="govuk-button",
            ),
        ],
        className="govuk-button-group",
    )
