"""format_visualisation_title"""

from dash import html


def format_visualisation_title(title):
    """Apply Gov.UK Design System styles to format title"""
    return html.Div(
        [
            html.Div(
                [
                    html.H1(
                        title,
                        id="title",
                        className="govuk-heading-m govuk-!-margin-bottom-1",
                    ),
                ],
                className="govuk-grid-column-full",
            )
        ],
        className="govuk-grid-row",
    )
