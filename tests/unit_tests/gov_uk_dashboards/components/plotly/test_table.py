"""Tests for the table component"""
import pandas
import pytest
from dash import html

from gov_uk_dashboards.components.plotly.table import table_from_dataframe

df = pandas.DataFrame(columns=["Col1", "Col2", "Col3"],
                          data=[["1,1", "1,2", "1,3"],
                          ["2,1", "2,2", "2,3"]])

def test_table_shows_all_columns():
    table = table_from_dataframe(df)
    assert len(table.children[0].children.children) == 3


def test_table_hides_columns_when_they_are_provided():
    table = table_from_dataframe(df, columns_to_exclude=['Col2'])
    assert len(table.children[0].children.children) == 2


def test_first_column_formatter_produces_expected_value_in_first_column_when_provided():
    def hello_world(df, row, index):
        if index%2 == 0:
            return "hello"
        return "world"
    table = table_from_dataframe(df, first_column_formatter=hello_world)
    assert table.children[1].children[0].children[0].children == "hello"
    assert table.children[1].children[0].children[2].children == "1,3"
    assert table.children[1].children[1].children[0].children == "world"
    assert table.children[1].children[1].children[1].children == "2,2"