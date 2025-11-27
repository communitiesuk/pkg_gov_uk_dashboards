"""data_quality_banner"""

from enum import Enum
from dataclasses import dataclass
from dash import html
from gov_uk_dashboards.components.dash.notification_banner import notification_banner
from gov_uk_dashboards.formatting.text_functions import create_id_from_string
from gov_uk_dashboards.constants import (
    NOTIFICATION_STYLE_GREEN,
    NOTIFICATION_STYLE_ORANGE,
    NOTIFICATION_STYLE_RED,
    NOTIFICATION_STYLE_YELLOW,
)


@dataclass
class DataQualityConfig:
    """
    Configuration class for defining the display and linking details of a data quality metric.

    Attributes:
        title (str): The title of the data quality metric.
        text (str): Descriptive text or explanation of the metric.
        style (str): The visual style or format for displaying the metric.
        title_color (str, optional): Optional color to use for the title. Defaults to None.
        glossary_url (str, optional): Optional URL linking to a glossary entry for this metric.
            If not provided, a URL is automatically generated based on the title.

    Methods:
        __post_init__(): Automatically generates a glossary URL if none is provided.
    """

    title: str
    text: str
    style: str
    title_color: str = None
    glossary_url: str = None

    def __post_init__(self):
        if not self.glossary_url:
            slug = create_id_from_string(self.title)
            self.glossary_url = f"/glossary#data-quality-{slug}"


class DataQualityLabels(Enum):
    """Enumeration of standard labels used to categorize or describe data quality."""

    OFFICIAL = DataQualityConfig(
        title="OFFICIAL public data",
        text="Use with confidence.",
        style=NOTIFICATION_STYLE_GREEN,
    )
    MI = DataQualityConfig(
        title="Management information",
        text="Use for early insights, but with caution.",
        style=NOTIFICATION_STYLE_YELLOW,
        title_color="black",
    )
    EXPERIMENTAL_MI = DataQualityConfig(
        title="Experimental management information",
        text="Indicative only, requires expert guidance on use.",
        style=NOTIFICATION_STYLE_ORANGE,
        title_color="black",
    )
    OPERATIONAL = DataQualityConfig(
        title="Operational data",
        text="Never use in isolation, always verify independently.",
        style=NOTIFICATION_STYLE_RED,
    )


def data_quality_notification_banner(label: DataQualityLabels):
    """Return data quality notification banner based on Gov UK Design component notification
    banner component."""
    config = label.value
    text = [
        f"{config.text} Read more in our ",
        html.A(
            "glossary",
            href=config.glossary_url,
            target="_blank",
            rel="noopener noreferrer",
        ),
        ".",
    ]
    return notification_banner(
        title=config.title,
        text=text,
        style=config.style,
        title_color=config.title_color,
    )
