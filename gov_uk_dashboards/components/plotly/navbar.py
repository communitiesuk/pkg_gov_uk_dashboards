"""navbar"""

from dash import html, dcc

# <nav class="moj-sub-navigation" aria-label="Sub navigation">

#   <ul class="moj-sub-navigation__list">
#     <li class="moj-sub-navigation__item">
#       <a class="moj-sub-navigation__link" aria-current="page" href="#1">Nav item 1</a>
#     </li>

#     <li class="moj-sub-navigation__item">
#       <a class="moj-sub-navigation__link" href="#2">Nav item 2</a>
#     </li>

#     <li class="moj-sub-navigation__item">
#       <a class="moj-sub-navigation__link" href="#3">Nav item 3</a>
#     </li>
#   </ul>

# </nav>

def navbar(links):
    """A navigation bar for switching between dashboards."""
    return html.Nav(
        html.Ul(
            links, className="moj-sub-navigation__list", id="navigation-items"
        ),
        className="moj-sub-navigation",
        role="navigation",
    )


def navbar_link(text, href):
    """A link to another dashboard"""
    return html.Li(
        html.A(text, href=href),
        className="moj-sub-navigation__item",
    )


def navbar_link_active(text, href):
    """
    A link to another dashboard that appears highlighted, suggesting to the user that they are
    already viewing the linked dashboard.
    """
    return html.Li(
        html.A(text, href=href,aria-current="page"),
        className="moj-sub-navigation__item",
    )
