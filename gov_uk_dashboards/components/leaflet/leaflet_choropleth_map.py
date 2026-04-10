"""Leaflet choropleth map class"""

import copy
import time
from typing import Optional
from dash_extensions.javascript import Namespace
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
        id_for_choropleth_map_on_page: Optional[str] = "",
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
        self.id_for_choropleth_map_on_page = (
            "choropleth-map-" + id_for_choropleth_map_on_page
        )
        self.colorbar_title = self.resolve_colorbar_title(colorbar_title)
        self.show_tile_layer = show_tile_layer
        self._add_data_to_geojson_and_get_bounds()
        self.instance_number = instance_number

    def get_leaflet_choropleth_map(self):
        """Creates and returns:
        - dl.Map: leaflet choropleth map chart for display on application, which highlights and
            zooms to selected LA.
        - List[List[float]]: bounds for selected LA
        - dl.Map: leaflet choropleth map for chart download, with LA selected if present
        """
        geojson_layer, selected_bounds = self._add_data_to_geojson_and_get_bounds()
        london_layer, _ = self._add_data_to_geojson_and_get_bounds(True)
        geojson_layer_download, _ = self._add_data_to_geojson_and_get_bounds()

        # Build children list safely (exclude None)
        children = [
            *([dl.TileLayer()] if self.show_tile_layer else []),
            dl.Pane(name="hover-pane", style={"zIndex": 500}),
            dl.Pane(name="selected-top-pane", style={"zIndex": 600}),
        ]
        display_children = (
            children
            + [self._get_colorbar(), *([self._get_colorbar_title(self.enable_zoom)])]
            + [geojson_layer]
        )
        london_display_children = children + [*([self._get_london_map_insert_title()])]+ [london_layer]
        download_children = (
            children
            + [self._get_colorbar(), *([self._get_colorbar_title()])]
            + [geojson_layer_download]
        )

        disabled_zoom_controls = {
            "scrollWheelZoom": False,
            "dragging": False,
            "zoomControl": False,
            "doubleClickZoom": False,
            "touchZoom": False,
        }
        zoom_controls = {} if self.enable_zoom else disabled_zoom_controls
        choropleth_map = dl.Map(
            children=display_children,
            bounds=[[49.8, -10], [55.9, 1.8]],
            id=self.id_for_choropleth_map_on_page,
            boundsOptions={
                "padding": [20, 20],
                "maxZoom": 10,
            },  # ensures LA fills map nicely
            minZoom=6.5,
            maxZoom=10 if self.enable_zoom else 6.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
            center=[54.5, -2.5],  # Centered on the UK
            zoom=6.5,
            **zoom_controls,
            attributionControl=False,
            style={"width": "100%", "height": "960px", "background": "white"},
        )

        london_map = dl.Map(
            children=london_display_children,
            bounds=[[49.8, -10], [55.9, 1.8]],
            id=self.id_for_choropleth_map_on_page + "-london",
            boundsOptions={
                "padding": [20, 20],
                "maxZoom": 10,
            },  # ensures LA fills map nicely
            minZoom=6.5,
            maxZoom=10 if self.enable_zoom else 6.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
            center=[51.5, -0.1],  # Centered on the UK
            zoom=9,
            attributionControl=False,
            style={"width": "100%", "height": "960px", "background": "white"},
            **disabled_zoom_controls,
        )
        
        download_london_map = dl.Map(
            children=london_display_children,
            bounds=[[49.8, -10], [55.9, 1.8]],
            id=self.id_for_choropleth_map_on_page + "-london",
            boundsOptions={
                "padding": [20, 20],
                "maxZoom": 10,
            },  # ensures LA fills map nicely
            minZoom=6.5,
            maxZoom=10 if self.enable_zoom else 6.5,
            maxBounds=[[49.8, -10], [55.9, 1.8]],
            center=[51.5, -0.25],  # Centered on the UK
            zoom=9,
            attributionControl=False,
            style={"width": "100%", "height": "960px", "background": "white"},
            **disabled_zoom_controls,
        )

        download_choropleth_map = dl.Map(
            children=download_children,
            center=[54.5, -2.5],
            zoom=6.5,
            maxBounds=[
                [49.5, -10],
                [57.2, 2],
            ],  # restrict panning but keep England tight
            zoomControl=False,
            attributionControl=False,
            style={"width": "100%", "height": "100%", "background": "white"},
            id=f"download-map-{self.selected_la or 'national'}-{int(time.time()*1000)}",
            # unique ID to force map to regenerate
        )

        maps_container = html.Div(
            style={
                "display": "flex",
                "gap": "20px",  # space between maps
            },
            children=[
                # NATIONAL MAP (add right padding so inset doesn't overlap content)
                html.Div(
                    choropleth_map,
                    style={
                        "width": "100%",
                        "height": "100%",
                        "paddingRight": "380px",  # 👈 key fix
                        "boxSizing": "border-box",
                    },
                ),
                # London inset map
                html.Div(
                    london_map,
                    style={
                        "position": "absolute",
                        "top": "300px",
                        "right": "20px",
                        "width": "350px",
                        "height": "350px",
                        "zIndex": 1000,
                    },
                ),
            ],
        )

        download_maps_container = html.Div(
            style={
                "display": "flex",
                "width": "1200px",
                "height": "1200px",
                "background": "white",
            },
            children=[
                # NATIONAL MAP
                html.Div(
                    download_choropleth_map,
                    style={
                        "width": "880px",  # 👈 fixed width WAS 880
                        "height": "100%",
                        "minWidth": "0",
                        "marginLeft": "50px",
                    },
                ),
                # LONDON MAP (RIGHT SIDE)
                html.Div(
                    download_london_map,
                    style={
                        "width": "320px",  # 👈 fixed width # WAS 400
                        "height": "350px",
                        "marginTop": "300px",  # 👈 vertical positioning
                        "background": "white",
                        "minWidth": "0",
                        "marginLeft": "-100px",  # 👈 spacing instead of gap
                    },
                ),
            ],
        )

        choropleth_map = display_chart_or_table_with_header(
            maps_container,
            self.title,
            self.subtitle,
            None,
            self.download_data_button_id,
            self.download_chart_button_id,
            None,
            instance=self.instance_number,
        )
        download_choropleth_map_display = display_chart_or_table_with_header(
            download_maps_container,
            self.title,
            self.subtitle,
        )

        return [
            choropleth_map,
            selected_bounds,
            html.Div(
                [download_choropleth_map_display],
                id=f"{self.download_chart_button_id}-hidden-map-container",
                # style={
                #     "position": "absolute",
                #     "top": "-10000px",
                #     "left": "-10000px",
                # },  # hide off screen
            ),
        ]

    def _add_data_to_geojson_and_get_bounds(self, london_las=False):
        """Adds data to features, highlights selected LA, and returns dl.GeoJSON and
        selected_bounds."""
        # pylint: disable=too-many-locals
        london_la_codes = [
            "E09000017",
            "E09000022",
            "E09000027",
            "E09000014",
            "E09000025",
            "E09000026",
            "E09000030",
            "E09000029",
            "E09000015",
            "E09000031",
            "E09000004",
            "E09000009",
            "E09000013",
            "E09000023",
            "E09000005",
            "E09000019",
            "E09000001",
            "E09000010",
            "E09000012",
            "E09000021",
            "E09000008",
            "E09000007",
            "E09000032",
            "E09000006",
            "E09000024",
            "E09000002",
            "E09000003",
            "E09000018",
            "E09000011",
            "E09000028",
            "E09000033",
            "E09000016",
            "E09000020",
        ]
        selected_bounds = None
        # Make a deep copy so each map (display or download) has independent data
        geojson_copy = copy.deepcopy(self.geojson_data)

        info_map = {
            row["Area_Code"]: {
                "value": row[self.column_to_plot],
                "area": row[self.area_column],
                **{col: row[col] for col in self.hover_text_columns},
            }
            for row in self.df.iter_rows(named=True)
        }

        if london_las == True:
            geojson_copy["features"] = [
                feature
                for feature in geojson_copy["features"]
                if feature["properties"].get("geo_id") in london_la_codes
            ]

        for feature in geojson_copy["features"]:
            region_code = feature["properties"].get("geo_id")
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
                # Other LAs
                feature["properties"]["style"] = {
                    "color": "white",
                    "weight": 2,
                    "fillOpacity": 0.7 if self.show_tile_layer else 1,
                }
                feature["properties"]["permanentWeight"] = 2
                feature["properties"]["hoverColor"] = "#666"
                feature["properties"]["hoverWeight"] = 4  # smaller than selected LA

        # Move selected LA to the end so it's drawn on top
        features = [
            f
            for f in geojson_copy["features"]
            if f["properties"].get("area") != self.selected_la
        ]
        selected_features = [
            f
            for f in geojson_copy["features"]
            if f["properties"].get("area") == self.selected_la
        ]
        geojson_copy["features"] = features + selected_features

        style = {
            "weight": 2,
            "opacity": 1,
            "color": "white",
            "fillOpacity": 0.7 if self.show_tile_layer else 1,
        }

        national_layer = dl.GeoJSON(
            data={"type": "FeatureCollection", "features": geojson_copy["features"]},
            hoverStyle={"weight": 5, "color": "#666", "dashArray": ""},
            style=self._get_style_handle(),
            hideout={
                "colorscale": self._get_colorscale(),
                "style": style,
                "colorProp": "density",
                "min": self.df[self.column_to_plot].min(),
                "max": self.df[self.column_to_plot].max(),
            },
            options={"pane": "hover-pane"},  # interactive layer below selected border
        )

        # Layer for selected LA only
        selected_la_layer = dl.GeoJSON(
            data={"type": "FeatureCollection", "features": selected_features},
            options={
                "pane": "selected-top-pane",  # draw on top of hover layer
                "style": {
                    "color": "red",
                    "weight": 5,
                    "fillOpacity": 0,
                },
                "hoverStyle": {
                    "color": "red",
                    "weight": 8,
                    "fillOpacity": 0,
                    "dashArray": "",
                },
                "interactive": True,
            },
        )
        geojson_layer = dl.LayerGroup([national_layer, selected_la_layer])

        return geojson_layer, selected_bounds

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
    
    def _get_london_map_insert_title(self):
            return html.Div(
                "London (zoomed)",
                style={
                    "position": "absolute",
                    "top": "340px",  # Adjusted to place above the colorbar
                    "left": "10px",  # Align with the left side of the colorbar
                    "background": "white",
                    "padding": "2px 6px",
                    "borderRadius": "5px",
                    "fontWeight": "bold",
                    "fontSize": "14px",
                    "zIndex": "999",  # Ensure it appears above map elements
                },
            )

    def resolve_colorbar_title(self, colorbar_title: str):
        """Returns text for colorbar title."""
        if colorbar_title is None:
            return None  # exclude title
        if colorbar_title == "default":
            return self.hover_text_columns[0]
        return colorbar_title  # custom title
