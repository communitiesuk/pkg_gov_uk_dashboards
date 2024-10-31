"""Function for creating a table component from a dataframe"""
from typing import Optional
from pandas import DataFrame
from dash import html, dcc
from gov_uk_dashboards.components.plotly.card import card
from gov_uk_dashboards.components.plotly.paragraph import paragraph
from gov_uk_dashboards.components.plotly.row_component import row_component


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


def table_from_polars_dataframe(
    dataframe: DataFrame,
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    first_column_is_header: bool = True,
    short_table: bool = True,
    last_row_unbolded: bool = False,
    format_column_headers_as_markdown: bool = False,
    table_id: str = "table",
    table_footer: str = None,
    column_widths: Optional[list[str]] = None,
    columns_to_right_align: Optional[list[str]] = None,
    **table_properties,
):  # pylint: disable=too-many-arguments
    """
    Displays a Polars DataFrame as a table formatted in the Gov.UK style. By default text is
    aligned to the left, unless column name is in columns_to_right_align.

    Part of the Gov.UK Design System:
    https://design-system.service.gov.uk/components/table/


    Args:
        dataframe (DataFrame): Dataframe containing formatted data to display.
        title (str, optional): Title to display above the table. Defaults to None.
        subtitle (str, optional):  Subtitle to display above the table. May be
            set alone or underneath the Title.  Defaults to None.
        first_column_is_header (bool, optional): Sets if the first column is a header column.
            Defaults to True.
        short_table: (bool, optional): if False the header of the table will scroll with window.
        last_row_unbolded: (bool, optional): Sets if the last row should not be bolded if
            first_column_is_header is True. Defaults to False.
        format_column_headers_as_markdown: (bool, optional): Sets if the column headers should
            be formatted as markdown. Defaults to False.
        table_id: (str, optional): ID for the table Defaults to "table".
        table_footer: (str, optional): Text to display underneath table as footer.
        column_widths: (list[str], optional): Determines width of table columns. Format as a list,
            "x%". List must be same length as dataframe columns. Defaults to None.
        columns_to_right_align: (Optional[list[str]]): List of columns whose content should be
            right aligned in tables. Defaults to None.
        **table_properties: Any additional arguments for the html.Table object,
            such as setting a width or id.

    Returns:
        html.Table: The dash HTML object for the table.

    Raises:
        ValueError: If the number of column_widths does not equal the number of columns in
            the dataframe.
    """
    if column_widths is None:
        column_widths = [None] * len(dataframe.columns)
    if len(column_widths) != len(dataframe.columns):
        raise ValueError(
            "Number of column_widths must equal number of columns in dataframe."
        )

    if columns_to_right_align is None:
        columns_to_right_align = []

    table_contents = []

    if title:
        table_contents.append(
            html.Caption(
                title,
                className=(
                    "govuk-table__caption govuk-table__caption--m margin-if-subtitle"
                    if subtitle
                    else "govuk-table__caption govuk-table__caption--m"
                ),
            )
        )
    if subtitle:
        table_contents.append(
            html.Caption(
                subtitle,
                className="govuk-table__caption .govuk-table__caption--s custom-subtitle",
            )
        )

    table_contents.append(
        html.Thead(
            html.Tr(
                [
                    (
                        html.Th(
                            dcc.Markdown(header),
                            scope="col",
                            className="govuk-table__header",
                            style={"width": width or None},
                        )
                        if format_column_headers_as_markdown
                        else html.Th(
                            header,
                            scope="col",
                            className="govuk-table__header",
                            style={
                                **({"width": width} if width else {}),
                                **(
                                    {"text-align": "right"}
                                    if header in columns_to_right_align
                                    else {}
                                ),
                            },
                        )
                    )
                    for header, width in zip(dataframe.columns, column_widths)
                ],
                className="govuk-table__row",
            ),
            className="govuk-table__head-short" if short_table else "govuk-table__head",
            style={
                "position": "sticky",
                "top": 0,
                "z-index": 1,
                "background-color": "#fff",
            },
        )
    )

    last_row_index = len(dataframe) - 1 if last_row_unbolded else len(dataframe)

    table_contents.append(
        html.Tbody(
            [
                (
                    html.Tr(
                        [html.Th(row[0], scope="row", className="govuk-table__header")]
                        + [
                            html.Td(
                                cell,
                                className="govuk-table__cell",
                                style={"text-align": "right"}
                                if column_name in columns_to_right_align
                                else {},
                            )
                            for cell, column_name in zip(row[1:], dataframe.columns[1:])
                        ]
                    )
                    if first_column_is_header and index != last_row_index
                    else html.Tr(
                        [
                            html.Td(
                                cell,
                                className="govuk-table__cell",
                                style={"text-align": "right"}
                                if column_name in columns_to_right_align
                                else {},
                            )
                            for cell, column_name in zip(row, dataframe.columns)
                        ]
                    )
                )
                for index, row in enumerate(dataframe.rows())
            ],
            className="govuk-table__body",
        )
    )

    return row_component(
        card(
            row_component(
                card(
                    [
                        html.Table(
                            table_contents,
                            className="govuk-table table-header-cell-top-padding",
                            id=table_id,
                            role="table",
                            **table_properties,
                        ),
                        paragraph(table_footer) if table_footer else None,
                    ],
                    amend_style={"padding": "0px"},
                ),
                horizontal_scroll=True,
            )
        ),
        horizontal_scroll=True,
    )
