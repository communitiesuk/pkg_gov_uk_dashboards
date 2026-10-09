"""Geography helper functions"""

import json
from pathlib import Path

import geobuf
from shapely.geometry import Polygon, shape

WORLD = Polygon(
    [
        (-180, -90),
        (180, -90),
        (180, 90),
        (-180, 90),
        (-180, -90),
    ]
)


def generate_la_map_geography(
    la_code: str,
    feature: dict,
    output_dir: Path,
) -> None:
    """Generate Geobuf boundary, outside mask and Leaflet bounds for an LA."""
    geometry = shape(feature["geometry"])

    if geometry.is_empty or not geometry.is_valid:
        raise ValueError(f"Invalid geometry for {la_code}")

    boundary_geojson = {
        "type": "FeatureCollection",
        "features": [feature],
    }

    outside_geometry = WORLD.difference(geometry)

    mask_geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": outside_geometry.__geo_interface__,
                "properties": {},
            }
        ],
    }

    minx, miny, maxx, maxy = geometry.bounds
    bounds = [
        [miny - 0.01, minx - 0.01],
        [maxy + 0.01, maxx + 0.01],
    ]

    boundary_bytes = geobuf.encode(boundary_geojson)
    mask_bytes = geobuf.encode(mask_geojson)

    # Check generated files are decodable.
    if len(geobuf.decode(boundary_bytes)["features"]) != 1:
        raise ValueError(f"Invalid boundary Geobuf for {la_code}")

    if len(geobuf.decode(mask_bytes)["features"]) != 1:
        raise ValueError(f"Invalid mask Geobuf for {la_code}")

    output_dir.mkdir(parents=True, exist_ok=True)

    (output_dir / "boundary.pbf").write_bytes(boundary_bytes)
    (output_dir / "mask.pbf").write_bytes(mask_bytes)
    (output_dir / "bounds.json").write_text(
        json.dumps(bounds, separators=(",", ":")),
        encoding="utf-8",
    )
