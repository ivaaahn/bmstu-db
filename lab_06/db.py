import asyncpg
from asyncpg import Connection

from config import DatabaseConfig


async def setup_connection(c: DatabaseConfig) -> Connection:
    return await asyncpg.connect(
        user=c.username,
        password=c.password,
        database=c.database,
        host=c.host,
        port=c.port,
    )
