"""test convert_date_string_to_text_string"""

from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_date_string_to_text_string,
)


def test_convert_date_string_to_text_string_abbreviate_month_include_year():
    """test convert_date_string_to_text_string abbreviates month and includes year"""
    date = "2000-10-29"
    expected = "29 Oct 2000"
    actual = convert_date_string_to_text_string(date)
    assert actual == expected


def test_convert_date_string_to_text_string_month_exclude_year():
    """test convert_date_string_to_text_string doesn't abbreviate month and doesn't include year"""
    date = "2000-10-29"
    expected = "29 October"
    actual = convert_date_string_to_text_string(
        date, abbreviate_month=False, include_year=False
    )
    assert actual == expected


def test_convert_date_string_to_text_string_month_exclude_date():
    """test convert_date_string_to_text_string doesn't include date when required"""
    date = "2000-10-29"
    expected = "Oct 2000"
    actual = convert_date_string_to_text_string(date, include_day_of_month=False)
    assert actual == expected


def test_convert_date_string_to_text_string_non_default_date_format():
    """test convert_date_string_to_text_string with non-default date_format"""
    date = "29-10-2000"
    expected = "29 Oct 2000"
    actual = convert_date_string_to_text_string(date, date_format="%d-%m-%Y")
    assert actual == expected
