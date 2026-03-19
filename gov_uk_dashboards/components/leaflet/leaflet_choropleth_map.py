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
        id_for_choropleth_map_on_page: Optional[str]="",
        subtitle: Optional[str] = None,
        enable_zoom: bool = True,
        download_chart_button_id: Optional[str] = None,
        download_data_button_id: Optional[str] = None,
        color_scale_is_discrete: bool = True,
        colorbar_title: str = None,
        show_tile_layer: bool = False,
        selected_la: str = None,
    ):  # pylint: disable=too-many-locals
        self.geojson_data = geojson
        self.df = df
        self.selected_la = selected_la
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
        self.colorbar_title = self.resolve_colorbar_title(colorbar_title)
        self.show_tile_layer = show_tile_layer
        self._add_data_to_geojson_and_get_bounds()
        self.instance_number = instance_number
        self.id_for_choropleth_map_on_page = "choropleth-map-"+id_for_choropleth_map_on_page

    def get_leaflet_choropleth_map(self):
        """Creates and returns:
        - dl.Map: leaflet choropleth map chart for display on application, which highlights and zooms to selected LA.
        - List[List[float]]: bounds for selected LA
        - dl.Map: leaflet choropleth map for chart download
        """
        """Builds the choropleth map with proper highlighting and zoom."""
        geojson_layer, selected_bounds = self._get_dl_geojson()

        # Build children list safely (exclude None)
        children = [
            *([dl.TileLayer()] if self.show_tile_layer else []),
            self._get_colorbar(),
            *([self._get_colorbar_title(self.enable_zoom)] if self._get_colorbar_title(self.enable_zoom) else []),
            geojson_layer,
        ]

        disabled_zoom_controls = {
            "scrollWheelZoom": False,
            "dragging": False,
            "zoomControl": False,
            "doubleClickZoom": False,
            "touchZoom": False,
        }
        zoom_controls = {} if self.enable_zoom else disabled_zoom_controls

        choropleth_map = dl.Map(
            children=children,
            bounds=[[49.8, -10], [55.9, 1.8]],
            id=self.id_for_choropleth_map_on_page,
            boundsOptions={"padding": [20, 20], "maxZoom": 10},  # ensures LA fills map nicely
            minZoom=6.5,
            maxZoom=10 if self.enable_zoom else 6.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
            **zoom_controls,
            attributionControl=False,
            style={"width": "100%", "height": "960px", "background": "white"},
        )
        download_choropleth_map = dl.Map(
            children=children,
            center=[54.5, -25.0],
            zoom=7.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
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
            selected_bounds,
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

    def _add_data_to_geojson_and_get_bounds(self):
        """Adds data to features, highlights selected LA, and returns dl.GeoJSON + selected_bounds."""
        selected_bounds = None
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

            # Highlight only the selected LA
            if self.selected_la and feature["properties"]["area"] == self.selected_la:
                feature["properties"]["style"] = {
                    "color": "red",
                    "weight": 4,
                    "fillOpacity": feature.get("properties", {}).get("fillOpacity", 0.7),
                }

                # Compute bounds of the selected feature
                coords = []
                geom_type = feature["geometry"]["type"]
                if geom_type == "Polygon":
                    coords = feature["geometry"]["coordinates"][0]
                elif geom_type == "MultiPolygon":
                    for poly in feature["geometry"]["coordinates"]:
                        coords.extend(poly[0])
                lats = [pt[1] for pt in coords]
                lngs = [pt[0] for pt in coords]
                selected_bounds = [[min(lats), min(lngs)], [max(lats), max(lngs)]]

            else:
                feature["properties"].pop("style", None)

        # Create the GeoJSON component
        geojson_layer = dl.GeoJSON(
            data=self.geojson_data,
            id="geojson",
            hoverStyle={"weight": 5, "color": "#666", "dashArray": ""},
            style=self._get_style_handle(),
            hideout={
                "colorscale": self._get_colorscale(),
                "style": {
                    "weight": 2,
                    "opacity": 1,
                    "color": "white",
                    "fillOpacity": 0.7 if self.show_tile_layer else 1,
                },
                "colorProp": "density",
                "min": self.df[self.column_to_plot].min(),
                "max": self.df[self.column_to_plot].max(),
            },
        )

        return geojson_layer, selected_bounds

    def _get_dl_geojson(self):
        return self._add_data_to_geojson_and_get_bounds()

    def _get_style_handle(self):
        ns = Namespace("myNamespace", "mapColorScaleFunctions")
        if self.color_scale_is_discrete:
            return ns("discreteColorScale")
        return ns("continuousColorScale")

    def _get_colorscale(self):
        if self.color_scale_is_discrete:
            if len(self.df[self.column_to_plot].unique()) == 3:
                return ["#080C54", "#1F9EB7", "#CDE594"]
            if len(self.df[self.column_to_plot].unique()) == 4:
                return ["#080C54", "#1F9EB7", "#80C6A3", "#CDE594"]
            if len(self.df[self.column_to_plot].unique()) == 5:
                return [
                    "#080C54",
                    "#186290",
                    "#1F9EB7",
                    "#80C6A3",
                    "#CDE594",
                ]
            if len(self.df[self.column_to_plot].unique()) == 6:
                return [
                    "#080C54",
                    "#186290",
                    "#1F9EB7",
                    "#80C6A3",
                    "#CDE594",
                    "#ffffcc",
                ]
        return ["#80C6A3", "#186290"]

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
        top_margin = ("100px" if self.colorbar_title else None,)
        if self.color_scale_is_discrete:
            return dlx.categorical_colorbar(
                categories=self._get_color_bar_categories(),
                colorscale=self._get_colorscale()[::-1],
                width=30,
                height=200,
                position="topleft",
                style={
                    "padding": "6px",
                    "backgroundColor": "white",
                    "borderRadius": "4px",
                    "fontSize": "16px",
                    "marginTop": top_margin,
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

        tick_text = [format_number_into_thousands_or_millions(x) for x in tick_values]

        # If duplicates appear in tick_text, change rounding
        if len(set(tick_text)) < len(tick_text):
            tick_text = [
                format_number_into_thousands_or_millions(x, 1) for x in tick_values
            ]

        tick_text = [
            str(int(val)) if val < 1000 else text
            for text, val in zip(tick_text, tick_values)
        ]  # values less than 1000 are ints

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
                "marginTop": top_margin,
            },
            tickValues=tick_values,
            tickText=tick_text,  # Optional, makes labels look cleaner
        )

    def _get_colorbar_title(self, enable_zoom: bool = False):
        if self.colorbar_title:
            top = "70px" if enable_zoom is False else "140px"
            return html.Div(
                self.colorbar_title,
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
        return None

    def resolve_colorbar_title(self, colorbar_title: str):
        """Returns text for colorbar title."""
        if colorbar_title is None:
            return None  # exclude title
        if colorbar_title == "default":
            return self.hover_text_columns[0]
        return colorbar_title  # custom title
