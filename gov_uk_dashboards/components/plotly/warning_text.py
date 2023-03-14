"""warning_text"""
from dash import html


def warning_text(text: str):
    """
    Return Gov UK Design component warning text component, ! with text.
    """
    text = html.Div(
        [
            html.Span(
                ["!"], className="govuk-warning-text__icon", **{"aria-hidden": "true"}
            ),
            html.Strong(
                [
                    html.Span(["Warning"], className="govuk-warning-text__assistive"),
                    text,
                ],
                className="govuk-warning-text__text",
            ),
        ],
        className="govuk-warning-text",
    )
    return text
