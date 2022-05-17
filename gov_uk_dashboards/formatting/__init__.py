"""Module containing tools to assist with formatting of numbers in dashboards.

Contains:
- format_as_human_readable: Format a number as a human readable string, with
    options to customise elements such as prefix and suffix.
- rounding: Functions to round data to the standard rounding we want for display.
    - round_thousands_to_1dp: Rounds values to 1dp in steps of 1000.
"""

from .human_readable import format_as_human_readable
from . import rounding
