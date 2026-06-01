"""
helper_functions.py
-------------------

A collection of small, reusable utility functions used across the Housing
data pipeline.

These helpers support common operations such as list handling, JSON loading,
data validation, and general-purpose transformations that are not tied to
specific business logic.

Functions:
    flatten(lst):
        Recursively flatten a nested list into a single-level iterator.

    load_json_file(filepath):
        Load and parse a JSON file with explicit error handling.

Classes:
    JsonFileLoadError:
        Raised when a JSON file cannot be read or parsed.
"""


import json
from pathlib import Path
from typing import Any


def flatten(lst):
    """
    Recursively flattens a nested list structure into a single-level iterator.

    Args:
        lst (list): A potentially nested list containing any level of sublists.

    Yields:
        Any: Individual elements from the nested list in a flattened sequence.

    Example:
        >>> list(flatten([1, [2, 3], [4, [5, 6]]]))
        [1, 2, 3, 4, 5, 6]
    """
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

class JsonFileLoadError(RuntimeError):
    """Raised when a JSON file cannot be loaded or parsed."""


def load_json_file(filepath: str | Path) -> Any:
    """Load JSON from a file with explicit error handling.

    Args:
        filepath: Path to the JSON file.

    Returns:
        Parsed JSON content.

    Raises:
        JsonFileLoadError: If the file cannot be read or contains malformed JSON.
    """
    path = Path(filepath)

    try:
        with path.open("r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except json.JSONDecodeError as exc:
        raise JsonFileLoadError(
            f"Malformed JSON in file '{path}': {exc.msg} "
            f"at line {exc.lineno}, column {exc.colno}."
        ) from exc
    except OSError as exc:
        raise JsonFileLoadError(
            f"Could not read JSON file '{path}': {exc}"
        ) from exc