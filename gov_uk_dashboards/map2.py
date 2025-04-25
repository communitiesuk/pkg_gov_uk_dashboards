import pandas as pd
from dash_extensions.enrich import Dash
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.javascript import arrow_function, assign
from dash import html
import polars as pl
from data.get_regional_housing_supply_summary_df import (
    get_regional_housing_supply_summary_df,
)
from data.get_rhs_map_boundaries import get_rhs_map_boundaries_json
from gov_uk_dashboards.assets import get_assets_folder
from lib.number_formatting import format_number_into_thousands_or_millions
import os
df = get_regional_housing_supply_summary_df()

geojson_data = get_rhs_map_boundaries_json()
print(df.columns)
info_map = {
    row["Area_Code"]: {
        "value": row["Value"],
        "value_for_display": row["Number of homes delivered"],
        "region": row["Region"],
        "percentage_contribution": row["Percentage contribution to national estimate"],
    }
    for row in df.iter_rows(named=True)
}

# Step 2: Merge into GeoJSON
for feature in geojson_data["features"]:
    region_code = feature["properties"]["geo_id"]
    info = info_map.get(region_code)
    print(info)
    if info:
        feature["properties"]["density"] = info["value"]
        feature["properties"]["region"] = info["region"]
        feature["properties"]["tooltip"] = (
            f"<b>{info['region']}</b><br>Number of homes delivered: {info['value_for_display']}"
            f"<br>Percentage contribution to national estimate: {info['percentage_contribution']}"
        )
    else:
        feature["properties"]["density"] = None
        feature["properties"]["region"] = "Unknown"
        feature["properties"]["tooltip"] = "No data"

    # name = feature["properties"]["geo_id"]
    # value = density_map.get(name, None)
    # feature["properties"]["density"] = density_map.get(
    #     name, None
    # )  # or 0 instead of None
    # feature["properties"]["tooltip"] = f"{feature['properties']['geo_id']}: {value}"

# --- 4. Color setup ---
colorscale = ["#B0F2BC", "#257D98"]
classes = [10, 25, 50]
style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
hover_style = arrow_function(dict(weight=5, color="#666", dashArray=""))

# --- 5. JS dynamic style handler ---
# style_handle = assign(
#     """function(feature, context){
#     const {colorscale, colorProp, style, min, max} = context.hideout;
#     const value = feature.properties[colorProp];
#     const colors = Array.from(colorscale);  // defensive copy
#     // Normalize value to 0-1
#     const t = (value - min) / (max - min);

#     // Helper: interpolate between two hex colors
#     function interpolateColor(color1, color2, t) {
#         const c1 = parseInt(color1.slice(1), 16);
#         const c2 = parseInt(color2.slice(1), 16);
#         const r = Math.round(((c2 >> 16) - (c1 >> 16)) * t + (c1 >> 16));
#         const g = Math.round((((c2 >> 8) & 0xFF) - ((c1 >> 8) & 0xFF)) * t + ((c1 >> 8) & 0xFF));
#         const b = Math.round(((c2 & 0xFF) - (c1 & 0xFF)) * t + (c1 & 0xFF));
#         return `rgb(${r},${g},${b})`;
#     }

#     // Find segment and interpolate
#     const n = colors.length - 1;
#     const idx = Math.min(Math.floor(t * n), n - 1);
#     const local_t = (t * n) - idx;
#     const fillColor = interpolateColor(colors[idx], colors[idx + 1], local_t);

#     return {...style, fillColor: fillColor};
# }"""
# )
style_handle = "dashExtensions.continuousColorScale"
# B0F2BC
# 257D98
# --- 6. GeoJSON Component ---


# --- 7. Colorbar ---
min_value = df.select(pl.min("Value")).item()
colorbar_min = min(min_value, 0)
max_value = df.select(pl.max("Value")).item()
colorbar = dl.Colorbar(
    colorscale=colorscale,
    width=20,
    height=200,
    min=colorbar_min,
    max=max_value,
    position="topright",
)


# OPTIONALLY CAN SET TICK VALUES AND TICK TEXT
min_value = df.select(pl.min("Value")).item()
colorbar_min = min(min_value, 0)
max_value = df.select(pl.max("Value")).item()
mid_value = (colorbar_min + max_value) / 2
quarter_value = (colorbar_min + max_value) / 4
three_quarter_value = 3 * (colorbar_min + max_value) / 4
tick_values = [colorbar_min, quarter_value, mid_value, three_quarter_value, max_value]
tick_text = [
    format_number_into_thousands_or_millions(x) for x in tick_values
]  # Optional, for formatting

colorbar_title = html.Div(
    "Number of homes delivered",
    style={
        "position": "absolute",
        "bottom": "240px",  # Adjusted to place above the colorbar
        "left": "10px",  # Align with the left side of the colorbar
        "background": "white",
        "padding": "2px 6px",
        "borderRadius": "5px",
        "fontWeight": "bold",
        "fontSize": "14px",
        "zIndex": "999",  # Ensure it appears above map elements
    },
)
colorbar = dl.Colorbar(
    colorscale=colorscale,
    width=20,
    height=200,
    min=colorbar_min,
    max=max_value,
    position="bottomleft",
    style={
        "backgroundColor": "white",
        "padding": "5px",
        "borderRadius": "4px",
        "boxShadow": "0 0 6px rgba(0,0,0,0.2)",
        "marginTop": "20px",  # adjust as needed to sit just below zoom buttons
    },
    # position="topright",
    # style={
    #     "backgroundColor": "white","padding": "5px",
    #     "borderRadius": "4px",
    #     "boxShadow": "0 0 6px rgba(0,0,0,0.2)"},
    tickValues=tick_values,
    tickText=tick_text,  # Optional, makes labels look cleaner
)

# colorbar = dlx.(
#     categories=[str(c) for c in classes],
#     colorscale=colorscale,
#     width=300,
#     height=30,
#     position="bottomright"
# )

# --- 8. App Setup ---
def get_leaflet_choropleth_map(geo_function, df_function):
    df = df_function()
    geojson_data = geo_function()
    info_map = {
        row["Area_Code"]: {
            "value": row["Value"],
            "value_for_display": row["Number of homes delivered"],
            "region": row["Region"],
            "percentage_contribution": row[
                "Percentage contribution to national estimate"
            ],
        }
        for row in df.iter_rows(named=True)
    }

    # Step 2: Merge into GeoJSON
    for feature in geojson_data["features"]:
        region_code = feature["properties"]["geo_id"]
        info = info_map.get(region_code)
        print(info)
        if info:
            feature["properties"]["density"] = info["value"]
            feature["properties"]["region"] = info["region"]
            feature["properties"]["tooltip"] = (
                f"<b>{info['region']}</b><br>Number of homes delivered: {info['value_for_display']}"
                f"<br>Percentage contribution to national estimate: {info['percentage_contribution']}"
            )
        else:
            feature["properties"]["density"] = None
            feature["properties"]["region"] = "Unknown"
            feature["properties"]["tooltip"] = "No data"

    # name = feature["properties"]["geo_id"]
    # value = density_map.get(name, None)
    # feature["properties"]["density"] = density_map.get(
    #     name, None
    # )  # or 0 instead of None
    # feature["properties"]["tooltip"] = f"{feature['properties']['geo_id']}: {value}"

    # --- 4. Color setup ---
    colorscale = ["#B0F2BC", "#257D98"]
    classes = [10, 25, 50]
    style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
    hover_style = arrow_function(dict(weight=5, color="#666", dashArray=""))
    style_handle = assign(
        """function(feature, context){
        const {colorscale, colorProp, style, min, max} = context.hideout;
        const value = feature.properties[colorProp];
        const colors = Array.from(colorscale);  // defensive copy
        // Normalize value to 0-1
        const t = (value - min) / (max - min);

        // Helper: interpolate between two hex colors
        function interpolateColor(color1, color2, t) {
            const c1 = parseInt(color1.slice(1), 16);
            const c2 = parseInt(color2.slice(1), 16);
            const r = Math.round(((c2 >> 16) - (c1 >> 16)) * t + (c1 >> 16));
            const g = Math.round((((c2 >> 8) & 0xFF) - ((c1 >> 8) & 0xFF)) * t + ((c1 >> 8) & 0xFF));
            const b = Math.round(((c2 & 0xFF) - (c1 & 0xFF)) * t + (c1 & 0xFF));
            return `rgb(${r},${g},${b})`;
        }

        // Find segment and interpolate
        const n = colors.length - 1;
        const idx = Math.min(Math.floor(t * n), n - 1);
        const local_t = (t * n) - idx;
        const fillColor = interpolateColor(colors[idx], colors[idx + 1], local_t);

        return {...style, fillColor: fillColor};
    }"""
    )
    geojson = dl.GeoJSON(
        data=geojson_data,
        id="geojson",
        zoomToBounds=True,
        zoomToBoundsOnClick=True,
        style=style_handle,
        hoverStyle=hover_style,
        hideout=dict(
            colorscale=colorscale,  # Use hex strings
            style=style,
            colorProp="density",
            min=df["Value"].min(),
            max=df["Value"].max(),
        ),
    )
    min_value = df.select(pl.min("Value")).item()
    colorbar_min = min(min_value, 0)
    max_value = df.select(pl.max("Value")).item()
    colorbar = dl.Colorbar(
        colorscale=colorscale,
        width=20,
        height=200,
        min=colorbar_min,
        max=max_value,
        position="topright",
    )

    # OPTIONALLY CAN SET TICK VALUES AND TICK TEXT
    min_value = df.select(pl.min("Value")).item()
    colorbar_min = min(min_value, 0)
    max_value = df.select(pl.max("Value")).item()
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

    colorbar_title = html.Div(
        "Number of homes delivered",
        style={
            "position": "absolute",
            "bottom": "240px",  # Adjusted to place above the colorbar
            "left": "10px",  # Align with the left side of the colorbar
            "background": "white",
            "padding": "2px 6px",
            "borderRadius": "5px",
            "fontWeight": "bold",
            "fontSize": "14px",
            "zIndex": "999",  # Ensure it appears above map elements
        },
    )
    colorbar = dl.Colorbar(
        colorscale=colorscale,
        width=20,
        height=200,
        min=colorbar_min,
        max=max_value,
        position="bottomleft",
        style={
            "backgroundColor": "white",
            "padding": "5px",
            "borderRadius": "4px",
            "boxShadow": "0 0 6px rgba(0,0,0,0.2)",
            "marginTop": "20px",  # adjust as needed to sit just below zoom buttons
        },
        # position="topright",
        # style={
        #     "backgroundColor": "white","padding": "5px",
        #     "borderRadius": "4px",
        #     "boxShadow": "0 0 6px rgba(0,0,0,0.2)"},
        tickValues=tick_values,
        tickText=tick_text,  # Optional, makes labels look cleaner
    )

    return dl.Map(
        children=[dl.TileLayer(), colorbar, colorbar_title, geojson],
        center=[54.5, -2.5],  # Centered on the UK
        zoom=5,
        minZoom=6,
        maxZoom=7,
        maxBounds=[[49.8, -6.5], [55.9, 1.8]],
        style={"width": "600px", "height": "500px"},
    )


# app = Dash(__name__)
# app.layout = html.Div(
#     [
#         dl.Map(
#             children=[dl.TileLayer(), colorbar,colorbar_title,geojson],
#             center=[54.5, -2.5],  # Centered on the UK
#             zoom=5,
#             minZoom=6,
#             maxZoom=7,
#             maxBounds=[[49.8, -6.5], [55.9, 1.8]],
#             style={"width": "600px", "height": "500px"},
#         )
#     ]
# )

# if __name__ == "__main__":
#     app.run_server(debug=True)
