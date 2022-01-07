from app.config import Config
from app.databases import Databases

from app.store.redis import RedisAccessor
from app.store.orders import OrdersAccessor
from app.store.restaurants import RestaurantsAccessor


class Store:
    def __init__(self, dbs: Databases, cfg: Config):
        from app.store.orders import OrdersAccessor
        from app.store.redis import RedisAccessor
        from app.store.restaurants import RestaurantsAccessor

        self.orders = OrdersAccessor(dbs, cfg, self)
        self.redis = RedisAccessor(dbs, cfg, self)
        self.restaurants = RestaurantsAccessor(dbs, cfg, self)


def setup_store(dbs: Databases, cfg: Config) -> Store:
    return Store(dbs, cfg)
