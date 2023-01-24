from abc import ABC, abstractmethod

from command_coach.command import Command


class Query(Command):
    _q: bool = True


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query):
        ...


class QueryHandlerAsync(ABC):
    @abstractmethod
    async def handle(self, query: Query):
        ...
