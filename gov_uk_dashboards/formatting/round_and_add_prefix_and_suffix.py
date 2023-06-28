"""
Function to add a prefix and suffix to a number and also show the number of decimal places 
specified.
"""


def round_and_add_prefix_and_suffix(value, decimal_places=None, prefix="", suffix=""):
    if decimal_places is not None:
        value = round(value, decimal_places)
        value = f"{value:.{decimal_places}f}"
    return f"{prefix}{value}{suffix}"
