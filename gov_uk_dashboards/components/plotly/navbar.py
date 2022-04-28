"""navbar"""

from dash import html, dcc


def navbar(links):
    """A navigation bar for switching between dashboards."""
    return html.Nav(
        html.Ul(
            links, className="moj-side-navigation__list", id="navigation-items"
        ),
        className="moj-side-navigation",
        role="navigation",
    )


def navbar_link(text, href):
    """A link to another dashboard"""
    return html.Li(
        dcc.Link(text, href=href, className="govuk-link govuk-link--no-visited-state"),
        className="moj-side-navigation__item",
    )


def navbar_link_active(text, href):
    """
    A link to another dashboard that appears highlighted, suggesting to the user that they are
    already viewing the linked dashboard.
    """
    return html.Li(
        dcc.Link(text, href=href, className="govuk-link govuk-link--no-visited-state"),
        className="moj-side-navigation__item moj-side-navigation__item--active",
    )
