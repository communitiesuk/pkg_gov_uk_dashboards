"""Tests for convert_days_to_weeks_and_days"""

import pytest
from gov_uk_dashboards.components.dash.context_card import (
    convert_days_to_weeks_and_days,
)


@pytest.mark.parametrize(
    "input_int, expected, value_error",
    [
        (25, "3 weeks and 4 days", False),
        (8, "1 week and 1 day", False),
        (15, "2 weeks and 1 day", False),
        (5, "0 weeks and 5 days", False),
        (6.0, "total_days must be an int", True),
    ],
)
def test_convert_days_to_weeks_and_days_returns_correct_content(
    input_int, expected, value_error
):
    """Test convert_days_to_weeks_and_days returns correct content"""
    if value_error is True:
        with pytest.raises(ValueError, match=expected):
            convert_days_to_weeks_and_days(input_int)  # Expecting an exception
    else:
        actual = convert_days_to_weeks_and_days(input_int)
        assert actual == expected
