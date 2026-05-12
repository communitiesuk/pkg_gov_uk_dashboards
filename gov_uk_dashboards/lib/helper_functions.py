"""
helper_functions.py
-------------------

A collection of small, reusable utility functions used across the Housing
data pipeline. These functions support common operations such as list handling,
data validation, and general-purpose transformations that are not tied to
specific business logic.

Functions:
    flatten(lst): Recursively flatten a nested list into a single-level iterator.
"""


def flatten(lst):
    """
    Recursively flattens a nested list structure into a single-level iterator.

    Args:
        lst (list): A potentially nested list containing any level of sublists.

    Yields:
        Any: Individual elements from the nested list in a flattened sequence.

    Example:
        >>> list(flatten([1, [2, 3], [4, [5, 6]]]))
        [1, 2, 3, 4, 5, 6]
    """
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item
