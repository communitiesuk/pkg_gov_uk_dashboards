"""Record raw page view events for the Dash app.

This module normalises Dash URL pathnames so equivalent routes are counted as
the same page and supports logging page view events for downstream reporting.
"""


def normalise_pathname(pathname: str | None) -> str:
    """Normalise a Dash pathname for page view reporting.

    Rules:
    - None or empty -> "/"
    - ensure leading slash
    - remove trailing slash except for root
    - treat "/" and "/home" as the same page
    """
    if not pathname:
        return "/"

    normalised = pathname.strip()

    if not normalised:
        return "/"

    if not normalised.startswith("/"):
        normalised = f"/{normalised}"

    if normalised != "/":
        normalised = normalised.rstrip("/")

    if normalised in {"/", "/home"}:
        return "/"

    return normalised
