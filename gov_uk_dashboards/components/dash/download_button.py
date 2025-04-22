"""download_button"""
import warnings
from dash import html

from gov_uk_dashboards.constants import DOWNLOAD_BUTTON_CLASSES


def download_button(button_text: str, button_id: str = "download-button"):
    """
    Return a download button which is aligned to the right

    Args:
    button_text (str): The text to display on the button.
    button_id: (str, Optional) = id for dropdown, default to "download-button"
    """
    warnings.warn(
        "Note there is an alternative function to download_button() called "
        "create_download_button_with_icon() which includes a download icon and improved styling.",
        Warning,
        stacklevel=2,
    )

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


def create_download_button_with_icon(
    button_text: str, button_id_name: str
) -> html.Button:
    """Create a download button with icon, aligned to the left.

    Parameters:
    - button_id_name (str): A unique identifier for the button.

    Returns:
    - html.Button: Download button.
    """
    download_type = button_text.lower().replace(" ", "-")
    return html.Button(
        [
            html.Div("", className="download-icon"),
            button_text,
        ],
        id={
            "download-type": download_type,
            "name": button_id_name,
        },
        n_clicks=0,
        className=DOWNLOAD_BUTTON_CLASSES,
        type="submit",
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
        },
    )
