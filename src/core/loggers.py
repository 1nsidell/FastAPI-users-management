"""
Logger config module.
"""

import json
import logging
import logging.config
from pathlib import Path

from src.settings import Settings


def setup_logging(settings: Settings):
    """Function to apply the logging settings."""
    config_file: Path = settings.paths.PATH_TO_BASE_FOLDER / "log_config.json"
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
