import abc
from typing import Any, Generic, TypeVar, Type

R = TypeVar("R", contravariant=True)
C = TypeVar("C")


class Command(Generic[R]):
    pass


class CommandHandler(Generic[R, C]):
    @abc.abstractmethod
    def __call__(self, command: C) -> R:
        raise NotImplementedError


class CommandBus:
    _handlers: dict[type[Command[Any]], CommandHandler[Any, Command[Any]]]

    def __init__(self) -> None:
        self._handlers = {}

    def register(
        self,
        command_type: Type[Command[R]],
        handler: CommandHandler[R, Command[R]],
    ) -> None:
        self._handlers[command_type] = handler

    def execute(self, command: Command[R]) -> R:
        handler: CommandHandler[R, Command[R]] = self._handlers[type(command)]
        return handler(command)
