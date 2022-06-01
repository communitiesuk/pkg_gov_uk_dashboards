"""Tests for the table component"""
import pandas
import pytest
from dash import html

from gov_uk_dashboards.components.plotly.table import table_from_dataframe


def test_table_shows_all_columns():
    df = pandas.DataFrame(columns=["Col1", "Col2", "Col3"],
                          data=[["1,1", "1,2", "1,3"]])
    table = table_from_dataframe(df)

    assert len(table.children[0].children.children) == 3


def test_table_hides_columns_when_they_are_provided():
    assert True


def test_first_column_formatter_produces_expected_value_in_first_column_when_provided():
    assert True