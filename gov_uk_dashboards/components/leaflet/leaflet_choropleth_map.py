from dash_extensions.javascript import arrow_function
import dash_leaflet as dl
from dash import html
import polars as pl
class LeafletChoroplethMap:
    def __init__(self, get_geojson_function, get_df_function):
        self.geojson_boundaries = get_geojson_function()
        self.df = get_df_function()
        self.geojson_data = self._add_data_to_geojson()
    def get_leaflet_choropleth_map(self):
        style_handle = "dashExtensions.continuousColorScale"
        colorscale = ["#B0F2BC", "#257D98"]
        style = dict(weight=2, opacity=1, color="white", dashArray="3", fillOpacity=0.7)
        hover_style = arrow_function(dict(weight=5, color="#666", dashArray=""))
        geojson = dl.GeoJSON(
            data=self.geojson_data,
            id="geojson",
            zoomToBounds=True,
            zoomToBoundsOnClick=True,
            style=style_handle,
            hoverStyle=hover_style,
            hideout=dict(
                colorscale=colorscale,  # Use hex strings
                style=style,
                colorProp="density",
                min=self.df["Value"].min(),
                max=self.df["Value"].max(),
            ),
        )
        min_value = self.df.select(pl.min("Value")).item()
        colorbar_min = min(min_value, 0)
        max_value = self.df.select(pl.max("Value")).item()
        colorbar = dl.Colorbar(
            colorscale=colorscale,
            width=20,
            height=200,
            min=colorbar_min,
            max=max_value,
            position="topright",
        )

        # OPTIONALLY CAN SET TICK VALUES AND TICK TEXT
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
        # tick_text = [
        #     format_number_into_thousands_or_millions(x) for x in tick_values
        # ]  # Optional, for formatting

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
            # tickText=tick_text,  # Optional, makes labels look cleaner
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
    def _add_data_to_geojson(self):
        info_map = {
            row["Area_Code"]: {
                "value": row["Value"],
                "value_for_display": row["Number of homes delivered"],
                "region": row["Region"],
                "percentage_contribution": row[
                    "Percentage contribution to national estimate"
                ],
            }
            for row in self.df.iter_rows(named=True)
        }

        # Step 2: Merge into GeoJSON
        for feature in self.geojson_data["features"]:
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
