"""Logging utility for KPI runs.

This module provides a reusable function `log_message` that appends
a message to a KPI log file, prefixed with a UK-time timestamp
(including milliseconds). It can be called directly from the command
line or imported and reused in other scripts.
"""

import sys
import os
from datetime import datetime
from zoneinfo import ZoneInfo

# Path to KPI log file (should be provided via environment variable)
KPI_LOG = os.environ.get("KPI_LOG_FILE")
UK_TZ = ZoneInfo("Europe/London")


def log_message(message: str) -> None:
    """Write a message to the KPI log with a UK-time timestamp.

    Args:
        message (str): The log message to append.
    """
    timestamp = datetime.now(UK_TZ).strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]  # keep ms
    line = f"[{timestamp}] {message}\n"

    with open(KPI_LOG, "a", encoding="utf-8") as f:
        f.write(line)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    MESSAGE = " ".join(sys.argv[1:])
    log_message(MESSAGE)
