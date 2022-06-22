"""filter_panel"""
from dash import html

from .collapsible_panel import collapsible_panel
from .row_component import row_component
from gov_uk_dashboards.components.plotly.heading import heading2


def filter_panel(children, title=None):
    """
    A container with a grey background and a title that allows the user to select and filter metrics
    on the dashboard.

    Args:
        children (list): Dash HTML elements representing the individual selection
            and filtering widgets. E.g.dropdown menus, sliders, text input boxes etc.
    """
    return row_component(
        html.Div(
            [
                heading2(title) if title else None,
                collapsible_panel(
                    title="Select and filter metrics",
                    default_open=True,
                    children=[
                        html.Div(
                            html.A(
                                "Clear all selections",
                                className="govuk-button govuk-button--warning govuk-!-margin-0",
                                href="?",
                            ),
                            style={"width": "100%"},
                        ),
                        *children,
                    ],
                ),
            ],
            className="govuk-!-margin-0",
            style={"flex": "1 1 100%"},
        )
    )


def hidden_filter(html_id):
    """
    An empty, invisible HTML element that stands in for a filter component.

    Used to keep the state of the filter panel current across dashboards,
    even those that don't allow the user to filter for a particular metric.
    """
    return html.Div(id=html_id, style={"display": "none"})
