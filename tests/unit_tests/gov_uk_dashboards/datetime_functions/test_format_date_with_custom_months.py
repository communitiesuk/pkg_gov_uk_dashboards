"""Test format_date_with_custom_months"""

from datetime import date
import pytest
from lib.datetime_functions.datetime_functions import format_date_with_custom_months


@pytest.mark.parametrize(
    "date_object, expected_output",
    [
        (date(2024, 6, 21), "21 June 2024"),
        (date(2024, 7, 21), "21 July 2024"),
        (date(2024, 8, 21), "21 Aug 2024"),
    ],
)
def test_format_date_with_custom_months(date_object, expected_output):
    """Test format_date_with_custom_months performs as expected"""
    assert format_date_with_custom_months(date_object) == expected_output
