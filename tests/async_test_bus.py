import asyncio

from command_coach.bus import async_command_bus_maker, CommandCoachAsync
from run_test_command import AsyncTestCommand
from run_test_query import TestQueryAsync

test_bus: CommandCoachAsync = async_command_bus_maker([])
test_query_bus: CommandCoachAsync = async_command_bus_maker([])


async def main():
    command = AsyncTestCommand('test')
    await test_bus.handle(command)

    query_param = 'aye async'
    test_query = TestQueryAsync(property=query_param)
    result = await test_query_bus.handle(test_query)

    print(result, result == query_param)

asyncio.run(main())
