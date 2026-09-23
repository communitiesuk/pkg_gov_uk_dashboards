"""Leaflet choropleth map class"""

import copy
import time
from typing import Optional
from shapely.geometry import shape, Polygon, mapping
from shapely.ops import unary_union
from shapely.affinity import scale
from dash_extensions.javascript import Namespace
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import html
import polars as pl

from gov_uk_dashboards.components.helpers.display_chart_or_table_with_header import (
    display_chart_or_table_with_header,
)
from gov_uk_dashboards.components.dash.green_button import green_button
from gov_uk_dashboards.formatting.number_formatting import (
    format_number_into_thousands_or_millions,
)

from data.get_data import load_data
from lib.absolute_path import absolute_path

LONDON_REGION_MAP_BOUNDS = [[49.8, -10], [55.9, 1.8]]


class LeafletChoroplethMap:
    """Class for  generating leaflet choropleth map charts.
    Note: Values in the numeric column should use 1 for the highest value, with larger numbers
    representing lower values.
    If color_scale_is_discrete is false, colour scale will be continuous, otherwise it will be
    discrete.
    Note: Hover text width is based off leaflet-tooltip class in css"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

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
        show_london_map: bool = False,
        os_basemap_api_key: str = None,
        os_basemap_attribution: str = None,
        include_markers: bool = False,
        legend_order: list[str] = None,
        include_new_towns: bool = False,
        new_town_geojson: dict | None = None,
    ):
        self.geojson_data = geojson
        self.new_town_geojson = new_town_geojson
        self.os_basemap_api_key = os_basemap_api_key
        self.os_basemap_attribution = os_basemap_attribution
        self.include_markers = include_markers
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
        self.show_london_map = show_london_map
        self.legend_order = legend_order
        self.include_new_towns = include_new_towns

    def get_leaflet_choropleth_map(self):
        """Creates and returns:
        - dl.Map: leaflet choropleth map chart for display on application, which highlights and
            zooms to selected LA.
        - List[List[float]]: bounds for selected LA
        - dl.Map: leaflet choropleth map for chart download, with LA selected if present
        """
        geojson_layer, selected_bounds, _ = self._add_data_to_geojson_and_get_bounds()
        geojson_layer_download, _, _ = self._add_data_to_geojson_and_get_bounds()

        is_single_boundary_map = self._is_single_boundary_map()

        # Build children list safely (exclude None)
        children = [
            *(
                [
                    dl.TileLayer(
                        url=(
                            "https://api.os.uk/maps/raster/v1/zxy/"
                            "Road_3857/{z}/{x}/{y}.png"
                            f"?key={self.os_basemap_api_key}"
                        ),
                        attribution=self.os_basemap_attribution,
                        # maxZoom=20,
                    )
                ]
                if self.show_tile_layer
                else []
            ),
            dl.Pane(name="hover-pane", style={"zIndex": 500}),
            dl.Pane(name="new-towns-pane", style={"zIndex": 525}),
            dl.Pane(name="mask-pane", style={"zIndex": 550}),
            dl.Pane(name="selected-top-pane", style={"zIndex": 600}),
            dl.Pane(name="marker-pane", style={"zIndex": 700}),
            dl.Pane(name="tooltip-pane", style={"zIndex": 800}),
        ]

        if is_single_boundary_map:
            markers = (
                self._get_project_markers() if self.include_markers else []
            )


            new_town_layer = (
                self._get_new_town_layer()
                if self.new_town_geojson
                else None
            )

            new_town_children = [new_town_layer] if new_town_layer else []

            national_display_children = (
                children
                + [geojson_layer]
                + new_town_children
                + markers
            )

            national_download_children = (
                children
                + [geojson_layer_download]
                + new_town_children
                + markers
            )

        else:
            # Preserve existing national choropleth behaviour.
            national_display_children = (
                children
                + [
                    self._get_colorbar(),
                    *([self._get_colorbar_title(self.enable_zoom)]),
                ]
                + [geojson_layer]
            )

            national_download_children = (
                children
                + [
                    self._get_colorbar(),
                    *([self._get_colorbar_title()]),
                ]
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

        map_container_for_display = dl.Map(
            children=national_display_children,
            bounds=[
                [49.66247637044628, -6.568378284916049],
                [55.8212081746314, 1.77370560966352],
            ],  # got from a print in self._add_data_to_geojson_and_get_bounds
            maxBounds=[
                [49.66247637044628, -6.568378284916049],
                [55.8212081746314, 1.77370560966352],
            ],
            id=self.id_for_choropleth_map_on_page,
            boundsOptions={
                "padding": [20, 20],
            },  # ensures LA fills map nicely
            minZoom=5,
            maxZoom=20 if self.enable_zoom else 6.5,
            center=[54.5, -2.5],  # Centered on the UK
            zoom=6.5,
            **zoom_controls,
            attributionControl=False,
            style={"width": "100%", "height": "1000px", "background": "white"},
        )

        if self.include_markers:
            map_container_for_display = html.Div(
                [
                    map_container_for_display,
                    self._get_local_authority_legend(),
                ],
                style={
                    "position": "relative",
                    "width": "100%",
                },
            )

        national_download_choropleth_map = dl.Map(
            children=national_download_children,
            center=[54.5, -2.5],
            zoom=6.5,
            maxBounds=[
                [49.5, -10],
                [57.2, 2],
            ],  # restrict panning but keep England tight
            zoomControl=False,
            attributionControl=False,
            style={"width": "1200px", "height": "1200px", "background": "white"},
            id=f"download-map-{self.selected_la or 'national'}-{int(time.time()*1000)}",
            # unique ID to force map to regenerate
        )

        if self.include_markers:
            download_map_with_legend = html.Div(
                [
                    national_download_choropleth_map,
                    self._get_local_authority_legend(),
                ],
                style={
                    "position": "relative",
                    "width": "1200px",
                    "height": "1200px",
                },
            )

        if self.show_london_map:
            london_layer, _, london_region_bounds = (
                self._add_data_to_geojson_and_get_bounds(True)
            )
            london_region_rectangle = dl.Rectangle(
                bounds=london_region_bounds,
                color="black",
                weight=2,
                fill=False,
                interactive=False,
            )
            london_display_children = (
                children
                + [london_layer]
                + [*([self._get_london_map_insert_title()])]
                + [london_region_rectangle]
            )
            london_download_children = (
                children
                + [*([self._get_london_map_insert_title(for_download=True)])]
                + [london_layer]
                + [london_region_rectangle]
            )
            london_map = dl.Map(
                children=london_display_children,
                bounds=LONDON_REGION_MAP_BOUNDS,
                id=self.id_for_choropleth_map_on_page + "-london",
                boundsOptions={
                    "padding": [20, 20],
                    "maxZoom": 10,
                },
                minZoom=6.5,
                maxZoom=10 if self.enable_zoom else 6.5,
                maxBounds=LONDON_REGION_MAP_BOUNDS,
                center=[51.5, -0.1],  # Centered on the UK
                zoom=9,
                attributionControl=False,
                style={
                    "width": "350px",
                    "height": "300px",
                    "background": "white",
                    "padding-left": "40px",
                },
                **disabled_zoom_controls,
            )

            london_overlay_div = html.Div(
                [london_map],
                id="london-overlay-container",
            )

            map_container_for_display = html.Div(
                style={"position": "relative"},
                children=[map_container_for_display, london_overlay_div],
            )

            download_london_map = dl.Map(
                children=london_download_children,
                bounds=LONDON_REGION_MAP_BOUNDS,
                id=self.id_for_choropleth_map_on_page + "-london",
                boundsOptions={
                    "padding": [20, 20],
                    "maxZoom": 10,
                },
                minZoom=6.5,
                maxZoom=10 if self.enable_zoom else 6.5,
                maxBounds=LONDON_REGION_MAP_BOUNDS,
                center=[51.5, -0.25],
                zoom=9,
                attributionControl=False,
                style={"width": "100%", "height": "960px", "background": "white"},
                **disabled_zoom_controls,
            )

            national_and_london_download_maps_container = html.Div(
                style={
                    "position": "relative",
                    "width": "1400px",
                    "height": "1200px",
                    "background": "white",
                },
                children=[
                    html.Div(
                        national_download_choropleth_map,
                        style={
                            "width": "100%",
                            "height": "100%",
                            "marginLeft": "50px",
                        },
                    ),
                    html.Div(
                        download_london_map,
                        style={
                            "position": "absolute",
                            "top": "200px",
                            "left": "40px",
                            "width": "400px",
                            "height": "350px",
                            "zIndex": 10,
                            "background": "white",
                        },
                    ),
                ],
            )

        choropleth_map = display_chart_or_table_with_header(
            html.Div(
                [green_button("Reset map", "reset-map-btn"), map_container_for_display]
            ),
            self.title,
            self.subtitle,
            None,
            self.download_data_button_id,
            self.download_chart_button_id,
            None,
            instance=self.instance_number,
        )
        download_choropleth_map_display = display_chart_or_table_with_header(
            (
                national_and_london_download_maps_container
                if self.show_london_map
                else national_download_choropleth_map
            ),
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

    def _add_data_to_geojson_and_get_bounds(self, london_las=False):
        """Adds data to features, highlights selected LA, and returns layers + bounds for selected
        LA's region."""
        # pylint: disable=too-many-locals, too-many-branches
        selected_la_region_bounds = None
        london_region_bounds = None

        # Make a deep copy so each map (display or download) has independent data
        geojson_copy = copy.deepcopy(self.geojson_data)

        single_boundary = "features" not in geojson_copy

        if single_boundary:

            if geojson_copy.get("type") == "Feature":
                feature = geojson_copy
            else:
                feature = {
                    "type": "Feature",
                    "geometry": geojson_copy,
                    "properties": {},
                }

            # Put the single LA boundary into a FeatureCollection
            geojson_copy = {
                "type": "FeatureCollection",
                "features": [feature],
            }

            # Calculate bounds so the map can zoom to the LA
            bounds = self.compute_bounds(geojson_copy["features"])

            if bounds:
                selected_la_region_bounds = self.pad_bounds(bounds)

            # now paler layer for elsewhere
            # Get the LA geometry
            la_geometries = [
                shape(feature["geometry"]) for feature in geojson_copy["features"]
            ]

            la_geometry = unary_union(la_geometries)

            # Large polygon covering the whole map
            world = Polygon(
                [
                    (-180, -90),
                    (180, -90),
                    (180, 90),
                    (-180, 90),
                    (-180, -90),
                ]
            )

            # Everything outside the LA
            outside_la = world.difference(la_geometry)

            outside_la_geojson = {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": outside_la.__geo_interface__,
                        "properties": {},
                    }
                ],
            }

            outside_la_layer = dl.GeoJSON(
                data=outside_la_geojson,
                options={
                    "pane": "mask-pane",
                    "interactive": False,
                },
                style={
                    "color": "grey",
                    "weight": 0,
                    "fillColor": "grey",
                    "fillOpacity": 0.8,  # faded outside area
                },
            )

            # Selected LA: transparent fill so the normal tile colour shows through
            geojson_layer = dl.GeoJSON(
                data=geojson_copy,
                options={
                    "pane": "selected-top-pane",
                    "interactive": False,
                },
                style={
                    "color": "black",
                    "weight": 2,
                    "opacity": 1,
                    "fillOpacity": 0,  # transparent — tile layer shows through
                },
            )

            new_layer = geojson_layer = dl.LayerGroup([geojson_layer, outside_la_layer])

            return (
                new_layer,
                selected_la_region_bounds,
                london_region_bounds,
            )

        info_map = {
            row["Area_Code"]: {
                "value": row[self.column_to_plot],
                "area": row[self.area_column],
                **{col: row[col] for col in self.hover_text_columns},
            }
            for row in self.df.iter_rows(named=True)
        }

        if london_las:
            london_la_codes = (
                self.df.filter(pl.col("Region") == "London")
                .select(pl.col("Area_Code").unique())
                .to_series()
                .to_list()
            )
            geojson_copy["features"] = [
                feature
                for feature in geojson_copy["features"]
                if feature["properties"].get("geo_id") in london_la_codes
            ]
            london_region_bounds = self.pad_bounds(
                self.compute_bounds(geojson_copy["features"])
            )

        area_codes_for_las_in_same_region_as_selected_la = None
        if self.selected_la:
            area_codes_for_las_in_same_region_as_selected_la = set(
                self.df.filter(
                    pl.col("Region")
                    == self.df.filter(pl.col("Local authority") == self.selected_la)
                    .select("Region")
                    .item()
                )
                .select("Area_Code")
                .to_series()
                .to_list()
            )

        for i, feature in enumerate(geojson_copy["features"]):
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
            if feature["properties"].get("geo_id") == "E06000053":  # IoS LA code
                geojson_copy["features"][i] = self.scale_feature(feature, 5.0)

        # Compute regional bounds for selected LA'a region
        if self.selected_la and area_codes_for_las_in_same_region_as_selected_la:
            coords = []

            for feature in geojson_copy["features"]:
                if (
                    feature["properties"].get("geo_id")
                    not in area_codes_for_las_in_same_region_as_selected_la
                ):
                    continue

                geom = feature["geometry"]

                if geom["type"] == "Polygon":
                    coords.extend(geom["coordinates"][0])

                elif geom["type"] == "MultiPolygon":
                    for poly in geom["coordinates"]:
                        coords.extend(poly[0])

            if coords:
                lats = [p[1] for p in coords]
                lngs = [p[0] for p in coords]
                selected_la_region_bounds = [
                    [min(lats), min(lngs)],
                    [max(lats), max(lngs)],
                ]
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

        return geojson_layer, selected_la_region_bounds, london_region_bounds

    def _get_local_authority_legend(self):
        """Return a legend for point-based local authority maps."""

        legend_df = (
            self.df.select(
                [
                    self.legend_column,
                    self.column_to_plot,
                ]
            )
            .drop_nulls()
            .unique(
                subset=[self.legend_column],
                maintain_order=True,
            )
        )

        if self.legend_order:
            legend_df = (
                legend_df.with_columns(
                    pl.col(self.legend_column)
                    .replace(
                        self.legend_order,
                        list(range(len(self.legend_order))),
                        default=len(self.legend_order),
                    )
                    .alias("_legend_order")
                )
                .sort("_legend_order")
                .drop("_legend_order")
            )

        legend_rows = []

        for row in legend_df.iter_rows(named=True):
            color = row[self.column_to_plot]

            legend_rows.append(
                html.Div(
                    [
                        html.Span(
                            style={
                                "display": "inline-block",
                                "width": "14px",
                                "height": "14px",
                                "borderRadius": "50%",
                                "backgroundColor": color,
                                "border": f"1px solid {color}",
                                "boxSizing": "border-box",
                                "marginRight": "10px",
                                "flexShrink": "0",
                            }
                        ),
                        html.Span(row[self.legend_column]),
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "marginBottom": "8px",
                    },
                )
            )

        # Proposed new town is an area rather than a project point,
        # so represent it with an outlined square.
        legend_rows.append(
            html.Div(
                [
                    html.Span(
                        style={
                            "display": "inline-block",
                            "width": "16px",
                            "height": "16px",
                            "border": "3px solid #0000FF",
                            "backgroundColor": "rgba(0, 0, 255, 0.5)",
                            "marginRight": "10px",
                            "boxSizing": "border-box",
                            "flexShrink": "0",
                        }
                    ),
                    html.Span("Proposed new town"),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                },
            )
        )

        return html.Div(
            legend_rows,
            style={
                "position": "absolute",
                "bottom": "30px",
                "left": "30px",
                "backgroundColor": "white",
                "border": "1px solid #b1b4b6",
                "padding": "14px 16px",
                "fontSize": "16px",
                "lineHeight": "1.25",
                "zIndex": "1000",
                "pointerEvents": "none",
                "minWidth": "210px",
                "boxShadow": "0 1px 4px rgba(0, 0, 0, 0.2)",
            },
        )

    def _get_style_handle(self):
        ns = Namespace("myNamespace", "mapColorScaleFunctions")
        if self.color_scale_is_discrete:
            return ns("discreteColorScale")
        return ns("continuousColorScale")

    def _get_colorscale(self):
        if self.color_scale_is_discrete:
            column_to_plot_range = (
                self.df[self.column_to_plot].max() - self.df[self.column_to_plot].min()
            )
            if (
                len(self.df[self.column_to_plot].unique()) == 6
                or column_to_plot_range == 5
            ):
                return [
                    "#080C54",
                    "#186290",
                    "#1F9EB7",
                    "#80C6A3",
                    "#CDE594",
                    "#ffffcc",
                ]
            if (
                len(self.df[self.column_to_plot].unique()) == 5
                or column_to_plot_range == 4
            ):
                return [
                    "#080C54",
                    "#186290",
                    "#1F9EB7",
                    "#80C6A3",
                    "#CDE594",
                ]
            if (
                len(self.df[self.column_to_plot].unique()) == 4
                or column_to_plot_range == 3
            ):
                return ["#080C54", "#1F9EB7", "#80C6A3", "#CDE594"]
            if (
                len(self.df[self.column_to_plot].unique()) == 3
                or column_to_plot_range == 2
            ):
                return ["#080C54", "#1F9EB7", "#CDE594"]
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
                className="colorbar-title",
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

    def _get_london_map_insert_title(self, for_download=False):
        base_style = {
            "background": "white",
            "borderRadius": "5px",
            "fontWeight": "bold",
            "fontSize": "14px",
            "zIndex": "99",
            "top": "10px",
        }

        position_style = {
            "top": "150px" if for_download else "330px",
            "left": "20px" if for_download else "40px",
            "position": "absolute" if for_download else None,
        }

        return html.Div("London", style={**base_style, **position_style})

    def resolve_colorbar_title(self, colorbar_title: str):
        """Returns text for colorbar title."""
        if colorbar_title is None:
            return None  # exclude title
        if colorbar_title == "default":
            return self.hover_text_columns[0]
        return colorbar_title  # custom title

    def scale_feature(self, feature, factor):
        """Scale a GeoJSON feature geometry around its centroid."""
        geom = shape(feature["geometry"])

        scaled_geom = scale(geom, xfact=factor, yfact=factor, origin="centroid")

        new_feature = feature.copy()
        new_feature["geometry"] = mapping(scaled_geom)
        return new_feature

    def compute_bounds(self, features):
        """Return bounds for GeoJSON features.

        Takes Polygon/MultiPolygon features and returns
        [[south, west], [north, east]] or None if empty."""
        lats = []
        lngs = []

        for f in features:
            geom = f.get("geometry")
            if not geom:
                continue

            coords = geom.get("coordinates")
            gtype = geom.get("type")

            if gtype == "Polygon":
                for pt in coords[0]:
                    lngs.append(pt[0])
                    lats.append(pt[1])

            elif gtype == "MultiPolygon":
                for poly in coords:
                    for pt in poly[0]:
                        lngs.append(pt[0])
                        lats.append(pt[1])

        if not lats or not lngs:
            return None

        return [[min(lats), min(lngs)], [max(lats), max(lngs)]]  # SW  # NE

    def pad_bounds(self, bounds, pad=0.01):
        """Expand bounds by applying padding."""
        (south, west), (north, east) = bounds

        return [[south - pad, west - pad], [north + pad, east + pad]]

    def _get_project_markers(self):
        """Create coloured Leaflet markers for project points."""

        markers = []

        for row in self.df.iter_rows(named=True):
            coordinates = row.get(self.area_column)
            color = row.get(self.column_to_plot)

            if not coordinates or not color:
                continue

            latitude, longitude = coordinates[0]

            tooltip_content = [
                html.Div(
                    [
                        html.Strong(f"{column}: "),
                        str(row.get(column, "")),
                    ]
                )
                for column in self.hover_text_columns
            ]

            markers.append(
                dl.CircleMarker(
                    center=[latitude, longitude],
                    radius=7,
                    color=color,
                    fillColor=color,
                    fillOpacity=1,
                    weight=1,
                    pane="marker-pane",
                    children=[
                        dl.Tooltip(tooltip_content, pane="tooltip-pane"),
                    ],
                )
            )

        return markers

    def _get_new_town_layer(self):
        """Create proposed new town GeoJSON layer."""



        return dl.GeoJSON(
            data=self.new_town_geojson,
            options={
                "pane": "new-towns-pane",
                "interactive": False,
            },
            style={
                "color": "#0000FF",
                "weight": 3,
                "opacity": 1,
                "fillColor": "#0000FF",
                "fillOpacity": 0.5,
            },
        )

    def _is_single_boundary_map(self) -> bool:
        """Return True when GeoJSON represents a single LA boundary."""
        return "features" not in self.geojson_data
