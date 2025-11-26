from dataclasses import dataclass
from enum import Enum
from gov_uk_dashboards.components.dash.notification_banner import notification_banner
from gov_uk_dashboards.constants import (
    NOTIFICATION_STYLE_GREEN,
    NOTIFICATION_STYLE_ORANGE,
    NOTIFICATION_STYLE_RED,
    NOTIFICATION_STYLE_YELLOW,
)


@dataclass
class DataQualityConfig:
    title: str
    text: str
    style: str
    title_color: str = None


class DataQualityLabels(Enum):
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
        text="Use only as a directional indicator, and seek expert advice before acting. ",
        style=NOTIFICATION_STYLE_ORANGE,
        title_color="black",
    )
    OPERATIONAL = DataQualityConfig(
        title="Operational data",
        text="Never use in isolation—always verify independently.",
        style=NOTIFICATION_STYLE_RED,
    )


def data_quality_notification_banner(label: DataQualityLabels):
    config = label.value
    return notification_banner(
        title=config.title,
        text=config.text,
        style=config.style,
        title_color=config.title_color,
    )
