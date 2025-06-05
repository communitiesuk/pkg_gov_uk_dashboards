import re


def create_id_from_string(string):
    if string is None:
        return ""
    return re.sub(r"[^a-z0-9]+", "-", string.lower()).strip("-")