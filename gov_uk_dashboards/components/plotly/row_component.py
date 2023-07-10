"""row_component"""
from dash import html


def row_component(cards, horizontal_scroll=None):
    """
    Creates a horizontal row used to contain cards.
    The card and row_component work together to create a
    layout that stretches and shrinks when the user changes the size of the window,
    or accesses the dashboard from a mobile device.

    See https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout for more information.
    """
    style = {"alignItems": "stretch"}
    if horizontal_scroll:
        style["overflow-x"] = "auto"

    return html.Div(cards, className="govuk-list card-container", style=style)
