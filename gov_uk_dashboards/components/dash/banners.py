"""HTML components for displaying messages to the user in a banner format"""

from dash import html

from gov_uk_dashboards.constants import BANNER_STYLE, ERROR_MESSAGE_BANNER_STYLE


def message_banner(category, message, style=None):
    """
    Return a coronavirus dashboard-style changelog banner to be used to communicate to the user
    when the dashboard was last updated.

    See https://coronavirus.data.gov.uk
    """
    return html.Div(
        html.P(
            [
                html.Strong(
                    category,
                    className="govuk-tag",
                    style={
                        "background": "black",
                        "color": "white",
                        "margin": "0 1rem 0 0",
                        "lineHeight": "initial",
                    },
                ),
                message,
            ],
            className="govuk-body-s govuk-!-margin-bottom-0",
        ),
        className="change-log-banner govuk-!-margin-bottom-2",
        style=style,
    )


def get_warning_banner(banner_text: str) -> html.Div:
    """Returns warning banner with banner_text displayed.

    Args:
        banner_text (str): Text to display on warning banner.
    """
    return html.Div(
        [
            message_banner(
                "UPDATE",
                html.Span(banner_text),
                style=ERROR_MESSAGE_BANNER_STYLE,
            )
        ],
        style=BANNER_STYLE,
    )
