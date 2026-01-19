"""Test _get_df_list_for_time_series returns correct list of dataframes"""

import pytest
import polars as pl
from gov_uk_dashboards.constants import DATE_VALID, MEASURE, UNIT_SIZE, VALUE
from gov_uk_dashboards.components.plotly.time_series_chart import TimeSeriesChart

DF_MEASURE1_SMALL = pl.DataFrame(
    {
        MEASURE: ["Measure 1 Small"] * 3,
        VALUE: [35.5, 30.5, 32.5],
        DATE_VALID: ["2021-11-15", "2021-12-15", "2023-10-12"],
        UNIT_SIZE: ["Small"] * 3,
    }
)
DF_MEASURE1_MEDIUM = pl.DataFrame(
    {
        MEASURE: ["Measure 1 Medium"] * 3,
        VALUE: [26.5, 29.5, 22.5],
        DATE_VALID: ["2021-11-15", "2021-12-15", "2023-10-12"],
        UNIT_SIZE: ["Medium"] * 3,
    }
)
DF_MEASURE1_LARGE = pl.DataFrame(
    {
        MEASURE: ["Measure 1 Large"] * 3,
        VALUE: [16.5, 20.5, 23.5],
        DATE_VALID: ["2021-11-15", "2021-12-15", "2023-10-12"],
        UNIT_SIZE: ["Large"] * 3,
    }
)
DF_MEASURE2_SMALL = pl.DataFrame(
    {
        MEASURE: ["Measure 2 Small"] * 3,
        VALUE: [39.5, 44.5, 55.5],
        DATE_VALID: ["2023-10-12", "2023-11-15", "2023-12-25"],
        UNIT_SIZE: ["Small"] * 3,
    }
)
DF_MEASURE2_MEDIUM = pl.DataFrame(
    {
        MEASURE: ["Measure 2 Medium"] * 3,
        VALUE: [30.5, 45.5, 42.5],
        DATE_VALID: ["2023-10-12", "2023-11-15", "2024-01-15"],
        UNIT_SIZE: ["Medium"] * 3,
    }
)
DF_MEASURE2_LARGE = pl.DataFrame(
    {
        MEASURE: ["Measure 2 Large"] * 3,
        VALUE: [25.5, 40.5, 75.5],
        DATE_VALID: ["2023-10-12", "2023-11-15", "2023-12-25"],
        UNIT_SIZE: ["Large"] * 3,
    }
)
DF_MEASURE1 = pl.concat([DF_MEASURE1_SMALL, DF_MEASURE1_MEDIUM, DF_MEASURE1_LARGE])
DF_MEASURE2 = pl.concat([DF_MEASURE2_SMALL, DF_MEASURE2_MEDIUM, DF_MEASURE2_LARGE])


@pytest.mark.parametrize(
    "df, expected_df_list",
    [
        (
            DF_MEASURE1,
            [DF_MEASURE1_SMALL, DF_MEASURE1_MEDIUM, DF_MEASURE1_LARGE],
        ),
        (
            DF_MEASURE2,
            [DF_MEASURE2_SMALL, DF_MEASURE2_MEDIUM, DF_MEASURE2_LARGE],
        ),
    ],
)
def test_get_df_list_for_time_series_returns_correct_df_list_when_trace_name_column_not_none(
    df, expected_df_list
):
    """test to check _get_df_list_for_time_series returns correct dataframe list when
    trace_name_column is not None."""
    trace_name_list = ["Small", "Medium", "Large"]
    hover_data = {}

    for trace_name in trace_name_list:

        hover_data[trace_name] = {
            "custom_data": [DATE_VALID, VALUE],
            "hover_text_headers": ["header1", "header2"],
        }
    time_series_class = TimeSeriesChart(
        {"main_title": "test", "subtitle": "testsub"},
        VALUE,
        hover_data,
        df,
        trace_name_list,
        trace_name_column=UNIT_SIZE,
    )
    # pylint: disable=protected-access
    actual_df_list = time_series_class._get_df_list_for_time_series()

    assert len(actual_df_list) == len(expected_df_list)
    for actual_df, expected_df in zip(actual_df_list, expected_df_list):
        assert actual_df.equals(expected_df)


def test_get_df_list_for_time_series_returns_correct_df_list_when_trace_name_column_is_none():
    """test to check _get_df_list_for_time_series returns correct dataframe list when
    trace_name_column is None."""
    test_df = pl.DataFrame(
        {
            "Measure": ["Measure1", "Measure2", "Measure3"],
            "Date valid": ["2023-10-12", "2023-11-15", "2023-12-25"],
            "Value": [1, 2, 3],
        }
    )
    trace_name_list = ["trace name"]
    hover_data = {}

    for trace_name in trace_name_list:

        hover_data[trace_name] = {
            "custom_data": ["Date valid", "Measure"],
            "hover_text_headers": ["header1", "header2"],
        }
    time_series_class = TimeSeriesChart(
        {"main_title": "test", "subtitle": "testsub"},
        "Value",
        hover_data,
        test_df,
        trace_name_list,
    )
    # pylint: disable=protected-access
    actual_df_list = time_series_class._get_df_list_for_time_series()
    expected_df_list = [test_df]
    assert len(actual_df_list) == len(expected_df_list)
    for actual_df, expected_df in zip(actual_df_list, expected_df_list):
        assert actual_df.equals(expected_df)
