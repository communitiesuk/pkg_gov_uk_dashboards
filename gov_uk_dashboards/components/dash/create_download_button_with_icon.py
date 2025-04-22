"""create_download_button_with_icon"""

from dash import html

from gov_uk_dashboards.constants import DOWNLOAD_BUTTON_CLASSES


def create_download_button_with_icon(
    button_text: str, button_id_name: str
) -> html.Button:
    """Create a download button with icon, aligned to the left.

    Parameters:
    - button_id_name (str): A unique identifier for the button.

    Returns:
    - html.Button: Download button.
    """
    download_type = button_text.lower().replace(" ", "-")
    return html.Button(
        [
            html.Div("", className="download-icon"),
            button_text,
        ],
        id={
            "download-type": download_type,
            "name": button_id_name,
        },
        n_clicks=0,
        className=DOWNLOAD_BUTTON_CLASSES,
        type="submit",
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
        },
    )
