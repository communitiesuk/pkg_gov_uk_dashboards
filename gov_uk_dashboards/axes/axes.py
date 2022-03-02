"""Function for calculating the axis range"""
from math import floor, ceil
import pandas as pd


def calc_axis_range(df: pd.DataFrame, column: str) -> list:
    """Show origin on dashboard axis or negative value for numeric type column"""
    range_multiplier = 1.01
    axis_range = [
        floor(df[[column]].min() * range_multiplier),
        ceil(df[[column]].max() * range_multiplier),
    ]
    if axis_range[0] < 0:
        return axis_range
    return [0, axis_range[1]]
