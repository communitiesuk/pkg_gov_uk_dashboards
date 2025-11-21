"""download_button"""

from typing import Union
from dash import html

from gov_uk_dashboards.constants import DOWNLOAD_BUTTON_CLASSES


def create_download_button_with_icon(
    button_text: str,
    button_id_name: str,
    instance: Union[str, int] = None,
    download_type: str = None,
) -> html.Button:
    """Create a download button with icon, aligned to the left.

    Parameters:
    - button_text (str): Text to display on button.
    - button_id_name (str): A unique identifier for the button.
    - instance (Union[int,str]): Optional additional id parameter for when button_text is
        "Download map".

    Returns:
    - html.Button: Download button.
    """
    if download_type:
        download_type = f"download-{download_type}"
    else:
        download_type = button_text.lower().replace(" ", "-")
    if button_text == "Download map":
        id_dict = {
            "download-type": download_type,
            "name": button_id_name,
            "instance": instance,
        }
    else:
        id_dict = {"download-type": download_type, "name": button_id_name}
    return html.Button(
        [
            html.Div("", className="download-icon"),
            button_text,
        ],
        id=id_dict,
        n_clicks=0,
        className=DOWNLOAD_BUTTON_CLASSES,
        type="submit",
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
        },
    )
