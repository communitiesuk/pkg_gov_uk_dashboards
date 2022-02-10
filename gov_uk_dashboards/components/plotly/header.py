"""header"""
from dash import html


def header(title):
    """
    The header component, shared across all dashboard views.

    Based on the header component provided by the GOV.UK Design System.
    https://design-system.service.gov.uk/components/header/
    """
    return html.Header(
        html.Div(
            html.Div(
                [
                    html.Img(
                        src="assets\\images\\hm-government-logo.png",
                        style={"width": "62px"},
                    ),
                    html.Span(
                        [
                            "Department for Levelling Up,",
                            html.Br(),
                            "Housing & Communities",
                        ],
                        className=" ".join(
                            [
                                "govuk-header__link",
                                "govuk-header__link--service-name",
                                "govuk-!-padding-left-3",
                                "govuk-!-font-size-14",
                            ]
                        ),
                    ),
                    html.A(
                        title,
                        href="/",
                        className=" ".join(
                            [
                                "govuk-header__link",
                                "govuk-header__link--service-name dashboard-title",
                                "govuk-!-padding-top-3",
                            ],
                        ),
                    ),
                    html.Strong(
                        "OFFICIAL",
                        className="govuk-tag protective-marking",
                        id="protective-marking",
                    ),
                ],
                className="govuk-header__content",
            ),
            className="govuk-header__container govuk-width-container",
        ),
        style={"alignItems": "center", "justifyContent": "center"},
        className="govuk-header",
        role="banner",
        **{"data-module": "govuk-header"},
    )
