"""test get_changed_from_content"""

import pytest
from gov_uk_dashboards.components.dash.context_card import get_changed_from_content


@pytest.mark.parametrize(
    "current_value,previous_value,increase_is_positive,colour,direction",
    [
        (5, 4, True, "green", "up"),
        (2, 4, True, "red", "down"),
        (5, 4, False, "red", "up"),
        (2, 4, False, "green", "down"),
        # (4, 4, True, "grey", "right") # needs implementing/testing
    ],
)
def test_get_changed_from_content_increase_positive_and_increase(
    current_value, previous_value, increase_is_positive, colour, direction
):
    """test get_changed_from_content returns correctly styled arrow and colour
    for different value cases"""
    actual = get_changed_from_content(
        current_value, previous_value, increase_is_positive=increase_is_positive
    )

    assert colour in actual.children[0].className
    assert "arrow_" + direction in actual.children[0].className


def test_get_changed_from_content_no_change_and_percentage():
    """test get_changed_from_content when there is no change in the value and percentage included"""
    actual = get_changed_from_content(1, 1, True)
    # good to add extra asserts when arrow implemented.
    assert (
        "unchanged from" in actual.children[0].children[0].children
    )  # percentage change is zero
    assert "0.0%" in actual.children[0].children[1].children


def test_get_changed_from_content_formatting_and_suffix():
    """test get_changed_from_content formatting function rounds previous value input
    and adds suffix"""
    actual = get_changed_from_content(
        3.141592,
        2.71828183,
        True,
    )
    assert "up " in actual.children[0].children[0].children
    assert "15%" in actual.children[0].children[1].children


def test_get_changed_from_content_when_use_difference_in_weeks_days():
    """test get_changed_from_content returns expected content when
    use_difference_in_weeks_days=True"""
    actual = get_changed_from_content(
        10,
        5,
        increase_is_positive=True,
        use_difference_in_weeks_days=True,
    )
    assert "0 weeks and 5 days" in actual.children[0].children[0].children
    assert "slower than" in actual.children[0].children[1].children
    assert "green" in actual.children[0].className
    assert "arrow_up" in actual.children[0].className
