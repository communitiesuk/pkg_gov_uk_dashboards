import math
import polars as pl


def format_yaxes(fig, stacked, df, x_axis_column, y_axis_column):
    ticks = _get_y_axis_ticks(stacked, df, x_axis_column, y_axis_column)

    max_y_range = ticks[-2] + 2 * (ticks[-1] - ticks[-2]) / 3

    fig.update_yaxes(
        rangemode="tozero",
        showgrid=True,
        range=[0, max_y_range],
        tickvals=ticks,
        ticktext=[f"{v:,}" for v in ticks],  # formatted with commas,
    )


def generate_nice_ticks(y_min, y_max, max_ticks=10):
    """
    Generate "nice" tick values for a numeric axis.
    Args:
        y_min (float): Minimum axis value
        y_max (float): Maximum axis value
        max_ticks (int): Maximum number of ticks
    Returns:
        list: Tick values (floats) that are rounded and evenly spaced
    """

    # Step 1: compute raw step
    raw_step = (y_max - y_min) / (max_ticks - 1)

    # Step 2: round step to nearest 1, 2, 5 * 10^n
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

    # Step 3: compute nice min and max ticks
    nice_min = math.floor(y_min / nice_step) * nice_step
    nice_max = math.ceil(y_max / nice_step) * nice_step

    # Step 4: generate ticks
    ticks = []
    current = nice_min
    while current <= nice_max + 1e-8:  # small epsilon for floating point
        ticks.append(round(current, 10))
        current += nice_step

    # Step 5: limit number of ticks
    if len(ticks) > max_ticks:
        # pick evenly spaced subset including first and last
        step = len(ticks) / (max_ticks - 1)
        ticks = [ticks[round(i * step)] for i in range(max_ticks)]

    return ticks


def _get_y_axis_ticks(stacked, df, x_axis_column, y_axis_column):
    """Get the y axis range maximum value to ensure there is an axis label greater than the
    maximum y value."""
    if stacked:
        largest_y_value = (
            df.group_by(x_axis_column)  # group by date
            .agg(pl.col(y_axis_column).sum())  # total per date
            .select(pl.col(y_axis_column).max())  # largest daily total
            .item()  # extract scalar
        )
    else:
        largest_y_value = df[y_axis_column].max()
    y_axis_max = largest_y_value + (0.3 * largest_y_value)

    # Generate nice ticks
    ticks = generate_nice_ticks(0, y_axis_max)

    return ticks
