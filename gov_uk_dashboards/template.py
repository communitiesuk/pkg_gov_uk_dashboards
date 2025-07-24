"""
Read government dashboard template
"""

import os


def read_template(favicon_path: str = r"assets\images\MHCLG_favicon.png") -> str:
    """
    Read the government html template.
    Args:
        favicon_path (str): Optional file path to favicon.
    :return: String version of the template.
    """
    gtag = os.environ.get("GTAG", "")
    path = os.path.join(os.path.dirname(__file__), "template.html")

    with open(path, encoding="utf-8") as file:
        template = file.read()

        rendered_template = template.replace("{{favicon_path}}", favicon_path)
        rendered_template = rendered_template.replace("{{gtag}}", gtag)
        return rendered_template
