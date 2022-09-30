"""navbar"""

from typing import Optional
from dash import html, dcc


def side_navbar(links, identifier: Optional[str] = None):
    """A navigation bar for switching between dashboards."""
    return html.Nav(
        links,
        className="moj-side-navigation moj-side-navigation__list",
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
