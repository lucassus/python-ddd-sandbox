from dataclasses import dataclass

from sandbox.command_bus.command_bus import Command, CommandBus, CommandHandler


@dataclass(frozen=True)
class DoSomething(Command):
    foo: str
    bar: int


class DoSomethingHandler(CommandHandler[DoSomething]):
    def __call__(self, command: DoSomething) -> None:
        print(command)


def test_command_bus() -> None:
    bus = CommandBus()
    bus.register(DoSomething, DoSomethingHandler())
    bus.execute(DoSomething(foo="foo", bar=1))
