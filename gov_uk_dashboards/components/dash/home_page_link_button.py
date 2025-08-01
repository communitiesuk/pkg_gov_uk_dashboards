"""home_page_link_button"""

from typing import Optional
from dash import html


def home_page_link_button(
    title: str,
    pathname_or_url_link: str,
    pathname_rather_than_url: bool,
    image_path: str,
    info: Optional[str] = None,
):
    """Creates home page link card.

    Args:
        title (str): Button title.
        pathname_or_url_link (str): The target link, either a pathname or full URL.
        pathname_rather_than_url (bool): If True, `pathname_or_url_link` is treated as a pathname
            (loading content in the same tab). If False, it is treated as a full URL
            (opening in a new tab).
        image_path (str): The path to an SVG image used as an icon for the button.
        info (Optional[str], optional): Additional text for the button. Defaults to None.

    Returns:
        dash_html_components.A: A Dash HTML `A` element representing the link button.
    """

    link_attributes = {
        "href": pathname_or_url_link,
        "id": f"link-to-{title.replace(' ', '-')}",
        "className": "govuk-body homepage-card-grid-item",
    }

    if pathname_rather_than_url is False:
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
                                className=(
                                    "govuk-heading-l" if info is not None else None
                                ),
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
                            "textAlign": "left",
                            "textDecoration": "none",
                            "paddingLeft": "5%",
                        },
                    ),
                    html.Img(src=image_path, style={"width": "100%"}),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "5fr 1fr",
                    "alignItems": "center",
                },
            )
        ],
        **link_attributes,
    )
