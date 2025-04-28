"""Functions to add formatting to number values"""


def format_number_into_thousands_or_millions(
    number: int, thousand_decimal_places: int = 0
) -> str:
    """Format number into thousands or millions, eg. 1,500 becomes 1.5k & 1,234,567 becomes 1.235m

    Args:
        number (int): Integer to format.
        thousand_decimal_places (int or str): The number of decimal places to display for
            1_000<=number<1_000_000. Defaults to 0. If "default" is passed, number is simply
            divided by 1_000.
    """
    if number >= 1_000_000:
        formatted_number = f"{number / 1_000_000:.3f}m"
    elif number >= 1_000:
        if thousand_decimal_places == "default":
            formatted_number = f"{number / 1_000}k"
        else:
            formatted_number = f"{number / 1_000:.{thousand_decimal_places}f}k"
    else:
        formatted_number = str(number)
    return formatted_number
