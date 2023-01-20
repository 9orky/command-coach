import contextvars
import logging

from .adapter import AsyncDatabase
from .command import Command
from .error import CommandCoachPluginError
from .plugin import CommandCoachPlugin


logger = logging.getLogger('command_coach')


class LockingPlugin(CommandCoachPlugin):
    current_command = contextvars.ContextVar('current_command', default='')

    async def before_handle(self, command: Command):
        current = self.current_command.get()
        logger.debug(f'LockingPlugin.before_handle: trying to run a {command.__class__.__name__}')

        if current:
            raise CommandCoachPluginError(f'LockingMiddleware is already handling a command: {current}')

        self.current_command.set(command.__class__.__name__)

    async def handle_failed(self):
        logger.error(f'LockingPlugin.handle_failed: unlocking bus after failed handle')
        self.current_command.set('')

    async def after_handle(self, command: Command):
        logger.debug(f'LockingPlugin.after_handle: unlocking bus after {self.current_command.get()}')
        self.current_command.set('')


class LoggingPlugin(CommandCoachPlugin):
    async def before_handle(self, command: Command):
        logger.debug(f'LoggingPlugin.before_handle: Command is about to be handled {command}')

    async def handle_failed(self):
        logger.error(f'LoggingPlugin.handle_failed: unlocking bus after failed handle')

    async def after_handle(self, command: Command):
        logger.debug(f'LoggingPlugin.after_handle: Command {command} have been just handled')


class TransactionPluginAsync(CommandCoachPlugin):
    def __init__(self, async_database: AsyncDatabase):
        self.database: AsyncDatabase = async_database

    async def before_handle(self, command: Command):
        await self.database.begin_transaction()

    async def handle_failed(self):
        await self.database.rollback_transaction()

    async def after_handle(self, command: Command):
        await self.database.commit_transaction()
