"""ChartData dataclass"""
from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class ChartData:
    """
    Dataclass containing standard information useful for plotting charts.

    Attributes:
        dataframe (pd.DataFrame): The dataframe containing the data for the chart.
        x_column (str): The label of the column containing the x axis values.
        y_column (str): The label of the column containing the y axis values.
        category_column (str, optional): If there are multiple categories in the data,
            this column gives the value to categorize them. Defaults to None.
    """

    dataframe: pd.DataFrame
    x_column: str
    y_column: str
    category_column: Optional[str] = None
