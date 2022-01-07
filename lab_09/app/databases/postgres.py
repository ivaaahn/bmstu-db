from pprint import pprint
from typing import Optional
from asyncpg import Connection, connect as asyncpg_connect

from app.base.database import BaseDatabase
from app.config import Config, PostgresConfig


class Postgres(BaseDatabase):
    def __init__(self, config: Config) -> None:
        super().__init__(config)
        self.conn: Optional[Connection] = None

    @property
    def cfg(self) -> PostgresConfig:
        return self.config.postgres

    async def connect(self) -> None:
        c = self.cfg
        self.conn = await asyncpg_connect(
            user=c.user,
            password=c.password,
            database=c.db,
            host=c.host,
            port=c.port,
        )
        
    async def disconnect(self) -> None:
        await self.conn.close()


def setup_postgres(config: Config) -> Postgres:
    return Postgres(config)
