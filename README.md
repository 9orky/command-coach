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
touch display_invitation.py
```

Now open the file you have just created, and define command and respective handler.

```python
# display_invitation.py
from dataclasses import dataclass

@dataclass(frozen=True)
class AddProductToCartCommand(Command):
    cart_id: int
    customer_id: int
    product_id: int

```

In its simplest form, Command Coach can be used like this:
```python
from command_coach.bus import command_bus_maker

bus = command_bus_maker([])
```