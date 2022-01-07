from pprint import pprint
from typing import TYPE_CHECKING, Optional

import asyncpg

from app.api.workflow.dcs import (
    CreateOrder,
    UpdateOrder, DeleteOrder,
)

from app.api.workflow.schemas import OrderCreateDataResponseSchema
from app.base.accessor import BaseAccessor
from app.config import Config
from app.databases import Databases, Postgres
from asyncpg import Connection as AsyncpgConnection

if TYPE_CHECKING:
    from app.store import Store


class OrdersAccessor(BaseAccessor):
    def __init__(self, databases: Databases, config: Config, store: 'Store') -> None:
        super().__init__(databases, config, store)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass

    @property
    def conn(self) -> AsyncpgConnection:
        return self.databases.postgres.conn

    async def update(self, data: UpdateOrder) -> Optional[int]:
        query = '''
            update orders set dst_address = $1 where id = $2
            returning id;
        '''

        order_id = await self.conn.fetchval(
            query,
            data.dst_address,
            data.id,
        )

        return order_id

    async def create(self, data: CreateOrder) -> Optional[int]:
        query_order = '''
            insert into orders(customer_id, dst_address, src_address, restaurant_id, employee_id, order_number, status)
            values ($1, $2, $3, $4, $5, $6, $7)
            returning id
        '''

        query_od = '''
            insert into order_details(order_id, product_id, amount)
            values ($1, $2, $3)
        '''

        async with self.conn.transaction():
            order_id = await self.conn.fetchval(
                query_order,
                data.customer_id,
                data.dst_address,
                data.src_address,
                data.restaurant_id,
                data.employee_id,
                data.order_number,
                data.status,
            )

            await self.conn.executemany(
                query_od,
                [
                    (order_id, od.product_id, od.amount)
                    for od in data.products
                ]
            )

        return order_id

    async def delete(self, data: DeleteOrder) -> Optional[int]:
        query = '''
            delete from orders where id = $1
            returning id;
        '''

        order_id = await self.conn.fetchval(
            query,
            data.id,
        )

        return order_id
