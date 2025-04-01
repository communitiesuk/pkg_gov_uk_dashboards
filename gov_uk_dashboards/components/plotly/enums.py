"""Classes to be used for defined enums and type structures"""

from enum import Enum
from typing import TypedDict


class XAxisFormat(Enum):
    """Enum for date format on x axis"""

    YEAR = "year"
    MONTH_YEAR = "month_year"
    MONTH_YEAR_MONTHLY_DATA = "month_year_monthly_data"
    FINANCIAL_QUARTER = "financial_quarter"


class TitleDataStructure(TypedDict):
    """A TypedDict representing the structure of title_data"""

    MAIN_TITLE: str
    SUBTITLE: str


class HoverDataStructure(TypedDict):
    """A TypedDict representing the structure of hover_data"""

    CUSTOM_DATA: list[str]
    HOVER_TEXT_HEADERS: list[str]


class HoverDataByTrace(TypedDict):
    """A TypedDict representing hover_data organized by tracename"""

    tracename: dict[
        str, HoverDataStructure
    ]  # Each tracename maps to a HoverDataStructure
