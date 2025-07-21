"""apply_and_reset_filters_buttons"""

from dash import html


def apply_and_reset_filters_buttons():
    """
    Return clear all selections link which is aligned to the right
    """
    return html.Div(
        [
            html.A(
                "Reset filters",
                href="?",
                className="govuk-link govuk-body",
                role="button",
            ),
            html.Button(
                "Apply filters",
                id="submit-button",
                n_clicks=0,
                className="govuk-button govuk-!-margin-left-5",
            ),
        ],
        className="govuk-button-group horizontal-button-group",
    )
