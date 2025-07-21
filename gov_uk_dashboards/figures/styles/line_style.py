"""LineStyle dataclass"""

from dataclasses import dataclass
from typing import Union
from ..enums.dash_patterns import DashPatterns


@dataclass
class LineStyle:
    """
    Dataclass containing information on how to style a line on a line chart.

    Attributes:
        color (str): The colour of a line, represented by a hex colour code.
        dash_pattern (str): Whether the line should be solid, dash, dot, etc.
            Use the enum in figures.enums.DashPatterns for valid values.
    """

    color: str
    dash_pattern: Union[DashPatterns, str]
