"""Choropleth map class"""

import polars as pl
import plotly.graph_objects as go
from dash import dcc
from gov_uk_dashboards import colours
from gov_uk_dashboards.components.display_chart_or_table_with_header import (
    display_chart_or_table_with_header,
)


class ChoroplethMap:
    """Class for  generating choropleth map charts.
    Note: dataframe_function must contain columns: 'Region', 'Area_Code', 'Local authority',
    category_column, column_to_plot, custom_data"""

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-few-public-methods
    def __init__(
        self,
        dataframe_function,
        region,
        get_geos_function,
        category_column,
        column_to_plot,
        desired_category_order,
        custom_data,
        hover_header_list,
        download_data_button_id,
        legend_title_text=None,
        **choropleth_properties,
    ):
        self.dataframe = dataframe_function()
        self.region = region
        self.geographic_boundaries = get_geos_function()
        self.boundaries_by_area = self._get_boundaries_by_area(self.dataframe)
        self.category_column = category_column
        self.column_to_plot = column_to_plot
        self.df_dict = self._get_dataframe_dict_by_category()
        self.desired_category_order = desired_category_order
        self.colours_list = self._get_colour_list()
        self.custom_data = custom_data
        self.hover_header_list = hover_header_list
        self.download_data_button_id = download_data_button_id
        self.legend_title_text = legend_title_text
        self.fig = go.Figure()
        self.choropleth_properties = choropleth_properties

    def get_choropleth_map(self):
        """Creates and returns choropleth map chart for display on application.

        Returns:
            html.Div: Styled div containing title, subtile and chart.
        """
        self._update_fig()
        choropleth_map = dcc.Graph(
            id="local-authority-choropleth",
            responsive=True,
            config={"topojsonURL": "/assets/topojson/", "displayModeBar": False},
            figure=self.fig,
            style={
                "height": "750px",
                "width": "100%",
            },  # height hard-coded so that map always displays within tab
        )
        return display_chart_or_table_with_header(
            choropleth_map, download_data_button_id=self.download_data_button_id
        )

    def _update_fig(self):
        self._add_traces()
        self._handle_missing_data()
        self._crop_to_region()
        self._remove_background_map()

    def _get_dataframe_dict_by_category(self):
        if self.region is not None and self.region != "England":
            self.dataframe = self.dataframe.filter(pl.col("Region") == self.region)
        else:
            self.dataframe = self.dataframe
        grouped_dfs_dict_keys_as_tuples = self.dataframe.partition_by(
            self.category_column, as_dict=True
        )
        grouped_dfs_dict = {
            key[0]: value for key, value in grouped_dfs_dict_keys_as_tuples.items()
        }
        return grouped_dfs_dict

    def _get_boundaries_by_area(self, dataframe):
        las_to_display = dataframe["Area_Code"].to_list()
        filtered_boundaries = {
            key: (
                value
                if key != "features"
                else [
                    features
                    for features in value
                    if features["properties"]["geo_id"] in las_to_display
                ]
            )
            for key, value in self.geographic_boundaries.items()
        }
        return filtered_boundaries

    def _add_traces(self):
        for count, category in enumerate(self.desired_category_order):
            if category not in self.df_dict:
                df = self._create_df_for_empty_trace(category)
            else:
                df = self.df_dict[category]
            colour = self.colours_list[count % len(self.colours_list)]
            self.fig.add_trace(
                self._create_choropleth_trace(
                    df,
                    colour,
                )
            )

    def _create_df_for_empty_trace(self, category):
        """Method to create df where all columns are empty except for the category column to force
        all legend items to always appear"""
        columns = next(iter(self.df_dict.values())).columns
        data = {col: [None] for col in columns}
        data[self.category_column] = [category]
        return pl.DataFrame(data)

    def _create_choropleth_trace(
        self,
        dataframe,
        colour,
        column_to_plot=None,
        is_missing_data=False,
        marker=None,
    ):
        # pylint: disable=too-many-positional-arguments
        """Return a chlorepleth trace set up for UK LAs, with optional configuration for markers"""
        if not column_to_plot:
            column_to_plot = self.column_to_plot
        if not is_missing_data:
            hovertemplate = (
                "<b>%{hovertext}</b><br>"
                + "<br>".join(
                    f"{header}: " + "%{customdata[" + str(i) + "]}"
                    for i, header in enumerate(self.hover_header_list)
                )
                + "<br><br><extra></extra>"
            )
        else:
            hovertemplate = (
                "<b>%{customdata[0]}</b><br>" + "%{hovertext}<extra></extra>"
            )
        return go.Choropleth(
            geojson=self.geographic_boundaries,
            featureidkey="properties.geo_id",
            locations=dataframe["Area_Code"],
            locationmode="geojson-id",
            z=dataframe[column_to_plot],
            hovertext=(
                dataframe["Local authority"]
                if not is_missing_data
                else ["No data available"] * len(dataframe["Local authority"])
            ),
            customdata=(
                dataframe[self.custom_data]
                if not is_missing_data
                else dataframe[["Local authority"]]
            ),
            hovertemplate=hovertemplate,
            marker=marker,
            marker_line_color=colours.GovUKColours.DARK_GREY.value,
            showscale=False,
            showlegend=True,
            colorscale=[
                [0, colour],
                [1, colour],
            ],  # dataframe is grouped by column_to_plot, hence only
            # contains one value for column_to_plot- this ensures a discrete categorical colourscale
            # for trace
            name=(
                dataframe[self.category_column][0]
                if not is_missing_data
                else "No data available"
            ),
            **self.choropleth_properties,
        )

    def _handle_missing_data(self):
        missing_data = self.dataframe.filter(pl.col(self.column_to_plot).is_null())
        missing_data = missing_data.with_columns(pl.lit(0).alias("data"))

        if not missing_data.is_empty():
            self.fig.add_trace(
                self._create_choropleth_trace(
                    missing_data,
                    colours.GovUKColours.MID_GREY.value,
                    column_to_plot="data",
                    is_missing_data=True,
                )
            )

    def _crop_to_region(self):
        self.fig.update_layout(
            {
                "margin": {"r": 0, "t": 0, "l": 0, "b": 0},
                "geo": {
                    "bgcolor": "rgba(0, 0, 0, 0)",
                    "fitbounds": "locations",
                },
                "coloraxis_colorbar_title_text": "",
                "dragmode": False,  # fixes and not zoomable
                "legend_x": 0.9,
                "legend_y": 0.95,
                "legend_title_text": self.legend_title_text,
            },
        )

    def _remove_background_map(self):
        self.fig.update_geos(
            center={"lat": 53, "lon": -2},
            visible=False,
            projection_type="mercator",
        )

    def _get_colour_list(self):
        """Amends colour list based on the number of categories"""
        colour_list = ["#217847", "#23BBBE", "#8CCE69", "#FFEA80"]
        if len(self.desired_category_order) == 3:
            colour_list.pop(1)
        return colour_list
