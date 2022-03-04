"""phase_banner"""
from dash import html


def phase_banner_with_feedback(
    phase: str, feedback_link: str, link_id: str = "feedback-link"
):
    """Creates a phase banner with a feedback link, which can be specified.
    The id of the 'feedback' link can be set to allow for targeting with callbacks.

    The phase banner is set out here as part of the Gov.UK design system:
    https://design-system.service.gov.uk/components/phase-banner/"""
    return html.Div(
        [
            html.P(
                [
                    html.Strong(
                        [phase],
                        className="govuk-tag govuk-phase-banner__content__tag",
                    ),
                    html.Span(
                        [
                            "This is a new service - your ",
                            html.A(
                                ["feedback"],
                                href=feedback_link,
                                className="govuk-link",
                                id=link_id,
                            ),
                            " will help us to improve it.",
                        ],
                        className="govuk-phase-banner__text",
                    ),
                ],
                className="govuk-phase-banner__content",
            )
        ],
        className="govuk-phase-banner",
    )
