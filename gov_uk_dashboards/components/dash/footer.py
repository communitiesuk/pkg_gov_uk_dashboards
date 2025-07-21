"""footer"""

from typing import Optional
from dash import html


def footer(footer_links: Optional[list[any]]):
    """
    HTML component for a Gov.UK standard footer.

    The footer provides copyright, licensing and other information about your
    service and department.

    Part of the Gov.UK Design System:
    https://design-system.service.gov.uk/components/footer/

    Returns:
        html.Footer: A footer element with copyright information.
    """
    return html.Footer(
        html.Div(
            html.Div(
                [
                    html.Div(
                        [
                            (
                                html.H2(
                                    "Support Links", className="govuk-visually-hidden"
                                )
                                if footer_links
                                else None
                            ),
                            (
                                html.Ul(
                                    children=[
                                        html.Li(
                                            item,
                                            className="govuk-footer__inline-list-item",
                                        )
                                        for item in footer_links
                                    ],
                                    className=(
                                        "govuk-footer__inline-list "
                                        "govuk-!-display-none-print"
                                    ),
                                )
                                if footer_links
                                else None
                            ),
                            html.Span(
                                [
                                    "All content is available under the ",
                                    html.A(
                                        "Open Government Licence v3.0",
                                        rel="license",
                                        href="https://www.nationalarchives.gov.uk/doc/"
                                        "open-government-licence/version/3/",
                                        className="govuk-footer__link",
                                        target="_blank",
                                    ),
                                    ", except where otherwise stated",
                                ],
                                className="govuk-footer__licence-description",
                            ),
                        ],
                        className="govuk-footer__meta-item govuk-footer__meta-item--grow",
                    ),
                    html.Div(
                        html.A(
                            "© Crown copyright",
                            className="govuk-footer__link pyvis-govuk-footer__copyright-logo",
                            href="https://www.nationalarchives.gov.uk/information-management/"
                            "re-using-public-sector-information/uk-government-licensing-framework/"
                            "crown-copyright/",
                            target="_blank",
                        ),
                        className="govuk-footer__meta-item",
                    ),
                ],
                className="govuk-footer__meta",
            ),
            className="govuk-width-container",
        ),
        className="govuk-footer",
        role="contentinfo",
    )
