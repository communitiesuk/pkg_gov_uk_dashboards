"""header"""

from dash import html


def header(title: str, strong_class: str = "", background_colour: str = None):
    """
    The header component, shared across all dashboard views. Includes optional strong_class
    parameter to provide extra styling in the form of a class.
    Includes optional background_colour parameter to override default black background colour.

    Based on the header component provided by the GOV.UK Design System.
    https://design-system.service.gov.uk/components/header/
    """
    header_style = {"backgroundColor": background_colour} if background_colour else {}

    return html.Header(
        html.Div(
            html.Div(
                [
                    html.Img(
                        src="assets\\images\\mhclg_coat_of_arms.png",
                        srcSet="assets\\images\\mhclg_coat_of_arms.png 490w",
                        sizes="(min-width: 600px) 400px, 30vw",
                        className="header-image",
                        style={"maxWidth": "400px"},
                        alt="Ministry of Housing, Communities & Local Government",
                    ),
                    html.Div(
                        ["Ministry of Housing, Communities & Local Government"],
                        style={"fontSize": "20px", "fontWeight": "200px"},
                    ),
                    html.A(
                        title,
                        href="/",
                        className=" ".join(
                            [
                                "govuk-header__link",
                                "govuk-header__link--service-name",
                                "dashboard-title",
                            ],
                        ),
                    ),
                    html.Div(
                        [
                            html.Strong(
                                "OFFICIAL",
                                className="govuk-tag protective-marking",
                                id="protective-marking",
                                style={"backgroundColor": "#000000"},
                            )
                        ],
                        className=f"{strong_class}",
                    ),
                    html.Button(
                        "Menu ▼",
                        id="mobile-menu-btn",
                        className="mobile-menu-button govuk-button",
                    ),
                ],
                className="govuk-header__content",
            ),
            className="govuk-header__container govuk-width-container",
            style={"borderBottom": "10px solid #000000"},
        ),
        className="govuk-header",
        role="banner",
        style=header_style
        | {"borderColor": "#000000", "backgroundColor": "rgb(0,98,94)"},
        **{"data-module": "govuk-header"},
    )
