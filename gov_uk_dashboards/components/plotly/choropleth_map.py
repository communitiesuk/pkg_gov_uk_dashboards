"""Choropleth map class"""

from constants import DEFAULT_COLOURSCALE
import polars as pl
import plotly.graph_objects as go
from dash import dcc
from gov_uk_dashboards import colours
from gov_uk_dashboards.components.display_chart_or_table_with_header import (
    display_chart_or_table_with_header,
)

class ChoroplethMap:
    """Class for  generating choropleth map charts.
    Note: dataframe_function must contain columns: 'Region', 'Area_Code',
    category_column, column_to_plot, custom_data"""

    def __init__(
        self,
        map_name: str,
        get_dataframe: callable,
        get_geos: callable,
        region: str,
        area_focus_level: str,
        column_to_plot: str,
        hover_header_list: list[str],
        hover_data_list: list[str],
        category_column: str = None,
        desired_category_order: list[str] = None,
        legend_title_text: str = None,
        **choropleth_properties
    ):
        self.map_name = map_name
        self.dataframe = get_dataframe()
        self.geographic_boundaries = get_geos()
        self.region = region
        self.area_focus_level = area_focus_level
        self.column_to_plot = column_to_plot
        self.hover_header_list = hover_header_list
        self.hover_data_list = hover_data_list

        self.category_column = category_column
        self.legend_title_text = legend_title_text
        self.desired_category_order = desired_category_order
        self.choropleth_properties = choropleth_properties

        self.fig = go.Figure()
        self.discrete_map = (self.category_column != None and self.desired_category_order != None)
        if self.discrete_map:
            self.df_dict = self._get_dataframe_dict_by_category()
            self.colours_list = self._get_colour_list()
    
    def _get_choropleth_map(self):
        """Creates and returns choropleth map chart for display on application.

        Returns:
            html.Div: Styled div containing title, subtile and chart.
        """
        self._update_fig()
        choropleth_map = dcc.Graph(
            id=f"{self.map_name}-choropleth",
            responsive=True,
            config={"topojsonURL": "/assets/topojson/", "displayModeBar": False},
            figure=self.fig,
            style={
                "height": "750px",
                "width": "100%",
            },  # height hard-coded so that map always displays within tab
        )
        return display_chart_or_table_with_header(
            choropleth_map, download_data_button_id=f"{self.map_name}-download-btn"
        )
    
    def _update_fig(self):
        self._add_traces()
        self._handle_missing_data()
        self._crop_to_region()
        self._remove_background_map()

    def _create_choropleth_trace(
        self,
        dataframe,
        colourscale,
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
                dataframe[self.area_focus_level]
                if not is_missing_data
                else ["No data available"] * len(dataframe[self.area_focus_level])
            ),
            customdata=(
                dataframe[self.hover_data_list]
                if not is_missing_data
                else dataframe[[self.area_focus_level]]
            ),
            colorbar=self._get_color_bar(),
            hovertemplate=hovertemplate,
            marker=marker,
            marker_line_color=colours.GovUKColours.DARK_GREY.value,
            showscale=self._get_scale(),
            showlegend=self._get_legend(),
            colorscale=colourscale,  # dataframe is grouped by column_to_plot, hence only
            # contains one value for column_to_plot- this ensures a discrete categorical colourscale
            # for trace
            name=self._get_trace_name(
                dataframe, is_missing_data
            ),
            **self.choropleth_properties,
        )


    def _add_traces(self):
        if(not self.discrete_map):
            self.fig.add_trace(
                self._create_choropleth_trace(
                    self.dataframe,
                    DEFAULT_COLOURSCALE
                )
            )
        else:
            for count, category in enumerate(self.desired_category_order):
                if category not in self.df_dict:
                    df = self._create_df_for_empty_trace(category)
                else:
                    df = self.df_dict[category]
                colour = [
                    [0, self.colours_list[count % len(self.colours_list)]],
                    [1, self.colours_list[count % len(self.colours_list)]]
                ]
                self.fig.add_trace(
                    self._create_choropleth_trace(
                        df,
                        colour,
                    )
                )
    
    def _handle_missing_data(self):
        missing_data = self.dataframe.filter(pl.col(self.column_to_plot).is_null())
        missing_data = missing_data.with_columns(pl.lit(0).alias("data"))

        colour = [
                    [0, colours.GovUKColours.MID_GREY.value],
                    [1, colours.GovUKColours.MID_GREY.value]
                ]
        if not missing_data.is_empty():
            self.fig.add_trace(
                self._create_choropleth_trace(
                    missing_data,
                    colour,
                    column_to_plot="data",
                    is_missing_data=True,
                )
            )

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

    def _get_color_bar(self):
        if self.discrete_map: 
            return None

        return dict(
            title=self.column_to_plot,
            thickness=20,   # Adjust the thickness of the colorbar
            len=0.8,        # Adjust the length of the colorbar
            x=0.9,          # Position the colorbar horizontally (0-1 scale)
            y=0.5,
        )

    def _get_scale(self):
        return not self.discrete_map
    
    def _get_legend(self):
        return self.discrete_map

    def _get_trace_name(self, dataframe, missing_data = False):
        if self.category_column == None:
            return None

        if not missing_data:
            return dataframe[self.category_column][0]
        
        return "No data available"

    def _remove_background_map(self):
        self.fig.update_geos(
            center={"lat": 53, "lon": -2},
            visible=False,
            projection_type="mercator",
        )

    def _get_colour_list(self):
        """Amends colour list based on the number of categories"""
        colour_list = ["#217847", "#23BBBE", "#8CCE69", "#FFEA80"]

        if self.discrete_map and len(self.desired_category_order) == 3:
            colour_list.pop(1)
        return colour_list