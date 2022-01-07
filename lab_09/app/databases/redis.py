from typing import Optional

from aioredis import from_url, client

from app.base.database import BaseDatabase
from app.config import Config, RedisConfig


class Redis(BaseDatabase):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.client: Optional[client.Redis] = None

    @property
    def cfg(self) -> RedisConfig:
        return self.config.redis

    async def connect(self) -> None:
        cfg = self.cfg

        self.client = from_url(
            url=f'redis://{cfg.host}',
            port=cfg.port,
            # username=cfg.user,
            # password=cfg.password,
            db=cfg.db,
            decode_responses=True,
        )

    async def disconnect(self) -> None:
        await self.client.close()


def setup_redis(config: Config) -> Redis:
    return Redis(config)
