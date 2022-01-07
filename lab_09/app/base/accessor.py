from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

from app.config import Config
from app.databases import Databases

if TYPE_CHECKING:
    from app.store import Store


class BaseAccessor(metaclass=ABCMeta):
    def __init__(self, databases: Databases, config: Config, store: 'Store'):
        self.databases = databases
        self.config = config
        self.store = store

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass
