"""Logger config module."""

from __future__ import annotations

import json
import logging
import logging.config
from pathlib import Path
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from users_management.core.settings import Settings


def setup_logging(settings: Settings) -> None:
    config_file: Path = settings.paths.PATH_TO_BASE_FOLDER / "log_config.json"
    with open(config_file) as file:
        config = json.load(file)
    logging.config.dictConfig(config)
