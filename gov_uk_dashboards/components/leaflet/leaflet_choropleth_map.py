"""Leaflet choropleth map class"""

from typing import Optional
from dash_extensions.javascript import arrow_function, Namespace
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import html
import polars as pl

from gov_uk_dashboards.components.helpers.display_chart_or_table_with_header import (
    display_chart_or_table_with_header,
)
from gov_uk_dashboards.formatting.number_formatting import (
    format_number_into_thousands_or_millions,
)


class LeafletChoroplethMap:
    """Class for  generating leaflet choropleth map charts.
    Note: Values in the numeric column should use 1 for the highest value, with larger numbers
    representing lower values.
    If color_scale_is_discrete is false, colour scale will be continuous, otherwise it will be
    discrete"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments

    def __init__(
        self,
        geojson: dict,
        df: pl.DataFrame,
        hover_text_columns: list[str],
        column_to_plot: str,
        legend_column: str,
        area_column: str,
        title: str,
        instance_number: int,
        subtitle: Optional[str] = None,
        enable_zoom: bool = True,
        download_chart_button_id: Optional[str] = None,
        download_data_button_id: Optional[str] = None,
        color_scale_is_discrete: bool = True,
        show_tile_layer: bool = False,
    ):
        self.geojson_data = geojson
        self.df = df
        self.hover_text_columns = hover_text_columns
        self.column_to_plot = column_to_plot
        self.legend_column = legend_column
        self.area_column = area_column
        self.title = title
        self.subtitle = subtitle
        self.enable_zoom = enable_zoom
        self.download_chart_button_id = download_chart_button_id
        self.download_data_button_id = download_data_button_id
        self.color_scale_is_discrete = color_scale_is_discrete
        self.show_tile_layer = show_tile_layer
        self._add_data_to_geojson()
        self.instance_number = instance_number

    def get_leaflet_choropleth_map(self):
        """Creates and returns leaflet choropleth map chart for display on application.

        Returns:
            dl.Map: A dash leaflet map chart.
        """
        disabled_zoom_controls = {
            "scrollWheelZoom": False,
            "dragging": False,
            "zoomControl": False,
            "doubleClickZoom": False,
            "touchZoom": False,
        }
        zoom_controls = {} if self.enable_zoom else disabled_zoom_controls
        choropleth_map = dl.Map(
            children=[
                dl.TileLayer() if self.show_tile_layer else None,
                self._get_colorbar(),
                self._get_colorbar_title(self.enable_zoom),
                self._get_dl_geojson(),
            ],
            center=[54.5, -2.5],  # Centered on the UK
            zoom=6.5,
            minZoom=6.5,
            maxZoom=10 if self.enable_zoom else 6.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
            **zoom_controls,
            attributionControl=False,
            style={"width": "100%", "height": "960px", "background": "white"},
        )
        download_choropleth_map = dl.Map(
            children=[
                dl.TileLayer() if self.show_tile_layer else None,
                self._get_colorbar(),
                self._get_colorbar_title(),
                self._get_dl_geojson(),
            ],
            center=[54.5, -25.0],
            zoom=7.5,
            maxBounds=[[49.5, -30], [60, 2]],
            zoomControl=False,
            attributionControl=False,
            style={"width": "1200px", "height": "1200px", "background": "white"},
        )
        choropleth_map = display_chart_or_table_with_header(
            choropleth_map,
            self.title,
            self.subtitle,
            None,
            self.download_data_button_id,
            self.download_chart_button_id,
            None,
            instance=self.instance_number,
        )
        download_choropleth_map_display = display_chart_or_table_with_header(
            download_choropleth_map,
            self.title,
            self.subtitle,
        )

        return [
            choropleth_map,
            html.Div(
                [download_choropleth_map_display],
                id=f"{self.download_chart_button_id}-hidden-map-container",
                style={
                    "position": "absolute",
                    "top": "-10000px",
                    "left": "-10000px",
                },  # hide off screen
            ),
        ]

    def _add_data_to_geojson(self):
        info_map = {
            row["Area_Code"]: {
                "value": row[self.column_to_plot],
                "area": row[self.area_column],
                **{col: row[col] for col in self.hover_text_columns},
            }
            for row in self.df.iter_rows(named=True)
        }

        for feature in self.geojson_data["features"]:
            region_code = feature["properties"]["geo_id"]
            info = info_map.get(region_code)
            if info:

                feature["properties"]["density"] = info["value"]
                feature["properties"]["area"] = info["area"]

                tooltip_parts = [f"<b>{info['area']}</b>"]
                if info["value"] is None:
                    tooltip_parts.append("<br>No data available")
                else:
                    for col in self.hover_text_columns:
                        tooltip_parts.append(f"<br>{col}: {info[col]}")

                feature["properties"]["tooltip"] = "".join(tooltip_parts)
            else:
                feature["properties"]["density"] = None
                feature["properties"]["area"] = "Unknown"
                feature["properties"]["tooltip"] = "No data available"

    def _get_dl_geojson(self):
        style_handle = self._get_style_handle()
        colorscale = self._get_colorscale()
        style = {
            "weight": 2,
            "opacity": 1,
            "color": "white",
            "fillOpacity": 0.7 if self.show_tile_layer else 1,
        }
        hover_style = arrow_function({"weight": 5, "color": "#666", "dashArray": ""})
        return dl.GeoJSON(
            data=self.geojson_data,
            id="geojson",
            zoomToBounds=True,
            zoomToBoundsOnClick=True,
            style=style_handle,
            hoverStyle=hover_style,
            hideout={
                "colorscale": colorscale,  # Use hex strings
                "style": style,
                "colorProp": "density",
                "min": self.df[self.column_to_plot].min(),
                "max": self.df[self.column_to_plot].max(),
            },
        )

    def _get_style_handle(self):
        ns = Namespace("myNamespace", "mapColorScaleFunctions")
        if self.color_scale_is_discrete:
            return ns("discreteColorScale")
        return ns("continuousColorScale")

    def _get_colorscale(self):
        if self.color_scale_is_discrete:
            discrete_colours = ["#217847", "#23BBBE", "#8CCE69", "#FFEA80"]
            if len(self.df[self.column_to_plot].unique()) == 3:
                discrete_colours.pop(1)
            return discrete_colours
        return ["#B0F2BC", "#257D98"]

    def _get_color_bar_categories(self):
        return (
            self.df.select([self.legend_column, self.column_to_plot])
            .unique()
            .sort(self.column_to_plot, descending=True)
            .select(self.legend_column)
            .to_series()
            .to_list()
        )

    def _get_colorbar(self):
        if self.color_scale_is_discrete:
            self._get_color_bar_categories()
            return dlx.categorical_colorbar(
                categories=self._get_color_bar_categories(),  # reversed order
                colorscale=self._get_colorscale()[::-1],
                width=30,
                height=200,
                position="topleft",
                style={
                    "padding": "6px",
                    "backgroundColor": "white",
                    "borderRadius": "4px",
                    "fontSize": "16px",
                },
            )
        min_value = self.df.select(pl.min(self.column_to_plot)).item()
        colorbar_min = min(min_value, 0)
        max_value = self.df.select(pl.max(self.column_to_plot)).item()
        mid_value = (colorbar_min + max_value) / 2
        quarter_value = (colorbar_min + max_value) / 4
        three_quarter_value = 3 * (colorbar_min + max_value) / 4
        tick_values = [
            colorbar_min,
            quarter_value,
            mid_value,
            three_quarter_value,
            max_value,
        ]
        tick_text = [
            format_number_into_thousands_or_millions(x) for x in tick_values
        ]  # Optional, for formatting

        return dl.Colorbar(
            colorscale=self._get_colorscale(),
            width=20,
            height=200,
            min=colorbar_min,
            max=max_value,
            position="topleft",
            style={
                "backgroundColor": "white",
                "padding": "5px",
                "borderRadius": "4px",
                "marginTop": "100px",
            },
            tickValues=tick_values,
            tickText=tick_text,  # Optional, makes labels look cleaner
        )

    def _get_colorbar_title(self, enable_zoom: bool = False):
        if self.color_scale_is_discrete:
            return None
        top = "70px" if enable_zoom is False else "140px"
        return html.Div(
            self.hover_text_columns[0],
            style={
                "position": "absolute",
                "top": top,  # Adjusted to place above the colorbar
                "left": "10px",  # Align with the left side of the colorbar
                "background": "white",
                "padding": "2px 6px",
                "borderRadius": "5px",
                "fontWeight": "bold",
                "fontSize": "14px",
                "zIndex": "999",  # Ensure it appears above map elements
            },
        )
