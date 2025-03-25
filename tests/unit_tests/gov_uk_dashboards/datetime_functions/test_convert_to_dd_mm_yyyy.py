"""test convert_to_dd_mm_yyyy function"""

from gov_uk_dashboards.lib.datetime_functions.datetime_functions import convert_to_dd_mm_yyyy


def test_convert_to_dd_mm_yyyy_with_date_string():
    """Test function works as expected with date string"""
    actual = convert_to_dd_mm_yyyy("2019-05-23")
    expected = "23-05-2019"
    assert actual == expected


def test_convert_to_dd_mm_yyyy_with_datetime_string():
    """Test function works as expected with datetime string"""
    actual = convert_to_dd_mm_yyyy("2019-05-23 00:00:00.000", True)
    expected = "23-05-2019"
    assert actual == expected
