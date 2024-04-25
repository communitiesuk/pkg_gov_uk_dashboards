"""
Read government dashboard template
"""
import os


def read_template(favicon_path: str = r"assets\images\gov_favicon.ico") -> str:
    """
    Read the government html template.
    Args:
        favicon_path (str): Optional file path to favicon.
    :return: String version of the template.
    """
    path = os.path.dirname(__file__)
    path = os.path.join(path, "template.html")
    with open(path, encoding="utf-8") as file:
        template = file.read()
        return template.replace("{{favicon_path}}", favicon_path)
