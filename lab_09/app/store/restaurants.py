from typing import TYPE_CHECKING

from app.base.accessor import BaseAccessor
from app.config import Config
from app.databases import Databases, Postgres
from asyncpg import Connection as AsyncpgConnection, Record

if TYPE_CHECKING:
    from app.store import Store


def rows_to_json(rows: list[Record]) -> list[dict]:
    return [dict(row) for row in rows]


class RestaurantsAccessor(BaseAccessor):
    def __init__(self, databases: Databases, config: Config, store: 'Store') -> None:
        super().__init__(databases, config, store)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    @property
    def conn(self) -> AsyncpgConnection:
        return self.databases.postgres.conn

    async def fetch_stats(self) -> list[dict]:
        query = ''' 
            select r.id, 
                   r.name, 
                   sum(p.price * od.amount) as summary, 
                   count(o.id) as number_of_orders
            from restaurants r
                     join orders o on r.id = o.restaurant_id
                     join order_details od on o.id = od.order_id
                     join products p on r.id = p.restaurant_id
            group by r.id
            order by summary desc;
        '''

        raw_data = await self.conn.fetch(query)

        return rows_to_json(raw_data)

    # async def execute(self, query: str) -> str:
    #     return await self.conn.execute(query)
