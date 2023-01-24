from command_coach.bus import command_bus_maker, CommandCoach
from run_test_command import TestCommand
from run_test_query import TestQuery

test_bus: CommandCoach = command_bus_maker([])

command = TestCommand('test')
test_bus.handle(command)

test_query_bus: CommandCoach = command_bus_maker([])

query_param = 'aye'
test_query = TestQuery(property=query_param)
result = test_query_bus.handle(test_query)

print(result, result == query_param)
