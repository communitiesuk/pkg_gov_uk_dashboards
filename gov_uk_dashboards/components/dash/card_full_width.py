"""card_full_width"""

from dash import html


def card_full_width(children):
    """
    Apply CSS classes and styles to create a card with a grey background
    that fits the full width of its parent container using CSS flexbox.

    See https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout for more information.
    """
    return html.Div(children, className="mini-card", style={"flex": "1 1 100%"})
