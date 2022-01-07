import yaml
from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str
    port: int
    user: str = 'redis'
    password: str = 'redis'
    db: int = 0


@dataclass
class PostgresConfig:
    host: str
    port: int
    db: str
    user: str
    password: str


@dataclass
class Config:
    postgres: PostgresConfig
    redis: RedisConfig


def setup_config(config_path: str) -> Config:
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    return Config(
        postgres=PostgresConfig(**raw_config['postgres']),
        redis=RedisConfig(**raw_config['redis']),
    )
