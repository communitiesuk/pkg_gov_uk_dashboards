"""test convert_to_date_range function"""

from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_to_date_range,
)


def test_convert_to_date_range_function():
    """Test convert_to_date_range function performs as expected"""
    date_str = "2023-10-15"
    expected = "Oct 2022 to Oct 2023"
    actual = convert_to_date_range(date_str)
    assert actual == expected


def test_convert_to_date_range_function_june():
    """Test convert_to_date_range function performs as expected when month is june"""
    date_str = "2023-06-15"
    expected = "Jun 2022 to Jun 2023"
    actual = convert_to_date_range(date_str)
    assert actual == expected


def test_convert_to_date_range_function_july():
    """Test convert_to_date_range function performs as expected when month is july"""
    date_str = "2023-07-15"
    expected = "Jul 2022 to Jul 2023"
    actual = convert_to_date_range(date_str)
    assert actual == expected
