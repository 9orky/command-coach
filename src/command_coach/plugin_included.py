import logging
from time import time

from .adapter import DatabaseTransaction, DatabaseTransactionAsync
from .command import Command
from .plugin import CommandCoachPlugin, CommandCoachPluginAsync

logger = logging.getLogger('command_coach')


class LockingPlugin(CommandCoachPlugin):
    def before_handle(self, command: Command):
        logger.debug(f'LockingPlugin.before_handle: trying to run a {command.__class__.__name__}')

    def handle_failed(self):
        logger.error(f'LockingPlugin.handle_failed: unlocking bus after failed handle')

    def after_handle(self, command: Command):
        logger.debug(f'LockingPlugin.after_handle: unlocking bus after')


class LockingPluginAsync(CommandCoachPluginAsync):
    async def before_handle(self, command: Command):
        logger.debug(f'LockingPlugin.before_handle: trying to run a {command.__class__.__name__}')

    async def handle_failed(self):
        logger.error(f'LockingPlugin.handle_failed: unlocking bus after failed handle')

    async def after_handle(self, command: Command):
        logger.debug(f'LockingPlugin.after_handle: unlocking bus after')


class LoggingPlugin(CommandCoachPlugin):
    def before_handle(self, command: Command):
        logger.debug(f'LoggingPlugin.before_handle: Command is about to be handled {command}')

    def handle_failed(self):
        logger.error(f'LoggingPlugin.handle_failed: command failed')

    def after_handle(self, command: Command):
        logger.debug(f'LoggingPlugin.after_handle: Command {command} have been just handled')


class LoggingPluginAsync(CommandCoachPluginAsync):
    async def before_handle(self, command: Command):
        logger.debug(f'LoggingPlugin.before_handle: Command is about to be handled {command}')

    async def handle_failed(self):
        logger.error(f'LoggingPlugin.handle_failed: command failed')

    async def after_handle(self, command: Command):
        logger.debug(f'LoggingPlugin.after_handle: Command {command} have been just handled')


class TransactionPlugin(CommandCoachPlugin):
    def __init__(self, database: DatabaseTransaction):
        self.database: DatabaseTransaction = database

    def before_handle(self, command: Command):
        self.database.begin_transaction()

    def handle_failed(self):
        self.database.rollback_transaction()

    def after_handle(self, command: Command):
        self.database.commit_transaction()


class TransactionPluginAsync(CommandCoachPluginAsync):
    def __init__(self, async_database: DatabaseTransactionAsync):
        self.database: DatabaseTransactionAsync = async_database

    async def before_handle(self, command: Command):
        await self.database.begin_transaction()

    async def handle_failed(self):
        await self.database.rollback_transaction()

    async def after_handle(self, command: Command):
        await self.database.commit_transaction()


class ExecutionTimePlugin(CommandCoachPlugin):
    def before_handle(self, command: Command):
        logger.info(f'ExecutionTimePlugin.before_handle started at: {time()}')

    def handle_failed(self):
        ...

    def after_handle(self, command: Command):
        logger.info(f'ExecutionTimePlugin.after_handle finished at: {time()}')


class ExecutionTimePluginAsync(CommandCoachPluginAsync):
    async def before_handle(self, command: Command):
        logger.info(f'ExecutionTimePlugin.before_handle started at: {time()}')

    async def handle_failed(self):
        ...

    async def after_handle(self, command: Command):
        logger.info(f'ExecutionTimePlugin.after_handle finished at: {time()}')
