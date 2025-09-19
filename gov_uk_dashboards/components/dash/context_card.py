"""Context card functions"""

from typing import Union
import calendar
from datetime import datetime
import polars as pl
from dateutil.relativedelta import relativedelta
from dash import html
from dash.development.base_component import Component
from gov_uk_dashboards.components.dash import (
    heading2,
)
from gov_uk_dashboards.formatting.number_formatting import add_commas
from gov_uk_dashboards.lib.datetime_functions.datetime_functions import (
    convert_date_string_to_text_string,
)

from gov_uk_dashboards.constants import (
    CHANGED_FROM_GAP_STYLE,
    DATE_VALID,
    LARGE_BOLD_FONT_STYLE,
    LATEST_YEAR,
    MEASURE,
    METRIC_VALUE,
    PERCENTAGE_CHANGE_FROM_PREV_YEAR,
    PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR,
    PREVIOUS_2YEAR,
    PREVIOUS_YEAR,
    TWENTY_NINETEEN,
    TWENTY_NINETEEN_VALUE,
    VALUE,
    YEAR_END,
)


def get_rolling_period_context_card(
    df_function, measure, heading, text_for_main_number, main_number_units=None
):
    """
    Build a context card showing the latest value of a measure with comparisons
    to the previous two years.

    The function fetches data via `df_function`, filters it for the given measure,
    extracts the most recent year, and constructs an HTML card with a heading,
    main value, and percentage change context.

    Args:
        df_function (Callable): A function that returns a Polars DataFrame
            containing the measure of interest.
        measure (str): The measure identifier to filter data by.
        heading (str): The heading text for the context card.
        text_for_main_number (str): Supporting explanatory text displayed under
            the main number.
        main_number_units (str, optional): Units to display after the main number
            (e.g. "%", "days"). Defaults to None.

    Returns:
        html.Div: A GOV.UK-styled HTML div containing the context card.
    """
    df = df_function()
    df_filtered = df.filter(pl.col(MEASURE) == measure)

    latest_year_data = df_filtered.filter(
        pl.col(DATE_VALID) == df_filtered[DATE_VALID].max()
    )

    context_card_data = {
        VALUE: latest_year_data[VALUE][0],
        DATE_VALID: latest_year_data[DATE_VALID][0],
        PERCENTAGE_CHANGE_FROM_PREV_YEAR: latest_year_data[
            PERCENTAGE_CHANGE_FROM_PREV_YEAR
        ][0],
        PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR: latest_year_data[
            PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR
        ][0],
    }
    return html.Div(
        [
            heading2(heading),
            html.Div(
                [
                    _get_rolling_period_data_content_for_x_years(
                        context_card_data, text_for_main_number, main_number_units
                    ),
                ],
                className="govuk-body",
            ),
        ],
        className="context-card-grid-item",
    )


def _get_rolling_period_data_content_for_x_years(
    data, text_for_main_number, main_number_units
):
    formatted_latest_year = convert_date_string_to_text_string(
        data[DATE_VALID], abbreviate_month=False, include_year=True
    )

    current_date = data[DATE_VALID]
    previous_year_datetime = get_a_previous_date(current_date, "previous", False)
    two_years_ago_datetime = get_a_previous_date(current_date, "two_previous", False)
    formatted_year_ago = convert_date_string_to_text_string(
        previous_year_datetime.strftime("%Y-%m-%d"),
        abbreviate_month=False,
        include_year=True,
    )
    formatted_two_years_ago = convert_date_string_to_text_string(
        two_years_ago_datetime.strftime("%Y-%m-%d"),
        abbreviate_month=False,
        include_year=True,
    )

    return html.Div(
        [
            html.Div(
                f"{add_commas(data[VALUE], True)}"
                f"{' ' + main_number_units if main_number_units else ''}",
                className="govuk-body govuk-!-font-weight-bold",
                style=LARGE_BOLD_FONT_STYLE | {"marginBottom": "0px"},
            ),
            html.P(
                f"{text_for_main_number} ending {formatted_latest_year}",
                className="govuk-body",
            ),
            get_changed_from_content(
                calculated_percentage_change=data[PERCENTAGE_CHANGE_FROM_PREV_YEAR],
                use_calculated_percentage_change=True,
                increase_is_positive=True,
                comparison_period_text=f"from same rolling period ending {formatted_year_ago}",
            ),
            html.Div(
                [
                    get_changed_from_content(
                        calculated_percentage_change=data[
                            PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR
                        ],
                        use_calculated_percentage_change=True,
                        increase_is_positive=True,
                        comparison_period_text="from same rolling period "
                        f"ending {formatted_two_years_ago}",
                    ),
                ],
                style=CHANGED_FROM_GAP_STYLE,
            ),
        ],
        # className="context-card-grid-item"
    )


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-positional-arguments
def get_changed_from_content(
    current_value: Union[int, float] = None,
    previous_value: Union[int, float] = None,
    calculated_percentage_change=None,
    increase_is_positive: bool = True,
    comparison_period_text: str = "",
    use_previous_value_rather_than_change: bool = False,
    use_difference_in_weeks_days: bool = False,
    percentage_change_rounding: int = 1,
    use_calculated_percentage_change: bool = False,
    use_number_rather_than_percentage: bool = False,
) -> Component:
    """
    Build an HTML component describing how a metric has changed over time.

    Depending on arguments, this function renders either:
    - a percentage change between current and previous values,
    - the absolute previous value,
    - or the difference expressed in weeks/days.

    Styling and arrows (up, down, right) are applied to indicate direction
    and whether an increase is considered positive.

    Args:
        current_value (Union[int, float], optional): The current metric value. Defaults to None.
        previous_value (Union[int, float], optional): The previous metric value. Defaults to None.
        calculated_percentage_change (float, optional): Pre-calculated percentage change
            (e.g. from a database). Used only if `use_calculated_percentage_change=True`.
            Defaults to None.
        increase_is_positive (bool, optional): Whether an increase is considered a positive change.
            Defaults to True.
        comparison_period_text (str, optional): Text describing the comparison period
            (e.g. "last year", "previous quarter"). Defaults to "".
        use_previous_value_rather_than_change (bool, optional): If True, show the actual previous
            value instead of a calculated change. Defaults to False.
        use_difference_in_weeks_days (bool, optional): If True, show the difference in
            weeks/days (requires `current_value` and `previous_value` as day counts).
            Defaults to False.
        percentage_change_rounding (int, optional): Decimal places to round percentage change.
            Defaults to 1.
        use_calculated_percentage_change (bool, optional): If True, use the supplied
            `calculated_percentage_change` instead of computing it. Defaults to False.
        use_number_rather_than_percentage (bool, optional): If True, display the change as
            an absolute number instead of a percentage. Defaults to False.

    Returns:
        Component: An HTML component (Dash) representing the change, styled with GOV.UK classes.

    Raises:
        ValueError: If `use_previous_value_rather_than_change` and
            `use_difference_in_weeks_days` are both True.
    """
    if use_previous_value_rather_than_change and use_difference_in_weeks_days:
        raise ValueError(
            "use_previous_value_rather_than_percentage_change and use_difference_in_weeks_days "
            "both cannot be true"
        )
    if use_calculated_percentage_change:
        percentage_change = calculated_percentage_change
    else:
        percentage_change = ((current_value - previous_value) / previous_value) * 100

    if percentage_change is None:
        return None
    if percentage_change > 0:
        colour = "green" if increase_is_positive else "red"
        arrow_direction = "up"
        prefix = "up"
    elif percentage_change < 0:
        colour = "red" if increase_is_positive else "green"
        arrow_direction = "down"
        prefix = "down"
    else:
        colour = "grey"
        arrow_direction = "right"  # this needs implementing in CSS
        prefix = ""

    box_style_class = f"govuk-tag govuk-tag--{colour} changed-from-box-formatting"
    if percentage_change != 0:
        box_style_class = (
            box_style_class + f" changed-from-arrow_{arrow_direction}_{colour}"
        )

    content = []
    if use_number_rather_than_percentage:
        unit = ""
    else:
        unit = "%"

    if use_previous_value_rather_than_change:
        content.append(
            html.Span(
                f"{prefix} from " if percentage_change != 0 else "unchanged from ",
                className="govuk-body-s govuk-!-margin-bottom-0 text-color-inherit"
                + " text-no-transform",  # text-no-transform prevents capitalisation,
                # which is added from govuk-tag class
            )
        )
        content.append(
            html.Span(
                f"{previous_value}{unit}",
                className="govuk-body-s govuk-!-margin-bottom-0 govuk-!-margin-right-1 "
                + "changed-from-number-formatting",
            )
        )
    elif use_difference_in_weeks_days:
        difference_in_weeks_and_days = convert_days_to_weeks_and_days(
            current_value - previous_value
        )
        if percentage_change > 0:
            comparison_period_text_prefix = "slower than "
        elif percentage_change < 0:
            comparison_period_text_prefix = "faster than "
        else:
            comparison_period_text_prefix = "unchanged from "

        comparison_period_text = comparison_period_text_prefix + comparison_period_text
        if percentage_change != 0:
            content.append(
                html.Span(
                    f"{difference_in_weeks_and_days}",
                    className="govuk-body-s govuk-!-margin-bottom-0 govuk-!-margin-right-1 "
                    + "changed-from-number-formatting"
                    + " text-no-transform",  # text-no-transform prevents capitalisation,
                    # which is added from govuk-tag class,
                )
            )
    else:
        content.append(
            html.Span(
                f"{prefix} " if percentage_change != 0 else "unchanged from ",
                className="govuk-body-s govuk-!-margin-bottom-0 text-color-inherit"
                + " text-no-transform",  # text-no-transform prevents capitalisation,
                # which is added from govuk-tag class
            )
        )
        content.append(
            html.Span(
                f"{round(abs(percentage_change), percentage_change_rounding)}{unit}",
                className="govuk-body-s govuk-!-margin-bottom-0 govuk-!-margin-right-1 "
                + "changed-from-number-formatting",
            )
        )

    content.append(
        html.Span(
            comparison_period_text,
            className="govuk-body-s govuk-!-margin-bottom-0 text-color-inherit"
            + " text-no-transform",  # text-no-transform prevents capitalisation,
            # which is added from govuk-tag class
        )
    )

    return html.Div(
        [
            html.Div(
                content,
                className=box_style_class,
            ),
        ]
    )


def convert_days_to_weeks_and_days(
    total_days: int,
) -> str:
    """Converts a given number of total days into a string representing the equivalent number
    of weeks and days.

    Args:
        total_days (int): The total number of days to convert. This value can be positive
                          or negative; the absolute value will be used.

    Returns:
        str: A string in the format 'x weeks and y days', where x is the number of weeks
             and y is the number of days. The correct pluralization ('week'/'weeks' and
             'day'/'days') is applied based on the values."""
    if not isinstance(total_days, int):
        raise ValueError("total_days must be an int")
    total_days = abs(total_days)
    weeks = total_days // 7
    days = total_days % 7
    week_or_weeks = "week" if weeks == 1 else "weeks"
    day_or_days = "day" if days == 1 else "days"
    return f"{weeks} {week_or_weeks} and {days} {day_or_days}"


def get_data_for_context_card(
    measure: str,
    df: pl.DataFrame,
    value_column: str = VALUE,
    include_data_from_2_years_ago: bool = False,
    display_value_as_int: bool = False,
    abbreviate_month: bool = True,
    include_percentage_change: bool = False,
    include_2019: bool = True,
    data_expected_for_previous_year_and_previous_2years: bool = True,
) -> dict:
    # pylint: disable=too-many-locals
    """
    Fetches the latest year, previous year, 2019 data and optionally data from 2 years ago for a
    specific measure.
    Args:
        measure (str): The measure for which data is to be fetched.
        df (pl.DataFrame): The dataframe to fetch the measure from.
        value_column (str): The name of the column to get the value for.
        include_data_from_2_years_ago (bool): Whether to include data from 2 years ago. Defaults
        to False.
        display_value_as_int (bool): Whether to display the value as an int. Defaults to False.
        abbreviate_month (bool): Whether to abbreviate the month. Defaults to True.
        include_percentage_change (bool): Whether to include percentage change from previous year
            and 2 years ago. Defaults to False.
        include_2019 (bool): Whether to include data from 2019. Defaults to True.
        data_expected_for_previous_year_and_previous_2years (bool): Whether data is expexcted for
            previous 2 years. Defaults to True. If True raises a value error if data not found,
            otherwise returns None.
    Returns:
        dict: A dictionary containing the latest year and previous year, and optionally 2019 and
        optionally 2 years ago data for the specified measure and percentage change.
    """
    df_measure = df.filter(df[MEASURE] == measure)
    if display_value_as_int:
        df_measure = df_measure.with_columns(df_measure[value_column].cast(pl.Int32))
    latest_date = df_measure[DATE_VALID].max()
    previous_year_date = get_a_previous_date(latest_date, "previous")
    latest_data = get_latest_data_for_year(
        df_measure,
        latest_date,
        value_column,
        abbreviate_month=abbreviate_month,
        data_expected=True,
        include_percentage_change=include_percentage_change,
    )
    date_of_latest_data = latest_data[DATE_VALID]

    previous_year_data = get_latest_data_for_year(
        df_measure,
        previous_year_date,
        value_column,
        abbreviate_month,
        data_expected_for_previous_year_and_previous_2years,
        include_percentage_change,
        date_of_latest_data,
    )

    data_to_return = {
        LATEST_YEAR: latest_data,
        PREVIOUS_YEAR: previous_year_data,
    }

    if include_2019:
        twenty_nineteen_data = df_measure.get_column(TWENTY_NINETEEN_VALUE)[0]
        data_to_return = {
            **data_to_return,
            TWENTY_NINETEEN: {METRIC_VALUE: twenty_nineteen_data},
        }

    if include_data_from_2_years_ago:
        date_2_years_ago = get_a_previous_date(previous_year_date, "previous")
        data_from_2_years_ago = get_latest_data_for_year(
            df_measure,
            date_2_years_ago,
            value_column,
            abbreviate_month,
            data_expected_for_previous_year_and_previous_2years,
            include_percentage_change,
            previous_year_date,
        )
        data_to_return = {**data_to_return, PREVIOUS_2YEAR: data_from_2_years_ago}

    return data_to_return


def get_a_previous_date(
    date_str: str, desired_year="previous", return_string=True
) -> Union[str, datetime]:
    "desired_year can either be previous or a year int eg. 2024"
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if desired_year == "previous":
        desired_year = date.year - 1
    if desired_year == "two_previous":
        desired_year = date.year - 2
    try:
        new_date = date.replace(year=desired_year)
        if calendar.isleap(desired_year) and date.month == 2 and date.day == 28:
            new_date = datetime(desired_year, 2, 29)
    except ValueError:
        # This handles the case where the original date is February 29th in a leap year
        # Since the resulting year won't be a leap year, we subtract one year and set the date to
        # February 28th
        new_date = date.replace(year=desired_year, month=2, day=28)
    # Format the new date back into a string

    if return_string:
        new_date_str = new_date.strftime("%Y-%m-%d")
        return new_date_str
    return new_date


def get_latest_data_for_year(
    df_measure: pl.DataFrame,
    date: str,
    value_column: str,
    abbreviate_month: bool,
    data_expected: bool = True,
    include_percentage_change: bool = False,
    date_of_latest_data=None,
) -> dict:
    """
    Retrieve the most recent metric value for a given reference date.

    This function looks up data for the specified `date` in the provided
    DataFrame. If data exists, it returns the latest entry (or the entry
    corresponding to one year before `date_of_latest_data`, if provided).
    Optionally, percentage changes from previous years can be included.

    Args:
        df_measure (pl.DataFrame): Source DataFrame containing the data.
        date (str): The reference date (format: YYYY-MM-DD) to search for.
        value_column (str): Column name containing the metric value.
        abbreviate_month (bool): Whether to abbreviate month names in output text.
        data_expected (bool, optional): If True, raises a ValueError when no
            matching data is found. If False, returns None values instead.
            Defaults to True.
        include_percentage_change (bool, optional): If True, includes percentage
            change from the previous year and two years prior. Defaults to False.
        date_of_latest_data (str, optional): A specific "latest data" date
            (format: YYYY-MM-DD). If provided, returns the value from one year
            before this date instead of the latest available.

    Returns:
        dict: A dictionary containing:
            - YEAR_END (str): Formatted year-end date.
            - METRIC_VALUE: The metric value (or None if not found).
            - DATE_VALID (str): The raw date corresponding to the result.
            - PERCENTAGE_CHANGE_FROM_PREV_YEAR (optional): Change vs. previous year.
            - PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR (optional): Change vs. two years prior.

    Raises:
        ValueError: If no matching data is found when `data_expected=True`.
    """
    year_data = df_measure.filter(df_measure[DATE_VALID] == date)

    if year_data.height == 0:
        if data_expected:
            raise ValueError(f"No data found for the date: {date}")
        return {
            YEAR_END: convert_date_string_to_text_string(
                date,
                include_day_of_month=False,
                abbreviate_month=abbreviate_month,
            ),
            METRIC_VALUE: None,
            DATE_VALID: date,
            **(
                {
                    PERCENTAGE_CHANGE_FROM_PREV_YEAR: None,
                    PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR: None,
                }
                if include_percentage_change
                else {}
            ),
        }
    if date_of_latest_data:
        date_of_latest_data_dt = datetime.strptime(date_of_latest_data, "%Y-%m-%d")

        one_year_before = date_of_latest_data_dt - relativedelta(years=1)

        # If the original date was Feb 28 and the new year is a leap year, adjust to Feb 29
        if (
            date_of_latest_data_dt.month == 2
            and date_of_latest_data_dt.day == 28
            and one_year_before.year % 4 == 0
            and (one_year_before.year % 100 != 0 or one_year_before.year % 400 == 0)
        ):
            one_year_before = one_year_before.replace(day=29)

        one_year_before_str = one_year_before.strftime("%Y-%m-%d")
        target_date_data = year_data.filter(pl.col(DATE_VALID) == one_year_before_str)
        if target_date_data.height == 0:
            raise ValueError(
                f"No data found for the date {date} with date {one_year_before}"
            )
    else:
        target_date_data = year_data.sort(DATE_VALID, descending=True).head(1)

    output = {
        YEAR_END: convert_date_string_to_text_string(
            target_date_data.get_column(DATE_VALID)[0],
            include_day_of_month=False,
            abbreviate_month=abbreviate_month,
        ),
        METRIC_VALUE: target_date_data.get_column(value_column)[0],
        DATE_VALID: target_date_data.get_column(DATE_VALID)[0],
    }

    if include_percentage_change:
        output[PERCENTAGE_CHANGE_FROM_PREV_YEAR] = target_date_data.get_column(
            PERCENTAGE_CHANGE_FROM_PREV_YEAR
        )[0]

        output[PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR] = target_date_data.get_column(
            PERCENTAGE_CHANGE_FROM_TWO_PREV_YEAR
        )[0]
    return output
