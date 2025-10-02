import sys
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# Change this to the path of your KPI log file
KPI_LOG = os.environ.get("KPI_LOG_FILE")
UK_TZ = ZoneInfo("Europe/London")


def log_message(message: str):
    # UTC timestamp with milliseconds
    ts = datetime.now(UK_TZ).strftime("%Y-%m-%d %H:%M:%S.%f")[
        :-4
    ]  # drop last 3 digits for ms
    line = f"[{ts}] {message}\n"

    with open(KPI_LOG, "a", encoding="utf-8") as f:
        f.write(line)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    msg = " ".join(sys.argv[1:])
    log_message(msg)
