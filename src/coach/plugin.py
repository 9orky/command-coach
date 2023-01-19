from abc import ABC, abstractmethod
from typing import List

from .command import Command


class CommandCoachPlugin(ABC):
    @abstractmethod
    async def before_handle(self, command: Command):
        pass

    @abstractmethod
    async def after_handle(self, command: Command):
        pass


class Plugin:
    def __init__(self, found: List[CommandCoachPlugin]):
        self.found = found

    def __call__(self, *args, **kwargs):
        self.found.append(args[0]())

    async def before(self, command: Command):
        for m in self.found:
            await m.before_handle(command)

    async def after(self, command: Command):
        reversed_found = list(reversed(self.found))
        for m in reversed_found:
            await m.after_handle(command)
