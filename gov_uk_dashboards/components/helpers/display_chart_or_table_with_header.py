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
    download_map_button_id: str = None,
    download_all_data_button_id: str = None,
    alternative_data_button_text: str = None,
    alternative_all_data_button_text: str = None,
    footnote: str = None,
    instance=1,
    text_below_subheading: str = None,
) -> html.Div:
    """Generate the wrapping information/header for a chart or table.

    Args:
        chart_or_table (Component): the chart or table to display.
        heading (str, optional): the heading for the chart,
        sub_heading (str, optional): the sub-heading for the chart,
        download_button_id (str, optional): id for download button if required. Defaults to None.
                                            if None then the button will not be included.
        download_data_button_id (str, optional): the id to be applied to the download data button.
        download_map_button_id (str, optional): the id to be applied to the download map button.
        download_all_data_button_id (str, optional): the id to be applied to the download all data
            button
        alternative_data_button_text (str, optional): Optional alternative to button text
            "Download data"
        alternative_all_data_button_text (str, optional): Optional alternative to button text
            "Download all data"
        footnote (str, optional): the footnote to be added to charts and downloads.
        instance (int or str): Optional additional paramter for id dict.
        text_below_subheading (str, optional): Optional text to go below subheading but above
            chart_or_table.

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
            paragraph(text_below_subheading),
            chart_or_table,
            html.Div([paragraph(footnote)], style={"paddingTop": "20px"}),
            html.Div(
                (
                    [
                        html.Div(
                            [
                                (
                                    create_download_button_with_icon(
                                        "Download chart", download_button_id, instance
                                    )
                                    if download_button_id
                                    else []
                                ),
                                (
                                    create_download_button_with_icon(
                                        "Download map", download_map_button_id, instance
                                    )
                                    if download_map_button_id
                                    else []
                                ),
                                (
                                    create_download_button_with_icon(
                                        (
                                            alternative_data_button_text
                                            if alternative_data_button_text
                                            else "Download data"
                                        ),
                                        download_data_button_id,
                                        instance,
                                        "data",
                                    )
                                    if download_data_button_id
                                    else []
                                ),
                                (
                                    create_download_button_with_icon(
                                        (
                                            alternative_all_data_button_text
                                            if alternative_all_data_button_text
                                            else "Download all data"
                                        ),
                                        download_all_data_button_id,
                                        instance,
                                        "data",
                                    )
                                    if download_all_data_button_id
                                    else []
                                ),
                            ],
                            className="govuk-button-group",
                            style={"paddingTop": "20px"},
                        ),
                    ]
                ),
            ),
        ],
        className="container-class box_container_layout bg_white",
    )
