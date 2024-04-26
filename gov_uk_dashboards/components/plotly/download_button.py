"""download_button"""
import warnings
from dash import html


def download_button(button_text: str, button_id: str = "download-button"):
    """
    Return a download button which is aligned to the right

    Args:
    button_text (str): The text to display on the button.
    button_id: (str, Optional) = id for dropdown, default to "download-button"
    """
    warnings.warn(
        "Note there is an alternative function to download_button() called "
        "download_button_with_icon() which includes a download icon and improved styling.",
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


def download_button_with_icon(button_text: str, button_id: str = "download-button"):
    """
    Return a download button styled with additional classes and an SVG icon,
    aligned to the right.

    Args:
    button_text (str): The text to display on the button.
    button_id (str, Optional): ID for the button, defaults to "download-button".
    """
    classes = (
        "govuk-button govuk-button--primary "
        "govuk-!-margin-bottom-0 govuk-!-margin-top-4 "
        "flex w-auto items-center gap-2 print:hidden"
    )
    return html.Div(
        [
            html.Button(
                [html.Div("", className="download-icon"), button_text],
                id=button_id,
                n_clicks=0,
                className=classes,
                type="submit",
                style={"display": "flex", "alignItems": "center", "gap": "8px"},
            ),
        ],
        className="govuk-button-group",
        style={"float": "right"},
    )
