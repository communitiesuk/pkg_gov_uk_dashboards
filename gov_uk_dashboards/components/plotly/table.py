"""Function for creating a table component from a dataframe"""
from pandas import DataFrame
from dash import html


def table_from_dataframe(
    dataframe: DataFrame,
    title: str = None,
    include_headers: bool = True,
    first_column_is_header: bool = True,
    **table_properties
):
    """
    Displays a pandas DataFrame as a table formatted in the Gov.UK style

    Part of the Gov.UK Design System:
    https://design-system.service.gov.uk/components/table/


    Args:
        df (DataFrame): Dataframe containing formatted data to display.
        title (str, optional): Title to display above the table. Defaults to None.
        include_headers (bool, optional): If the column labels should be included as headers.
            Defaults to True.
        first_column_is_header (bool, optional): _description_. Defaults to True.
        **table_properties: Any additional arguments for the html.Table object,
            such as setting a width or id.

    Returns:
        html.Table: The dash HTML object for the table.
    """
    table_contents = []

    if title:
        table_contents.append(
            html.Caption(
                title, className="govuk-table__caption govuk-table__caption--m"
            )
        )

    if include_headers:
        table_contents.append(
            html.Thead(
                html.Tr(
                    [
                        html.Th(header, scope="col", className="govuk-table__header")
                        for header in dataframe.columns
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
