from enum import Enum
from dash import html


class ParagraphSizes(str, Enum):
    LEAD = "govuk-body-l"
    DEFAULT = "govuk-body"
    SMALL = "govuk-body-s"


def paragraph(text: str, size: ParagraphSizes = ParagraphSizes.DEFAULT) -> html.P:
    if size not in list(ParagraphSizes):
        raise ValueError(
            f"Size {size} is not a valid paragraph size (use ParagraphSize enum)."
        )

    return html.P(
        text,
        className=size,
    )
