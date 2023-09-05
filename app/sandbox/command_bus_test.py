from dataclasses import dataclass
from typing import reveal_type

from app.sandbox.command_bus import Command, CommandBus, CommandHandler


@dataclass(frozen=True)
class DoSomething(Command[int]):
    foo: str
    bar: int


@dataclass(frozen=True)
class DoSomethingElse(Command[str]):
    foo: str
    bar: int


class DoSomethingHandler(CommandHandler[DoSomething, int]):
    def __call__(self, command: DoSomething) -> int:
        return command.bar + 1


class DoSomethingElseHandler(CommandHandler[DoSomethingElse, str]):
    def __call__(self, command: DoSomethingElse) -> str:
        return command.foo.upper()


def test_command_bus() -> None:
    bus = CommandBus()

    bus.register(DoSomething, DoSomethingHandler())
    bus.register(DoSomethingElse, DoSomethingElseHandler())

    result_1 = bus.execute(DoSomething(foo="foo", bar=40))
    reveal_type(result_1)
    assert result_1 == 41

    result_2 = bus.execute(DoSomethingElse(foo="foo", bar=1))
    reveal_type(result_2)
    assert result_2 == "FOO"
