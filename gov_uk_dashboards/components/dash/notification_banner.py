"""notification_banner"""

from dash import html


def notification_banner(
    text: str, text_class_name: str = "govuk-warning-text__text", style: dict = None
):
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
