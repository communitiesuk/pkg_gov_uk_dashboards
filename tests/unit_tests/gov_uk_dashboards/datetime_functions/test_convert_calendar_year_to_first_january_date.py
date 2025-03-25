"""test convert_calendar_year_to_first_january_date"""

from datetime import datetime
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_calendar_year_to_first_january_date,
)


def test_convert_financial_year_to_date():
    """test convert_calendar_year_to_first_january_date"""
    actual = convert_calendar_year_to_first_january_date("2018")
    assert actual == datetime(2018, 1, 1)
