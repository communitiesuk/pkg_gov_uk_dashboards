"""collapsible_panel"""

from dash import html


def collapsible_panel(title, children, default_open=False):
    """Returns a Dash HTML component that allows the user to open and close a
    collapsible panel containing children"""
    return html.Details(
        [
            html.Summary(
                html.Span(
                    title,
                    className="govuk-!-margin-0 govuk-details__summary-text",
                ),
                className="govuk-details__summary govuk-!-margin-0",
                **{"data-module": "govuk-details"}
            ),
            html.Div(
                children,
                className="govuk-!-padding-0 govuk-!-margin-top-1",
                style={
                    "display": "flex",
                    "alignContent": "stretch",
                    "alignItems": "flex-end",
                    "flexFlow": "row wrap",
                    "justifyContent": "space-between",
                    "gap": "1rem",
                    "margin": "0",
                    "padding": "0",
                },
            ),
        ],
        className="govuk-details govuk-!-margin-0",
        **{"open": default_open}
    )
