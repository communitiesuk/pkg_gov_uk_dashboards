"""test_number_formatting"""

from gov_uk_dashboards.formatting.number_formatting import (
    format_number_into_thousands_or_millions,
)


def test_format_number_into_thousands_or_millions_less_than_thousand():
    """test_format_number_into_thousands_or_millions when number less than one-thousand"""
    assert format_number_into_thousands_or_millions(123) == "123"


def test_format_number_into_thousands_or_millions_thousands():
    """test_format_number_into_thousands_or_millions when number less than one-million
    but more than one-thousand"""
    assert format_number_into_thousands_or_millions(12_345) == "12k"


def test_format_number_into_thousands_or_millions_thousands_decimal_places():
    """test_format_number_into_thousands_or_millions when number less than one-million
    but more than one-thousand, with non-default thousand decimal places"""
    assert (
        format_number_into_thousands_or_millions(12_345, thousand_decimal_places=1)
        == "12.3k"
    )


def test_format_number_into_thousands_or_millions_millions():
    """test_format_number_into_thousands_or_millions when number more than one-million"""
    assert format_number_into_thousands_or_millions(1_234_567) == "1.235m"
