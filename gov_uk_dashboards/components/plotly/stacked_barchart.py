"""stacked_barchart function"""

import math
from typing import Optional
from dash import html
import polars as pl

import plotly.graph_objects as go

from gov_uk_dashboards.constants import (
    CHART_LABEL_FONT_SIZE,
    CUSTOM_DATA,
    DATE_VALID,
    FINANCIAL_YEAR_ENDING,
    HOVER_TEXT_HEADERS,
    MAIN_TITLE,
    MEASURE,
    SUBTITLE,
    VALUE,
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
)
from gov_uk_dashboards.components.plotly.enums import (
    HoverDataByTrace,
    TitleDataStructure,
    XAxisFormat,
)
from gov_uk_dashboards.formatting.human_readable import format_as_human_readable

from gov_uk_dashboards.components.helpers.update_layout_bgcolor_margin import (
    update_layout_bgcolor_margin,
)


class StackedBarChart:
    """Class for use in generating stacked bar charts."""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals
    # pylint: disable = too-many-positional-arguments
    def __init__(
        self,
        title_data: TitleDataStructure,
        y_column: str,
        hover_data: HoverDataByTrace,
        df: pl.DataFrame,
        trace_name_list: list[str],
        trace_name_column: Optional[str] = None,
        xaxis_tick_text_format: XAxisFormat = XAxisFormat.YEAR.value,
        line_trace_name: Optional[str] = None,
        x_axis_column=DATE_VALID,
        download_chart_button_id: Optional[str] = None,
        download_data_button_id: Optional[str] = None,
    ):
        """Initializes the StackedBarChart instance.
        To display the chart, call the `get_stacked_bar_chart()` method.

        Args:
            title_data (TitleDataStructure): Data structure containing the chart title information.
            y_column (str): The column name representing the Y-axis data.
            hover_data (HoverDataByTrace): Data structure for hover information.
            df (pl.DataFrame): The dataset for the chart.
            trace_name_list (list[str]): List of trace names for the stacked bars.
            trace_name_column (Optional[str], optional): Column name representing trace categories,
                if applicable. Defaults to None.
            xaxis_tick_text_format (XAxisFormat, optional): Format for X-axis tick labels.
                Defaults to XAxisFormat.YEAR.value.
            line_trace_name (Optional[str], optional): Name for an optional line trace overlay,
                must be in MEASURE column of df, line_trace_name will display in legend.
                Defaults to None.
            x_axis_column (_type_, optional): The column used for the X-axis values.
                Defaults to DATE_VALID.
            download_chart_button_id (Optional[str], optional): ID for the chart download button,
                if applicable. Defaults to None.
            download_data_button_id (Optional[str], optional): ID for the data download button, if
                applicable. Defaults to None.
        """
        self.title_data = title_data
        self.y_axis_column = y_column
        self.hover_data = hover_data
        self.df = df
        self.trace_name_list = trace_name_list
        self.trace_name_column = trace_name_column
        self.xaxis_tick_text_format = xaxis_tick_text_format
        self.line_trace_name = line_trace_name
        self.x_axis_column = x_axis_column
        self.download_chart_button_id = download_chart_button_id
        self.download_data_button_id = download_data_button_id
        self.fig = self.create_stacked_bar_chart()

    def get_stacked_bar_chart(self) -> html.Div:
        """Creates and returns stacked bar chart for display on application.

        Returns:
            html.Div: Styled div containing title, subtile and chart.
        """
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

    def create_stacked_bar_chart(
        self,
    ):
        """generates a stacked bar chart"""
        # pylint: disable=too-many-locals
        fig = go.Figure()
        colour_list = (
            AFAccessibleColours.CATEGORICAL.value
            if len(self.trace_name_list) != 2
            else [
                AFAccessibleColours.DARK_BLUE.value,
                AFAccessibleColours.ORANGE.value,
            ]  # if 2 lines should use dark blue & orange as have highest contrast ratio
        )
        for _, (df, trace_name, colour) in enumerate(
            zip(
                self._get_df_list_for_time_series(),
                self.trace_name_list,
                colour_list,
            )
        ):
            fig.add_trace(
                self.create_bar_chart_trace(
                    df.sort(self.x_axis_column),
                    trace_name,
                    hover_label=None,
                    colour=colour,
                )
            )

        if self.line_trace_name is not None:
            colour = AFAccessibleColours.CATEGORICAL.value[len(self.trace_name_list)]
            df = self.df.filter(pl.col(MEASURE) == self.line_trace_name)

            fig.add_trace(
                go.Scatter(
                    x=df[FINANCIAL_YEAR_ENDING],
                    y=df[VALUE],
                    customdata=self._get_custom_data(self.line_trace_name, df),
                    mode="lines",
                    line={"color": colour, "width": 3},
                    name=self.line_trace_name,
                    hovertemplate=self._get_hover_template(self.line_trace_name),
                    legendrank=99999,  # a high number to ensure it is bottom of the legend
                )
            )

        max_y, min_y, tickvals, ticktext = _get_y_range_tickvals_and_ticktext(
            self.df, "£", self.trace_name_list
        )
        update_layout_bgcolor_margin(fig, "#FFFFFF")

        fig.update_layout(
            legend=get_legend_configuration(),
            font={"size": CHART_LABEL_FONT_SIZE},
            yaxis={
                "range": [min_y * 1.1, max_y * 1.1],
                "tickmode": "array",
                "tickvals": tickvals,
                "ticktext": ticktext,
            },
            showlegend=True,
            barmode="relative",
            xaxis={"categoryorder": "category ascending"},
        )
        return fig

    def _format_x_axis(self, fig):
        tick_text, tick_values, range_x = self._get_x_axis_content()
        fig.update_xaxes(
            tickvals=tick_values,
            ticktext=tick_text,
            tickmode="array",
            range=range_x,
        )

        return tick_values

    def create_bar_chart_trace(
        self,
        df: pl.DataFrame,
        trace_name: str,
        hover_label: dict[str, str],
        colour: str,
    ):
        """Creates a trace for the plot.

        Args:
            df (pl.DataFrame): Dataframe to use to create trace. Must contain x and y columns,
            and columns defined in self.hover_data[CUSTOM_DATA].
            trace_name (str): Name of trace.
            hover_label (dict[str,str]): Properties for hoverlabel parameter.
            colour (str): Colour for bar.
        """

        return go.Bar(
            x=df[self.x_axis_column],
            y=df[self.y_axis_column],
            name=trace_name,
            hovertemplate=[
                self._get_hover_template(trace_name) for i in range(df.shape[0])
            ],
            customdata=self._get_custom_data(trace_name, df),
            hoverlabel=hover_label,
            marker={"color": colour},
        )

    def _get_hover_template(self, trace_name):
        hover_text_headers = self.hover_data[trace_name][HOVER_TEXT_HEADERS]
        hover_template = (
            f"{trace_name}<br>"
            f"{hover_text_headers[0]}"
            ": %{customdata[0]}<br>"
            f"{hover_text_headers[1]}"
            ": %{customdata[1]}<extra></extra>"
        )
        return hover_template

    def _get_custom_data(self, trace_name, df):
        customdata = df[self.hover_data[trace_name][CUSTOM_DATA]]
        return customdata

    def _get_x_axis_content(self):
        """Generates tick text and values for the x-axis based on the unique years calculated from
        the FINANCIAL_YEAR_ENDING column in the dataframe.
        Returns:
            tuple: A tuple containing tick_text, tick_values and range_x.
        """
        if self.xaxis_tick_text_format == XAxisFormat.YEAR.value:
            year_list = self.df[FINANCIAL_YEAR_ENDING].unique().to_list()
            int_min_year = int(min(year_list))
            int_max_year = int(max(year_list))

            tick_text = []
            year = int_min_year
            while year <= int_max_year:
                tick_text.append(str(year + 1))
                year = year + 1

            tick_values = tick_text

            range_x = [
                tick_values[0],
                tick_values[-1],
            ]
        else:
            raise ValueError(
                f"Invalid xaxis_tick_text_format: {self.xaxis_tick_text_format}"
            )
        return tick_text, tick_values, range_x

    def _get_df_list_for_time_series(self) -> list[pl.DataFrame]:
        if self.trace_name_column is not None:
            df_list = [
                self.df.filter(pl.col(self.trace_name_column) == trace_name)
                for trace_name in self.trace_name_list
            ]
        else:
            df_list = [self.df]
        return df_list


def _get_y_range_tickvals_and_ticktext(
    dataframe: pl.DataFrame, tick_prefix: str, yaxis_with_values: list[str]
):
    barchart_df = dataframe.pivot(
        index=FINANCIAL_YEAR_ENDING, columns=MEASURE, values=VALUE
    )
    positive_sum = sum(
        pl.when(pl.col(col) > 0).then(pl.col(col)).otherwise(0)
        for col in yaxis_with_values
    )
    negative_sum = sum(
        pl.when(pl.col(col) < 0).then(pl.col(col)).otherwise(0)
        for col in yaxis_with_values
    )
    barchart_df = barchart_df.with_columns(positive_sum.alias("Positive sum"))
    barchart_df = barchart_df.with_columns(negative_sum.alias("Negative sum"))
    maxy = barchart_df.select([pl.col("Positive sum").max()]).item()
    miny = barchart_df.select([pl.col("Negative sum").min()]).item()
    tickvals = _generate_tickvals(maxy, miny)
    ticktext = [format_as_human_readable(val, prefix=tick_prefix) for val in tickvals]
    return tickvals[-1], tickvals[0], tickvals, ticktext


def _generate_tickvals(maxy, miny):
    range_size = maxy - miny

    # Determine the order of magnitude of the range
    order = int(math.log10(range_size))

    # Start with an initial step size
    step_size = 10**order

    # Calculate the number of ticks based on the step size
    num_ticks = math.ceil(range_size / step_size)

    # Adjust step size to ensure the number of ticks is between 6 and 10
    while num_ticks < 6 or num_ticks > 10:
        if num_ticks < 6:  # Too few ticks -> decrease step size
            step_size /= 2
        elif num_ticks > 10:  # Too many ticks -> increase step size
            step_size *= 2
        num_ticks = math.ceil(range_size / step_size)

    # Adjust the start and end of the range to align with the step size
    start = math.floor(miny / step_size) * step_size
    end = math.ceil(maxy / step_size) * step_size

    # Generate tick values
    tickvals = list(range(int(start), int(end) + 1, int(step_size)))
    return tickvals
