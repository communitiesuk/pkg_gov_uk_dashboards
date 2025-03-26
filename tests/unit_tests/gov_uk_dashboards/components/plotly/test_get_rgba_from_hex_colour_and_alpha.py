"""Test the function to get RGBA values from a hex colour code works"""

import pytest
from gov_uk_dashboards.components.helpers.plotting_helper_functions import (
    get_rgba_from_hex_colour_and_alpha,
)


def test_hex_code_starts_with_hash():
    """Given a hex value which does not start with a hash
    the function returns an error"""
    hex_code = "FFCCFF"

    with pytest.raises(ValueError):
        get_rgba_from_hex_colour_and_alpha(hex_code)


def test_hex_code_is_valid_length():
    """Given a hex value which is not a valid length
    the function returns an error"""
    hex_code = "#FFCCF"

    with pytest.raises(ValueError):
        get_rgba_from_hex_colour_and_alpha(hex_code)


def test_hex_code_returns_valid_rgb_code_without_opacity():
    """Given a valid hex value function returns correct RGB code"""

    hex_code = "#FF66B2"

    expected_outcome = "rgba(255, 102, 178, 1.0)"

    actual_outcome = get_rgba_from_hex_colour_and_alpha(hex_code)

    assert expected_outcome == actual_outcome


def test_hex_code_returns_valid_rgb_code_with_opacity():
    """Given a valid hex value function returns correct RGB code"""

    hex_code = "#FF66B2"
    alpha = 0.7

    expected_outcome = "rgba(255, 102, 178, 0.7)"

    actual_outcome = get_rgba_from_hex_colour_and_alpha(hex_code, alpha)

    assert expected_outcome == actual_outcome
