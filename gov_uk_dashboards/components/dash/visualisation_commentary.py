"""format_visualisation_commentary"""

from dash import html


def format_visualisation_commentary(commentary):
    """Apply Gov.UK Design System styles to format title and accompanying commentary"""
    return html.Div(
        [
            html.Div(
                [
                    html.P(
                        commentary,
                        className="govuk-heading-m govuk-!-margin-bottom-1",
                        style={"fontSize": "14px", "fontWeight": "normal"},
                    ),
                ],
                className="govuk-grid-column-full",
            )
        ],
        className="govuk-grid-row",
    )
