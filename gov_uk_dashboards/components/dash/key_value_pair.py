"""key_value_pair"""

import numpy as np
from dash import html


def key_value_pair(key, value):
    """
    Create an HTML element that displays a value (such as a metric) labelled by a key (such as the
    name of the metric).
    """
    if isinstance(value, float):
        value_can_be_displayed = value is not None and not np.isnan(value)
    else:
        value_can_be_displayed = value is not None

    return [
        html.Dt(
            key,
            className="govuk-body-s govuk-!-margin-bottom-0",
        ),
        html.Dd(
            value if value_can_be_displayed else "-",
            className="govuk-heading-m govuk-!-margin-0 govuk-!-padding-0",
        ),
    ]
