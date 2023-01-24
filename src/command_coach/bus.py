from importlib import import_module
from typing import List

from .command import Command
from .plugin import Plugins, CommandCoachPlugin, PluginsAsync, CommandCoachPluginAsync


def _instantiate_handler(command: Command):
    command_class_name = command.__class__.__name__
    module = import_module(command.__module__)

    handler_class = getattr(module, f'{command_class_name}Handler')
    return handler_class()


class CommandCoach:
    def __init__(self, plugins_collection: List[CommandCoachPlugin]):
        self._plugins = Plugins(plugins_collection)

    def handle(self, command: Command) -> None:
        handler = _instantiate_handler(command)

        self._plugins.before(command)

        try:
            result = handler.handle(command)
        except BaseException as e:
            self._plugins.failure()
            raise e

        self._plugins.after(command)

        if getattr(command, '_q', None):
            return result


class CommandCoachAsync:
    def __init__(self, plugins_collection: List[CommandCoachPluginAsync]):
        self._plugins = PluginsAsync(plugins_collection)

    async def handle(self, command: Command) -> None:
        handler = _instantiate_handler(command)

        await self._plugins.before(command)

        try:
            result = await handler.handle(command)
        except BaseException as e:
            await self._plugins.failure()
            raise e

        await self._plugins.after(command)

        if getattr(command, '_q', None):
            return result


def command_bus_maker(plugins: List[CommandCoachPlugin]) -> CommandCoach:
    return CommandCoach(plugins)


def async_command_bus_maker(plugins: List[CommandCoachPluginAsync]) -> CommandCoachAsync:
    return CommandCoachAsync(plugins)
