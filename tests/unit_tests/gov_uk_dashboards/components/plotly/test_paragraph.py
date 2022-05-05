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


def test_paragraph_default_class():
    """Test component has correct CSS class under default"""
    test_text = "A sentence"

    actual = paragraph(test_text)

    assert getattr(actual, "className") == "govuk-body"


def test_paragraph_lead_class():
    """Test component has correct class when lead size is specified"""
    test_text = "A sentence"

    actual = paragraph(test_text, ParagraphSizes.LEAD)

    assert getattr(actual, "className") == "govuk-body-l"


def test_paragraph_small_class():
    """Test component has correct class when small size is specified"""
    test_text = "A sentence"

    actual = paragraph(test_text, ParagraphSizes.SMALL)

    assert getattr(actual, "className") == "govuk-body-s"


def test_paragraph_specify_default_class():
    """Test component has correct class when default size is specified"""
    test_text = "A sentence"

    actual = paragraph(test_text, ParagraphSizes.DEFAULT)

    assert getattr(actual, "className") == "govuk-body"


def test_paragraph_specify_unknown_class():
    """Test component raises ValueError when provided an invalid paragraph size."""
    test_text = "A sentence"

    pytest.raises(ValueError, paragraph, test_text, "abc")
