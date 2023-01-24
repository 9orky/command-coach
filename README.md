# Command Coach
Command Coach is small, yet powerful **Command Bus** implementation for Python. It has a pluggable architecture, 
so you can do whatever you want.

## Why use it?
* suitable for both **sync** and **async** applications
* plugable architecture
* some **plugins already provided** for the most popular use cases

## Installation
To install Command Coach just type:

```shell
pip install commandcoach
```

## Usage
First, we need some **Command** and **Handler**. It is a good practice to keep them together in a `use case` like 
module. Let's create it.

```shell
touch display_greetings.py
```

Now open the file you have just created, and define command and its respective handler.

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

Another module we need is one for command bus itself.

```shell
touch command_bus.py
```

This is **all** you have to do, now let's create a file, where we are going to initiate the **bus**. In its 
simplest form, **Command Coach** can be used like this:

```python
# command_bus.py

from command_coach.bus import command_bus_maker

from display_greetings import DisplayGreetingsCommand


bus = command_bus_maker([])

bus.handle(DisplayGreetingsCommand(greetings='Hello from Command Coach'))
```

It works of course, but it hasn't showed anything yet. The real power of Command Coach lies in its pluggable 
architecture, which allows you to hook in to a command handling process. 

## Plugins
There are already some plugins available for you out of the box. You may use Command Coach without any plugins at all.

### LockingPlugin
* locks nad unlocks bus during command handling
* when locked then no other command can be handled

### LoggingPlugin
* logs what currently happens
* may provide useful info

### ExecutionTimePlugin
* tells you how long given command was handled

Example of usage:

```python
# command_bus.py

from command_coach.adapter import DatabaseTransactionAsync
from command_coach.bus import command_bus_maker
from command_coach.plugin_included import LoggingPlugin, LockingPlugin, ExecutionTimePlugin

from display_greetings import DisplayGreetingsCommand

bus = command_bus_maker([
  LockingPlugin(),
  LoggingPlugin(),
  ExecutionTimePlugin(),
])

bus.handle(DisplayGreetingsCommand(greetings='Hello from Command Coach'))
```

The important fact here is that the ordering of the plugins **matters!** In the example above, in the `command_bus.py`
module, plugin methods will run in this order:

* `LockingPlugin.before_handle()`
  * `LoggingPlugin.before_handle()`
    * `ExecutionTimePlugin.before_handle()`
    * `ExecutionTimePlugin.after_handle()`
  * `LoggingPlugin.after_handle()`
* `LockingPlugin.after_handle()`

### TransactionPluginAsync
* wraps command handling around database transaction
* provides simple adapter for engine abstraction

This is how you may deal with it:
```python
# command_bus.py

from command_coach.bus import command_bus_maker
from command_coach.plugin_included import TransactionPluginAsync

from my_database import my_db_instance
from display_greetings import DisplayGreetingsCommand


class DatabaseAdapter(AsyncDatabase):
    def __init__(self, db):
        self._db = db

    async def begin_transaction(self):
        await self._db.begin()

    async def commit_transaction(self):
        await self._db.commit()

    async def rollback_transaction(self):
        await self._db.rollback()

        
bus = command_bus_maker([
    TransactionPluginAsync(DatabaseAdapter(my_db_instance)),
])

bus.handle(DisplayGreetingsCommand(greetings='Hello from Command Coach'))
```

### Create Your Own Plugin
Just before we go further, we need to take the closer look at the base plugin class:

```python
class CommandCoachPlugin(ABC):
    @abstractmethod
    async def before_handle(self, command: Command):
        pass

    @abstractmethod
    async def handle_failed(self):
        pass
    
    @abstractmethod
    async def after_handle(self, command: Command):
        pass
```

Basically, plugin must contain these methods:

* `before_handle()` will be called just before running **Command Handler**
* `handle_failed()` called when Command Handler raised an **Exception**
* `after_handle()` is fired right after the handling process

Making your own plugin is a piece of cake. Just create a class that inherits from `CommandCoachPlugin` and you're done.
For our purposes, we will create a `JokesInLogsPlugin`.

```python
# command_bus.py

from command_coach.bus import command_bus_maker
from command_coach.command import Command
from command_coach.plugin import CommandCoachPlugin
from command_coach.plugin_included import LoggingPlugin


class JokesInLogsPlugin(CommandCoachPlugin):
    def __init(self, logger):
      self._logger = logger
      
    async def before_handle(self, command: Command):
        self._logger.log('Chuck Norris counted to infinity... twice.')

    async def handle_failed(self):
        self._logger.log('No worries, Chuck Norris can build a snowman out of rain.')
        
    async def after_handle(self, command: Command):
        self._logger.log('The chief export of Chuck Norris is pain.')


bus = command_bus_maker([
    LoggingPlugin(),
    JokesInLogsPlugin(),
])
```

All you have to do, is to add your plugin during command bus creation. Happy using!