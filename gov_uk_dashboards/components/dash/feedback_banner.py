import urllib
from dash import html
from gov_uk_dashboards.components.dash import heading2, paragraph

def get_feedback_banner(page_path: str, app_name: str, email_address: str):
    new_user_email_request_body = (
        "Please provide email addresses to request new users for the "
        "Explore Data platform. We will add requested users as soon as possible. Thanks.\n\n"
    )

    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H2(
                                        "Is this page useful?",
                                        style={"marginRight": "20px"},
                                    ),
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    html.Button(
                                                        ["Yes"],
                                                        id="feedback-yes",
                                                        className="govuk-button feedback-button",
                                                    )
                                                ],
                                                className="feedback-list-item",
                                            ),
                                            html.Li(
                                                [
                                                    html.Button(
                                                        ["No"],
                                                        id="feedback-no",
                                                        className="govuk-button feedback-button",
                                                    )
                                                ],
                                                className="feedback-list-item",
                                            ),
                                        ],
                                        className="feedback-list",
                                    ),
                                ],
                                className="feedback-question-answer",
                            )
                        ],
                        className="feedback-questions",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Ul(
                                        [
                                            html.Li(
                                                [
                                                    html.A(
                                                        "Report a problem with this page",
                                                        id="feedback-problem",
                                                        href=(
                                                            f"mailto:{email_address}?subject=Problem found "
                                                            f"in product: '{app_name}', page: '{page_path}'"
                                                        ),
                                                        className="govuk-button feedback-button",
                                                    )
                                                ],
                                                className="feedback-list-item",
                                            ),
                                            html.Li(
                                                [
                                                    html.A(
                                                        "Request a new user",
                                                        id="new-user-request",
                                                        href=(
                                                            f"mailto:{email_address}?subject=New user request "
                                                            f"in product: '{app_name}'"
                                                            f"&body={urllib.parse.quote(new_user_email_request_body)}"
                                                        ),
                                                        className="govuk-button feedback-button",
                                                    )
                                                ],
                                                className="feedback-list-item",
                                            ),
                                        ],
                                        className="feedback-list",
                                    ),
                                ],
                                className="feedback-question-answer",
                            ),
                        ],
                        className="feedback-questions",
                    ),
                ],
                id="feedback-inner-content",
                className="feedback-content",
            )
        ],
        className="feedback-container",
    )
    
def get_thank_you_message(
    button_id: str, feedback_email_subject: str, email_address: str
):
    return html.Div(
        [
            heading2("Thank you."),
            (
                paragraph(
                    [
                        "If you would like to provide further feedback, email us at: ",
                        html.A(
                            email_address,
                            href=(
                                f"mailto:{email_address}?"
                                f"subject={feedback_email_subject}"
                            ),
                        ),
                        ".",
                    ]
                )
                if button_id != "feedback-problem"
                else None
            ),
        ],
        style={"paddingTop": "20px", "paddingLeft": "20px", "paddingBottom": "20px"},
    )