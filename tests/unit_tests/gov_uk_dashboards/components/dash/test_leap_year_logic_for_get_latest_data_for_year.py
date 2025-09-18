"""Tests for leap year logic for get_latest_data_for_year"""

import pytest
import polars as pl
from gov_uk_dashboards.constants import METRIC_VALUE, DATE_VALID, VALUE
from gov_uk_dashboards.components.dash.context_card import get_latest_data_for_year


@pytest.mark.parametrize(
    "date_of_latest_data, expected_previous_date, expected_value",
    [
        ("2024-02-29", "2023-02-28", 100),
        ("2021-02-28", "2020-02-29", 50),
        ("2025-02-28", "2024-02-29", 250),
        (None, "2023-02-28", 100),
        (None, "2020-02-29", 50),
        (None, "2024-02-29", 250),
    ],
)
def test_leap_year_logic_in_get_latest_data_for_year(
    date_of_latest_data: str, expected_previous_date: str, expected_value: int
) -> bool:
    """Test to check the leap year logic used in the get_latest_data_for_year"""

    df_measure = pl.DataFrame(
        [
            {DATE_VALID: "2023-02-28", VALUE: 100},
            {DATE_VALID: "2024-02-28", VALUE: 150},
            {DATE_VALID: "2024-02-29", VALUE: 250},
            {DATE_VALID: "2025-02-28", VALUE: 250},
            {DATE_VALID: "2022-02-28", VALUE: 50},
            {DATE_VALID: "2020-02-29", VALUE: 50},
        ]
    )

    result = get_latest_data_for_year(
        df_measure=df_measure,
        date=expected_previous_date,
        value_column=VALUE,
        abbreviate_month=True,
        date_of_latest_data=date_of_latest_data,
    )

    assert result[DATE_VALID] == expected_previous_date
    assert result[METRIC_VALUE] == expected_value
