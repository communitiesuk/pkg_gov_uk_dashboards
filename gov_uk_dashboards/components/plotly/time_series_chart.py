"""get_time_series_chart function"""

from datetime import datetime, date
from typing import Optional
from dateutil.relativedelta import relativedelta
from dash import html
import polars as pl

import plotly.graph_objects as go

from gov_uk_dashboards.constants import (
    CHART_LABEL_FONT_SIZE,
    CUSTOM_DATA,
    DATE_VALID,
    FILL_TO_PREVIOUS_TRACE,
    HOVER_TEXT_HEADERS,
    MAIN_TITLE,
    REMOVE_INITIAL_MARKER,
    SUBTITLE,
    YEAR,
)
from gov_uk_dashboards.colours import AFAccessibleColours
from gov_uk_dashboards.components.helpers.display_chart_or_table_with_header import (
    display_chart_or_table_with_header,
)
from gov_uk_dashboards.components.helpers.generate_dash_graph_from_figure import (
    generate_dash_graph_from_figure,
)
from gov_uk_dashboards.components.helpers.plotting_helper_functions import (
    get_legend_configuration,
    get_rgba_from_hex_colour_and_alpha,
)
from gov_uk_dashboards.components.helpers.update_layout_bgcolor_margin import (
    update_layout_bgcolor_margin,
)
from gov_uk_dashboards.components.plotly.enums import (
    HoverDataByTrace,
    TitleDataStructure,
    XAxisFormat,
)
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_financial_quarter_to_financial_quarter_text,
    replace_jun_jul_month_abbreviations,
)


class TimeSeriesChart:
    """Class for use in generating time series charts."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-positional-arguments

    def __init__(
        self,
        title_data: TitleDataStructure,
        y_column: str,
        hover_data: HoverDataByTrace,
        filtered_df: pl.DataFrame,
        trace_name_list: list[str],
        hover_data_for_traces_with_different_hover_for_last_point: Optional[
            HoverDataByTrace
        ] = None,
        legend_dict: dict[str, str] = None,
        trace_name_column: Optional[str] = None,
        xaxis_tick_text_format: XAxisFormat = XAxisFormat.YEAR.value,
        verticle_line_x_value_and_name: tuple = None,
        last_2_traces_filled=False,
        trace_names_to_prevent_hover_of_first_point_list=None,
        x_axis_column=DATE_VALID,
        x_axis_title: Optional[str] = None,
        download_chart_button_id: Optional[str] = None,
        download_data_button_id: Optional[str] = None,
        number_of_traces_colour_shift_dict: Optional[dict] = None,
    ):
        self.title_data = title_data
        self.y_axis_column = y_column
        self.hover_data = hover_data
        self.hover_data_for_traces_with_different_hover_for_last_point = (
            hover_data_for_traces_with_different_hover_for_last_point
        )
        self.filtered_df = filtered_df
        self.trace_name_list = trace_name_list
        self.legend_dict = legend_dict
        self.trace_name_column = trace_name_column
        self.xaxis_tick_text_format = xaxis_tick_text_format
        self.verticle_line_x_value_and_name = verticle_line_x_value_and_name
        self.last_2_traces_filled = last_2_traces_filled
        self.trace_names_to_prevent_hover_of_first_point = (
            trace_names_to_prevent_hover_of_first_point_list
        )
        self.x_axis_column = x_axis_column
        self.x_axis_title = x_axis_title
        self.download_chart_button_id = download_chart_button_id
        self.download_data_button_id = download_data_button_id
        self.markers = ["square", "diamond", "circle", "triangle-up"]
        self.number_of_traces_colour_shift_dict = number_of_traces_colour_shift_dict
        self.colour_list = self._get_colour_list()
        self.fig = self.create_time_series_chart()

    def get_time_series_chart(self) -> html.Div:
        """Creates and returns time series chart for display on application.

        Returns:
            html.Div: Styled div containing title, subtile and chart.
        """
        # pylint: disable=duplicate-code
        graph_name = self.title_data[MAIN_TITLE].replace(" ", "-")
        return display_chart_or_table_with_header(
            generate_dash_graph_from_figure(
                self.fig,
                graph_name,
                class_name="default-cursor-graph non-interactive-legend-cursor",
            ),
            self.title_data[MAIN_TITLE],
            self.title_data[SUBTITLE],
            self.download_chart_button_id,
            self.download_data_button_id,
        )

    def create_time_series_chart(
        self,
    ):
        """generates a time series chart"""
        # pylint: disable=too-many-locals
        # pylint: disable=duplicate-code
        fig = go.Figure()
        for i, (df, trace_name, colour, marker) in enumerate(
            zip(
                self._get_df_list_for_time_series(),
                self.trace_name_list,
                self.colour_list,
                self.markers,
            )
        ):
            is_last = is_second_last = False
            if self.last_2_traces_filled is True:
                number_of_traces = len(self._get_df_list_for_time_series())
                is_last = i == number_of_traces - 1
                is_second_last = i == number_of_traces - 2
            if REMOVE_INITIAL_MARKER in df.columns and True in df.get_column(
                REMOVE_INITIAL_MARKER
            ):
                marker_sizes = [0] + [12] * (len(df.with_row_count()) - 1)
            else:
                marker_sizes = [12] * (len(df.with_row_count()))
            fig.add_trace(
                self.create_time_series_trace(
                    df.sort(self.x_axis_column),
                    trace_name,
                    (
                        {"width": 0}
                        if is_last or is_second_last
                        else {"dash": "solid", "color": colour}
                    ),
                    fill=(
                        "tonexty"
                        if FILL_TO_PREVIOUS_TRACE in df.columns
                        and True in df.get_column(FILL_TO_PREVIOUS_TRACE)
                        else None
                    ),
                    hover_label=(
                        {"bgcolor": AFAccessibleColours.TURQUOISE.value}
                        if is_last or is_second_last
                        else None
                    ),
                    marker=(
                        {"opacity": 0}
                        if is_last or is_second_last
                        else {"symbol": marker, "size": marker_sizes, "opacity": 1}
                    ),
                )
            )
        self._format_x_axis(fig)

        # if self.average_increment_for_average_trace is not None:
        #     trace_name = LINEAR_TRAJECTORY
        #     dates = [
        #         datetime(2024, 7, 9) + relativedelta(months=1 * i)
        #         for i in range(len(tick_values))
        #     ]
        #     values = [
        #         self.average_increment_for_average_trace * i for i in range(len(dates))
        #     ]
        #     fig.add_trace(
        #         go.Scatter(
        #             x=dates,
        #             y=values,
        #             mode="lines",
        #             name=trace_name,
        #             line={"dash": "dash", "color": "darkgray", "width": 2},
        #             hoverinfo="skip",
        #         )
        #     )
        if self.verticle_line_x_value_and_name is not None:

            fig.add_vline(
                x=self.verticle_line_x_value_and_name[0],
                line_width=2,
                line_dash="dash",
                line_color="#b3b3b3",
            )
            fig.add_annotation(
                x=self.verticle_line_x_value_and_name[0],
                yref="paper",
                y=0.9,
                text=self.verticle_line_x_value_and_name[1],
                showarrow=False,
                font={"color": "#414042", "size": 16},
                xanchor="left",
                yanchor="bottom",
            )

        y_range = [0, self._get_y_axis_range_max()]

        fig.update_yaxes(rangemode="tozero", showgrid=True, range=y_range)
        update_layout_bgcolor_margin(fig, "#FFFFFF")

        if self.x_axis_title is not None:
            fig.add_annotation(
                xref="x domain",
                yref="y domain",
                x=1,
                y=-0.25,
                text=self.x_axis_title,
                showarrow=False,
                font={"size": CHART_LABEL_FONT_SIZE},
            )

        fig.update_layout(
            legend=get_legend_configuration(),
            font={"size": CHART_LABEL_FONT_SIZE},
            yaxis_tickformat=",",
        )
        return fig

    # pylint: disable=duplicate-code
    def _format_x_axis(self, fig):
        tick_text, tick_values, range_x = self._get_x_axis_content()

        fig.update_xaxes(
            tickvals=tick_values,
            ticktext=tick_text,
            tickmode="array",
            range=range_x,
        )

    def create_time_series_trace(
        self,
        df: pl.DataFrame,
        trace_name: str,
        line_style: dict[str, str],
        fill: str,
        hover_label: dict[str, str],
        marker: dict[str, str],
    ):
        """Creates a trace for the plot.

        Args:
            df (pl.DataFrame): Dataframe to use to create trace. Must contain "Date valid" column,
            y_value column and columns defined in self.hover_data[CUSTOM_DATA].
            trace_name (str): Name of trace.
            line_style (dict[str, str]): Properties for line_style parameter.
            fill (str): Properties for fill parameter.
            hover_label (dict[str,str]): Properties for hoverlabel parameter.
            marker (dict[str,str]): Properties for marker parameter.
        """
        return go.Scatter(
            x=df[self.x_axis_column],
            y=df[self.y_axis_column],
            line=line_style,
            name=self._get_trace_name(trace_name),
            hovertemplate=self._get_hover_template(df, trace_name),
            customdata=self._get_custom_data(df, trace_name),
            marker=marker,
            fill=fill,
            hoverlabel=hover_label,
            fillcolor=(
                get_rgba_from_hex_colour_and_alpha(
                    AFAccessibleColours.TURQUOISE.value, alpha=0.2
                )
                if fill
                else None
            ),
            showlegend=(
                trace_name in self.legend_dict if self.legend_dict is not None else True
            ),
        )

    def _get_hover_template(self, df, trace_name):
        return [
            (
                ""
                if i == 0
                and self.trace_names_to_prevent_hover_of_first_point is not None
                and trace_name in self.trace_names_to_prevent_hover_of_first_point
                else self._get_custom_hover_template(i, df, trace_name)
            )
            for i in range(df.shape[0])  # the number of rows in df
        ]

    def _get_custom_hover_template(self, i, df, trace_name):
        hover_text_headers = self.hover_data[trace_name][HOVER_TEXT_HEADERS]
        if (
            self.hover_data_for_traces_with_different_hover_for_last_point is not None
            and trace_name
            in self.hover_data_for_traces_with_different_hover_for_last_point
            and i == df.shape[0] - 1
        ):
            hover_text_headers = (
                self.hover_data_for_traces_with_different_hover_for_last_point[
                    trace_name
                ][HOVER_TEXT_HEADERS]
            )
        # pylint: disable=duplicate-code

        return (
            f"{trace_name}<br>"
            f"{hover_text_headers[0]}"
            ": %{customdata[0]}<br>"
            f"{hover_text_headers[1]}"
            ": %{customdata[1]}<extra></extra>"
        )

    def _get_custom_data(self, df, trace_name):
        # For last points of trace_name in [], we want different custom data.
        customdata = df[self.hover_data[trace_name][CUSTOM_DATA]]
        if (
            self.hover_data_for_traces_with_different_hover_for_last_point is not None
            and trace_name
            in self.hover_data_for_traces_with_different_hover_for_last_point
        ):
            customdata = [
                (
                    [df[col][i] for col in self.hover_data[trace_name][CUSTOM_DATA]]
                    if i < df.shape[0] - 1
                    else [
                        df[col][i]
                        for col in self.hover_data_for_traces_with_different_hover_for_last_point[
                            trace_name
                        ][
                            CUSTOM_DATA
                        ]
                    ]
                )  # Use different columns for the last point
                for i in range(df.shape[0])
            ]
        return customdata

    def _get_trace_name(self, trace_name):
        if self.legend_dict is not None and trace_name in self.legend_dict:
            return self.legend_dict[trace_name]
        return trace_name

    def _get_x_axis_content(self):
        """Generates tick text and values for the x-axis based on the unique years calculated from
        the DATE_VALID column in the dataframe.
        Returns:
            tuple: A tuple containing tick_text, tick_values and range_x.
        """
        if self.xaxis_tick_text_format == XAxisFormat.YEAR.value:
            df_with_year_column = self.filtered_df.with_columns(
                pl.col(self.x_axis_column)
                .str.strptime(pl.Date, "%Y-%m-%d")
                .dt.year()
                .alias(YEAR)
            )
            date_list = df_with_year_column[self.x_axis_column].unique().to_list()
            min_date_string = min(date_list)
            max_date_string = max(date_list)
            min_datetime = datetime.strptime(min_date_string, "%Y-%m-%d")
            max_datetime = datetime.strptime(max_date_string, "%Y-%m-%d")
            year_list = df_with_year_column[YEAR].unique().to_list()
            tick_text = list(range(min(year_list) - 1, max(year_list) + 2))
            tick_values = [date(year, 1, 1) for year in tick_text]
            range_x = [
                min_datetime - relativedelta(months=6),
                max_datetime + relativedelta(months=6),
            ]

        elif self.xaxis_tick_text_format == XAxisFormat.MONTH_YEAR.value:
            df = self.filtered_df.with_columns(
                pl.col(self.x_axis_column)
                .str.strptime(pl.Date, "%Y-%m-%d")
                .alias(self.x_axis_column)
            ).sort(self.x_axis_column)

            start_datetime = datetime(2024, 7, 1).date()
            latest_datetime = df[self.x_axis_column].max()
            tick_text = []
            current = start_datetime
            while current <= latest_datetime:
                tick_text.append(current.strftime("%b %Y"))
                current += relativedelta(months=1)

            tick_text_length = len(tick_text)
            total_tick_points = int((tick_text_length / 5) * 7)
            additional_tick_points = total_tick_points - tick_text_length

            last_current_tick_text = datetime.strptime(tick_text[-1], "%b %Y")

            for x in range(additional_tick_points):
                tick_text = tick_text + [
                    (last_current_tick_text + relativedelta(months=x + 1)).strftime(
                        "%b %Y"
                    )
                ]

            tick_values = [
                datetime.strptime(month_year, "%b %Y").replace(day=1)
                for month_year in tick_text
            ]

            range_x = [
                tick_values[0],
                tick_values[-1] + relativedelta(months=1),
            ]
            tick_text = replace_jun_jul_month_abbreviations(tick_text)
        elif self.xaxis_tick_text_format == XAxisFormat.FINANCIAL_QUARTER.value:
            tick_values = [1, 2, 3, 4]
            tick_text = [
                convert_financial_quarter_to_financial_quarter_text(quarter)
                for quarter in tick_values
            ]

            range_x = [0.5, 4.5]
        else:
            raise ValueError(
                f"Invalid xaxis_tick_text_format: {self.xaxis_tick_text_format}"
            )
        return tick_text, tick_values, range_x

    def _get_y_axis_range_max(self):
        """Get the y axis range maximum value to ensure there is an axis label greater than the
        maximum y value."""
        largest_number_of_weeks = self.filtered_df[self.y_axis_column].max()

        y_axis_max = largest_number_of_weeks + (0.3 * largest_number_of_weeks)
        return y_axis_max

    def _get_df_list_for_time_series(self) -> list[pl.DataFrame]:
        if self.trace_name_column is not None:
            df_list = [
                self.filtered_df.filter(pl.col(self.trace_name_column) == trace_name)
                for trace_name in self.trace_name_list
            ]
        else:
            df_list = [self.filtered_df]
        return df_list

    def _get_colour_list(self):
        """Returns a list of colours."""
        number_of_traces = len(self.trace_name_list)
        if number_of_traces == 2:
            colour_list = [
                AFAccessibleColours.DARK_BLUE.value,
                AFAccessibleColours.ORANGE.value,
            ]  # if 2 lines should use dark blue & orange as have highest contrast ratio
        else:
            colour_list = AFAccessibleColours.CATEGORICAL.value.copy()
        colour_shift_dict = (
            {"default": 0}
            if self.number_of_traces_colour_shift_dict is None
            else self.number_of_traces_colour_shift_dict
        )

        colour_shift_value = colour_shift_dict.get(
            number_of_traces, colour_shift_dict["default"]
        )
        if isinstance(colour_shift_value, list):
            return colour_shift_value  # list of colours
        while colour_shift_value > 0:
            colour_list.append(colour_list.pop(0))
            colour_shift_value -= 1
        return colour_list
