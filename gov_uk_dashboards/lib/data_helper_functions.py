"""Data helper functions"""

import hashlib
import json
from deepdiff import DeepDiff


def csv_files_differ(local_path, blob_text):
    """
    Compare a local CSV file with a CSV stored as a string in a blob.

    Args:
        local_path (str): Path to the local CSV file.
        blob_text (str): Content of the CSV file from the blob.

    Returns:
        bool: True if the files differ, False if they are identical.
    """
    with open(local_path, "rb") as data:
        hash_local = hashlib.sha256(data.read()).hexdigest()
    hash_blob = hashlib.sha256(blob_text.encode("utf-8")).hexdigest()
    return hash_local != hash_blob


def geojson_files_differ(local_path, blob_text):
    """
    Compare a local GeoJSON file with a GeoJSON stored as a string in a blob.

    Normalizes features and coordinates to ignore ordering, IDs, and minor
    floating-point differences.

    Args:
        local_path (str): Path to the local GeoJSON file.
        blob_text (str): Content of the GeoJSON file from the blob.

    Returns:
        bool: True if the GeoJSON files differ, False if they are equivalent.
    """
    with open(local_path, "r", encoding="utf-8") as f:
        local_json = json.load(f)
    blob_json = json.loads(blob_text)

    norm_local = _normalize_geojson(local_json)
    norm_blob = _normalize_geojson(blob_json)
    diff = DeepDiff(
        norm_local,
        norm_blob,
        ignore_order=True,
        significant_digits=6,
        exclude_paths=["root['features'][*]['id']"],
    )
    return bool(diff)


def _normalize_geojson(data):
    """
    Normalize a GeoJSON FeatureCollection for consistent comparison.

    This includes:
        - Sorting features by properties
        - Normalizing coordinates to a fixed precision
        - Removing unnecessary feature IDs

    Args:
        data (dict): The GeoJSON object.

    Returns:
        dict: Normalized GeoJSON object.
    """
    if data.get("type") != "FeatureCollection":
        return data

    features = [_normalize_feature(f) for f in data["features"]]
    features.sort(key=lambda f: json.dumps(f["properties"], sort_keys=True))
    return {"type": "FeatureCollection", "features": features}


def _normalize_coords(coords, precision=6):
    """
    Recursively round coordinates to a fixed precision.

    Args:
        coords (list|float|int): Coordinates to normalize.
        precision (int): Number of decimal places to round to.

    Returns:
        list|float|int: Normalized coordinates.
    """
    if isinstance(coords, list):
        return [_normalize_coords(c, precision) for c in coords]
    if isinstance(coords, (float, int)):
        return round(coords, precision)
    return coords


def _normalize_feature(f):
    """
    Normalize a GeoJSON feature by removing ID-like fields and normalizing coordinates.

    Args:
        f (dict): GeoJSON feature.

    Returns:
        dict: Normalized feature with sorted properties and rounded coordinates.
    """
    ignore_keys = {"id", "objectid", "OBJECTID", "fid"}
    geometry = f.get("geometry", {})
    props = {k: v for k, v in f.get("properties", {}).items() if k not in ignore_keys}
    return {
        "type": f.get("type"),
        "geometry": {
            "type": geometry.get("type"),
            "coordinates": _normalize_coords(geometry.get("coordinates", [])),
        },
        "properties": dict(sorted(props.items())),
    }
