"""Functions to manipulate and format date strings"""

import calendar
import os
from datetime import datetime, date
import re
from typing import Optional


def convert_date_string_to_text_string(
    date_str: str,
    date_format: Optional[str] = "%Y-%m-%d",
    include_day_of_month: Optional[bool] = True,
    abbreviate_month: Optional[bool] = True,
    include_year: Optional[bool] = True,
) -> str:
    """Converts date string in format passed in to text string, with format determined by
    parameters.
    Args:
        date_str (str): The date string to format.
        date_format (str, optional): The format of the "date" string. Defaults to "%Y-%m-%d".
        include_day_of_month (bool, optional): Whether to include the date.
        abbreviate_month (bool, optional): Whether to abbreviate the month eg. Mar over March.
            Defaults to True.
        include_year (bool, optional): Whether to include the year. Defaults to True.
    Returns:
        str: Formatted date string.
    """
    dt_obj = datetime.strptime(date_str, date_format)
    return convert_date_obj_to_text_string(
        dt_obj, include_day_of_month, abbreviate_month, include_year
    )


def convert_date_obj_to_text_string(
    dt_obj: datetime,
    include_day_of_month: Optional[bool] = True,
    abbreviate_month: Optional[bool] = True,
    include_year: Optional[bool] = True,
) -> str:
    """Converts date object to text string, with format determined by parameters. If month is June
    or July, abbreviate_month is set to False.
    Args:
        dt_obj (datetime): The datetime object to format, in form YYYY-MM-DD.
        include_day_of_month (bool, optional): Whether to include the date.
        abbreviate_month (bool, optional): Whether to abbreviate the month eg. Mar over March.
            Defaults to True.
        include_year (bool, optional): Whether to include the year. Defaults to True.
    Returns:
        str: Formatted date string.
    """
    if dt_obj.month in (6, 7):
        abbreviate_month = False
    if include_day_of_month:
        text_string_format = "%e"
        if abbreviate_month:
            text_string_format += " %b"
        else:
            text_string_format += " %B"
    else:
        text_string_format = ""
        if abbreviate_month:
            text_string_format += "%b"
        else:
            text_string_format += "%B"
    if include_year:
        text_string_format += " %Y"
    return dt_obj.strftime(text_string_format).strip()


def format_year_month_to_month_year(date_string: str):
    """
    Converts a date string from 'YYYY-MM' format to 'Month YYYY' format.
    Args:
    date_string (str): A date string in the format 'YYYY-MM'.
    Returns:
    str: The formatted date string in 'Month YYYY' format.
    """
    if not date_string:
        raise ValueError("No date_string provided")
    return datetime.strptime(date_string, "%Y-%m").strftime("%B %Y")


def convert_financial_year_to_date(
    financial_year_str: str, use_start_date: bool = True
) -> datetime:
    """Converts a financial year string to a datetime object.
    If `use_start_date` is True, the function will return April 1st of the
    start year of the financial year. If `use_start_date` is False,
    it will return March 31st of the end year of the financial year.

    Args:
        financial_year_str (str): Financial year string in format YYYY-YY
        use_start_date (bool, optional): Whether to use start or end date. Defaults to True.

    Returns:
        datetime.datetime: A datetime object corresponding to the requested date
                (either April 1st of the start year or March 31st of the end year).
    """
    start_year = int(financial_year_str[:4])
    end_year = start_year + 1
    if use_start_date:
        date_str = f"{start_year}-04-01"
    else:
        date_str = f"{end_year}-03-31"
    return datetime.strptime(date_str, "%Y-%m-%d")


def convert_calendar_year_to_first_january_date(date_str: str):
    """Converts a string in format YYYY to datetime object on January 1st"""
    date_str = f"{date_str}-01-01"
    return datetime.strptime(date_str, "%Y-%m-%d")


def convert_to_dd_mm_yyyy(date_str: str, includes_time: bool = False) -> str:
    """Converts a date string to a string in the format DD-MM-YYYY

    Args:
        date_str (str): Date string, either in format YYYY-MM-DD OR YYYY-DD-HH HH:MM:SS.MsMsMs
        includes_time (bool, optional): Whether the date_str contains time. Defaults to False.

    Returns:
        str: String in the format DD-MM-YYYY
    """
    datetime_format = "%Y-%m-%d %H:%M:%S.%f" if includes_time else "%Y-%m-%d"
    datetime_object = datetime.strptime(date_str, datetime_format)
    return datetime_object.strftime("%d-%m-%Y")


def convert_to_financial_year(date_str: str, date_format: str = "%d-%m-%Y") -> str:
    """Convert a date string to financial year format (e.g., '01-04-2023' to '2023-24')"""
    date_obj = datetime.strptime(date_str, date_format)
    year = date_obj.year
    if date_obj.month < 4:
        financial_year = f"{year-1}-{str(year)[-2:]}"
    else:
        financial_year = f"{year}-{str(year+1)[-2:]}"
    return financial_year


def convert_to_financial_year_ending(
    date_str: str, date_format: str = "%d-%m-%Y"
) -> str:
    """Convert a date string to financial year ending format (e.g., '01-04-2023' to '2024')"""
    date_obj = datetime.strptime(date_str, date_format)
    year = date_obj.year
    if date_obj.month < 4:
        return f"{year}"
    return f"{year + 1}"


def get_todays_date() -> str:
    """get a string of todays date fixing value for visual tests"""
    if os.environ.get("STAGE") and os.environ.get("STAGE") == "testing":
        return "2023-12-25"
    return str(date.today())


def get_todays_date_for_downloaded_csv() -> str:
    """get a string of todays date for use in download csv, fixing value for testing"""
    if os.environ.get("STAGE") and os.environ.get("STAGE") == "testing":
        return "25/12/2023"
    return str(datetime.today().strftime("%d/%m/%Y"))


def convert_datetime_to_dd_mm_yyy_string(input_datetime: datetime):
    """convert datetime to DD/MM/YYYY string"""
    return str(input_datetime.strftime("%d/%m/%Y"))


def date_string_is_full_month_and_full_year_format(date_string: str):
    """checks if a date string is in the format $B $Y"""
    try:
        datetime.strptime(date_string, "%B %Y")
        return True
    except ValueError:
        return False


def convert_to_date_range(date_str: str) -> str:
    """Convert a date string in the format "YYYY-MM-DD", to a date range from the previous year to
    the current year for the month of the provided date. Abbreviates the month if it isn't June or
    July.

    Args:
        date_str (str): A date string in the format "YYYY-MM-DD".

    Returns:
        str: Date range in the format "MMM YYYY to MMM YYYY", where MMM is the abbreviated month
        name, if it isn't June or July. eg. Mar 2021 to Mar 2022
    """
    date_object = datetime.strptime(date_str, "%Y-%m-%d").date()

    if date_object.month in (6, 7):
        current_month = date_object.strftime("%B")
    else:
        current_month = date_object.strftime("%b")

    current_year = date_object.year

    previous_year = current_year - 1

    date_range = f"{current_month} {previous_year} to {current_month} {current_year}"

    return date_range


def shorten_month_range(date_str: str) -> str:
    """Shortens months when given a range in the format Month to Month YYYY.
        eg. January to February 2024 becomes Jan to Feb 2024.
    Args:
        date_str (str): String in format "Month to Month YYYY"
    Returns:
        str: String with abbreviated months
    """
    parts = date_str.split()
    start_month, end_month, year = parts[0], parts[2], parts[3]

    start_month_short = calendar.month_abbr[
        list(calendar.month_name).index(start_month)
    ]
    end_month_short = calendar.month_abbr[list(calendar.month_name).index(end_month)]

    return f"{start_month_short} to {end_month_short} {year}"


def date_string_is_month_to_month_year_range(date_str: str) -> bool:
    """Check if the input string is in the format "Month to Month Year".
        This function uses a regular expression to verify whether the provided
        string follows the specific format where the first and second words are
        full month names, followed by "to" and a four-digit year.
    Args:
        date_str (str): A string representing a date range in the format "Month to Month Year".
    Returns:
        bool: True if the string matches the format; False otherwise.
    """
    # Regex pattern to match "Month to Month Year"
    pattern = r"^(January|February|March|April|May|June|July|August|September|October|November|December) to (January|February|March|April|May|June|July|August|September|October|November|December) \d{4}$"  # pylint: disable=(line-too-long)
    return bool(re.match(pattern, date_str))


def convert_april_date_string_to_fye(date_str: str):
    """Converts an april date to the year in which that financial year ends"""
    year = str(int(date_str[:4]) + 1)
    return year


def get_year_from_date_object(date_obj):
    """Returns a year from a date object"""
    year = date_obj.year
    return str(year)


def replace_jun_jul_month_abbreviations(month_year_list: list[str]) -> list[str]:
    """Replace abbreviated Jun and Jul month names in a list of "Month Year" or "Month" strings with
    their full names. eg. Jun 2024 returns June 2024 and Jul returns July. Other parts of the
    strings remain unchanged.

    Args:
        month_year_list (list[str]): A list of strings containing abbreviated month names followed
            by a year or month alone (e.g., ["Jun 2023", "Jul 2024", "Jun"])

    Returns:
        list[str]: A list of strings with abbreviated Jun and Jul replaced by full month.
    """
    month_map = {"Jun": "June", "Jul": "July"}
    updated_list = [
        " ".join([month_map.get(part, part) for part in item.split()])
        for item in month_year_list
    ]
    return updated_list


def format_date_with_custom_months(date_object: datetime.date, include_day=True) -> str:
    """Format a date object into a custom string, in format "day month year", where month is
    abbreviated, unless month is June or July. eg. 10 Jan 2023, 14 June 2024.

    Args:
        date_object (datetime.date): A `datetime.date` object to format.
        include_day (bool): Boolean to determine whether to include day of month in output

    Returns:
        str: The formatted date string with custom month formatting.
    """
    if date_object.month in (6, 7):
        month = date_object.strftime("%B")
    else:
        month = date_object.strftime("%b")

    day = date_object.day
    year = date_object.year
    if include_day:

        return f"{day} {month} {year}"
    return f"{month} {year}"


def weeks_between_dates(date1: str, date2: str) -> float:
    """Calculate the unrounded number of weeks between two dates provided as strings in the format
    'YYYY-MM-DD'.

    Args:
        date1 (str): The first date in 'YYYY-MM-DD' format.
        date2 (str): The second date in 'YYYY-MM-DD' format.

    Returns:
        float: Number of weeks between the two dates.
    """

    date_format = "%Y-%m-%d"
    d1 = datetime.strptime(date1, date_format)
    d2 = datetime.strptime(date2, date_format)
    return abs((d2 - d1).days) / 7


def convert_date_to_financial_quarter(date_str: str):
    """Convert date string in the format yyyy-mm-dd to a financial quarter

    Args:
        date_str (str): yyyy-mm-dd

    Returns:
        integer with april-june being 1 and so on
    """
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    if date_obj.month < 4:
        return 4
    if date_obj.month < 7:
        return 1
    if date_obj.month < 10:
        return 2
    return 3


def convert_financial_quarter_to_financial_quarter_text(quarter: int):
    """Convert quarter integer to financial quarter text including months

    Args:
        quarter (str): 1, 2, 3, 4 representing quarters with apr-june being 1

    Returns:
        integer with april-june being 1 and so on
    """
    quarter_map = {
        1: "Q1 (Apr-June)",
        2: "Q2 (July-Sep)",
        3: "Q3 (Oct-Dec)",
        4: "Q4 (Jan-Mar)",
    }
    return quarter_map[quarter]
