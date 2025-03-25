"""Helper functions for use to plot charts"""


from constants import (
    CHART_LABEL_FONT_SIZE,
)


def get_legend_configuration(itemclick=True, itemdoubleclick=True):
    """
    Returns the legend configuration for charts with customizable interaction settings.
    Args:
        itemclick (bool): Determines whether clicking on a legend item toggles its visibility.
                          Set to True by default, allowing click interactions.
        itemdoubleclick (bool): Determines the behavior when double-clicking on a legend item.
                                Set to True by default, allowing double-click interactions.
    Returns:
        dict: A dictionary containing the configuration settings for the legend.
    """
    return {
        "x": 0,
        "y": -0.22,
        "yanchor": "top",
        "traceorder": "normal",
        "orientation": "v",
        "font": {"size": CHART_LABEL_FONT_SIZE},
        "itemclick": "toggle" if itemclick else False,
        "itemdoubleclick": "toggle" if itemdoubleclick else False,
    }
