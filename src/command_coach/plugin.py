from abc import ABC, abstractmethod
from typing import List

from .command import Command


class CommandCoachPlugin(ABC):
    @abstractmethod
    def before_handle(self, command: Command):
        ...

    @abstractmethod
    def handle_failed(self):
        ...

    @abstractmethod
    def after_handle(self, command: Command):
        ...


class CommandCoachPluginAsync(ABC):
    @abstractmethod
    async def before_handle(self, command: Command):
        ...

    @abstractmethod
    async def handle_failed(self):
        ...

    @abstractmethod
    async def after_handle(self, command: Command):
        ...


class Plugins:
    def __init__(self, installed_plugins: List[CommandCoachPlugin]):
        self.installed = installed_plugins

    def before(self, command: Command):
        for plugin in self.installed:
            plugin.before_handle(command)

    def failure(self):
        for plugin in self.installed:
            plugin.handle_failed()

    def after(self, command: Command):
        reversed_order = list(reversed(self.installed))
        for plugin in reversed_order:
            plugin.after_handle(command)


class PluginsAsync:
    def __init__(self, installed_plugins: List[CommandCoachPluginAsync]):
        self.installed = installed_plugins

    async def before(self, command: Command):
        for plugin in self.installed:
            await plugin.before_handle(command)

    async def failure(self):
        for plugin in self.installed:
            await plugin.handle_failed()

    async def after(self, command: Command):
        reversed_order = list(reversed(self.installed))
        for plugin in reversed_order:
            await plugin.after_handle(command)
