"""Helper functions for data schema tests"""

import calendar
from datetime import datetime
import re
from typing import Annotated, Literal, Optional, get_args, get_origin
from dateutil.relativedelta import relativedelta


def extract_main_type(typ):
    """Extracts the non-None type from Optional[T] or returns the type as-is."""
    args = get_args(
        typ
    )  # Get inner types (e.g., (float, NoneType) or ("val1", "val2"))

    if args:
        # Handle Annotated[T, ...]
        if get_origin(args[0]) is Annotated:
            return get_args(args[0])[0]  # Extract the primary type from Annotated

        # Handle Optional[Literal[...]] -> Extract Literal values
        if get_origin(typ) is Literal:
            return str  # Literals are usually strings, so return `str`

        # If the first argument is Literal itself, extract the inner values
        if get_origin(args[0]) is Literal:
            literal_values = get_args(args[0])  # Get valid values from Literal
            print("Valid Literal Values:", literal_values)
            return str  # Since Literals typically hold strings, return `str`

        # If it's a tuple containing types, filter out NoneType and return the first non-None
        non_none_args = [
            arg for arg in args if arg is not type(None)
        ]  # Remove NoneType
        return (
            non_none_args[0] if non_none_args else typ
        )  # Return the first non-None type

    return typ


def date_is_valid_format(
    cls, date_value, formats: list[str], alternative_value: Optional[str] = None
) -> bool:
    # pylint: disable=unused-argument
    """
    Helper function to check that a date is in YYYY-MM-DD format.

    Parameters:
    date (str): date string to test

    Returns: bool: True if string is in correct format, False otherwise.
    """
    date_checking_key = {
        "YYYY-MM-DD": {"format": "%Y-%m-%d", "regex": r"\d{4}-\d{2}-\d{2}"},
        "Month YYYY": {
            "format": "%B %Y",
            "regex": r"^(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$",  # pylint: disable=line-too-long
        },
        "Mon YYYY": {
            "format": "%b %Y",
            "regex": r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{4}$",
        },
        "YYYY-YY": {"format": "%Y-%y", "regex": r"^\d{4}-\d{2}$"},
        "YYYY-MM": {"format": "%Y-%m", "regex": r"^\d{4}-(0[1-9]|1[0-2])$"},
        "YYYY-MM-DD-with-time": {
            "format": "%Y-%m-%dT%H:%M:%S.%f",
            "regex": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}$",
        },
        "FYE YYYY": {
            "format": "FYE %Y",
            "regex": r"^FYE \d{4}$",
        },
    }

    if alternative_value is not None and date_value == alternative_value:
        return True

    format_matched = False

    for date_format in formats:
        regex_format = date_checking_key[date_format]["regex"]

        # Check if the date matches the regex for the format
        if re.fullmatch(regex_format, date_value):
            try:
                # Attempt to parse the date with the matching format
                date_format = date_checking_key[date_format]["format"]
                datetime.strptime(date_value, date_format)
                format_matched = True  # If this succeeds, set format_matched to True
                break  # Stop checking other formats if one is valid
            except ValueError:
                # Skip and move to the next format if parsing fails
                continue

    # If none of the formats were valid, raise an error
    if not format_matched:
        raise ValueError(
            f"Date {date_value} must match one of the following " f"formats: {formats}"
        )
    return format_matched


def date_is_in_15_year_range(cls, date_value, date_format):
    """Validates that the year provided is within 15 years of today's date

    Args:
        date_value (str): Date to be checked
        date_format (str): Format of the date passed in.

    Raises:
        ValueError: Raises ValueError if date is not in required range
    """
    # pylint: disable=unused-argument
    today = datetime.today().date()
    fifteen_years_ago = today - relativedelta(years=15)
    fifteen_years_ahead = today + relativedelta(years=15)
    if date_format != "YYYY-YY":
        if not (
            fifteen_years_ago
            <= datetime.strptime(date_value, date_format).date()
            <= fifteen_years_ahead
        ):
            raise ValueError(
                f"Date {date_value} must be between {fifteen_years_ago} and {fifteen_years_ahead}"
            )
    else:
        start_year, _ = map(int, date_value.split("-"))

        # Check if within the 15-year range
        if not fifteen_years_ago.year <= start_year <= fifteen_years_ahead.year:
            raise ValueError(
                f"Financial year range YYYY-YY: {date_value} must start between "
                f"{fifteen_years_ago.year} and {fifteen_years_ahead.year}."
            )


def date_is_last_day_of_month(cls, date_str: str, date_format: str):
    """Validates that the date provided is the last day of a month.

    Args:
        date_str (str): Date to be checked
        date_format (str): Format of the date passed in.

    Raises:
        ValueError: Raises ValueError if date is not the last day of a month.
    """
    # pylint: disable=unused-argument
    date_obj = datetime.strptime(date_str, date_format)

    # Get the last day of the given month and year
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]

    if date_obj.day == last_day:
        return True

    raise ValueError(f"Date {date_str} must be the last day of a month")


def date_is_last_day_of_financial_year(cls, date_str: str, date_format: str):
    """Validates that the date provided is the last day of the financial year, eg. 31 March.

    Args:
        date_str (str): Date to be checked
        date_format (str): Format of the date passed in.

    Raises:
        ValueError: Raises ValueError if date is not the last day of the financial year.
    """
    # pylint: disable=unused-argument
    date_obj = datetime.strptime(date_str, date_format)

    # Check if the date is March 31
    if date_obj.month == 3 and date_obj.day == 31:
        return True

    raise ValueError(f"Date {date_str} must be March 31")


def financial_year_is_greater_or_equal_to_2009_10(cls, date_value: str):
    # pylint: disable=unused-argument
    """Validates that the provided financial year is greater than or equal to '2009-10'.

    Args:
        date_value (str): In format YYYY-YY

    Raises:
        ValueError: If the provided financial year is less than '2009-10'.
                    The error message will indicate the invalid value.
    """
    start_year, end_year = date_value.split("-")
    start_year = int(start_year)
    end_year = int(end_year)

    # Ensure the financial year is greater than 2009-10
    if start_year < 2010 or (start_year == 2010 and end_year < 10):
        raise ValueError(
            f"Financial year must be greater than '2009-10'. Provided: {date_value}"
        )


def date_is_greater_than_year_2000(cls, date_value: str, date_format: str):
    # pylint: disable=unused-argument
    """Validates that the year of the given date is equal to or after the year 2000.

    Args:
        date_value (str): The date string to validate, in the format specified by `date_format`.
        date_format (str): The format in which the `date_value` is provided (e.g., '%Y-%m-%d').

    Raises:
        ValueError: If the year of the `date_value` is less than 2000.
    """
    value_year = datetime.strptime(date_value, date_format).date().year
    if not value_year >= 2000:
        raise ValueError(f"Date {date_value} must be equal to or after year 2000")
    return date_value


def value_matches_regex_pattern_or_alternative_value(
    cls, value: str, regex_pattern_type: str, alternative_values: list[str] = None
):
    # pylint: disable=unused-argument
    """Validates if the given value matches a specified regex pattern or the alternative value.

    Args:
        value (str): The value to validate.
        regex_pattern_type (str): The key that determines which regex pattern to use.
        alternative_values (list[str], optional): A list of alternative values that will pass the
            validation even if it doesn't match the regex pattern. Defaults to None.

    Raises:
        ValueError: If the `value` doesn't match the specified regex pattern or isn't in
            alternative_values.

    Returns:
        str: The valid value (either the `value` or the `alternative_values`).
    """
    regex_pattern_dict = {
        "email": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "url": r"https?:\/\/(www\.)?[a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-zA-Z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",  # pylint: disable=line-too-long
        "x_weeks_and_y_days": r"^\d+\s+weeks\s+and\s+\d+\s+days$",
        "area_code": r"^^E(?:0[6789]|[01][06789])\d{6}$",
        "YYYY-YY": r"^\d{4}-\d{2}$",
        "YYYY-MM": r"^\d{4}-(0[1-9]|1[0-2])$",
    }
    if value is not None and not re.fullmatch(
        regex_pattern_dict[regex_pattern_type], value, re.IGNORECASE
    ):
        if alternative_values is not None and value in alternative_values:
            return value

        raise ValueError(
            f"Value '{value}' is invalid: doesn't match '{regex_pattern_type}' regex or "
            f"allowed alternatives '{alternative_values}'."
        )
    return value
