"""Game config: loads the .env file and sets up logging."""

import os
import logging

from dotenv import load_dotenv

LOG_FILE = "game.log"
LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


def setup():
    """Loads the .env values and sets up logging to game.log. Must run before anything logs."""
    load_dotenv()
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    valid_level = level in LOG_LEVELS
    logging.basicConfig(
        filename=LOG_FILE,
        level=level if valid_level else "INFO",
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    if not valid_level:
        logging.warning(f"LOG_LEVEL '{level}' is not valid, using INFO")
