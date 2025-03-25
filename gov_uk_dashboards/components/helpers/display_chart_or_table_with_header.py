"""Generate the wrapping information/header for a chart or table."""

from dash import html
from dash.development.base_component import Component

from gov_uk_dashboards.components.dash.create_download_chart_button import (
    create_download_chart_button,
)
from gov_uk_dashboards.components.dash.create_download_data_button import (
    create_download_data_button,
)
from gov_uk_dashboards.components.dash.heading import HeadingSizes


def display_chart_or_table_with_header(
    chart_or_table: Component,
    heading: str = None,
    sub_heading: str = None,
    download_button_id: str = None,
    download_data_button_id: str = None,
) -> html.Div:
    """Generate the wrapping information/header for a chart or table.

    Args:
        chart_or_table (Component): the chart or table to display.
        heading (str, optional): the heading for the chart,
        sub_heading (str, optional): the sub-heading for the chart,
        download_button_id (str, optional): id for download button if required. Defaults to None.
                                            if None then the button will not be included.
        download_data_button_id (str, optional): the id to be applied to the download data button.

    Returns:
        html.Div: Div containing Header and chart/table.
    """
    return html.Div(
        [
            html.Div(
                [
                    (
                        create_download_chart_button(button_id_name=download_button_id)
                        if download_button_id
                        else None
                    ),
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
            html.Div(
                (
                    [
                        html.H3(
                            "Download this data",
                            className=HeadingSizes.SMALL,
                            style={
                                **{"color": "black", "margin": "0px 0px 5px"},
                                **{"padding-top": "20px"},
                            },
                        ),
                        create_download_data_button(
                            button_id_name=download_data_button_id
                        ),
                    ]
                    if download_data_button_id
                    else []
                ),
            ),
        ],
        className="container-class box_container_layout bg_white",
    )
