"""phase_banner"""

from dash import html


def phase_banner_with_feedback(
    phase: str,
    feedback_link: str = None,
    link_id: str = "feedback-link",
    link_target: str = "_self",
):
    """Creates a phase banner with an optional feedback link.

    The id of the 'feedback' link can be set to allow for targeting with callbacks.
    By default the link will open on the same window, to open in a new window, set link_target
    to "_blank".

    GOV.UK design system reference:
    https://design-system.service.gov.uk/components/phase-banner/
    """

    # Always include the phase tag
    content_children = [
        html.Strong(
            [phase],
            className="govuk-tag govuk-phase-banner__content__tag",
        )
    ]

    # Add feedback link text if provided
    if feedback_link:
        content_children.append(
            html.Span(
                [
                    "This is a new service - your ",
                    html.A(
                        ["feedback"],
                        href=feedback_link,
                        className="govuk-link",
                        id=link_id,
                        target=link_target,
                        rel="noopener noreferrer" if link_target == "_blank" else "",
                    ),
                    " will help us to improve it.",
                ],
                className="govuk-phase-banner__text",
            )
        )

    # Return the banner
    return html.Div(
        html.P(content_children, className="govuk-phase-banner__content"),
        className="govuk-phase-banner",
    )
