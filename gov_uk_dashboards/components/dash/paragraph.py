"""paragraph component"""

from enum import Enum
from typing import Union

from dash import html


class ParagraphSizes(str, Enum):
    """Enum class to specify the allowed paragraph sizes"""

    LEAD = "govuk-body-l"
    DEFAULT = "govuk-body"
    SMALL = "govuk-body-s"


def paragraph(
    children: Union[str, list], size: ParagraphSizes = ParagraphSizes.DEFAULT
) -> html.P:
    """
    Create a <p> Html component with the children provided

    Args:
        children (DataFrame): The children to render inside the dash paragraph component.
        size (str, list): The size of the text that this paragraph will display.
            Defaults to DEFAULT.

    Returns:
        html.P: The dash HTML object for a paragraph.

    Raises:
        ValueError: If the paragraph size supplied is not a valid size.
    """
    if size not in list(ParagraphSizes):
        raise ValueError(
            f"Size {size} is not a valid paragraph size (use ParagraphSize enum)."
        )

    return html.P(
        children,
        className=size,
    )
