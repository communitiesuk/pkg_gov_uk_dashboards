"""Tests for html list component"""

from dash import html

from gov_uk_dashboards.components.dash.html_list import html_list


def test_returns_bulleted_list_by_default():
    """Test component returns a dash <ul>"""
    actual = html_list([])

    assert isinstance(actual, html.Ul)


def test_returns_bulleted_list():
    """Test component returns a dash <ul>"""
    actual = html_list([], numbered_list=False)

    assert isinstance(actual, html.Ul)


def test_returns_numbered_list():
    """Test component returns a dash <ol>"""
    actual = html_list([], numbered_list=True)

    assert isinstance(actual, html.Ol)


def test_returns_bulleted_list_with_expected_list_elements():
    """Test component returns a dash <ul> with <li> containing expected values"""
    list_items = ["a", "b", "c"]
    expected = [html.Li(x) for x in list_items]
    actual = html_list(list_items)

    assert all([a.children == b.children for a, b in zip(actual.children, expected)])


def test_returns_numbered_list_with_expected_list_elements():
    """Test component returns a dash <ol> with <li> containing expected values"""
    list_items = ["a", "b", "c"]
    expected = [html.Li(x) for x in list_items]
    actual = html_list(list_items, numbered_list=True)

    assert all([a.children == b.children for a, b in zip(actual.children, expected)])


def test_returns_bulleted_list_with_correct_class_name():
    """Test component returns a dash <ul> with the correct className"""
    actual = html_list([])
    assert "govuk-list govuk-list--bullet" in getattr(actual, "className")


def test_returns_numbered_list_with_correct_class_name():
    """Test component returns a dash <ol> with the correct className"""
    actual = html_list([], numbered_list=True)
    assert "govuk-list govuk-list--number" in getattr(actual, "className")


def test_returns_bulleted_list_with_extra_spacing():
    """Test component returns a dash <ul> with the extra spacing className"""
    actual = html_list([], extra_spacing=True)
    assert "govuk-list--spaced" in getattr(actual, "className")


def test_returns_numbered_list_with_extra_spacing():
    """Test component returns a dash <ol> with the extra spacing className"""
    actual = html_list([], extra_spacing=True, numbered_list=True)
    assert "govuk-list--spaced" in getattr(actual, "className")
