"""test convert_to_financial_year function"""

from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_to_financial_year,
)


def test_convert_to_financial_year_month_after_april():
    """Test function works as expected with date string where month is after April"""
    expected = "2019-20"
    actual = convert_to_financial_year("25-10-2019")
    assert actual == expected


def test_convert_to_financial_year_month_before_april():
    """Test function works as expected with date string where month is before April"""
    expected = "2018-19"
    actual = convert_to_financial_year("25-02-2019")
    assert actual == expected


def test_convert_to_financial_year_month_is_april():
    """Test function works as expected with date string where month is April"""
    expected = "2017-18"
    actual = convert_to_financial_year("25-04-2017")
    assert actual == expected
