import hashlib
import hmac


def get_anonymous_user_id(email: str, secret_key: str) -> str:
    normalised_email = email.strip().lower()

    return hmac.new(
        secret_key.encode(),
        normalised_email.encode(),
        hashlib.sha256,
    ).hexdigest()