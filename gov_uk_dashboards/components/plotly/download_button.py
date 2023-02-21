"""download_button"""
from dash import html


def download_button():
    """
    Return download button which is aligned to the right
    """
    return html.Div(
        [
            html.Button(
                "Download data",
                id="download-button",
                n_clicks=0,
                className="govuk-button govuk-button--secondary",
            ),
        ],
        className="govuk-button-group",
        style={"float": "right"},
    )
