"""tooltip_title"""

from dash import html
import dash_bootstrap_components as dbc


def tooltip_title(title, tooltiptext):
    """Creates a tooltip title for explaining metrics"""

    land_constrained_tooltip = html.Div(
        [
            html.H1(
                [
                    title,
                    html.Span(
                        " ⓘ",
                        id="tooltip-target",
                        style={"cursor": "pointer"},
                    ),
                ],
                className="govuk-heading-m govuk-!-margin-bottom-1",
            ),
            dbc.Tooltip(
                tooltiptext,
                target="tooltip-target",
                class_name="tooltip tooltiptext",
                style={"color": "white", "fontSize": 12, "width": "10px"},
            ),
        ]
    )

    return land_constrained_tooltip
