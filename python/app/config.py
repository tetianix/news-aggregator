import os
from pathlib import Path

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"


def config_path() -> Path:
    custom = os.getenv("CONFIG")
    if custom:
        return Path(custom)
    own = CONFIG_DIR / "config.yaml"
    return own if own.exists() else CONFIG_DIR / "config.example.yaml"


def load_config() -> dict:
    with open(config_path(), encoding="utf-8") as file:
        return yaml.safe_load(file) or {}
