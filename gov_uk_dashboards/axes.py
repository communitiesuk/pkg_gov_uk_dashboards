"""Module containing functions related to graph axes.

Contains:
- calc_axis_range: Return a range for a column of a dataframe so the derived
    axis is at the origin or the lowest negative value in the column, whichever
    is lower.
"""
from math import floor, ceil
import pandas as pd


def calc_axis_range(dataframe: pd.DataFrame, column: str) -> list:
    """Show origin on dashboard axis or negative value for numeric type column"""
    range_multiplier = 1.01
    axis_range = [
        floor(dataframe[[column]].min().iloc[0] * range_multiplier),
        ceil(dataframe[[column]].max().iloc[0] * range_multiplier),
    ]
    if axis_range[0] < 0:
        return axis_range
    return [0, axis_range[1]]
