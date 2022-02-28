from dash import html, dcc

from gov_uk_dashboards.components.plotly.navbar import navbar_link


def test_navbar_link_is_li_element():
    """test the navbar element is returning a dash.html.Li element"""
    # act
    sut = navbar_link("", "")

    # assert
    assert isinstance(sut, html.Li)


def test_navbar_link_has_children():
    """test the navbar link has a dash.dcc.Link as child element"""
    # act
    sut = navbar_link("", "")
    list_element = sut.children

    # assert
    assert isinstance(list_element, dcc.Link)


def test_navbar_link_classname():
    """test navbar link classname"""
    # act
    sut = navbar_link("", "")

    # assert
    assert sut.className == "moj-side-navigation__item"


def test_navbar_link_child_classname():
    """test navbar children classname"""
    # act
    sut = navbar_link("", "")
    list_element = sut.children

    # assert
    assert list_element.className == "govuk-link govuk-link--no-visited-state"


def test_navbar_link_text_and_href_are_set():
    """test navbar link text and href are set"""
    # arrange
    actual_text = "test text"
    actual_href = "test href"

    # act
    sut = navbar_link(actual_text, actual_href)

    # assert
    assert sut.children.children == actual_text
    assert sut.children.href == actual_href
