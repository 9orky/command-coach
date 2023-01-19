import contextvars

from .command import Command
from .error import CommandCoachPluginError
from .plugin import CommandCoachPlugin

import logging
logger = logging.getLogger('command_coach')


class LockingPlugin(CommandCoachPlugin):
    current_command = contextvars.ContextVar('current_command', default='')

    async def before_handle(self, command: Command):
        current = self.current_command.get()
        logger.debug(f'LockingMiddleware.before_handle: trying to run a {command.__class__.__name__}')

        if current:
            raise CommandCoachPluginError(f'LockingMiddleware is already handling a command: {current}')

        self.current_command.set(command.__class__.__name__)

    async def after_handle(self, command: Command):
        logger.debug(f'LockingMiddleware.after_handle: unlocking bus after {self.current_command.get()}')
        self.current_command.set('')


class LoggingPlugin(CommandCoachPlugin):
    async def before_handle(self, command: Command):
        logger.debug(f'LoggingMiddleware.before_handle: Command is about to be handled {command}')

    async def after_handle(self, command: Command):
        logger.debug(f'LoggingMiddleware.after_handle: Command {command} have been just handled')
