"""Context_box"""
from dash import html


def put_context_banner(
    text: str, text_class_name: str = "govuk-warning-text__text", style: dict = None
):
    """
    Return Context Box based on Gov UK Design notification banner component.
    """
    banner = html.Div(
        [
            html.Div(
                [
                    html.P(
                        [
                            text,
                        ],
                        className=text_class_name,
                    )
                ],
                className="govuk-notification-banner__content",
            ),
        ],
        className="govuk-notification-banner",
        role="region",
        style=style,
        **{
            "aria-labelledby": "govuk-notification-banner-title",
            "data-module": "govuk-notification-banner",
        }
    )
    return banner

