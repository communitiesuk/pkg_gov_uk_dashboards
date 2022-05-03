"""navbar"""

from dash import html, dcc

def navbar(links):
    """A navigation bar for switching between dashboards."""
    return html.Nav(
        html.Ul(
            links, className="moj-primary-navigation__list", id="navigation-items"
        ),
        className="moj-primary-navigation",
        role="navigation",
        **{"aria-label": "Primary navigation"}
    )


def navbar_link(text, href):
    """A link to another dashboard"""
    return html.Li(
        html.A(text, href=href, className="moj-primary-navigation__link"),
        className="moj-primary-navigation__item",
    )


def navbar_link_active(text, href):
    """
    A link to another dashboard that appears highlighted, suggesting to the user that they are
    already viewing the linked dashboard.
    """
    return html.Li(
        html.A(text, href=href, className="moj-primary-navigation__link",
               **{'aria-current': 'page'}),
        className="moj-primary-navigation__item",
    )
