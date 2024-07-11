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
                        src="assets\\images\\mhclg_white_no_background.png",
                        srcSet="assets\\images\\mhclg_white_no_background.png 490w",
                        sizes="(min-width: 600px) 200px, 30vw",
                        className="header-image",
                        style={"maxWidth": "200px"},
                        alt="Department for Levelling Up, Housing & Communities",
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
                                style={"background-color": "#000000"},
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
            style={"border-bottom": "10px solid #000000"},
        ),
        className="govuk-header",
        role="banner",
        style=header_style
        | {"border-color": "#000000", "background-color": "rgb(0,98,94)"},
        **{"data-module": "govuk-header"},
    )
