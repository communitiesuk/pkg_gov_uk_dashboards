from typing import Optional
from dash import html


def home_page_link_button(
    title: str,
    pathname_or_url_link: str,
    pathname_rather_than_url: bool,
    image_path: str,
    info: Optional[str] = None,
):
    """Creates home page link card"""

    link_attributes = {
        "href": pathname_or_url_link,
        "id": f"link-to-{title.replace(' ', '-')}",
        "className": "govuk-body homepage-card-grid-item",
    }

    if pathname_rather_than_url == False:
        link_attributes["target"] = "_blank"
        link_attributes["rel"] = "noopener noreferrer"

    return html.A(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [title],
                                className="govuk-heading-l"
                                if info is not None
                                else None,
                            ),
                            (
                                html.Div(
                                    [info], className="font-weight-normal-override"
                                )
                                if info is not None
                                else None
                            ),
                        ],
                        style={
                            "text-align": "left",
                            "text-decoration": "none",
                            "padding-left": "5%",
                        },
                    ),
                    html.Img(src=image_path, style={"width": "100%"}),
                ],
                style={
                    "display": "grid",
                    "grid-template-columns": "5fr 1fr",
                    "align-items": "center",
                },
            )
        ],
        **link_attributes,
    )
