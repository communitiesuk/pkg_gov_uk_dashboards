"""test format_year_month_to_month_year"""

import pytest
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    format_year_month_to_month_year,
)


def test_format_year_month_to_month_year_with_valid_date():
    """test format_year_month_to_month_year when valid string provided"""
    actual = format_year_month_to_month_year("2020-12")
    assert actual == "December 2020"


def test_format_year_month_to_month_year_with_no_date():
    """test format_year_month_to_month_year when valid string provided"""
    with pytest.raises(ValueError, match="No date_string provided"):
        format_year_month_to_month_year("")
