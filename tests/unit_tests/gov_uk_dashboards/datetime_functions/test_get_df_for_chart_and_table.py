"""test _get_df_for_chart_and_table"""

import polars as pl
from constants import (
    AREA_CODE,
    BY_UNIT_SIZE,
    DATE_VALID,
    LARGE,
    MEASURE,
    MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT,
    MEDIUM,
    SMALL,
    TIME_TAKEN,
    TWENTY_NINETEEN_VALUE,
    UNIT_SIZE,
)
from dashboards.time_taken_to_develop import _get_df_for_chart_and_table


def test_get_df_for_chart_and_table(mocker):
    """Test get_df_for_chart_and_table returns expected value."""
    mock_get_new_developments_time_df = mocker.patch(
        "dashboards.time_taken_to_develop.get_new_developments_time_df"
    )
    mock_get_new_developments_time_df.return_value = pl.DataFrame(
        {
            MEASURE: [
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT,
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT + BY_UNIT_SIZE + LARGE,
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT
                + BY_UNIT_SIZE
                + MEDIUM,
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT + BY_UNIT_SIZE + SMALL,
            ],
            AREA_CODE: ["E92000001"] * 4,
            TIME_TAKEN: [
                "100 weeks and 3 days",
                "12 weeks and 5 days",
                "22 weeks and 5 days",
                "35 weeks and 5 days",
            ],
            TWENTY_NINETEEN_VALUE: [
                "86 weeks and 1 days",
                "82 weeks and 3 days",
                "87 weeks and 5 days",
                "65 weeks and 4 days",
            ],
            DATE_VALID: [
                "2022-10-18",
                "2023-09-12",
                "2023-10-12",
                "2021-11-15",
            ],
            UNIT_SIZE: [
                None,
                "Large (500+ units)",
                "Medium (101 - 499 units)",
                "Small (1 - 100 units)",
            ],
        }
    )
    actual = _get_df_for_chart_and_table(
        MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT
    )
    expected = pl.DataFrame(
        {
            MEASURE: [
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT + BY_UNIT_SIZE + SMALL,
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT + BY_UNIT_SIZE + LARGE,
                MEDIAN_TIME_APPLICATION_TO_COMPLETED_DEVELOPMENT
                + BY_UNIT_SIZE
                + MEDIUM,
            ],
            TIME_TAKEN: [
                "35 weeks and 5 days",
                "12 weeks and 5 days",
                "22 weeks and 5 days",
            ],
            DATE_VALID: ["2021-11-15", "2023-09-12", "2023-10-12"],
            UNIT_SIZE: [
                "Small (1 - 100 units)",
                "Large (500+ units)",
                "Medium (101 - 499 units)",
            ],
        }
    )

    assert actual.equals(expected)
