"""
Absolute path
"""

import os


def absolute_path(file):
    """
    In production the current working directory is NOT set to the repository root.
    This method will convert a path relative to the repository root, to an absolute path.
    """
    lib_folder = os.path.dirname(__file__)
    repository_root = os.path.dirname(lib_folder)
    return os.path.join(os.environ.get("DATA_FOLDER_LOCATION", repository_root), file)
