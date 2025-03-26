"""create_download_chart_button"""

from dash import html
from gov_uk_dashboards.components.dash import download_button_with_icon


def create_download_chart_button(button_id_name: str) -> html.Div:
    """Create a download button for charts, aligned to the right.

    Parameters:
    - button_id_name (str): A unique identifier for the button.

    Returns:
    - html.Div: A Div element containing a download button.
    """
    return html.Div(
        download_button_with_icon(
            button_text="Download chart",
            button_id={
                "download-type": "download-chart",
                "name": button_id_name,
            },
        ),
        style={"textAlign": "right"},
    )
