import pytest
from dash import html

from gov_uk_dashboards.components.plotly.navbar import navbar


def test_navbar_is_nav_element():
    """test the navbar element is returning a dash.html.Nav element"""
    # act
    sut = navbar("")

    # assert
    assert isinstance(sut, html.Nav)


def test_navbar_has_children():
    """test navbar has children that are dash.html.Div and dash.html.Ul element"""
    #  act
    sut = navbar("")
    children = sut.children

    # assert
    assert isinstance(children, html.Div)
    assert isinstance(children.children, html.Ul)


def test_navbar_classname():
    """test navbar classname"""
    # act
    sut = navbar("")

    # assert
    assert sut.className == "dashboard-menu"


def test_navbar_children_classname():
    """test navbar children classname"""
    # act
    sut = navbar("")
    children = sut.children

    # assert
    assert children.className == "moj-side-navigation govuk-!-padding-right-2"
    assert children.children.className == "moj-side-navigation__list"


def test_navbar_link():
    """test navbar link is set"""
    # arrange
    expected_link = "testing link"

    # act
    sut = navbar(expected_link)
    actual_link = sut.children.children.children

    # assert
    assert actual_link == expected_link
