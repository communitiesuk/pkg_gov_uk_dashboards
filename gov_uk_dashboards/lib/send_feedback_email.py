"""send_feedback_email function"""

from notifications_python_client.notifications import (
    NotificationsAPIClient,
)


def send_feedback_email(
    feedback: str,
    page_path: str,
    environment: str,
    app_name: str,
    email_address: str,
    template_id: str,
    api_key: str
):
    """Send feedback email."""
    client = NotificationsAPIClient(api_key)
    subject = (
        f"You have received feedback on a page in {app_name} dashboard - {environment}"
    )

    email_body = (
        "A user has given feedback on the following page:\n\n"
        f'"{page_path}"\n\n'
        "Here are the responses:\n\n"
        f"- Is this page useful?\n - {feedback}"
    )
    client.send_email_notification(
        email_address=email_address,
        template_id=template_id,
        personalisation={"subject": subject, "email_body": email_body},
    )
