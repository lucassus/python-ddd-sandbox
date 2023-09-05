from dataclasses import dataclass
from typing import reveal_type

from app.sandbox.command_bus import Command, CommandBus, CommandHandler


@dataclass(frozen=True)
class DoSomething(Command[int]):
    foo: str
    bar: int


class DoSomethingHandler(CommandHandler[int, DoSomething]):
    def __call__(self, command: DoSomething) -> int:
        print(command)
        return 41


def test_command_bus() -> None:
    bus = CommandBus()
    bus.register(DoSomething, DoSomethingHandler())
    result = bus.execute(DoSomething(foo="foo", bar=1))
    reveal_type(result)
    assert result == 41
