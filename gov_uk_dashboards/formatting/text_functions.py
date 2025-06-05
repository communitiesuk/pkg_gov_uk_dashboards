"""Functions to format text"""

import re


def create_id_from_string(string):
    """Function to create an id from a string. Remove non alphanumeric characters and replaces
    spaces with dashes"""
    if string is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "-", string.lower()).strip("-")
