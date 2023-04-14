"""navbar"""

from typing import Optional
from dash import html, dcc


def side_navbar(
    links, identifier: Optional[str] = None, list_id: Optional[str] = "navbar_list"
):
    """A navigation bar for switching between dashboards."""
    return html.Nav(
        html.Ul(links, id=list_id, className="moj-side-navigation__list"),
        className="moj-side-navigation",
        role="navigation",
        id=identifier if identifier is not None else "",
    )


def side_navbar_link(text, href):
    """A link to another dashboard"""
    return html.Li(
        dcc.Link(text, href=href, className="govuk-link govuk-link--no-visited-state"),
        className="moj-side-navigation__item govuk-!-margin-bottom-1",
    )


def side_navbar_link_active(text, href):
    """
    A link to another dashboard that appears highlighted, suggesting to the user that they are
    already viewing the linked dashboard.
    """
    return html.Li(
        dcc.Link(text, href=href, className="govuk-link govuk-link--no-visited-state"),
        className=(
            "moj-side-navigation__item moj-side-navigation__item--active "
            "govuk-!-margin-bottom-1"
        ),
    )
