"""time_series_and_stacked_barchart_helper_functions"""

import math
from typing import List
import plotly
import polars as pl


def format_yaxes(
    fig: plotly.graph_objects.Figure,
    stacked: bool,
    df: pl.DataFrame,
    x_axis_column: str,
    y_axis_column: str,
):
    """
    Format the y-axis of a Plotly figure with “nice” tick values and range.

    Args:
        fig (plotly.graph_objects.Figure): The Plotly figure to update.
        stacked (bool): Whether the data is stacked; affects how the max y value is computed.
        df (pl.DataFrame): Polars DataFrame containing the data.
        x_axis_column (str): Name of the column to group by if stacked.
        y_axis_column (str): Name of the column to use for the y-axis values.

    Behavior:
        - Computes “nice” y-axis tick values using `_get_y_axis_ticks`.
        - Sets the axis range to slightly above the top tick for visual padding.
        - Formats tick labels with commas for readability.
        - Enables gridlines and sets the y-axis to start at zero.
    """
    ticks = compute_y_axis_ticks(stacked, df, x_axis_column, y_axis_column)

    max_y_range = ticks[-2] + 2 * (ticks[-1] - ticks[-2]) / 3
    if ticks[0] == 0:
        min_y_range = 0
    else:
        min_y_range = min(ticks[0] - 2 * (ticks[1] - ticks[0]) / 3, 0)

    fig.update_yaxes(
        rangemode="tozero",
        showgrid=True,
        range=[min_y_range, max_y_range],
        tickvals=ticks,
        ticktext=[f"{v:,}" for v in ticks],
    )


def generate_human_readable_yticks(
    y_min: float, y_max: float, max_ticks: int = 10
) -> List[float]:
    """
    Generates human readable ticks for yaxis.

    This function computes evenly spaced ticks that are rounded to
    multiples of 1, 2, or 5 × 10^n, ensuring that the tick labels are
    easy to read. It also limits the total number of ticks to `max_ticks`.

    Args:
        y_min (float): Minimum value of the axis.
        y_max (float): Maximum value of the axis.
        max_ticks (int, optional): Maximum number of tick values. Defaults to 10.

    Returns:
        List[float]: A list of tick values, rounded and evenly spaced.

    Example:
        >>> generate_human_readable_ticks(0, 502060)
        [0, 100000, 200000, 300000, 400000, 500000, 600000]
    """

    raw_step = (y_max - y_min) / (max_ticks - 1)

    magnitude = 10 ** math.floor(math.log10(raw_step))
    residual = raw_step / magnitude

    if residual <= 1:
        nice_step = 1 * magnitude
    elif residual <= 2:
        nice_step = 2 * magnitude
    elif residual <= 5:
        nice_step = 5 * magnitude
    else:
        nice_step = 10 * magnitude

    nice_min = math.floor(y_min / nice_step) * nice_step
    nice_max = math.ceil(y_max / nice_step) * nice_step

    ticks = []
    current = nice_min
    while current <= nice_max + 1e-8:
        ticks.append(round(current, 10))
        current += nice_step

    if len(ticks) > max_ticks:
        step = len(ticks) / (max_ticks - 1)
        ticks = [ticks[round(i * step)] for i in range(max_ticks)]

    return ticks


def compute_y_axis_ticks(
    stacked: bool, df: pl.DataFrame, x_axis_column: str, y_axis_column: str
) -> List[float]:
    """Compute human-readable y-axis tick values for a chart.

    This function calculates the maximum y value from the data, applies
    optional stacking if needed, and generates “nice” tick values
    suitable for chart axes. It ensures that the top tick is above the
    maximum data value and rounds ticks to human-friendly intervals.

    Args:
        stacked (bool): Whether to sum values per x-axis group before finding the max.
        df (pl.DataFrame): Polars DataFrame containing the data.
        x_axis_column (str): Name of the column to group by if stacked.
        y_axis_column (str): Name of the column containing y-axis values.

    Returns:
        List[float]: A list of “nice” tick values for the y-axis.

    Example:
        >>> compute_y_axis_ticks(False, df, "date", "sales")
        [0, 100000, 200000, 300000, 400000, 500000, 600000]"""
    if stacked:
        df_positive = df.filter(pl.col(y_axis_column) > 0)
        df_negative = df.filter(pl.col(y_axis_column) < 0)

        # Sum positives per x-axis group
        largest_y_value = (
            df_positive.group_by(x_axis_column)
            .agg(pl.col(y_axis_column).sum())
            .get_column(y_axis_column)
            .max()
            if df_positive.height > 0
            else 0
        )

        # Sum negatives per x-axis group
        smallest_y_value = (
            df_negative.group_by(x_axis_column)
            .agg(pl.col(y_axis_column).sum())
            .get_column(y_axis_column)
            .min()
            if df_negative.height > 0
            else 0
        )

    else:
        largest_y_value = df[y_axis_column].max()
        smallest_y_value = df[y_axis_column].min()

    # Add padding
    y_axis_max = largest_y_value * 1.3
    y_axis_min = min(smallest_y_value * 1.3, 0)

    ticks = generate_human_readable_yticks(y_axis_min, y_axis_max)
    return ticks
