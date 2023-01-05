"""Module containing Enums for Gov.UK colours and ONS Accessible Colours.

Contains:
- GovUKColours: From the GOV.UK colour scheme:
    https://design-system.service.gov.uk/styles/colour/
- ONSAccessibleColours: ONS colours taken from the Subnational Indicators Explorer.
"""
from enum import Enum


class GovUKColours(Enum):
    """
    From the GOV.UK colour scheme: https://design-system.service.gov.uk/styles/colour/
    """

    RED = "#d4351c"
    YELLOW = "#ffdd00"
    GREEN = "#00703c"
    BLUE = "#1d70b8"
    DARK_BLUE = "#003078"
    LIGHT_BLUE = "#5694ca"
    PURPLE = "#4c2c92"
    BLACK = "#0b0c0c"
    DARK_GREY = "#505a5f"
    MID_GREY = "#b1b4b6"
    LIGHT_GREY = "#f3f2f1"
    WHITE = "#ffffff"
    LIGHT_PURPLE = "#6f72af"
    BRIGHT_PURPLE = "#912b88"
    PINK = "#d53880"
    LIGHT_PINK = "#f499be"
    ORANGE = "#f47738"
    BROWN = "#b58840"
    LIGHT_GREEN = "#85994b"
    TURQUOISE = "#28a197"
    DLUHC_BLUE = "#092237"

    RED_LIGHT_TO_DARK = ["#fbebe8", "#ea9a8e", "#d4351c", "#6a1b0e", "#150503"]
    BLUE_LIGHT_TO_DARK = [
        "#e8f1f8",
        "#77a9d4",
        "#1d70b8",
        "#11436e",
        "#092237",
    ]


class ONSAccessibleColours(Enum):
    """ONS colours taken from their Subnational indicators explorer
    (https://www.ons.gov.uk/peoplepopulationandcommunity/wellbeing/articles/
    subnationalindicatorsexplorer/2022-01-06)

    Orange added to differentiate from CIPFA light blue
    """

    DARK_BLUE = "#206095"
    LIME = "#a8bd3a"
    MAROON = "#871a5b"
    # LIGHT_BLUE = "#27a0cc"
    ORANGE = "#f47738"
