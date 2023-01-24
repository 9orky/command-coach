from abc import ABC, abstractmethod


class Command:
    pass


class CommandHandler(ABC):
    @abstractmethod
    def handle(self, command: Command):
        ...


class CommandHandlerAsync(ABC):
    @abstractmethod
    async def handle(self, command: Command):
        ...
