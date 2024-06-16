import logging.config as logger_config
from pathlib import Path

import yaml

LOGGER_CONFIG_PATH = Path(__file__).parent / "logger_config.yaml"


def setup_logging() -> None:
    """Setup logging configuration"""
    with LOGGER_CONFIG_PATH.open() as f:
        config = yaml.safe_load(f.read())
    logger_config.dictConfig(config)
