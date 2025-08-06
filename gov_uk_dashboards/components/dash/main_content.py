"""main_content"""

import warnings
import re
from dash import html


def main_content(children, id_fragment=None):
    """
    Wrapper for the main content of the dashboard, containing visualisations.

    https://developer.mozilla.org/en-US/docs/Web/HTML/Element/main

    Using semantic HTML elements makes it easier for users with accessibility issues to
    interpret webpages using assistive devices.

    See https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML for more guidance.
    """
    if id_fragment:
        parts = re.split(r"\W+", id_fragment.lower())
        slug = "main-content-" + "-".join(filter(None, parts))
    else:
        slug = ""
        warnings.warn(
            "WARNING: No id_fragment provided to main_content(). This is usually the page heading "
            "and helps create a unique and consistent id attribute. Providing an id_fragment "
            "improves accessibility, aids automated testing, and prevents issues with duplicate or "
            "missing page headings.",
            UserWarning,
            stacklevel=2,
        )
    return html.Main(children, className="main", id=slug, role="main")
