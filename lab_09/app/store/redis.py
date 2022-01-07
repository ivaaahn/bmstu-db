import json
from typing import Optional, TYPE_CHECKING, Union

import aioredis.client

from app.base.accessor import BaseAccessor
from app.config import Config
from app.databases import Databases, Redis, Postgres

if TYPE_CHECKING:
    from app.store import Store


class RedisAccessor(BaseAccessor):
    DEFAULT_KEY = 'DEFAULT_KEY'

    def __init__(self, databases: Databases, config: Config, store: 'Store') -> None:
        super().__init__(databases, config, store)

    @property
    def redis(self) -> Redis:
        return self.databases.redis

    @property
    def cli(self) -> aioredis.client.Redis:
        return self.redis.client

    async def set(self, *, key: str = DEFAULT_KEY, value: Union[list[dict], dict], ttl: int = 3600) -> None:
        await self.cli.set(key, json.dumps(value), ex=ttl)

    async def get(self, *, key: str = DEFAULT_KEY, default: Optional[dict] = None) -> dict:
        if (data_json := await self.cli.get(key)) is not None:
            return json.loads(data_json)
        return default

    async def flush_all(self):
        await self.cli.flushall()

    async def delete(self, key: str):
        await self.cli.delete(key)

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass
