from typing import TYPE_CHECKING

from app.config import Config

from .redis import Redis
from .postgres import Postgres

if TYPE_CHECKING:
    from app.app import Application


class Databases:
    def __init__(self, config: Config) -> None:
        self.redis = Redis(config)
        self.postgres = Postgres(config)

    async def connect(self, _: 'Application') -> None:
        await self.redis.connect()
        await self.postgres.connect()

    async def disconnect(self, _: 'Application') -> None:
        await self.redis.disconnect()
        await self.postgres.disconnect()

    # async def connect_aiohttp(self, _: 'Application') -> None:
    #     await self.mongo.connect()
    #
    # async def disconnect_aiohttp(self, _: 'Application') -> None:
    #     await self.mongo.disconnect()


def setup_databases(config: Config) -> Databases:
    return Databases(config)
