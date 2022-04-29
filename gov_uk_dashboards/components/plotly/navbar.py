"""navbar"""

from dash import html, dcc

# <div class = "moj-primary-navigation" >

#  <div class = "moj-primary-navigation__container" >

#    <div class = "moj-primary-navigation__nav" >

#       <nav class = "moj-primary-navigation" aria-label = "Primary navigation" >

#        <ul class = "moj-primary-navigation__list" >
#          <li class = "moj-primary-navigation__item" >
#             <a class = "moj-primary-navigation__link" aria-current = "page" href = "#1" > Nav item 1 < /a >
#           </li >

#           <li class = "moj-primary-navigation__item" >
#             <a class = "moj-primary-navigation__link" href = "#2">Nav item 2</a>
#           </li >

#           <li class = "moj-primary-navigation__item" >
#             <a class = "moj-primary-navigation__link" href = "#3">Nav item 3</a>
#           </li >
#         </ul >

#       </nav >

#     </div >
#   </div >

# </div >


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
