"""test convert_to_financial_year_ending function"""

from lib.datetime_functions.datetime_functions import convert_to_financial_year_ending


def test_convert_to_financial_year_ending_month_after_april():
    """Test function works as expected with date string where month is after April"""
    expected = "2020"
    actual = convert_to_financial_year_ending("25-10-2019")
    assert actual == expected


def test_convert_to_financial_year_ending_month_before_april():
    """Test function works as expected with date string where month is before April"""
    expected = "2019"
    actual = convert_to_financial_year_ending("25-02-2019")
    assert actual == expected


def test_convert_to_financial_year_ending_month_is_april():
    """Test function works as expected with date string where month is April"""
    expected = "2018"
    actual = convert_to_financial_year_ending("25-04-2017")
    assert actual == expected
