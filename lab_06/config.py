from dataclasses import dataclass
from typing import Optional

import yaml


@dataclass
class DatabaseConfig:
    database: str
    host: str = "127.0.0.1"
    port: int = 5432
    username: Optional[str] = None
    password: Optional[str] = None


def setup_config(config_path: str) -> DatabaseConfig:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
        return DatabaseConfig(**raw_config["database"])

