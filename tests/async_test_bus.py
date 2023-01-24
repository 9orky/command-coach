import asyncio

from command_coach.bus import async_command_bus_maker, CommandCoachAsync
from run_test_command import AsyncTestCommand

test_bus: CommandCoachAsync = async_command_bus_maker([])


async def main():
    command = AsyncTestCommand('test')
    await test_bus.handle(command)


asyncio.run(main())
