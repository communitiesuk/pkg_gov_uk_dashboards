"""Functions to filter sentry errors"""

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


def is_statsbeat_export_timeout(
    event: SentryEvent,
    hint: SentryHint,
) -> bool:
    exceptions = (event.get("exception") or {}).get("values") or []

    exception_text = " ".join(
        f"{exception.get('type', '')} {exception.get('value', '')}"
        for exception in exceptions
    )

    exc_info = hint.get("exc_info")

    if exc_info:
        exception_text += f" {exc_info[0].__name__} {exc_info[1]}"

    return (
        event.get("logger") == "azure.monitor.opentelemetry.exporter.export._base"
        and "ServiceResponseTimeoutError" in exception_text
        and "westeurope-5.in.applicationinsights.azure.com" in exception_text
        and "Read timed out" in exception_text
    )


def is_transient_export_error(
    event: SentryEvent,
    hint: SentryHint,
) -> bool:
    """Return True for transient Azure Monitor telemetry export failures."""

    logger = event.get("logger", "")
    if not logger.startswith("azure.monitor.opentelemetry.exporter.export"):
        return False

    exc_info = hint.get("exc_info")
    if not exc_info:
        return False

    exception_type, exception, _ = exc_info

    return (
        exception_type.__name__ == "ServiceResponseError"
        and "Remote end closed connection without response" in str(exception)
    )


SENTRY_EVENT_FILTERS: list[SentryFilter] = [
    is_transient_live_metrics_error,
    is_statsbeat_export_timeout,
    is_transient_export_error,
]


def before_send(
    event: SentryEvent,
    hint: SentryHint,
) -> SentryEvent | None:
    """Discard events matching any known non-actionable error filter."""

    if any(event_filter(event, hint) for event_filter in SENTRY_EVENT_FILTERS):
        return None

    return event
