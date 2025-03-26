"""Tests for shorten_month_year_range"""

import pytest
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    shorten_month_range,
)


def test_standard_case():
    """Test a regular month range"""
    assert shorten_month_range("January to February 2024") == "Jan to Feb 2024"
    assert shorten_month_range("March to April 2023") == "Mar to Apr 2023"
    assert shorten_month_range("September to October 2021") == "Sep to Oct 2021"


def test_same_month():
    """Test when the start and end months are the same"""
    assert shorten_month_range("January to January 2024") == "Jan to Jan 2024"
    assert shorten_month_range("July to July 2020") == "Jul to Jul 2020"


def test_case_insensitivity():
    """Test case insensitivity"""
    with pytest.raises(ValueError):
        shorten_month_range("january to february 2024")
    with pytest.raises(ValueError):
        shorten_month_range("MARCH to APRIL 2023")


def test_invalid_month():
    """Test invalid month names"""
    with pytest.raises(ValueError):
        shorten_month_range("Januar to February 2024")
    with pytest.raises(ValueError):
        shorten_month_range("January to Febuary 2024")


def test_invalid_format():
    """Test invalid formats"""
    with pytest.raises(IndexError):
        shorten_month_range("January 2024")  # Missing 'to Month'
    with pytest.raises(ValueError):
        shorten_month_range("2024 January to February")  # Wrong format
