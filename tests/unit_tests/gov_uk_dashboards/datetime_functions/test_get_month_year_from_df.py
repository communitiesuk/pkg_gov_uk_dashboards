"""test get_month_year_from_df"""

import polars as pl
from lib.datetime_functions.datetime_functions import get_month_year_from_df


def test_get_month_year_from_df_one_datetime():
    """test get_month_year_from_df when there is one datetime in data along with nulls"""
    data = {
        "date_column": [
            "2024-03",
            None,
            None,
        ]
    }
    pl_df = pl.DataFrame(data)

    actual = get_month_year_from_df(pl_df, "date_column")
    assert actual == "March 2024"


def test_get_month_year_from_df_one_datetime_no_nulls():
    """test get_month_year_from_df when there is multiple datetimes and no nulls"""
    data = {"date_column": ["2024-03"] * 3}
    pl_df = pl.DataFrame(data)

    actual = get_month_year_from_df(pl_df, "date_column")
    assert actual == "March 2024"
