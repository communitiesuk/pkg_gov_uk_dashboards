"""Module containing Enums for jitter symbols.

Contains:
- Symbols from the Plotly graphing library
https://plotly.com/python/marker-style/#:~:text=The%20basic%20symbols%20are%3A%20circle,hash%20%2C%20y%20%2C%20and%20line%20.
"""
from enum import Enum


class PlotSymbols(Enum):
    """
    From theplotly graphing library: https://plotly.com/python/marker-style/#:~:text=The%20basic%20symbols%20are%3A%20circle,hash%20%2C%20y%20%2C%20and%20line%20.
    """

    CIRCLE = "circle"
    CROSS = "cross"
    DIAMOND = "diamond"
    HEXAGRAM = "hexagram"
