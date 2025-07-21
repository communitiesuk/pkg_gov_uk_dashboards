"""DashPatterns enum"""

from enum import Enum


class DashPatterns(str, Enum):
    """
    Sets out valid dash patterns used by plotly/plotly express.
    """

    SOLID = "solid"
    DOT = "dot"
    DASH = "dash"
    LONG_DASH = "longdash"
    DASH_DOT = "dashdot"
    LONG_DASH_DOT = "longdashdot"
