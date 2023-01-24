from dataclasses import dataclass

from command_coach.command import Command, CommandHandler


@dataclass
class TestCommand(Command):
    property: str


class TestCommandHandler(CommandHandler):
    def handle(self, command: TestCommand):
        print(f'{command.property}')


@dataclass
class AsyncTestCommand(Command):
    property: str


class AsyncTestCommandHandler(CommandHandler):
    async def handle(self, command: TestCommand):
        print(f'async {command.property}')
