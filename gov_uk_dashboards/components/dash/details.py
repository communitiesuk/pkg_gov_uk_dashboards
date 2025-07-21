"""details"""

from dash import html


def details(details_summary: str, details_text: str) -> html.Details:
    """
    HTML component for showing a summary expandable with more information beneath.

    Makes a page easier to scan by letting users reveal more detailed information
    only if they need it.

    Part of the Gov.UK Design System:
    https://design-system.service.gov.uk/components/details/

    Args:
        details_summary (str): The summary text to display all the time.
        details_text (str): The details to reveal when the use requests them.

    Returns:
        html.Details: A Details HTML element with the specified text
    """
    return html.Details(
        [
            html.Summary(
                [
                    html.Span(
                        details_summary,
                        className="govuk-details__summary-text",
                    )
                ],
                className="govuk-details__summary",
            ),
            html.Div(details_text, className="govuk-details__text"),
        ],
        className="govuk-details",
    )
