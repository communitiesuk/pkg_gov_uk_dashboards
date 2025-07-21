"""warning_text"""

from dash import html


def warning_text(text: str, style: dict = None) -> html.Div:
    """
    Return Gov UK Design component warning text component, ! with text.
    """
    text = html.Div(
        format_text(text),
        className="govuk-warning-text",
        style=style,
    )
    return text


def format_text(text: str) -> list:
    """
    Formats a segment of text.
    If the tag <b> is found the process transform the text in bold
    If the tag <a> is found the process transform the text in link

    Args:
        text (str): The text to be formatted.

    Returns:
        list of components.
    """
    formatted_text = []
    formatted_text.append(
        html.Span(["Warning"], className="govuk-warning-text__assistive"),
    )
    segments = text.split("$")
    for segment in segments:
        if segment.startswith("<b>"):
            raw_text = segment.replace("<b>", "")
            formatted_text.append(html.B(raw_text))
        elif segment.startswith("<a>"):
            info_link = segment.replace("<a>", "")
            link_description = info_link.split("|")[0]
            link = info_link.split("|")[1]
            formatted_text.append(
                html.A(
                    link_description,
                    href=link,
                )
            )
        else:
            formatted_text.append(segment)

    return [
        html.Span(
            ["!"], className="govuk-warning-text__icon", **{"aria-hidden": "true"}
        ),
        html.Strong(
            formatted_text,
            className="govuk-warning-text__text",
        ),
    ]
