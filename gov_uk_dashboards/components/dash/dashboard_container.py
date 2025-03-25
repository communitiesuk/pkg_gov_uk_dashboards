"""dashboard_container"""

from dash import html


def dashboard_container(children):
    """
    A HTML wrapper for a whole dashboard.

    Applies styles that make sure the application uses the full width of the browser.

    Unfortunately, due to the way Dash adds further HTML wrappers when it serves content,
    this wrapper cannot be applied once in template.html,
    and must be added within the application for each new dashboard.
    """
    return html.Div(children, className="dashboard-container")
