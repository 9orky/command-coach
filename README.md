# Command Coach
Command Coach is an easy to use yet small **Command Bus** implementation for Python3. It has a pluggable architecture, 
so you can do whatever you want.

## Installation
To install Command Coach just type:
```shell
pip install commandcoach
```

## Usage
First, we need some command and handler. It is a good practice to keep them together in a `use-case` like module. Let's
create it.

```shell
touch display_greetings.py
```

Now open the file you have just created, and define command and respective handler.

```python
# display_greetings.py
from dataclasses import dataclass

from command_coach.command import Command, CommandHandler


@dataclass(frozen=True)
class DisplayGreetingsCommand(Command):
    greetings: str


class DisplayGreetingCommandHandler(CommandHandler):
    async def handle(self, command: DisplayGreetingsCommand):
        print(command.greetings)
```

This is all you have to do, now let's create a file, where we initiate the bus. In its simplest form, Command Coach can
be used like this:

```python
# command_bus.py
from command_coach.bus import command_bus_maker

from display_greetings import DisplayGreetingsCommand


bus = command_bus_maker([])
bus.handle(DisplayGreetingsCommand(greetings='Hello from Command Coach'))
```

It works of course, but it hasn't showed anything yet. The real power behind Command Coach is its pluggable 
architecture, which allows you to hook into command handling process. 

## Plugins
There are two plugins included:

* `LockingPlugin` responsible to lock the bus during command handling, so no other command can be dispatched from the
handler
* `LoggingPlugin` which logs command handling steps

Let's load them.

```python
# command_bus.py
from command_coach.bus import command_bus_maker
from command_coach.plugin_included import LoggingPlugin, LockingPlugin

from display_greetings import DisplayGreetingsCommand


bus = command_bus_maker([
    LockingPlugin(),
    LoggingPlugin(),
])

bus.handle(DisplayGreetingsCommand(greetings='Hello from Command Coach'))
```

And just before we go further, we need to take the closer look at the the base plugin class:

```python
from abc import ABC, abstractmethod

from command_coach.command import Command


class CommandCoachPlugin(ABC):
    @abstractmethod
    async def before_handle(self, command: Command):
        pass

    @abstractmethod
    async def after_handle(self, command: Command):
        pass
```

Basically, plugins have two methods:

* `before_handle()` which is called just before the command will be dispatched
* `after_handle()` which is called right after the handling process

The important fact here is that the ordering of the plugins **matters!** In the example above, in the `command_bus.py`
module, plugin methods will run in this order:

* `LockingPlugin.before_handle()`
  * `LoggingPlugin.before_handle()`
  * `LoggingPlugin.after_handle()`
* `LockingPlugin.after_handle()`

### Create Your Own Plugin
Making your own plugin is a piece of cake. Just create a class that inherits from `CommandCoachPlugin` and you're done.
For our purpouses, we will create a Execution Time plugin.

```python
# command_bus.py
from time import time

from command_coach.bus import command_bus_maker
from command_coach.command import Command
from command_coach.plugin import CommandCoachPlugin
from command_coach.plugin_included import LoggingPlugin, LockingPlugin


class ExecutionTimePlugin(CommandCoachPlugin):
    async def before_handle(self, command: Command):
        print(f'ExecutionTimeMiddleware.before_handle started at: {time()}')

    async def after_handle(self, command: Command):
        print(f'ExecutionTimeMiddleware.after_handle finished at: {time()}')


bus = command_bus_maker([
    LockingPlugin(),
    LoggingPlugin(),
    ExecutionTimePlugin(),
])
```

All you have to do, is to add your plugin during command bus creation. Happy using!