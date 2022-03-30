"""Functions for converting values to human readable format"""


def format_as_human_readable(value_to_format: float, /, *, prefix: str = "") -> str:
    """Format a number as a human readable string
    Appends bn, m, k as appropriate
    Rounds number to 3dp

    Args:
        value_to_format(float): number to format
        prefix(str,optional): prefix to append to the start

    Returns:
        str: formatted number
    """

    if value_to_format >= 1_000_000_000:
        return f"{prefix}{value_to_format/1_000_000_000:g}bn"
    if value_to_format >= 1_000_000:
        return f"{prefix}{value_to_format/1_000_000:g}m"
    if value_to_format >= 1_000:
        return f"{prefix}{value_to_format/1_000:g}k"
    return f"{prefix}{value_to_format:,g}"
