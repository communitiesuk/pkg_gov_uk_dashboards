"""Leaflet choropleth map class"""

from dash_extensions.javascript import arrow_function, Namespace
import dash_leaflet as dl
from dash import html
import polars as pl

from gov_uk_dashboards.formatting.number_formatting import (
    format_number_into_thousands_or_millions,
)


class LeafletChoroplethMap:
    """Class for  generating leaflet choropleth map charts.
    Note: dataframe_function must contain columns: 'Region', 'Area_Code',
    column_to_plot, hover_text_columns
    If color_scale_is_discrete is false, colour scale will be continuous, otherwise it will be
    discrete"""

    # pylint: disable=too-few-public-methods

    def __init__(
        self,
        get_geojson_function,
        get_df_function,
        hover_text_columns,
        color_scale_is_discrete=True,
    ):
        self.geojson_data = get_geojson_function()
        self.df = get_df_function()
        self.hover_text_columns = hover_text_columns
        self.color_scale_is_discrete = color_scale_is_discrete
        self._add_data_to_geojson()

    def get_leaflet_choropleth_map(self):
        """Creates and returns leaflet choropleth map chart for display on application.

        Returns:
            dl.Map: A dash leaflet map chart.
        """
        return dl.Map(
            children=[
                dl.TileLayer(),
                self._get_colorbar(),
                self._get_colorbar_title(),
                self._get_dl_geojson(),
            ],
            center=[54.5, -2.5],  # Centered on the UK
            zoom=6.5,
            minZoom=6.5,
            maxZoom=6.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
            scrollWheelZoom=False,  # Disable zooming via mouse scroll
            dragging=False,  # Optional: prevent dragging too if you want
            zoomControl=False,  # Hide the zoom buttons (+/-)
            doubleClickZoom=False,  # Prevent double click zoom
            touchZoom=False,  # Prevent pinch zoom
            attributionControl=False,
            style={"width": "100%", "height": "800px", "background": "white"},
        )

    def _add_data_to_geojson(self):
        info_map = {
            row["Area_Code"]: {
                "value": row["Value"],
                "region": row["Region"],
                **{col: row[col] for col in self.hover_text_columns},
            }
            for row in self.df.iter_rows(named=True)
        }

        for feature in self.geojson_data["features"]:
            region_code = feature["properties"]["geo_id"]
            info = info_map.get(region_code)
            if info:

                feature["properties"]["density"] = info["value"]
                feature["properties"]["region"] = info["region"]

                tooltip_parts = [f"<b>{info['region']}</b>"]
                if info["value"] is None:
                    tooltip_parts.append("<br>No data available")
                else:
                    for col in self.hover_text_columns:
                        tooltip_parts.append(f"<br>{col}: {info[col]}")

                feature["properties"]["tooltip"] = "".join(tooltip_parts)
            else:
                feature["properties"]["density"] = None
                feature["properties"]["region"] = "Unknown"
                feature["properties"]["tooltip"] = "No data available"

    def _get_dl_geojson(self):
        style_handle = self._get_style_handle()
        colorscale = self._get_colorscale()
        style = {"weight": 2, "opacity": 1, "color": "white", "fillOpacity": 1}
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
                "min": self.df["Value"].min(),
                "max": self.df["Value"].max(),
            },
        )

    def _get_style_handle(self):
        ns = Namespace("myNamespace", "mapColorScaleFunctions")
        if self.color_scale_is_discrete:
            return ""
        return ns("continuousColorScale")

    def _get_colorscale(self):
        if self.color_scale_is_discrete:
            return ""
        return ["#B0F2BC", "#257D98"]

    def _get_colorbar(self):
        min_value = self.df.select(pl.min("Value")).item()
        colorbar_min = min(min_value, 0)
        max_value = self.df.select(pl.max("Value")).item()
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

    def _get_colorbar_title(self):
        return html.Div(
            self.hover_text_columns[0],
            style={
                "position": "absolute",
                "bottom": "700px",  # Adjusted to place above the colorbar
                "left": "10px",  # Align with the left side of the colorbar
                "background": "white",
                "padding": "2px 6px",
                "borderRadius": "5px",
                "fontWeight": "bold",
                "fontSize": "14px",
                "zIndex": "999",  # Ensure it appears above map elements
            },
        )
