"""Tests for leap year logic for _get_a_previous_date"""

from gov_uk_dashboards.components.dash.context_card import get_a_previous_date


def test_leap_year_logic_for_get_a_previous_date():
    """A test to check the leap year logic used in the get_a_previous_date"""
    # Test a basic date
    non_leap_year_to_non_leap_year_result = get_a_previous_date(
        "2024-03-01", "previous"
    )
    non_leap_year_to_non_leap_year_expected = "2023-03-01"

    assert (
        non_leap_year_to_non_leap_year_result == non_leap_year_to_non_leap_year_expected
    )

    # Test leap year to non leap year
    leap_to_non_leap_year_result = get_a_previous_date("2024-02-29", "previous")
    leap_to_non_leap_year_expected = "2023-02-28"

    assert leap_to_non_leap_year_result == leap_to_non_leap_year_expected

    # Test non leap year to leap year
    non_leap_year_to_leap_year_result = get_a_previous_date("2025-03-01", "previous")
    non_leap_year_to_leap_year_expected = "2024-03-01"

    assert non_leap_year_to_leap_year_result == non_leap_year_to_leap_year_expected

    non_leap_year_to_leap_year_feb_result = get_a_previous_date(
        "2025-02-28", "previous"
    )
    non_leap_year_to_leap_year_expected = "2024-02-29"

    assert non_leap_year_to_leap_year_feb_result == non_leap_year_to_leap_year_expected
