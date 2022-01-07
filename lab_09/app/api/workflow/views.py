from random import randint

from aiohttp_apispec import (
    docs,
    json_schema,
    response_schema,
    querystring_schema,
)

from app.app import View
from app.store import (
    RedisAccessor,
    OrdersAccessor,
)
from .dcs import (
    CreateOrder,
    OrderDetails,
    UpdateOrder,
    DeleteOrder,
)
from .schemas import (
    OrderCreateRequestSchema,
    OrderCreateDataResponseSchema,
    OrderCreateResponseSchema,
    OrderUpdateRequestSchema,
    OrderUpdateResponseSchema, OrderDeleteResponseSchema, OrderDeleteRequestSchema
)
from ..app.utils import json_response


class OrdersView(View):
    @property
    def cache(self) -> RedisAccessor:
        return self.store.redis

    @property
    def orders(self) -> OrdersAccessor:
        return self.store.orders

    @docs(tags=["orders"], summary="Create", description="Create new order")
    @json_schema(OrderCreateRequestSchema)
    @response_schema(OrderCreateResponseSchema, 200)
    async def post(self):
        order_details_info: list[dict[int, int]] = self.data.pop('products')
        order_info = self.data

        employee_id = randint(1, 1000)
        order_number = randint(1, 99999)
        status = 1

        order_id = await self.orders.create(CreateOrder(
            **order_info,
            employee_id=employee_id,
            order_number=order_number,
            status=status,
            products=[OrderDetails(**item) for item in order_details_info]
        ))

        await self.cache.flush_all()

        return json_response(
            OrderCreateDataResponseSchema().load({
                'order_id': order_id,
                'order_number': order_number,
                'employee_id': employee_id,
                'status': status,
            })
        )

    @docs(tags=["orders"], summary="Update", description="Update order")
    @json_schema(OrderUpdateRequestSchema)
    @response_schema(OrderUpdateResponseSchema, 200)
    async def patch(self):
        order_id = await self.orders.update(
            UpdateOrder(**self.data)
        )

        if order_id is None:
            return json_response(OrderUpdateResponseSchema().load({'order_id': order_id}), status=404)

        await self.cache.flush_all()
        return json_response(OrderUpdateResponseSchema().load({'order_id': order_id}))

    @docs(tags=["orders"], summary="Delete", description="Delete order")
    @querystring_schema(OrderDeleteRequestSchema)
    @response_schema(OrderDeleteResponseSchema, 200)
    async def delete(self):
        order_id = await self.orders.delete(
            DeleteOrder(**self.query_data)
        )

        if order_id is None:
            return json_response(OrderDeleteResponseSchema().load({'order_id': order_id}), status=404)

        await self.cache.flush_all()
        return json_response(OrderDeleteResponseSchema().load({'order_id': order_id}))
