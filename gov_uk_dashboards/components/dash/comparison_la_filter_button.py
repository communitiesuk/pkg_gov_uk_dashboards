"""comparison_la_filter_button"""

from dash import html


def add_filter_button(style: dict, id_string: str):
    """
    Return a 'Compare to additional authority' button which is aligned to the right

    Args:
    style (dict): The CSS styling to add to the button.
    id_string (str): ID for the button.
    """
    return html.Div(
        [
            html.Button(
                "Compare to additional authority",
                id=id_string,
                n_clicks=0,
                className="govuk-button govuk-button--secondary comparison-button-background",
            ),
        ],
        className="govuk-button-group",
        style=style,
    )
