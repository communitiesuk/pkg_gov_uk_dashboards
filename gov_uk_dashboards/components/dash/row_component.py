"""row_component"""

from dash import html


def row_component(cards, horizontal_scroll=None, amend_style=None):
    """
    Creates a horizontal row used to contain cards.
    The card and row_component work together to create a
    layout that stretches and shrinks when the user changes the size of the window,
    or accesses the dashboard from a mobile device.

    See https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout for more information.
    """
    style = {"alignItems": "stretch"} | (amend_style if amend_style else {})

    if horizontal_scroll:
        style["overflow-x"] = "auto"

    return html.Div(cards, className="govuk-list card-container", style=style)
