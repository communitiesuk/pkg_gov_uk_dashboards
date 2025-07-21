"""Module containing Enums for jitter symbols.

Contains:
- Symbols from the Plotly graphing library
https://plotly.com/python/marker-style/#custom-marker-symbols
"""

from enum import Enum


class PlotSymbols(Enum):
    """
    From theplotly graphing library: https://plotly.com/python/marker-style/#custom-marker-symbols
    """

    CIRCLE = "circle"
    CROSS = "cross"
    DIAMOND = "diamond"
    HEXAGRAM = "hexagram"
