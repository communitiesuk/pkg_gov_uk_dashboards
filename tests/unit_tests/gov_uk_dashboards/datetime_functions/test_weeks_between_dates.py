"""Tests for weeks_between_dates"""

from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    weeks_between_dates,
)


def test_weeks_between_dates():
    """Test weeks_between_dates performas as expected."""
    assert weeks_between_dates("2023-01-12", "2024-01-12") == 365 / 7
    assert weeks_between_dates("2024-01-01", "2024-01-31") == 30 / 7
