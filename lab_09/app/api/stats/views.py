from aiohttp_apispec import docs, response_schema, querystring_schema

from app.app import View
from app.api.app.utils import json_response
from app.store.redis import RedisAccessor
from app.store.restaurants import RestaurantsAccessor

from .schemas import (
    StatsRequestSchema,
    StatsListResponseSchema, StatsItemResponseSchema
)


class RestStatsView(View):
    @property
    def rests(self) -> RestaurantsAccessor:
        return self.store.restaurants

    @property
    def cache(self) -> RedisAccessor:
        return self.store.redis

    @docs(tags=["stats"], summary="Restaurant statistics", description="Get statistic of the all restaurants")
    @querystring_schema(StatsRequestSchema)
    @response_schema(StatsListResponseSchema, 200)
    async def get(self):
        if not self.query_data['cached']:
            fetched = await self.rests.fetch_stats()
        elif (cached_data := await self.cache.get(default=None)) is None:
            fetched = await self.rests.fetch_stats()
            await self.cache.set(value=fetched)
        else:
            fetched = cached_data

        return json_response(data=StatsItemResponseSchema(many=True).load(fetched))
