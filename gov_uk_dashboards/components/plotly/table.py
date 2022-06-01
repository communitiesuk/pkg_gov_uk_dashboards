"""Function for creating a table component from a dataframe"""
from typing import Optional
from pandas import DataFrame
from dash import html


def table_from_dataframe(
        dataframe: DataFrame,
        title: Optional[str] = None,
        include_headers: bool = True,
        first_column_is_header: bool = True,
        title_is_subtitle: bool = False,
        first_column_formatter: Optional = None,
        columns_to_exclude: Optional[list[str]] = [],
        **table_properties
):
    """
    Displays a pandas DataFrame as a table formatted in the Gov.UK style

    Part of the Gov.UK Design System:
    https://design-system.service.gov.uk/components/table/


    Args:

        dataframe (DataFrame): Dataframe containing formatted data to display.
        title (str, optional): Title to display above the table. Defaults to None.
        include_headers (bool, optional): If the column labels should be included as headers.
            Defaults to True.
        first_column_is_header (bool, optional): Sets if the first column is a header column.
            Defaults to True.
        title_is_subtitle (bool, optional): Sets if the title should be displayed as a subtitle
            or full title. Defaults to False.
        first_column_formatter: a function that will be provided a dataframe:pd.dataFrame,
            row:pd.Series and index:int that can be used to reformat the first column
        columns_to_exclude: A list of column names to exclude from displaying in the table
        **table_properties: Any additional arguments for the html.Table object,
            such as setting a width or id.

    Returns:
        html.Table: The dash HTML object for the table.
    """
    if first_column_formatter is None:
        first_column_formatter = lambda df, row, index: row[index]

    table_contents = []

    filtered_dataframe = dataframe.loc[:, ~dataframe.columns.isin(columns_to_exclude)]

    if title:
        table_contents.append(
            html.Caption(
                title,
                className="govuk-table__caption govuk-table__caption--s"
                if title_is_subtitle
                else "govuk-table__caption govuk-table__caption--m",
            )
        )

    if include_headers:
        table_contents.append(
            html.Thead(
                html.Tr(
                    [
                        html.Th(header, scope="col", className="govuk-table__header")
                        for header in filtered_dataframe.columns
                    ],
                    className="govuk-table__row",
                ),
                className="govuk-table__head",
            )
        )

    table_contents.append(
        html.Tbody(
            [
                html.Tr(
                    (
                        [
                            html.Th(
                                first_column_formatter(dataframe, row, index),
                                scope="row",
                                className="govuk-table__header",
                            )
                        ]
                        if first_column_is_header
                        else [
                            html.Td(
                                first_column_formatter(dataframe, row, index),
                                className="govuk-table__cell",
                            )
                        ]
                    )
                    + [html.Td(cell, className="govuk-table__cell") for cell in row[1:]]
                )
                for index, row in filtered_dataframe.iterrows()
            ],
            className="govuk-table__body",
        )
    )

    return html.Table(table_contents, className="govuk-table", **table_properties)
