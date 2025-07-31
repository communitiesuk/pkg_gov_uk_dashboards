"""Context_banner"""

from dash import html


def context_banner():
    """
    Return context banner based on Gov UK Design component notification banner component.
    """
    banner = html.Div(
        [
            html.Div(
                [
                    html.P(
                        [
                            "Data on its own does not present a complete picture. This explorer"
                            " should be used to generate questions and not reach judgements."
                            " See about the data section for more information.",
                        ],
                        className="govuk-warning-text__text notification-banner-under-filter-panel",
                    )
                ],
                className="govuk-notification-banner__content",
            ),
        ],
        className="govuk-notification-banner",
        role="region",
        style={"maxWidth": "1000px", "marginTop": "20px", "marginBottom": "20px"},
    )
    return banner
