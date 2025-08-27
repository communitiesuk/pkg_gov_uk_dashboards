"""test_barchart_data"""

import polars as pl
from gov_uk_dashboards.components.plotly.stacked_barchart import StackedBarChart


def validate_barchart_instance(
    barchart_instance: StackedBarChart,
    identifier_name: str | None = None,
    identifier_value: str | None = None,
    context_msg: str = "",
):
    """
    Helper function to validate a barchart_instance dataframe.

    Args:
        barchart_instance: The barchart object with dataframe and metadata
        identifier_name: Optional label for the entity (e.g., 'LA', 'School')
        identifier_value: Optional value of the entity (e.g., 'Manchester', 'ABC123')
        context_msg: Additional context for assertion messages
    """
    barchart_df = barchart_instance.df
    trace_name_list = barchart_instance.trace_name_list
    trace_name_column = barchart_instance.trace_name_column
    x_axis_column = barchart_instance.x_axis_column
    unique_x_axis_values = set(barchart_df[x_axis_column].unique())

    # Build label for error messages
    if identifier_name and identifier_value:
        entity_label = f"{identifier_name}={identifier_value}"
    elif identifier_value:
        entity_label = str(identifier_value)
    elif identifier_name:
        entity_label = identifier_name
    else:
        entity_label = "entity"

    for trace_name in trace_name_list:
        if not trace_name_column:
            df = barchart_df
        else:
            trace_values = barchart_df[trace_name_column].unique().to_list()
            if trace_name not in trace_values:
                raise AssertionError(
                    f"Trace '{trace_name}' expected in column '{trace_name_column}' "
                    f"but not found for {entity_label}. {context_msg}"
                )
            df = barchart_df.filter(pl.col(trace_name_column) == trace_name)

        # Check trace has at least one row
        assert (
            df.height > 0
        ), f"Trace '{trace_name}' has no data for {entity_label}. {context_msg}"

        # Check trace has all required x-axis values
        x_values_for_trace = set(df[x_axis_column].unique())
        assert x_values_for_trace == unique_x_axis_values, (
            f"{unique_x_axis_values - x_values_for_trace} missing for trace '{trace_name}' in "
            f"{entity_label}. {context_msg}"
        )

        # Check x-axis uniqueness
        assert df[x_axis_column].is_unique().to_numpy()[0], (
            f"x_axis-column '{x_axis_column}' for {entity_label}, "
            f"trace '{trace_name}' contains duplicate values in {trace_name_column}. {context_msg}"
        )
