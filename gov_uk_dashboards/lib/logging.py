"""Module for logging configuration"""

import os

import logging


def configure_logging():
    """Configure logging to a given level."""
    logging_level = os.environ.get("LOGGING_LEVEL")
    if not logging_level:
        logging_level = logging.INFO

    logger = logging.getLogger("root")
    logger.setLevel(logging_level)
    logging.basicConfig()
