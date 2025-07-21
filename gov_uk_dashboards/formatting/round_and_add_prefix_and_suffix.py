"""
Function to add a prefix and suffix to a number and also show the number of decimal places
specified.
"""

import math
import decimal


def round_and_add_prefix_and_suffix(
    value, decimal_places=None, prefix="", suffix="", separator="-"
):
    """
    Rounds a number to the specified number of decimal places, for example rounds 12 to 2dp as
    12.00. Returns the formatted number as a string with and optional prefix and suffix.

    Args:
        value(float or int): number to format
        prefix(str,optional): prefix to append to the start (e.g. £). Defaults to no prefix.
        suffix(str,optional): suffix to append to the end (e.g. %). Defaults to no suffix.
        decimal_places(int, optional): If set, rounds formatted number to that many d.p.
            Defaults to None, which does not apply rounding.
        separator(str,optional): If set, will be returned for a NaN or None passed as
            value_to_format

    Returns:
        str: formatted number
    """
    if value is None or math.isnan(value):
        return separator

    if decimal_places is not None:
        decimal_value = decimal.Decimal(str(value))

        if decimal_places >= 0:
            value = decimal_value.quantize(
                decimal.Decimal(f"0.{'0' * decimal_places}"),
                rounding=decimal.ROUND_HALF_UP,
            )
        else:
            value = round(value, decimal_places)

    return f"{prefix}{value}{suffix}"
