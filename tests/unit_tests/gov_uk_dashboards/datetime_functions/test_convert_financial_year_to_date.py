"""test convert_financial_year_to_date"""

from datetime import datetime
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import convert_financial_year_to_date


def test_convert_financial_year_to_date():
    """test convert_financial_year_to_date with default arg"""
    actual = convert_financial_year_to_date("2018-19")
    assert actual == datetime(2018, 4, 1)


def test_convert_financial_year_to_date_non_default_arg():
    """test convert_financial_year_to_date with non default arg"""
    actual = convert_financial_year_to_date("2018-19", use_start_date=False)
    assert actual == datetime(2019, 3, 31)
