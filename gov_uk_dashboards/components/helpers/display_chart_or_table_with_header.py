"""Generate the wrapping information/header for a chart or table."""

from dash import html
from dash.development.base_component import Component

from gov_uk_dashboards.components.dash.download_button import (
    create_download_button_with_icon,
)
from gov_uk_dashboards.components.dash.heading import HeadingSizes
from gov_uk_dashboards.components.dash.paragraph import paragraph


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
def display_chart_or_table_with_header(
    chart_or_table: Component,
    heading: str = None,
    sub_heading: str = None,
    download_button_id: str = None,
    download_data_button_id: str = None,
    footnote: str = None,
) -> html.Div:
    """Generate the wrapping information/header for a chart or table.

    Args:
        chart_or_table (Component): the chart or table to display.
        heading (str, optional): the heading for the chart,
        sub_heading (str, optional): the sub-heading for the chart,
        download_button_id (str, optional): id for download button if required. Defaults to None.
                                            if None then the button will not be included.
        download_data_button_id (str, optional): the id to be applied to the download data button.
        footnote (str, optional): the footnote to be added to charts and downloads.

    Returns:
        html.Div: Div containing Header and chart/table.
    """
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H2(
                                heading,
                                className=HeadingSizes.MEDIUM,
                                style={"color": "black", "margin": "0px 0px 5px"},
                            ),
                            html.H3(
                                sub_heading,
                                className=HeadingSizes.SMALL,
                                style={"color": "black", "margin": "0px 0px 5px"},
                            ),
                        ],
                    ),
                ]
            ),
            chart_or_table,
            html.Div([paragraph(footnote)], style={"padding-top": "20px"}),
            html.Div(
                (
                    [
                        html.Div(
                            [
                                create_download_button_with_icon(
                                    "Download chart", download_button_id
                                )
                                if download_button_id
                                else [],
                                create_download_button_with_icon(
                                    "Download data", download_data_button_id
                                )
                                if download_data_button_id
                                else [],
                            ],
                            className="govuk-button-group",
                            style={"padding-top": "20px"},
                        ),
                    ]
                ),
            ),
        ],
        className="container-class box_container_layout bg_white",
    )
