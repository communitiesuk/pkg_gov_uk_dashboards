"""heading components"""

from enum import Enum

from dash import html


class HeadingSizes(str, Enum):
    """Enum class to specify the allowed paragraph sizes"""

    EXTRA_LARGE = "govuk-heading-xl"
    LARGE = "govuk-heading-l"
    MEDIUM = "govuk-heading-m"
    SMALL = "govuk-heading-s"


def heading1(text: str, size: HeadingSizes = HeadingSizes.LARGE) -> html.H1:
    """Return a H1 dash component"""
    heading_id = f"heading1-{"-".join(text.lower())}"
    return html.H1(text, className=size, id=heading_id)


def heading2(text: str, size: HeadingSizes = HeadingSizes.MEDIUM) -> html.H2:
    """Return a H2 dash component"""
    heading_id = f"heading2-{"-".join(text.lower())}"
    return html.H2(text, className=size, id=heading_id)


def heading3(text: str, size: HeadingSizes = HeadingSizes.SMALL) -> html.H3:
    """Return a H3 dash component"""
    heading_id = f"heading3-{"-".join(text.lower())}"
    return html.H3(text, className=size, id=heading_id)
