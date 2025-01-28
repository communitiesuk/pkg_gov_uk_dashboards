"""Module containing functions to round data to the standard rounding needed
for display.

Contains:
- round_thousands_to_1dp: Rounds values to 1dp in steps of 1000.
"""


def round_thousands_to_1dp(value: float) -> float:
    """
    Rounds values to 1dp in steps of 1000.
    Rounds values greater than 1B to nearest 100M
    Rounds values > 1B and >= 1M to nearest 100k
    Rounds values > 1M and >= 1k to nearest 100
    Rounds values less than 1000 to 1dp.
    If value is not a number, return original value.

    Args:
        value (float): Value to round

    Returns:
        float: Rounded value
    """
    try:
        if value >= 1_000_000_000 or value <= -1_000_000_000:
            return round(value, -8)
        if value >= 1_000_000 or value <= -1_000_000:
            return round(value, -5)
        if value >= 1000 or value <= -1_000:
            return round(value, -2)
        return round(value, 1)

    except TypeError:
        return value
