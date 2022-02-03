"""Dash HTML components that allow the user to select options from a pre-determined list"""
from dash import html, dcc


def dropdown(label, options, selected, element_id, **dropdown_properties):
    """A simple Dash Dropdown list.  Must have a value selected."""
    return html.Div(
        [
            html.Label(
                label,
                className="govuk-label",
                htmlFor=element_id,
            ),
            dcc.Dropdown(
                id=element_id,
                options=options,
                value=selected,
                clearable=False,
                **dropdown_properties
            ),
        ],
        className="govuk-form-group govuk-!-padding-0 govuk-!-margin-0 govuk-!-padding-right-3",
        style={
            "minWidth": "35%",
            "flexGrow": "1",
        },
    )


def clearable_dropdown(element_id, label, options, selected):
    """A simple Dash Dropdown list.  Does not have to have a value selected"""
    return (
        html.Div(
            [
                html.Label(
                    label,
                    className="govuk-label",
                    htmlFor=element_id,
                ),
                dcc.Dropdown(
                    id=element_id,
                    options=options,
                    value=selected,
                    clearable=True,
                ),
            ],
            className="govuk-form-group govuk-!-padding-0 govuk-!-margin-0 govuk-!-padding-right-3",
            style={
                "minWidth": "25%",
                "flexGrow": "1",
                "borderRight": "1px solid #b1b4b6",
            },
        ),
    )
