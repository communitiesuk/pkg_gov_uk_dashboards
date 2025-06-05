# """Testing calculate axis range"""
# import pandas as pd
# import pytest

# from gov_uk_dashboards.axes import calc_axis_range


# def test_given_positive_data_returns_min_range_zero():
#     """Testing the axis range given values greater than zero returns zero for min range"""
#     df = pd.DataFrame(data={"col1": [6, 8]})
#     axis_range = calc_axis_range(df, "col1")
#     assert axis_range == [0, 9]


# def test_given_negative_min_data_returns_negative_min_range():
#     """Testing the axis range given a min value less than zero returns a negative min range"""
#     df = pd.DataFrame(data={"col1": [-6, 8]})
#     axis_range = calc_axis_range(df, "col1")
#     assert axis_range == [-7, 9]


# def test_given_negative_data_returns_negative_range():
#     """Testing the axis range given a negative range returns a negative range"""
#     df = pd.DataFrame(data={"col1": [-6, -2]})
#     axis_range = calc_axis_range(df, "col1")
#     assert axis_range == [-7, -2]


# def test_given_str_data_throws_type_error():
#     """Testing that given str data for axis range function throws a TypeError"""
#     df = pd.DataFrame(data={"col1": ["abc", "def"]})
#     with pytest.raises(TypeError):
#         calc_axis_range(df, "col1")
