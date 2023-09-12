"""Function for creating a table component from a dataframe"""
from typing import Optional
from pandas import DataFrame
from dash import html, dcc


def table_from_dataframe(
    dataframe: DataFrame,
    title: Optional[str] = None,
    first_column_is_header: bool = True,
    title_is_subtitle: bool = False,
    short_table: bool = True,
    last_row_unbolded: bool = False,
    format_column_headers_as_markdown: bool = False,
    **table_properties,
):  # pylint: disable=too-many-arguments
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
        last_row_unbolded: (bool, optional): Sets if the last row should not be bolded if
            first_column_is_header is True. Defaults to False.
        format_column_headers_as_markdown: (bool, optional): Sets if the column headers should
            be formatted as markdown. Defaults to False.
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
                    html.Th(
                        dcc.Markdown(header),
                        scope="col",
                        className="govuk-table__header",
                    )
                    if format_column_headers_as_markdown
                    else html.Th(header, scope="col", className="govuk-table__header")
                    for header in dataframe.columns
                ],
                className="govuk-table__row",
            ),
            className="govuk-table__head-short" if short_table else "govuk-table__head",
        )
    )

    last_row_index = len(dataframe) - 1 if last_row_unbolded else len(dataframe)
    table_contents.append(
        html.Tbody(
            [
                html.Tr(
                    [html.Th(row.iloc[0], scope="row", className="govuk-table__header")]
                    + [html.Td(cell, className="govuk-table__cell") for cell in row[1:]]
                )
                if first_column_is_header and index != last_row_index
                else html.Tr(
                    [html.Td(cell, className="govuk-table__cell") for cell in row]
                )
                for index, row in dataframe.iterrows()
            ],
            className="govuk-table__body",
        )
    )

    return html.Table(
        table_contents,
        className="govuk-table",
        id="table",
        role="table",
        **table_properties,
    )
