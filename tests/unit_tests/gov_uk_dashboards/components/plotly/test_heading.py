"""Tests for heading components"""
import itertools

import pytest
from dash import html

from gov_uk_dashboards.components.dash.heading import (
    heading1,
    HeadingSizes,
    heading2,
    heading3,
)


@pytest.mark.parametrize(
    "heading, expected_type",
    [(heading1, html.H1), (heading2, html.H2), (heading3, html.H3)],
)
def test_heading_returns_expected_html_heading_type(heading, expected_type):
    """Test component returns expected dash component type"""
    actual = heading("")

    assert isinstance(actual, expected_type)


@pytest.mark.parametrize("heading", [heading1, heading2, heading3])
def test_heading_has_text_in_children(heading):
    """heading component has supplied text as its children"""
    test_text = "A heading"

    actual = heading(test_text)

    assert actual.children == test_text


@pytest.mark.parametrize(
    "heading, default_class",
    [
        (heading1, HeadingSizes.LARGE),
        (heading2, HeadingSizes.MEDIUM),
        (heading3, HeadingSizes.SMALL),
    ],
)
def test_heading_has_default_class(heading, default_class):
    """heading component has a default class when none is provided"""

    actual = heading("")

    assert getattr(actual, "className") == default_class


@pytest.mark.parametrize(
    "heading, size",
    list(
        itertools.product(
            [heading1, heading2, heading3],
            [
                HeadingSizes.EXTRA_LARGE,
                HeadingSizes.LARGE,
                HeadingSizes.MEDIUM,
                HeadingSizes.SMALL,
            ],
        )
    ),
)
def test_heading_has_expected_class(heading, size):
    """heading component has expected size"""

    actual = heading("", size)

    assert getattr(actual, "className") == size
