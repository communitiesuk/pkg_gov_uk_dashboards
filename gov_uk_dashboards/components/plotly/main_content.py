"""main_content"""
from dash import html


def main_content(children):
    """
    Wrapper for the main content of the dashboard, containing visualisations.

    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/main

    Using semantic HTML elements makes it easier for users with accessibility issues to
    interpret webpages using assistive devices.

    See https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML for more guidance.
    """
    return html.Main(children, className="main", id="main-content", role="main")
