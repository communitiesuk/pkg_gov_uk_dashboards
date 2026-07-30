from collections.abc import Callable
from typing import Any

SentryEvent = dict[str, Any]
SentryHint = dict[str, Any]
SentryFilter = Callable[[SentryEvent, SentryHint], bool]


def is_transient_live_metrics_error(
    event: SentryEvent,
    hint: SentryHint,
) -> bool:
    """Return True for known transient Azure Live Metrics ping failures."""

    logger = event.get("logger", "")

    if not logger.startswith("azure.monitor.opentelemetry.exporter._quickpulse"):
        return False

    log_entry = event.get("logentry") or {}
    message = log_entry.get("formatted") or log_entry.get("message") or ""

    if "Exception occurred while pinging live metrics" not in message:
        return False

    exc_info = hint.get("exc_info")

    if not exc_info:
        return False

    exception_type, exception, _ = exc_info
    exception_name = exception_type.__name__
    exception_message = str(exception)

    return (
        exception_name == "HttpResponseError"
        and "Service Unavailable" in exception_message
    ) or (
        exception_name == "ServiceResponseError"
        and "Remote end closed connection without response" in exception_message
    )


SENTRY_EVENT_FILTERS: list[SentryFilter] = [
    is_transient_live_metrics_error,
]


def before_send(
    event: SentryEvent,
    hint: SentryHint,
) -> SentryEvent | None:
    """Discard events matching any known non-actionable error filter."""

    if any(event_filter(event, hint) for event_filter in SENTRY_EVENT_FILTERS):
        return None

    return event
