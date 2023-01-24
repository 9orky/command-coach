from command_coach.bus import command_bus_maker, CommandCoach
from run_test_command import TestCommand

test_bus: CommandCoach = command_bus_maker([])

command = TestCommand('test')
test_bus.handle(command)
