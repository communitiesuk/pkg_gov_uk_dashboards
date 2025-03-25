"""Tests for date_string_is_month_to_month_year_range"""

from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    date_string_is_month_to_month_year_range,
)


def test_valid_format():
    """Test strings with the correct format"""
    assert date_string_is_month_to_month_year_range("January to February 2024") is True
    assert date_string_is_month_to_month_year_range("January to January 2024") is True


def test_invalid_format_missing_to():
    """Test strings missing the "to" keyword"""
    assert date_string_is_month_to_month_year_range("January February 2024") is False


def test_invalid_format_incorrect_month_name():
    """Test strings with incorrect month names"""
    assert (
        date_string_is_month_to_month_year_range("Jannuary to February 2024") is False
    )


def test_invalid_year_format():
    """Test strings with incorrect year formats"""
    assert (
        date_string_is_month_to_month_year_range("January to February 24") is False
    )  # Two-digit year
    assert (
        date_string_is_month_to_month_year_range("January to February 20245") is False
    )  # Five-digit year
    assert (
        date_string_is_month_to_month_year_range("January to February") is False
    )  # No year


def test_case_sensitivity():
    """Test strings with various capitalizations"""
    assert date_string_is_month_to_month_year_range("january to february 2024") is False
    assert date_string_is_month_to_month_year_range("January to february 2024") is False
    assert date_string_is_month_to_month_year_range("JANUARY to FEBRUARY 2024") is False


def test_non_month_words():
    """Test strings with non-month words"""
    assert date_string_is_month_to_month_year_range("Week to Month 2024") is False
    assert date_string_is_month_to_month_year_range("June to Holiday 2023") is False


def test_additional_text():
    """Test strings with extra text before or after"""
    assert (
        date_string_is_month_to_month_year_range("From January to February 2024")
        is False
    )
    assert (
        date_string_is_month_to_month_year_range("January to February 2024 onward")
        is False
    )
