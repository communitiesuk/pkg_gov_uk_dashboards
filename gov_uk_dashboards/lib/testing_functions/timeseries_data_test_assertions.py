"""Assertion functions for use in timeseries data tests"""

import polars as pl


def timeseries_df_contains_unique_x_values_per_trace(timeseries_instance, **context):
    """
    Validates that the x_axis_column has unique values per trace.

    Args:
        timeseries_instance (TimeSeriesChart):
            Object with filtered_df, trace_name_list, trace_name_column,
            and x_axis_column attributes.
        **context: Arbitrary key-value pairs (e.g., la="LA1", expenditure_area="Health").
            These will be included in the assertion message if provided.
    """
    timeseries_df = timeseries_instance.filtered_df
    trace_name_list = timeseries_instance.trace_name_list
    trace_name_column = timeseries_instance.trace_name_column
    x_axis_column = timeseries_instance.x_axis_column
    context_str = ", ".join(f"{k}={v}" for k, v in context.items())
    for trace_name in trace_name_list:
        if not trace_name_column:
            df = timeseries_df
        else:
            df = timeseries_df.filter(pl.col(trace_name_column) == trace_name)
        assert (
            df[x_axis_column].is_unique().to_numpy()[0]
        ), f"x_axis-column: {x_axis_column} contains duplicate values. For {context_str}"
