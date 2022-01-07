from aiohttp_apispec import setup_aiohttp_apispec
from typing import Optional

from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView
)
from multidict import MultiDictProxy

from .api.app.routes import setup_routes
from .api.app.middlewares import setup_middlewares

from app.config import Config, setup_config
from app.databases import Databases, setup_databases
from app.store import setup_store, Store


class Application(AiohttpApplication):
    config: Optional[Config]
    store: Optional[Store]
    databases: Optional[Databases]


class Request(AiohttpRequest):
    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get('json', {})

    @property
    def query_data(self) -> MultiDictProxy[str]:
        return self.request.get('querystring', {})


app = Application()


def setup_app(config_path: str) -> Application:
    app.config = setup_config(config_path)

    setup_routes(app)
    setup_middlewares(app)
    setup_aiohttp_apispec(app, title='lab9', url='/docs/json', swagger_path='/docs')

    app.databases = setup_databases(app.config)
    app.store = setup_store(app.databases, app.config)

    app.on_startup.append(app.databases.connect)
    app.on_cleanup.append(app.databases.disconnect)

    return app
