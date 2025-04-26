"""Logger config module."""

import json
import logging
import logging.config
from pathlib import Path

from users_management.core.settings import Paths


def setup_logging(paths: Paths) -> None:
    config_file: Path = paths.PATH_TO_BASE_FOLDER / "log_config.json"
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
