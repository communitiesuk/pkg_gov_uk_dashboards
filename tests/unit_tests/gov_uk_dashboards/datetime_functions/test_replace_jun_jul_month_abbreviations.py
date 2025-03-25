"""test replace_jun_jul_month_abbreviations"""

from lib.datetime_functions.datetime_functions import (
    replace_jun_jul_month_abbreviations,
)


def test_replace_jun_jul_month_abbreviations():
    """Test replace_jun_jul_month_abbreviations performs as expected"""
    input_list = [
        "Jan 2023",
        "January 2023",
        "Jun 2024",
        "June 2025",
        "Jul 2026",
        "July 2027",
    ]
    expected_list = [
        "Jan 2023",
        "January 2023",
        "June 2024",
        "June 2025",
        "July 2026",
        "July 2027",
    ]
    actual_list = replace_jun_jul_month_abbreviations(input_list)
    assert expected_list == actual_list
