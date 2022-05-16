"""Functions for converting values to human readable format."""
import math
from typing import Optional


def format_as_human_readable(
    value_to_format: float,
    *,
    prefix: str = "",
    suffix: str = "",
    decimal_places: Optional[int] = None,
    separator="-",
) -> str:
    """
    Format a number as a human readable string.
    Appends bn, m, k as appropriate.
    E.g. 1,200,000 -> 1.2m

    Args:
        value_to_format(float): number to format
        prefix(str,optional): prefix to append to the start (e.g. £). Defaults to no prefix.
        suffix(str,optional): suffix to append to the end (e.g. %). Defaults to no suffix.
        decimal_places(int, optional): If set, rounds formatted number to that many d.p.
            This is applied after shortening, e.g. 1,234,000 with decimal places = 1 becomes
            1.2m. Defaults to None, which does not apply rounding.
        separator(str,optional): If set, will be returned for a NaN or None passed as
            value_to_format

    Returns:
        str: formatted number
    """
    value_suffix = ""
    value = value_to_format

    if value_to_format is None or math.isnan(value_to_format):
        return separator

    if value_to_format >= 1_000_000_000:
        value = value_to_format / 1_000_000_000
        value_suffix = "bn"
    elif value_to_format >= 1_000_000:
        value = value_to_format / 1_000_000
        value_suffix = "m"
    elif value_to_format >= 1_000:
        value = value_to_format / 1_000
        value_suffix = "k"

    if decimal_places is not None:
        value = round(value, decimal_places)

    return f"{prefix}{value:g}{value_suffix}{suffix}"
