# pylint: disable=too-many-lines
"""Leaflet choropleth map class"""

import copy
import math
import base64
from io import BytesIO
import time
from typing import Optional

import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

from shapely.geometry import shape, mapping
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

LONDON_REGION_MAP_BOUNDS = [[49.8, -10], [55.9, 1.8]]

# HEAT MAP RENDERING PARAMETERS
# Scale smoothing to the authority's geographical extent while preventing
# very small or very large authorities from producing unusable heat radii.
MINIMUM_HEAT_RADIUS_METRES = 250
MAXIMUM_HEAT_RADIUS_METRES = 5_000
HEAT_RADIUS_EXTENT_RATIO = 0.025

# Control heat-surface smoothness, resolution and maximum visual strength.
HEAT_MAX_OPACITY = 0.7
HEAT_BLUR_RATIO = 0.4
HEAT_RASTER_SIZE = 600

# Preserve medium concentrations without allowing one extreme hotspot or
# negligible Gaussian tails to dominate the rendered surface.
HEAT_DENSITY_PERCENTILE = 99
HEAT_DISPLAY_POWER = 0.65
MINIMUM_VISIBLE_HEAT_INTENSITY = 0.03

HEAT_COLOUR_RGB = (18, 67, 109)

# PIN PARAMETERS
MAJOR_SITE_THRESHOLD = 200
VERY_LARGE_SITE_THRESHOLD = 500


class LeafletChoroplethMap:
    """Create Leaflet choropleth and local-authority project maps.

    National maps display choropleth values using either a discrete or continuous
    colour scale. For discrete scales, numeric values are expected to use 1 for
    the highest category, with larger numbers representing lower categories.

    Precomputed single-authority maps can additionally display project markers,
    proposed New Town and Green Belt overlays, and a continuous heat-density
    surface.

    When ``units_column`` is supplied, marker shape represents development size.
    Projects below the major-site threshold use circle markers, larger projects
    use pins, and projects above the very-large-site threshold use star pins.
    Marker colour continues to represent the category defined by
    ``legend_column`` and ``column_to_plot``. Without ``units_column``, the
    original coloured-circle marker behaviour is preserved.

    When ``display_heat_map`` is True, proposed units are used directly as weights
    to create a continuous density surface. Heat intensity represents relative
    concentration within the selected local authority and is not directly
    comparable between authorities.

    Tooltip width is controlled by the ``leaflet-tooltip`` CSS class.
    """

    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    # pylint: disable=too-many-locals
    # pylint: disable=too-many-statements

    def __init__(
        self,
        geojson: dict | None,
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
        new_town_geojson: dict | None = None,
        green_belt_geojson: dict | None = None,
        footnote: str = None,
        boundary_url: str | None = None,
        mask_url: str | None = None,
        precomputed_bounds: list[list[float]] | None = None,
        units_column: str | None = None,
        display_heat_map: bool = False,
        legend_colour_heading: str | None = None,
    ):
        self.legend_colour_heading = legend_colour_heading
        self.units_column = units_column
        self.display_heat_map = display_heat_map
        self.geojson_data = geojson
        self.new_town_geojson = new_town_geojson
        self.green_belt_geojson = green_belt_geojson
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
        self.instance_number = instance_number
        self.show_london_map = show_london_map
        self.legend_order = legend_order
        self.footnote = footnote
        self.boundary_url = boundary_url
        self.mask_url = mask_url
        self.precomputed_bounds = precomputed_bounds

        precomputed_values = (
            self.boundary_url,
            self.mask_url,
            self.precomputed_bounds,
        )

        if any(value is not None for value in precomputed_values):
            if not all(value is not None for value in precomputed_values):
                raise ValueError(
                    "Precomputed maps require boundary_url, "
                    "mask_url and precomputed_bounds."
                )

        if self.geojson_data is None and self.boundary_url is None:
            raise ValueError(
                "Either GeoJSON data or precomputed geography must be provided."
            )

        if self.boundary_url and self.show_london_map:
            raise ValueError(
                "Precomputed single-LA maps do not support show_london_map."
            )

        if self.display_heat_map and not self.units_column:
            raise ValueError("units_column is required when display_heat_map is True.")

        required_columns = {
            "area_column": self.area_column,
            "column_to_plot": self.column_to_plot,
            "legend_column": self.legend_column,
        }

        if self.units_column:
            required_columns["units_column"] = self.units_column

        for parameter_name, column_name in required_columns.items():
            if column_name not in self.df.columns:
                raise ValueError(
                    f"{parameter_name} '{column_name}' was not found in the DataFrame."
                )

        missing_hover_columns = [
            column
            for column in self.hover_text_columns
            if column not in self.df.columns
        ]

        if missing_hover_columns:
            raise ValueError(
                "hover_text_columns contains columns not found in the DataFrame: "
                f"{missing_hover_columns}"
            )

        if (
            self.include_markers
            and self.units_column
            and not self.legend_colour_heading
        ):
            raise ValueError(
                "legend_colour_heading is required when unit-based "
                "project markers are enabled."
            )

        if self.display_heat_map and not self.boundary_url:
            raise ValueError(
                "display_heat_map is only supported for precomputed "
                "single-authority maps."
            )

    def get_leaflet_choropleth_map(self):
        """Build the display and download versions of the map.

        Precomputed single-authority maps can include project markers, a
        proposed-units heat surface, New Towns and Green Belt overlays.

        Returns:
            list: The rendered map component, selected map bounds, and hidden
            download-map component.
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
                    )
                ]
                if self.show_tile_layer
                else []
            ),
            dl.Pane(name="hover-pane", style={"zIndex": 500}),
            dl.Pane(name="new-towns-pane", style={"zIndex": 525}),
            dl.Pane(name="green-belt-pane", style={"zIndex": 520}),
            dl.Pane(name="mask-pane", style={"zIndex": 550}),
            dl.Pane(name="selected-top-pane", style={"zIndex": 600}),
            dl.Pane(name="density-pane", style={"zIndex": 650}),
            dl.Pane(name="marker-pane", style={"zIndex": 700}),
            dl.Pane(name="outline-dot-pane", style={"zIndex": 700}),
            dl.Pane(name="detailed-dot-pane", style={"zIndex": 710}),
            dl.Pane(name="outline-pin-pane", style={"zIndex": 720}),
            dl.Pane(name="detailed-pin-pane", style={"zIndex": 730}),
            dl.Pane(name="tooltip-pane", style={"zIndex": 800}),
        ]

        if is_single_boundary_map:
            heat_density_layer = (
                self._get_heat_density_layer() if self.display_heat_map else None
            )

            marker_layer = self._get_project_markers() if self.include_markers else None

            new_town_layer = (
                self._get_new_town_layer() if self.new_town_geojson else None
            )

            green_belt_layer = (
                self._get_green_belt_layer() if self.green_belt_geojson else None
            )

            additional_layers = [
                layer
                for layer in [
                    heat_density_layer,
                    new_town_layer,
                    marker_layer,
                    green_belt_layer,
                ]
                if layer is not None
            ]

            national_display_children = children + [geojson_layer] + additional_layers

            national_download_children = (
                children + [geojson_layer_download] + additional_layers
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

        national_bounds = [
            [49.66247637044628, -6.568378284916049],
            [55.8212081746314, 1.77370560966352],
        ]

        initial_bounds = (
            selected_bounds
            if is_single_boundary_map and selected_bounds
            else national_bounds
        )

        (south, west), (north, east) = initial_bounds

        initial_center = [
            (south + north) / 2,
            (west + east) / 2,
        ]

        map_container_for_display = dl.Map(
            children=national_display_children,
            bounds=initial_bounds,
            maxBounds=national_bounds,
            id=self.id_for_choropleth_map_on_page,
            boundsOptions={"padding": [20, 20]},
            zoomSnap=0.1,
            minZoom=5,
            maxZoom=20 if self.enable_zoom else 6.5,
            center=initial_center,
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
            footnote=self.footnote if self.footnote else None,
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

        if self.boundary_url is not None:
            layer, bounds = self._get_precomputed_boundary_layer()
            return layer, bounds, None

        if self.geojson_data is None:
            raise ValueError("GeoJSON data is required for national choropleth maps.")

        if self.geojson_data.get("type") != "FeatureCollection":
            raise ValueError(
                "Single-LA maps require precomputed boundary and mask URLs."
            )

        geojson_copy = copy.deepcopy(self.geojson_data)

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
        """Return the legend for a point-based local-authority map.

        Preserve the original coloured-circle legend when ``units_column`` is not
        supplied. For unit-aware maps, separately show colour, development-size
        markers, heat concentration and optional geographical overlays.
        """

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
                    .replace_strict(
                        self.legend_order,
                        list(range(len(self.legend_order))),
                        default=len(self.legend_order),
                    )
                    .alias("_legend_order")
                )
                .sort("_legend_order")
                .drop("_legend_order")
            )

        row_style = {
            "display": "flex",
            "alignItems": "center",
            "minHeight": "18px",
            "marginBottom": "4px",
        }

        symbol_container_style = {
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "width": "25px",
            "minWidth": "25px",
            "marginRight": "7px",
        }

        legend_rows = []

        # Preserve the original legend when proposed-unit information
        # is not supplied.
        if not self.units_column:
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

        else:
            section_heading_style = {
                "fontWeight": "bold",
                "fontSize": "16px",
                "marginTop": "8px",
                "marginBottom": "5px",
            }

            first_section_heading_style = {
                **section_heading_style,
                "marginTop": "0",
            }

            pin_row_style = {
                **row_style,
                "minHeight": "30px",
            }

            pin_symbol_container_style = {
                **symbol_container_style,
                "position": "relative",
                "top": "-2px",
            }

            divider_style = {
                "borderTop": "1px solid #b1b4b6",
                "marginTop": "8px",
            }

            neutral_marker_colour = "#505a5f"
            neutral_marker_centre_colour = "#0b0c0c"

            legend_rows.append(
                html.Div(
                    f"{self.legend_colour_heading} (colour)",
                    style=first_section_heading_style,
                )
            )

            # Square swatches show that colour and marker shape have
            # separate meanings.
            for row in legend_df.iter_rows(named=True):
                colour = row[self.column_to_plot]

                legend_rows.append(
                    html.Div(
                        [
                            html.Span(
                                html.Span(
                                    style={
                                        "display": "block",
                                        "width": "14px",
                                        "height": "14px",
                                        "backgroundColor": colour,
                                    }
                                ),
                                style=symbol_container_style,
                            ),
                            html.Span(row[self.legend_column]),
                        ],
                        style=row_style,
                    )
                )

            legend_rows.extend(
                [
                    html.Div(style=divider_style),
                    html.Div(
                        "Development size (marker)",
                        style=section_heading_style,
                    ),
                    html.Div(
                        [
                            html.Span(
                                html.Span(
                                    style={
                                        "display": "block",
                                        "width": "9px",
                                        "height": "9px",
                                        "borderRadius": "50%",
                                        "backgroundColor": neutral_marker_colour,
                                        "border": f"1px solid {neutral_marker_colour}",
                                        "boxSizing": "border-box",
                                    }
                                ),
                                style=symbol_container_style,
                            ),
                            html.Span(f"Up to {MAJOR_SITE_THRESHOLD:,} units"),
                        ],
                        style=row_style,
                    ),
                    html.Div(
                        [
                            html.Span(
                                html.Span(
                                    html.Span(
                                        style={
                                            "display": "block",
                                            "width": "6px",
                                            "height": "6px",
                                            "borderRadius": "50%",
                                            "backgroundColor": (
                                                neutral_marker_centre_colour
                                            ),
                                        }
                                    ),
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "width": "20px",
                                        "height": "20px",
                                        "backgroundColor": neutral_marker_colour,
                                        "border": (
                                            f"2px solid {neutral_marker_colour}"
                                        ),
                                        "borderRadius": "50% 50% 50% 0",
                                        "transform": "rotate(-45deg)",
                                        "boxSizing": "border-box",
                                    },
                                ),
                                style=pin_symbol_container_style,
                            ),
                            html.Span(
                                f"{MAJOR_SITE_THRESHOLD + 1:,}–"
                                f"{VERY_LARGE_SITE_THRESHOLD:,} "
                                "units"
                            ),
                        ],
                        style=pin_row_style,
                    ),
                    html.Div(
                        [
                            html.Span(
                                html.Span(
                                    html.Span(
                                        "★",
                                        style={
                                            "display": "block",
                                            "color": "white",
                                            "fontSize": "12px",
                                            "lineHeight": "1",
                                            "transform": "rotate(45deg)",
                                        },
                                    ),
                                    style={
                                        "display": "flex",
                                        "alignItems": "center",
                                        "justifyContent": "center",
                                        "width": "20px",
                                        "height": "20px",
                                        "backgroundColor": (neutral_marker_colour),
                                        "border": (
                                            f"2px solid {neutral_marker_colour}"
                                        ),
                                        "borderRadius": "50% 50% 50% 0",
                                        "transform": "rotate(-45deg)",
                                        "boxSizing": "border-box",
                                    },
                                ),
                                style=pin_symbol_container_style,
                            ),
                            html.Span(f"More than {VERY_LARGE_SITE_THRESHOLD:,} units"),
                        ],
                        style=pin_row_style,
                    ),
                ]
            )

            if self.display_heat_map:
                legend_rows.extend(
                    [
                        html.Div(style=divider_style),
                        html.Div(
                            "Proposed units concentration",
                            style=section_heading_style,
                        ),
                        html.Div(
                            [
                                html.Span(
                                    html.Span(
                                        style={
                                            "display": "block",
                                            "width": "14px",
                                            "height": "14px",
                                            "backgroundColor": (
                                                f"rgba({HEAT_COLOUR_RGB[0]}, "
                                                f"{HEAT_COLOUR_RGB[1]}, "
                                                f"{HEAT_COLOUR_RGB[2]}, 0.20)"
                                            ),
                                        }
                                    ),
                                    style=symbol_container_style,
                                ),
                                html.Span("Lower relative concentration"),
                            ],
                            style=row_style,
                        ),
                        html.Div(
                            [
                                html.Span(
                                    html.Span(
                                        style={
                                            "display": "block",
                                            "width": "14px",
                                            "height": "14px",
                                            "backgroundColor": (
                                                f"rgba({HEAT_COLOUR_RGB[0]}, "
                                                f"{HEAT_COLOUR_RGB[1]}, "
                                                f"{HEAT_COLOUR_RGB[2]}, 0.70)"
                                            ),
                                        }
                                    ),
                                    style=symbol_container_style,
                                ),
                                html.Span("Higher relative concentration"),
                            ],
                            style=row_style,
                        ),
                    ]
                )

            if self.new_town_geojson or self.green_belt_geojson:
                legend_rows.extend(
                    [
                        html.Div(style=divider_style),
                        html.Div(
                            "Additional layers",
                            style=section_heading_style,
                        ),
                    ]
                )

        # Additional geographical layers apply to both the original and
        # unit-based marker legends.
        if self.new_town_geojson:
            if self.units_column:
                new_town_symbol = html.Span(
                    html.Span(
                        style={
                            "display": "block",
                            "width": "14px",
                            "height": "14px",
                            "border": "3px solid #0000FF",
                            "backgroundColor": "rgba(0, 0, 255, 0.20)",
                            "boxSizing": "border-box",
                        }
                    ),
                    style=symbol_container_style,
                )
            else:
                new_town_symbol = html.Span(
                    style={
                        "display": "inline-block",
                        "width": "14px",
                        "height": "14px",
                        "border": "3px solid #0000FF",
                        "backgroundColor": "rgba(0, 0, 255, 0.20)",
                        "marginRight": "10px",
                        "boxSizing": "border-box",
                        "flexShrink": "0",
                    }
                )

            legend_rows.append(
                html.Div(
                    [
                        new_town_symbol,
                        html.Span("Proposed new town"),
                    ],
                    style=(
                        row_style
                        if self.units_column
                        else {
                            "display": "flex",
                            "alignItems": "center",
                            "marginBottom": "8px",
                        }
                    ),
                )
            )

        if self.green_belt_geojson:
            if self.units_column:
                green_belt_symbol = html.Span(
                    html.Span(
                        style={
                            "display": "block",
                            "width": "14px",
                            "height": "14px",
                            "border": "3px solid #008000",
                            "backgroundColor": "rgba(0, 128, 0, 0.20)",
                            "boxSizing": "border-box",
                        }
                    ),
                    style=symbol_container_style,
                )
            else:
                green_belt_symbol = html.Span(
                    style={
                        "display": "inline-block",
                        "width": "14px",
                        "height": "14px",
                        "border": "3px solid #008000",
                        "backgroundColor": "rgba(0, 128, 0, 0.20)",
                        "marginRight": "10px",
                        "boxSizing": "border-box",
                        "flexShrink": "0",
                    }
                )

            legend_rows.append(
                html.Div(
                    [
                        green_belt_symbol,
                        html.Span("Green belt"),
                    ],
                    style=(
                        row_style
                        if self.units_column
                        else {
                            "display": "flex",
                            "alignItems": "center",
                            "marginBottom": "8px",
                        }
                    ),
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
                "padding": "10px 12px",
                "fontSize": "16px",
                "lineHeight": "1.15",
                "zIndex": "1000",
                "pointerEvents": "none",
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
        top_margin = "100px" if self.colorbar_title else None
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
        """Create project markers using optional proposed-unit thresholds.

        When ``units_column`` is supplied, projects up to 200 units use circle
        markers, projects from 201 to 500 units use pins, and projects above
        500 units use star pins.

        When ``units_column`` is not supplied, preserve the original coloured
        circle-marker behaviour.
        """
        features = []

        for row in self.df.iter_rows(named=True):
            coordinates = row.get(self.area_column)
            color = row.get(self.column_to_plot)

            if not coordinates or not color:
                continue

            latitude, longitude = coordinates[0]

            properties = {
                "color": color,
                "tooltip": {
                    column: row.get(column) for column in self.hover_text_columns
                },
            }

            if self.units_column:
                units = row.get(self.units_column)

                try:
                    units = float(units)
                except (TypeError, ValueError):
                    units = 0

                properties.update(
                    {
                        "units": units,
                        "maturity": row.get(self.legend_column),
                        "major_site_threshold": MAJOR_SITE_THRESHOLD,
                        "very_large_site_threshold": VERY_LARGE_SITE_THRESHOLD,
                    }
                )

            features.append(
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [
                            longitude,
                            latitude,
                        ],
                    },
                    "properties": properties,
                }
            )

        geojson = {
            "type": "FeatureCollection",
            "features": features,
        }

        ns = Namespace(
            "myNamespace",
            "mapMarkerFunctions",
        )

        return dl.GeoJSON(
            data=geojson,
            options={
                "pointToLayer": ns("pointToLayer"),
                "onEachFeature": ns("onEachFeature"),
            },
        )

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

    def _get_green_belt_layer(self):
        """Create green belt GeoJSON layer."""

        return dl.GeoJSON(
            data=self.green_belt_geojson,
            options={
                "pane": "green-belt-pane",
                "interactive": False,
            },
            style={
                "color": "#008000",
                "weight": 3,
                "opacity": 1,
                "fillColor": "#008000",
                "fillOpacity": 0.5,
            },
        )

    def _is_single_boundary_map(self) -> bool:
        """Return True when using precomputed LA geography."""
        return self.boundary_url is not None

    def _get_precomputed_boundary_layer(self):
        """Create boundary and mask layers from precomputed Geobuf URLs."""

        boundary_layer = dl.GeoJSON(
            url=self.boundary_url,
            format="geobuf",
            options={
                "pane": "selected-top-pane",
                "interactive": False,
            },
            style={
                "color": "black",
                "weight": 2,
                "opacity": 1,
                "fillOpacity": 0,
            },
        )

        mask_layer = dl.GeoJSON(
            url=self.mask_url,
            format="geobuf",
            options={
                "pane": "mask-pane",
                "interactive": False,
            },
            style={
                "color": "grey",
                "weight": 0,
                "fillColor": "grey",
                "fillOpacity": 0.8,
            },
        )

        return (
            dl.LayerGroup([boundary_layer, mask_layer]),
            self.precomputed_bounds,
        )

    def _get_heat_weight(self, units: float) -> float:
        """Use proposed units directly so larger sites contribute more heat."""
        return units

    def _get_heat_density_layer(self):
        """Create a continuous heat surface weighted by proposed units.

        Project unit totals are placed onto a raster and smoothed using a Gaussian
        filter. The result is normalised within the selected local authority so
        that relative concentrations remain visible across authorities of different
        sizes and development patterns.

        The resulting intensity is relative within each authority and should not
        be interpreted as an absolute density that is directly comparable between
        authorities.
        """

        if not self.precomputed_bounds:
            return None

        heat_radius_metres = self._get_heat_radius_metres()

        (south, west), (north, east) = self.precomputed_bounds

        width_metres = self._get_distance_metres(
            (south + north) / 2,
            west,
            (south + north) / 2,
            east,
        )

        height_metres = self._get_distance_metres(
            south,
            (west + east) / 2,
            north,
            (west + east) / 2,
        )

        if width_metres <= 0 or height_metres <= 0:
            return None

        raster_width = HEAT_RASTER_SIZE

        raster_height = max(
            1,
            round(raster_width * (height_metres / width_metres)),
        )

        # Prevent very narrow or elongated authorities from generating
        # an unnecessarily large raster.
        raster_height = min(
            raster_height,
            HEAT_RASTER_SIZE * 2,
        )

        weighted_points = np.zeros(
            (
                raster_height,
                raster_width,
            ),
            dtype=float,
        )

        valid_project_count = 0

        for row in self.df.iter_rows(named=True):
            coordinates = row.get(self.area_column)
            units = row.get(self.units_column)

            if not coordinates or units is None:
                continue

            try:
                units = float(units)
            except (TypeError, ValueError):
                continue

            if units <= 0:
                continue

            latitude, longitude = coordinates[0]

            if latitude is None or longitude is None:
                continue

            if not (south <= latitude <= north and west <= longitude <= east):
                continue

            x_fraction = (longitude - west) / (east - west)

            y_fraction = (north - latitude) / (north - south)

            x_index = min(
                raster_width - 1,
                max(
                    0,
                    round(x_fraction * (raster_width - 1)),
                ),
            )

            y_index = min(
                raster_height - 1,
                max(
                    0,
                    round(y_fraction * (raster_height - 1)),
                ),
            )

            weighted_points[
                y_index,
                x_index,
            ] += self._get_heat_weight(units)

            valid_project_count += 1

        if valid_project_count == 0:
            return None

        metres_per_x_pixel = width_metres / raster_width

        metres_per_y_pixel = height_metres / raster_height

        blur_radius_metres = heat_radius_metres * HEAT_BLUR_RATIO

        sigma_x = max(
            1,
            blur_radius_metres / metres_per_x_pixel,
        )

        sigma_y = max(
            1,
            blur_radius_metres / metres_per_y_pixel,
        )

        heat_surface = gaussian_filter(
            weighted_points,
            sigma=(
                sigma_y,
                sigma_x,
            ),
            mode="constant",
        )

        positive_density = heat_surface[heat_surface > 0]

        if positive_density.size == 0:
            return None

        # Prevent one exceptionally strong hotspot from making the rest of the
        # authority's heat surface almost invisible.
        density_reference = np.percentile(
            positive_density,
            HEAT_DENSITY_PERCENTILE,
        )

        heat_surface = np.clip(
            heat_surface / density_reference,
            0,
            1,
        )

        # Retain visible medium-density areas while preserving darker peaks.
        heat_surface = np.power(
            heat_surface,
            HEAT_DISPLAY_POWER,
        )

        image_url = self._heat_array_to_data_url(heat_surface)

        return dl.ImageOverlay(
            url=image_url,
            bounds=self.precomputed_bounds,
            opacity=1,
            interactive=False,
            pane="density-pane",
        )

    def _get_distance_metres(
        self,
        latitude_1: float,
        longitude_1: float,
        latitude_2: float,
        longitude_2: float,
    ) -> float:
        """Return the distance between two coordinates in metres."""

        earth_radius_metres = 6_371_000

        latitude_1_radians = math.radians(latitude_1)
        latitude_2_radians = math.radians(latitude_2)

        latitude_difference = math.radians(latitude_2 - latitude_1)
        longitude_difference = math.radians(longitude_2 - longitude_1)

        haversine_value = (
            math.sin(latitude_difference / 2) ** 2
            + math.cos(latitude_1_radians)
            * math.cos(latitude_2_radians)
            * math.sin(longitude_difference / 2) ** 2
        )

        angular_distance = 2 * math.atan2(
            math.sqrt(haversine_value),
            math.sqrt(1 - haversine_value),
        )

        return earth_radius_metres * angular_distance

    def _get_heat_radius_metres(self) -> int:
        """Calculate a heat radius from the local authority's geographical extent.

        The radius is based on a proportion of the authority's longest dimension
        and clamped between the configured minimum and maximum values so that
        compact and geographically large authorities remain visually usable.
        """
        if not self.precomputed_bounds:
            return 2_000

        (south, west), (north, east) = self.precomputed_bounds

        centre_latitude = (south + north) / 2
        centre_longitude = (west + east) / 2

        width_metres = self._get_distance_metres(
            centre_latitude,
            west,
            centre_latitude,
            east,
        )

        height_metres = self._get_distance_metres(
            south,
            centre_longitude,
            north,
            centre_longitude,
        )

        longest_dimension_metres = max(
            width_metres,
            height_metres,
        )

        calculated_radius = longest_dimension_metres * HEAT_RADIUS_EXTENT_RATIO

        return round(
            max(
                MINIMUM_HEAT_RADIUS_METRES,
                min(
                    MAXIMUM_HEAT_RADIUS_METRES,
                    calculated_radius,
                ),
            )
        )

    def _heat_array_to_data_url(
        self,
        heat_array: np.ndarray,
    ) -> str:
        """Convert the normalised heat surface to a transparent PNG data URL.

        Density is represented using the heat-map blue with varying alpha.
        Negligible intensity is removed before rendering so Gaussian tails do not
        produce a faint background haze or expose the underlying raster cells.
        """

        intensity = np.clip(
            heat_array,
            0,
            1,
        )

        red_value, green_value, blue_value = HEAT_COLOUR_RGB

        red = np.full(
            intensity.shape,
            red_value,
            dtype=np.uint8,
        )
        green = np.full(
            intensity.shape,
            green_value,
            dtype=np.uint8,
        )
        blue = np.full(
            intensity.shape,
            blue_value,
            dtype=np.uint8,
        )

        # Remove negligible Gaussian tails so the raster remains transparent
        # outside meaningful areas of development density.
        visible_intensity = np.clip(
            (intensity - MINIMUM_VISIBLE_HEAT_INTENSITY)
            / (1 - MINIMUM_VISIBLE_HEAT_INTENSITY),
            0,
            1,
        )

        alpha = (visible_intensity * HEAT_MAX_OPACITY * 255).astype(np.uint8)

        rgba = np.dstack(
            [
                red,
                green,
                blue,
                alpha,
            ]
        )

        image = Image.fromarray(
            rgba,
            mode="RGBA",
        )

        image_buffer = BytesIO()

        image.save(
            image_buffer,
            format="PNG",
            optimise=True,
        )

        encoded_image = base64.b64encode(image_buffer.getvalue()).decode("ascii")

        return f"data:image/png;base64,{encoded_image}"
