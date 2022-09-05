"""Function for creating a table component from a dataframe"""
from typing import Optional
from pandas import DataFrame
from dash import html


def table_from_dataframe(
    dataframe: DataFrame,
    title: Optional[str] = None,
    first_column_is_header: bool = True,
    title_is_subtitle: bool = False,
    short_table: bool = True,
    **table_properties,
):
    """
    Displays a pandas DataFrame as a table formatted in the Gov.UK style

    Part of the Gov.UK Design System:
    https://design-system.service.gov.uk/components/table/


    Args:
        dataframe (DataFrame): Dataframe containing formatted data to display.
        title (str, optional): Title to display above the table. Defaults to None.
        first_column_is_header (bool, optional): Sets if the first column is a header column.
            Defaults to True.
        title_is_subtitle (bool, optional): Sets if the title should be displayed as a subtitle
            or full title. Defaults to False.
        short_table: (bool, optional): if False the header of the table will scroll with window.
        **table_properties: Any additional arguments for the html.Table object,
            such as setting a width or id.

    Returns:
        html.Table: The dash HTML object for the table.
    """
    table_contents = []

    if title:
        table_contents.append(
            html.Caption(
                title,
                className="govuk-table__caption govuk-table__caption--s"
                if title_is_subtitle
                else "govuk-table__caption govuk-table__caption--m",
            )
        )

    table_contents.append(
        html.Thead(
            html.Tr(
                [
                    html.Th(header, scope="col", className="govuk-table__header")
                    for header in dataframe.columns
                ],
                className="govuk-table__row",
            ),
            className="govuk-table__head-short" if short_table else "govuk-table__head",
        )
    )

    table_contents.append(
        html.Tbody(
            [
                html.Tr(
                    [html.Th(row[0], scope="row", className="govuk-table__header")]
                    + [html.Td(cell, className="govuk-table__cell") for cell in row[1:]]
                )
                if first_column_is_header
                else html.Tr(
                    [html.Td(cell, className="govuk-table__cell") for cell in row]
                )
                for _, row in dataframe.iterrows()
            ],
            className="govuk-table__body",
        )
    )

    return html.Table(table_contents, className="govuk-table", **table_properties)
