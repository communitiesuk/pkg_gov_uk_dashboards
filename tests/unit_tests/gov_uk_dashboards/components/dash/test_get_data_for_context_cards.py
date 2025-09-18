"""Tests for get_data_for_context_card functions"""

import polars as pl
import pytest
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_date_string_to_text_string,
)
from gov_uk_dashboards.constants import (
    PLANNING_APPLICATIONS_GRANTED,
    METRIC_VALUE,
    YEAR_END,
    PERIOD_END,
    DATE_VALID,
    VALUE,
    LATEST_YEAR,
    PREVIOUS_YEAR,
    TWENTY_NINETEEN,
)
from lib.absolute_path import absolute_path

from lib.get_data_for_context_cards import (
    get_data_for_context_card,
    get_latest_data_for_year,
)


def test_get_data_for_context_card():
    """Test get_data_for_context_card function"""
    test_df = pl.read_csv(
        absolute_path("tests/data/housing/housing_supply_summary.csv")
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

    result = get_data_for_context_card(PLANNING_APPLICATIONS_GRANTED, test_df)

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
