"""test convert_date_obj_to_text_string"""

from datetime import datetime
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_date_obj_to_text_string,
)


def test_convert_date_obj_to_text_string_default():
    """test convert_date_obj_to_text_string with default bools"""
    actual = convert_date_obj_to_text_string(datetime(year=2020, month=12, day=25))
    assert actual == "25 Dec 2020"


def test_convert_date_obj_to_text_string_no_day_no_abbrev():
    """test convert_date_obj_to_text_string when no day of month is wanted
    and full month word is wanted"""
    actual = convert_date_obj_to_text_string(
        datetime(year=2020, month=12, day=25),
        include_day_of_month=False,
        abbreviate_month=False,
        include_year=True,
    )
    assert actual == "December 2020"


def test_convert_date_obj_to_text_string_no_year():
    """test convert_date_obj_to_text_string when no year is wanted"""
    actual = convert_date_obj_to_text_string(
        datetime(year=2020, month=12, day=25),
        include_day_of_month=True,
        abbreviate_month=True,
        include_year=False,
    )
    assert actual == "25 Dec"


def test_convert_date_obj_to_text_string_abbreviate_month_true_but_month_june():
    """test convert_date_obj_to_text_string when abbreviate_month is True but month is june"""
    actual = convert_date_obj_to_text_string(
        datetime(year=2020, month=6, day=25),
        include_day_of_month=True,
        abbreviate_month=True,
        include_year=False,
    )
    assert actual == "25 June"


def test_convert_date_obj_to_text_string_abbreviate_month_true_but_month_july():
    """test convert_date_obj_to_text_string when abbreviate_month is True but month is july"""
    actual = convert_date_obj_to_text_string(
        datetime(year=2020, month=7, day=25),
        include_day_of_month=True,
        abbreviate_month=True,
        include_year=False,
    )
    assert actual == "25 July"
