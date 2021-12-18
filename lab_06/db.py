import asyncpg

from config import DatabaseConfig


async def setup_connection(c: DatabaseConfig):
    return await asyncpg.connect(
        user=c.username,
        password=c.password,
        database=c.database,
        host=c.host,
        port=c.port,
    )
