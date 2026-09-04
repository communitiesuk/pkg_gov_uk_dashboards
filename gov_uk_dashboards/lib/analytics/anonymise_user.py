"""Utilities for generating pseudonymous user identifiers for analytics."""

import hashlib
import hmac


def get_anonymous_user_id(email: str, secret_key: str) -> str:
    """Generate a stable pseudonymous user ID from an email address.

    The email address is normalised before being hashed with HMAC-SHA256
    using the supplied secret key.

    Args:
        email: The user's email address.
        secret_key: The secret key used to generate the HMAC digest.

    Returns:
        A hexadecimal HMAC-SHA256 digest representing the user.
    """
    normalised_email = email.strip().lower()

    return hmac.new(
        secret_key.encode(),
        normalised_email.encode(),
        hashlib.sha256,
    ).hexdigest()
