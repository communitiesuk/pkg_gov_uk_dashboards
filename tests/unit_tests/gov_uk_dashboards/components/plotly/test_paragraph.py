"""Tests for paragraph component"""
import pytest
from dash import html

from gov_uk_dashboards.components.plotly.paragraph import ParagraphSizes, paragraph


def test_paragraph_returns_html_p():
    """Test component returns a dash <P>"""
    actual = paragraph("")

    assert isinstance(actual, html.P)


def test_paragraph_has_text_in_children():
    """Test component has supplied text as its children"""
    test_text = "A sentence"

    actual = paragraph(test_text)

    assert actual.children == test_text


def test_paragraph_has_all_components_in_children():
    """Test component has supplied text as its children"""
    test_text = "A sentence"
    test_link = html.A("A Link")

    actual = paragraph([test_text, test_link])

    assert actual.children == [test_text, test_link]


def test_paragraph_default_class():
    """Test component has correct CSS class under default"""
    test_text = "A sentence"

    actual = paragraph(test_text)

    assert getattr(actual, "className") == "govuk-body"


@pytest.mark.parametrize(
    "size", [ParagraphSizes.SMALL, ParagraphSizes.LEAD, ParagraphSizes.DEFAULT],
)
def test_paragraph_has_expected_class(size):
    """Test component has correct class when lead size is specified"""
    test_text = "A sentence"

    actual = paragraph(test_text, size=size)

    assert getattr(actual, "className") == size


def test_paragraph_specify_unknown_class():
    """Test component raises ValueError when provided an invalid paragraph size."""
    test_text = "A sentence"

    pytest.raises(ValueError, paragraph, test_text, "abc")
