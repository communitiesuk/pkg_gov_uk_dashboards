"""notification_banner"""

from dash import html


def notification_banner(
    text: list,
    title: str = "Important",
    text_class_name: str = "govuk-notification-banner__heading",
    style: dict = None,
    title_color: str = None,
):
    """
    Return Gov UK Design component notification banner component.
    """
    banner = html.Div(
        [
            html.Div(
                [
                    html.H2(
                        [title],
                        className="govuk-notification-banner__title",
                        id="govuk-notification-banner-title",
                        style={"color": title_color} if title_color else None,
                    )
                ],
                className="govuk-notification-banner__header",
            ),
            html.Div(
                [
                    html.P(
                        text,
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
