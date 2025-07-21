"""Helper functions for use to plot charts"""

from gov_uk_dashboards.constants import CHART_LABEL_FONT_SIZE


def get_legend_configuration(itemclick=True, itemdoubleclick=True, reverse_order=False):
    """
    Returns the legend configuration for charts with customizable interaction settings.
    Args:
        itemclick (bool): Determines whether clicking on a legend item toggles its visibility.
                          Set to True by default, allowing click interactions.
        itemdoubleclick (bool): Determines the behavior when double-clicking on a legend item.
                                Set to True by default, allowing double-click interactions.
        reverse_order (bool): Whether to reverse legend order. Defaults to False.
    Returns:
        dict: A dictionary containing the configuration settings for the legend.
    """
    traceorder = {} if not reverse_order else {"traceorder": "reversed"}
    return {
        "x": 0,
        "y": -0.22,
        "yanchor": "top",
        "traceorder": "normal",
        "orientation": "h",
        "font": {"size": CHART_LABEL_FONT_SIZE},
        "itemclick": "toggle" if itemclick else False,
        "itemdoubleclick": "toggle" if itemdoubleclick else False,
        **traceorder,
    }


def get_rgba_from_hex_colour_and_alpha(hex_code: str, alpha: float = 1.0) -> str:
    """Get the rgba string corresponding to a hex-code colour and its alpha (opacity)

    Args:
        hex_code (str): hex code for converting (with #), e.g. "#00FF00"
        alpha (float, optional): Desired transparency from 0 to 1. Defaults to 1.0.

    Returns:
        str: rgba string
    """
    if hex_code[0] != "#" or len(hex_code) != 7:
        raise ValueError
    rgb_colour = tuple(int(hex_code[i : i + 2], 16) for i in (1, 3, 5))

    return f"rgba{rgb_colour + (alpha,)}"
