"""Tests for get_data_for_context_card functions"""

import polars as pl
import pytest
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_date_string_to_text_string,
)
from gov_uk_dashboards.constants import (
    MEASURE,
    METRIC_VALUE,
    YEAR_END,
    PERIOD_END,
    DATE_VALID,
    VALUE,
    LATEST_YEAR,
    PREVIOUS_YEAR,
    TWENTY_NINETEEN,
)
from gov_uk_dashboards.components.dash.context_card import (
    get_data_for_context_card,
    get_latest_data_for_year,
)


def test_get_data_for_context_card():
    """Test get_data_for_context_card function"""
    test_df = pl.DataFrame(
        {
            MEASURE: ["measure1", "measure1", "measure1"],
            "Area_Code": ["E92000001", "E92000001", "E92000001"],
            "Value": [10000.0,15000.0,16000.0],
            "twenty_nineteen_value": [13000.0,13000.0,13000.0],
            "Date valid": ["2023-12-31","2022-12-31","2020-12-31"],
            "value_unrounded": [10001,15001,16001],
            "Percentage change from prev year": [None,None,None],
            "Percentage change from two prev year": [None,None,None],
            "Financial year": ["2023-24","2022-23","2020-21"],
            "Date submitted": ["2025-07-01T20:07:17.000","2025-07-01T20:07:17.000","2025-07-01T20:07:17.000"],
        }
    )

    expected = {
        LATEST_YEAR: {
            YEAR_END: "Dec 2023",
            METRIC_VALUE: 10000.0,
            DATE_VALID: "2023-12-31",
        },
        PREVIOUS_YEAR: {
            YEAR_END: "Dec 2022",
            METRIC_VALUE: 15000.0,
            DATE_VALID: "2022-12-31",
        },
        TWENTY_NINETEEN: {
            METRIC_VALUE: 13000.0,
        },
    }

    result = get_data_for_context_card("measure1", test_df)

    assert result == expected


SAMPLE_DATA = pl.DataFrame(
    {
        DATE_VALID: ["2023-03-01", "2023-06-01", "2024-03-01"],
        PERIOD_END: ["2023-03-31", "2023-06-30", "2024-03-31"],
        VALUE: [100, 200, 150],
    }
)


def test_get_latest_data_for_year():
    """Testing _get_latest_data_for_year function with the year 2023"""

    result = get_latest_data_for_year(SAMPLE_DATA, "2023-06-01", VALUE, True)
    expected_period_end = convert_date_string_to_text_string(
        "2023-06-30", include_day_of_month=False
    )
    assert result == {
        YEAR_END: expected_period_end,
        METRIC_VALUE: 200,
        DATE_VALID: "2023-06-01",
    }


def test_no_data_for_year():
    """Testing the _get_latest_data_for_year function with a year not present
    in the DataFrame ("2025-26")"""
    with pytest.raises(ValueError) as excinfo:
        get_latest_data_for_year(SAMPLE_DATA, "2025-26", VALUE, True)
    assert str(excinfo.value) == "No data found for the date: 2025-26"
