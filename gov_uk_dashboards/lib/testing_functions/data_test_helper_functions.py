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
        date_value (str): Date to be checked
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
    cls, value: str, regex_pattern_type: str, alternative_value: str = None
):
    # pylint: disable=unused-argument
    """alidates if the given value matches a specified regex pattern or the alternative value.

    Args:
        value (str): The value to validate.
        regex_pattern_type (str): The key that determines which regex pattern to use.
        alternative_value (str, optional): An alternative value that will pass the validation
            even if it doesn't match the regex pattern. Defaults to None.

    Raises:
        ValueError: If the `value` doesn't match the specified regex pattern or the
            `alternative_value`.

    Returns:
        str: The valid value (either the `value` or the `alternative_value`).
    """
    regex_pattern_dict = {
        "email": r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "url": r"https?:\/\/(www\.)?[a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-zA-Z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",  # pylint: disable=line-too-long
        "x_weeks_and_y_days": r"^\d+\s+weeks\s+and\s+\d+\s+days$",
        "area_code": r"^E0[6789]\d{6}$",
        "YYYY-YY": r"^\d{4}-\d{2}$",
        "YYYY-MM": r"^\d{4}-(0[1-9]|1[0-2])$",
    }
    if value is not None and not re.fullmatch(
        regex_pattern_dict[regex_pattern_type], value, re.IGNORECASE
    ):
        if alternative_value is not None and value == alternative_value:
            return value

        raise ValueError(
            f"Value '{value}' is invalid: doesn't match '{regex_pattern_type}' regex or "
            f"allowed alternative '{alternative_value}'."
        )
    return value


def get_list_of_las(schema):
    """Gets list of las for use in schema, passing housing_delivery_test or
    permissions_per_month adds extra las"""
    la_list = [
        "Scarborough",
        "Gateshead",
        "Bromley",
        "Birmingham",
        "Waveney",
        "Liverpool",
        "Sefton",
        "Luton",
        "Halton",
        "Ribble Valley",
        "South Cambridgeshire",
        "Runnymede",
        "Wealden",
        "Charnwood",
        "Brentwood",
        "Bedford",
        "Rochdale",
        "Lincoln",
        "Barrow-in-Furness",
        "Darlington",
        "County Durham",
        "Torbay",
        "Adur",
        "Great Yarmouth",
        "Mole Valley",
        "Croydon",
        "Canterbury",
        "Redditch",
        "Walsall",
        "Southampton",
        "Enfield",
        "East Dorset",
        "Lichfield",
        "Cherwell",
        "Christchurch",
        "South Ribble",
        "South Staffordshire",
        "Tameside",
        "Wirral",
        "East Staffordshire",
        "Worcester",
        "Arun",
        "Waverley",
        "Dudley",
        "Bournemouth, Christchurch and Poole",
        "Malvern Hills",
        "North Lincolnshire",
        "North Warwickshire",
        "Brighton and Hove",
        "Worthing",
        "Bristol",
        "Welwyn Hatfield",
        "Warwick",
        "Northampton",
        "South Kesteven",
        "West Devon",
        "Haringey",
        "Greenwich",
        "Tewkesbury",
        "Salford",
        "Isle of Wight",
        "North Norfolk",
        "West Berkshire",
        "West Suffolk",
        "Mid Sussex",
        "Ryedale",
        "Winchester",
        "Stroud",
        "Sutton",
        "South Hams",
        "Kirklees",
        "North Somerset",
        "Milton Keynes",
        "Northumberland",
        "East Lindsey",
        "Dorset",
        "Maidstone",
        "Derbyshire Dales",
        "Lancaster",
        "Ipswich",
        "East Cambridgeshire",
        "Wandsworth",
        "Hackney",
        "St Albans",
        "Redcar and Cleveland",
        "Wigan",
        "Trafford",
        "Test Valley",
        "Eden",
        "Gosport",
        "Crawley",
        "Newcastle-under-Lyme",
        "Harrow",
        "Lewes",
        "Leicester",
        "St Edmundsbury",
        "Teignbridge",
        "Mid Devon",
        "Allerdale",
        "Redbridge",
        "Lewisham",
        "Wiltshire",
        "Reigate and Banstead",
        "Stockton-on-Tees",
        "Newcastle upon Tyne",
        "Oldham",
        "Mendip",
        "Tamworth",
        "Braintree",
        "St. Helens",
        "Gedling",
        "Uttlesford",
        "Stevenage",
        "Epsom and Ewell",
        "North East Lincolnshire",
        "Blackpool",
        "Elmbridge",
        "Hambleton",
        "Guildford",
        "Daventry",
        "Nuneaton and Bedworth",
        "Dartford",
        "Hillingdon",
        "West Dorset",
        "Hounslow",
        "Rossendale",
        "Portsmouth",
        "Central Bedfordshire",
        "Barnsley",
        "Torridge",
        "Rother",
        "North West Leicestershire",
        "Ashfield",
        "East Hampshire",
        "Poole",
        "Preston",
        "Merton",
        "Solihull",
        "Babergh",
        "King's Lynn and West Norfolk",
        "Wakefield",
        "Derby",
        "Sheffield",
        "Gravesham",
        "Hastings",
        "Sunderland",
        "North Dorset",
        "West Lancashire",
        "Fylde",
        "Bexley",
        "Kettering",
        "Hartlepool",
        "South Bucks",
        "Newham",
        "Southwark",
        "Bath and North East Somerset",
        "Doncaster",
        "Bracknell Forest",
        "South Lakeland",
        "Nottingham",
        "Forest of Dean",
        "Fareham",
        "East Devon",
        "Tunbridge Wells",
        "Bromsgrove",
        "Vale of White Horse",
        "Lambeth",
        "Forest Heath",
        "Newark and Sherwood",
        "East Riding of Yorkshire",
        "Maldon",
        "Burnley",
        "Castle Point",
        "Tower Hamlets",
        "Sandwell",
        "Cheshire West and Chester",
        "Horsham",
        "Middlesbrough",
        "Huntingdonshire",
        "Boston",
        "South Tyneside",
        "North East Derbyshire",
        "High Peak",
        "Dacorum",
        "City of London",
        "Broxbourne",
        "Dover",
        "Surrey Heath",
        "Bolsover",
        "Blaby",
        "Rotherham",
        "Mid Suffolk",
        "Watford",
        "Bassetlaw",
        "Chichester",
        "Oxford",
        "Broxtowe",
        "Cheltenham",
        "Staffordshire Moorlands",
        "Kingston upon Thames",
        "Exeter",
        "South Norfolk",
        "Wychavon",
        "Woking",
        "Harrogate",
        "Shropshire",
        "Hyndburn",
        "New Forest",
        "South Derbyshire",
        "North Northamptonshire",
        "Chelmsford",
        "Ashford",
        "Wellingborough",
        "Fenland",
        "Eastleigh",
        "North Hertfordshire",
        "Telford and Wrekin",
        "Pendle",
        "North Tyneside",
        "Barking and Dagenham",
        "Peterborough",
        "Southend-on-Sea",
        "Richmondshire",
        "Plymouth",
        "Aylesbury Vale",
        "Carlisle",
        "Sevenoaks",
        "Leeds",
        "North Kesteven",
        "Knowsley",
        "Slough",
        "Chiltern",
        "Stafford",
        "Purbeck",
        "Erewash",
        "Kingston Upon Hull",
        "Wycombe",
        "Blackburn with Darwen",
        "Thanet",
        "Wyre Forest",
        "Coventry",
        "West Lindsey",
        "Cotswold",
        "Thurrock",
        "Windsor and Maidenhead",
        "Medway",
        "Tandridge",
        "Stockport",
        "Reading",
        "Weymouth and Portland",
        "Richmond upon Thames",
        "Breckland",
        "Taunton Deane",
        "Rutland",
        "Folkestone and Hythe",
        "Swale",
        "Harborough",
        "Hammersmith and Fulham",
        "Basingstoke and Deane",
        "Gloucester",
        "Cambridge",
        "Rushmoor",
        "East Hertfordshire",
        "Bury",
        "Bradford",
        "Warrington",
        "York",
        "Cannock Chase",
        "Islington",
        "Tonbridge and Malling",
        "West Northamptonshire",
        "Norwich",
        "Spelthorne",
        "Waltham Forest",
        "Isles of Scilly",
        "Swindon",
        "Rugby",
        "Stoke-on-Trent",
        "Basildon",
        "Westminster",
        "South Northamptonshire",
        "Colchester",
        "Hinckley and Bosworth",
        "Herefordshire",
        "West Oxfordshire",
        "Harlow",
        "Hertsmere",
        "South Somerset",
        "Chesterfield",
        "Mansfield",
        "Melton",
        "Wyre",
        "Rushcliffe",
        "East Northamptonshire",
        "Calderdale",
        "Bournemouth",
        "Chorley",
        "Brent",
        "South Holland",
        "Suffolk Coastal",
        "Wokingham",
        "Epping Forest",
        "Bolton",
        "Wolverhampton",
        "Tendring",
        "Cheshire East",
        "Havant",
        "Stratford-on-Avon",
        "Oadby and Wigston",
        "Havering",
        "West Somerset",
        "Camden",
        "Broadland",
        "Craven",
        "Selby",
        "Cornwall",
        "Manchester",
        "Barnet",
        "Rochford",
        "Ealing",
        "Eastbourne",
        "Amber Valley",
        "Hart",
        "South Gloucestershire",
        "Corby",
        "Three Rivers",
        "Kensington and Chelsea",
        "Somerset West and Taunton",
        "South Oxfordshire",
        "Copeland",
        "Sedgemoor",
        "North Devon",
        "North Gloucestershire",
        "LA1",
        "LA2",
        "LA3",
        "LA4",
        "LA5",
        "LA6",
        "LA7",
        "LA8",
        "LA9",
        "LA10",
    ]
    if schema == "housing_delivery_test":
        la_list.extend(
            [
                "Buckinghamshire",
                "East Suffolk",
                "London Legacy Development Corporation",
                "Old Oak and Park Royal Development Corporation",
            ]
        )
    if schema == "permissions":
        la_list.extend(
            [
                "Buckinghamshire",
                "North Yorkshire",
                "Somerset",
                "Crewe and Nantwich",
                "Macclesfield",
                "East Suffolk",
                "Westmorland and Furness",
                "Cumberland",
            ]
        )
    return la_list


def get_list_of_regions(schema=None):
    """Gets list of regions for use in schema, passing housing_delivery_test adds extra regions"""
    region_list = [
        "Yorkshire and The Humber",
        "East Midlands",
        "West Midlands",
        "South East",
        "London",
        "North East",
        "South West",
        "North West",
        "East of England",
    ]
    if schema == "housing_delivery_test":
        region_list.extend(["Check region"])
    return region_list
