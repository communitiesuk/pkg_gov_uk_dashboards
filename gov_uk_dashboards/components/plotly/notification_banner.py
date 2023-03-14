"""notification_banner"""
from dash import html


def notification_banner(text: str):
    """
    Return Gov UK Design component notification banner component.
    """
    banner = html.Div(
        [
            html.Div(
                [
                    html.H2(
                        ["Important"],
                        className="govuk-notification-banner__title",
                        id="govuk-notification-banner-title",
                    )
                ],
                className="govuk-notification-banner__header",
            ),
            html.Div(
                [
                    html.P(
                        [
                            text,
                        ],
                        className="govuk-notification-banner__heading",
                    )
                ],
                className="govuk-notification-banner__content",
            ),
        ],
        className="govuk-notification-banner",
        role="region",
        **{
            "aria-labelledby": "govuk-notification-banner-title",
            "data-module": "govuk-notification-banner",
        }
    )
    return banner
